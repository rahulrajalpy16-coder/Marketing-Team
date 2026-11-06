# Design DNA: cinematic dark scroll style

Study date: 2026-11-06. Type: style study, not a client site. Author: ui-designer.
Hex values read from images are APPROXIMATE (eyeballed from compressed stills, two of them photos of a screen, so camera and screen glare shift colour). Only the Scrollytelling live-page numbers marked MEASURED come from page source.

## What was and was not seen
- Pin 1 (Scrollytelling): still photo of a laptop, plus a live first-viewport screenshot of https://scrollytelling.ai/ taken 2026-11-06 with headless Google Chrome at 1440 x 900 and 375 x 812 (Playwright is not installed; I did not install it). Page source was also read. Only the first screen was captured. Scroll motion was NOT seen.
- Pin 2 (Flowty via a gallery tile): one still. The Flowty site itself was not opened.
- Pin 3 (unnamed site, TikTok credit): one still photo of a monitor, tilted, dim. Site not identified.
- Motion, scroll behaviour, hover states, mobile layout of pins 2 and 3, and page structure below the hero were NOT seen. Anything about them is inference.
- Third-party screenshots are in /tmp, not in the repo.

## Style statement
A near-black stage with one luminous focal object (rocket, phone, particle form) behind or beside a very large, confident headline. Almost no chrome: tiny uppercase nav, one or two small pill buttons, short body copy. Colour comes from the hero object and a single glow, not from the interface. The feel is a film title card that you scroll through.

## Reference 1: scrollytelling.ai (pin 1)
OBSERVED
- Palette (approx, from image): background black #000000 to #0A0A0A; text white #FFFFFF; hero glow orange to amber #F28A3C, ember red #C0391F, deep blue-violet sky #1B1F5C; pill button white. MEASURED from page source: most frequent colours #FFFFFF, #000000, #86868B (grey), #2D2D2F, #0A0A0A.
- Type: huge high-contrast serif display headline in white, tight tracking, mixed case. Sub-headline also serif, large (about 36 px at 1440 in screenshot). Nav and buttons in small uppercase sans with wide letter spacing. Page source declares Inter, a Fraunces/Instrument Serif/Georgia stack, and Space Grotesk; which is used where on the hero was not tested.
- Layout: full-viewport hero, centred text stack over a full-bleed image, thin top bar with logo left, four links centred, one pill right, hairline under the bar. Headline wraps to two lines at 375 px, sub-headline to four.
- Hero pattern: centred headline, sub-headline, one pill CTA, over a lit launch scene; a darkening gradient behind text.
- Buttons and nav: white filled pill with black uppercase label, soft shadow; nav links uppercase, small, no underline in the still.
- Imagery: single cinematic photo-real or rendered scene (rocket on launch pad), strong central light source. Page source includes canvas elements and references to GSAP and Lenis; a prefers-reduced-motion rule exists somewhere in the source. I did not test what it does.
- Density: very low. Tone: bold claim with a number ("17x better"), which I will not reuse.
INFERRED
- Serif plus dark reads as "editorial, premium, storytelling". Targets product marketers who want drama.
- The hero text sits over a bright glow, so contrast under the sub-headline is probably weak at the glow centre (the screenshot shows the white text crossing the brightest area). Not measured.

## Reference 2: Flowty tile on details.so (pin 2)
OBSERVED
- Palette (approx): background #000000 to #0B0B10; headline light grey-lavender #C9C6D6; purple diagonal glow #4B3A78 fading to #1A1530; phone body graphite #1E1E22; pill button pale grey #D8D6E0 with dark label; secondary text mid grey #8A8A92.
- Type: large light-weight geometric sans (round letterforms) headline, sentence case, anchored bottom-left and cropped by the frame. Small body in the same family at roughly 10 to 11 px equivalent in the still.
- Layout: asymmetric. Text and CTA left, 3D object right of centre, a small floating info card top right, headline bottom left. Card has rounded corners (about 12 px) and a hairline border.
- Hero pattern: object-led, off-centre. Two small pill buttons plus a small icon button.
- Imagery: one rendered 3D product (a dark phone) lit by a coloured diagonal beam. No photography.
- Density: low to medium. Tone: calm, quiet.
INFERRED
- Light weight type on black can lose legibility at small sizes; the body copy in the still is very small and grey. A product-demo mood aimed at consumer apps.

## Reference 3: unnamed 3D site (pin 3)
OBSERVED
- Palette (approx, camera-affected): background near-black blue #05070D; star dots white; particle form orange #E8A33D and blue #6FA3E0 with white core; headline white with a light outline; small body text light grey with bold white keywords.
- Type: tall condensed bold sans, uppercase, stacked on three short lines, with an outline on the first line; body in a regular sans at small size with bold keywords. Tiny top-right nav: text links plus a menu icon.
- Layout: headline and body in left third, 3D object filling the right two thirds, tilt of the photo is the camera, not the design.
- Hero pattern: object-led particle form (a rocket drawn from many dots) on a starfield, small round icon beside the headline.
- Imagery: generative particle object, starfield. Motion unknown.
- Density: low. Tone: energetic, agency showreel. Claim copy is generic.
INFERRED
- Two-tone particle colours (warm and cool) give depth with no gradients. Condensed uppercase headline is a distinctive choice and I will not copy it.

