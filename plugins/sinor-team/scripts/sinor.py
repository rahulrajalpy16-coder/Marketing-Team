#!/usr/bin/env python3
"""Sinor AI Executive Team - deterministic support tool.

Standard library only, so it runs in every Claude Code session without installs.
Data lives in the executive root of the Sinor workspace (scripts/workspace_lib.py);
env SINOR_ROOT overrides it. Nothing is ever written inside the plugin folder.

Subcommands (run `python3 sinor.py <cmd> -h` for details):
  context        Compact briefing printed by the SessionStart hook.
  task           new | list | show | close  (task records + requirement matrix)
  pref           add | list | update | supersede | forget
  lesson         add | list
  correction     add | list
  registry       Regenerate knowledge/user/PREFERENCE_CONFIDENCE.md
  learned        Recent lessons, corrections and preference changes (/what-you-learned)
  metrics        Team performance summary (/team-performance)
  calc           Quotation arithmetic with a traceable calculation log
  lint           Style and placeholder checks on a deliverable (md, txt, html, pdf, docx)
  validate       Validate the plugin's agents, skills and hooks plus the workspace data
  signal         Append a feedback signal (used by the UserPromptSubmit hook)
  quote          add | update | list   (quotation history in records/quotes.json)
  client         add | update | list   (clients in records/clients.json)
  doc            add | list            (document library in records/library/)
  sync           Commit knowledge/learning/quality/tasks/records and push them to main
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import workspace_lib  # noqa: E402

# Plugin folder (agents/, skills/, hooks/). Read only. SINOR_PLUGIN_ROOT exists for tests.
PLUGIN_ROOT = Path(os.environ.get("SINOR_PLUGIN_ROOT") or SCRIPT_DIR.parent)
SYNC_PATHS = ["knowledge", "learning", "quality", "tasks", "records"]

ROOT: Path | None = None  # executive data root; set by _set_root()


def _set_root(root: Path | None) -> None:
    """Point every data path at `root` (None means unresolved: paths are inert placeholders)."""
    global ROOT, USER_DIR, TASKS_ACTIVE, TASKS_DONE, METRICS, SIGNALS, LESSON_EVAL
    global RECORDS, QUOTES_FILE, CLIENTS_FILE, LIBRARY_DIR, LIBRARY_INDEX
    global LESSON_FILE, CORRECTION_FILE, REGISTRY_FILE, TOMB_FILE
    ROOT = Path(root) if root else None
    base = ROOT if ROOT else Path("__sinor_workspace_unresolved__")
    USER_DIR = base / "knowledge" / "user"
    TASKS_ACTIVE = base / "tasks" / "active"
    TASKS_DONE = base / "tasks" / "completed"
    METRICS = base / "quality" / "metrics" / "tasks.jsonl"
    SIGNALS = base / "quality" / "metrics" / "feedback_signals.jsonl"
    LESSON_EVAL = base / "learning" / "lessons" / "lesson_applications.jsonl"
    RECORDS = base / "records"
    QUOTES_FILE = RECORDS / "quotes.json"
    CLIENTS_FILE = RECORDS / "clients.json"
    LIBRARY_DIR = RECORDS / "library"
    LIBRARY_INDEX = LIBRARY_DIR / "index.json"
    LESSON_FILE = USER_DIR / "LEARNED_LESSONS.md"
    CORRECTION_FILE = USER_DIR / "CORRECTION_HISTORY.md"
    REGISTRY_FILE = USER_DIR / "PREFERENCE_CONFIDENCE.md"
    TOMB_FILE = USER_DIR / ".tombstones.json"


def _default_root(workspace: str | None = None) -> Path | None:
    """SINOR_ROOT always wins (compatibility); otherwise the workspace's executive root."""
    env = os.environ.get("SINOR_ROOT")
    if env:
        return Path(env)
    return workspace_lib.resolve_root("executive", workspace=workspace)


_set_root(_default_root())
QUOTE_STATUS = ["draft", "sent", "won", "lost", "expired", "unknown"]
DOC_KINDS = ["quotation", "supplier-quote", "datasheet", "manual", "drawing", "purchase-order", "certificate", "report", "other"]

PREF_FILES = {
    "USER_PROFILE": "Facts about the user's role and context",
    "COMMUNICATION_STYLE": "How the user writes and wants to be written to",
    "WORK_PREFERENCES": "Formats, deliverables, working methods",
    "DECISION_PATTERNS": "How the user prioritises and decides",
    "APPROVED_INSTRUCTIONS": "Standing instructions the user explicitly gave",
}

PREF_TYPES = {"explicit", "observed", "tentative"}
PREF_STATUS = {"active", "superseded"}
LESSON_STATUS = {"active", "tentative", "retired"}
CONFIDENCE = {"high", "medium", "low"}
TYPE_CONFIDENCE = {"explicit": "high", "observed": "medium", "tentative": "low"}
ROOT_CAUSES = [
    "misunderstood-objective",
    "missed-requirement",
    "excessive-modification",
    "poor-formatting",
    "incorrect-technical-info",
    "ignored-original-reference",
    "insufficient-verification",
    "ignored-previous-instruction",
    "unnecessary-questions",
    "wrong-output-medium",
    "other",
]
QA_STATUSES = {"PASS", "FAIL", "BLOCKED", "NOT VERIFIED", "PENDING"}
MANDATORY_KINDS = {"explicit", "implied"}

HEADER_RE = re.compile(r"^### (PREF|LES|COR)-(\d{4}) \| (.+?)\s*$")
FIELD_RE = re.compile(r"^- ([a-z_]+): ?(.*)$")
EM_DASH = "\u2014"


def today() -> str:
    return dt.date.today().isoformat()


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


# --------------------------------------------------------------------------
# Entry storage (PREF / LES / COR blocks inside Markdown files)
# --------------------------------------------------------------------------

def parse_entries(path: Path) -> list[dict]:
    """Parse '### KIND-NNNN | title' blocks followed by '- key: value' lines."""
    if not path.exists():
        return []
    entries, cur = [], None
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = HEADER_RE.match(line)
        if m:
            cur = {"kind": m.group(1), "id": f"{m.group(1)}-{m.group(2)}",
                   "title": m.group(3), "file": path.name, "line": lineno}
            entries.append(cur)
            continue
        if cur is None:
            continue
        f = FIELD_RE.match(line)
        if f:
            cur[f.group(1)] = f.group(2).strip()
        elif line.startswith("#") or line.strip() == "---":
            cur = None
    return entries


def all_pref_entries() -> list[dict]:
    out = []
    for name in PREF_FILES:
        out += parse_entries(USER_DIR / f"{name}.md")
    return out


def all_entries() -> list[dict]:
    return all_pref_entries() + parse_entries(LESSON_FILE) + parse_entries(CORRECTION_FILE)


def next_id(kind: str) -> str:
    nums = [int(e["id"].split("-")[1]) for e in all_entries() if e["kind"] == kind]
    # Tombstones keep deleted IDs from being reused.
    nums += [int(t["id"].split("-")[1]) for t in load_tombstones() if t["id"].startswith(kind + "-")]
    return f"{kind}-{(max(nums) + 1) if nums else 1:04d}"


def render_entry(entry_id: str, title: str, fields: dict) -> str:
    lines = [f"### {entry_id} | {title}"]
    for k, v in fields.items():
        if v is None:
            continue
        v = str(v).replace("\n", " ").strip()
        lines.append(f"- {k}: {v}")
    return "\n".join(lines) + "\n"


