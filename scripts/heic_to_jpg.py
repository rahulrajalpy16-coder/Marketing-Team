#!/usr/bin/env python3
"""Convert iPhone HEIC photos to EXIF-oriented JPG copies (originals untouched).

One-time setup per cloud session (approved by Rahul 2026-11-06; isolated, no system change):
  python3 -m venv /tmp/work/venv && /tmp/work/venv/bin/pip install -q pillow pillow-heif
Usage:
  /tmp/work/venv/bin/python scripts/heic_to_jpg.py <heic_dir> <out_dir>
ImageMagick and ffmpeg in this environment cannot read iPhone HEIC files that carry depth maps
(error 'Non-existing depth image referenced'); pillow-heif can. Run on working copies in /tmp, never in the repo.
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    ok = bad = 0
    for f in sorted(src.iterdir()):
        if f.suffix.lower() not in (".heic", ".heif"):
            continue
        try:
            im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
            im.save(dst / (f.stem + ".jpg"), quality=95)
            ok += 1
            print("ok  ", f.name, im.size)
        except Exception as e:  # report, never hide
            bad += 1
            print("FAIL", f.name, e)
    print(f"converted {ok}, failed {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
