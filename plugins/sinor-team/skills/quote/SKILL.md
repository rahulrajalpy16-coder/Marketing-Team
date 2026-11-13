---
name: quote
description: Prepare or revise a Sinor quotation from supplied inputs under the controlled sales workflow, then produce the editable source and the requested PDF after independent QA.
argument-hint: "<inputs: client, vessel, scope, prices, QTN number, attached RFQ>"
disable-model-invocation: true
---

Prepare or revise a Sinor quotation from these inputs: $ARGUMENTS

1. Load the `sales-estimation-protocol` skill and follow it (task record, requirement matrix, current scope).
2. Identify the approved template and the exact current scope. If no approved template exists for this scope, say so and report the controlled output as BLOCKED; the standard PDF layout from the `sinor-quotation` skill can still be produced as a DRAFT when the user wants it.
3. Use sourced pricing or mark missing prices as unresolved. Never invent a price, discount, quote number, address or bank detail. Calculate only with `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sales.py" calc <spec>` (or `sinor.py calc`).
4. Deliver the editable source plus the requested PDF after independent QA by the qa-auditor agent. Keep everything marked DRAFT until Rahul approves issue.
