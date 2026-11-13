---
name: what-you-learned
description: Show what the team has learned about the user recently (lessons, preference changes, corrections) with the evidence behind each item.
argument-hint: "[days, default 30]"
---

Resolve the data root first: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" root executive`. If it reports no workspace, tell the user to run `/sinor-team:setup` and stop.

1. Arguments given: `$ARGUMENTS`. Let N be that number of days, or 30 if it is empty or not a number. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" learned --days N`.
2. Present the result for a phone screen:
   - **Lessons**: ID, the lesson in one line, why (evidence), status (tentative or active), times applied and helped.
   - **Preferences added or changed**: ID, statement, type (explicit means you said it; observed means seen repeatedly; tentative means a single inference used only as a hint), evidence.
   - **Corrections you gave**: date, your words, what category of problem it was.
3. If there is nothing in the window, say so and mention the total counts from `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" pref list` and `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" lesson list`.
4. End with one line: "To fix any item: /sinor-team:correct-learning <ID> <what is right>. To delete: /sinor-team:forget-preference <ID>."

Do not invent or summarise items that the tool did not print. No em dashes.
