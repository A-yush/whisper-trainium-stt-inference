#!/bin/bash
# Rename audio files to match their actual durations

echo "Renaming audio files to match actual durations..."
echo "=================================================="

# Files that are correctly named (0-10s range, actually 4-5 seconds)
echo "✓ audio_01_0-10s.mp3 - 4.39s (correct)"
echo "✓ audio_02_0-10s.mp3 - 5.30s (correct)"
echo "✓ audio_03_0-10s.mp3 - 5.45s (correct)"
echo "✓ audio_04_0-10s.mp3 - 4.42s (correct)"
echo "✓ audio_05_0-10s.mp3 - 5.45s (correct)"
echo ""

# Files labeled 10-20s but actually 20-30s (need rename to 20-30s)
echo "Renaming 10-20s files (actually 20-30s):"
mv audio_06_10-20s.mp3 audio_06_20-30s.mp3 && echo "  audio_06_10-20s.mp3 → audio_06_20-30s.mp3 (27.07s)"
mv audio_07_10-20s.mp3 audio_07_20-30s.mp3 && echo "  audio_07_10-20s.mp3 → audio_07_20-30s.mp3 (22.20s)"
mv audio_08_10-20s.mp3 audio_08_20-30s.mp3 && echo "  audio_08_10-20s.mp3 → audio_08_20-30s.mp3 (22.13s)"
mv audio_09_10-20s.mp3 audio_09_20-30s.mp3 && echo "  audio_09_10-20s.mp3 → audio_09_20-30s.mp3 (20.40s)"
mv audio_10_10-20s.mp3 audio_10_20-30s.mp3 && echo "  audio_10_10-20s.mp3 → audio_10_20-30s.mp3 (20.81s)"
echo ""

# Files labeled 20-40s but actually in different ranges
echo "Renaming 20-40s files (actually mixed ranges):"
mv audio_11_20-40s.mp3 audio_11_60s+.mp3 && echo "  audio_11_20-40s.mp3 → audio_11_60s+.mp3 (60.65s)"
mv audio_12_20-40s.mp3 audio_12_60s+.mp3 && echo "  audio_12_20-40s.mp3 → audio_12_60s+.mp3 (61.49s)"
mv audio_13_20-40s.mp3 audio_13_40-60s.mp3 && echo "  audio_13_20-40s.mp3 → audio_13_40-60s.mp3 (57.41s)"
mv audio_14_20-40s.mp3 audio_14_40-60s.mp3 && echo "  audio_14_20-40s.mp3 → audio_14_40-60s.mp3 (55.13s)"
mv audio_15_20-40s.mp3 audio_15_40-60s.mp3 && echo "  audio_15_20-40s.mp3 → audio_15_40-60s.mp3 (52.85s)"
echo ""

# Files labeled 40-60s but actually 160-170s (need rename to 60s+)
echo "Renaming 40-60s files (actually 160-170s, 60s+):"
mv audio_16_40-60s.mp3 audio_16_60s+.mp3 && echo "  audio_16_40-60s.mp3 → audio_16_60s+.mp3 (165.36s)"
mv audio_17_40-60s.mp3 audio_17_60s+.mp3 && echo "  audio_17_40-60s.mp3 → audio_17_60s+.mp3 (167.47s)"
mv audio_18_40-60s.mp3 audio_18_60s+.mp3 && echo "  audio_18_40-60s.mp3 → audio_18_60s+.mp3 (169.90s)"
mv audio_19_40-60s.mp3 audio_19_60s+.mp3 && echo "  audio_19_40-60s.mp3 → audio_19_60s+.mp3 (162.91s)"
mv audio_20_40-60s.mp3 audio_20_60s+.mp3 && echo "  audio_20_40-60s.mp3 → audio_20_60s+.mp3 (170.88s)"
echo ""

echo "=================================================="
echo "✓ Renaming complete!"
echo ""
echo "New file distribution:"
echo "  0-10s:   audio_01 to audio_05 (5 files)"
echo "  20-30s:  audio_06 to audio_10 (5 files)"
echo "  40-60s:  audio_13 to audio_15 (3 files)"
echo "  60s+:    audio_11, audio_12, audio_16 to audio_20 (7 files)"
