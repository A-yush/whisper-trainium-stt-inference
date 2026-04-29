"""Batch audio processing example"""
import sys
from pathlib import Path
import json
import time
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from whisper_nxd import WhisperNxD


def process_batch(audio_folder, output_file="batch_results.json", language="hi"):
    """
    Process all audio files in a folder.

    Args:
        audio_folder: Path to folder containing audio files
        output_file: Path to save results JSON
        language: Input language code
    """
    audio_folder = Path(audio_folder)

    if not audio_folder.exists():
        print(f"Error: Folder not found: {audio_folder}")
        return

    # Find all audio files
    audio_files = []
    for ext in ['*.mp3', '*.wav', '*.flac', '*.m4a']:
        audio_files.extend(audio_folder.glob(ext))

    if not audio_files:
        print(f"No audio files found in {audio_folder}")
        return

    print(f"Found {len(audio_files)} audio files")
    print("=" * 80)

    # Initialize model
    print("\nInitializing model...")
    model = WhisperNxD(
        model_path="models/whisper-hindi2hinglish-swift",
        compiled_path="models/whisper-hindi2hinglish-swift-compiled-tp2",
        tp_degree=2,
        language=language
    )

    model.load()

    # Process all files
    results = []
    total_audio_duration = 0
    total_processing_time = 0

    print(f"\nProcessing {len(audio_files)} files...")
    print("=" * 80)

    for i, audio_file in enumerate(sorted(audio_files), 1):
        print(f"\n[{i}/{len(audio_files)}] {audio_file.name}")

        try:
            start = time.time()
            result = model.transcribe(str(audio_file))
            elapsed = time.time() - start

            rtf = elapsed / result['duration']
            total_audio_duration += result['duration']
            total_processing_time += elapsed

            print(f"  Duration: {result['duration']:.2f}s")
            print(f"  Processing: {elapsed:.3f}s")
            print(f"  RTF: {rtf:.4f}x")
            print(f"  Text: {result['text'][:80]}...")

            results.append({
                'file': str(audio_file),
                'duration': result['duration'],
                'processing_time': elapsed,
                'rtf': rtf,
                'text': result['text'],
                'success': True
            })

        except Exception as e:
            print(f"  Error: {e}")
            results.append({
                'file': str(audio_file),
                'success': False,
                'error': str(e)
            })

    # Save results
    output = {
        'total_files': len(audio_files),
        'successful': sum(1 for r in results if r.get('success')),
        'failed': sum(1 for r in results if not r.get('success')),
        'total_audio_duration': total_audio_duration,
        'total_processing_time': total_processing_time,
        'avg_rtf': total_processing_time / total_audio_duration if total_audio_duration > 0 else 0,
        'files': results
    }

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    # Summary
    print("\n" + "=" * 80)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 80)
    print(f"Total files: {len(audio_files)}")
    print(f"Successful: {output['successful']}")
    print(f"Failed: {output['failed']}")
    print(f"Total audio: {total_audio_duration/60:.1f} minutes")
    print(f"Total processing: {total_processing_time:.1f} seconds")
    print(f"Average RTF: {output['avg_rtf']:.4f}x")
    print(f"Speed: {1/output['avg_rtf']:.1f}x faster than real-time")
    print(f"\nResults saved to: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Batch process audio files')
    parser.add_argument('folder', help='Folder containing audio files')
    parser.add_argument('--output', default='batch_results.json', help='Output JSON file')
    parser.add_argument('--language', default='hi', help='Input language code')

    args = parser.parse_args()

    process_batch(args.folder, args.output, args.language)
