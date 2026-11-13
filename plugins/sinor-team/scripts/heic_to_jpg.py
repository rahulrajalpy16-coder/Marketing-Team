#!/usr/bin/env python3
"""Convert iPhone HEIC photos to EXIF-oriented JPG copies (originals untouched).

Needs pillow and pillow-heif. Install them in an isolated virtual environment (ask Rahul first), for example:
  python3 -m venv <work_dir>/venv && <work_dir>/venv/bin/pip install -q pillow pillow-heif
Usage:
  <work_dir>/venv/bin/python "${CLAUDE_PLUGIN_ROOT}/scripts/heic_to_jpg.py" <heic_dir> <out_dir>
ImageMagick and ffmpeg in this environment cannot read iPhone HEIC files that carry depth maps
(error 'Non-existing depth image referenced'); pillow-heif can. Run on working copies outside the git repository.
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

try:
    import pillow_heif
except ImportError:
    sys.exit("pillow-heif is not installed. See the setup note at the top of this script (optional dependency).")

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
