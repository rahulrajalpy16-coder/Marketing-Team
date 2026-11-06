# Design system proposal: cinematic dark (style study)

Status: PROPOSAL for the next project, pending Rahul's approval of the dark direction. Tokens live in tokens.css. Source of style: references/design-dna.md. Ratios below were computed 2026-11-06 with a Python WCAG 2.2 relative-luminance script.

## Colour and contrast (computed)
Text on surfaces (ratio, all pass 4.5:1 unless noted):
| Token | Hex | abyss #050A12 | deep #0A1626 | surface #101F33 | raise #16293F |
|---|---|---|---|---|---|
| text | #F2F6FA | 18.27 | 16.73 | 15.28 | 13.59 |
| muted | #A9B8C9 | 9.81 | 8.99 | 8.21 | 7.30 |
| faint | #8497AD | 6.62 | 6.07 | 5.54 | 4.93 |
| accent | #5BA4E0 | 7.40 | 6.78 | 6.19 | 5.50 |
| accent-hi | #8CC4F2 | 10.67 | 9.77 | 8.92 | 7.94 |
| steel | #7F9BB8 | 6.88 | 6.30 | 5.75 | 5.12 |
| glow | #F2A65A | 9.80 | 8.98 | 8.20 | 7.29 |
Other pairs:
- Button ink abyss on pill #F2F6FA: 18.27. On hover #FFFFFF: 19.84. On accent: 7.40. On accent-hi: 10.67.
- Focus ring accent-hi on deep: 9.77 (needs 3:1).
- Control border #6A86A5 on deep 4.82, on surface 4.40 (needs 3:1 for WCAG 1.4.11).
- Hairline #2A4260 on deep: 1.77. Decorative only, never the sole boundary of a control.
- Disabled text #6B7C90 on deep: 4.25. Disabled controls are exempt from the minimum but this token must never be used for live text.
- Brand navy #0D4A85: 8.99 on white, 2.02 on deep. Never as text or icon on dark.
- Reference note: the Scrollytelling grey #86868B measured 5.80 on #000 and 5.46 on #0A0A0A, so grey on black can pass; the risk is size and weight, not hex.
Rule: text over an image always sits on a scrim token; check against the lightest pixel behind it. Not computed here because no imagery exists yet.

## Logo on dark (inspected)
assets/brand/sinor-logo.png is 1041 x 396 RGB with an opaque white background (corner pixels 255,255,255). Placed on #080C14 it appears as a hard white rectangle; the blue wordmark and ellipse are legible but the box looks pasted. Resolution: show the logo on a white pill or rounded plate (radius --r-md, padding 8 by 16 px) in the nav and footer. Do not recolour, invert or crop it. The Drive white variant is uninspected; ask Rahul before use.

## Type
- Display: serif stack (Iowan Old Style, Palatino, Georgia). Matches the editorial feel of reference 1 without a font file. Body and UI: system sans. No CDN.
- Optional upgrade needing Rahul's approval and a licence check: a self-hosted variable serif and sans (woff2, each under 100 KB subsetted). Do not add without approval.
- Scale (tokens): body --fs-0 16 to 18 px; --fs-1 18 to 22; --fs-2 22 to 30; --fs-3 30 to 48; --fs-4 40 to 80; --fs-hero 44 to 120 px. Line height 1.02 hero, 1.12 headings, 1.6 body. Hero tracking -0.025em. Labels 13 px, uppercase, 0.14em tracking, weight 600, never used for paragraphs.
- Hero headline: two to five words, max-width 14ch at 375 px, center or left per layout.

## Spacing, radii, shadows, breakpoints
- Spacing 4 px base: 4, 8, 12, 16, 24, 32, 48, 64, 96, 144. Section padding clamp(64px, 12vw, 144px).
- Layout max width 1200 px, text 62ch, gutter 20 to 48 px.
- Radii 8, 14, 24, pill 999.
- Shadows: card, pill, one soft blue glow. No more than one glow per viewport.
- Breakpoints 480, 768, 1024, 1440. Mobile first. Verify no horizontal scroll at 375, 768, 1440.

