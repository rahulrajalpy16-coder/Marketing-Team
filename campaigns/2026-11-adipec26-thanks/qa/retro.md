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

## Extra revision cycles
Two video revisions (v1 to v2 to v3), the maximum of three QA cycles. One caption wording fix after copy QA (checked by script by the Director, not re-reviewed by a separate reviewer).

## What took time
- 7 of 16 photos are HEIC with depth maps that no installed tool can decode.
- Partner names were dictated roughly and needed a fact check.

## What worked
- Drive connector downloads of originals (byte-exact, 16 of 16).
- Rahul's earlier repos supplied the approved logo and context for partner names.
- Building the video from a script (build_video.py) so v2 was a quick rebuild.

## Scope honesty
- Photos inspected: 9 of 16 (the 9 JPGs). 7 HEIC not inspected.
- The video was reviewed through sampled frames and full-file ffprobe, black and freeze detection. Nobody listened to the audio (it is silent by design) and it was not played on a phone.
- Comparable LinkedIn post research (Part 10) was NOT done for this job; effort scaled to a quick thank-you post.
