#!/usr/bin/env python3
"""Draw the news poster for Sunday 22 November 2026.

Renders a 1024x1024 newspaper-style front page with five stories, each
with a small code-drawn pictogram, a headline and a short deck. Everything
is drawn from scratch with Pillow primitives: no photos, no copied images,
no network, no randomness, no timestamps -- so repeated runs produce
byte-identical PNG output.

Run:  python3 draw.py   (writes entry.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = 1024
H = 1024

PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
NAVY_LIGHT = (38, 56, 92)
RED = (179, 38, 30)
GOLD = (201, 162, 39)
INK = (28, 28, 28)
GREY = (92, 92, 88)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)
GREEN = (46, 125, 50)
TEAL = (0, 121, 107)
SKY = (176, 216, 230)
SUN = (242, 183, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines = []
    for raw in text.split("\n"):
        words = raw.split(" ")
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, color, max_w, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def panel(draw, box, border=NAVY, width=3):
    """A white story panel with a navy frame."""
    draw.rectangle(box, fill=PANEL, outline=border, width=width)


def kicker(draw, x, y, text):
    """Small red uppercase section label with a short rule after it."""
    fnt = font(SANS_B, 19)
    draw.text((x, y), text, font=fnt, fill=RED)
    tw = draw.textlength(text, font=fnt)
    draw.line([(x + tw + 10, y + 10), (x + tw + 46, y + 10)], fill=RED, width=3)
    return y + 30


def headline(draw, x, y, text, size, max_w, color=INK):
    """Bold serif headline, wrapped; returns y below it."""
    fnt = font(SERIF_B, size)
    return draw_wrapped(draw, x, y, text, fnt, color, max_w,
                         leading=int(size * 1.12))


def deck(draw, x, y, text, size, max_w, color=GREY):
    """Small sans-serif deck text; returns y below it."""
    fnt = font(SANS, size)
    return draw_wrapped(draw, x, y, text, fnt, color, max_w,
                         leading=int(size * 1.35))


# ---------------------------------------------------------------- pictograms
# Each draws a small flat illustration inside the given box (x0, y0, x1, y1).

def pic_globe(draw, box):
    """COP31: a globe with a green leaf."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 6
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=NAVY, width=4)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=NAVY, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340, fill=NAVY, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 20, 160, fill=NAVY, width=2)
    # leaf overlapping the globe's lower right
    lx, ly = cx + r // 3, cy + r // 2
    draw.polygon([(lx, ly - 34), (lx + 34, ly - 6), (lx + 4, ly + 26), (lx - 18, ly + 2)],
                 fill=GREEN, outline=NAVY)
    draw.line([(lx - 8, ly + 14), (lx + 22, ly - 14)], fill=WHITE, width=3)