def append_entry(path: Path, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if text and not text.endswith("\n"):
        text += "\n"
    if text and not text.endswith("\n\n"):
        text += "\n"
    path.write_text(text + block, encoding="utf-8")


def find_entry(entry_id: str) -> dict:
    for e in all_entries():
        if e["id"] == entry_id:
            return e
    die(f"{entry_id} not found")
    return {}


def block_span(lines: list[str], start_idx: int) -> int:
    """Return the exclusive end index of the entry block starting at start_idx."""
    end = start_idx + 1
    while end < len(lines):
        ln = lines[end]
        if ln.startswith("#") or ln.strip() == "---":
            break
        if not ln.strip():
            # a blank line ends the block only if the next line is not a field
            if end + 1 >= len(lines) or not FIELD_RE.match(lines[end + 1]):
                break
        end += 1
    return end


def set_fields(entry_id: str, updates: dict) -> None:
    e = find_entry(entry_id)
    path = USER_DIR / e["file"]
    lines = path.read_text(encoding="utf-8").splitlines()
    start = e["line"] - 1
    end = block_span(lines, start)
    block = lines[start:end]
    for key, val in updates.items():
        val = str(val).replace("\n", " ").strip()
        for i, ln in enumerate(block):
            f = FIELD_RE.match(ln)
            if f and f.group(1) == key:
                block[i] = f"- {key}: {val}"
                break
        else:
            block.append(f"- {key}: {val}")
    lines[start:end] = block
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def remove_entry(entry_id: str) -> dict:
    e = find_entry(entry_id)
    path = USER_DIR / e["file"]
    lines = path.read_text(encoding="utf-8").splitlines()
    start = e["line"] - 1
    end = block_span(lines, start)
    while end < len(lines) and not lines[end].strip():
        end += 1
    del lines[start:end]
    path.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")
    return e


# --------------------------------------------------------------------------
# Preferences
# --------------------------------------------------------------------------

def cmd_pref(a: argparse.Namespace) -> None:
    if a.action == "add":
        if a.file not in PREF_FILES:
            die(f"--file must be one of {', '.join(PREF_FILES)}")
        if a.type not in PREF_TYPES:
            die(f"--type must be one of {sorted(PREF_TYPES)}")
        if a.type == "explicit" and not a.evidence:
            die("explicit preferences need --evidence quoting the user's own words")
        conf = a.confidence or TYPE_CONFIDENCE[a.type]
        if conf not in CONFIDENCE:
            die("--confidence must be high, medium or low")
        if a.type == "tentative" and conf == "high":
            die("a tentative inference cannot have high confidence")
        pid = next_id("PREF")
        block = render_entry(pid, a.title, {
            "status": "active", "type": a.type, "scope": a.scope, "confidence": conf,
            "statement": a.statement, "source": a.source, "evidence": a.evidence or "",
            "observations": "1", "created": today(), "updated": today(),
        })
        append_entry(USER_DIR / f"{a.file}.md", block)
        write_registry()
        print(pid)
    elif a.action == "list":
        rows = all_pref_entries()
        if not a.all:
            rows = [r for r in rows if r.get("status") == "active"]
        if a.type:
            rows = [r for r in rows if r.get("type") == a.type]
        for r in rows:
            print(f"{r['id']} [{r.get('type')}/{r.get('confidence')}/{r.get('scope')}/{r.get('status')}] "
                  f"{r['title']}: {r.get('statement', '')}")
        if not rows:
            print("(no matching preferences)")
    elif a.action == "update":
        e = find_entry(a.id)
        updates = {}
        for k in ("statement", "scope", "evidence", "source", "type", "confidence", "title"):
            v = getattr(a, k, None)
            if v:
                updates[k] = v
        if a.observe:
            updates["observations"] = str(int(e.get("observations", "1") or 1) + 1)
            updates["evidence"] = (e.get("evidence", "") + " ; " + a.observe).strip(" ;")
            if e.get("type") == "tentative" and int(updates["observations"]) >= 2 and not a.type:
                updates["type"] = "observed"
                updates["confidence"] = "medium"
        if updates.get("type") == "explicit" and not (updates.get("evidence") or e.get("evidence")):
            die("promoting to explicit needs --evidence with the user's own words")
        if "type" in updates and "confidence" not in updates:
            updates["confidence"] = TYPE_CONFIDENCE[updates["type"]]
        title = updates.pop("title", None)
        updates["updated"] = today()
        set_fields(a.id, updates)
        if title:
            rename_entry(a.id, title)
        write_registry()
        print(f"updated {a.id}: {', '.join(sorted(updates))}")
    elif a.action == "supersede":
        find_entry(a.id)
        find_entry(a.by)
        set_fields(a.id, {"status": "superseded", "superseded_by": a.by, "updated": today()})
        write_registry()
        print(f"{a.id} superseded by {a.by}")
    elif a.action == "forget":
        e = remove_entry(a.id)
        tomb = {"id": a.id, "deleted": today(), "reason": a.reason or "user request"}
        tombs = load_tombstones()
        tombs.append(tomb)
        save_tombstones(tombs)
        write_registry()
        print(f"forgot {a.id} ('{e['title']}') from {e['file']}. "
              "Note: earlier versions remain in git history until history is rewritten.")


def rename_entry(entry_id: str, title: str) -> None:
    e = find_entry(entry_id)
    path = USER_DIR / e["file"]
    lines = path.read_text(encoding="utf-8").splitlines()
    lines[e["line"] - 1] = f"### {entry_id} | {title}"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_tombstones() -> list[dict]:
    if TOMB_FILE.exists():
        return json.loads(TOMB_FILE.read_text(encoding="utf-8"))
    return []


def save_tombstones(t: list[dict]) -> None:
    TOMB_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOMB_FILE.write_text(json.dumps(t, indent=2) + "\n", encoding="utf-8")


def write_registry() -> None:
    prefs = all_pref_entries()
    lessons = parse_entries(LESSON_FILE)

    def table(rows: list[dict]) -> list[str]:
        if not rows:
            return ["_None._", ""]
        out = ["| ID | Title | Scope | Confidence | Obs. | Updated | File |",
               "|---|---|---|---|---|---|---|"]
        for r in rows:
            out.append(f"| {r['id']} | {r['title']} | {r.get('scope', '')} | {r.get('confidence', '')} | "
                       f"{r.get('observations', '')} | {r.get('updated', '')} | {r['file']} |")
        return out + [""]

    act = [p for p in prefs if p.get("status") == "active"]
    lines = [
        "# Preference Confidence Registry",
        "",
        "GENERATED FILE. Do not edit by hand. Regenerate with `python3 sinor.py registry`.",
        "",
        "Precedence when entries conflict: (1) the user's explicit instruction in the current task, "
        "(2) explicit preferences, (3) project or client scoped entries over global ones, "
        "(4) observed preferences, (5) tentative inferences. Tentative entries are hints only and "
        "must never override anything the user actually said.",
        "",
        "## Explicit confirmed preferences",
        *table([p for p in act if p.get("type") == "explicit" and p.get("scope", "global") == "global"]),
        "## Project, client or task-type scoped preferences",
        *table([p for p in act if p.get("scope", "global") != "global"]),
        "## Repeatedly observed preferences",
        *table([p for p in act if p.get("type") == "observed" and p.get("scope", "global") == "global"]),
        "## Tentative inferences (hints only)",
        *table([p for p in act if p.get("type") == "tentative" and p.get("scope", "global") == "global"]),
        "## Superseded preferences",
        *table([p for p in prefs if p.get("status") == "superseded"]),
        "## Lessons",
        "",
    ]
    if lessons:
        lines += ["| ID | Lesson | Status | Scope | Applied | Helped |", "|---|---|---|---|---|---|"]
        for l in lessons:
            lines.append(f"| {l['id']} | {l['title']} | {l.get('status', '')} | {l.get('scope', '')} | "
                         f"{l.get('applied', '0')} | {l.get('helped', '0')} |")
        lines.append("")
    else:
        lines += ["_None._", ""]
    lines += ["## Deleted at user request (tombstones, content removed)", ""]
    tombs = load_tombstones()
    if tombs:
        lines += ["| ID | Deleted | Reason |", "|---|---|---|"]
        lines += [f"| {t['id']} | {t['deleted']} | {t['reason']} |" for t in tombs]
    else:
        lines.append("_None._")
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def cmd_registry(_a: argparse.Namespace) -> None:
    write_registry()
    print(f"wrote {REGISTRY_FILE.relative_to(ROOT)}")


# --------------------------------------------------------------------------
# Lessons and corrections
# --------------------------------------------------------------------------

def cmd_lesson(a: argparse.Namespace) -> None:
    if a.action == "add":
        if a.root_cause not in ROOT_CAUSES:
            die(f"--root-cause must be one of {ROOT_CAUSES}")
        status = a.status or "tentative"
        if status not in LESSON_STATUS:
            die(f"--status must be one of {sorted(LESSON_STATUS)}")
        lid = next_id("LES")
        append_entry(LESSON_FILE, render_entry(lid, a.title, {
            "status": status, "scope": a.scope, "trigger": a.trigger, "lesson": a.lesson,
            "root_cause": a.root_cause, "source": a.source, "evidence": a.evidence,
            "applied": "0", "helped": "0", "created": today(), "updated": today(),
        }))
        write_registry()
        print(lid)
    elif a.action == "update":
        updates = {k: v for k, v in (("status", a.status), ("lesson", a.lesson), ("scope", a.scope),
                                     ("trigger", a.trigger)) if v}
        if a.status and a.status not in LESSON_STATUS:
            die(f"--status must be one of {sorted(LESSON_STATUS)}")
        updates["updated"] = today()
        set_fields(a.id, updates)
        write_registry()
        print(f"updated {a.id}")
    else:
        rows = parse_entries(LESSON_FILE)
        if not a.all:
            rows = [r for r in rows if r.get("status") != "retired"]
        for r in rows[-a.recent:]:
            print(f"{r['id']} [{r.get('status')}/{r.get('scope')}] {r['title']}\n"
                  f"   lesson: {r.get('lesson', '')}\n   when: {r.get('trigger', '')}\n"
                  f"   evidence: {r.get('evidence', '')} (source {r.get('source', '')})\n"
                  f"   applied {r.get('applied', '0')}x, helped {r.get('helped', '0')}x")
        if not rows:
            print("(no lessons recorded yet)")


def cmd_correction(a: argparse.Namespace) -> None:
    if a.action == "add":
        if a.category not in ROOT_CAUSES:
            die(f"--category must be one of {ROOT_CAUSES}")
        cid = next_id("COR")
        append_entry(CORRECTION_FILE, render_entry(cid, a.title, {
            "date": today(), "task": a.task, "user_feedback": a.feedback, "category": a.category,
            "what_went_wrong": a.wrong, "fix_applied": a.fix, "lesson": a.lesson or "none",
            "detail": a.detail or "",
        }))
        print(cid)
    else:
        rows = parse_entries(CORRECTION_FILE)
        for r in rows[-a.recent:]:
            print(f"{r['id']} {r.get('date')} [{r.get('category')}] {r['title']}\n"
                  f"   user said: {r.get('user_feedback', '')}\n   wrong: {r.get('what_went_wrong', '')}\n"
                  f"   fix: {r.get('fix_applied', '')}  lesson: {r.get('lesson', '')}")
        if not rows:
            print("(no corrections recorded yet)")


def cmd_learned(a: argparse.Namespace) -> None:
    since = (dt.date.today() - dt.timedelta(days=a.days)).isoformat()
    prefs = [p for p in all_pref_entries() if p.get("updated", "") >= since]
    lessons = [l for l in parse_entries(LESSON_FILE) if l.get("updated", "") >= since]
    cors = [c for c in parse_entries(CORRECTION_FILE) if c.get("date", "") >= since]
    print(f"# What the team learned (last {a.days} days)\n")
    print("## Preferences added or changed")
    for p in prefs or []:
        print(f"- {p['id']} ({p.get('type')}, {p.get('confidence')}, {p.get('scope')}, {p.get('status')}): "
              f"{p.get('statement', '')}\n  evidence: {p.get('evidence', '') or 'n/a'} | source: {p.get('source', '')}")
    if not prefs:
        print("- none")
    print("\n## Lessons")
    for l in lessons:
        print(f"- {l['id']} ({l.get('status')}, {l.get('scope')}): {l.get('lesson', '')}\n"
              f"  why: {l.get('evidence', '')} | applied {l.get('applied', '0')}x, helped {l.get('helped', '0')}x")
    if not lessons:
        print("- none")
    print("\n## Corrections you gave")
    for c in cors:
        print(f"- {c['id']} {c.get('date')}: \"{c.get('user_feedback', '')}\" -> {c.get('category')}; "
              f"lesson {c.get('lesson', 'none')}")
    if not cors:
        print("- none")
    tombs = [t for t in load_tombstones() if t["deleted"] >= since]
    if tombs:
        print("\n## Forgotten at your request")
        for t in tombs:
            print(f"- {t['id']} on {t['deleted']}")


# --------------------------------------------------------------------------
# Tasks and requirement matrix
# --------------------------------------------------------------------------

TASK_TEMPLATE = """# {tid}: {title}

- opened: {opened}
- tier: {tier}
- type: {ttype}
- status: active

## 1. Original instruction (verbatim, never edit)

{instruction_block}

## 2. Intent interpretation

1. Literal request:
2. Likely intended outcome:
3. Non-negotiable constraints:
4. Relevant preferences and lessons applied (IDs):
5. Required deliverables (medium and format):
6. Potential misunderstandings:
7. Confidence (high / medium / low) and decision (proceed / ask one question):

## 3. Requirement matrix

Kind: explicit (user said it), implied (strongly supported), optional (improvement). Status: PASS, FAIL, BLOCKED, NOT VERIFIED, PENDING.

| ID | Original instruction | Interpretation | Kind | Owner | Deliverable | Acceptance criteria | Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| R1 | | | explicit | | | | | PENDING |

## 4. Plan and delegation log

| Step | Agent | Mode (parallel / sequential) | Brief | Result |
|---|---|---|---|---|

## 5. Deliverables

Files live in `deliverables/` next to this record.

## 6. QA results

| Cycle | Auditor verdict | Failing requirements | Corrective action | Report |
|---|---|---|---|---|

## 7. Assumptions and open items

## 8. User feedback and learning
"""


def slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s[:40] or "task"


def all_task_dirs() -> list[Path]:
    out = []
    for base in (TASKS_ACTIVE, TASKS_DONE):
        if base.exists():
            out += [p for p in base.iterdir() if p.is_dir() and p.name.startswith("TASK-")]
    return sorted(out)


def task_id(dirname: str) -> str:
    m = re.match(r"^(TASK-\d{8}-\d+)", dirname)
    return m.group(1) if m else dirname


def find_task(tid: str) -> Path:
    for p in all_task_dirs():
        if p.name == tid or p.name.startswith(tid + "-") or p.name.startswith(tid):
            return p
    die(f"task {tid} not found")
    return Path()


def cmd_task(a: argparse.Namespace) -> None:
    if a.action == "new":
        instruction = a.instruction if a.instruction is not None else sys.stdin.read()
        instruction = instruction.strip()
        if not instruction:
            die("the original instruction is required (--instruction or stdin)")
        # Time-based IDs: parallel cloud sessions cannot collide (a sequence number could).
        stamp = dt.datetime.now()
        tid = f"TASK-{stamp:%Y%m%d-%H%M%S}"
        while any(p.name.startswith(tid) for p in all_task_dirs()):
            stamp += dt.timedelta(seconds=1)
            tid = f"TASK-{stamp:%Y%m%d-%H%M%S}"
        d = TASKS_ACTIVE / f"{tid}-{slugify(a.title)}"
        (d / "deliverables").mkdir(parents=True, exist_ok=False)
        quoted = "\n".join("> " + ln if ln else ">" for ln in instruction.splitlines())
        (d / "TASK.md").write_text(TASK_TEMPLATE.format(
            tid=tid, title=a.title, opened=now(), tier=a.tier or 1, ttype=a.type or "general",
            instruction_block=quoted), encoding="utf-8")
        (d / "original_instruction.txt").write_text(instruction + "\n", encoding="utf-8")
        print(d.relative_to(ROOT))
    elif a.action == "list":
        for p in all_task_dirs():
            if a.all or p.parent == TASKS_ACTIVE:
                state = "active" if p.parent == TASKS_ACTIVE else "completed"
                print(f"{state:9} {p.name}")
    elif a.action == "show":
        p = find_task(a.id)
        print((p / "TASK.md").read_text(encoding="utf-8"))
        reqs = parse_requirements(p / "TASK.md")
        print(json.dumps(summarise_requirements(reqs), indent=2))
    elif a.action == "close":
        close_task(a)


def parse_requirements(task_md: Path) -> list[dict]:
    text = task_md.read_text(encoding="utf-8")
    sec = re.search(r"## 3\. Requirement matrix(.*?)(?:\n## |\Z)", text, re.S)
    if not sec:
        return []
    rows = []
    for ln in sec.group(1).splitlines():
        if not ln.startswith("| R"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 9:
            continue
        rows.append({"id": cells[0], "original": cells[1], "kind": cells[3].lower(),
                     "owner": cells[4], "evidence": cells[7], "status": cells[8].upper()})
    return rows


def summarise_requirements(reqs: list[dict]) -> dict:
    mand = [r for r in reqs if r["kind"] in MANDATORY_KINDS]
    counts: dict[str, int] = {}
    for r in reqs:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    unresolved = [r["id"] for r in mand if r["status"] != "PASS"]
    no_evidence = [r["id"] for r in reqs if r["status"] == "PASS" and not r["evidence"]]
    return {"total": len(reqs), "mandatory": len(mand), "status_counts": counts,
            "mandatory_not_pass": unresolved, "pass_without_evidence": no_evidence,
            "fully_verified": bool(mand) and not unresolved and not no_evidence}


def close_task(a: argparse.Namespace) -> None:
    p = find_task(a.id)
    reqs = parse_requirements(p / "TASK.md")
    summ = summarise_requirements(reqs)
    bad = [r["id"] for r in reqs if r["status"] not in QA_STATUSES]
    if bad:
        die(f"invalid status values in rows {bad}; use {sorted(QA_STATUSES)}")
    if not reqs:
        die("requirement matrix is empty; record at least one requirement before closing")
    final = "PASS" if summ["fully_verified"] else ("BLOCKED" if any(
        r["status"] == "BLOCKED" for r in reqs) else "PARTIAL")
    if a.claim_pass and final != "PASS":
        die(f"cannot close as PASS: mandatory not PASS {summ['mandatory_not_pass']}, "
            f"PASS without evidence {summ['pass_without_evidence']}", 2)
    lessons = [x for x in (a.lessons or "").split(",") if x]
    head = (p / "TASK.md").read_text(encoding="utf-8")
    if a.tier is None:
        m = re.search(r"^- tier: (\d+)", head, re.M)
        a.tier = int(m.group(1)) if m else 1
    if a.type is None:
        m = re.search(r"^- type: (\S+)", head, re.M)
        a.type = m.group(1) if m else "general"
    rec = {
        "task": task_id(p.name), "title": p.name[len(task_id(p.name)) + 1:], "tier": a.tier, "type": a.type,
        "agents": [x for x in (a.agents or "").split(",") if x],
        "closed": now(), "requirements": summ, "final_status": final,
        "qa_cycles": a.qa_cycles, "qa_first_pass": a.qa_cycles == 1 and final == "PASS",
        "user_corrections": a.corrections, "clarifications": a.clarifications,
        "feedback": a.feedback, "lessons_applied": lessons,
        "cost_usd": a.cost_usd, "notes": a.notes or "",
    }
    METRICS.parent.mkdir(parents=True, exist_ok=True)
    with METRICS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
    for lid in lessons:
        e = find_entry(lid)
        helped = a.feedback in ("accepted", "none")
        set_fields(lid, {"applied": str(int(e.get("applied", "0")) + 1),
                         "helped": str(int(e.get("helped", "0")) + (1 if helped else 0)),
                         "last_applied": today()})
        LESSON_EVAL.parent.mkdir(parents=True, exist_ok=True)
        with LESSON_EVAL.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"lesson": lid, "task": rec["task"], "date": today(),
                                 "feedback": a.feedback, "helped": helped}) + "\n")
    if lessons:
        write_registry()
    text = (p / "TASK.md").read_text(encoding="utf-8")
    text = text.replace("- status: active", f"- status: closed ({final}) {now()}", 1)
    (p / "TASK.md").write_text(text, encoding="utf-8")
    if not a.keep_active and p.parent == TASKS_ACTIVE:
        TASKS_DONE.mkdir(parents=True, exist_ok=True)
        dest = TASKS_DONE / p.name
        shutil.move(str(p), str(dest))
        p = dest
    print(json.dumps({"closed": p.name, "final_status": final, "requirements": summ}, indent=2))


