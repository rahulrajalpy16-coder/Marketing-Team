# Sitemap and user flow: Sinor website, version 1

Date: 2026-11-07. Author: ux-architect. Status: draft for the Director.
Sources read: brain/brand-profile.md, brain/preferences.md, brain/lessons-learned.md, website-build-standards SKILL.md, brief.md, strategy.md, design-dna.md, design-system.md. Nothing under /tmp/work or campaigns/2026-11-sinor-site was read.
Labels: STATED (Rahul said it), DECISION (from the brief), NEEDED FROM RAHUL (visible slot on the page), PROPOSAL (my structural choice, open to change).
No copy is written here. Page text is the web-copywriter's job.

## 1. Page list

Five pages, five separate HTML files, flat structure, all in the site root so every URL is short and stable.

| Page | File | URL (placeholder domain) | Nav label | Page job | Primary call to action |
|---|---|---|---|---|---|
| Home | index.html | / | Home | Say what Sinor does, map the six areas, route to enquiry | Send an enquiry (contact.html) |
| Solutions | solutions.html | /solutions.html | Solutions | Let an engineer find their system | Discuss this system (contact.html?topic=...) |
| Service and support | service.html | /service.html | Service and support | Show what happens after supply, route to support | Request support (contact.html?topic=service-support) |
| About | about.html | /about.html | About | Say who the company is, honestly, with slots | Contact the team (contact.html) |
| Contact | contact.html | /contact.html | Contact | Complete the one conversion | Send the enquiry (form, not connected) |

Utility file (PROPOSAL, not a sixth page): 404.html. Static hosts differ, so this is a plain file with the same header and footer, one h1, a link home and a link to Contact. It is not in the nav or the footer. The Director should confirm it is wanted, since the brief says five pages.

Domain, canonical URLs and hosting are placeholders (DECISION 10). Use root-relative or plain relative links only, so the site works from any folder or preview.

## 2. Navigation

Header (all pages, identical markup except the current-page marker):
- Left: text wordmark "SINOR MARINE TECHNOLOGIES" and slot S29 for the official logo (DECISION 7; the repo logo is the Services company logo and is not used), links to index.html. Accessible name "Sinor Marine Technologies, home".
- Links in order: Home, Solutions, Service and support, About, Contact.
- One pill call to action, "Send an enquiry", pointing to contact.html. At 1024 px and wider it sits right of the links. Below 1024 px it sits inside the menu panel, last row, so the header stays tiny.
- Current page: aria-current="page" on its link, plus the visual marker from the design system (text colour plus underline).
- On contact.html the pill is not shown (the page is the destination); the link row still shows Contact as current.

Mobile behaviour (375 px, first design):
- Header bar 64 px: logo plate left, native button right with visible text "Menu" (accessible name stays "Menu"; the open state may read "Close" via text swap, aria-expanded flips true and false).
- The button is a real button element with aria-expanded and aria-controls pointing at the panel id. No role="menu", no hover-only behaviour.
- Panel: full width, directly under the bar, solid dark surface (not transparent over the canvas), a list of 5 links plus the pill. Each link row is 44 px minimum height and full width. The pill row is 48 px.
- Opening: panel slides or fades only when motion is allowed; with reduced motion it appears instantly.
- Closing: Escape closes and returns focus to the button. Activating a link navigates (new page), so no close handler is needed. Tab past the last panel item closes nothing automatically; the panel is simply the next content in the tab order. Clicking the button again closes it.
- No JavaScript: the panel is visible as a plain list below the logo (the button is hidden with the hidden attribute until JS runs, or the panel uses a details-free static layout). Either way all five links are reachable. PROPOSAL: the HTML ships with the list visible and JS adds the toggle, so nothing breaks without JS.
- Page scroll is not locked when the panel is open (the panel is short, five rows).

768 px: the same toggle pattern, panel becomes a two-column grid of links (still 44 px rows). The header stays 64 px.
1024 px and up (including 1440): the Menu button is hidden, links show inline in the header, small uppercase style per design system, the pill at the right. No dropdowns. Nothing in the nav is a disabled link.

Skip link: first focusable element on every page, text "Skip to main content", visually hidden until focused, then shown top left on a high-contrast plate, target is the main element (id="main", tabindex="-1"). On index.html the first item inside main is the hero, and a second skip target is not needed.

Breadcrumbs: none. Five flat pages, one level deep, the nav is always visible. Breadcrumbs would only repeat the nav. Reconsider if a News or Partners section with sub-pages is added.

Footer (all pages, identical):
1. Text wordmark and logo slot S29 (a supplied logo with an opaque white background sits on a white plate).
2. Company name "Sinor Marine Technologies" (STATED 2026-11-07), kept in one place (DECISION 4). Legal entity and registration: slot S30.
3. Links column "Pages": Home, Solutions, Service and support, About, Contact.
4. Links column "Find us": Company LinkedIn page: slot S31 (NEEDED FROM RAHUL; the sinor-marine-services page is the Services company and is not used), then contact slots (see wireframes, slot register): email, phone, address, hours, all NEEDED FROM RAHUL.
5. Legal row: privacy, cookies and terms are not built. Visible slot "Legal pages: NEEDED FROM RAHUL" until a decision. Copyright year and company line: year is generated or fixed by the builder, no founding year shown.
6. Small line (readable, 14 px or larger): "Industry focus as stated by the company, not independently verified." Final wording from copy, but the line itself is required by the brief.

