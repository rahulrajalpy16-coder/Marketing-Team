#!/usr/bin/env python3
"""Rebuild the ADIPEC 2026 thank-you video (LinkedIn 4:5) from the working copies of the photos.

Usage:  python3 build_video.py <jpg_dir> <out_dir> [version]
  jpg_dir : folder with the auto-oriented JPG copies of the Drive originals (NOT in the repo)
  out_dir : where slides, the MP4 and the cover are written (NOT in the repo)
Needs: Pillow, ffmpeg with libx264/aac, Inter fonts at /usr/share/fonts/opentype/inter.
Originals are never touched. The logo is assets/brand/sinor-logo.png (official, supplied).
No music: a silent AAC track is added so players treat the file normally.
"""
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1350, 25
NAVY, BLUE, STEEL = (10, 42, 74), (13, 74, 133), (122, 168, 204)
FONT_DIR = "/usr/share/fonts/opentype/inter/"
LOGO = Path(__file__).resolve().parents[3] / "assets/brand/sinor-logo.png"

# ---- content (edit here, then rebuild) -------------------------------------------------------
EVENT_LINE = "ADIPEC 2026  ·  ABU DHABI"
DATE_LINE = "2-5 November 2026"
PARTNERS = ["Sonardyne", "Fugro", "NAVIS", "Marine Technologies"]
# (file, mode, duration_s, caption or None)  mode: cover | fit | auto
SLIDES = [
    ("0f44943b-22e6-4381-aac3-66a9dfc31218.jpg", "cover", 4.5, "TITLE"),
    ("0bc7989f-ffd8-4930-b538-267cc2414e4e.jpg", "fit", 3.8, "DP console on the stand"),
    ("0CDC96B1-3817-4C16-B71D-B9108ECD8AD4.jpg", "fit", 3.8, "Conversations at the stand"),
    ("cf677e0a-bf65-4e06-8a7a-9a40f904137c.jpg", "cover", 3.8, "At the stand"),
    ("a07555b5-23b3-4497-92aa-a3613e384bc5.jpg", "fit", 3.8, "Thank you for stopping by"),
]
END_DUR, XFADE = 6.0, 0.5
# The supplied collage stacks two photos with a white seam near row 714 to 725; use only the sharp top photo.
CROPS = {"0CDC96B1-3817-4C16-B71D-B9108ECD8AD4.jpg": (0, 0, 1206, 710)}
LIGHT = (196, 218, 240)  # small text on dark backgrounds (higher contrast than STEEL)
# ------------------------------------------------------------------------------------------------


def font(weight, size):
    return ImageFont.truetype(f"{FONT_DIR}Inter-{weight}.otf", size)


def cover(im, crop_top=0.5):
    """Scale to fill WxH. crop_top = share of the excess height removed from the top (0.5 = centred)."""
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = round((im.height - H) * crop_top)
    y = min(max(y, 0), im.height - H)
    return im.crop((x, y, x + W, y + H))


