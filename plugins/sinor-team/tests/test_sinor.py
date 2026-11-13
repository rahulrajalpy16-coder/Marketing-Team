"""Tests for scripts/sinor.py (ported from the Claude-Agent-Team-SMS unit tests).

Each test runs against a throwaway workspace (SINOR_ROOT or an executive/ folder in tmp_path).
Hook tests from the source suite are not ported here: hooks belong to scripts/hooks.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[1]
TOOL = PLUGIN / "scripts" / "sinor.py"


def run(root, *args, stdin=None, check=True, env=None, cwd=None):
    e = dict(os.environ, SINOR_ROOT=str(root))
    e.update(env or {})
    r = subprocess.run([sys.executable, str(TOOL), *args], cwd=cwd or root, env=e, input=stdin,
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        raise AssertionError(f"{args} failed ({r.returncode}): {r.stderr}{r.stdout}")
    return r


@pytest.fixture
def root(tmp_path):
    ws = tmp_path / "ws"
    for d in ("knowledge/user", "tasks/active", "tasks/completed", "quality/metrics", "learning/lessons"):
        (ws / d).mkdir(parents=True)
    (ws / "knowledge/user/.tombstones.json").write_text("[]")
    return ws


def add_pref(root, **kw):
    args = ["pref", "add"]
    for k, v in kw.items():
        args += [f"--{k}", v]
    return run(root, *args).stdout.strip()


# ---------------------------------------------------------------- preferences

def test_pref_lifecycle_and_registry(root):
    pid = add_pref(root, file="COMMUNICATION_STYLE", type="explicit", title="Short emails",
                   statement="Client emails under 80 words", source="test", evidence='"keep it short"')
    assert pid == "PREF-0001"
    reg = (root / "knowledge/user/PREFERENCE_CONFIDENCE.md").read_text()
    assert "PREF-0001" in reg and "Explicit confirmed" in reg
    tid = add_pref(root, file="WORK_PREFERENCES", type="tentative", title="Likes tables",
                   statement="Prefers tables", source="test", evidence="observed once")
    assert tid == "PREF-0002"
    run(root, "pref", "update", tid, "--observe", "observed again in TASK-2")
    out = run(root, "pref", "list", "--type", "observed").stdout
    assert "PREF-0002" in out and "medium" in out  # auto-promoted after 2 observations
    new = add_pref(root, file="COMMUNICATION_STYLE", type="explicit", title="Detailed emails",
                   statement="Client emails detailed", source="test", evidence='"make them detailed"')
    run(root, "pref", "supersede", pid, "--by", new)
    assert "PREF-0001" not in run(root, "pref", "list").stdout
    assert "superseded" in run(root, "pref", "list", "--all").stdout


def test_explicit_requires_evidence_and_tentative_not_high(root):
    r = run(root, "pref", "add", "--file", "WORK_PREFERENCES", "--type", "explicit", "--title", "x",
            "--statement", "y", "--source", "z", check=False)
    assert r.returncode != 0 and "evidence" in r.stderr
    r = run(root, "pref", "add", "--file", "WORK_PREFERENCES", "--type", "tentative", "--confidence", "high",
            "--title", "x", "--statement", "y", "--source", "z", "--evidence", "e", check=False)
    assert r.returncode != 0


def test_forget_removes_content_and_never_reuses_id(root):
    pid = add_pref(root, file="WORK_PREFERENCES", type="explicit", title="Secret thing",
                   statement="REMOVE-ME-TEXT", source="t", evidence='"x"')
    keep = add_pref(root, file="WORK_PREFERENCES", type="explicit", title="Keep",
                    statement="KEEP-TEXT", source="t", evidence='"y"')
    run(root, "pref", "forget", pid, "--reason", "user request")
    body = (root / "knowledge/user/WORK_PREFERENCES.md").read_text()
    assert "REMOVE-ME-TEXT" not in body and "KEEP-TEXT" in body
    reg = (root / "knowledge/user/PREFERENCE_CONFIDENCE.md").read_text()
    assert "REMOVE-ME-TEXT" not in reg and pid in reg  # tombstone only
    nxt = add_pref(root, file="WORK_PREFERENCES", type="explicit", title="New", statement="n",
                   source="t", evidence='"z"')
    assert nxt == "PREF-0003" and keep == "PREF-0002"


def test_fresh_workspace_without_folders_still_works(tmp_path):
    """Deliberate change: the tool creates missing knowledge folders on demand."""
    ws = tmp_path / "bare"
    ws.mkdir()
    pid = add_pref(ws, file="WORK_PREFERENCES", type="explicit", title="t", statement="s",
                   source="x", evidence='"e"')
    assert pid == "PREF-0001"
    assert (ws / "knowledge/user/PREFERENCE_CONFIDENCE.md").exists()


# ---------------------------------------------------------------- lessons, corrections, learned

def test_lessons_corrections_and_learned_report(root):
    cid = run(root, "correction", "add", "--title", "Too long", "--task", "TASK-1", "--feedback",
              "not what I wanted, too long", "--category", "missed-requirement", "--wrong", "180 words",
              "--fix", "cut to 70").stdout.strip()
    lid = run(root, "lesson", "add", "--title", "Captain emails short", "--lesson", "Under 80 words",
              "--trigger", "email to vessel captain", "--scope", "task-type:email", "--root-cause",
              "missed-requirement", "--source", cid, "--evidence", "user said too long").stdout.strip()
    assert (cid, lid) == ("COR-0001", "LES-0001")
    rep = run(root, "learned", "--days", "1").stdout
    assert "LES-0001" in rep and "COR-0001" in rep and "too long" in rep
    bad = run(root, "lesson", "add", "--title", "x", "--lesson", "x", "--trigger", "x", "--scope", "x",
              "--root-cause", "made-up", "--source", "x", "--evidence", "x", check=False)
    assert bad.returncode != 0


# ---------------------------------------------------------------- tasks

def fill_matrix(task_md, rows):
    text = task_md.read_text()
    tbl = "\n".join(rows)
    text = text.replace("| R1 | | | explicit | | | | | PENDING |", tbl)
    task_md.write_text(text)


def test_task_new_preserves_instruction_and_close_gates_pass(root):
    instr = "Draft email to Capt. Ali, MV TEST, 20/10/2026 at 0800 hrs.\nKeep it short."
    rel = run(root, "task", "new", "--title", "Email test", "--tier", "1", "--type", "email",
              stdin=instr).stdout.strip()
    d = root / rel
    assert (d / "original_instruction.txt").read_text().strip() == instr
    assert "> Draft email to Capt. Ali" in (d / "TASK.md").read_text()
    fill_matrix(d / "TASK.md", [
        "| R1 | email | draft | explicit | doc | email.md | exists | deliverables/email.md | PASS |",
        "| R2 | short | <80 words | explicit | doc | email.md | words<80 | | NOT VERIFIED |",
        "| R3 | nicer tone | | optional | doc | | | | FAIL |",
    ])
    tid = d.name[:20]
    r = run(root, "task", "close", tid, "--claim-pass", check=False)
    assert r.returncode == 2 and "R2" in r.stderr
    fill_matrix(d / "TASK.md", [])
    t = (d / "TASK.md").read_text().replace("| | NOT VERIFIED |", "| lint: 61 words | PASS |")
    (d / "TASK.md").write_text(t)
    out = json.loads(run(root, "task", "close", tid, "--claim-pass", "--agents", "documentation-communication,qa-auditor",
                         "--feedback", "accepted").stdout)
    assert out["final_status"] == "PASS"  # optional R3 FAIL does not block
    assert (root / "tasks/completed" / d.name).exists()
    rec = json.loads((root / "quality/metrics/tasks.jsonl").read_text().splitlines()[-1])
    assert rec["tier"] == 1 and rec["type"] == "email" and rec["qa_first_pass"] is True
    assert rec["task"] == tid and re.match(r"^TASK-\d{8}-\d{6}$", tid)
    m = run(root, "metrics").stdout
    assert "Tasks closed | 1" in m and "First-pass QA success | 1/1" in m


def test_pass_without_evidence_is_not_fully_verified(root):
    rel = run(root, "task", "new", "--title", "x", "--instruction", "do x").stdout.strip()
    d = root / rel
    fill_matrix(d / "TASK.md", ["| R1 | x | x | explicit | a | f | c | | PASS |"])
    out = json.loads(run(root, "task", "close", d.name[:20]).stdout)
    assert out["final_status"] == "PARTIAL"
    assert out["requirements"]["pass_without_evidence"] == ["R1"]


def test_lesson_application_counted_on_close(root):
    lid = run(root, "lesson", "add", "--title", "t", "--lesson", "l", "--trigger", "tr", "--scope", "global",
              "--root-cause", "other", "--source", "s", "--evidence", "e").stdout.strip()
    rel = run(root, "task", "new", "--title", "x", "--instruction", "do x").stdout.strip()
    d = root / rel
    fill_matrix(d / "TASK.md", ["| R1 | x | x | explicit | a | f | c | ev | PASS |"])
    run(root, "task", "close", d.name[:20], "--lessons", lid, "--feedback", "accepted")
    assert "applied 1x, helped 1x" in run(root, "lesson", "list").stdout


def test_task_ids_unique_when_created_in_same_second(root):
    a = run(root, "task", "new", "--title", "one", "--instruction", "x").stdout.strip()
    b = run(root, "task", "new", "--title", "two", "--instruction", "y").stdout.strip()
    assert Path(a).name[:20] != Path(b).name[:20]


# ---------------------------------------------------------------- calculator

def calc(root, spec):
    p = root / "spec.json"
    p.write_text(json.dumps(spec))
    return run(root, "calc", str(p), "--json", check=False)


def test_calc_totals_vat_fx(root):
    r = calc(root, {"currency": "USD", "items": [
        {"no": 1, "description": "DGPS receiver", "qty": 2, "unit": "Nos", "unit_price": "12,450.00"},
        {"no": 2, "description": "Installation", "qty": 1, "unit": "Lsum", "unit_price": "3800"},
        {"no": 3, "description": "Engineer", "qty": 3, "unit": "Day", "unit_price": "650"}],
        "vat_percent": "5", "fx": {"to": "AED", "rate": "3.6725", "source": "user"}})
    res = json.loads(r.stdout)
    assert res["subtotal"] == "30,650.00" and res["vat"] == "1,532.50" and res["total"] == "32,182.50"
    assert res["fx"]["total"] == "118,190.23"  # 32182.50 x 3.6725 = 118190.23125


def test_calc_refuses_missing_price_and_unsourced_discount(root):
    r = calc(root, {"currency": "USD", "items": [{"qty": 1, "unit_price": ""}]})
    assert r.returncode != 0 and "never invents" in r.stderr
    r = calc(root, {"currency": "USD", "items": [{"qty": 1, "unit_price": "100"}],
                    "discount": {"type": "percent", "value": "10"}})
    assert r.returncode != 0 and "source" in r.stderr


def test_calc_half_up_rounding_and_alternatives(root):
    res = json.loads(calc(root, {"currency": "USD", "items": [{"qty": "3", "unit_price": "0.335"}]}).stdout)
    assert res["lines"][0]["amount"] == "1.01"  # 1.005 rounds half up
    alt = json.loads(calc(root, {"currency": "USD", "alternatives": True, "items": [
        {"qty": 1, "unit_price": "283000"}, {"qty": 1, "unit_price": "190000"}]}).stdout)
    assert "total" not in alt and alt["lines"][1]["amount"] == "190,000.00"


def test_calc_and_lint_work_without_any_workspace(tmp_path):
    """calc and lint need no data root, so they must not demand a workspace."""
    spec = tmp_path / "s.json"
    spec.write_text(json.dumps({"currency": "USD", "items": [{"qty": 1, "unit_price": "10"}]}))
    env = {k: v for k, v in os.environ.items() if k != "SINOR_ROOT"}
    r = subprocess.run([sys.executable, str(TOOL), "calc", str(spec), "--json"], cwd=tmp_path, env=env,
                       capture_output=True, text=True)
    assert r.returncode == 0 and json.loads(r.stdout)["total"] == "10.00"


# ---------------------------------------------------------------- lint

def test_lint_flags_em_dash_and_placeholders(root):
    f = root / "x.md"
    f.write_text("Hello \u2014 there\nQTN SMS-QT2026-XXXXX\nfine line\n")
    r = run(root, "lint", str(f), check=False)
    assert r.returncode == 1 and "em dash" in r.stdout and "XXXXX" in r.stdout
    f.write_text("Clean text, with commas: and colons. See note [1] and [optional] text.\n")
    r = run(root, "lint", str(f))
    assert r.returncode == 0 and "0 warning" in r.stdout
    f.write_text("Best regards,\n[SIGNATORY NAME]\n[TITLE]\n")
    r = run(root, "lint", str(f))
    assert r.returncode == 0 and "2 warning(s)" in r.stdout and "SIGNATORY NAME" in r.stdout


# ---------------------------------------------------------------- validate (plugin registry + workspace)

def make_plugin(tmp_path, agent_ok=True):
    pl = tmp_path / "plugin"
    (pl / "agents").mkdir(parents=True)
    (pl / "skills" / "demo").mkdir(parents=True)
    (pl / "hooks").mkdir()
    (pl / "agents" / "helper.md").write_text(
        "---\nname: helper\ndescription: does things\n---\nBody\n" if agent_ok
        else "---\nname: other-name\ndescription: x\n---\nBody\n")
    (pl / "skills" / "demo" / "SKILL.md").write_text("---\nname: demo\ndescription: a skill\n---\nBody\n")
    return pl


def test_validate_lists_plugin_agents_and_skills(root, tmp_path):
    pl = make_plugin(tmp_path)
    for d in ("records",):
        (root / d).mkdir(exist_ok=True)
    r = run(root, "validate", env={"SINOR_PLUGIN_ROOT": str(pl)}, check=False)
    assert r.returncode == 0, r.stdout
    assert "agents: 1, skills: 1" in r.stdout and "VALID" in r.stdout


def test_validate_reports_plugin_and_workspace_problems(root, tmp_path):
    pl = make_plugin(tmp_path, agent_ok=False)
    (pl / "skills" / "broken").mkdir()
    (pl / "hooks" / "hooks.json").write_text(json.dumps({"hooks": {"PreToolUse": [
        {"hooks": [{"type": "command", "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/hooks/missing.py"}]}]}}))
    shutil.rmtree(root / "learning")  # workspace structure problem
    r = run(root, "validate", env={"SINOR_PLUGIN_ROOT": str(pl)}, check=False)
    assert r.returncode == 1
    assert "does not match file name" in r.stdout
    assert "skills/broken: no SKILL.md" in r.stdout
    assert "hook script missing: scripts/hooks/missing.py" in r.stdout
    assert "workspace folder missing: executive/learning" in r.stdout


def test_validate_em_dash_in_knowledge(root, tmp_path):
    pl = make_plugin(tmp_path)
    (root / "records").mkdir(exist_ok=True)
    (root / "knowledge" / "note.md").write_text("bad \u2014 dash\n")
    r = run(root, "validate", env={"SINOR_PLUGIN_ROOT": str(pl)}, check=False)
    assert r.returncode == 1 and "contains an em dash" in r.stdout


def test_real_plugin_validate_does_not_crash(root):
    r = run(root, "validate", check=False)  # the plugin folder is still being assembled by others
    assert r.returncode in (0, 1) and "Traceback" not in r.stderr


# ---------------------------------------------------------------- workspace resolution inside sinor.py

def test_resolves_executive_root_from_workspace_and_sinor_root_wins(tmp_path):
    ws = tmp_path / "team"
    (ws / "executive" / "knowledge" / "user").mkdir(parents=True)
    (ws / ".sinor-workspace").write_text("x")
    other = tmp_path / "other"
    other.mkdir()
    env = {k: v for k, v in os.environ.items() if k != "SINOR_ROOT"}
    env["SINOR_WORKSPACE"] = str(ws)
    r = subprocess.run([sys.executable, str(TOOL), "pref", "add", "--title", "t", "--statement", "s",
                        "--type", "explicit", "--source", "x", "--evidence", "e"],
                       cwd=other, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert (ws / "executive/knowledge/user/WORK_PREFERENCES.md").exists()
    # SINOR_ROOT must still win over the workspace
    env["SINOR_ROOT"] = str(other)
    r = subprocess.run([sys.executable, str(TOOL), "pref", "add", "--title", "t", "--statement", "s",
                        "--type", "explicit", "--source", "x", "--evidence", "e"],
                       cwd=other, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert (other / "knowledge/user/WORK_PREFERENCES.md").exists()


def test_unresolved_workspace_gives_setup_hint_exit_2(tmp_path):
    env = {k: v for k, v in os.environ.items() if k != "SINOR_ROOT"}
    r = subprocess.run([sys.executable, str(TOOL), "pref", "list"], cwd=tmp_path, env=env,
                       capture_output=True, text=True)
    assert r.returncode == 2 and "/sinor-team:setup" in r.stderr


# ---------------------------------------------------------------- sync

def git(cwd, *a):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True, check=True).stdout


def make_repo(tmp_path, sub=""):
    remote = tmp_path / "remote.git"
    work = tmp_path / "work"
    git(tmp_path, "init", "--bare", "-b", "main", str(remote))
    git(tmp_path, "clone", str(remote), str(work))
    for k, v in (("user.email", "t@example.com"), ("user.name", "t")):
        git(work, "config", k, v)
    data = work / sub if sub else work
    (data / "knowledge").mkdir(parents=True)
    (data / "knowledge" / "a.md").write_text("one\n")
    (work / "src.py").write_text("code\n")
    git(work, "add", ".")
    git(work, "commit", "-m", "init")
    git(work, "push", "-u", "origin", "main")
    return work, data


@pytest.mark.parametrize("sub", ["", "executive"])
def test_sync_from_feature_branch_lands_on_main(tmp_path, sub):
    work, data = make_repo(tmp_path, sub)
    git(work, "checkout", "-b", "claude/session-x")
    (data / "knowledge" / "a.md").write_text("one\ntwo\n")
    (work / "src.py").write_text("code changed, must not sync\n")
    r = run(data, "sync", "-m", "knowledge-sync: test", cwd=work)
    assert r.returncode == 0, r.stderr
    assert "pushed the same change" in r.stdout
    git(work, "fetch", "origin")
    prefix = f"{sub}/" if sub else ""
    assert git(work, "show", f"origin/main:{prefix}knowledge/a.md") == "one\ntwo\n"
    assert git(work, "show", "origin/main:src.py") == "code\n"  # code is never synced
    assert git(work, "rev-parse", "--abbrev-ref", "HEAD").strip() == "claude/session-x"
    again = run(data, "sync", cwd=work)
    assert "nothing to sync" in again.stdout


def test_sync_never_stages_other_paths(tmp_path):
    work, data = make_repo(tmp_path)
    (data / "knowledge" / "a.md").write_text("changed\n")
    (work / "src.py").write_text("staged by someone else\n")
    git(work, "add", "src.py")
    r = run(data, "sync", "--no-push", cwd=work)
    assert "not pushed" in r.stdout
    assert "src.py" not in git(work, "show", "--name-only", "--format=", "HEAD")
    assert "src.py" in git(work, "diff", "--cached", "--name-only")  # still staged, untouched


def test_sync_on_main_pushes_without_force(tmp_path):
    work, data = make_repo(tmp_path)
    (data / "knowledge" / "a.md").write_text("main change\n")
    r = run(data, "sync", cwd=work)
    assert r.returncode == 0 and "pushed" in r.stdout
    git(work, "fetch", "origin")
    assert git(work, "show", "origin/main:knowledge/a.md") == "main change\n"


def test_sync_without_git_repo_says_so(tmp_path):
    ws = tmp_path / "plain"
    (ws / "knowledge").mkdir(parents=True)
    (ws / "knowledge" / "a.md").write_text("x")
    r = run(ws, "sync", check=False)
    assert r.returncode == 1 and "not inside a git repository" in r.stderr
    assert "Traceback" not in r.stderr


def test_sync_without_remote_keeps_commit_local(tmp_path):
    repo = tmp_path / "solo"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    for k, v in (("user.email", "t@example.com"), ("user.name", "t")):
        git(repo, "config", k, v)
    (repo / "knowledge").mkdir()
    (repo / "knowledge" / "a.md").write_text("x\n")
    r = run(repo, "sync", check=False)
    assert r.returncode == 1 and "no git remote" in r.stderr and "Traceback" not in r.stderr
    assert "knowledge-sync" in git(repo, "log", "--format=%s")


# ---------------------------------------------------------------- records

def test_quote_records_lifecycle(root):
    r = run(root, "quote", "add", "--qtn", "SMS-QT2026-00010", "--date", "20/10/2026", "--client", "Synthetic Marine LLC",
            "--vessel", "MV SYNTHETIC STAR", "--amount", "32,182.50", "--status", "sent")
    assert "added SMS-QT2026-00010" in r.stdout
    rows = json.loads((root / "records/quotes.json").read_text())
    assert rows[0]["date"] == "2026-10-20" and rows[0]["amount"] == 32182.5
    assert run(root, "quote", "add", "--qtn", "SMS-QT2026-00010", check=False).returncode != 0  # no duplicates
    assert "updated SMS-QT2026-00010: won" in run(root, "quote", "update", "--qtn", "SMS-QT2026-00010", "--status", "won").stdout
    assert run(root, "quote", "update", "--qtn", "X", "--status", "nonsense", check=False).returncode != 0
    assert run(root, "quote", "add", "--qtn", "Y", "--date", "31/02/2026", check=False).returncode != 0  # impossible date
    out = run(root, "quote", "list").stdout
    assert "32,182.50" in out and "win rate 100%" in out


def test_client_and_doc_records(root):
    run(root, "client", "add", "--name", "Synthetic Marine LLC", "--vessels", "MV A, MV B", "--trn", "123")
    assert json.loads((root / "records/clients.json").read_text())[0]["vessels"] == ["MV A", "MV B"]
    assert run(root, "client", "add", "--name", "synthetic marine llc", check=False).returncode != 0  # case-insensitive dup
    src = root / "spec sheet.pdf"
    src.write_bytes(b"%PDF-1.4 test")
    run(root, "doc", "add", str(src), "--kind", "datasheet", "--client", "Synthetic Marine LLC")
    run(root, "doc", "add", str(src), "--kind", "datasheet")
    idx = json.loads((root / "records/library/index.json").read_text())
    assert [d["name"] for d in idx] == ["spec sheet.pdf", "spec sheet-2.pdf"]  # never overwrites
    assert (root / "records/library/datasheet/spec sheet-2.pdf").exists()
    assert run(root, "doc", "add", str(src), "--kind", "photo", check=False).returncode != 0


def test_signal_and_context(root):
    run(root, "signal", "--category", "correction", "--phrase", "not correct")
    assert "correction" in (root / "quality/metrics/feedback_signals.jsonl").read_text()
    out = run(root, "context").stdout
    assert "Executive Supervisor" in out and "CLAUDE.md" not in out
