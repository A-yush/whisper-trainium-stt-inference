# Whisper STT on AWS Trainium1 - Complete Deployment Solution

## GitHub Repository: `whisper-trainium-deployment`

**Complete end-to-end solution for deploying HuggingFace Whisper STT models on AWS Trainium1 instances with production-ready performance.**

---

## 🎯 Repository Overview

This repository provides a **production-ready deployment pipeline** for running OpenAI Whisper-based Speech-to-Text (STT) models on AWS Trainium1 hardware using NeuronX Distributed Inference. The solution is optimized for **low latency, high throughput, and cost-effective** transcription at scale.

### What's Included

✅ **Complete Deployment Guide** - Step-by-step instructions from environment setup to production  
✅ **Ready-to-Use Code** - Wrapper classes, compilation scripts, and inference services  
✅ **Comprehensive Benchmarking** - Duration-based analysis with P50/P90/P99 metrics  
✅ **Performance Optimization** - 15-30% latency reduction techniques  
✅ **Production Templates** - Service wrappers, monitoring, and health checks  
✅ **Real Benchmark Data** - Tested on 31 audio files (4s - 171s duration)

---

## 📊 Benchmark Results

**Model:** Oriserve/Whisper-Hindi2Hinglish-Swift (Whisper Base)  
**Hardware:** AWS Trainium1 (trn1.2xlarge) - 2 NeuronCores  
**Total Audio Files:** 31 (21 original + 10 AWS speech files)

### Overall Performance

| Metric | Value |
|--------|-------|
| **Total Files Processed** | 31 |
| **Total Audio Duration** | 1,551.9 seconds (~25.9 minutes) |
| **Total Processing Time** | 15.9 seconds |
| **Average Processing Time** | 513.1ms |
| **P50 Processing Time** | 153.2ms |
| **P90 Processing Time** | 1,417.2ms |
| **P99 Processing Time** | 3,200.4ms |
| **Average RTF** | 0.011x |
| **Throughput** | 1.95 requests/second |
| **Speed vs Real-time** | 93.5x faster |

### Performance by Duration Range

| Duration Range | Files | Avg Audio Duration | Avg Processing | P90 Processing | P99 Processing | Avg RTF |
|----------------|-------|-------------------|----------------|----------------|----------------|---------|
| **0-10s**      | 5     | 5.00s             | 75.4ms         | 78.3ms         | 79.2ms         | 0.015x  |
| **10-30s**     | 15    | 17.21s            | 170.0ms        | 237.2ms        | 398.6ms        | 0.010x  |
| **30-60s**     | 3     | 55.13s            | 484.6ms        | 645.4ms        | 702.6ms        | 0.009x  |
| **60s+**       | 8     | 137.93s           | 1,440.8ms      | 2,201.3ms      | 3,774.9ms      | 0.010x  |

### Key Insights

✅ **93.5x faster than real-time** processing  
✅ **Sub-second latency** for most audio lengths  
✅ **Consistent RTF** across duration ranges (~0.010x)  
✅ **P99 latency under 4 seconds** even for 171-second audio  
✅ **1.95 requests/second** throughput on single instance

**Full benchmark details:** See [docs/BENCHMARK_RESULTS.md](docs/BENCHMARK_RESULTS.md)

---

## 🚀 Quick Start

### Prerequisites

- AWS account with access to Trainium instances
- EC2 instance: `trn1.2xlarge` or larger
- OS: Ubuntu 22.04 or 24.04
- AWS Neuron SDK pre-installed (included in DLAMI)

### Installation (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/your-org/whisper-trainium-deployment.git
cd whisper-trainium-deployment

# 2. Run automated setup (verifies environment and installs dependencies)
bash scripts/setup_environment.sh

# 3. Download the model
python src/download_model.py

# 4. Compile for Trainium (1-2 minutes)
python src/compile_model.py

