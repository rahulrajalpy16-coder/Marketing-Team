"""Workspace resolution for the sinor-team plugin (DESIGN.md section 2).

Standard library only. The plugin holds code; the workspace holds business data.

Domain markers, checked in this order for a base folder B and domain D:

    domain      combined layout        legacy marker (B itself is the root)
    marketing   B/marketing/           B/brain/
    executive   B/executive/           B/knowledge/user/
    sales       B/sales/               B/config/routing.json or B/incoming/

Base folder resolution, first hit wins:
    1. explicit argument (--workspace)
    2. env SINOR_WORKSPACE
    3. walk up from CLAUDE_PROJECT_DIR, then from the current directory, looking for
       .sinor-workspace (preferred) or a legacy marker
    4. the user config file (config.json, key "workspace")

Config file location: $SINOR_CONFIG_DIR/config.json if set, else
$XDG_CONFIG_HOME/sinor-team/config.json if set, else ~/.config/sinor-team/config.json.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

DOMAINS = ("marketing", "executive", "sales")
MARKER_FILE = ".sinor-workspace"

# domain -> (combined folder name, legacy marker relative paths, any one is enough)
LEGACY_MARKERS = {
    "marketing": [("brain",)],
    "executive": [("knowledge", "user")],
    "sales": [("config", "routing.json"), ("incoming",)],
}

SETUP_HINT = ("Run /sinor-team:setup to choose or create the Sinor workspace, "
              "or set the SINOR_WORKSPACE environment variable to its folder.")


# --------------------------------------------------------------------------
# Config file
# --------------------------------------------------------------------------

def config_dir(env: dict | None = None) -> Path:
    env = os.environ if env is None else env
    explicit = env.get("SINOR_CONFIG_DIR")
    if explicit:
        return Path(explicit)
    xdg = env.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / "sinor-team"
    return Path(os.path.expanduser("~")) / ".config" / "sinor-team"


def config_path(env: dict | None = None) -> Path:
    return config_dir(env) / "config.json"


def read_config(env: dict | None = None) -> dict:
    p = config_path(env)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def write_config(workspace: str | Path, env: dict | None = None) -> Path:
    """Store the workspace as an absolute path. Keeps other keys already in the file."""
    p = config_path(env)
    data = read_config(env)
    data["workspace"] = str(Path(workspace).expanduser().resolve())
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return p


# --------------------------------------------------------------------------
# Markers
# --------------------------------------------------------------------------

def legacy_marker_domains(base: Path) -> list[str]:
    """Domains for which `base` itself looks like a legacy single-repo root."""
    found = []
    for dom in DOMAINS:
        for parts in LEGACY_MARKERS[dom]:
            if (base.joinpath(*parts)).exists():
                found.append(dom)
                break
    return found


def combined_domains(base: Path) -> list[str]:
    return [d for d in DOMAINS if (base / d).is_dir()]


def domain_root_in(base: Path, domain: str) -> Path | None:
    """Root of `domain` inside base: combined layout first, then legacy marker."""
    if domain not in DOMAINS:
        raise ValueError(f"unknown domain {domain!r}; use one of {', '.join(DOMAINS)}")
    if (base / domain).is_dir():
        return (base / domain).resolve()
    if domain in legacy_marker_domains(base):
        return base.resolve()
    return None


def _walk_up(start: Path):
    start = start.resolve()
    yield start
    yield from start.parents


def find_base_by_walking(start: Path) -> Path | None:
    """Nearest folder holding .sinor-workspace; failing that, nearest legacy marker."""
    for d in _walk_up(start):
        if (d / MARKER_FILE).is_file():
            return d
    for d in _walk_up(start):
        if legacy_marker_domains(d):
            return d
    return None


# --------------------------------------------------------------------------
# Base folder resolution
# --------------------------------------------------------------------------

def candidates(workspace: str | Path | None = None, env: dict | None = None,
               cwd: str | Path | None = None) -> list[dict]:
    """All four resolution steps in order, each with the base it produced (or None)."""
    env = os.environ if env is None else env
    out: list[dict] = []

    def add(step: str, base: Path | None, detail: str = ""):
        out.append({"step": step, "base": str(base) if base else None, "detail": detail})

    # 1. explicit argument
    if workspace:
        add("argument", Path(workspace).expanduser().resolve(), "--workspace")
    else:
        add("argument", None, "not given")
    # 2. environment variable
    ev = env.get("SINOR_WORKSPACE")
    if ev:
        add("env", Path(ev).expanduser().resolve(), "SINOR_WORKSPACE")
    else:
        add("env", None, "SINOR_WORKSPACE not set")
    # 3. walk up
    found = None
    detail = "nothing found"
    starts = []
    if env.get("CLAUDE_PROJECT_DIR"):
        starts.append(("CLAUDE_PROJECT_DIR", Path(env["CLAUDE_PROJECT_DIR"])))
    starts.append(("current directory", Path(cwd) if cwd else Path.cwd()))
    for label, s in starts:
        try:
            hit = find_base_by_walking(s)
        except OSError:
            hit = None
        if hit:
            found, detail = hit, f"walked up from {label}"
            break
    add("walk-up", found, detail)
    # 4. config file
    cfg = read_config(env).get("workspace")
    if cfg:
        add("config", Path(cfg).expanduser(), str(config_path(env)))
    else:
        add("config", None, "no workspace in config file")
    return out


def find_base(workspace: str | Path | None = None, env: dict | None = None,
              cwd: str | Path | None = None) -> tuple[Path | None, str]:
    """First hit wins. Returns (base, source step name)."""
    for c in candidates(workspace, env, cwd):
        if c["base"]:
            return Path(c["base"]), c["step"]
    return None, "none"


def resolve_root(domain: str, workspace: str | Path | None = None, env: dict | None = None,
                 cwd: str | Path | None = None) -> Path | None:
    """Absolute root of `domain`, or None when it cannot be resolved."""
    if domain not in DOMAINS:
        raise ValueError(f"unknown domain {domain!r}; use one of {', '.join(DOMAINS)}")
    base, _src = find_base(workspace, env, cwd)
    if base is None:
        return None
    return domain_root_in(base, domain)


def unresolved_message(domain: str, workspace: str | Path | None = None, env: dict | None = None,
                       cwd: str | Path | None = None) -> str:
    base, src = find_base(workspace, env, cwd)
    if base is None:
        why = "No Sinor workspace was found (checked --workspace, SINOR_WORKSPACE, the project folder and its parents, and the saved setup)."
    else:
        why = (f"A workspace folder was found ({src}) but it has no '{domain}' data "
               f"(expected '{domain}/' inside it, or a legacy {domain} repository layout).")
    return f"Cannot resolve the {domain} workspace root. {why} {SETUP_HINT}"


def detect(workspace: str | Path | None = None, env: dict | None = None,
           cwd: str | Path | None = None) -> dict:
    env = os.environ if env is None else env
    cands = candidates(workspace, env, cwd)
    base, src = find_base(workspace, env, cwd)
    domains = {}
    for d in DOMAINS:
        r = domain_root_in(base, d) if base else None
        domains[d] = str(r) if r else None
    info = {
        "base": str(base) if base else None,
        "source": src,
        "marker_file": bool(base and (base / MARKER_FILE).is_file()),
        "combined_layout": combined_domains(base) if base else [],
        "legacy_markers": legacy_marker_domains(base) if base else [],
        "domains": domains,
        "candidates": cands,
        "config_file": str(config_path(env)),
        "config_exists": config_path(env).is_file(),
    }
    return info


# --------------------------------------------------------------------------
# init: scaffold the combined layout (no business data)
# --------------------------------------------------------------------------

MARKER_TEXT = ("Sinor team workspace marker. Created by the sinor-team plugin. "
               "Do not delete: it tells the tools this folder holds team data.\n")

# folder skeleton per domain; every leaf gets a .gitkeep so a git clone keeps the folders
SKELETON = {
    "marketing": ["brain", "campaigns", "assets"],
    "executive": ["knowledge/user", "tasks/active", "tasks/completed", "quality/metrics",
                  "quality/audit-reports", "quality/test-evidence", "learning/lessons",
                  "records/library"],
    "sales": ["records", "knowledge", "templates", "tasks", "quality", "incoming", "sources"],
}

README = {
    "marketing": (
        "# Marketing workspace\n\n"
        "Campaign data for the Marketing Director workflow.\n\n"
        "- brain/: preferences, lessons, brand profile, platform specs, deliveries log\n"
        "- campaigns/: one folder per campaign (brief, manifest, research, QA, captions)\n"
        "- assets/: pointers to media (links and notes only; raw or edited media never goes in git)\n\n"
        "This folder starts empty. The plugin never writes its own files here.\n"),
    "executive": (
        "# Executive workspace\n\n"
        "Records for the Executive Supervisor workflow.\n\n"
        "- knowledge/user/: learned preferences, lessons, corrections\n"
        "- tasks/: task records (active and completed)\n"
        "- quality/: QA audit reports, evidence and metrics\n"
        "- learning/: lesson application records\n"
        "- records/: quote history, clients, document library\n\n"
        "This folder starts empty. Business data is added by the team, never by the plugin.\n"),
    "sales": (
        "# Sales and estimation workspace\n\n"
        "Records for the Sales and Estimation workflow.\n\n"
        "- records/: registered documents, memory and task records\n"
        "- knowledge/: approved sales knowledge\n"
        "- templates/: approved quotation templates (add them here; none are supplied)\n"
        "- tasks/: task folders with original instruction and outputs\n"
        "- quality/: QA records\n"
        "- incoming/: new files waiting for registration\n"
        "- sources/: registered source files kept by SHA-256\n\n"
        "This folder starts empty. Prices and templates come from the team, never from the plugin.\n"),
}

ROOT_README = (
    "# Sinor team workspace\n\n"
    "Private business data for the sinor-team plugin: marketing/, executive/ and sales/.\n"
    "Keep this folder in a private repository shared only with the team.\n"
    "The plugin code lives elsewhere and is never stored here.\n")


def init_workspace(path: str | Path) -> dict:
    """Create the combined layout at `path`. Never overwrites an existing file.

    Returns {"path", "created": [...], "skipped": [...]} with paths relative to `path`.
    Raises ValueError if `path` exists and is not a directory.
    """
    base = Path(path).expanduser()
    if base.exists() and not base.is_dir():
        raise ValueError(f"{base} exists and is not a folder")
    base.mkdir(parents=True, exist_ok=True)
    base = base.resolve()
    created: list[str] = []
    skipped: list[str] = []

    def write_new(rel: str, text: str):
        p = base / rel
        if p.exists():
            skipped.append(rel)
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("x", encoding="utf-8") as fh:  # 'x' refuses to overwrite
            fh.write(text)
        created.append(rel)

    def make_dir(rel: str):
        p = base / rel
        if not p.exists():
            p.mkdir(parents=True)
            created.append(rel + "/")

    write_new(MARKER_FILE, MARKER_TEXT)
    write_new("README.md", ROOT_README)
    for dom in DOMAINS:
        make_dir(dom)
        write_new(f"{dom}/README.md", README[dom])
        for sub in SKELETON[dom]:
            make_dir(f"{dom}/{sub}")
            keep = f"{dom}/{sub}/.gitkeep"
            # only add .gitkeep when the folder holds nothing else yet
            folder = base / dom / sub
            if not any(folder.iterdir()):
                write_new(keep, "")
    return {"path": str(base), "created": created, "skipped": skipped}
