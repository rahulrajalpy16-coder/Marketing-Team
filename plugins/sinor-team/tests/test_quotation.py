"""Tests for scripts/build_quotation.py. All data is fictional."""
import copy
import json
import re
import shutil
import subprocess
from decimal import Decimal
from pathlib import Path

import pytest

import build_quotation as bq

FIXTURE = Path(__file__).parent / "fixtures" / "quotation_example.json"
SCRIPT = Path(bq.__file__)


def spec(**over):
    s = {"client": {"name": "EXAMPLE CLIENT LTD"}, "subject": "TEST - TEST VESSEL",
         "items": [{"title": "Item A", "qty": 1, "unit": "Set", "price": "100.00"}]}
    s.update(over)
    return s


def pdf_text(path):
    pypdf = pytest.importorskip("pypdf")
    rd = pypdf.PdfReader(str(path))
    return [p.extract_text() or "" for p in rd.pages]


# ------------------------------------------------------------------ words
WORD_CASES = [
    ("0", "USD ZERO ONLY"),
    ("1", "USD ONE ONLY"),
    ("15", "USD FIFTEEN ONLY"),
    ("20", "USD TWENTY ONLY"),
    ("21", "USD TWENTY ONE ONLY"),
    ("90", "USD NINETY ONLY"),
    ("99", "USD NINETY NINE ONLY"),
    ("100", "USD ONE HUNDRED ONLY"),
    ("101", "USD ONE HUNDRED ONE ONLY"),
    ("110", "USD ONE HUNDRED TEN ONLY"),
    ("999", "USD NINE HUNDRED NINETY NINE ONLY"),
    ("1000", "USD ONE THOUSAND ONLY"),
    ("1001", "USD ONE THOUSAND ONE ONLY"),
    ("1234.56", "USD ONE THOUSAND TWO HUNDRED THIRTY FOUR AND CENT FIFTY SIX ONLY"),
    ("1687.50", "USD ONE THOUSAND SIX HUNDRED EIGHTY SEVEN AND CENT FIFTY ONLY"),
    ("21770.00", "USD TWENTY ONE THOUSAND SEVEN HUNDRED SEVENTY ONLY"),
    ("28383.75", "USD TWENTY EIGHT THOUSAND THREE HUNDRED EIGHTY THREE AND CENT SEVENTY FIVE ONLY"),
    ("191100.00", "USD ONE HUNDRED NINETY ONE THOUSAND ONE HUNDRED ONLY"),
    ("195000", "USD ONE HUNDRED NINETY FIVE THOUSAND ONLY"),
    ("283000.00", "USD TWO HUNDRED EIGHTY THREE THOUSAND ONLY"),
    ("1000000", "USD ONE MILLION ONLY"),
    ("1000001.01", "USD ONE MILLION ONE AND CENT ONE ONLY"),
    ("12345678.90", "USD TWELVE MILLION THREE HUNDRED FORTY FIVE THOUSAND SIX HUNDRED SEVENTY EIGHT AND CENT NINETY ONLY"),
    ("0.05", "USD ZERO AND CENT FIVE ONLY"),
    ("0.99", "USD ZERO AND CENT NINETY NINE ONLY"),
    ("19.995", "USD TWENTY ONLY"),  # rounds half-up to 20.00 first
]


@pytest.mark.parametrize("value,expected", WORD_CASES)
def test_amount_in_words(value, expected):
    assert bq.amount_in_words(Decimal(value)) == expected


def test_words_style_has_no_hyphen_and_correct_spelling():
    for value, text in WORD_CASES:
        assert "-" not in text
        assert "NINENTY" not in text
        assert " AND " not in text.replace(" AND CENT ", " ")


def test_words_other_currency():
    assert bq.amount_in_words(Decimal("5"), "AED") == "AED FIVE ONLY"


# ------------------------------------------------------------------ arithmetic
def test_amount_rounds_half_up():
    m = bq.normalise(spec(items=[{"title": "x", "qty": "3", "unit": "Nos", "price": "0.335"}]))
    # price normalised to 0.34 first, then 3 x 0.34 = 1.02
    assert m["sections"][0]["items"][0]["price"] == Decimal("0.34")
    assert m["total"] == Decimal("1.02")


