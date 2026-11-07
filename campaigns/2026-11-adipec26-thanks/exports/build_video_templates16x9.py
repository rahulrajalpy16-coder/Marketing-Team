#!/usr/bin/env python3
"""ADIPEC 2026 thank-you, three 16:9 recreations of the template designs Rahul supplied (v14).

Rahul asked for videos "like the template": the same scene designs and motion, with the event's own content. The
originals are paid After Effects projects that cannot be used here, so each design is recreated from what the
preview videos show, drawn from scratch with the event photos (no template assets).

  clean   : 'corporate clean design'. Faint greyscale ghost of the hero photo fills the background; full-colour hero
            in a white keyline with the caption inside it; layered blue duotone crops of the SAME photo, black
            squares, big white tokens, dashed technical lines; 3D camera whip (perspective) between scenes.
  dynamic : 'dynamic colourful'. Full-bleed photos with a giant word whose letters build one by one (ghost/outline
            states), a text-as-window reveal on cream, framed photo cards with the word across them, nested colour
            frames collapsing between scenes.
  promo   : 'corporate event promo'. Navy-duotone full-bleed photos with a left-aligned title, aqua chip and info
            box, speaker-style framed photos, a photo-wall grid transition and blurred big-type slides.

Usage: python3 build_video_templates16x9.py <jpg_dir> <extra_dir> <out_dir> <version> <clean|dynamic|promo> [limit_s]
Needs Pillow, numpy, ffmpeg (libx264/aac), Inter fonts. No music: a silent AAC track is added. All motion is drawn per
frame with sub-pixel sampling and piped to ffmpeg.
"""
import math
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

STYLE = sys.argv[5] if len(sys.argv) > 5 else "clean"
LIMIT = float(sys.argv[6]) if len(sys.argv) > 6 else None
W, H, FPS = 1920, 1080, 25
SAFE = H - 70
NAVY, BLUE, LIGHT, WHITE = (10, 42, 74), (13, 74, 133), (196, 218, 240), (255, 255, 255)
CREAM, SKY, AQUA, STEEL = (245, 239, 227), (207, 227, 245), (53, 214, 197), (122, 168, 204)
FONT_DIR = "/usr/share/fonts/opentype/inter/"
REPO = Path(__file__).resolve().parents[3]
LOGO = REPO / "assets/brand/sinor-logo.png"
PARTNER_DIR = REPO / "assets/brand/partners"
EVENT_LINE = "ADIPEC 2026  ·  ABU DHABI"
DATE_LINE = "2-5 November 2026"
PARTNERS = [("Sonardyne", "sonardyne.png"), ("Fugro", "fugro.png"), ("Navis Engineering", "navis-engineering.png"),
            ("Marine Technologies", "marine-technologies-mt.png"), ("Guidance Marine", "guidance-marine.png")]

# layout: full = full-bleed photo scene, card = framed card scene, speaker = framed photo + text (promo)
BEATS = [
    dict(kind="hero", src="s8_2.jpg", cap="The Sinor Marine team at ADIPEC 2026", word="OUR TEAM", chip="TEAM", lay="full", lay_p="speaker", logo=True),
    dict(kind="title"),
    dict(kind="hero", src="s7_1.jpg", cap="Conversations at our stand", word="CONVERSATIONS", chip="VISITORS", lay="full", lay_p="speaker"),
    dict(kind="hero", src="s3_1.jpg", cap="Visitors at our stand", word="VISITORS", chip="VISITORS", lay="card"),
    dict(kind="hero", src="IMG_4413.jpg", cap="NAVIS console", word="TECHNOLOGY", chip="TECHNOLOGY", lay="card"),
    dict(kind="hero", src="IMG_4464.jpg", cap="Sonardyne SPRINT-Nav on the stand", word="DISCUSSIONS", chip="TECHNOLOGY", lay="full"),
    dict(kind="hero", src="IMG_4188.jpg", cap="Marine Technologies on the stand", word="PARTNERS", chip="PARTNERS", lay="card"),
    dict(kind="hero", src="a07555b5-23b3-4497-92aa-a3613e384bc5.jpg", cap="With Guidance Marine at our stand", word="WELCOME", chip="PARTNERS", lay="card"),
    dict(kind="hero", src="s2_2.jpg", cap="Together at our stand", word="TOGETHER", chip="STAND", lay="full", lay_p="speaker"),
    dict(kind="end"),
]
HERO_D, TITLE_D, END_D = 2.95, 2.7, 6.0
HALF = 0.26  # half length of the transition around a boundary


# ------------------------------------------------------------------------------------------------ helpers
def font(weight, size):
    return ImageFont.truetype(f"{FONT_DIR}Inter-{weight}.otf", int(size))


def eo(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def eio(x):
    x = min(max(x, 0.0), 1.0)
    return 3 * x * x - 2 * x ** 3


def tlen(text, f):
    return f.getlength(text)


def find(name, jpg, extra):
    for d in (jpg, extra):
        if (d / name).exists():
            return d / name
    raise FileNotFoundError(name)


def cover(im, w=W, h=H, crop=(0.5, 0.5)):
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    x = round((im.width - w) * crop[0])
    y = round((im.height - h) * crop[1])
    return im.crop((x, y, x + w, y + h))


def zoom_xf(img, z, size=None, cx=0.5, cy=0.5):
    w, h = img.size
    ow, oh = size or (w, h)
    return img.transform((ow, oh), Image.AFFINE,
                         (1 / z, 0, w * cx - ow * cx / z, 0, 1 / z, h * cy - oh * cy / z), resample=Image.BICUBIC)


def duotone(im, gain=1.0, dark=(5, 16, 40), mid=(24, 76, 168), light=(150, 196, 240)):
    g = np.asarray(im.convert("L"), np.float32) / 255.0
    g = np.clip((g - 0.5) * 1.2 + 0.5, 0, 1) * gain
    g = np.clip(g, 0, 1)[..., None]
    d, m, l = (np.array(c, np.float32) for c in (dark, mid, light))
    lo = d + (m - d) * (g * 2).clip(0, 1)
    hi = m + (l - m) * ((g - 0.5) * 2).clip(0, 1)
    return Image.fromarray(np.where(g < 0.5, lo, hi).astype(np.uint8), "RGB")


def vignette_bg(centre=(208, 211, 217), edge=(146, 151, 162)):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.48) / (H * 0.66)) ** 2)
    t = np.clip(r, 0, 1.15) ** 1.6
    arr = np.array(centre, np.float32)[None, None, :] * (1 - t[..., None]) + np.array(edge, np.float32)[None, None, :] * t[..., None]
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def logo_card(width, pad=18, radius=20):
    lg = Image.open(LOGO).convert("RGB")
    lg = lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)
    c = Image.new("RGBA", (lg.width + 2 * pad, lg.height + 2 * pad), (255, 255, 255, 255))
    c.paste(lg, (pad, pad))
    m = Image.new("L", c.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, c.width, c.height], radius=radius, fill=255)
    c.putalpha(m)
    return c


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
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w, h], radius=16, fill=255)
    t.putalpha(m)
    return t


