# Universal QA Checklist (applies to every deliverable)

> Command shorthand in these checklists: `sinor.py` means `python3 "<plugin root>/scripts/sinor.py"`. Your agent instructions give the exact resolved command. The bundled calculator for sales work is `sales.py calc` in the same folder.

| # | Check | How to verify (objective evidence required) |
|---|---|---|
| U1 | Every mandatory requirement (explicit + implied) in the task's requirement matrix is met | Walk each row; cite the line, page, test or file that satisfies it |
| U2 | Delivered in the requested medium (file vs text, working software vs mockup) | File exists at stated path; open or parse it |
| U3 | Nothing requested was substituted, dropped or quietly reinterpreted | Compare against `original_instruction.txt` verbatim |
| U4 | No unrequested changes when minimal modification was asked | `diff` or `git diff` against the original |
| U5 | All numbers recomputed independently | Recalculate from inputs, do not reuse the producer's log |
| U6 | Every factual claim has a source or an UNVERIFIED tag | List claims; check each |
| U7 | Applicable user preferences followed (list the PREF IDs checked) | `sinor.py pref list` |
| U8 | Style: no em dashes, no unresolved placeholders | `sinor.py lint <file>` exit code 0 |
| U9 | Open items and assumptions clearly listed for the user | Read the deliverable summary |
| U10 | No secrets, credentials or unrelated private data in the output | grep for key patterns, review |