def test_additive_defaults_zero_discount_zero_vat():
    m = bq.normalise(spec())
    assert (m["total"], m["discount"], m["vat"], m["net"]) == (Decimal("100.00"),) + (Decimal("0.00"),) * 1 + (Decimal("0.00"), Decimal("100.00"))
    assert m["vat_label"] == "VAT :" and m["disc_label"] == "Discount :"
    assert m["words"] == "USD ONE HUNDRED ONLY"


def test_discount_absolute_and_percent():
    items = [{"title": "x", "qty": 2, "unit": "Nos", "price": "1000.00"}]
    a = bq.normalise(spec(items=items, discount={"amount": "250.555"}))
    assert a["discount"] == Decimal("250.56") and a["net"] == Decimal("1749.44")
    p = bq.normalise(spec(items=items, discount={"percent": 13}))
    assert p["discount"] == Decimal("260.00") and p["net"] == Decimal("1740.00")
    assert p["disc_label"] == "Discount 13% :"
    p2 = bq.normalise(spec(items=items, discount={"percent": "2.5"}))
    assert p2["disc_label"] == "Discount 2.5% :" and p2["discount"] == Decimal("50.00")


def test_vat_applies_to_total_minus_discount():
    items = [{"title": "x", "qty": 1, "unit": "Lsum", "price": "1000.00"}]
    m = bq.normalise(spec(items=items, discount={"percent": 10}, vat_percent=5))
    # discount 100.00, VAT on 900.00 = 45.00, net = 1000 - 100 + 45
    assert (m["discount"], m["vat"], m["net"]) == (Decimal("100.00"), Decimal("45.00"), Decimal("945.00"))
    assert m["vat_label"] == "VAT 5% :"
    assert m["words"] == "USD NINE HUNDRED FORTY FIVE ONLY"


def test_vat_zero_and_vat_label_override():
    m = bq.normalise(spec(vat_percent=0, vat_label="VAT 5%"))
    assert m["vat"] == Decimal("0.00") and m["vat_label"] == "VAT 5% :"


def test_vat_rounding_half_up():
    m = bq.normalise(spec(items=[{"title": "x", "qty": 1, "unit": "Nos", "price": "0.10"}], vat_percent=5))
    assert m["vat"] == Decimal("0.01")  # 0.005 -> 0.01


def test_sections_and_subtotals():
    s = spec()
    del s["items"]
    s["sections"] = [
        {"name": "VMS", "items": [{"title": "a", "qty": 1, "unit": "Set", "price": "10.50"},
                                  {"title": "b", "qty": 2, "unit": "Nos", "price": "4.25"}]},
        {"name": "DP", "items": [{"title": "c", "qty": 1, "unit": "Lsum", "price": "100"}]},
    ]
    m = bq.normalise(s)
    nos = [it["no"] for sec in m["sections"] for it in sec["items"]]
    assert nos == ["1.1", "1.2", "2.1"]
    assert m["total"] == Decimal("119.00")


def test_alternatives_mode_has_no_totals():
    m = bq.normalise(spec(mode="alternatives", discount={"percent": 5}, vat_percent=5))
    assert m["words"] is None and m["discount"] == 0 and m["vat"] == 0
    assert any("ignored" in w for w in m["warnings"])


def test_discount_larger_than_total_rejected():
    with pytest.raises(bq.SpecError):
        bq.normalise(spec(discount={"amount": "1000"}))


# ------------------------------------------------------------------ defaults, notes, terms
def test_defaults_and_warnings():
    m = bq.normalise(spec(), today=bq.datetime.date(2026, 11, 13))
    assert m["qtn"] == "SMS-QT2026-XXXXX"
    assert m["date"] == "13/11/2026" and m["currency"] == "USD" and m["your_ref"] == "Email"
    assert m["terms"]["payment"] == ["100% Advance"] and m["terms"]["validity"] == ["10 Days"]
    assert m["terms"]["warranty"] == ["Standard OEM Warranty"]
    assert any("qtn_no" in w for w in m["warnings"])
    assert any("delivery_period" in w for w in m["warnings"])


