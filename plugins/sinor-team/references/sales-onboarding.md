# Supply your company references

Start a Claude session with the Sinor Team plugin and attach files. Say `/sinor-team:onboard` and identify which documents are approved.

1. Brand: logos, approved legal identity, address/contact data, fonts/colors and bank details if required.
2. Templates: original editable Word/Excel files, reference PDFs, template IDs, revisions, applicable scope and fixed clauses.
3. History: quotations, supplier costs, confirmed POs and actual costs. Label their status and dates; don't mix them.
4. Technical: scope lists, OEM documents, approved inclusions/exclusions, installation and commissioning responsibilities.
5. Commercial: approved margin/markup rules, taxes, payment, validity, warranty and delivery policies.

Drop originals into the matching `incoming/` subfolder of the sales workspace (`sales/incoming/` in the combined layout). incoming/README.md lists each folder's `--category`, the reference/revision format and the historical vs current approved pricing convention.

Register command example:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sales.py" register <sales workspace>/incoming/offer.pdf --category supplier --reference SUP-001 --status draft` (the `/sinor-team:onboard` skill runs this for you)
Only use approved status with Rahul's evidence of approval. Review extracted text against source. PDF scans need OCR/manual review; embedded images, drawings, DOCX headers and complex spreadsheets need agent visual inspection. CLI extraction is search assistance, not complete technical interpretation.

The plugin intentionally contains no real customer prices or approved branded templates. Unknown pricing and missing templates are flagged, never invented. Keep the workspace GitHub repository PRIVATE before uploading commercial records.
