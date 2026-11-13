# Agent merge report

Output: 22 agent files in `plugins/sinor-team/agents/`. Source repos were read only.

## Source file to target file

| Source | Target | Kind |
|---|---|---|
| Marketing brand-strategist, art-director, copywriter, distribution-analyst, fact-reviewer, media-librarian, photo-editor, platform-researcher, qa-reviewer, video-editor | same names | 1:1, paths fixed |
| SMS design-visualization, research-verification, software-automation | same names | 1:1, paths fixed |
| Sales rfq-quotation-analyst, document-search, document-controller | same names | 1:1, paths fixed |
| SMS qa-auditor + Sales qa-auditor | qa-auditor | merge |
| SMS user-intelligence + Sales knowledge-learning | user-intelligence | merge |
| SMS marine-technical-engineer + Sales marine-technical-evaluator | marine-technical-engineer | merge |
| SMS procurement-operations + Sales procurement-supplier | procurement-operations | merge |
| SMS documentation-communication + Sales proposal-documents | documentation-communication | merge |
| SMS sales-commercial + Sales estimator-pricing + Sales commercial-contracts | sales-commercial | merge |
| SMS executive-supervisor | none (persona becomes skill) | not an agent |
| Sales sales-manager | none (persona becomes skill) | not an agent |

## Merged agents: what was combined and conflicts resolved

