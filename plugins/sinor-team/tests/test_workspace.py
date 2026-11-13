"""Tests for scripts/workspace_lib.py and scripts/workspace.py (DESIGN.md section 2)."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import workspace_lib as wl

CLI = Path(__file__).resolve().parents[1] / "scripts" / "workspace.py"


def cli(*args, cwd, env_extra=None, drop=()):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("SINOR_") and k not in ("CLAUDE_PROJECT_DIR", "XDG_CONFIG_HOME") and k not in drop}
    env.update(env_extra or {})
    return subprocess.run([sys.executable, str(CLI), *args], cwd=cwd, env=env, capture_output=True, text=True)


def make_ws(path):
    wl.init_workspace(path)
    return Path(path).resolve()


# ---------------------------------------------------------------- the four resolution paths, in order

def test_resolution_order_argument_env_walkup_config(tmp_path):
    a, b, c, d = (make_ws(tmp_path / n) for n in "abcd")
    cfgdir = tmp_path / "cfg"
    wl.write_config(d, {"SINOR_CONFIG_DIR": str(cfgdir)})
    project = c / "executive" / "tasks"  # inside workspace c
    env = {"SINOR_WORKSPACE": str(b), "CLAUDE_PROJECT_DIR": str(project), "SINOR_CONFIG_DIR": str(cfgdir)}
    elsewhere = tmp_path / "nowhere"
    elsewhere.mkdir()

    # 1. argument beats everything
    base, src = wl.find_base(workspace=a, env=env, cwd=elsewhere)
    assert (base, src) == (a, "argument")
    # 2. env beats walk-up and config
    base, src = wl.find_base(env=env, cwd=elsewhere)
    assert (base, src) == (b, "env")
    # 3. walk-up (CLAUDE_PROJECT_DIR) beats config
    env3 = {k: v for k, v in env.items() if k != "SINOR_WORKSPACE"}
    base, src = wl.find_base(env=env3, cwd=elsewhere)
    assert (base, src) == (c, "walk-up")
    # 3b. current directory is used when CLAUDE_PROJECT_DIR is not set
    env3b = {"SINOR_CONFIG_DIR": str(cfgdir)}
    base, src = wl.find_base(env=env3b, cwd=a / "marketing" / "campaigns")
    assert (base, src) == (a, "walk-up")
    # 4. config is the last resort
    base, src = wl.find_base(env={"SINOR_CONFIG_DIR": str(cfgdir)}, cwd=elsewhere)
    assert (base, src) == (d, "config")
    # nothing at all
    base, src = wl.find_base(env={"SINOR_CONFIG_DIR": str(tmp_path / "empty")}, cwd=elsewhere)
    assert base is None and src == "none"


def test_claude_project_dir_is_tried_before_cwd(tmp_path):
    a, c = make_ws(tmp_path / "a"), make_ws(tmp_path / "c")
    base, _ = wl.find_base(env={"CLAUDE_PROJECT_DIR": str(c), "SINOR_CONFIG_DIR": str(tmp_path / "x")}, cwd=a)
    assert base == c


# ---------------------------------------------------------------- layouts and markers

def test_combined_layout_resolves_each_domain(tmp_path):
    ws = make_ws(tmp_path / "team")
    for d in wl.DOMAINS:
        assert wl.resolve_root(d, workspace=ws) == ws / d
    # walking up from deep inside a domain still finds the workspace marker, not a legacy hit
    deep = ws / "marketing" / "brain"
    assert wl.resolve_root("executive", env={"SINOR_CONFIG_DIR": str(tmp_path / "x")}, cwd=deep) == ws / "executive"


def test_combined_layout_wins_over_legacy_marker(tmp_path):
    base = tmp_path / "both"
    (base / "marketing").mkdir(parents=True)
    (base / "brain").mkdir()
    assert wl.resolve_root("marketing", workspace=base) == base / "marketing"


@pytest.mark.parametrize("domain,marker", [
    ("marketing", "brain"),
    ("executive", "knowledge/user"),
    ("sales", "config/routing.json"),
    ("sales", "incoming"),
])
def test_each_legacy_marker(tmp_path, domain, marker):
    repo = tmp_path / "legacy"
    target = repo / marker
    if marker.endswith(".json"):
        target.parent.mkdir(parents=True)
        target.write_text("{}")
    else:
        target.mkdir(parents=True)
    env = {"SINOR_CONFIG_DIR": str(tmp_path / "x")}
    # opened inside the legacy repo (walk-up from a subfolder)
    sub = repo / "sub"
    sub.mkdir()
    assert wl.resolve_root(domain, env=env, cwd=sub) == repo.resolve()
    # explicit base works too
    assert wl.resolve_root(domain, workspace=repo) == repo.resolve()
    # other domains are not resolved by this marker
    others = [d for d in wl.DOMAINS if d != domain and d not in wl.legacy_marker_domains(repo)]
    for o in others:
        assert wl.resolve_root(o, workspace=repo) is None


def test_walk_up_prefers_marker_file_over_nearer_legacy_marker(tmp_path):
    ws = make_ws(tmp_path / "team")
    (ws / "executive" / "knowledge" / "user").mkdir(parents=True, exist_ok=True)
    got = wl.find_base_by_walking(ws / "executive" / "knowledge" / "user")
    assert got == ws


# ---------------------------------------------------------------- unresolved errors

def test_root_unresolved_text_and_exit_code(tmp_path):
    r = cli("root", "marketing", cwd=tmp_path, env_extra={"SINOR_CONFIG_DIR": str(tmp_path / "cfg")})
    assert r.returncode == 2
    assert "/sinor-team:setup" in r.stderr and "marketing" in r.stderr
    assert r.stdout == ""


def test_root_domain_missing_in_found_workspace(tmp_path):
    legacy = tmp_path / "mk"
    (legacy / "brain").mkdir(parents=True)
    r = cli("root", "executive", "--workspace", str(legacy), cwd=tmp_path)
    assert r.returncode == 2
    assert "/sinor-team:setup" in r.stderr and "no 'executive' data" in r.stderr


def test_root_prints_absolute_path(tmp_path):
    ws = make_ws(tmp_path / "team")
    r = cli("root", "sales", "--workspace", str(ws), cwd=tmp_path)
    assert r.returncode == 0 and r.stdout.strip() == str(ws / "sales") and Path(r.stdout.strip()).is_absolute()
    r = cli("--workspace", str(ws), "root", "executive", cwd=tmp_path)  # option before the subcommand
    assert r.stdout.strip() == str(ws / "executive")


def test_unknown_domain_rejected(tmp_path):
    assert cli("root", "finance", cwd=tmp_path).returncode == 2  # argparse error


# ---------------------------------------------------------------- detect

def test_detect_json(tmp_path):
    ws = make_ws(tmp_path / "team")
    r = cli("detect", cwd=tmp_path, env_extra={"SINOR_WORKSPACE": str(ws)})
    info = json.loads(r.stdout)
    assert r.returncode == 0
    assert info["base"] == str(ws) and info["source"] == "env" and info["marker_file"] is True
    assert info["combined_layout"] == ["marketing", "executive", "sales"]
    assert info["domains"]["sales"] == str(ws / "sales")
    assert [c["step"] for c in info["candidates"]] == ["argument", "env", "walk-up", "config"]
    r = cli("detect", cwd=tmp_path, env_extra={"SINOR_CONFIG_DIR": str(tmp_path / "none")})
    info = json.loads(r.stdout)
    assert r.returncode == 0 and info["base"] is None and info["domains"]["executive"] is None


# ---------------------------------------------------------------- init

def snapshot(base):
    return {str(p.relative_to(base)): (p.read_bytes() if p.is_file() else None) for p in sorted(base.rglob("*"))}


def test_init_creates_layout_without_business_data(tmp_path):
    ws = tmp_path / "team"
    r = cli("init", str(ws), cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    assert (ws / ".sinor-workspace").is_file()
    for d in wl.DOMAINS:
        assert (ws / d / "README.md").is_file()
    for rel in ("marketing/brain", "marketing/campaigns", "executive/knowledge/user", "executive/tasks/active",
                "executive/quality/metrics", "executive/records/library", "sales/records", "sales/templates",
                "sales/incoming", "sales/sources", "sales/knowledge", "sales/tasks", "sales/quality"):
        assert (ws / rel).is_dir(), rel
    # only markers, READMEs and .gitkeep files: no data, no copies of knowledge
    files = [p.name for p in ws.rglob("*") if p.is_file()]
    assert set(files) <= {".sinor-workspace", "README.md", ".gitkeep"}
    # the new workspace resolves for every domain
    for d in wl.DOMAINS:
        assert wl.resolve_root(d, workspace=ws) == ws.resolve() / d


def test_init_is_idempotent_and_never_overwrites(tmp_path):
    ws = tmp_path / "team"
    first = wl.init_workspace(ws)
    assert first["created"] and first["skipped"] == []
    base = Path(first["path"])
    (base / "executive" / "README.md").write_text("MY OWN NOTES\n")
    (base / ".sinor-workspace").write_text("custom marker\n")
    (base / "sales" / "records" / "mine.json").write_text("{}")
    before = snapshot(base)
    second = wl.init_workspace(ws)
    assert second["created"] == []
    assert "executive/README.md" in second["skipped"] and ".sinor-workspace" in second["skipped"]
    assert snapshot(base) == before
    assert (base / "executive" / "README.md").read_text() == "MY OWN NOTES\n"
    # CLI run on top of existing data also leaves it alone
    r = cli("init", str(ws), cwd=tmp_path)
    assert r.returncode == 0 and snapshot(base) == before


def test_init_refuses_a_file_path(tmp_path):
    f = tmp_path / "afile"
    f.write_text("x")
    r = cli("init", str(f), cwd=tmp_path)
    assert r.returncode == 1 and "not a folder" in r.stderr
    assert f.read_text() == "x"


def test_init_into_existing_folder_keeps_other_files(tmp_path):
    ws = tmp_path / "team"
    (ws / "executive").mkdir(parents=True)
    (ws / "executive" / "existing.txt").write_text("keep")
    wl.init_workspace(ws)
    assert (ws / "executive" / "existing.txt").read_text() == "keep"


# ---------------------------------------------------------------- set and config file

def test_set_writes_config_and_root_uses_it(tmp_path):
    ws = make_ws(tmp_path / "team")
    cfgdir = tmp_path / "cfg"
    r = cli("set", str(ws), cwd=tmp_path, env_extra={"SINOR_CONFIG_DIR": str(cfgdir)})
    assert r.returncode == 0, r.stderr
    data = json.loads((cfgdir / "config.json").read_text())
    assert data == {"workspace": str(ws)}
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    r = cli("root", "executive", cwd=elsewhere, env_extra={"SINOR_CONFIG_DIR": str(cfgdir)})
    assert r.returncode == 0 and r.stdout.strip() == str(ws / "executive")


def test_set_honours_xdg_config_home(tmp_path):
    ws = make_ws(tmp_path / "team")
    xdg = tmp_path / "xdg"
    r = cli("set", str(ws), cwd=tmp_path, env_extra={"XDG_CONFIG_HOME": str(xdg), "HOME": str(tmp_path / "home")})
    assert r.returncode == 0, r.stderr
    assert json.loads((xdg / "sinor-team" / "config.json").read_text())["workspace"] == str(ws)


def test_sinor_config_dir_wins_over_xdg(tmp_path):
    env = {"SINOR_CONFIG_DIR": str(tmp_path / "a"), "XDG_CONFIG_HOME": str(tmp_path / "b")}
    assert wl.config_path(env) == tmp_path / "a" / "config.json"
    assert wl.config_path({"XDG_CONFIG_HOME": str(tmp_path / "b")}) == tmp_path / "b" / "sinor-team" / "config.json"


def test_default_config_location_is_under_home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "h"))
    assert wl.config_path({}) == tmp_path / "h" / ".config" / "sinor-team" / "config.json"


def test_set_rejects_missing_folder_and_keeps_other_keys(tmp_path):
    cfgdir = tmp_path / "cfg"
    r = cli("set", str(tmp_path / "missing"), cwd=tmp_path, env_extra={"SINOR_CONFIG_DIR": str(cfgdir)})
    assert r.returncode == 1 and not (cfgdir / "config.json").exists()
    cfgdir.mkdir()
    (cfgdir / "config.json").write_text(json.dumps({"other": 1}))
    ws = make_ws(tmp_path / "team")
    cli("set", str(ws), cwd=tmp_path, env_extra={"SINOR_CONFIG_DIR": str(cfgdir)})
    assert json.loads((cfgdir / "config.json").read_text()) == {"other": 1, "workspace": str(ws)}


def test_corrupt_config_is_ignored(tmp_path):
    cfgdir = tmp_path / "cfg"
    cfgdir.mkdir()
    (cfgdir / "config.json").write_text("{not json")
    assert wl.read_config({"SINOR_CONFIG_DIR": str(cfgdir)}) == {}
