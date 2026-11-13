---
name: correct-learning
description: Correct an inaccurate preference or lesson the team learned. Use when the user says a learned preference or lesson is wrong, too broad, or outdated.
argument-hint: "<PREF/LES id or topic> <what is actually right>"
---

The user wants to correct something the team learned: `$ARGUMENTS`

Resolve the data root first: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" root executive` and call the printed path `<ROOT>`. If it reports no workspace, tell the user to run `/sinor-team:setup` and stop.

1. Identify the entry. If an ID is given, show it with `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" pref list --all` or `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" lesson list --all` (grep for the ID). If a topic is given, search: `grep -n -i "<topic>" "<ROOT>/knowledge/user/"*.md`. If more than one entry could match, list them (ID and one line each) and ask the user which one, then stop.
2. Apply the correction exactly as the user stated it (their words are the evidence):
   - Wrong statement: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" pref update <ID> --statement "<corrected>" --evidence "User correction <date>: \"<their words>\"" --type explicit`
   - Too broad: narrow it with `--scope client:<x>` or `task-type:<x>`.
   - Replaced by a new rule: add the new rule with `pref add --type explicit ...`, then `pref supersede <OLD> --by <NEW>`.
   - Wrong lesson: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" lesson update <ID> --lesson "<corrected>"` or `--status retired`.
   - The user says it should not exist at all: follow the `forget-preference` skill instead.
3. Record the correction: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" correction add --title "Learning corrected: <ID>" --feedback "<user's words>" --category other --wrong "<what the entry said>" --fix "<what changed>"`.
4. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" validate`, then `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" sync -m "knowledge-sync: corrected <ID>"`.
5. Reply in two lines: the entry before, the entry after. No em dashes.
