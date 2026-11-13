# Validation report: sinor-team 0.1.0

Everything marked **Passed** was run in this build session and the result was observed. Anything I
could not run is marked **Not tested** with the exact steps to check it. Nothing here is
inferred from documentation alone unless it says "per Anthropic documentation".

Environment: Claude Code 2.1.323 on Linux (cloud container), Python 3.13, reportlab 5.0.1,
headless runs (`claude -p`), Anthropic documentation read on 2026-11-13.

Verdict: **ready for private team trial in Claude Code. Not yet accepted as production-ready**:
the items under "Not tested" and "Owner decisions" are open.

## 1. Acceptance criteria

| # | Criterion | Result |
|---|---|---|
| A1 | One plugin contains all skills, merged agents, tools, hooks, no business data | Passed |
| A2 | Manifest, marketplace file and every skill and agent validate with Anthropic's own validator | Passed |
| A3 | Installs through the marketplace flow and every component is discovered | Passed (local marketplace) |
| A4 | Each workflow type triggers the right skill and ignores unrelated requests | Passed with limits (see R2) |
| A5 | Missing essentials are asked for, never invented | Passed |
| A6 | Quotation PDF is correct to the cent and matches the standard layout | Passed |
| A7 | Independent QA step runs and cannot edit the work it audits | Passed |
| A8 | No secrets, machine paths or client names in the package | Passed |
| A9 | Package works when installed from GitHub (private repo, cached copy) | Passed. Chat, Cowork, Windows and macOS: **Not tested** |
| A10 | Output quality against the owner's real example outputs | **Not tested** (no examples supplied) |

## 2. Static validation

| Check | Result | Evidence |
|---|---|---|
| `claude plugin validate plugins/sinor-team --strict` | Passed | "Validation passed" (only note: no listing icon, directory profile) |
| `claude plugin validate . --strict` (marketplace) | Passed | "Validation passed" |
| Same check on the extracted upload zip | Passed | zip unpacked to a clean folder, "Validation passed" |
| Frontmatter of 22 agents parses, `name` equals file name, only allowed keys | Passed | parsed with a YAML library |
| Referenced paths: every `${CLAUDE_PLUGIN_ROOT}/...` reference in skills, agents, hooks and README | Passed | 141 references, 0 missing; 11 script names mentioned, 0 missing |
| Stale repo-style references (`tools/sinor.py`, `.claude/...`, `CLAUDE.md`) | Passed after fixes | found in copied checklists and onboarding, fixed; the brief of record is kept verbatim with a mapping note |
| Em dashes in the package | Passed | 0 found |
| Secret patterns (keys, tokens, private keys, passwords) | Passed | none; the only regex hit is the pattern list inside `guard_large_files.sh`. Pattern based, not a full scanner |
| Machine paths (`/home/...`, `/Users/...`) | Passed | none in the shipped files |
| Client or project names | Passed | none. Names present: Rahul (approver), Naveen Thandarath (quotation signatory) |
| Upload zip integrity | Passed | `unzip -t` clean, 89 files, 604 KB, plugin folder is the single top-level entry, no `bin/` folder |
| Component inventory | Passed | `claude plugin details`: 22 skills, 22 agents, 3 hook events (4 hook commands), 0 MCP servers |

## 3. Unit and script tests

`python3 -m pytest -q` from the plugin folder: **174 passed** (re-run by me after each change).

| File | Tests | Covers |
|---|---|---|
| test_sinor.py | 29 | ported executive tool: calc, lint, tasks, preferences, lessons, records, sync safety |
| test_sales.py | 21 | ported sales tool, workspace resolution through the CLI |
| test_workspace.py | 24 | all four resolution steps in order, both layouts, legacy markers, init, config |
| test_hooks.py | 26 | each hook as a real subprocess: gating, approval gate, QA guard (bare and scoped agent name, fail closed), feedback detector, session start |
| test_quotation.py | 74 | amount in words (26 values), arithmetic, validation errors, end-to-end PDF read back, 25-item multi-page |

Bug found and fixed by these tests: the QA write guard passed a string where a path object was
required, crashed, and a crashing hook does not block. It now works and fails closed for the QA agent.

## 4. Runtime tests (live Claude Code, headless)

Reproducible with `tests/runtime/`. Results vary run to run; read them as evidence, not guarantees.

