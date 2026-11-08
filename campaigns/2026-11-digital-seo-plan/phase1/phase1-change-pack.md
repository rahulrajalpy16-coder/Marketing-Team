# Phase 1 change pack: for your approval (nothing is published)

Prepared 2026-11-08 for Rahul Raj. Status: **AWAITING YOUR APPROVAL**. Nothing on sinormarine.com has been changed. I have no access to Hostinger or WordPress and I will never ask for your login. You apply the approved items, then I re-run the audit to prove each one worked.

How to approve: reply with "approve all", or list the item numbers you approve and any changes. Items marked DECISION need your answer first.

## 0. Before anyone edits

1. Make a backup first (hPanel backups or a backup plugin). I have not verified which backup options your Hostinger plan includes.
2. Work on one item at a time and check the page after each.
3. Every item below lists its "before" value so it can be reversed.

## 1. Decisions I need (short answers are fine)

| # | Question | My default if you say "your call" |
|---|----------|---|
| D1 | Claims (see item 9): use 100+ projects and 15+ years, remove 98% satisfaction, remove 50+ team, drop "from 2024"? | Yes to all four |
| D2 | Is "Fuel Monitoring" a real offer? It is in the enquiry form but has no page. | Remove it from the dropdown until a page exists |
| D3 | The "Trusted by Global Partners" strip shows 12 logos: Siemens, DEIF, Marine Technologies, Navis Engineering, Sonardyne, Fugro, Guidance Marine, SMT, Woodward, Vacon, Schneider Electric, ABB. You confirmed five as technology partners who supported the stand. Does Sinor have the right to show the other seven, and is "Trusted by Global Partners" accurate for them? | Keep the five confirmed, retitle the section to "Technologies we work with", hide the rest until confirmed. This is only a default, you decide |
| D4 | The strip includes an "SMT" logo. You said sinor-marine.com (Sinor Marine Technologies) has no connection with sinormarine.com. What is SMT on your site and stand? | Leave it as is and I note the question |
| D5 | The Navis Engineering and Marine Technologies pages: what may we say about the relationship? I used the neutral "supported by Sinor Marine Services". | Use my neutral wording |
| D6 | Home call-to-action shows your personal email and mobile. Switch the email link to sales@sinormarine.com and keep the phone? | Switch the email, keep the phone |

Resolved from your last message: sinor-marine.com is a separate company (no redirect or merge, only brand disambiguation); Naveen stays named as GM and you post on his behalf.

## 2. The items

### Item 1. Fix the broken DP page button (404)
- Before: "Schedule Consultation" on /services/dp-system/ links to /services/contact.html (HTTP 404).
- After: links to /contact/.
- How: WordPress admin > Pages > "DP system" > Edit with Elementor > click the button > Link field > /contact/ > Update.
- Risk: none. Reverse by restoring the old link (not recommended).

### Item 2. Fix two mislinked service cards on the home page
- Before: "Navigation Systems" card links to /contact. "Electrical Solutions" card links to /services/marine-automation/.
- After: Navigation links to /services/navigation-systems/. Electrical links to /services/electrical-solutions/.
- How: Elementor on the Home page > each card > Link field > Update.
- Both target pages exist and are in the sitemap.

### Item 3. New page titles and meta descriptions (15 pages)

Titles are 60 characters or less, descriptions 155 or less (checked by script). 12 of 16 pages have no description today, so Google writes its own. The DP page description today begins "DP Systems | Sinor Marine Technology", which is the name of an unrelated company, so it must go.

How: edit each page > scroll to the Yoast SEO box > "SEO title" and "Meta description" > paste > Update. Keep the %%sitename%% variable out so the title is exactly as written.

