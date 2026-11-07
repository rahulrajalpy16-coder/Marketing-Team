# Retro: ADIPEC 2026 thank-you post (v1 and v2), 2026-11-06

## What Rahul approved
Nothing yet. Drafts only. He asked for a thank-you post plus a video from the currently available photos and said it will be corrected later when the rest of the Drive upload arrives.

## What Rahul corrected
Nothing yet.

## What QA caught
- Copy QA (independent): PASS with open items. Partner names NAVIS and Marine Technologies are inferences; personal versus company account unanswered; "ADIPEC 2026" repeated in hook and first sentence (fixed).
- Video QA cycle 1 (independent): spec PASS; low defects: pill touching hair, collage seam and blurred face, marginal small text, tight bottom margin, two captions slightly over-claiming. All fixed in v2.
- Director self-review before QA caught: "our DP console" (ownership not confirmed) and "Four days of real conversations" (assumes Rahul attended all days). Fixed in the caption.
- Video QA cycle 2 (independent): new medium defect, a media file name readable on the stand TV in one photo (that photo held back), plus a collage border and text inside the bottom 150 px. Fixed in v3.
- Video QA cycle 3 (independent): technically PASS, D5, D9, D10 fixed; only the unconfirmed partner names remain (needs Rahul).

## After Rahul's correction (trend and template research)
Rahul pointed out that trending formats and templates were not checked. Research was run (research/research.md), then the video was rebuilt: v4 added slow motion on photos, tighter pacing, a 9:16 alternative and story-first opening. Independent QA caught stepped judder from ffmpeg zoompan (integer pixel rounding); v5 renders the motion with sub-pixel sampling. Measured frame-to-frame change became uniform. v5 passes technically in both ratios; only the unconfirmed partner names block publishing.

## Extra revision cycles
Two video revisions (v1 to v2 to v3), the maximum of three QA cycles. One caption wording fix after copy QA (checked by script by the Director, not re-reviewed by a separate reviewer).

## What took time
- 7 of 16 photos are HEIC with depth maps that no installed tool can decode.
- Partner names were dictated roughly and needed a fact check.

## What worked
- Independent QA found a real motion defect that a contact sheet could not show; measuring it (phase correlation) was the right fix check.
- Drive connector downloads of originals (byte-exact, 16 of 16).
- Rahul's earlier repos supplied the approved logo and context for partner names.
- Building the video from a script (build_video.py) so v2 was a quick rebuild.

## Scope honesty
- Photos inspected: 9 of 16 (the 9 JPGs). 7 HEIC not inspected.
- The video was reviewed through sampled frames and full-file ffprobe, black and freeze detection. Nobody listened to the audio (it is silent by design) and it was not played on a phone.
- Comparable LinkedIn post research (Part 10) was NOT done for this job; effort scaled to a quick thank-you post.

## Update after Rahul's answers (company page, Guidance Marine, all photos)
- Rahul confirmed partners, chose the company page, added Guidance Marine, approved HEIC tooling, the file-name photo and the panel figures. Folder grew to 21 photos while I worked (5 HEIC arrived mid-job).
- v6/v7: 8 beats, 29.8 s, 11 photos, split-screen pairs, five-partner end card. Independent QA (video v6, v7; company caption) all pass; defects found and fixed: 9x16 NAVIS caption over the logo, pair headroom.
- Still open: Rahul to play both files once; optional "Navis Engineering" spelling and partner order; Fugro and Guidance Marine have no photo yet.

## v8 to v10 (logos, Rahul's sequence feedback)
- Rahul supplied five partner logos and asked for full spelling: end card rebuilt with white logo tiles and full names (v8). Rahul then asked for the team photo first, then the thank-you title, and sharper captions, and said the woman in one photo represents Guidance Marine (v10). Independent QA passed v8 and v10 (both ratios).
- Correction of my own claim: I said trimming the logos' empty margins made them larger. QA showed the source files have no empty margin, so the end card did not change; the Fugro mark is simply small because its shape is wide. Lesson: check a claimed visual change by diffing before reporting it.
- Interpretation to confirm with Rahul: the "full Sinor Marine team photo" was read as the group of four at the stand.

