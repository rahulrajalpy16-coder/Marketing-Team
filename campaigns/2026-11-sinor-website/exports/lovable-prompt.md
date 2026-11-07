# Lovable prompt: Sinor marine website, cinematic dark (v1)

How to use: open a new Lovable project, attach the logo file (assets/brand/sinor-logo.png from the repo) and screenshots of the three reference pins if you can, then paste everything inside the box below as the first message. The copy in it is DRAFT built only from facts Rahul stated. It will be replaced by the reviewed copy from the website team. Nothing here has been published.

```
Build a complete 5-page marketing website for a marine and offshore technology company. Follow every rule below exactly. Do not add anything I did not ask for.

COMPANY (use only this)
- Name: Sinor Marine Services Middle East FZCO, based in the UAE. Keep the company name in ONE constant in the code so I can change it later.
- What the company does (as stated by the owner, not independently verified): marine and offshore technology, Dynamic Positioning, reference systems, marine electrical and automation, propulsion and thruster controls, integration, upgrades, commissioning, service, technical support.
- LinkedIn page (link in footer and contact page): https://www.linkedin.com/company/sinor-marine-services/
- Logo: use the logo file I attach. It has an opaque white background, so ALWAYS place it on a white rounded plate (radius 8px, padding 6px 10px) on dark pages. Never recolor, stretch or redraw it. Until I attach it, show a white plate with the text "LOGO".

HARD CONTENT RULES (important, you tend to break these)
- Do NOT invent anything: no partner or client names, no certifications or ISO numbers, no statistics, no years in business, no project names, no testimonials, no awards, no team members, no phone numbers, no email addresses, no street address, no product trademarks, no stock claims like "trusted by" or "industry leading".
- Where real content is missing, show a visible dashed-border slot box with the label "NEEDED FROM OWNER" and one line saying what goes there. Slots needed: contact email, phone, address, opening hours, partners, certifications, projects, team, company story, photos.
- No lorem ipsum. No emoji. No em dashes or en dashes anywhere in the text; use commas or full stops.
- Use exactly the draft copy below. Do not rewrite it.

STACK AND LIMITS
- React, TypeScript, Tailwind. Five routes: / (Home), /solutions, /service (Service and support), /about, /contact. A 404 page with the same header and footer.
- No backend, no database, no Supabase, no authentication, no analytics, no cookies, no tracking, no external fonts, no CDN requests. System font stacks only.
- No 3D libraries and no animation libraries (no three.js, no GSAP, no Lenis, no framer-motion). The hero scene is a plain HTML canvas drawn with JavaScript, described below.
- No video and no raster hero images. Visuals are canvas, inline SVG and CSS only.
- The contact form must not send anywhere. It validates on the client and then shows the message in the NOT CONNECTED notice below. Never claim a message was sent.

LOOK (cinematic dark). References for the mood only, never copy their text, images or layouts:
1. https://pin.it/6mizOnKak  (scroll-driven landing page: black stage, one glowing launch scene, large serif headline, small white pill button, tiny uppercase nav; source site https://scrollytelling.ai/)
2. https://pin.it/7pXE3pxNY  (3D scroll animation: near-black stage, one rendered object lit by a coloured diagonal beam, large light headline, small pill buttons, a small floating info card; source gallery https://www.details.so/inspo/flowty-f0ddcc)
3. https://pin.it/1skTsyhdi  (3D website on black starfield: one luminous particle object, tall headline, tiny top-right nav)
What all three share, and what to build: a near-black stage, ONE luminous focal object carrying all the colour, a huge short headline, tiny quiet nav, small pill buttons, one soft glow of a single colour, lots of empty space, short supporting copy.

Design tokens (use these exact values as CSS variables):
- Surfaces: abyss #050A12, deep #0A1626, surface #101F33, raise #16293F
- Text: #F2F6FA, muted #A9B8C9, faint #8497AD (only at 16px or larger)
- Accents: #5BA4E0, accent-hi #8CC4F2, steel #7F9BB8, warm glow #F2A65A (use very sparingly, optional)
- Focus ring: 2px #8CC4F2 with 3px offset on every interactive element, never removed
- Control border: #6A86A5. Hairlines: #2A4260 (decorative only)
- Brand navy #0D4A85 must never be used as text or icons on dark backgrounds
- Minimum text contrast 4.5:1 (3:1 for large text). The "not connected" notice and all small print must use muted #A9B8C9 or lighter on dark.
- Fonts: display serif stack "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif for headlines; system-ui for everything else. Body 16 to 18px, line height 1.6. Labels 13px uppercase, letter spacing 0.14em, weight 600. Hero headline clamp(2.75rem, 1.4rem + 6.8vw, 7.5rem), line height 1.02, tracking -0.025em, max 14 characters wide on a 375px phone.
- Radii 8, 14, 24 and pill. Spacing on a 4px base. Max content width 1200px, text width 62ch, section padding clamp(64px, 12vw, 144px).
- Primary pill button: height 48px, padding 0 28px, background #F2F6FA, text #050A12, 13px uppercase, tracking 0.12em, weight 600. Hover: background #FFFFFF and lift 1px. Secondary: transparent with 1px #6A86A5 border and #F2F6FA text.
- Cards: background #101F33, radius 14, padding 24, soft shadow, body text muted.
- Header: 64px, uppercase 13px links in muted colour, active link underlined, one pill "Contact" on the right. Transparent over the hero with a dark gradient behind, solid #0A1626 after scrolling 40px. On screens under 1024px the links collapse into a "Menu" button that toggles a full-width panel (aria-expanded, 44px rows, Escape closes and returns focus).
- Footer: background #050A12, logo plate, links, LinkedIn link, line "Sinor Marine Services Middle East FZCO, UAE".

HOME HERO (the one cinematic moment)
- A tall scroll runway (400vh) with a sticky full-viewport stage. Inside it, a canvas that redraws from scroll progress p (0 to 1). Headline and buttons are real HTML text over the canvas, never drawn on it.
- Scene: navy-black field with a few faint static stars. The focal object is an offshore support vessel drawn as luminous line art (side view, bow to the right, hull, bridge block, mast, crane) in #8CC4F2 with a soft glow, plus a station-keeping ring (dashed ellipse) around it.
- Storyboard: p=0 vessel small and calm, faint ring, headline visible. p=0.33 camera moves in, vessel larger, two dashed rings expand. p=0.66 the view tilts to a plan view: compass ticks around a ring, crosshair, vessel outline from above, a trail that wanders slightly and returns to the centre. p=1 plan view settles with a "set point" label; the second caption appears.
- Fallbacks: if JavaScript is off or the user prefers reduced motion, show one static composition (the p=0.66 plan view) with no scroll linkage. Add a "Skip animation" link before the runway. Animate only transform and opacity where CSS is used, keep the scroll handler light (requestAnimationFrame, passive listener), and keep layout shift at zero.

DRAFT COPY (use exactly)

HOME
- Label: MARINE AND OFFSHORE TECHNOLOGY
- H1: Dynamic positioning and marine control.
- Support line: Dynamic Positioning, reference systems, marine electrical and automation, propulsion and thruster controls.
- Buttons: "Discuss a project" (to /contact), "See solutions" (secondary, to /solutions)
- Second caption at the end of the runway: Systems for vessels that need to stay exactly where they are.
- Section "What we work on" (six cards, each links to /solutions#anchor):
  1. Dynamic Positioning: Systems that keep a vessel on position and heading.
  2. Reference systems: The position and heading inputs that Dynamic Positioning relies on.
  3. Marine electrical and automation: Power, control and monitoring for vessel systems.
  4. Propulsion and thruster controls: Control of the thrusters and propellers that move and hold the vessel.
  5. Integration, upgrades and commissioning: Bringing systems together, updating existing installations and bringing them into service.
  6. Service and technical support: Help for systems that are already in operation.
- Section "How a project runs": four steps with only these words: Discover. Design. Install and commission. Support. One short generic line each, no durations and no numbers.
- Service strip: "Already in operation? Request service or technical support." button to /contact?topic=service-support.
- About teaser: "Sinor Marine Services Middle East FZCO is a marine and offshore technology company based in the UAE." plus a slot box for the company story, and a link "About us".
- Closing band: "Tell us about your vessel or project." button "Start an enquiry".

SOLUTIONS
- H1: Solutions. Intro: "Six areas of work. Choose the system you are working on."
- One section per focus area above (give each an id: dp, reference, electrical, propulsion, integration, service). Each shows the one-line description, a slot box "Scope, system types and named products: NEEDED FROM OWNER", and a button "Discuss this system" to /contact?topic=<id>.

SERVICE AND SUPPORT
- H1: Service and support. Intro: "Support for systems after they enter service, including commissioning, upgrades and technical support."
- Slot boxes: hours, emergency route, coverage area, response commitment (all NEEDED FROM OWNER). Button "Request support" to /contact?topic=service.

ABOUT
- H1: About. Text: "Sinor Marine Services Middle East FZCO is a marine and offshore technology company based in the UAE. Its work covers Dynamic Positioning, reference systems, marine electrical and automation, propulsion and thruster controls, integration, upgrades, commissioning, service and technical support."
- Slot boxes: company story, year founded, team, certifications, partners, regions served. Button "Contact the team".

CONTACT
- H1: Contact. Intro: "Tell us what you are working on."
- Form fields with visible labels and ids: Full name, Company, Email, Topic (select: Dynamic Positioning, Reference systems, Marine electrical and automation, Propulsion and thruster controls, Integration upgrades and commissioning, Service and technical support, General enquiry; preselect from the ?topic= query value), Vessel or project (optional), Message. Required: name, email, message. Inline error text under each field in a readable light red (check 4.5:1 on #0A1626). Submit button "Send enquiry".
- Directly under the button, always visible, in muted #A9B8C9 at 15px or larger: "This form is not connected yet. Nothing you type is sent anywhere." After a valid submit show: "Your enquiry is ready, but nothing has been sent because this form is not connected yet."
- Slot boxes: email, phone, address, opening hours (NEEDED FROM OWNER). LinkedIn link.

ACCESSIBILITY AND QUALITY
- Semantic landmarks (header, nav, main, footer), one h1 per page, no skipped heading levels, a skip-to-content link, visible focus, all tap targets at least 44px, every image or canvas has an accessible name or aria-hidden, set a unique document title and meta description per page (plain descriptive text from the copy above).
- Mobile first. Check 375px, 768px and 1440px: no horizontal scroll, no clipped text.
- Respect prefers-reduced-motion everywhere. Nothing may flash.
- Keep the first load light: no large assets, no external requests.

When done, list anything you could not do and any rule you had to bend.
```

## What to attach in Lovable
1. The logo: assets/brand/sinor-logo.png.
2. Optional: screenshots of the three Pinterest pins (open each link, save the image). They are the mood only.

## Known differences from the team's own build
The team's build is plain HTML, CSS and JavaScript in this repo. Lovable will produce React. The hero storyboard in this prompt is a simplified version; the team's wireframes may differ in detail. Draft copy here will be replaced by reviewed copy.
