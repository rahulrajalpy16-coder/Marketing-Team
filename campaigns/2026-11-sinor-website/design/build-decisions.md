# Build decisions (Director, 2026-11-07)

Settles the issues raised by the accessibility specialist and the earlier briefs. frontend-developer follows these over any older wording.

1. Entity: Sinor Marine Technologies. No FZCO, UAE, Middle East, Services LinkedIn page, or assets/brand/sinor-logo.png. Header and footer show a text wordmark (sentence case in HTML, capitals by CSS text-transform, letter-spaced, 14 px or larger) and slot S29 for the official logo.
2. Scrim: the token --c-scrim is transparent at the top, but the hero headline and buttons sit in the upper 45 percent of the stage. Add a top-weighted scrim layer under the hero text, for example linear-gradient(to bottom, rgba(5,10,18,.80) 0%, rgba(5,10,18,.55) 45%, rgba(5,10,18,0) 100%), and cap the canvas luminance behind text as a11y-spec.md section 2.3 says. Keep tokens.css unchanged and put the new layer in the site's own CSS.
3. Sticky stage: the stage uses min-height 560px. Below 560 px viewport height, and when text is zoomed to 200 percent, drop the runway and the scroll link and show the static composition so nothing is clipped.
4. Menu: keep the label "Menu" at all times (aria-expanded carries the state). Do not swap it to "Close".
5. Forms: on a failed submit move focus to the error summary; on a valid submit move focus to the "Not sent" panel. Do not add role="alert" or role="status" on top of the focus move.
6. Skip animation link: present in the Home tab order only while the scroll scene is active.
7. Home headline, titles and meta descriptions: titles and descriptions come from design/seo-spec.md once written; body text comes from copy/*.md word for word. Anything the fact check marks UNSUPPORTED or OVERSTATED is replaced by the reviewer's neutral wording that the Director approves.
8. No external requests at all. No fonts, scripts, analytics or images from other hosts. No og:image.
9. The canvas is decorative (aria-hidden) with all real text in the DOM. Static SVG fallback for no JavaScript and for prefers-reduced-motion.
10. Forms are not connected. The notice is visible text at 4.5 to 1 or better and says so in plain words.
