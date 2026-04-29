# Deployment Guide: Whisper STT on AWS Trainium1
## Using the whisper-trainium-deployment Repository

This guide walks you through deploying the Whisper Hindi2Hinglish STT model on AWS Trainium1 using the pre-built scripts and tools in this repository.

---

## Table of Contents
1. [Environment Overview](#environment-overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Environment Setup](#phase-1-environment-setup)
4. [Phase 2: Model Download](#phase-2-model-download)
5. [Phase 3: Model Compilation](#phase-3-model-compilation)
6. [Phase 4: Testing & Validation](#phase-4-testing--validation)
7. [Phase 5: Benchmarking](#phase-5-benchmarking)
8. [Phase 6: Production Deployment](#phase-6-production-deployment)
9. [Troubleshooting](#troubleshooting)

---

## Environment Overview

**Target Instance:**
- **Instance Type:** `trn1.2xlarge` (AWS Trainium1)
- **OS:** Ubuntu 22.04 or 24.04 LTS
- **NeuronCores:** 2 cores, 32 GB Neuron memory
- **Python:** 3.10+

**Neuron Stack Required:**
- **AWS Neuron Driver:** 2.27.4.0+
- **Neuron Runtime:** 2.31.x+
- **Neuron Tools:** 2.29.x+

---

## Prerequisites

✅ AWS Trainium instance (trn1.2xlarge or larger)  
✅ Neuron SDK pre-installed (included in DLAMI)  
✅ Git installed  
✅ Internet access for model download  

---

## Phase 1: Environment Setup

### Step 1.1: Clone Repository

```bash
cd ~
git clone https://github.com/your-org/whisper-trainium-deployment.git
cd whisper-trainium-deployment
```

**What you get:**
```
whisper-trainium-deployment/
├── src/               # Source code (whisper_nxd.py, etc.)
├── benchmarks/        # Benchmarking tools
├── scripts/           # Setup and monitoring scripts
├── configs/           # Configuration files
├── docs/              # Documentation
├── examples/          # Usage examples
└── test_audio/        # Sample audio files
```

### Step 1.2: Run Automated Environment Setup

Use the provided setup script to verify your environment:

```bash
bash scripts/setup_environment.sh
```

**What this script does:**
1. ✓ Verifies NeuronCore availability (`neuron-ls`)
2. ✓ Checks Neuron kernel module (`lsmod | grep neuron`)
3. ✓ Validates Neuron device access (`/dev/neuron*`)
4. ✓ Activates virtual environment
5. ✓ Checks PyTorch, torch-neuronx, NxD Inference versions
6. ✓ Installs additional dependencies (`soundfile`, `jiwer`, `openai-whisper`)
7. ✓ Creates necessary directories

**Expected Output:**
```
==========================================
Whisper Trainium Environment Setup
==========================================

Step 1: Verifying Trainium Hardware...
✓ NeuronCores detected

Step 2: Checking Neuron Driver...
✓ Neuron kernel module loaded

Step 3: Checking Neuron Device...
✓ Neuron device accessible

Step 4: Checking Virtual Environment...
✓ Neuron virtual environment found

Step 5: Verifying Python Packages...
✓ PyTorch installed
✓ torch-neuronx installed
✓ neuronx-distributed-inference installed

Step 6: Installing Additional Dependencies...
✓ All dependencies installed

Step 7: Creating Directory Structure...
✓ Directories created

==========================================
Environment Setup Complete!
==========================================
```

### Step 1.3: Activate Virtual Environment

The setup script activates the environment, but for future sessions:

```bash
source /opt/aws_neuronx_venv_pytorch_2_9_nxd_inference/bin/activate
```

---

## Phase 2: Model Download

### Step 2.1: Download Model from HuggingFace

Use the provided download script:

```bash
cd ~/whisper-trainium-deployment
python src/download_model.py
```

**What `src/download_model.py` does:**
- Downloads `Oriserve/Whisper-Hindi2Hinglish-Swift` from HuggingFace
- Saves to `models/whisper-hindi2hinglish-swift/`
- Downloads model weights (~277 MB)
- Downloads processor (tokenizer, feature extractor)
- Verifies file integrity

**Expected Output:**
```
Downloading model: Oriserve/Whisper-Hindi2Hinglish-Swift
This may take several minutes depending on network speed...

[1/2] Downloading model weights...
✓ Model weights saved

[2/2] Downloading processor...
✓ Processor saved

✓ Download complete → models/whisper-hindi2hinglish-swift
  Model size: ~0.28 GB
```

### Step 2.2: Verify Downloaded Files

```bash
ls -lh models/whisper-hindi2hinglish-swift/
```

**Expected Files:**
```
config.json              # Model configuration
generation_config.json   # Generation parameters
model.safetensors       # Model weights (277MB)
preprocessor_config.json # Audio preprocessing config
tokenizer.json          # Tokenizer (3.8MB)
tokenizer_config.json   # Tokenizer configuration
vocab.json              # Vocabulary (816KB)
merges.txt              # BPE merges (483KB)
special_tokens_map.json # Special tokens
added_tokens.json       # Custom tokens
```

**Total Size:** ~283 MB (Whisper Base model, 74M parameters)

---

## Phase 3: Model Compilation

### Step 3.1: Understanding the Whisper NxD Wrapper

The repository includes `src/whisper_nxd.py` - a wrapper class that simplifies Whisper deployment on Trainium:

**Key Features:**
- Automatic model compilation for Neuron hardware
- Optimized configuration (TP degree, FP16, batch size)
- Audio preprocessing (resampling, mono conversion)
- Simple API: `compile()`, `load()`, `transcribe()`

### Step 3.2: Compile Model for Trainium

Use the provided compilation script:

```bash
python src/compile_model.py
```

**What `src/compile_model.py` does:**
1. Imports `WhisperNxD` from `src/whisper_nxd.py`
2. Configures compilation:
   - Source: `models/whisper-hindi2hinglish-swift`
   - Target: `models/whisper-hindi2hinglish-swift-compiled-tp2`
   - TP Degree: 2 (for trn1.2xlarge's 2 NeuronCores)
   - Language: Hindi (hi)
3. Compiles encoder and decoder for Neuron
4. Saves compiled artifacts

**Expected Output:**
```
================================================================================
Whisper Model Compilation for AWS Trainium1
================================================================================

Configuration:
  Model: models/whisper-hindi2hinglish-swift
  Output: models/whisper-hindi2hinglish-swift-compiled-tp2
  TP Degree: 2
  Language: hi

Compiling Whisper model for Trainium...
  Source: models/whisper-hindi2hinglish-swift
  Target: models/whisper-hindi2hinglish-swift-compiled-tp2
  TP Degree: 2
  Language: hi

This will take 1-2 minutes for Whisper Base...

[Compiler logs...]

✓ Compilation complete
  Compiled artifacts saved to: models/whisper-hindi2hinglish-swift-compiled-tp2

✓ Compilation completed in 86.0 seconds (1.4 minutes)
  Compiled model ready at: models/whisper-hindi2hinglish-swift-compiled-tp2
```

**Compilation Time:**
- Whisper Base: 1-2 minutes ✓
- Whisper Small: 3-5 minutes
- Whisper Medium: 10-15 minutes

### Step 3.3: Verify Compilation Artifacts

```bash
tree models/whisper-hindi2hinglish-swift-compiled-tp2/ -L 2
```

**Expected Structure:**
```
models/whisper-hindi2hinglish-swift-compiled-tp2/
├── encoder/
│   ├── model.pt              # Compiled encoder for Neuron
│   └── neuron_config.json    # Encoder configuration
└── decoder/
    ├── model.pt              # Compiled decoder for Neuron
    └── neuron_config.json    # Decoder configuration
```

---

## Phase 4: Testing & Validation

### Step 4.1: Verify Test Audio Files

The repository includes test audio in `test_audio/`:

```bash
ls -la test_audio/
ls -la test_audio/benchmark/
```

**Test Audio Structure:**
```
test_audio/
├── en_aws_tranium_250words.mp3    # English sample (145s)
└── benchmark/                      # 30 benchmark files
    ├── audio_01-05_0-10s.mp3      # 5 files: 4-5s
    ├── audio_06-10_20-30s.mp3     # 5 files: 20-30s
    ├── audio_13-15_40-60s.mp3     # 3 files: 40-60s
    ├── audio_11-12,16-20_60s+.mp3 # 7 files: 60-171s
    └── audio_21-30_0-10s.mp3      # 10 files: AWS speech (12-16s)
```

**Total:** 31 test files covering durations from 4s to 171s

### Step 4.2: Run Single File Test

Use the provided test inference script:

```bash
python benchmarks/test_inference.py test_audio/benchmark/audio_01_0-10s.mp3
```

**What `benchmarks/test_inference.py` does:**
1. Imports `WhisperNxD` from `src/whisper_nxd.py`
2. Loads compiled model onto NeuronCores
3. Transcribes the audio file
4. Displays results with timing metrics

**Expected Output:**
```
Loading model...
Loading compiled model onto NeuronCores...
✓ Model loaded and ready for inference

Transcribing: test_audio/benchmark/audio_01_0-10s.mp3

================================================================================
INFERENCE RESULTS
================================================================================
Audio File:      test_audio/benchmark/audio_01_0-10s.mp3
Audio Duration:  4.39 seconds
Processing Time: 0.075 seconds
RTF (Real-Time Factor): 0.0171x

Transcription:
  [Hindi/Hinglish transcription text]
================================================================================
```

**Key Metrics to Note:**
- **Processing Time:** Should be <100ms for short files
- **RTF (Real-Time Factor):** Should be <0.02x (50x+ faster than real-time)

### Step 4.3: Test Different Audio Lengths

Test across various durations:

```bash
# Short audio (4-5s)
python benchmarks/test_inference.py test_audio/benchmark/audio_01_0-10s.mp3

# Medium audio (20-30s)
python benchmarks/test_inference.py test_audio/benchmark/audio_06_20-30s.mp3

# Long audio (40-60s)
python benchmarks/test_inference.py test_audio/benchmark/audio_13_40-60s.mp3

# Very long audio (60s+)
python benchmarks/test_inference.py test_audio/benchmark/audio_11_60s+.mp3

# English sample
python benchmarks/test_inference.py test_audio/en_aws_tranium_250words.mp3 en
```

**Note:** Add `en` as second argument for English audio (default is Hindi `hi`)

---

## Phase 5: Benchmarking

### Step 5.1: Run Comprehensive Benchmark

Use the comprehensive benchmark script to test all 31 audio files:

```bash
python benchmarks/benchmark_stt.py
```

**What `benchmarks/benchmark_stt.py` does:**
1. Loads `WhisperNxD` model from `src/whisper_nxd.py`
2. Finds all audio files in `test_audio/` and `test_audio/benchmark/`
3. Runs 2 warmup iterations
4. Processes all 31 files sequentially
5. Categorizes by duration (0-10s, 10-30s, 30-60s, 60s+)
6. Calculates statistics (avg, P50, P90, P99)
7. Generates formatted table output
8. Saves detailed JSON results

**Expected Output:**
```
================================================================================
Whisper STT Comprehensive Benchmark
================================================================================

Initializing model...
Loading compiled model onto NeuronCores...
✓ Model loaded and ready for inference

Found 31 audio files:
  - In test_audio/: 1 files
  - In test_audio/benchmark/: 30 files

================================================================================
Starting benchmark...
================================================================================

Running 2 warmup iterations...
✓ Warmup complete

[1/31] Processing: audio_01_0-10s.mp3
     Duration: 4.39s | Time: 0.075s | RTF: 0.0171x
[2/31] Processing: audio_02_0-10s.mp3
     Duration: 5.30s | Time: 0.072s | RTF: 0.0135x
...
[31/31] Processing: en_aws_tranium_250words.mp3
     Duration: 144.79s | Time: 1.368s | RTF: 0.0094x

====================================================================================================
WHISPER STT BENCHMARK - FINAL RESULTS
====================================================================================================

Overall Performance (31 files)
----------------------------------------------------------------------------------------------------
• Processing Time: Avg 513.1ms, P90 1417.2ms, P99 3200.4ms
• RTF: Avg 0.011x, P90 0.017x, P99 0.022x
• Audio Duration: Avg 50.06s (range: 4.39s - 170.88s)


Performance by Duration Range
----------------------------------------------------------------------------------------------------
Duration     Files   Avg Audio    Avg Processing    P90 Processing    P99 Processing    Avg RTF   
----------------------------------------------------------------------------------------------------
0-10s        5       5.00s        75.4ms            78.3ms            79.2ms            0.015x
10-30s       15      17.21s       170.0ms           237.2ms           398.6ms           0.010x
30-60s       3       55.13s       484.6ms           645.4ms           702.6ms           0.009x
60s+         8       137.93s      1440.8ms          2201.3ms          3774.9ms          0.010x


Key Insights
----------------------------------------------------------------------------------------------------
• All processing is much faster than real-time (RTF < 1.0)
• Longer audio files show better efficiency (lower RTF)
• P99 latency remains under 3.2s even for 171s audio
• The model processes ~25.9 minutes of audio in just 15.9 seconds on average
• Performance: ~93.5x faster than real-time
• Throughput: 1.95 requests/second

====================================================================================================

✓ Detailed results saved to: benchmark_results.json
====================================================================================================
```

### Step 5.2: Review Benchmark Results

**JSON Output:** Detailed results saved to `benchmark_results.json`

```bash
# View summary
jq '.overall_metrics' benchmark_results.json

# View duration bins
jq '.duration_bins' benchmark_results.json

# View individual files
jq '.files[] | {file, duration, rtf}' benchmark_results.json
```

**Markdown Report:** See `docs/BENCHMARK_RESULTS.md` for detailed analysis

---

## Phase 6: Production Deployment

### Step 6.1: Use Production Service Wrapper

The repository includes `src/stt_service.py` - a production-ready service wrapper:

**Features:**
- Health monitoring
- Error handling
- Statistics tracking
- Warmup automation
- Logging integration

**Usage:**

```python
from src.stt_service import STTService

# Initialize service
service = STTService(
    compiled_model_path="models/whisper-hindi2hinglish-swift-compiled-tp2",
    base_model_path="models/whisper-hindi2hinglish-swift",
    language="hi"
)

# Start service (includes warmup)
service.initialize()

# Transcribe audio
result = service.transcribe("path/to/audio.mp3")

if result['success']:
    print(f"Transcription: {result['text']}")
    print(f"Duration: {result['duration']:.2f}s")
    print(f"Processing Time: {result['processing_time']:.3f}s")
    print(f"RTF: {result['rtf']:.4f}x")
else:
    print(f"Error: {result['error']}")

# Health check
health = service.health_check()
print(health)
```

### Step 6.2: Run Production Service

Test the production service:

```bash
python src/stt_service.py test_audio/benchmark/audio_01_0-10s.mp3
```

**Expected Output:**
```json
{
  "status": "healthy",
  "ready": true,
  "statistics": {
    "total_requests": 1,
    "successful_requests": 1,
    "failed_requests": 0,
    "success_rate": 100.0,
    "avg_processing_time": 0.075,
    "avg_rtf": 0.0171,
    "total_audio_processed": 4.39
  }
}
```

### Step 6.3: Monitor Service Health

Use the provided monitoring script:

```bash
bash scripts/monitor_service.sh
```

**What `scripts/monitor_service.sh` does:**
1. Checks NeuronCore status (`neuron-ls`)
2. Displays NeuronCore utilization (`neuron-top`)
3. Shows system memory usage
4. Lists Neuron processes
5. Verifies device accessibility

**For continuous monitoring:**
```bash
bash scripts/monitor_service.sh --watch
```

Press `Ctrl+C` to exit.

---

## Configuration Options

### Baseline Configuration

See `configs/baseline_config.yaml`:

```yaml
model:
  language: "hi"
  
neuron:
  tp_degree: 2
  batch_size: 1
  torch_dtype: "float16"
  async_mode: false        # Standard mode
  k_cache_transposed: false
```

**Use for:** Standard deployment, tested and stable

### Optimized Configuration

See `configs/optimized_config.yaml`:

```yaml
model:
  language: "hi"
  
neuron:
  tp_degree: 2
  batch_size: 1
  torch_dtype: "float16"
  async_mode: true         # Enable async I/O
  k_cache_transposed: true # Optimize KV cache
```

**Use for:** 15-30% performance improvement (requires WER validation)

---

## Batch Processing Example

Use the batch processing example:

```bash
python examples/batch_processing.py /path/to/audio/folder
```

**What `examples/batch_processing.py` does:**
1. Finds all audio files in the folder (mp3, wav, flac, m4a)
2. Initializes `WhisperNxD` model
3. Processes all files sequentially
4. Tracks total duration, processing time, RTF
5. Saves results to JSON
6. Displays summary statistics

**Example output:**
```
Found 50 audio files

Processing 50 files...
================================================================================

[1/50] audio_001.mp3
  Duration: 12.34s
  Processing: 0.145s
  RTF: 0.0117x
  Text: [transcription...]
...

================================================================================
BATCH PROCESSING COMPLETE
================================================================================
Total files: 50
Successful: 50
Failed: 0
Total audio: 18.5 minutes
Total processing: 11.2 seconds
Average RTF: 0.0101x
Speed: 99.0x faster than real-time

Results saved to: batch_results.json
================================================================================
```

---

## Troubleshooting

### Issue: Environment setup fails

**Solution:**
```bash
# Check NeuronCores
neuron-ls

# Verify kernel module
lsmod | grep neuron

# Reload if needed
sudo modprobe neuron

# Re-run setup
bash scripts/setup_environment.sh
```

### Issue: Model download fails

**Solution:**
```bash
# Check internet connectivity
ping huggingface.co

# Clear cache and retry
rm -rf models/whisper-hindi2hinglish-swift/
python src/download_model.py
```

### Issue: Compilation fails

**Solution:**
```bash
# Clear compilation cache
rm -rf /tmp/neuron_cache/*

# Remove partial compilation
rm -rf models/whisper-hindi2hinglish-swift-compiled-tp2/

# Retry compilation
python src/compile_model.py
```

### Issue: Inference is slow

**Diagnosis:**
```bash
# Check for competing processes
neuron-top

# Monitor during inference
bash scripts/monitor_service.sh --watch
```

**Solution:**
- Ensure warmup was performed (2-3 iterations)
- Check no other models are loaded on NeuronCores
- Verify using compiled model (not base model)

### Issue: Import errors

**Solution:**
```bash
# Activate virtual environment
source /opt/aws_neuronx_venv_pytorch_2_9_nxd_inference/bin/activate

# Verify imports
python -c "from src.whisper_nxd import WhisperNxD; print('✓ Import successful')"

# Install missing dependencies
pip install -r requirements.txt
```

---

## Repository File Reference

### Source Code (`src/`)

| File | Purpose |
|------|---------|
| `whisper_nxd.py` | Main Whisper NxD wrapper class |
| `download_model.py` | HuggingFace model downloader |
| `compile_model.py` | Model compilation script |
| `stt_service.py` | Production service wrapper |

### Benchmarks (`benchmarks/`)

| File | Purpose |
|------|---------|
| `benchmark_stt.py` | Comprehensive benchmark (31 files) |
| `test_inference.py` | Single-file inference testing |

### Scripts (`scripts/`)

| File | Purpose |
|------|---------|
| `setup_environment.sh` | Automated environment setup |
| `monitor_service.sh` | Health monitoring |

### Configuration (`configs/`)

| File | Purpose |
|------|---------|
| `baseline_config.yaml` | Standard configuration |
| `optimized_config.yaml` | Performance-optimized |

### Examples (`examples/`)

| File | Purpose |
|------|---------|
| `batch_processing.py` | Batch folder processing |

---

## Performance Summary

**Hardware:** AWS trn1.2xlarge (2 NeuronCores)  
**Model:** Whisper Base (74M params, 283MB)  
**Configuration:** TP=2, FP16, Batch=1

| Metric | Value |
|--------|-------|
| **Average Latency** | 513ms |
| **P90 Latency** | 1.4s |
| **P99 Latency** | 3.2s |
| **Average RTF** | 0.011x |
| **Speed vs Real-time** | 93.5x faster |
| **Throughput** | 1.95 req/sec |

**Full performance analysis:** See `docs/BENCHMARK_RESULTS.md`

---

## Additional Resources

- **Full Deployment Guide:** `docs/DEPLOYMENT_GUIDE.md`
- **Quick Start:** `QUICK_START.md` (5 minutes)
- **Benchmark Results:** `docs/BENCHMARK_RESULTS.md`
- **Repository Checklist:** `REPOSITORY_CHECKLIST.md`

**External Links:**
- [AWS Neuron Documentation](https://awsdocs-neuron.readthedocs-hosted.com/)
- [HuggingFace Model](https://huggingface.co/Oriserve/Whisper-Hindi2Hinglish-Swift)
- [Trainium Instances](https://aws.amazon.com/ec2/instance-types/trn1/)

---

## Summary Checklist

### Setup
- [ ] Cloned repository
- [ ] Ran `scripts/setup_environment.sh`
- [ ] Virtual environment activated

### Model
- [ ] Downloaded with `src/download_model.py` (~283 MB)
- [ ] Compiled with `src/compile_model.py` (~1-2 min)
- [ ] Verified compiled artifacts exist

### Testing
- [ ] Tested single file with `benchmarks/test_inference.py`
- [ ] Ran full benchmark with `benchmarks/benchmark_stt.py`
- [ ] Reviewed performance metrics

### Production
- [ ] Tested `src/stt_service.py`
- [ ] Monitored with `scripts/monitor_service.sh`
- [ ] Reviewed configurations in `configs/`

---

**Deployment Status:** ✅ Ready for Production

**Time to Deploy:** 5-10 minutes (excluding downloads)

**Next Steps:** Scale to production with load balancing and auto-scaling

---

*Created: 2026-04-29*  
*Version: 1.0.0 - Repository-based Deployment*  
*Repository: whisper-trainium-deployment*
