#!/usr/bin/env python3
"""Convert A-Z, a-z, 0-9 to Mathematical Sans-Serif Bold. Everything else is unchanged.

URLs, email addresses, #hashtags and @mentions are left in normal characters.
Usage:
  python3 scripts/unicode_bold.py "Text to style"
  echo "Text" | python3 scripts/unicode_bold.py
  python3 scripts/unicode_bold.py --selftest
Wrap only short emphasis in the text with [[double square brackets]] to style only those
parts, for example:  "[[Strong opening line.]] Body stays plain."
Without brackets the whole input is styled (use for a short hook only).
Always save the final caption as UTF-8 and provide a plain-text version too.
"""
import re
import sys

BOLD_UPPER = 0x1D5D4  # Mathematical Sans-Serif Bold Capital A
BOLD_LOWER = 0x1D5EE  # Mathematical Sans-Serif Bold Small a
BOLD_DIGIT = 0x1D7EC  # Mathematical Sans-Serif Bold Digit Zero

PROTECTED = re.compile(r"(https?://\S+|www\.\S+|\S+@\S+\.\S+|[#@][\w-]+)")


def _map_char(ch: str) -> str:
    if "A" <= ch <= "Z":
        return chr(BOLD_UPPER + ord(ch) - ord("A"))
    if "a" <= ch <= "z":
        return chr(BOLD_LOWER + ord(ch) - ord("a"))
    if "0" <= ch <= "9":
        return chr(BOLD_DIGIT + ord(ch) - ord("0"))
    return ch


def bold(text: str) -> str:
    parts = PROTECTED.split(text)
    out = []
    for i, part in enumerate(parts):
        out.append(part if i % 2 == 1 else "".join(_map_char(c) for c in part))
    return "".join(out)


def bold_marked(text: str) -> str:
    """Style only the [[...]] segments; strip the brackets."""
    def repl(m):
        return bold(m.group(1))
    return re.sub(r"\[\[(.+?)\]\]", repl, text, flags=re.S)


def selftest() -> int:
    s = bold("Hello ABC xyz 2026 #Marine https://sinor.example a@b.co")
    expected_prefix = "\U0001D5DB\U0001D5F2\U0001D5F9\U0001D5F9\U0001D5FC"  # Hello
    ok = (
        s.startswith(expected_prefix)
        and "#Marine" in s
        and "https://sinor.example" in s
        and "a@b.co" in s
        and bold("2026") == "\U0001D7EE\U0001D7EC\U0001D7EE\U0001D7F2"
        and bold_marked("[[Hi]] there") == bold("Hi") + " there"
    )
    print(s)
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        sys.exit(selftest())
    data = " ".join(args) if args else sys.stdin.read()
    sys.stdout.write(bold_marked(data) if "[[" in data else bold(data))
    if not data.endswith("\n"):
        sys.stdout.write("\n")
