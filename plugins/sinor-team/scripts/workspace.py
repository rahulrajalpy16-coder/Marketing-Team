#!/usr/bin/env python3
"""Find, choose and create the Sinor team workspace (where all business data lives).

Subcommands:
  root <marketing|executive|sales>   print the absolute data root; exit 2 with a setup hint if unresolved
  detect                              JSON describing what was found and how
  set <path>                          remember the workspace in the user config file
  init <path>                         create the combined layout (empty skeleton, no business data)

Resolution order (first hit wins): --workspace, env SINOR_WORKSPACE, walk up from
CLAUDE_PROJECT_DIR then the current directory, then the saved config file.
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import workspace_lib as wl  # noqa: E402


def cmd_root(a) -> int:
    root = wl.resolve_root(a.domain, workspace=a.workspace)
    if root is None:
        print(wl.unresolved_message(a.domain, workspace=a.workspace), file=sys.stderr)
        return 2
    print(root)
    return 0


def cmd_detect(a) -> int:
    print(json.dumps(wl.detect(workspace=a.workspace), indent=2))
    return 0


def cmd_set(a) -> int:
    p = Path(a.path).expanduser()
    if not p.is_dir():
        print(f"ERROR: {p} is not an existing folder. Create it first, or run: workspace.py init {p}",
              file=sys.stderr)
        return 1
    cfg = wl.write_config(p)
    print(f"saved workspace {p.resolve()} to {cfg}")
    if not (p / wl.MARKER_FILE).is_file() and not wl.legacy_marker_domains(p) and not wl.combined_domains(p):
        print("note: this folder has no .sinor-workspace marker or Sinor data yet; "
              "run `workspace.py init` on it to create the layout.", file=sys.stderr)
    return 0


def cmd_init(a) -> int:
    try:
        res = wl.init_workspace(a.path)
    except (ValueError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(json.dumps(res, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="workspace", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", default=None, help="explicit workspace base folder")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("root")
    r.add_argument("domain", choices=list(wl.DOMAINS))
    r.add_argument("--workspace", dest="workspace_sub", default=None)
    r.set_defaults(fn=cmd_root)
    d = sub.add_parser("detect")
    d.add_argument("--workspace", dest="workspace_sub", default=None)
    d.set_defaults(fn=cmd_detect)
    s = sub.add_parser("set")
    s.add_argument("path")
    s.set_defaults(fn=cmd_set)
    i = sub.add_parser("init")
    i.add_argument("path")
    i.set_defaults(fn=cmd_init)
    return ap


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    sub_ws = getattr(a, "workspace_sub", None)
    if sub_ws:
        a.workspace = sub_ws
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
