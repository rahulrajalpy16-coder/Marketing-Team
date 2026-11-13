---
name: team-performance
description: Show measured team performance metrics (requirement coverage, first-pass QA, corrections, clarifications, acceptance, cost) computed from recorded task data only.
argument-hint: "[--include-tests]"
---

Resolve the data root first: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" root executive`. If it reports no workspace, tell the user to run `/sinor-team:setup` and stop.

1. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" metrics $ARGUMENTS`.
2. Show the table as printed (it is short). Do not add, estimate or round numbers that are not in the output.
3. Add at most three observations, each tied to a number in the output (for example "2 of 3 corrections were missed-requirement, so intake now checks ..."). If an observation suggests changing agent instructions, skills or routing, propose the change and ask before editing anything in the plugin.
4. If there is no data yet, say so plainly. No em dashes.