| Page | Before (title / description) | After title | After description |
|---|---|---|---|
| / | Sinor Marine Services Middle East FZCO | DP System & Dynamic Positioning System Services Dubai - Sinor Marine Services / Explore Sinor Marine Services DP System for expert Dynamic Positioning solutions, dynamic ... | DP Systems and Marine Automation, Dubai | Sinor Marine (54) | Dubai-based specialists in dynamic positioning, thruster control and marine automation for offshore vessels: upgrades, commissioning and service. (145) |
| /about/ | About - Sinor Marine Services / NONE | About Sinor Marine Services | DP and Automation, Dubai (54) | Sinor Marine Services Middle East FZCO is a Dubai marine technology company for DP, automation and electrical systems and vessel technical support. (147) |
| /services/ | Services - Sinor Marine Services / NONE | Marine Engineering Services | Sinor Marine, Dubai (49) | DP systems, marine automation, electrical solutions, navigation systems, thruster control and frequency power converters from Sinor Marine Services, Dubai. (155) |
| /services/dp-system/ | DP system - Sinor Marine Services / Sinor Marine Services (SMS) delivers type-approved DP systems across all classes, along wi... | Dynamic Positioning Systems, Dubai | Sinor Marine (49) | DP and joystick control systems, integration, upgrades, retrofits, commissioning and after-sales support for offshore vessels, from Dubai. (138) |
| /services/marine-automation/ | Marine Automation - Sinor Marine Services / NONE | Marine Automation and Alarm Monitoring | Sinor Marine (53) | Vessel automation, alarm monitoring and control systems, integrated, upgraded and commissioned by Sinor Marine Services in Dubai. (129) |
| /services/electrical-solutions/ | Electrical Solutions - Sinor Marine Services / NONE | Marine Electrical and Power Systems | Sinor Marine (50) | Marine electrical systems, power management and switchboard installations for vessels, from Sinor Marine Services in Dubai. (123) |
| /services/navigation-systems/ | Navigation Systems - Sinor Marine Services / NONE | Marine Navigation Systems: ECDIS, Radar | Sinor Marine (54) | ECDIS, radar and integrated bridge systems for precise maritime navigation, from Sinor Marine Services in Dubai. (112) |
| /services/thruster-control/ | Thruster Control - Sinor Marine Services / Thruster Control System brochure. Integrated control architecture for marine propulsion an... | Thruster Control Systems (Z-Thrust) | Sinor Marine (50) | Z-Thrust: a PLC-based independent control solution for vessel propulsion and steering systems, offered by Sinor Marine Services in Dubai. (137) |
| /services/frequency-power-converter/ | Frequency Power Converter - Sinor Marine Services / AMP-SPC Series Frequency Power Converter. Shore-ship power system with IEC 80005-3 complia... | Frequency Power Converters, Shore Power | Sinor Marine (54) | Frequency power converters for shore-to-ship power: MV/LV installation, 50/60 Hz output and ship connections, from Sinor Marine Services in Dubai. (146) |
| /navis/ | Navis - Sinor Marine Services / NONE | Navis Engineering DP Technology | Sinor Marine Services (55) | DP and joystick control technology from Navis Engineering, supported by Sinor Marine Services in Dubai. (103) |
| /mt/ | MT - Sinor Marine Services / NONE | Marine Technologies DP and Bridge Systems | Sinor Marine (56) | Integrated bridge and DP technology from Marine Technologies, supported by Sinor Marine Services in Dubai. (106) |
| /products/ | Products - Sinor Marine Services / NONE | DP Reference Systems and Navigation Instruments | Sinor (55) | DP position reference systems and marine navigation instruments supported by Sinor Marine Services, Dubai. Ask our engineers for the right option. (146) |
| /projects/ | Projects - Sinor Marine Services / NONE | Projects: DP Upgrades and Marine Automation | Sinor Marine (58) | Selected DP, automation and electrical projects by Sinor Marine Services. Contact our engineers to discuss a similar scope on your vessel. (138) |
| /blog/ | Blog - Sinor Marine Services / NONE | Marine and DP Insights | Sinor Marine Services (46) | Technical insights and updates on dynamic positioning, marine automation and offshore vessel systems from the Sinor Marine Services team. (137) |
| /contact/ | Contact - Sinor Marine Services / NONE | Contact Sinor Marine Services | Hamariya Port, Dubai (52) | Contact Sinor Marine Services at Hamariya Port, Dubai for DP, automation and electrical enquiries. Call +971 4 665 7162 or send us a message. (141) |

Hold until D5 is answered: /navis/ and /mt/.

### Item 4. Keep the thank-you page out of search
- Before: /thank-you/ is in the sitemap and open to indexing.
- After: noindex, so it leaves the sitemap automatically.
- How: edit the page > Yoast SEO > Advanced > "Allow search engines to show this Page in search results?" = No > Update. Keep the page working, it is the form conversion page.

### Item 5. Structured data (organisation details for Google and AI tools)
- Before: no JSON-LD found on any of the 16 pages.
- After: a small block that states the legal name, address, phone, sales email, logo and LinkedIn page. Only facts already on your site or confirmed. No ratings, no claims.
- Code: `jsonld-organization.json` in this folder (valid JSON, checked). Wrap it in `<script type="application/ld+json"> ... </script>` and add it site-wide with a code snippets plugin (for example WPCode) in the header.
- Check afterwards: Google Rich Results Test and Search Console.

### Item 6. Image descriptions (alt text)
- Before: on the home page 29 of 31 image tags have no alt text (plus 1 on /products/; the other 14 pages are fine).
- After: the text below. Set it in Media Library > the image > Alternative Text, or in Elementor on each image.
- I wrote descriptions from what each image shows. They do not claim these are real Sinor projects.

