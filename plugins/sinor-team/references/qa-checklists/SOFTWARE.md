# QA Checklist: Software and Automation

- S1 The software runs. Re-run the test suite yourself and record the exact command and output summary.
- S2 Tests cover the stated requirements, including edge cases named in the instruction.
- S3 It is functional, not a mockup, when functionality was requested.
- S4 No secrets in code or config. No calls to external services without approval.
- S5 Install and run instructions are present and correct (try them).
- S6 For web or PWA work, load it headlessly (Playwright with Chromium at /opt/pw-browsers) and check the main flow and mobile viewport.
