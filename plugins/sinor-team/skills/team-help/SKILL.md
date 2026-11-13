---
name: team-help
description: Show how to use the Sinor Team plugin from a phone or desktop - what each skill does, example instructions, the team of specialists, and where the data lives.
disable-model-invocation: true
---

Reply with this guide (keep it phone-friendly, no em dashes), then stop:

**Sinor Team**: give one instruction in plain words (English, short notes or Manglish are fine). The right workflow works out what you need, routes it to the right specialists, has an independent reviewer check it, and sends you the result with a short explanation.

**Three workflows**
- Executive: emails, quotations, technical replies, procurement, software and design tasks (`executive-supervisor-protocol`).
- Sales and estimation: RFQs, estimates, proposals, price history (`sales-estimation-protocol`).
- Marketing: LinkedIn posts, photo and video campaigns (`marketing-director-protocol`).

**Try**
- "Draft an email to <client> confirming our engineer attends <vessel> at <port> on <date>."
- "Quote 2 x <item> at <price> USD each plus 3 days engineer at 650/day, VAT 5%, QTN SMS-QT2026-01890, vessel <name>."
- "Client asks if Ranger 2 can feed NAVIS DP. Give me a technical reply with sources."
- "Write a LinkedIn post thanking our partners after ADIPEC. Company account."

**Commands** (all start with `/sinor-team:`)
- `team <request>`: run any request through the full workflow on purpose (routing, task record, independent QA)
- `setup`: connect or create the team workspace where data lives
- `sales`, `quote`, `onboard`, `find-reference`: sales and estimation workflows
- `remember <rule>`: save a standing instruction
- `what-you-learned`, `correct-learning`, `forget-preference`: manage what the team learned
- `team-status`, `team-performance`: open work and measured quality

**Approvals**: the team drafts and prepares. It asks you before sending emails, spending money, deleting, publishing or deploying.

**Data**: this plugin holds instructions and tools only. Your records, prices, quotes and learned preferences live in the team workspace (run `/sinor-team:setup` once).
