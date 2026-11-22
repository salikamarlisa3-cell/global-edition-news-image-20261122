#!/usr/bin/env python3
"""The Global Edition - 22 November 2026. One-image world-news poster.

Written fresh in this session (2026-11-22). Deterministic: no timestamps,
no randomness, no network calls. Run: python3 main.py -> entry.png 1024x1024.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
MUTED = (90, 86, 76)
RED = (179, 39, 30)
BLUE = (29, 78, 137)
GOLD = (176, 124, 24)
TEAL = (14, 110, 110)
GREEN = (46, 110, 46)
PURPLE = (96, 66, 140)
ORANGE = (196, 94, 10)
CARD = (255, 255, 255)
LINE = (200, 192, 172)
MAPDOT = (52, 52, 52)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt, max_w, ellipsis="\u2026"):
    """Truncate one line to max width."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + ellipsis, font=fnt) > max_w:
        text = text[:-1]
    return text + ellipsis


# ---------------------------------------------------------------- stories
# (number, headline, outlet) - every item published/reported in the
# 22 Nov 2026 news cycle (21 Nov 00:00 UTC -> 22 Nov 02:00 UTC). See SOURCES.md.
REGIONS = [
    ("NORTH AMERICA", RED, [
        (1, "Trump seeks permanent Iran deal: \u201cthey break the deal\u201d", "FOX/AJP"),
        (2, "Trump vows to cap credit-card rates at 10%", "AP"),
        (3, "FBI probes hack of key crime database", "AP"),
        (4, "Virginia\u2019s first measles death of 2026: a child", "AP"),
        (5, "San Francisco braces for massive king tides", "AP"),
        (6, "Mets, A.J. Ewing agree $95m, 8-year deal", "AP"),
        (7, "Herro\u2019s career-high 50 not enough as Bucks lose", "AP"),
        (8, "Watkins: 36 pts, 6 steals as No. 4 USC beats Baylor", "AP"),
    ]),
    ("LATIN AMERICA", ORANGE, [
        (9, "Mexico captures cartel boss \u2018El Chapo Isidro\u2019", "AP"),
        (10, "Peru quake 6.7: moviegoers flee cinemas", "AL JAZEERA"),
        (11, "Peru quake toll: 15 hurt, 152 homes uninhabitable", "RIO TIMES"),
        (12, "Brazil town clears rubble after deadly storm", "AFP"),
        (13, "Bolsonaro in intensive care, bowel obstruction", "AL JAZEERA"),
        (14, "US signs new military deal with Venezuela", "REUTERS"),
        (15, "Migrant caravans test Mexico after US vote", "RIO TIMES"),
        (16, "Lula: fiscal bill \u201can adjustment, not a reform\u201d", "RIO TIMES"),
    ]),
    ("EUROPE", BLUE, [
        (17, "Berlin coalition vows united front to push Moscow", "DW"),
        (18, "Denmark expels Russian attach\u00e9 over \u2018rapper plot\u2019", "AL JAZEERA"),
        (19, "Russian missiles land in Poland near NATO exercise", "BBC/AP"),
        (20, "Finland probes suspected Russian helicopter incursion", "WIRE"),
        (21, "NATO jets over Estonia as drone threat grows", "WIRE"),
        (22, "Meloni shocked as ex-police chief found dead", "AP"),
        (23, "France: sixth Saturday of cost-of-living rallies", "AFP"),
        (24, "Man City\u2019s 14-year run vs Fulham ends in draw", "AP"),
    ]),
    ("MIDDLE EAST", PURPLE, [
        (25, "Iran hits US bases in Bahrain with missiles, drones", "AL JAZEERA"),
        (26, "Bahrain: Iranian attack sets industrial site ablaze", "AL JAZEERA"),
        (27, "Iran strikes 3 tankers, shows off missile launchers", "AP"),
        (28, "Tanker ablaze after hitting mine in Hormuz", "WIRE"),
        (29, "Aoun: Israel out \u201cof every inch\u201d; Iran era over", "AL JAZEERA"),
        (30, "Israeli strike kills 3 in Gaza aid car, witnesses say", "WIRE"),
        (31, "Man shot dead by West Bank settler guards", "AFP"),
        (32, "US warns airlines of al-Qaeda hijack calls", "WIRE"),
    ]),
    ("AFRICA", GREEN, [
        (33, "24 dead as boat capsizes en route to funeral", "AP"),
        (34, "Mlambo-Ngcuka, ex-SA deputy president, dies at 71", "AP"),
        (35, "Sudan alliance seizes key Bau region in Blue Nile", "WIRE"),
        (36, "Ebola fight in DR Congo hit by violence, distrust", "AFP"),
        (37, "Motsepe backs Infantino as CAF chief", "AFP"),
        (38, "Kenyan girl, 8, takes climate plea to COP31", "RNZ"),
        (39, "Kenya awards minerals deal to US consortium", "BBC"),
        (40, "Egypt secures $2.3bn IMF deal", "AFRICANEWS"),
    ]),
    ("ASIA", TEAL, [
        (41, "ICJ: Myanmar guilty of Rohingya genocide", "DEMOCRACY NOW!"),
        (42, "Trump tells Nvidia to reinstate \u2018brilliant\u2019 Huang", "AL JAZEERA"),
        (43, "SEC reviewing Nvidia accounting; shares -14%", "KIMKJ"),
        (44, "Anthropic -9% a day after IPO; Nasdaq -5.28%", "KIMKJ"),
        (45, "Riemann proof claimed with Claude; rival draft", "KIMKJ/AP"),
        (46, "China Mobile buys 52,160 AI accelerator cards", "KIMKJ"),
        (47, "Toxic alcohol kills 11, sickens 180 in Manipur", "WIRE"),
        (48, "Pakistan drop ex-captains Rizwan and Masood", "AFP"),
    ]),
    ("OCEANIA", (150, 90, 20), [
        (49, "Fred Nile, NSW political figurehead, dies at 92", "GUARDIAN"),
        (50, "Victoria power at risk as Yallourn closure nears", "GUARDIAN"),
        (51, "Red crabs begin annual Christmas Island march", "WIRE"),
        (52, "Tonga declares emergency as El Ni\u00f1o drought bites", "RNZ"),
        (53, "Philippines, Australia update defence pact", "WIRE"),
        (54, "Marianas groups query US training consultation", "RNZ"),
        (55, "Vanuatu warns world on fossil fuels at COP31", "RNZ"),
        (56, "Boy, 12, among arrests after car hits NT police home", "ABC"),
    ]),
]

