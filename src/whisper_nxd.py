"""Whisper with NeuronX Distributed Inference"""
import torch
import soundfile as sf
import numpy as np
import scipy.signal
from pathlib import Path
from transformers import AutoProcessor

from neuronx_distributed_inference.models.config import NeuronConfig
from neuronx_distributed_inference.models.whisper.modeling_whisper import (
    WhisperInferenceConfig,
    NeuronApplicationWhisper,
)
from neuronx_distributed_inference.utils.hf_adapter import load_pretrained_config


class WhisperNxD:
    """Whisper model optimized for AWS Trainium/Inferentia"""
    
    def __init__(self, model_path, compiled_path, tp_degree=2, language="hi"):
        """
        Initialize Whisper NxD model.
        
        Args:
            model_path: Path to HuggingFace model directory
            compiled_path: Path to save/load compiled model
            tp_degree: Tensor parallelism degree (2 for trn1.2xlarge)
            language: Input language code (hi=Hindi, en=English, ja=Japanese)
        """
        self.model_path = Path(model_path)
        self.compiled_path = Path(compiled_path)
        self.tp_degree = tp_degree
        self.language = language
        self.model = None
        self.processor = None

    def compile(self):
        """Compile the model for Neuron hardware."""
        if self.compiled_path.exists():
            print(f"✓ Compiled model found at {self.compiled_path}")
            print("  Skipping compilation (delete directory to recompile)")
            return

        print(f"Compiling Whisper model for Trainium...")
        print(f"  Source: {self.model_path}")
        print(f"  Target: {self.compiled_path}")
        print(f"  TP Degree: {self.tp_degree}")
        print(f"  Language: {self.language}")
        print("\nThis will take 10-15 minutes...")

        # Configure for compilation
        config = WhisperInferenceConfig(
            NeuronConfig(
                batch_size=1,              # Optimal for latency
                torch_dtype=torch.float16, # FP16 for speed/accuracy balance
                tp_degree=self.tp_degree   # 2 cores on trn1.2xlarge
            ),
            load_config=load_pretrained_config(str(self.model_path)),
        )

        # Compile model
        self.model = NeuronApplicationWhisper(str(self.model_path), config=config)
        self.compiled_path.mkdir(parents=True, exist_ok=True)
        self.model.compile(str(self.compiled_path))
        
        print("\n✓ Compilation complete")
        print(f"  Compiled artifacts saved to: {self.compiled_path}")

    def load(self):
        """Load the compiled model onto NeuronCores."""
        if not self.compiled_path.exists():
            raise FileNotFoundError(
                f"Compiled model not found at {self.compiled_path}. "
                f"Run compile() first."
            )

        print("Loading compiled model onto NeuronCores...")
        
        # Load processor
        self.processor = AutoProcessor.from_pretrained(str(self.model_path))
        
        # Configure for inference
        config = WhisperInferenceConfig(
            NeuronConfig(
                batch_size=1,
                torch_dtype=torch.float16,
                tp_degree=self.tp_degree
            ),
            load_config=load_pretrained_config(str(self.model_path)),
        )

        # Load onto NeuronCores
        self.model = NeuronApplicationWhisper(str(self.compiled_path), config=config)
        self.model.load(str(self.compiled_path))
        
        print("✓ Model loaded and ready for inference")

    def transcribe(self, audio_path):
        """
        Transcribe an audio file.
        
        Args:
            audio_path: Path to audio file (supports mp3, wav, flac, etc.)
            
        Returns:
            dict: {'text': transcription, 'duration': audio_duration_seconds}
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load() first.")
        
        # Load audio file
        audio_data, sr = sf.read(audio_path)

        # Resample to 16kHz if needed (Whisper requirement)
        if sr != 16000:
            audio_data = scipy.signal.resample_poly(
                audio_data, 16000, sr
            ).astype(np.float32)

        # Convert stereo to mono if needed
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)

        # Ensure float32 dtype
        audio_data = audio_data.astype(np.float32)
        audio_duration = len(audio_data) / 16000

        # Run transcription on NeuronCores
        result = self.model.transcribe(
            audio_data,
            language=self.language,
            verbose=False
        )

        return {
            'text': result['text'].strip(),
            'duration': audio_duration
        }
