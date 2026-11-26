#!/usr/bin/env python3
"""make.fun entry news-image-20261126: 26 November 2026 in one image.

Template v2 anatomy (winner study 2026-11-25) + 2026-11-26 improvements:
  * 40 stories (up from 36): 3 heroes + 10 illustrated + 27 one-liners.
  * WHY IT MATTERS line under each hero (from 20261125 rank-1 entry).
  * Fields strip under the strap (War/Trade/Markets counts).
Deterministic: no network, no randomness, no clock.
Run: python3 generate.py -> assets/entry.png (1024x1024)
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "entry.png")
W = H = 1024
FD = "/usr/share/fonts/truetype/dejavu"

PAPER = (248, 244, 235)
INK = (22, 22, 22)
NAVY = (18, 38, 66)
RED = (176, 32, 32)
BLUE = (28, 74, 118)
TEAL = (13, 108, 108)
GOLD = (172, 122, 20)
GREY = (96, 96, 96)
LIGHT = (234, 227, 212)
WHITE = (255, 255, 255)
GREEN = (28, 122, 52)
PURPLE = (92, 52, 140)
ORANGE = (196, 96, 20)

def f(name, s):
    return ImageFont.truetype(os.path.join(FD, name), s)

def sb(s): return f("DejaVuSerif-Bold.ttf", s)
def sr(s): return f("DejaVuSerif.ttf", s)
def nb(s): return f("DejaVuSans-Bold.ttf", s)
def nr(s): return f("DejaVuSans.ttf", s)

def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def lines(d, x, y, ls, fnt, fill, lead):
    for ln in ls:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lead
    return y

def badge(d, x, y, text, bg, fg=WHITE, size=11):
    fnt = nb(size)
    w = int(d.textlength(text, font=fnt)) + 12
    d.rectangle([x, y, x + w, y + size + 8], fill=bg)
    d.text((x + 6, y + 3), text, font=fnt, fill=fg)
    return w

def numdot(d, x, y, n, col=RED, r=11):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=col)
    d.text((x + r, y + r), str(n), font=nb(12), fill=WHITE, anchor="mm")

def ic_ship(d, x, y, s, c):
    d.polygon([(x, y+s*.55),(x+s, y+s*.55),(x+s*.85, y+s*.85),(x+s*.15, y+s*.85)], fill=c)
    d.line([(x+s*.5, y+s*.55),(x+s*.5, y+s*.12)], fill=c, width=4)
    d.polygon([(x+s*.5, y+s*.14),(x+s*.85, y+s*.42),(x+s*.5, y+s*.42)], fill=c)

def ic_tower(d, x, y, s, c):
    d.rectangle([x+s*.34, y+s*.28, x+s*.66, y+s*.92], fill=c)
    for yy in (.44, .58, .72):
        d.line([(x+s*.4, y+s*yy),(x+s*.6, y+s*yy)], fill=PAPER, width=3)
    d.polygon([(x+s*.5, y+s*.05),(x+s*.62, y+s*.24),(x+s*.5, y+s*.19),(x+s*.38, y+s*.24)], fill=c)

def ic_star(d, x, y, s, c):
    cx, cy, r = x+s/2, y+s/2, s*.44
    pts = []
    for i in range(10):
        a = math.radians(-90 + i*36); rr = r if i % 2 == 0 else r*.45
        pts.append((cx+rr*math.cos(a), cy+rr*math.sin(a)))
    d.polygon(pts, fill=c)

def ic_chip(d, x, y, s, c):
    d.rectangle([x+s*.24, y+s*.24, x+s*.76, y+s*.76], outline=c, width=4)
    d.rectangle([x+s*.42, y+s*.42, x+s*.58, y+s*.58], fill=c)
    for i in range(3):
        o = s*(.34+.16*i)
        d.line([(x+o, y+s*.08),(x+o, y+s*.24)], fill=c, width=3)
        d.line([(x+o, y+s*.76),(x+o, y+s*.92)], fill=c, width=3)
        d.line([(x+s*.08, y+o),(x+s*.24, y+o)], fill=c, width=3)
        d.line([(x+s*.76, y+o),(x+s*.92, y+o)], fill=c, width=3)

def ic_medal(d, x, y, s, c):
    cx, cy = x+s/2, y+s*.6
    d.line([(x+s*.3, y+s*.08),(cx, y+s*.32)], fill=c, width=5)
    d.line([(x+s*.7, y+s*.08),(cx, y+s*.32)], fill=c, width=5)
    d.ellipse([cx-s*.3, cy-s*.3, cx+s*.3, cy+s*.3], outline=c, width=5)
    d.text((cx, cy), "*", font=nb(int(s*.4)), fill=c, anchor="mm")

def ic_burst(d, x, y, s, c):
    cx, cy = x+s/2, y+s/2
    for k in range(8):
        a = math.radians(k*45)
        d.line([(cx+.18*s*math.cos(a), cy+.18*s*math.sin(a)),
                (cx+.42*s*math.cos(a), cy+.42*s*math.sin(a))], fill=c, width=5)
    d.ellipse([cx-s*.14, cy-s*.14, cx+s*.14, cy+s*.14], fill=c)

def ic_chart(d, x, y, s, c):
    d.line([(x+s*.12, y+s*.85),(x+s*.9, y+s*.85)], fill=c, width=4)
    pts = [(x+s*.15, y+s*.7),(x+s*.4, y+s*.45),(x+s*.6, y+s*.6),(x+s*.88, y+s*.2)]
    d.line(pts, fill=c, width=5)
    d.polygon([(x+s*.88, y+s*.2),(x+s*.74, y+s*.22),(x+s*.84, y+s*.34)], fill=c)

def ic_plane(d, x, y, s, c):
    d.polygon([(x+s*.05, y+s*.55),(x+s*.95, y+s*.3),(x+s*.7, y+s*.62),
               (x+s*.55, y+s*.9),(x+s*.45, y+s*.9),(x+s*.5, y+s*.62)], fill=c)

def ic_globe(d, x, y, s, c):
    d.ellipse([x+s*.08, y+s*.08, x+s*.92, y+s*.92], outline=c, width=4)
    d.ellipse([x+s*.34, y+s*.08, x+s*.66, y+s*.92], outline=c, width=3)
    d.line([(x+s*.08, y+s*.5),(x+s*.92, y+s*.5)], fill=c, width=3)

def ic_scale(d, x, y, s, c):
    d.line([(x+s*.5, y+s*.12),(x+s*.5, y+s*.8)], fill=c, width=4)
    d.line([(x+s*.15, y+s*.22),(x+s*.85, y+s*.22)], fill=c, width=4)
    for cx in (x+s*.15, x+s*.85):
        d.line([(cx, y+s*.22),(cx-s*.12, y+s*.45)], fill=c, width=3)
        d.line([(cx, y+s*.22),(cx+s*.12, y+s*.45)], fill=c, width=3)
        d.arc([cx-s*.13, y+s*.38, cx+s*.13, y+s*.58], 0, 180, fill=c, width=4)
    d.line([(x+s*.3, y+s*.86),(x+s*.7, y+s*.86)], fill=c, width=4)

def ic_rocket(d, x, y, s, c):
    d.polygon([(x+s*.5, y+s*.05),(x+s*.68, y+s*.4),(x+s*.68, y+s*.7),
               (x+s*.32, y+s*.7),(x+s*.32, y+s*.4)], fill=c)
    d.ellipse([x+s*.42, y+s*.34, x+s*.58, y+s*.5], fill=PAPER)
    d.polygon([(x+s*.32, y+s*.6),(x+s*.18, y+s*.85),(x+s*.32, y+s*.85)], fill=c)
    d.polygon([(x+s*.68, y+s*.6),(x+s*.82, y+s*.85),(x+s*.68, y+s*.85)], fill=c)
    d.polygon([(x+s*.42, y+s*.72),(x+s*.58, y+s*.72),(x+s*.5, y+s*.95)], fill=ORANGE)

def ic_trophy(d, x, y, s, c):
    d.polygon([(x+s*.28, y+s*.12),(x+s*.72, y+s*.12),(x+s*.66, y+s*.5),(x+s*.34, y+s*.5)], fill=c)
    d.arc([x+s*.12, y+s*.14, x+s*.34, y+s*.4], 90, 270, fill=c, width=4)
    d.arc([x+s*.66, y+s*.14, x+s*.88, y+s*.4], 270, 90, fill=c, width=4)
    d.rectangle([x+s*.44, y+s*.5, x+s*.56, y+s*.68], fill=c)
    d.rectangle([x+s*.3, y+s*.68, x+s*.7, y+s*.76], fill=c)

ICONS = {"ship": ic_ship, "tower": ic_tower, "star": ic_star, "chip": ic_chip,
         "medal": ic_medal, "burst": ic_burst, "chart": ic_chart,
         "plane": ic_plane, "globe": ic_globe, "scale": ic_scale,
         "rocket": ic_rocket, "trophy": ic_trophy}

VCOL = {"CONFIRMED": GREEN, "OFFICIAL": BLUE, "REPORTED": ORANGE,
        "CLAIM": RED, "ONGOING": PURPLE}

DATE_LINE = "Thursday 26 November 2026"
STRAP = ("Macy's 100th parade postponed  ·  Cairo tanker fire kills 31  ·  "
         "US proposes tariffs on 14")
FIELDS = "FIELDS  War 6 · Disaster 5 · Trade 4 · Markets 3 · Politics 4 · Sport 3 · Labour 2 · Space 1"
NUMBERS = [("31", "killed in Cairo tanker fire"), ("14", "face proposed US tariffs"),
           ("490,334", "Russian war dead, leaked data"), ("4,500+", "US flights delayed Wed"),
           ("2,000", "reach Canaries in one day"), ("100th", "Macy's parade, moved to Sat")]
REGIONS = [("AMERICAS 10", PURPLE), ("EUROPE 7", BLUE), ("MIDDLE EAST 6", ORANGE),
           ("ASIA 8", RED), ("AFRICA 4", GREEN), ("OCEANIA 1", TEAL),
           ("WORLD 4", INK)]
TIMELINE = [("00:00", "Thanksgiving"), ("02:07", "Prisoner swap"), ("05:24", "Cairo toll 30"),
            ("07:42", "Parade moved"), ("13:30", "Parade was due"), ("14:00", "Chess Game 3")]

HEROES = [
    ("AMERICAS · NEW YORK", "Macy's 100th parade postponed to Saturday",
     "A nor'easter grounds the balloons; first weather postponement in 100 years.",
     "AP · Xinhua", "CONFIRMED", "star", NAVY, "POSTPONED TO SAT",
     "WHY: Biggest parade, moved for safety"),
    ("AFRICA · CAIRO", "Fuel tanker fire kills 31 near Cairo",
     "Blaze on the Ring Road injures 21 and chars dozens of cars, ministry says.",
     "AP · CNN", "CONFIRMED", "burst", RED, "31 KILLED",
     "WHY: Deadliest road fire this year"),
    ("GLOBAL · TRADE", "US proposes tariffs on 14 economies",
     "China faces the highest rates in a drive against excess factory capacity.",
     "Reuters · USTR", "OFFICIAL", "chart", BLUE, "14 ECONOMIES",
     "WHY: Top trade partners face duties"),
]

SMALL = [
    ("AMERICAS · TRAVEL", "Thanksgiving travel snarled by storms",
     "4,500+ delays; NJ emergency.", "FlightAware · Fox", "CONFIRMED", "plane", TEAL, "4,500 DELAYS"),
    ("ASIA · MUMBAI", "India marks 18 years since 26/11 attacks",
     "Also 77 years of Constitution.", "PTI", "CONFIRMED", "star", GOLD, "18 YEARS"),
    ("SPORT · GENEVA", "Gukesh meets Sindarov in Game 3",
     "Level after two draws.", "FIDE", "ONGOING", "trophy", GREEN, "GAME 3"),
    ("EUROPE · WAR", "Ukraine says it hit Russian air base",
     "Five planes claimed hit.", "Reuters", "CLAIM", "plane", NAVY, "5 PLANES"),
    ("EUROPE · WAR", "Leaked data put war dead at 490,334",
     "BBC Rosstat analysis.", "BBC · Mediazona", "REPORTED", "scale", PURPLE, "490,334"),
    ("GLOBAL · MARKETS", "Nasdaq slides as AI fears spread",
     "Down 4% intraday; -0.6% close.", "Reuters · CNA", "CONFIRMED", "chart", RED, "NASDAQ -4%"),
    ("ASIA · DHAKA", "Bangladesh lifts garment wage 36%",
     "To Tk17,000 from 1 Dec.", "AFP · Reuters", "CONFIRMED", "chip", BLUE, "TK17,000 +36%"),
    ("EUROPE · MIGRATION", "Nearly 2,000 reach Canaries in a day",
     "Record arrival, officials say.", "AP", "REPORTED", "ship", TEAL, "2,000 IN A DAY"),
    ("AMERICAS · JOBS", "US jobless claims fall to 189,000",
     "Below forecast, stable jobs.", "Labor Dept · Reuters", "OFFICIAL", "chart", GREEN, "189,000"),
    ("ASIA · TRADE", "Vietnam working with US on trade deal",
     "After new tariff proposals.", "Reuters", "REPORTED", "globe", ORANGE, "DEAL PUSH"),
]

ALSO = [
    ("Judge bars FCC from threatening ABC licence", "Reuters"),
    ("Brazil indignant over proposed US tariffs", "Xinhua"),
    ("US proposes tariffs on Brazilian imports", "Xinhua"),
    ("UN warns meningitis rising in Gaza", "Xinhua"),
    ("Coalition intercepts 3 Houthi missiles", "Xinhua"),
    ("Houthis claim Jeddah, Jazan port attacks", "Xinhua"),
    ("Belarus, Russia sign 2027-29 policy pact", "Xinhua"),
    ("Heavy rains kill 8 in southern Brazil", "Xinhua"),
    ("Ukraine: prisoner swap could start late Nov", "Xinhua"),
    ("S. Africa court: Ramaphosa report unlawful", "Xinhua"),
    ("Putin removes Murmansk governor in probe", "Xinhua"),
    ("UK car investment faces triple risks", "SMMT"),
    ("Nepal, UNDP launch $49.9m flood project", "Xinhua"),
    ("Algeria collision kills 12, injures 15", "Xinhua"),
    ("China urges Japan on chemical weapons", "Xinhua"),
    ("Hamas security chief killed in Gaza", "Xinhua"),
    ("China urges fair climate in Nexperia row", "Reuters"),
    ("Saudi national kidnapped in Niger", "Reuters"),
    ("RBI net buyer of $6.94bn dollars in Sept", "Reuters"),
    ("Poundland nears administration, 600 stores", "Sky · Reuters"),
    ("AI metals meltdown: LME index -15%", "Reuters"),
    ("India: Das told not to use passport", "Reuters"),
    ("Shenzhou-24: first Pakistani in orbit", "Xinhua"),
    ("Solomons signs security pact with Australia", "AP"),
    ("Colombia frees supermarket hostages", "AP"),
    ("Sudan drone strikes kill 19 in Blue Nile", "Reuters"),
    ("Black Friday? Some brands opt out", "Reuters"),
]

DATE_CHECK = ("Left out as other days' news: COP31 ends without a pact (22 Nov) · "
              "Nvidia reinstates Huang (24 Nov) · Belgium strike grounds flights (23 Nov) · "
              "Israel kills Hamas chief Abu Nahal (24 Nov) · US shelves Russia deal plan (25 Nov).")

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

d.rectangle([0, 0, W, 30], fill=NAVY)
d.text((18, 7), "THE WORLD IN ONE DAY", font=nb(15), fill=WHITE)
d.text((W - 18, 7), "40 STORIES · 9 REGIONS · EVERY ONE DATED 26 NOV 2026",
       font=nb(13), fill=(255, 213, 64), anchor="ra")

_mf = 66
while d.textlength(DATE_LINE, font=sb(_mf)) > W - 40 and _mf > 30:
    _mf -= 2
d.text((W // 2, 38), DATE_LINE, font=sb(_mf), fill=INK, anchor="ma")
d.text((W // 2, 116), STRAP, font=sr(19), fill=RED, anchor="ma")
d.text((W // 2, 136), FIELDS, font=nb(11), fill=GREY, anchor="ma")
d.line([(18, 154), (W - 18, 154)], fill=INK, width=3)

nx = 18
nw = (W - 36) // 6
for i, (num, cap) in enumerate(NUMBERS):
    x = nx + i * nw
    d.text((x + nw // 2, 162), num, font=sb(30), fill=INK, anchor="ma")
    ls = wrap(d, cap, nr(12), nw - 14)
    yy = 198
    for ln in ls[:2]:
        d.text((x + nw // 2, yy), ln, font=nr(12), fill=GREY, anchor="ma")
        yy += 14
    if i:
        d.line([(x, 164), (x, 224)], fill=LIGHT, width=2)

y = 230
x = 18
for label, col in REGIONS:
    wch = int(d.textlength(label, font=nb(13))) + 18
    d.rectangle([x, y, x + wch, y + 24], fill=col)
    d.text((x + 9, y + 4), label, font=nb(13), fill=WHITE)
    x += wch + 8
d.text((W - 18, y + 4), "= 40 stories", font=nb(13), fill=GREY, anchor="ra")

y = 260
d.rectangle([18, y, W - 18, y + 26], fill=INK)
d.text((26, y + 5), "THE DAY IN UTC", font=nb(12), fill=WHITE)
tx = 150
for t, lab in TIMELINE:
    d.text((tx, y + 5), t, font=nb(12), fill=(255, 213, 64))
    d.text((tx + 42, y + 5), lab, font=nr(12), fill=WHITE)
    tx += 42 + int(d.textlength(lab, font=nr(12))) + 18

hy = 290
HW = (W - 36 - 2 * 12) // 3
for i, (kick, head, summ, src, bdg, icon, col, art, why) in enumerate(HEROES):
    x = 18 + i * (HW + 12)
    d.rectangle([x, hy, x + HW, hy + 80], fill=col)
    ICONS[icon](d, x + 14, hy + 8, 64, WHITE)
    d.text((x + HW - 10, hy + 56), art, font=nb(15), fill=WHITE, anchor="ra")
    numdot(d, x + 8, hy + 8, i + 1)
    yy = hy + 88
    d.text((x, yy), kick, font=nb(12), fill=RED)
    badge(d, x + HW - int(d.textlength(bdg, font=nb(10))) - 10, yy - 2, bdg, VCOL[bdg], size=10)
    yy += 20
    yy = lines(d, x, yy, wrap(d, head, sb(22), HW)[:2], sb(22), INK, 26)
    yy += 3
    yy = lines(d, x, yy, wrap(d, summ, sr(12), HW)[:2], sr(12), INK, 16)
    d.text((x, yy + 2), src, font=nr(10), fill=GREY)
    yy += 15
    lines(d, x, yy, wrap(d, why, nb(10), HW)[:1], nb(10), RED, 13)

sy = 520
SW = (W - 36 - 4 * 10) // 5
SH = 122
for i, (kick, head, summ, src, bdg, icon, col, art) in enumerate(SMALL):
    r, c = divmod(i, 5)
    x = 18 + c * (SW + 10)
    y = sy + r * (SH + 8)
    d.rectangle([x, y, x + SW, y + SH], outline=INK, width=1)
    d.rectangle([x, y, x + SW, y + 40], fill=col)
    ICONS[icon](d, x + 8, y + 5, 30, WHITE)
    d.text((x + SW - 6, y + 23), art, font=nb(10), fill=WHITE, anchor="ra")
    numdot(d, x + 4, y + 44, i + 4, r=9)
    yy = y + 46
    d.text((x + 26, yy), kick, font=nb(9), fill=RED)
    badge(d, x + SW - int(d.textlength(bdg, font=nb(8))) - 8, yy - 2, bdg, VCOL[bdg], size=8)
    yy += 16
    yy = lines(d, x + 8, yy, wrap(d, head, nb(13), SW - 16)[:3], nb(13), INK, 16)
    yy += 2
    yy = lines(d, x + 8, yy, wrap(d, summ, nr(10), SW - 16)[:2], nr(10), GREY, 13)
    d.text((x + 8, y + SH - 14), src, font=nr(9), fill=GREY)

by = sy + 2 * (SH + 8) + 4
MAP = [
    "  ####        ##   ##### ##########   ##  ",
    " #########  ###### ####################   ",
    "  ######## ################ ##########    ",
    "   ######   #############  #####  ##      ",
    "    ####     ##########     ####          ",
    "     ###      ########       ##    #      ",
    "     ##        ######                  ## ",
    "     #          ####            ####  ####",
    "                ###              ##    ## ",
]
mx, my, mw = 18, by + 18, 300
d.text((mx, by), "WHERE IT HAPPENED · PINS = STORIES", font=nb(12), fill=INK)
cell = mw // 42
for r, row in enumerate(MAP):
    for c, ch in enumerate(row):
        if ch == "#":
            cx, cy = mx + c * cell + 3, my + r * cell + 3
            d.ellipse([cx, cy, cx + 4, cy + 4], fill=(150, 160, 140))
PINS = [(0.18, 0.35), (0.52, 0.28), (0.62, 0.45), (0.78, 0.3), (0.7, 0.55),
        (0.3, 0.6), (0.55, 0.62), (0.85, 0.65), (0.45, 0.2), (0.25, 0.25),
        (0.66, 0.38), (0.58, 0.5), (0.9, 0.45)]
for i, (px, py) in enumerate(PINS):
    numdot(d, int(mx + px * mw), int(my + py * 9 * cell), i + 1, r=8)

ax = 336
d.text((ax, by), "ALSO ON THURSDAY 26 NOVEMBER — 27 MORE STORIES", font=nb(12), fill=INK)
colw = (W - ax - 18 - 12) // 2
half = (len(ALSO) + 1) // 2
for ci, chunk in enumerate((ALSO[:half], ALSO[half:])):
    x = ax + ci * (colw + 12)
    yy = by + 18
    for j, (t, s) in enumerate(chunk):
        n = 14 + ci * half + j
        numdot(d, x, yy, n, col=NAVY, r=7)
        avail = colw - 54
        txt = t
        while d.textlength(txt, font=nr(10)) > avail and len(txt) > 4:
            txt = txt[:-1]
        if txt != t:
            txt = txt.rstrip() + "…"
        d.text((x + 20, yy), txt, font=nr(10), fill=INK)
        d.text((x + colw, yy), s, font=nr(9), fill=GREY, anchor="ra")
        yy += 11

dy = 956
d.rectangle([18, dy, W - 18, dy + 38], outline=RED, width=2)
d.text((26, dy + 3), "DATE CHECK", font=nb(12), fill=RED)
lines(d, 26, dy + 18, wrap(d, DATE_CHECK, nr(11), W - 60)[:2], nr(11), INK, 13)
d.text((18, 1000),
       "CONFIRMED 2+ outlets · OFFICIAL on the record · REPORTED outlets' reports · "
       "CLAIM one side's account · Original drawings, no photos · Every story dated 26 Nov 2026 (UTC)",
       font=nr(11), fill=GREY)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, format="PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
