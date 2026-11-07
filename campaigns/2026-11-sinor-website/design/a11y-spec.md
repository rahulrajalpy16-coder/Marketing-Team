# Accessibility specification: Sinor Marine Technologies website, version 1 (pass 1)

Date: 2026-11-07. Author: seo-a11y-specialist, pass 1. Status: draft for the Director, to be routed to frontend-developer and qa-reviewer.
Target: WCAG 2.2 Level AA (https://www.w3.org/TR/WCAG22/). Project rules that go beyond AA are marked PROJECT RULE.
Sources read: website-build-standards SKILL.md, brain files, brief.md, strategy.md, sitemap.md, wireframes.md, the style study design-system.md and tokens.css, and (for the coverage table only) the check list in scripts/web_qa.mjs.
Company name: "Sinor Marine Technologies" (Rahul's correction, 2026-11-07, via the Director). Where sitemap.md, wireframes.md or the brief still name another entity or its logo file or LinkedIn page, this spec overrides them. No other entity name, base or social page is used here.
Status of numbers: ratios copied from design-system.md were computed by the ui-designer on 2026-11-06. Ratios marked NEW were computed by me by hand with the formula below, because this session had no shell to run the script. The script is included in section 2.4 so QA can run it and confirm. Treat NEW numbers as unconfirmed until QA has run it.

## 1. Scope and honesty notes
- Conformance cannot be proven by a script. scripts/web_qa.mjs finds a subset of problems (section 13). Everything else needs manual or assistive technology testing and is NOT covered by the script.
- No assistive technology has been run for this spec. Nothing here claims the site passes.

## 2. Colour and contrast

### 2.1 Rules
- Normal text: at least 4.5:1 (SC 1.4.3). Large text (24 px or 18.66 px bold and up): at least 3:1.
- PROJECT RULE: treat all running text as normal text and meet 4.5:1 everywhere, so no size exception is relied on. Body text 16 px minimum, weight 400 minimum.
- UI component boundaries, focus rings, icons that carry meaning: at least 3:1 against adjacent colours (SC 1.4.11).
- Colour is never the only signal (SC 1.4.1): links in running text are underlined; errors have the text "Error:"; the current page has an underline plus aria-current; required fields have the word "required".
- Text over the canvas or any gradient: the worst (lightest) pixel behind the text must still give 4.5:1. See 2.3.
- Disabled controls are exempt from contrast, but PROJECT RULE: the disabled label stays at 3:1 or more so it can be read.

### 2.2 Token pairs allowed (from design-system.md, computed 2026-11-06)
Surfaces: abyss #050A12, deep #0A1626, surface #101F33, raise #16293F.

| Text token | abyss | deep | surface | raise | Use |
|---|---|---|---|---|---|
| text #F2F6FA | 18.27 | 16.73 | 15.28 | 13.59 | All body, headings, buttons, notice and status text. Default. |
| muted #A9B8C9 | 9.81 | 8.99 | 8.21 | 7.30 | Secondary text, nav links, card body, footer links. Any size at 16 px and up. |
| faint #8497AD | 6.62 | 6.07 | 5.54 | 4.93 | Hints, placeholders, legal line. 16 px and up only (PROJECT RULE: 14 px allowed for the footer legal line only, it still passes 4.5). Never for the not-connected notice, errors, required wording or slot labels. |
| accent #5BA4E0 | 7.40 | 6.78 | 6.19 | 5.50 | Inline link text, with underline. |
| accent-hi #8CC4F2 | 10.67 | 9.77 | 8.92 | 7.94 | Focus ring, hover link text. |
| steel #7F9BB8 | 6.88 | 6.30 | 5.75 | 5.12 | Decorative labels at 16 px or more. Not for essential text. |
| glow #F2A65A | 9.80 | 8.98 | 8.20 | 7.29 | Decorative only, not used as the sole signal. |

Other allowed pairs (design-system.md):
- Pill ink abyss on #F2F6FA 18.27; on hover #FFFFFF 19.84. Secondary pill text on deep 16.73.
- Control border #6A86A5 on deep 4.82, on surface 4.40 (needs 3). Computed here from those luminances: on raise 3.91, on abyss 5.26 (NEW, derived).
- Focus ring #8CC4F2 on deep 9.77 (needs 3).

Pairs NOT allowed:
- Brand navy #0D4A85 on deep: 2.02. Never as text, border, icon or focus colour on dark.
- Hairline #2A4260 (1.77 on deep): decoration only, never the only boundary of a control, slot box or the notice.
- Disabled text #6B7C90: 4.25 on deep (3.45 on raise, NEW, derived). Not for live text.
- Focus ring accent-hi against the white logo plate is about 1.9:1 (NEW, derived), so the ring must sit outside the plate (outline-offset 3 px onto the dark header), never inset on it.

### 2.3 Text over the canvas and glow (hero)
- Highest background luminance that still gives 4.5:1 (NEW, hand computed): behind text #F2F6FA at most 0.165 relative luminance; behind muted #A9B8C9 at most 0.065. So hero support text and beat captions use the text token, not muted.
- Peak glow check (NEW, hand computed): the shadow token --sh-glow at full strength over deep gives about #1E3A55, luminance 0.040. Text #F2F6FA on it is about 10.8:1 and muted about 5.8:1. This passes, but the canvas can draw brighter pixels than the shadow, so measure real pixels (check A9 in section 13).
- Caution on the scrim token: --c-scrim runs from transparent at the top to 0.92 abyss at the bottom, but wireframes.md puts the headline and buttons in the upper 45 percent of the stage. The scrim is weakest exactly where text is. Requirement: the upper text area must be backed by a solid or near-solid dark layer (abyss at 0.7 alpha or more under the whole text stack, or the canvas must keep that region at the deep colour), or the gradient direction must be changed. Frontend-developer and ui-designer decide which; the pass criterion is the pixel rule above at beat 3 (highest glow).
- Fixed header bar over the hero: same rule, plus a solid fallback with no JS.

### 2.4 NEW pairs: error red and related
Error text and error borders use a warm light red. Token proposal (to be added to tokens.css by the ui-designer, not by me): --c-error: #FF8A80.

Computed by hand with the WCAG 2.2 formula (linearise each channel c/255: c/12.92 if 0.03928 or less, else ((c+0.055)/1.055)^2.4; L = 0.2126R + 0.7152G + 0.0722B; ratio = (Llight+0.05)/(Ldark+0.05)):

| Pair | Ratio (hand computed, NEW) | Result |
|---|---|---|
| #FF8A80 on abyss #050A12 | 8.69 | pass |
| #FF8A80 on deep #0A1626 | 7.97 | pass for text and 3:1 border |
| #FF8A80 on surface #101F33 | 7.27 | pass |
| #FF8A80 on raise #16293F | 6.47 | pass |

Luminances used: #FF8A80 = 0.4101; deep 0.00776; surface 0.01330; raise 0.02116; abyss 0.00293.
Use: error text, the "Error:" prefix, the invalid field border (2 px), the error summary heading. Error summary body and links stay text token. An error is never red alone.

Script for QA to confirm (not run by me; run with `python3 -I script.py`, no files read):
```python
def lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
def lum(h):
    h = h.lstrip('#'); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
for bg in ('#050A12', '#0A1626', '#101F33', '#16293F'):
    print('#FF8A80 on', bg, round(ratio('#FF8A80', bg), 2))
print('border #6A86A5 on raise', round(ratio('#6A86A5', '#16293F'), 2))
print('disabled #6B7C90 on raise', round(ratio('#6B7C90', '#16293F'), 2))
print('accent-hi #8CC4F2 on white', round(ratio('#8CC4F2', '#FFFFFF'), 2))
```
Expected: about 8.69, 7.97, 7.27, 6.47, 3.91, 3.45, 1.86. A different result overrides this table.

### 2.5 Company mark (logo) cases
The repo file assets/brand/sinor-logo.png must not be used on this site (it carries a different entity name). The logo is a slot until Rahul supplies the Sinor Marine Technologies logo.
Case A, until then: a TEXT wordmark.
- Real DOM text "Sinor Marine Technologies" in the header and footer, text token #F2F6FA (16.73 on deep, 18.27 on abyss), 16 px or more, weight 600 or more, no letter-spaced uppercase below 14 px, not an image, not a canvas.
- It is a link to index.html. Visible text is "Sinor Marine Technologies". Accessible name: "Sinor Marine Technologies, home" (visible text first, so SC 2.5.3 Label in Name passes; ", home" is visually hidden text).
- On the transparent header over the hero the contrast rule 2.3 applies. Link area at least 44 px high.
- The footer wordmark is plain text or the same link; if a link, same name.
Case B, once a logo image is supplied:
- img inside the same link, alt "Sinor Marine Technologies" (the link name then is the alt plus a visually hidden ", home"). width and height attributes set. Footer copy: same alt, or empty alt if the link text elsewhere already names it, never both.
- If the file has an opaque white background: sit it on a white plate (as the design system), focus ring outside the plate (2.2).
- If transparent: before use, sample the logo's lightest and darkest colours against #0A1626 and abyss; every part needed to read the name must reach 3:1 (SC 1.4.11 for the graphic, 4.5:1 for any text rendered inside the image, because text in images is still judged as text). Navy marks fail (2.02) and need the plate. QA records the numbers.
- Never recolour, invert or crop the supplied logo.

## 3. Target size
- SC 2.5.8 (AA): every pointer target at least 24 by 24 CSS px, unless spacing, an inline text link inside a sentence, or the browser default control applies.
- PROJECT RULE: 44 by 44 CSS px minimum for Menu button, nav rows, pills (48 high), list rows (area rows 56), footer link rows, mailto and tel links, form controls (48), the skip animation link and the wordmark link.
- Standalone text links outside a sentence ("See all solutions", "About the company", "Service and support" under a list, upgrades cross-link, any social link) get padding or inline-flex so the box is 44 px high. Links inside a paragraph rely on the inline exception but the line-height (1.6 at 16 px is 25.6 px) keeps them at 24 px or more anyway.
- Aria-hidden arrow glyphs inside a link are part of the link box, not separate targets.
- Targets stay at least 24 px at 375, 768 and 1440 px. The script only checks 375 (section 13).

## 4. Keyboard, focus and order

### 4.1 Rules
- Everything operable by keyboard (SC 2.1.1), no trap (2.1.2), logical order (2.4.3) equal to DOM order. No positive tabindex. CSS order, grid placement or float never reorders interactive items against the DOM.
- Visible focus (2.4.7, 2.4.13 target): 2 px outline in --c-focus (#8CC4F2), offset 3 px, never removed. Use outline, not box-shadow alone, so it survives forced colours. Do not use outline:none without a replacement. Ring contrast 3:1 or more against the adjacent colour (9.77 on deep). Use :focus-visible for mouse comfort; forms controls also show it on :focus-visible.
- Focus not obscured (2.4.11): html scroll-padding-top 80 px and scroll-margin-top 80 px on anchor targets and h2 targets, so the 64 px header never covers the focused item. Nothing else is fixed or sticky above content (the hero stage is sticky but is the viewport, see 6).
- Skip link: first focusable element on every page, text "Skip to main content", hidden until focus, then shown top left on a plate with ink abyss on #F2F6FA (18.27), 44 px high, ring outside the plate. Target id="main" tabindex="-1", with outline suppressed only on this programmatic focus if a replacement is shown.
- Programmatic focus targets (h2 with tabindex="-1" on hash arrivals, form heading, error summary, status panel) show the focus ring too.
- Dragging, path gestures: none used (2.5.7 satisfied by absence). Pointer cancellation: use the click event; no down-event activation (2.5.2).
- Consistent navigation and help (3.2.3, 3.2.4, 3.2.6): same nav order on all pages, same names for repeated links, footer contact area in the same place on every page. The header pill is absent on Contact; QA checks that this does not count as moved help.

### 4.2 Tab order per page (from wireframes.md, with changes)
Common prefix on all pages: 1 skip link; 2 wordmark link; 3 Menu button (below 1024 px) or the five inline links (1024 and up); 4 header pill "Send an enquiry" (1024 and up, not on Contact; below 1024 it is the last row inside the open panel). Closed panel links are not focusable (hidden attribute or display none).

Home: prefix; hero pill "Send an enquiry"; hero pill "See solutions"; link "Skip the animation" (NEW, section 6.5; present only when the scroll scene is active; sits after the pills in the DOM so the stage stays in reading order); six area links; "See all solutions"; "Service and support" link in how work flows; service strip pill; About teaser link; closing band pill; footer links. Canvas, SVG, captions, slots and the "Scroll" cue are never focusable.
Solutions: prefix; six jump links; six "Discuss this system" links in section order; closing band pill; "Service and support" link; footer.
Service and support: prefix; intro pill "Request support"; upgrades cross-link; support pill; closing band pill and its secondary link; footer. Slots are text, not focusable.
About: prefix; "Service and support" link (5.3); closing band pill; footer. (The Company LinkedIn link in the wireframes is removed until Rahul supplies a Sinor Marine Technologies page.)
Contact: prefix without header pill; form fields Name, Organisation, Email, Phone, Topic, Vessel or project type, Message; "Send enquiry" (disabled without JS, so skipped there); contact detail links once real (mailto, tel); footer. The not-connected notice is static text, no tabindex.
404: prefix; "Back to home"; "Send an enquiry"; footer.
Footer on every page: nav "Pages" links, then any real contact links. No external social link until supplied.

## 5. Menu button and panel (below 1024 px)
Pattern: disclosure, not an ARIA menu.
- Markup: `<button type="button" id="menu-btn" aria-expanded="false" aria-controls="menu-panel">` with visible text "Menu". The panel is a `<ul>` inside `<nav aria-label="Main">`, id="menu-panel". No role="menu", role="menuitem", aria-haspopup.
- Name: visible text and accessible name are both "Menu". Recommendation to the Director: do NOT swap the text to "Close" (sitemap.md allows it). The state is carried by aria-expanded, and a changing name plus aria-expanded makes screen readers say "Close, expanded". If the design needs the swap, the name must change with the visible text, never diverge (SC 2.5.3).
- Open: Enter or Space (native button) or click sets aria-expanded="true" and shows the panel. Focus stays on the button (disclosure pattern); Tab then moves into the first link because the panel follows the button in the DOM. Panel is solid (not transparent over the canvas), text contrast per 2.2 on its own background.
- Close: clicking the button again, or Escape. Escape closes the panel when focus is on the button or inside the panel; if focus was inside the panel, focus returns to the button. If focus is elsewhere, Escape does nothing. Tab past the last item does not close it (sitemap decision). Optional: a click outside closes it without moving focus.
- Closed state is hidden from keyboard and screen readers (hidden attribute or display none), not just moved off screen.
- Resize to 1024 px and above: button hidden, panel always visible inline, aria-expanded and the closed state removed so links stay reachable. Resize below with the panel open keeps the stored state.
- No JS: the button is hidden (hidden attribute until script runs, or an html class `js` set by an inline head script) and the full list is a visible static list. Add the `js` class in the head so the closed state does not cause layout shift.
- Reduced motion: the panel appears with no slide or fade.
- Target size: button 44 by 44 minimum, rows 44, pill row 48.
- aria-current="page" on the current link, plus underline and text token colour (not colour alone).

## 6. Home hero: sticky scroll-linked scene

### 6.1 Real DOM text
- The h1, support line, pills and the four beat captions are real text in the DOM, in this order: h1, support line, pills, skip animation link, captions list. Nothing is conveyed only by the canvas. No content appears only through scroll position.
- Captions: `<ol>` of four items, with a short accessible name from copy (aria-label or a visually hidden heading is not needed if the list has aria-label). With JS and motion allowed only the active caption is visible by opacity; the others stay in the accessibility tree (opacity, not display none or visibility hidden), so a screen reader reads all four. No aria-live (scroll would flood announcements).
- Contrast of the active caption is judged at full opacity over the real pixels (section 2.3). Opacity cross-fades are transitions; the resting states must pass.

### 6.2 Canvas and SVG
- `<canvas aria-hidden="true">`, no tabindex, no role, no text fallback inside it that duplicates captions. The SVG fallback: `aria-hidden="true" focusable="false"`, no `<title>` or `<desc>` inside it. They are decorative because all meaning is in the captions and the h1.
- Under forced colours the SVG strokes use system colours (CanvasText) or currentColor.
- No keyboard focus can land on anything inside the canvas group.

### 6.3 Reduced motion and no-JS static path
Static path is the default state of the HTML and CSS; motion is the enhancement.
- Triggers: JS off, `prefers-reduced-motion: reduce`, 2D canvas unavailable, script error, print, and the short viewport rule in 6.4.
- Static path: stage position static, height auto (one screen at most), no tall runway, no parallax, no fade-rise reveals, the SVG shown in its beat 4 state, the four captions visible as a list, the "Scroll" cue and the skip animation link not rendered.
- Wrap all fades, rises, parallax and smooth scrolling in `@media (prefers-reduced-motion: no-preference)`. `scroll-behavior: smooth` only inside it. Hover transitions 0.01 ms under reduce (the tokens already do this).
- If the preference changes live, swap to static at once and remove the scroll listener (wireframes 2.1.3 step 3).
- No setting needs to be stored, so no cookie or storage is needed.

### 6.4 Zoom, reflow and short viewports
- The stage is `min-height: 100svh`, not a fixed height, and has no overflow hidden that could clip the h1, pills or captions. At 200 percent zoom or on a landscape phone (about 667 by 375) the viewport is short, so the content can exceed the stage; a sticky stage taller than the viewport hides its bottom (fails SC 1.4.4, 1.4.10, 2.4.11).
- Rule: below a viewport height of 560 px (`@media (max-height: 560px)`), and at 320 px width, use the static path. Zoom shrinks the CSS viewport, so this also covers 200 and 400 percent zoom.
- The page must reflow at 320 CSS px wide with no horizontal scroll (SC 1.4.10). Project gates test 375, 768, 1440; QA also tests 320.
- No fixed heights on text boxes; use min-height for pills and rows so text spacing changes (SC 1.4.12: line height 1.5, paragraph spacing 2x, letter 0.12em, word 0.16em) do not clip.
- Viewport meta is `width=device-width, initial-scale=1`. Never `maximum-scale` below 5 and never `user-scalable=no`.

### 6.5 Skip animation link
- A real link or button with visible text "Skip the animation", shown whenever the scroll scene is active. It is visually hidden until focused, then visible near the pills on the stage, ring outside, 44 px high, ink and plate as the skip link (18.27).
- It is a link to the id of the section after the runway (suggest id="areas", the "what the company does" section), whose h2 has tabindex="-1" and scroll-margin-top 80 px. Activating it moves the view and focus there. Without JS or under reduced motion the link is not rendered (there is no runway to skip).
- Pointer users can also scroll normally; nothing is hijacked. Keyboard users who tab through the pills are not trapped in the runway because the pills live in the sticky stage.

### 6.6 Motion, flashing and pause
- No autoplay. The scene is a pure function of scroll position, so it is user controlled and not subject to the 5 second pause rule (SC 2.2.2).
- PROJECT RULE: any time-based motion that runs longer than 5 s on a page (an idle glow pulse, a ring that keeps ticking) is not allowed unless it has a visible pause control and respects reduced motion. Default build: none.
- Flashing (SC 2.3.1): nothing flashes more than 3 times per second. The scene uses continuous, eased changes in one direction. No strobing glow, no hard cuts between beats, no large area changing between near black and near white. Glow stays inside the ring (wireframes beat 3).
- Parallax and motion triggered by scroll (SC 2.3.3 is AAA, but PROJECT RULE follows it): disabled under reduced motion.
- Scroll cue "Scroll" is real text, hidden once p exceeds 0.05 or when static.
- No scroll hijacking, no scroll snap locking, no wheel event capture; the scroll listener is passive.

## 7. Contact form

### 7.1 Not-connected notice
- Static text above the form heading, in main, never hidden, dismissible or collapsed. Bold label "Not connected yet" plus one or two sentences, 16 px minimum, weight 400 or more, text token on raise (13.59), box border 1 px or more in control border #6A86A5 (4.82 vs deep, 3.91 vs raise, both 3 or more). Optional icon is aria-hidden and never replaces the words.
- No role="alert" and no aria-live (it is not a change). id="not-connected-notice". The submit button gets aria-describedby pointing to it.
- Never use faint, steel, disabled or glow tokens for the notice text.
- The notice is removed in the same change that connects the form (build note).

### 7.2 Labels, required, hints
- Every control has a visible `<label for>` above it. No placeholder-as-label. Placeholders are not used for instructions.
- Required fields (Name, Email, Topic, Message): HTML `required` attribute and the word "required" in the label text (for example "Name (required)"). The line above the form says "Fields marked required are needed to send." An asterisk alone is never used (SC 3.3.2, 1.4.1).
- Hints are real text under the control, linked by aria-describedby (hint first, then the error id when present).
- Autocomplete (SC 1.3.5): Name autocomplete="name"; Organisation autocomplete="organization" (the token is spelled in American English); Email "email"; Phone "tel". Email type="email", phone type="tel". Text 16 px or more, controls 48 px high.
- Topic select: first option equals the default from ?topic= or General enquiry. Changing it must not submit or change focus (SC 3.2.2).
- Message counter appears at 1800 characters or more. No per-keystroke announcements: a polite live region is updated only when 1800 is crossed and at the limit (2000).
- Control state colours: border #6A86A5 on deep (4.82), focus ring, error border #FF8A80 2 px (7.97).

### 7.3 Validation, errors, focus management
- Form has novalidate; HTML required, type and minlength stay in the markup.
- Validate on submit. After a failed submit, re-validate a field on blur and on change. No errors on first focus or per key press.
- Failed submit: build an error summary at the top of the form, container tabindex="-1", with an h2 "There is a problem" (copy), then a list of links in field order, each href="#<field id>" and text equal to that field's error message. Move focus to the summary container. Because focus moves, do not also add role="alert" or a live region (double reading). Test with a screen reader before adding either.
- Per field: message directly under the label or control in a `<p id="<field>-error">` that starts with visible text "Error:" in the error colour, aria-invalid="true" on the control, aria-describedby gives hint id then error id. Remove aria-invalid and the message when fixed. The summary updates on the next submit.
- Messages say what is wrong and how to fix it (SC 3.3.1, 3.3.3): empty name, empty email, "does not look like an email address, for example name@company.com", phone allowed characters, message at least 10 characters or over 2000.
- Clicking a summary link moves focus into the field (anchor to a form control focuses it) and scrolls clear of the header (scroll-padding 80 px).
- Valid submit while not connected: nothing is sent, values stay (SC 3.3.7 redundant entry). A status panel with a heading "Not sent" appears above the button. Panel container tabindex="-1", focus moves to it. wireframes.md 6.5 asks for role="status" AND focus move; I recommend focus move only for the same double-reading reason. This is a deviation to confirm with the Director.
- Never say "thank you" or success when nothing was sent.
- No authentication, no captcha, no timed step, no drag (SC 3.3.8 and 2.2.1 satisfied by absence). Consent and legal slot S05 sits above the submit button as plain text.
- No JS: the submit is disabled, which removes it from tab order; the visible not-connected notice, linked by aria-describedby, explains why, and the contact slots and links are the route.
- Later, when connected: success and failure panels follow the same focus rule, and aria-disabled (not disabled) while sending.

## 8. Slot boxes (NEEDED FROM RAHUL)
- Announcement: a slot is plain visible text. The box is a div with a data-slot attribute (for QA), no role, no aria-hidden, no aria-label, not focusable. The label text "NEEDED FROM RAHUL" and the one-line description are real DOM text, so a screen reader reads them in order. They are not hidden from assistive technology because reviewers need to know a gap exists.
- Where the layout is a definition list (support details, contact details, footer contact), the slot sits inside the dd, the term in the dt.
- Visual: dashed 1 px or 2 px border in #6A86A5 (4.40 or more on surface), text token or muted, 14 px or more (PROJECT RULE for slot labels), not faint. The dashed border and the words together carry the meaning, not colour.
- Slots that sit in a row on desktop (credibility strip) must not imply real content, such as three people cards (wireframes 5.5 already says one box).
- No slot reaches the published site. QA counts [data-slot] and the visible text "NEEDED FROM RAHUL".

## 9. Language
- `<html lang="en-GB">` on every page including 404 (copy uses British spelling such as enquiry and organisation; `en` is also acceptable if the Director prefers). The only language is English, so no lang attributes on parts. If a term from another language is added, wrap it with its own lang.
- No language switcher.
- Title element present and unique per page (pass 2 owns the text).

## 10. Landmarks and structure
Every page: skip link first inside body; `<header>` (banner) containing the wordmark link and `<nav aria-label="Main">`; one `<main id="main" tabindex="-1">`; `<footer>` (contentinfo). Footer contains `<nav aria-label="Footer">` for the Pages links; the contact slots group has its own visible heading, not a second nav.
- Landmark names are unique (Main, Footer). No role="navigation" on a div; use native elements.
- Section landmarks: a `<section>` is given aria-labelledby its h2 only where it is a main region of the page (hero uses aria-labelledby the h1 id). Do not create unnamed sections that act as noise.
- Contact form element has an accessible name by aria-labelledby the form h2, so it is a form landmark.
- Closing enquiry band: a plain div with a short line and a pill, or a section with its own h2. Not both an h2 and a duplicate p headline.
- Language and title are on the html and head; no content outside landmarks except the skip link.

## 11. Heading outline checks
Rules: exactly one h1; no skipped levels (h1, h2, h3 only in steps of one); every section has a heading; hero h1 is the headline; heading text is meaningful out of context; headings are not used for style; footer group headings are small h2 elements (visually small via CSS, the level unchanged). Copy text is not final, so the outline lists structure only.

| Page | Expected outline |
|---|---|
| Home | h1 hero headline. h2 "what the company does" (id areas). h2 how work flows, with four h3 steps. h2 service strip. h2 credibility (slots) with h3 per slot label. h2 About teaser. Closing band (h2 or plain). Footer h2 groups. |
| Solutions | h1. h2 per area, six, in the order dynamic-positioning, reference-systems, electrical-automation, propulsion-thrusters, integration, upgrades. Optional h3 "What the work covers" inside each. Jump list preceded by a visually shown or hidden h2 only if copy supplies one. |
| Service and support | h1. h2 Commissioning, h2 Service, h2 Technical support, h2 Upgrades (cross-link card), h2 How to reach support (dl with slots), h2 What to include. (Stages as h2 so the outline stays flat; wireframes allowed h2 or h3.) |
| About | h1. h2 Company line. h2 How the company works with four h3 steps. h2 Certifications and partners (slots). h2 Team (slot). Photo section only if filled. |
| Contact | h1. h2 "Send an enquiry" (id enquiry, tabindex -1). The error summary h2 and status h2 only exist after a submit. Contact details h2. |
| 404 | h1 only, then footer headings. |

Checks: if the error summary or status panel injects an h2, the outline stays valid because it appears inside the form below the h1 and the form h2.

## 12. Per-component notes
- Header and nav: sections 4 and 5. Bar 64 px. Solid background without JS and after 40 px of scroll. Current page uses aria-current.
- Pill buttons: real a or button elements. Links that look like buttons are `a`, buttons that act are `button`. Disabled is the native attribute where focus is not needed; aria-disabled with a visible reason where focus must remain. Border 1 px transparent so the shape survives forced colours. Hover must not be the only way to reveal anything.
- Links with a repeated label: the six "Discuss this system" links keep that visible text first and add visually hidden text "about Dynamic Positioning" and so on (name begins with the visible label, SC 2.5.3). "Request support" and "Send an enquiry" repeat with one destination each, which is allowed.
- External links (when any exist): visible text that says it leaves the site, for example "opens linkedin.com", same tab. No target=_blank without warning. No external social link until Rahul supplies a Sinor Marine Technologies page.
- Cards: only a link card has hover and focus-within styles. Do not nest links inside a linked card.
- Area list on Home: each row one link with the name and one line inside the same anchor, 56 px minimum, arrow glyph aria-hidden. Hairline separators are decorative.
- Lifecycle steps: an ol, so order reaches assistive technology; no printed digits needed.
- Definition lists (support and contact details): dl, dt, dd. No wide tables, so reflow holds. If a real table is ever added it needs th scope and a caption.
- Images and SVG: informative images need alt; decorative get empty alt or aria-hidden. Wireframes plan no raster images. Any logo image follows 2.5. No text inside images, so SC 1.4.5 is met.
- Footer: text on abyss, links muted (9.81), 44 px rows, legal line 14 px or more in faint (6.62) or muted.
- Print: SVG only, text colours inverted by a print stylesheet is optional, not required.
- Forced colours (`forced-colors: active`): borders, outlines and SVG strokes remain; no information only in background colour or box-shadow.
- Colour scheme: set `color-scheme: dark` on :root so native select popups, scrollbars and autofill are dark and readable. QA checks the select list by eye.
- Time: no time limits and no auto-refresh.
- 404: no meta refresh (a refresh would break SC 2.2.1 and 3.2.5).

## 13. Acceptance checks

### 13.1 Checks scripts/web_qa.mjs can run (it crawls at 375, 768 and 1440 px, writes FAIL or WARN)
Mapped from the rules the script contains. The script's contrast check is approximate (it ignores background images and opacity, so it does not judge the canvas).
- A1 html lang present (FAIL if missing). This only proves presence; QA also reads that it starts with "en".
- A2 viewport meta present. QA also reads the content for no maximum-scale or user-scalable=no (not tested by the script).
- A3 exactly one h1 per page (FAIL).
- A4 heading order skips (WARN, reports skipped levels). Treat any WARN here as a defect.
- A5 img alt attribute missing (FAIL). Empty alt is accepted, so decorative versus informative needs a human.
- A6 main, header and footer landmarks present (main FAIL, others WARN); skip link detected (WARN).
- A7 links and buttons with no accessible name (FAIL), at 375 and 1440, which tests the Menu button at 375.
- A8 form controls without a label (FAIL).
- A9 low contrast text, approximate (FAIL), at three viewports.
- A10 pointer target smaller than 24 px, at 375 only (WARN). Treat as a defect.
- A11 horizontal overflow at 375, 768, 1440 (FAIL).
- A12 broken anchors and broken internal links (FAIL), which covers the skip link target, #enquiry, solutions section ids and the skip animation target.
- A13 em or en dash in visible text, title, meta description or alt (WARN).
- A14 console errors, page errors, failed requests, external requests (a font or tracker would show).
- A15 lorem ipsum (FAIL), and title, meta description, canonical, Open Graph presence (pass 2 territory).
Manual command for QA outside the script: grep -rnP "[\x{2013}\x{2014}]" over the site folder for dashes in source.

### 13.2 NOT covered by the script (manual or assistive technology testing needed)
These cannot be proven by the script. QA reports each as tested by hand, or as not tested.
- M1 Keyboard-only pass of every page in the order in 4.2: no trap, every control reachable, Escape behaviour, skip link works, skip animation link works.
- M2 Focus visibility: a visible ring on every focusable item, including the programmatic targets, at three viewports, and not hidden by the 64 px header (SC 2.4.11) after hash arrival and after Tab.
- M3 Menu pattern: aria-expanded flips on open and close, aria-controls resolves, Escape returns focus to the button, closed links not tabbable, desktop shows inline links and no button.
- M4 prefers-reduced-motion emulated (Playwright emulateMedia reducedMotion reduce, or the browser setting): static hero, no fades, no sticky runway, captions visible; and live change swaps state.
- M5 JavaScript disabled: all five pages complete, nav list visible, hero static, contact submit disabled with the notice.
- M6 Hero contrast over real canvas pixels at beat 3: screenshot with the text hidden, sample the lightest pixel behind each text block, compare with the luminance caps in 2.3 (A9 in the script ignores the canvas).
- M7 Zoom and reflow: 200 percent and 400 percent zoom, 320 px width, landscape phone 667 by 375, no clipped hero content, no horizontal scroll; text spacing override bookmarklet or CSS with no loss.
- M8 Contact form flow: submit empty, check summary focus, links move focus into fields, aria-invalid and aria-describedby, "Error:" text, valid submit shows "Not sent" with focus on the panel and values kept, no success wording.
- M9 Screen reader pass (at least one of NVDA with Firefox or Chrome, VoiceOver with Safari on iPhone, TalkBack): wordmark name, Menu, hero reading order including all four captions, area links, the six "Discuss this system" links, slot text, form errors, status panel. No assistive technology has been run at spec time.
- M10 Label in name (SC 2.5.3): the accessible name of each control contains its visible text. Can be semi-automated by reading accessibility tree names, but the script does not.
- M11 Target size 44 px project rule and 24 px at 768 and 1440, using Playwright bounding boxes in a separate check (the script only tests 375 for 24 px).
- M12 Forced colours and dark select popup by eye.
- M13 Flashing: record or step through the hero scroll sweep; no repeated flashes, glow inside the ring.
- M14 The company name and logo case: header and footer show text "Sinor Marine Technologies" (case A) or the supplied logo with alt text exactly "Sinor Marine Technologies" (case B), logo contrast numbers recorded, no file from assets/brand/sinor-logo.png, no other entity name in markup or alt.
- M15 Slots: count of [data-slot] and visible "NEEDED FROM RAHUL" per page, each announced as plain text, none focusable.
- M16 Page titles unique and descriptive (SC 2.4.2) and link purposes clear out of context (2.4.4): read by a person; the script only checks presence and length.
- M17 Consistent help (3.2.6) and consistent identification (3.2.4) across the five pages by comparing the header and footer markup.

## 14. Items for the Director
1. Menu label: keep "Menu" constant (this spec) rather than swapping to "Close" (sitemap.md allows swap).
2. Contact error summary and status panel: focus move without role="alert" or role="status" (wireframes.md allows both). Confirm.
3. Hero scrim covers the bottom, but text is at the top (section 2.3). The ui-designer or frontend-developer must change the layer or the gradient direction.
4. New token --c-error #FF8A80 for the ui-designer to add to the project tokens; confirm after QA runs the script in 2.4.
5. wireframes.md and sitemap.md still reference the repo logo file, the old entity line and a LinkedIn link; this spec overrides them, so the on-disk files should be corrected so frontend-developer is not misled.
6. Short viewport rule (static path below 560 px height) is new and affects the hero design.
7. Logo is a slot; the wordmark is text until a logo arrives.
8. Footer "Find us" had the LinkedIn link as the only real item; with none to show, Find us is slots only.
