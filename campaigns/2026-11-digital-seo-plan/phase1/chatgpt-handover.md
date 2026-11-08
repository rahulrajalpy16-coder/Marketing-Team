# ChatGPT project handover: Sinor website Phase 1 (sinormarine.com)

Prepared 2026-11-08 by Claude for Rahul Raj. This file is self-contained: everything needed is inside it. It contains no passwords or keys and never should.

---
## PART 1. PASTE THIS AS THE PROJECT INSTRUCTION / FIRST MESSAGE
---

You are working for Rahul Raj, who runs the website of Sinor Marine Services Middle East FZCO (Dubai). The site is https://sinormarine.com (WordPress, Elementor page builder, Yoast SEO, hosted on Hostinger with a LiteSpeed server). Rahul has approved a fixed list of 11 website changes, listed in full in PART 3. You apply exactly those changes and nothing else, through the logged-in admin session you already have access to.

HOW YOU MUST WORK
1. Confirm what access you really have (WordPress admin, Hostinger hPanel) before you begin. If a login, 2-step code or Google sign-in is needed, ask Rahul to do that step himself. Never ask him to paste a password or code into chat.
2. Do only the 11 approved items. If you see anything else that looks wrong, write it down and report it at the end. Do not change it.
3. Make a backup first (hPanel backups, or a backup plugin). Tell Rahul what you used. Do not continue if no backup is possible, ask him.
4. Work one item at a time in the order in PART 2. After each item, open the live public page in a fresh private window (or add ?nc=1 to the URL) and confirm the change is visible. Write down what you saw.
5. If a screen, plugin or setting does not match the instructions, STOP and ask Rahul. Do not guess. Do not delete pages, posts, plugins or media. Never edit or delete original images in the Media Library, only add new ones.
6. Do not install or activate any plugin except the two named in the plan: Google Site Kit (item 8) and a code snippets plugin such as WPCode (items 5 and 8). Ask before installing. Rahul does the Google sign-in himself.
7. Copy text exactly as written in PART 3, including capitalisation. Do not rewrite, "improve" or add claims. Never use em dashes (the long dash character) in anything you write.
8. Do not publish, post, email or contact anyone, and do not spend money.
9. At the end, give the report in the format in PART 5. Never say an item is done unless you saw it live.

FACTS TO RESPECT
- sinor-marine.com (with a hyphen, "Sinor Marine Technologies") is a different company with no connection to sinormarine.com. Never link to it or reuse its wording.
- Naveen Thandarath stays named as General Manager. He does not post on social media. Rahul posts.
- Do not change the "Trusted by Global Partners" logo strip or the "SMT" logo. Rahul has not decided yet.
- Do not remove or change these unverified claims: "24/7 Support", "class-approved", "OEM-certified technicians", and the DNV, ABS and Lloyd's Register wording. They are open questions for Rahul.

---
## PART 2. ORDER OF WORK
---
1. Backup.
2. Items 1, 2, 10, 11 (links, forms, in Elementor).
3. Item 9 (claims text).
4. Items 3 and 4 (Yoast titles and descriptions, thank-you page noindex).
5. Items 6 and 7 (alt text, images).
6. Items 5 and 8 (structured data, Site Kit, click-tracking code).
7. Purge the site cache (LiteSpeed Cache plugin, "Purge All", if installed).
8. Re-check every item on the live site using PART 4 and report using PART 5.

---
## PART 3. THE 11 APPROVED ITEMS
---

### Item 1. Fix the broken DP page button
- Page: https://sinormarine.com/services/dp-system/
- Before: the "Schedule Consultation" button links to /services/contact.html (this gives a 404 error page).
- After: the button links to /contact/
- How: WordPress admin > Pages > "DP system" > Edit with Elementor > click the button > Link field > type /contact/ > Update.

### Item 2. Fix two service cards on the home page
- Page: https://sinormarine.com/ (Home)
- Before: the "Navigation Systems" card "Learn More" links to /contact. The "Electrical Solutions" card "Learn More" links to /services/marine-automation/.
- After: Navigation Systems links to /services/navigation-systems/. Electrical Solutions links to /services/electrical-solutions/.
- How: Elementor on the Home page, each card, Link field, then Update. Both target pages already exist.

