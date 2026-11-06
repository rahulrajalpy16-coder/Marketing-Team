# Retro: web team setup (2026-11-06)

## What happened
Reel link read via TinyFish (caption only). It was about editing reels, not websites; request interpreted as "same operating pattern for web". Built 7 agents, 3 skills, 3 scripts, playbook. Standards numbers checked against web.dev and W3C search excerpts. Independent review by the existing qa-reviewer found 1 MAJOR (mobile-only elements untested), 3 MINOR, several LOW; all MAJOR and MINOR fixed, most LOW fixed.

## Not done, said plainly
- The 7 new agents have not been run (they load next session). No real website was built.
- Video content of the reel not seen. No review of the fixes by a second independent pass; the fixes were re-tested by running the script on fixtures only.
- LOW items left open: WCAG 2.5.8 spacing exception not modelled (may over-warn), opacity not in contrast, extensionless links count as broken.

## Sorting
A. Applied now: platform-specs website rows (verified 2026-11-06), manifest.
B. Provisional lessons added: 5 (brain/lessons-learned.md).
C. Proposed, needs approval: P-004 and P-005 (CLAUDE.md pointer and website rule) in brain/proposed-changes.md.
