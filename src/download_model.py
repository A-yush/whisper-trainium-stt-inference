"""Download Whisper Hindi2Hinglish model from HuggingFace"""
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from pathlib import Path
import sys

model_id = "Oriserve/Whisper-Hindi2Hinglish-Swift"
save_dir = "models/whisper-hindi2hinglish-swift"

print(f"Downloading model: {model_id}")
print("This may take several minutes depending on network speed...")

try:
    # Download model
    print("\n[1/2] Downloading model weights...")
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, 
        low_cpu_mem_usage=True,
        trust_remote_code=False
    )
    model.save_pretrained(save_dir)
    print("✓ Model weights saved")
    
    # Download processor (tokenizer, feature extractor)
    print("\n[2/2] Downloading processor...")
    processor = AutoProcessor.from_pretrained(model_id)
    processor.save_pretrained(save_dir)
    print("✓ Processor saved")
    
    print(f"\n✓ Download complete → {save_dir}")
    
    # Calculate model size
    model_path = Path(save_dir)
    total_size = sum(f.stat().st_size for f in model_path.rglob('*') if f.is_file())
    print(f"  Model size: ~{total_size / (1024**3):.2f} GB")
    
except Exception as e:
    print(f"\n✗ Error downloading model: {e}", file=sys.stderr)
    sys.exit(1)