## Template-inspired designs (mosaic, kinetic, promo)
- Rahul supplied three Pinterest pins (After Effects template previews) and asked for the same content in each style. Each pin's video was downloaded for analysis only; the designs were drawn from scratch with the event photos (build_video_mosaic.py, build_video_styles.py). Independent QA passed all four files technically; defects it found were fixed: over-claiming labels (TEAMWORK, TEAM chip, three captions), letter overlap in kinetic words, stepped blur in promo, a 1 px line and orphan words, small sub-text, half-empty 9:16 end card.
- Cosmetic fixes made after that QA (kinetic, promo, 9:16 mosaic) were verified by me through ffprobe, frame inspection and pixel checks, NOT re-reviewed by a separate reviewer. The 4:5 mosaic file was the one reviewed exactly as delivered.
- Open for Rahul: comfort with recognisable visitor faces and other companies' signage in the blurred background tiles (mosaic, promo; the kinetic design shows none); promo "VISITORS"/"PARTNERS" labels; 9:16 only exists for the mosaic design.
- Process note: two worker restarts (out-of-memory) happened when several heavy jobs ran together; run renders one at a time.

## 16:9 template recreations (clean, dynamic, promo), 2026-11-07
- Rahul: "I want the same template edited videos like all the links I gave." The earlier 4:5 versions were only inspired by the templates. Studied the three reference previews frame by frame (ghost background and 3D whip; letter-by-letter words, colour frames, text-as-window; navy duotone, aqua chips, photo wall) and rebuilt each in the templates' native 16:9 (build_video_templates16x9.py).
- HONEST LIMITS: the originals are paid After Effects projects that cannot be used or run here, so these are recreations, not the templates. QA fidelity ranking: clean (closest), promo, dynamic (weakest: the template's multi-colour palette was replaced by brand navy/cream, so it feels much less colourful; no 3D depth, aerial footage or light leaks).
- QA found and I fixed: NAVIS caption cut and covering the logo (clean), giant words covering faces (dynamic), orphan caption words (promo), end-card heading touching tiles, dark window-title photo. Independent re-check passed all three. One later change (dynamic NAVIS word moved off the logo) was verified by me with a frame check, not re-reviewed independently.
- Open: neighbouring-stand brands, visitor faces and partly legible badges are visible in all three (Rahul to decide); soft full-bleed crops because source photos are about 1200 px wide (higher-resolution originals would help).

## Photo-wall reels v1/v2 (2026-11-07)
- Request: recreate Rahul's two compressed clips in high quality with modern captions and LinkedIn-suitable audio.
- Built from original photos (not upscaled); audio is an original generated bed (cannot be listened to by me).
- Independent QA (qa_photowall_v2.md): technical gate passed; majors D-01 title over faces, D-02 low-contrast subtitle, D-05 over-claiming caption. Fixed; re-check was mine only.
- Open minor items: "The Sinor Marine team" caption shows while the team tile is not featured; "Visitors"/"Together" are vague; Sinor logo chip near top 150 px; neighbouring-stand brands visible; 9:16 used though the original brief said 4:5 (Rahul's clips are 9:16).
- Learning: B) a full-bleed opening title needs a strong veil (about 0.7) to protect faces and contrast; captions must not name a team over an unverified photo.

## Photo-wall v3/v4 final corrections (2026-11-07)
- Rahul's list: transparent logo, staff photos in the opening, supplied SPRINT-Nav close-up and Sonardyne group photo, partner logos on captions, "Together" changed to "Visitors" with supplied group photo, more professional look, LinkedIn-ready.
- QA v3 blockers: logo box (halo looked like a rectangle) and true peak 0.0 dBTP (AAC overs after loudnorm). Fixed (scrim instead of halo; loudnorm TP -3 plus alimiter, final -1.9 dBTP). Independent re-check passed.
- Lessons (B, provisional): a halo behind a block of text reads as a box, use a gradient scrim; check true peak AFTER the AAC encode, not on the WAV; transparent logo from a white-background JPG needs a noise threshold on alpha.
- Open: group photo above SPRINT-Nav hero cropped (minor), logo contrast on dark tiles, Visitors identity, audio not listened to by me.