# --------------------------------------------------------------------------
# Metrics
# --------------------------------------------------------------------------

def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def cmd_metrics(a: argparse.Namespace) -> None:
    recs = load_jsonl(METRICS)
    if a.include_tests is False:
        recs = [r for r in recs if r.get("type") != "e2e-test"]
    sig = load_jsonl(SIGNALS)
    print("# Sinor AI Executive Team - performance summary\n")
    print(f"Source: {METRICS.relative_to(ROOT)} ({len(recs)} closed tasks"
          f"{'' if a.include_tests else ', e2e test runs excluded'}), "
          f"{SIGNALS.relative_to(ROOT)} ({len(sig)} feedback signals). Nothing here is estimated.\n")
    if not recs:
        print("No closed tasks recorded yet. Metrics appear after the first task is closed with "
              "`python3 sinor.py task close`.")
    else:
        n = len(recs)
        tot = sum(r["requirements"]["total"] for r in recs)
        mand = sum(r["requirements"]["mandatory"] for r in recs)
        mand_open = sum(len(r["requirements"]["mandatory_not_pass"]) for r in recs)
        fp = sum(1 for r in recs if r.get("qa_first_pass"))
        done = sum(1 for r in recs if r["final_status"] == "PASS")
        cyc = sum(r.get("qa_cycles", 0) for r in recs)
        corr = sum(r.get("user_corrections", 0) for r in recs)
        clar = sum(r.get("clarifications", 0) for r in recs)
        acc = sum(1 for r in recs if r.get("feedback") == "accepted")
        fb = sum(1 for r in recs if r.get("feedback") in ("accepted", "corrected"))
        costs = [r["cost_usd"] for r in recs if r.get("cost_usd") is not None]
        pct = lambda x, y: f"{(100 * x / y):.0f}%" if y else "n/a"
        print("| Metric | Value |\n|---|---|")
        print(f"| Tasks closed | {n} |")
        print(f"| Fully verified (all mandatory requirements PASS with evidence) | {done} ({pct(done, n)}) |")
        print(f"| Requirement coverage (mandatory PASS / mandatory) | {mand - mand_open}/{mand} ({pct(mand - mand_open, mand)}) |")
        print(f"| Requirements tracked | {tot} |")
        print(f"| First-pass QA success | {fp}/{n} ({pct(fp, n)}) |")
        print(f"| Average QA cycles per task | {cyc / n:.2f} |")
        print(f"| User corrections | {corr} |")
        print(f"| Clarifying questions asked | {clar} ({clar / n:.2f} per task) |")
        print(f"| User acceptance (accepted / tasks with feedback) | {acc}/{fb} ({pct(acc, fb)}) |")
        print(f"| Recorded cost | {'$%.2f over %d tasks' % (sum(costs), len(costs)) if costs else 'not recorded'} |")
        types: dict[str, int] = {}
        for r in recs:
            types[r.get("type", "?")] = types.get(r.get("type", "?"), 0) + 1
        print("\nTasks by type: " + ", ".join(f"{k} {v}" for k, v in sorted(types.items())))
        agents: dict[str, int] = {}
        for r in recs:
            for ag in r.get("agents", []):
                agents[ag] = agents.get(ag, 0) + 1
        if agents:
            print("Agent usage: " + ", ".join(f"{k} {v}" for k, v in sorted(agents.items(), key=lambda x: -x[1])))
    cors = parse_entries(CORRECTION_FILE)
    if cors:
        cats: dict[str, int] = {}
        for c in cors:
            cats[c.get("category", "?")] = cats.get(c.get("category", "?"), 0) + 1
        print("\nRepeated failure types (from corrections): " +
              ", ".join(f"{k} {v}" for k, v in sorted(cats.items(), key=lambda x: -x[1])))
    lessons = parse_entries(LESSON_FILE)
    used = [l for l in lessons if int(l.get("applied", "0")) > 0]
    if used:
        print("\nLesson effectiveness:")
        for l in used:
            print(f"- {l['id']} {l['title']}: applied {l['applied']}x, helped {l.get('helped', '0')}x")
    if sig:
        kinds: dict[str, int] = {}
        for s in sig:
            kinds[s["category"]] = kinds.get(s["category"], 0) + 1
        print("\nFeedback signals detected in your messages: " +
              ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())))


