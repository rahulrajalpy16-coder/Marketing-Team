---
name: team-status
description: Show open task records for executive and sales work, open marketing campaigns, the latest QA results, and whether learned knowledge is synced to the shared workspace repository.
---

Report only what is recorded on disk. Do not fabricate live worker telemetry, model names, owners or progress.

1. Resolve the data roots: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" detect` (JSON). Use only the domains it found; say which domains are missing.
2. Executive root: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" task list` (open tasks) and `ls -t "<EXECUTIVE_ROOT>/quality/audit-reports" | head -5` (latest QA reports).
3. Sales root: read the task folders under `<SALES_ROOT>/tasks/` and report active owners, dependencies, requested and observed model (only where recorded), outputs and blockers. Latest audits are under `<SALES_ROOT>/quality/`.
4. Marketing root: list `<MARKETING_ROOT>/campaigns/*/` with each campaign's manifest or `qa/retro.md` status if present.
5. Sync check, run inside the workspace repository: `git fetch -q origin` then `git status --short` (uncommitted knowledge) and `git log --oneline -3 origin/HEAD`. If the workspace is not a git repository, say so.
6. Reply in at most 10 short lines: open tasks per domain, last QA verdicts, whether knowledge is fully synced. If unsynced executive changes exist, offer to run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" sync`. No em dashes.
