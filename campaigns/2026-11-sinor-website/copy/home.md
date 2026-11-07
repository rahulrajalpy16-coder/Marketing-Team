# Copy: Home (index.html)

Author: web-copywriter. Date: 2026-11-07. Status: draft, correction pass 2 applied (fact_check.md). Titles and meta are owned by design/seo-spec.md and were not changed in this pass.
Sources: brain/brand-profile.md (STATED items only), brain/verified-facts.md, marine-technical-accuracy skill, brief, strategy, sitemap, wireframes, research/fact_check.md.
Company name: Sinor Marine Technologies (STATED by Rahul 2026-11-07). Legal entity and base are UNKNOWN, so they are slots (S30, S23). No legal suffix, region or other-company name appears in visitor text.
Marker rule: CLAIM TO VERIFY = the sentence depends on the STATED industry focus. Rahul gave that focus list for his employer; confirm it applies to Sinor Marine Technologies (fact_check Q1). Also used for technical definitions.
Scope rule: copy never says the company sells or fits equipment. Stated focus only: integration, upgrades, commissioning, service, technical support.

## Title and meta
- Title: Sinor Marine Technologies | Marine and Offshore Technology (58 characters, counted by hand)
- Meta description: Sinor Marine Technologies: Dynamic Positioning, reference systems, marine electrical and automation, propulsion and thruster controls, service. (143 characters, counted by hand)
- CLAIM TO VERIFY: the meta description states the scope. Source: STATED by Rahul 2026-11-06 for his employer; confirm it applies to Sinor Marine Technologies.

## Shared parts (same text on every page; defined once here)

Skip link: Skip to main content
Header brand link accessible name: Sinor Marine Technologies, home
Header brand: text wordmark "Sinor Marine Technologies" until the logo is provided. Do not use the old logo file in assets/brand (it names a different company).
SLOT S29 | NEEDED FROM RAHUL | Official Sinor Marine Technologies logo, with approval to use it. Alt text when provided: "Sinor Marine Technologies logo".
Nav labels in order: Home | Solutions | Service and support | About | Contact
Menu button: Menu (open state text: Close)
Header pill and menu panel pill: Send an enquiry

Footer
- Brand: text wordmark "Sinor Marine Technologies" (logo per S29 when provided).
- Company line: Sinor Marine Technologies
- SLOT S30 | NEEDED FROM RAHUL | Legal entity name and registration for Sinor Marine Technologies.
- SLOT S23 | NEEDED FROM RAHUL | Base and offices.
- Group heading: Pages (links: Home, Solutions, Service and support, About, Contact)
- Group heading: Find us
  - SLOT S31 | NEEDED FROM RAHUL | Sinor Marine Technologies LinkedIn page address. The page of the other company must not be used. Link text will be "LinkedIn page" with visible extra text "opens linkedin.com".
  - SLOT S01 | NEEDED FROM RAHUL | Public email address.
  - SLOT S02 | NEEDED FROM RAHUL | Public phone number.
  - SLOT S03 | NEEDED FROM RAHUL | Public address.
  - SLOT S04 | NEEDED FROM RAHUL | Opening hours and time zone.
- SLOT S05 | NEEDED FROM RAHUL | Decision on privacy, cookie and terms pages, or approval to launch without them.
- Stated-scope line (14 px or larger): Industry focus as stated by the company, not independently verified.
- CLAIM TO VERIFY: this line attributes the focus to Sinor Marine Technologies, but Rahul gave it for his employer. Remove once fact_check Q1 is answered; not suitable as final public copy.
- Copyright line: the builder adds the year. No founding year is shown.

404 draft (utility file, Director to confirm it is wanted)
- Title: Page not found | Sinor Marine Technologies (42 characters, utility page, below the 50 target by design)
- H1: Page not found
- Line: The page you asked for does not exist or has moved.
- Primary button: Back to home
- Text link: Send an enquiry

## Hero (section id="hero")

H1 (5 words): Dynamic Positioning and marine control
- Alternate for Rahul (descriptive): "Marine and offshore technology" (4 words); "Marine technology, supported" (3 words).
- CLAIM TO VERIFY: names a STATED focus area (Dynamic Positioning). It describes the field, not an outcome the company promises. "Marine control" is a loose umbrella for the stated automation and thruster control areas; confirm Rahul is comfortable with it.

Support line (max 2 lines at 375 px): Marine and offshore technology, from Dynamic Positioning to service and support.
- CLAIM TO VERIFY: scope is STATED for Rahul's employer; confirm for Sinor Marine Technologies.

Buttons
- Primary: Send an enquiry (contact.html)
- Secondary: See solutions (solutions.html)

Scroll cue (hidden when reduced motion, no JS, or after p exceeds 0.05): Scroll

Beat captions (ordered list of four, one line each, real DOM text)
1. Dynamic Positioning: automatic control of a vessel's position and/or heading using its thrusters.
2. Reference systems: the position measurements a DP system relies on.
3. Marine electrical and automation, propulsion and thruster controls.
4. Integration, commissioning, service and technical support.
- Technical note: caption 1 follows the fact-reviewer's neutral wording of the IMO MSC.1/Circ.1580 definition ("position and/or heading"). Primary text not read by the reviewer (fact_check A1), so keep CLAIM TO VERIFY. No DP class, accuracy or product is mentioned.
- CLAIM TO VERIFY: captions 3 and 4 list STATED areas and say nothing about outcomes.

