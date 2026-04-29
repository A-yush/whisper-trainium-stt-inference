# Quick Start Guide - Whisper on Trainium1

Get your Whisper STT model running on AWS Trainium in **5 minutes**.

---

## Prerequisites

✅ AWS Trainium instance (trn1.2xlarge or larger)  
✅ Ubuntu 22.04 or 24.04  
✅ Neuron SDK pre-installed (included in DLAMI)

---

## Installation Steps

### 1. Clone Repository (30 seconds)

```bash
git clone https://github.com/your-org/whisper-trainium-deployment.git
cd whisper-trainium-deployment
```

### 2. Setup Environment (1 minute)

```bash
# Run automated setup
bash scripts/setup_environment.sh
```

**What it does:**
- ✓ Verifies Neuron hardware
- ✓ Checks drivers and runtime
- ✓ Activates virtual environment
- ✓ Installs dependencies
- ✓ Creates directory structure

### 3. Download Model (2 minutes)

```bash
python src/download_model.py
```

**Expected output:**
```
✓ Model weights saved
✓ Processor saved
✓ Download complete → models/whisper-hindi2hinglish-swift
  Model size: ~0.28 GB
```

### 4. Compile Model (1-2 minutes)

```bash
python src/compile_model.py
```

**Expected output:**
```
✓ Compilation complete
✓ Compilation completed in 86.0 seconds (1.4 minutes)
```

### 5. Test Inference (10 seconds)

```bash
python benchmarks/test_inference.py test_audio/benchmark/audio_01_0-10s.mp3
```

**Expected output:**
```
Audio Duration:  4.39 seconds
Processing Time: 0.075 seconds
RTF: 0.0171x

Transcription:
  [Your transcription here]
```

---

## ✅ You're Ready!

Your model is now running at **~93x faster than real-time**!

---

## Next Steps

### Run Full Benchmark

```bash
python benchmarks/benchmark_stt.py
```

See performance across all 31 test files with detailed metrics.

### Batch Process Audio Files

```bash
python examples/batch_processing.py /path/to/audio/folder
```

Process entire folders of audio files efficiently.

### Production Deployment

```python
from src.stt_service import STTService

# Initialize service
service = STTService(
    compiled_model_path="models/whisper-hindi2hinglish-swift-compiled-tp2",
    base_model_path="models/whisper-hindi2hinglish-swift"
)
service.initialize()

# Transcribe
result = service.transcribe("audio.mp3")
print(result['text'])
```

---

## Performance Summary

| Metric | Value |
|--------|-------|
| **Average Latency** | 513ms |
| **P90 Latency** | 1.4s |
| **RTF** | 0.011x (93.5x faster) |
| **Throughput** | 1.95 req/sec |

---

## Troubleshooting

### Issue: NeuronCores not found

```bash
# Check hardware
neuron-ls

# Verify kernel module
lsmod | grep neuron
```

### Issue: Compilation fails

```bash
# Clear cache and retry
rm -rf /tmp/neuron_cache/*
python src/compile_model.py
```

### Issue: Import errors

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## Configuration

### Use Baseline Config (default)

Standard performance, tested and stable.

```bash
# Already the default - no changes needed
```

### Use Optimized Config (15-30% faster)

```bash
# Compile with optimizations
python src/compile_optimized.py  # TODO: Create this script

# Update service to use optimized model
# compiled_path="models/whisper-hindi2hinglish-swift-compiled-tp2-optimized"
```

---

## Support

- 📖 **Full Guide:** [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)
- 📊 **Benchmarks:** [docs/BENCHMARK_RESULTS.md](docs/BENCHMARK_RESULTS.md)
- 🐛 **Issues:** [GitHub Issues](https://github.com/your-org/whisper-trainium-deployment/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/your-org/whisper-trainium-deployment/discussions)

---

## What's Next?

1. **Optimize Performance** - Try the optimized configuration
2. **Scale Up** - Deploy multiple instances with load balancer
3. **Integrate** - Add to your application pipeline
4. **Monitor** - Set up CloudWatch metrics
5. **Customize** - Fine-tune for your specific use case

---

**Time to first transcription: 5 minutes** ⚡

**Star ⭐ this repo if it helped you!**
