---
name: forget-preference
description: Permanently remove a learned preference or lesson from the team's knowledge files at the user's request.
argument-hint: "<PREF/LES id or topic>"
---

The user wants the team to forget: `$ARGUMENTS`

Resolve the data root first: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" root executive` and call the printed path `<ROOT>`. If it reports no workspace, tell the user to run `/sinor-team:setup` and stop.

1. Find the entry (ID, or `grep -n -i "<topic>" "<ROOT>/knowledge/user/"*.md`). Show the matching entry or entries (ID and statement). If the request is ambiguous or matches several, ask which one(s) and stop.
2. If the user named it unambiguously (an ID, or a single clear match), proceed without a further confirmation: they already asked.
3. Remove it:
   - Preference: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" pref forget <ID> --reason "user request <date>"`
   - Lesson: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" lesson update <ID> --status retired` and then delete its block from `<ROOT>/knowledge/user/LEARNED_LESSONS.md` with the Edit tool; regenerate with `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" registry`.
   The tool removes the content and keeps only a tombstone (ID and date, no content) so the ID is never reused.
4. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" validate`, then `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" sync -m "knowledge-sync: forgot <ID> at user request"`.
5. Tell the user honestly, in short lines:
   - It is removed from the team's active knowledge and will not be used again.
   - Earlier versions still exist in the private workspace repository's git history. Fully purging history needs a history rewrite and force push, which this team will not do without the user's explicit approval.
   - Claude's own account-level memory (if enabled in the Claude app) is separate and is managed in the app's settings.
No em dashes.
