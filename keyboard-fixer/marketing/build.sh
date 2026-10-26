#!/usr/bin/env bash
# Builds marketing/out/keyflip-promo-9x16.mp4 (video + sfx + music, no voice) from promo.html.
# Requires: node + playwright (preinstalled in the dev container), python3 + numpy, ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
WORK="${1:-/tmp/keyflip-promo}"
mkdir -p "$WORK/frames" out
node render.cjs "$WORK/frames" "$WORK/sfx.json" 30
python3 make_audio.py "$WORK/sfx.json" "$WORK/audio.wav"
ffmpeg -y -loglevel error -framerate 30 -i "$WORK/frames/f%05d.jpg" -i "$WORK/audio.wav" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -shortest -movflags +faststart \
  out/keyflip-promo-9x16.mp4
ls -la out/keyflip-promo-9x16.mp4
