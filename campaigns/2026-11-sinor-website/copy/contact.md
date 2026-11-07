# Copy: Contact (contact.html)

Author: web-copywriter. Date: 2026-11-07. Status: draft. Shared header, footer and skip link text are defined in copy/home.md. The header pill is not shown on this page.
Marker rule: CLAIM TO VERIFY = depends on Rahul's STATED facts. The form is NOT connected to anything. No email, phone, address, hours, response time or "thank you" is written. No reply promise appears anywhere.

## Title and meta
- Title: Contact Sinor Marine | Send an Enquiry or Support Request (57 characters, counted by hand)
- Meta description: Send an enquiry to Sinor Marine about Dynamic Positioning, automation, thrusters or support. The form is not connected yet; see other routes. (141 characters, counted by hand)
- CLAIM TO VERIFY: topics listed come from the STATED scope. Remove the "not connected" sentence from the meta once Rahul connects the form.

## 6.1 Page intro

H1 (3 words): Contact Sinor Marine
Intro line: Tell the team what you need. Read the notice below first, because the form does not send yet.

## 6.2 Not-connected notice (above the form heading, always visible, not dismissible)

Bold label: Not connected yet
Text: This form does not send messages yet. Anything you type stays on this page and goes nowhere. To reach the team now, use the contact routes below or the Company LinkedIn page.
Note: the notice is removed in the same change that connects the handler (slot S27).
SLOT S27 | NEEDED FROM RAHUL | Form endpoint or mailto address, and who receives enquiries. Build note only, not visible to visitors. Success and failure wording is written once this is known.

## 6.3 Enquiry form (id="enquiry")

H2: Send an enquiry
Line: Fields marked required are needed to send.

Fields (label above control; "required" is part of the label text)
1. Label: Name (required)
   - Help text: Your full name.
2. Label: Organisation
   - Help text: Optional. The company you work for.
3. Label: Email (required)
   - Help text: The address this message is from.
4. Label: Phone
   - Help text: Optional. Digits, spaces, plus, hyphen and brackets, 6 to 20 characters.
5. Label: Topic (required)
   - Help text: Choose the closest match.
   - Options in order: General enquiry | Dynamic Positioning | Reference systems | Marine electrical and automation | Propulsion and thruster controls | Integration | Upgrades | Service and support
6. Label: Vessel or project type
   - Help text: Optional. For example the kind of vessel or project.
7. Label: Message (required)
   - Help text: Useful to include: vessel or project type, the system, location, urgency.
   - Counter (shown at 1800 characters or more): [number] characters remaining
   - No placeholder text on any field.

SLOT S05 | NEEDED FROM RAHUL | Privacy notice text, directly above the submit button, or a recorded decision to launch without it.

Submit button label: Send enquiry

## 6.4 Error messages

Error summary heading: There is a problem
Summary intro line: Check these fields:
Each summary item links to its field and repeats the field message below.
Field messages (each starts with the word "Error:")
- Name empty or under 2 characters: Error: Enter your name, at least 2 characters.
- Email empty: Error: Enter your email address.
- Email malformed: Error: This does not look like an email address. Use the format name@example.com.
- Phone malformed: Error: Use only digits, spaces, plus, hyphen and brackets, 6 to 20 characters.
- Message empty or under 10 characters: Error: Enter a message of at least 10 characters.
- Message over 2000 characters: Error: The message is too long. The limit is 2000 characters.
- Topic: no message needed. If the value is changed outside the form, it resets to General enquiry.

## 6.5 Status messages while not connected

Valid form, with JavaScript (role="status", focus moves here, shown above the button)
- Heading: Not sent
- Text: Your message was not sent. This form is not connected yet, so nothing has left this page. Your text is still in the form. Copy it, then use the contact routes below or the Company LinkedIn page.
- Do not write "thank you", "success" or "we will reply".

No JavaScript state
- The Send enquiry button is switched off. The notice in 6.2 stays visible and says why.
- Extra line under the disabled button: This button is switched off because the form is not connected yet.

Reserved for later (not written, layout reserved): real success and failure messages, to be written once S27 is answered. While sending: button label Sending.

## 6.6 Contact details

H2: Other ways to reach the team
Line shown in draft: These routes appear once Rahul confirms them.
Definition list
- Email: SLOT S01 | NEEDED FROM RAHUL | Public email address.
- Phone: SLOT S02 | NEEDED FROM RAHUL | Public phone number.
- Address: SLOT S03 | NEEDED FROM RAHUL | Public address.
- Hours: SLOT S04 | NEEDED FROM RAHUL | Opening hours and time zone.
- LinkedIn: Company LinkedIn page (opens linkedin.com). URL: https://www.linkedin.com/company/sinor-marine-services/ . STATED by Rahul 2026-11-06, page not opened.
Collapse text if slots are removed at publish: Use the form.

## Alt text on this page
No images. Any decorative icon beside the notice: aria-hidden="true", no alt text. The notice never relies on the icon or on colour.
