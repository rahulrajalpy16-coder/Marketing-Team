# QA report v2: Sinor Products Catalogue 2026 (DRAFT v2, A4, 26 pages)

Reviewer: independent qa-reviewer (did not produce the PDF). Date: 2026-11-11. File: /tmp/work/products-brochure/brochure_v2.pdf (4.58 MB, 26 pages, A4 595 x 842 pt, Chromium/Skia, Inter fonts embedded as Type 3).

Verdict: PASS WITH DEFECTS. Blockers 0, major 6, minor 26. Structure, numbering and rules are sound. The majors are mostly photo branding, unsupported lifecycle or maker claims, and one printed contradiction on the MRU page. They should be fixed or decided before it goes to Rahul as a final.

## Verification scope (what was and was not done)
- Rendered all 26 pages with pdftoppm at 80 dpi into /tmp/work/products-brochure/qa2_pages/ and viewed every page image (26 of 26). One 200 dpi crop of page 2 header. 80 dpi judges layout and clipping, not print sharpness.
- Photos: built 4 contact sheets of all 50 originals in img_ready (labelled with ref, old_id, pixel size) and viewed them; opened C01 (DP-03), D09 (SP-09) and B03 (PR-17) at full size. Compared each card photo on its page with the original. Cards without a photo checked against images_needed.csv.
- Facts: script check of all 65 cards: every number/model token in each card (description, features, specs) was searched in that item's evidence in results/slice1-5.json, r2_a/b/c.json and extra_items.json (0 missing). Second script: every number/model token in the final PDF text of pages 4-24 searched in the whole evidence corpus plus catalogue_v2.json, register_text and dp_sources.md (3 hits, all line-break artefacts: 20-0306, 750-552, 758-873). Then I read brand_note and notes of all 65 cards for flags and compared printed claims with them. About 40 cards read semantically (all 3 DP, all 3 MRU, PR-01 to PR-21, SN-04 to SN-08, CA-01, 02, 07, 08, 09, 10, 11, 12, 14, 15, 18, 23, 24, SP-01, 02, 05, 09).
- Independent external check: one only. I fetched inertiallabs.com MRU page (HTTP 200); its model table confirms B1 = Heave, Surge and Sway; B1.1 = Pitch and Roll; B2 = Heave, Surge, Sway, Pitch and Roll. Sonardyne and Guidance Marine pages returned 403 from the proxy. So for all other cards "supported" means traceable to the team's evidence files, NOT re-verified against the vendor page. Whether the evidence files themselves are accurate was not independently checked.
- Page references: script check, 65 of 65 refs have the same page in the card page text, the section opener list and the item index.
- Rules: grep for em and en dashes, price, authorised, dealer, vessel names, contact details on the PDF text; read cover, contents and back page. Compared DP-page wording with the Sinor profile brochure (/tmp/work/products-brochure/ref/profile_v2.pdf, text extracted) and dp_sources.md.
- Not done: no print proof, bleed or colour check; no check that the product list is complete against the job register; no live check that claims are current; Chromium Type 3 fonts (poppler prints "Bad bounding box in Type 3 glyph" warnings) not judged beyond noting them.

## 1. Structure, headings, page numbers: PASS
- Order delivered: 1 DP Systems (p03), 2 Position Reference Systems (p07), 3 Position Reference Sensors (p14), 4 Control, HMI and automation (p17), 5 Power, spares and service kits (p22), Item index (p25), back cover (p26). Matches Rahul's order and headings.
- Section 1 holds only NAVIS (DP-01, DP-03) and Marine Technologies (DP-02); no "package" section.
- Section 2 starts with radar and laser (RadaScan View, Mini RadaScan, CyScan, SceneScan, Artemis, RADius, Fanbeam), then acoustic/inertial (Ranger 2 USBL, NSH, SPRINT-Nav DP), taut wire, GNSS and targets/transponders.
- Section 3 has both B types: SN-01 MRU-B1 (heave), SN-02 MRU-B1.1 (pitch and roll), SN-03 MRU-B2 (heave, surge, sway, pitch, roll); then gyro, wind sensors, GNSS antenna.
- Counts in contents (3, 21, 8, 24, 9 = 65) match the cards. Footers 02 to 25 correct; cover and back page unnumbered.
- Opener lists and index page numbers all match real card pages.

