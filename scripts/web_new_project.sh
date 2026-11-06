#!/usr/bin/env bash
# Scaffolds a website project folder. Usage: scripts/web_new_project.sh <short-name>
# Creates campaigns/<YYYY-MM>-<short-name>/ with the standard layout and starter files. Never overwrites.
set -eu
[ $# -eq 1 ] || { echo "Usage: $0 <short-name>"; exit 2; }
name=$(printf '%s' "$1" | tr 'A-Z' 'a-z' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//')
root="campaigns/$(TZ=Asia/Dubai date +%Y-%m)-$name"
[ -e "$root" ] && { echo "Exists already: $root (nothing changed)"; exit 1; }
mkdir -p "$root"/{brief,inputs,references,research,design,copy,site/assets,sources,qa,exports}
cat > "$root/brief/brief.md" <<T
# Brief: $name
Date: $(TZ=Asia/Dubai date +%F)
Request (Rahul's words, verbatim):
Goal and main action:
Audience:
Pages wanted:
Hosting and domain (never publish without approval):
Open questions:
T
cat > "$root/references/reference-sites.md" <<'T'
# Reference websites (3 or more, the style to learn)
Add one URL per line with a note on what Rahul likes about it.
1.
2.
3.
T
cat > "$root/inputs/inputs.md" <<'T'
# Inputs supplied (links and descriptions only, never raw files)
Logo (assets/brand/ in repo):
Photos (Google Drive link):
Text, product lists, certificates (Drive link):
NEEDED FROM RAHUL:
T
echo "Created $root"; ls "$root"
