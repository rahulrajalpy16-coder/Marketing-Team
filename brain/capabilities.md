# Capabilities (checked 2026-11-06, first run)

Cloud session (Claude Code on the web). Re-run only if something changes.

| Area | Result | Evidence |
|------|--------|----------|
| OS and shell | Ubuntu 24.04.5, bash, Linux 6.18, cloud session | uname, os-release |
| Disk | About 30 GB available (per-session allowance) | df |
| git | Works. git 2.43. Remote reachable. Push to the assigned branch succeeded (commit b0877cd). | git push |
| Default branch | The repo's default branch is claude/new-session-yarexb. No `main` exists. Pushes go to the session's assigned branch. | GitHub REST API |
| GitHub CLI | gh 2.89 installed. `gh auth status` reports the token invalid, and GraphQL is blocked, but REST calls (gh api repos/...) work. | gh auth status, gh api |
| Releases | NOT POSSIBLE in this session type. Creating a draft release returned HTTP 403: "Creating, editing, or deleting releases is not permitted for this session type." Nothing was created, so nothing needed deleting. The GitHub MCP tools only list and read releases. | gh release create |
| Release per-file limit | Each file must be under 2 GiB (official docs). Untestable here because creation is blocked. | docs.github.com about-releases |
| ffmpeg / ffprobe | Installed, 6.1.1. libx264 and aac encoders present. Synthetic test clip encoded, probed, contact-sheeted and loudness-measured successfully. | ffmpeg -encoders, script tests |
| Python | 3.13. Pillow 12.3 and numpy 2.5 present. OpenCV (cv2) missing. | import test |
| Speech-to-text | None installed (whisper, faster-whisper, vosk all missing). Smallest fix: pip install faster-whisper (needs Rahul's approval; model download needs network access to Hugging Face, which may be blocked by the network policy). Until then SRT is hand-built from supplied scripts. | import test |
| Web research | Available: Firecrawl search (run live, returned official GitHub docs), subagent WebFetch (run live). WebSearch, Firecrawl scrape and TinyFish are listed as available but were not run. | tool listing, live calls |
| Google Drive | Connected and working (updated 2026-11-06, second run). Folder listing and search work (query syntax: `parentId = '<id>'`, `title contains '...'`). download_file_content returns ORIGINAL bytes: a 156,424-byte JPG decoded to exactly 156,424 bytes, valid JPEG 960x1280. The tool result is base64 text; when large, the harness saves it to a file under tool-results/ and the file can be decoded with python (json, base64) without reading it into context. Largest size that works: UNKNOWN (only 156 KB tested; no videos in Drive folder yet, and base64 inflates size by about 33 percent). Drive share links are NOT public: a direct curl download returned the Google sign-in page, so the connector is the only route. Upload (create_file with base64Content) exists, NOT tested. | live download and decode test |
| HEIC photos | Initially FAILED (ImageMagick 'Non-existing depth image referenced', ffmpeg and Pillow cannot read iPhone HEIC). FIXED 2026-11-06 with Rahul's approval: pillow-heif 1.8.1 in an isolated venv (/tmp/work/venv, ephemeral per session). All 12 HEIC files decoded. Re-create each session with the two commands in scripts/heic_to_jpg.py, then run that script. | live decode of 12 files |
| iCloud | Private iCloud cannot be read. TESTED 2026-11-07 with a public shared-album link (photos.icloud.com/shared/album/<token>): the page and its cover thumbnail load, but the album's file list and videos are NOT retrievable from here (the shared-stream host derived from the token did not resolve or answered 404; the iCloud web app loads its data through other services). Treat iCloud links as unreadable: ask Rahul to save the files into the Google Drive Adipec26 folder instead. | live test |
| Subagents | Launch successfully (trivial Explore agent returned correctly; claude-code-guide agent returned a sourced answer). | live test |
| Persistent subagent memory | Documented as supported: frontmatter `memory: user|project|local`, project scope stored in .claude/agent-memory/<name>/ (source: https://code.claude.com/docs/en/sub-agents.md, read 2026-11-06). Enabling it auto-enables Read, Write and Edit for that agent. Not yet proven in a real multi-session run, and the container is ephemeral, so only memory that is committed and pushed survives. Added to 9 agents, deliberately not to qa-reviewer. | docs via subagent |
| Platform analytics access | None (assumed, not proven). | n/a |

## Repository visibility warning (2026-11-06)
GitHub API reports repo rahulrajalpy16-coder/Marketing-Team as PUBLIC (visibility: public), though the brief says private. Everything committed is visible to anyone. Nothing confidential has been committed. Do not commit confidential material or deliver finals here until Rahul confirms or changes the visibility. Changing visibility is an account setting, so Rahul decides.

## Delivery fallback while Releases are blocked
1. Keep finals in /tmp/work/<campaign> during the session and offer Drive Outputs upload (create_file) only if the upload test passes and Rahul approves; large files may not fit through the base64 tool.
2. Ask Rahul to run the job from a session type that allows Releases, or tell him the exact limit hit.
3. Never split a video without telling him. Never commit media.

## SEO and analytics tooling check (2026-11-08, digital marketing and SEO plan job)
- Firecrawl scrape and search: work for public site audits (live fetch with maxAge 0 returned page text, metadata and links).
- curl to the public website works through the proxy (robots, sitemaps, headers, redirect chains).
- Google PageSpeed Insights API without a key: HTTP 429 (shared daily quota exceeded). Core Web Vitals NOT MEASURED. Use Search Console data or Rahul's own PSI key.
- Ahrefs, Similarweb, Supermetrics, Canva, HubSpot, Klaviyo connectors: need Rahul to authorise them in Claude connector settings (HubSpot failed to connect). No keyword volume, backlink or competitor traffic data is available until then.
- No access to Search Console, GA4, LinkedIn analytics or Google Business Profile.
