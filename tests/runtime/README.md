# Runtime checks (live Claude Code)

These are not unit tests. They run real prompts through the `claude` CLI and need a signed-in
session, so they cost usage and their results vary from run to run. Read the summaries; do not
expect identical wording.

```
python3 plugins/sinor-team/scripts/workspace.py init /tmp/sinor-test-ws     # throwaway workspace
export PLUGIN_DIR=$PWD/plugins/sinor-team WORKSPACE=/tmp/sinor-test-ws
tests/runtime/run_case.sh linkedin "Write a LinkedIn post for the company account thanking our partners after ADIPEC."
python3 tests/runtime/summarize.py ./runtime-results
```

`cases.tsv` lists the prompts used for the 0.1.0 validation and what each one should show.
Headless runs cannot answer permission prompts, so tools you do not allow in `run_case.sh`
are denied; judge workflow behaviour with that in mind (see `docs/VALIDATION_REPORT.md`).