| Where | Image file | Alt text |
|---|---|---|
| Home, partner strip | 5.png | Siemens logo |
| Home, partner strip | 8.png | DEIF logo |
| Home, partner strip | 10.png | Marine Technologies (MT) logo |
| Home, partner strip | 9.png | Navis Engineering logo |
| Home, partner strip | 6.png | Sonardyne logo |
| Home, partner strip | 7.png | Fugro logo |
| Home, partner strip | Untitled-design-27.png | Guidance Marine logo |
| Home, partner strip | 11.png | SMT logo |
| Home, partner strip | 1-1.png | Woodward logo |
| Home, partner strip | 2-1.png | Vacon logo |
| Home, partner strip | 3.png | Schneider Electric logo |
| Home, partner strip | 4.png | ABB logo |
| Home, DP Systems card | WhatsApp-Image-2026-02-04-at-19.09.38-2.jpeg | Engineer in Sinor Marine Services overalls operating a vessel bridge control console |
| Home, Marine Automation card | WhatsApp-Image-2026-02-04-at-19.09.38-1.jpeg | Technician in a Sinor Marine shirt working on marine control system modules |
| Home, Electrical Solutions card | WhatsApp-Image-2026-02-04-at-19.09.54.jpeg | Two engineers in Sinor Marine Services overalls working on a control cabinet on deck |
| Home, Navigation Systems card | ChatGPT-Image-Feb-4-2026-06_41_46-PM-1.png | Vessel bridge navigation displays and radar screens |
| Home, Thruster Control card | ChatGPT-Image-Feb-4-2026-06_52_58-PM.png | Thruster control touchscreen and joystick on a vessel bridge console |
| Home, Frequency Power Converter card | WhatsApp-Image-2026-02-04-at-19.10.53.jpeg | Electrical cabinet with power converter equipment |

### Item 7. Compress the heavy images (page speed)
- Before: the two largest home images are 2.1 MB PNGs (about 4.3 MB of 5.4 MB of unique images on the page). Both appear under the names ChatGPT-Image-...
- After: WebP copies of about 110 to 125 KB each, same picture, 1400 px wide. Files are supplied separately with a list. Upload them to the Media Library and re-point the two cards, or let your caching or image plugin convert them.
- Note: those two images look like generated illustrations. For a safety-critical buyer, real project photos are better when you have them.

### Item 8. Analytics, Search Console and click tracking
- Before: no analytics found in the page source. Tag may exist another way, please check in the WordPress plugin list first.
- After: install the official Google Site Kit plugin, sign in with your Google account (never share the login with me), connect GA4 and Search Console, submit https://sinormarine.com/sitemap_index.xml, mark the thank-you page view as a key event.
- Click tracking: `click-tracking-snippet.html` records calls, emails and WhatsApp clicks as GA4 events. I tested it in a browser with a stand-in tracker, not on your live site.

### Item 9. Align the claims (needs D1)

| Where | Change | Why |
|---|---|---|
| Home hero, "50+ Projects Completed" | 100+ Projects Completed | You confirmed 100+ for public use on 2026-11-06 |
| Home hero, "98% Client Satisfaction" | 15+ Years of DP Engineering | No source for 98%. 15+ years is confirmed for public use |
| Home and DP page, other places that repeat 50+ or 98% | Same replacements on every page | Consistency |
| About, stats "50+ Projects", "20+ Years Experience" | 100+ Projects, 15+ Years | Matches your confirmed figures |
| About, stat "50+ Team Members" | Remove until you give me a number you can prove | Not seen anywhere else, unconfirmed |
| About, headline "...from 2024" | "Engineering Reliable Marine Automation Solutions" (drop "from 2024") | Conflicts with 15+ years. Tell me the founding year if you want it kept |

Also still unverified and not changed: "24/7 Support", "class-approved", "OEM-certified technicians", and the DNV, ABS and Lloyd's Register compliance wording on the DP page. Tell me which are true and provable, otherwise soften them.

### Item 10. Enquiry form dropdown (needs D2)
- Before: dropdown includes "Fuel Monitoring".
- After: option removed.
- How: Elementor > the form on the Home and Contact pages > Service field > options.

### Item 11. Email link on the home call-to-action (needs D6)
- Before: link opens an email to a named person. After: sales@sinormarine.com. Phone number unchanged.

## 3. After you publish

Tell me when items are live. I will re-run the same audit script, confirm each item with proof (titles, descriptions, links, alt text, JSON-LD, noindex, sitemap), and report any item that did not take effect. Search results may take days or weeks to show new titles. That is normal.

## 4. Not done in Phase 1
- GA4 and Search Console setup on your Google account: only you can do it.
- The shared enquiry-form redesign and GBP listings: next batch.
- Speed scores (PageSpeed quota error earlier): measure after item 7 with your own run.


## Simple explanation
This pack is a list of small, safe website fixes with the exact words to paste and the exact place to click. Nothing is live until you say yes. After you apply them, I check the live site and show proof that each one worked.