def pic_flags(draw, box):
    """Nepal-India: the two flags, small and flat."""
    x0, y0, x1, y1 = box
    # India: saffron / white / green with a navy wheel
    ix, iy, iw, ih = x0 + 4, y0 + 4, 104, 54
    draw.rectangle([ix, iy, ix + iw, iy + ih // 3], fill=(255, 153, 51))
    draw.rectangle([ix, iy + ih // 3, ix + iw, iy + 2 * ih // 3], fill=WHITE)
    draw.rectangle([ix, iy + 2 * ih // 3, ix + iw, iy + ih], fill=(19, 136, 8))
    draw.ellipse([ix + iw // 2 - 8, iy + ih // 2 - 8,
                  ix + iw // 2 + 8, iy + ih // 2 + 8], outline=NAVY, width=2)
    # Nepal: double pennant, crimson with a white border
    nx, ny = x0 + 128, y0 + 2
    draw.polygon([(nx, ny), (nx + 46, ny + 20), (nx, ny + 40),
                  (nx + 22, ny + 40), (nx + 46, ny + 56), (nx, ny + 56)],
                 fill=(220, 20, 60), outline=NAVY)
    draw.polygon([(nx + 7, ny + 8), (nx + 34, ny + 20), (nx + 7, ny + 32),
                  (nx + 19, ny + 32), (nx + 34, ny + 44), (nx + 7, ny + 48)],
                 fill=WHITE)
    draw.ellipse([nx + 12, ny + 14, nx + 20, ny + 22], fill=(220, 20, 60))
    draw.ellipse([nx + 12, ny + 36, nx + 20, ny + 44], fill=(220, 20, 60))


def pic_cricket(draw, box):
    """Wellington Test: stumps, bat and ball, in a short strip."""
    x0, y0, x1, y1 = box
    base = y1 - 6
    # red ball on the left
    bx, by = x0 + 34, y0 + 34
    draw.ellipse([bx - 17, by - 17, bx + 17, by + 17], fill=RED, outline=NAVY, width=3)
    draw.arc([bx - 12, by - 12, bx + 12, by + 12], 40, 220, fill=WHITE, width=2)
    # stumps in the middle
    cx = x0 + 130
    for dx in (-18, 0, 18):
        draw.rectangle([cx + dx - 5, base - 44, cx + dx + 5, base],
                       fill=(232, 190, 90), outline=NAVY, width=2)
    draw.rectangle([cx - 23, base - 50, cx + 23, base - 44], fill=NAVY)
    # bat leaning on the right
    draw.polygon([(cx + 66, y0 + 2), (cx + 92, y0 + 10),
                  (cx + 74, base - 4), (cx + 54, base - 10)],
                 fill=(222, 184, 135), outline=NAVY)
    draw.rectangle([cx + 70, y0 - 2, cx + 80, y0 + 12],
                   fill=(222, 184, 135), outline=NAVY)


def pic_factory(draw, box):
    """IG Metall: a factory with a gear."""
    x0, y0, x1, y1 = box
    base = y1 - 12
    # factory body with sawtooth roof
    draw.polygon([(x0 + 10, base), (x0 + 10, base - 84), (x0 + 62, base - 118),
                  (x0 + 114, base - 84), (x0 + 166, base - 118),
                  (x0 + 218, base - 84), (x0 + 218, base)],
                 fill=NAVY_LIGHT, outline=NAVY)
    draw.rectangle([x0 + 196, base - 118, x0 + 216, base - 84], fill=NAVY)
    draw.rectangle([x0 + 30, base - 52, x0 + 66, base - 16], fill=GOLD)
    draw.rectangle([x0 + 86, base - 52, x0 + 122, base - 16], fill=GOLD)
    draw.rectangle([x0 + 142, base - 52, x0 + 178, base - 16], fill=GOLD)
    # gear on the right
    gx, gy, gr = x1 - 58, y0 + 52, 34
    for a in range(0, 360, 45):
        import math
        x = gx + int(gr * 1.35 * math.cos(math.radians(a)))
        y = gy + int(gr * 1.35 * math.sin(math.radians(a)))
        draw.rectangle([x - 9, y - 9, x + 9, y + 9], fill=GOLD, outline=NAVY)
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=GOLD, outline=NAVY, width=3)
    draw.ellipse([gx - 12, gy - 12, gx + 12, gy + 12], fill=PAPER, outline=NAVY, width=3)


def pic_skyline(draw, box):
    """Singapore: towers, sun and water."""
    x0, y0, x1, y1 = box
    base = y1 - 16
    draw.ellipse([x1 - 78, y0 + 12, x1 - 18, y0 + 72], fill=SUN, outline=NAVY, width=2)
    towers = [(0, 85, 58), (66, 108, 58), (132, 73, 58), (198, 95, 58)]
    for dx, hgt, wdt in towers:
        tx = x0 + 14 + dx
        draw.rectangle([tx, base - hgt, tx + wdt, base], fill=NAVY_LIGHT, outline=NAVY)
        for wy in range(base - hgt + 14, base - 8, 24):
            for wx in range(tx + 10, tx + wdt - 8, 18):
                draw.rectangle([wx, wy, wx + 8, wy + 10], fill=GOLD)
    draw.line([(x0 + 8, base + 2), (x1 - 8, base + 2)], fill=TEAL, width=4)
    draw.line([(x0 + 30, base + 12), (x1 - 40, base + 12)], fill=TEAL, width=2)


# ------------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    title = font(SERIF_B, 62)
    d.text((24, 18), "THE WORLD IN ONE IMAGE", font=title, fill=WHITE)
    date = font(SANS_B, 30)
    d.text((24, 96), "SUNDAY  22  NOVEMBER  2026", font=date, fill=GOLD)
    d.text((W - 24 - d.textlength("No. 326  ·  ONE DAY, FIVE STORIES", font=font(SANS, 22)),
            104), "No. 326  ·  ONE DAY, FIVE STORIES", font=font(SANS, 22), fill=WHITE)

    # --- lead: COP31 (top left, large)
    panel(d, (24, 172, 636, 516))
    y = kicker(d, 56, 192, "CLIMATE  ·  ANTALYA")
    y = headline(d, 56, y, "COP31 NEARS A DEAL AFTER OVERTIME", 36, 548)
    pic_globe(d, (56, 322, 216, 472))
    y = deck(d, 240, 330,
             "After two days of overtime, a final package is unveiled in the "
             "early hours of Sunday; delegates have until 03:00 GMT to object.",
             20, 360)
    d.line([(56, 484), (604, 484)], fill=NAVY, width=2)
    d.text((56, 492), "Antalya, Turkey — Reuters, Sunday",
           font=font(SANS, 16), fill=GREY)

    # --- Nepal (top right)
    panel(d, (656, 172, 1000, 334))
    pic_flags(d, (676, 178, 980, 238))
    y = kicker(d, 676, 244, "DIPLOMACY  ·  NEW DELHI")
    headline(d, 676, y, "NEPAL'S PM LANDS IN DELHI", 22, 304)

    # --- cricket (middle right)
    panel(d, (656, 354, 1000, 516))
    pic_cricket(d, (676, 358, 980, 412))
    y = kicker(d, 676, 418, "SPORT  ·  WELLINGTON")
    headline(d, 676, y, "PANT'S 128 PUTS INDIA ON TOP", 20, 304)

    # --- IG Metall (bottom left)
    panel(d, (24, 536, 500, 896))
    pic_factory(d, (52, 552, 472, 684))
    y = kicker(d, 52, 700, "LABOUR  ·  GERMANY")
    y = headline(d, 52, y, "23,000 METALWORKERS TO STRIKE ON MONDAY", 29, 420)
    deck(d, 52, y + 8,
         "IG Metall calls a 24-hour walkout at 19 firms in a pay dispute.",
         19, 420)

    # --- Singapore (bottom right)
    panel(d, (520, 536, 1000, 896))
    pic_skyline(d, (548, 552, 972, 684))
    y = kicker(d, 548, 700, "DIPLOMACY  ·  SINGAPORE")
    y = headline(d, 548, y, "CHINA'S VICE-PREMIER BEGINS SINGAPORE VISIT", 29, 424)
    deck(d, 548, y + 8,
         "Ding Xuexiang arrives for two days of talks, 22–23 November.",
         19, 424)

    # --- footer
    d.line([(24, 918), (1000, 918)], fill=NAVY, width=2)
    foot = font(SANS, 19)
    d.text((24, 932),
           "Every story above happened or was first reported on Sunday 22 November 2026.",
           font=foot, fill=INK)
    d.text((24, 960),
           "Sources: Reuters, Associated Press, ICC, India's Ministry of External Affairs.",
           font=foot, fill=GREY)
    d.text((24, 988), "make.fun  ·  news-image-20261122",
           font=font(SANS_B, 19), fill=NAVY)

    img.save(os.path.join(HERE, "entry.png"), format="PNG")
    return os.path.join(HERE, "entry.png")


if __name__ == "__main__":
    path = build()
    print("wrote", path, os.path.getsize(path), "bytes")
