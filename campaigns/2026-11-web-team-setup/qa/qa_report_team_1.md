# QA report team 1: website design and development team package

Reviewer: independent checker (separate invocation from the builder). Date: 2026-11-06.
Nothing in the package was edited. Only this file was written in the repo.

## Verdict
No FAIL that blocks use. 1 MAJOR bug in scripts/web_qa.mjs (mobile-only elements go untested), 3 MINOR consistency defects, several LOW notes. Fix the MAJOR and the ordering conflict before the first real project.

## Checks and results

### 1. Dashes (U+2014, U+2013)
Ran grep -nP '\xE2\x80[\x93\x94]' over all 15 files. Result: exactly one hit, scripts/web_qa.mjs:133, an em dash literal inside the regex `/—/` that detects em dashes on pages. It is functional, not prose. See D6 (use `—` so the repo grep stays clean). No other file has em or en dashes. PASS with note.

### 2. Frontmatter
Checked lines 1-6 of every file. All 7 agents have name, description, tools. memory: project present on the 6 agents that should have it; absent on web-qa-reviewer (correct). 3 skills have name and description (skills have no tools field in this repo; I did not compare with existing skills beyond that). Tool sets: web-qa-reviewer matches qa-reviewer (Read, Bash, Glob, Grep, Write). PASS.

### 3. Path consistency
web_new_project.sh creates: brief, inputs, references, research, design, copy, site/assets, qa, exports, plus brief.md, reference-sites.md, inputs.md. Everything agents write is covered by those folders: brief/strategy.md, design/{sitemap,wireframes,design-system,seo-spec,a11y-spec}.md, design/tokens.css, references/design-dna.md, copy/<page>.md, site/, exports/build-notes.md, qa/web_qa_report_<n>.md, qa/retro.md. Design folder file names are identical across the ux-architect, ui-designer, seo-a11y, frontend and skill files. Existing paths referenced exist: assets/brand/sinor-logo.png, brain files, marine-technical-accuracy skill, platform-researcher, fact-reviewer, art-director, media-librarian agents, all three scripts. No broken path found.
Mismatches (not broken paths):
- D4: the brief says "finished site in exports" (brief.md line 14) but every agent, the skill and the playbook put the site in site/ and only notes in exports/. Wording only.
- D8: web-qa-reviewer and the skill name the QA output `/tmp/work/<name>/qa` (outside the repo) while saying "never write outside qa/". Screenshots going to /tmp/work is intended (repo-size rule) but the rule text conflicts; state the exemption.

### 4. Contradictions
- D1 (MINOR, real ordering conflict): playbook line 33 and build-standards "Order of work" run ux-architect and seo-a11y-specialist in parallel, but seo-a11y-specialist reads design/sitemap.md (and copy/ "if present") that ux-architect has not yet written. Also ui-designer (playbook line 33) is told to start in parallel but reads wireframes "if present", which is fine. Owner: Director (playbook, skill), seo-a11y-specialist.
- D2 (MINOR, duplicate ownership): page title and meta description are specified by seo-a11y-specialist (seo-spec.md, written before copy exists) AND proposed by web-copywriter (copy/<page>.md, targets 50-60 and 120-155 chars). frontend-developer is told to implement them "only as written in seo-spec.md", and web-qa-reviewer compares rendered text with copy/. If the two differ, QA cannot tell which is right. Name one owner (suggest copywriter drafts, seo-a11y approves into seo-spec.md) and have the order say so. Owner: Director.
- D3 (LOW): length thresholds differ slightly: copywriter 50-60 / 120-155; web_qa.mjs warns at title >65 and description <70 or >165. Not contradictory (looser warn band) but undocumented.
- No contradiction found in: QA cycle count (2 in skill and playbook), 5 MB repo limit, image limits (300 KB each, 2 MB total, only in the build skill), publishing rule (never without approval, in strategist, frontend, skill, playbook), forms not connected, no CDN/fonts, brain/ edits by Director only.
- D9 (LOW): frontend-developer and ui-designer have Bash but no agent says "do not install packages". Setup script says ask Rahul first. Add one line.

### 5. Honesty
- Playbook line 3 correctly says only the reel's caption was read, and the brief says the video was not watched and the reel is about editing reels. Good.
- D5 (MINOR): playbook heading "The seven steps (the reel's pattern, applied to web)" presents a mapping as if it were the reel's list. The brief records the reel's steps as: desktop app, dedicated folder (raw/references/exports), one setup prompt, outside API key for speech to text, teach style from 3+ reels, drop footage in raw, run one edit prompt. Playbook step 1 swaps "desktop app" for "Claude Code with this repo", step 3 reverses the API-key step, the folder differs (no raw). Add "adapted" and say so in the playbook, not only in the brief. Also playbook line 19 says "Nothing to install", true in this session (setup check OK) but not guaranteed in a fresh cloud session; the script itself can report MISSING.
- Brief claims "Tested with a fixture site": I confirmed that fixtures exist in the scratchpad and web_qa.mjs works on them (see section 6). I did not verify the claim about "brain updates" in the brief: git status shows no brain/ changes yet (all new files untracked, none under brain/). Either the brain updates are still to come or the brief overstates. Owner: Director.
- I could NOT independently verify: the reel caption text and posting date (not fetched), or that the URLs in the quality-gate table were opened on 2026-11-06 ("verified 2026-11-06"). Treat as builder-reported.
- Build-standards says Web Vitals are field metrics at p75 and the lab run is indicative only; web_qa.mjs report repeats it. Honest.

