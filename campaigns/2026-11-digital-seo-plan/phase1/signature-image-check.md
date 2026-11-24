# Email signature image check (2026-11-24)

File checked: Jacob_Jose_Signature.htm (supplied by Rahul). File NOT modified.

## Result
- 13 image tags, all already hosted at https://sinormarine.com/signature/ (no data: images, no other domains, no CSS background images).
- All 13 return HTTP 200, content-type image/png, valid images. Plain http redirects to https. No hotlink block: works with no referrer, with a mail.google.com referrer, and with the Gmail image proxy user agent.
- Rendered in a browser at 700 px and 390 px wide: 0 broken images, 0 failed requests.
- Cache header: public, max-age 604800 (7 days). To replace an image later, keep the same name and add a new ?v= number in the file, as the Guidance Marine logo already does.

## Existing quality issues (left unchanged on purpose, "no layout change")
| Image | Real size | Shown at | Effect |
|---|---|---|---|
| logo-hd.png | 1238x675 | 230x150 | aspect ratio 1.83 shown as 1.53, about 20% vertical stretch; file is 204 KB |
| iso.png | 71x34 | 71x40 | about 17% vertical stretch, low resolution |
| imca.png | 40x34 | 40x40 | stretched, looks cropped at the right edge |
| icv.png | 63x34 | 63x40 | about 17% vertical stretch, low resolution |
| google.png, whatsapp.png | 24x24 | 30x30 | enlarged 25%, soft on screens |
| LinkedIn and six partner logos | match | match | fine |

## Content points for Rahul (not changed)
- The HTML title tag says "Shijitha Alex" while the signature shows Jacob Jose, likely a leftover. Not visible in email.
- "Accredited" block (ISO 9001 / 14001 / 45001, IMCA Member, ICV): certificates and memberships not seen by the team. Earlier rule: do not use ISO claims in public copy until Rahul confirms.
- SMT logo in the partner strip: same open question as the website strip (D4). Fugro, Sonardyne, Navis Engineering, Marine Technologies and Guidance Marine are the five confirmed partners.
- Linked images may be hidden by some mail programs until the reader allows pictures. That is normal for any signature that links images instead of embedding them.
