#!/usr/bin/env bash
# Fails if any staged file is over 5 MB, has a media extension, or looks like it holds a secret.
# Usage: guard_large_files.sh [repo_path]   (default: the git repository of the current directory)
# Run before every commit. Never bypass. If it fails, unstage the file and tell Rahul.
set -u
TARGET="${1:-.}"
if [ ! -d "$TARGET" ]; then echo "GUARD FAIL: not a folder: $TARGET"; exit 1; fi
TOP=$(git -C "$TARGET" rev-parse --show-toplevel 2>/dev/null) || { echo "GUARD FAIL: $TARGET is not inside a git repository, so staged files cannot be checked."; exit 1; }
cd "$TOP" || exit 1
LIMIT=$((5 * 1024 * 1024))
MEDIA_RE='\.(mp4|mov|m4v|avi|mkv|mxf|webm|mp3|wav|aac|m4a|flac|zip|7z|psd|heic|cr2|nef|arw|dng)$'
SECRET_RE='(AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9]{32,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(password|passwd|api[_-]?key|secret|token)[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9/+_-]{12,})'
fail=0
while IFS= read -r f; do
  [ -z "$f" ] && continue
  lower=$(printf '%s' "$f" | tr 'A-Z' 'a-z')
  if printf '%s' "$lower" | grep -Eq "$MEDIA_RE"; then
    echo "GUARD FAIL: media extension staged: $f"; fail=1; continue
  fi
  [ -f "$f" ] || continue
  size=$(wc -c < "$f")
  if [ "$size" -gt "$LIMIT" ]; then
    echo "GUARD FAIL: over 5 MB ($size bytes): $f"; fail=1
  fi
done < <(git diff --cached --name-only --diff-filter=ACMR)

# Secret scan on added lines only (this script is excluded so its own pattern does not match)
if git diff --cached -U0 -- . ':(exclude,glob)**/guard_large_files.sh' | grep -E '^\+[^+]' | grep -Eiq "$SECRET_RE"; then
  echo "GUARD FAIL: possible secret in staged changes. Review with: git diff --cached"; fail=1
fi

if [ "$fail" -ne 0 ]; then
  echo "Guard failed. Unstage the offending file(s) (git reset HEAD <file>) and tell Rahul."; exit 1
fi
echo "Guard OK: no oversized, media or secret-like content staged."
