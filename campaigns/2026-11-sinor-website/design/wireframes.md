# Wireframes: Sinor website, version 1 (mobile first, text)

Date: 2026-11-07. Author: ux-architect. Status: draft for the Director.
Companion file: sitemap.md (page list, navigation, footer, user flow, topic values).
This file has no final copy and no colours or fonts. Tokens come from campaigns/2026-11-style-cinematic-dark/design/design-system.md; the ui-designer chooses them for this project.
Design width order: 375 px first, then notes for 768 px and 1440 px. Every page: one h1, header, main, footer, skip link first.

## 0. How to read this

- Each section lists: purpose, content needed, primary call to action (P), secondary call to action (S), slot marks.
- Slot means a visible block on the page, in a calm bordered box, with the label text "NEEDED FROM RAHUL" and a one-line description of what goes there. IDs (S01 and up) are in the register at the end. A slot never holds invented text. Slots carry a data attribute (for example data-slot="S04") so QA can count them and the builder can remove them.
- Page width: 375 px, side gutter 20 px, content width 335 px. Sections stack in one column.
- All text is real DOM text. No text is inside an image or canvas. No content appears only through scroll animation.
- Section spacing, type scale and button styling come from the design system (pill buttons 48 px tall, 44 px minimum).

## 1. Shared parts (every page)

### 1.1 Skip link
First focusable element. Text "Skip to main content". Hidden until focused, then top left, above the header.

### 1.2 Header (64 px)
- 375 px: logo plate left (tap target at least 44 px high), native button "Menu" right with aria-expanded and aria-controls. Panel below the bar as described in sitemap.md section 2.
- Panel rows, in order: Home, Solutions, Service and support, About, Contact, then the pill "Send an enquiry". Rows 44 px, pill 48 px.
- Over the Home hero the bar is transparent over a scrim; on all other pages, and on Home once scrolled 40 px, it is solid. Without JS it is always solid.
- 768 px: panel is a two-column link grid; pill spans both columns.
- 1440 px: no Menu button. Inline links (small uppercase), pill right. Bar content width max 1200 px.

### 1.3 Footer
Order and content as sitemap.md section 2 (logo plate, legal entity line, Pages links, Find us with LinkedIn and contact slots, legal slot, stated-scope line).
- 375 px: single column, each group under a small heading (h2 or a labelled nav), rows 44 px.
- 768 px: two columns (logo and entity left; links right).
- 1440 px: four columns on one row.
- Footer slots: S01 (email), S02 (phone), S03 (address), S04 (hours), S05 (legal pages decision). The same slot IDs are reused on Contact so one answer fills both.

### 1.4 Closing enquiry band (all pages except Contact)
Purpose: end every page with the one action. Content: a short line, one pill "Send an enquiry" (or the page-specific label), optional second line "or read about the company" only on Home. P: Send an enquiry (Home, Solutions) or the page-specific primary (Service, About). S: none, kept to a single action.

## 2. HOME: index.html

Job: say what Sinor does in one headline, map the six areas, establish credibility honestly, route to enquiry or Solutions.
Page title area: the h1 is the hero headline (a very large, short line, 2 to 5 words, final text from copy).

### 2.1 Hero runway (cinematic stage)

Structure in the DOM, in this order:
1. header (see 1.2)
2. main, first child: section id="hero" (the runway).
3. Inside the runway: a sticky stage (div, position sticky, top 0, height 100svh) containing: the canvas (aria-hidden="true", no text alternative needed, decorative), the text stack (h1, one support line, the pill buttons), and a beat caption list.
4. Fallback block inside the stage: the static SVG vessel (see 2.1.5), shown when JS is off or reduced motion is set. Canvas is injected or shown by JS only.

Runway height (the scroll distance that drives the canvas):
- Section height 400svh at 375 px (stage 100svh sticky, so 300svh of scroll travel is the animation). With svh unit fallback 400vh. With JS the height is set by CSS, not by JS, so there is no layout shift.
- 768 px: 400svh. 1440 px: 350svh (a wide screen needs less scroll to read the same beats).
- Progress value p runs 0 to 1 as the runway travels from the top of the viewport to the end of the sticky range. p is computed from getBoundingClientRect in one requestAnimationFrame-throttled passive scroll listener (INP budget). No scroll hijacking, no smooth-scroll library.
- Reduced motion or no JS: runway height is 100svh plus the caption list (no tall runway, nothing to scroll through).