def cmd_signal(a: argparse.Namespace) -> None:
    SIGNALS.parent.mkdir(parents=True, exist_ok=True)
    with SIGNALS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": now(), "category": a.category, "phrase": a.phrase}) + "\n")


# --------------------------------------------------------------------------
# Quotation calculator
# --------------------------------------------------------------------------

TWO = Decimal("0.01")


def dec(v, field: str) -> Decimal:
    if v is None or str(v).strip() == "":
        die(f"missing value for {field}. Prices, quantities and rates must come from the user "
            "or an approved source; the calculator never invents them.")
    try:
        return Decimal(str(v).replace(",", ""))
    except InvalidOperation:
        die(f"{field} is not a number: {v!r}")
    return Decimal(0)


def money(d: Decimal) -> str:
    return f"{d.quantize(TWO, rounding=ROUND_HALF_UP):,.2f}"


def calculate(spec: dict) -> dict:
    cur = spec.get("currency") or die("currency is required") or ""
    log, lines = [], []
    sub = Decimal(0)
    for i, it in enumerate(spec.get("items") or [], 1):
        qty = dec(it.get("qty"), f"items[{i}].qty")
        price = dec(it.get("unit_price"), f"items[{i}].unit_price")
        amt = (qty * price).quantize(TWO, rounding=ROUND_HALF_UP)
        sub += amt
        lines.append({"no": it.get("no", i), "description": it.get("description", ""),
                      "qty": str(qty.normalize()) if qty == qty.to_integral() else str(qty),
                      "unit": it.get("unit", ""), "unit_price": money(price), "amount": money(amt)})
        log.append(f"Line {it.get('no', i)}: {qty} x {money(price)} = {money(amt)} {cur}")
    if not lines:
        die("no items supplied")
    res = {"currency": cur, "lines": lines, "log": log}
    if spec.get("alternatives"):
        log.append("Items are alternative options, so no subtotal or total is computed.")
        return res
    res["subtotal"] = money(sub)
    log.append(f"Subtotal = {' + '.join(l['amount'] for l in lines)} = {money(sub)} {cur}")
    base = sub
    disc = spec.get("discount")
    if disc:
        if not disc.get("source"):
            die("discount needs a 'source' (who approved it). Discounts are never invented.")
        val = dec(disc.get("value"), "discount.value")
        if disc.get("type") == "percent":
            d_amt = (sub * val / 100).quantize(TWO, rounding=ROUND_HALF_UP)
            log.append(f"Discount {val}% of {money(sub)} = {money(d_amt)} {cur} (source: {disc['source']})")
        else:
            d_amt = val.quantize(TWO, rounding=ROUND_HALF_UP)
            log.append(f"Discount fixed {money(d_amt)} {cur} (source: {disc['source']})")
        base = sub - d_amt
        res["discount"] = money(d_amt)
        res["after_discount"] = money(base)
        log.append(f"After discount = {money(sub)} - {money(d_amt)} = {money(base)} {cur}")
    vat_amt = Decimal(0)
    if spec.get("vat_percent") not in (None, ""):
        vp = dec(spec["vat_percent"], "vat_percent")
        vat_amt = (base * vp / 100).quantize(TWO, rounding=ROUND_HALF_UP)
        res["vat_percent"] = str(vp)
        res["vat"] = money(vat_amt)
        log.append(f"VAT {vp}% of {money(base)} = {money(vat_amt)} {cur}")
    total = base + vat_amt
    res["total"] = money(total)
    log.append(f"Total = {money(base)} + {money(vat_amt)} = {money(total)} {cur}")
    fx = spec.get("fx")
    if fx:
        if not fx.get("source"):
            die("fx needs a 'source' and date for the exchange rate")
        rate = dec(fx.get("rate"), "fx.rate")
        conv = (total * rate).quantize(TWO, rounding=ROUND_HALF_UP)
        res["fx"] = {"to": fx.get("to"), "rate": str(rate), "source": fx["source"], "total": money(conv)}
        log.append(f"Converted total = {money(total)} {cur} x {rate} = {money(conv)} {fx.get('to')} "
                   f"(rate source: {fx['source']})")
    return res


