# QA Checklist: Quotation and Commercial

- Q1 Every price, discount and rate traces to a stated source (user, supplier quote, price list). No invented numbers.
- Q2 Independent recomputation: run `sinor.py calc` on an input spec you build yourself from the instruction, and compare line amounts, subtotal, VAT, total and any currency conversion to the deliverable (extract PDF text with `pdftotext -layout`).
- Q3 Currency labelled on every money column and total.
- Q4 Layout follows the sinor-quotation skill: header, info box, items table, terms table, notes, closing, footer with Page X of Y. Render with `pdftoppm -png -r 60` and inspect.
- Q5 QTN number given by the user or shown as SMS-QT{YYYY}-XXXXX and flagged.
- Q6 Job-specific notes (DP integration note, HPR lead-time note) present only when they apply.
- Q7 Inclusions and exclusions consistent with the scope described.
- Q8 Validity, payment and delivery terms match instruction or approved defaults.
