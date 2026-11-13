---
name: find-reference
description: Search registered Sinor documents (quotations, supplier offers, orders, scopes) and return exact source, page, date, revision and status without treating history as current approval.
argument-hint: "<what to find: client, vessel, equipment, QTN number>"
disable-model-invocation: true
---

Search registered documents for $ARGUMENTS

1. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sales.py" search "<query>"` (add `--approved-only` when only approved records may be used).
2. Read the matching originals, not only the search snippets. Return the exact source, page or sheet, date, revision and status for each hit.
3. Do not interpret a historical price as a current approval. Label every price with its status (supplier cost, offered, ordered, actual), currency, quantities, and whether it is itemized or lump sum.
4. If nothing matches, say so and suggest which documents to onboard with `/sinor-team:onboard`. Never fill the gap from memory.
