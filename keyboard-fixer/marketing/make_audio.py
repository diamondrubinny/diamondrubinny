"""Synthesizes the sound-effects track and a soft music bed (no external audio; royalty-free by construction).
Usage: python3 make_audio.py sfx.json out.wav"""
import json, sys, wave
import numpy as np

SR = 44100
data = json.load(open(sys.argv[1]))
dur = data['duration']
n = int(SR * dur)
rng = np.random.default_rng(7)
mix = np.zeros(n)

def put(sig, t, gain=1.0):
    i = int(t * SR)
    if i >= n:
        return
    j = min(n, i + len(sig))
    mix[i:j] += sig[: j - i] * gain

def env(length, attack=0.003, decay=8.0):
    x = np.arange(length) / SR
    return np.minimum(1, x / attack) * np.exp(-decay * x)

def click():
    L = int(0.05 * SR)
    noise = rng.standard_normal(L) * env(L, 0.001, 90)
    tone = np.sin(2 * np.pi * 1800 * np.arange(L) / SR) * env(L, 0.001, 70)
    return 0.5 * noise + 0.5 * tone

def pop():
    L = int(0.18 * SR)
    x = np.arange(L) / SR
    f = 500 + 900 * np.exp(-25 * x)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(L, 0.002, 20)

def whoosh():
    L = int(0.5 * SR)
    x = np.arange(L) / SR
    noise = rng.standard_normal(L)
    k = np.ones(40) / 40
    sm = np.convolve(noise, k, 'same')
    return sm * np.sin(np.pi * x / 0.5) ** 2 * 2.5

def flip():
    L = int(0.22 * SR)
    x = np.arange(L) / SR
    f = 300 + 1400 * x / 0.22
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(L, 0.005, 14) * 0.7

def ding():
    L = int(0.9 * SR)
    x = np.arange(L) / SR
    s = np.sin(2 * np.pi * 988 * x) + 0.6 * np.sin(2 * np.pi * 1480 * x) + 0.3 * np.sin(2 * np.pi * 1976 * x)
    return s * env(L, 0.004, 4.5) * 0.5

def buzz():
    L = int(0.3 * SR)
    x = np.arange(L) / SR
    s = np.sign(np.sin(2 * np.pi * 120 * x)) * 0.4 + np.sin(2 * np.pi * 95 * x) * 0.4
    return s * env(L, 0.005, 7)

makers = {'click': (click, 0.55), 'pop': (pop, 0.7), 'whoosh': (whoosh, 0.5), 'flip': (flip, 0.6), 'ding': (ding, 0.8), 'buzz': (buzz, 0.5)}
for e in data['sfx']:
    fn, g = makers[e['type']]
    put(fn(), e['t'], g)

# --- music bed: Am - F - C - G, 110 bpm, soft pad + bass + light pulse
bpm = 110
beat = 60 / bpm
chords = [(220.0, [220.0, 261.63, 329.63]), (174.61, [174.61, 220.0, 261.63]), (130.81, [196.0, 261.63, 329.63]), (196.0, [196.0, 246.94, 293.66])]
music = np.zeros(n)
bar = 0
t = 0.0
while t < dur:
    root, notes = chords[bar % 4]
    L = int(4 * beat * SR)
    x = np.arange(L) / SR
    pad = sum(np.sin(2 * np.pi * f * x) + 0.4 * np.sin(2 * np.pi * 2 * f * x) for f in notes) / len(notes)
    pad *= np.minimum(1, x / 0.25) * np.minimum(1, (4 * beat - x) / 0.25)
    i = int(t * SR); j = min(n, i + L)
    music[i:j] += pad[: j - i] * 0.30
    bass = np.sin(2 * np.pi * (root / 2) * x) * np.exp(-1.2 * x)
    music[i:j] += bass[: j - i] * 0.35
    for b in range(4):
        tb = t + b * beat
        k = int(tb * SR)
        if k < n:
            Lk = int(0.12 * SR)
            xk = np.arange(Lk) / SR
            kick = np.sin(2 * np.pi * (110 * np.exp(-18 * xk) + 45) * xk) * np.exp(-22 * xk)
            seg = min(Lk, n - k)
            music[k:k + seg] += kick[:seg] * 0.30
        th = tb + beat / 2
        kh = int(th * SR)
        if kh < n:
            Lh = int(0.04 * SR)
            hat = rng.standard_normal(Lh) * np.exp(-90 * np.arange(Lh) / SR)
            seg = min(Lh, n - kh)
            music[kh:kh + seg] += hat[:seg] * 0.05
    t += 4 * beat
    bar += 1
fade = np.ones(n)
fi = int(1.0 * SR); fo = int(1.5 * SR)
fade[:fi] = np.linspace(0, 1, fi)
fade[-fo:] = np.linspace(1, 0, fo)
mix += music * fade * 0.38

peak = np.max(np.abs(mix)) or 1
mix = mix / peak * 0.85
pcm = (mix * 32767).astype('<i2')
with wave.open(sys.argv[2], 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('audio ok', dur)