## Components
Nav
- Height 64 px, transparent over hero with --c-scrim behind, becomes --c-deep with hairline after 40 px scroll (or always, if no JS). Logo on white plate left; links uppercase 13 px, 0.14em tracking, --c-muted; one pill CTA right.
- Hover: link text to --c-text, underline 1 px offset 6 px. Focus: 2 px --c-focus outline, 3 px offset, never removed. Active page: --c-text plus underline.
- Mobile: links collapse into a native button toggling a full-width panel (aria-expanded), 44 px rows. Disabled links are not used in nav.
Hero
- Min height 100svh, content stack: label (optional), headline, one line of support (max 2 lines at 1440), one primary pill. Visual: one optimised image under 300 KB (navy-graded vessel photo or SVG chart motif). Scrim token below text. h1 appears once.
- Static state is the default; motion is enhancement (see below).
Pill button (primary)
- Height 48 px (44 minimum), padding 0 28 px, radius pill, bg --c-text, ink --c-abyss, label 13 px uppercase 0.12em weight 600, shadow --sh-pill.
- Hover: bg #FFFFFF, translateY(-1px). Active: translateY(0), bg #E4EBF2. Focus: 2 px --c-focus ring, 3 px offset. Disabled: bg --c-raise, text --c-disabled-text, no shadow, cursor not-allowed, aria-disabled.
- Secondary: transparent, 1 px --c-control-border, text --c-text; hover bg --c-surface; same focus and disabled rules.
Card
- bg --c-surface, radius --r-md, padding 24 px, shadow --sh-card, hairline top highlight. Title --fs-1 display, body --c-muted.
- Hover (only if the card is a link): bg --c-raise, border --c-control-border, no movement beyond 2 px. Focus-within: same ring as buttons. Disabled: not applicable, use a plain card.
Forms (for completeness)
- Input bg --c-deep, 1 px --c-control-border, radius --r-sm, height 48 px, text --c-text, placeholder --c-faint. Hover border --c-accent. Focus 2 px --c-focus. Error border and text use a warm red that must be computed when used. Disabled: bg --c-raise, text --c-disabled-text. Form stays unconnected until Rahul approves an endpoint.
Footer
- bg --c-abyss, hairline top, logo on white plate, link columns in --c-muted, hover --c-text underline, focus ring as nav. Legal text --c-faint at 14 px or larger. No invented certifications or partner logos.

## Motion spec (enhancement only)
Principle: content is complete and readable with no motion and without JS.
- Default (no-preference only): sections fade and rise 16 px over --dur-slow with --ease as they enter; hero visual shifts up to 24 px with scroll (parallax) using CSS animation-timeline: view() where supported, otherwise IntersectionObserver adding a class. No scroll hijacking, no smooth-scroll library, no autoplay audio or video.
- Budget: animate only transform and opacity; no layout-shifting animation (CLS 0.1 or less); no animation that blocks first paint (LCP 2.5 s or less); INP 200 ms or less so no heavy scroll handlers.
- Reduced motion: wrap all of the above in @media (prefers-reduced-motion: no-preference). With reduce, everything renders in its final position, no parallax, no fades, hover transitions 0.01 ms. Test with the emulated setting.
- Pause: any loop longer than 5 s needs a visible pause control (WCAG 2.2.2).
- 3D or WebGL (references): NOT in the default stack. Needs Rahul's approval, a stated reason, self-hosted library, a still-image fallback, and a recheck of the 1.5 MB budget. A rendered still or short image sequence is the safer route.

## Not verified
Real scroll behaviour of all three references, hover states, mobile layouts of pins 2 and 3, and contrast over real imagery. Tokens have not been built into a page or tested in a browser.
