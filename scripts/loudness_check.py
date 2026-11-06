#!/usr/bin/env python3
"""Measure integrated loudness (LUFS), true peak (dBTP) and loudness range with ffmpeg loudnorm.

Usage: python3 scripts/loudness_check.py <media_file> [target_lufs=-14] [max_tp=-1]
Measurement only; nothing is modified. Prints PASS/CHECK against the working targets.
The targets are starting points, not platform guarantees: confirm in brain/platform-specs.md.
"""
import json
import re
import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    f = sys.argv[1]
    target = float(sys.argv[2]) if len(sys.argv) > 2 else -14.0
    max_tp = float(sys.argv[3]) if len(sys.argv) > 3 else -1.0
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", f, "-vn", "-af",
                        "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"\{\s*\"input_i\".*?\}", r.stderr, re.S)
    if not m:
        print("No loudness data (no audio stream?).")
        print(r.stderr[-400:])
        return 1
    d = json.loads(m.group(0))
    i, tp, lra = float(d["input_i"]), float(d["input_tp"]), float(d["input_lra"])
    print(f"Integrated: {i:.1f} LUFS | True peak: {tp:.1f} dBTP | LRA: {lra:.1f} LU")
    ok_i = abs(i - target) <= 1.5
    ok_tp = tp <= max_tp
    print(f"Loudness within +/-1.5 LU of {target}: {'PASS' if ok_i else 'CHECK'}")
    print(f"True peak at or below {max_tp} dBTP: {'PASS' if ok_tp else 'CHECK'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
