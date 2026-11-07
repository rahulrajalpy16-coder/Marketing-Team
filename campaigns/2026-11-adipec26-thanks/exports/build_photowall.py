#!/usr/bin/env python3
"""ADIPEC 2026 'photo wall' reels (1080x1920, 30 fps): a high-quality recreation of the two compressed clips Rahul sent.

The sent clips (360x640) are animated photo walls: a dense masonry of rounded-corner photos on a light grained
background, with a camera that glides across the wall and zooms onto one photo at a time. This script rebuilds that
design from the ORIGINAL photos (not the low-resolution video frames): a masonry wall is composed at 2x resolution
and a virtual camera (smooth cubic path) crops and zooms it per frame with sub-pixel Lanczos resampling.
Modern type captions (glass panel, animated lines), an opening title and a closing thank-you card with the five
partner logos are drawn on top. Audio is made separately (make_music_bed.py) and muxed in.

Usage: python3 build_photowall.py <jpg_dir> <extra_dir> <out_dir> <version> <v1|v2> [audio.wav]
Needs Pillow, numpy, ffmpeg. All drawing is per frame; frames are piped to ffmpeg (libx264, yuv420p, AAC).
"""
import math
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
SAFE = H - 300
S = 2.0                      # wall resolution factor (wall pixels per base unit)
COLS, CW, GAP = 5, 252, 18   # masonry columns, column width, gutter (base units)
NAVY, BLUE, LIGHT, WHITE = (10, 42, 74), (13, 74, 133), (196, 218, 240), (255, 255, 255)
BG = (222, 217, 211)
FONT_DIR = "/usr/share/fonts/opentype/inter/"
REPO = Path(__file__).resolve().parents[3]
LOGO = REPO / "assets/brand/sinor-logo-transparent.png"
PARTNER_DIR = REPO / "assets/brand/partners"
PARTNERS = [("Sonardyne", "sonardyne.png"), ("Fugro", "fugro.png"), ("Navis Engineering", "navis-engineering.png"),
            ("Marine Technologies", "marine-technologies-mt.png"), ("Guidance Marine", "guidance-marine.png")]

# Photos that may fill the wall (original-resolution Drive photos first, then crops of Rahul's chat sheets).
POOL = ["0f44943b-22e6-4381-aac3-66a9dfc31218.jpg", "0bc7989f-ffd8-4930-b538-267cc2414e4e.jpg", "a07555b5-23b3-4497-92aa-a3613e384bc5.jpg",
        "cf677e0a-bf65-4e06-8a7a-9a40f904137c.jpg", "IMG_4156.jpg", "IMG_4158.jpg", "IMG_4163.jpg", "IMG_4188.jpg", "IMG_4255.jpg",
        "IMG_4403.jpg", "IMG_4413.jpg", "IMG_4432.jpg", "IMG_4464.jpg",
        "s2_1.jpg", "s2_2.jpg", "s3_1.jpg", "s3_2.jpg", "s3_3.jpg", "s4_1.jpg", "s4_3.jpg", "s5_1.jpg", "s6_1.jpg", "s7_1.jpg",
        "s7_3.jpg", "s8_1.jpg", "s8_2.jpg", "IMG_4434.jpg", "IMG_4435.jpg", "n1_sonardyne_group.jpg"]

# Hero beats: photo, title line, small line. Each hero beat lasts 4 beats at 100 BPM (2.4 s).
HEROES = {
    "v1": [("s8_2.jpg", "The Sinor Marine team", "at ADIPEC 2026", None),
           ("s7_1.jpg", "Conversations", "at our stand", None),
           ("n2_sprintnav.jpg", "Sonardyne SPRINT-Nav", "on the stand", "sonardyne.png"),
           ("IMG_4413.jpg", "Navis Engineering", "console on the stand", "navis-engineering.png"),
           ("IMG_4188.jpg", "Marine Technologies", "on the stand", "marine-technologies-mt.png"),
           ("a07555b5-23b3-4497-92aa-a3613e384bc5.jpg", "With Guidance Marine", "at our stand", "guidance-marine.png"),
           ("n3_visitors.jpg", "Visitors", "at our stand", None)],
    "v2": [("s8_2.jpg", "The Sinor Marine team", "at ADIPEC 2026", None),
           ("n2_sprintnav.jpg", "Sonardyne SPRINT-Nav", "on the stand", "sonardyne.png"),
           ("IMG_4413.jpg", "Navis Engineering", "console on the stand", "navis-engineering.png"),
           ("IMG_4188.jpg", "Marine Technologies", "on the stand", "marine-technologies-mt.png"),
           ("a07555b5-23b3-4497-92aa-a3613e384bc5.jpg", "With Guidance Marine", "at our stand", "guidance-marine.png"),
           ("n3_visitors.jpg", "Visitors", "at our stand", None)],
}
# Photos that show Sinor Marine staff: they fill the wall around the opening title (top of the wall).
OPEN_TEAM = ["s8_2.jpg", "s8_1.jpg", "s2_2.jpg", "s5_1.jpg", "s2_1.jpg", "0f44943b-22e6-4381-aac3-66a9dfc31218.jpg",
             "cf677e0a-bf65-4e06-8a7a-9a40f904137c.jpg", "s8_3.jpg"]
