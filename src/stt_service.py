"""Production STT service with health monitoring and error handling"""
from whisper_nxd import WhisperNxD
from pathlib import Path
import logging
import time
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class STTService:
    """Production-ready STT service with monitoring and health checks"""

    def __init__(self, compiled_model_path, base_model_path, language="hi"):
        """
        Initialize STT service.

        Args:
            compiled_model_path: Path to compiled Neuron model
            base_model_path: Path to HuggingFace base model
            language: Input language code (hi, en, etc.)
        """
        self.compiled_path = compiled_model_path
        self.base_path = base_model_path
        self.language = language
        self.model = None
        self.is_ready = False
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_processing_time': 0,
            'total_audio_duration': 0
        }

    def initialize(self):
        """Initialize service and load model onto NeuronCores"""
        logger.info("Initializing STT service...")

        try:
            self.model = WhisperNxD(
                model_path=self.base_path,
                compiled_path=self.compiled_path,
                tp_degree=2,
                language=self.language
            )

            logger.info("Loading model onto NeuronCores...")
            self.model.load()

            # Warmup
            logger.info("Running warmup...")
            self._warmup()

            self.is_ready = True
            logger.info("✓ Service ready for inference")

        except Exception as e:
            logger.error(f"Failed to initialize service: {e}")
            raise

    def _warmup(self):
        """Warmup the model with dummy audio"""
        import numpy as np
        import soundfile as sf

        # Create 5-second dummy audio
        dummy_audio = np.random.randn(16000 * 5).astype(np.float32) * 0.001
        warmup_file = "/tmp/warmup.wav"
        sf.write(warmup_file, dummy_audio, 16000)

        # Run 2 warmup iterations
        for i in range(2):
            try:
                self.model.transcribe(warmup_file)
                logger.info(f"  Warmup iteration {i+1}/2 complete")
            except Exception as e:
                logger.warning(f"Warmup iteration {i+1} failed: {e}")

    def transcribe(self, audio_file):
        """
        Transcribe audio file.

        Args:
            audio_file: Path to audio file

        Returns:
            dict: {
                'success': bool,
                'text': str,
                'duration': float,
                'processing_time': float,
                'rtf': float,
                'error': str (if failed)
            }
        """
        if not self.is_ready:
            return {
                'success': False,
                'error': 'Service not initialized. Call initialize() first.'
            }

        self.stats['total_requests'] += 1

        try:
            start = time.time()
            result = self.model.transcribe(audio_file)
            elapsed = time.time() - start

            # Update stats
            self.stats['successful_requests'] += 1
            self.stats['total_processing_time'] += elapsed
            self.stats['total_audio_duration'] += result['duration']

            logger.info(
                f"Transcribed {Path(audio_file).name} "
                f"({result['duration']:.2f}s) in {elapsed:.3f}s "
                f"(RTF: {elapsed/result['duration']:.4f}x)"
            )

            return {
                'success': True,
                'text': result['text'],
                'duration': result['duration'],
                'processing_time': elapsed,
                'rtf': elapsed / result['duration']
            }

        except Exception as e:
            self.stats['failed_requests'] += 1
            logger.error(f"Transcription failed for {audio_file}: {e}")

            return {
                'success': False,
                'error': str(e)
            }

    def health_check(self):
        """
        Check service health.

        Returns:
            dict: Health status and statistics
        """
        avg_processing_time = (
            self.stats['total_processing_time'] / self.stats['successful_requests']
            if self.stats['successful_requests'] > 0 else 0
        )

        avg_rtf = (
            self.stats['total_processing_time'] / self.stats['total_audio_duration']
            if self.stats['total_audio_duration'] > 0 else 0
        )

        return {
            'status': 'healthy' if self.is_ready else 'unhealthy',
            'ready': self.is_ready,
            'statistics': {
                'total_requests': self.stats['total_requests'],
                'successful_requests': self.stats['successful_requests'],
                'failed_requests': self.stats['failed_requests'],
                'success_rate': (
                    self.stats['successful_requests'] / self.stats['total_requests'] * 100
                    if self.stats['total_requests'] > 0 else 0
                ),
                'avg_processing_time': avg_processing_time,
                'avg_rtf': avg_rtf,
                'total_audio_processed': self.stats['total_audio_duration']
            }
        }

    def get_stats(self):
        """Get service statistics"""
        return self.stats.copy()


# Example usage
if __name__ == "__main__":
    # Initialize service
    service = STTService(
        compiled_model_path="models/whisper-hindi2hinglish-swift-compiled-tp2",
        base_model_path="models/whisper-hindi2hinglish-swift",
        language="hi"
    )

    service.initialize()

    # Health check
    health = service.health_check()
    print(json.dumps(health, indent=2))

    # Example transcription
    import sys
    if len(sys.argv) > 1:
        result = service.transcribe(sys.argv[1])
        print(json.dumps(result, indent=2))
