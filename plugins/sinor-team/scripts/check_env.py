#!/usr/bin/env python3
"""Report which Python modules and command line tools the sinor-team scripts can use.

Read only: nothing is installed or changed. Exit code is always 0; read the report.
Usage: python3 check_env.py [--json]
"""
import importlib.util
import json
import shutil
import sys

MODULES = [
    ("reportlab", "quotation PDFs (build_quotation.py)", True),
    ("pypdf", "reading PDFs (sales.py register)", True),
    ("docx", "python-docx: Word files (sales.py register and fill)", True),
    ("openpyxl", "Excel files (sales.py register)", True),
    ("PIL", "Pillow: images (contact_sheet.py, heic_to_jpg.py)", True),
    ("numpy", "audio synthesis (make_music_bed.py)", True),
    ("pillow_heif", "iPhone HEIC photos (heic_to_jpg.py), optional", False),
]
BINARIES = [
    ("ffmpeg", "video and audio (loudness_check.py, contact_sheet.py)", True),
    ("ffprobe", "media inspection (probe_media.py, contact_sheet.py)", True),
    ("pdftotext", "PDF text for lint of PDFs (sinor.py lint)", False),
    ("pdftoppm", "PDF to image for visual checks", False),
    ("git", "knowledge sync and release guard", True),
    ("gh", "GitHub Releases (publish_release.sh)", False),
]


def main() -> int:
    report = {"python": sys.version.split()[0], "modules": {}, "binaries": {}}
    for name, why, core in MODULES:
        report["modules"][name] = {"present": importlib.util.find_spec(name) is not None,
                                   "used_for": why, "required": core}
    for name, why, core in BINARIES:
        path = shutil.which(name)
        report["binaries"][name] = {"present": bool(path), "path": path, "used_for": why, "required": core}
    if "--json" in sys.argv[1:]:
        print(json.dumps(report, indent=2))
        return 0
    print(f"Python {report['python']}")
    print("\nPython modules:")
    for n, v in report["modules"].items():
        print(f"  {'OK     ' if v['present'] else 'MISSING'} {n}: {v['used_for']}")
    print("\nBinaries:")
    for n, v in report["binaries"].items():
        print(f"  {'OK     ' if v['present'] else 'MISSING'} {n}: {v['used_for']}")
    miss = [n for n, v in {**report["modules"], **report["binaries"]}.items() if not v["present"] and v["required"]]
    print("\nMissing required items: " + (", ".join(miss) if miss else "none"))
    print("Nothing was installed. Install with: python3 -m pip install -r requirements.txt (ask first).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