def cmd_calc(a: argparse.Namespace) -> None:
    raw = Path(a.spec).read_text(encoding="utf-8") if a.spec != "-" else sys.stdin.read()
    res = calculate(json.loads(raw))
    if a.json:
        print(json.dumps(res, indent=2))
        return
    cur = res["currency"]
    print(f"| No | Description | Qty | Unit | Price ({cur}) | Amount ({cur}) |\n|---|---|---|---|---|---|")
    for l in res["lines"]:
        print(f"| {l['no']} | {l['description']} | {l['qty']} | {l['unit']} | {l['unit_price']} | {l['amount']} |")
    print("\nCalculation log:")
    for s in res["log"]:
        print(f"- {s}")


# --------------------------------------------------------------------------
# Lint
# --------------------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\b(XXXXX+|TBD|TODO|lorem ipsum)\b|\[(INSERT|PLACEHOLDER)[^\]]*\]", re.I)
# Upper-case bracket fields such as [SIGNATORY NAME] or [EMAIL ADDRESS] (case-sensitive on purpose,
# so ordinary bracketed text like [1] or [optional] is not flagged).
FIELD_PLACEHOLDER_RE = re.compile(r"\[[A-Z][A-Z0-9 _/&.-]{2,}\]")


def extract_text(path: Path) -> str:
    suf = path.suffix.lower()
    if suf == ".pdf":
        if shutil.which("pdftotext"):
            return subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True,
                                  text=True, check=False).stdout
        die("pdftotext not available to read the PDF")
    if suf in (".docx", ".pptx", ".xlsx"):
        with zipfile.ZipFile(path) as z:
            parts = [n for n in z.namelist() if n.endswith(".xml") and
                     (n.startswith("word/") or n.startswith("ppt/slides/") or "sharedStrings" in n)]
            xml = " ".join(z.read(n).decode("utf-8", "ignore") for n in parts)
        return re.sub(r"<[^>]+>", " ", xml)
    return path.read_text(encoding="utf-8", errors="ignore")


def lint_text(text: str) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    for i, ln in enumerate(text.splitlines(), 1):
        if EM_DASH in ln:
            errors.append(f"line {i}: em dash (user preference PREF: no em dashes): {ln.strip()[:90]}")
        for m in PLACEHOLDER_RE.finditer(ln):
            warnings.append(f"line {i}: unresolved placeholder '{m.group(0)}'")
        for m in FIELD_PLACEHOLDER_RE.finditer(ln):
            warnings.append(f"line {i}: unfilled field '{m.group(0)}' (must be listed as an open item for the user)")
    return errors, warnings


def cmd_lint(a: argparse.Namespace) -> None:
    total_err = 0
    for f in a.files:
        p = Path(f)
        errors, warnings = lint_text(extract_text(p))
        words = len(re.findall(r"\b\w[\w'-]*\b", extract_text(p)))
        print(f"{p}: {len(errors)} error(s), {len(warnings)} warning(s), {words} words")
        for e in errors:
            print(f"  ERROR {e}")
        for w in warnings:
            print(f"  WARN  {w}")
        total_err += len(errors)
    sys.exit(1 if total_err else 0)


# --------------------------------------------------------------------------
# Validate configuration
# --------------------------------------------------------------------------

def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    out = {}
    for ln in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", ln)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def _rel(p: Path) -> str:
    for base in (PLUGIN_ROOT, ROOT):
        try:
            return str(p.relative_to(base))
        except (ValueError, TypeError):
            continue
    return str(p)


