# Copy: Home (index.html)

Author: web-copywriter. Date: 2026-11-07. Status: draft. seo-a11y-specialist finalises title and meta in design/seo-spec.md, which wins.
Sources: brain/brand-profile.md (STATED items only), brain/verified-facts.md, marine-technical-accuracy skill, brief, strategy, sitemap, wireframes.
Company name token: "Sinor Marine" (working name, UNRESOLVED, see brief decision 4). Legal line: "Sinor Marine Services Middle East FZCO, UAE" (STATED).
Marker rule: CLAIM TO VERIFY = the sentence depends on Rahul's STATED industry focus (not independently verified) or on a technical definition for fact-reviewer.

## Title and meta
- Title: Sinor Marine | Dynamic Positioning and Marine Technology (56 characters, counted by hand)
- Meta description: Sinor Marine covers Dynamic Positioning, reference systems, marine electrical and automation, propulsion and thruster controls, service and support. (148 characters, counted by hand)
- CLAIM TO VERIFY: the meta description states the scope. Source: STATED by Rahul 2026-11-06, not independently verified.

## Shared parts (same text on every page; defined once here)

Skip link: Skip to main content
Header logo link accessible name: Sinor Marine, home
Logo image alt (inside the link, on the white plate): Sinor Marine Services Middle East FZCO logo
Nav labels in order: Home | Solutions | Service and support | About | Contact
Menu button: Menu (open state text: Close)
Header pill and menu panel pill: Send an enquiry

Footer
- Logo alt: Sinor Marine Services Middle East FZCO logo
- Legal entity line: Sinor Marine Services Middle East FZCO, UAE
- Group heading: Pages (links: Home, Solutions, Service and support, About, Contact)
- Group heading: Find us
  - Link text: Company LinkedIn page (visible extra text: opens linkedin.com). URL: https://www.linkedin.com/company/sinor-marine-services/
  - SLOT S01 | NEEDED FROM RAHUL | Public email address for the footer and Contact page.
  - SLOT S02 | NEEDED FROM RAHUL | Public phone number.
  - SLOT S03 | NEEDED FROM RAHUL | Public address.
  - SLOT S04 | NEEDED FROM RAHUL | Opening hours and time zone.
- SLOT S05 | NEEDED FROM RAHUL | Decision on privacy, cookie and terms pages, or approval to launch without them.
- Stated-scope line (14 px or larger): Industry focus as stated by the company, not independently verified.
- Copyright line: the builder adds the year. No founding year is shown.

404 draft (utility file, Director to confirm it is wanted)
- Title: Page not found | Sinor Marine (31 characters, utility page, below the 50 target by design)
- H1: Page not found
- Line: The page you asked for does not exist or has moved.
- Primary button: Back to home
- Text link: Send an enquiry

## Hero (section id="hero")

H1 (4 words): Hold position at sea
- Alternates for Rahul: "Marine technology, supported" (3 words); "Systems that hold position" (4 words).
- CLAIM TO VERIFY: the headline refers to Dynamic Positioning, a STATED focus area. It describes what DP does, not a Sinor claim of performance.

Support line (max 2 lines at 375 px): Marine and offshore technology, from Dynamic Positioning to service and support.
- CLAIM TO VERIFY: scope is STATED by Rahul.

Buttons
- Primary: Send an enquiry (contact.html)
- Secondary: See solutions (solutions.html)

Scroll cue (hidden when reduced motion, no JS, or after p exceeds 0.05): Scroll

