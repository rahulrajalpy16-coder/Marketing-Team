#!/usr/bin/env python3
"""PreToolUse hook for Write, Edit and NotebookEdit: QA independence.

Plugin subagents cannot carry their own hooks, so this plugin-level hook acts only when the
calling subagent is the qa-auditor (hook input field agent_type, bare or plugin-scoped name).
Inside a Sinor workspace the auditor may write only under <domain root>/quality/. Paths outside
any workspace (scratch space) are allowed. Exit code 2 blocks the call and shows the message.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import workspace_base, wl  # noqa: E402


def is_qa(agent_type) -> bool:
    return isinstance(agent_type, str) and agent_type.split(":")[-1] == "qa-auditor"


def check(data) -> int:
    tin = data.get("tool_input") or {}
    path = tin.get("file_path") or tin.get("notebook_path") or ""
    if not path:
        return 0
    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    full = os.path.realpath(path if os.path.isabs(path) else os.path.join(cwd, path))
    base = workspace_base(os.path.dirname(full) if not os.path.isdir(full) else full)
    if base is None:
        return 0  # outside any workspace: scratch space
    base = os.path.realpath(str(base))
    if not (full == base or full.startswith(base + os.sep)):
        return 0
    for dom in wl.DOMAINS:
        root = wl.domain_root_in(wl.Path(base), dom)
        if root is None:
            continue
        q = os.path.join(os.path.realpath(str(root)), "quality") + os.sep
        if full.startswith(q):
            return 0
    print(f"QA independence rule: qa-auditor may only write under <domain root>/quality/ "
          f"(audit reports, test evidence). Blocked write to {path}. "
          f"Report the defect to the supervisor instead of fixing it.", file=sys.stderr)
    return 2


def debug_log(data) -> None:
    """Opt-in: set SINOR_HOOK_LOG=<file> to record the payload fields that identify the caller."""
    path = os.environ.get("SINOR_HOOK_LOG")
    if not path:
        return
    try:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({k: data.get(k) for k in
                                 ("hook_event_name", "tool_name", "agent_type", "agent_id", "cwd")}) + "\n")
    except OSError:
        pass


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    debug_log(data)
    if not is_qa(data.get("agent_type")):
        return 0
    try:
        return check(data)
    except Exception as exc:  # fail closed for the QA agent: an unexpected error must not open the guard
        print(f"QA independence rule: guard error ({exc!r}); write blocked to be safe. "
              f"Report this to the supervisor.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
