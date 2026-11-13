"""Shared test setup: scripts on sys.path and a clean environment (no leaking SINOR_* settings)."""
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[1]
SCRIPTS = PLUGIN / "scripts"
sys.path.insert(0, str(SCRIPTS))


@pytest.fixture(autouse=True)
def clean_env(monkeypatch, tmp_path_factory):
    for k in ("SINOR_ROOT", "SINOR_WORKSPACE", "CLAUDE_PROJECT_DIR", "SINOR_PLUGIN_ROOT",
              "SINOR_CONFIG_DIR", "XDG_CONFIG_HOME"):
        monkeypatch.delenv(k, raising=False)
    # never read or write the real user config during tests
    monkeypatch.setenv("SINOR_CONFIG_DIR", str(tmp_path_factory.mktemp("cfg")))
