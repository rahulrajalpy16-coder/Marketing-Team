#!/bin/bash
# Build the upload zip for claude.ai / Cowork (and for sending the plugin to one person).
# The plugin folder is the single top-level entry of the archive, as Anthropic's upload accepts.
# Usage: tools/package_plugin.sh [output-dir]   (default: ./dist)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUG="$HERE/plugins/sinor-team"
OUT="${1:-$HERE/dist}"
VER="$(python3 -c "import json,sys;print(json.load(open('$PLUG/.claude-plugin/plugin.json'))['version'])")"
mkdir -p "$OUT"
ZIP="$OUT/sinor-team-$VER.zip"
rm -f "$ZIP"
cd "$HERE/plugins"
zip -qr "$ZIP" sinor-team -x '*/__pycache__/*' '*.pyc' '*/.pytest_cache/*' '*/.DS_Store'
unzip -tq "$ZIP"
echo "built $ZIP ($(du -h "$ZIP" | cut -f1), $(unzip -Z1 "$ZIP" | grep -vc '/$') files)"
