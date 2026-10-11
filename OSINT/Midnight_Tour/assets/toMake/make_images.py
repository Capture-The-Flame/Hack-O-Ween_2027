#!/usr/bin/env python3
# Regenerates everything under app/site/img. Needs Pillow: pip install pillow
import random
from pathlib import Path
from PIL import Image, ImageDraw

IMG = Path(__file__).resolve().parents[1] / 'app' / 'site' / 'img'
W, H = 1200, 800
LIT, TOTAL = 11, 19  # the lit count is part of the gate password
DARK = (20, 16, 24)


def save(img, name, artist, desc=None, gps=None):
    ex = Image.Exif()
    ex[0x013b] = artist
    if desc: ex[0x010e] = desc
    if gps: ex[0x8825] = gps
    (IMG / name).parent.mkdir(parents=True, exist_ok=True)
    img.save(IMG / name, quality=88, exif=ex)


def night(seed, w=W, h=H):
    random.seed(seed)
    img = Image.new('RGB', (w, h), (12, 10, 24))
    d = ImageDraw.Draw(img)
    for _ in range(150): d.point((random.randrange(w), random.randrange(h // 2)), fill=(230, 230, 200))
    mx = random.randrange(120, w - 120)
    d.ellipse([mx - 50, 60, mx + 50, 160], fill=(240, 230, 190))
    return img, d


def trees(d, n, w=W, h=H):
    for _ in range(n):
        x, t = random.randrange(w), random.randrange(200, 450)
        d.polygon([(x - 70, h), (x + 70, h), (x, h - t)], fill=(5, 5, 10))


def pumpkin(d, x, y, r, lit):
    d.rectangle([x - r * .12, y - r * 1.2, x + r * .12, y - r * .7], fill=(80, 120, 40))
    d.ellipse([x - r, y - r * .85, x + r, y + r * .85], fill=(236, 122, 28), outline=(150, 70, 10), width=2)
    for k in (-.45, .45): d.ellipse([x + k * r - r * .55, y - r * .85, x + k * r + r * .55, y + r * .85], outline=(200, 95, 15), width=2)
    c = (255, 228, 90) if lit else (35, 18, 8)
    d.polygon([(x - r * .55, y - r * .05), (x - r * .15, y - r * .05), (x - r * .35, y - r * .45)], fill=c)
    d.polygon([(x + r * .15, y - r * .05), (x + r * .55, y - r * .05), (x + r * .35, y - r * .45)], fill=c)
    d.polygon([(x - r * .1, y + r * .15), (x + r * .1, y + r * .15), (x, y - r * .02)], fill=c)
    d.polygon([(x + r * k, y + r * (.25 if i % 2 == 0 else .45)) for i, k in enumerate((-.6, -.4, -.2, 0, .2, .4, .6))] + [(x, y + r * .7)], fill=c)


def porch():
    img, d = night(1031)
    d.polygon([(40, 140), (600, 10), (1160, 140)], fill=(28, 20, 26))
    d.rectangle([90, 140, 1110, H], fill=(52, 36, 44))
    for wx in (210, 870): d.rectangle([wx, 260, wx + 120, 400], fill=(58, 44, 18), outline=(95, 75, 65), width=5)
    d.rectangle([520, 290, 680, 570], fill=(26, 14, 18), outline=(95, 75, 65), width=5)
    d.rectangle([0, 570, W, H], fill=(74, 58, 52))
    for i in range(3): d.rectangle([0, 700 + i * 34, W, H], fill=(64 - i * 8, 50 - i * 6, 46 - i * 5))
    d.rounded_rectangle([790, 150, 870, 290], radius=40, fill=(235, 235, 242))
    for ex in (812, 848): d.ellipse([ex - 8, 190, ex + 8, 212], fill=DARK)
    d.ellipse([230, 360, 330, 402], fill=(8, 8, 12)); d.ellipse([300, 335, 345, 380], fill=(8, 8, 12))
    d.polygon([(305, 345), (312, 322), (322, 345)], fill=(8, 8, 12)); d.polygon([(325, 345), (333, 322), (342, 345)], fill=(8, 8, 12))
    # jittered 2x10 grid keeps the pumpkins from overlapping so the count is unambiguous
    slots = [(90 + c * 113 + random.randrange(-12, 13), 615 + r * 115 + random.randrange(-10, 11)) for r in range(2) for c in range(10)]
    random.shuffle(slots)
    for i, (x, y) in enumerate(slots[:TOTAL]): pumpkin(d, x, y, random.randrange(30, 43), i < LIT)
    save(img, 'gallery/porch.jpg', 'Wren Ashgrove', 'home.')


def cemetery():
    img, d = night(1849, 600, 600)
    trees(d, 3, 600, 600)
    d.ellipse([-200, 400, 800, 900], fill=(16, 22, 16))
    for x, h in ((70, 90), (190, 130), (320, 80), (440, 110)):
        d.rounded_rectangle([x, 480 - h, x + 70, 490], radius=30, fill=(120, 122, 118), outline=(70, 72, 68), width=3)
    d.rectangle([540, 260, 552, 470], fill=(6, 6, 6))
    for y, dx in ((300, 60), (340, -50), (380, 45)): d.line([(546, y), (546 + dx, y - 60)], fill=(6, 6, 6), width=7)
    # 41°05'23"N 73°51'41"W -> Sleepy Hollow Cemetery, NY
    save(img, 'staff/wren.jpg', 'Wren Ashgrove', 'day off.', {1: 'N', 2: (41.0, 5.0, 23.0), 3: 'W', 4: (73.0, 51.0, 41.0)})


def avatar(name, artist, color):
    img = Image.new('RGB', (600, 600), color)
    d = ImageDraw.Draw(img)
    d.ellipse([200, 120, 400, 320], fill=DARK); d.ellipse([90, 340, 510, 760], fill=DARK)
    save(img, f'staff/{name}.jpg', artist)


def scene(name, seed, artist, extra):
    img, d = night(seed)
    trees(d, 14)
    extra(d)
    save(img, f'gallery/{name}.jpg', artist)


def wagon(d): d.rectangle([380, 560, 820, 680], fill=(60, 40, 20)); [d.ellipse([x, 640, x + 100, 740], fill=DARK) for x in (400, 700)]
def corn(d): [d.line([(x, H), (x + random.randrange(-10, 10), 520)], fill=(90, 80, 30), width=4) for x in range(0, W, 14)]
def sawmill(d): d.rectangle([300, 420, 900, 720], fill=(40, 30, 28)); d.polygon([(280, 420), (600, 300), (920, 420)], fill=(30, 22, 22)); d.rectangle([560, 560, 640, 720], fill=(10, 8, 8))
def path(d): d.polygon([(500, H), (700, H), (610, 520), (590, 520)], fill=(40, 34, 30))
def people(d): [(d.ellipse([x - 25, 520, x + 25, 570], fill=DARK), d.rectangle([x - 40, 570, x + 40, H], fill=DARK)) for x in range(150, W, 180)]


if __name__ == '__main__':
    porch(); cemetery()
    avatar('dario', 'Dario Mott', (120, 40, 30)); avatar('priya', 'Priya Vance', (90, 30, 90))
    avatar('hollis', 'Hollis Crane', (30, 70, 70)); avatar('june', 'June Okafor', (110, 80, 20))
    scene('hayride', 1, 'Dario Mott', wagon); scene('maze', 2, 'Priya Vance', corn); scene('sawmill', 3, 'Hollis Crane', sawmill)
    scene('trail', 4, 'Wren Ashgrove', path); scene('crew', 5, 'June Okafor', people)
    print(f'porch: {TOTAL} pumpkins, {LIT} lit')