## 3. Where later pages would go (not designed, not built)

| Later page | Proposed file | Nav position | Footer position | Waits for |
|---|---|---|---|---|
| Training | training.html | After Service and support | Pages column | Confirmed training offer |
| Simulator | simulator.html | After Training | Pages column | Confirmed simulator offer |
| Partners | partners.html | After About | Pages column | Rahul's written approval of each partner name and logo |
| Team | team.html | Inside About as a section first; its own page only if it grows | Pages column | Names, roles, photos, consent |
| News | news.html | Last link before Contact | Pages column | Real items to publish |

Rules when adding: the header holds at most seven links plus the pill; beyond that, group under a "Company" link on the About page rather than adding dropdowns. Home gets a new strip only if the page has real content. The About page already reserves slots for team, partners and certifications, so those can be filled in place before a separate page is justified.

## 4. URL and anchor rules

- Lowercase, hyphen-free file names as above.
- Query value for topics on contact.html, key "topic":
  - dynamic-positioning
  - reference-systems
  - electrical-automation
  - propulsion-thrusters
  - integration
  - upgrades
  - service-support
  - general (default)
- Example: contact.html?topic=dynamic-positioning#enquiry. The fragment #enquiry lands at the form heading so the visitor does not have to scroll past the page intro on a phone.
- Any unknown topic value falls back to general with no error shown.
- Solutions section ids match the topic values, so a link such as solutions.html#reference-systems works from Home (area list items link to these ids). Service and support ids: commissioning, service, technical-support.

## 5. Six stated focus areas (shared list used on Home and Solutions)

The brief and strategy list five system areas on Solutions, the task asks for six. Derived only from the STATED scope line ("Dynamic Positioning, reference systems, marine electrical and automation, propulsion and thruster controls, integration, upgrades, commissioning, service, technical support"). PROPOSAL, flagged for the Director:

1. Dynamic Positioning
2. Reference systems
3. Marine electrical and automation
4. Propulsion and thruster controls
5. Integration
6. Upgrades

Commissioning, service and technical support are the lifecycle on Service and support (and appear in the Home "how work flows" band). Upgrades appears on both: a system-level section on Solutions, and a cross-link from Service and support. If the Director prefers the strategy's five areas, delete Upgrades from the Solutions list and the Home list; no other structure changes. "Marine and offshore technology" is the sector line, not a focus area.

## 6. Main user flow: the enquiry

Entry points (HYPOTHESIS, no analytics): a link shared by message or LinkedIn lands on Home on a phone; a search lands on Solutions or Service; a trade-event contact lands on Home or About.

```
Entry
 |
 +-- Home (index.html)
 |     hero pill "Send an enquiry" ------------------------------+
 |     area list item -> solutions.html#<topic> -> button -------+
 |     closing enquiry band pill --------------------------------+
 |
 +-- Solutions (solutions.html)
 |     "Discuss this system" on each area -> contact.html?topic=<value>#enquiry
 |
 +-- Service and support (service.html)
 |     "Request support" -> contact.html?topic=service-support#enquiry
 |
 +-- About (about.html)
 |     "Contact the team" -> contact.html#enquiry
 |
 v
Contact (contact.html)
  1. Page loads. Topic select preselected from query, or General.
  2. Visitor reads the "not connected yet" notice (above the form, always visible).
  3. Visitor fills Name, Email, Message (required) and optional fields.
  4. Press "Send enquiry".
        |-- invalid: error summary at the top of the form, focus moves to the summary,
        |            each bad field shows its own message, first bad field is linked
        |-- valid:   nothing is sent. A status panel (role="status") says, in readable text,
        |            that the message was not sent because the form is not connected yet,
        |            and points to the contact slots. Entered values stay in the fields.
  5. Visitor uses direct contact (slots, once filled by Rahul) or the LinkedIn page.
```

Steps from any page to the form: 1 tap on mobile (the pill is in the hero, in each Solutions area, in the closing band, and in the menu panel). The longest path is 3 taps (Home, Solutions via area list, Discuss this system).

Known gap (strategy risk 1): until Rahul supplies an endpoint or mailto address, step 4 cannot complete. The design makes this honest and visible and leaves a single place (the form handler) to connect later.

## 7. Content inventory by page (what must exist, owner)

| Page | Real text from supplied facts | Slots (NEEDED FROM RAHUL) |
|---|---|---|
| Home | Scope line, six area names, lifecycle words | Differentiator line, numbers, projects, partners, certifications strip, photo |
| Solutions | Area names, generic descriptions to be written by copy | Scope per area at approved depth, vessel and system types, named products and trademarks |
| Service and support | Lifecycle words (commissioning, service, technical support, upgrades) | Hours, emergency route, coverage, response commitment |
| About | Legal entity line, scope line | Founded year, base, team, history, certifications, partners, regions |
| Contact | Form labels, LinkedIn URL | Email, phone, address, hours, endpoint, privacy text |

See wireframes.md for the numbered slot register (S01 and up) and every slot's position.
