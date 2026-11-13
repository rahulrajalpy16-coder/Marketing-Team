#!/usr/bin/env python3
"""ffprobe every media file under a folder and write a manifest CSV with the basics.

Usage: python3 "${CLAUDE_PLUGIN_ROOT}/scripts/probe_media.py" <media_dir> <out.csv>
Writes: filename, relative path, type, size, sha256, width, height, orientation,
duration_s, fps, codec, pix_fmt, audio_codec, status. The Director/media-librarian then
adds subject, quality notes, clip timestamps and selection status by viewing the media.
Run on a COPY of the media in a working folder outside the git repository.
"""
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

EXT = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".mxf", ".webm", ".jpg", ".jpeg",
       ".png", ".heic", ".tif", ".tiff", ".mp3", ".wav", ".m4a", ".aac", ".flac"}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(p: Path) -> dict:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(p)],
        capture_output=True, text=True)
    if r.returncode != 0:
        return {"status": "ffprobe failed: " + r.stderr.strip()[:120]}
    d = json.loads(r.stdout)
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), None)
    a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), None)
    row = {"status": "ok", "duration_s": d.get("format", {}).get("duration", "")}
    if v:
        w, h = v.get("width", 0), v.get("height", 0)
        row.update(width=w, height=h,
                   orientation="portrait" if h > w else "landscape" if w > h else "square",
                   codec=v.get("codec_name", ""), pix_fmt=v.get("pix_fmt", ""))
        try:
            n, dn = v.get("avg_frame_rate", "0/1").split("/")
            row["fps"] = round(float(n) / float(dn), 3) if float(dn) else ""
        except Exception:
            row["fps"] = ""
    if a:
        row["audio_codec"] = a.get("codec_name", "")
    return row


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    cols = ["filename", "path", "type", "size_bytes", "sha256", "width", "height", "orientation",
            "duration_s", "fps", "codec", "pix_fmt", "audio_codec", "status"]
    rows = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.suffix.lower() in EXT:
            row = {"filename": p.name, "path": str(p.relative_to(root)),
                   "type": p.suffix.lower().lstrip("."), "size_bytes": p.stat().st_size,
                   "sha256": sha256(p)}
            row.update(probe(p))
            rows.append(row)
    seen = {}
    for r in rows:
        seen.setdefault(r["sha256"], []).append(r["path"])
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    dups = {k: v for k, v in seen.items() if len(v) > 1}
    print(f"{len(rows)} files probed -> {out}")
    print(f"exact duplicate groups: {len(dups)}")
    for v in dups.values():
        print("  duplicate:", ", ".join(v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
