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

## P-004 | CLAUDE.md and .claude/skills/platform-video-specs/SKILL.md | proposed 2026-11-06
- Before: research is "when it would improve the result"; the skill covers specs only.
- After: CLAUDE.md platform rules gain "Every video or visual job starts with research of current trending formats, comparable posts and template styles on the target platform (campaigns/<name>/research/research.md). Never skipped for small jobs." The skill gains a "Trend and template scan" step with the same content. Already applied as a working rule through brain/preferences.md; this formalises it.
- Reason: Rahul's explicit instruction, 2026-11-06.


## P-005 | new skill .claude/skills/product-catalogue-brochure/SKILL.md | proposed 2026-11-11
- Before: no written procedure for catalogue or brochure jobs.
- After: add a skill with the workflow that worked: extract products from the job register by frequency, build a catalogue JSON with register evidence counts, split into slices for Firecrawl discovery agents (official image and description only, no downloads), batch-approve exact image hosts, download, build a labelled contact sheet and look at it, drop wrong or generic images and ASK Rahul for them, generate A4 HTML to PDF with Node Playwright, independent qa-reviewer pass, credit sheet per image.
- Reason: the job took many steps and several wrong turns; the procedure is reusable for any future catalogue.

## P-006 | .claude/agents/platform-researcher.md | proposed 2026-11-11
- Before: tools are Read, Write, WebSearch, WebFetch.
- After: add the Firecrawl search and scrape tools, and a rule "if a page fails to load because the host is not allowed, retry the same page through Firecrawl scrape before reporting it unread".
- Reason: in the brochure job every WebFetch failed on blocked hosts and the catalogue-layout study was not done.