## What all three SHARE (the real style signal)
1. Near-black background, no light mode in the hero.
2. One dominant focal object or scene carrying all the colour; the interface itself is monochrome.
3. Very large display headline, short (two to four words), with generous empty space.
4. Tiny, quiet nav and small pill-shaped buttons; no heavy bars, no banners.
5. Short supporting copy, one primary action.
6. Object is 3D or cinematic, and (INFERRED from the recording format) is tied to scroll.
7. Glow or beam of one colour used as light, not decoration.

## Differences
- Headline type: serif (1), light round sans (2), condensed bold uppercase (3).
- Composition: centred (1), asymmetric (2), left text right object (3).
- Object origin: photographic scene (1), rendered product (2), generative particles (3).
- Accent: warm orange (1), purple (2), orange and blue (3).

## Do
- Use a deep navy-black stage, not pure black, so the Sinor blues belong to it.
- Keep one focal visual per section and one accent colour at a time.
- Use a very large headline of few words; keep the supporting line short.
- Use small pill buttons with clear text labels and a visible keyboard focus ring.
- Put a solid or gradient scrim behind any text that sits over imagery.
- Provide a static (no-motion) version of every animated section.
- Use only supplied or properly licensed imagery.

## Do not
- Do not copy a reference's headline, layout, rocket, phone or particle object, or colour set.
- Do not use claim numbers like "17x" or any invented statistic.
- Do not put body text on the brightest part of a glow.
- Do not rely on scroll animation to reveal content that is not otherwise in the DOM.
- Do not use text below 4.5:1 (3:1 for large) or text under about 14 px for body copy.
- Do not use the logo on dark as-is (see conflicts).
- Do not load fonts, libraries or video from a CDN.

## Conflicts and how to resolve
| Conflict | Resolution |
|---|---|
| Sinor default is navy and white, light first; references are dark | Dark is a proposal for Rahul to approve. Build as "dark stage sections" inside a light-compatible system: tokens support both. Open question stays with the Director. |
| Official logo has an opaque white background (inspected: shows as a white rectangle on navy-black) | Place the logo on a white or very light plate (pill or rounded rectangle) in the nav, or use the white variant in Drive once Rahul supplies and approves it. Never recolour or edit the logo. |
| Small grey light-weight text on black fails or nears 4.5:1 | Use tokens with computed ratios (see design-system.md). Minimum body 16 px, weight 400 or higher. |
| Text over glowing imagery | Scrim layer plus text on a token background; check ratio against the lightest pixel behind text. |
| Default stack forbids framework and CDN; references use GSAP, Lenis, WebGL canvas | Default to CSS only: scroll-driven CSS (animation-timeline) with a static fallback, IntersectionObserver with a small vanilla script. GSAP, Three.js or self-hosted video need Rahul's approval and a stated reason. |
| 1.5 MB page budget and LCP 2.5 s | Hero visual must be an optimised image under 300 KB (AVIF or WebP plus JPEG fallback, or SVG). No video in the repo. 3D models and canvas count toward the budget. If not achievable, use a poster image only. |
| prefers-reduced-motion | Every animation wrapped in a no-preference media query; reduced motion shows the final static state, no parallax, no autoplay. Provide the full content without scrolling effects. |
| Pointer target and focus | Pills at least 44 px tall on touch; focus ring 3:1 against its background. |
| No invented facts or partner logos | Hero visuals must be supplied photography or neutral abstract graphics; no fake certifications, clients or numbers. |

## Adapting the style for a marine and offshore company (no invented facts)
- Replace space with night sea: deep navy-black, a horizon line, a single cool light (vessel deck lights, a lighthouse-like beam, sonar-style ring) as the "focal glow".
- Focal object should be real: a supplied photograph of a vessel, bridge, DP console or thruster, graded to navy, with a scrim. If none exists, use an abstract SVG of a chart grid, bathymetric contour lines or a vessel outline drawn in steel blue. Mark NEEDED FROM RAHUL for photos.
- Scroll story idea (structure only, content to be confirmed): one scene per service area Rahul has stated (Dynamic Positioning, reference systems, marine electrical and automation, propulsion and thruster controls, integration, upgrades, commissioning, service, support). No client names, projects, numbers or certifications until confirmed.
- Headline voice: short, factual, calm. Replace hype ("boost", "kill") with plain statements. Tone stays confident and accurate per the brand profile.
- Keep an optional light variant: the same tokens inverted, so the corporate navy and white look is still available.

## Source notes
- scrollytelling.ai: pin https://pin.it/6mizOnKak, live page captured 2026-11-06 (first viewport only), via headless Chrome.
- Flowty via details.so tile: pin https://pin.it/7pXE3pxNY, still viewed 2026-11-06; gallery https://www.details.so/inspo/flowty-f0ddcc not reopened by me.
- Unnamed: pin https://pin.it/1skTsyhdi, still viewed 2026-11-06; credit in pin text to a TikTok creator.