def test_revision_suffix_kept_verbatim():
    m = bq.normalise(spec(quote={"qtn_no": "SMS-QT2026-01234-R2"}))
    assert m["qtn"] == "SMS-QT2026-01234-R2"
    m = bq.normalise(spec(quote={"qtn_no": "SMS-QT2026-01234-D1"}))
    assert m["qtn"] == "SMS-QT2026-01234-D1"


def test_note_sets_verbatim_and_editing():
    assert bq.normalise(spec(notes="supply_only"))["notes"] == bq.NOTE_SETS["supply_only"]
    assert len(bq.NOTE_SETS["standard"]) == 10 and len(bq.NOTE_SETS["installation_newer"]) == 9
    m = bq.normalise(spec(notes={"set": "standard", "drop": [6, 10], "add": ["Extra note."]}))
    assert len(m["notes"]) == 9 and m["notes"][-1] == "Extra note."
    assert bq.normalise(spec(notes=["One", "Two"]))["notes"] == ["One", "Two"]
    default = bq.normalise(spec())["notes"]
    assert len(default) == 8 and bq.NOTE_SETS["standard"][5] not in default


def test_terms_override_and_numbered_exclusions():
    m = bq.normalise(spec(terms={"payment": "50% Advance", "exclusions": "NA", "delivery_period": "4-6 weeks"}))
    assert m["terms"]["payment"] == ["50% Advance"] and m["terms"]["exclusions"] == ["NA"]
    assert not any("delivery_period" in w for w in m["warnings"])


# ------------------------------------------------------------------ validation
@pytest.mark.parametrize("mutate,needle", [
    (lambda s: s.pop("client"), "client.name"),
    (lambda s: s["client"].update(name="  "), "client.name"),
    (lambda s: s.pop("items"), "at least one item"),
    (lambda s: s.update(items=[]), "at least one item"),
    (lambda s: s["items"][0].update(qty="abc"), "qty"),
    (lambda s: s["items"][0].update(price="12x"), "price"),
    (lambda s: s["items"][0].update(price=None), "price"),
    (lambda s: s["items"][0].update(qty=0), "qty"),
    (lambda s: s["items"][0].update(price=-1), "negative"),
    (lambda s: s["items"][0].update(price="NaN"), "finite"),
    (lambda s: s["items"][0].update(unit=""), "unit"),
    (lambda s: s.update(mode="weird"), "mode"),
    (lambda s: s.update(quote={"date": "2026-11-13"}), "DD/MM/YYYY"),
    (lambda s: s.update(vat_percent="x"), "vat_percent"),
    (lambda s: s.update(discount={"amount": 1, "percent": 1}), "exactly one"),
    (lambda s: s.update(notes="nope"), "unknown set"),
    (lambda s: s.update(terms={"bogus": "x"}), "unknown terms"),
    (lambda s: s.update(sections=[{"name": "x", "items": [{"title": "t", "qty": 1, "unit": "u", "price": 1}]}]), "not both"),
])
def test_validation_errors(mutate, needle):
    s = spec()
    mutate(s)
    with pytest.raises(bq.SpecError) as e:
        bq.normalise(s)
    assert needle in str(e.value)


def test_cli_invalid_spec_exits_nonzero(tmp_path, capsys):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"client": {}, "items": []}))
    rc = bq.main([str(p), "--out", str(tmp_path / "x.pdf")])
    err = capsys.readouterr().err
    assert rc == 2 and "client.name" in err and "at least one item" in err
    assert not (tmp_path / "x.pdf").exists()
    p.write_text("{not json")
    assert bq.main([str(p), "--out", str(tmp_path / "x.pdf")]) == 2


def test_cli_missing_spec_file(tmp_path):
    assert bq.main([str(tmp_path / "nope.json"), "--out", str(tmp_path / "x.pdf")]) == 2


