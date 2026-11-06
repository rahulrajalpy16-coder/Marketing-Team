---
name: website-qa-checklist
description: Use to independently test a built website in a real browser against the build standards. Runnable procedure for the web-qa-reviewer.
---
# Website QA checklist

Run each step on the actual files. Record the command and result. State exactly what was and was not tested.

1. Setup: bash scripts/web_setup_check.sh (confirms node, Playwright and Chromium).
2. Automated run: node scripts/web_qa.mjs campaigns/<name>/site /tmp/work/<name>/qa. Screenshots and JSON go to /tmp/work on purpose (media stays out of the repo); only your written report goes in qa/. It serves the site locally, crawls internal links, tests each page at 375, 768 and 1440 px wide, and writes report.md, report.json and screenshots to the output folder. Exit code 1 means at least one FAIL.
3. Read report.md fully. Every FAIL becomes a defect with an ID.
4. Look at the screenshots (use the Read tool on the PNGs): overlap, clipped text, broken images, unreadable text, logo distortion, awkward spacing, sticky header covering content.
5. Copy check: compare rendered body text with campaigns/<name>/copy/*.md, and titles and meta descriptions with design/seo-spec.md. Flag any difference, any lorem ipsum, any claim not in brain/verified-facts.md, any em dash.
6. Network check: confirm the report shows zero external requests (no CDN, fonts, trackers). Any external request is a WARN unless the brief approved it.
7. Forms: labelled, errors readable, and clearly marked not connected unless an endpoint was approved.
8. SEO basics from the report: title, meta description, canonical, h1, lang, viewport, Open Graph. Compare with design/seo-spec.md.
9. Write campaigns/<name>/qa/web_qa_report_<n>.md: defects (ID, severity, page, location, owner), what was verified, what was NOT verified.

## True scope statement (always include)
Headless Chromium on Linux only. Not tested: real iPhone or Android devices, Safari or Firefox rendering, screen readers, a full manual WCAG audit, real-user performance, hosting or HTTPS behaviour. Lab LCP and CLS from the script are local, unthrottled and indicative only.

Never report a check that was not run. If independence was not possible, write "self-reviewed".
