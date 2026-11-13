#!/usr/bin/env python3
"""Extract frames at intervals from a video and tile them into one contact sheet JPEG.

Usage: python3 "${CLAUDE_PLUGIN_ROOT}/scripts/contact_sheet.py" <video> <out.jpg> [interval_s=2] [cols=5] [thumb_w=320]
Each tile is labeled with its timestamp. Keep the output small (it may be committed to
campaigns/<name>/qa/ if under 5 MB). Reports exactly how many frames were sampled.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw


def duration(video: str) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", video], capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    video, out = sys.argv[1], Path(sys.argv[2])
    interval = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
    cols = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    tw = int(sys.argv[5]) if len(sys.argv) > 5 else 320
    dur = duration(video)
    times = []
    t = 0.0
    while t < dur:
        times.append(t)
        t += interval
    tiles = []
    with tempfile.TemporaryDirectory() as td:
        for i, t in enumerate(times):
            fp = Path(td) / f"f{i:04d}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                            "-vf", f"scale={tw}:-2", "-y", str(fp)], check=False)
            if fp.exists():
                im = Image.open(fp).convert("RGB")
                ImageDraw.Draw(im).text((6, 6), f"{t:.1f}s", fill=(255, 255, 0))
                tiles.append(im.copy())
    if not tiles:
        print("No frames extracted.")
        return 1
    th = max(im.height for im in tiles)
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (0, 0, 0))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=80)
    print(f"Sampled {len(tiles)} frames every {interval}s of {dur:.1f}s -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