# ------------------------------------------------------------------ rendering
def test_missing_qtn_warning_and_placeholder_in_pdf(tmp_path, capsys):
    p = tmp_path / "s.json"
    p.write_text(json.dumps(spec()))
    out = tmp_path / "o.pdf"
    assert bq.main([str(p), "--out", str(out)]) == 0
    assert "SMS-QT" in capsys.readouterr().err
    assert "SMS-QT%d-XXXXX" % bq.datetime.date.today().year in "\n".join(pdf_text(out))


def test_logo_fallback_text_header_and_warning(tmp_path, capsys):
    p = tmp_path / "s.json"
    p.write_text(json.dumps(spec(quote={"qtn_no": "SMS-QT2026-XXXXX"})))
    out = tmp_path / "o.pdf"
    assert bq.main([str(p), "--out", str(out), "--logo", str(tmp_path / "missing.png")]) == 0
    assert "logo not found" in capsys.readouterr().err
    text = "\n".join(pdf_text(out))
    assert "SINOR MARINE SERVICES" in text and "MIDDLE EAST FZCO" in text and "QUOTATION" in text


def test_default_logo_resolved_relative_to_script():
    assert Path(bq.DEFAULT_LOGO) == SCRIPT.resolve().parent.parent / "assets" / "brand" / "sinor-logo.png"
    assert Path(bq.DEFAULT_LOGO).is_file()
    assert "/home/" not in SCRIPT.read_text()


def test_end_to_end_fixture(tmp_path, capsys):
    out = tmp_path / "ex.pdf"
    rc = bq.main([str(FIXTURE), "--out", str(out), "--check"])
    stdout = capsys.readouterr().out
    assert rc == 0, stdout
    assert out.read_bytes()[:5] == b"%PDF-"
    pages = pdf_text(out)
    n = len(pages)
    assert n >= 1
    full = "\n".join(pages)
    assert "QUOTATION" in full and "EXAMPLE CLIENT LTD" in full and "104218013100003" in full
    for i, pg in enumerate(pages, 1):
        assert "Page %d of %d" % (i, n) in pg
        assert "sales@sinormarine.com" in pg and "www.sinormarine.com" in pg
        assert "* This is a computer generated document and doesn't need any signature. *" in pg
    assert "Page 1 of %d" % n in pages[0]
    # independent calculation
    total = Decimal("283000.00") + Decimal("2") * Decimal("843.75")
    disc = (total * 13 / 100).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")
    vat = ((total - disc) * 5 / 100).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")
    net = total - disc + vat
    flat = re.sub(r"\s+", " ", full)
    for label, v in (("Total :", total), ("Discount 13% :", disc), ("VAT 5% :", vat), ("Net Amount :", net)):
        assert "%s %s" % (label, f"{v:,.2f}") in flat, label
    assert "USD TWO HUNDRED SIXTY THOUSAND SIXTY TWO AND CENT THREE ONLY" in flat
    assert "PASS    Totals and Amount in Words" in stdout
    assert "FAIL" not in stdout


@pytest.mark.skipif(shutil.which("pdftotext") is None, reason="pdftotext not installed")
def test_end_to_end_pdftotext(tmp_path):
    out = tmp_path / "ex.pdf"
    assert bq.main([str(FIXTURE), "--out", str(out)]) == 0
    txt = subprocess.run(["pdftotext", "-layout", str(out), "-"], capture_output=True, text=True).stdout
    assert "sales@sinormarine.com" in txt and re.search(r"Page 1 of \d+", txt)
    assert "Net Amount :" in txt and "260,062.03" in txt


def test_alternatives_pdf_blank_totals(tmp_path):
    s = spec(mode="alternatives", items=[
        {"title": "Option 1:-", "text": ["System A"], "qty": 1, "unit": "Set", "price": "100"},
        {"title": "Option 2:-", "text": ["System B"], "qty": 1, "unit": "Set", "price": "200"}])
    p = tmp_path / "s.json"
    p.write_text(json.dumps(s))
    out = tmp_path / "o.pdf"
    assert bq.main([str(p), "--out", str(out), "--check"]) == 0
    text = "\n".join(pdf_text(out))
    assert "Net Amount" not in text and "Amount in Words" not in text


