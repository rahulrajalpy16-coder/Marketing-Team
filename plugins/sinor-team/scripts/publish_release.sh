#!/usr/bin/env bash
# Publish a final deliverable as a GitHub Release asset in a private repo and verify it.
# Usage: publish_release.sh <file> <tag> "<two-line summary>" "<platform | duration | resolution>" [repo_path]
# repo_path: any folder inside the target git repository (default: the current directory).
# Tag format: campaign-YYYY-MM-DD-short-name-vN. Requires an authenticated gh.
# Release per-file limit is under 2 GiB (docs.github.com, verified 2026-11-06).
# Never deletes anything. Never makes anything public.
set -euo pipefail
if [ "$#" -lt 4 ]; then sed -n '2,6p' "$0"; exit 2; fi
FILE="$1"; TAG="$2"; SUMMARY="$3"; META="$4"; REPO_PATH="${5:-.}"
[ -f "$FILE" ] || { echo "File not found: $FILE"; exit 1; }
FILE="$(cd "$(dirname "$FILE")" && pwd)/$(basename "$FILE")"
command -v gh >/dev/null || { echo "gh not installed"; exit 1; }
[ -d "$REPO_PATH" ] || { echo "Not a folder: $REPO_PATH"; exit 1; }
cd "$REPO_PATH" || exit 1
git rev-parse --show-toplevel >/dev/null 2>&1 || { echo "$REPO_PATH is not inside a git repository"; exit 1; }
# Note: `gh auth status` can report an invalid token in cloud sessions even when REST calls work,
# so it is not used as a gate. If release creation fails (for example HTTP 403 "not permitted for
# this session type"), report the exact error, offer the Drive Outputs route, and never
# ask Rahul to paste a token in chat.
VIS=$(gh api "repos/$(git config --get remote.origin.url | sed -E 's#.*github.com[/:]##; s#\.git$##')" --jq .visibility 2>/dev/null || echo unknown)
if [ "$VIS" != "private" ]; then echo "WARNING: repository visibility is '$VIS', not private. Ask Rahul before uploading a deliverable here."; [ "${ALLOW_NONPRIVATE:-0}" = "1" ] || exit 1; fi

SIZE=$(wc -c < "$FILE")
MAX=$((2 * 1024 * 1024 * 1024))
if [ "$SIZE" -ge "$MAX" ]; then echo "File is $SIZE bytes, at or above the 2 GiB Release limit. Offer a smaller export or the Drive Outputs route."; exit 1; fi
SHA=$(sha256sum "$FILE" | awk '{print $1}')
NAME=$(basename "$FILE")
NOTES=$(printf '%s\n\nSpec: %s\nFile: %s\nSize: %s bytes\nSHA-256: %s\n' "$SUMMARY" "$META" "$NAME" "$SIZE" "$SHA")

gh release create "$TAG" "$FILE" --title "$TAG" --notes "$NOTES"

# Verify: list the release and compare asset name and size
ASSET=$(gh release view "$TAG" --json assets,url -q ".assets[] | select(.name==\"$NAME\") | [.name,.size] | @tsv")
URL=$(gh release view "$TAG" --json url -q .url)
echo "Local : $NAME $SIZE bytes sha256=$SHA"
echo "Remote: $ASSET"
REMOTE_SIZE=$(printf '%s' "$ASSET" | awk -F'\t' '{print $2}')
if [ "$REMOTE_SIZE" = "$SIZE" ]; then echo "VERIFIED: asset name and size match."; else echo "MISMATCH: do not report success."; exit 1; fi
echo "Release page: $URL"
echo "Direct link : $URL/../download/$TAG/$NAME  (private repo: opens while signed into GitHub)"