def shadow_for(w, h, blur=22, alpha=120, off=(0, 16), pad=70):
    s = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(s).rectangle([pad + off[0], pad + off[1], pad + off[0] + w, pad + off[1] + h], fill=(8, 16, 36, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur)), pad


def wrap(text, f, max_w):
    ws, lines, cur = text.split(), [], ""
    for w_ in ws:
        t = (cur + " " + w_).strip()
        if tlen(t, f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    lines.append(cur)
    if len(lines) == 2:
        best = min(range(1, len(ws)), key=lambda k: max(tlen(" ".join(ws[:k]), f), tlen(" ".join(ws[k:]), f)))
        cand = [" ".join(ws[:best]), " ".join(ws[best:])]
        if max(tlen(c, f) for c in cand) <= max_w:
            lines = cand
    return lines


def fit_size(text, weight, max_w, start=420):
    s = start
    while s > 24 and tlen(text, font(weight, s)) > max_w:
        s -= 4
    return s


def find_coeffs(dst, src):
    rows = []
    for (x, y), (u, v) in zip(dst, src):
        rows.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        rows.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return tuple(np.linalg.solve(np.array(rows, float), np.array(src, float).reshape(8)))


def quad_warp(img, dst_quad):
    """Warp the whole frame into dst_quad (TL, TR, BR, BL); returns (RGB, mask)."""
    src = [(0, 0), (W, 0), (W, H), (0, H)]
    co = find_coeffs(dst_quad, src)
    out = img.transform((W, H), Image.PERSPECTIVE, co, resample=Image.BICUBIC)
    m = Image.new("L", (W, H), 255).transform((W, H), Image.PERSPECTIVE, co, resample=Image.BILINEAR)
    return out, m


def hblur(img, px, vertical=False):
    if px < 2:
        return img
    a = np.asarray(img).astype(np.float32)
    acc = np.zeros_like(a)
    n = 11
    for k in range(n):
        acc += np.roll(a, int((k - (n - 1) / 2) * px / (n - 1)), axis=0 if vertical else 1)
    return Image.fromarray((acc / n).astype(np.uint8), "RGB")


def text_rgba(size_wh, items):
    """items: (x, y, text, font, fill, anchor) drawn on a transparent layer."""
    layer = Image.new("RGBA", size_wh, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x, y, text, f, fill, anchor in items:
        d.text((x, y), text, font=f, fill=fill, anchor=anchor)
    return layer


def fade(layer, a):
    if a >= 0.999:
        return layer
    layer = layer.copy()
    layer.putalpha(layer.getchannel("A").point(lambda v: int(v * max(0.0, a))))
    return layer


def end_card(theme):
    """16:9 closing card. theme: bg ('navy' | 'cream' | 'dark'), text, accent, sub colours."""
    img = Image.new("RGB", (W, H), theme["bg"])
    d = ImageDraw.Draw(img)
    if theme.get("grad"):
        for y in range(H):
            c = tuple(int(NAVY[i] + (BLUE[i] - NAVY[i]) * (y / H) * 0.9) for i in range(3))
            d.line([(0, y), (W, y)], fill=c)
    img = img.convert("RGBA")
    lc = logo_card(460, 20, 22)
    sh, sp = shadow_for(lc.width, lc.height, 14, 60, (0, 8), 40)
    img.alpha_composite(sh, (140 - sp, 150 - sp))
    img.alpha_composite(lc, (140, 150))
    d = ImageDraw.Draw(img)
    d.text((140, 400), "Thank you", font=font("ExtraBold", fit_size("Thank you", "ExtraBold", 800, 170)), fill=theme["text"] + (255,))
    d.rectangle([146, 590, 146 + 120, 599], fill=theme["accent"] + (255,))
    f1, f2 = font("SemiBold", 40), font("Medium", 38)
    y = 636
    for ln in wrap("To every client and visitor who stopped by our stand.", f1, 760):
        d.text((140, y), ln, font=f1, fill=theme["text"] + (255,))
        y += 54
    y += 20
    for ln in wrap("And to our technology partners for their support:", f2, 760):
        d.text((140, y), ln, font=f2, fill=theme["sub"] + (255,))
        y += 50
    tw_, th_ = 400, 120
    xs = [1020, 1450]
    ys = [140, 380, 620]
    for k, (name, logo) in enumerate(PARTNERS):
        r, c = divmod(k, 2)
        alone = (k == len(PARTNERS) - 1) and (len(PARTNERS) % 2 == 1)
        x = (xs[0] + xs[1] + tw_) // 2 - tw_ // 2 if alone else xs[c]
        yy = ys[r]
        tile = partner_tile(logo, tw_, th_)
        sh, sp = shadow_for(tw_, th_, 12, 70, (0, 8), 40)
        img.alpha_composite(sh, (x - sp, yy - sp))
        img.alpha_composite(tile, (x, yy))
        d.text((x + tw_ // 2, yy + th_ + 10), name, font=font("SemiBold", 32), fill=theme["text"] + (255,), anchor="mt")
    return img.convert("RGB")


def hero_rect(im, max_w, max_h):
    a = im.width / im.height
    if a >= max_w / max_h:
        return int(max_w), int(max_w / a)
    return int(max_h * a), int(max_h)


# ================================================================================================ STYLE: clean
class CleanBeat:
    def __init__(self, idx, spec, start, dur, jpg, extra):
        self.i, self.spec, self.start, self.dur, self.kind = idx, spec, start, dur, spec["kind"]
        rng = random.Random(300 + idx * 13)
        if self.kind == "hero":
            im = Image.open(find(spec["src"], jpg, extra)).convert("RGB")
            self.hw, self.hh = hero_rect(im, 0.50 * W, 0.58 * H)
            self.src = im.resize((self.hw, self.hh), Image.LANCZOS)
            self.cx, self.cy = W / 2, 0.50 * H
            g = cover(im).convert("L").filter(ImageFilter.GaussianBlur(3)).convert("RGB")
            base = vignette_bg()
            self.bg = Image.blend(base, g, 0.38)
            self.make_tiles(rng, im)
            self.shadow, self.spad = shadow_for(self.hw, self.hh, 28, 130, (0, 20), 80)
            self.portrait = self.hw < 600
            self.cap_layer = self.make_caption(spec["cap"])
        elif self.kind == "title":
            self.hw, self.hh = int(0.56 * W), int(0.62 * H)
            self.cx, self.cy = W / 2, 0.50 * H
            self.bg = vignette_bg()
            self.make_tiles(rng, None)
            self.src = self.make_title()
            self.shadow, self.spad = shadow_for(self.hw, self.hh, 28, 130, (0, 20), 80)
        else:
            self.bg = vignette_bg()
            card = end_card(dict(bg=NAVY, text=WHITE, accent=LIGHT, sub=LIGHT, grad=True))
            sc = 0.90
            self.src = card.resize((int(W * sc), int(H * sc)), Image.LANCZOS)
            self.hw, self.hh = self.src.size
            self.cx, self.cy = W / 2, H / 2
            self.make_tiles(rng, None)
            self.shadow, self.spad = shadow_for(self.hw, self.hh, 28, 130, (0, 20), 80)

    def make_tiles(self, rng, im):
        self.tiles = []
        pool = [im] if im is not None else None
        for k in range(10):
            w, h = rng.choice([(200, 150), (260, 200), (340, 250), (420, 300), (520, 360), (240, 320), (300, 400)])
            if im is None:
                src = Image.open(rng.choice(sorted(TILE_POOL))).convert("RGB")
            else:
                src = im
            s = rng.uniform(0.35, 0.85)
            cw = src.width * s
            ch = cw * h / w
            if ch > src.height:
                ch = src.height * s
                cw = ch * w / h
            x0 = rng.uniform(0, src.width - cw)
            y0 = rng.uniform(0, src.height - ch)
            crop = src.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS)
            tile = duotone(crop, rng.uniform(0.75, 1.15)).convert("RGBA")
            side = rng.choice([-1, 1])
            tx = W / 2 + side * rng.uniform(0.28 * W, 0.50 * W)
            ty = rng.uniform(0.04 * H, 0.96 * H)
            if rng.random() < 0.35:  # some tiles tuck under the hero edges
                tx = W / 2 + side * rng.uniform(0.18 * W, 0.30 * W)
            self.tiles.append(dict(img=tile, cx=tx, cy=ty, vx=rng.uniform(-9, 9), vy=rng.uniform(-6, 6),
                                   alpha=rng.uniform(0.70, 0.95), depth=w * h))
        self.tiles.sort(key=lambda t: t["depth"])
        self.squares = [(rng.randint(40, W - 80), rng.randint(40, H - 80), rng.choice([22, 30, 40, 52])) for _ in range(6)]
        self.tokens = [("26", rng.choice([(0.08, 0.08), (0.74, 0.70)])), ("AD", rng.choice([(0.74, 0.07), (0.07, 0.72)]))]

    def make_caption(self, cap):
        if self.portrait:  # narrow photo: a navy plate under the frame so nothing covers the picture
            f1, f2 = font("SemiBold", 22), font("ExtraBold", 46)
            w = int(max(tlen(cap, f2), tlen("ADIPEC 2026  \u00b7  ABU DHABI", f1)) + 64)
            plate = Image.new("RGBA", (w, 112), NAVY + (245,))
            pd = ImageDraw.Draw(plate)
            pd.rectangle([0, 0, 8, 112], fill=LIGHT + (255,))
            pd.text((30, 14), "ADIPEC 2026  \u00b7  ABU DHABI", font=f1, fill=LIGHT + (255,))
            pd.text((30, 48), cap, font=f2, fill=WHITE + (255,))
            return plate
        w, h = self.hw, self.hh
        lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        g = ImageDraw.Draw(lay)
        for y in range(int(h * 0.55), h):
            a = int(210 * (max(0.0, (y - h * 0.55)) / (h * 0.45)) ** 1.5)
            g.line([(0, y), (w, y)], fill=NAVY + (a,))
        g.text((34, h - 98), "ADIPEC 2026  ·  ABU DHABI", font=font("SemiBold", 22), fill=LIGHT + (255,))
        g.text((34, h - 68), cap, font=font("ExtraBold", 46), fill=WHITE + (255,))
        return lay

    def make_title(self):
        w, h = self.hw, self.hh
        p = Image.new("RGB", (w, h), NAVY)
        d = ImageDraw.Draw(p)
        for y in range(h):
            c = tuple(int(NAVY[i] + (BLUE[i] - NAVY[i]) * (y / h) * 0.9) for i in range(3))
            d.line([(0, y), (w, y)], fill=c)
        r = p.convert("RGBA")
        lc = logo_card(340, 20, 20)
        r.alpha_composite(lc, ((w - lc.width) // 2, 50))
        d = ImageDraw.Draw(r)
        d.text((w // 2, 50 + lc.height + 30), "Thank you.", font=font("ExtraBold", 168), fill=WHITE + (255,), anchor="mt")
        d.text((w // 2, 50 + lc.height + 236), EVENT_LINE, font=font("SemiBold", 48), fill=WHITE + (255,), anchor="mt")
        d.text((w // 2, 50 + lc.height + 300), DATE_LINE, font=font("Medium", 42), fill=LIGHT + (255,), anchor="mt")
        return r.convert("RGB")

    def draw(self, t):
        img = self.bg.copy()
        d_in = eo(t / 0.5)
        # dashed technical lines and plus marks
        d = ImageDraw.Draw(img, "RGBA")
        for y in (int(H * 0.30), int(H * 0.74)):
            for x in range(0, W, 36):
                d.line([(x, y), (x + 16, y)], fill=(255, 255, 255, 80), width=1)
        for x in (int(W * 0.17), int(W * 0.83)):
            for y in range(0, H, 36):
                d.line([(x, y), (x, y + 16)], fill=(255, 255, 255, 70), width=1)
        for (px, py) in ((0.06, 0.40), (0.93, 0.34), (0.20, 0.90), (0.88, 0.88)):
            d.line([(px * W - 9, py * H), (px * W + 9, py * H)], fill=(60, 70, 90, 150), width=2)
            d.line([(px * W, py * H - 9), (px * W, py * H + 9)], fill=(60, 70, 90, 150), width=2)
        for k in range(4):  # tiny text-block lines
            d.rectangle([int(W * 0.06), int(H * 0.52) + k * 11, int(W * 0.06) + 150 - k * 28, int(H * 0.52) + k * 11 + 4], fill=(255, 255, 255, 130))
        # big white tokens
        ft = font("ExtraBold", 230)
        for k, (word, (fx, fy)) in enumerate(self.tokens):
            lay = text_rgba((520, 300), [(10, 0, word, ft, (255, 255, 255, 235), "la")])
            img.paste(lay, (int(fx * W + (1 - d_in) * (-1) ** k * 120), int(fy * H)), lay)
        # drifting duotone tiles (crops of the same photo)
        for tl in self.tiles:
            w, h = tl["img"].size
            px = tl["cx"] + tl["vx"] * t - w / 2 + (1 - d_in) * (400 if tl["cx"] > W / 2 else -400)
            py = tl["cy"] + tl["vy"] * t - h / 2
            ix, iy = math.floor(px), math.floor(py)
            tile = tl["img"].transform((w + 2, h + 2), Image.AFFINE, (1, 0, -(1 + px - ix), 0, 1, -(1 + py - iy)), resample=Image.BICUBIC)
            tile.putalpha(tile.getchannel("A").point(lambda v: int(v * tl["alpha"] * d_in)))
            img.paste(tile, (ix - 1, iy - 1), tile)
        dr = ImageDraw.Draw(img)
        for (sx, sy, ss) in self.squares:
            dr.rectangle([sx, sy, sx + ss, sy + ss], fill=(14, 22, 40))
        # hero in white keyline
        z = 1.0 + 0.055 * min(1.0, t / self.dur) if self.kind == "hero" else 1.0
        hero = zoom_xf(self.src.convert("RGB"), z).convert("RGBA")
        hx, hy = int(round(self.cx - self.hw / 2)), int(round(self.cy - self.hh / 2))
        a = min(1.0, d_in * 1.6)
        sh = self.shadow.copy()
        sh.putalpha(sh.getchannel("A").point(lambda v: int(v * a)))
        img.paste(sh, (hx - self.spad, hy - self.spad), sh)
        hero.putalpha(int(255 * a))
        ImageDraw.Draw(img).rectangle([hx - 12, hy - 12, hx + self.hw + 12, hy + self.hh + 12], outline=(255, 255, 255), width=3)
        img.paste(hero, (hx, hy), hero)
        if self.kind == "hero":
            cap = fade(self.cap_layer, eo((t - 0.2) / 0.5))
            img.paste(cap, (hx - 12, hy + self.hh + 16) if self.portrait else (hx, hy), cap)
            if self.spec.get("logo"):
                lc = logo_card(200, 14, 16)
                img.paste(lc, (hx - 12, hy - 12 - lc.height - 14), lc)
        return img


# ================================================================================================ STYLE: dynamic
class DynBeat:
    PALS = [dict(bg=CREAM, text=NAVY, a=BLUE), dict(bg=NAVY, text=CREAM, a=(70, 150, 235)),
            dict(bg=SKY, text=NAVY, a=BLUE), dict(bg=BLUE, text=WHITE, a=CREAM)]

    def __init__(self, idx, spec, start, dur, jpg, extra):
        self.i, self.spec, self.start, self.dur, self.kind = idx, spec, start, dur, spec["kind"]
        self.pal = self.PALS[idx % 4]
        self.lay = spec.get("lay", "full")
        self.col = [NAVY, BLUE, SKY]
        if self.kind == "hero":
            self.im = Image.open(find(spec["src"], jpg, extra)).convert("RGB")
            if self.lay == "full":
                self.full = cover(self.im, int(W * 1.05), int(H * 1.05))
            else:
                hw, hh = hero_rect(self.im, 0.60 * W, 0.66 * H)
                b = 20
                card = Image.new("RGB", (hw + 2 * b, hh + 2 * b), (255, 255, 255))
                card.paste(self.im.resize((hw, hh), Image.LANCZOS), (b, b))
                self.card = card.convert("RGBA")
                self.cw, self.ch = self.card.size
                self.shadow, self.spad = shadow_for(self.cw, self.ch, 26, 120, (0, 20), 80)
        elif self.kind == "title":
            self.pal = dict(bg=CREAM, text=NAVY, a=BLUE)
            _im = Image.open(find("s8_2.jpg", jpg, extra)).convert("RGB")
            _base = cover(_im, int(W * 1.1), int(H * 1.1)).filter(ImageFilter.GaussianBlur(40))
            _fw = int(W * 1.08)
            _fg = _im.resize((_fw, int(_im.height * _fw / _im.width)), Image.LANCZOS)
            _base.paste(_fg, ((_base.width - _fw) // 2, int(0.17 * H)))
            self.photo = _base
        elif self.kind == "end":
            self.pal = dict(bg=CREAM, text=NAVY, a=BLUE)
            self.endimg = end_card(dict(bg=CREAM, text=NAVY, accent=BLUE, sub=BLUE))

    # ---- letter animations
    def letters(self, t, text, size, cx, cy, fill, outline_idx=None, exit_t=None):
        f = font("ExtraBold", size)
        total = sum(f.getlength(c) for c in text) + (len(text) - 1) * size * 0.012
        x = cx - total / 2
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for k, ch in enumerate(text):
            adv = f.getlength(ch)
            delay = 0.045 * k
            e = eo((t - delay) / 0.30)
            if exit_t is not None:
                e *= 1 - eo((t - (exit_t + 0.03 * k)) / 0.25)
            if e > 0.01 and ch != " ":
                if outline_idx is not None and k in outline_idx and e < 1.0 or (outline_idx is not None and k in outline_idx and t < 0.55 + delay):
                    big = Image.new("L", (int(adv + 40), int(size * 1.5)), 0)
                    small = Image.new("L", big.size, 0)
                    ImageDraw.Draw(big).text((20, 10), ch, font=f, fill=255, stroke_width=3)
                    ImageDraw.Draw(small).text((20, 10), ch, font=f, fill=255)
                    ol = ImageChops.subtract(big, small)
                    col = Image.new("RGBA", big.size, fill + (255,))
                    col.putalpha(ol.point(lambda v: int(v * min(1, e * 1.4))))
                    layer.alpha_composite(col, (int(x - 20), int(cy - size * 0.62 + (1 - e) * size * 0.3)))
                else:
                    d.text((x, cy - size * 0.62 + (1 - e) * size * 0.35), ch, font=f, fill=fill + (int(255 * min(1, e * 1.5)),))
            x += adv + size * 0.012
        return layer

    def draw(self, t):
        pal = self.pal
        if self.kind == "hero" and self.lay == "full":
            z = 1.0 + 0.035 * min(1, t / self.dur)
            img = zoom_xf(self.full, z).crop(((self.full.width - W) // 2, (self.full.height - H) // 2, (self.full.width - W) // 2 + W, (self.full.height - H) // 2 + H))
            img = img.convert("RGBA")
            if not hasattr(DynBeat, "_grad"):
                g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                gd = ImageDraw.Draw(g)
                for y in range(H):
                    gd.line([(0, y), (W, y)], fill=(6, 20, 44, int(40 + 150 * (y / H) ** 2.2)))
                DynBeat._grad = g
            img.alpha_composite(DynBeat._grad)
            word = self.spec["word"]
            size = min(fit_size(word, "ExtraBold", 0.84 * W, 250), 250)
            lay = self.letters(t, word, size, W / 2, H * 0.735, (255, 255, 255), outline_idx={min(3, len(word) - 1)})
            sh = lay.filter(ImageFilter.GaussianBlur(10))
            sh.putalpha(sh.getchannel("A").point(lambda v: int(v * 0.35)))
            img.alpha_composite(sh, (0, 8))
            img.alpha_composite(lay)
            self.caption(img, t, light=True)
            return img.convert("RGB")
        img = Image.new("RGB", (W, H), pal["bg"])
        d = ImageDraw.Draw(img)
        if self.kind == "hero":
            e = eo((t - 0.05) / 0.5)
            cxx, cyy = W / 2, H * 0.47
            # layered colour block behind the card
            side = 1 if self.i % 2 else -1
            d.rectangle([cxx - self.cw / 2 - side * 54, cyy - self.ch / 2 + 46, cxx + self.cw / 2 - side * 54, cyy + self.ch / 2 + 46],
                        fill=pal["a"] if pal["bg"] != BLUE else CREAM)
            # card with slow zoom and slight tilt (sub-pixel)
            z = 0.92 + 0.08 * e + 0.04 * min(1, t / self.dur)
            ang = side * -2.0 * (1 - 0.5 * min(1, t / self.dur))
            big = Image.new("RGBA", (int(self.cw * 1.2), int(self.ch * 1.2)), (0, 0, 0, 0))
            big.paste(self.card, ((big.width - self.cw) // 2, (big.height - self.ch) // 2))
            a = math.radians(ang)
            ca, sa = math.cos(a) / z, math.sin(a) / z
            bx, by = big.width / 2, big.height / 2
            xf = big.transform(big.size, Image.AFFINE, (ca, sa, bx - ca * bx - sa * by, -sa, ca, by + sa * bx - ca * by), resample=Image.BICUBIC)
            sh = fade(self.shadow, e)
            img.paste(sh, (int(cxx - self.cw / 2 - self.spad), int(cyy - self.ch / 2 - self.spad)), sh)
            xf = fade(xf, e * 1.4)
            img.paste(xf, (int(cxx - big.width / 2), int(cyy - big.height / 2)), xf)
            # the word runs ACROSS the card in white (like the template's STYLSH card)
            word = self.spec["word"]
            size = min(fit_size(word, "ExtraBold", 0.60 * W, 230), 230)
            wy = cyy + self.ch * 0.27
            out_col = CREAM if pal["bg"] in (NAVY, BLUE) else NAVY
            lay_in = self.letters(t, word, size, cxx, wy, (255, 255, 255), outline_idx={0})
            lay_out = self.letters(t, word, size, cxx, wy, out_col, outline_idx={0})
            clip = Image.new("L", (W, H), 0)
            ImageDraw.Draw(clip).rectangle([int(cxx - self.cw / 2 + 14), int(cyy - self.ch / 2 + 14), int(cxx + self.cw / 2 - 14), int(cyy + self.ch / 2 - 14)], fill=255)
            lay_in.putalpha(ImageChops.multiply(lay_in.getchannel("A"), clip))
            lay_out.putalpha(ImageChops.multiply(lay_out.getchannel("A"), ImageChops.invert(clip)))
            sh2 = lay_in.filter(ImageFilter.GaussianBlur(8))
            sh2.putalpha(sh2.getchannel("A").point(lambda v: int(v * 0.4)))
            img = img.convert("RGBA")
            img.alpha_composite(sh2, (0, 6))
            img.alpha_composite(lay_out)
            img.alpha_composite(lay_in)
            self.caption(img, t, light=(pal["text"] in (CREAM, WHITE)))
            return img.convert("RGB")
        if self.kind == "title":
            # text-as-window: the team photo shows through giant letters on cream
            e = eo(t / 0.7)
            word = "THANK YOU."
            size = fit_size(word, "ExtraBold", 0.90 * W, 360)
            f = font("ExtraBold", size)
            mask = Image.new("L", (W, H), 0)
            md = ImageDraw.Draw(mask)
            total = tlen(word, f)
            md.text(((W - total) / 2, H * 0.52 - size * 0.55), word, font=f, fill=255)
            sc = 1.55 - 0.55 * e
            mask = zoom_xf(mask, sc)
            z = 1.0 + 0.05 * min(1, t / self.dur)
            ph = zoom_xf(self.photo, z).crop(((self.photo.width - W) // 2, (self.photo.height - H) // 2, (self.photo.width - W) // 2 + W, (self.photo.height - H) // 2 + H))
            ol = Image.new("L", (W, H), 0)
            ImageDraw.Draw(ol).text(((W - total) / 2, H * 0.52 - size * 0.55), word, font=f, fill=255, stroke_width=9)
            ol = zoom_xf(ol, sc)
            img.paste(Image.new("RGB", (W, H), NAVY), (0, 0), ol)
            ph = ImageEnhance.Brightness(ImageEnhance.Contrast(ph).enhance(1.15)).enhance(1.45)
            img.paste(ph, (0, 0), mask)
            ef = eo((t - 0.7) / 0.5)
            lc = logo_card(300, 16, 18)
            img.paste(lc, ((W - lc.width) // 2, int(H * 0.06)), lc)
            lay = text_rgba((W, 120), [(W / 2, 0, EVENT_LINE, font("SemiBold", 46), pal["text"] + (int(255 * ef),), "mt"),
                                       (W / 2, 62, DATE_LINE, font("Medium", 40), BLUE + (int(255 * ef),), "mt")])
            img.paste(lay, (0, int(H * 0.84 + (1 - ef) * 20)), lay)
            return img
        # end card
        e = eo(t / 0.5)
        im = self.endimg.copy()
        return im

    def caption(self, img, t, light):
        e = eo((t - 0.32) / 0.45)
        col = (255, 255, 255) if light else self.pal["text"]
        bar = (255, 255, 255) if light else self.pal["a"]
        d = ImageDraw.Draw(img)
        d.rectangle([90, H - 176, 90 + 110 * e, H - 167], fill=bar + (255,))
        lay = text_rgba((W, 90), [(90, 0, self.spec["cap"], font("ExtraBold", 52), col + (int(255 * e),), "la")])
        img.alpha_composite(lay, (0, int(H - 152 + (1 - e) * 22))) if img.mode == "RGBA" else img.paste(lay, (0, int(H - 152 + (1 - e) * 22)), lay)


# ================================================================================================ STYLE: promo
class PromoBeat:
    wall = None

    def __init__(self, idx, spec, start, dur, jpg, extra):
        self.i, self.spec, self.start, self.dur, self.kind = idx, spec, start, dur, spec["kind"]
        self.lay = spec.get("lay_p", spec.get("lay", "full"))
        if self.kind == "hero":
            im = Image.open(find(spec["src"], jpg, extra)).convert("RGB")
            if self.lay == "full":
                self.full = cover(im, int(W * 1.1), int(H * 1.1))
                self.tinted = Image.blend(self.full, duotone(self.full, 0.95, (4, 12, 32), (18, 60, 140), (130, 180, 235)), 0.62)
            else:
                self.hw, self.hh = hero_rect(im, 0.46 * W, 0.78 * H)
                self.src = im.resize((self.hw, self.hh), Image.LANCZOS)
                self.shadow, self.spad = shadow_for(self.hw, self.hh, 26, 150, (0, 18), 80)
        elif self.kind == "end":
            self.endimg = end_card(dict(bg=NAVY, text=WHITE, accent=AQUA, sub=AQUA, grad=True))

    def chip(self, text):
        f = font("Bold", 30)
        w = int(tlen(text, f) + 52)
        c = Image.new("RGBA", (w, 56), AQUA + (255,))
        ImageDraw.Draw(c).text((26, 11), text, font=f, fill=NAVY + (255,))
        return c

    def info(self, ct, left, top, img):
        box = Image.new("RGBA", (520, 124), (0, 0, 0, 0))
        bd = ImageDraw.Draw(box)
        bd.rectangle([0, 0, 518, 122], outline=AQUA + (int(255 * ct),), width=2)
        bd.text((22, 16), "ADIPEC 2026", font=font("Bold", 32), fill=WHITE + (int(255 * ct),))
        bd.text((22, 62), "ABU DHABI  ·  2-5 NOV 2026", font=font("Medium", 30), fill=LIGHT + (int(255 * ct),))
        img.paste(box, (left, int(top + (1 - ct) * 24)), box)

    def draw(self, t, wall_off):
        if self.kind == "end":
            return self.endimg.copy()
        if self.kind == "title":
            img = PromoBeat.wall_frame(wall_off)
            d = ImageDraw.Draw(img, "RGBA")
            e = eo(t / 0.5)
            lc = logo_card(300, 16, 18)
            img.paste(lc, (140, int(H * 0.10)), lc)
            f = font("ExtraBold", 250)
            lay = Image.new("RGBA", (W, 560), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            ld.text((140, 0), "THANK", font=f, fill=WHITE + (int(255 * e),))
            bw = (tlen("YOU", f) + 70) * eo((t - 0.15) / 0.45)
            ld.rectangle([140, 268, 140 + bw, 268 + 262], fill=AQUA + (255,))
            if bw > 30:
                ld.text((175, 262), "YOU", font=f, fill=NAVY + (255,))
            img.paste(lay, (0, int(H * 0.24 + (1 - e) * 40)), lay)
            ef = eo((t - 0.6) / 0.5)
            lay2 = text_rgba((900, 130), [(0, 0, EVENT_LINE, font("SemiBold", 48), WHITE + (int(255 * ef),), "la"),
                                          (0, 64, DATE_LINE, font("Medium", 42), AQUA + (int(255 * ef),), "la")])
            img.paste(lay2, (140, int(H * 0.82 + (1 - ef) * 20)), lay2)
            return img.convert("RGB")
        if self.lay == "full":
            z = 1.0 + 0.06 * min(1, t / self.dur)
            ph = zoom_xf(self.tinted, z).crop(((self.tinted.width - W) // 2, (self.tinted.height - H) // 2, (self.tinted.width - W) // 2 + W, (self.tinted.height - H) // 2 + H)).convert("RGBA")
            sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            sd = ImageDraw.Draw(sh)
            for x in range(0, int(W * 0.72)):
                sd.line([(x, 0), (x, H)], fill=(4, 12, 34, int(190 * (1 - x / (W * 0.72)) ** 1.3)))
            ph.alpha_composite(sh)
            img = ph
            self.title_block(img, t, left=140, top=int(H * 0.36), width=int(W * 0.56))
            lc = logo_card(150, 12, 14)
            img.alpha_composite(lc, (W - lc.width - 60, 50))
            return img.convert("RGB")
        # speaker layout: framed photo left, text right on the dim photo wall
        img = PromoBeat.wall_frame(wall_off)
        e = eo(t / 0.45)
        hx, hy = 150, (H - self.hh) // 2
        zz = 1.0 + 0.05 * min(1, t / self.dur)
        hero = zoom_xf(self.src, zz).convert("RGBA")
        hero.putalpha(int(255 * min(1, e * 1.5)))
        sh = self.shadow
        img.paste(sh, (hx - self.spad, hy - self.spad), sh)
        ImageDraw.Draw(img).rectangle([hx - 12, hy - 12, hx + self.hw + 12, hy + self.hh + 12], outline=(255, 255, 255), width=3)
        img.paste(hero, (hx, hy), hero)
        self.title_block(img, t, left=hx + self.hw + 110, top=int(H * 0.30), width=W - (hx + self.hw + 110) - 90)
        return img.convert("RGB")

    def title_block(self, img, t, left, top, width):
        ec = eo((t - 0.1) / 0.4)
        chip = self.chip(self.spec["chip"])
        chip = fade(chip, ec)
        img.paste(chip, (left - int((1 - ec) * 50), top), chip) if img.mode == "RGBA" else img.paste(chip, (left - int((1 - ec) * 50), top), chip)
        ct = eo((t - 0.22) / 0.5)
        for fs in (92, 84, 76, 68, 60):
            f1 = font("ExtraBold", fs)
            lines = wrap(self.spec["cap"], f1, width)
            if len(lines) <= 2:
                break
        lay = Image.new("RGBA", (W, 330), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for k, ln in enumerate(lines[:3]):
            ld.text((left, k * int(fs * 1.08)), ln, font=f1, fill=WHITE + (int(255 * ct),))
        y = top + 84 + (1 - ct) * 30
        if img.mode == "RGBA":
            img.alpha_composite(lay, (0, int(y)))
        else:
            img.paste(lay, (0, int(y)), lay)
        self.info(ct, left, int(y + len(lines[:3]) * int(fs * 1.08) + 28), img)

    @staticmethod
    def build_wall(pool):
        cols = 8
        s = W // cols
        rows = (H // s) + 4
        rows += rows % 2
        rng = random.Random(11)
        wall = Image.new("RGB", (W, rows * s))
        order = pool[:]
        rng.shuffle(order)
        for r in range(rows):
            for c in range(cols):
                im = Image.open(order[(r * cols + c) % len(order)]).convert("RGB")
                side = min(im.size)
                x0, y0 = rng.randint(0, im.width - side), rng.randint(0, im.height - side)
                tile = im.crop((x0, y0, x0 + side, y0 + side)).resize((s, s), Image.LANCZOS)
                wall.paste(duotone(tile, rng.uniform(0.7, 1.05)), (c * s, r * s))
        a = np.asarray(wall).astype(np.float32) * 0.62 + np.array([8, 22, 56], np.float32) * 0.38
        PromoBeat.wall_img = Image.fromarray(a.astype(np.uint8), "RGB")
        PromoBeat.wall_h = rows * s
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r_ = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.5) / (H * 0.8)) ** 2)
        PromoBeat.vig = (1 - np.clip(r_ - 0.25, 0, 1) * 0.55)[..., None]

    @staticmethod
    def wall_frame(off):
        off = int(off) % PromoBeat.wall_h
        w = PromoBeat.wall_img
        if off + H <= PromoBeat.wall_h:
            crop = w.crop((0, off, W, off + H))
        else:
            crop = Image.new("RGB", (W, H))
            crop.paste(w.crop((0, off, W, PromoBeat.wall_h)), (0, 0))
            crop.paste(w.crop((0, 0, W, H - (PromoBeat.wall_h - off))), (0, PromoBeat.wall_h - off))
        a = np.asarray(crop).astype(np.float32) * PromoBeat.vig
        return Image.fromarray(a.astype(np.uint8), "RGB").convert("RGBA")


TILE_POOL = []


# ================================================================================================ main
def main():
    global TILE_POOL
    if len(sys.argv) < 6:
        print(__doc__)
        return 2
    jpg, extra, out, ver = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
    out.mkdir(parents=True, exist_ok=True)
    pool = sorted(list(jpg.glob("*.jpg")) + list(extra.glob("*.jpg")))
    TILE_POOL = pool
    Cls = {"clean": CleanBeat, "dynamic": DynBeat, "promo": PromoBeat}[STYLE]
    if STYLE == "promo":
        PromoBeat.build_wall(pool)
    beats, t0 = [], -0.55
    for i, spec in enumerate(BEATS):
        dur = {"hero": HERO_D, "title": TITLE_D, "end": END_D}[spec["kind"]]
        beats.append(Cls(i, spec, t0, dur, jpg, extra))
        t0 += dur
    total = t0 if LIMIT is None else min(t0, LIMIT)
    n_frames = int(round(total * FPS))
    name = f"adipec26-thanks_linkedin_{STYLE}_16x9_v{ver}.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000", "-t", f"{total:.3f}",
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(out / name)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    bounds = [b.start for b in beats[1:]]
    base_bg = vignette_bg()
    for fi in range(n_frames):
        T = fi / FPS
        wall_off = fi * 2
        bi = max(k for k, b in enumerate(beats) if b.start <= T)
        near = [bd for bd in bounds if abs(T - bd) < HALF]
        draw = (lambda b, tt: b.draw(tt, wall_off)) if STYLE == "promo" else (lambda b, tt: b.draw(tt))
        if not near:
            b = beats[bi]
            frame = draw(b, T - b.start)
        else:
            bd = near[0]
            nxt = [k for k, b in enumerate(beats) if abs(b.start - bd) < 1e-6][0]
            old, new = beats[nxt - 1], beats[nxt]
            q = (T - (bd - HALF)) / (2 * HALF)
            if STYLE == "clean":  # 3D camera whip: both scenes in perspective, sliding through each other
                fo = draw(old, old.dur + (T - bd) if T < bd else old.dur)
                fn = draw(new, max(0.0, T - bd))
                canvas = base_bg.copy()
                qo, qn = eio(min(1.0, q * 1.25)), eio(max(0.0, (q - 0.2) / 0.8))
                so, sn = -W * 1.15 * qo, W * 1.15 * (1 - qn)
                ho, hn = 0.5 * qo, 0.5 * (1 - qn)
                if qo > 0.001:
                    wo, mo = quad_warp(fo.convert("RGB"), [(so, H * ho / 2), (so + W, 0), (so + W, H), (so, H - H * ho / 2)])
                    wo = hblur(wo, 90 * math.sin(math.pi * min(1, qo)))
                    canvas.paste(wo, (0, 0), mo)
                if qn < 0.999:
                    wn, mn = quad_warp(fn.convert("RGB"), [(sn, 0), (sn + W, H * hn / 2), (sn + W, H - H * hn / 2), (sn, H)])
                    wn = hblur(wn, 90 * math.sin(math.pi * min(1, 1 - qn)))
                    canvas.paste(wn, (0, 0), mn)
                frame = canvas
            elif STYLE == "dynamic":  # nested colour frames collapse: cover, then open onto the new scene
                scene = draw(new if T >= bd else old, (T - new.start) if T >= bd else (old.dur + (T - bd)))
                frame = scene.convert("RGB")
                cols = [NAVY, BLUE, SKY]
                if q < 0.5:
                    for k in range(3):
                        p = eio(q * 2 * 1.3 - 0.12 * k)
                        w_, h_ = int(W * p), int(H * p)
                        if w_ > 2:
                            ImageDraw.Draw(frame).rectangle([(W - w_) // 2, (H - h_) // 2, (W + w_) // 2, (H + h_) // 2], fill=cols[k])
                else:
                    for k in range(3):
                        p = 1 - eio((q - 0.5) * 2 * 1.3 - 0.12 * (2 - k))
                        if p > 0.002:
                            mask = Image.new("L", (W, H), 255)
                            md = ImageDraw.Draw(mask)
                            ph = 1 - p
                            md.rectangle([(W - int(W * ph)) // 2, (H - int(H * ph)) // 2, (W + int(W * ph)) // 2, (H + int(H * ph)) // 2], fill=0)
                            frame.paste(Image.new("RGB", (W, H), cols[k]), (0, 0), mask)
            else:  # promo: blurred slide (even boundaries) or photo-wall grid (odd boundaries)
                fo = draw(old, old.dur + (T - bd) if T < bd else old.dur).convert("RGB")
                fn = draw(new, max(0.0, T - bd)).convert("RGB")
                if nxt % 2 == 1:
                    p = eio(q)
                    shift = int(W * p)
                    canvas = Image.new("RGB", (W, H))
                    canvas.paste(fo, (-shift, 0))
                    canvas.paste(fn, (W - shift, 0))
                    frame = hblur(canvas, abs(math.sin(math.pi * p)) * 90)
                else:
                    frame = (fo if q < 0.5 else fn).copy()
                    cols_n, rows_n = 8, 4
                    cw_, ch_ = W // cols_n, H // rows_n + 1
                    rr = random.Random(nxt)
                    for r in range(rows_n):
                        for c in range(cols_n):
                            order = rr.random() * 0.4
                            pq = q * 2 if q < 0.5 else (1 - q) * 2
                            a = min(1.0, max(0.0, (pq - order) / 0.6))
                            if a > 0:
                                tile = PromoBeat.wall_img.crop((c * cw_, (r * ch_) % PromoBeat.wall_h, (c + 1) * cw_, (r * ch_) % PromoBeat.wall_h + ch_))
                                base = frame.crop((c * cw_, r * ch_, (c + 1) * cw_, r * ch_ + ch_))
                                frame.paste(Image.blend(base, tile.resize(base.size), a), (c * cw_, r * ch_))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", out / name, "frames", n_frames, "duration", round(total, 2), "s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
