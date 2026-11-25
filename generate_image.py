#!/usr/bin/env python3
"""Build the news-image-20261125 front page (1024x1024 PNG).

Layout: newspaper front page in the proven winners' skeleton
(masthead + date, black ticker, 3 illustrated leads with one dominant
hero, 5 small illustrated stories, numbered "ALSO ON" briefs, DATE CHECK
box, sources footer) — but with photographic illustrations for the three
leads instead of flat drawings, and fewer, larger briefs so the page
reads at 300 px.

Illustrations: assets/hero-naval.png, assets/thumb-riyadh.png and
assets/thumb-awacs.png are generated at build time by the agent's image
tool (no text in them). If an asset is missing, a flat PIL scene is
drawn in its place so the script still runs standalone.
All type is set with PIL; no network, no randomness.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (166, 25, 46)
NAVY = (22, 35, 63)
GREY = (96, 96, 96)
LIGHTRED = (247, 232, 232)
CARD = (255, 255, 255)
TEAL = (23, 84, 92)
GREEN = (31, 94, 52)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
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


def fit_text(draw, text, fnt_path, max_w, start_size, min_size=10):
    """Largest font size (<= start_size) at which text fits max_w."""
    size = start_size
    while size > min_size:
        fnt = font(fnt_path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(fnt_path, min_size)


def photo_panel(path, box, fallback_kind):
    """Crop-fill a photo into box (x0,y0,x1,y1); flat fallback if missing."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if os.path.exists(path):
        im = Image.open(path).convert("RGB")
        return ImageOps.fit(im, (w, h), Image.LANCZOS)
    im = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(im)
    if fallback_kind == "ship":
        d.polygon([(0, h), (0, int(h * 0.62)), (w, int(h * 0.62)), (w, h)],
                  fill=(18, 38, 66))
        d.polygon([(int(w * 0.15), int(h * 0.62)), (int(w * 0.85), int(h * 0.62)),
                   (int(w * 0.78), int(h * 0.42)), (int(w * 0.25), int(h * 0.42))],
                  fill=(40, 40, 44))
        d.rectangle([int(w * 0.45), int(h * 0.30), int(w * 0.52), int(h * 0.44)],
                    fill=(40, 40, 44))
        d.ellipse([int(w * 0.60), int(h * 0.10), int(w * 0.75), int(h * 0.38)],
                  fill=(214, 96, 32))
        d.ellipse([int(w * 0.55), int(h * 0.05), int(w * 0.82), int(h * 0.30)],
                  fill=(90, 90, 96))
    elif fallback_kind == "tower":
        d.rectangle([0, 0, w, h], fill=(38, 52, 84))
        d.polygon([(int(w * 0.42), h), (int(w * 0.42), int(h * 0.12)),
                   (int(w * 0.58), int(h * 0.12)), (int(w * 0.58), h)],
                  fill=(180, 190, 205))
        d.ellipse([int(w * 0.45), 0, int(w * 0.85), int(h * 0.30)],
                  fill=(120, 120, 126))
    else:  # plane
        d.rectangle([0, 0, w, h], fill=(58, 74, 96))
        d.ellipse([int(w * 0.30), int(h * 0.38), int(w * 0.70), int(h * 0.58)],
                  fill=(210, 214, 220))
        d.polygon([(int(w * 0.10), int(h * 0.50)), (int(w * 0.90), int(h * 0.50)),
                   (int(w * 0.86), int(h * 0.56)), (int(w * 0.14), int(h * 0.56))],
                  fill=(210, 214, 220))
    return im


