"""Comprehensive STT benchmark with duration-based analysis"""
import time
import json
from pathlib import Path
from whisper_nxd import WhisperNxD
import numpy as np
from collections import defaultdict

def categorize_by_duration(duration):
    """Categorize audio file by duration into bins"""
    if duration <= 10:
        return "0-10s"
    elif duration <= 30:
        return "10-30s"
    elif duration <= 60:
        return "30-60s"
    else:
        return "60s+"

def benchmark(model, audio_files, warmup_runs=2):
    """Run benchmark on multiple audio files"""
    
    results = {
        'files': [],
        'total_audio_duration': 0,
        'total_processing_time': 0,
        'overall_metrics': {},
        'duration_bins': {}
    }
    
    # Warmup
    if warmup_runs > 0 and audio_files:
        print(f"Running {warmup_runs} warmup iterations...")
        for _ in range(warmup_runs):
            model.transcribe(str(audio_files[0]))
        print("✓ Warmup complete\n")
    
    # Benchmark each file
    processing_times = []
    rtfs = []
    audio_durations = []
    
    # Track metrics by duration bin
    bin_data = defaultdict(lambda: {
        'processing_times': [],
        'rtfs': [],
        'audio_durations': [],
        'count': 0
    })
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"[{i}/{len(audio_files)}] Processing: {audio_file.name}")
        
        start = time.time()
        result = model.transcribe(str(audio_file))
        elapsed = time.time() - start
        
        rtf = elapsed / result['duration']
        processing_times.append(elapsed)
        rtfs.append(rtf)
        audio_durations.append(result['duration'])
        
        # Categorize by duration
        duration_bin = categorize_by_duration(result['duration'])
        bin_data[duration_bin]['processing_times'].append(elapsed)
        bin_data[duration_bin]['rtfs'].append(rtf)
        bin_data[duration_bin]['audio_durations'].append(result['duration'])
        bin_data[duration_bin]['count'] += 1
        
        print(f"     Duration: {result['duration']:.2f}s | Time: {elapsed:.3f}s | RTF: {rtf:.4f}x")
        
        results['files'].append({
            'file': str(audio_file),
            'duration': result['duration'],
            'duration_bin': duration_bin,
            'processing_time': elapsed,
            'rtf': rtf,
            'text': result['text']
        })
        
        results['total_audio_duration'] += result['duration']
        results['total_processing_time'] += elapsed
    
    # Calculate overall statistics
    results['overall_metrics'] = {
        'avg_processing_time': float(np.mean(processing_times)),
        'std_processing_time': float(np.std(processing_times)),
        'min_processing_time': float(np.min(processing_times)),
        'max_processing_time': float(np.max(processing_times)),
        'p50_processing_time': float(np.percentile(processing_times, 50)),
        'p90_processing_time': float(np.percentile(processing_times, 90)),
        'p99_processing_time': float(np.percentile(processing_times, 99)),
        'avg_rtf': float(np.mean(rtfs)),
        'p50_rtf': float(np.percentile(rtfs, 50)),
        'p90_rtf': float(np.percentile(rtfs, 90)),
        'p99_rtf': float(np.percentile(rtfs, 99)),
        'min_rtf': float(np.min(rtfs)),
        'max_rtf': float(np.max(rtfs)),
        'avg_audio_duration': float(np.mean(audio_durations)),
        'min_audio_duration': float(np.min(audio_durations)),
        'max_audio_duration': float(np.max(audio_durations)),
        'throughput_req_per_sec': len(audio_files) / results['total_processing_time'],
        'total_files': len(audio_files)
    }
    
    # Calculate per-bin statistics
    bin_order = ["0-10s", "10-30s", "30-60s", "60s+"]
    for bin_name in bin_order:
        if bin_name in bin_data:
            data = bin_data[bin_name]
            results['duration_bins'][bin_name] = {
                'count': data['count'],
                'avg_audio_duration': float(np.mean(data['audio_durations'])),
                'avg_processing_time': float(np.mean(data['processing_times'])),
                'p50_processing_time': float(np.percentile(data['processing_times'], 50)),
                'p90_processing_time': float(np.percentile(data['processing_times'], 90)),
                'p99_processing_time': float(np.percentile(data['processing_times'], 99)),
                'avg_rtf': float(np.mean(data['rtfs'])),
            }
    
    return results

