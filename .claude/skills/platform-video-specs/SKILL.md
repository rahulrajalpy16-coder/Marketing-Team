---
name: platform-video-specs
description: Use before planning or rendering any video, image or carousel for a named platform. Explains how to choose and verify format, resolution, length and safe zones, and how to keep brain/platform-specs.md current.
---
# Platform video specs

1. Read brain/platform-specs.md for the platform and note its "last verified" date and status.
2. If the entry is missing, marked unverified, or older than 30 days, and the spec affects the deliverable, look up the current official documentation (WebSearch, WebFetch). Record the value, the source URL and today's date. Tell Rahul only if something changed in a way that matters.
3. If official docs cannot be reached, use the starting points in the entry, label them "unverified" and say so in the handoff.
4. Choose the aspect ratio from the source footage and story, not by habit. Prefer the ratio that fills the mobile feed when the footage allows it. Never crop away faces or key equipment to force a ratio.
5. Set resolution, frame rate (match the source unless the platform requires otherwise), duration, caption length, subtitle style, cover image and file size from the verified spec.
6. Keep titles and faces inside the interface-safe zone. Check readability at phone size.
7. Check whether the platform allows the planned combination in one post (for example photos plus video). If not, offer a supported alternative.
8. Several platforms means separate versions: different crop, pacing, hook, caption, thumbnail and CTA.
9. Target length, hook timing and posting time are hypotheses to test, never rules. Never promise reach.

Export defaults (adjust to the verified spec): MP4, libx264, yuv420p, AAC 48 kHz stereo about 192 kbps, -movflags +faststart, constant frame rate, CRF about 18 to 21 for finals, about -14 LUFS integrated with true peak at or below -1 dBTP as a starting point.
