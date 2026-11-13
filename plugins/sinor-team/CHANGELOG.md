# Changelog

All notable changes to the `sinor-team` plugin. Versioning follows MAJOR.MINOR.PATCH. The `version`
field in `.claude-plugin/plugin.json` pins what team members receive: bump it for every change you
want them to get, otherwise installed copies keep the old version.

## 0.1.0 (release candidate, not yet accepted by the owner)

First combined package. It merges three private repositories into one plugin.

### Added
- 22 skills: three workflow protocols converted from the repositories' `CLAUDE.md` files
  (`executive-supervisor-protocol`, `sales-estimation-protocol`, `marketing-director-protocol`),
  the `sinor-operating-rules` router with the shared rules, 4 marketing skills, 7 learning and
  status skills, 4 sales commands converted to skills (`sales`, `quote`, `onboard`,
  `find-reference`), the new `sinor-quotation` skill, the new `setup` skill and the new `team` command (forces the full workflow).
- 22 specialist agents (see `docs/agent-merge-report.md` in the marketplace repository).
- Workspace-aware tools in `scripts/`: `workspace.py` (new), `sinor.py`, `sales.py`,
  `build_quotation.py` (new, spec-driven quotation PDF), marketing media scripts, `check_env.py`.
- Hooks (active only inside a Sinor workspace): session briefing with a first-action routing directive,
  feedback detector, approval gate, QA write guard.
- Bundled references: QA checklists, marketing brief of record, sales operating standard,
  onboarding guide, routing policy.

### Changed from the source repositories
- Business data no longer lives in the tool folder. Records, knowledge, tasks, campaigns and
  learned preferences are read from and written to a separate team workspace.
- `CLAUDE.md` rules became skills (a plugin cannot load a root `CLAUDE.md`).
- Sales slash commands became skills (Anthropic recommends skills over commands for new plugins).
- `remember` and `team-status` merged across the three domains.
- The QA write guard moved from agent frontmatter to a plugin-level hook because plugin agents
  cannot carry hooks. It fails closed for the QA agent.
- Hooks no longer auto-install Python packages unless `SINOR_AUTO_INSTALL=1` is set.
- `sinor.py sync` works on whichever git repository contains the executive data root and keeps its
  original safety properties (no force push, narrow scope).
- Missing approved quotation templates still mean BLOCKED for controlled sales output (unchanged rule).

### Agent merges (31 source agents became 22)
- `qa-auditor` (executive and sales), `user-intelligence` + `knowledge-learning`,
  `marine-technical-engineer` + `marine-technical-evaluator`,
  `procurement-operations` + `procurement-supplier`,
  `documentation-communication` + `proposal-documents`,
  `sales-commercial` + `estimator-pricing` + `commercial-contracts`.
- Not carried as agents: `executive-supervisor` and `sales-manager`. Their roles are the main
  conversation and now live in the protocol skills.

### Not included
- The `sinor-desk` interface mod from the executive repository (Claude Code only, needs separate
  packaging and testing).
- Approved quotation Word and Excel templates (QF-01 to QF-04): they were never in any repository.
- Any MCP server. No workflow requires one.

### Known open items
See the README section "Open items and limits".