def validate() -> list[str]:
    """Check the plugin's own agents, skills and hooks, then the workspace data."""
    problems: list[str] = []
    names = set()
    agents_dir = PLUGIN_ROOT / "agents"
    if not agents_dir.is_dir():
        problems.append("plugin agents/ folder is missing")
    for f in sorted(agents_dir.glob("*.md")):
        fm = frontmatter(f)
        if not fm.get("name") or not fm.get("description"):
            problems.append(f"agents/{f.name}: missing name or description frontmatter")
            continue
        if fm["name"] != f.stem:
            problems.append(f"agents/{f.name}: name '{fm['name']}' does not match file name")
        if fm["name"] in names:
            problems.append(f"duplicate agent name {fm['name']}")
        names.add(fm["name"])
    skills_dir = PLUGIN_ROOT / "skills"
    if not skills_dir.is_dir():
        problems.append("plugin skills/ folder is missing")
    for d in sorted(skills_dir.glob("*")):
        if d.is_dir():
            sk = d / "SKILL.md"
            if not sk.exists():
                problems.append(f"skills/{d.name}: no SKILL.md")
            elif not frontmatter(sk).get("description"):
                problems.append(f"skills/{d.name}/SKILL.md: missing description")
    hooks_file = PLUGIN_ROOT / "hooks" / "hooks.json"
    if hooks_file.exists():
        try:
            cfg = json.loads(hooks_file.read_text(encoding="utf-8"))
            hooks_cfg = cfg.get("hooks", cfg) if isinstance(cfg, dict) else {}
            for ev, groups in hooks_cfg.items():
                if not isinstance(groups, list):
                    continue
                for g in groups:
                    for h in g.get("hooks", []):
                        cmd = h.get("command", "")
                        m = re.search(r"\$\{?CLAUDE_PLUGIN_ROOT\}?\"?/([^\s\"]+)", cmd)
                        if m and not (PLUGIN_ROOT / m.group(1)).exists():
                            problems.append(f"hooks.json {ev} hook script missing: {m.group(1)}")
        except json.JSONDecodeError as e:
            problems.append(f"hooks/hooks.json invalid JSON: {e}")
    # workspace data structure
    if ROOT is None:
        problems.append("executive workspace root is not resolved; run /sinor-team:setup")
        return problems
    for rel in ("knowledge/user", "tasks", "quality", "learning", "records"):
        if not (ROOT / rel).is_dir():
            problems.append(f"workspace folder missing: executive/{rel} (run workspace.py init to create the skeleton)")
    ids = {}
    for e in all_entries():
        if e["id"] in ids:
            problems.append(f"duplicate id {e['id']} in {e['file']} and {ids[e['id']]}")
        ids[e["id"]] = e["file"]
        if e["kind"] == "PREF":
            for k in ("status", "type", "scope", "confidence", "statement", "source", "created"):
                if not e.get(k):
                    problems.append(f"{e['id']} ({e['file']}): missing field '{k}'")
            if e.get("type") and e["type"] not in PREF_TYPES:
                problems.append(f"{e['id']}: bad type {e['type']}")
            if e.get("status") and e["status"] not in PREF_STATUS:
                problems.append(f"{e['id']}: bad status {e['status']}")
            if e.get("type") == "explicit" and not e.get("evidence"):
                problems.append(f"{e['id']}: explicit preference without evidence")
            if e.get("type") == "tentative" and e.get("confidence") == "high":
                problems.append(f"{e['id']}: tentative inference marked high confidence")
        if e["kind"] == "LES":
            for k in ("status", "scope", "lesson", "root_cause", "source", "evidence"):
                if not e.get(k):
                    problems.append(f"{e['id']}: missing field '{k}'")
            if e.get("status") and e["status"] not in LESSON_STATUS:
                problems.append(f"{e['id']}: bad status {e['status']}")
        if e["kind"] == "COR" and e.get("category") not in ROOT_CAUSES:
            problems.append(f"{e['id']}: bad category {e.get('category')}")
    scan = [PLUGIN_ROOT / "agents", PLUGIN_ROOT / "skills", ROOT / "knowledge", ROOT / "learning"]
    for p in scan:
        for f in (list(p.rglob("*.md")) if p.exists() else []):
            if EM_DASH in f.read_text(encoding="utf-8", errors="ignore"):
                problems.append(f"{_rel(f)}: contains an em dash")
    return problems


def cmd_validate(_a: argparse.Namespace) -> None:
    probs = validate()
    agents = len(list((PLUGIN_ROOT / "agents").glob("*.md")))
    skills = len([d for d in (PLUGIN_ROOT / "skills").glob("*") if d.is_dir()])
    print(f"agents: {agents}, skills: {skills}, knowledge entries: {len(all_entries())}")
    for p in probs:
        print(f"PROBLEM: {p}")
    print("VALID" if not probs else f"{len(probs)} problem(s)")
    sys.exit(1 if probs else 0)


# --------------------------------------------------------------------------
# Records: quotes, clients, document library (what the Sinor Desk shows)
# --------------------------------------------------------------------------

def load_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8") or "[]")
    return data if isinstance(data, list) else []


