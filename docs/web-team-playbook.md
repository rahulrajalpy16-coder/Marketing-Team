# Website design and development team: playbook

Built 2026-11-06. Modelled on the operating pattern in the VYON reel (https://www.instagram.com/reel/DfZC7SOzO16/): one project folder, one setup check, a style taught from 3+ examples, inputs dropped in one place, one run prompt. Only the reel's caption was read, not the video itself.

## The team
| Role | Agent file | Writes to |
|------|-----------|-----------|
| Director (orchestrator, owns the result) | CLAUDE.md, the main session | brain/, campaign records |
| Strategy | web-strategist | brief/strategy.md |
| Structure and flows | ux-architect | design/sitemap.md, design/wireframes.md |
| Visual style and design system | ui-designer | references/design-dna.md, design/design-system.md, design/tokens.css |
| Page copy | web-copywriter | copy/<page>.md |
| SEO and accessibility spec | seo-a11y-specialist | design/seo-spec.md, design/a11y-spec.md |
| Build | frontend-developer | site/, exports/build-notes.md |
| Independent QA | web-qa-reviewer | qa/web_qa_report_<n>.md |
Reused existing agents: platform-researcher (reference and competitor research), fact-reviewer (copy claims, marine terms), art-director (only if custom graphics are needed), media-librarian (if Rahul supplies a photo folder).

## The seven steps (ADAPTED from the reel's caption; not the reel's own list)
The reel's seven steps were: desktop app, dedicated folder (raw / references / exports), one setup prompt, an outside API key for speech to text, teach style from 3+ reels, drop footage in raw, run one edit prompt. The list below keeps the idea and changes the details for web work.
1. Use Claude Code with this repo. Run bash scripts/web_setup_check.sh; it confirmed Node, Playwright and Chromium in the 2026-11-06 session and reports MISSING for anything absent in a fresh session. It installs nothing; installing needs Rahul's approval.
2. Make the project folder: bash scripts/web_new_project.sh <short-name>. It creates brief, inputs, references, research, design, copy, site, qa, exports.
3. No outside API key is needed for web work (the reel needed one for speech to text, so this step is dropped).
4. Teach the style: put 3 or more reference website URLs in references/reference-sites.md, or just paste them in the chat.
5. Drop inputs: logo already in assets/brand/. Photos and documents go in Google Drive; paste the link.
6. Run the kickoff prompt below.
7. Review the result, request changes. Publishing is a separate approval.

## Kickoff prompt (paste on iPhone, fill the brackets)
Build a website for [company or topic]. Goal: [main action, for example get quote requests]. Pages: [list or "you decide"]. References I like: [url 1] [url 2] [url 3]. Photos and files: [Drive link or "none yet"]. Run the full website team, QA it independently, and give me the preview steps. Do not publish anything.

## Pipeline the Director runs
1. git pull, read CLAUDE.md and brain/, scaffold the project, write brief/brief.md, list open questions.
2. web-strategist (and platform-researcher for references and competitors in parallel).
3. ux-architect first (sitemap, wireframes).
4. In parallel: seo-a11y-specialist pass 1 (a11y-spec), ui-designer (needs the reference sites), web-copywriter. Then seo-a11y-specialist pass 2 writes seo-spec.md from the copywriter's drafts (it is the single owner of titles and meta descriptions). fact-reviewer checks the copy.
5. frontend-developer builds site/ and runs scripts/web_qa.mjs itself.
6. web-qa-reviewer, a separate invocation, tests the build and writes the report.
7. Fix loop through frontend-developer, at most 2 QA cycles, then report what remains.
8. Retro, learning loop, guard script, commit, pull --rebase, push.

## Limits to know
- New agent files load when a session starts. Agents added mid-session are not launchable until the next session.
- Local QA is headless Chromium on Linux only. Not covered: real phones, Safari, Firefox, screen readers, real-user speed.
- Preview: the site is static, so it can be opened by serving site/ locally. A shareable preview link is a "make public or share" action and needs Rahul's approval.
- Publishing, domains, hosting, analytics, cookies and real form endpoints all need Rahul's approval.
- Repo visibility was reported public in brain/capabilities.md. Do not put confidential client content in site files until Rahul confirms visibility.
