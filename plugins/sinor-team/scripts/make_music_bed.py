#!/usr/bin/env python3
"""Generate an ORIGINAL instrumental music bed (no samples, no third-party music, so no licensing issue).

Warm pad + plucked arpeggio with a ping-pong echo + soft bass, and from bar 3 a gentle kick and hats with sidechain
pumping. Key A minor, progression Am - F - C - G, one chord per bar. Cuts in a video can land on the beat grid.

Usage: python3 "${CLAUDE_PLUGIN_ROOT}/scripts/make_music_bed.py" <out.wav> <duration_s> [bpm=100] [seed=1]
Then normalise for LinkedIn (about -14 LUFS integrated, true peak below -1 dBTP):
  ffmpeg -i out.wav -af loudnorm=I=-14:TP=-1.5:LRA=7 -ar 48000 final.wav
Honest limit: it is synthesised, so it sounds like a clean corporate bed, not a produced track. Listen before posting.
"""
import sys
import wave

import numpy as np

SR = 48000


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    out, dur = sys.argv[1], float(sys.argv[2])
    bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 100.0
    rng = np.random.default_rng(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
    beat = 60.0 / bpm
    bar = 4 * beat
    n = int(dur * SR) + SR
    t = np.arange(n) / SR
    L, R = np.zeros(n, np.float32), np.zeros(n, np.float32)
    pad_l, pad_r = np.zeros(n, np.float32), np.zeros(n, np.float32)
    arp_l, arp_r = np.zeros(n, np.float32), np.zeros(n, np.float32)
    bass = np.zeros(n, np.float32)
    kick = np.zeros(n, np.float32)
    hats = np.zeros(n, np.float32)
    clap = np.zeros(n, np.float32)
    riser = np.zeros(n, np.float32)
    chords = [(57, 60, 64, 45), (53, 57, 60, 41), (60, 64, 67, 48), (55, 59, 62, 43)]  # Am F C G (3 notes + bass root)
    n_bars = int(dur / bar) + 2

    def add(dst, start, sig):
        i = int(start * SR)
        j = min(n, i + len(sig))
        if i < n:
            dst[i:j] += sig[: j - i]

    for b in range(n_bars):
        c = chords[b % 4]
        t0 = b * bar
        # ---- pad: slow attack, overlaps next chord
        seg = int((bar + 0.9) * SR)
        tt = np.arange(seg) / SR
        env = np.minimum(tt / 0.55, 1.0) * np.clip((bar + 0.9 - tt) / 0.9, 0, 1)
        for m in c[:3]:
            f = midi(m)
            for side, det in ((0, 0.9985), (1, 1.0015)):
                w = (np.sin(2 * np.pi * f * det * tt) + 0.28 * np.sin(2 * np.pi * 2 * f * det * tt + 0.7) +
                     0.10 * np.sin(2 * np.pi * 3 * f * det * tt + 1.9)) * env * 0.10
                add(pad_l if side == 0 else pad_r, t0, w.astype(np.float32))
        # ---- bass: quarter notes
        for q in range(4):
            tt2 = np.arange(int(0.5 * SR)) / SR
            f = midi(c[3])
            w = (np.sin(2 * np.pi * f * tt2) + 0.25 * np.sin(2 * np.pi * 2 * f * tt2)) * np.exp(-tt2 / 0.28) * np.minimum(tt2 / 0.01, 1) * 0.30
            add(bass, t0 + q * beat, w.astype(np.float32))
        # ---- arpeggio: 8th notes up/down the chord one octave higher
        order = [0, 1, 2, 1, 0, 2, 1, 2]
        for k, idx in enumerate(order):
            tt3 = np.arange(int(0.6 * SR)) / SR
            f = midi(c[idx] + 12)
            w = (np.sin(2 * np.pi * f * tt3) + 0.30 * np.sin(2 * np.pi * 2 * f * tt3) + 0.08 * np.sin(2 * np.pi * 3 * f * tt3))
            w = w * np.exp(-tt3 / 0.20) * np.minimum(tt3 / 0.004, 1) * 0.17
            pan = 0.5 + (0.28 if k % 2 == 0 else -0.28)
            add(arp_l, t0 + k * beat / 2, (w * (1 - pan)).astype(np.float32))
            add(arp_r, t0 + k * beat / 2, (w * pan).astype(np.float32))
        # ---- drums from bar 3 (4.8 s at 100 BPM): kick on every beat, hats on the off-beat
        if b >= 1:
            for q in range(4):
                tk = np.arange(int(0.30 * SR)) / SR
                f = 48 + 100 * np.exp(-tk / 0.035)
                ph = 2 * np.pi * np.cumsum(f) / SR
                add(kick, t0 + q * beat, (np.sin(ph) * np.exp(-tk / 0.11) * 0.62).astype(np.float32))
                th = np.arange(int(0.07 * SR)) / SR
                noise = rng.normal(0, 1, len(th)).astype(np.float32)
                hp = np.diff(noise, prepend=0)
                hp = np.diff(hp, prepend=0)
                add(hats, t0 + q * beat + beat / 2, (hp * np.exp(-th / 0.016) * 0.045).astype(np.float32))
            if b >= 2:  # clap on beats 2 and 4
                for q in (1, 3):
                    tc = np.arange(int(0.20 * SR)) / SR
                    nz = rng.normal(0, 1, len(tc)).astype(np.float32)
                    nz = np.diff(nz, prepend=0)
                    burst = (np.exp(-tc / 0.045) + 0.6 * np.exp(-((tc - 0.012) ** 2) / 0.00002)) * nz * 0.10
                    add(clap, t0 + q * beat, burst.astype(np.float32))

    # ---- riser over the first bar (opening title) into the first beat drop
    rl = int(bar * SR)
    rn = rng.normal(0, 1, rl).astype(np.float32)
    rn = np.diff(rn, prepend=0)
    swell = (np.arange(rl) / rl) ** 2.2
    rf = 220 + 900 * (np.arange(rl) / rl) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(rf) / SR).astype(np.float32)
    riser[:rl] = (rn * 0.05 + tone * 0.04) * swell
    riser[:rl] *= np.clip((rl - np.arange(rl)) / (0.02 * SR), 0, 1)
    # ---- sidechain pump: duck pad/arp/bass under the kick
    duck = np.ones(n, np.float32)
    kick_env = np.abs(kick)
    k = int(0.09 * SR)
    smooth_k = np.convolve(kick_env, np.ones(k, np.float32) / k, mode="same")
    duck -= np.clip(smooth_k * 1.6, 0, 0.42)
    # ---- one-pole low-pass on pad and arp (about 4.5 kHz) to keep it soft on phone speakers
    def lp(x, a=0.30):
        y = np.empty_like(x)
        acc = 0.0
        for i in range(0, len(x)):
            acc += a * (x[i] - acc)
            y[i] = acc
        return y
    pad_l, pad_r = lp(pad_l), lp(pad_r)
    arp_l, arp_r = lp(arp_l, 0.35), lp(arp_r, 0.35)

    # ---- ping-pong echo on the arpeggio (dotted 8th)
    d = int(0.75 * beat * SR)
    el, er = arp_l.copy(), arp_r.copy()
    for rep in range(1, 5):
        g = 0.38 ** rep
        sh = d * rep
        if sh < n:
            if rep % 2 == 1:
                er[sh:] += arp_l[: n - sh] * g
                el[sh:] += arp_r[: n - sh] * g * 0.6
            else:
                el[sh:] += arp_l[: n - sh] * g
                er[sh:] += arp_r[: n - sh] * g * 0.6
    # ---- plate-style reverb (synthetic decaying-noise impulse response) on pad, arp and claps
    ir_n = int(1.7 * SR)
    ti = np.arange(ir_n) / SR
    size = 1 << int(np.ceil(np.log2(n + ir_n)))
    def reverb(x, seed):
        g = np.random.default_rng(seed)
        ir = g.normal(0, 1, ir_n).astype(np.float32) * np.exp(-ti / 0.42)
        ir = np.diff(ir, prepend=0)  # lighter low end
        ir /= np.abs(ir).sum() ** 0.5 * 18
        return np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:n].astype(np.float32)
    wet_l = reverb(el + pad_l + clap + riser, 7)
    wet_r = reverb(er + pad_r + clap + riser, 8)
    L = (pad_l + el + bass) * duck + kick + hats + clap + riser + 0.9 * wet_l
    R = (pad_r + er + bass) * duck + kick + hats + clap + riser + 0.9 * wet_r
    # intro swell and end fade
    fade_in = np.clip(t / 1.2, 0, 1)
    fade_out = np.clip((dur - t) / 2.2, 0, 1)
    g = fade_in * fade_out
    L, R = np.tanh(1.25 * L * g), np.tanh(1.25 * R * g)
    L, R = L[: int(dur * SR)], R[: int(dur * SR)]
    peak = max(np.abs(L).max(), np.abs(R).max(), 1e-6)
    stereo = (np.stack([L, R], axis=1) / peak * 0.89 * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())
    print("wrote", out, f"{dur:.1f}s {bpm:.0f} BPM")
    return 0


if __name__ == "__main__":
    sys.exit(main())
