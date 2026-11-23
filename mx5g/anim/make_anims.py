#!/usr/bin/env python3
"""Pillow GIFs using searched cutout characters (Twemoji + rembg Commons)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
CUT = OUT.parent / "assets" / "cutouts"
W, H = 480, 300
INK = (15, 26, 22, 255)
JADE = (31, 122, 85, 255)
GOLD = (212, 160, 23, 255)
GOLD2 = (240, 215, 140, 255)
CORAL = (196, 75, 60, 255)
PAPER = (244, 247, 245, 255)
WHITE = (255, 255, 255, 255)


def font(size: int):
    for p in (
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    ):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()


FT, FB, FS = font(30), font(20), font(16)


def load_char(name: str, size: int = 120) -> Image.Image:
    im = Image.open(CUT / name).convert("RGBA")
    im.thumbnail((size, size), Image.Resampling.LANCZOS)
    return im


def paste(base: Image.Image, char: Image.Image, xy: tuple[int, int]) -> None:
    base.paste(char, xy, char)


def center_text(d, text, y, f, fill=INK):
    b = d.textbbox((0, 0), text, font=f)
    d.text(((W - (b[2] - b[0])) / 2, y), text, font=f, fill=fill)


def save_gif(frames, name, duration=90):
    rgb = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    rgb[0].save(OUT / name, save_all=True, append_images=rgb[1:], duration=duration, loop=0)
    print("wrote", name, len(frames))


def anim_de_vs_li():
    crown, fist = load_char("crown.png", 110), load_char("fist.png", 110)
    frames = []
    for i in range(28):
        img = Image.new("RGBA", (W, H), INK)
        d = ImageDraw.Draw(img)
        center_text(d, "德 vs 力", 12, FT, GOLD2)
        t = i / 27
        d.rounded_rectangle((30, 60, 220, 240), 18, fill=JADE)
        d.rounded_rectangle((260, 60, 450, 240), 18, fill=CORAL)
        paste(img, crown, (80, 80))
        paste(img, fist, (310, 85))
        d.text((70, 200), "心悅誠服", font=FB, fill=WHITE)
        d.text((300, 200), "暫時屈服", font=FB, fill=WHITE)
        if t > 0.55:
            center_text(d, "君子：以德服人", H - 36, FS, GOLD)
        frames.append(img)
    save_gif(frames, "01_de_vs_li.gif")


def anim_ren_ai():
    book, student, check = load_char("book.png", 70), load_char("student.png", 70), load_char("check.png", 50)
    labels = ["仁愛：分享筆記", "恭敬謙讓：排隊", "和為貴：吵完仍一隊"]
    icons = [book, student, check]
    frames = []
    for i in range(36):
        img = Image.new("RGBA", (W, H), PAPER)
        d = ImageDraw.Draw(img)
        center_text(d, "仁愛謙和", 10, FT, JADE)
        step = min(2, i // 12)
        for s in range(3):
            y = 60 + s * 70
            on = s <= step
            d.rounded_rectangle((24, y, W - 24, y + 58), 14, fill=JADE if on else (210, 220, 214, 255))
            paste(img, icons[s], (40, y + 4))
            d.text((120, y + 16), labels[s], font=FB, fill=WHITE if on else (90, 100, 95, 255))
        frames.append(img)
    save_gif(frames, "02_ren_ai.gif", 100)


def anim_san_fan():
    mirror, student, check = load_char("mirror.png", 100), load_char("student.png", 90), load_char("check.png", 70)
    frames = []
    for i in range(28):
        img = Image.new("RGBA", (W, H), PAPER)
        d = ImageDraw.Draw(img)
        center_text(d, "三反其身", 10, FT, JADE)
        paste(img, mirror, (90, 70))
        paste(img, student, (110, 95))
        t = i / 27
        if t < 0.45:
            d.ellipse((320, 90, 400, 170), fill=GOLD)
            d.text((345, 110), "?", font=FT, fill=INK)
        else:
            paste(img, check, (330, 100))
            center_text(d, "先反省自己", H - 36, FS, JADE)
        frames.append(img)
    save_gif(frames, "03_san_fan.gif")


def anim_yu_xiong():
    fish, bear = load_char("fish.png", 130), load_char("bear.png", 130)
    frames = []
    for i in range(32):
        img = Image.new("RGBA", (W, H), INK)
        d = ImageDraw.Draw(img)
        center_text(d, "魚 VS 熊掌 → 舍生取義", 10, FT, GOLD2)
        paste(img, fish, (40, 70))
        paste(img, bear, (300, 65))
        d.text((70, 220), "生命", font=FS, fill=GOLD2)
        d.text((340, 220), "義", font=FS, fill=GOLD2)
        if i / 31 > 0.5:
            d.polygon([(200, 130), (260, 130), (260, 110), (300, 150), (260, 190), (260, 170), (200, 170)], fill=GOLD)
        frames.append(img)
    save_gif(frames, "04_yu_xiong.gif", 85)


def anim_zun_yan():
    heart, student = load_char("heart2.png", 90), load_char("student.png", 110)
    frames = []
    for i in range(30):
        img = Image.new("RGBA", (W, H), PAPER)
        d = ImageDraw.Draw(img)
        center_text(d, "天賦尊嚴", 10, FT, JADE)
        paste(img, heart, (70, 70))
        paste(img, heart, (180, 70))
        d.text((80, 175), "憐憫", font=FS, fill=INK)
        d.text((190, 175), "羞恥", font=FS, fill=INK)
        if i / 29 > 0.4:
            paste(img, student, (330, 80))
            center_text(d, "→ 仁義 → 尊嚴人格", H - 36, FB, JADE)
        frames.append(img)
    save_gif(frames, "05_zun_yan.gif")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    anim_de_vs_li()
    anim_ren_ai()
    anim_san_fan()
    anim_yu_xiong()
    anim_zun_yan()
    print("done", OUT)


if __name__ == "__main__":
    main()
