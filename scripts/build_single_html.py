#!/usr/bin/env python3
"""Pack a multi-file static website into ONE self-contained HTML file (opens by double-click, works offline).

Usage: python3 scripts/build_single_html.py <src_dir> <out_file.html>

What it does
- Replaces <link rel="stylesheet" href="x.css"> with an inline <style>; url(...) references inside the CSS to local
  files (fonts, images) become data: URIs.
- Replaces <script src="x.js"></script> with an inline <script> (order preserved; "</script" is escaped).
- Collects every file under <src_dir>/media/ into window.__ASSETS = {"media/..": {t: mime, d: base64}}, inserted before
  the other scripts. The page resolves assets with A('media/...') (see js/assets.js in the source), which decodes once
  and returns a cached blob: URL. Videos and images therefore work from file:// with no network.
- Reports the final size and any local references it could not inline.

Media and personal content stay OUT of the git repository: run it on a source folder under /tmp/work and hand the
output file to the owner. Never commit the output.
"""
import base64
import json
import mimetypes
import os
import re
import sys

MIME = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".gif": "image/gif",
    ".svg": "image/svg+xml", ".mp4": "video/mp4", ".webm": "video/webm", ".woff2": "font/woff2", ".woff": "font/woff",
    ".mp3": "audio/mpeg", ".json": "application/json",
}


def mime_of(path):
    ext = os.path.splitext(path)[1].lower()
    return MIME.get(ext) or mimetypes.guess_type(path)[0] or "application/octet-stream"


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def inline_css(css, base_dir):
    def repl(m):
        ref = m.group(2).strip()
        if re.match(r"^(data:|https?:|//|#)", ref):
            return m.group(0)
        p = os.path.normpath(os.path.join(base_dir, ref.split("?")[0].split("#")[0]))
        if not os.path.isfile(p):
            print("WARN css url not found:", ref)
            return m.group(0)
        return "url(data:%s;base64,%s)" % (mime_of(p), b64(p))

    return re.sub(r"url\(\s*(['\"]?)([^)'\"]+)\1\s*\)", repl, css)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    html = read(os.path.join(src, "index.html"))

    # 1. stylesheets
    def link_repl(m):
        tag = m.group(0)
        if not re.search(r'rel=["\']stylesheet["\']', tag):
            return tag
        href = re.search(r'href=["\']([^"\']+)["\']', tag)
        if not href or re.match(r"^(https?:|//)", href.group(1)):
            return tag
        p = os.path.join(src, href.group(1))
        css = inline_css(read(p), os.path.dirname(p))
        return "<style>\n" + css + "\n</style>"

    html = re.sub(r"<link\b[^>]*>", link_repl, html)

    # 2. scripts
    def script_repl(m):
        attrs, = m.groups()
        sm = re.search(r'src=["\']([^"\']+)["\']', attrs)
        if not sm or re.match(r"^(https?:|//)", sm.group(1)):
            return m.group(0)
        code = read(os.path.join(src, sm.group(1))).replace("</script", "<\\/script")
        other = re.sub(r'\s*src=["\'][^"\']+["\']', "", attrs)
        return "<script%s>\n%s\n</script>" % (other, code)

    html = re.sub(r"<script\b([^>]*)>\s*</script>", script_repl, html)

    # 3. media map
    assets = {}
    media_dir = os.path.join(src, "media")
    for root, _, files in os.walk(media_dir):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            key = os.path.relpath(p, src).replace(os.sep, "/")
            assets[key] = {"t": mime_of(p), "d": b64(p)}
    asset_tag = "<script>window.__ASSETS=" + json.dumps(assets, separators=(",", ":")) + ";</script>\n"
    first_script = html.find("<script")
    if first_script == -1:
        html = html.replace("</head>", asset_tag + "</head>", 1)
    else:
        html = html[:first_script] + asset_tag + html[first_script:]

    # 4. report leftovers
    left = re.findall(r'(?:src|href)=["\'](?!https?:|mailto:|tel:|#|data:|javascript:)([^"\']+)["\']', html)
    left = [x for x in left if not x.startswith(("#", "?"))]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s  %.2f MB  (%d media files, %.2f MB base64)" % (
        out, os.path.getsize(out) / 1048576, len(assets), sum(len(a["d"]) for a in assets.values()) / 1048576))
    if left:
        print("WARN local references left in the HTML (not inlined):", sorted(set(left))[:12])


if __name__ == "__main__":
    main()
