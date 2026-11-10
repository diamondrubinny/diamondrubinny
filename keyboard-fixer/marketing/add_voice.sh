#!/usr/bin/env bash
# Mixes a narration file over the promo (music/SFX are lowered so the voice stays clear).
# Usage: ./add_voice.sh voice.mp3
set -euo pipefail
cd "$(dirname "$0")"
VOICE="${1:?usage: add_voice.sh voice.mp3}"
ffmpeg -y -loglevel error -i out/keyflip-promo-9x16.mp4 -i "$VOICE" \
  -filter_complex "[0:a]volume=0.45[bg];[1:a]volume=1.4,apad[v];[bg][v]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/keyflip-promo-9x16-voice.mp4
ls -la out/keyflip-promo-9x16-voice.mp4
