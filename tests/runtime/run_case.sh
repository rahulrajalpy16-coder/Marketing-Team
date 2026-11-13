#!/bin/bash
# Run one prompt through headless Claude Code with the plugin loaded, saving the event stream.
# usage: PLUGIN_DIR=plugins/sinor-team WORKSPACE=/path/to/test-workspace tests/runtime/run_case.sh <case-id> "<prompt>"
# Needs the `claude` CLI signed in. Use a THROWAWAY workspace (python3 scripts/workspace.py init <dir>).
# Headless runs cannot answer permission prompts: allowed tools are listed below, anything else is denied.
set -uo pipefail
ID="${1:?case id}"; shift
PLUGIN_DIR="${PLUGIN_DIR:?set PLUGIN_DIR to the plugin folder}"
WORKSPACE="${WORKSPACE:?set WORKSPACE to a throwaway workspace folder}"
OUT="${OUT_DIR:-./runtime-results}"; mkdir -p "$OUT"
cd "$WORKSPACE"
timeout "${CASE_TIMEOUT:-600}" claude -p "$*" --plugin-dir "$PLUGIN_DIR" \
  --output-format stream-json --verbose --max-turns "${MAX_TURNS:-40}" \
  --allowedTools "Bash" "Read" "Write" "Edit" "Skill" "Agent" ${EXTRA_TOOLS:-} \
  > "$OUT/out-$ID.jsonl" 2> "$OUT/err-$ID.txt"
echo "$ID exit=$?"
