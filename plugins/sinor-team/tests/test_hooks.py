"""Tests for the plugin hooks (scripts/hooks). Each hook is run as a real subprocess with a
JSON payload on stdin, the way Claude Code runs it."""
import json
import os
import subprocess
import sys

import pytest

import workspace_lib as wl
from conftest import SCRIPTS

HOOKS = SCRIPTS / "hooks"


def run_hook(name, payload, project_dir, extra_env=None):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project_dir))
    env.pop("SINOR_WORKSPACE", None)
    if extra_env:
        env.update(extra_env)
    return subprocess.run([sys.executable, str(HOOKS / name)], input=json.dumps(payload),
                          capture_output=True, text=True, env=env, cwd=str(project_dir))


@pytest.fixture
def ws(tmp_path):
    base = tmp_path / "team"
    wl.init_workspace(base)
    return base


@pytest.fixture
def outside(tmp_path):
    d = tmp_path / "unrelated-project"
    d.mkdir()
    return d


# ---------------------------------------------------------------- approval gate
RISKY_BASH = ["git push --force origin main", "npm publish", "curl -X POST https://x.example/a",
              "git reset --hard HEAD~1", "sendmail a@b.c"]


@pytest.mark.parametrize("cmd", RISKY_BASH)
def test_approval_gate_asks_inside_workspace(ws, cmd):
    r = run_hook("approval_gate.py", {"tool_name": "Bash", "tool_input": {"command": cmd}}, ws / "executive")
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "ask"


def test_approval_gate_silent_for_safe_bash(ws):
    r = run_hook("approval_gate.py", {"tool_name": "Bash", "tool_input": {"command": "ls -la"}}, ws)
    assert r.stdout.strip() == ""


def test_approval_gate_asks_for_outward_mcp_action(ws):
    r = run_hook("approval_gate.py", {"tool_name": "mcp__Gmail__send_message", "tool_input": {}}, ws)
    assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "ask"


@pytest.mark.parametrize("tool", ["mcp__Gmail__create_draft", "mcp__Gmail__search_threads"])
def test_approval_gate_allows_drafts_and_reads(ws, tool):
    r = run_hook("approval_gate.py", {"tool_name": tool, "tool_input": {}}, ws)
    assert r.stdout.strip() == ""


def test_approval_gate_inactive_outside_workspace(outside):
    r = run_hook("approval_gate.py", {"tool_name": "Bash", "tool_input": {"command": "git push --force"}}, outside)
    assert r.stdout.strip() == "" and r.returncode == 0


# ---------------------------------------------------------------- QA write guard
def qa_payload(path, agent="qa-auditor", tool="Write"):
    return {"agent_type": agent, "tool_name": tool, "tool_input": {"file_path": str(path)}}


@pytest.mark.parametrize("agent", ["qa-auditor", "sinor-team:qa-auditor"])
def test_qa_guard_blocks_writes_outside_quality(ws, agent):
    target = ws / "executive" / "tasks" / "active" / "T1" / "deliverables" / "x.md"
    r = run_hook("qa_write_guard.py", qa_payload(target, agent), ws)
    assert r.returncode == 2 and "QA independence" in r.stderr


@pytest.mark.parametrize("domain", ["executive", "sales"])
def test_qa_guard_allows_quality_folder(ws, domain):
    target = ws / domain / "quality" / "audit-reports" / "T1-qa1.md"
    assert run_hook("qa_write_guard.py", qa_payload(target), ws).returncode == 0


def test_qa_guard_allows_scratch_outside_workspace(ws, tmp_path):
    scratch = tmp_path / "scratch" / "note.txt"
    scratch.parent.mkdir()
    assert run_hook("qa_write_guard.py", qa_payload(scratch), ws).returncode == 0


def test_qa_guard_ignores_other_agents_and_main_thread(ws):
    target = ws / "executive" / "knowledge" / "x.md"
    assert run_hook("qa_write_guard.py", qa_payload(target, "copywriter"), ws).returncode == 0
    main_thread = {"tool_name": "Write", "tool_input": {"file_path": str(target)}}
    assert run_hook("qa_write_guard.py", main_thread, ws).returncode == 0


def test_qa_guard_blocks_edit_tool_and_relative_path(ws):
    p = {"agent_type": "qa-auditor", "tool_name": "Edit", "cwd": str(ws / "executive"),
         "tool_input": {"file_path": "knowledge/user/x.md"}}
    assert run_hook("qa_write_guard.py", p, ws / "executive").returncode == 2


def test_qa_guard_survives_bad_input(ws):
    r = subprocess.run([sys.executable, str(HOOKS / "qa_write_guard.py")], input="not json",
                       capture_output=True, text=True, cwd=str(ws))
    assert r.returncode == 0


# ---------------------------------------------------------------- feedback detector
def test_feedback_detector_flags_correction_and_logs(ws):
    r = run_hook("feedback_detector.py", {"prompt": "That is not correct, check again"}, ws / "executive")
    ctx = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "correction" in ctx and "recheck" in ctx
    assert "executive-supervisor-protocol" in ctx and "CLAUDE.md" not in ctx


def test_feedback_detector_flags_manglish_standing_instruction(ws):
    r = run_hook("feedback_detector.py", {"prompt": "ini muthal always use USD"}, ws)
    assert "standing_instruction" in r.stdout


def test_feedback_detector_silent_for_plain_task(ws):
    r = run_hook("feedback_detector.py", {"prompt": "Draft an email to the client about Tuesday"}, ws)
    assert r.stdout.strip() == ""


def test_feedback_detector_inactive_outside_workspace(outside):
    r = run_hook("feedback_detector.py", {"prompt": "that is wrong"}, outside)
    assert r.stdout.strip() == ""


# ---------------------------------------------------------------- session start
def test_session_start_silent_outside_workspace(outside):
    r = run_hook("session_start.py", {"hook_event_name": "SessionStart"}, outside)
    assert r.stdout.strip() == "" and r.returncode == 0


def test_session_start_prints_briefing_inside_workspace(ws):
    r = run_hook("session_start.py", {"hook_event_name": "SessionStart"}, ws)
    assert r.returncode == 0 and r.stdout.strip() != ""


# ---------------------------------------------------------------- hooks.json
def test_hooks_json_is_valid_and_references_existing_scripts():
    cfg = json.loads((SCRIPTS.parent / "hooks" / "hooks.json").read_text())
    cmds = [h["command"] for ev in cfg["hooks"].values() for g in ev for h in g["hooks"]]
    assert len(cmds) == 4
    for c in cmds:
        assert "${CLAUDE_PLUGIN_ROOT}" in c
        rel = c.split("${CLAUDE_PLUGIN_ROOT}/")[1].rstrip('"')
        assert (SCRIPTS.parent / rel).is_file(), rel


def test_qa_guard_fails_closed_on_malformed_tool_input(ws):
    bad = {"agent_type": "qa-auditor", "tool_name": "Write", "tool_input": "oops-not-an-object"}
    r = run_hook("qa_write_guard.py", bad, ws)
    assert r.returncode == 2 and "blocked to be safe" in r.stderr
