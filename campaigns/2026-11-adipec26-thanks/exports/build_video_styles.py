#!/usr/bin/env python3
"""ADIPEC 2026 thank-you video, two more designs (v12 'kinetic' and v13 'promo') for LinkedIn.

Same content as the mosaic version (build_video_mosaic.py): same photos, same order, same captions, same partner
end card. Only the visual treatment differs. Both are original drawings inspired by STYLE references Rahul supplied
(Pinterest pins of After Effects template previews); no template assets are used.

  kinetic : inspired by a 'dynamic and colorful' template. Flat colour-block backgrounds, giant geometric words that
            build letter by letter, white-bordered photo cards with soft shadow and slight tilt, colour wipes.
  promo   : inspired by a 'corporate event promo' template. Dark duotone photo wall behind the content, framed hero
            photo, big white type, aqua chips and an outlined info box, fast slides with motion blur.

Usage: python3 build_video_styles.py <jpg_dir> <extra_dir> <out_dir> <version> <kinetic|promo> [4x5|9x16]
Needs Pillow, numpy, ffmpeg (libx264/aac), Inter fonts. No music: a silent AAC track is added.
All motion is drawn per frame with sub-pixel sampling and piped to ffmpeg.
"""
import math
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

STYLE = sys.argv[5] if len(sys.argv) > 5 else "kinetic"
ASPECT = sys.argv[6] if len(sys.argv) > 6 else "4x5"
W, H = (1080, 1350) if ASPECT == "4x5" else (1080, 1920)
SAFE = H - (150 if ASPECT == "4x5" else 300)
FPS = 25
NAVY, BLUE, LIGHT, WHITE = (10, 42, 74), (13, 74, 133), (196, 218, 240), (255, 255, 255)
CREAM, SKY, AQUA = (245, 239, 227), (207, 227, 245), (53, 214, 197)
FONT_DIR = "/usr/share/fonts/opentype/inter/"
REPO = Path(__file__).resolve().parents[3]
LOGO = REPO / "assets/brand/sinor-logo.png"
PARTNER_DIR = REPO / "assets/brand/partners"

EVENT_LINE = "ADIPEC 2026  ·  ABU DHABI"
DATE_LINE = "2-5 November 2026"
PARTNERS = [("Sonardyne", "sonardyne.png"), ("Fugro", "fugro.png"), ("Navis Engineering", "navis-engineering.png"),
            ("Marine Technologies", "marine-technologies-mt.png"), ("Guidance Marine", "guidance-marine.png")]

# Same beats as the mosaic design. word / chip are decorative labels per style.
BEATS = [
    dict(kind="hero", src="s8_2.jpg", cap="The Sinor Marine team at ADIPEC 2026", word="OUR TEAM", chip="TEAM", logo=True),
    dict(kind="title"),
    dict(kind="hero", src="s7_1.jpg", cap="Conversations at our stand", word="CONVERSATIONS", chip="VISITORS"),
    dict(kind="hero", src="s3_1.jpg", cap="Visitors at our stand", word="VISITORS", chip="VISITORS"),
    dict(kind="hero", src="IMG_4413.jpg", cap="NAVIS console", word="TECHNOLOGY", chip="TECHNOLOGY"),
    dict(kind="hero", src="IMG_4464.jpg", cap="Sonardyne SPRINT-Nav on the stand", word="DISCUSSIONS", chip="TECHNOLOGY"),
    dict(kind="hero", src="IMG_4188.jpg", cap="Marine Technologies on the stand", word="PARTNERS", chip="PARTNERS"),
    dict(kind="hero", src="a07555b5-23b3-4497-92aa-a3613e384bc5.jpg", cap="With Guidance Marine at our stand", word="WELCOME", chip="PARTNERS"),
    dict(kind="hero", src="s2_2.jpg", cap="Together at our stand", word="TEAMWORK", chip="TEAM"),
    dict(kind="end"),
]
HERO_D, TITLE_D, END_D = 2.95, 2.7, 6.0
T_HALF = 0.20  # half length of a transition around each boundary

