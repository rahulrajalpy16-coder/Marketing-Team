"""Shared helpers for the sinor-team hooks.

Every hook is a no-op unless the session is working inside a Sinor workspace (found by
walking up from the project folder). This keeps the plugin from disturbing unrelated projects.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

import workspace_lib as wl  # noqa: E402


def project_dir() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())


def workspace_base(start: Path | None = None) -> Path | None:
    """Workspace base folder when `start` (default: the project folder) is inside one."""
    try:
        return wl.find_base_by_walking(Path(start) if start else project_dir())
    except OSError:
        return None


def domain_root(domain: str, start: Path | None = None) -> Path | None:
    base = workspace_base(start)
    return wl.domain_root_in(base, domain) if base else None
