#!/usr/bin/env python3
"""ADIPEC 2026 thank-you video, "photo mosaic" design (v11), for LinkedIn.

Design basis: Rahul's reference (a Pinterest pin showing a corporate 'clean design' After Effects template
preview). What is taken from it is the STYLE only: light grey vignette background, one full-colour hero photo in a
thin white keyline frame, scattered blue duotone crops of the other photos drifting at different speeds around it
(parallax), big white type fragments, small dark square accents, thin technical lines, quick whip entries and exits.
Everything is drawn from scratch here with the event's own photos; no template assets are used.

Usage: python3 build_video_mosaic.py <jpg_dir> <extra_dir> <out_dir> <version> [4x5|9x16]
  jpg_dir   : oriented JPG copies of the Drive photos (not in the repo)
  extra_dir : photos cropped out of the sheets Rahul sent in chat (not in the repo)
  out_dir   : MP4 and cover are written here (not in the repo)
Needs Pillow, numpy, ffmpeg (libx264/aac), Inter fonts. No music: a silent AAC track is added.
All motion is rendered per frame with sub-pixel sampling (no ffmpeg zoompan), then piped to ffmpeg.
"""
import math
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ASPECT = sys.argv[5] if len(sys.argv) > 5 else "4x5"
W, H = (1080, 1350) if ASPECT == "4x5" else (1080, 1920)
SAFE = H - (150 if ASPECT == "4x5" else 300)
FPS = 25
NAVY, BLUE, LIGHT, WHITE = (10, 42, 74), (13, 74, 133), (196, 218, 240), (255, 255, 255)
FONT_DIR = "/usr/share/fonts/opentype/inter/"
REPO = Path(__file__).resolve().parents[3]
LOGO = REPO / "assets/brand/sinor-logo.png"
PARTNER_DIR = REPO / "assets/brand/partners"

EVENT_LINE = "ADIPEC 2026  ·  ABU DHABI"
DATE_LINE = "2-5 November 2026"
PARTNERS = [("Sonardyne", "sonardyne.png"), ("Fugro", "fugro.png"), ("Navis Engineering", "navis-engineering.png"),
            ("Marine Technologies", "marine-technologies-mt.png"), ("Guidance Marine", "guidance-marine.png")]

# Beats in order. src is looked up in jpg_dir first, then extra_dir.
BEATS = [
    dict(kind="hero", src="s8_2.jpg", cap="The Sinor Marine team at ADIPEC 2026", logo=True),
    dict(kind="title"),
    dict(kind="hero", src="s7_1.jpg", cap="Conversations at our stand"),
    dict(kind="hero", src="s3_1.jpg", cap="Visitors at our stand"),
    dict(kind="hero", src="IMG_4413.jpg", cap="NAVIS console"),
    dict(kind="hero", src="IMG_4464.jpg", cap="Discussions at the Sonardyne display"),
    dict(kind="hero", src="IMG_4188.jpg", cap="Marine Technologies on the stand"),
    dict(kind="hero", src="a07555b5-23b3-4497-92aa-a3613e384bc5.jpg", cap="Guidance Marine at our stand"),
    dict(kind="hero", src="s2_2.jpg", cap="The team at our stand"),
    dict(kind="end"),
]
HERO_D, TITLE_D, END_D = 3.0, 2.9, 6.4
ENTRY, EXIT, OVERLAP = 0.55, 0.42, 0.30
# ----------------------------------------------------------------------------------------------------------


def font(weight, size):
    return ImageFont.truetype(f"{FONT_DIR}Inter-{weight}.otf", int(size))


def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = min(max(x, 0.0), 1.0)
    return x ** 3


def find(name, jpg, extra):
    for d in (jpg, extra):
        if (d / name).exists():
            return d / name
    raise FileNotFoundError(name)


# ---------- static assets ---------------------------------------------------------------------------------
def make_bg():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.46) / (H * 0.62)) ** 2)
    t = np.clip(r, 0, 1.15) ** 1.6
    centre, edge = np.array([208, 211, 217], np.float32), np.array([146, 151, 162], np.float32)
    arr = centre[None, None, :] * (1 - t[..., None]) + edge[None, None, :] * t[..., None]
    img = Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for x in (int(W * 0.09), int(W * 0.91)):  # thin technical lines with ticks
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 70), width=1)
        for y in range(40, H, 90):
            d.line([(x - 6, y), (x + 6, y)], fill=(255, 255, 255, 110), width=1)
    for y in (int(H * 0.075), int(H * 0.88)):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 70), width=1)
    f = font("Medium", 15)
    d.text((int(W * 0.09) + 12, int(H * 0.075) + 8), "ADIPEC 2026  /  ABU DHABI  /  02-05 NOV", font=f, fill=(255, 255, 255, 150))
    for k in range(3):  # tiny text-block bars like the reference
        d.rectangle([int(W * 0.82), int(H * 0.91) + k * 9, int(W * 0.82) + 120 - k * 30, int(H * 0.91) + k * 9 + 3], fill=(255, 255, 255, 120))
    return Image.alpha_composite(img, ov).convert("RGB")


