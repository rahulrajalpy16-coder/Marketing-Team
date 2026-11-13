# Sinor Team plugin: design contract

One plugin (`sinor-team`) merges three private repos (Marketing-Team, Claude-Agent-Team-SMS,
Sinor-Sales-Estimation-Team) into one installable package for Rahul and his team.
This file is the contract every part of the package follows.

## 1. Principles

1. **Plugin = code and instructions. Workspace = business data.** The plugin never contains client
   records, quote history, prices from quotes, campaign media, learned preferences or credentials.
2. **Nothing writes inside the plugin directory.** `${CLAUDE_PLUGIN_ROOT}` changes on every update.
3. **Original intent is preserved.** Rules from the three source `CLAUDE.md` files become skills
   (a `CLAUDE.md` at a plugin root is not loaded by Claude Code).
4. **Never invent.** Missing templates, prices, specs or approvals stay open items. No placeholders
   pretending to be real business documents.
5. **No em dashes** in anything written for the user (source rule, kept).
6. **Honest environment support.** Skills and commands work in chat, Cowork and Claude Code.
   Hooks, sub-agents and local scripts that touch a workspace work in Cowork and Claude Code only
   (documented by Anthropic). Anything not verified is labelled so.

## 2. Workspace (where team data lives)

Recommended home: **one private GitHub repository** that the whole team can clone
(access = GitHub collaborators). Layout:

```
<workspace>/
  .sinor-workspace          marker file
  marketing/                was Marketing-Team   (brain/, campaigns/, assets/ for media pointers)
  executive/                was Claude-Agent-Team-SMS (knowledge/, learning/, quality/, records/, tasks/)
  sales/                    was Sinor-Sales-Estimation-Team (records/, knowledge/, templates/, tasks/, quality/, incoming/, sources/)
```

Legacy single-repo layouts keep working unchanged: if the folder Claude is opened in matches a
domain marker, it is used as that domain's root.

Domain markers (checked in this order for a base folder B and domain D):

| Domain | Combined layout | Legacy marker (B itself is the root) |
|---|---|---|
| marketing | `B/marketing/` exists | `B/brain/` exists |
| executive | `B/executive/` exists | `B/knowledge/user/` exists |
| sales | `B/sales/` exists | `B/config/routing.json` or `B/incoming/` exists |

Base folder resolution (first hit wins):
1. `--workspace` argument, 2. env `SINOR_WORKSPACE`, 3. walk up from `CLAUDE_PROJECT_DIR` then the
current directory looking for `.sinor-workspace` or a legacy marker, 4. `~/.config/sinor-team/config.json`
(`{"workspace": "<abs path>"}`, written by `/sinor-team:setup`).
If nothing resolves, tools exit with a clear message that tells the user to run `/sinor-team:setup`.

## 3. Path conventions inside skills, agents and scripts

* Bundled files: `${CLAUDE_PLUGIN_ROOT}/...` (Claude Code substitutes it in skill and agent bodies).
* Data roots: first step of every workflow runs
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" root <marketing|executive|sales>`
  and uses the printed absolute path as `<ROOT>`. All other data paths are written relative to
  that `<ROOT>` (for example `<ROOT>/knowledge/user/`, `<ROOT>/tasks/active/`).
* Scripts that need a data root resolve it themselves through `scripts/workspace_lib.py`.
* No absolute machine paths, no `/home/user`, no `${CLAUDE_PROJECT_DIR}` in skills or agents.

## 4. Component map

| Source | Becomes |
|---|---|
| Marketing `CLAUDE.md` | skill `marketing-director-protocol` |
| SMS `CLAUDE.md` | skill `executive-supervisor-protocol` |
| Sales `CLAUDE.md` + `docs/OPERATING_STANDARD.md` | skill `sales-estimation-protocol` |
| 4 Marketing skills | same names, paths fixed |
| 7 SMS skills | same names, paths fixed (`remember`, `team-status` merged with the Sales commands of the same name) |
| Sales commands `sales`, `quote`, `onboard`, `find-reference` | skills of the same names, user-invoked only |
| `sinor-quotation` (account skill + 2026-10-20 update) | skill `sinor-quotation` plus `scripts/build_quotation.py` |
| 31 agents | 22 agents (merges listed in CHANGELOG) |
| `tools/sinor.py`, `tools/sales.py`, `scripts/*` | `scripts/` (workspace-aware) |
| SMS hooks | `hooks/hooks.json`, active only inside a Sinor workspace |
| `quality/checklists/` | `references/qa-checklists/` |
| New | skills `setup`, `sinor-operating-rules`; `scripts/workspace.py` |

## 5. Hook behaviour

All hooks are no-ops outside a Sinor workspace so the plugin never disturbs unrelated projects.
Plugin agents cannot carry their own hooks, so the QA write-guard is a plugin-level PreToolUse hook
that only acts when the calling subagent is `qa-auditor`.

## 6. Out of scope for v0.1 (stated, not hidden)

* No MCP server is added. Nothing in the workflows requires one.
* Approved quotation Word/Excel templates (Sales `templates/`) are not in any repo (only an empty
  register). They are an open item for the owner; proposal work stays BLOCKED without them, as the
  source rules already require.
