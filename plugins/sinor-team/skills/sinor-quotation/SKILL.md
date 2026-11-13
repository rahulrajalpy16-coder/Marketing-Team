---
name: sinor-quotation
description: Create a Sinor Marine Services Middle East FZCO quotation PDF in the company's standard layout from finished line items (client, vessel, items, prices, terms). Use for "make the quotation PDF", revisions (-R1), draft (-D) copies and additional-day claims. For RFQ analysis or estimating from cost, use the sales workflow first.
---

# Sinor Marine standard quotation

Produce a quotation that matches Sinor Marine's standard format (reference: SMS-QT2026-01829). Output a PDF by default; make a .docx only if the user asks for Word.

**Build with the bundled script, not by hand.** Write the job data to a JSON spec (schema in `${CLAUDE_PLUGIN_ROOT}/references/quotation-spec.md`) and run:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_quotation.py" <spec.json> --out <output.pdf>`
The script computes every amount, discount, VAT and the Net Amount in decimal arithmetic, writes the Amount in Words, applies the logo `${CLAUDE_PLUGIN_ROOT}/assets/brand/sinor-logo.png` and the header and footer on every page. Needs the Python library reportlab (`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check_env.py"` shows if it is installed). If the script cannot run (for example in plain chat without code execution), produce the content as a structured draft and label it "editing package requiring rendering", never as a finished PDF.

**Status.** Everything this skill produces is a DRAFT until Rahul approves issue. Never email or send it to a client without his explicit approval. This skill contains company identity details (TRN, address, signatory contact, standard tariff); keep the plugin private to the team.

## 1. Collect the variable fields
Take whatever the user gives; ask once, briefly, only for what is missing and essential (client name, items/prices). Use defaults for everything else and state them.

