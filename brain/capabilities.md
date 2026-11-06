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
| Google Drive | Connected. list_recent_files works and shows HEIC photos (about 1 MB each). download_file_content returns file content as base64 inside the chat context, so only small files are practical. Whether it returns ORIGINAL video bytes, and the largest size that works, are NOT yet tested: waiting for Rahul's small and large test video links. Upload tool create_file exists (base64Content); not tested yet. | tool schemas, list call |
| iCloud | Cannot read. Copy files to the Drive Inbox first. | by design |
| Subagents | Launch successfully (trivial Explore agent returned correctly; claude-code-guide agent returned a sourced answer). | live test |
| Persistent subagent memory | Documented as supported: frontmatter `memory: user|project|local`, project scope stored in .claude/agent-memory/<name>/ (source: https://code.claude.com/docs/en/sub-agents.md, read 2026-11-06). Enabling it auto-enables Read, Write and Edit for that agent. Not yet proven in a real multi-session run, and the container is ephemeral, so only memory that is committed and pushed survives. Added to 9 agents, deliberately not to qa-reviewer. | docs via subagent |
| Platform analytics access | None (assumed, not proven). | n/a |

## Repository visibility warning (2026-11-06)
GitHub API reports repo rahulrajalpy16-coder/Marketing-Team as PUBLIC (visibility: public), though the brief says private. Everything committed is visible to anyone. Nothing confidential has been committed. Do not commit confidential material or deliver finals here until Rahul confirms or changes the visibility. Changing visibility is an account setting, so Rahul decides.

## Delivery fallback while Releases are blocked
1. Keep finals in /tmp/work/<campaign> during the session and offer Drive Outputs upload (create_file) only if the upload test passes and Rahul approves; large files may not fit through the base64 tool.
2. Ask Rahul to run the job from a session type that allows Releases, or tell him the exact limit hit.
3. Never split a video without telling him. Never commit media.
