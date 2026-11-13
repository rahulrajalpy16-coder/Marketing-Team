---
name: team
description: Run any Sinor business request through the full team workflow on purpose, with routing, task record and independent QA. Use when you want the complete process guaranteed instead of a quick answer.
argument-hint: "<your request, in plain words>"
disable-model-invocation: true
---

Handle this request as the Sinor team: $ARGUMENTS

1. Load the `sinor-operating-rules` skill and apply its shared rules.
2. Route the request as that skill's table says, then load the matching protocol skill (`executive-supervisor-protocol`, `sales-estimation-protocol` or `marketing-director-protocol`) and follow it fully: classify the tier, record the task, delegate to the specialist agents (`sinor-team:<agent>`), have the independent QA agent check the result, and finish with the short hand-off including a simple explanation.
3. Do not skip the record or the QA step for Tier 1 or higher work. If something blocks a step (no workspace, a tool you may not run, missing files), say exactly which step was skipped and why, instead of presenting the result as fully checked.
