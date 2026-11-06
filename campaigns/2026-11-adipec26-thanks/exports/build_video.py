#!/usr/bin/env python3
"""Build the ADIPEC 2026 thank-you video for LinkedIn from working copies of the photos (v4 design).

Usage:  python3 build_video.py <jpg_dir> <out_dir> <version> [4x5|9x16]
  jpg_dir : folder with auto-oriented JPG copies of the Drive originals (NOT in the repo)
  out_dir : where overlays, the MP4 and the cover are written (NOT in the repo)
Needs: Pillow, ffmpeg with libx264/aac, Inter fonts in /usr/share/fonts/opentype/inter.
Originals are never touched. Logo: assets/brand/sinor-logo.png (official, supplied).
No music (none supplied): a silent AAC track is added so players treat the file normally.

Design basis: research/research.md. Slow push-in or drift on each photo (template style
"cinematic recap"), thank-you message and best photo in the first seconds (LinkedIn tip),
burned-in text for silent viewing, text-only partner card, all text kept above a bottom
safe margin that scales with the format. 4x5 is the master; 9x16 is an alternative to post
INSTEAD of (not with) the master.
"""
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ASPECT = sys.argv[4] if len(sys.argv) > 4 else "4x5"
W, H = (1080, 1350) if ASPECT == "4x5" else (1080, 1920)
SAFE = H - (150 if ASPECT == "4x5" else 300)  # nothing important below this y
FPS = 25
NAVY, BLUE = (10, 42, 74), (13, 74, 133)
LIGHT = (196, 218, 240)
WHITE = (255, 255, 255)
FONT_DIR = "/usr/share/fonts/opentype/inter/"
LOGO = Path(__file__).resolve().parents[3] / "assets/brand/sinor-logo.png"

# ---- content (edit here, then rebuild) ---------------------------------------------------------
EVENT_LINE = "ADIPEC 2026  ·  ABU DHABI"
DATE_LINE = "2-5 November 2026"
PARTNERS = ["Sonardyne", "Fugro", "NAVIS", "Marine Technologies"]  # names pending Rahul's confirmation
# (file, mode, duration_s, caption)  mode: cover | fit.  First slide carries the title.
SLIDES = [
    ("0f44943b-22e6-4381-aac3-66a9dfc31218.jpg", "cover", 4.0, "TITLE"),
    ("0bc7989f-ffd8-4930-b538-267cc2414e4e.jpg", "fit", 3.4, "DP console on the stand"),
    ("0CDC96B1-3817-4C16-B71D-B9108ECD8AD4.jpg", "fit", 3.4, "Conversations at the stand"),
    # cf677e0a (two men at the stand) held back: a media file name is readable on the stand TV.
    ("a07555b5-23b3-4497-92aa-a3613e384bc5.jpg", "fit", 3.4, "Thank you for stopping by"),
]
END_DUR, XFADE = 5.0, 0.45
# The supplied collage stacks two photos with a white seam near rows 714 to 725: use only the
# sharp top photo, starting at row 14 to drop the white border.
CROPS = {"0CDC96B1-3817-4C16-B71D-B9108ECD8AD4.jpg": (0, 14, 1206, 710)}
# -------------------------------------------------------------------------------------------------


def font(weight, size):
    return ImageFont.truetype(f"{FONT_DIR}Inter-{weight}.otf", size)


def cover(im, crop_top=0.5):
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


def photo_layer(path, mode):
    im = Image.open(path).convert("RGB")
    if Path(path).name in CROPS:
        im = im.crop(CROPS[Path(path).name])
    if ASPECT == "9x16" or mode == "fit":
        return fit_blur(im)
    return cover(im, crop_top=0.78)  # trim ceiling, keep shoes


def gradient_layer(start, strength):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    for y in range(max(start, 0), H):
        a = int(strength * ((y - start) / (H - start)) ** 1.4)
        d.line([(0, y), (W, y)], fill=NAVY + (a,))
    return g


def logo_card_rgba(width):
    lg = Image.open(LOGO).convert("RGB")
    lg = lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)
    pad = 18
    card = Image.new("RGBA", (lg.width + 2 * pad, lg.height + 2 * pad), (255, 255, 255, 255))
    card.paste(lg, (pad, pad))
    mask = Image.new("L", card.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, card.width, card.height], radius=22, fill=255)
    card.putalpha(mask)
    return card


