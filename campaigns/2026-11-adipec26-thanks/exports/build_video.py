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
# (full name written under the tile, supplied logo file). Names confirmed by Rahul 2026-11-06; "use full spelling".
PARTNERS = [("Sonardyne", "sonardyne.png"), ("Fugro", "fugro.png"), ("Navis Engineering", "navis-engineering.png"),
            ("Marine Technologies", "marine-technologies-mt.png"), ("Guidance Marine", "guidance-marine.png")]
PARTNER_DIR = Path(__file__).resolve().parents[3] / "assets/brand/partners"
# Each beat: files (1 file, or 2 for a stacked split-screen pair), mode (cover | fit | pair),
# dur seconds, cap (caption; "TITLE" = opening title), optional crop_top for portrait cover crops.
SLIDES = [
    dict(files=["0f44943b-22e6-4381-aac3-66a9dfc31218.jpg"], mode="cover", dur=4.0, cap="TITLE"),
    dict(files=["IMG_4413.jpg"], mode="fith", dur=2.8, cap="NAVIS console"),
    dict(files=["IMG_4432.jpg"], mode="cover", dur=2.8, cap="Sonardyne SPRINT-Nav on the stand", crop_top=0.6),
    dict(files=["IMG_4464.jpg", "0bc7989f-ffd8-4930-b538-267cc2414e4e.jpg"], mode="pair", dur=3.2, cap="Conversations at the stand"),
    dict(files=["IMG_4188.jpg", "IMG_4255.jpg"], mode="pair", dur=3.2, cap="Marine Technologies on the stand"),
    dict(files=["IMG_4403.jpg", "IMG_4156.jpg"], mode="pair", dur=3.2, cap="Welcome to our stand"),
    dict(files=["cf677e0a-bf65-4e06-8a7a-9a40f904137c.jpg"], mode="cover", dur=2.8, cap="At the stand", crop_top=0.78),
    dict(files=["a07555b5-23b3-4497-92aa-a3613e384bc5.jpg"], mode="fit", dur=2.8, cap="Thank you for stopping by"),
]
END_DUR, XFADE = 5.5, 0.45
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


def cell(im, cw, ch, crop_top=0.5):
    s = max(cw / im.width, ch / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - cw) // 2, round((im.height - ch) * crop_top)
    return im.crop((x, y, x + cw, y + ch))


def photo_layer(jpg, it):
    ims = []
    for f in it["files"]:
        im = Image.open(jpg / f).convert("RGB")
        if f in CROPS:
            im = im.crop(CROPS[f])
        ims.append(im)
    mode = it["mode"]
    if mode == "pair":
        ch, gap = (600, 10) if ASPECT == "4x5" else (700, 10)
        bg = cover(ims[0]).filter(ImageFilter.GaussianBlur(38))
        bg = Image.blend(bg, Image.new("RGB", (W, H), NAVY), 0.55)
        stack = 2 * ch + gap
        top = max((SAFE - stack) // 2, 30) if ASPECT == "9x16" else 60
        bg.paste(cell(ims[0], W, ch, crop_top=0.0), (0, top))  # keep headroom in the top photo
        bg.paste(cell(ims[1], W, ch), (0, top + ch + gap))
        return bg
    if mode == "fith":
        # tall photo shown whole (nothing cropped, for example a logo) with soft bands, kept well above the caption
        fh = 1250 if ASPECT == "4x5" else SAFE - 120
        bg = cover(ims[0]).filter(ImageFilter.GaussianBlur(38))
        bg = Image.blend(bg, Image.new("RGB", (W, H), NAVY), 0.45)
        fg = ims[0].resize((round(ims[0].width * fh / ims[0].height), fh), Image.LANCZOS)
        bg.paste(fg, ((W - fg.width) // 2, 0))
        return bg
    if ASPECT == "9x16" or mode == "fit":
        return fit_blur(ims[0])
    return cover(ims[0], crop_top=it.get("crop_top", 0.78))


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


def partner_tile(logo_file, tw, th):
    """White rounded tile with the supplied logo scaled to fit (never distorted or recoloured)."""
    lg = Image.open(PARTNER_DIR / logo_file).convert("RGBA")
    box_w, box_h = tw - 44, th - 26
    sc = min(box_w / lg.width, box_h / lg.height)
    lg = lg.resize((max(1, round(lg.width * sc)), max(1, round(lg.height * sc))), Image.LANCZOS)
    tile = Image.new("RGBA", (tw, th), (255, 255, 255, 255))
    tile.alpha_composite(lg, ((tw - lg.width) // 2, (th - lg.height) // 2))
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw, th], radius=18, fill=255)
    tile.putalpha(mask)
    return tile


def end_card():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(H):
        c = tuple(int(NAVY[i] + (BLUE[i] - NAVY[i]) * (y / H) * 0.9) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    tw, th, gx, pitch = 470, 124, 20, 184
    rows = (len(PARTNERS) + 1) // 2
    block = 600 + (rows - 1) * pitch + th + 42  # y of the bottom edge of the last caption for o = 0
    o = (SAFE - block) // 2 - 6
    img = img.convert("RGBA")
    card = logo_card_rgba(420)
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
        last_alone = (k == len(PARTNERS) - 1) and (len(PARTNERS) % 2 == 1)
        x = (W - tw) // 2 if last_alone else (W - (2 * tw + gx)) // 2 + c * (tw + gx)
        y = y0 + r * pitch
        img.alpha_composite(partner_tile(logo, tw, th), (x, y))
        d.text((x + tw // 2, y + th + 8), name, font=font("SemiBold", 32), fill=WHITE + (255,), anchor="mt")
    return img.convert("RGB")


def make_clip(photo, n, zoom_in, amt, path):
    """Render n frames of a smooth push-in (or pull-out) with sub-pixel bicubic sampling.
    ffmpeg zoompan rounds its crop to whole pixels, which shows as stepped judder, so the
    motion is rendered here and piped to ffmpeg as raw frames (near-lossless intermediate)."""
    ff = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", str(path)],
        stdin=subprocess.PIPE)
    for k in range(n):
        t = k / (n - 1)
        z = 1 + amt * t if zoom_in else 1 + amt * (1 - t)
        cx, cy = W / 2 - (W / 2) / z, H / 2 - (H / 2) / z
        ff.stdin.write(photo.transform((W, H), Image.AFFINE, (1 / z, 0, cx, 0, 1 / z, cy), resample=Image.BICUBIC).tobytes())
    ff.stdin.close()
    ff.wait()


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    jpg, out, ver = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    out.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    parts, tags, durs = [], [], []
    idx = 0
    for i, it in enumerate(SLIDES):
        dur, cap = it["dur"], it["cap"]
        photo = photo_layer(jpg, it)
        ov = overlay_layer(cap)
        pp, op = out / f"photo_{i:02d}.png", out / f"overlay_{i:02d}.png"
        photo.save(pp)
        ov.save(op)
        if i == 0:
            Image.alpha_composite(photo.convert("RGBA"), ov).convert("RGB").save(
                out / f"adipec26-thanks_cover_{ASPECT}_v{ver}.jpg", quality=90)
        n = int((dur + XFADE) * FPS)
        clip = out / f"clip_{i:02d}.mp4"
        make_clip(photo, n, i % 2 == 0, 0.06 if i == 0 else 0.075, clip)
        cmd += ["-i", str(clip), "-loop", "1", "-framerate", str(FPS), "-t", f"{dur + XFADE:.3f}", "-i", str(op)]
        parts.append(
            f"[{idx}:v]fps={FPS},format=yuv420p[p{i}];"
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