PAL_K = [  # kinetic palettes (brand colours + cream)
    dict(bg=CREAM, text=NAVY, accent=BLUE, accent2=SKY),
    dict(bg=NAVY, text=CREAM, accent=(70, 150, 235), accent2=LIGHT),
    dict(bg=BLUE, text=WHITE, accent=CREAM, accent2=(120, 180, 240)),
    dict(bg=SKY, text=NAVY, accent=BLUE, accent2=WHITE),
]
# ----------------------------------------------------------------------------------------------------------


def font(weight, size):
    return ImageFont.truetype(f"{FONT_DIR}Inter-{weight}.otf", int(size))


def eo(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def eio(x):
    x = min(max(x, 0.0), 1.0)
    return 3 * x * x - 2 * x ** 3


def tw(text, f):
    return f.getlength(text)


def find(name, jpg, extra):
    for d in (jpg, extra):
        if (d / name).exists():
            return d / name
    raise FileNotFoundError(name)


def fit_size(text, weight, max_w, start=400):
    s = start
    while s > 20 and tw(text, font(weight, s)) > max_w:
        s -= 4
    return s


def logo_card(width, pad=18, radius=20):
    lg = Image.open(LOGO).convert("RGB")
    lg = lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)
    card = Image.new("RGBA", (lg.width + 2 * pad, lg.height + 2 * pad), (255, 255, 255, 255))
    card.paste(lg, (pad, pad))
    m = Image.new("L", card.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width, card.height], radius=radius, fill=255)
    card.putalpha(m)
    return card


