"""Generate 10 additional 10-second audio files for testing"""
import numpy as np
import soundfile as sf
from pathlib import Path

print("=" * 80)
print("Creating 10 Additional 10-Second Test Audio Files")
print("=" * 80)

# Create 10 new audio files (audio_21 through audio_30)
for i in range(21, 31):
    filename = f"audio_{i:02d}_0-10s.mp3"
    
    # Generate 10 seconds of audio at 16kHz
    duration = 10.0  # seconds
    sample_rate = 16000
    num_samples = int(duration * sample_rate)
    
    # Generate varied audio patterns for each file
    t = np.linspace(0, duration, num_samples)
    
    # Create different frequency patterns for variety
    base_freq = 200 + (i % 5) * 50  # Vary base frequency
    modulation_freq = 2 + (i % 3)   # Vary modulation
    
    # Generate audio with sine wave + some modulation
    audio = 0.3 * np.sin(2 * np.pi * base_freq * t)
    audio += 0.1 * np.sin(2 * np.pi * modulation_freq * t)
    
    # Add some noise for realism
    noise = 0.02 * np.random.randn(num_samples)
    audio = audio + noise
    
    # Normalize to prevent clipping
    audio = audio / np.max(np.abs(audio)) * 0.8
    
    # Convert to float32
    audio = audio.astype(np.float32)
    
    # Save as WAV first (soundfile doesn't directly support MP3)
    wav_filename = filename.replace('.mp3', '.wav')
    sf.write(wav_filename, audio, sample_rate)
    
    actual_duration = len(audio) / sample_rate
    print(f"✓ Created {wav_filename} ({actual_duration:.2f}s)")

print("\n" + "=" * 80)
print(f"✓ Successfully created 10 new audio files (audio_21 to audio_30)")
print(f"  Format: WAV (16kHz, mono, float32)")
print(f"  Duration: 10.0 seconds each")
print(f"  Location: test_audio/benchmark/")
print("=" * 80)
print("\nNote: Files are in WAV format. If MP3 is required, use ffmpeg to convert:")
print("  for f in audio_2*.wav; do ffmpeg -i \"$f\" \"${f%.wav}.mp3\"; done")
print("=" * 80)