def overlay_layer(caption):
    layer = gradient_layer(SAFE - (500 if caption == "TITLE" else 270), 245 if caption == "TITLE" else 230)
    t = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    if caption == "TITLE":
        d.rectangle([64, SAFE - 320, 64 + 96, SAFE - 312], fill=LIGHT + (255,))
        d.text((64, SAFE - 290), "Thank you.", font=font("ExtraBold", 132), fill=WHITE + (255,))
        d.text((64, SAFE - 134), EVENT_LINE, font=font("SemiBold", 42), fill=WHITE + (255,))
        d.text((64, SAFE - 78), DATE_LINE, font=font("Medium", 40), fill=LIGHT + (255,))
        t.alpha_composite(logo_card_rgba(250), (48, 48 if ASPECT == "4x5" else 130))
    else:
        d.rectangle([64, SAFE - 104, 64 + 72, SAFE - 97], fill=LIGHT + (255,))
        d.text((64, SAFE - 82), caption, font=font("SemiBold", 48), fill=WHITE + (255,))
    return Image.alpha_composite(layer, t)


def end_card():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(H):
        c = tuple(int(NAVY[i] + (BLUE[i] - NAVY[i]) * (y / H) * 0.9) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    o = (SAFE - 1200) // 2  # centre the block above the safe margin
    img = img.convert("RGBA")
    card = logo_card_rgba(560)
    img.alpha_composite(card, ((W - card.width) // 2, 80 + o))
    d = ImageDraw.Draw(img)
    cx = W // 2
    d.text((cx, 380 + o), "Thank you", font=font("ExtraBold", 120), fill=WHITE + (255,), anchor="mt")
    d.rectangle([cx - 48, 530 + o, cx + 48, 538 + o], fill=LIGHT + (255,))
    d.text((cx, 575 + o), "To every client and visitor", font=font("SemiBold", 44), fill=WHITE + (255,), anchor="mt")
    d.text((cx, 633 + o), "who stopped by our stand.", font=font("SemiBold", 44), fill=WHITE + (255,), anchor="mt")
    d.text((cx, 725 + o), "And to our technology partners", font=font("Medium", 40), fill=LIGHT + (255,), anchor="mt")
    d.text((cx, 775 + o), "for their support:", font=font("Medium", 40), fill=LIGHT + (255,), anchor="mt")
    y = 860 + o
    for p in PARTNERS:
        d.text((cx, y), p, font=font("Bold", 52), fill=WHITE + (255,), anchor="mt")
        y += 72
    d.text((cx, y + 20), "Sinor Marine Services Middle East FZCO", font=font("Medium", 34), fill=LIGHT + (255,), anchor="mt")
    return img.convert("RGB")


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    jpg, out, ver = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    out.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    parts, tags, durs = [], [], []
    idx = 0
    for i, (f, mode, dur, cap) in enumerate(SLIDES):
        photo = photo_layer(jpg / f, mode)
        ov = overlay_layer(cap)
        pp, op = out / f"photo_{i:02d}.png", out / f"overlay_{i:02d}.png"
        photo.save(pp)
        ov.save(op)
        if i == 0:
            Image.alpha_composite(photo.convert("RGBA"), ov).convert("RGB").save(
                out / f"adipec26-thanks_cover_{ASPECT}_v{ver}.jpg", quality=90)
        n = int((dur + XFADE) * FPS)
        zin = i % 2 == 0
        z = f"1+{0.06 if i == 0 else 0.075}*on/{n}" if zin else f"1.075-0.075*on/{n}"
        cmd += ["-i", str(pp), "-loop", "1", "-framerate", str(FPS), "-t", f"{dur + XFADE:.3f}", "-i", str(op)]
        parts.append(
            f"[{idx}:v]scale={W * 2}:{H * 2}:flags=lanczos,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={n}:s={W}x{H}:fps={FPS},format=yuv420p[p{i}];"
            f"[{idx + 1}:v]format=rgba[o{i}];[p{i}][o{i}]overlay=0:0:format=auto,format=yuv420p,setsar=1[v{i}]")
        tags.append(f"v{i}")
        durs.append(dur)
        idx += 2
    ep = out / "end_card.png"
    end_card().save(ep)
    cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{END_DUR + XFADE:.3f}", "-i", str(ep)]
    parts.append(f"[{idx}:v]fps={FPS},format=yuv420p,setsar=1[vend]")
    tags.append("vend")
    durs.append(END_DUR)
    idx += 1
    cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    last, t = tags[0], durs[0]
    for k in range(1, len(tags)):
        parts.append(f"[{last}][{tags[k]}]xfade=transition=fade:duration={XFADE}:offset={t:.3f}[x{k}]")
        last = f"x{k}"
        t += durs[k]
    total = sum(durs)
    name = f"adipec26-thanks_linkedin_{ASPECT}_v{ver}.mp4"
    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{last}]", "-map", f"{idx}:a", "-t", f"{total:.3f}",
            "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high",
            "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", str(out / name)]
    subprocess.run(cmd, check=True)
    print("wrote", out / name, "expected duration", round(total, 2), "s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