OPEN_ZONE = 1250           # wall y (base units) below which fillers are team photos
PIN = "n1_sonardyne_group.jpg"   # Sonardyne team + SPRINT-Nav group photo, pinned beside the SPRINT-Nav hero
PIN_FOR = "n2_sprintnav.jpg"
BEAT = 0.6                 # seconds per beat (100 BPM)
HERO_D = 4 * BEAT          # 2.4 s
OPEN_D = 4 * BEAT
TOTAL = {"v1": 24.6, "v2": 22.2}
# ------------------------------------------------------------------------------------------------------


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}{name}.otf", int(size))


def smooth(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def eo(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def find(name, jpg, extra):
    for d in (jpg, extra):
        if (d / name).exists():
            return d / name
    raise FileNotFoundError(name)


def cover_to(im, w, h, focus=(0.5, 0.45)):
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    x = round((im.width - w) * focus[0])
    y = round((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))


def rounded_mask(w, h, r):
    m = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=r * 2, fill=255)
    return m.resize((w, h), Image.LANCZOS)


# =========================================================================================================== wall
def build_wall(heroes, jpg, extra, seed):
    rng = random.Random(seed)
    cols_x = [GAP + c * (CW + GAP) for c in range(COLS)]
    wall_w = GAP + COLS * (CW + GAP)
    heights = [GAP] * COLS
    placed = []
    last = {}

    def pick(avoid, y=None):
        cands = [p for p in POOL if p not in avoid]
        if y is not None and y < OPEN_ZONE:
            team = [p for p in OPEN_TEAM if p not in avoid]
            if team:
                cands = team
        cands.sort(key=lambda p: last.get(p, -999))
        top = cands[:max(4, len(cands) // 3)] if len(cands) > 8 else cands[:2]
        p = rng.choice(top)
        last[p] = len(placed)
        return p

    def add(col, w, h, path, hero=False):
        placed.append(dict(path=path, x=cols_x[col], y=heights[col], w=w, h=h, hero=hero))
        heights[col] += h + GAP
        return placed[-1]

    hero_rects, hero_pairs = [], [(1, 2), (2, 3), (0, 1), (2, 3), (1, 2), (3, 4), (0, 1), (2, 3)]
    avoid_near = set()
    for j, (hp, _, _, _) in enumerate(heroes):
        c1, c2 = hero_pairs[j % len(hero_pairs)]
        target = 330 + j * 640
        while min(heights[c1], heights[c2]) < target:
            col = c1 if heights[c1] <= heights[c2] else c2
            add(col, CW, rng.choice([210, 270, 330, 390, 450]), pick({hp} | avoid_near, heights[col]))
        if hp == PIN_FOR:  # Sonardyne group photo directly above the SPRINT-Nav hero tile
            add(c1, CW, 390, PIN)
        y = max(heights[c1], heights[c2])
        for col in (c1, c2):  # level the shorter column so the wide hero tile has no hole beside it
            gap = y - heights[col]
            if gap > 0:
                if gap - GAP >= 70:
                    add(col, CW, gap - GAP, pick({hp} | avoid_near, heights[col]))
                else:
                    heights[col] = y
        im = Image.open(find(hp, jpg, extra))
        ar = min(max(im.width / im.height, 0.58), 1.8)
        hw = 2 * CW + GAP
        hh = int(round(hw / ar))
        placed.append(dict(path=hp, x=cols_x[c1], y=y, w=hw, h=hh, hero=True))
        hero_rects.append((cols_x[c1], y, hw, hh))
        heights[c1] = heights[c2] = y + hh + GAP
        avoid_near = {hp}
    # tail fill below the last hero, then level every column
    for _ in range(14):
        col = heights.index(min(heights))
        add(col, CW, rng.choice([210, 270, 330, 390]), pick(avoid_near))
    wall_h = max(heights)
    for col in range(COLS):
        gap = wall_h - heights[col]
        if gap - GAP >= 60:
            add(col, CW, gap - GAP, pick(avoid_near))
    return placed, hero_rects, wall_w, wall_h


def render_wall(placed, wall_w, wall_h, jpg, extra):
    ww, wh = int(wall_w * S), int(wall_h * S)
    rng = np.random.default_rng(5)
    wall = Image.new("RGB", (ww, wh), BG)
    # fine paper grain added in thin strips (keeps memory small)
    for y0 in range(0, wh, 256):
        y1 = min(wh, y0 + 256)
        strip = np.empty((y1 - y0, ww, 3), np.int16)
        strip[:] = np.array(BG, np.int16)
        strip += rng.normal(0, 4.2, (y1 - y0, ww, 1)).astype(np.int16)
        wall.paste(Image.fromarray(np.clip(strip, 0, 255).astype(np.uint8), "RGB"), (0, y0))
    cache = {}
    R = int(14 * S)
    for t in placed:
        w, h = int(t["w"] * S), int(t["h"] * S)
        if t["path"] not in cache:
            cache[t["path"]] = Image.open(find(t["path"], jpg, extra)).convert("RGB")
            if len(cache) > 8:
                cache.pop(next(iter(cache)))
        src = cache[t["path"]]
        focus = (0.5, 0.42)
        tile = cover_to(src, w, h, focus)
        x, y = int(t["x"] * S), int(t["y"] * S)
        sh = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([30, 36, 30 + w, 36 + h], radius=R, fill=(40, 30, 20, 60))
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        wall.paste(sh, (x - 30, y - 30), sh)
        wall.paste(tile, (x, y), rounded_mask(w, h, R))
    return wall


# ====================================================================================================== camera
def hermite(keys, t):
    """keys: list of (time, value, tangent_mode). Cubic Hermite with Catmull-Rom tangents; tangent_mode 0 = zero velocity."""
    if t <= keys[0][0]:
        return keys[0][1]
    if t >= keys[-1][0]:
        return keys[-1][1]
    for i in range(len(keys) - 1):
        if keys[i][0] <= t <= keys[i + 1][0]:
            break
    t0, p0, m0 = keys[i]
    t1, p1, m1 = keys[i + 1]

    def tan(k, idx):
        if keys[idx][2] == 0:
            return 0.0
        a = keys[max(idx - 1, 0)]
        b = keys[min(idx + 1, len(keys) - 1)]
        return (b[1] - a[1]) / max(b[0] - a[0], 1e-6)

    h = t1 - t0
    u = (t - t0) / h
    d0, d1 = tan(keys, i) * h, tan(keys, i + 1) * h
    return ((2 * u ** 3 - 3 * u ** 2 + 1) * p0 + (u ** 3 - 2 * u ** 2 + u) * d0 + (-2 * u ** 3 + 3 * u ** 2) * p1 + (u ** 3 - u ** 2) * d1)


def build_camera(hero_rects, wall_w, wall_h, total):
    kx, ky, kz = [], [], []
    cx0, cy0 = wall_w / 2, 560
    kx.append((0.0, cx0, 1)), ky.append((0.0, cy0, 1)), kz.append((0.0, math.log(1.5), 1))
    prev = (cx0, cy0)
    for i, (hx, hy, hw, hh) in enumerate(hero_rects):
        s = OPEN_D + i * HERO_D
        z = min(0.90 * W / hw, 0.54 * H / hh)
        hcx, hcy = hx + hw / 2, hy + hh / 2
        view_cy = hcy + 0.115 * H / z  # hero sits above the caption panel
        mid = ((prev[0] + hcx) / 2, (prev[1] + hcy) / 2)
        kx.append((s, mid[0], 1)), ky.append((s, mid[1], 1)), kz.append((s, math.log(1.18), 1))
        kx.append((s + 0.95, hcx, 0)), ky.append((s + 0.95, view_cy, 0)), kz.append((s + 0.95, math.log(z), 0))
        kx.append((s + 1.95, hcx, 0)), ky.append((s + 1.95, view_cy - 8 / z, 0)), kz.append((s + 1.95, math.log(z * 1.035), 0))
        prev = (hcx, hcy)
    end_s = OPEN_D + len(hero_rects) * HERO_D
    kx.append((end_s + 0.2, wall_w / 2 + 40, 1)), ky.append((end_s + 0.2, min(wall_h - 700, prev[1] + 520), 1)), kz.append((end_s + 0.2, math.log(1.05), 1))
    kx.append((total, wall_w / 2 + 40, 0)), ky.append((total, min(wall_h - 700, prev[1] + 640), 0)), kz.append((total, math.log(0.95), 0))

    def at(t):
        z = math.exp(hermite(kz, t))
        vw, vh = W / z, H / z
        cx = hermite(kx, t)
        cy = hermite(ky, t)
        cx = min(max(cx, vw / 2), wall_w - vw / 2)
        cy = min(max(cy, vh / 2), wall_h - vh / 2)
        return cx, cy, z
    return at


# =================================================================================================== overlays
INK, SLATE, TEAL = (10, 42, 74), (62, 88, 120), (0, 150, 140)
PAPER = (244, 247, 250)


def trimmed(path):
    lg = Image.open(path).convert("RGBA")
    bb = lg.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    return lg.crop(bb) if bb else lg


def fit(lg, w, h):
    sc = min(w / lg.width, h / lg.height)
    return lg.resize((max(1, round(lg.width * sc)), max(1, round(lg.height * sc))), Image.LANCZOS)


def logo_variants(width):
    """Sinor logo with transparent background: original blue (+ soft light halo for photos) and an all-white knockout."""
    lg = fit(trimmed(LOGO), width, 999)
    al = lg.getchannel("A")
    blue = lg
    halo_a = al.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(11)).point(lambda v: int(min(255, v * 0.95)))
    pad = 40
    base = Image.new("RGBA", (lg.width + 2 * pad, lg.height + 2 * pad), (0, 0, 0, 0))
    halo = Image.new("RGBA", lg.size, (255, 255, 255, 255))
    halo.putalpha(halo_a)
    base.alpha_composite(halo, (pad, pad))
    base.alpha_composite(blue, (pad, pad))
    white = Image.new("RGBA", lg.size, (255, 255, 255, 255))
    white.putalpha(al)
    wbase = Image.new("RGBA", base.size, (0, 0, 0, 0))
    wbase.alpha_composite(white, (pad, pad))
    return base, wbase, pad


def tracked(draw, xy, text, f, fill, track):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + track
    return x


def tracked_len(text, f, track):
    return sum(f.getlength(ch) + track for ch in text) - track


def scale_alpha(im, a):
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    return im


class Overlays:
    def __init__(self, heroes):
        self.heroes = heroes
        self.n = len(heroes)
        self.logo_blue, self.logo_white, self.logo_pad = logo_variants(210)
        self.f_chip = font("Inter-SemiBold", 24)
        self.f_title = font("InterDisplay-ExtraBold", 76)
        self.f_sub = font("InterDisplay-Medium", 42)
        self.f_big = font("InterDisplay-Black", 262)
        self.f_mid = font("InterDisplay-Black", 190)
        self.plogos = {}
        for _, _, _, lg in heroes:
            if lg and lg not in self.plogos:
                self.plogos[lg] = fit(trimmed(PARTNER_DIR / lg), 330, 70)
        self.closing = self.make_closing()

    # ---- frosted light caption panel for hero beat i at local time t (seconds since beat start)
    def caption(self, frame, i, t):
        if t < 0.62 or t > HERO_D + 0.05:
            return frame
        e_in = eo((t - 0.62) / 0.55)
        e_out = 1 - smooth((t - 2.05) / 0.32)
        a = min(e_in, e_out)
        if a <= 0.01:
            return frame
        x0, x1, y1 = 48, W - 48, SAFE - 36
        y0 = y1 - 300
        off = int((1 - e_in) * 34)
        box = (x0, y0 + off, x1, y1 + off)
        pw, ph = box[2] - box[0], box[3] - box[1]
        # soft drop shadow for lift
        sh = Image.new("RGBA", (pw + 120, ph + 120), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([60, 74, 60 + pw, 74 + ph], radius=40, fill=(8, 24, 48, int(95 * a)))
        sh = sh.filter(ImageFilter.GaussianBlur(22))
        frame.paste(sh, (box[0] - 60, box[1] - 60), sh)
        region = frame.crop(box).filter(ImageFilter.GaussianBlur(18))
        region = Image.blend(region, Image.new("RGB", region.size, PAPER), 0.86 * a)
        mask = rounded_mask(pw, ph, 40).point(lambda v: int(v * a))
        frame.paste(region, (box[0], box[1]), mask)
        lay = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        _, title, sub, plogo = self.heroes[i]
        chip = f"{i + 1:02d} / {self.n:02d}  ·  ADIPEC 2026"
        cw_ = tracked_len(chip, self.f_chip, 2.6)
        if plogo:
            lg = self.plogos[plogo]
            lay.alpha_composite(scale_alpha(lg, e_in), (44, 22 + (70 - lg.height) // 2))
            tracked(d, (pw - 44 - cw_, 40), chip, self.f_chip, SLATE + (int(255 * a),), 2.6)
        else:
            tracked(d, (44, 40), chip, self.f_chip, SLATE + (int(255 * a),), 2.6)
        for k, (txt, f, y, col) in enumerate(((title, self.f_title, 100, INK), (sub, self.f_sub, 190, SLATE))):
            ek = eo((t - 0.72 - 0.10 * k) / 0.5) * e_out
            if ek > 0.01:
                tmp = Image.new("RGBA", lay.size, (0, 0, 0, 0))
                ImageDraw.Draw(tmp).text((44, y + (1 - ek) * 38), txt, font=f, fill=col + (int(255 * ek),))
                lay.alpha_composite(tmp)
        d.rectangle([44, 274, 44 + 110 * e_in, 279], fill=TEAL + (int(255 * a),))
        frame.paste(lay, (box[0], box[1]), lay)
        return frame

    @staticmethod
    def open_alpha(T):
        return 0.0 if T > OPEN_D + 0.1 else 1 - smooth((T - 1.85) / 0.55)

    def top_brand(self, frame, T, total):
        a = eo(T / 0.6) * (1 - smooth((T - (total - 5.4)) / 0.5))
        if a <= 0.01:
            return frame
        oa = self.open_alpha(T)
        x, y = 48 - self.logo_pad, 92 - self.logo_pad
        for img, k in ((self.logo_white, oa), (self.logo_blue, 1 - oa)):
            if a * k > 0.01:
                lc = scale_alpha(img, a * k)
                frame.paste(lc, (x, y), lc)
        return frame

    def opening(self, frame, T):
        if T > OPEN_D + 0.1:
            return frame
        a = self.open_alpha(T)
        if a <= 0.01:
            return frame
        veil = Image.new("RGB", (W, H), NAVY)
        frame = Image.blend(frame, veil, 0.74 * a)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for k, (word, y) in enumerate((("ADIPEC", 690), ("2026", 920))):
            e = eo((T - 0.10 - 0.16 * k) / 0.55)
            if e > 0.01:
                tmp = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
                ImageDraw.Draw(tmp).text((60, 0 + (1 - e) * 120), word, font=self.f_big, fill=WHITE + (int(255 * min(1, e * 1.4)),))
                tmp = tmp.crop((0, 0, W, 300))
                lay.alpha_composite(tmp, (0, y))
        e3 = eo((T - 0.65) / 0.5)
        tracked(d, (66, 1250), "ABU DHABI   ·   2-5 NOVEMBER 2026", font("Inter-Bold", 34), (255, 255, 255, int(255 * e3)), 4.0)
        d.rectangle([66, 1215, 66 + 120 * e3, 1221], fill=(53, 214, 197, 255))
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
        frame = frame.convert("RGBA")
        frame.alpha_composite(lay)
        return frame.convert("RGB")

    def make_closing(self):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        lg = fit(trimmed(LOGO), 440, 999)
        lay.alpha_composite(lg, ((W - lg.width) // 2, 240))
        d.text((W // 2, 470), "Thank you.", font=self.f_mid, fill=INK + (255,), anchor="mt")
        d.rectangle([W // 2 - 56, 700, W // 2 + 56, 708], fill=TEAL + (255,))
        f1, f2 = font("InterDisplay-SemiBold", 42), font("InterDisplay-Medium", 40)
        d.text((W // 2, 740), "To every client and visitor", font=f1, fill=INK + (255,), anchor="mt")
        d.text((W // 2, 796), "who stopped by our stand.", font=f1, fill=INK + (255,), anchor="mt")
        d.text((W // 2, 880), "And to our technology partners", font=f2, fill=TEAL + (255,), anchor="mt")
        d.text((W // 2, 932), "for their support:", font=f2, fill=TEAL + (255,), anchor="mt")
        tw_, th_, gx = 440, 120, 24
        ys = [1010, 1210, 1410]
        for k, (name, logo) in enumerate(PARTNERS):
            r, c = divmod(k, 2)
            alone = (k == len(PARTNERS) - 1) and (len(PARTNERS) % 2 == 1)
            x = (W - tw_) // 2 if alone else (W - (2 * tw_ + gx)) // 2 + c * (tw_ + gx)
            pl = fit(trimmed(PARTNER_DIR / logo), tw_ - 60, th_ - 20)
            lay.alpha_composite(pl, (x + (tw_ - pl.width) // 2, ys[r] + (th_ - pl.height) // 2))
            d.text((x + tw_ // 2, ys[r] + th_ + 8), name, font=font("InterDisplay-SemiBold", 32), fill=SLATE + (255,), anchor="mt")
        return lay

    def closing_overlay(self, frame, T, total):
        s = total - 5.4
        if T < s:
            return frame
        a = smooth((T - s) / 0.7)
        soft = frame.filter(ImageFilter.GaussianBlur(16))
        frame = Image.blend(frame, Image.blend(soft, Image.new("RGB", (W, H), PAPER), 0.90), a)
        lay = self.closing.copy()
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
        frame = frame.convert("RGBA")
        frame.alpha_composite(lay)
        return frame.convert("RGB")


# ===================================================================================================== main
def main():
    if len(sys.argv) < 6:
        print(__doc__)
        return 2
    jpg, extra, out, ver, which = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5]
    audio = sys.argv[6] if len(sys.argv) > 6 else None
    out.mkdir(parents=True, exist_ok=True)
    heroes = HEROES[which]
    total = TOTAL[which]
    placed, hero_rects, wall_w, wall_h = build_wall(heroes, jpg, extra, seed=11 if which == "v1" else 29)
    print("wall", wall_w, "x", wall_h, "base units;", len(placed), "tiles", flush=True)
    wall = render_wall(placed, wall_w, wall_h, jpg, extra)
    print("wall rendered", wall.size, flush=True)
    cam = build_camera(hero_rects, wall_w, wall_h, total)
    ov = Overlays(heroes)
    n_frames = int(round(total * FPS))
    name = f"adipec26-thanks_linkedin_photowall_{which}_9x16_v{ver}.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if audio:
        cmd += ["-i", audio]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    cmd += ["-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
            "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(out / name)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(n_frames):
        T = fi / FPS
        cx, cy, z = cam(T)
        vw, vh = W / z, H / z
        box = ((cx - vw / 2) * S, (cy - vh / 2) * S, (cx + vw / 2) * S, (cy + vh / 2) * S)
        frame = wall.resize((W, H), Image.LANCZOS, box=box)
        bi = int((T - OPEN_D) // HERO_D) if T >= OPEN_D else -1
        if 0 <= bi < len(heroes):
            frame = ov.caption(frame, bi, T - (OPEN_D + bi * HERO_D))
        frame = ov.opening(frame, T)
        frame = ov.top_brand(frame, T, total)
        frame = ov.closing_overlay(frame, T, total)
        if fi == int(1.4 * FPS):
            frame.save(out / f"adipec26-thanks_cover_photowall_{which}_v{ver}.jpg", quality=92)
        ff.stdin.write(frame.convert("RGB").tobytes())
        if fi % 150 == 0:
            print("frame", fi, "/", n_frames, flush=True)
    ff.stdin.close()
    ff.wait()
    print("wrote", out / name, "frames", n_frames, "duration", total, "s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
