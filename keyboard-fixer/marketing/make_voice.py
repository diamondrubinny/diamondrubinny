"""Synthesizes the narration locally with Piper (offline TTS) and places each line at its start time.
Usage: python3 make_voice.py sfx.json voice_model.onnx out.wav
Requires: pip install piper-tts, a Piper voice (.onnx + .onnx.json), ffmpeg."""
import json, subprocess, sys, tempfile, wave, os
import numpy as np

SR = 44100
data = json.load(open(sys.argv[1], encoding='utf8'))
model, out = sys.argv[2], sys.argv[3]
total = np.zeros(int(SR * data['duration']))

def dur(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]).decode())

with tempfile.TemporaryDirectory() as tmp:
    for i, (start, end, text) in enumerate(data['narration']):
        raw = os.path.join(tmp, f'{i}.wav')
        subprocess.run([sys.executable, '-m', 'piper', '-m', model, '-f', raw], input=text.encode(), check=True, capture_output=True)
        window = end - start - 0.25
        tempo = min(1.35, max(1.0, dur(raw) / window))
        fit = os.path.join(tmp, f'{i}_fit.wav')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-filter:a', f'atempo={tempo:.3f}', '-ar', str(SR), '-ac', '1', fit], check=True)
        with wave.open(fit) as w:
            pcm = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float64) / 32768
        k = int((start + 0.08) * SR)
        seg = pcm[: max(0, len(total) - k)]
        total[k:k + len(seg)] += seg
        print(f'line {i}: {dur(fit):.2f}s in {end - start:.1f}s window (tempo {tempo:.2f})')

total = total / (np.max(np.abs(total)) or 1) * 0.9
with wave.open(out, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((total * 32767).astype('<i2').tobytes())
