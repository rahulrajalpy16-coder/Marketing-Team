# QA report v1: Sinor Products Catalogue 2026 (DRAFT, 23 pages A4)

Reviewer: independent qa-reviewer (did not produce the PDF). Date: 2026-11-11.
Verdict: PASS WITH DEFECTS. Blockers 0, major 4, minor 12. Not ready to issue until the 4 majors are decided by Rahul or fixed by the producer.

## Verification scope (what was and was not done)
- Rendered all 23 pages with pdftoppm at 80 dpi and viewed every page image (23 of 23). 80 dpi is enough for layout and clipping, not for judging print sharpness of body text.
- Photos: all 33 photo cards judged from the page renders. Originals in img_ready opened individually only for A12 and B18; pixel sizes of all 33 originals read by script. Others not opened one by one.
- Facts: script comparison of ALL 66 cards in catalogue_final.json against results/slice1-5.json (description substring, every feature and spec identical, every number present in the source). This proves the PDF data equals the research record, NOT that the web sources were read correctly. I did not re-open any web source. Then read the source records, brand notes and caveats for about 40 cards (all of A01-A18, B01-B18 except B10, C03-C24 selectively, D01-D09), against what the PDF prints.
- Rules: grep of brochure.txt for em/en dashes, price, vessel, our, partner, dealer, authoris; read the cover, contents and back page.
- Not done: no print proof, no check of PDF fonts embedding, no check that the register item list is complete, no live check that product claims are current.

## 1. Layout, page numbers, counts: PASS (minor notes)
- No clipped, overlapping or overflowing text seen on any page. Footers show correct page numbers 02 to 23 (cover has none).
- Contents page numbers (A p.03, B p.10, C p.14, D p.19, index p.22) match the real divider pages.
- Item index (p.22): every reference checked against the page where its card sits; all correct (A03 04, A04-A06 05, A07-A09 06, A10-A12 07, A13-A15 08, A16-A18 09, B01-B06 11, B07-B13 12, B14-B18 13, C03-C08 15, C09-C14 16, C15-C20 17, C21-C24 18, D01-D06 20, D07-D09 21).
- Section counts: A 18, B 17, C 22, D 9 (total 66), all match the cards printed. Cross-references in "Components listed separately" resolve to existing cards.
- L1 (minor, p.06-09, 20-21): several cards leave a large empty block under the text where there is no components line (A07, A09, A10, A13, A15, A16, D07-D09 page). Looks unfinished rather than broken. Producer: layout.
- L2 (minor, whole document): smallest text (supplied models, supplied configuration, back-page disclaimer, footers) measures about 6 to 6.5 pt, small for A4 print and hard on a phone. Producer: layout.
- L3 (minor, B, C): reference numbers are not contiguous: B10, C01, C02 do not exist (items dropped for lack of data). A reader may think pages are missing. Producer: renumber or note.

## 2. Photos
- 33 cards show a photo, 33 show "Product photo to be supplied" (A03, A06, A11, A14, A16, A18; B03, B05, B06, B07, B09, B15, B17; C04, C05, C07-C13, C15, C17, C19, C21, C23, C24; D01, D02, D06, D07, D09). The placeholder is a hatched dashed panel with centred text, consistent on every page: looks deliberate, PASS. (Count by sampling the PDF: 6+7+15+5 = 33; img_ready holds 33 files; credit CSV has 33 rows.)
- Every photo plausibly shows its product (RadaScan dome, CyScan, SceneScan, Artemis, Fanbeam head, Sonardyne HPT, SPRINT-Nav, NSH, Z-range taut wire, Seastar receiver, Encore panel, MRU-B2, wind sensors, GA830, Hatteland monitor, NTI extender, S7-1200, Delomatic, Moxa switch, Actisense, Omron, Mean Well, Phoenix QUINT, SITOP, LMR-400 cables). No warped or stretched image seen.
- P1 (minor, B18 p.13): photo is a tight close-up of a red winch drum with wire, not the Bandak unit as a whole; source record says it is not stated that it shows the MK15B. Acceptable but could mislead. Producer: image choice.
- P2 (minor, A12 p.07): photo is an OEM project photo of an installed bridge (700 x 300 px, shown letterboxed with white bars); shows a console, not a Bridge Mate product shot, low resolution. No vessel name visible. Producer: image choice.
- P3 (minor, low resolution for print): originals C20 300x300, D05 300x300, C14 446x400, B16 500x500, D08 500x334, A17 612x496, C06 650x314. At card width about 80 mm these are roughly 100 to 190 dpi: soft in print, fine on screen. Producer: image.
- P4 (minor, D03): the only non-OEM photo is a Digikey distributor image (credit CSV source_type distributor). Contents page says photos are "drawn from the manufacturers' published information" (see F7).