| # | Test | Result |
|---|---|---|
| R1 | Discovery in a real session | Passed. 22 skills and 22 agents appear as `sinor-team:*` |
| R2 | Trigger routing | Passed with limits. LinkedIn request loaded the LinkedIn skill. RFQ request loaded the sales protocol. "Make the Sinor quotation PDF" loaded `sinor-quotation`. An unrelated Python request loaded nothing. A direct marine question did **not** load `marine-technical-accuracy`; the model answered from memory and said it had not checked sources |
| R3 | Missing-input behaviour | Passed. Quotation request asked for client, items and QTN and invented none. RFQ request without the PDF asked for it and for the missing template. Email with no details used bracketed placeholders. A technical reply with web access blocked refused to write unsourced claims and asked how to proceed |
| R4 | Full executive workflow, same plain email request, 4 runs after the routing fix | Passed. 4 of 4: router, protocol, task record, documentation agent, independent QA agent, audit report under `quality/`. 3 of 4 also closed the task record (1 left it open; across all 5 workflow runs including R14, 3 closed and 2 stayed open). Deliverable facts matched the instruction exactly. Before the fix, 1 of 2 runs skipped the whole workflow (answered directly), which is why the session hook now carries an explicit first-action directive and the `/sinor-team:team` command exists |
| R5 | Specialist delegation by namespaced name | Passed. `sinor-team:marine-technical-engineer` and `sinor-team:research-verification` were both launched for the same technical-reply task (simultaneity was not measured) |
| R6 | `remember` then `forget-preference` | Passed. Preference written to disk with exact wording, then removed leaving only a tombstone. Sync reported honestly that the test folder was not a git repository |
| R7 | `setup` in a folder with no workspace | Passed. Reported none found, listed tools present and missing, installed nothing |
| R8 | Quotation end to end through the skill and script, plugin copy in a folder with spaces | Passed. Net Amount 4,519.92 matches my hand calculation (4,531.25 less 226.56 plus 215.23 VAT) |
| R9 | Quotation arithmetic and layout, independent spec with half-cent rounding | Passed. 5,132.24 / 513.22 / 230.95 / 4,849.97, words correct. Page 1 of the PDF viewed and matches the layout in the skill |
| R10 | QA write guard in a live session | Passed. Write outside `quality/` blocked with the intended message; write inside `quality/` passed the hook (then refused only by headless permissions). Plugin subagents report `agent_type` as `sinor-team:qa-auditor`, a detail the documentation does not state; the guard handles it |
| R11 | Agent skill preloading (`skills:` frontmatter) | Passed for `copywriter` and `fact-reviewer`, which quoted their preloaded skill text correctly. `qa-reviewer` and `video-editor` use the same mechanism but were not individually tested |
| R12 | Session hook output reaches the model | Passed (seen in the event stream) |
| R13 | Install from the real private GitHub repository (`claude plugin marketplace add <owner>/<repo>#<branch>`, then install) | Passed. Clone of the private repo worked in this environment, plugin cached (1.2 MB, plugin folder only), 22 skills and 22 agents listed |
| R14 | Live workflows on that genuine cached install (no `--plugin-dir`) | Passed. Plain email request: router, protocol, task record, QA audit 1 **failed** the draft for an invented sign-off name, correction made, QA audit 2 passed 5 of 5. Quotation request: sinor-quotation skill, script run, Net Amount 12,271.88 equals my hand calculation (11,687.50 + 584.38) |

## 5. Not tested

| Area | Why | How to check |
|---|---|---|
| claude.ai chat and Cowork (zip upload, skills visible, scripts runnable, hooks and agents greyed out in chat) | No access from this environment | Customize, Plugins, Upload `sinor-team-0.1.0.zip`; run `/sinor-team:team-help`, then a LinkedIn prompt and the quotation prompt. Per Anthropic documentation agents and hooks do not run in chat |
| Teammates' own GitHub authentication (each person's `gh auth login` or SSH key) | I tested with this environment's credentials only | Each teammate runs the install steps in the README |
| Windows and macOS | Linux only | Install, run the pytest suite, run R4 |
| Marketing campaign end to end (strategist, copywriter, art director, photo and video editor, QA reviewer) | Needs real photos and video; only the LinkedIn skill was run | Run a small campaign with 2 photos and review the result |
| Media scripts: `make_music_bed.py`, `probe_media.py`, `loudness_check.py`, `contact_sheet.py`, `heic_to_jpg.py`, `publish_release.sh` | Needed media files and GitHub release rights; only `guard_large_files.sh` was run, in a temporary repository | Run each on a sample file; `publish_release.sh` only against a test release |
| Real RFQ with a real document; `sales fill` with a real template | No RFQ sample and no approved template exist in the repositories | Supply an RFQ PDF and the QF templates, then run `/sinor-team:sales` |
| `sinor.py sync` against the team's real remote (push path) | Tested only with temporary repositories in unit tests | Run `/sinor-team:remember ...` in a real workspace clone |
| Interactive permission prompts | Headless runs cannot answer them (they blocked some commands, which the model reported) | Use in a normal session |
| Output quality against the owner's real examples | No representative examples were supplied | Send 2 good emails, 2 quotations, 2 LinkedIn posts you consider ideal |
| `claude plugin eval` suites | Not written | Optional follow-up |

## 6. Known issues and limits

1. The old account skill `anthropic-skills:sinor-quotation` is still listed beside `sinor-team:sinor-quotation`. The plugin version was chosen in the test; remove the old one.
2. Skill triggering is the model's choice. Inside a workspace the hook makes it reliable (4 of 4); outside one, or in chat, use `/sinor-team:team <request>`.
3. Direct technical questions are not routed to the accuracy skill; ask for "a technical reply with sources" to engage the engineer and research agents.
4. Task records are not always closed (2 of 5 runs left one open); `team-status` shows open tasks.
5. When one quotation item splits across a page, the table has no bottom line at the break. Cosmetic.
6. Two quotation checks stay manual (title, scope and exclusions agree; revision suffix matches a scope change). The script says NOT RUN for them.
7. `sinor-desk` is not included. No icon. License is a default proprietary notice that needs owner review.

## 7. Owner decisions and inputs still needed

See the hand-off message: repository for hosting, plan type for sharing, workspace repository, approved templates QF-01 to QF-04, Rahul Raj title line, service tariff confirmation, and examples for quality checks.
