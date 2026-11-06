# Lessons learned

Format: date | scope (one-off, this platform, this account, always) | status (provisional, approved) | lesson | trigger or Rahul's exact words.

- 2026-11-06 | always | provisional | The qa-reviewer has no `memory` field because the documented memory feature auto-enables Write and Edit, which would break its read-only independence. | Director decision at bootstrap.
- 2026-11-06 | always | provisional | Google Drive download tool returns base64 inside the chat context, so only small files are practical through it; large originals need another route. | Capability check, see brain/capabilities.md.

- 2026-11-06 | always | provisional | Cloud sessions can push git but this session type cannot create GitHub Releases (HTTP 403), so the Release delivery route needs a different session type or the Drive fallback. Check brain/capabilities.md before promising a download link. | Capability check.
- 2026-11-06 | always | provisional | `gh auth status` can say the token is invalid while REST calls work. Judge capability by a real call, not by auth status. | Capability check.
- 2026-11-06 | always | provisional | Check repository visibility (gh api repos/<owner>/<repo> --jq .visibility) at the start of any delivery job. The repo was found public although described as private. | Capability check.

- 2026-11-06 | always | provisional | Google Drive downloads work for originals: save-to-file then decode base64 with python. Do not Read the saved file. Use `parentId = '<id>'` to list a folder. | Second-run test.
- 2026-11-06 | always | provisional | Rahul's earlier repos hold approved brand material (logo, company profile, style preferences). Look there before asking him for brand files. | Rahul: "you might can retrieve from any of our previous chats or previous repos".

(No Rahul corrections yet.)
