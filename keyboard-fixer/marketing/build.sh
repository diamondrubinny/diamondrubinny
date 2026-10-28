#!/usr/bin/env bash
# Usage: ./build.sh [he|en] [workdir]
#   he -> out/keyflip-promo-9x16.mp4        (video + sfx + music, no voice)
#   en -> out/keyflip-promo-en-9x16.mp4     (same + English narration generated offline with Piper)
# Requires: node + playwright, python3 + numpy, ffmpeg; for "en": pip install piper-tts and PIPER_MODEL=/path/to/voice.onnx
set -euo pipefail
cd "$(dirname "$0")"
LANG_CODE="${1:-he}"
WORK="${2:-/tmp/keyflip-promo-$LANG_CODE}"
mkdir -p "$WORK/frames" out
rm -f "$WORK"/frames/*.jpg
node render.cjs "$WORK/frames" "$WORK/sfx.json" 30 "$LANG_CODE"
python3 make_audio.py "$WORK/sfx.json" "$WORK/audio.wav"
AUDIO="$WORK/audio.wav"
OUT="out/keyflip-promo-9x16.mp4"
if [ "$LANG_CODE" = "en" ]; then
  : "${PIPER_MODEL:?set PIPER_MODEL to a Piper .onnx voice}"
  python3 make_voice.py "$WORK/sfx.json" "$PIPER_MODEL" "$WORK/voice.wav"
  ffmpeg -y -loglevel error -i "$WORK/audio.wav" -i "$WORK/voice.wav" \
    -filter_complex "[0:a]volume=0.5[bg];[1:a]volume=1.0[v];[bg][v]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" \
    -map "[a]" "$WORK/mixed.wav"
  AUDIO="$WORK/mixed.wav"
  OUT="out/keyflip-promo-en-9x16.mp4"
fi
ffmpeg -y -loglevel error -framerate 30 -i "$WORK/frames/f%05d.jpg" -i "$AUDIO" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -shortest -movflags +faststart "$OUT"
ls -la "$OUT"