## 3. Facts (spot-check scope above: 66 of 66 by script, about 40 read in detail, all four sections, 14 of 18 package systems)
No number, feature or spec on any card is absent from its results JSON. No spelling error found for RADius, cNODE, easYgen, RadaScan, CyScan, SceneScan, Sonardyne, VACON, Hatteland. Defects:
- F1 (MAJOR, C09 p.16): RRAIO16 / RRDIO15 / RRRLY8 card rests on reseller listings and model names only. Source note: "weak sourcing", no Rolls-Royce page confirms the maker, RRVIO8 not found at all, channel counts "per reseller listing". The card states channel counts and "Rack modules for Rolls-Royce marine systems" as fact and shows Rolls-Royce as maker. Source also says the maker discontinued RRDIO15 (not shown). Owner: copy and research specialist. Fix: label as legacy family card, soften, or mark as supplied-by-Sinor spares with maker to be confirmed.
- F2 (MAJOR, C13 p.16, C17 p.17, D05 p.20, D09 p.21, C09 p.16): lifecycle status found in research is not printed. TSX P57 4634M discontinued 2 Dec 2020; VLT 5000 discontinued with no Danfoss spares; SITOP 6EP1337-3BA00 phased out 2017 (successor given); WAGO 758-873 discontinued (410 Gone). Cards read like current products. Only C16 (Delomatic) shows lifecycle. Owner: copy. Fix: add "legacy / discontinued, available as spare or refurbished" line, wording for Rahul to confirm.
- F3 (MAJOR, D02 p.20): RadaScan Service Kit contents are Sinor-register and unverified against any OEM kit list (source note says so). The card shows RadaScan View sensor figures (range 600 m, close range 10 m, IP66) under the kit and the sentence "scheduled servicing keeps the 360 degree scanner reliable", which is inference, not source. D01 kit contents and part numbers come from a Singapore reseller listing, not Guidance Marine, and Guidance has no kit page. Owner: copy. Fix: drop the sensor performance specs from the kit card, state "contents per Sinor stock list", and confirm with Rahul.
- F4 (MAJOR, cover p.01, contents p.02, section A p.03): cover says "Supplied, installed and supported from Dubai" and section A says "Complete systems supplied, installed and supported as one scope". Brief open question 1 limits the wording to "supplied and supported by Sinor" until Rahul confirms. Installation as one scope is a service commitment for every package (including intercom, GNSS receiver). Owner: Director to ask Rahul, copy to adjust.
- F5 (minor, B15 p.13, whole doc): "Anschutz" printed without the umlaut (brand is Anschütz). Appears in brand label "RAYTHEON ANSCHUTZ", description and index. Fix: use Anschütz (or Anschuetz consistently, as the maker's own site does).
- F6 (minor, A15 p.08): "Seastar" in title and description, "SeaStar" in the supplied-configuration line. Fugro writes SeaStar. Make consistent.
- F7 (minor, p.02): "Photos and descriptions are drawn from the manufacturers' published information" is not true for several cards (C07, C09 to C12, C15, C19, C21, D01, D03 and D09 rely on reseller or distributor pages per the source notes). Reword to "published product information".
- F8 (minor, D07 p.21): specs are for the 2 A variant ("Rated current 2 A (this part)", 50 kA Icu) while Supplied models lists 6 A and 10 A breakers; "this part" is not Sinor's part. I could not independently confirm the 50 kA figure, it is as read from the Schneider HK page. Also register brand was a Schneider/ABB/Siemens mix, card shows Schneider only.
- F9 (minor, D08 p.21): brand label "Pasternack and Times Microwave" names the assembly maker; source note says Pasternack is not Sinor's actual supplier, and supplied models also list RG223, Cat7 and 3-core marine cable that the card does not cover. Source warns not to imply marine grade; the card does not, good.
- F10 (minor, B11 p.12): supplied models line "MRU B1 (roll and pitch)" contradicts Inertial Labs' table (B1 = heave/surge/sway, B1.1 = pitch and roll); flagged in the source as a possible register error. Printed unchanged.
- F11 (minor, B17 p.13): "cNode Minis 34-180": Kongsberg writes MiniS, and the 34-180 mapping is marked possibly wrong in the source. Printed unchanged.
- F12 (minor, A07 p.06): brand shown as FANBEAM; source says maker is unsettled (MDL per snippets, Techmak branding on fanbeam.com). Same for B03 (Kongsberg SpotTrack vs Guidance vs other) and C03 (card is the generic JH 19T27 MMD; Sinor supplies "19 in and 23 in" units, new or refurbished). C03 is linked as a component on A11 and A12 although no source ties Hatteland to NavDP or Bridge Mate (register-derived). Director to confirm with Rahul.
- Notes, not defects: A09 specs use the datasheet where the web page differs (source note), no altitude figure printed, good. A03, B05, C04, C05, C12 carry PARTIAL status in research; the printed text stays within what was read, but part numbers on those cards (for example 20-0310, 38-0037-4) are register data not verified by any source.

## 4. Rules: PASS with F4 noted
- No em dashes or en dashes anywhere in brochure.txt (grep for U+2014 and U+2013 returned nothing). Hyphens only.
- No customer names, vessel names, prices or PO data found (grep for vessel, Ocean, Swift, MPSV, price, AED, USD, purchase: only generic "vessel" in product text and the sentence "prices are quoted per enquiry").
- No dealer, partner or authorised claim. Back page: "supplies and supports the products listed as an independent company unless a specific authorisation is stated in writing". Cover is neutral. PASS (wording still for Rahul to confirm per brief).
- "our": zero occurrences. PASS.
- Trademark disclaimer present on p.23: "Product names, logos and trademarks belong to their respective owners ..." PASS.

## 5. Contact details: PASS
Back page: Sinor Marine Services Middle East FZCO, 601, Al Nokitha Building, Hamariya Port, P.O. Box 95842, Dubai, UAE; sales@sinormarine.com; support@sinormarine.com; +971 4 665 7162; sinormarine.com. Cover: Dubai, UAE, sales@, +971 4 665 7162, sinormarine.com. All match the approved list; nothing extra. (service@sinormarine.com from the profile brochure is not printed, fine.) I did not independently verify the address against a source outside the task brief; brain/brand-profile.md does not list the address.

## 6. Brand look: PASS
Navy background with cyan accents and headings, photo cards on white panels, logo on a white badge top-left of every page (cover, contents, dividers, cards, index, back). Readable at screen size on all pages. Whole pages are dark rather than white pages with navy headers; consistent with the DP profile style as described, but I did not open the profile brochure to compare.

## Defect table
| ID | Sev | Page / item | Owner |
|---|---|---|---|
| F1 | major | p.16 C09 | copy / research |
| F2 | major | C13, C17, D05, D09, C09 | copy |
| F3 | major | p.20 D02 (and D01 sourcing) | copy |
| F4 | major | p.01-03 "installed ... as one scope" | Director + copy |
| F5-F12 | minor | see above | copy |
| L1-L3 | minor | layout, small text, numbering gaps | layout |
| P1-P4 | minor | B18, A12, low-res images, D03 | image |

## Candidate lessons for the Director (provisional, not recorded by me)
1. Carry lifecycle status (discontinued, phase out) from research onto the card; research found it but the template dropped it.
2. When a card is a representative of a family (D07, D08, C03), show that wording on the card and keep the register part list separate.
3. Provenance sentences ("from manufacturers' information") must match the credit sheet; check them against the source_type column.
4. Keep brand spellings with diacritics (Anschütz) in the data and check the font supports them.
