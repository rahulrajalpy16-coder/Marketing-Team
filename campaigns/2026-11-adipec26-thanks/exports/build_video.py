#!/usr/bin/env python3
"""Rebuild the ADIPEC 2026 thank-you video for LinkedIn (4:5, 1080x1350, 30 fps) from the working copies of the photos.

Usage:  python3 build_video.py <jpg_dir> <out_dir> [version]
  jpg_dir : folder with the JPG working copies (NOT in the repo); file names are listed in SLIDES below
  out_dir : where overlays, the MP4, cover and SRT are written (NOT in the repo)
Needs: Pillow, ffmpeg with libx264/aac, Inter fonts at /usr/share/fonts/opentype/inter.
Originals are never touched. The logo is assets/brand/sinor-logo.png (official Sinor Marine Services logo, supplied).
No music: a silent AAC track is added so players treat the file normally.

v4 (2026-11-07): longer "Our visitors" section with slow pans across the wide photos, 30 fps (LinkedIn accepts 10 to 60,
see brain/platform-specs.md), key text kept inside the safe area (nothing in the bottom 150 px, 64 px side margins),
a cover image for the LinkedIn thumbnail upload and an SRT of the on-screen captions.
"""
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1350, 30
NAVY, BLUE, STEEL = (10, 42, 74), (13, 74, 133), (122, 168, 204)
LIGHT = (196, 218, 240)  # small text on dark backgrounds
FONT_DIR = "/usr/share/fonts/opentype/inter/"
LOGO = Path(__file__).resolve().parents[3] / "assets/brand/sinor-logo.png"

# ---- content (edit here, then rebuild) -------------------------------------------------------
EVENT_LINE = "ADIPEC 2026  ·  ABU DHABI"
DATE_LINE = "2-5 November 2026"
PARTNERS = ["Sonardyne", "Fugro", "NAVIS", "Marine Technologies"]  # still unconfirmed by Rahul
XFADE, END_DUR = 0.4, 6.0
# kind: cover (fill, crop_top) | box (crop box in source px, any ratio then fitted onto blurred bg) | pan (full height, slides sideways)
# pan = (start, end) as fractions 0..1 of the available sideways travel
# visitors=True adds the small OUR VISITORS label
SLIDES = [
    dict(f="0f44943b-22e6-4381-aac3-66a9dfc31218.jpg", kind="cover", dur=4.0, cap="TITLE"),
    dict(f="u7.jpg", kind="pan", pan=(0.0, 0.80), dur=3.4, cap="Welcome to the stand", visitors=True),
    dict(f="u1.jpg", kind="pan", pan=(0.15, 0.60), dur=3.4, cap="Hands-on with the DP console", visitors=True),
    dict(f="u5.jpg", kind="pan", pan=(0.30, 0.90), dur=3.4, cap="Questions at the console", visitors=True),
    dict(f="u8.jpg", kind="pan", pan=(0.30, 1.0), dur=3.4, cap="Technical discussions", visitors=True),
    dict(f="u3.jpg", kind="pan", pan=(0.95, 0.0), dur=3.4, cap="Face to face", visitors=True),
    dict(f="u4.jpg", kind="pan", pan=(0.0, 0.85), dur=3.4, cap="Sharing experience", visitors=True),
    dict(f="u6.jpg", kind="cover", crop=(520, 0, 1480, 1200), dur=3.2, cap="DP console on the stand"),
    # the supplied collage stacks two photos with a seam at rows 713 to 714; use only the sharp top photo
    dict(f="u2.jpg", kind="box", crop=(0, 10, 1205, 708), dur=3.2, cap="Conversations at the stand", visitors=True),
    dict(f="a07555b5-23b3-4497-92aa-a3613e384bc5.jpg", kind="box", crop=None, dur=3.2, cap="Thank you for stopping by"),
]
# cf677e0a (two men at the stand) stays out: a media file name is readable on the stand TV behind them.
# ------------------------------------------------------------------------------------------------


def font(weight, size):
    return ImageFont.truetype(f"{FONT_DIR}Inter-{weight}.otf", size)


def cover(im, crop_top=0.5):
    """Scale to fill WxH. crop_top = share of the excess height removed from the top (0.5 = centred)."""
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = min(max(round((im.height - H) * crop_top), 0), im.height - H)
    return im.crop((x, y, x + W, y + H))


