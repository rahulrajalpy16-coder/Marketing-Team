# Sinor Team plugin

The Sinor Marine Services AI team as one installable plugin. It gives Claude three working
modes, 22 specialist agents, an independent QA reviewer, a Sinor quotation PDF builder and the
tools that keep records, quotes and learned preferences in a shared team workspace.

- **Executive**: emails, quotations from prices you give, technical replies, procurement, software and design tasks.
- **Sales and estimation**: customer RFQs, supplier price comparison, estimates, proposals on approved templates.
- **Marketing**: LinkedIn posts and captions, photo and video campaigns, platform formats.

Status: version 0.1.0, release candidate. See `CHANGELOG.md` and the validation report in the
marketplace repository (`docs/VALIDATION_REPORT.md`) for exactly what was and was not tested.

This package is **private**. It contains company identity details (TRN, address, signatory
contact, service tariff) inside the `sinor-quotation` skill. Never make the repository public.

## What is inside

| Part | Count | What it is |
|---|---|---|
| Skills | 22 | Workflows, rules, commands (listed below) |
| Agents | 22 | Specialists the main conversation delegates to (`sinor-team:<name>`) |
| Hooks | 4 | Session briefing, feedback detector, approval gate, QA write guard. Active only inside a Sinor workspace |
| Scripts | | `sinor.py` (records, tasks, learning, calculator), `sales.py`, `build_quotation.py`, `workspace.py`, media tools |
| References | | QA checklists, marketing brief of record, sales operating standard, onboarding, routing policy |
| MCP servers | 0 | None needed |

### Skills and example prompts

All skill names are prefixed `sinor-team:` when you type them as commands.

| Skill | Use it for | Example prompt |
|---|---|---|
| `sinor-operating-rules` | Shared rules and routing (loads automatically) | "Handle this request for Sinor: ..." |
| `executive-supervisor-protocol` | Emails, technical replies, procurement, software, design, record keeping | "Draft an email to <client> confirming our engineer attends <vessel> at <port> on <date>." |
| `sales-estimation-protocol` | RFQ analysis, estimates, supplier comparison, proposals | "Take this RFQ through the sales workflow: <attach PDF>." |
| `marketing-director-protocol` | LinkedIn and media campaigns | "Make a LinkedIn post and photo set thanking partners after ADIPEC. Company account." |
| `sinor-quotation` | The final quotation PDF in the Sinor layout | "Make the quotation PDF: client <name>, vessel <name>, item 1 ... at ..., QTN <number>." |
| `linkedin-copy-and-unicode-bold` | LinkedIn voice and Unicode bold with a plain-text copy | "Write a company LinkedIn post about <event>. Bold the hook." |
| `marine-technical-accuracy` | Check marine, DP and reference-system wording | "Fact check this draft for DP and HPR terminology: <text>." |
| `platform-video-specs` | Format, length and safe zones for a named platform | "What video format should I use for LinkedIn and Instagram for this clip?" |
| `video-qa-checklist` | Independent check of a rendered video | "QA this video file: <path>." |
| `team` | Run any request through the full workflow on purpose (routing, task record, independent QA) | `/sinor-team:team Draft an email to <client> confirming ...` |
| `setup` | Connect or create the team workspace, check tools | `/sinor-team:setup <folder>` |
| `sales`, `quote`, `onboard`, `find-reference` | Sales commands (you type them) | `/sinor-team:find-reference <client or QTN>` |
| `remember`, `what-you-learned`, `correct-learning`, `forget-preference` | Standing instructions and what the team has learned | `/sinor-team:remember always write vessel names in capitals in client emails` |
| `team-status`, `team-performance`, `team-help` | Open work, measured quality, usage guide | `/sinor-team:team-status` |

## Requirements

- Claude Code (tested with 2.1.323) for the full feature set. Chat and Cowork get the skills only (see the support table).
- `python3` on the PATH (the hooks and scripts call `python3`).
- Python libraries for documents and media: `python3 -m pip install -r scripts/requirements.txt`
  (reportlab, pypdf, python-docx, openpyxl, Pillow, numpy; pillow-heif is optional for iPhone photos).
  `python3 scripts/check_env.py` lists what is present. The plugin never installs anything on its own unless you set `SINOR_AUTO_INSTALL=1`.
- Optional command-line tools: ffmpeg and ffprobe (video checks), pdftotext and pdftoppm (PDF checks), git, gh.

## Install

### Claude Code (terminal, desktop app, or the Code tab)

1. Add the marketplace. For the team's private GitHub repository:
   `claude plugin marketplace add <owner>/<repo>`
   Until the plugin is merged to the repository's default branch, add the branch it lives on: `claude plugin marketplace add <owner>/<repo>#<branch>` (this form was tested).
   Each person needs GitHub access to that repository: sign in with `gh auth login` then run `gh auth setup-git`, or use an SSH key without a passphrase. Claude Code has no token of its own for git.
2. Install: `claude plugin install sinor-team@sinor-team-marketplace`
3. Restart the session, then check: `claude plugin list` (should show `sinor-team` enabled) and `claude plugin details sinor-team` (22 skills, 22 agents).
4. Run `/sinor-team:setup` once (see Workspace below).

Inside a session you can use `/plugin` instead of the commands above.

### Claude chat and Cowork (claude.ai, Claude Desktop)

Anthropic documents that skills and commands from a plugin work in chat and Cowork, while agents and hooks run only in Cowork and Claude Code. Upload the zip: Customize, Plugins, Add, Upload a plugin, then pick `sinor-team-0.1.0.zip` (built by `tools/package_plugin.sh`, 200 MB limit). Plugins you add there are saved to your account and also sync to Claude Code when you sign in with the same account. I could not test claude.ai or Cowork from this build environment, so treat the chat and Cowork behaviour as unverified until someone runs the checks in the validation report.