def duotone(im, gain):
    g = np.asarray(im.convert("L"), np.float32) / 255.0
    g = np.clip((g - 0.5) * 1.25 + 0.5, 0, 1) * gain
    g = np.clip(g, 0, 1)[..., None]
    dark, mid, light = np.array([6, 20, 52], np.float32), np.array([28, 84, 180], np.float32), np.array([176, 208, 246], np.float32)
    lo = dark + (mid - dark) * (g * 2).clip(0, 1)
    hi = mid + (light - mid) * ((g - 0.5) * 2).clip(0, 1)
    arr = np.where(g < 0.5, lo, hi)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def make_tile(rng, pool, w, h, gain):
    src = Image.open(rng.choice(pool)).convert("RGB")
    s = rng.uniform(0.48, 0.90)  # wide crops: no tight, upscaled face close-ups
    cw, ch = src.width * s, src.width * s * h / w
    if ch > src.height:
        ch = src.height * s
        cw = ch * w / h
    cx = rng.uniform(cw / 2, src.width - cw / 2)
    cy = rng.uniform(ch / 2, src.height - ch / 2)
    crop = src.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((w, h), Image.LANCZOS)
    t = duotone(crop, gain).convert("RGBA")
    return t


def shifted(tile_rgba, fx, fy, alpha):
    """Sub-pixel shifted copy (w+2, h+2) with soft edges; alpha scales opacity."""
    w, h = tile_rgba.size
    out = tile_rgba.transform((w + 2, h + 2), Image.AFFINE, (1, 0, -(1 + fx), 0, 1, -(1 + fy)), resample=Image.BICUBIC)
    if alpha < 1:
        a = out.getchannel("A").point(lambda v: int(v * alpha))
        out.putalpha(a)
    return out