### qa-auditor (model: inherit)
- Combined: the full SMS procedure (original instruction, checklists, pref list, lint, PDF render, own calc spec, software rerun, source check, diff, PASS/FAIL/BLOCKED/NOT VERIFIED, report format) and all Sales checks (extraction completeness, price provenance, units, currency, formulas, scope/exclusion consistency, template revision, page layout, independent `sales.py calc` rerun, never PASS for unavailable renderers, unread sources or untested live behavior).
- Tools: union (Read, Grep, Glob, Bash, Write, WebSearch, WebFetch). disallowedTools: Agent, Edit, NotebookEdit (Sales had no Edit either).
- Hook block removed; sentence added saying the QA independence rule is also enforced by a plugin-level hook but the agent must obey it itself.
- Conflict: model inherit vs sonnet. Chose inherit (follows the caller's model, which is never weaker than sonnet in practice). Please confirm.
- Conflict: write location. Executive writes under `<EXECUTIVE_ROOT>/quality/audit-reports/`, Sales under the brief's path inside `<SALES_ROOT>/quality/`. Kept both by workflow.

### user-intelligence (model: sonnet)
- Combined: all SMS modes (A intent interpretation, B learning update, vague-feedback table, hard rules, `sinor.py pref/lesson/correction/validate`) plus the Sales knowledge-learning rules (record every outcome, correction capture, `sales.py remember` with mandatory source, proposed vs `--approved`, never promote generated prices, current instruction wins, persist git only in the intended private repo and never force push) and the Sales shared controls.
- Conflict: model sonnet vs haiku. Chose sonnet (more capable).
- Conflict: SMS says a tentative lesson needs confirmation or recurrence to be active; Sales says proposed stays proposed unless explicit standing instruction. Not contradictory; kept both, each in its own section.

### marine-technical-engineer (model: inherit)
- Combined: SMS method, truth discipline, claims register and return format; Sales compliance matrix, included/excluded scope, interface matrix, open technical questions, scope coverage list (supply to third-party responsibilities), OEM/model/certification identity preservation, older scopes cannot override current requirements, primary-source review and stronger-model escalation for high-consequence DP or class claims.
- Conflict: model inherit vs sonnet. Chose inherit.
- Conflict: Sales evaluator had no WebSearch/WebFetch; SMS engineer has them. Tools are the union. Added the SMS rule that private company data stays out of search queries. Please confirm web access for RFQ evaluation is acceptable.
- "Stronger-model escalation": the Sales agent is told not to change its own model, so the text says to tell the caller a stronger-model review is needed.
- Added HISTORICAL to the status tags for sales work (Sales taxonomy).

### procurement-operations (model: sonnet)
- Combined: SMS document-first method, CONFIRMED/ESTIMATE/UNKNOWN labels, code-only arithmetic, DD/MM/YYYY, lead-time flags, no ordering/contacting; Sales like-for-like comparison fields, expired offers, clarification/RFQ drafts, no assumed availability.
- Conflict: two label sets. Executive keeps CONFIRMED/ESTIMATE/UNKNOWN; RFQ work uses VERIFIED/USER-SUPPLIED/HISTORICAL/UNVERIFIED, stated explicitly in the body.
- Calculator: `sinor.py calc` for executive, `sales.py calc` for RFQ work.

### documentation-communication (model: sonnet)
- Combined: SMS email/quotation/Office/report rules, lint, PDF preview, return format; Sales template selection QF-01 to QF-04, preserve design, `sales.py fill`, page render inspection, spreadsheet formula recalculation labelling, editable source plus export plus manifest, missing template means BLOCKED.
- Tools: SMS list including Skill (Sales had no Skill; superset).
- Conflict: SMS allows a reportlab fallback if the quotation skill is missing; Sales says a missing controlled template is BLOCKED and never a redesign. Resolved by mode: the reportlab fallback applies to executive quotation work only; in sales-estimation controlled-template work BLOCKED governs. This is the more careful reading.
- Skill name: `anthropic-skills:sinor-quotation` replaced with "the sinor-quotation skill (try the plugin-namespaced name if the plain name fails)". The `anthropic-skills:docx/xlsx/pptx/pdf` names are kept as written (they are external account skills, not plugin skills).

### sales-commercial (model: inherit)
- Combined: SMS sources of numbers, MISSING rule, calc spec format, defaults, QTN rule, return format; Sales estimator rules (explicit pricing first, history with reference/date/currency/quantity/scope/status, separate cost/selling/PO/actual, no lump-sum splitting, never infer FX, gross margin vs markup not both, supported lines only, PRICE REQUIRES MANUAL CONFIRMATION, suggestions unapproved); Sales commercial-contracts checks (payments total 100, currency, tax basis, validity, warranty, delivery assumptions, cancellation, exclusions, no legal conclusions, deviation notes).
- Conflict: SMS says never estimate a missing number; Sales allows evidence-based suggestions. Resolved: no estimating; history only as a labelled, unapproved, sourced suggestion; missing stays MISSING or PRICE REQUIRES MANUAL CONFIRMATION.
- Conflict: QTN placeholder `SMS-QT{YYYY}-XXXXX` (executive) vs `DRAFT-UNASSIGNED` (sales). Kept by workflow.
- Conflict: model inherit (SMS) vs sonnet (Sales, twice). Chose inherit.
- Note: the `sales.py calc` input format is not documented in the sources, so it is not described here; the agent is told to use the tool's own format.

## Other deliberate changes
- `skills:` frontmatter preload added to copywriter (linkedin-copy-and-unicode-bold), fact-reviewer (marine-technical-accuracy), qa-reviewer (video-qa-checklist), video-editor (platform-video-specs). The sources told these agents to read a skill file by repo path; their tool lists have no Skill tool, so a preload is the only way to deliver it. Bodies also name the skill. Needs one live test that plugin skill names resolve in `skills:` (fallback: add the Skill tool or use namespaced names).
- Descriptions were wrapped in double quotes because several contain colons (unquoted they fail YAML parsing).
- Descriptions of the Sales 1:1 agents and a few others were lengthened slightly to state the workflow they serve (all under 600 characters, longest 441).
- Playwright note: "Chromium at /opt/pw-browsers" became "the Chromium already installed in the environment" (no machine path). `/tmp/work/<campaign>` is kept only as a "normally" example for the temporary working directory the brief names.
- Marketing and SMS agents: added the Workspace paragraph; "Do not edit brain/ files" and all Never/Return rules unchanged.
- Sales "Shared controls" paragraph kept verbatim in meaning on rfq-quotation-analyst, document-search and document-controller, and folded into merged agents.

## Repo-only references (kept, pointed at the data root)
- `<EXECUTIVE_ROOT>/knowledge/company/SINOR_COMPANY_PROFILE.md`, `knowledge/technical/` and its `README.md` table format, `knowledge/projects/<project>/PROJECT.md`, `knowledge/approved-templates/EMAIL_STANDARD.md` and `QUOTATION_STANDARD.md`, `knowledge/user/PREFERENCE_CONFIDENCE.md`, `CORRECTION_HISTORY.md`, `tasks/active/<task>/original_instruction.txt` and `TASK.md`.
- `<SALES_ROOT>/tasks/<id>/outputs/extraction.json`, `<SALES_ROOT>/templates/` and the template register, QF-01 to QF-04 templates (not in any repo per DESIGN.md section 6), `stored_path` records used by `sales.py search`.
- `<MARKETING_ROOT>/brain/*` files, `campaigns/<name>/...`, `assets/brand/` (agent also told about the bundled logo).
- Scripts assumed bundled in `${CLAUDE_PLUGIN_ROOT}/scripts/`: `probe_media.py`, `contact_sheet.py`, `loudness_check.py`, `unicode_bold.py`, `sinor.py` (subcommands pref, lesson, correction, validate, lint, calc), `sales.py` (search, register, calc, fill, remember), `workspace.py`. They did not yet exist when this report was written.
- Hook: `qa_write_guard.py` is replaced by the plugin-level hook; the hook must exist for the independence sentence in qa-auditor to be accurate.

## Dropped
Nothing except: the two persona files (executive-supervisor, sales-manager) and the qa-auditor `hooks:` block. No rule, checklist, duty or return format from any other source was removed.