### One person trying it from a folder (no marketplace)

`claude --plugin-dir /path/to/sinor-team-marketplace/plugins/sinor-team`

## Workspace: where your data lives

The plugin holds instructions and tools only. Records, quote history, knowledge, campaigns and learned preferences live in a **workspace** that the whole team shares. Recommended: one private GitHub repository that every member clones, laid out as:

```
<workspace>/
  .sinor-workspace
  marketing/    brain/, campaigns/ ...
  executive/    knowledge/, learning/, quality/, records/, tasks/
  sales/        records/, knowledge/, templates/, tasks/, quality/, incoming/, sources/
```

- `/sinor-team:setup <folder>` connects an existing folder or creates this structure (it adds no business data and never overwrites files).
- The older single-purpose repositories keep working as they are: if you open Claude in one of them it is recognised as that domain's data (marketing has `brain/`, executive has `knowledge/user/`, sales has `config/routing.json` or `incoming/`).
- Resolution order: `--workspace`, env `SINOR_WORKSPACE`, the project folder and its parents, then the saved setup file (`~/.config/sinor-team/config.json`).
- Keep the workspace repository private. Do not put raw media in it (5 MB per file limit is enforced by the guard script).
- Where there is no workspace (for example plain chat), the skills work in draft mode: they say what they could not read, ask you to attach files and never invent missing business documents.

## Sharing with your team

- **Everyone uses Claude Code:** share the private marketplace repository and the install steps above. Updates reach people when you raise the plugin version.
- **Team or Enterprise plan on claude.ai:** upload the zip, then use Customize, Plugins, the plugin's menu, Share, and pick people (an organization owner must turn on plugin sharing first). Recipients get the updated version automatically at next use. Owners can also publish it to the organization library.
- **One-off:** send the zip. Receivers upload it as above.

## Updating

1. Edit the files, add a line to `CHANGELOG.md`, and raise `version` in `.claude-plugin/plugin.json`. Without a version bump, installed copies stay on the old version.
2. `claude plugin validate .` from the marketplace folder, and `python3 -m pytest -q` from the plugin folder.
3. Push. Team members run `claude plugin marketplace update sinor-team-marketplace` then `claude plugin update sinor-team@sinor-team-marketplace`, and restart.
4. For claude.ai uploads, build a new zip and upload it with the same plugin name.

## Safety rules built in

Never invent prices, specifications, certifications or sources. Everything stays DRAFT until Rahul approves it. Nothing is emailed, published, bought, deleted or deployed without explicit approval. Inside a workspace, a hook asks for confirmation before risky shell or connector actions, and another hook stops the QA agent from editing the work it audits. Plugins cannot ship permission allowlists, so each person's own Claude settings decide which commands prompt.

## Open items and limits

- **Approved quotation templates QF-01 to QF-04** (Word or Excel) were never in any repository. Controlled sales output stays BLOCKED until they are supplied. The standard PDF layout from `sinor-quotation` works without them and is marked DRAFT.
- **Old account skill:** if the older `sinor-quotation` skill is still enabled in your Claude account, two skills share the name (`sinor-team:sinor-quotation` and `anthropic-skills:sinor-quotation`). In the one test run the plugin version was chosen, but remove or disable the old one to avoid confusion.
- **Owner confirmations still open (from the source records):** the title line for Rahul Raj, and whether the service tariff (engineer 93.75, 117.25, 140.75 USD per hour) is still current. The skill asks before using the tariff.
- **`sinor-desk`** (the quick-action band and records pane from the executive repository) is not included. It is a Claude Code interface mod and needs separate packaging and testing.
- **Windows:** the hooks and scripts call `python3`; make sure it is on the PATH. Not tested on Windows or macOS.
- **No icon** is set. Add `.claude-plugin/icon.png` (square, 512 to 2048 px) if you want a listing icon.
- Plain requests are routed to the right workflow by a session hook inside a Sinor workspace; without a workspace or hooks the model decides, so use `/sinor-team:team <request>` when you want the full process guaranteed.
- Hooks and agents do not run in plain chat. Skills that use scripts need code execution and the plugin files available; unverified in chat.

## Troubleshooting

| Symptom | Fix |
|---|---|
| "No Sinor workspace was found" | Run `/sinor-team:setup <folder>` or set `SINOR_WORKSPACE`. |
| `Plugin "sinor-team" not found in marketplace` | Run `claude plugin marketplace update sinor-team-marketplace`. The marketplace entry name and the plugin name must match (they do). |
| Skills appear but scripts fail with `python3: not found` | Install Python 3 and put it on the PATH. |
| PDF or DOCX tools say a library is missing | `python3 -m pip install -r scripts/requirements.txt`, or ask Claude to run `/sinor-team:setup`. |
| Git clone of the marketplace asks for a password or fails | Run `gh auth login` and `gh auth setup-git`, or set up an SSH key. A `GITHUB_TOKEN` alone does not authenticate background updates. |
| Hooks seem silent | By design they act only when the project folder is inside a Sinor workspace. For the QA guard, `SINOR_HOOK_LOG=<file>` records which agent triggered it. |
| A change is not picked up | Restart the session or run `/reload-plugins`; for installed copies raise the version first. |

## Licence

Proprietary, all rights reserved (see `LICENSE`). A default notice was chosen by the package builder because no licence existed. Have the owner or counsel review it before wider distribution.
