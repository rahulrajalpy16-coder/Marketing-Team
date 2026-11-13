---
name: setup
description: Connect this plugin to the team workspace where Sinor data lives, create a new workspace folder structure, and check that required tools and Python libraries are present. Run once per machine or when a skill says no workspace was found.
argument-hint: "[path to an existing or new workspace folder]"
disable-model-invocation: true
---

Set up the Sinor Team workspace. Argument given: `$ARGUMENTS`

The plugin holds instructions and tools only. Business data (records, quotes, knowledge, campaigns, learned preferences) lives in a workspace that the whole team shares, ideally a private GitHub repository that each member clones. Never put commercial data into the plugin folder.

1. Show what is currently detected: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" detect`.
2. If the user gave a path, or a workspace is detected and correct, connect it: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" set "<path>"`. This writes a small per-user config file on this machine only.
3. If the user has no workspace yet, ask for the folder (a fresh clone of the team's private repository is best), then create the structure: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" init "<path>"`. It never overwrites existing files and adds no business data. Then connect it with `set`.
4. If the user already has the older single-purpose folders (the marketing repo, the executive repo or the sales repo), no move is needed: opening Claude in that folder, or passing its path, is recognised as that domain's data root. Mention that a single combined workspace is the recommended long-term layout (`marketing/`, `executive/`, `sales/` folders) and offer to explain the migration, but do not move or delete anything without explicit approval.
5. Check the environment: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check_env.py"`. Report missing Python libraries or tools (ffmpeg, pdftotext, git, gh). Do not install anything without the user's approval; if they approve, the libraries are listed in `${CLAUDE_PLUGIN_ROOT}/scripts/requirements.txt`.
6. Check that the workspace is a git repository and that it is private if it holds commercial data; say what you cannot verify. Never ask for a token in chat; if GitHub access is missing, tell the user to connect GitHub in the Claude app settings.
7. Finish with a short status: workspace path, domains found (marketing, executive, sales), tools found and missing, next suggested step.

No em dashes.
