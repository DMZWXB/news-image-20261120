#!/usr/bin/env python3
"""Render the 1024x1024 news infographic for make.fun news-image-20261120.

All drawing is code-only (PIL primitives): no external images, photos or
logos. Fonts are DejaVu from /usr/share/fonts. Output is deterministic:
same input produces the same PNG bytes.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952

PAPER = (251, 248, 241)
INK = (20, 20, 20)
RED = (179, 38, 30)
GRAY = (90, 86, 78)
HAIR = (201, 194, 180)
WHITE = (255, 255, 255)
TEAL = (31, 110, 138)
BLUE = (47, 111, 178)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
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


def draw_tracked(draw, xy, text, fnt, fill, tracking=2):
    """Draw uppercase text with extra letter spacing."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def fit_lines(draw, text, fnt, max_w, max_lines, min_size, path):
    """Shrink font until wrapped text fits max_lines; return (font, lines)."""
    size = fnt.size
    while size >= min_size:
        f = font(path, size)
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        size -= 2
    raise RuntimeError(f"text does not fit in {max_lines} lines: {text!r}")


def starburst(draw, cx, cy, r_out, r_in, n=8, fill=RED):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def icon_bridge(draw, x, y, s):
    """Bridge silhouette + red burst. Box (x, y, s, s)."""
    cx, cy = x + s // 2, y + s // 2
    # burst above the deck
    starburst(draw, cx, y + s * 0.22, s * 0.20, s * 0.09, fill=RED)
    # deck
    draw.line([(x + s * 0.06, cy + s * 0.18), (x + s * 0.94, cy + s * 0.18)],
              fill=INK, width=max(3, s // 28))
    # two arches
    draw.arc([x + s * 0.08, cy - s * 0.02, x + s * 0.48, cy + s * 0.42],
             180, 360, fill=INK, width=max(3, s // 28))
    draw.arc([x + s * 0.52, cy - s * 0.02, x + s * 0.92, cy + s * 0.42],
             180, 360, fill=INK, width=max(3, s // 28))
    # supports
    for fx in (0.08, 0.28, 0.48, 0.68, 0.88):
        draw.line([(x + s * fx, cy + s * 0.18), (x + s * fx, cy + s * 0.44)],
                  fill=INK, width=max(2, s // 40))
    # water lines
    for i, wy in enumerate((0.56, 0.66)):
        draw.line([(x + s * 0.10, cy + s * wy), (x + s * 0.90, cy + s * wy)],
                  fill=TEAL, width=max(2, s // 40))


def icon_deal(draw, x, y, s):
    """Document with a red seal. Box (x, y, s, s)."""
    dw, dh = s * 0.62, s * 0.78
    ox, oy = x + s * 0.06, y + s * 0.10
    draw.rectangle([ox, oy, ox + dw, oy + dh], fill=WHITE, outline=INK,
                   width=max(3, s // 28))
    # folded corner
    draw.polygon([(ox + dw - s * 0.16, oy), (ox + dw, oy + s * 0.16),
                  (ox + dw - s * 0.16, oy + s * 0.16)], fill=HAIR)
    for i in range(3):
        ly = oy + dh * (0.28 + i * 0.18)
        draw.line([(ox + dw * 0.14, ly), (ox + dw * 0.86, ly)],
                  fill=GRAY, width=max(2, s // 40))
    # red seal
    sx, sy, sr = x + s * 0.72, y + s * 0.74, s * 0.20
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=RED)
    draw.line([(sx - sr * 0.45, sy), (sx - sr * 0.08, sy + sr * 0.42),
               (sx + sr * 0.5, sy - sr * 0.42)], fill=WHITE,
              width=max(3, s // 24), joint="curve")


def icon_chart(draw, x, y, s):
    """Falling market chart with red arrow. Box (x, y, s, s)."""
    # axes
    draw.line([(x + s * 0.10, y + s * 0.12), (x + s * 0.10, y + s * 0.88)],
              fill=GRAY, width=max(2, s // 40))
    draw.line([(x + s * 0.10, y + s * 0.88), (x + s * 0.92, y + s * 0.88)],
              fill=GRAY, width=max(2, s // 40))
    pts = [(0.14, 0.30), (0.30, 0.26), (0.44, 0.44), (0.58, 0.40),
           (0.72, 0.62), (0.86, 0.74)]
    xy = [(x + s * px, y + s * py) for px, py in pts]
    draw.line(xy, fill=INK, width=max(4, s // 22), joint="curve")
    # red down arrow at the end
    ex, ey = xy[-1]
    draw.polygon([(ex - s * 0.02, ey - s * 0.16), (ex + s * 0.10, ey - s * 0.02),
                  (ex - s * 0.10, ey + s * 0.06)], fill=RED)
    draw.line([(ex - s * 0.02, ey - s * 0.16), (ex + s * 0.02, ey + s * 0.10)],
              fill=RED, width=max(4, s // 22))


def icon_cyclone(draw, x, y, s):
    """Spiral. Box (x, y, s, s)."""
    cx, cy = x + s // 2, y + s // 2
    pts = []
    steps = 90
    for i in range(steps + 1):
        t = i / steps * 3.2 * math.pi
        r = s * 0.04 + s * 0.115 * t / math.pi
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    draw.line(pts, fill=TEAL, width=max(4, s // 22), joint="curve")
    draw.ellipse([cx - s * 0.05, cy - s * 0.05, cx + s * 0.05, cy + s * 0.05],
                 fill=RED)


def icon_shield(draw, x, y, s):
    """Shield with check. Box (x, y, s, s)."""
    pts = [(x + s * 0.08, y + s * 0.10), (x + s * 0.92, y + s * 0.10),
           (x + s * 0.92, y + s * 0.52), (x + s * 0.50, y + s * 0.92),
           (x + s * 0.08, y + s * 0.52)]
    draw.polygon(pts, fill=BLUE)
    draw.line([(x + s * 0.28, y + s * 0.48), (x + s * 0.44, y + s * 0.64),
               (x + s * 0.74, y + s * 0.30)], fill=WHITE,
              width=max(5, s // 18), joint="curve")


ICONS = {"bridge": icon_bridge, "deal": icon_deal, "chart": icon_chart,
         "cyclone": icon_cyclone, "shield": icon_shield}

LEAD = {
    "num": "1", "kicker": "WAR IN UKRAINE", "icon": "bridge",
    "headline": "Russia Strikes Kyiv Bridges, Missiles Land in Poland",
    "summary": ("Overnight barrage hit three Kyiv bridges, killing eight and "
                "injuring 28; two missiles and a drone fell in Poland."),
    "stat": "8 DEAD  ·  28 INJURED  ·  400+ DRONES",
}

GRID = [
    {"num": "2", "kicker": "UK–EU SUMMIT", "icon": "deal",
     "headline": "UK and EU Seal Post-Brexit Reset Deal",
     "summary": ("Brussels summit agreed food-trade easing, linked carbon "
                 "markets, and youth mobility for 100,000 people a year."),
     "stat": "100,000 / YEAR  ·  3 YEARS"},
    {"num": "3", "kicker": "MARKETS", "icon": "chart",
     "headline": "Asian Stocks Plunge as AI Sell-Off Deepens",
     "summary": ("Japan's Nikkei fell 4.8% to a seven-month low, SoftBank "
                 "plunged about 15%, and South Korea's KOSPI dropped 4.7%."),
     "stat": "NIKKEI −4.8%  ·  SOFTBANK −15%"},
    {"num": "4", "kicker": "WEATHER", "icon": "cyclone",
     "headline": "Cyclone Akvan Hits India's Eastern Coast",
     "summary": ("Akvan made landfall near Gopalpur with 70–80 km/h winds "
                 "after more than 300,000 people were evacuated to shelters."),
     "stat": "300,000+ EVACUATED  ·  9,341 SHELTERS"},
    {"num": "5", "kicker": "MIDDLE EAST", "icon": "shield",
     "headline": "Saudi Arabia Intercepts Houthi Missile, Drones",
     "summary": ("The Saudi-led coalition said it shot down a Houthi ballistic "
                 "missile and two drones aimed at southern Saudi Arabia."),
     "stat": "1 MISSILE  ·  2 DRONES DOWN"},
]


def draw_block(draw, x, y, w, h, item, headline_size, summary_size,
               icon_size, kicker_size=19, stat_size=19):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    # red number badge
    bs = 34
    draw.rectangle([x, y, x + bs, y + bs], fill=RED)
    bf = font(F_SANS_B, 20)
    tw = draw.textlength(item["num"], font=bf)
    draw.text((x + (bs - tw) / 2, y + 5), item["num"], font=bf, fill=WHITE)
    # kicker
    kf = font(F_SANS_B, kicker_size)
    draw_tracked(draw, (x + bs + 12, y + 8), item["kicker"], kf, RED, tracking=2)
    # icon on the right
    ix = x + w - icon_size - 16
    iy = y + 14
    ICONS[item["icon"]](draw, ix, iy, icon_size)
    # headline (left of icon)
    hw = w - icon_size - 16 - (bs + 12) - 24
    hf, hlines = fit_lines(draw, item["headline"], font(F_SANS_B, headline_size),
                           hw, 2, 20, F_SANS_B)
    hy = y + 48
    for ln in hlines:
        draw.text((x + 16, hy), ln, font=hf, fill=INK)
        hy += hf.size + 4
    # summary
    sf = font(F_SANS, summary_size)
    sw = w - 32
    slines = wrap(draw, item["summary"], sf, sw)
    sy = hy + 6
    for ln in slines:
        draw.text((x + 16, sy), ln, font=sf, fill=(52, 50, 46))
        sy += sf.size + 5
    # stat line: pinned to the bottom, but never overlapping the summary
    stf = font(F_SANS_B, stat_size)
    stat_y = max(y + h - stat_size - 14, sy + 10)
    if stat_y + stat_size + 6 > y + h:
        raise RuntimeError(f"block {item['num']} overflows: summary ends {sy}, box ends {y + h}")
    draw.text((x + 16, stat_y), item["stat"], font=stf, fill=RED)
    return sy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- masthead ---
    y = 30
    kf = font(F_SANS_B, 21)
    draw_tracked(draw, (MARGIN, y), "THE WORLD IN ONE DAY", kf, GRAY, tracking=5)
    y += 34
    # date, auto-fit to content width
    date_text = "FRIDAY 20 NOVEMBER 2026"
    size = 62
    while size > 30:
        df = font(F_SERIF, size)
        if draw.textlength(date_text, font=df) <= CW:
            break
        size -= 2
    draw.text((MARGIN, y), date_text, font=df, fill=INK)
    y += size + 12
    sf = font(F_SANS, 24)
    draw.text((MARGIN, y), "The day in five stories — war, diplomacy, markets, weather, and the Gulf.",
              font=sf, fill=GRAY)
    y += 36
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RED, width=6)
    y += 10
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 16

    # --- lead story ---
    lead_h = 238
    draw_block(draw, MARGIN, y, CW, lead_h, LEAD, headline_size=40,
               summary_size=23, icon_size=150, kicker_size=20, stat_size=20)
    y += lead_h + 16

    # --- 2x2 grid ---
    gap = 16
    gw = (CW - gap) // 2
    gh = 255
    for i, item in enumerate(GRID):
        gx = MARGIN + (i % 2) * (gw + gap)
        gy = y + (i // 2) * (gh + gap)
        draw_block(draw, gx, gy, gw, gh, item, headline_size=27,
                   summary_size=20, icon_size=96, kicker_size=17, stat_size=17)
    y = y + 2 * gh + gap + 14

    # --- footer ---
    ff = font(F_SANS, 16)
    foot = "Sources: Al Jazeera  ·  Morningstar  ·  Reuters  ·  Malay Mail      All events 20 Nov 2026"
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, y), foot, font=ff, fill=GRAY)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