# 5. Run test inference
python benchmarks/test_inference.py test_audio/benchmark/audio_01_0-10s.mp3
```

**Result:** Your first STT transcription in under 200ms!

**For detailed step-by-step instructions, see [DEPLOYMENT_GUIDE_REPO.md](docs/DEPLOYMENT_GUIDE_REPO.md)**

---

## 📁 Repository Structure

```
whisper-trainium-deployment/
├── README.md                           # This file - Getting started guide
├── QUICK_START.md                      # 5-minute quick start guide
├── LICENSE                             # MIT License
├── requirements.txt                    # Python dependencies
│
├── src/                               # Source code
│   ├── whisper_nxd.py                # Main Whisper NxD wrapper class
│   ├── download_model.py             # HuggingFace model downloader
│   ├── compile_model.py              # Trainium compilation script
│   └── stt_service.py                # Production service wrapper
│
├── benchmarks/                        # Benchmarking tools
│   ├── benchmark_stt.py              # Comprehensive benchmark tool
│   └── test_inference.py             # Single-file testing
│
├── scripts/                          # Automation scripts
│   ├── setup_environment.sh          # Environment setup & verification
│   └── monitor_service.sh            # Health monitoring
│
├── configs/                          # Configuration files
│   ├── baseline_config.yaml          # Standard configuration
│   └── optimized_config.yaml         # Performance-optimized config
│
├── docs/                             # Documentation
│   ├── DEPLOYMENT_GUIDE_REPO.md      # Complete step-by-step deployment guide
│   ├── DEPLOYMENT_GUIDE.md           # Original detailed guide
│   └── BENCHMARK_RESULTS.md          # Detailed performance analysis
│
├── examples/                         # Usage examples
│   └── batch_processing.py           # Batch transcription example
│
├── test_audio/                       # Test audio files
│   ├── en_aws_tranium_250words.mp3  # English sample
│   └── benchmark/                    # 30 benchmark files (4s - 171s)
│       ├── audio_01-05_0-10s.mp3    # Short audio samples
│       ├── audio_21-30_0-10s.mp3    # AWS service descriptions
│       └── ...
│
└── models/                           # Model storage (excluded from git)
    ├── whisper-hindi2hinglish-swift/         # Base model (283 MB)
    └── whisper-hindi2hinglish-swift-compiled-tp2/  # Compiled artifacts
```

---

## 🎓 Deployment Phases

**See [DEPLOYMENT_GUIDE_REPO.md](docs/DEPLOYMENT_GUIDE_REPO.md) for complete step-by-step instructions**

### Phase 1: Environment Setup (5 minutes)
```bash
bash scripts/setup_environment.sh
```
- Verifies Neuron hardware and drivers
- Activates virtual environment
- Installs Python dependencies
- Validates environment compatibility

### Phase 2: Model Download (2-3 minutes)
```bash
python src/download_model.py
```
- Downloads from HuggingFace: `Oriserve/Whisper-Hindi2Hinglish-Swift`
- Size: 283 MB (Whisper Base, 74M parameters)
- Includes: Model weights, tokenizer, processor

### Phase 3: Model Compilation (1-2 minutes)
```bash
python src/compile_model.py
```
- Compiles model for Trainium NeuronCores
- Configuration: TP degree = 2, FP16 precision
- Output: Neuron-optimized artifacts (~900 MB)
- One-time compilation (cached for reuse)

### Phase 4: Testing & Validation (5 minutes)
```bash
# Single file test
python benchmarks/test_inference.py test_audio/benchmark/audio_01_0-10s.mp3

# Full benchmark (31 files)
python benchmarks/benchmark_stt.py
```
- Single-file inference testing
- Comprehensive benchmarking (31 files)
- Performance metrics collection
- Duration-based analysis (0-10s, 10-30s, 30-60s, 60s+)

### Phase 5: Production Deployment
```bash
# Run production service
python src/stt_service.py

# Monitor health
bash scripts/monitor_service.sh
```
- Production service wrapper with monitoring
- Health checks and error handling
- Statistics tracking

### Phase 6: Batch Processing (Optional)
```bash
python examples/batch_processing.py /path/to/audio/folder
```
- Process entire folders
- Automatic file discovery
- Results saved to JSON

**Total Time:** 10-15 minutes from clone to production

**For detailed instructions, see [DEPLOYMENT_GUIDE_REPO.md](docs/DEPLOYMENT_GUIDE_REPO.md)**

---

## 🔍 Monitoring & Observability

### Health Check

```bash
# Check NeuronCore status
neuron-ls

# Monitor real-time utilization
neuron-top