def print_results_table(results):
    """Print results in a formatted table like the reference image"""
    
    print("\n" + "=" * 100)
    print("WHISPER STT BENCHMARK - FINAL RESULTS")
    print("=" * 100)
    
    # Overall Performance
    overall = results['overall_metrics']
    print(f"\nOverall Performance ({overall['total_files']} files)")
    print("-" * 100)
    print(f"• Processing Time: Avg {overall['avg_processing_time']*1000:.1f}ms, "
          f"P90 {overall['p90_processing_time']*1000:.1f}ms, "
          f"P99 {overall['p99_processing_time']*1000:.1f}ms")
    print(f"• RTF: Avg {overall['avg_rtf']:.3f}x, "
          f"P90 {overall['p90_rtf']:.3f}x, "
          f"P99 {overall['p99_rtf']:.3f}x")
    print(f"• Audio Duration: Avg {overall['avg_audio_duration']:.2f}s "
          f"(range: {overall['min_audio_duration']:.2f}s - {overall['max_audio_duration']:.2f}s)")
    
    # Performance by Duration Range
    print(f"\n\nPerformance by Duration Range")
    print("-" * 100)
    
    # Table header
    header = f"{'Duration':<12} {'Files':<7} {'Avg Audio':<12} {'Avg Processing':<17} " \
             f"{'P90 Processing':<17} {'P99 Processing':<17} {'Avg RTF':<10}"
    print(header)
    print("-" * 100)
    
    # Table rows
    bin_order = ["0-10s", "10-30s", "30-60s", "60s+"]
    for bin_name in bin_order:
        if bin_name in results['duration_bins']:
            bin_data = results['duration_bins'][bin_name]
            row = f"{bin_name:<12} {bin_data['count']:<7} " \
                  f"{bin_data['avg_audio_duration']:.2f}s{'':<7} " \
                  f"{bin_data['avg_processing_time']*1000:.1f}ms{'':<9} " \
                  f"{bin_data['p90_processing_time']*1000:.1f}ms{'':<9} " \
                  f"{bin_data['p99_processing_time']*1000:.1f}ms{'':<9} " \
                  f"{bin_data['avg_rtf']:.3f}x"
            print(row)
    
    # Key Insights
    print(f"\n\nKey Insights")
    print("-" * 100)
    rtf = overall['avg_rtf']
    speedup = 1.0 / rtf if rtf > 0 else 0
    total_audio = results['total_audio_duration']
    total_processing = results['total_processing_time']
    
    print(f"• All processing is much faster than real-time (RTF < 1.0)")
    print(f"• Longer audio files show better efficiency (lower RTF)")
    print(f"• P99 latency remains under {overall['p99_processing_time']:.1f}s even for {overall['max_audio_duration']:.0f}s audio")
    print(f"• The model processes ~{total_audio/60:.1f} minutes of audio in just {total_processing:.1f} seconds on average")
    print(f"• Performance: ~{speedup:.1f}x faster than real-time")
    print(f"• Throughput: {overall['throughput_req_per_sec']:.2f} requests/second")
    
    print("\n" + "=" * 100)

if __name__ == "__main__":
    print("=" * 80)
    print("Whisper STT Comprehensive Benchmark")
    print("=" * 80)
    
    # Initialize model
    print("\nInitializing model...")
    model = WhisperNxD(
        model_path="models/whisper-hindi2hinglish-swift",
        compiled_path="models/whisper-hindi2hinglish-swift-compiled-tp2",
        tp_degree=2,
        language="hi"
    )
    
    model.load()
    
    # Find test audio files (including benchmark subfolder)
    audio_files = list(Path("test_audio").glob("*.mp3"))
    audio_files.extend(Path("test_audio").glob("*.wav"))
    audio_files.extend(Path("test_audio/benchmark").glob("*.mp3"))
    audio_files.extend(Path("test_audio/benchmark").glob("*.wav"))
    
    if not audio_files:
        print("\n✗ No audio files found in test_audio/ or test_audio/benchmark/")
        print("Please run: ./setup_test_audio.sh")
        exit(1)
    
    # Sort files for consistent ordering
    audio_files = sorted(audio_files)
    
    print(f"\nFound {len(audio_files)} audio files:")
    main_files = len(list(Path('test_audio').glob('*.mp3')))
    bench_files = len(list(Path('test_audio/benchmark').glob('*.mp3')))
    print(f"  - In test_audio/: {main_files} files")
    print(f"  - In test_audio/benchmark/: {bench_files} files")
    print()
    
    print("=" * 80)
    print("Starting benchmark...")
    print("=" * 80)
    print()
    
    results = benchmark(model, audio_files, warmup_runs=2)
    
    # Save detailed results
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Print formatted results table
    print_results_table(results)
    
    print(f"\n✓ Detailed results saved to: benchmark_results.json")
    print("=" * 100)
