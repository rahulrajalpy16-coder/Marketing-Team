---
name: onboard
description: Register supplied Sinor company references (brand, templates, price history, technical scopes, commercial rules) into the sales workspace, retaining originals and flagging what still needs approval.
argument-hint: "<the files you attached, and which of them are approved>"
disable-model-invocation: true
---

Register the supplied Sinor files: $ARGUMENTS

1. Resolve the sales data root with `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" root sales`. If it reports no workspace, tell the user to run `/sinor-team:setup` and stop.
2. Follow the bundled onboarding guide at `${CLAUDE_PLUGIN_ROOT}/references/sales-onboarding.md`. Retain originals unchanged (content-addressed); never edit, move or delete a supplied original.
3. Register each file with `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sales.py" register <file> --category <category> --reference <ref> --status draft`. Use `--status approved` only when Rahul gave evidence of approval; a filename never establishes approval.
4. Inspect extraction quality against the source. Scanned PDFs need OCR or manual review; images, drawings, DOCX headers and complex spreadsheets need visual inspection. CLI extraction is search assistance, not full technical interpretation.
5. Propose categories and template mappings, and identify missing approvals. List what is still missing (for example the approved templates QF-01 to QF-04 are not supplied unless the user attaches them). Never invent them.
6. Keep the workspace repository PRIVATE before committing commercial records. Report persistence status honestly.