def test_sections_pdf_shows_subtotals(tmp_path):
    s = spec()
    del s["items"]
    s["sections"] = [
        {"name": "VMS", "items": [{"title": "a", "qty": 1, "unit": "Set", "price": "10.50"}]},
        {"name": "DP", "items": [{"title": "c", "qty": 3, "unit": "Nos", "price": "100"}]}]
    p = tmp_path / "s.json"
    p.write_text(json.dumps(s))
    out = tmp_path / "o.pdf"
    assert bq.main([str(p), "--out", str(out), "--check"]) == 0
    flat = re.sub(r"\s+", " ", "\n".join(pdf_text(out)))
    assert "Sub-total Section 1 (VMS) : 10.50" in flat
    assert "Sub-total Section 2 (DP) : 300.00" in flat
    assert "Total : 310.50" in flat


def test_25_items_multi_page(tmp_path, capsys):
    items = [{"title": "Item %d with a rather long title that is expected to wrap across the description column "
                       "of the items table to prove wrapping" % i,
              "include": ["Component line %d.%d" % (i, k) for k in range(1, 4)],
              "scope": ["Step %d" % k for k in range(1, 3)],
              "qty": i, "unit": "Nos", "price": "%d.10" % (i * 7)} for i in range(1, 26)]
    s = spec(items=items, discount={"percent": 5}, vat_percent=5,
             terms={"delivery_period": "Item 1 : 4 weeks; Items 2 & 25 : 8 weeks"})
    p = tmp_path / "s.json"
    p.write_text(json.dumps(s))
    out = tmp_path / "many.pdf"
    assert bq.main([str(p), "--out", str(out), "--check"]) == 0
    stdout = capsys.readouterr().out
    assert "FAIL" not in stdout and "PASS    Item arithmetic" in stdout
    pages = pdf_text(out)
    assert len(pages) >= 3
    for i, pg in enumerate(pages, 1):
        assert "Page %d of %d" % (i, len(pages)) in pg
    # header row repeats on continuation pages
    assert sum("Description" in pg for pg in pages) >= 2
    assert "Item 25" in "\n".join(pages)


def test_check_flags_missing_item_reference(tmp_path, capsys):
    s = spec(terms={"delivery_period": "Item 7 : 4 weeks"})
    p = tmp_path / "s.json"
    p.write_text(json.dumps(s))
    rc = bq.main([str(p), "--out", str(tmp_path / "o.pdf"), "--check"])
    assert rc == 4 and "FAIL    Delivery lines reference existing item numbers" in capsys.readouterr().out


def test_check_flags_address_artefact(tmp_path, capsys):
    s = spec()
    s["client"]["address"] = ". Some Road"
    p = tmp_path / "s.json"
    p.write_text(json.dumps(s))
    rc = bq.main([str(p), "--out", str(tmp_path / "o.pdf"), "--check"])
    assert rc == 4 and "FAIL    No leading '. ' in client address" in capsys.readouterr().out


def test_signatory_options(tmp_path):
    for sig, present in (("default", True), (False, False), ({"name": "Test Person", "phone": "+000"}, True)):
        out = tmp_path / "o.pdf"
        p = tmp_path / "s.json"
        p.write_text(json.dumps(spec(signatory=sig)))
        assert bq.main([str(p), "--out", str(out)]) == 0
        text = "\n".join(pdf_text(out))
        assert "For SINOR MARINE SERVICES MIDDLE EAST FZCO" in text
        name = "Test Person" if isinstance(sig, dict) else "Naveen Thandarath"
        assert (name in text) == present


def test_special_characters_escaped(tmp_path):
    s = spec(subject="A & B <test> - TEST VESSEL")
    s["items"][0]["title"] = "Fish & Chips <b>raw</b>"
    p = tmp_path / "s.json"
    p.write_text(json.dumps(s))
    out = tmp_path / "o.pdf"
    assert bq.main([str(p), "--out", str(out)]) == 0
    text = "\n".join(pdf_text(out))
    assert "A & B <test>" in text and "Fish & Chips <b>raw</b>" in text


def test_no_em_dashes_in_generated_text():
    src = SCRIPT.read_text()
    assert chr(0x2014) not in src
