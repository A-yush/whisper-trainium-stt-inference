"""Compile Whisper model for Trainium"""
from whisper_nxd import WhisperNxD
import time
import sys

print("=" * 80)
print("Whisper Model Compilation for AWS Trainium1")
print("=" * 80)

# Configuration
model_path = "models/whisper-hindi2hinglish-swift"
compiled_path = "models/whisper-hindi2hinglish-swift-compiled-tp2"
tp_degree = 2  # trn1.2xlarge has 2 NeuronCores
language = "hi"  # Hindi input → Hinglish output

print(f"\nConfiguration:")
print(f"  Model: {model_path}")
print(f"  Output: {compiled_path}")
print(f"  TP Degree: {tp_degree}")
print(f"  Language: {language}")
print()

try:
    # Initialize model
    model = WhisperNxD(
        model_path=model_path,
        compiled_path=compiled_path,
        tp_degree=tp_degree,
        language=language
    )
    
    # Compile
    start = time.time()
    model.compile()
    elapsed = time.time() - start
    
    print(f"\n✓ Compilation completed in {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
    print(f"  Compiled model ready at: {compiled_path}")
    
except Exception as e:
    print(f"\n✗ Compilation failed: {e}", file=sys.stderr)
    sys.exit(1)
