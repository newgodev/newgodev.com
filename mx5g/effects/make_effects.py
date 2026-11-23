#!/usr/bin/env python3
"""Pillow visual effects for mx5g Mencius HTML deck + wheel game."""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)
RNG = random.Random(20261123)


def glow_orb(size: int = 512, color=(45, 160, 110), name="glow.png") -> None:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = size // 2
    for i, alpha in enumerate((18, 36, 70, 120, 180)):
        r = int(size * (0.48 - i * 0.07))
        c = (*color, alpha)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
    img = img.filter(ImageFilter.GaussianBlur(28))
    core = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(core)
    r = int(size * 0.12)
    d2.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*color, 230))
    core = core.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img, core)
    img.save(OUT / name)


def particle_burst_frames(frames: int = 24, size: int = 360) -> list[Image.Image]:
    colors = [(255, 214, 102), (45, 160, 110), (232, 93, 74), (248, 250, 252), (120, 200, 170)]
    particles = []
    for _ in range(70):
        ang = RNG.uniform(0, math.tau)
        speed = RNG.uniform(3.5, 11.5)
        particles.append(
            {
                "ang": ang,
                "speed": speed,
                "size": RNG.randint(3, 9),
                "color": RNG.choice(colors),
                "spin": RNG.uniform(-0.25, 0.25),
            }
        )
    out = []
    cx = cy = size // 2
    for f in range(frames):
        t = f / max(frames - 1, 1)
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        for p in particles:
            dist = p["speed"] * f * 1.35
            x = cx + math.cos(p["ang"] + p["spin"] * f) * dist
            y = cy + math.sin(p["ang"] + p["spin"] * f) * dist + 0.18 * f * f
            alpha = max(0, int(255 * (1 - t) ** 1.2))
            s = max(1, int(p["size"] * (1 - 0.55 * t)))
            col = (*p["color"], alpha)
            draw.ellipse((x - s, y - s, x + s, y + s), fill=col)
        out.append(img.filter(ImageFilter.GaussianBlur(0.6)))
    return out


def save_burst_gif() -> None:
    frames = particle_burst_frames()
    frames[0].save(
        OUT / "burst.gif",
        save_all=True,
        append_images=frames[1:],
        duration=42,
        loop=0,
        disposal=2,
        optimize=False,
    )


def confetti_strip(width: int = 900, height: int = 220, name="confetti.png") -> None:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    palette = [(232, 93, 74), (45, 160, 110), (255, 214, 102), (90, 140, 220), (248, 250, 252)]
    for _ in range(160):
        x = RNG.randint(0, width)
        y = RNG.randint(0, height)
        w = RNG.randint(4, 14)
        h = RNG.randint(8, 22)
        ang_fake = RNG.choice([0, 1, 2])
        col = (*RNG.choice(palette), RNG.randint(160, 255))
        if ang_fake == 0:
            draw.rectangle((x, y, x + w, y + h), fill=col)
        elif ang_fake == 1:
            draw.ellipse((x, y, x + w, y + w), fill=col)
        else:
            draw.polygon([(x, y + h), (x + w // 2, y), (x + w, y + h)], fill=col)
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    img.save(OUT / name)


def wheel_glow_ring(size: int = 640, name="wheel-glow.png") -> None:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = size // 2
    for r, a in ((300, 40), (285, 90), (270, 140)):
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(45, 160, 110, a), width=18)
    img = img.filter(ImageFilter.GaussianBlur(10))
    img.save(OUT / name)


def number_badge(n: int, size: int = 128) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((8, 8, size - 8, size - 8), fill=(26, 35, 50, 255))
    draw.ellipse((16, 16, size - 16, size - 16), outline=(45, 160, 110, 255), width=4)
    text = str(n)
    # default font; size approx via repeated draw
    draw.text((size // 2 - 10 * len(text), size // 2 - 14), text, fill=(248, 250, 252, 255))
    return img


def badge_sheet() -> None:
    cols, rows = 10, 3
    cell = 96
    sheet = Image.new("RGBA", (cols * cell, rows * cell), (0, 0, 0, 0))
    for i in range(1, 31):
        badge = number_badge(i, cell)
        r, c = divmod(i - 1, cols)
        sheet.paste(badge, (c * cell, r * cell), badge)
    sheet.save(OUT / "numbers.png")


def main() -> None:
    glow_orb(color=(45, 160, 110), name="glow.png")
    glow_orb(color=(255, 214, 102), name="glow-gold.png")
    save_burst_gif()
    confetti_strip()
    wheel_glow_ring()
    badge_sheet()
    print("Wrote effects to", OUT)


if __name__ == "__main__":
    main()
