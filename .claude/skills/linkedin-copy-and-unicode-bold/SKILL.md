---
name: linkedin-copy-and-unicode-bold
description: Use when writing LinkedIn posts for Rahul or Sinor Marine Services, including voice, structure, and the Unicode bold copy-paste procedure.
---
# LinkedIn copy and Unicode bold

## Voice and structure
- Direct, natural, polished, technically credible. Strong factual opening, clear sentences, useful specifics, short paragraphs.
- Restrained emojis, relevant hashtags. No em dashes. No exaggeration, empty corporate language or invented promises.
- Avoid "proud", "thrilled", "delighted" openings unless the occasion genuinely suits it.
- Personal account: first person, modest, relationship-led, appreciative of colleagues and partners, never overstating Rahul's contribution.
- Company account: confident, accurate, customer-focused.
- Thank partners only where the source material supports it.

## Unicode bold procedure
1. Use real Unicode Mathematical Sans-Serif Bold, never Markdown asterisks.
2. Mark the few words to style with [[double brackets]] in the draft, then run: python3 scripts/unicode_bold.py "<draft>". The script styles A-Z, a-z, 0-9 and leaves URLs, emails, hashtags and @mentions in normal characters.
3. Test on a sample first (python3 scripts/unicode_bold.py --selftest).
4. Style only a hook or short emphasis. Keep body text ordinary for readability and accessibility.
5. Always provide a plain-text version too. Remind Rahul in one line that Unicode bold is styled text, not native formatting, and may render differently across devices and screen readers.
6. Do not invent working @mentions. Tell Rahul which people or companies he must select manually in the composer.
7. Save the final caption as a UTF-8 .txt in campaigns/<name>/exports/ and also show it.
8. The final caption block contains only the text to paste: no labels, comments or upload instructions.