## 2. Page-by-page layout (all 26 viewed)
No clipped, overlapping or unreadable text, no broken or empty pages. Notes:
- L1 (minor, p06): page holds one small card (DP-03) and is about 80 percent empty. Owner: art-director.
- L2 (minor, p16, p24, also bottom of p04, p05): 2 to 3 cards then a large empty area; looks unfinished. Owner: art-director.
- L3 (minor, all inner pages): the section label under the logo (for example "CONTENTS", "POSITION REFERENCE SYSTEMS") touches the bottom edge of the logo plate at the top left; cramped though not overlapping. Owner: art-director.
- L4 (minor, whole document): smallest text 5.6 to 7 pt (spec rows, supplied models line, footers, back-page disclaimer). Small for A4 print, hard on a phone. Carried over from v1 (not fixed). Owner: art-director.
- L5 (minor, p13): brand chips and group labels wrap to two lines on the half-width cards (for example "GUIDANCE MARINE", "KONGSBERG SPOTTRACK", "TARGETS, RESPONDERS AND TRANSPONDERS"), so chip rows are uneven. Owner: art-director.

## 3. Photos (most important)
Counts: 65 cards. 50 show a photo, 15 show a placeholder. Photo source types in image_credits.csv (50 unique photo refs): oem 36, reseller 7, distributor 5, catalogue (trade press or news site) 2. So 14 of 50 are not from the manufacturer.
- Reseller (7): DP-03 (fornaes.com), PR-06 (uniquegroup.com), PR-17 (tetramaritimeservices.com), PR-18 (ashtead-technology.com), SN-04 (nauticalelectronics.com), CA-16 (rexroth-parts.com), SP-09 (auto2mation.com).
- Distributor (5): DP-01 (alphatronmarine.com), CA-11 (smtssg.com), CA-14 (woodward.store), CA-20 (adiglobaldistribution.us), SP-03 (digikey.com).
- Catalogue or trade press (2): PR-02 (rivieramm.com news), PR-15 (insidegnss.com).
- The contents page now says "manufacturer and distributor published information" (v1 F7 fixed), but reseller and trade press photos are wider than "distributor"; consider "manufacturer, distributor and trade published information".

Every photo shows the product or its family. No vessel-only photo, no drawing instead of a photo, no event banner. Defects:
- P1 (MAJOR, SN-04 p15): the photo carries a "NAUTICAL ELECTRONICS" circular seal over the product (reseller watermark, visible on the page). Also a composite of three separate units (display, rate unit, repeater), so not a clean product shot. Owner: media-librarian (replace with OEM photo of Standard 22 NX or Standard 22, or remove card photo).
- P2 (MAJOR, DP-03 p06): photo is a phone picture of a used panel on foam with a blue "FORNAES SHIP RECYCLING" card lying in front (visible in the page render). Third-party company branding, used-equipment context, low quality, and it is the only visual on a mostly empty page. Owner: media-librarian / photo-editor (crop out the card or replace; ask Rahul for a Sinor or Navis image).
- P3 (minor, PR-02 p08): scene photo on a vessel with an offshore platform; Mini RadaScan radome is on the left but a CyScan unit is also in frame. Trade press source (Riviera). Honest enough but not an isolated product shot; image rights for a news photo are a question for Rahul. Owner: media-librarian.
- P4 (minor, PR-12 p11): tight close-up of an orange winch drum with wire, not recognisable as the Bandak taut wire unit; source note says the page does not say it is the MK15B or LTW 16B. Same as v1 P1, still open. Owner: media-librarian.
- P5 (minor, PR-13 p12): photo is the RX45 antenna; the title is "R1 GNSS/DGPS Receiver System". The text mentions the RX45 but there is no caption saying the picture is the antenna. Owner: copywriter (caption) or media-librarian.
- P6 (minor, CA-24 p21): credited as OEM (highlander-global.com) but the research note says the OEM image is the 900S variant used only as a style fallback. Family photo, not the black-box 900. Owner: media-librarian.
- P7 (minor, CA-11 p19, SP-09 p24): surplus-unit photos show third-party artefacts: "TESTED OK 29 OCT 2014" label (CA-11) and a legible label with ID, serial number and MAC addresses (SP-09). Not Sinor data, but should not be printed. Owner: photo-editor (crop or retouch) or replace.
- P8 (minor, SN-01, SN-02, SN-03 p15): the three MRU photos are the same OEM render with only the label text changed (MRU-B1, MRU-B1.1, MRU-B2). Correct per OEM renders, but a reader may think it is one product. Optional note "same housing". Owner: art-director.
- P9 (minor, resolution): CA-21 300x300, SP-05 300x300, SN-08 500x500, PR-06 400x320, PR-13 400x400, SP-08 500x334 are small for A4 print at card width (about 130 to 175 dpi). Acceptable for screen, soft in print. Owner: media-librarian.
- P10 (minor, credits file): image_credits.csv has 52 rows for 50 photos because DP-01 and DP-02 appear twice (a photo row and a "document, no image" row with source_type "user-supplied"). Clean up so the CSV is one row per photo. Owner: media-librarian.