def flat_icon(d, kind, box):
    """Small flat illustration for a row-2 card."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w // 2, y0 + h // 2
    if kind == "medal":
        d.rectangle(box, fill=NAVY)
        d.polygon([(cx, cy - 26), (cx + 8, cy - 8), (cx + 27, cy - 6),
                   (cx + 13, cy + 7), (cx + 17, cy + 26), (cx, cy + 14),
                   (cx - 17, cy + 26), (cx - 13, cy + 7), (cx - 27, cy - 6),
                   (cx - 8, cy - 8)], fill=(212, 175, 55))
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(22, 35, 63))
    elif kind == "chart":
        d.rectangle(box, fill=CARD)
        d.line([(x0 + 14, y0 + h - 16), (x0 + 60, y0 + 26),
                (x0 + 105, y0 + 44), (x0 + w - 14, y0 + h - 14)],
               fill=RED, width=5)
        d.polygon([(x0 + w - 14, y0 + h - 14), (x0 + w - 30, y0 + h - 14),
                   (x0 + w - 14, y0 + h - 30)], fill=RED)
    elif kind == "chip":
        d.rectangle(box, fill=CARD)
        d.rectangle([cx - 26, cy - 22, cx + 26, cy + 22], fill=NAVY)
        d.rectangle([cx - 14, cy - 11, cx + 14, cy + 11], fill=(212, 175, 55))
        for dx in (-26, 0, 26):
            d.line([(cx + dx, y0 + 8), (cx + dx, cy - 22)], fill=INK, width=3)
            d.line([(cx + dx, cy + 22), (cx + dx, y0 + h - 8)], fill=INK, width=3)
    elif kind == "tanker":
        d.rectangle(box, fill=TEAL)
        d.polygon([(x0 + 18, cy + 12), (x0 + w - 18, cy + 12),
                   (x0 + w - 30, cy + 26), (x0 + 30, cy + 26)], fill=(30, 30, 34))
        d.rectangle([x0 + 52, cy - 12, x0 + 76, cy + 12], fill=(30, 30, 34))
        d.rectangle([x0 + 110, cy - 20, x0 + 118, cy + 12], fill=(30, 30, 34))
        d.ellipse([x0 + 130, cy - 30, x0 + 160, cy - 2], fill=(214, 96, 32))
    else:  # cricket
        d.rectangle(box, fill=GREEN)
        d.polygon([(cx - 34, cy + 24), (cx + 6, cy - 26), (cx + 20, cy - 18),
                   (cx - 18, cy + 30)], fill=(222, 196, 138))
        d.ellipse([cx + 22, cy - 26, cx + 38, cy - 10], fill=(178, 34, 34))


def kicker_tag(d, x, y, num, label, source=None):
    """Numbered red badge + red kicker label; optional source tag at right."""
    badge = 20
    d.rectangle([x, y, x + badge, y + badge], fill=RED)
    f_num = font(SANS_B, 13)
    tw = d.textlength(str(num), font=f_num)
    d.text((x + (badge - tw) / 2, y + 3), str(num), font=f_num, fill=(255, 255, 255))
    f_lab = font(SANS_B, 15)
    d.text((x + badge + 7, y + 2), label, font=f_lab, fill=RED)
    if source:
        f_src = font(SANS_B, 11)
        sw = d.textlength(source, font=f_src)
        d.text((x + 532 - sw, y + 4), source, font=f_src, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 24                      # side margin
    RX = W - MX                  # right edge (1000)

    # ---- kicker line -------------------------------------------------
    f_kick = font(SANS_B, 18)
    d.text((MX, 10), "ONE DAY OF WORLD NEWS, ONE PICTURE", font=f_kick, fill=RED)
    right = "23 STORIES  •  6 REGIONS  •  8 FIELDS"
    d.text((RX - d.textlength(right, font=f_kick), 10), right,
           font=f_kick, fill=INK)

    # ---- masthead ----------------------------------------------------
    mast = "Wednesday 25 November 2026"
    f_mast = fit_text(d, mast, SERIF_B, RX - MX, 80)
    mw = d.textlength(mast, font=f_mast)
    d.text(((W - mw) / 2, 36), mast, font=f_mast, fill=INK)
    d.line([(MX, 122), (RX, 122)], fill=INK, width=3)

    # ---- black ticker ------------------------------------------------
    d.rectangle([MX, 128, RX, 158], fill=INK)
    tick = ("UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA  •  "
            "HOUTHIS HIT RIYADH'S TALLEST TOWER  •  NATO JETS FOR POLAND")
    f_tick = fit_text(d, tick, SANS_B, RX - MX - 16, 19)
    tw = d.textlength(tick, font=f_tick)
    d.text(((W - tw) / 2, 136), tick, font=f_tick, fill=(255, 255, 255))

    # ---- LEAD 1 (hero, left, wide) ----------------------------------
    LX0, LX1 = MX, 556
    hero = photo_panel(os.path.join(ASSETS, "media-generation-hero-naval-0-da552f64-d7b3-47bc-a847-ed3654b4c5c0.png"),
                       (LX0, 166, LX1, 356), "ship")
    img.paste(hero, (LX0, 166))
    d.rectangle([LX0, 166, LX1, 356], outline=INK, width=2)
    d.rectangle([LX0, 166, LX0 + 150, 188], fill=RED)
    f_cap = font(SANS_B, 13)
    d.text((LX0 + 8, 171), "BENGHAZI  •  LIBYA", font=f_cap, fill=(255, 255, 255))
    kicker_tag(d, LX0, 364, 1, "UKRAINE  •  SEA WAR")
    f_src = font(SANS_B, 11)
    src = "CONFIRMED  •  REUTERS, RFE/RL"
    d.text((LX1 - d.textlength(src, font=f_src), 368), src, font=f_src, fill=GREY)
    f_h1 = font(SERIF_B, 35)
    head1 = "Zelenskiy confirms Ukraine sank Russian warship off Libya"
    for i, ln in enumerate(wrap(d, head1, f_h1, LX1 - LX0)):
        d.text((LX0, 390 + i * 41), ln, font=f_h1, fill=INK)
    f_deck = font(SERIF, 19)
    deck1 = ("Kyiv: two Russian vessels struck off the Libyan coast — one "
             "sunk in Benghazi harbour — and a cargo ship hit in the Gulf "
             "of Finland.")
    for i, ln in enumerate(wrap(d, deck1, f_deck, LX1 - LX0)[:2]):
        d.text((LX0, 492 + i * 23), ln, font=f_deck, fill=INK)

    # ---- LEADS 2 & 3 (stacked, right) -------------------------------
    def side_lead(y0, y1, num, label, source, img_path, kind, headline, deck):
        x0, x1 = 572, RX
        tw_ = 168
        thumb = photo_panel(img_path, (x0, y0, x0 + tw_, y1), kind)
        img.paste(thumb, (x0, y0))
        d.rectangle([x0, y0, x0 + tw_, y1], outline=INK, width=2)
        tx = x0 + tw_ + 12
        twd = x1 - tx
        kicker_tag(d, tx, y0 + 2, num, label)
        f_h = font(SERIF_B, 25)
        lines = wrap(d, headline, f_h, twd)
        for i, ln in enumerate(lines[:3]):
            d.text((tx, y0 + 28 + i * 30), ln, font=f_h, fill=INK)
        f_dk = font(SERIF, 16)
        dy = y0 + 28 + min(len(lines), 3) * 30 + 4
        for i, ln in enumerate(wrap(d, deck, f_dk, twd)[:2]):
            d.text((tx, dy + i * 20), ln, font=f_dk, fill=(60, 60, 60))
        f_sr = font(SANS_B, 11)
        d.text((tx, y1 - 16), source, font=f_sr, fill=GREY)

    side_lead(166, 352, 2, "MIDDLE EAST", "SAUDI CIVIL DEFENCE  •  REUTERS",
              os.path.join(ASSETS, "media-generation-thumb-riyadh-0-773bb5ce-80d2-4f60-8fc2-957f47647b1a.png"),
              "tower",
              "Houthis hit Riyadh's tallest tower; 11 wounded",
              "Drone strike on the capital's tallest tower; Saudi-led "
              "coalition condemns a \u201cterrorist attack\u201d.")
    side_lead(362, 548, 3, "EUROPE", "REPORTED  •  MULTIPLE OUTLETS",
              os.path.join(ASSETS, "media-generation-thumb-awacs-0-e5325143-db9b-46e4-8b54-d0389cd99a92.png"),
              "plane",
              "NATO to send early-warning jets to Poland",
              "Move follows missiles landing in Poland during an attack "
              "on Ukraine.")

    d.line([(MX, 560), (RX, 560)], fill=INK, width=2)

    # ---- ROW 2: five small stories ----------------------------------
    row2 = [
        (4, "UNITED STATES", "medal",
         "Trump gives Giuliani the Medal of Freedom",
         "WHITE HOUSE  •  AP"),
        (5, "MARKETS", "chart",
         "Anthropic shares fall below $83 IPO price",
         "NEARLY $200BN OF VALUE LOST"),
        (6, "TECH", "chip",
         "Huawei guilty of stealing trade secrets",
         "ACQUITTED OF RACKETEERING"),
        (7, "MIDDLE EAST", "tanker",
         "Three tankers hit by mines in Hormuz strait",
         "IRAN'S GUARD NAVY CLAIM"),
        (8, "SPORT", "cricket",
         "England beat Australia in 2nd T20I",
         "ENGLAND CHASE 185"),
    ]
    col_w, gap = 188, 8
    y0 = 570
    for i, (num, label, kind, head, src) in enumerate(row2):
        x0 = MX + i * (col_w + gap)
        x1 = x0 + col_w
        flat_icon(d, kind, (x0, y0, x1, y0 + 74))
        d.rectangle([x0, y0, x1, y0 + 74], outline=INK, width=1)
        kicker_tag(d, x0, y0 + 82, num, label)
        f_h = font(SERIF_B, 18)
        lines = wrap(d, head, f_h, col_w)
        for j, ln in enumerate(lines[:3]):
            d.text((x0, y0 + 106 + j * 22), ln, font=f_h, fill=INK)
        f_s = font(SANS_B, 10)
        sy = y0 + 106 + min(len(lines), 3) * 22 + 2
        for j, ln in enumerate(wrap(d, src, f_s, col_w)[:2]):
            d.text((x0, sy + j * 13), ln, font=f_s, fill=GREY)
        if i < 4:
            d.line([(x1 + 4, y0), (x1 + 4, y0 + 172)], fill=(200, 195, 185), width=1)

    # ---- ALSO ON ------------------------------------------------------
    d.line([(MX, 756), (RX, 756)], fill=INK, width=2)
    f_also = font(SANS_B, 21)
    d.text((MX, 764), "ALSO ON WEDNESDAY 25 NOVEMBER", font=f_also, fill=RED)
    d.text((RX - d.textlength("15 MORE STORIES", font=f_also), 764),
           "15 MORE STORIES", font=f_also, fill=INK)
    briefs = [
        "Putin: retaliation \u201cinevitable\u201d after Ukraine hit Russian oil plants",
        "Russia, Ukraine trade accusations at the UN over Black Sea shipping",
        "EU announces further sanctions on Russia",
        "Libya: Russian ship sinking stirs frozen-conflict fears",
        "UN warns over Gaza hardship for civilians seeking aid",
        "Iraq orders Kurdish oilfields under federal control; Kurds reject",
        "US envoy \u201cnot certain\u201d Israel military aid ends this year",
        "Trump set to unveil new tariffs after factory-capacity probe",
        "CIA, ODNI hit by cyber breach, US sources say",
        "Trump pardons Thanksgiving turkeys Freedom and Feathers",
        "Fort Hood gunman Hasan seeks stay of execution",
        "Sarkozy corruption case sent to trial; hearing 1 Apr 2027",
        "Sweden votes on Kristersson staying as prime minister",
        "BJP, Akali Dal reunite for Punjab 2027 polls",
        "Today: International Day against Violence against Women",
    ]
    f_br = font(SANS, 15)
    f_brb = font(SANS_B, 15)
    cols, rows = 3, 5
    colw = (RX - MX - (cols - 1) * 16) // cols
    for idx, text in enumerate(briefs):
        c, r = idx % cols, idx // cols
        bx = MX + c * (colw + 16)
        by = 794 + r * 34
        n = str(9 + idx)
        d.text((bx, by), n, font=f_brb, fill=RED)
        nw = d.textlength(n + "  ", font=f_brb)
        for j, ln in enumerate(wrap(d, text, f_br, colw - int(nw))[:2]):
            d.text((bx + nw, by + j * 17), ln, font=f_br, fill=INK)

    # ---- DATE CHECK ---------------------------------------------------
    d.rectangle([MX, 968, RX, 1000], fill=LIGHTRED, outline=RED, width=1)
    d.rectangle([MX, 968, MX + 104, 1000], fill=RED)
    f_dc = font(SANS_B, 14)
    d.text((MX + 8, 977), "DATE CHECK", font=f_dc, fill=(255, 255, 255))
    f_dct = font(SANS, 13)
    dct = ("Left out on purpose, first reported before Wednesday: COP31's collapse "
           "(Sun 23 Nov)  •  GTA 6's release (19 Nov)  •  Nepal PM's India visit "
           "(22\u201323 Nov). Gulf of Finland strike happened Saturday \u2014 "
           "today's news is Zelenskiy's confirmation.")
    for j, ln in enumerate(wrap(d, dct, f_dct, RX - MX - 120)[:2]):
        d.text((MX + 114, 971 + j * 15), ln, font=f_dct, fill=INK)

    # ---- footer -------------------------------------------------------
    f_ft = font(SANS, 12)
    foot = ("Every story happened or was first reported on Wed 25 Nov 2026  •  "
            "Sources: Reuters, RFE/RL, BBC, AP, Al Jazeera  •  "
            "Illustrations made for this page")
    fw = d.textlength(foot, font=f_ft)
    d.text(((W - fw) / 2, 1006), foot, font=f_ft, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
