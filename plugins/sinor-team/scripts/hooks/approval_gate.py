#!/usr/bin/env python3
"""PreToolUse hook: force an explicit user confirmation before outward-facing or
irreversible actions (the "Approval gates" section of the protocol skills).

Returns permissionDecision "ask" so the user sees a confirmation prompt in the app.
It never auto-approves anything; silence means the normal permission flow applies.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import workspace_base  # noqa: E402

# MCP connector actions that leave the building: email, chat, publishing, money, deletion.
MCP_RISKY = re.compile(
    r"(send|reply|forward|post_message|publish|share|invite|delete|remove|archive|purchase|order|pay|"
    r"transfer|merge_pull_request|create_repository|deploy|update_trigger|create_trigger|schedule)",
    re.I,
)
MCP_SAFE = re.compile(r"(draft|search|list|get|read|fetch|query|find|status|view)", re.I)

BASH_RISKY = [
    (re.compile(r"\bgit\s+push\b.*(--force|-f\b|--delete|:refs)"), "force or delete push"),
    (re.compile(r"\b(npm|pnpm|yarn)\s+publish\b"), "package publish"),
    (re.compile(r"\b(vercel|netlify|firebase|fly|heroku|wrangler|gcloud\s+app|az\s+webapp)\b.*\bdeploy\b"),
     "production deployment"),
    (re.compile(r"\bcurl\b.*(-X\s*(POST|PUT|PATCH|DELETE)|--data|-d\s)"), "outbound write request"),
    # mail clients only in command position (start, or after ; && || | $( ), so grep "mail" is not flagged
    (re.compile(r"(^|[;&|(]\s*|\$\(\s*)(sendmail|mail|mailx|mutt|swaks)\s"), "sending email"),
    (re.compile(r"\brm\s+-[a-z]*r[a-z]*f?\s+(/|~|\.\.?/?\s|knowledge|learning|\.git)\b"), "bulk deletion of important data"),
    (re.compile(r"\bgit\s+(reset\s+--hard|clean\s+-[a-z]*f)"), "discarding work"),
]


def ask(reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": f"Sinor approval gate: {reason}. Requires the user's explicit approval.",
    }}))
    sys.exit(0)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if workspace_base() is None:  # only inside a Sinor workspace
        return
    name = data.get("tool_name", "")
    tin = data.get("tool_input") or {}
    if name.startswith("mcp__"):
        action = name.split("__")[-1]
        if MCP_RISKY.search(action) and not MCP_SAFE.match(action):
            ask(f"connector action '{action}'")
        return
    if name == "Bash":
        cmd = tin.get("command", "")
        for rx, why in BASH_RISKY:
            if rx.search(cmd):
                ask(why)
    return


if __name__ == "__main__":
    main()