### Item 3. New page titles and meta descriptions (15 pages)

Set in the Yoast SEO box at the bottom of each page editor: "SEO title" and "Meta description". Type the text exactly, with no site-name variable added. Update the page. Character counts are in brackets and are within limits.

| Page URL path | SEO title | Meta description |
|---|---|---|
| / | DP Systems and Marine Automation, Dubai | Sinor Marine (54) | Dubai-based specialists in dynamic positioning, thruster control and marine automation for offshore vessels: upgrades, commissioning and service. (145) |
| /about/ | About Sinor Marine Services | DP and Automation, Dubai (54) | Sinor Marine Services Middle East FZCO is a Dubai marine technology company for DP, automation and electrical systems and vessel technical support. (147) |
| /services/ | Marine Engineering Services | Sinor Marine, Dubai (49) | DP systems, marine automation, electrical solutions, navigation systems, thruster control and frequency power converters from Sinor Marine Services, Dubai. (155) |
| /services/dp-system/ | Dynamic Positioning Systems, Dubai | Sinor Marine (49) | DP and joystick control systems, integration, upgrades, retrofits, commissioning and after-sales support for offshore vessels, from Dubai. (138) |
| /services/marine-automation/ | Marine Automation and Alarm Monitoring | Sinor Marine (53) | Vessel automation, alarm monitoring and control systems, integrated, upgraded and commissioned by Sinor Marine Services in Dubai. (129) |
| /services/electrical-solutions/ | Marine Electrical and Power Systems | Sinor Marine (50) | Marine electrical systems, power management and switchboard installations for vessels, from Sinor Marine Services in Dubai. (123) |
| /services/navigation-systems/ | Marine Navigation Systems: ECDIS, Radar | Sinor Marine (54) | ECDIS, radar and integrated bridge systems for precise maritime navigation, from Sinor Marine Services in Dubai. (112) |
| /services/thruster-control/ | Thruster Control Systems (Z-Thrust) | Sinor Marine (50) | Z-Thrust: a PLC-based independent control solution for vessel propulsion and steering systems, offered by Sinor Marine Services in Dubai. (137) |
| /services/frequency-power-converter/ | Frequency Power Converters, Shore Power | Sinor Marine (54) | Frequency power converters for shore-to-ship power: MV/LV installation, 50/60 Hz output and ship connections, from Sinor Marine Services in Dubai. (146) |
| /navis/ | Navis Engineering DP Technology | Sinor Marine Services (55) | DP and joystick control technology from Navis Engineering, supported by Sinor Marine Services in Dubai. (103) |
| /mt/ | Marine Technologies DP and Bridge Systems | Sinor Marine (56) | Integrated bridge and DP technology from Marine Technologies, supported by Sinor Marine Services in Dubai. (106) |
| /products/ | DP Reference Systems and Navigation Instruments | Sinor (55) | DP position reference systems and marine navigation instruments supported by Sinor Marine Services, Dubai. Ask our engineers for the right option. (146) |
| /projects/ | Projects: DP Upgrades and Marine Automation | Sinor Marine (58) | Selected DP, automation and electrical projects by Sinor Marine Services. Contact our engineers to discuss a similar scope on your vessel. (138) |
| /blog/ | Marine and DP Insights | Sinor Marine Services (46) | Technical insights and updates on dynamic positioning, marine automation and offshore vessel systems from the Sinor Marine Services team. (137) |
| /contact/ | Contact Sinor Marine Services | Hamariya Port, Dubai (52) | Contact Sinor Marine Services at Hamariya Port, Dubai for DP, automation and electrical enquiries. Call +971 4 665 7162 or send us a message. (141) |

Note: the DP page description used to begin "DP Systems | Sinor Marine Technology". That is the name of an unrelated company, so it must be fully replaced, not edited.