### 6. scripts/web_qa.mjs (code read in full, run on fixtures)
Ran on scratchpad good (0 FAIL, 1 WARN: 375px input under 24 px, plausible) and bad (20 FAIL, 8 WARN, exit 1; found 404, console error, overflow, missing title, lang, viewport, 2 h1, alt, nameless button, unlabeled input, no main, low contrast 1.92:1, lorem, broken links). Exit codes correct. bash scripts/web_setup_check.sh: all OK, rc 0.
Defects:
- D6 (MAJOR): only the 1440 px pass feeds the findings (line 136 `if (vp.w === 1440)`); the 375 pass result `d` is used only for target size (line 171). Elements that exist only on mobile (hamburger button, mobile nav) are hidden at 1440, so `vis()` filters them out of empty-button, empty-link, label and contrast checks. Reproduced: a nameless `<button>` shown only under 600 px produced no FAIL. Contrast at 375 is computed and discarded. Fix: run name/label/contrast checks at both widths. Owner: frontend-developer or Director (script owner).
- D7 (LOW): `aria-labelledby` returns the id string as the accessible name (line 88) without checking the id exists or has text, so a broken reference passes. Contrast ignores opacity and text alpha; documented partly ("ignores semi-transparent backgrounds").
- D10 (LOW): crawl follows only links ending in `/` or `.htm(l)` (line 168); a link like /about is checked with fs and reported as a broken internal link even if a host would serve it. Static-site default avoids it but the report would give a false FAIL. Crawl stops silently at 50 pages (line 49) with no note in the report.
- D11 (LOW): server path guard `f.startsWith(siteDir)` allows a sibling directory with the same prefix; malformed percent-encoding in a URL throws in decodeURIComponent and crashes the run (line 28). Local only. Internal link existence check does not decode percent-encoded names (line 177), so a file with a space may false-FAIL.
- D12 (LOW): em dash check is on body.innerText only (not title, meta, alt) and does not check en dash. Rule says visible text, so partial.
- D13 (LOW): WCAG 2.5.8 check flags any target under 24 px without the spacing exception, so false WARNs are possible (WARN only).
- Lazy images: tested, a full-page screenshot did load a lazy image below the fold (404 was caught), so that suspected gap does not exist in this Chromium.
- Not tested: external-request detection against a real external URL (no network use), a page with a CSS background image, pages above 50, hover/focus states.

### 7. Authority limits (CLAUDE.md)
No agent is told to publish, deploy, share links, spend money, contact anyone or install software. Strategist, frontend-developer, skill and playbook explicitly require Rahul's approval for publishing, domain, hosting, analytics, form endpoints and shareable previews. Setup script installs nothing and says ask first. Playbook correctly notes the repo is public per brain/capabilities.md. Gap only D9 (no explicit no-install line in agents). Also the web-qa-reviewer and frontend-developer run a headless local server on 127.0.0.1, which is local, not public. PASS.

## Defect table
| ID | Sev | File and line | Issue | Owner |
|----|-----|---------------|-------|-------|
| D6 | MAJOR | scripts/web_qa.mjs 136, 171 | Mobile-only elements not checked | Director / frontend-developer |
| D1 | MINOR | docs/web-team-playbook.md 33; website-build-standards "Order of work" | seo-a11y runs parallel to ux-architect but needs sitemap | Director |
| D2 | MINOR | web-copywriter 9, seo-a11y-specialist 9, frontend-developer 9 | Titles and meta have two owners | Director |
| D5 | MINOR | docs/web-team-playbook.md heading of seven steps, line 19 | Adapted steps labeled as the reel's pattern; "Nothing to install" overstated | Director |
| D4 | LOW | brief.md 14 | "finished site in exports" vs site/ | Director |
| D8 | LOW | web-qa-reviewer 8-10, website-qa-checklist step 2 | /tmp/work output vs "never write outside qa/" | Director |
| D9 | LOW | frontend-developer, ui-designer | No no-install rule | Director |
| D3 | LOW | web-copywriter 9 vs web_qa.mjs 138-139 | Different length thresholds | Director |
| D7, D10-D13 | LOW | web_qa.mjs lines 88, 168, 49, 28, 177, 133, 171 | See section 6 | Director |
| D14 | LOW | brief.md "brain updates" | Not seen in git status; unverified claim | Director |

## Scope: what I did and did not do
Did: read all 15 files and the three comparison agent headers; grep for dashes; frontmatter inspection; path cross-check against the file system; ran web_setup_check.sh; ran web_qa.mjs on good, bad and one new mobile fixture in the scratchpad (not in the repo).
Did not: open or fetch Instagram or the web.dev and W3C URLs; judge design quality; launch any of the agents; run the full pipeline; test the guard script; verify Chromium on Safari or devices; compare skill frontmatter with existing skills line by line.

## Candidate lessons for the Director
- A QA script that only evaluates at one viewport hides mobile-only controls; require checks at each viewport and prove it with a fixture.
- When two agents can both draft the same field (title, meta), name one owner in the pipeline.
- Label adapted workflows as adapted; do not call a mapping the source's own pattern.
