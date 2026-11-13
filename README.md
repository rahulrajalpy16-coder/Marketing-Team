# Sinor team marketplace

Private Claude plugin marketplace for the Sinor Marine Services team. It currently lists one plugin:

| Plugin | What it is |
|---|---|
| `sinor-team` | Executive, sales and estimation, and marketing AI workflows: 22 skills, 22 specialist agents, QA, a quotation PDF builder, workspace-aware tools |

**Users:** read `plugins/sinor-team/README.md` (install, workspace, sharing, troubleshooting).

**Status:** 0.1.0 release candidate. What was and was not tested is in `docs/VALIDATION_REPORT.md`.

## Layout

```
.claude-plugin/marketplace.json     the catalog (marketplace name: sinor-team-marketplace)
plugins/sinor-team/                 the plugin (skills, agents, hooks, scripts, references, tests)
docs/DESIGN.md                      design contract: workspace model, paths, component map
docs/agent-merge-report.md          how 31 source agents became 22
docs/VALIDATION_REPORT.md           validation results
tests/runtime/                      live Claude Code checks (need a signed-in `claude`)
tools/package_plugin.sh             builds the zip for claude.ai and Cowork upload
```

## Maintainer checklist for each change

1. Edit the plugin, add a line to `plugins/sinor-team/CHANGELOG.md`, raise `version` in `plugins/sinor-team/.claude-plugin/plugin.json`.
2. `claude plugin validate . --strict` and `claude plugin validate ./plugins/sinor-team --strict`
3. `cd plugins/sinor-team && python3 -m pytest -q`
4. Optional live checks: `tests/runtime/README.md`
5. Commit and push. Team members run `claude plugin marketplace update sinor-team-marketplace` then `claude plugin update sinor-team@sinor-team-marketplace`.
6. For claude.ai or Cowork: `tools/package_plugin.sh` and upload the new zip.

## Keep it private

The `sinor-quotation` skill contains company identity details and a service tariff. Do not make this repository public. For any public release, remove those details, the logo, the brief of record, and the names Rahul and Naveen first.