### Item 4. Keep the thank-you page out of search
- Page: /thank-you/ (keep it working, it is the form confirmation page)
- Before: indexable and listed in the sitemap.
- After: noindex.
- How: edit the page > Yoast SEO > Advanced > "Allow search engines to show this Page in search results?" = No > Update. It then leaves the sitemap automatically.

### Item 5. Structured data (organisation details, invisible to visitors)
- Before: no JSON-LD on any page.
- After: the block below on every page, in the site header, using a code snippets plugin (for example WPCode, Insert Headers and Footers, location Site Wide Header). Wrap it in a script tag exactly like this:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://sinormarine.com/#website",
      "url": "https://sinormarine.com/",
      "name": "Sinor Marine Services",
      "publisher": {
        "@id": "https://sinormarine.com/#organization"
      },
      "inLanguage": "en"
    },
    {
      "@type": "ProfessionalService",
      "@id": "https://sinormarine.com/#organization",
      "name": "Sinor Marine Services Middle East FZCO",
      "alternateName": "Sinor Marine Services",
      "url": "https://sinormarine.com/",
      "logo": "https://sinormarine.com/wp-content/uploads/2026/02/cropped-Untitled-design-28.png",
      "image": "https://sinormarine.com/wp-content/uploads/2026/02/cropped-Untitled-design-28.png",
      "description": "Dubai-based marine technology company for dynamic positioning, marine automation and electrical systems.",
      "telephone": "+97146657162",
      "email": "sales@sinormarine.com",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "601, Al Nokitha Building, Hamariya Port",
        "addressLocality": "Dubai",
        "addressCountry": "AE",
        "postOfficeBoxNumber": "95842"
      },
      "sameAs": [
        "https://www.linkedin.com/company/sinor-marine-services/"
      ]
    }
  ]
}
</script>
```
- Do not add any other fields, ratings or claims.

### Item 6. Image descriptions (alt text)

- Before: on the Home page 29 of 31 image tags have no alt text, and 1 image on /products/ has none.
- After: set the alt text below. Set it in Media Library > the image > "Alternative Text", or in Elementor on each image. Match images by the file name shown.
- These descriptions do not claim the pictures are real Sinor projects. Do not add that.

| Where | Image file name | Alt text |
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
| /products/ page | the one image with no alt text | Describe what it shows in one plain sentence, no claims. Tell Rahul what you wrote. |

### Item 7. Make the two heavy images smaller
- Before: two home page card images are about 2.1 MB each:
  - https://sinormarine.com/wp-content/uploads/2026/02/ChatGPT-Image-Feb-4-2026-06_41_46-PM-1.png (Navigation Systems card)
  - https://sinormarine.com/wp-content/uploads/2026/02/ChatGPT-Image-Feb-4-2026-06_52_58-PM.png (Thruster Control card)
- After: new copies about 110 to 125 KB each: same picture, 1400 pixels wide, WebP format, quality about 80. Upload them as NEW media files (never overwrite or delete the originals), then point those two cards at the new files. Keep the alt text from item 6.
- If an image optimisation plugin (for example the LiteSpeed Cache image optimisation) is already installed, using it to produce WebP copies is acceptable. Tell Rahul which route you used.
- Target: all unique images on the Home page together under 1.5 MB (they were about 5.4 MB).

### Item 8. Analytics and click tracking
- Before: no analytics tag found in the page source. First check the installed plugin list in case one already exists. If one does, do NOT add a second, report it.
- After: (a) install the official "Site Kit by Google" plugin and let RAHUL do the Google sign-in himself, then connect Analytics (GA4) and Search Console, and submit https://sinormarine.com/sitemap_index.xml. (b) In Analytics, mark the page view of /thank-you/ as a key event if Rahul can do it. (c) Add this click-tracking snippet in the site footer with the code snippets plugin. It records calls, emails and WhatsApp clicks as events and only works once Google's tracking code is on the site:

```html
<script>
document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a[href]'); if(!a||typeof gtag!=='function')return;
  var h=a.getAttribute('href')||'',t=null;
  if(h.indexOf('tel:')===0)t='click_to_call';
  else if(h.indexOf('mailto:')===0)t='click_to_email';
  else if(/wa\.me|api\.whatsapp\.com|^whatsapp:/.test(h))t='click_to_whatsapp';
  if(t)gtag('event',t,{link_url:h,page_path:location.pathname});
},true);
</script>
```

### Item 9. Claims text (Rahul confirmed these figures for public use on 2026-11-06)

| Where | Change |
|---|---|
| Home hero, "50+ Projects Completed" | 100+ Projects Completed |
| Home hero, "98% Client Satisfaction" | 15+ Years of DP Engineering |
| Home and DP page, other places that repeat 50+ or 98% | Same replacements on every page |
| About, stats "50+ Projects", "20+ Years Experience" | 100+ Projects, 15+ Years |
| About, stat "50+ Team Members" | Remove until you give me a number you can prove |
| About, headline "...from 2024" | "Engineering Reliable Marine Automation Solutions" (drop "from 2024") |

Leave everything else on those pages as it is. If a stat block has one fewer item after a removal, tell Rahul how it looks before saving.

### Item 10. Remove "Fuel Monitoring" from the enquiry form
- Before: the "Service Required" dropdown includes "Fuel Monitoring" (no such page exists).
- After: remove only that option. Keep the others: DP Systems, Navigation Systems, Marine Automation, Electrical Solutions, Thruster Control System, Frequency Power Converter, Other.
- Where: the form on the Home page and on the Contact page (Elementor, the form widget, the Service field options).

### Item 11. Home page email link
- Before: the call-to-action near the bottom of the Home page opens an email to a named person.
- After: the email link goes to sales@sinormarine.com. The phone number stays exactly as it is.

---
## PART 4. CHECKS (do these on the live public site after purging the cache)
---
Use view-source or the page itself.
1. DP page: the "Schedule Consultation" button opens the contact page, not an error page.
2. Home: Navigation card opens /services/navigation-systems/. Electrical card opens /services/electrical-solutions/.
3. Every one of the 15 pages shows its new title in the browser tab, and the meta description in view-source matches PART 3. The DP page description no longer says "Sinor Marine Technology".
4. /thank-you/ has a robots meta tag containing noindex and is not listed in https://sinormarine.com/page-sitemap.xml.
5. Home view-source contains a script of type application/ld+json with "Sinor Marine Services Middle East FZCO" and "ProfessionalService".
6. No image on Home or /products/ lacks alt text.
7. Home images total under 1.5 MB (browser network panel, images only).
8. A Google tracking tag is present (view-source shows googletagmanager or gtag), and the text click_to_call appears in the page source.
9. Home shows 100+ Projects Completed, 40+ Countries Served and 15+ Years of DP Engineering. No "98%". About has no "from 2024", no "50+ Team Members", no "20+".
10. Neither the Home nor Contact form dropdown contains "Fuel Monitoring".
11. The Home email link is sales@sinormarine.com and not a personal address.

---
## PART 5. REPORT FORMAT (reply to Rahul like this)
---
- Backup: what you used.
- Items 1 to 11: DONE (seen live) or NOT DONE, one line each, with what you saw. Say plainly if a step did not work.
- Anything you did not do and why. Anything unexpected you saw but did not touch.
- Questions for Rahul.
- Finish with: "Rahul, bring this report back to Claude and say done. Claude re-checks the live site with a read-only script and gives a pass or fail for 17 checks."
- Then a simple explanation in 2 to 4 plain sentences.

---
## PART 6. BACKGROUND (for context only, not instructions)
---
- Why: the audit found a broken button, mislinked cards, missing page descriptions (12 of 16 pages), no structured data, no analytics found, missing alt text, two 2 MB images, and conflicting company numbers. A full plan and evidence live in the GitHub repository rahulrajalpy16-coder/Marketing-Team, folder campaigns/2026-11-digital-seo-plan/ (you may not have access, you do not need it).
- Before any change, a read-only check of the live site passed 0 of 17 checks. After your work the same check will be run by Claude.
- Nothing in this file authorises anything beyond the 11 items.