LEADS = [
    ("1", "IRAN STRIKES US BASES IN BAHRAIN",
     "IRGC missiles and drones hit al-Riffa and Awali; Bahrain says an "
     "industrial facility caught fire. Washington weighs its response.",
     "AL JAZEERA \u00b7 21 NOV", "missile"),
    ("2", "WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
     "The ICJ finds Myanmar committed genocide against the Rohingya \u2014 "
     "the first time any court has found a state guilty of genocide.",
     "DEMOCRACY NOW! \u00b7 21\u201322 NOV", "court"),
    ("3", "PERU QUAKE 6.7 RATTLES THE ANDES",
     "Moviegoers flee cinemas as the tremor hits; 15 hurt and 152 homes "
     "left uninhabitable in the revised count.",
     "AL JAZEERA \u00b7 22 NOV", "quake"),
]

# 13 feature tiles: (story number, caption, scene)
TILES = [
    (43, "Nvidia", "chip"), (44, "Anthropic", "chart"), (45, "Riemann", "pi"),
    (9, "Chapo", "cuffs"), (12, "Brazil storm", "storm"), (17, "Berlin", "flags"),
    (19, "Poland", "warn"), (27, "Hormuz", "tanker"), (33, "Nigeria boat", "boat"),
    (34, "Mlambo", "candle"), (39, "Kenya minerals", "gem"),
    (51, "Red crabs", "crab"), (49, "Fred Nile", "portrait"),
]

TIMELINE = [
    ("\u224805:15", "Virginia reports its first measles death of 2026", "AP"),
    ("\u224806:15", "FBI probes hack of its crime database; 24 dead in Nigeria boat capsize", "AP"),
    ("\u224807:30", "UN talks on autonomous weapons end with no firm rules", "WIRE"),
    ("\u224807:50", "Trump tells Fox News he wants a permanent Iran deal", "FOX/AJP"),
    ("\u224809:15", "Peru quake toll revised: 152 homes uninhabitable", "WIRE"),
    ("\u224810:30", "France rallies for a sixth Saturday over living costs", "AFP"),
]

