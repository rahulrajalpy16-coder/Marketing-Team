# Quotation spec (input of `scripts/build_quotation.py`)

The script reads one JSON file and renders the Sinor standard quotation PDF described in
`skills/sinor-quotation/SKILL.md`. The spec carries only the job data. Nothing about a client or a price
is stored in the plugin.

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_quotation.py" spec.json --out "<QTN No> - <Vessel or Client>.pdf" [--logo logo.png] [--check]
```

Needs `reportlab`. `--check` also uses `pdftotext` or `pypdf` to read the PDF back.
Exit codes: 0 ok, 2 invalid spec or arguments (every problem is listed on stderr), 3 render failure,
4 `--check` found a FAIL. Warnings (assumed values) go to stderr and never stop the build.

## Fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `client.name` | string | none, **required** | printed bold |
| `client.address`, `client.tel`, `client.attn`, `client.trn` | string | blank | blank is allowed. An address must not start with `. ` (flagged by `--check`) |
| `quote.qtn_no` | string | `SMS-QT{YYYY}-XXXXX` + warning | printed exactly as given, so `-R1`, `-R2`, `-D`, `-D1` are simply part of it. `YYYY` is the year of the quote date |
| `quote.date` | `DD/MM/YYYY` | today + warning | |
| `quote.your_ref` | string | `Email` | client RFQ or enquiry reference when known |
| `quote.currency` | string | `USD` | used in column headings and in Amount in Words |
| Sinor TRN | fixed | `104218013100003` | not in the spec |
| `subject` | string | blank | `{Equipment/System} - {Scope} - {VESSEL}` |
| `mode` | `additive` or `alternatives` | `additive` | alternatives prints four blank total rows and no Amount in Words |
| `items` | list | | flat list, numbered 1, 2, 3. Give `items` or `sections`, never both |
| `sections` | list of `{name, items}` | | items numbered `1.1, 1.2, 2.1`. Additive mode prints `Sub-total Section n (name) :` after each section. In alternatives mode the numbering is kept and no sub-totals are printed |
| `discount` | `{"amount": n}` or `{"percent": n}` | none | exactly one key. Percent prints the label `Discount 13% :` |
| `vat_percent` | number 0 to 100 | `0` | 0 prints the row `VAT :` with `0.00` |
| `vat_label` | string | `VAT {rate}% :` (or `VAT :` at 0) | override, for example `"VAT 5%"` to print `VAT 5% :  0.00` on an exclusive-of-VAT quote as many issued quotations do |
| `terms` | object | see below | each of `payment`, `delivery_terms`, `delivery_period`, `validity`, `exclusions`, `warranty` is a string or a list of strings (a list of two or more is printed numbered `1. 2.`) |
| `notes` | list, set name, or object | `standard` without notes 6 and 10 | see below |
| `signatory` | `"default"`, `false`, or `{name, title, phone, email}` | `"default"` | default is the block named in the skill. `false` prints no block. Only `name` is required in an object |

### Item fields

| Field | Type | Notes |
|---|---|---|
| `title` | string | bold first line. Required unless `text` is given |
| `text` | list of strings | extra plain description lines under the title |
| `include` | list of strings | one component per line under the heading `Include:-` (override with `include_heading`, for example `System Consists of:`) |
| `scope` | list of strings | one service step per line under `Scope of Work:` (override with `scope_heading`) |
| `blocks` | list of `{heading, lines}` | any further headed list, printed after `scope` |
| `qty` | number | required, greater than 0 |
| `unit` | string | required (Lsum, Nos, Set, Day, Days) |
| `price` | number or string | required, 0 or more. Commas are accepted in strings |

Long descriptions wrap. Each description line is its own table row, so an item can split across pages and the
header row repeats on every page.

### Terms defaults

| Field | Default |
|---|---|
| `payment` | `100% Advance` |
| `delivery_terms` | `Ex Works UAE` |
| `delivery_period` | blank, with a warning (never invented; say it per item or option) |
| `validity` | `10 Days` (use `30 Days` for techno-commercial proposals) |
| `exclusions` | 1. Visa, Travel tickets, Boarding & Lodging if not in UAE. 2. Mechanical & Hot works, Cable Penetration, Fabrication, Carpentry, Rigging & Mounting. (use `"NA"` for supply only) |
| `warranty` | `Standard OEM Warranty` |

Terms that mention items must use the numbers that exist in the table (`Item 1`, `Items 2 & 3`, `Item 1.2`).
`--check` fails when a delivery line names an item that does not exist.

### Notes

`notes` is one of:

* a list of strings: used as given, numbered 1, 2, 3.
* a set name: `"standard"` (10 notes), `"installation_newer"` (9 notes), `"supply_only"` (3 notes). The wording is
  verbatim from SKILL.md section 2.
* `{"set": "<name>", "drop": [6, 10], "add": ["extra note"]}`: start from a set (default `standard`), remove notes by
  their 1-based number in the set, then append new notes. Numbers in print are renumbered continuously.

When `notes` is absent the `standard` set is used without note 6 (DP integration) and note 10 (HPR lead time),
because the skill marks them job specific. Ask for them explicitly with `"notes": "standard"` or by listing them.
In `installation_newer`, note 4 (sea trial) and note 5 (DP interfacing) are conditional: drop them with
`"drop": [4, 5]` when they do not apply.

## Computation rules (decimal.Decimal only, rounding half-up)

1. Unit price is normalised to 2 decimals (half-up) before use, so the printed price always reproduces the amount.
2. `amount = round2(qty * price)` per item.
3. `Total = sum(amount)` over all items.
4. Discount, normalised to 2 decimals before it is subtracted:
   * `{"amount": a}`: `discount = round2(a)`.
   * `{"percent": p}`: `discount = round2(Total * p / 100)`.
   * A discount larger than Total is rejected.
5. **VAT base: Total minus Discount.** `VAT = round2((Total - Discount) * vat_percent / 100)`.
6. `Net Amount = Total - Discount + VAT`.
7. Amount in Words states the Net Amount: `USD <WORDS> ONLY`, cents as `AND CENT <WORDS>`.
8. Money prints as `283,000.00`. Quantities print without trailing zeros.
9. In `alternatives` mode no Total, Discount, VAT, Net Amount or words are computed or printed.
   A `discount` or `vat_percent` in the spec is ignored with a warning.

Sub-totals are the sum of the item amounts of that section (before discount and VAT).

### Amount in Words style (house style from QUOTATION_PRACTICE.md section 5)

Upper case, `USD` first, `ONLY` last, no hyphens, no `AND` inside the number, tens and units separated by a space:

* `283,000.00` gives `USD TWO HUNDRED EIGHTY THREE THOUSAND ONLY`
* `28,383.75` gives `USD TWENTY EIGHT THOUSAND THREE HUNDRED EIGHTY THREE AND CENT SEVENTY FIVE ONLY`
* `0` gives `USD ZERO ONLY`; `0.05` gives `USD ZERO AND CENT FIVE ONLY`

## Complete example

This is `tests/fixtures/quotation_example.json` (fictional data only).

```json
{
  "client": {
    "name": "EXAMPLE CLIENT LTD",
    "address": "Office 100, Example Tower, Sample Street, EXAMPLE CITY",
    "tel": "+000 00 000 0000",
    "attn": "Test Contact / +000 00 000 0001",
    "trn": ""
  },
  "quote": {"qtn_no": "SMS-QT2026-XXXXX", "date": "05/11/2026", "your_ref": "E-000-2026", "currency": "USD"},
  "subject": "TEST SYSTEM (Example Model) - Supply, Installation & Commissioning - TEST VESSEL",
  "mode": "additive",
  "discount": {"percent": 13},
  "vat_percent": 5,
  "items": [
    {
      "title": "Supply, Installation & Commissioning of Test Reference System",
      "include": ["Test sensor unit, titanium housing, with 30 m cable",
                  "Interface hub, 1U rack mount, three Ethernet ports and configurable serial ports",
                  "Marine computer kit, 2U rack mount, fanless, with mains cables for UK, USA and Euro"],
      "scope": ["System installation.", "Cable laying and termination.", "Continuity and loop testing.",
                "System commissioning and functional testing.",
                "Sea trial attendance for performance verification and final acceptance."],
      "qty": 1, "unit": "Set", "price": "283000.00"
    },
    {"title": "Additional Air Freight Charges for Test Reference System", "qty": 2, "unit": "Nos", "price": "843.75"}
  ],
  "terms": {"delivery_period": "Item 1 : 8-12 weeks upon PO; Item 2 : Ex stock strictly subject to prior sale"},
  "notes": {"set": "installation_newer", "drop": [4, 5], "add": ["This is a draft quotation for approval before final issue."]}
}
```

Result: Total 284,687.50, Discount 13% 37,009.38, VAT 5% on 247,678.12 = 12,383.91, Net Amount 260,062.03.

## `--check` (what it does and does not do)

Run after rendering. Each line prints `PASS`, `FAIL` or `NOT RUN`; a check that could not run is never PASS.

* Page X of Y present on every page.
* Footer disclaimer, `sales@sinormarine.com`, `www.sinormarine.com`, address lines and `E&OE` complete on every page (not wrapped).
* Item rows read back from the PDF text: qty x price = amount, and the set of amounts equals the computed one.
* Additive mode: sum of items = Total, Total - Discount + VAT = Net Amount, Amount in Words equals the words of the Net Amount.
* No line of the PDF text starts with `. `; client address in the spec does not start with `. `.
* Known typos absent (NINENTY, Stricty, Rechargable, Taught wire, sytem, Thandarth, anaysis).
* Delivery Terms and Delivery Period lines refer only to item numbers that exist in the table.

Not automatic (always printed as NOT RUN, manual): looking at the rendered PNG pages, title versus scope versus
exclusions agreement, and revision suffix versus scope change.
