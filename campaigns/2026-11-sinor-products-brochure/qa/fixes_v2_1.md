# Fixes after independent QA v2 (producer fixes, self-reviewed)

QA v2 (separate qa-reviewer invocation, qa_report_v2.md): PASS WITH DEFECTS, 0 blockers, 6 major, about 26 minor. Fixes below were made by the Director and checked by re-rendering and viewing pages 4, 5, 14, 15, 16, 20 to 24 and by text checks. NOT re-audited independently (self-reviewed).

| QA ref | Fix |
|---|---|
| P1 SN-04 gyro photo watermark | photo removed, card keeps text, photo requested |
| P2 DP-03 NAVIS panel (another firm's card in photo, near-empty page) | card removed, listed as left out |
| F1 CA-23 Clear-Com "55 beltpacks" | retailer figure removed from specs, description and models line trimmed |
| F2 PR-17 maker unsettled | chip now "Laser reflector prisms", no maker claim |
| F3 SN-03 "B1 (roll and pitch)" | models line now "MRU-B2 (with heave for HPR)" |
| B1 to B3 legacy badges | kept only where research shows lifecycle evidence: C13 Modicon TSX P57, C16 Delomatic 3, D05 SITOP PSU100M, D09 WAGO IPC; removed from C10, C11, C12, C17 |
| F4 B2 supply voltage | unchanged (from B2 sources), flagged for Rahul |
| F5 MRU-B1 website conflict | spec now says datasheet heave, website also lists surge and sway |
| F6 CA-02 specs from another maker | specs removed |
| F7 Highlander "24 in" | models line no longer says 24 in; photo corrected to the X-band antenna (earlier photo was the 900S variant because my download list lacked www.malinsmarine.com) |
| F8 PR-21 cNODE numbers | numbers removed |
| F9 SMT | chip shows "SMT" only. brain/verified-facts.md says Rahul's files use SMT for Sinor Marine Technologies, the research found Specialist Marine Technologies (UK): question to Rahul |
| F11 to F13 | MT type-approval bullet attributed; HT CO3 removed from DP-01; NAVIS spelling unified |
| P5 | Ronav card title now names receiver and RX45 antenna |
| placeholder wording | "Photo to follow" |

Open (not changed): reseller photos are used on 5 cards and trade-press on 2 (see image_credits.csv, source_type); small source images are soft in print; third-party tags visible on the Converteam AMC and WAGO IPC photos; DP pages say Sinor engineers provide installation, commissioning, DP trials and FMEA support (matches the profile brochure in substance, Rahul to confirm for NAVIS and MT).
Mechanical checks after fixes: 0 em dashes, 0 en dashes, no retailer or reseller wording, 25 pages, 4.3 MB.
