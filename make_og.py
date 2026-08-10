#!/usr/bin/env python3
"""Idea Finder social-share card — 1200x630 OG image, same visual language as the app icon."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630
BG1 = (24, 17, 48)            # deep indigo-black (matches --bg dark)
BG2 = (58, 33, 112)           # violet
GLOW = (167, 139, 250)        # --brand dark
MAGENTA = (222, 74, 244)
WHITE = (255, 255, 255)
MUTED = (183, 169, 220)       # --ink-2 dark

FONT_DIR = "/usr/share/fonts/truetype/noto"
BOLD = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def diag_gradient(size, c1, c2):
    w, h = size
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = lerp(c1, c2, ((x / w) + (y / h)) / 2)
    return img


def build():
    base = diag_gradient((W, H), BG1, BG2)

    # magenta glow, bottom-right
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(glow).ellipse([W * 0.55, H * 0.35, W * 1.35, H * 1.45], fill=MAGENTA)
    glow = glow.filter(ImageFilter.GaussianBlur(150))
    base = Image.blend(base, glow, 0.30)

    # violet glow, top-left
    glow2 = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(glow2).ellipse([-W * 0.25, -H * 0.5, W * 0.5, H * 0.6], fill=GLOW)
    glow2 = glow2.filter(ImageFilter.GaussianBlur(170))
    base = Image.blend(base, glow2, 0.22)

    d = ImageDraw.Draw(base, "RGBA")

    f_kicker = ImageFont.truetype(BOLD, 24)
    f_h1 = ImageFont.truetype(BOLD, 76)
    f_sub = ImageFont.truetype(REG, 30)
    f_chip = ImageFont.truetype(BOLD, 23)

    PAD = 78
    icon_size = 108
    icon_path = os.path.join(HERE, "icons", "icon-512.png")
    icon = Image.open(icon_path).convert("RGBA").resize((icon_size, icon_size), Image.LANCZOS)
    base.paste(icon, (PAD, PAD - 8), icon)

    d.text((PAD + icon_size + 24, PAD + 16), "IDEA FINDER", font=f_kicker, fill=WHITE)
    d.text((PAD + icon_size + 24, PAD + 52), "100% local  ·  no account", font=ImageFont.truetype(REG, 22), fill=MUTED)

    y = 258
    d.text((PAD, y), "Find what people need", font=f_h1, fill=WHITE)
    d.text((PAD, y + 88), "before you build it.", font=f_h1, fill=GLOW)

    d.text((PAD, y + 200),
           "Seed a niche · hunt 12 live free sources · score every opportunity",
           font=f_sub, fill=MUTED)

    # feature chips along the bottom
    chips = ["Reddit", "Google Trends", "Etsy", "Amazon reviews", "Product Hunt", "+7 more"]
    cx = PAD
    cy = H - 108
    for c in chips:
        tw = d.textlength(c, font=f_chip)
        w_chip = int(tw) + 36
        if cx + w_chip > W - PAD:
            break
        d.rounded_rectangle([cx, cy, cx + w_chip, cy + 46], radius=23,
                            fill=(255, 255, 255, 26), outline=(255, 255, 255, 60), width=2)
        d.text((cx + 18, cy + 11), c, font=f_chip, fill=WHITE)
        cx += w_chip + 12

    out = os.path.join(HERE, "og-image.png")
    base.save(out, optimize=True)
    print("wrote", out, base.size)


if __name__ == "__main__":
    build()
