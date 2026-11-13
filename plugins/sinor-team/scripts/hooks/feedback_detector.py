#!/usr/bin/env python3
"""UserPromptSubmit hook: detect feedback, corrections and standing instructions.

It never stores preferences by itself. It only (1) logs the signal category to
<executive root>/quality/metrics/feedback_signals.jsonl (no message text beyond the matched phrase)
and (2) injects a short reminder so the Supervisor runs the right protocol.
Understands common English and Manglish (Malayalam in Latin script) phrasing.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import SCRIPTS, domain_root  # noqa: E402

PATTERNS = {
    "correction": [
        r"not correct", r"not what i (wanted|asked|meant)", r"that'?s not (it|right)", r"\bnot right\b",
        r"\bwrong\b", r"\bincorrect\b", r"\bredo\b", r"you missed", r"\bmistake\b",
        r"sheri ?y?alla", r"sheriyayilla", r"\bthett?(u|anu|i)\b", r"\bith ?alla\b", r"\bmosham\b",
    ],
    "repeat_instruction": [
        r"i (already )?told you", r"already (said|told|mentioned|explained)", r"as i said",
        r"paranj(athalle|ille|athu alle|irunnu)",
    ],
    "preserve_original": [
        r"use (the )?original", r"(don'?t|do not|dont) change anything else", r"same design",
        r"keep (it |the )?(the )?(original|same)", r"only change", r"\bm+att?(anda|aruthu|enda)\b",
    ],
    "recheck": [r"check again", r"\brecheck\b", r"verify again", r"double[- ]check", r"onnu koode (check|nokk)"],
    "standing_instruction": [
        r"from now on", r"\bin future\b", r"every time", r"remember (this|that)", r"\balways\b", r"\bnever\b",
        r"ini muthal", r"\beppozhum\b",
    ],
}
ACCEPT_STRONG = [r"\bproceed\b", r"\bapproved?\b", r"\bperfect\b", r"looks good", r"go ahead",
                 r"\bnannayi\b", r"\bkollam\b", r"\bexcellent\b"]
ACCEPT_SHORT = [r"^(ok|okay|good|great|super|better|sheri|done|fine|thanks|thank you)[.! ]*$"]

GUIDANCE = {
    "correction": "The user signalled the previous result is wrong. Run the Correction Protocol in the executive-supervisor-protocol skill: "
                  "re-read the original instruction in the task record, identify exactly what failed, fix only that, "
                  "re-run QA on the affected requirements, then have user-intelligence log a COR entry and a narrowly "
                  "scoped lesson.",
    "repeat_instruction": "The user says they already gave this instruction. Search the task record, knowledge/user/ and "
                          "this conversation for it before answering. Log category 'ignored-previous-instruction'. "
                          "Do not ask the user to repeat it.",
    "preserve_original": "Minimal-change mode: preserve the original source, design, model and data exactly. Change only "
                         "what the user named. QA must diff against the original and FAIL any unrequested change.",
    "recheck": "The user asked for re-verification. Send the deliverable back to qa-auditor for a fresh independent "
               "check with evidence. Do not simply reassert the earlier result.",
    "standing_instruction": "This message may contain a standing instruction (from now on / always / never). If it is a "
                            "general rule about future work (not just this task), record it via user-intelligence as an "
                            "explicit preference with the user's exact words as evidence, and confirm in one line.",
    "acceptance": "The user accepted the result. Close the task record with feedback=accepted and credit any lessons applied.",
}


def classify(prompt: str) -> list[tuple[str, str]]:
    text = prompt.lower().replace("’", "'")
    hits = []
    for cat, pats in PATTERNS.items():
        for p in pats:
            m = re.search(p, text)
            if m:
                hits.append((cat, m.group(0)))
                break
    if not any(c == "correction" for c, _ in hits):
        words = len(text.split())
        for p in ACCEPT_STRONG:
            m = re.search(p, text)
            if m and words <= 25:
                hits.append(("acceptance", m.group(0)))
                break
        else:
            for p in ACCEPT_SHORT:
                m = re.search(p, text.strip())
                if m:
                    hits.append(("acceptance", m.group(0).strip()))
                    break
    # "always"/"never" inside a long task brief is usually not a standing rule; keep it only
    # when an explicit future marker is present or the message is short.
    if any(c == "standing_instruction" and ph in ("always", "never") for c, ph in hits):
        explicit_future = re.search(r"from now on|in future|every time|remember (this|that)|ini muthal", text)
        if not explicit_future and len(text.split()) > 30:
            hits = [h for h in hits if h[0] != "standing_instruction"]
    return hits


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    prompt = data.get("prompt") or ""
    if not prompt.strip():
        return
    hits = classify(prompt)
    if not hits:
        return
    root = domain_root("executive")
    if root is None:
        return
    tool = str(SCRIPTS / "sinor.py")
    env = dict(os.environ, SINOR_ROOT=str(root))
    for cat, phrase in hits:
        subprocess.run([sys.executable, tool, "signal", "--category", cat, "--phrase", phrase[:60]],
                       capture_output=True, check=False, env=env)
    msg = "[feedback-detector] Signals: " + ", ".join(f"{c} ('{p}')" for c, p in hits) + ". " + \
          " ".join(GUIDANCE[c] for c, _ in hits)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": msg}}))


if __name__ == "__main__":
    main()