**Client block (left)**
- Name (bold)
- Address
- Tel (may be blank)
- Attn. (contact name / phone)
- TRN (client's, may be blank)

**Quote block (right)**
- QTN No: format `SMS-QT{YYYY}-{NNNNN}` (ask user for the number; never invent one silently - if not given, use `SMS-QT{YYYY}-XXXXX` and flag it). Revision: add `-R1`, `-R2`... to the same number. Draft for approval: `-D`, `-D1`.
- QTN Date: DD/MM/YYYY, default today
- Your Ref.: default `Email`; use the client's RFQ/enquiry reference when given (e.g. `E-088-2026`)
- Currency: default `USD`
- TRN: fixed `104218013100003` (Sinor's)

**Subject line**: `{Equipment/System} – {Scope} - {VESSEL NAME}` e.g. `HPR (Sonardyne Ranger 2) – Supply, Installation & Commissioning - DE JIAN`

**Line items** (one row each): No | Description | Qty | Unit (e.g. Lsum, Nos, Set, Day) | Price | Amount
- Several systems in one quote: number items in sections (`1.1, 1.2 ... 2.1`) with a `Sub-total Section n (name) :` row after each section. Terms that mention items must use the same numbers.
- Rental: put the period and day rate in the description (`... for a 6-month period. Per day charges: $425.00/ day`).
- Additional-day claim: one Lsum line `Service Engineer Attendance - Additional Day Charges for the Below Scopes:`, numbered jobs, `Additional Days Onboard: n Days`, `(Refer the attached calculation)`. Attendance tariff (USD/hour, engineer / technician): normal 93.75 / 60.00, OT A 117.25 / 75.00, OT B 140.75 / 90.00; 9-hour engineer day = 843.75 (unit `Days`). Confirm the tariff with the user before use.
- A PDF stamped `NOT APPROVED` is a local ERP draft, never a final approved quote (stated by the user on 2026-10-20). Never send a stamped copy to a client as final.
- Description = bold-ish title line (e.g. `Option 1:-` then system name), then `Include:-` (or `System Consists of:`) followed by one component per line, then `Scope of Work:` with one service step per line.
- Amount = Qty x Price, formatted `283,000.00`.
- If items are alternatives (Option 1/2/3), leave the total rows under the table blank (as in the original).
- If items are additive, always print four rows: `Total :`, `Discount :` (0.00, or the amount; label may show the rate, e.g. `Discount 13% :`), `VAT 5% :` (0.00 when prices are exclusive of VAT), `Net Amount :`. At the left: `Amount in Words : USD {NET AMOUNT IN UPPER-CASE WORDS} ONLY`, cents as `AND CENT {WORDS}`.

## 2. Standard terms (defaults, editable per quote)
| Field | Default |
|---|---|
| Payment Terms | 100% Advance |
| Delivery Terms | Ex Works UAE (per option if several) |
| Delivery Period | per item / option, e.g. `4–6 weeks`, `Ex stock strictly subject to prior sale`, `8-12 weeks upon PO` |
| Validity | 10 Days (30 days for techno-commercial proposals) |
| Exclusions | 1. Visa, Travel tickets, Boarding & Lodging if not in UAE.<br>2. Mechanical & Hot works, Cable Penetration, Fabrication, Carpentry, Rigging & Mounting. |
| Warranty | Standard OEM Warranty |

**Notes (default list, numbered):**
1. All price quoted above are exclusive of VAT.
2. Any approvals / entry pass requirements for engineers/technicians / labors to be arranged by client.
3. All Mechanical site Jobs like Hot works, Painting Jobs, will be client scope.
4. The site/ area access supports like staging's, clear access etc. if required to be arranged by Client /Yard.
5. There will be supports required from client regarding the access, permission, Isolation and identification of power, existing cables, route etc.
6. Integration with the existing DP system shall be carried out by the DP manufacturer. *(keep only for DP/HPR-related jobs)*
7. Any scopes which required other than mentioned in the quotation, will be quoted separate.
8. Any additional days or scope of work beyond those mentioned in this quotation will be charged separately.
9. Shipping and delivery costs are excluded.
10. For HPR the lead time mentioned in our quotation is considered up to delivery onboard. *(keep only for HPR jobs)*

Drop or adjust job-specific notes (6, 10) when they don't apply; add any the user asks for.

**Newer note wording (used on installation quotes from Aug 2026; prefer it for I&C jobs):**
1. Any additional standby days or delays arising beyond our responsibility shall be charged separately on an additional man-day basis.
2. Any scope of work not explicitly mentioned in this quotation shall be considered excluded and will be quoted separately.
3. All prices quoted above are exclusive of VAT.
4. Sea trial attendance and support are included in our scope. *(only if included)*
5. DP hardware/software interfacing and integration on the vessel's DP system side are excluded from our scope. *(DP sensor jobs)*
6. Any approvals, entry passes, permits, or authorization requirements for engineers, technicians, and labor shall be arranged by the Client.
7. All mechanical site works, including hot works and painting, shall remain under the Client's scope.
8. Site and area access support, including staging, scaffolding, and provision of clear working access (if required), shall be arranged by the Client/Yard.
9. The Client shall provide necessary support for access, permits, power isolation, identification of existing cables, and confirmation of cable routing and system interfaces required for execution.

**Supply-only notes:** `Shipping and delivery costs are excluded.` / `The quotation only covers the supply of the unit.` / `Price quoted above are exclusive of VAT`. Exclusions `NA`.

**Additional-day claim notes:** `We have considered total {n} days including travel for the below jobs,` (each job with `(PO Ref : ...)`) / `Any additional days required beyond this period were counted separately and charged as per our standard tariff rates. (Additional - {n} days)` / `Sundays were also considered under normal tariff rates and Overtime is not counted.`

**Rental:** add the rental note (final invoice on actual rental days; extra days at the daily rate) and the Rental Equipment Warranty & Support clause. Liquidated damages clause only when the user asks.

## 3. Layout (A4 portrait, ~15 mm margins)
**Every page header**: Sinor logo + `SINOR MARINE SERVICES` (navy ~#0D4A85, bold) with `MIDDLE EAST FZCO` beneath, top-left; `QUOTATION` large bold black, top-right.
- Logo: the bundled `${CLAUDE_PLUGIN_ROOT}/assets/brand/sinor-logo.png` (1041 x 396 px, includes the wordmark) is used by the script. If the user supplies a newer logo, ask before replacing it.

**Page 1**
1. Bordered info box, two columns: client block left (labels Name/Address/Tel/Attn./TRN with `:`), quote block right (QTN No bold value, QTN Date, Your Ref., Currency, TRN). Full-width `Subject :` row beneath.
2. `Dear Sir,` then `Thank you very much for your enquiry and we are pleased to quote you the following.`
3. Items table: grey (#E6E6E6) header row, columns No | Description | Qty | Unit | Price (USD) | Amount (USD); thin black grid; prices right-aligned; rows may split across pages, repeat header on new pages.
4. Below items: empty block with 4 blank total rows in the Price/Amount columns (filled only when totals apply).
5. Terms table: bold label column (Payment Terms, Delivery Terms, Delivery Period, Validity, Exclusions, Warranty), value column.
6. `Notes:` numbered list.

**Closing (last page)**
`We sincerely trust that this quotation is in accordance with your requirement and look forward to your kind order.`
`Thanking You,`
**For SINOR MARINE SERVICES MIDDLE EAST FZCO** (bold)
Signatory block used on issued quotations: `Naveen Thandarath` (correct spelling; older quotes misprint it as Thandarth) / `+971 58 662 6123` / `naveen@sinormarine.com` - or the signatory the user names.

**Every page footer**
- Centered: `* This is a computer generated document and doesn't need any signature. *`, with `E&OE` at right.
- Left: SINOR MARINE SERVICES MIDDLE EAST FZCO / 601, Al Nokitha Building, Hamariya Port, DUBAI / Post Box : 95842 / UAE
- Center: `Page X of Y`
- Right: Tel : 04 665 7162 / Fax : / sales@sinormarine.com / www.sinormarine.com

Font: Helvetica/Arial 9-10 pt body, 8 pt footer.

## 4. Quality checks before sending
- Recompute every Amount and any totals in code. Net Amount = Total - Discount + VAT, and Amount in Words must state the Net Amount.
- Spell-check descriptions (e.g. `system`, not `sytem`; seen before: `Stricty`, `NINENTY`, `Rechargable`, `Taught wire`); make sure Delivery Terms/Period lines are labelled with the right option or item numbers that exist in the table.
- A revision that changes scope or quantities updates the revision suffix and the price, or says the price is unchanged.
- Title, scope and exclusions must agree (no installation text in a supply-only quote; write "supervision only" when Sinor only supervises work it also excludes).
- No template artefacts: leading `. ` in the address, repeated field labels, stray amounts in descriptions, broken numbering.
- Render pages to PNG and look at them: header, footer, page numbers, nothing clipped. The footer email must not wrap (`sales@sinormarine.co` / `m` happened in drafts) and the disclaimer line must be complete.
- File name: `{QTN No} - {Vessel or Client}.pdf`. Deliver the file with the file-sending tool when available (otherwise give its path) and give a one-line summary (client, vessel, options and amounts).
- After delivering a PDF in an executive workflow, record it: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sinor.py" quote add --status draft --file <pdf path> ...` with exactly the known values (never guess missing fields).

## 5. Missing-input behaviour
Ask once, briefly, only for what is missing and essential (client name, items and prices). Never invent a QTN number (use `SMS-QT{YYYY}-XXXXX` and flag it), a client address, TRN, price, discount rate or delivery period. Do not reuse historical prices as defaults. Confirm the attendance tariff with the user before using it. Open items that the owner has not confirmed: the title line for Rahul Raj, and any tariff change after 2026-10-20.
