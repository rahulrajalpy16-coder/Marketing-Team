# Build notes: Sinor Marine Technologies website v1

Date: 2026-11-07. Builder: frontend-developer. Nothing published, nothing shared.

## What was built (campaigns/2026-11-sinor-website/site/, 152 KB, no images, no fonts)
index.html, solutions.html, service.html, about.html, contact.html, 404.html, css/tokens.css (copied unchanged), css/site.css, js/hero.js, js/site.js, robots.txt, sitemap.xml.
- Home hero: sticky scroll-linked canvas (plain JS, rAF, one passive scroll listener, one resize listener), vessel as line art in plan view, station-keeping ring, 4 beats, static inline SVG for no JS, reduced motion, short or narrow viewports. Canvas aria-hidden, all text is DOM text. "Skip the animation" link exists in the tab order only while the scene is live. Top-weighted scrim in site.css (tokens.css untouched).
- Header: Menu button (label always "Menu", aria-expanded, Escape closes and returns focus), inline links from 1024 px, skip link, text wordmark, slot S29. Footer with slots S29, S30, S23, S31, S01 to S04, S05.
- Contact: seven fields, per-field and summary errors, focus to summary on failed submit and to "Not sent" panel on valid submit, ?topic= preselect, NOT CONNECTED notice (text colour on raise, 13.6 to 1). No endpoint; nothing is sent.
- SEO: titles, descriptions, canonical, OG, Twitter, JSON-LD (Home, 4 keys) exactly per seo-spec.md; noindex, nofollow on every page; robots.txt Disallow all; no og:image.

## Not wired (report to Director)
- Contact form: not connected (slot S27). Remove the notice, the meta/OG/Twitter sentence "The form is not connected yet; see other routes." and the no-JS note in the same change that connects it.
- All slots (S01 to S26, S28 to S31) are visible dashed boxes. No logo, LinkedIn link, contact details, legal pages, favicon.
- Domain is https://DOMAIN.example everywhere. Launch flip: robots meta to "index, follow" (404: "noindex, follow"), robots.txt to Allow plus Sitemap line.

## Preview
cd campaigns/2026-11-sinor-website/site && python3 -m http.server 8000, open http://localhost:8000/ . Open the site root (404.html uses root-absolute paths).

## Deviations and decisions to confirm
1. Header is solid and sticky (not transparent over the hero). The hero stage sits below it. S29 slot is a thin strip above the bar that scrolls away; the 64 px bar stays.
2. Home h1 and section h2 text follow copy/home.md ("Dynamic Positioning and marine control", "Areas of work", "What the work includes"), not the older outline in seo-spec.md ("Hold position at sea", "What Sinor Marine Technologies does", "How work flows"). Service h2 also follows copy. Director to confirm.
3. Hero vessel is placed in the space left under the text (measured from the DOM), not fixed at the lower 45 percent. On narrow screens that is the lower part; on 1024 px and wider it sits right of the text. If less than about 52 px of ring radius fits, the page falls back to the static composition.
4. Static path below 360 px width or 560 px height, and when reduced motion is set; also toggles live if the media state changes. An inline head script adds the `js` and `hero-live` classes before first paint to avoid layout shift. If hero.js fails to load, the hero shows text but no art.
5. Caption list has aria-label "Scene captions" (not in copy; not visible). UI labels use 14 px (token --fs-label is 13 px).
6. Copy author notes and the copy "open state text: Close" for Menu were not used (build-decisions item 4).
7. Slot descriptions were trimmed to "what goes there"; instruction sentences were dropped. S27 and S07 are not shown. S30 is not repeated in the Home teaser. Closing-band LinkedIn links are omitted until S31 is supplied.
8. Copyright line "2026" is fixed text.
9. Topic select keeps the copy order and preselects by value.
10. sitemap.xml contains the standard sitemaps.org namespace URL (not a request).

## QA (scripts/web_qa.mjs, 2026-11-07): 0 FAIL, 0 WARN, 6 NOTE (favicon missing, expected)
Also tested by hand with Playwright: hero beats at 375 and 1440, reduced motion, no JS, short viewport, menu open and Escape, form fail and valid paths, skip-animation reachable by Tab, 404 renders. Greps for FZCO, UAE, Middle East, Marine Services, sinor-logo, lorem, em or en dashes, external URLs: all clean.
NOT tested: screen readers, real devices, Safari, Firefox, forced colours, hero contrast over real canvas pixels (M6), 200 percent zoom by hand, 320 px width.

## Open issues
- Validation on blur can remove an error message and shift the button upward between mouse down and up; a click right after fixing a field may need a second press. Consider reserving space or validating only on submit and change.
- Hero text over canvas at beat 3 was not measured pixel by pixel.
- The generator used to write the pages is not in the repo; files are plain and hand-editable.

## Candidate lessons
- A hero with inline head classes avoids layout shift but needs a script-failure path; test it.
- Blur validation that removes messages can swallow the next click; test with a real pointer.
- Strict QA contrast checks skip background images: keep text on flat colours where possible.

## Fix pass 1 (after web_qa_report_1)
- W1: blur and change checks are skipped while a pointer is pressed on Send enquiry, so nothing can move between mouse down and mouse up. Playwright (real mouse down and up, fail, fix, one click) at 1440 and 375: button moved 0 px, "Not sent" panel shown, focus on it.
- W2: page-intro buttons are content width (service.html and every other pill checked at 1440 and 375; none stretch outside bands and hero rows). .actions no longer stretches items.
- Home "After the system is in service": the three outlined boxes are now a plain bullet list (nothing non-interactive looks clickable).
- Contact: two columns only from 1024 px, with a larger gap and a 300 px minimum right column, so "Other ways to reach the team" wraps cleanly.
- New draft slots (dashed box, label "DRAFT, NEEDS RAHUL TO CONFIRM"): S32 "Project steps are a proposal, not confirmed" (Home and About, after the step list); S33 "Confirm these areas apply to Sinor Marine Technologies" (Home and About beside the "Industry focus as stated by the company" label; Solutions above the jump list). Step and area text unchanged. Slot list is now S01 to S26, S28 to S33 visible (S27 and S07 are build-note only).
- web_qa: 0 FAIL, 0 WARN, 6 NOTE (favicon). Greps clean.
