"""Test Whisper STT inference"""
import time
from whisper_nxd import WhisperNxD
import sys
from pathlib import Path

def test_inference(audio_file, language="hi"):
    """Run inference on a single audio file"""
    
    # Initialize model
    model = WhisperNxD(
        model_path="models/whisper-hindi2hinglish-swift",
        compiled_path="models/whisper-hindi2hinglish-swift-compiled-tp2",
        tp_degree=2,
        language=language
    )
    
    # Load compiled model onto NeuronCores
    print("Loading model...")
    model.load()
    
    # Run transcription
    print(f"\nTranscribing: {audio_file}")
    start = time.time()
    result = model.transcribe(audio_file)
    elapsed = time.time() - start
    
    # Display results
    print("\n" + "=" * 80)
    print("INFERENCE RESULTS")
    print("=" * 80)
    print(f"Audio File:      {audio_file}")
    print(f"Audio Duration:  {result['duration']:.2f} seconds")
    print(f"Processing Time: {elapsed:.3f} seconds")
    print(f"RTF (Real-Time Factor): {elapsed/result['duration']:.4f}x")
    print(f"\nTranscription:")
    print(f"  {result['text']}")
    print("=" * 80)
    
    return result, elapsed

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_inference.py <audio_file> [language]")
        print("Example: python test_inference.py test_audio/sample.mp3 hi")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "hi"
    
    if not Path(audio_file).exists():
        print(f"Error: Audio file not found: {audio_file}")
        sys.exit(1)
    
    test_inference(audio_file, language)
