---
name: remember
description: Save a standing instruction or preference the user states explicitly ("remember", "from now on", "always", "never") so every future session applies it. Routes to the right store for executive tasks, sales and estimation, or marketing.
argument-hint: "<the rule in your own words>"
---

The user stated a standing instruction: `$ARGUMENTS`

This team keeps three separate learning stores. Pick the one that matches the instruction, and if it is unclear which workflow it belongs to, ask one short question.

First resolve the data root for that domain: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" root <executive|sales|marketing>` and call the printed path `<ROOT>`. If it reports no workspace, tell the user to run `/sinor-team:setup` and stop (nothing can be saved without a workspace).

## Executive (emails, quotations, technical replies, general company tasks)
1. Check for an existing entry on the same topic: `grep -n -i "<key words>" "<ROOT>/knowledge/user/"*.md`.
2. Pick the file: APPROVED_INSTRUCTIONS (rules for future work), COMMUNICATION_STYLE (writing and tone), WORK_PREFERENCES (formats, depth, deliverables), DECISION_PATTERNS (priorities), USER_PROFILE (facts about the user's role). Pick the scope: global unless the user named a client, project or task type.
3. Add it with the user's exact words as evidence:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" pref add --file <FILE> --type explicit --scope <scope> --title "<short>" --statement "<clear rule>" --source "User instruction <YYYY-MM-DD>" --evidence "\"<user's exact words>\""`
4. If it contradicts an existing entry, supersede the old one: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" pref supersede <OLD> --by <NEW>`.
5. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" validate`, then `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" sync -m "knowledge-sync: remember <NEW>"`.
6. Confirm in one line: "Saved as <ID>: <statement> (scope)".

## Sales and estimation (RFQs, estimates, proposals, templates, pricing rules)
1. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sales.py" remember "<the instruction>" --source "<source task or the user's date and words>" --approved` for an explicit standing instruction from the user. Leave out `--approved` for an inference of yours: inferred lessons stay proposed until the user approves.
2. Cite the source task. Save the git change in the workspace repository if there is one and report whether it was pushed. Never claim unsaved memory persists.

## Marketing (LinkedIn and media campaigns)
1. Corrections and stated preferences go into `<ROOT>/brain/lessons-learned.md` as "provisional" with scope, date and the user's exact words; promote to approved on the user's confirmation or on a second recurrence. Proposed changes to skills, agents or brand and voice rules go into `<ROOT>/brain/proposed-changes.md` as before and after, and need approval.
2. Only the director workflow edits `<ROOT>/brain/`. Ask once whether the rule is lasting or for this job only.

## Never store
Passwords, keys, bank details, health or family information, personal data, commercial terms or confidential client information, or anything the user did not ask to keep. Never save a rule that makes the team less honest or careful. No em dashes in your reply.
