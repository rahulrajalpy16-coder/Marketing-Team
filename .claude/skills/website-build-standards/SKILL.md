---
name: website-build-standards
description: Use before planning, designing, writing or coding any website. Defines the default stack, project folder layout, content and asset rules, and the quality gates with verified numbers.
---
# Website build standards

## Default stack (change only with a stated reason and Rahul's word)
Plain HTML, CSS and vanilla JS. No build step, no framework, no external CDN, font service, tracker or cookie. Reason: it previews anywhere, is fast, is easy to QA, and runs from a phone-driven cloud session. Escalate to a framework or CMS only if the brief needs login, shop, search or non-technical editing, and ask first.

## Project folder (create with scripts/web_new_project.sh <short-name>)
campaigns/<YYYY-MM-name>/
- brief/ brief.md, strategy.md
- inputs/ inputs.md (Drive links and a list of what Rahul supplied; never the raw files)
- references/ reference-sites.md (3 or more URLs Rahul likes), design-dna.md
- research/ competitor and fact-check notes
- design/ sitemap.md, wireframes.md, design-system.md, tokens.css, seo-spec.md, a11y-spec.md
- copy/ one file per page
- site/ the built website (text files, SVG, and small optimised images)
- qa/ web_qa_report_<n>.md, retro.md
- exports/ build-notes.md and delivery notes
Heavy work (screenshots, original images, bundles) goes in /tmp/work/<name>/, never in the repo.

## Repo size and media rules
Every file under 5 MB (guard script). Website images in site/assets/ must be optimised copies: each under 300 KB, total under 2 MB, plus SVG. Originals stay in Google Drive, read-only. No video files in the repo; link or host video elsewhere only with approval. Large deliverables are not committed.

## Content rules
- Only supplied or properly licensed images. No hotlinking. Alt text on every informative image, empty alt for decorative.
- No lorem ipsum in a deliverable. Missing content is marked NEEDED FROM RAHUL.
- No invented clients, logos, testimonials, statistics, certifications, awards, dealerships or project names. ISO claims stay out until brain/verified-facts.md records Rahul's confirmation.
- Contact forms are not connected to anything unless Rahul approves a real endpoint. Mark them clearly and report it.
- Legal pages (privacy, terms, cookies) need Rahul or legal sign-off; draft text is labelled DRAFT NOT LEGAL ADVICE.
- No em dashes in visible text or in messages to Rahul.

## Quality gates (verified 2026-11-06)
| Gate | Target | Source |
|------|--------|--------|
| LCP | 2.5 s or less | https://web.dev/articles/vitals |
| INP | 200 ms or less | https://web.dev/articles/vitals |
| CLS | 0.1 or less | https://web.dev/articles/cls |
| Text contrast | 4.5:1 normal, 3:1 large text (WCAG 2.2 SC 1.4.3, AA) | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html |
| Pointer target size | at least 24 by 24 CSS px (WCAG 2.2 SC 2.5.8, AA) | https://www.w3.org/TR/WCAG22/ |
Re-verify if this table is older than 90 days. Web.dev frames LCP, INP and CLS as field metrics at the 75th percentile of real visits. The local lab run in scripts/web_qa.mjs is indicative only, not proof.
Project-level gates (own rules, not external standards): total transfer per page under 1.5 MB, zero console errors, zero failed requests, zero broken internal links, no horizontal scroll at 375, 768 and 1440 px wide, exactly one h1 per page.

## Order of work
Strategy, then ux-architect (sitemap and wireframes), then in parallel: seo-a11y-specialist pass 1 (a11y-spec), ui-designer (design system) and web-copywriter. Then seo-a11y-specialist pass 2 (seo-spec, the single owner of titles and meta descriptions, starting from the copywriter's drafts), fact check of copy, build, independent QA, fix loop (maximum 2 QA cycles before reporting remaining issues), handoff. Publishing, domains and hosting are never done without Rahul's approval.