# Service health check
python scripts/monitor_service.py
```

### Key Metrics to Monitor

| Metric | Tool | Threshold |
|--------|------|-----------|
| NeuronCore Utilization | `neuron-top` | 70-90% optimal |
| Memory Usage | `neuron-monitor` | <28GB per core |
| P99 Latency | Application logs | <5 seconds |
| Error Rate | Application logs | <0.1% |
| Queue Depth | Application metrics | <100 requests |

---

## 🛠️ Troubleshooting

### Issue: Compilation fails

**Solution:**
```bash
# Clear compilation cache
rm -rf /tmp/neuron_cache/*

# Verify NeuronCore availability
neuron-ls

# Check Neuron driver
lsmod | grep neuron
```

### Issue: Slow inference

**Solution:**
```bash
# Check for background processes
neuron-top

# Ensure warmup was performed
# Run 2-3 warmup iterations before benchmarking

# Verify async mode is enabled (optimized config)
```

### Issue: ModuleNotFoundError

**Solution:**
```bash
# Install missing dependencies
pip install openai-whisper soundfile jiwer

# Verify environment
python -c "import torch_neuronx; import neuronx_distributed_inference"
```

**Full troubleshooting guide:** See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 📊 Cost Analysis

### AWS Trainium1 Pricing (us-east-1)

| Instance Type | vCPUs | Memory | NeuronCores | On-Demand | Spot (avg) |
|---------------|-------|--------|-------------|-----------|------------|
| trn1.2xlarge  | 8     | 32 GB  | 2           | $1.34/hr  | $0.40/hr   |
| trn1.32xlarge | 128   | 512 GB | 32          | $21.50/hr | $6.45/hr   |

### Cost per Transcription

**Assumptions:**
- Instance: trn1.2xlarge on-demand ($1.34/hr)
- Throughput: 1.95 requests/second
- Utilization: 70% (1.37 req/s effective)

**Cost Calculation:**
- Hourly capacity: 1.37 req/s × 3,600s = 4,932 transcriptions/hour
- **Cost per transcription: $0.000272** (0.027 cents)
- **Cost per 1,000 transcriptions: $0.27**

**With Spot Instances (70% savings):**
- **Cost per 1,000 transcriptions: $0.08**

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Getting started guide (you are here) |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Complete step-by-step deployment |
| [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md) | Detailed performance analysis |
| [docs/PERFORMANCE_TUNING.md](docs/PERFORMANCE_TUNING.md) | Optimization techniques |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues and fixes |
| [docs/API_REFERENCE.md](docs/API_REFERENCE.md) | Code documentation |
| [examples/](examples/) | Usage examples |

---

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🔗 Quick Links

- **[📖 Deployment Guide](docs/DEPLOYMENT_GUIDE_REPO.md)** - Complete step-by-step instructions
- **[⚡ Quick Start](QUICK_START.md)** - 5-minute quick start
- **[📊 Benchmark Results](docs/BENCHMARK_RESULTS.md)** - Detailed performance data
- **[📚 Original Guide](docs/DEPLOYMENT_GUIDE.md)** - Comprehensive reference
- **[💻 Examples](examples/)** - Code examples
- **[🐛 Issues](https://github.com/your-org/whisper-trainium-deployment/issues)** - Bug reports
- **[💬 Discussions](https://github.com/your-org/whisper-trainium-deployment/discussions)** - Community help

---

## ⚡ TL;DR - Start in 5 Minutes

```bash
# Clone and setup
git clone https://github.com/your-org/whisper-trainium-deployment.git
cd whisper-trainium-deployment
bash scripts/setup_environment.sh

# Download and compile
python src/download_model.py
python src/compile_model.py

# Test
python benchmarks/test_inference.py test_audio/benchmark/audio_01_0-10s.mp3

# You're ready for production! 🚀
```

**For detailed instructions:** [DEPLOYMENT_GUIDE_REPO.md](docs/DEPLOYMENT_GUIDE_REPO.md)

---

**Built with ❤️ for the AWS Trainium community**

**Star ⭐ this repo if it helped you!**

---

*Last Updated: April 29, 2026*  
*Version: 1.0.0*  
*Tested on: AWS trn1.2xlarge, Ubuntu 24.04, Neuron SDK 2.31*