Beat captions (ordered list of four, one line each, real DOM text, topics match storyboard 2.1.1)
1. Dynamic Positioning: a vessel holds its position and heading with its own thrusters.
2. Reference systems: the position measurements the vessel is held against.
3. Marine electrical and automation, propulsion and thruster controls.
4. Integration, commissioning and service: the whole system, supported.
- Technical note for fact-reviewer: caption 1 follows the generic definition of DP (automatic control of position and heading using the vessel's thrust). Check against IMO MSC.1/Circ.1580 wording. It says nothing about DP class, accuracy or any product. Caption 2 says reference systems give position measurements; it does not rank or interchange types.
- CLAIM TO VERIFY: captions 3 and 4 list STATED areas.

Canvas and SVG alternative text
- Canvas: aria-hidden="true", no alt text. It is decorative; the four captions carry the meaning.
- Static SVG fallback: aria-hidden="true", no alt text. If the designer prefers role="img" instead, use this: "Line drawing of a vessel inside a circular ring with four reference points." Recommendation: keep it hidden, to avoid repeating the captions.

## 2.2 What the company does (id for jump if needed: what-we-do)

H2: What Sinor does
Label above list: Industry focus as stated by the company
Intro line: Six areas of marine and offshore technology, from positioning to upgrades.
- CLAIM TO VERIFY: all six areas come from the STATED scope line. "Upgrades" as a sixth area is a Director proposal (sitemap section 5).

Area list (each row links to solutions.html#<id>; the arrow glyph is aria-hidden)
1. Dynamic Positioning (dynamic-positioning): Systems that hold a vessel's position and heading automatically.
2. Reference systems (reference-systems): The position measurements a DP system relies on.
3. Marine electrical and automation (electrical-automation): Electrical and control systems on board vessels and offshore units.
4. Propulsion and thruster controls (propulsion-thrusters): Controls for the units that move and position a vessel.
5. Integration (integration): Bringing separate vessel systems together to work as one.
6. Upgrades (upgrades): Bringing existing systems up to date.
- Write "Dynamic Positioning" in full in row 1 and "DP" in row 2 (first use on the page is the hero, so "DP" is already defined by row 1).

Text link below the list: See all solutions

SLOT S06 | NEEDED FROM RAHUL | One-line scope per area at the depth Rahul approves. It replaces the generic lines above.
SLOT S28 | NEEDED FROM RAHUL | One differentiator line: what makes Sinor different. Nothing is written until Rahul supplies it.

## 2.3 How work flows

H2: How work flows
Intro line: Work does not stop at supply. It follows the system through its life on board.
Steps (ordered list, h3 each, no numerals printed)
1. Discover: Understand the vessel, the system and what the operator needs.
2. Design: Plan the solution and how it fits the systems already on board.
3. Install and commission: Fit the equipment and bring it into service on the vessel.
4. Support: Keep the system working after handover, with service and technical support.
- CLAIM TO VERIFY: Commissioning, service and technical support are STATED. "Discover" and "Design" as named steps, and the order of steps, are wireframe proposals and are NOT stated by Rahul. Confirm that this describes how Sinor actually works, or reduce to the stated words.
Text link under the list: Service and support

## 2.4 Service strip

H2: After the system is in service
Line: Commissioning, service and technical support for marine and offshore systems.
- CLAIM TO VERIFY: STATED scope.
Three items (name only): Commissioning | Service | Technical support
Secondary pill: Service and support (service.html)

## 2.5 Credibility strip (slots only; whole section removed at publish if empty)

H2: Credentials and references
Line shown in draft: Nothing appears here until each item is confirmed.
SLOT S08 | NEEDED FROM RAHUL | Certifications: certificate numbers and issuing body. No ISO text is shown until confirmed.
SLOT S09 | NEEDED FROM RAHUL | Partners and authorisations: each name with written approval to display it.
SLOT S10 | NEEDED FROM RAHUL | Selected projects: names only if Rahul permits.
SLOT S11 | NEEDED FROM RAHUL | Company numbers: only figures Rahul confirms for public use (the stand panel figures are NOT used).

## 2.6 About teaser

H2: About the company
Sentence 1: Sinor Marine Services Middle East FZCO, UAE.
Sentence 2: The company works in marine and offshore technology, including Dynamic Positioning, reference systems, marine electrical and automation, and propulsion and thruster controls.
- CLAIM TO VERIFY: entity line and scope are STATED, not independently verified.
Text link: About the company (about.html)
SLOT S12 | NEEDED FROM RAHUL | Real company photo with rights confirmed, as an optimised copy. If it stays empty the section is text only.
Photo alt text when supplied: NEEDED FROM RAHUL, describe what the photo actually shows.

## 2.7 Closing enquiry band

Line: Tell the team what you need.
Primary pill: Send an enquiry (contact.html)
Secondary text link: Company LinkedIn page (opens linkedin.com)
Optional second line (Home only): Or read about the company. (links to about.html)
