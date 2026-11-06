# Proposed changes (waiting for Rahul's approval)

Show at most five in a handoff. When approved: apply, log in brain/change-log.md, remove from this queue.
Format: ID | target file | before | after | reason | date proposed.

## P-001 | .claude/skills/video-qa-checklist/SKILL.md | proposed 2026-11-06
- Before: step 7 checks logos, claims and partner names only.
- After: add step "Scan every source photo used for incidental on-screen text (file names, readable badges, other companies' branding, personal data) and list what is visible."
- Reason: a media file name was visible on the stand video wall in an ADIPEC photo; QA found it only because the prompt asked.

## P-002 | .claude/agents/copywriter.md | proposed 2026-11-06
- Before: Never list has no rule about ownership words.
- After: add "Never write 'our' or 'my' for equipment, products or partner systems unless ownership is confirmed in the brief or verified-facts.md."
- Reason: the first draft said "our DP console" for equipment that Rahul's layout notes list as MT or NAVIS units.

## P-003 | .claude/skills/platform-video-specs/SKILL.md | proposed 2026-11-06
- Before: no guidance for photo-only slideshows.
- After: add "Photo-only video: use 4:5 1080x1350, cover-crop portrait photos (trim the ceiling, keep feet), fit landscape photos on a blurred copy, keep captions and titles above the bottom 150 px, hold each photo 3.5 to 4.5 s, 0.5 s crossfades, one end card thanking people and partners."
- Reason: this layout worked for the ADIPEC post and is reproducible via campaigns/2026-11-adipec26-thanks/exports/build_video.py.

## P-004 | CLAUDE.md | proposed 2026-11-06
- Before: Pointers section lists 4 skills and says specialists are in .claude/agents/ (10 files). No mention of the website team.
- After: add one line under Pointers: "Website team (7 agents, 3 website-* skills): see docs/web-team-playbook.md. Scaffold with scripts/web_new_project.sh, test with scripts/web_qa.mjs." and change "(10 files)" to "(17 files)".
- Reason: so every future session knows the website team exists without reading the docs folder. CLAUDE.md edits need approval.

## P-005 | CLAUDE.md | proposed 2026-11-06
- Before: Platform and quality rules cover video and LinkedIn only.
- After: add "Website: build with the website-build-standards skill; independent QA with web-qa-reviewer; never publish, connect forms, add trackers or share a preview link without approval."
- Reason: makes the website approval limits permanent rules, not only agent text.
