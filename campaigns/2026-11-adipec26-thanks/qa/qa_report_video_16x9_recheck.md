# QA recheck: three 16:9 videos after fixes (v14 files overwritten)

Reviewer: qa-reviewer (independent). Date 2026-11-07. Files in /tmp/work/adipec26. New SHA-256 (first 16): clean 1764f724d374ffe4 (14,842,592 B), dynamic 7352c204947b8ca2 (6,732,102 B), promo 8a639946113de587 (19,797,950 B). These differ from the first QA, so the files are the re-rendered ones.

## True scope
- Scripted on whole files, one at a time: ffprobe, moov position, blackdetect (d=0.1, 320 px decode), volumedetect.
- Frames viewed at FULL 1920x1080, one image each: clean 12.2 s (NAVIS) and 3.6 s (title) and 29 s (end card); dynamic 3.6 (title), 10.3 (VISITORS), 12.6 (NAVIS/TECHNOLOGY), 18.0 (MT/PARTNERS), 22.2 (WELCOME), 29 (end); promo 15.3 (Sonardyne), 18.0 (Marine Technologies), 22.2 (Guidance), 29 (end). First frames (t=0) of all three viewed at 640 px wide in a contact row.
- NOT redone: freezedetect, transitions and motion series, loudness_check.py, logo aspect measurement (end cards judged by eye only), other beats (clean beats 1 to 4 and 6 to 9, dynamic beats 1 to 3 and 5 to 6, promo beats 1 to 7 other than those listed). Not played in real time, not on a phone, audio is silent and was not listened to. Face checks are my visual judgement of single frames mid-beat; the tilted card and word are static after build, but I did not view the word at the moment it builds.
- Scratch images: /home/user/Marketing-Team/campaigns/2026-11-adipec26-thanks/qa/scratch16r/ (each under 150 KB).

## 1. CL-1 clean NAVIS beat (frame 12.2 s): FIXED
Navy plate now sits below the portrait hero: plate x 772 to 1172, y 869 to 980. Text "ADIPEC 2026 · ABU DHABI" and "NAVIS console" are complete, last letter "e" at about x 1138, 34 px inside the plate edge. The hero ends at y 865, so the plate does not cover the NAVIS Engineering logo (visible at x 880 to 1000, y 685 to 775). Plate bottom 980 is above the 1010 safe line. Plate is about 24 px wider than the hero on the right (cosmetic, not a defect).

## 2. DY-1 giant word versus faces (full frames)
| Beat | Word band (y) | What it crosses | Faces covered |
|---|---|---|---|
| WELCOME (22.2 s) | 625 to 790 | necks, torsos, lanyards, badges of both people, QR badge; card edge and white wall at right | none (woman's chin about 620 and man's chin about 620 sit just above the top of the letters) |
| VISITORS (10.3 s) | 615 to 785 | shoulders, coveralls and backs of heads' lower part, tote bag; ghutra man's torso | none (all faces end above about 530) |
| PARTNERS, Marine Technologies (18.0 s) | 610 to 770 | jackets, badges, desk, the MT desk plate | none (faces at y 340 to 440) |
| TECHNOLOGY, NAVIS (12.6 s) | 645 to 770 | console body, console base and the NAVIS Engineering logo on it, white card border | no faces in the photo |
DY-1 is FIXED. The word no longer sits on any face. Caption line (y 935 to 985) is clear of the word and the card on all four.

## 3. DY-4 title window letters (3.6 s): IMPROVED, acceptable
Letters now show faces: T/H/A/N/K/Y/O/U each contain at least one recognisable face (A: two, N: two, K: one, O and U: one each). Photo is soft and some letters show lanyards or screens (T, H partly), but the reveal now reads as people. Closed as fixed; softness remains (see DY-2).

## 4. PR-1 promo captions: FIXED
Sonardyne: "Sonardyne SPRINT-Nav / on the stand" (two lines). Marine Technologies: "Marine Technologies / on the stand". Guidance: "With Guidance / Marine at our stand". Two lines each, no orphan word. Right edge of longest line about 1795 px, inside the margin. Info box bottom 705 (Guidance), well clear.

## 5. CL-2 clean title (3.6 s): FIXED
"Thank you." spans x 497 to 1415 inside a panel x 420 to 1497, so 77 px left and 82 px right clearance. Evenly spaced.

## 6. Regression
| Check | clean | dynamic | promo |
|---|---|---|---|
| Video | H.264 High yuv420p 1920x1080 25 fps, 794 frames | same | same |
| Audio | AAC LC 48 kHz stereo, -91.0 dB (silent) | same | same |
| Duration | 31.76 s (video), audio 31.75 s | same | same |
| moov before mdat | yes (offset 40) | yes | yes |
| blackdetect | none | none | none |
| First frame content | team photo, caption, tiles, logo | team photo, "OUR TEAM", caption | framed photo, TEAM chip, caption |
| End card | logos look undistorted; "Thank you" right edge about 920, tiles start 1014 (94 px gap); lowest text about 860 | heading right edge 915, tiles from 1020; lowest text about 860 | same as dynamic |
End-card logos (5 partners plus Sinor) judged undistorted by eye; aspect not re-measured. Name labels read: Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine. All text in sampled frames is inside the 70 px bottom margin (lowest: dynamic captions about 985, clean NAVIS plate 980).

## 7. New or remaining observations
| ID | Severity | File, location | Detail | Owner |
|---|---|---|---|---|
| DY-5 | Minor (new) | dynamic WELCOME (22.2 s) | Right-hand "E" and left "W" of the cream-tinted word sit on the cream card shadow and white wall; low contrast on those two letters, still readable. | video producer |
| DY-6 | Minor (new) | dynamic TECHNOLOGY (12.6 s) | White "N" and "O" cover most of the NAVIS Engineering logo on the console (the product branding is hidden behind letters). Not a fidelity or safety issue; flag to Director. | video producer |
| DY-3 | Minor (persists) | dynamic TECHNOLOGY | White "H" and "L" lose their edge where they cross the white card border. | video producer |
| DY-2 | Minor (persists, not rechecked) | dynamic title and beats 1 to 3 | Soft upscaled crops. Window letters are soft too. | video producer |
| FD-1, FD-2, FD-3, ALL-1 | Notes (unchanged) | all | Template fidelity gaps and visible neighbouring brands and visitor faces: Director to disclose or ask Rahul. | Director |
No plate-over-margin or word-over-caption problem was introduced. No em dashes seen on screen.

## Verdicts (within the scope above)
- clean v14: PASS on rechecked items (CL-1 and CL-2 fixed). Unviewed beats assumed unchanged, not verified.
- dynamic v14: PASS with minor items (DY-1 and DY-4 fixed; DY-5, DY-6, DY-3, DY-2 remain).
- promo v14: PASS (PR-1 fixed).

## Candidate lessons for the Director
1. Face-avoidance placement worked when the word was placed at a fixed fraction of the card; keep checking each new photo, since one crop change shifts faces.
2. White display words need a contrast check against card borders and cream shadows.
3. Do not cover the partner product branding with decorative words when the beat is about that product.
