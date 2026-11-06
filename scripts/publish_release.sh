#!/usr/bin/env bash
# Publish a final deliverable as a GitHub Release asset in this private repo and verify it.
# Usage: scripts/publish_release.sh <file> <tag> "<two-line summary>" "<platform | duration | resolution>"
# Tag format: campaign-YYYY-MM-DD-short-name-vN. Requires an authenticated gh.
# Release per-file limit is under 2 GiB (docs.github.com, verified 2026-11-06).
# Never deletes anything. Never makes anything public.
set -euo pipefail
if [ "$#" -lt 4 ]; then sed -n '2,6p' "$0"; exit 2; fi
FILE="$1"; TAG="$2"; SUMMARY="$3"; META="$4"
[ -f "$FILE" ] || { echo "File not found: $FILE"; exit 1; }
command -v gh >/dev/null || { echo "gh not installed"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh is not authenticated. Ask Rahul to connect GitHub in the Claude app settings. Do not request a token in chat."; exit 1; }

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
