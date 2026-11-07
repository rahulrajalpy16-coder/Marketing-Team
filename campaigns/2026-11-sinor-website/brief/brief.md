# Brief: Sinor full website design (cinematic dark), version 1

Date: 2026-11-07
Rahul's words: "Make the full website design as per my request." Earlier requests in this chat: a website design and development team (done), three Pinterest samples as the style (dark cinematic 3D scroll sites), and "Use it as the first project" for his Sinor Marine Technologies artifact.
Type: a complete multi-page static website design and build, delivered as source in this repo. Not published. A NEW copy: Rahul's original private artifact is untouched.

## Decisions made by the Director (state each to Rahul)
1. Style: the cinematic dark style from campaigns/2026-11-style-cinematic-dark (design-dna.md, design/design-system.md, design/tokens.css). That study is the style source of truth. Dark navy stage, one luminous focal object, huge short headline, tiny nav, pill buttons, one glow.
2. No 3D or animation library (not approved). The "3D" moment is a canvas 2D scene drawn in plain JavaScript, linked to scroll, with a static fallback and a prefers-reduced-motion path. No video, no raster hero image. Everything text, SVG or canvas so the repo stays media-free.
3. Stack: plain HTML, CSS, vanilla JS, multi-page (real URLs, good for SEO and QA), shared css/ and js/ folders. System font stack, no Google Fonts, no external requests.
4. Company name: Sinor Marine Technologies (STATED by Rahul 2026-11-07: "This is for sinor marine technologies. Not services"). Kept in ONE place. Base (UAE or Singapore) and legal entity are UNKNOWN: slots S23 and S30. The Sinor Marine Services Middle East FZCO identifiers (entity line, UAE, LinkedIn page, repo logo) are NOT used on this site.
5. Facts allowed: ONLY brain/brand-profile.md items marked STATED or VERIFIED. The STATED industry focus is: marine and offshore technology, Dynamic Positioning, reference systems, marine electrical and automation, propulsion and thruster controls, integration, upgrades, commissioning, service, technical support. Label it as stated by Rahul, not independently verified.
6. NOT allowed anywhere: partner or dealership names, ISO or any certification, project names, client names, statistics, testimonials, years in business, phone numbers, email addresses, street addresses, product trademarks, any text taken from Rahul's private artifact. Missing content is shown as a visible slot marked NEEDED FROM RAHUL.
7. Logo: assets/brand/sinor-logo.png reads SINOR MARINE SERVICES MIDDLE EAST FZCO, so it belongs to the Services company and is NOT used. The header shows a text wordmark "SINOR MARINE TECHNOLOGIES" plus slot S29 until Rahul supplies the official Sinor Marine Technologies logo. The artifact's logos are unconfirmed and not used. A supplied logo with an opaque white background sits on a white plate; a transparent one is checked on #0A1626 first.
11. The six STATED focus areas were given for Rahul's employer. Treat the sentence that lists them as CLAIM TO VERIFY until Rahul confirms it applies to Sinor Marine Technologies.
12. LinkedIn: the STATED page (sinor-marine-services) is the Services company page and is NOT linked. Slot S31 until the Technologies page is supplied.
8. Contact form is not connected to anything and says so in readable text (contrast at least 4.5 to 1 on dark).
9. Pages: Home, Solutions, Service and support, About, Contact. Training, Simulator, News, Team and Partners are not built because they depend on unconfirmed content; the sitemap notes where they would go.
10. Domain, canonical URLs and hosting are placeholders. Nothing is published or shared.

## Files to read (all agents)
brain/brand-profile.md, brain/verified-facts.md, brain/preferences.md, brain/lessons-learned.md, .claude/skills/website-build-standards/SKILL.md, this brief, and the style study files named above. DO NOT read /tmp/work/2026-11-sinor-site (Rahul's private site) or any file under campaigns/2026-11-sinor-site except nothing; keep this build independent of it.

## Open questions for Rahul (unchanged and still unanswered)
Company name and base; which facts (partners, ISO, contacts, product names) are confirmed for public use; whether the artifact logos are approved; whether the repo may stay public; hosting and publishing approval.
