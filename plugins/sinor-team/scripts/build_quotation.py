#!/usr/bin/env python3
"""Sinor Marine standard quotation PDF generator (spec driven).

Usage:
    python3 build_quotation.py <spec.json> --out <file.pdf> [--logo <png>] [--check]

The spec format and every computation rule are in ../references/quotation-spec.md.
Only reportlab and the standard library are required. --check additionally uses
pdftotext (poppler) or pypdf to read the rendered PDF back; a check that cannot run is
reported as NOT RUN, never as PASS.

Exit codes: 0 ok, 2 invalid spec or bad arguments, 3 render failure, 4 --check found a FAIL.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from xml.sax.saxutils import escape

SINOR_TRN = "104218013100003"
TWO = Decimal("0.01")
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LOGO = os.path.normpath(os.path.join(HERE, "..", "assets", "brand", "sinor-logo.png"))

FOOTER_DISCLAIMER = "* This is a computer generated document and doesn't need any signature. *"
FOOTER_LEFT = ["SINOR MARINE SERVICES MIDDLE EAST FZCO", "601, Al Nokitha Building, Hamariya Port, DUBAI",
               "Post Box : 95842", "UAE"]
FOOTER_RIGHT = ["Tel : 04 665 7162", "Fax :", "sales@sinormarine.com", "www.sinormarine.com"]

DEFAULT_TERMS = {
    "payment": "100% Advance",
    "delivery_terms": "Ex Works UAE",
    "delivery_period": "",
    "validity": "10 Days",
    "exclusions": ["Visa, Travel tickets, Boarding & Lodging if not in UAE.",
                   "Mechanical & Hot works, Cable Penetration, Fabrication, Carpentry, Rigging & Mounting."],
    "warranty": "Standard OEM Warranty",
}
TERM_LABELS = [("payment", "Payment Terms"), ("delivery_terms", "Delivery Terms"),
               ("delivery_period", "Delivery Period"), ("validity", "Validity"),
               ("exclusions", "Exclusions"), ("warranty", "Warranty")]

# Verbatim from skills/sinor-quotation/SKILL.md section 2 (italic applicability hints removed).
NOTE_SETS = {
    "standard": [
        "All price quoted above are exclusive of VAT.",
        "Any approvals / entry pass requirements for engineers/technicians / labors to be arranged by client.",
        "All Mechanical site Jobs like Hot works, Painting Jobs, will be client scope.",
        "The site/ area access supports like staging's, clear access etc. if required to be arranged by Client /Yard.",
        "There will be supports required from client regarding the access, permission, Isolation and identification of power, existing cables, route etc.",
        "Integration with the existing DP system shall be carried out by the DP manufacturer.",
        "Any scopes which required other than mentioned in the quotation, will be quoted separate.",
        "Any additional days or scope of work beyond those mentioned in this quotation will be charged separately.",
        "Shipping and delivery costs are excluded.",
        "For HPR the lead time mentioned in our quotation is considered up to delivery onboard.",
    ],
    "installation_newer": [
        "Any additional standby days or delays arising beyond our responsibility shall be charged separately on an additional man-day basis.",
        "Any scope of work not explicitly mentioned in this quotation shall be considered excluded and will be quoted separately.",
        "All prices quoted above are exclusive of VAT.",
        "Sea trial attendance and support are included in our scope.",
        "DP hardware/software interfacing and integration on the vessel's DP system side are excluded from our scope.",
        "Any approvals, entry passes, permits, or authorization requirements for engineers, technicians, and labor shall be arranged by the Client.",
        "All mechanical site works, including hot works and painting, shall remain under the Client's scope.",
        "Site and area access support, including staging, scaffolding, and provision of clear working access (if required), shall be arranged by the Client/Yard.",
        "The Client shall provide necessary support for access, permits, power isolation, identification of existing cables, and confirmation of cable routing and system interfaces required for execution.",
    ],
    "supply_only": [
        "Shipping and delivery costs are excluded.",
        "The quotation only covers the supply of the unit.",
        "Price quoted above are exclusive of VAT",
    ],
}
# When "notes" is absent: the standard set without the two job specific notes (6 DP, 10 HPR).
DEFAULT_NOTES_DROP = [6, 10]

SIGNATORY_DEFAULT = {"name": "Naveen Thandarath", "phone": "+971 58 662 6123", "email": "naveen@sinormarine.com"}

KNOWN_TYPOS = ["NINENTY", "Stricty", "Rechargable", "Taught wire", "sytem", "Thandarth", "anaysis"]


class SpecError(Exception):
    def __init__(self, errors):
        super().__init__("\n".join(errors))
        self.errors = errors


def warn(msg):
    print("WARNING: " + msg, file=sys.stderr)


# ---------------------------------------------------------------- arithmetic
def q2(d):
    return d.quantize(TWO, rounding=ROUND_HALF_UP)


def money(d):
    return f"{q2(d):,.2f}"


def to_dec(value, what, errors, allow_zero=True, maximum=None):
    """Parse a spec number into Decimal. Appends to errors and returns None when invalid."""
    if isinstance(value, bool) or value is None or value == "":
        errors.append(f"{what}: a number is required (got {value!r})")
        return None
    try:
        d = Decimal(str(value).replace(",", "").strip())
    except (InvalidOperation, ValueError):
        errors.append(f"{what}: not a number ({value!r})")
        return None
    if not d.is_finite():
        errors.append(f"{what}: not a finite number ({value!r})")
        return None
    if d < 0:
        errors.append(f"{what}: must not be negative ({value!r})")
        return None
    if not allow_zero and d == 0:
        errors.append(f"{what}: must be greater than zero")
        return None
    if maximum is not None and d > maximum:
        errors.append(f"{what}: must be at most {maximum} ({value!r})")
        return None
    return d


def fmt_pct(d):
    s = format(d.normalize(), "f")
    return s


def fmt_qty(d):
    return format(d.normalize(), "f")


_ONES = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN",
         "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
_TENS = ["", "", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
_SCALES = ["", "THOUSAND", "MILLION", "BILLION", "TRILLION"]


def _below_1000(n):
    out = []
    if n >= 100:
        out += [_ONES[n // 100], "HUNDRED"]
        n %= 100
    if n >= 20:
        out.append(_TENS[n // 10])
        n %= 10
        if n:
            out.append(_ONES[n])
    elif n > 0:
        out.append(_ONES[n])
    return out


def int_words(n):
    if n == 0:
        return "ZERO"
    parts, i = [], 0
    while n > 0:
        n, chunk = divmod(n, 1000)
        if chunk:
            w = _below_1000(chunk)
            if _SCALES[i]:
                w.append(_SCALES[i])
            parts = w + parts
        i += 1
        if i >= len(_SCALES) and n:
            raise ValueError("amount too large")
    return " ".join(parts)


def amount_in_words(amount, currency="USD"):
    """House style (QUOTATION_PRACTICE.md section 5): no hyphens, no AND inside the number,
    `AND CENT <WORDS>` for cents, e.g. USD TWENTY EIGHT THOUSAND THREE HUNDRED EIGHTY THREE AND CENT SEVENTY FIVE ONLY."""
    a = q2(Decimal(amount))
    if a < 0:
        raise ValueError("negative amount")
    whole = int(a)
    cents = int((a - whole) * 100)
    text = f"{currency} {int_words(whole)}"
    if cents:
        text += f" AND CENT {int_words(cents)}"
    return text + " ONLY"


# ---------------------------------------------------------------- spec handling
def _s(v):
    return "" if v is None else str(v).strip()


def _str_list(v, what, errors):
    if v is None:
        return []
    if isinstance(v, str):
        return [v] if v.strip() else []
    if isinstance(v, list) and all(isinstance(x, str) for x in v):
        return [x for x in v if x.strip()]
    errors.append(f"{what}: must be a list of strings")
    return []


def _parse_item(raw, where, errors):
    if not isinstance(raw, dict):
        errors.append(f"{where}: item must be an object")
        return None
    title = _s(raw.get("title"))
    text = _str_list(raw.get("text"), where + ".text", errors)
    if not title and not text:
        errors.append(f"{where}: needs a title")
    qty = to_dec(raw.get("qty"), where + ".qty", errors, allow_zero=False)
    price = to_dec(raw.get("price"), where + ".price", errors)
    blocks = []
    inc = _str_list(raw.get("include"), where + ".include", errors)
    if inc:
        blocks.append((_s(raw.get("include_heading")) or "Include:-", inc))
    scope = _str_list(raw.get("scope"), where + ".scope", errors)
    if scope:
        blocks.append((_s(raw.get("scope_heading")) or "Scope of Work:", scope))
    for i, b in enumerate(raw.get("blocks") or []):
        if not isinstance(b, dict):
            errors.append(f"{where}.blocks[{i}]: must be an object with heading and lines")
            continue
        blocks.append((_s(b.get("heading")), _str_list(b.get("lines"), f"{where}.blocks[{i}].lines", errors)))
    unit = _s(raw.get("unit"))
    if not unit:
        errors.append(f"{where}.unit: required (for example Lsum, Nos, Set, Day)")
    if qty is None or price is None:
        return None
    price = q2(price)  # unit price normalised to 2 decimals first (same as the sales tool), then qty x price
    return {"title": title, "text": text, "blocks": blocks, "qty": qty, "unit": unit, "price": price,
            "amount": q2(qty * price)}


def load_spec(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SpecError([f"spec file not found: {path}"])
    except json.JSONDecodeError as e:
        raise SpecError([f"spec is not valid JSON: {e}"])


def normalise(spec, today=None):
    """Validate the spec and return the resolved model. Raises SpecError listing every problem.
    Warnings (assumed values) are returned in model['warnings']."""
    errors, warnings = [], []
    today = today or datetime.date.today()
    if not isinstance(spec, dict):
        raise SpecError(["spec must be a JSON object"])

    client = spec.get("client") if isinstance(spec.get("client"), dict) else {}
    cname = _s(client.get("name"))
    if not cname:
        errors.append("client.name is required")

    quote = spec.get("quote") if isinstance(spec.get("quote"), dict) else {}
    date_s = _s(quote.get("date"))
    if date_s:
        try:
            qdate = datetime.datetime.strptime(date_s, "%d/%m/%Y").date()
        except ValueError:
            errors.append(f"quote.date must be DD/MM/YYYY (got {date_s!r})")
            qdate = today
    else:
        qdate = today
        date_s = today.strftime("%d/%m/%Y")
        warnings.append(f"quote.date not given, using today {date_s}")
    qtn = _s(quote.get("qtn_no"))
    if not qtn:
        qtn = f"SMS-QT{qdate.year}-XXXXX"
        warnings.append(f"quote.qtn_no not given: printing {qtn}. Ask for the real QTN number before issue.")
    elif not re.match(r"^SMS-QT\d{4}-(\d{5}|X{5})(-R\d+|-D\d*)*$", qtn):
        warnings.append(f"quote.qtn_no {qtn!r} does not match SMS-QT{{YYYY}}-{{NNNNN}}[-Rn|-Dn]; printed unchanged")
    your_ref = _s(quote.get("your_ref")) or "Email"
    currency = (_s(quote.get("currency")) or "USD").upper()

    mode = _s(spec.get("mode")) or "additive"
    if mode not in ("additive", "alternatives"):
        errors.append(f"mode must be 'additive' or 'alternatives' (got {mode!r})")

    # items / sections
    sections = []
    if spec.get("items") and spec.get("sections"):
        errors.append("give either 'items' or 'sections', not both")
    if spec.get("sections"):
        if not isinstance(spec["sections"], list):
            errors.append("sections must be a list")
        else:
            for si, sec in enumerate(spec["sections"], 1):
                if not isinstance(sec, dict) or not sec.get("items"):
                    errors.append(f"sections[{si}]: needs a non-empty 'items' list")
                    continue
                items = []
                for ii, raw in enumerate(sec["items"], 1):
                    it = _parse_item(raw, f"sections[{si}].items[{ii}]", errors)
                    if it:
                        it["no"] = f"{si}.{ii}"
                        items.append(it)
                sections.append({"name": _s(sec.get("name")), "no": str(si), "items": items})
    elif spec.get("items"):
        if not isinstance(spec["items"], list):
            errors.append("items must be a list")
        else:
            items = []
            for ii, raw in enumerate(spec["items"], 1):
                it = _parse_item(raw, f"items[{ii}]", errors)
                if it:
                    it["no"] = str(ii)
                    items.append(it)
            sections = [{"name": "", "no": "", "items": items}]
    else:
        errors.append("at least one item is required ('items' or 'sections')")
    sectioned = bool(spec.get("sections"))

    # totals
    vat_pct = to_dec(spec.get("vat_percent", 0), "vat_percent", errors, maximum=Decimal(100))
    disc_raw = spec.get("discount")
    disc = {"kind": None}
    if disc_raw is not None:
        if not isinstance(disc_raw, dict) or (("amount" in disc_raw) == ("percent" in disc_raw)):
            errors.append("discount must be an object with exactly one of 'amount' or 'percent'")
        elif "amount" in disc_raw:
            a = to_dec(disc_raw["amount"], "discount.amount", errors)
            disc = {"kind": "amount", "value": a}
        else:
            p = to_dec(disc_raw["percent"], "discount.percent", errors, maximum=Decimal(100))
            disc = {"kind": "percent", "value": p}
    if mode == "alternatives" and (disc_raw is not None or spec.get("vat_percent")):
        warnings.append("discount/vat_percent ignored: mode 'alternatives' prints blank total rows")

    if errors:
        raise SpecError(errors)

    all_items = [it for s in sections for it in s["items"]]
    total = sum((it["amount"] for it in all_items), Decimal(0))
    discount = Decimal(0)
    if mode == "additive":
        if disc["kind"] == "amount":
            discount = q2(disc["value"])
        elif disc["kind"] == "percent":
            discount = q2(total * disc["value"] / 100)
        if discount > total:
            raise SpecError([f"discount {money(discount)} exceeds total {money(total)}"])
    base = total - discount
    vat = q2(base * vat_pct / 100) if mode == "additive" else Decimal(0)
    net = total - discount + vat

    disc_label = "Discount :"
    if disc["kind"] == "percent":
        disc_label = f"Discount {fmt_pct(disc['value'])}% :"
    vat_label = _s(spec.get("vat_label"))
    if not vat_label:
        vat_label = f"VAT {fmt_pct(vat_pct)}% :" if vat_pct > 0 else "VAT :"
    else:
        vat_label = vat_label if vat_label.endswith(":") else vat_label + " :"

    # terms
    terms_in = spec.get("terms") or {}
    if not isinstance(terms_in, dict):
        raise SpecError(["terms must be an object"])
    terms = {}
    for key, _label in TERM_LABELS:
        v = terms_in.get(key, DEFAULT_TERMS[key])
        lines = _str_list(v, f"terms.{key}", errors) if not isinstance(v, str) else [x for x in v.split("\n") if x.strip()]
        terms[key] = lines
    if not terms["delivery_period"]:
        warnings.append("terms.delivery_period not given: left blank (never invented). Confirm per item or option.")
    unknown = set(terms_in) - set(DEFAULT_TERMS)
    if unknown:
        errors.append("unknown terms field(s): " + ", ".join(sorted(unknown)))

    # notes
    notes_in = spec.get("notes")
    notes = []
    if notes_in is None:
        notes = [n for i, n in enumerate(NOTE_SETS["standard"], 1) if i not in DEFAULT_NOTES_DROP]
    elif isinstance(notes_in, list):
        notes = _str_list(notes_in, "notes", errors)
    elif isinstance(notes_in, str):
        if notes_in in NOTE_SETS:
            notes = list(NOTE_SETS[notes_in])
        else:
            errors.append(f"notes: unknown set {notes_in!r} (use {', '.join(NOTE_SETS)})")
    elif isinstance(notes_in, dict):
        setname = _s(notes_in.get("set")) or "standard"
        if setname not in NOTE_SETS:
            errors.append(f"notes.set: unknown set {setname!r} (use {', '.join(NOTE_SETS)})")
        else:
            drop = notes_in.get("drop") or []
            if not (isinstance(drop, list) and all(isinstance(x, int) and not isinstance(x, bool) for x in drop)):
                errors.append("notes.drop must be a list of 1-based note numbers")
            else:
                bad = [x for x in drop if not 1 <= x <= len(NOTE_SETS[setname])]
                if bad:
                    errors.append(f"notes.drop: no such note number(s) {bad} in set {setname!r}")
                notes = [n for i, n in enumerate(NOTE_SETS[setname], 1) if i not in drop]
            notes += _str_list(notes_in.get("add"), "notes.add", errors)
    else:
        errors.append("notes must be a list, a set name or an object")

    # signatory
    sig_in = spec.get("signatory", "default")
    if sig_in is False or sig_in is None:
        signatory = None
    elif sig_in == "default":
        signatory = dict(SIGNATORY_DEFAULT)
    elif isinstance(sig_in, dict):
        signatory = {k: _s(sig_in.get(k)) for k in ("name", "title", "phone", "email")}
        if not signatory["name"]:
            errors.append("signatory.name is required when signatory is an object")
    else:
        errors.append("signatory must be 'default', false or an object")
        signatory = None

    if errors:
        raise SpecError(errors)

    return {
        "client": {k: _s(client.get(k)) for k in ("name", "address", "tel", "attn", "trn")},
        "qtn": qtn, "date": date_s, "your_ref": your_ref, "currency": currency,
        "subject": _s(spec.get("subject")), "mode": mode, "sections": sections, "sectioned": sectioned,
        "total": total, "discount": discount, "vat": vat, "net": net,
        "disc_label": disc_label, "vat_label": vat_label, "vat_pct": vat_pct,
        "words": amount_in_words(net, currency) if mode == "additive" else None,
        "terms": terms, "notes": notes, "signatory": signatory, "warnings": warnings,
    }


# ---------------------------------------------------------------- rendering
def render(model, out_path, logo_path=None):
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.pdfgen import canvas as cv
    from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph, Spacer,
                                    Table, TableStyle)

    W, H = A4
    M = 15 * mm
    CW = W - 2 * M
    F, FB = "Helvetica", "Helvetica-Bold"
    NAVY = colors.HexColor("#0D4A85")
    cur = model["currency"]

    def S(name, **k):
        d = dict(fontName=F, fontSize=9, leading=11.5)
        d.update(k)
        return ParagraphStyle(name, **d)

    body, bold = S("b"), S("bb", fontName=FB)
    ctr, rgt = S("c", alignment=TA_CENTER), S("r", alignment=TA_RIGHT)
    hdr = S("h", fontName=FB, alignment=TA_CENTER)
    rb = S("rb", fontName=FB, alignment=TA_RIGHT)
    li = S("li", leftIndent=8, firstLineIndent=0)

    def P(t, s=body):
        return Paragraph(t, s)

    def E(t):
        return escape(t)

    have_logo = bool(logo_path) and os.path.isfile(logo_path)
    if not have_logo:
        warn(f"logo not found ({logo_path}); using the text-only header")

    class NumberedCanvas(cv.Canvas):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self._saved = []

        def showPage(self):
            self._saved.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            n = len(self._saved)
            for st in self._saved:
                self.__dict__.update(st)
                self._decor(n)
                super().showPage()
            super().save()

        def _decor(self, n):
            if have_logo:
                lh = 17 * mm
                lw = lh * 1041 / 396
                self.drawImage(logo_path, M, H - M - lh + 3 * mm, width=lw, height=lh, mask="auto")
            else:
                self.setFillColor(NAVY)
                self.setFont(FB, 15)
                self.drawString(M, H - M - 7 * mm, "SINOR MARINE SERVICES")
                self.setFont(FB, 10)
                self.drawString(M, H - M - 13 * mm, "MIDDLE EAST FZCO")
                self.setFillColor(colors.black)
            self.setFillColor(colors.black)
            self.setFont(FB, 18)
            self.drawRightString(W - M, H - M - 8 * mm, "QUOTATION")
            self.setFont(F, 8)
            self.drawCentredString(W / 2, 27 * mm, FOOTER_DISCLAIMER)
            self.drawRightString(W - M, 27 * mm, "E&OE")
            y = 22 * mm
            for i, t in enumerate(FOOTER_LEFT):
                self.drawString(M, y - i * 3.4 * mm, t)
            for i, t in enumerate(FOOTER_RIGHT):
                self.drawRightString(W - M, y - i * 3.4 * mm, t)
            self.drawCentredString(W / 2, y - 3.4 * mm, "Page %d of %d" % (self._pageNumber, n))

    doc = BaseDocTemplate(out_path, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M,
                          title=model["qtn"], author="Sinor Marine Services Middle East FZCO")
    frame = Frame(M, 32 * mm, CW, H - M - 32 * mm - 22 * mm, leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame])])

    black, box = colors.black, 0.8
    c = model["client"]
    el = []

    def val(t):
        return P(":  " + (E(t) if t else ""))

    info = Table([
        [P("Name"), P(":  <b>%s</b>" % E(c["name"])), P("QTN No"), P(":  <b>%s</b>" % E(model["qtn"]))],
        [P("Address"), val(c["address"]), P("QTN Date"), val(model["date"])],
        [P("Tel"), val(c["tel"]), P("Your Ref."), val(model["your_ref"])],
        [P("Attn."), val(c["attn"]), P("Currency"), val(cur)],
        [P("TRN"), val(c["trn"]), P("TRN"), val(SINOR_TRN)],
    ], colWidths=[18 * mm, CW - 18 * mm - 95 * mm, 20 * mm, 75 * mm])
    info.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), box, black), ("LINEBEFORE", (2, 0), (2, -1), box, black),
                              ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    subj = Table([[P("Subject"), P(":  " + E(model["subject"]))]], colWidths=[18 * mm, CW - 18 * mm])
    subj.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), box, black), ("TOPPADDING", (0, 0), (-1, -1), 3),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    el += [Spacer(1, 3 * mm), info, subj, Spacer(1, 4 * mm), P("Dear Sir,"), Spacer(1, 3 * mm),
           P("Thank you very much for your enquiry and we are pleased to quote you the following."),
           Spacer(1, 4 * mm)]

    # items table: one row per description line so long items can split across pages
    cw = [12 * mm, CW - 12 * mm - 12 * mm - 14 * mm - 28 * mm - 26 * mm, 12 * mm, 14 * mm, 28 * mm, 26 * mm]
    rows = [[P("No", hdr), P("Description", hdr), P("Qty", hdr), P("Unit", hdr),
             P("Price<br/>(%s)" % E(cur), hdr), P("Amount<br/>(%s)" % E(cur), hdr)]]
    cmds = [("BOX", (0, 0), (-1, -1), 0.5, black), ("GRID", (0, 0), (-1, 0), 0.5, black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("TOPPADDING", (0, 0), (-1, 0), 3), ("BOTTOMPADDING", (0, 0), (-1, 0), 3)]
    for col in range(1, 6):
        cmds.append(("LINEBEFORE", (col, 0), (col, -1), 0.5, black))

    def close_item(first, last):
        cmds.append(("LINEBELOW", (0, last), (-1, last), 0.5, black))
        cmds.append(("TOPPADDING", (0, first), (-1, first), 3))
        cmds.append(("BOTTOMPADDING", (0, last), (-1, last), 3))
        if last > first:
            cmds.append(("NOSPLIT", (0, first), (-1, first + 1)))

    for sec in model["sections"]:
        if model["sectioned"] and sec["name"]:
            r = len(rows)
            rows.append([P(sec["no"], ctr), P("<b>%s</b>" % E(sec["name"])), "", "", "", ""])
            close_item(r, r)
        for it in sec["items"]:
            first = len(rows)
            desc = []
            if it["title"]:
                desc.append(P("<b>%s</b>" % E(it["title"])))
            desc += [P(E(t)) for t in it["text"]]
            for heading, lines in it["blocks"]:
                if heading:
                    desc.append(P("<b>%s</b>" % E(heading)))
                desc += [P(E(t), li) for t in lines]
            rows.append([P(it["no"], ctr), desc[0], P(fmt_qty(it["qty"]), ctr), P(E(it["unit"]), ctr),
                         P(money(it["price"]), rgt), P(money(it["amount"]), rgt)])
            for d in desc[1:]:
                rows.append(["", d, "", "", "", ""])
            close_item(first, len(rows) - 1)
        if model["sectioned"] and model["mode"] == "additive":
            r = len(rows)
            sub = sum((i["amount"] for i in sec["items"]), Decimal(0))
            label = "Sub-total Section %s%s :" % (sec["no"], " (%s)" % E(sec["name"]) if sec["name"] else "")
            rows.append(["", P(label, rb), "", "", "", P(money(sub), rb)])
            close_item(r, r)
    items_tbl = Table(rows, colWidths=cw, repeatRows=1)
    items_tbl.setStyle(TableStyle(cmds))

    # totals block (4 rows, always; blank for alternatives)
    left_w = cw[0] + cw[1] + cw[2] + cw[3]
    if model["mode"] == "additive":
        trows = [[P("Amount in Words : " + E(model["words"])), P("Total :", rb), P(money(model["total"]), rb)],
                 ["", P(E(model["disc_label"]), rb), P(money(model["discount"]), rb)],
                 ["", P(E(model["vat_label"]), rb), P(money(model["vat"]), rb)],
                 ["", P("Net Amount :", rb), P(money(model["net"]), rb)]]
    else:
        trows = [["", "", ""] for _ in range(4)]
    tot = Table(trows, colWidths=[left_w, cw[4], cw[5]], rowHeights=None if model["mode"] == "additive" else [6.5 * mm] * 4)
    tot.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, black), ("LINEBEFORE", (1, 0), (2, -1), 0.5, black),
                             ("LINEBELOW", (1, 0), (-1, -2), 0.5, black), ("SPAN", (0, 0), (0, 3)),
                             ("VALIGN", (0, 0), (0, 3), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    el += [items_tbl, KeepTogether([tot]), Spacer(1, 4 * mm)]

    # terms
    trows = []
    for key, label in TERM_LABELS:
        lines = model["terms"][key]
        if len(lines) > 1:
            lines = ["%d. %s" % (i, t) for i, t in enumerate(lines, 1)]
        trows.append([P(label, bold), P("<br/>".join(E(t) for t in lines))])
    tt = Table(trows, colWidths=[32 * mm, CW - 32 * mm])
    tt.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, black), ("LINEBEFORE", (1, 0), (1, -1), 0.5, black),
                            ("LINEBELOW", (0, 0), (-1, -2), 0.5, black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    el += [tt, Spacer(1, 4 * mm)]

    if model["notes"]:
        el += [P("Notes:", bold), Spacer(1, 2)]
        nt = Table([[P("%d." % (i + 1)), P(E(t))] for i, t in enumerate(model["notes"])],
                   colWidths=[7 * mm, CW - 7 * mm])
        nt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 1), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
        el.append(nt)
    el.append(Spacer(1, 6 * mm))

    closing = [P("We sincerely trust that this quotation is in accordance with your requirement and look forward to your kind order."),
               Spacer(1, 3 * mm), P("Thanking You,"), Spacer(1, 3 * mm),
               P("For SINOR MARINE SERVICES MIDDLE EAST FZCO", bold)]
    sig = model["signatory"]
    if sig:
        closing.append(Spacer(1, 8 * mm))
        for k in ("name", "title", "phone", "email"):
            if sig.get(k):
                closing.append(P(E(sig[k])))
    el.append(KeepTogether(closing))
    doc.build(el, canvasmaker=NumberedCanvas)


# ---------------------------------------------------------------- --check
def _pdf_pages_text(pdf):
    """Return (list of page texts in layout mode, tool name) or (None, None)."""
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True)
        if r.returncode == 0:
            pages = r.stdout.split("\f")
            if pages and not pages[-1].strip():
                pages = pages[:-1]
            return pages, "pdftotext"
    try:
        import pypdf
        rd = pypdf.PdfReader(pdf)
        return [p.extract_text() or "" for p in rd.pages], "pypdf"
    except ImportError:
        return None, None


def _num(s):
    return Decimal(s.replace(",", ""))


def run_checks(model, pdf):
    """Return list of (name, status, detail); status in PASS, FAIL, NOT RUN."""
    res = []
    pages, tool = _pdf_pages_text(pdf)
    if pages is None:
        for n in ("Page X of Y on every page", "Footer complete and not wrapped", "Item arithmetic from PDF text",
                  "Totals and Amount in Words from PDF text", "No leading '. ' artefacts", "Known typos"):
            res.append((n, "NOT RUN", "neither pdftotext nor pypdf is available"))
    else:
        n = len(pages)
        missing = [i for i in range(1, n + 1) if not re.search(r"Page\s+%d\s+of\s+%d\b" % (i, n), pages[i - 1])]
        res.append(("Page X of Y on every page (%s)" % tool, "FAIL" if missing else "PASS",
                    f"missing on pages {missing}" if missing else f"{n} page(s)"))
        bad = []
        for i, pg in enumerate(pages, 1):
            flat = pg
            for need in (FOOTER_DISCLAIMER, "sales@sinormarine.com", "www.sinormarine.com", "E&OE",
                         "SINOR MARINE SERVICES MIDDLE EAST FZCO", "601, Al Nokitha Building, Hamariya Port, DUBAI"):
                if need not in flat:
                    bad.append(f"p{i}: missing {need!r}")
        res.append(("Footer complete and not wrapped", "FAIL" if bad else "PASS", "; ".join(bad) or "all pages"))

        full = "\n".join(pages)
        # item arithmetic from text
        pat = re.compile(r"(\S+)\s+(\S+)\s+([\d,]+\.\d\d)\s+([\d,]+\.\d\d)\s*$")
        found, errs = [], []
        for line in full.splitlines():
            m = pat.search(line)
            if not m:
                continue
            try:
                qty, price, amt = _num(m.group(1)), _num(m.group(3)), _num(m.group(4))
            except InvalidOperation:
                continue
            found.append(amt)
            if q2(qty * price) != amt:
                errs.append(f"{m.group(1)} x {m.group(3)} != {m.group(4)}")
        expected_items = [it["amount"] for s in model["sections"] for it in s["items"]]
        exp_n = len(expected_items)
        if errs or len(found) != exp_n or sorted(found) != sorted(expected_items):
            res.append(("Item arithmetic from PDF text", "FAIL",
                        "; ".join(errs) or f"found {len(found)} priced rows, expected {exp_n}"))
        else:
            res.append(("Item arithmetic from PDF text", "PASS", f"{exp_n} rows: qty x price = amount"))

        if model["mode"] != "additive":
            res.append(("Totals and Amount in Words from PDF text", "NOT RUN", "mode 'alternatives' prints no totals"))
        else:
            def grab(label):
                m = re.search(re.escape(label) + r"\s+([\d,]+\.\d\d)", full)
                return _num(m.group(1)) if m else None
            t, d, v, nt = grab("Total :"), None, None, grab("Net Amount :")
            md = re.search(r"Discount[^:\n]*:\s+([\d,]+\.\d\d)", full)
            mv = re.search(r"VAT[^:\n]*:\s+([\d,]+\.\d\d)", full)
            d = _num(md.group(1)) if md else None
            v = _num(mv.group(1)) if mv else None
            if None in (t, d, v, nt):
                res.append(("Totals and Amount in Words from PDF text", "FAIL", "total rows not found in text"))
            else:
                sum_items = sum(found, Decimal(0))
                probs = []
                if sum_items != t:
                    probs.append(f"sum of items {money(sum_items)} != Total {money(t)}")
                if t - d + v != nt:
                    probs.append(f"Total-Discount+VAT {money(t - d + v)} != Net {money(nt)}")
                # Amount in Words: take lines from 'Amount in Words' to 'Net Amount', drop right-hand label text
                lines = full.splitlines()
                start = next((i for i, l in enumerate(lines) if "Amount in Words" in l), None)
                words = ""
                if start is not None:
                    for l in lines[start:start + 6]:
                        l2 = re.sub(r"\s{2,}(Total|Discount[^:]*|VAT[^:]*|Net Amount)\s*:.*$", "", l)
                        words += " " + l2
                        if "ONLY" in l2:
                            break
                words = re.sub(r"\s+", " ", words).strip()
                want = "Amount in Words : " + amount_in_words(nt, model["currency"])
                if words != want:
                    probs.append(f"words {words!r} != {want!r}")
                res.append(("Totals and Amount in Words from PDF text", "FAIL" if probs else "PASS",
                            "; ".join(probs) or f"Total {money(t)}, Net {money(nt)}, words match Net"))

        art = [l for l in full.splitlines() if re.match(r"^\s*\.\s", l)]
        res.append(("No leading '. ' artefacts in PDF text", "FAIL" if art else "PASS",
                    f"{len(art)} line(s) start with '. '" if art else "none found"))
        typos = [t for t in KNOWN_TYPOS if t.lower() in full.lower()]
        res.append(("Known typos (NINENTY, Stricty, Rechargable, Taught wire, sytem, Thandarth, anaysis)",
                    "FAIL" if typos else "PASS", ", ".join(typos) or "none found"))

    # spec-level checks
    addr_bad = [l for l in model["client"]["address"].splitlines() if l.startswith(". ")] \
        or ([model["client"]["address"]] if model["client"]["address"].startswith(". ") else [])
    res.append(("No leading '. ' in client address (spec)", "FAIL" if addr_bad else "PASS",
                "address starts with '. '" if addr_bad else "ok"))
    nos = {it["no"] for s in model["sections"] for it in s["items"]}
    refs, missing = [], []
    for key in ("delivery_terms", "delivery_period"):
        for line in model["terms"][key]:
            for m in re.finditer(r"\bItems?\s+((?:\d+(?:\.\d+)?)(?:\s*(?:,|&|and|to)\s*\d+(?:\.\d+)?)*)", line, re.I):
                for num in re.findall(r"\d+(?:\.\d+)?", m.group(1)):
                    refs.append(num)
                    if num not in nos:
                        missing.append(num)
    if missing:
        res.append(("Delivery lines reference existing item numbers", "FAIL", "no such item(s): " + ", ".join(missing)))
    else:
        res.append(("Delivery lines reference existing item numbers", "PASS",
                    f"{len(refs)} reference(s) checked" if refs else "no 'Item n' references in delivery lines"))
    return res


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="Build a Sinor quotation PDF from a JSON spec.")
    ap.add_argument("spec")
    ap.add_argument("--out", required=True, help="output PDF path")
    ap.add_argument("--logo", help="logo PNG (default: ../assets/brand/sinor-logo.png next to this script)")
    ap.add_argument("--check", action="store_true", help="run the automatic section 4 checks on the PDF")
    args = ap.parse_args(argv)

    try:
        model = normalise(load_spec(args.spec))
    except SpecError as e:
        print("ERROR: invalid quotation spec:", file=sys.stderr)
        for line in e.errors:
            print("  - " + line, file=sys.stderr)
        return 2
    for w in model["warnings"]:
        warn(w)
    logo = args.logo if args.logo else DEFAULT_LOGO
    try:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        render(model, args.out, logo)
    except ImportError as e:
        print(f"ERROR: reportlab is required ({e}). Run: pip install reportlab", file=sys.stderr)
        return 3
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: could not render the PDF: {e}", file=sys.stderr)
        return 3
    print(f"Wrote {args.out}")
    if model["mode"] == "additive":
        print(f"Total {money(model['total'])}  Discount {money(model['discount'])}  VAT {money(model['vat'])}  "
              f"Net {money(model['net'])}  ({model['words']})")
    if args.check:
        failed = False
        for name, status, detail in run_checks(model, args.out):
            print(f"{status:7s} {name}: {detail}")
            failed |= status == "FAIL"
        print("NOT RUN (manual) Render pages to PNG and look: header, footer, nothing clipped")
        print("NOT RUN (manual) Title, scope and exclusions agree; revision suffix matches scope change")
        return 4 if failed else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