def partner_tile(logo_file, w, h):
    lg = Image.open(PARTNER_DIR / logo_file).convert("RGBA")
    bb = lg.getchannel("A").getbbox()
    if bb:
        lg = lg.crop(bb)
    sc = min((w - 44) / lg.width, (h - 26) / lg.height)
    lg = lg.resize((max(1, round(lg.width * sc)), max(1, round(lg.height * sc))), Image.LANCZOS)
    t = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    t.alpha_composite(lg, ((w - lg.width) // 2, (h - lg.height) // 2))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w, h], radius=18, fill=255)
    t.putalpha(m)
    return t


def shadow_for(w, h, blur=22, alpha=110, off=(0, 14), pad=70):
    s = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(s).rectangle([pad + off[0], pad + off[1], pad + off[0] + w, pad + off[1] + h], fill=(8, 16, 36, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur)), pad


def zoom_xf_unused(img, z, out_size=None):
    w, h = img.size
    return img.transform(out_size or (w, h), Image.AFFINE, (1 / z, 0, w / 2 - w / (2 * z), 0, 1 / z, h / 2 - h / (2 * z)), resample=Image.BICUBIC)


def zoom_xf(img, z):
    w, h = img.size
    return img.transform((w, h), Image.AFFINE, (1 / z, 0, w / 2 - w / (2 * z), 0, 1 / z, h / 2 - h / (2 * z)), resample=Image.BICUBIC)


def duotone(im, gain=1.0, dark=(5, 16, 40), mid=(24, 76, 168), light=(150, 196, 240)):
    g = np.asarray(im.convert("L"), np.float32) / 255.0
    g = np.clip((g - 0.5) * 1.2 + 0.5, 0, 1) * gain
    g = np.clip(g, 0, 1)[..., None]
    d, m, l = (np.array(c, np.float32) for c in (dark, mid, light))
    lo = d + (m - d) * (g * 2).clip(0, 1)
    hi = m + (l - m) * ((g - 0.5) * 2).clip(0, 1)
    return Image.fromarray(np.where(g < 0.5, lo, hi).astype(np.uint8), "RGB")


def hero_rect(im, max_w, max_h):
    a = im.width / im.height
    if a >= max_w / max_h:
        return int(max_w), int(max_w / a)
    return int(max_h * a), int(max_h)


def wrap(text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    lines.append(cur)
    return lines


# =========================================================================================================
#  KINETIC style
# =========================================================================================================
class KBeat:
    def __init__(self, idx, spec, start, dur, jpg, extra):
        self.i, self.spec, self.start, self.dur, self.kind = idx, spec, start, dur, spec["kind"]
        self.pal = PAL_K[idx % len(PAL_K)]
        if self.kind == "end":
            self.pal = PAL_K[0]
        self.side = 1 if idx % 2 == 0 else -1
        if self.kind == "hero":
            im = Image.open(find(spec["src"], jpg, extra)).convert("RGB")
            hw, hh = hero_rect(im, 0.84 * W, 0.50 * H)
            b = 14
            card = Image.new("RGB", (hw + 2 * b, hh + 2 * b), (255, 255, 255))
            card.paste(im.resize((hw, hh), Image.LANCZOS), (b, b))
            self.card = card.convert("RGBA")
            self.cw, self.ch = self.card.size
            self.shadow, self.spad = shadow_for(self.cw, self.ch, blur=24, alpha=120, off=(0, 18))
            self.tilt = self.side * (-2.2)
            self.cx, self.cy = W / 2 + self.side * 20, 0.50 * H
        self.word = spec.get("word")

    def word_layer(self, t, text, wmax, color, y, lines=1, accent=None, accent_idx=None):
        """Giant word built letter by letter (ExtraBold). Returns RGBA layer the size of the canvas."""
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        parts = text.split("|")
        size = min(fit_size(p, "ExtraBold", wmax) for p in parts)
        f = font("ExtraBold", size)
        d = ImageDraw.Draw(layer)
        yy = y
        ci = 0
        for p in parts:
            x0 = (W - tw(p, f)) / 2
            for k, ch in enumerate(p):
                xk = x0 + f.getlength(p[:k])
                delay = 0.03 * ci
                e = eo((t - delay) / 0.38)
                ci += 1
                if e <= 0:
                    continue
                col = accent if (accent is not None and accent_idx == ci - 1) else color
                d.text((xk, yy + (1 - e) * size * 0.45), ch, font=f, fill=col + (int(255 * min(1, e * 1.6)),))
            yy += size * 1.02
        return layer

    def draw(self, t):
        pal = self.pal
        img = Image.new("RGB", (W, H), pal["bg"])
        d = ImageDraw.Draw(img)
        if self.kind == "hero":
            # layered colour block behind the card
            bx = self.cx - self.cw / 2 - self.side * 44
            by = self.cy - self.ch / 2 + 44
            e_blk = eo(t / 0.5)
            d.rectangle([bx + (1 - e_blk) * self.side * -120, by, bx + self.cw + (1 - e_blk) * self.side * -120, by + self.ch], fill=pal["accent2"] if self.i % 2 else pal["accent"])
            # giant word at top (behind the card)
            wl = self.word_layer(t, self.word, W - 110, pal["text"], 0.06 * H)
            img.paste(wl, (0, 0), wl)
            # card (tilt + slow zoom, sub-pixel)
            e_c = eo((t - 0.08) / 0.5)
            z = 0.90 + 0.10 * e_c + 0.05 * min(1, t / self.dur)
            ang = self.tilt * (1 - 0.5 * min(1, t / self.dur))
            card = self.card
            big = Image.new("RGBA", (int(self.cw * 1.25), int(self.ch * 1.25)), (0, 0, 0, 0))
            big.paste(card, ((big.width - self.cw) // 2, (big.height - self.ch) // 2))
            a = math.radians(ang)
            ca, sa = math.cos(a) / z, math.sin(a) / z
            cx0, cy0 = big.width / 2, big.height / 2
            xf = big.transform(big.size, Image.AFFINE, (ca, sa, cx0 - ca * cx0 - sa * cy0, -sa, ca, cy0 + sa * cx0 - ca * cy0), resample=Image.BICUBIC)
            if e_c < 1:
                xf.putalpha(xf.getchannel("A").point(lambda v: int(v * min(1, e_c * 1.5))))
            sh = self.shadow.copy()
            sh.putalpha(sh.getchannel("A").point(lambda v: int(v * min(1, e_c * 1.5))))
            img.paste(sh, (int(self.cx - self.cw / 2 - self.spad), int(self.cy - self.ch / 2 - self.spad)), sh)
            img.paste(xf, (int(self.cx - big.width / 2), int(self.cy - big.height / 2)), xf)
            # caption under the card
            cap_y = self.cy + self.ch / 2 + 46
            e_t = eo((t - 0.30) / 0.45)
            bar_w = 96 * e_t
            d.rectangle([70, cap_y, 70 + bar_w, cap_y + 9], fill=pal["accent"] if pal["bg"] != BLUE else CREAM)
            f1 = font("ExtraBold", 50)
            lines = wrap(self.spec["cap"], f1, W - 140)
            for k, ln in enumerate(lines[:2]):
                ly = cap_y + 26 + k * 60 + (1 - e_t) * 24
                col = pal["text"] + (int(255 * e_t),)
                lay = Image.new("RGBA", (W, 80), (0, 0, 0, 0))
                ImageDraw.Draw(lay).text((70, 0), ln, font=f1, fill=col)
                img.paste(lay, (0, int(ly)), lay)
            if self.spec.get("logo"):
                card_l = logo_card(210, 14, 16)
                img.paste(card_l, (W - 70 - card_l.width, int(0.06 * H) + 4), card_l) if False else None
        elif self.kind == "title":
            wl = self.word_layer(t, "THANK|YOU.", W - 110, pal["text"], 0.20 * H, accent=pal["accent"], accent_idx=7)
            img.paste(wl, (0, 0), wl)
            e = eo((t - 0.55) / 0.5)
            lc = logo_card(300, 18, 20)
            img.paste(lc, ((W - lc.width) // 2, int(0.07 * H)), lc)
            f2, f3 = font("SemiBold", 46), font("Medium", 40)
            ly = int(0.66 * H)
            lay = Image.new("RGBA", (W, 160), (0, 0, 0, 0))
            dd = ImageDraw.Draw(lay)
            dd.text((W / 2, 0), EVENT_LINE, font=f2, fill=pal["text"] + (int(255 * e),), anchor="mt")
            dd.text((W / 2, 62), DATE_LINE, font=f3, fill=pal["accent2"] + (int(255 * e),), anchor="mt")
            img.paste(lay, (0, int(ly + (1 - e) * 26)), lay)
        else:
            self.draw_end(img, t)
        return img

    def draw_end(self, img, t):
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, W, int(H * 0.0)], fill=BLUE)
        tw_, th_, gx, pitch = 470, 124, 20, 184
        rows = (len(PARTNERS) + 1) // 2
        block = 560 + (rows - 1) * pitch + th_ + 42
        o = (SAFE - block) // 2 - 6
        e = eo(t / 0.55)
        lc = logo_card(420, 18, 22)
        sh, sp = shadow_for(lc.width, lc.height, 14, 70, (0, 8), 40)
        img.paste(sh, ((W - lc.width) // 2 - sp, 60 + o - sp), sh)
        img.paste(lc, ((W - lc.width) // 2, 60 + o), lc)
        f = font("ExtraBold", 118)
        d.text((W // 2, 280 + o), "Thank you", font=f, fill=NAVY, anchor="mt")
        d.rectangle([W // 2 - 48, 424 + o, W // 2 + 48, 433 + o], fill=BLUE)
        d.text((W // 2, 456 + o), "To every client and visitor who stopped by our stand.", font=font("SemiBold", 36), fill=NAVY, anchor="mt")
        d.text((W // 2, 520 + o), "And to our technology partners for their support:", font=font("Medium", 35), fill=BLUE, anchor="mt")
        y0 = 590 + o
        for k, (name, logo) in enumerate(PARTNERS):
            r, c = divmod(k, 2)
            alone = (k == len(PARTNERS) - 1) and (len(PARTNERS) % 2 == 1)
            x = (W - tw_) // 2 if alone else (W - (2 * tw_ + gx)) // 2 + c * (tw_ + gx)
            y = y0 + r * pitch
            tile = partner_tile(logo, tw_, th_)
            sh, sp = shadow_for(tw_, th_, 12, 80, (0, 8), 40)
            img.paste(sh, (x - sp, y - sp), sh)
            img.paste(tile, (x, y), tile)
            d.text((x + tw_ // 2, y + th_ + 8), name, font=font("SemiBold", 32), fill=NAVY, anchor="mt")


# =========================================================================================================
#  PROMO style
# =========================================================================================================
class PBeat:
    wall = None

    def __init__(self, idx, spec, start, dur, jpg, extra):
        self.i, self.spec, self.start, self.dur, self.kind = idx, spec, start, dur, spec["kind"]
        if self.kind == "hero":
            im = Image.open(find(spec["src"], jpg, extra)).convert("RGB")
            self.hw, self.hh = hero_rect(im, 0.86 * W, 0.40 * H)
            self.src = im.resize((self.hw, self.hh), Image.LANCZOS)
            self.hx = (W - self.hw) // 2
            self.hy = int(0.112 * H) + (int(0.40 * H) - self.hh) // 2 if ASPECT == "4x5" else int(0.12 * H)
            self.shadow, self.spad = shadow_for(self.hw, self.hh, 26, 150, (0, 20), 80)

    def chip(self, text):
        f = font("Bold", 26)
        w = int(tw(text, f) + 44)
        c = Image.new("RGBA", (w, 48), AQUA + (255,))
        ImageDraw.Draw(c).text((22, 9), text, font=f, fill=NAVY + (255,))
        return c

    def draw(self, t, wall_off):
        img = PBeat.wall_frame(wall_off)
        d = ImageDraw.Draw(img, "RGBA")
        n_hero = sum(1 for b in BEATS if b["kind"] == "hero")
        if self.kind == "hero":
            e = eo(t / 0.45)
            z = 1.0 + 0.05 * min(1, t / self.dur)
            hero = zoom_xf(self.src, z).convert("RGBA")
            hero.putalpha(int(255 * min(1, e * 1.5)))
            sh = self.shadow.copy()
            img.paste(sh, (self.hx - self.spad, self.hy - self.spad), sh)
            d.rectangle([self.hx - 12, self.hy - 12, self.hx + self.hw + 12, self.hy + self.hh + 12], outline=(255, 255, 255, 235), width=3)
            img.paste(hero, (self.hx, self.hy), hero)
            ec = eo((t - 0.12) / 0.4)
            chip = self.chip(self.spec["chip"])
            chip.putalpha(chip.getchannel("A").point(lambda v: int(v * ec)))
            img.paste(chip, (self.hx - 12 - int((1 - ec) * 60), self.hy + self.hh - 12), chip)
            idx = [k for k, b in enumerate([bb for bb in BEATS if bb["kind"] == "hero"]) if b is self.spec][0] + 1
            d.text((self.hx + self.hw + 12, self.hy - 44), f"{idx:02d} / {n_hero:02d}", font=font("Bold", 24), fill=AQUA + (255,), anchor="ra")
            # big caption + outlined info box
            ct = eo((t - 0.25) / 0.5)
            f1 = font("ExtraBold", 58)
            lines = wrap(self.spec["cap"], f1, int(0.86 * W) + 24)
            y = self.hy + self.hh + 78
            lay = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            for k, ln in enumerate(lines[:2]):
                ld.text((self.hx - 12, k * 68), ln, font=f1, fill=WHITE + (int(255 * ct),))
            img.paste(lay, (0, int(y + (1 - ct) * 30)), lay)
            by = int(y + len(lines[:2]) * 68 + 26 + (1 - ct) * 30)
            box = Image.new("RGBA", (int(0.52 * W), 112), (0, 0, 0, 0))
            bd = ImageDraw.Draw(box)
            bd.rectangle([0, 0, box.width - 2, box.height - 2], outline=AQUA + (int(255 * ct),), width=2)
            bd.text((20, 14), "ADIPEC 2026", font=font("Bold", 26), fill=WHITE + (int(255 * ct),))
            bd.text((20, 52), "ABU DHABI  ·  2-5 NOV 2026", font=font("Medium", 24), fill=LIGHT + (int(255 * ct),))
            img.paste(box, (self.hx - 12, by), box)
            if self.spec.get("logo"):
                lc = logo_card(220, 14, 16)
                img.paste(lc, (self.hx - 12, 28), lc)
        elif self.kind == "title":
            e = eo(t / 0.5)
            lc = logo_card(300, 18, 20)
            img.paste(lc, ((W - lc.width) // 2, int(0.07 * H)), lc)
            f = font("ExtraBold", 230)
            lay = Image.new("RGBA", (W, 520), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            ld.text((W // 2, 0), "THANK", font=f, fill=WHITE + (int(255 * e),), anchor="mt")
            yw = tw("YOU", f)
            bx0 = (W - yw) / 2 - 30
            bw = (1 - 0) * (yw + 60) * eo((t - 0.15) / 0.45)
            ld.rectangle([bx0, 258, bx0 + bw, 258 + 250], fill=AQUA + (255,))
            if bw > 20:
                ld.text((W // 2, 252), "YOU", font=f, fill=NAVY + (255,), anchor="mt")
            img.paste(lay, (0, int(0.27 * H + (1 - e) * 40)), lay)
            ef = eo((t - 0.6) / 0.5)
            lay2 = Image.new("RGBA", (W, 130), (0, 0, 0, 0))
            l2 = ImageDraw.Draw(lay2)
            l2.text((W / 2, 0), EVENT_LINE, font=font("SemiBold", 46), fill=WHITE + (int(255 * ef),), anchor="mt")
            l2.text((W / 2, 62), DATE_LINE, font=font("Medium", 40), fill=AQUA + (int(255 * ef),), anchor="mt")
            img.paste(lay2, (0, int(0.69 * H + (1 - ef) * 24)), lay2)
        else:
            self.draw_end(img, t)
        return img.convert("RGB")

    def draw_end(self, img, t):
        ov = Image.new("RGBA", (W, H), NAVY + (170,))
        img.alpha_composite(ov) if img.mode == "RGBA" else img.paste(ov, (0, 0), ov)
        d = ImageDraw.Draw(img, "RGBA")
        tw_, th_, gx, pitch = 470, 124, 20, 184
        rows = (len(PARTNERS) + 1) // 2
        block = 600 + (rows - 1) * pitch + th_ + 42
        o = (SAFE - block) // 2 - 6
        lc = logo_card(420, 18, 22)
        img.paste(lc, ((W - lc.width) // 2, 60 + o), lc)
        d.text((W // 2, 290 + o), "Thank you", font=font("ExtraBold", 118), fill=WHITE + (255,), anchor="mt")
        d.rectangle([W // 2 - 56, 432 + o, W // 2 + 56, 441 + o], fill=AQUA + (255,))
        d.text((W // 2, 462 + o), "To every client and visitor who stopped by our stand.", font=font("SemiBold", 36), fill=WHITE + (255,), anchor="mt")
        d.text((W // 2, 530 + o), "And to our technology partners for their support:", font=font("Medium", 35), fill=AQUA + (255,), anchor="mt")
        y0 = 600 + o
        for k, (name, logo) in enumerate(PARTNERS):
            r, c = divmod(k, 2)
            alone = (k == len(PARTNERS) - 1) and (len(PARTNERS) % 2 == 1)
            x = (W - tw_) // 2 if alone else (W - (2 * tw_ + gx)) // 2 + c * (tw_ + gx)
            y = y0 + r * pitch
            tile = partner_tile(logo, tw_, th_)
            img.paste(tile, (x, y), tile)
            d.text((x + tw_ // 2, y + th_ + 8), name, font=font("SemiBold", 32), fill=WHITE + (255,), anchor="mt")

    @staticmethod
    def build_wall(pool):
        cols = 4
        s = W // cols
        rows = (H // s) + 3
        rows += rows % 2
        rng = random.Random(7)
        wall = Image.new("RGB", (W, rows * s))
        order = pool[:]
        rng.shuffle(order)
        for r in range(rows):
            for c in range(cols):
                im = Image.open(order[(r * cols + c) % len(order)]).convert("RGB")
                side = min(im.size)
                x0 = rng.randint(0, im.width - side)
                y0 = rng.randint(0, im.height - side)
                tile = im.crop((x0, y0, x0 + side, y0 + side)).resize((s, s), Image.LANCZOS)
                wall.paste(duotone(tile, rng.uniform(0.7, 1.05)), (c * s, r * s))
        a = np.asarray(wall).astype(np.float32)
        veil = np.array([8, 22, 56], np.float32)
        a = a * 0.62 + veil * 0.38
        PBeat.wall_img = Image.fromarray(a.astype(np.uint8), "RGB")
        PBeat.wall_h = rows * s
        # vignette
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r_ = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.5) / (H * 0.75)) ** 2)
        PBeat.vig = (1 - np.clip(r_ - 0.25, 0, 1) * 0.55)[..., None]

    @staticmethod
    def wall_frame(off):
        off = int(off) % PBeat.wall_h
        w = PBeat.wall_img
        if off + H <= PBeat.wall_h:
            crop = w.crop((0, off, W, off + H))
        else:
            crop = Image.new("RGB", (W, H))
            crop.paste(w.crop((0, off, W, PBeat.wall_h)), (0, 0))
            crop.paste(w.crop((0, 0, W, H - (PBeat.wall_h - off))), (0, PBeat.wall_h - off))
        a = np.asarray(crop).astype(np.float32) * PBeat.vig
        return Image.fromarray(a.astype(np.uint8), "RGB").convert("RGBA")


def directional_blur(img, px):
    if px < 2:
        return img
    a = np.asarray(img).astype(np.float32)
    acc = np.zeros_like(a)
    n = 5
    for k in range(n):
        acc += np.roll(a, int((k - (n - 1) / 2) * px / (n - 1)), axis=1)
    return Image.fromarray((acc / n).astype(np.uint8), "RGB")


# =========================================================================================================
def main():
    if len(sys.argv) < 6:
        print(__doc__)
        return 2
    jpg, extra, out, ver = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
    out.mkdir(parents=True, exist_ok=True)
    pool = sorted(list(jpg.glob("*.jpg")) + list(extra.glob("*.jpg")))
    Cls = KBeat if STYLE == "kinetic" else PBeat
    if STYLE == "promo":
        PBeat.build_wall(pool)
    beats, t0 = [], -0.6  # start 0.6 s into the first entry so frame 1 already shows content
    for i, spec in enumerate(BEATS):
        dur = {"hero": HERO_D, "title": TITLE_D, "end": END_D}[spec["kind"]]
        beats.append(Cls(i, spec, t0, dur, jpg, extra))
        t0 += dur
    total = t0
    n_frames = int(round(total * FPS))
    name = f"adipec26-thanks_linkedin_{STYLE}_{ASPECT}_v{ver}.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000", "-t", f"{total:.3f}",
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(out / name)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    bounds = [b.start for b in beats[1:]]
    cover_T = 1.6
    for fi in range(n_frames):
        T = fi / FPS
        wall_off = fi * 1  # 1 px per frame: uniform scroll, no judder
        bi = max(k for k, b in enumerate(beats) if b.start <= T)
        near = [bd for bd in bounds if abs(T - bd) < T_HALF]
        if STYLE == "kinetic":
            if near:
                bd = near[0]
                nxt = [k for k, b in enumerate(beats) if abs(b.start - bd) < 1e-6][0]
                scene_idx = nxt if T >= bd else nxt - 1
                bb = beats[scene_idx]
                frame = bb.draw(max(0.0, T - bb.start))
                p = (T - (bd - T_HALF)) / (2 * T_HALF)
                nb = beats[nxt]
                col = nb.pal["accent"]
                if p < 0.5:
                    x0, x1 = int(W * (1 - 2 * eio(p * 2) * 1.0)), W
                    x0 = int(W * (1 - eio(p * 2)))
                    x1 = W
                else:
                    x0, x1 = 0, int(W * (1 - eio((p - 0.5) * 2)))
                if x1 > x0:
                    ImageDraw.Draw(frame).rectangle([x0, 0, x1, H], fill=col)
            else:
                bb = beats[bi]
                frame = bb.draw(T - bb.start)
        else:
            if near:
                bd = near[0]
                nxt = [k for k, b in enumerate(beats) if abs(b.start - bd) < 1e-6][0]
                p = eio((T - (bd - T_HALF)) / (2 * T_HALF))
                old, new = beats[nxt - 1], beats[nxt]
                fo = old.draw(old.dur + (T - bd) if T < bd else old.dur, wall_off)
                fn = new.draw(max(0.0, T - bd), wall_off)
                shift = int(W * p)
                canvas = Image.new("RGB", (W, H))
                canvas.paste(fo, (-shift, 0))
                canvas.paste(fn, (W - shift, 0))
                speed = abs(math.sin(math.pi * p)) * 70
                frame = directional_blur(canvas, speed)
            else:
                bb = beats[bi]
                frame = bb.draw(T - bb.start, wall_off)
        if fi == int(cover_T * FPS):
            frame.save(out / f"adipec26-thanks_cover_{STYLE}_{ASPECT}_v{ver}.jpg", quality=90)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", out / name, "frames", n_frames, "duration", round(total, 2), "s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
