# Lessons learned

Format: date | scope (one-off, this platform, this account, always) | status (provisional, approved) | lesson | trigger or Rahul's exact words.

- 2026-11-06 | always | provisional | The qa-reviewer has no `memory` field because the documented memory feature auto-enables Write and Edit, which would break its read-only independence. | Director decision at bootstrap.
- 2026-11-06 | always | provisional | Google Drive download tool returns base64 inside the chat context, so only small files are practical through it; large originals need another route. | Capability check, see brain/capabilities.md.

- 2026-11-06 | always | provisional | Cloud sessions can push git but this session type cannot create GitHub Releases (HTTP 403), so the Release delivery route needs a different session type or the Drive fallback. Check brain/capabilities.md before promising a download link. | Capability check.
- 2026-11-06 | always | provisional | `gh auth status` can say the token is invalid while REST calls work. Judge capability by a real call, not by auth status. | Capability check.
- 2026-11-06 | always | provisional | Check repository visibility (gh api repos/<owner>/<repo> --jq .visibility) at the start of any delivery job. The repo was found public although described as private. | Capability check.

- 2026-11-06 | always | provisional | Google Drive downloads work for originals: save-to-file then decode base64 with python. Do not Read the saved file. Use `parentId = '<id>'` to list a folder. | Second-run test.
- 2026-11-06 | always | provisional | Rahul's earlier repos hold approved brand material (logo, company profile, style preferences). Look there before asking him for brand files. | Rahul: "you might can retrieve from any of our previous chats or previous repos".

- 2026-11-06 | always | provisional | iPhone HEIC photos with depth maps cannot be decoded by ImageMagick or ffmpeg here. Ask early for approval to install pillow-heif, or ask Rahul to upload JPG copies, so half the folder is not lost. | ADIPEC 2026 job: 7 of 16 photos unusable.
- 2026-11-06 | this account | provisional | Do not write "our" for equipment shown at the stand (DP consoles are listed as MT and NAVIS units in Rahul's layout notes) unless he confirms ownership. Copy QA and my own review caught "our DP console". | ADIPEC 2026 caption review.
- 2026-11-06 | always | provisional | Dictated partner names need a check against Rahul's own repos first (README resolved Fugro and SMT context), then the web. Do not expand acronyms (ADIPEC, MT, SMT) in public copy without a source. | fact-reviewer candidate lessons.
- 2026-11-06 | always | provisional | Inspect photos for incidental on-screen text (media file names, badges, other brands) before using them; list them for Rahul. A file name was visible on the stand video wall in one photo. | Video QA cycle 2 prompt.

(No Rahul corrections yet.)