def fit_blur(im):
    bg = cover(im).filter(ImageFilter.GaussianBlur(38))
    bg = Image.blend(bg, Image.new("RGB", (W, H), NAVY), 0.45)
    s = W / im.width
    fg = im.resize((W, round(im.height * s)), Image.LANCZOS)
    bg.paste(fg, (0, (H - fg.height) // 2))
    return bg


def gradient_overlay(start, strength):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(start, H):
        a = int(strength * ((y - start) / (H - start)) ** 1.4)
        d.line([(0, y), (W, y)], fill=NAVY + (a,))
    return ov


def label_pill(ov, text, xy, size=24):
    d = ImageDraw.Draw(ov, "RGBA")
    f = font("SemiBold", size)
    tw = d.textlength(text, font=f)
    x, y = xy
    d.rounded_rectangle([x, y, x + tw + 34, y + size + 22], radius=(size + 22) // 2, fill=NAVY + (215,))
    d.text((x + 17, y + 10), text, font=f, fill=(255, 255, 255))


def logo_card(ov, width, xy):
    lg = Image.open(LOGO).convert("RGB")
    lg = lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)
    pad = 18
    card = Image.new("RGB", (lg.width + 2 * pad, lg.height + 2 * pad), (255, 255, 255))
    card.paste(lg, (pad, pad))
    mask = Image.new("L", card.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, card.width, card.height], radius=22, fill=255)
    ov.paste(card.convert("RGBA"), xy, mask)
    return card.size


def base_and_overlay(s, jpg):
    """Return (base PIL image, overlay RGBA 1080x1350). Pan slides have a wider base that ffmpeg slides across."""
    im = Image.open(jpg / s["f"]).convert("RGB")
    kind = s["kind"]
    if kind == "pan":
        k = H / im.height
        base = im.resize((round(im.width * k), H), Image.LANCZOS)
        ov = gradient_overlay(930, 230)
    elif kind == "cover":
        crop = s.get("crop")
        if crop:
            im = im.crop(crop)
        base = cover(im, 0.78)
        ov = gradient_overlay(700, 245) if s["cap"] == "TITLE" else gradient_overlay(930, 230)
    else:  # box
        if s.get("crop"):
            im = im.crop(s["crop"])
        base = fit_blur(im)
        ov = gradient_overlay(930, 230)
    d = ImageDraw.Draw(ov)
    if s["cap"] == "TITLE":
        d.rectangle([64, 880, 64 + 96, 880 + 8], fill=LIGHT)
        d.text((64, 910), "Thank you.", font=font("ExtraBold", 132), fill=(255, 255, 255))
        d.text((64, 1066), EVENT_LINE, font=font("SemiBold", 42), fill=(255, 255, 255))
        d.text((64, 1122), DATE_LINE, font=font("Medium", 40), fill=LIGHT)
        logo_card(ov, 250, (48, 48))
    else:
        d.rectangle([64, 1096, 64 + 72, 1096 + 7], fill=LIGHT)
        d.text((64, 1118), s["cap"], font=font("SemiBold", 48), fill=(255, 255, 255))
        if s.get("visitors"):
            label_pill(ov, "OUR VISITORS", (64, 64))
    return base, ov


def slide_end():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(H):  # navy to brand blue
        c = tuple(int(NAVY[i] + (BLUE[i] - NAVY[i]) * (y / H) * 0.9) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    logo_card(ov, 560, ((W - 596) // 2, 80))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((W // 2, 360), "Thank you", font=font("ExtraBold", 120), fill=(255, 255, 255), anchor="mt")
    d.rectangle([W // 2 - 48, 515, W // 2 + 48, 523], fill=STEEL)
    d.text((W // 2, 560), "To every client and visitor", font=font("SemiBold", 44), fill=(255, 255, 255), anchor="mt")
    d.text((W // 2, 618), "who stopped by our stand.", font=font("SemiBold", 44), fill=(255, 255, 255), anchor="mt")
    d.text((W // 2, 710), "And to our technology partners", font=font("Medium", 40), fill=LIGHT, anchor="mt")
    d.text((W // 2, 760), "for their support:", font=font("Medium", 40), fill=LIGHT, anchor="mt")
    y = 845
    for p in PARTNERS:
        d.text((W // 2, y), p, font=font("Bold", 52), fill=(255, 255, 255), anchor="mt")
        y += 72
    d.text((W // 2, 1140), "Sinor Marine Services Middle East FZCO", font=font("Medium", 34), fill=LIGHT, anchor="mt")
    return img


def srt_time(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    jpg, out = Path(sys.argv[1]), Path(sys.argv[2])
    ver = sys.argv[3] if len(sys.argv) > 3 else "1"
    out.mkdir(parents=True, exist_ok=True)
    items = []  # (base_png, overlay_png or None, dur, pan, base_width)
    for i, s in enumerate(SLIDES):
        base, ov = base_and_overlay(s, jpg)
        bp, op = out / f"base_{i:02d}.png", out / f"over_{i:02d}.png"
        base.save(bp)
        ov.save(op)
        items.append((bp, op, s["dur"], s.get("pan") if s["kind"] == "pan" else None, base.width))
    ep = out / f"base_{len(SLIDES):02d}.png"
    slide_end().save(ep)
    items.append((ep, None, END_DUR, None, W))

    n = len(items)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for bp, op, d, pan, bw in items:
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d + XFADE:.3f}", "-i", str(bp)]
        if op is not None:
            cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d + XFADE:.3f}", "-i", str(op)]
    cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    audio_idx = sum(2 if op is not None else 1 for _, op, _, _, _ in items)

    parts, idx = [], 0
    for i, (bp, op, d, pan, bw) in enumerate(items):
        if pan is not None:
            a, b = pan
            # hold about 14 percent of the time at each end, glide in between, so faces rest in frame
            u = f"clip((t/{d + XFADE:.3f}-0.14)/0.72,0,1)"
            ease = f"({u}*{u}*(3-2*{u}))"
            x = f"({bw - W})*({a}+({b}-{a})*{ease})"
            parts.append(f"[{idx}:v]crop={W}:{H}:x='{x}':y=0,fps={FPS},format=yuv420p,setsar=1[p{i}]")
        else:
            parts.append(f"[{idx}:v]fps={FPS},format=yuv420p,setsar=1[p{i}]")
        idx += 1
        if op is not None:
            parts.append(f"[{idx}:v]format=rgba[o{i}]")
            parts.append(f"[p{i}][o{i}]overlay=0:0:format=auto,format=yuv420p,setsar=1[v{i}]")
            idx += 1
        else:
            parts.append(f"[p{i}]null[v{i}]")
    last, t = "v0", items[0][2]
    for i in range(1, n):
        parts.append(f"[{last}][v{i}]xfade=transition=fade:duration={XFADE}:offset={t:.3f}[x{i}]")
        last = f"x{i}"
        t += items[i][2]
    total = sum(it[2] for it in items)
    name = f"adipec26-thanks_linkedin_4x5_v{ver}.mp4"
    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{last}]", "-map", f"{audio_idx}:a",
            "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-maxrate", "12M",
            "-bufsize", "24M", "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", str(FPS), "-g", str(FPS * 2),
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
            "-metadata", "title=Thank you, ADIPEC 2026", str(out / name)]
    subprocess.run(cmd, check=True)

    # cover (LinkedIn custom thumbnail) = the title slide as rendered
    base0, ov0 = base_and_overlay(SLIDES[0], jpg)
    Image.alpha_composite(base0.convert("RGBA"), ov0).convert("RGB").save(
        out / f"adipec26-thanks_cover_4x5_v{ver}.jpg", quality=90)

    # SRT of the on-screen captions (optional upload for accessibility; the video itself is silent)
    lines, t0, k = [], 0.0, 1
    for s, it in zip(SLIDES, items):
        if s["cap"] != "TITLE":
            lines.append(f"{k}\n{srt_time(t0 + 0.4)} --> {srt_time(t0 + it[2] - 0.2)}\n{s['cap']}\n")
            k += 1
        t0 += it[2]
    lines.append(f"{k}\n{srt_time(t0 + 0.4)} --> {srt_time(total - 0.2)}\nThank you to every client and visitor, and to our technology partners.\n")
    (out / f"adipec26-thanks_captions_v{ver}.srt").write_text("\n".join(lines), encoding="utf-8")
    print("wrote", out / name, "expected duration", round(total, 2), "s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