## 4. Photo-less cards and placeholder
- 15 of 65 cards (23 percent) have no photo: PR-16, PR-21, CA-02, CA-03, CA-05, CA-06, CA-07, CA-08, CA-09, CA-10, CA-12, CA-18, SP-01, SP-02, SP-07. This matches images_needed.csv (15 rows plus 2 "left out" items).
- Concentration: page 19 has 5 of 6 cards without a photo, page 18 has 4 of 6.
- The placeholder is a dashed frame with centred "PRODUCT PHOTO TO BE SUPPLIED". It looks deliberate and consistent. D1 (minor): the wording is an internal production note on customer-facing pages; consider neutral wording ("Image on request") for the issued version. Owner: copywriter / art-director.

## 5. Facts and wording
Result of scripts: no printed number or model token lacks evidence (see scope). Defects and observations below are about meaning, sourcing flags and badges.

### DP pages (compared with dp_sources.md and results)
- DP-02 Bridge Mate: DP 1, DP 2, DP 3 texts and the DP 1 to DP 2 upgrade statement match the Marine Technologies brochure quotes in dp_sources.md. OK. Minor F11: feature bullet "Type-approved DP in all classes" is a bare claim, while the paragraph attributes it ("Marine Technologies states"). Make the bullet attributed too. Owner: copywriter.
- DP-01 NavDP 4000: DP1 (4011 + 4001 IJ), DP2 (4022 + 4002 IJ, DP A and DP B stations, printers, VRS), thruster interfaces (dry contact, 4-20 mA, 0-10 V) and sensor list match dp_sources.md (Sinor's own proposals, user-supplied, not checked against OEM). Description and class list come from Navis brochure and nauticexpo (slice2.json). OK.
- F12 (minor, DP-01 p04): "control computer HT CO3" is printed in Supplied models, but the research note says it "is not on any page read (UNVERIFIED)" and images_needed.csv lists it as "left out". Either remove it or mark as register item. Owner: copywriter.
- F13 (minor, DP-01 p04): "Navis" and "NAVIS" are mixed (heading chip "NAVIS ENGINEERING", body "The Navis NavDP 4000 Series", "Navis states"). Official name is Navis Engineering Oy; "NAVIS = Navis Engineering Oy" is still an inference awaiting Rahul in brain/verified-facts.md. Pick one spelling after he confirms. Owner: copywriter.

### Installation, commissioning, DP trials and FMEA wording (question for Rahul)
- Both DP pages say "Installation, commissioning, DP trials and FMEA support by Sinor engineers". The Sinor profile brochure (v2.0, text read this session) says: "DP system retrofit, upgrade and class-witnessed FMEA trials", "Retrofit, upgrade and FMEA-witnessed sea trials", and a capability matrix with ticks for Installation, Commissioning and Trials under DP Systems. So the wording is consistent with the profile in substance. Differences: the profile says "class-witnessed FMEA trials", the catalogue says "FMEA support"; and the profile describes Sinor as an independent integrator for DP systems in general, it does not state that Sinor installs NAVIS or Marine Technologies systems specifically. Also dp_sources.md only paraphrases the profile and records no quote.
- Q1 for Rahul (open): is it correct to say Sinor engineers install, commission and run DP trials/FMEA on NAVIS and Marine Technologies systems? In v1 the producer replaced "installed" with "supplied and supported" because the brief did not allow more (fixes_v1_1.md F4). The DP pages now bring "installation" back. Needs his decision and wording. Owner: Director.
- Q2 for Rahul (open): "Marine Technologies" = Marine Technologies LLC and "NAVIS" = Navis Engineering Oy are inferences recorded in brain/verified-facts.md awaiting his confirmation.

### Legacy badges
Badges present on CA-09, CA-10, CA-11, CA-12, CA-15, CA-18, SP-05, SP-09.
- Supported by evidence (discontinued or phased out): CA-12 (Schneider discontinued 2 Dec 2020), CA-15 (DEIF phased out, replaced by DM-4), CA-18 (VLT 5000 discontinued; note the VACON NXP text describes a current range), SP-05 (Siemens phased out 06/2017), SP-09 (WAGO page 410 Gone).
- B1 (MAJOR, CA-10 p19): VersaMax IC200ALG240 has the badge, but its evidence (C11) contains no lifecycle statement at all. Unsupported. Owner: fact-reviewer to find a source or Director to remove the badge.
- B2 (minor, CA-09 p19, CA-11 p19): badge rests only on the word "legacy" in research text ("long-established legacy PLC part", "legacy part with no maker product page found"), not on a discontinued or phased-out statement. Same owner.
- B3 (minor, CA-08 p19, CA-07 p19, SN-04 p15): no badge although evidence says the maker discontinued RRDIO15 (CA-08), "legacy part, supplied refurbished" (CA-07), and Mackay lists the original Standard 22 as end of life (SN-04, whose spec data are from the 2018 brochure while current model is Standard 22 NX). Badge policy is inconsistent. Owner: fact-reviewer, Director.

### MRU cards (compared with r2_b.json NEW1 and the Inertial Labs page)
- SN-01 B1: "Outputs Heave, with heave velocity and acceleration; Heave accuracy 5% or 5 cm RMS; IP67, 120 x 50 x 53 mm, 220 g" matches the datasheet reading. SN-02 B1.1: pitch and roll, 0.02 deg RMS dynamic, ABS design assessment: matches. SN-03 B2: heave, surge, sway, pitch, roll; 5% or 5 cm; 0.02 deg; 120 x 50 x 53 mm; 24 VDC (18-36 VDC): heave and size match; the supply line is not in NEW1 (NEW1 says 9 to 36 VDC) but the token is in the B11 evidence, so see F4 below.
- F3 (MAJOR, SN-03 p15 vs SN-01, SN-02): the SN-03 Supplied models line reads "MRU B1 (roll and pitch), MRU B2 (with heave for HPR)". That is the register wording and contradicts SN-01 (B1 is heave) and SN-02 (B1.1 is pitch and roll) on the same page. The research note says the register "B1" may actually be B1.1 and to verify. A printed contradiction on the page Rahul cares most about. Owner: Director (ask Rahul which unit Sinor supplied), then copywriter.
- F4 (minor, SN-03 p15): "Supply 24 VDC (18-36 VDC)" is on the SN-03 card, while NEW1 research gives 9 to 36 VDC for the B1/B1.1 and the B2 datasheet value is not stated in NEW1. Token exists in the B11 evidence but check the B2 datasheet figure. Owner: fact-reviewer.
- F5 (minor, SN-01 p15): Inertial Labs website table (checked by me today) lists B1 as Heave, Surge and Sway; the card says heave only (datasheet). The research note itself suggested "heave (website also lists surge and sway)". The source conflict is not disclosed. Owner: copywriter.

### Other facts defects
- F1 (MAJOR, CA-23 p21): prints "MS-702 capacity (retailer) up to 55 beltpacks or 10 speaker stations". The research note for A17 says the figure came from a retailer snippet, "not read in full; do not print without checking". Still printed. Owner: fact-reviewer to verify on clearcom.com or Director to remove.
- F2 (MAJOR, PR-17 p13): maker chip "KONGSBERG SPOTTRACK" on an item the register calls "8-way prism". Research note: "Maker of Sinor's 8-way cluster is therefore not settled: Kongsberg SpotTrack, Guidance, or other"; photo is from Tetra Maritime, a reseller. Maker attribution is unsupported. Owner: Director (ask Rahul) and copywriter.
- F6 (minor, CA-02 p18): all three spec rows are labelled "Example" and one says "(JH 19T27 MMD)", so they belong to the Hatteland monitor on CA-01, not to the Guidance 20-0310 monitor; the research note says maker and model link is "plausible but unverified". The card mixes two products. Owner: copywriter.
- F7 (minor, CA-24 p21): features say antenna 6 ft or 8 ft, Supplied models says "HLD-900 24in X-band radar"; research note says the datasheet gives 6 ft or 8 ft and the 24 in may be the monitor, not read from the maker site. Unresolved conflict printed. Owner: fact-reviewer.
- F8 (minor, PR-21 p13): Supplied models "cNode Micro 31-180; cNode Minis 34-180": research says the 34-180 to Minis mapping "is UNVERIFIED and may be wrong". Casing is also mixed (title "cNODE", model line "cNode", "Minis" where Kongsberg writes "MiniS"). Card has no photo. Owner: fact-reviewer, copywriter.
- F9 (minor, PR-11 p11): maker chip "SMT SPECIALIST MARINE TECHNOLOGIES" is correct per smt-ab.com, but brain/verified-facts.md records "SMT = Sinor Marine Technologies (USER-SUPPLIED)" for Rahul's stand files. Confirm with Rahul that these are different. The card text says "SMT Z range MK2" while Supplied configuration says "Z-range 2.1" (research notes 2.0 versus 2.1 unresolved). Owner: Director, fact-reviewer.
- F10 (minor, SP-02 p23): description "Planned-maintenance and spares kit for ... RadaScan and Mini RadaScan sensors, supplied by Sinor"; research found no kit page anywhere and the kit contents are user-supplied and unverified. Printed as fact without a caveat. (SP-01 is sourced to a reseller listing, part number 31-0362-4, not printed.) Owner: copywriter.
- PR-14 etc.: spelling checks passed: Anschütz (umlaut present, 1 occurrence), Seastar (5, one spelling, no "SeaStar"), RADius (13), cNODE (5, see F8), easYgen (5), NavDP, Navis/NAVIS (see F13).

## 6. Rules
- Em dashes 0, en dashes 0 (grep on brochure_v2.txt).
- No customer, vessel, price, PO or register data found in the PDF text. The word "installed" appears only in "upgrades of installed NAVIS systems" (not an installation claim).
- No authorised-dealer claim. Back page: "supplies and supports the products listed as an independent company unless a specific authorisation is stated in writing". Trademark disclaimer present on p26. Wording still awaits Rahul's confirmation (brief).
- Contact details: only the approved ones: 601, Al Nokitha Building, Hamariya Port; P.O. Box 95842, Dubai, UAE; +971 4 665 7162; sales@sinormarine.com; support@sinormarine.com; sinormarine.com. Cover shows Dubai, UAE, sales@, phone, web. (Profile brochure uses info@; catalogue does not.)
- Sinor logo present on every page, looks consistent with the profile.

## Defect register
| ID | Sev | Page / ref | Defect | Owner |
|---|---|---|---|---|
| P1 | major | p15 SN-04 | "Nautical Electronics" reseller watermark on photo, composite image | media-librarian |
| P2 | major | p06 DP-03 | Photo shows Fornaes Ship Recycling card, used unit, low quality; near-empty page | media-librarian, photo-editor |
| F1 | major | p21 CA-23 | 55 beltpacks / 10 speaker stations printed though research said do not print unchecked | fact-reviewer |
| F2 | major | p13 PR-17 | Maker "Kongsberg SpotTrack" unsupported, maker unsettled | Director, copywriter |
| F3 | major | p15 SN-03 | Supplied models "B1 (roll and pitch)" contradicts SN-01 and SN-02 | Director, copywriter |
| B1 | major | p19 CA-10 | Legacy badge with no lifecycle evidence | fact-reviewer |
| B2 | minor | p19 CA-09, CA-11 | Badge rests on word "legacy" only | fact-reviewer |
| B3 | minor | p19 CA-07, CA-08; p15 SN-04 | Missing badges where evidence says discontinued or legacy | fact-reviewer |
| F4 | minor | p15 SN-03 | 24 VDC (18-36) vs 9 to 36 VDC in NEW1; confirm B2 datasheet | fact-reviewer |
| F5 | minor | p15 SN-01 | Website says B1 also lists surge and sway; conflict undisclosed | copywriter |
| F6 | minor | p18 CA-02 | Specs belong to Hatteland monitor, maker unverified | copywriter |
| F7 | minor | p21 CA-24 | 6/8 ft antenna vs "24in" unresolved | fact-reviewer |
| F8 | minor | p13 PR-21 | Unverified 31-180 / 34-180 mapping, mixed casing | fact-reviewer |
| F9 | minor | p11 PR-11 | SMT = Specialist Marine Technologies vs Sinor Marine Technologies in verified-facts; 2.0 vs 2.1 | Director |
| F10 | minor | p23 SP-02 | Unverified kit description printed as fact | copywriter |
| F11 | minor | p05 DP-02 | "Type-approved DP in all classes" bullet unattributed | copywriter |
| F12 | minor | p04 DP-01 | "HT CO3" unverified and listed as left out | copywriter |
| F13 | minor | p04 DP-01 | Navis / NAVIS mixed spelling | copywriter |
| P3 | minor | p08 PR-02 | Vessel scene, CyScan also in frame, trade press image | media-librarian |
| P4 | minor | p11 PR-12 | Winch drum close-up, not identifiable (repeat of v1 P1) | media-librarian |
| P5 | minor | p12 PR-13 | Picture is antenna, title is receiver system | copywriter |
| P6 | minor | p21 CA-24 | Photo is variant fallback credited as OEM | media-librarian |
| P7 | minor | p19 CA-11, p24 SP-09 | Third-party tags, serial and MAC visible | photo-editor |
| P8 | minor | p15 | Three MRU photos are one render with different labels | art-director |
| P9 | minor | several | Small source images soft in print | media-librarian |
| P10 | minor | credits csv | DP-01, DP-02 duplicated rows | media-librarian |
| D1 | minor | 15 cards | Placeholder wording is an internal note | copywriter, art-director |
| L1 to L5 | minor | p06, p16, p24, header, p04 to p05, p13 | Empty areas, cramped header, small type, uneven chips | art-director |

Count by severity: blocker 0, major 6 (P1, P2, F1, F2, F3, B1), minor 26 IDs (B2, B3, F4 to F13, P3 to P10, D1, L1 to L5).

## Questions for Rahul (not resolved by QA)
1. Is "Installation, commissioning, DP trials and FMEA support by Sinor engineers" accurate for NAVIS and Marine Technologies systems, and is that the wording he wants (the profile says class-witnessed FMEA trials as a general Sinor service)?
2. Confirm "NAVIS" = Navis Engineering Oy and "Marine Technologies" = Marine Technologies LLC.
3. Which MRU did Sinor supply under "B1 (roll and pitch)": B1.1 (pitch and roll) or B1 (heave)?
4. Maker of the 8-way prism cluster (PR-17).
5. Are Specialist Marine Technologies (SMT, taut wire) and Sinor Marine Technologies the same or separate?
6. Photos from resellers (Fornaes, Nautical Electronics etc.), trade press (Riviera) and surplus listings: acceptable, or only OEM and Sinor photos?

## Candidate lessons for the Director (not recorded by QA)
- Add a watermark and third-party-branding check on every non-OEM photo at full resolution before it enters img_ready (found NAUTICAL ELECTRONICS seal and a Fornaes card that survived into v2).
- Make the build script fail when a research note contains "do not print", "UNVERIFIED" or "not verified" for a field that is rendered (CA-23 figure, HT CO3, 34-180 mapping).
- Drive the "Legacy spare" badge from an explicit lifecycle field with a source URL, not from the word "legacy" in notes.
- Resolve register versus OEM conflicts (MRU B1 vs B1.1, 24 in vs 6/8 ft) with Rahul before rendering; printing the register wording next to the OEM wording creates visible contradictions.
- Keep one credits row per photo; do not mix document-only sources into image_credits.csv.
- Placeholder text on customer-facing pages should be neutral; internal notes belong in images_needed.csv.