def save_records(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def iso_date(v: str | None) -> str:
    """Accept DD/MM/YYYY (UAE convention) or YYYY-MM-DD; store ISO."""
    v = (v or "").strip()
    m = re.match(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$", v)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            return dt.date(y, mo, d).isoformat()
        except ValueError:
            die(f"not a real date: {v}")
    if v and not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
        die(f"date must be DD/MM/YYYY or YYYY-MM-DD, got {v!r}")
    return v


def amount_of(v: str | None):
    if v is None or str(v).strip() == "":
        return None
    try:
        return float(Decimal(str(v).replace(",", "")))
    except InvalidOperation:
        die(f"amount is not a number: {v!r}")
    return None


QUOTE_FIELDS = ("qtn", "date", "client", "vessel", "subject", "currency", "amount", "status", "valid_until", "notes", "source", "file")
CLIENT_FIELDS = ("name", "contact", "phone", "email", "trn", "address", "vessels", "notes")


def cmd_quote(a: argparse.Namespace) -> None:
    rows = load_records(QUOTES_FILE)
    if a.action in ("add", "update"):
        if not a.qtn:
            die("--qtn is required (use SMS-QT{YYYY}-XXXXX only if the number is truly unknown)")
        existing = next((r for r in rows if r.get("qtn") == a.qtn), None)
        if a.action == "add" and existing:
            die(f"{a.qtn} already exists; use quote update")
        if a.action == "update" and not existing:
            die(f"{a.qtn} not found")
        if a.status and a.status not in QUOTE_STATUS:
            die(f"--status must be one of {QUOTE_STATUS}")
        rec = existing or {"qtn": a.qtn, "created": now(), "status": "sent", "currency": "USD"}
        for k in QUOTE_FIELDS[1:]:
            v = getattr(a, k, None)
            if v is None:
                continue
            if k in ("date", "valid_until"):
                v = iso_date(v)
            elif k == "amount":
                v = amount_of(v)
            elif k == "currency":
                v = v.upper()
            rec[k] = v
        rec["updated"] = now()
        if not existing:
            rows.append(rec)
        save_records(QUOTES_FILE, rows)
        print(f"{'added' if a.action == 'add' else 'updated'} {a.qtn}: {rec.get('status')} {rec.get('currency', '')} {rec.get('amount') if rec.get('amount') is not None else 'amount not set'}")
        return
    q = (a.query or "").lower()
    sel = [r for r in rows if (not a.status or r.get("status") == a.status)
           and (not q or q in json.dumps(r, ensure_ascii=False).lower())]
    sel.sort(key=lambda r: r.get("date") or "", reverse=True)
    if a.json:
        print(json.dumps(sel, indent=2, ensure_ascii=False))
        return
    if not sel:
        print("(no quotes match)")
    for r in sel:
        amt = money(Decimal(str(r["amount"]))) if r.get("amount") is not None else "amount not set"
        print(f"{r.get('qtn')} | {r.get('date') or 'no date'} | {r.get('client') or '-'} | {r.get('vessel') or '-'} | "
              f"{r.get('currency', '')} {amt} | {r.get('status')} | {r.get('subject') or ''}")
    won = sum(1 for r in rows if r.get("status") == "won")
    lost = sum(1 for r in rows if r.get("status") == "lost")
    print(f"\n{len(rows)} quotes in history; won {won}, lost {lost}; win rate "
          f"{(str(round(100 * won / (won + lost))) + '%') if won + lost else 'n/a'}. Amounts are historical.")


def cmd_client(a: argparse.Namespace) -> None:
    rows = load_records(CLIENTS_FILE)
    if a.action in ("add", "update"):
        if not a.name:
            die("--name is required")
        existing = next((r for r in rows if r.get("name", "").lower() == a.name.lower()), None)
        if a.action == "add" and existing:
            die(f"{a.name} already exists; use client update")
        if a.action == "update" and not existing:
            die(f"{a.name} not found")
        rec = existing or {"name": a.name, "created": now(), "vessels": []}
        for k in CLIENT_FIELDS[1:]:
            v = getattr(a, k, None)
            if v is None:
                continue
            if k == "vessels":
                v = [x.strip() for x in re.split(r"[,;|]", v) if x.strip()]
            rec[k] = v
        rec["updated"] = now()
        if not existing:
            rows.append(rec)
        save_records(CLIENTS_FILE, rows)
        print(f"{'added' if a.action == 'add' else 'updated'} client {a.name}")
        return
    q = (a.query or "").lower()
    sel = sorted([r for r in rows if not q or q in json.dumps(r, ensure_ascii=False).lower()], key=lambda r: r.get("name", ""))
    if a.json:
        print(json.dumps(sel, indent=2, ensure_ascii=False))
        return
    quotes = load_records(QUOTES_FILE)
    if not sel:
        print("(no clients match)")
    for r in sel:
        n = sum(1 for x in quotes if (x.get("client") or "").lower() == r["name"].lower())
        print(f"{r['name']} | {r.get('contact') or '-'} | {r.get('phone') or '-'} | TRN {r.get('trn') or '-'} | "
              f"vessels {', '.join(r.get('vessels') or []) or '-'} | {n} quotes")


def cmd_doc(a: argparse.Namespace) -> None:
    rows = load_records(LIBRARY_INDEX)
    if a.action == "add":
        src = Path(a.file)
        if not src.is_file():
            die(f"file not found: {a.file}")
        if a.kind not in DOC_KINDS:
            die(f"--kind must be one of {DOC_KINDS}")
        dest_dir = LIBRARY_DIR / a.kind
        dest_dir.mkdir(parents=True, exist_ok=True)
        name = re.sub(r"[^A-Za-z0-9._ -]+", "_", src.name).strip() or "document"
        dest = dest_dir / name
        stem, suf, n = dest.stem, dest.suffix, 2
        while dest.exists():
            dest = dest_dir / f"{stem}-{n}{suf}"
            n += 1
        shutil.copy2(src, dest)
        rec = {"name": dest.name, "path": str(dest.relative_to(ROOT)), "kind": a.kind, "client": a.client or "",
               "vessel": a.vessel or "", "ref": a.ref or "", "notes": a.notes or "", "size": dest.stat().st_size, "added": now()}
        rows.append(rec)
        save_records(LIBRARY_INDEX, rows)
        print(f"saved {rec['path']} ({rec['size']} bytes)")
        return
    q = (a.query or "").lower()
    sel = [r for r in rows if (not a.kind or r.get("kind") == a.kind) and (not q or q in json.dumps(r, ensure_ascii=False).lower())]
    if a.json:
        print(json.dumps(sel, indent=2, ensure_ascii=False))
        return
    if not sel:
        print("(no documents match)")
    for r in sorted(sel, key=lambda r: r.get("added", ""), reverse=True):
        print(f"{r['path']} | {r.get('kind')} | {r.get('client') or '-'} | {r.get('vessel') or '-'} | {r.get('ref') or ''}")


# --------------------------------------------------------------------------
# Session context
# --------------------------------------------------------------------------

def cmd_context(_a: argparse.Namespace) -> None:
    prefs = [p for p in all_pref_entries() if p.get("status") == "active"]
    firm = sorted([p for p in prefs if p.get("type") in ("explicit", "observed")], key=lambda p: p["id"])
    tent = [p for p in prefs if p.get("type") == "tentative"]
    lessons = [l for l in parse_entries(LESSON_FILE) if l.get("status") == "active"]
    active = [p.name for p in all_task_dirs() if p.parent == TASKS_ACTIVE]
    print("[Sinor AI Executive Team] Executive briefing. For executive work you are the Executive Supervisor "
          "(main thread) and follow the executive-supervisor-protocol skill; the sinor-operating-rules router "
          "picks the protocol for sales or marketing work. Specialists are the sinor-team plugin agents.")
    print(f"Knowledge loaded from workspace: {len(firm)} confirmed/observed preferences, "
          f"{len(tent)} tentative hints, {len(lessons)} active lessons.")
    for p in firm[:20]:
        print(f"- {p['id']} ({p.get('type')}, {p.get('scope')}): {p.get('statement', '')}")
    if len(firm) > 20:
        print(f"- ... {len(firm) - 20} more: python3 sinor.py pref list")
    for l in lessons[:10]:
        print(f"- {l['id']} lesson ({l.get('scope')}): when {l.get('trigger', '')}: {l.get('lesson', '')}")
    if active:
        print("Open task records: " + ", ".join(active[:8]))
    print("Learned items are hints. The user's explicit words in the current message always win.")


# --------------------------------------------------------------------------
# Knowledge sync
# --------------------------------------------------------------------------

def git(*args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    r = subprocess.run(["git", *args], cwd=str(cwd or ROOT), capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip() or r.stdout.strip()}")
    return r


def push_with_retry(cwd: Path, refspec: str, remote: str) -> None:
    delay = 2
    for attempt in range(5):
        r = git("push", remote, refspec, cwd=cwd, check=False)
        if r.returncode == 0:
            return
        err = r.stderr.lower()
        if "rejected" in err or "non-fast-forward" in err or "fetch first" in err:
            raise RuntimeError("REJECTED:" + r.stderr.strip())
        if attempt == 4:
            raise RuntimeError(r.stderr.strip())
        time.sleep(delay)
        delay *= 2


def cmd_sync(a: argparse.Namespace) -> None:
    """Commit only SYNC_PATHS of the executive root, then push as the original rule did.

    Never force-pushes, never stages anything outside SYNC_PATHS. Works in whatever git
    repository contains the executive root. If there is no repository it says so.
    """
    try:
        _sync(a)
    except RuntimeError as e:
        die(f"{e}\nThe knowledge commit (if one was made) stays local. Tell the user once; do not retry blindly.")


def _sync(a: argparse.Namespace) -> None:
    remote, target = a.remote, a.branch
    try:
        top = git("rev-parse", "--show-toplevel", check=False)
    except (FileNotFoundError, NotADirectoryError, OSError) as e:
        die(f"cannot run git for the workspace at {ROOT}: {e}")
        return
    if top.returncode != 0:
        die(f"the workspace data folder {ROOT} is not inside a git repository, so nothing can be synced. "
            "Records are saved on disk only. To share and persist them, put the workspace in a private "
            "git repository (git init, add a remote) and run sync again.")
        return
    paths = [p for p in SYNC_PATHS if (ROOT / p).exists()]
    if not paths:
        print("nothing to sync")
        return
    git("add", "--", *paths)
    staged = git("diff", "--cached", "--name-only", "--", *paths).stdout.split()
    if not staged:
        print("nothing to sync")
        return
    msg = a.message or "knowledge-sync: update team knowledge"
    git("commit", "-m", msg, "--", *paths)
    sha = git("rev-parse", "HEAD").stdout.strip()
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if a.no_push:
        print(f"committed {sha[:8]} on {branch} (not pushed)")
        return
    if git("remote", "get-url", remote, check=False).returncode != 0:
        die(f"committed {sha[:8]} on {branch}, but there is no git remote named '{remote}', so it was not pushed.")
        return
    if branch == target:
        for _ in range(3):
            try:
                push_with_retry(ROOT, f"HEAD:{target}", remote)
                print(f"pushed {sha[:8]} to {remote}/{target}")
                return
            except RuntimeError as e:
                if not str(e).startswith("REJECTED"):
                    raise
                git("pull", "--rebase", remote, target)
        die("push to main kept being rejected; resolve manually")
    git("fetch", remote, target)
    wt = Path(tempfile.mkdtemp(prefix="sinor-sync-"))
    try:
        git("worktree", "add", "--detach", str(wt), f"{remote}/{target}")
        for _ in range(3):
            r = git("cherry-pick", sha, cwd=wt, check=False)
            if r.returncode != 0:
                git("cherry-pick", "--abort", cwd=wt, check=False)
                die(f"knowledge commit {sha[:8]} conflicts with {target}; it stays on {branch}. "
                    "Tell the user and merge manually.")
            try:
                push_with_retry(wt, f"HEAD:{target}", remote)
                print(f"committed {sha[:8]} on {branch} and pushed the same change to {remote}/{target}")
                return
            except RuntimeError as e:
                if not str(e).startswith("REJECTED"):
                    raise
                git("fetch", remote, target, cwd=wt)
                git("reset", "--hard", f"{remote}/{target}", cwd=wt)
        die("push to main kept being rejected")
    finally:
        git("worktree", "remove", "--force", str(wt), check=False)
        shutil.rmtree(wt, ignore_errors=True)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="sinor", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", default=None,
                    help="workspace base folder (ignored when env SINOR_ROOT is set)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("context").set_defaults(fn=cmd_context)
    sub.add_parser("registry").set_defaults(fn=cmd_registry)
    sub.add_parser("validate").set_defaults(fn=cmd_validate)

    t = sub.add_parser("task")
    t.add_argument("action", choices=["new", "list", "show", "close"])
    t.add_argument("id", nargs="?")
    t.add_argument("--title", default="task")
    t.add_argument("--instruction")
    t.add_argument("--tier", type=int)
    t.add_argument("--type")
    t.add_argument("--all", action="store_true")
    t.add_argument("--agents")
    t.add_argument("--qa-cycles", type=int, default=1)
    t.add_argument("--corrections", type=int, default=0)
    t.add_argument("--clarifications", type=int, default=0)
    t.add_argument("--feedback", choices=["accepted", "corrected", "none"], default="none")
    t.add_argument("--lessons")
    t.add_argument("--cost-usd", type=float)
    t.add_argument("--notes")
    t.add_argument("--claim-pass", action="store_true",
                   help="refuse to close unless every mandatory requirement is PASS with evidence")
    t.add_argument("--keep-active", action="store_true")
    t.set_defaults(fn=cmd_task)

    p = sub.add_parser("pref")
    p.add_argument("action", choices=["add", "list", "update", "supersede", "forget"])
    p.add_argument("id", nargs="?")
    p.add_argument("--file", default="WORK_PREFERENCES")
    p.add_argument("--title")
    p.add_argument("--statement")
    p.add_argument("--type")
    p.add_argument("--scope", default=None)
    p.add_argument("--confidence")
    p.add_argument("--source")
    p.add_argument("--evidence")
    p.add_argument("--observe", help="add one more independent observation as evidence")
    p.add_argument("--by", help="new PREF id that supersedes this one")
    p.add_argument("--reason")
    p.add_argument("--all", action="store_true")
    p.set_defaults(fn=cmd_pref)

    l = sub.add_parser("lesson")
    l.add_argument("action", choices=["add", "list", "update"])
    l.add_argument("id", nargs="?")
    l.add_argument("--title")
    l.add_argument("--lesson")
    l.add_argument("--trigger")
    l.add_argument("--scope")
    l.add_argument("--root-cause")
    l.add_argument("--source")
    l.add_argument("--evidence")
    l.add_argument("--status")
    l.add_argument("--recent", type=int, default=20)
    l.add_argument("--all", action="store_true")
    l.set_defaults(fn=cmd_lesson)

    c = sub.add_parser("correction")
    c.add_argument("action", choices=["add", "list"])
    c.add_argument("--title")
    c.add_argument("--task", default="")
    c.add_argument("--feedback")
    c.add_argument("--category")
    c.add_argument("--wrong")
    c.add_argument("--fix")
    c.add_argument("--lesson")
    c.add_argument("--detail")
    c.add_argument("--recent", type=int, default=20)
    c.set_defaults(fn=cmd_correction)

    le = sub.add_parser("learned")
    le.add_argument("--days", type=int, default=30)
    le.set_defaults(fn=cmd_learned)

    m = sub.add_parser("metrics")
    m.add_argument("--include-tests", action="store_true", default=False)
    m.set_defaults(fn=cmd_metrics)

    ca = sub.add_parser("calc")
    ca.add_argument("spec", help="JSON spec file, or - for stdin")
    ca.add_argument("--json", action="store_true")
    ca.set_defaults(fn=cmd_calc)

    li = sub.add_parser("lint")
    li.add_argument("files", nargs="+")
    li.set_defaults(fn=cmd_lint)

    s = sub.add_parser("signal")
    s.add_argument("--category", required=True)
    s.add_argument("--phrase", default="")
    s.set_defaults(fn=cmd_signal)

    qp = sub.add_parser("quote")
    qp.add_argument("action", choices=["add", "update", "list"])
    for k in QUOTE_FIELDS:
        qp.add_argument("--" + k.replace("_", "-"), dest=k)
    qp.add_argument("--query")
    qp.add_argument("--json", action="store_true")
    qp.set_defaults(fn=cmd_quote)

    cp = sub.add_parser("client")
    cp.add_argument("action", choices=["add", "update", "list"])
    for k in CLIENT_FIELDS:
        cp.add_argument("--" + k, dest=k)
    cp.add_argument("--query")
    cp.add_argument("--json", action="store_true")
    cp.set_defaults(fn=cmd_client)

    dp = sub.add_parser("doc")
    dp.add_argument("action", choices=["add", "list"])
    dp.add_argument("file", nargs="?")
    dp.add_argument("--kind", default=None)
    for k in ("client", "vessel", "ref", "notes", "query"):
        dp.add_argument("--" + k)
    dp.add_argument("--json", action="store_true")
    dp.set_defaults(fn=cmd_doc)

    sy = sub.add_parser("sync")
    sy.add_argument("-m", "--message")
    sy.add_argument("--remote", default="origin")
    sy.add_argument("--branch", default="main")
    sy.add_argument("--no-push", action="store_true")
    sy.set_defaults(fn=cmd_sync)
    return ap


def main(argv: list[str] | None = None) -> None:
    a = build_parser().parse_args(argv)
    if a.workspace:
        _set_root(_default_root(a.workspace))
    if ROOT is None and a.cmd not in ("calc", "lint"):
        die(workspace_lib.unresolved_message("executive", workspace=a.workspace), 2)
    if a.cmd == "pref" and a.action == "add":
        for req in ("title", "statement", "type", "source"):
            if not getattr(a, req):
                die(f"pref add needs --{req}")
        a.scope = a.scope or "global"
    if a.cmd == "pref" and a.action in ("update", "supersede", "forget") and not a.id:
        die("give the PREF id")
    if a.cmd == "pref" and a.action == "supersede" and not a.by:
        die("supersede needs --by NEW_ID")
    if a.cmd == "lesson" and a.action == "add":
        for req in ("title", "lesson", "trigger", "scope", "root_cause", "source", "evidence"):
            if not getattr(a, req):
                die(f"lesson add needs --{req.replace('_', '-')}")
    if a.cmd == "correction" and a.action == "add":
        for req in ("title", "feedback", "category", "wrong", "fix"):
            if not getattr(a, req):
                die(f"correction add needs --{req}")
    if a.cmd == "doc" and a.action == "add" and (not a.file or not a.kind):
        die("doc add needs the file path and --kind")
    if a.cmd == "task" and a.action in ("show", "close") and not a.id:
        die("give the task id")
    a.fn(a)


if __name__ == "__main__":
    main()
