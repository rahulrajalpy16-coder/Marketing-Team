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

## P-006 | .claude/skills/website-build-standards/SKILL.md | proposed 2026-11-06
- Before: no rule on 3D, WebGL or animation libraries.
- After: add "3D, WebGL canvas and animation libraries (GSAP, Lenis, three.js) need Rahul's approval. Default is CSS scroll-driven effects with a static fallback and a prefers-reduced-motion path. Hero visual under 300 KB."
- Reason: the three cinematic references rely on those libraries; the default stack and 1.5 MB budget forbid them silently.

## P-007 | .claude/agents/web-copywriter.md, seo-a11y-specialist.md, web-strategist.md, ux-architect.md, fact-reviewer.md | proposed 2026-11-07
- Before: these agents have no shell or Grep tool, so they cannot run dash scans, banned-word greps or character counts; three of them said so in their reports and counted lengths by hand.
- After: give web-copywriter and seo-a11y-specialist Bash and Grep (and seo-a11y-specialist Edit) so they can count characters, grep their own files and patch their own specs.
- Reason: the Director had to re-run every check after each report. Hand counts were right but unproven.

## P-008 | .claude/skills/website-build-standards/SKILL.md | proposed 2026-11-07
- Before: no rule for launch readiness of slot boxes or unconfirmed content.
- After: add "Every unfilled slot is a box with a data-slot attribute. Before launch count [data-slot] boxes and fill or remove each. DRAFT markers mark unconfirmed content and also count. Pre-launch builds ship noindex and a robots.txt Disallow."
- Reason: QA found 98 boxes with two different labels; a text search would have missed the DRAFT ones.