Mobile composition at 375 px (portrait, 375 by about 667 to 812):
```
+---------------------------+  0
| [logo plate]      [Menu]  |  64 px bar over scrim
|---------------------------|
|                           |
|  VERY LARGE               |  h1, left aligned, max 14ch, 3 lines at most
|  SHORT                    |  text sits in the upper 45 percent
|  HEADLINE                 |  on the scrim, away from the glow
|                           |
|  one support line         |  max 2 lines at 375
|  [Send an enquiry]        |  primary pill, full width up to 335 px
|  [See solutions]          |  secondary pill, below, 48 px
|                           |
|        ~~~~ ring ~~~~     |  canvas focal area: lower 45 percent
|       (  vessel line  )   |  vessel centred, ring around it
|        ~~~~~~~~~~~~~~    |
|  beat caption (1 line)    |  small, bottom, above the safe area
+---------------------------+  100svh
```
- The focal object (vessel plus ring) is centred horizontally and occupies the lower 45 percent, so no body text sits on the brightest part of the glow.
- Headline and buttons stay at the same position for all four beats (no layout movement, CLS 0). Only the canvas and the beat caption change.
- The buttons remain tappable throughout the runway because the stage is sticky and they are in the stage.
- Two pill buttons at most. P: "Send an enquiry" (contact.html). S: "See solutions" (solutions.html), secondary style.
- A small "Scroll" cue (text, not an icon-only control) near the bottom, hidden when reduced motion or no JS, and hidden after p exceeds 0.05.

Focal object (per the style study, decision in brief): one luminous vessel drawn as fine line art (a hull outline in side or three-quarter plan, deck line and mast or bridge silhouette), surrounded by a circular station-keeping ring (a thin circle with tick marks and four small reference nodes). One accent colour for the light, a single soft glow. Background: deep navy-black, with a faint horizon line and a few chart-grid arcs. No stars. No raster image, no video. All drawn with the canvas 2D API in plain JavaScript, device-pixel-ratio capped at 2, canvas resized on resize and orientation change.

#### 2.1.1 Scroll storyboard: 4 beats

The canvas draws from p. Each beat has a caption in the DOM. Beat names relate only to STATED areas. Caption text from copy; here only the topic.

| p | Beat | Canvas shows | Caption topic (real DOM text) |
|---|---|---|---|
| 0 percent | 1. The vessel on a dark sea | Navy-black field, faint horizon, faint grid arcs at low strength. The vessel hull is half drawn (line draw progress about 40 percent, bow first), glow at its lowest. No ring yet, only a small point at the vessel centre. | Dynamic Positioning (the vessel holds position) |
| 33 percent | 2. The ring appears | Vessel fully drawn. The station-keeping ring draws clockwise from the top and closes, radius settling to final size. Tick marks fade in. Glow at medium. | Reference systems (the positions the ring is held against) |
| 66 percent | 3. The systems connect | Four reference nodes light on the ring and thin lines run to the vessel. Small markers appear at the stern and bow (thruster positions) and a short line along the hull (electrical and automation). Glow at its highest, still contained inside the ring. | Marine electrical and automation, propulsion and thruster controls |
| 100 percent | 4. Held and settled | Everything in the final state: lines complete, ring steady, nodes steady, glow eased to medium, a very slight camera pull back so the vessel sits centred with air around it. This frame equals the static fallback exactly. | Integration, commissioning and service (the whole system supported) |

Interpolation: values are a pure function of p (no time-based loops), so scrolling back reverses the scene. Easing is applied to p with a gentle curve. Between beats, caption cross-fade uses opacity only. At p = 1 the stage unsticks and the next section follows.

#### 2.1.2 Beat captions in the DOM
- An ordered list with four items, each real text, in a container labelled for assistive tech (visually the current beat is shown; the others are visually dimmed to opacity 0 on JS only).
- With JS on and motion allowed, only the active caption is visible; screen readers still read the full list in order because opacity is not display none, and the list sits after the h1 and buttons in the DOM so reading order is headline, support line, buttons, captions.
- aria-live is not used (scroll updates would be noisy).
- Without JS or with reduced motion, all four captions are visible as a short list (see 2.1.4).

#### 2.1.3 JS enhancement logic (behaviour only)
1. Page loads with the SVG fallback visible and the runway at 100svh.
2. If JS runs and matchMedia("(prefers-reduced-motion: reduce)") is false and a 2D canvas context is available, add a class that: shows the canvas, hides the SVG, sets the runway to its full height.
3. If reduced motion changes live (matchMedia change event), swap back to the static state immediately and remove the scroll listener.
4. Pause drawing when the document is hidden or the runway is off screen (IntersectionObserver), so no work is done off screen.
5. No timers loop continuously. There is no autoplay animation, so no pause control is required (WCAG 2.2.2).