def fit_blur(im):
    bg = cover(im).filter(ImageFilter.GaussianBlur(38))
    bg = Image.blend(bg, Image.new("RGB", (W, H), NAVY), 0.45)
    s = W / im.width
    fg = im.resize((W, round(im.height * s)), Image.LANCZOS)
    bg.paste(fg, (0, (H - fg.height) // 2))
    return bg


def bottom_gradient(img, start, strength=235):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(start, H):
        a = int(strength * ((y - start) / (H - start)) ** 1.4)
        d.line([(0, y), (W, y)], fill=NAVY + (a,))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


def pill(img, text, xy, size=26):
    d = ImageDraw.Draw(img, "RGBA")
    f = font("SemiBold", size)
    tw = d.textlength(text, font=f)
    x, y = xy
    d.rounded_rectangle([x, y, x + tw + 36, y + size + 24], radius=(size + 24) // 2, fill=NAVY + (215,))
    d.text((x + 18, y + 11), text, font=f, fill=(255, 255, 255))


def logo_card(img, width, xy):
    lg = Image.open(LOGO).convert("RGB")
    s = width / lg.width
    lg = lg.resize((width, round(lg.height * s)), Image.LANCZOS)
    pad = 18
    card = Image.new("RGB", (lg.width + 2 * pad, lg.height + 2 * pad), (255, 255, 255))
    card.paste(lg, (pad, pad))
    mask = Image.new("L", card.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, card.width, card.height], radius=22, fill=255)
    img.paste(card, xy, mask)
    return card.size


def slide_photo(path, mode, caption, idx):
    im = Image.open(path).convert("RGB")
    if Path(path).name in CROPS:
        im = im.crop(CROPS[Path(path).name])
    img = fit_blur(im) if mode == "fit" else cover(im, crop_top=0.78)
    if caption == "TITLE":
        img = bottom_gradient(img, 760, 245)
        d = ImageDraw.Draw(img)
        d.rectangle([64, 978, 64 + 96, 978 + 8], fill=LIGHT)
        d.text((64, 1008), "Thank you.", font=font("ExtraBold", 132), fill=(255, 255, 255))
        d.text((64, 1164), EVENT_LINE, font=font("SemiBold", 42), fill=(255, 255, 255))
        d.text((64, 1220), DATE_LINE, font=font("Medium", 40), fill=LIGHT)
        logo_card(img, 250, (48, 48))
    else:
        img = bottom_gradient(img, 1000, 230)
        d = ImageDraw.Draw(img)
        d.rectangle([64, 1186, 64 + 72, 1186 + 7], fill=LIGHT)
        d.text((64, 1208), caption, font=font("SemiBold", 48), fill=(255, 255, 255))
    return img


def slide_end():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(H):  # navy to brand blue
        t = y / H
        c = tuple(int(NAVY[i] + (BLUE[i] - NAVY[i]) * t * 0.9) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    cw, ch = logo_card(img, 560, ((W - 596) // 2, 110))
    d.text((W // 2, 430), "Thank you", font=font("ExtraBold", 120), fill=(255, 255, 255), anchor="mt")
    d.rectangle([W // 2 - 48, 590, W // 2 + 48, 598], fill=STEEL)
    d.text((W // 2, 640), "To every client and visitor", font=font("SemiBold", 44), fill=(255, 255, 255), anchor="mt")
    d.text((W // 2, 698), "who stopped by our stand.", font=font("SemiBold", 44), fill=(255, 255, 255), anchor="mt")
    d.text((W // 2, 800), "And to our technology partners", font=font("Medium", 40), fill=LIGHT, anchor="mt")
    d.text((W // 2, 850), "for their support:", font=font("Medium", 40), fill=LIGHT, anchor="mt")
    y = 935
    for p in PARTNERS:
        d.text((W // 2, y), p, font=font("Bold", 52), fill=(255, 255, 255), anchor="mt")
        y += 76
    d.text((W // 2, 1236), "Sinor Marine Services Middle East FZCO", font=font("Medium", 34), fill=LIGHT, anchor="mt")
    return img


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    jpg, out = Path(sys.argv[1]), Path(sys.argv[2])
    ver = sys.argv[3] if len(sys.argv) > 3 else "1"
    out.mkdir(parents=True, exist_ok=True)
    pngs, durs = [], []
    for i, (f, mode, dur, cap) in enumerate(SLIDES):
        p = out / f"slide_{i:02d}.png"
        slide_photo(jpg / f, mode, cap, i).save(p)
        pngs.append(p)
        durs.append(dur)
    p = out / f"slide_{len(SLIDES):02d}.png"
    slide_end().save(p)
    pngs.append(p)
    durs.append(END_DUR)

    cmd = ["ffmpeg", "-v", "error", "-y"]
    for p, d in zip(pngs, durs):
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d + XFADE:.3f}", "-i", str(p)]
    cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    n = len(pngs)
    parts = [f"[{i}:v]fps={FPS},format=yuv420p,setsar=1[v{i}]" for i in range(n)]
    last, t = "v0", durs[0]
    for i in range(1, n):
        parts.append(f"[{last}][v{i}]xfade=transition=fade:duration={XFADE}:offset={t - 0 :.3f}[x{i}]")
        last = f"x{i}"
        t += durs[i]
    total = sum(durs)
    name = f"adipec26-thanks_linkedin_4x5_v{ver}.mp4"
    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{last}]", "-map", f"{n}:a",
            "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
            "-profile:v", "high", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", str(out / name)]
    subprocess.run(cmd, check=True)
    Image.open(pngs[0]).convert("RGB").save(out / f"adipec26-thanks_cover_4x5_v{ver}.jpg", quality=90)
    print("wrote", out / name, "expected duration", round(total, 2), "s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
