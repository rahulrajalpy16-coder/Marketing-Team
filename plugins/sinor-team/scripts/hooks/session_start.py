#!/usr/bin/env python3
"""SessionStart hook: print the team briefing (confirmed preferences, active lessons, open tasks).

Silent outside a Sinor workspace. Never installs anything unless SINOR_AUTO_INSTALL=1 is set.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import SCRIPTS, domain_root, workspace_base  # noqa: E402


def main() -> int:
    if workspace_base() is None:
        return 0
    missing = []
    for mod in ("reportlab", "pypdf"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        if os.environ.get("SINOR_AUTO_INSTALL") == "1":
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r",
                            str(SCRIPTS / "requirements.txt")], capture_output=True, check=False)
        else:
            print("[sinor-team] Optional Python libraries missing: " + ", ".join(missing) +
                  ". PDF and DOCX tools need them. Run: python3 -m pip install -r " +
                  str(SCRIPTS / "requirements.txt") + " (or ask the assistant to run /sinor-team:setup).")
    print("[sinor-team] This project is a Sinor workspace. Before replying to ANY Sinor business request "
          "(email, quotation, RFQ, estimate, technical reply, procurement, LinkedIn or media post), your FIRST "
          "action must be to call the Skill tool with skill \"sinor-team:sinor-operating-rules\"; it routes to "
          "the executive, sales or marketing protocol. Work of Tier 1 or higher needs a task record and an "
          "independent sinor-team:qa-auditor check before you present it as done. Casual chat and unrelated "
          "coding do not need this.")
    root = domain_root("executive")
    if root is None:
        return 0
    env = dict(os.environ, SINOR_ROOT=str(root))
    r = subprocess.run([sys.executable, str(SCRIPTS / "sinor.py"), "context"], env=env,
                       capture_output=True, text=True, check=False)
    if r.returncode == 0 and r.stdout.strip():
        print(r.stdout.rstrip())
    else:
        print("[sinor-team] Could not print the team briefing; run /sinor-team:team-status.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