NUMBERS = [
    ("6.7", "magnitude of the Peru quake"),
    ("24", "dead in the Nigeria boat capsize"),
    ("-14%", "Nvidia shares in a single day"),
    ("-5.28%", "Nasdaq, wiping out its 2026 gains"),
    ("-9%", "Anthropic a day after its IPO"),
    ("152", "homes uninhabitable after the quake"),
]

# Open-Meteo forecast API, 22 Nov 2026 (high / low, deg C)
WEATHER = [
    ("NEW YORK", "18\u00b0", "11\u00b0"), ("MEXICO CITY", "24\u00b0", "13\u00b0"),
    ("LONDON", "9\u00b0", "6\u00b0"), ("DUBAI", "30\u00b0", "24\u00b0"),
    ("LAGOS", "31\u00b0", "27\u00b0"), ("TOKYO", "13\u00b0", "4\u00b0"),
    ("SYDNEY", "31\u00b0", "23\u00b0"),
]

# land cells: (row, col_start, col_end) on a 72 x 30 equirectangular grid
# lon -180..180 (5 deg/col), lat 75..-55 (4.5 deg/row)
LAND = [
    (0, 15, 18), (0, 44, 52),
    (1, 2, 5), (1, 15, 18), (1, 36, 39), (1, 44, 68),
    (2, 3, 14), (2, 15, 17), (2, 34, 34), (2, 36, 39), (2, 44, 68),
    (3, 4, 14), (3, 34, 34), (3, 35, 42), (3, 44, 66),
    (4, 5, 14), (4, 35, 42), (4, 46, 56), (4, 66, 68),
    (5, 6, 14), (5, 35, 42), (5, 42, 47), (5, 46, 56), (5, 56, 63), (5, 66, 68),
    (6, 6, 13), (6, 34, 36), (6, 39, 41), (6, 42, 47), (6, 50, 53), (6, 56, 63),
    (7, 7, 12), (7, 35, 44), (7, 43, 46), (7, 50, 53), (7, 56, 62),
    (8, 7, 11), (8, 35, 44), (8, 43, 46), (8, 50, 53), (8, 58, 62),
    (9, 8, 11), (9, 35, 44), (9, 50, 52), (9, 58, 62),
    (10, 10, 12), (10, 36, 43), (10, 59, 66),
    (11, 13, 17), (11, 38, 43), (11, 59, 64),
    (12, 14, 17), (12, 38, 43), (12, 62, 69),
    (13, 14, 18), (13, 38, 43), (13, 62, 69),
    (14, 15, 18), (14, 38, 43), (14, 62, 69),
    (15, 15, 18), (15, 39, 42), (15, 62, 68),
    (16, 16, 18), (16, 39, 41), (16, 69, 70),
    (17, 16, 18), (17, 69, 70),
    (18, 17, 17),
    (19, 17, 17),
]

# region colour per grid cell: (row range, col range) -> region index
def region_of(r, c):
    if r <= 9 and c <= 18:
        return 0  # North America
    if r >= 10 and c <= 19:
        return 1  # Latin America
    if r <= 6 and 34 <= c <= 42:
        return 2  # Europe
    if 5 <= r <= 8 and 42 <= c <= 47:
        return 3  # Middle East
    if 7 <= r <= 16 and 35 <= c <= 45:
        return 4  # Africa
    if r <= 10 and c >= 46:
        return 5  # Asia
    if r >= 11 and c >= 59:
        return 6  # Oceania
    return 5


PINS = [  # (region index, grid row, grid col)
    (0, 4, 9), (1, 14, 16), (2, 3, 38), (3, 6, 44),
    (4, 11, 40), (5, 4, 57), (6, 13, 65),
]