Canvas and SVG alternative text
- Canvas: aria-hidden="true", no alt text. Decorative; the four captions carry the meaning.
- Static SVG fallback: aria-hidden="true", no alt text. If the designer prefers role="img", use: "Line drawing of a vessel inside a circular ring with four reference points." Recommendation: keep it hidden to avoid repeating the captions.

## 2.2 Areas of work

H2: Areas of work
Label above list: Industry focus as stated by the company
- CLAIM TO VERIFY: the label attributes the focus to the company; it was stated for Rahul's employer (fact_check C8).
Intro line: The company's work includes:
- CLAIM TO VERIFY: list below is the STATED focus, confirm for Sinor Marine Technologies. Grouping into six rows is a Director proposal, not Rahul's wording; "Integration" and "Upgrades" are activities, not fields.

Area list (each row links to solutions.html#<id>; the arrow glyph is aria-hidden)
1. Dynamic Positioning (dynamic-positioning): Automatic control of a vessel's position and/or heading using its thrusters.
2. Reference systems (reference-systems): The position measurements a DP system relies on.
3. Marine electrical and automation (electrical-automation): Electrical and control systems on board vessels and offshore units. (generic, no source read, low risk)
4. Propulsion and thruster controls (propulsion-thrusters): Controls for the units that move and position a vessel. (generic, no source read, low risk)
5. Integration (integration): Connecting separate vessel systems so they work together.
6. Upgrades (upgrades): Bringing existing systems up to date.
- "Dynamic Positioning" is in full in the hero and row 1; "DP" is used from row 2.

Text link below the list: See all solutions

SLOT S06 | NEEDED FROM RAHUL | One-line scope per area at the depth Rahul approves. It replaces the generic lines above.
SLOT S28 | NEEDED FROM RAHUL | One differentiator line: what makes Sinor Marine Technologies different. Nothing is written until Rahul provides it.

## 2.3 What the work includes

H2: What the work includes
Intro line: Work includes commissioning, service and technical support.
- CLAIM TO VERIFY: STATED words, confirm for Sinor Marine Technologies.
Steps (ordered list, h3 each, no numerals printed). PROPOSED, NOT STATED: the step names and their order were not given by Rahul (fact_check C1, Q4). Keep them only if Rahul confirms; otherwise use the items Integration, Commissioning, Service, Technical support with no order.
1. Discover: Understand the system and what the operator needs.
2. Design: Plan the solution and how it fits the systems already on board.
3. Install and commission: Commissioning is the testing and bringing into service of a newly installed or upgraded system.
4. Support: Provide service and technical support after handover.
Text link under the list: Service and support

## 2.4 Service strip

H2: After the system is in service
Line: Commissioning, service and technical support for marine and offshore systems.
- CLAIM TO VERIFY: STATED scope, confirm for Sinor Marine Technologies.
Three items (name only): Commissioning | Service | Technical support
Secondary pill: Service and support (service.html)

## 2.5 Credibility strip (slots only; whole section removed at publish if empty)

H2: Credentials and references
Line shown in draft: Nothing appears here until each item is confirmed.
SLOT S08 | NEEDED FROM RAHUL | Certifications: certificate numbers and issuing body. No ISO text is shown until confirmed, and only for Sinor Marine Technologies.
SLOT S09 | NEEDED FROM RAHUL | Partners and authorisations: each name with written approval to display it.
SLOT S10 | NEEDED FROM RAHUL | Selected projects: names only if Rahul permits.
SLOT S11 | NEEDED FROM RAHUL | Company numbers: only figures Rahul confirms for public use (the stand panel figures are NOT used).

## 2.6 About teaser

H2: About the company
Sentence 1: Sinor Marine Technologies works in marine and offshore technology.
Sentence 2: Its focus includes Dynamic Positioning, reference systems, marine electrical and automation, and propulsion and thruster controls.
- CLAIM TO VERIFY: both sentences rest on the STATED focus given for Rahul's employer; confirm it applies to Sinor Marine Technologies.
SLOT S30 | NEEDED FROM RAHUL | Legal entity name and registration (shown on About and in the footer; here only if Rahul wants it).
Text link: About the company (about.html)
SLOT S12 | NEEDED FROM RAHUL | Real company photo with rights confirmed, as an optimised copy. If it stays empty the section is text only.
Photo alt text when provided: NEEDED FROM RAHUL, describe what the photo actually shows.

## 2.7 Closing enquiry band

Line: Tell the team what you need.
Primary pill: Send an enquiry (contact.html)
Secondary text link: SLOT S31 | NEEDED FROM RAHUL | Sinor Marine Technologies LinkedIn page; link text "LinkedIn page" once provided. Omit the link until then.
Optional second line (Home only): Or read about the company. (links to about.html)