class Beat:
    def __init__(self, idx, spec, start, dur, jpg, extra, pool, bg_words):
        self.i, self.spec, self.start, self.dur = idx, spec, start, dur
        self.kind = spec["kind"]
        rng = random.Random(1000 + idx * 17)
        self.tiles = []
        if True:
            n = 11 if ASPECT == "4x5" else 14
            for k in range(n):
                size = rng.choice([(170, 130), (240, 190), (300, 230), (380, 290), (460, 350), (210, 280), (260, 340)])
                w, h = int(size[0] * (1.0 if ASPECT == "4x5" else 1.05)), int(size[1] * (1.0 if ASPECT == "4x5" else 1.05))
                tile = make_tile(rng, pool, w, h, rng.uniform(0.75, 1.15))
                depth = (w * h) ** 0.5 / 300.0
                self.tiles.append(dict(
                    img=tile, cx=rng.uniform(-0.02 * W, 1.02 * W), cy=rng.uniform(0.02 * H, 0.96 * H),
                    vx=rng.uniform(-14, 14) * (0.6 + depth * 0.5), vy=rng.uniform(-9, 9) * (0.6 + depth * 0.5),
                    ex=rng.choice([-1, 1]) * rng.uniform(0.35, 0.8) * W * (0.6 + depth * 0.4),
                    ey=rng.uniform(-0.12, 0.12) * H, depth=depth, alpha=rng.uniform(0.72, 0.95)))
            self.tiles.sort(key=lambda t: t["depth"])
            self.squares = [dict(x=rng.randint(60, W - 80), y=rng.randint(60, int(H * 0.9)), s=rng.choice([20, 26, 34, 42]),
                                 ex=rng.choice([-1, 1]) * rng.uniform(0.3, 0.7) * W) for _ in range(6)]
            wa, wb = rng.choice([("ADIPEC", "2026"), ("2026", "ADIPEC"), ("THANK", "YOU")]) if self.kind != "title" else ("ADIPEC", "2026")
            self.words = [(wa, rng.choice([(0.04, 0.06), (0.50, 0.04)])), (wb, rng.choice([(0.52, 0.86), (0.06, 0.84)]))]
        if self.kind == "hero":
            im = Image.open(find(spec["src"], jpg, extra)).convert("RGB")
            a = im.width / im.height
            max_w, max_h = (0.90 * W, 0.58 * H) if ASPECT == "4x5" else (0.90 * W, 0.42 * H)
            if a >= max_w / max_h:
                self.hw, self.hh = int(max_w), int(max_w / a)
            else:
                self.hh, self.hw = int(max_h), int(max_h * a)
            self.src = im.resize((self.hw, self.hh), Image.LANCZOS)
            self.cx, self.cy = W / 2, (0.455 * H if ASPECT == "4x5" else 0.47 * H)
            self.shadow = Image.new("RGBA", (self.hw + 160, self.hh + 160), (0, 0, 0, 0))
            ImageDraw.Draw(self.shadow).rectangle([80, 90, 80 + self.hw, 90 + self.hh], fill=(10, 20, 40, 120))
            self.shadow = self.shadow.filter(ImageFilter.GaussianBlur(26))
            self.plate = self.make_plate(spec["cap"])
        elif self.kind == "title":
            self.hw, self.hh = int(0.86 * W), int(0.50 * H if ASPECT == "4x5" else 0.34 * H)
            self.cx, self.cy = W / 2, (0.44 * H if ASPECT == "4x5" else 0.46 * H)
            self.src = self.make_title_plate()
            self.shadow = Image.new("RGBA", (self.hw + 160, self.hh + 160), (0, 0, 0, 0))
            ImageDraw.Draw(self.shadow).rectangle([80, 90, 80 + self.hw, 90 + self.hh], fill=(10, 20, 40, 130))
            self.shadow = self.shadow.filter(ImageFilter.GaussianBlur(26))
            self.plate = None
        else:
            card = make_end_card()
            sc = 0.86 if ASPECT == "4x5" else (SAFE - 80) / H
            self.src = card.resize((int(W * sc), int(H * sc)), Image.LANCZOS)
            self.hw, self.hh = self.src.size
            self.cx, self.cy = W / 2, (0.43 * H if ASPECT == "4x5" else (SAFE - 30) / 2)
            self.shadow = Image.new("RGBA", (self.hw + 160, self.hh + 160), (0, 0, 0, 0))
            ImageDraw.Draw(self.shadow).rectangle([80, 90, 80 + self.hw, 90 + self.hh], fill=(10, 20, 40, 140))
            self.shadow = self.shadow.filter(ImageFilter.GaussianBlur(26))
            self.plate = None

    def make_plate(self, cap):
        f1, f2 = font("SemiBold", 21), font("Bold", 42)
        tmp = ImageDraw.Draw(Image.new("RGB", (4, 4)))
        w = int(max(tmp.textlength(cap, font=f2), 260) + 64)
        h = 104
        p = Image.new("RGBA", (w, h), NAVY + (240,))
        d = ImageDraw.Draw(p)
        d.rectangle([0, 0, 8, h], fill=LIGHT + (255,))
        d.text((30, 14), "ADIPEC 2026", font=f1, fill=LIGHT + (255,))
        d.text((30, 44), cap, font=f2, fill=WHITE + (255,))
        return p

    def make_title_plate(self):
        p = Image.new("RGB", (self.hw, self.hh), NAVY)
        d = ImageDraw.Draw(p)
        for y in range(self.hh):
            c = tuple(int(NAVY[i] + (BLUE[i] - NAVY[i]) * (y / self.hh) * 0.9) for i in range(3))
            d.line([(0, y), (self.hw, y)], fill=c)
        rgba = p.convert("RGBA")
        lg = Image.open(LOGO).convert("RGB")
        lw = 300
        lg = lg.resize((lw, round(lg.height * lw / lg.width)), Image.LANCZOS)
        card = Image.new("RGBA", (lg.width + 36, lg.height + 36), (255, 255, 255, 255))
        card.paste(lg, (18, 18))
        m = Image.new("L", card.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width, card.height], radius=20, fill=255)
        card.putalpha(m)
        rgba.alpha_composite(card, ((self.hw - card.width) // 2, 36))
        d = ImageDraw.Draw(rgba)
        cx = self.hw // 2
        top = 36 + card.height + 22
        d.text((cx, top), "Thank you.", font=font("ExtraBold", 150), fill=WHITE + (255,), anchor="mt")
        d.text((cx, top + 190), EVENT_LINE, font=font("SemiBold", 42), fill=WHITE + (255,), anchor="mt")
        d.text((cx, top + 248), DATE_LINE, font=font("Medium", 38), fill=LIGHT + (255,), anchor="mt")
        return rgba.convert("RGB")


def partner_tile(logo_file, tw, th):
    lg = Image.open(PARTNER_DIR / logo_file).convert("RGBA")
    bbox = lg.getchannel("A").getbbox()
    if bbox:
        lg = lg.crop(bbox)
    sc = min((tw - 44) / lg.width, (th - 26) / lg.height)
    lg = lg.resize((max(1, round(lg.width * sc)), max(1, round(lg.height * sc))), Image.LANCZOS)
    tile = Image.new("RGBA", (tw, th), (255, 255, 255, 255))
    tile.alpha_composite(lg, ((tw - lg.width) // 2, (th - lg.height) // 2))
    m = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, tw, th], radius=18, fill=255)
    tile.putalpha(m)
    return tile


def make_end_card():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(H):
        c = tuple(int(NAVY[i] + (BLUE[i] - NAVY[i]) * (y / H) * 0.9) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    tw, th, gx, pitch = 470, 124, 20, 184
    rows = (len(PARTNERS) + 1) // 2
    block = 600 + (rows - 1) * pitch + th + 42
    o = (SAFE - block) // 2 - 6
    img = img.convert("RGBA")
    lg = Image.open(LOGO).convert("RGB")
    lg = lg.resize((420, round(lg.height * 420 / lg.width)), Image.LANCZOS)
    card = Image.new("RGBA", (lg.width + 36, lg.height + 36), (255, 255, 255, 255))
    card.paste(lg, (18, 18))
    m = Image.new("L", card.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width, card.height], radius=22, fill=255)
    card.putalpha(m)
    img.alpha_composite(card, ((W - card.width) // 2, 60 + o))
    d = ImageDraw.Draw(img)
    cx = W // 2
    d.text((cx, 290 + o), "Thank you", font=font("ExtraBold", 112), fill=WHITE + (255,), anchor="mt")
    d.rectangle([cx - 48, 428 + o, cx + 48, 436 + o], fill=LIGHT + (255,))
    d.text((cx, 462 + o), "To every client and visitor who stopped by our stand.", font=font("SemiBold", 36), fill=WHITE + (255,), anchor="mt")
    d.text((cx, 530 + o), "And to our technology partners for their support:", font=font("Medium", 35), fill=LIGHT + (255,), anchor="mt")
    y0 = 600 + o
    for k, (name, logo) in enumerate(PARTNERS):
        r, c = divmod(k, 2)
        alone = (k == len(PARTNERS) - 1) and (len(PARTNERS) % 2 == 1)
        x = (W - tw) // 2 if alone else (W - (2 * tw + gx)) // 2 + c * (tw + gx)
        y = y0 + r * pitch
        img.alpha_composite(partner_tile(logo, tw, th), (x, y))
        d.text((x + tw // 2, y + th + 8), name, font=font("SemiBold", 32), fill=WHITE + (255,), anchor="mt")
    return img.convert("RGB")


# ---------- per-frame drawing ---------------------------------------------------------------------------------
def draw_beat(canvas, b, t, words_cache):
    d_in = ease_out(t / ENTRY)
    x_out = max(0.0, (t - (b.dur - EXIT)) / EXIT)
    d_out = 0.0 if b.kind == "end" else ease_in(x_out)
    # big white type fragments (behind everything)
    for k, (word, (fx, fy)) in enumerate(b.words):
        key = (word, k)
        if key not in words_cache:
            f = font("ExtraBold", 250 if ASPECT == "4x5" else 270)
            w = int(ImageDraw.Draw(Image.new("RGB", (4, 4))).textlength(word, font=f)) + 20
            layer = Image.new("RGBA", (w, 300), (0, 0, 0, 0))
            ImageDraw.Draw(layer).text((10, 0), word, font=f, fill=(255, 255, 255, 235))
            words_cache[key] = layer
        layer = words_cache[key]
        px = fx * W + (1 - d_in) * W * 0.25 * (1 if k == 0 else -1) - d_out * W * 0.3 * (1 if k == 0 else -1)
        canvas.paste(layer, (int(px), int(fy * H)), layer)
    # drifting duotone tiles (parallax)
    for tl in b.tiles:
        w, h = tl["img"].size
        px = tl["cx"] + tl["vx"] * t - w / 2 + (1 - d_in) * tl["ex"] - d_out * tl["ex"] * 0.9
        py = tl["cy"] + tl["vy"] * t - h / 2 + (1 - d_in) * tl["ey"]
        ix, iy = math.floor(px), math.floor(py)
        if ix > W or iy > H or ix + w < -2 or iy + h < -2:
            continue
        al = tl["alpha"] * (1 - 0.6 * d_out)
        tile = shifted(tl["img"], px - ix, py - iy, al)
        canvas.paste(tile, (ix - 1, iy - 1), tile)
    dr = ImageDraw.Draw(canvas)
    for sq in b.squares:
        x = sq["x"] + (1 - d_in) * sq["ex"] - d_out * sq["ex"]
        dr.rectangle([int(x), sq["y"], int(x) + sq["s"], sq["y"] + sq["s"]], fill=(14, 22, 40))
    # hero or title plate
    side = 1 if (b.i % 2 == 0) else -1
    ox = (1 - d_in) * W * 0.34 * side - d_out * W * 0.34 * side
    a = min(1.0, d_in * 1.7) * (1 - d_out)
    if a <= 0.01:
        return
    z = 1.0 if b.kind == "end" else 1.0 + 0.065 * min(1.0, t / b.dur)
    if b.kind == "hero":
        hero = b.src.transform((b.hw, b.hh), Image.AFFINE,
                               (1 / z, 0, b.hw / 2 - b.hw / (2 * z), 0, 1 / z, b.hh / 2 - b.hh / (2 * z)), resample=Image.BICUBIC)
    else:
        hero = b.src.transform((b.hw, b.hh), Image.AFFINE,
                               (1 / z, 0, b.hw / 2 - b.hw / (2 * z), 0, 1 / z, b.hh / 2 - b.hh / (2 * z)), resample=Image.BICUBIC)
    hx, hy = int(round(b.cx - b.hw / 2 + ox)), int(round(b.cy - b.hh / 2))
    sh = b.shadow.copy()
    sh.putalpha(sh.getchannel("A").point(lambda v: int(v * a)))
    canvas.paste(sh, (hx - 80, hy - 80), sh)
    hero = hero.convert("RGBA")
    hero.putalpha(int(255 * a))
    dr = ImageDraw.Draw(canvas)
    kc = (255, 255, 255)
    dr.rectangle([hx - 12, hy - 12, hx + b.hw + 12, hy + b.hh + 12], outline=kc, width=3)
    canvas.paste(hero, (hx, hy), hero)
    if b.plate is not None:
        p = b.plate.copy()
        p.putalpha(p.getchannel("A").point(lambda v: int(v * a)))
        canvas.paste(p, (hx - 24, hy + b.hh + 4), p)
    if b.spec.get("logo"):
        lg = Image.open(LOGO).convert("RGB")
        lg = lg.resize((230, round(lg.height * 230 / lg.width)), Image.LANCZOS)
        card = Image.new("RGBA", (lg.width + 28, lg.height + 28), (255, 255, 255, int(255 * a)))
        card.paste(lg, (14, 14))
        m = Image.new("L", card.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width, card.height], radius=16, fill=int(255 * a))
        canvas.paste(card, (hx - 12, max(hy - 12 - card.height - 14, 18)), m)


def main():
    if len(sys.argv) < 5:
        print(__doc__)
        return 2
    jpg, extra, out, ver = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
    out.mkdir(parents=True, exist_ok=True)
    pool = sorted(list(jpg.glob("*.jpg")) + list(extra.glob("*.jpg")))
    bg = make_bg()
    beats, t0 = [], -0.30  # start 0.3 s into the first entry so frame 1 already shows the team photo
    for i, spec in enumerate(BEATS):
        dur = {"hero": HERO_D, "title": TITLE_D, "end": END_D}[spec["kind"]]
        beats.append(Beat(i, spec, t0, dur, jpg, extra, pool, None))
        t0 += dur - OVERLAP
    total = beats[-1].start + beats[-1].dur
    n_frames = int(round(total * FPS))
    name = f"adipec26-thanks_linkedin_mosaic_{ASPECT}_v{ver}.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000", "-t", f"{total:.3f}",
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(out / name)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    words_cache = {}
    cover_t = beats[0].start + 1.45
    for fi in range(n_frames):
        T = fi / FPS
        canvas = bg.copy()
        for b in beats:
            if b.start <= T < b.start + b.dur:
                draw_beat(canvas, b, T - b.start, words_cache)
        if fi == int(cover_t * FPS):
            canvas.save(out / f"adipec26-thanks_cover_mosaic_{ASPECT}_v{ver}.jpg", quality=90)
        ff.stdin.write(canvas.tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", out / name, "frames", n_frames, "duration", round(total, 2), "s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