# ---------------------------------------------------------------- scenes
def draw_scene(d, kind, x, y, w, h):
    """Small vector illustration inside box (x, y, w, h)."""
    cx, cy = x + w // 2, y + h // 2
    if kind == "missile":
        d.rectangle([x, y, x + w, y + h], fill=(24, 32, 48))
        d.ellipse([x + 8, y + h - 26, x + 30, y + h - 4], fill=(60, 70, 90))
        d.ellipse([x + w - 30, y + h - 26, x + w - 8, y + h - 4], fill=(60, 70, 90))
        d.arc([x + 10, y + 6, x + w - 10, y + h - 6], 200, 340, fill=(255, 190, 60), width=3)
        d.arc([x + 22, y + 14, x + w - 22, y + h - 14], 200, 340, fill=(255, 120, 40), width=2)
        d.polygon([(cx - 4, y + 16), (cx + 4, y + 16), (cx, y + 4)], fill=(255, 210, 90))
        d.ellipse([cx - 3, y + 14, cx + 3, y + 20], fill=(255, 210, 90))
        d.line([x + 6, y + h - 12, x + w - 6, y + h - 12], fill=(90, 120, 160), width=2)
    elif kind == "court":
        d.rectangle([x, y, x + w, y + h], fill=(38, 52, 74))
        d.polygon([(x + 6, y + 22), (cx, y + 6), (x + w - 6, y + 22)], fill=(214, 186, 120))
        for i in range(4):
            px = x + 14 + i * ((w - 28) // 3)
            d.rectangle([px, y + 24, px + 6, y + h - 22], fill=(226, 214, 180))
        d.rectangle([x + 8, y + h - 22, x + w - 8, y + h - 16], fill=(214, 186, 120))
        d.rectangle([x + 8, y + h - 14, x + w - 8, y + h - 8], fill=(180, 150, 90))
        d.ellipse([cx - 16, y + h - 46, cx + 16, y + h - 30], fill=(150, 90, 50))
        d.rectangle([cx - 3, y + h - 58, cx + 3, y + h - 44], fill=(120, 70, 40))
    elif kind == "quake":
        d.rectangle([x, y, x + w, y + h], fill=(58, 48, 40))
        for i, bh in enumerate([34, 52, 42, 58]):
            bx = x + 10 + i * ((w - 20) // 4)
            d.rectangle([bx, y + h - 26 - bh, bx + (w - 20) // 4 - 4, y + h - 26],
                        fill=(120, 104, 88))
            d.rectangle([bx, y + h - 26 - bh, bx + (w - 20) // 4 - 4, y + h - 26 - bh + 5],
                        fill=(150, 132, 110))
        d.polygon([(x + 4, y + h - 26), (x + w // 3, y + h - 12),
                   (x + w // 2, y + h - 26), (x + 2 * w // 3, y + h - 8),
                   (x + w - 4, y + h - 26), (x + w - 4, y + h - 4),
                   (x + 4, y + h - 4)], fill=(30, 24, 18))
        d.line([x + 6, y + 10, x + w // 4, y + 18, x + w // 2, y + 6,
                x + 3 * w // 4, y + 20, x + w - 6, y + 10], fill=(255, 90, 60), width=2)
    elif kind == "chip":
        d.rectangle([x, y, x + w, y + h], fill=(16, 40, 60))
        d.rectangle([x + w // 2 - 14, y + h // 2 - 14, x + w // 2 + 14, y + h // 2 + 14],
                    fill=(30, 120, 120), outline=(140, 220, 220), width=2)
        for i in range(4):
            d.line([x + w // 2 - 14 + i * 9, y + 4, x + w // 2 - 14 + i * 9, y + h // 2 - 14],
                   fill=(140, 220, 220), width=2)
            d.line([x + w // 2 - 14 + i * 9, y + h // 2 + 14, x + w // 2 - 14 + i * 9, y + h - 4],
                   fill=(140, 220, 220), width=2)
    elif kind == "chart":
        d.rectangle([x, y, x + w, y + h], fill=(20, 26, 40))
        d.line([x + 8, y + 12, x + w // 3, y + 22, x + w // 2, y + 16,
                x + 2 * w // 3, y + 34, x + w - 8, y + h - 12], fill=(255, 80, 60), width=3)
        d.polygon([(x + w - 16, y + h - 20), (x + w - 6, y + h - 12), (x + w - 16, y + h - 6)],
                  fill=(255, 80, 60))
        for i in range(4):
            d.line([x + 10 + i * 14, y + h - 8, x + 10 + i * 14, y + h - 8 - (i + 1) * 4],
                   fill=(90, 140, 200), width=5)
    elif kind == "pi":
        d.rectangle([x, y, x + w, y + h], fill=(40, 28, 60))
        d.text((cx - 16, cy - 20), "\u03c0", fill=(255, 220, 120),
               font=font(FB, 40))
        d.text((cx + 12, cy + 8), "=?", fill=(255, 255, 255), font=font(FB, 14))
    elif kind == "cuffs":
        d.rectangle([x, y, x + w, y + h], fill=(52, 52, 58))
        d.ellipse([x + 8, cy - 14, x + 30, cy + 8], outline=(200, 200, 210), width=4)
        d.ellipse([x + w - 30, cy - 14, x + w - 8, cy + 8], outline=(200, 200, 210), width=4)
        d.line([x + 30, cy - 3, x + w - 30, cy - 3], fill=(200, 200, 210), width=3)
    elif kind == "storm":
        d.rectangle([x, y, x + w, y + h], fill=(48, 56, 72))
        d.ellipse([x + 10, cy - 12, x + 34, cy + 6], fill=(200, 205, 215))
        d.ellipse([x + 26, cy - 18, x + 54, cy + 6], fill=(220, 224, 232))
        d.line([x + 22, cy + 10, x + 16, cy + 24], fill=(255, 220, 60), width=3)
        d.line([x + 34, cy + 10, x + 28, cy + 24], fill=(255, 220, 60), width=3)
        d.line([x + 46, cy + 10, x + 40, cy + 24], fill=(255, 220, 60), width=3)
    elif kind == "flags":
        d.rectangle([x, y, x + w, y + h], fill=(30, 44, 80))
        for i, col in enumerate([(255, 210, 60), (200, 40, 40), (40, 90, 200), (40, 160, 80)]):
            fx = x + 10 + i * ((w - 20) // 4)
            d.line([fx, y + 8, fx, y + h - 8], fill=(220, 220, 220), width=2)
            d.polygon([(fx, y + 8), (fx + (w - 20) // 4 - 2, y + 13), (fx, y + 18)], fill=col)
    elif kind == "warn":
        d.rectangle([x, y, x + w, y + h], fill=(60, 44, 16))
        d.polygon([(cx, y + 6), (x + w - 8, y + h - 8), (x + 8, y + h - 8)],
                  fill=(255, 200, 40), outline=(20, 20, 20))
        d.text((cx - 4, cy - 12), "!", fill=(20, 20, 20), font=font(FB, 26))
    elif kind == "tanker":
        d.rectangle([x, y, x + w, y + h], fill=(16, 48, 66))
        d.line([x + 4, y + h - 18, x + w - 4, y + h - 18], fill=(70, 140, 180), width=2)
        d.rectangle([x + 10, cy - 2, x + w - 10, cy + 12], fill=(180, 60, 40))
        d.rectangle([x + w - 26, cy - 14, x + w - 12, cy - 2], fill=(220, 220, 220))
        d.ellipse([cx - 14, cy - 18, cx - 4, cy - 8], fill=(255, 160, 50))
        d.ellipse([cx + 4, cy - 22, cx + 16, cy - 8], fill=(255, 120, 40))
    elif kind == "boat":
        d.rectangle([x, y, x + w, y + h], fill=(20, 60, 80))
        d.line([x + 4, y + h - 14, x + w - 4, y + h - 14], fill=(90, 160, 200), width=2)
        d.polygon([(x + 12, cy + 4), (x + w - 12, cy + 4), (x + w - 20, cy + 14),
                   (x + 20, cy + 14)], fill=(200, 140, 60))
        d.line([cx, cy + 4, cx, cy - 18], fill=(230, 230, 230), width=2)
        d.polygon([(cx, cy - 18), (cx + 16, cy - 10), (cx, cy - 2)], fill=(240, 240, 240))
    elif kind == "candle":
        d.rectangle([x, y, x + w, y + h], fill=(46, 40, 52))
        d.rectangle([cx - 6, cy - 4, cx + 6, cy + 18], fill=(240, 230, 200))
        d.ellipse([cx - 5, cy - 18, cx + 5, cy - 4], fill=(255, 200, 60))
        d.ellipse([cx - 2, cy - 14, cx + 2, cy - 8], fill=(255, 240, 160))
    elif kind == "gem":
        d.rectangle([x, y, x + w, y + h], fill=(24, 52, 40))
        d.polygon([(cx, y + 8), (x + w - 10, cy), (cx, y + h - 8), (x + 10, cy)],
                  fill=(90, 200, 220), outline=(220, 250, 250))
        d.line([x + 10, cy, x + w - 10, cy], fill=(220, 250, 250), width=2)
        d.line([cx, y + 8, cx, y + h - 8], fill=(220, 250, 250), width=2)
    elif kind == "crab":
        d.rectangle([x, y, x + w, y + h], fill=(120, 40, 30))
        d.ellipse([cx - 16, cy - 10, cx + 16, cy + 12], fill=(220, 70, 40))
        for i in range(3):
            d.line([cx - 16, cy - 4 + i * 6, x + 6, cy - 10 + i * 8], fill=(220, 70, 40), width=3)
            d.line([cx + 16, cy - 4 + i * 6, x + w - 6, cy - 10 + i * 8], fill=(220, 70, 40), width=3)
        d.ellipse([cx - 10, cy - 14, cx - 2, cy - 6], fill=(255, 255, 255))
        d.ellipse([cx + 2, cy - 14, cx + 10, cy - 6], fill=(255, 255, 255))
    elif kind == "portrait":
        d.rectangle([x, y, x + w, y + h], fill=(70, 60, 50))
        d.ellipse([cx - 12, cy - 18, cx + 12, cy + 6], fill=(210, 180, 150))
        d.polygon([(cx - 20, y + h - 6), (cx - 12, cy + 8), (cx + 12, cy + 8),
                   (cx + 20, y + h - 6)], fill=(40, 60, 90))


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 14
    CW = W - 2 * MX  # 996

    # ---- header
    d.rectangle([0, 0, W, 74], fill=INK)
    d.text((MX, 8), "THE GLOBAL EDITION", fill=(247, 243, 232), font=font(FB, 34))
    d.text((MX, 50), "SUNDAY 22 NOVEMBER 2026  \u00b7  THE WHOLE WORLD IN ONE IMAGE",
           fill=(200, 190, 160), font=font(FB, 13))
    d.text((W - MX, 12), "56 STORIES", fill=(255, 210, 90), font=font(FB, 20),
           anchor="ra")
    d.text((W - MX, 40), "7 REGIONS \u00b7 ALL VERIFIED", fill=(200, 190, 160),
           font=font(FB, 12), anchor="ra")

    # ---- 3 lead panels
    ly, lh, lw, gap = 80, 152, 328, 6
    for i, (num, title, body, tag, scene) in enumerate(LEADS):
        x = MX + i * (lw + gap)
        d.rectangle([x, ly, x + lw, ly + lh], fill=CARD, outline=LINE, width=1)
        d.rectangle([x, ly, x + lw, ly + 4], fill=RED)
        draw_scene(d, scene, x + 6, ly + 10, 96, 62)
        d.text((x + 110, ly + 10), "LEAD " + num, fill=RED, font=font(FB, 11))
        for j, ln in enumerate(wrap(d, title, font(FB, 13), lw - 118)):
            d.text((x + 110, ly + 26 + j * 15), ln, fill=INK, font=font(FB, 13))
        for j, ln in enumerate(wrap(d, body, font(FR, 10), lw - 16)):
            d.text((x + 8, ly + 80 + j * 13), ln, fill=(50, 50, 50), font=font(FR, 10))
        d.text((x + 8, ly + lh - 16), tag, fill=MUTED, font=font(FB, 9))

    # ---- 13 feature tiles
    ty, th = 238, 80
    tw = 72
    tgap = (CW - 13 * tw) / 12
    d.text((MX, ty), "IN PICTURES \u2014 13 FEATURES", fill=INK, font=font(FB, 11))
    for i, (num, cap, scene) in enumerate(TILES):
        x = MX + i * (tw + tgap)
        draw_scene(d, scene, x, ty + 16, tw, 44)
        d.rectangle([x, ty + 16, x + 16, ty + 30], fill=RED)
        d.text((x + 8, ty + 17), str(num), fill=(255, 255, 255),
               font=font(FB, 9), anchor="mm")
        d.text((x + tw // 2, ty + 62), fit(d, cap, font(FB, 8), tw),
               fill=INK, font=font(FB, 8), anchor="ma")

    # ---- dot-matrix world map + region key
    my, mh = 324, 168
    map_x, map_w = MX, 646
    d.rectangle([map_x, my, map_x + map_w, my + mh], fill=CARD, outline=LINE, width=1)
    d.text((map_x + 8, my + 6), "THE WORLD, DOTTED \u2014 7 REGIONS, 56 STORIES",
           fill=INK, font=font(FB, 11))
    gx0, gy0 = map_x + 10, my + 26
    cell_w, cell_h = (map_w - 20) / 72, (mh - 34) / 30
    landset = set()
    for r, c0, c1 in LAND:
        for c in range(c0, c1 + 1):
            landset.add((r, c))
    for (r, c) in sorted(landset):
        px = gx0 + c * cell_w + cell_w / 2
        py = gy0 + r * cell_h + cell_h / 2
        col = REGIONS[region_of(r, c)][1]
        d.ellipse([px - 2.1, py - 2.1, px + 2.1, py + 2.1], fill=col)
    for idx, gr, gc in PINS:
        px = gx0 + gc * cell_w + cell_w / 2
        py = gy0 + gr * cell_h + cell_h / 2
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=2)
        d.text((px, py), str(idx + 1), fill=(255, 255, 255), font=font(FB, 10),
               anchor="mm")
    # region key
    kx = map_x + map_w + 10
    kw = W - MX - kx
    d.rectangle([kx, my, kx + kw, my + mh], fill=CARD, outline=LINE, width=1)
    d.text((kx + 10, my + 6), "REGION KEY", fill=INK, font=font(FB, 11))
    for i, (name, col, stories) in enumerate(REGIONS):
        yy = my + 26 + i * 19
        d.rectangle([kx + 10, yy, kx + 24, yy + 12], fill=col)
        d.text((kx + 28, yy - 1), f"{i + 1}  {name}", fill=INK, font=font(FB, 10))
        d.text((kx + kw - 8, yy - 1), "8", fill=MUTED, font=font(FB, 10), anchor="ra")
    d.text((kx + 10, my + mh - 16), "Dots = land \u00b7 pins = regions",
           fill=MUTED, font=font(FR, 9))

    # ---- UTC timeline strip
    tly, tlh = 498, 36
    d.rectangle([MX, tly, MX + CW, tly + tlh], fill=INK)
    d.text((MX + 8, tly + 4), "THE DAY IN WIB \u2248", fill=(255, 210, 90), font=font(FB, 11))
    seg_w = (CW - 150) / 6
    for i, (tm, ev, _src) in enumerate(TIMELINE):
        x = MX + 150 + i * seg_w
        d.text((x, tly + 3), tm, fill=(255, 210, 90), font=font(FB, 9))
        for j, ln in enumerate(wrap(d, ev, font(FR, 8), seg_w - 8)):
            if j > 1:
                break
            d.text((x, tly + 15 + j * 10), ln, fill=(230, 225, 210), font=font(FR, 8))

    # ---- story grid: 7 region rows
    sy = 540
    row_h = 42
    for i, (name, col, stories) in enumerate(REGIONS):
        y = sy + i * row_h
        d.rectangle([MX, y, MX + 118, y + row_h - 2], fill=col)
        d.text((MX + 6, y + 3), f"{i + 1}", fill=(255, 255, 255), font=font(FB, 15))
        for j, ln in enumerate(wrap(d, name, font(FB, 9), 106)):
            d.text((MX + 6, y + 21 + j * 11), ln, fill=(255, 255, 255), font=font(FB, 9))
        col_w = (CW - 118 - 8) / 2
        for k, (num, head, outlet) in enumerate(stories):
            cc = k // 4
            rr = k % 4
            x = MX + 118 + 8 + cc * col_w
            yy = y + 1 + rr * 10.5
            d.text((x, yy), f"{num:>2}.", fill=col, font=font(FB, 9))
            d.text((x + 20, yy), fit(d, head, font(FR, 9), col_w - 20 - 68),
                   fill=INK, font=font(FR, 9))
            d.text((x + col_w - 2, yy), outlet, fill=MUTED, font=font(FB, 7),
                   anchor="ra")

    # ---- by-the-numbers strip
    ny, nh = 840, 56
    d.text((MX, ny), "BY THE NUMBERS", fill=INK, font=font(FB, 11))
    bw = CW / 6
    for i, (big, small) in enumerate(NUMBERS):
        x = MX + i * bw
        d.rectangle([x + 2, ny + 16, x + bw - 2, ny + nh], fill=CARD, outline=LINE, width=1)
        d.text((x + bw / 2, ny + 20), big, fill=RED, font=font(FB, 17), anchor="ma")
        for j, ln in enumerate(wrap(d, small, font(FR, 8), bw - 12)):
            d.text((x + bw / 2, ny + 38 + j * 9), ln, fill=(60, 60, 60),
                   font=font(FR, 8), anchor="ma")

    # ---- weather strip
    wy, wh = 902, 34
    d.rectangle([MX, wy, MX + CW, wy + wh], fill=(235, 230, 214))
    d.text((MX + 8, wy + 10), "WEATHER 22 NOV \u00b7 OPEN-METEO", fill=INK, font=font(FB, 10))
    ww = (CW - 210) / 7
    for i, (city, hi, lo) in enumerate(WEATHER):
        x = MX + 210 + i * ww
        d.text((x, wy + 4), city, fill=MUTED, font=font(FB, 8))
        d.text((x, wy + 16), f"{hi} / {lo}", fill=INK, font=font(FB, 11))

    # ---- left-out box + footer
    fy = 942
    d.rectangle([MX, fy, MX + 640, fy + 70], fill=(255, 255, 255), outline=LINE, width=1)
    d.text((MX + 8, fy + 5), "LEFT OUT & WHY \u2014 DATE CHECK", fill=RED, font=font(FB, 10))
    leftout = [
        "Shenzhen trilateral peace declaration (20 Nov) \u2014 covered in the 21 Nov edition; no new step today.",
        "GTA VI $3.79bn first-day record (20 Nov) \u2014 covered 21 Nov; no new figure today.",
        "Anthropic $81.3bn IPO debut (20 Nov) \u2014 covered 21 Nov; only the day-2 fall (-9%) is today\u2019s news.",
    ]
    for j, ln in enumerate(leftout):
        d.text((MX + 8, fy + 20 + j * 15), "\u2022 " + fit(d, ln, font(FR, 9), 624),
               fill=(60, 60, 60), font=font(FR, 9))
    fx = MX + 650
    d.text((fx, fy + 2), "SOURCES: full list with outlet + URL in SOURCES.md.",
           fill=INK, font=font(FB, 9))
    d.text((fx, fy + 16), "Just Security Early Edition for 22 Nov was not",
           fill=(60, 60, 60), font=font(FR, 9))
    d.text((fx, fy + 28), "published (weekday-only; latest: 20 Nov), so stories",
           fill=(60, 60, 60), font=font(FR, 9))
    d.text((fx, fy + 40), "were verified against Reuters, AP, BBC, Al Jazeera,",
           fill=(60, 60, 60), font=font(FR, 9))
    d.text((fx, fy + 52), "AFP, DW, RNZ, The Guardian and the wires.",
           fill=(60, 60, 60), font=font(FR, 9))
    d.text((W - MX, H - 8), "THE GLOBAL EDITION \u00b7 22 NOV 2026 \u00b7 PREPARED, NOT SUBMITTED",
           fill=MUTED, font=font(FB, 8), anchor="rb")

    img.save("entry.png", format="PNG")
    return img


if __name__ == "__main__":
    build()
    with open("entry.png", "rb") as f:
        print("sha256", hashlib.sha256(f.read()).hexdigest())
    print("size", Image.open("entry.png").size)
