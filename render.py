#!/usr/bin/env python3
"""Render the 1024x1024 news infographic for make.fun news-image-20261120 (v2).

31 stories from Friday 20 November 2026, all checked against same-day
reporting. Code-only drawing (PIL primitives): no external images, photos
or logos. Fonts are DejaVu from /usr/share/fonts. Output is deterministic:
same input produces the same PNG bytes.

Layout: masthead (with a same-day verification line) + one lead story +
"The day in brief": 30 compact items in 3 columns x 10 rows, grouped by
region, each with its source named.
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
    starburst(draw, cx, y + s * 0.22, s * 0.20, s * 0.09, fill=RED)
    draw.line([(x + s * 0.06, cy + s * 0.18), (x + s * 0.94, cy + s * 0.18)],
              fill=INK, width=max(3, s // 28))
    draw.arc([x + s * 0.08, cy - s * 0.02, x + s * 0.48, cy + s * 0.42],
             180, 360, fill=INK, width=max(3, s // 28))
    draw.arc([x + s * 0.52, cy - s * 0.02, x + s * 0.92, cy + s * 0.42],
             180, 360, fill=INK, width=max(3, s // 28))
    for fx in (0.08, 0.28, 0.48, 0.68, 0.88):
        draw.line([(x + s * fx, cy + s * 0.18), (x + s * fx, cy + s * 0.44)],
                  fill=INK, width=max(2, s // 40))
    for wy in (0.56, 0.66):
        draw.line([(x + s * 0.10, cy + s * wy), (x + s * 0.90, cy + s * wy)],
                  fill=TEAL, width=max(2, s // 40))


ICONS = {"bridge": icon_bridge}

LEAD = {
    "num": "1", "kicker": "WAR IN UKRAINE", "icon": "bridge",
    "headline": "Russia Strikes Kyiv Bridges, Missiles Land in Poland",
    "summary": ("Overnight barrage hit three Kyiv bridges; two missiles "
                "and a drone fell in Poland."),
    "stat": "8 DEAD  ·  28 INJURED  ·  400+ DRONES",
}

# 30 brief items, region order: Europe, Middle East, Africa, East Asia,
# South Asia, Southeast Asia, Oceania, Americas. Each: region tag, source,
# headline (key figure embedded where there is one).
BRIEF = [
    ("EUROPE", "Al Jazeera", "UK and EU Seal Post-Brexit Reset Deal"),
    ("EUROPE", "Reuters", "Students March Over Prices and Military Spending"),
    ("EUROPE", "Reuters", "Eurozone Consumer Confidence Rises in November"),
    ("UK", "Reuters", "UK Fixes Fridge-Freezer Flaw After EU Hacks"),
    ("GERMANY", "Reuters", "German Minister Sorry for 'Stupid' Jibe at US"),
    ("SPAIN", "Reuters", "Feijóo Wins TV Debate 51%–29%, Polls Show"),
    ("MIDDLE EAST", "Malay Mail", "Saudi Arabia Intercepts Houthi Missile, Drones"),
    ("GAZA", "AFP", "Israeli Strikes Kill Six in Gaza, Medics Say"),
    ("IRAQ", "Al Jazeera", "Iraqi Army Moves Into Militia Stronghold"),
    ("IRAN", "AP", "Trump Says Iran Wants a Nuclear Deal"),
    ("IRAN", "Al Jazeera", "Iran Rules Out Shipping Uranium Abroad"),
    ("ANGOLA", "Reuters", "Angola to Buy 10% of De Beers for $180m"),
    ("NIGERIA", "Reuters", "Rescue After Funeral Boat Capsizes in Nigeria"),
    ("NIGERIA", "Reuters", "Nigeria VP Urges Banks to Lend More to Farms"),
    ("MIGRATION", "Africanews", "UN, Senegal Push Back on Migrant Smuggling"),
    ("MARKETS", "Morningstar", "Nikkei −4.8% as AI Sell-Off Hits Asia"),
    ("JAPAN", "Reuters", "Japan Core Inflation Hits 2.2%, Year's High"),
    ("CHINA", "Reuters", "China Holds Loan Rates for 18th Month"),
    ("SOUTH KOREA", "BOK", "South Korea Producer Prices Edge Down 0.1%"),
    ("WEATHER", "Reuters", "Cyclone Akvan Hits India; 300,000 Evacuated"),
    ("INDIA", "PTI", "India Launches First Homegrown Bird-Flu Vaccine"),
    ("INDIA", "PTI", "Four Cheetah Cubs Born in India; Total Now 62"),
    ("THAILAND", "Khaosod English", "Thai–China Rail Link to Reach Malaysia, Singapore"),
    ("SINGAPORE", "Straits Times", "Singapore, China Open FTA Upgrade Talks"),
    ("AUSTRALIA", "BBC", "Cricket Australia Backs Captain Cummins"),
    ("OCEANIA", "GAC Canada", "Australia, Canada, NZ Urge Russia Ceasefire"),
    ("MEXICO", "NY Post", "Mexico Army Captures Drug Lord 'Chapo Isidro'"),
    ("EL SALVADOR", "Reuters", "Bukele Registers to Run for Third Term"),
    ("VENEZUELA", "AP", "US, Venezuela Resume Military Cooperation"),
    ("CANADA", "Washington Post", "US Curbs Military Cooperation With Canada"),
]


def draw_block(draw, x, y, w, h, item, headline_size, summary_size,
               icon_size, kicker_size=19, stat_size=19):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    bs = 34
    draw.rectangle([x, y, x + bs, y + bs], fill=RED)
    bf = font(F_SANS_B, 20)
    tw = draw.textlength(item["num"], font=bf)
    draw.text((x + (bs - tw) / 2, y + 5), item["num"], font=bf, fill=WHITE)
    kf = font(F_SANS_B, kicker_size)
    draw_tracked(draw, (x + bs + 12, y + 8), item["kicker"], kf, RED, tracking=2)
    ix = x + w - icon_size - 16
    iy = y + 14
    ICONS[item["icon"]](draw, ix, iy, icon_size)
    hw = w - icon_size - 16 - (bs + 12) - 24
    hf, hlines = fit_lines(draw, item["headline"], font(F_SANS_B, headline_size),
                           hw, 2, 20, F_SANS_B)
    hy = y + 44
    for ln in hlines:
        draw.text((x + 16, hy), ln, font=hf, fill=INK)
        hy += hf.size + 4
    sf = font(F_SANS, summary_size)
    sw = w - 32
    slines = wrap(draw, item["summary"], sf, sw)
    if len(slines) > 1:
        raise RuntimeError(f"lead summary must fit one line: {item['summary']!r}")
    sy = hy + 4
    draw.text((x + 16, sy), slines[0], font=sf, fill=(52, 50, 46))
    sy += sf.size + 5
    stf = font(F_SANS_B, stat_size)
    stat_y = max(y + h - stat_size - 14, sy + 6)
    if stat_y + stat_size + 6 > y + h:
        raise RuntimeError(f"lead block overflows: stat at {stat_y}, box ends {y + h}")
    draw.text((x + 16, stat_y), item["stat"], font=stf, fill=RED)


def draw_brief_item(draw, x, y, w, h, region, source, headline):
    """One compact brief row: red region tag + gray source, bold headline
    (max 2 lines), hairline at the bottom. Raises on overflow."""
    # tag line
    tf = font(F_SANS_B, 12)
    rx = draw_tracked(draw, (x, y + 2), region, tf, RED, tracking=1)
    sf = font(F_SANS, 12)
    draw.text((rx + 4, y + 2), "· " + source, font=sf, fill=GRAY)
    # headline, max 2 lines, shrink 15 -> 13
    hf, hlines = fit_lines(draw, headline, font(F_SANS_B, 15), w, 2, 13,
                           F_SANS_B)
    hy = y + 20
    for ln in hlines:
        draw.text((x, hy), ln, font=hf, fill=INK)
        hy += hf.size + 3
    if hy > y + h - 4:
        raise RuntimeError(f"brief item overflows: {headline!r} ends {hy}, row ends {y + h}")
    draw.line([(x, y + h - 1), (x + w, y + h - 1)], fill=HAIR, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- masthead ---
    y = 26
    kf = font(F_SANS_B, 20)
    draw_tracked(draw, (MARGIN, y), "THE WORLD IN ONE DAY", kf, GRAY, tracking=5)
    y += 30
    date_text = "FRIDAY 20 NOVEMBER 2026"
    size = 54
    while size > 30:
        df = font(F_SERIF, size)
        if draw.textlength(date_text, font=df) <= CW:
            break
        size -= 2
    draw.text((MARGIN, y), date_text, font=df, fill=INK)
    y += size + 10
    sf = font(F_SANS, 21)
    draw.text((MARGIN, y),
              "Thirty-one stories from six continents — war, diplomacy, markets, weather and more.",
              font=sf, fill=GRAY)
    y += 28
    vf = font(F_SANS_B, 13)
    draw_tracked(draw, (MARGIN, y),
                 "EVERY STORY CHECKED AGAINST SAME-DAY REPORTING · ALL EVENTS 20 NOV 2026 (UTC)",
                 vf, RED, tracking=1)
    y += 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RED, width=6)
    y += 6
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 8
    mast_end = y

    # --- lead story ---
    lead_h = 162
    draw_block(draw, MARGIN, mast_end, CW, lead_h, LEAD, headline_size=26,
               summary_size=18, icon_size=100, kicker_size=18, stat_size=18)
    y = mast_end + lead_h + 10

    # --- section header ---
    hf = font(F_SANS_B, 16)
    draw_tracked(draw, (MARGIN, y), "THE DAY IN BRIEF", hf, RED, tracking=2)
    rf = font(F_SANS, 13)
    right = "30 MORE STORIES · SOURCES NAMED WITH EACH"
    rw = draw.textlength(right, font=rf)
    draw.text((W - MARGIN - rw, y + 2), right, font=rf, fill=GRAY)
    y += 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=1)
    y += 6
    brief_top = y

    # --- brief grid: 3 columns x 10 rows, column-major ---
    gap = 14
    col_w = (CW - 2 * gap) // 3  # 308
    row_h = 61
    assert len(BRIEF) == 30, f"expected 30 brief items, got {len(BRIEF)}"
    for col in range(3):
        cx = MARGIN + col * (col_w + gap)
        for row in range(10):
            item = BRIEF[col * 10 + row]
            iy = brief_top + row * row_h
            draw_brief_item(draw, cx, iy, col_w, row_h, *item)
    y = brief_top + 10 * row_h
    if y > 992:
        raise RuntimeError(f"brief grid ends at {y}, footer would overflow")

    # --- footer ---
    ff = font(F_SANS, 12)
    foot1 = ("Sources: Reuters · Al Jazeera · AP · AFP · Morningstar · Malay Mail · "
             "PTI · BBC · WaPo · Khaosod · Straits Times · Africanews · BOK · "
             "GAC Canada · NY Post")
    fw = draw.textlength(foot1, font=ff)
    if fw > CW:
        raise RuntimeError(f"footer line 1 too wide: {fw:.0f}px > {CW}px")
    draw.text(((W - fw) / 2, y + 4), foot1, font=ff, fill=GRAY)
    foot2 = "All events 20 November 2026 (UTC) · Every story checked against same-day reporting"
    fw2 = draw.textlength(foot2, font=ff)
    draw.text(((W - fw2) / 2, y + 20), foot2, font=ff, fill=GRAY)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