#### 2.1.4 Static fallback (no JavaScript, and prefers-reduced-motion)
- The stage is one screen tall: h1, support line, the two pills, then the static SVG vessel and ring in the final (p = 1) state, then the four captions as a visible list under the SVG (one line each, topics as in the storyboard).
- The SVG is inline, aria-hidden, and equals the beat 4 frame, built from the same geometry as the canvas so the two cannot drift apart.
- No parallax, no fades, no sticky behaviour (position static), no tall runway.
- The same fallback shows if canvas is unsupported or the script throws. A failing script must leave the page complete.

#### 2.1.5 Canvas states
- Loading: static SVG is already visible, so there is never an empty hero. The canvas replaces it after the first frame is ready, with no layout shift.
- Resize or rotate: redraw at the same p.
- Print: SVG only.
- Forced-colours: the SVG strokes use currentColor-compatible system colours; text unchanged.

#### 2.1.6 Hero content needed
- h1 headline, one support line, label for each pill, four beat captions, accessible name for the canvas group (none, it is hidden), the "Scroll" cue text.
- No slot in the hero. The hero uses only STATED scope.

Focus order inside hero: header controls, then h1 (not focusable), P pill, S pill. The canvas and the captions are never focusable.

### 2.2 What the company does (the six stated focus areas)
- Purpose: answer "what exactly do they do" in plain terms, and give a quick map of scope.
- Content needed: one short intro line (copy) and a list of the six areas (sitemap.md section 5). Each list item is a link to solutions.html#<topic>, with the area name and, at most, one short descriptive line (copy). A one-line label above the list: "Industry focus as stated by the company" (or the copy equivalent; source note kept in build notes).
- Layout 375 px: single column list, each item a full-width row of at least 56 px with the area name, one line of text, and a right-pointing arrow glyph that is aria-hidden. Hairline between rows (decorative only, the row's touch area is the boundary).
- 768 px: two columns, three rows. 1440 px: three columns, two rows, or a numbered column beside a sticky intro on the left (intro 4 of 12 columns, list 8 of 12).
- P: none inside the list items beyond the links. S: "See all solutions" text link below the list to solutions.html.
- Slot: none. If Rahul supplies one-line scope per area, it replaces the generic line; mark S06 "Home area descriptions at approved depth".

### 2.3 How work flows
- Purpose: show that Sinor covers the full lifecycle, not only supply. Generic, no durations, no numbers (DECISION and strategy rule).
- Content needed: four steps in order: Discover, Design, Install and commission, Support. Each: a step name (h3) and one short generic sentence (copy). Step labels use words, not digits, because no count claim is wanted beyond the order; an ordered list (ol) gives the order to assistive tech without printing numerals if the designer chooses.
- Layout 375 px: vertical stack with a thin vertical line on the left linking the four steps (decorative), each step a card on a flat surface panel, 24 px padding. Text not on glow.
- 768 px: 2 by 2 grid. 1440 px: one row of four with a horizontal connecting line above.
- P: none. S: "Service and support" text link under the list to service.html.
- Slot: none.

### 2.4 Service strip
- Purpose: bridge to the second page. State the support offer in one band and one action.
- Content needed: a heading, one line, and three short items: commissioning, service, technical support (STATED words). One link or pill to service.html.
- Layout 375 px: heading, line, three small rows (name only, 44 px), then a secondary pill "Service and support". 768 px: items in a row. 1440 px: copy left, three items right on one line.
- P: "Request support" is not here (it lives on Service); the strip's P is the secondary-style pill to service.html. Decision: the strip's single action is "Service and support" to avoid two competing primary pills on Home.
- Slot: S07 "Support hours and emergency route headline" is NOT shown here; it stays on Service only.

### 2.5 Credibility strip (slots only)
- Purpose: show where proof would sit and honestly say nothing is shown yet. Without this, a visitor sees no partners, certifications, projects or numbers and cannot tell if the absence is deliberate.
- Content needed: four labelled slots in a row or stack: S08 Certifications, S09 Partners and authorisations, S10 Selected projects (names only if permitted), S11 Company numbers (only if confirmed). Each slot shows the NEEDED FROM RAHUL label and one line on what is needed and that nothing will be shown until Rahul confirms.
- Layout 375 px: four stacked slot boxes, dashed border, 16 px text, each 80 px minimum. 768 px: 2 by 2. 1440 px: 4 in a row.
- P: none. S: none.
- This whole section is removed (not hidden) at publish time if slots are not filled. It is allowed to stay in the draft preview so Rahul sees the gaps.

### 2.6 About teaser
- Purpose: put a human line between the offer and the enquiry; link to About.
- Content needed: heading, two short sentences (legal entity line, STATED, and the scope line, STATED), one text link "About the company" to about.html. A photo slot S12 "Company photo (real, rights confirmed)" beside or above the text.
- Layout 375 px: photo slot first (16 by 9 box, no image yet), then text, then link. 768 px: photo left 5 columns, text right 7 columns. 1440 px: same, wider, maximum 1200 px.
- P: "About the company" (text link). S: none.
- Empty state: if S12 stays empty at publish, the section becomes text only, no empty frame.

### 2.7 Closing enquiry band
- As 1.4. Content: a short line (copy), pill "Send an enquiry" to contact.html, optional LinkedIn text link ("Company LinkedIn page") as an alternative. P: Send an enquiry. S: Company LinkedIn page.

### 2.8 Home focus order
1. Skip link
2. Logo link
3. Menu button (below 1024 px) or the five inline links (1024 px and up)
4. Header pill "Send an enquiry" (1024 px and up; below that it is inside the panel, which comes right after the Menu button when open)
5. Main: hero pill "Send an enquiry"
6. Hero pill "See solutions"
7. Six area links in list order
8. "See all solutions"
9. "Service and support" link in how work flows
10. Service strip pill
11. About teaser link
12. Closing band pill, then LinkedIn link
13. Footer: Pages links, LinkedIn link, contact slots (not focusable unless they become links), then nothing else.
The canvas, the SVG, the captions, the slots (plain text boxes) and the scroll cue are never focusable.

### 2.9 Home states
- Empty: slots (2.5, 2.6 photo) as described. No other section can be empty because content is static.
- Error: if the canvas script fails, the SVG fallback stays and nothing else changes. No error is shown to the visitor.
- No JS: as 2.1.4, whole page readable, all links work.

## 3. SOLUTIONS: solutions.html

Job: let an engineer find their system fast and ask about it.

### 3.1 Page intro
- Purpose: orient, name the page. h1 is a short headline (copy). One short intro line.
- Layout 375 px: a calm dark panel (no canvas, no glow, flat) with h1 and the intro. 768 and 1440 px: intro left aligned in 8 of 12 columns, with a small static SVG ring motif at the right (decorative, optional, aria-hidden).
- P: none. S: none.

### 3.2 Area jump list
- Purpose: quick scanning on a phone. A list of the six area names as anchor links to the sections below.
- Layout 375 px: a vertical list, 44 px rows (not a horizontal scroller, so no horizontal scroll). 768 px: three columns by two. 1440 px: six in one row of small pills or a sticky left rail (sticky only if it does not cover content; otherwise static).
- Without JS: plain anchor links work.
- P: none. S: the anchors.

### 3.3 Six area sections (repeat the same pattern)
Order: Dynamic Positioning (id="dynamic-positioning"), Reference systems (id="reference-systems"), Marine electrical and automation (id="electrical-automation"), Propulsion and thruster controls (id="propulsion-thrusters"), Integration (id="integration"), Upgrades (id="upgrades").
Each section contains, in order:
1. h2: the area name. "Dynamic Positioning" is written in full here and "DP" afterwards on the page.
2. Description: generic descriptive text slot. Text in the DOM is generic (what the area is, in plain words, from copy, no claims). One paragraph of up to 62 characters per line width.
3. "What the work covers": a short list of 3 to 4 generic items (copy, drawn only from STATED words: integration, upgrades, commissioning, service, technical support). Items link nowhere.
4. Slot S13 to S18 (one per area): "Scope at approved depth, vessel and system types, named products and trademarks: NEEDED FROM RAHUL". Dashed box, one per section, 64 px minimum.
5. Button: "Discuss this system" pill, links to contact.html?topic=<value>#enquiry. The accessible name includes the area, for example the link has visually hidden text "about Dynamic Positioning" after the label, so six identical labels are not ambiguous.
- Layout 375 px: each section on a flat surface panel, 24 px padding, 48 px gap between panels, h2 first. A thin number-free area label above h2 is optional.
- 768 px: two columns inside each section: h2 and button left (4 of 12, button sticky while the right column scrolls only if the section is taller than the viewport), description, list and slot right (8 of 12).
- 1440 px: the same with 1200 px max width, alternate sections may swap sides only if it does not break the reading order (the DOM order never changes).
- P: Discuss this system. S: none inside the section.

### 3.4 Closing enquiry band
As 1.4, general topic: P "Send an enquiry" to contact.html#enquiry. S: "Service and support" text link.

### 3.5 Solutions focus order
1. Skip link, logo, Menu or inline links, header pill (as Home)
2. Area jump links in list order (six)
3. For each of the six sections in order: its "Discuss this system" button (headings and slot are not focusable)
4. Closing band pill, then the Service and support link
5. Footer links
Hash navigation: activating a jump link moves focus to the target h2 (h2 has tabindex="-1") so screen reader and keyboard users continue from the section start.

### 3.6 Solutions states
- Empty: if a slot S13 to S18 is empty at publish, the dashed box is removed and the generic description stands alone. A section with no description at all is never shown (not possible with static content).
- Unknown hash (solutions.html#something): the page loads at the top, no error.
- No JS: complete.

## 4. SERVICE AND SUPPORT: service.html

Job: show what happens after supply (commissioning, service, technical support, upgrades) and give a support route.

### 4.1 Page intro
- h1 and one short line. Flat panel. P: "Request support" pill to contact.html?topic=service-support#enquiry. S: none. The intro pill is allowed here because the support visitor is often in a hurry and must find the action without scrolling on a phone.

### 4.2 Lifecycle after supply
- Purpose: show three stages: Commissioning (id="commissioning"), Service (id="service"), Technical support (id="technical-support"). Upgrades gets a one-line cross-link card to solutions.html#upgrades.
- Each: h2 or h3, one paragraph of generic description (copy), no durations or numbers. 
- Layout 375 px: vertical stack of cards. 768 px: three columns for the three stages, the upgrades card full width below. 1440 px: three columns with the upgrades card beside as a fourth.
- P: none. S: the Upgrades cross-link.

### 4.3 How to reach support (slots)
- Purpose: answer "who do I call when something fails". Today it cannot be answered, so show honest slots.
- Content needed: S19 Support hours and time zone, S20 Emergency route (phone, email or other), S21 Coverage (regions or vessel types), S22 Response commitment (only if Rahul approves wording). Plus the shared contact slots S01 and S02.
- Layout 375 px: a stacked definition list (term above value), each value a slot box. 768 px: two columns. 1440 px: terms left, values right in a table-like layout (dl, not a table).
- P: "Request support" pill (repeat, below the slots). S: the Company LinkedIn page link.

### 4.4 What to include in a support request
- Purpose: help the visitor prepare and reduce back and forth, as a convenience not a requirement.
- Content needed: a short list of items to bring (vessel or project type, the system, location, urgency), from the strategy. Copy writes the list; no commitments are made.
- Layout: a plain list. No slot.

### 4.5 Closing enquiry band
As 1.4, with P "Request support" (topic service-support) and S "General enquiry" (contact.html#enquiry).

### 4.6 Service focus order
Skip link, logo, nav and header pill (as Home); intro pill; upgrades cross-link; support slots (not focusable unless they become links); support pill; LinkedIn link; closing band pill and its secondary link; footer.

### 4.7 Service states
- Empty: slots S19 to S22 empty at publish are removed and the section collapses to "Use the Contact page" with a link; the section is never left blank.
- No JS: complete.

## 5. ABOUT: about.html

Job: say who the company is, honestly, with slots for everything unconfirmed.

### 5.1 Page intro
- h1 and a short intro line. Flat panel. P: none. S: none.

### 5.2 Company line
- Purpose: state the legal entity and what the company does.
- Content needed: the company name "Sinor Marine Technologies" (STATED 2026-11-07, shared with the footer, one source), the legal entity as slot S30, the scope line as a sentence marked CLAIM TO VERIFY (the list was given for Rahul's employer; confirm it applies to Sinor Marine Technologies), and the label "Industry focus as stated by the company".
- Layout 375 px: one column of text at 62ch maximum, large text size. 768 px: heading left, text right. 1440 px: same with wider gap.
- Slots: S23 Base and offices (UAE versus Singapore is unresolved), S30 Legal entity and registration, S24 Year founded (only if Rahul confirms), S25 Regions served.

### 5.3 How the company works
- Purpose: reuse the four-step lifecycle with a few extra sentences for people checking credibility. Content needed: the same four step names as Home, one generic sentence each (copy). No numbers.
- Layout: same as Home 2.3 but on a flat panel.
- P: none. S: "Service and support" link.

### 5.4 Certifications and partners (slots)
- Purpose: show where trust marks would sit and why they are absent. ISO and partner names are NOT ALLOWED until confirmed.
- Content: S08 Certifications (certificate numbers and issuer), S09 Partners and authorisations (each with written approval to name them).
- Layout 375 px: two stacked slots. 768 px: two columns. This section stays a section on About, not a separate Partners page (sitemap.md section 3).

### 5.5 Team (slot)
- Purpose: show where people would be shown.
- Content: S26 Team members (names, roles, photos, consent to publish; a named contact person and Rahul's job title are not shown by default).
- Layout 375 px: one slot box. 768 px: three slot cards in a row is not allowed (it would imply three people); keep one slot box of full width. 1440 px: one full width box.

### 5.6 Photos (slot)
- S12 reused: company or workshop photo, real and rights confirmed, optimised copy. Without it the section is omitted.

### 5.7 Closing enquiry band
- As 1.4. P: "Contact the team" to contact.html#enquiry. S: Company LinkedIn page.

### 5.8 About focus order
Skip link, logo, nav, header pill; Service and support link in 5.3; closing band pill and LinkedIn link; footer.

### 5.9 About states
- Empty: every slot has a defined removal rule at publish: S23 to S26 removed, text sections remain.
- No JS: complete.

## 6. CONTACT: contact.html

Job: complete the one conversion. The form is NOT connected to anything, and the page says so in readable text (DECISION 8).

### 6.1 Page intro
- h1 and one short line. Flat panel. The header pill is not shown on this page (sitemap.md section 2).
- P: none. S: a text link "Skip to the form" is not needed (the form is within one screen on a phone).

### 6.2 Not-connected notice
- Purpose: tell the visitor, before they type, that the form does not send.
- Position: directly above the form heading, inside main, not hidden, not dismissible, not inside a collapsed element.
- Appearance (requirements for the ui-designer): a bordered box, text at 16 px minimum, weight 400 or more, text contrast at least 4.5 to 1 against the box background on the dark stage, and the box border at least 3 to 1 against the page. Pick text colour from the text token (not muted or faint) so the pair clears 4.5 to 1 (design system: text on raise #F2F6FA on #16293F is 13.59 to 1). An icon may accompany the text but never replaces it, and conveys nothing by colour alone.
- Content needed: a bold label "Not connected yet" and one or two sentences: this form does not send messages yet, use the contact details below or the Company LinkedIn page (copy writes it). role="note" is optional; no aria-live because it is static.
- Notice removal rule: when Rahul approves an endpoint, the notice is removed in the same change that connects the handler (one build step, listed in the build notes).

### 6.3 Enquiry form (id="enquiry")
Heading h2 "Send an enquiry" (copy). A short line: "Fields marked required are needed to send." Required fields are marked with the word "required" in the label text (not only an asterisk or colour).

Fields, in order, 375 px single column, label above control, 48 px control height, 16 px minimum text (stops iOS zoom on focus):

| # | Label | Control | Required | Name and autocomplete | Rules |
|---|---|---|---|---|---|
| 1 | Name | text | Yes | name, autocomplete name | At least 2 characters after trim |
| 2 | Organisation | text | No | organisation, autocomplete organization | Free text |
| 3 | Email | email | Yes | email, autocomplete email | Must look like an address (one @, a dot after it), trimmed |
| 4 | Phone | tel | No | phone, autocomplete tel | If entered: digits, spaces, plus, hyphen, brackets, 6 to 20 characters |
| 5 | Topic | select | Yes | topic | Options: General enquiry, Dynamic Positioning, Reference systems, Marine electrical and automation, Propulsion and thruster controls, Integration, Upgrades, Service and support. Default from ?topic=; fallback General enquiry. |
| 6 | Vessel or project type | text | No | vessel | Free text, hint line (see below) |
| 7 | Message | textarea, 5 rows | Yes | message | At least 10 characters after trim, maximum 2000 with a visible live remaining counter only at 1800 or more |
| 8 | (button) | Send enquiry | | | See 6.5 |

Hint lines under controls (in text, not placeholder only): Email "We reply to this address" is NOT written because response is unconfirmed; hint only says what the field is for. Message hint: "Useful to include: vessel or project type, the system, location, urgency." Placeholder text is never used for instructions or labels.
- The country list, attachments, consent checkbox and a captcha are not added (not requested). Privacy text is slot S05 "Privacy notice: NEEDED FROM RAHUL", placed directly above the submit button, because a live form collects personal data. If Rahul decides to launch without it, the decision is recorded and the slot is removed.

### 6.4 Validation and error states
- Validation runs on submit (not on every key press, no premature errors). After the first failed submit, a field is re-validated when it loses focus or changes.
- Native browser bubbles are turned off with novalidate, because they are inconsistent; the HTML required, type and minlength attributes remain so the form works for assistive tech and as a fallback.
- Error summary: a box at the top of the form with role="alert" (or focus moved to it), heading "There is a problem" (copy), and a list of links, one per invalid field, each linking to the field. Focus moves to the summary on a failed submit.
- Field error: a message directly under the label or control, linked with aria-describedby, aria-invalid="true" on the control, error border and a leading text "Error:" so colour is not the only signal. The error colour and text must be computed for contrast on the field background (design system note) at 4.5 to 1.
- Messages (copy owns the final wording; the structure here):
  - Name empty: asks for a name.
  - Email empty: asks for an email address. Email malformed: says it does not look like an email address and shows the format.
  - Phone malformed: says which characters are allowed.
  - Topic not chosen: cannot happen (default is always set), but if the value is tampered the form resets it to General enquiry.
  - Message empty or too short: asks for at least 10 characters. Message too long: says the limit.
- Success state (form valid, nothing sent): see 6.5.
- No JS state: see 6.5.

### 6.5 Submit behaviour while not connected
- With JS: the button is enabled and labelled "Send enquiry". On press, validation runs. If valid, nothing is transmitted. Fields keep their values. A status panel appears above the button (role="status", focus moved to it), with a heading "Not sent" (copy) and text that the form is not connected yet, pointing to the contact details and LinkedIn page, with copy-friendly text of the entered message left in the field so the visitor can paste it elsewhere. The page does not navigate and does not say "thank you".
- Without JS: the submit button has the disabled attribute and the not-connected notice stays visible; JS removes disabled only when it takes over. Disabled button text still reads clearly (it is exempt from contrast rules but the label must stay legible), and the notice explains why it is not usable.
- Later, when an endpoint is approved: the handler sends the same fields, the status panel changes to a real success or failure message (success: heading and next step; failure: heading, what failed, what to do, entered data kept), and the not-connected notice is removed. This wireframe reserves those two states so the layout does not change.
- Double submit: not relevant now; when connected, the button is set aria-disabled while sending and its label changes to "Sending".

### 6.6 Contact details (slots)
- Purpose: let the visitor reach a person by another route while the form is not live.
- Content needed: S01 Email, S02 Phone, S03 Address, S04 Hours and time zone. Plus slot S31 for the Sinor Marine Technologies LinkedIn page (the earlier sinor-marine-services page is the Services company and is not used).
- Layout 375 px: below the form, a definition list; each value a slot box except LinkedIn. Rows are links once real (mailto and tel links need 44 px minimum height). 768 px: contact details move to a right column beside the form (form 7 of 12, details 5 of 12), notice stays above both. 1440 px: same, with the notice spanning both columns.
- If a visitor needs contact details first on a phone, the page could put details above the form; PROPOSAL rejected because the form is the main conversion and the details are currently all slots. Revisit once S01 and S02 are filled.
- P: Send enquiry. S: Company LinkedIn page.

### 6.7 Contact focus order
1. Skip link
2. Logo link
3. Menu button or inline links (no header pill on this page)
4. Main: not-connected notice is not focusable (static text, no tabindex)
5. Form fields in order: Name, Organisation, Email, Phone, Topic, Vessel or project type, Message
6. Send enquiry
7. Contact details links (when real; slots are plain text)
8. Company LinkedIn page link
9. Footer links
After a failed submit, focus is on the error summary, then Tab goes to its links, then the fields. After a valid submit, focus is on the status panel, then Tab continues to Send enquiry. The topic preselection does not move focus; on arrival via #enquiry the browser scrolls to the h2 and the h2 has tabindex="-1" so focus starts there.

### 6.8 Contact states
- Empty: contact detail slots as above; remove rule at publish is to keep a heading line "Use the form" and drop empty slots.
- Error: as 6.4.
- Topic query: unknown value falls back to General enquiry silently.
- Long values: Name and Organisation wrap, never overflow. Email addresses in details wrap with overflow-wrap anywhere.
- No JS: notice visible, form fields work (the visitor can see them), submit disabled, with the contact slots and LinkedIn link as the route.

## 7. 404 state (404.html, utility)

- Purpose: recover from a bad URL, same header and footer, one h1.
- Content needed: h1 saying the page was not found, one line, P pill "Back to home" (index.html), S text link "Send an enquiry" (contact.html). No search box (not requested), no canvas, no glow.
- Layout 375 px: centred left aligned text on the flat panel; buttons 48 px stacked. 768 and 1440 px: same, content width 62ch.
- Focus order: skip link, logo, nav, Back to home, Send an enquiry, footer.
- The page sets a status of 404 only at the server; on a static host that is the host's setting. Not verified here; note for the build step. Do not use a meta refresh.

## 8. Global states and rules

- Empty states: every slot has a defined remove rule at publish. A page never ships a visible NEEDED FROM RAHUL box. Count of visible slots is a QA measure (strategy section 8).
- Error states: only Contact has user input. Missing images are not possible (no raster images); an inline SVG that fails leaves a text page. Fonts are system fonts so no font failure state.
- No JavaScript: all five pages are complete and navigable. Without JS the Home hero is the static fallback, the nav is a visible list, the Contact submit is disabled with the notice.
- Reduced motion: no scroll-linked canvas, no fades, no parallax, no sticky stage. Menu panel appears instantly. Hover transitions 0.01 ms.
- Keyboard: every interactive element reachable by Tab in DOM order, visible focus ring (design system: 2 px focus colour, 3 px offset, never removed), Escape closes the menu. No keyboard trap anywhere, no focus-only-by-mouse control. Skip link works on every page.
- Sticky stage vs focus: the sticky hero never covers a focused element, because the header is the only fixed item and main content scroll-margin-top is 80 px so focused items are not hidden under the bar (WCAG 2.2 SC 2.4.11).
- Touch targets: 44 px minimum for nav rows, buttons, list rows; text links in running paragraphs have at least 24 px (WCAG 2.2 SC 2.5.8).
- Horizontal scroll: none at 375, 768 and 1440 px; no horizontal carousels, no wide tables (definition lists instead), long words wrap.
- Headings: one h1, h2 for sections, h3 for items. Hero headline is the h1; footer headings are visually small h2 or labelled nav landmarks.
- Performance notes for the hero: one canvas, DPR capped at 2, no per-frame allocation, no listeners other than one passive scroll and one resize, no images fetched.

## 9. Slot register (all NEEDED FROM RAHUL)

| ID | What | Where shown | Removal rule at publish |
|---|---|---|---|
| S01 | Public email | Footer, Contact, Service | Remove if not supplied |
| S02 | Public phone | Footer, Contact, Service | Remove if not supplied |
| S03 | Address | Footer, Contact | Remove if not supplied |
| S04 | Hours and time zone | Footer, Contact | Remove if not supplied |
| S05 | Privacy and legal pages decision | Footer, Contact (above submit) | Record decision, remove slot |
| S06 | One-line scope per area at approved depth | Home area list | Generic line stays |
| S07 | Support headline (hours, emergency route) | Service only, not on Home | Part of S19 and S20 |
| S08 | Certifications (certificate numbers and issuer) | Home credibility strip, About | Remove, never replaced by ISO text |
| S09 | Partners and authorisations (with approval) | Home credibility strip, About | Remove |
| S10 | Selected projects (names only if permitted) | Home credibility strip | Remove |
| S11 | Company numbers (only if confirmed) | Home credibility strip | Remove |
| S12 | Company or workshop photo (real, rights confirmed) | Home about teaser, About | Section becomes text only |
| S13 to S18 | Scope, vessel and system types, named products per area (six slots) | Solutions, one per area | Remove, generic text stays |
| S19 | Support hours and time zone | Service | Remove |
| S20 | Emergency route | Service | Remove |
| S21 | Coverage | Service | Remove |
| S22 | Response commitment (only if approved) | Service | Remove |
| S23 | Base and offices (UAE versus Singapore unresolved) | About | Remove |
| S24 | Year founded (only if confirmed) | About | Remove |
| S25 | Regions served | About | Remove |
| S26 | Team (names, roles, photos, consent) | About | Remove |
| S27 | Form endpoint or mailto address and who receives enquiries | Contact (not visible, build note) | Required to remove the not-connected notice |
| S28 | Differentiator line | Home, below the area list | Remove |
| S29 | Official Sinor Marine Technologies logo (header, footer; text wordmark until supplied) | Header, footer | Remove |
| S30 | Legal entity name and registration | About, footer | Remove |
| S31 | Sinor Marine Technologies LinkedIn page | Footer, Contact | Remove |
| S32 | DRAFT marker: project steps are a proposal, not confirmed | Home, About | Remove with the steps or after Rahul confirms |
| S33 | DRAFT marker: confirm the focus areas apply to Sinor Marine Technologies | Home, Solutions, About | Remove after Rahul confirms |

S28 position: a single slot box under the area list on Home (section 2.2), after S06. Count: 28 distinct slot IDs (S01 to S28). Some are repeated across pages, so the number of boxes on screen across the whole site can be higher than 28. (Director correction of the architect's footnote, 2026-11-07.)

## 10. Open items for the Director

1. Six areas versus the strategy's five (sitemap.md section 5): Upgrades added as the sixth. Confirm or drop.
2. 404.html is a utility file beyond the five pages: confirm.
3. Hero runway heights (400svh at 375 and 768, 350svh at 1440) are proposals to be tuned in the build against LCP, INP and CLS.
4. Support request topic is a form topic, not a separate form. Confirm.
5. The Contact submit while unconnected: enabled with a visible "Not sent" result (with JS), disabled (without JS). Confirm this over a permanently disabled button, which would hide the error states.
6. The wording of beat captions reuses only STATED words; copywriter writes the actual lines.
