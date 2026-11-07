# Brief: Sinor full website design (cinematic dark), version 1

Date: 2026-11-07
Rahul's words: "Make the full website design as per my request." Earlier requests in this chat: a website design and development team (done), three Pinterest samples as the style (dark cinematic 3D scroll sites), and "Use it as the first project" for his Sinor Marine Technologies artifact.
Type: a complete multi-page static website design and build, delivered as source in this repo. Not published. A NEW copy: Rahul's original private artifact is untouched.

## Decisions made by the Director (state each to Rahul)
1. Style: the cinematic dark style from campaigns/2026-11-style-cinematic-dark (design-dna.md, design/design-system.md, design/tokens.css). That study is the style source of truth. Dark navy stage, one luminous focal object, huge short headline, tiny nav, pill buttons, one glow.
2. No 3D or animation library (not approved). The "3D" moment is a canvas 2D scene drawn in plain JavaScript, linked to scroll, with a static fallback and a prefers-reduced-motion path. No video, no raster hero image. Everything text, SVG or canvas so the repo stays media-free.
3. Stack: plain HTML, CSS, vanilla JS, multi-page (real URLs, good for SEO and QA), shared css/ and js/ folders. System font stack, no Google Fonts, no external requests.
4. Company name: UNRESOLVED. Working name token is "Sinor Marine" with the legal entity line from brain/brand-profile.md ("Sinor Marine Services Middle East FZCO, UAE"), kept in ONE place so it can change. Rahul's private site says "Sinor Marine Technologies" and "Singapore"; that is NOT used here.
5. Facts allowed: ONLY brain/brand-profile.md items marked STATED or VERIFIED. The STATED industry focus is: marine and offshore technology, Dynamic Positioning, reference systems, marine electrical and automation, propulsion and thruster controls, integration, upgrades, commissioning, service, technical support. Label it as stated by Rahul, not independently verified.
6. NOT allowed anywhere: partner or dealership names, ISO or any certification, project names, client names, statistics, testimonials, years in business, phone numbers, email addresses, street addresses, product trademarks, any text taken from Rahul's private artifact. Missing content is shown as a visible slot marked NEEDED FROM RAHUL.
7. Logo: only assets/brand/sinor-logo.png (opaque white background), so it sits on a white plate on dark pages. The artifact's transparent logos are unconfirmed and not used.
8. Contact form is not connected to anything and says so in readable text (contrast at least 4.5 to 1 on dark).
9. Pages: Home, Solutions, Service and support, About, Contact. Training, Simulator, News, Team and Partners are not built because they depend on unconfirmed content; the sitemap notes where they would go.
10. Domain, canonical URLs and hosting are placeholders. Nothing is published or shared.

## Files to read (all agents)
brain/brand-profile.md, brain/verified-facts.md, brain/preferences.md, brain/lessons-learned.md, .claude/skills/website-build-standards/SKILL.md, this brief, and the style study files named above. DO NOT read /tmp/work/2026-11-sinor-site (Rahul's private site) or any file under campaigns/2026-11-sinor-site except nothing; keep this build independent of it.

## Open questions for Rahul (unchanged and still unanswered)
Company name and base; which facts (partners, ISO, contacts, product names) are confirmed for public use; whether the artifact logos are approved; whether the repo may stay public; hosting and publishing approval.
