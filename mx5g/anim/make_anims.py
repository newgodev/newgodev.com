#!/usr/bin/env python3
"""Looping classroom GIFs for 3G Group 5 — Mencius talk.

Palette: #0f1a16 #1f7a55 #d4a017 #c44b3c
Font:    /usr/share/fonts/truetype/wqy/wqy-microhei.ttc
Run:     python3 make_anims.py
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
SIZE = 400
SCALE = 2

INK = (15, 26, 22)       # #0f1a16
GREEN = (31, 122, 85)    # #1f7a55
GOLD = (212, 160, 23)    # #d4a017
RED = (196, 75, 60)      # #c44b3c

_FONTS: dict[int, ImageFont.FreeTypeFont] = {}


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def font(px: float) -> ImageFont.FreeTypeFont:
    key = max(8, int(round(px * SCALE)))
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(FONT_PATH, key, index=0)
    return _FONTS[key]


def ping(t: float, phase: float = 0.0) -> float:
    """Seamless 0 → 1 → 0 pulse. t is frame/count, in [0, 1)."""
    return 0.5 - 0.5 * math.cos((t + phase) * math.tau)


def wave(t: float, phase: float = 0.0, cycles: float = 1.0) -> float:
    return math.sin((t + phase) * cycles * math.tau)


class Canvas:
    def __init__(self) -> None:
        self.s = SCALE
        self.im = Image.new("RGB", (SIZE * SCALE, SIZE * SCALE), INK)
        self.d = ImageDraw.Draw(self.im)

    def ellipse(self, cx, cy, rx, ry, fill=None, outline=None, width=1) -> None:
        s = self.s
        kw = {}
        if fill is not None:
            kw["fill"] = fill
        if outline is not None:
            kw["outline"] = outline
            kw["width"] = max(1, int(round(width * s)))
        self.d.ellipse(((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s), **kw)

    def rect(self, x, y, w, h, fill) -> None:
        s = self.s
        self.d.rectangle((x * s, y * s, (x + w) * s, (y + h) * s), fill=fill)

    def rrect(self, x, y, w, h, r, fill=None, outline=None, width=2) -> None:
        if w <= 1 or h <= 1:
            return
        r = max(0, min(r, w / 2, h / 2))
        s = self.s
        kw = {}
        if fill is not None:
            kw["fill"] = fill
        if outline is not None:
            kw["outline"] = outline
            kw["width"] = max(1, int(round(width * s)))
        self.d.rounded_rectangle((x * s, y * s, (x + w) * s, (y + h) * s), radius=r * s, **kw)

    def line(self, pts, fill, width=2) -> None:
        s = self.s
        self.d.line([(p[0] * s, p[1] * s) for p in pts], fill=fill, width=max(1, int(round(width * s))))

    def polygon(self, pts, fill) -> None:
        s = self.s
        self.d.polygon([(p[0] * s, p[1] * s) for p in pts], fill=fill)

    def arc(self, cx, cy, rx, ry, start, end, fill, width=2) -> None:
        s = self.s
        self.d.arc(
            ((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s),
            start=start,
            end=end,
            fill=fill,
            width=max(1, int(round(width * s))),
        )

    def text(self, x, y, text, fnt, fill, anchor="mm") -> None:
        if text is None or text == "":
            return
        lines = str(text).split("\n")
        boxes = [self.d.textbbox((0, 0), line, font=fnt) for line in lines]
        heights = [b[3] - b[1] for b in boxes]
        gap = int(round(3 * self.s))
        total_h = sum(heights) + gap * (len(lines) - 1)
        ax, ay = anchor[0], anchor[1]
        if ay == "m":
            top = y * self.s - total_h / 2
        elif ay == "b":
            top = y * self.s - total_h
        else:
            top = y * self.s
        for line, b, h in zip(lines, boxes, heights):
            tw = b[2] - b[0]
            if ax == "m":
                left = x * self.s - tw / 2 - b[0]
            elif ax == "r":
                left = x * self.s - tw - b[0]
            else:
                left = x * self.s - b[0]
            self.d.text((left, top - b[1]), line, font=fnt, fill=fill)
            top += h + gap

    def finish(self) -> Image.Image:
        s = self.s
        self.d.rectangle((3 * s, 3 * s, (SIZE - 3) * s, (SIZE - 3) * s), outline=GOLD, width=2 * s)
        return self.im.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def header(c: Canvas, title: str, n: int) -> None:
    c.rect(0, 0, SIZE, 48, mix(INK, GREEN, 0.45))
    c.text(200, 24, title, font(26), GOLD, "mm")
    c.text(378, 24, f"{n}/5", font(13), GOLD, "rm")
    c.rect(0, 48, SIZE, 3, GOLD)


def footer(c: Canvas, text: str) -> None:
    c.rect(0, 360, SIZE, 40, mix(INK, GREEN, 0.45))
    c.rect(0, 360, SIZE, 3, GOLD)
    c.text(200, 380, text, font(16), GOLD, "mm")


def capsule(c: Canvas, x1, y1, x2, y2, r, fill, outline=None) -> None:
    if outline is not None:
        capsule(c, x1, y1, x2, y2, r + 1.6, outline)
    c.line([(x1, y1), (x2, y2)], fill, max(1, r * 2))
    c.ellipse(x1, y1, r, r, fill=fill)
    c.ellipse(x2, y2, r, r, fill=fill)


def heart(c: Canvas, cx, cy, s, fill) -> None:
    r = s * 0.28
    c.ellipse(cx - r * 0.62, cy - r * 0.15, r, r, fill=fill)
    c.ellipse(cx + r * 0.62, cy - r * 0.15, r, r, fill=fill)
    c.polygon([(cx - s * 0.52, cy + s * 0.02), (cx + s * 0.52, cy + s * 0.02), (cx, cy + s * 0.58)], fill)


def face(c: Canvas, x, y, r, mood: str) -> None:
    if r < 7:
        return
    er = max(1.3, r * 0.13)
    dx = r * 0.34
    ey = y - r * 0.12
    c.ellipse(x - dx, ey, er, er * 1.15, fill=INK)
    c.ellipse(x + dx, ey, er, er * 1.15, fill=INK)
    if mood == "happy":
        c.arc(x, y + r * 0.22, r * 0.42, r * 0.30, 15, 165, INK, 1.6)
    elif mood == "shout":
        c.ellipse(x, y + r * 0.32, r * 0.20, r * 0.16, fill=INK)
        c.line([(x - dx - r * 0.05, ey - r * 0.28), (x - dx + r * 0.16, ey - r * 0.12)], INK, 1.5)
        c.line([(x + dx + r * 0.05, ey - r * 0.28), (x + dx - r * 0.16, ey - r * 0.12)], INK, 1.5)
    elif mood == "down":
        c.arc(x, y + r * 0.58, r * 0.38, r * 0.26, 200, 340, INK, 1.6)
    else:
        c.line([(x - r * 0.2, y + r * 0.34), (x + r * 0.2, y + r * 0.34)], INK, 1.6)


def person(c: Canvas, x, foot_y, h, color, mood="calm", arm="down", face_dir=1, crouch=0.0, bob=0.0, reach=0.42):
    """Blob classmate. foot_y stays on the floor; bob lifts the body."""
    crouch = max(0.0, min(1.0, crouch))
    h = h * (1 - 0.36 * crouch)
    y = foot_y - bob
    head_r = h * 0.165
    body_h = h * 0.36
    leg_h = h * 0.23
    body_w = h * 0.40
    lw = max(3.0, h * 0.095)
    c.ellipse(x, foot_y + 3, h * 0.20, h * 0.05, fill=mix(INK, color, 0.28))
    leg_top = y - leg_h
    body_top = leg_top - body_h + h * 0.05
    shoulder_y = body_top + body_h * 0.28
    arm_r = max(2.2, h * 0.05)
    hands = {}

    def arm_to(x2, y2, key):
        sx = x + (-body_w * 0.28 if x2 < x else body_w * 0.28)
        capsule(c, sx, shoulder_y, x2, y2, arm_r, color, GOLD)
        hands[key] = (x2, y2)

    if arm == "open":
        arm_to(x - h * reach, shoulder_y + h * 0.02, "l")
        arm_to(x + h * reach, shoulder_y + h * 0.02, "r")
    elif arm == "offer":
        arm_to(x + face_dir * h * reach, shoulder_y - h * 0.02, "offer")
        arm_to(x - face_dir * h * 0.16, shoulder_y + h * 0.26, "down")
    elif arm == "self":
        arm_to(x + head_r * 0.15, body_top + body_h * 0.48, "self")
        arm_to(x - h * 0.20, shoulder_y + h * 0.24, "down")
    else:
        arm_to(x - body_w * 0.62, shoulder_y + h * 0.26, "l")
        arm_to(x + body_w * 0.62, shoulder_y + h * 0.26, "r")

    c.rrect(x - body_w * 0.30, leg_top, lw, leg_h, lw / 2, fill=color, outline=GOLD, width=2)
    c.rrect(x + body_w * 0.30 - lw, leg_top, lw, leg_h, lw / 2, fill=color, outline=GOLD, width=2)
    c.rrect(x - body_w / 2, body_top, body_w, body_h, min(body_w * 0.45, body_h / 2), fill=color, outline=GOLD, width=2)
    c.line(
        [(x - body_w * 0.26, body_top + h * 0.07), (x + body_w * 0.26, body_top + h * 0.07)],
        GOLD,
        2,
    )
    head_cy = body_top - head_r * 0.72 + crouch * head_r * 0.2
    c.ellipse(x, head_cy, head_r, head_r, fill=color, outline=GOLD, width=2)
    face(c, x, head_cy, head_r, mood)
    if arm == "self":
        hx, hy = hands["self"]
        c.ellipse(hx, hy, arm_r + 1.4, arm_r + 1.4, fill=GOLD)
        c.ellipse(hx, hy, arm_r * 0.45, arm_r * 0.45, fill=RED)
    return {
        "head": (x, head_cy),
        "chest": (x, body_top + body_h * 0.48),
        "hands": hands,
        "foot": (x, foot_y),
    }


def megaphone(c: Canvas, x, y, length, face_dir=1) -> None:
    w = length * 0.42
    x2 = x + face_dir * length
    c.polygon(
        [
            (x, y - w * 0.28),
            (x2, y - w * 0.95),
            (x2, y + w * 0.95),
            (x, y + w * 0.28),
        ],
        GOLD,
    )
    c.ellipse(x, y, w * 0.34, w * 0.34, fill=RED, outline=GOLD, width=1.5)


def sound_waves(c: Canvas, x, y, t: float) -> None:
    for i in range(3):
        p = (t + i / 3.0) % 1.0
        rad = 7 + p * 20
        col = mix(GOLD, INK, 0.05 + 0.8 * p)
        c.arc(x, y, rad, rad * 0.78, -58, 58, col, 2.4)


def notebook(c: Canvas, x, y, w, h) -> None:
    c.rrect(x, y, w, h, 3, fill=GOLD, outline=INK, width=1)
    c.rect(x, y, max(3, w * 0.16), h, RED)
    for i in range(3):
        yy = y + h * (0.28 + i * 0.22)
        c.line([(x + w * 0.28, yy), (x + w - 3, yy)], INK, 1.3)


def fish_icon(c: Canvas, cx, cy, s, fill, face_dir=1) -> None:
    c.ellipse(cx, cy, s * 0.46, s * 0.28, fill=fill, outline=GOLD, width=2)
    bx = cx - face_dir * s * 0.28
    c.polygon(
        [
            (bx, cy),
            (bx - face_dir * s * 0.40, cy - s * 0.28),
            (bx - face_dir * s * 0.40, cy + s * 0.28),
        ],
        fill,
    )
    c.polygon(
        [
            (cx - face_dir * s * 0.02, cy - s * 0.02),
            (cx - face_dir * s * 0.16, cy - s * 0.32),
            (cx + face_dir * s * 0.12, cy - s * 0.08),
        ],
        GOLD,
    )
    ex = cx + face_dir * s * 0.16
    c.ellipse(ex, cy - s * 0.04, max(1.6, s * 0.07), max(1.6, s * 0.07), fill=INK)
    c.ellipse(ex + face_dir * s * 0.02, cy - s * 0.06, max(1, s * 0.025), max(1, s * 0.025), fill=GOLD)


def paw_icon(c: Canvas, cx, cy, s, fill) -> None:
    for tx, ty in ((-0.36, -0.34), (-0.12, -0.48), (0.14, -0.48), (0.36, -0.32)):
        c.ellipse(cx + tx * s, cy + ty * s, s * 0.16, s * 0.16, fill=fill, outline=GOLD, width=2)
    c.ellipse(cx, cy + s * 0.10, s * 0.34, s * 0.28, fill=fill, outline=GOLD, width=2)
    c.ellipse(cx, cy + s * 0.12, s * 0.11, s * 0.08, fill=GOLD)


def arrow(c: Canvas, x1, y1, x2, y2, color, width=3) -> None:
    c.line([(x1, y1), (x2, y2)], color, width)
    ang = math.atan2(y2 - y1, x2 - x1)
    length = 10
    p1 = (x2 - length * math.cos(ang - 0.45), y2 - length * math.sin(ang - 0.45))
    p2 = (x2 - length * math.cos(ang + 0.45), y2 - length * math.sin(ang + 0.45))
    c.polygon([(x2, y2), p1, p2], color)


def draw_scale(c: Canvas, cx, cy, angle_deg: float, arm: float):
    c.polygon([(cx - 20, cy + 74), (cx + 20, cy + 74), (cx + 7, cy + 60), (cx - 7, cy + 60)], GOLD)
    c.rrect(cx - 4, cy + 4, 8, 60, 2, fill=GOLD)
    rad = math.radians(angle_deg)
    left = (cx - math.cos(rad) * arm, cy - math.sin(rad) * arm)
    right = (cx + math.cos(rad) * arm, cy + math.sin(rad) * arm)
    c.line([left, right], GOLD, 5)
    c.ellipse(cx, cy, 6.5, 6.5, fill=RED, outline=GOLD, width=2)
    pans = []
    for x, y in (left, right):
        c.line([(x, y), (x, y + 18)], GOLD, 2)
        c.arc(x, y + 26, 15, 8, 15, 165, GOLD, 3)
        pans.append((x, y + 16))
    return pans


def anim_de_vs_li(n: int = 32):
    frames = []
    for i in range(n):
        t = i / n
        c = Canvas()
        header(c, "德 vs 力", 1)
        panels = (
            (8, RED, "force", "力", "以力服人", "暫時屈服"),
            (204, GREEN, "virtue", "德", "以德服人", "心悅誠服"),
        )
        for x, accent, kind, big, sub, label in panels:
            bg = mix(INK, accent, 0.20)
            c.rrect(x, 58, 188, 294, 14, fill=bg)
            c.rrect(x + 10, 70, 7, 250, 3, fill=accent)
            c.text(x + 94, 86, big, font(34), GOLD, "mm")
            c.text(x + 94, 116, sub, font(15), GOLD, "mm")
            floor = 318
            c.line([(x + 22, floor + 2), (x + 170, floor + 2)], mix(accent, GOLD, 0.35), 3)
            c.text(x + 94, 338, label, font(16), GOLD, "mm")
            leader_x = x + 52
            if kind == "force":
                info = person(
                    c, leader_x, floor, 148, RED, mood="shout", arm="offer",
                    face_dir=1, reach=0.20, bob=0,
                )
                hand = info["hands"]["offer"]
                megaphone(c, hand[0] + 2, hand[1], 22, 1)
                sound_waves(c, hand[0] + 26, hand[1], t)
                for k, sx in enumerate((x + 112, x + 142, x + 170)):
                    person(
                        c, sx + 6 * ping(t, k * 0.06), floor, 62, mix(RED, GOLD, 0.12),
                        mood="down", arm="down", crouch=ping(t, k * 0.06),
                    )
            else:
                info = person(
                    c, leader_x, floor, 148, GREEN, mood="happy", arm="open",
                    reach=0.16, bob=2 * ping(t),
                )
                hx, hy = info["chest"]
                c.ellipse(hx, hy + 2, 13 + ping(t) * 2, 13 + ping(t) * 2, fill=GOLD)
                heart(c, hx, hy + 1, 16 + ping(t) * 2, RED)
                for k, sx in enumerate((x + 112, x + 142, x + 170)):
                    person(
                        c, sx - 5 * ping(t, 0.15), floor, 62, GREEN,
                        mood="happy", arm="down", bob=7 * ping(t, k * 0.1),
                    )
        footer(c, "力只服口，德先服心")
        frames.append(c.finish())
    return frames


def anim_ren_ai(n: int = 30):
    frames = []
    rows = (
        ("仁", GREEN, GOLD, "仁愛", "主動分享筆記", "share"),
        ("謙", GOLD, INK, "謙讓", "排隊，讓人先行", "yield"),
        ("和", RED, GOLD, "和為貴", "輸咗都係一隊", "peace"),
    )
    for i in range(n):
        t = i / n
        c = Canvas()
        header(c, "仁愛謙和", 2)
        for r, (char, med_fill, med_ink, title, sub, kind) in enumerate(rows):
            y = 58 + r * 100
            tone = mix(INK, GREEN if r < 2 else RED, 0.16 + 0.05 * (r % 2))
            c.rrect(10, y, 380, 94, 12, fill=tone)
            c.ellipse(46, y + 47, 24, 24, fill=med_fill, outline=GOLD, width=2)
            c.text(46, y + 47, char, font(22), med_ink, "mm")
            c.text(82, y + 32, title, font(20), GOLD, "lm")
            c.text(82, y + 60, sub, font(14), GOLD, "lm")
            foot = y + 80
            if kind == "share":
                person(c, 248, foot, 64, GREEN, mood="happy", arm="offer", face_dir=1, reach=0.34)
                person(c, 346, foot, 64, mix(GREEN, GOLD, 0.25), mood="happy", arm="down")
                u = ping(t)
                notebook(c, 262 + 52 * u, y + 34, 24, 18)
                if u > 0.62:
                    heart(c, 346, y + 16, 12 + 8 * (u - 0.62), RED)
            elif kind == "yield":
                person(c, 250, foot, 64, GREEN, mood="down", arm="down", crouch=ping(t))
                person(c, 328, foot, 64, mix(GREEN, GOLD, 0.2), mood="happy", arm="offer", face_dir=1, reach=0.28, bob=3 * ping(t, 0.2))
                c.text(292, y + 24 - 6 * ping(t), "讓", font(16), GOLD, "mm")
                c.line([(368, y + 18), (368, y + 82)], GOLD, 3)
            else:
                person(c, 250, foot, 64, GREEN, mood="happy", arm="offer", face_dir=1, reach=0.40)
                person(c, 342, foot, 64, mix(GREEN, GOLD, 0.25), mood="happy", arm="offer", face_dir=-1, reach=0.40)
                rad = 8 + ping(t) * 8
                c.ellipse(296, y + 48, rad, rad, outline=GOLD, width=2)
                c.ellipse(296, y + 48, 6, 6, fill=RED)
        footer(c, "有愛、有禮、以和為貴")
        frames.append(c.finish())
    return frames


def anim_san_fan(n: int = 36):
    banners = (
        "對人好但疏遠 · 反省仁",
        "管人唔掂 · 反省智",
        "有禮冇回禮 · 反省敬",
    )
    words = ("仁", "智", "敬")
    frames = []
    for i in range(n):
        t = i / n
        phase = min(2, int(t * 3))
        c = Canvas()
        header(c, "三反其身", 3)
        bubble = mix(INK, GREEN, 0.5)
        c.polygon([(54, 126), (78, 126), (60, 142)], bubble)
        c.rrect(16, 60, 132, 68, 14, fill=bubble, outline=GOLD, width=2)
        c.text(82, 94, "點解\n疏遠我？", font(18), GOLD, "mm")
        person(c, 78, 300, 150, GREEN, mood="down", arm="self", bob=1.5 * ping(t))
        # travelling dot toward the mirror
        x1, y1, x2, y2 = 118, 230, 196, 196
        p = (t * 1.5) % 1.0
        arrow(c, x1, y1, x2, y2, GOLD, 3)
        c.ellipse(x1 + (x2 - x1) * p, y1 + (y2 - y1) * p, 4.5, 4.5, fill=RED)

        cx, cy, rx, ry = 292, 186, 74, 90
        c.ellipse(cx, cy, rx, ry, fill=mix(INK, GREEN, 0.38))
        ox = wave(t) * rx * 0.28
        c.ellipse(cx + ox, cy - ry * 0.35, rx * 0.22, ry * 0.1, fill=mix(GREEN, GOLD, 0.55))
        c.ellipse(cx, cy, rx, ry, outline=GOLD, width=4)
        c.ellipse(cx, cy, rx - 8, ry - 8, outline=mix(GOLD, GREEN, 0.4), width=2)
        for k, word in enumerate(words):
            wy = cy - 38 + k * 38
            if k == phase:
                c.rrect(cx - 28, wy - 16, 56, 32, 8, fill=mix(INK, GOLD, 0.55), outline=GOLD, width=2)
                c.text(cx, wy, word, font(22), INK, "mm")
            else:
                c.text(cx, wy, word, font(18), GOLD, "mm")
        c.rrect(cx - 7, cy + ry - 4, 14, 16, 3, fill=GOLD)
        c.rrect(cx - 26, cy + ry + 10, 52, 7, 3, fill=GOLD)
        c.rrect(28, 316, 344, 36, 10, fill=mix(INK, GOLD, 0.22), outline=GOLD, width=2)
        c.text(200, 334, banners[phase], font(16), GOLD, "mm")
        footer(c, "行有不得，皆反求諸己")
        frames.append(c.finish())
    return frames


def anim_yu_xiong(n: int = 32):
    frames = []
    for i in range(n):
        t = i / n
        c = Canvas()
        header(c, "魚與熊掌", 4)
        c.text(78, 78, "魚＝生", font(18), GOLD, "mm")
        c.text(200, 78, "VS", font(16), RED, "mm")
        c.text(322, 78, "熊掌＝義", font(18), GOLD, "mm")
        angle = 5 + 13 * ping(t)
        pans = draw_scale(c, 200, 198, angle, 96)
        fish_icon(c, pans[0][0], pans[0][1] - 32, 54, mix(GREEN, GOLD, 0.15), face_dir=1)
        ring = 40 + 6 * ping(t)
        c.ellipse(pans[1][0], pans[1][1] - 30, ring, ring * 0.82, outline=GOLD, width=3)
        paw_icon(c, pans[1][0], pans[1][1] - 28, 56, RED)
        c.text(200, 332, "二者不可得兼", font(18), GOLD, "mm")
        footer(c, "舍生取義 · 守住底線")
        frames.append(c.finish())
    return frames


def heaven(c: Canvas, cx, cy, t: float) -> None:
    outer = 46 + 3 * wave(t, cycles=1)
    rot = t * math.tau
    for i in range(9):
        ang = rot + i * math.tau / 9
        c.line(
            [
                (cx + math.cos(ang) * 24, cy + math.sin(ang) * 24),
                (cx + math.cos(ang) * outer, cy + math.sin(ang) * outer),
            ],
            GOLD,
            3,
        )
    c.ellipse(cx, cy, 22, 22, fill=mix(INK, GOLD, 0.35), outline=GOLD, width=2)
    c.text(cx, cy, "天", font(20), GOLD, "mm")


def chip(c: Canvas, x, y, glyph, label, fill, glyph_fill, bob) -> None:
    y = y + bob
    c.ellipse(x, y, 26, 26, fill=fill, outline=GOLD, width=2)
    if glyph == "heart":
        heart(c, x, y + 1, 22, RED)
    else:
        c.text(x, y, glyph, font(18), glyph_fill, "mm")
    c.text(x, y + 42, label, font(14), GOLD, "mm")


def anim_zun_yan(n: int = 30):
    frames = []
    for i in range(n):
        t = i / n
        c = Canvas()
        header(c, "天賦尊嚴", 5)
        heaven(c, 200, 92, t)
        c.text(200, 152, "你本來就有", font(16), GOLD, "mm")
        # flow lines into the person, drawn first so the figure covers the ends
        c.line([(200, 116), (200, 168)], mix(GOLD, GREEN, 0.2), 2)
        c.line([(86, 228), (150, 248)], GOLD, 2)
        c.line([(314, 228), (250, 248)], GOLD, 2)
        person(c, 200, 332, 158, GREEN, mood="happy", arm="open", reach=0.20, bob=3 * ping(t))
        rr = 34 + 8 * ping(t)
        c.ellipse(200, 336, rr, 9, outline=GOLD, width=2)
        chip(c, 62, 214, "heart", "憐憫", mix(INK, GREEN, 0.55), GOLD, 4 * wave(t))
        chip(c, 338, 214, "羞", "羞恥", GOLD, INK, 4 * wave(t, 0.35))
        footer(c, "憐憫＋羞恥 → 仁義")
        frames.append(c.finish())
    return frames


def save_gif(frames: list[Image.Image], name: str, duration: int) -> Path:
    path = OUT / name
    w, h = frames[0].size
    step = max(1, len(frames) // 8)
    sample = frames[::step]
    sheet = Image.new("RGB", (w, h * len(sample)))
    for i, fr in enumerate(sample):
        sheet.paste(fr, (0, i * h))
    palette = sheet.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    converted = [fr.quantize(palette=palette, dither=Image.Dither.NONE) for fr in frames]
    converted[0].save(
        path,
        save_all=True,
        append_images=converted[1:],
        duration=duration,
        loop=0,
        disposal=2,
        optimize=False,
    )
    return path


def verify(path: Path, frames: int) -> None:
    im = Image.open(path)
    n = im.n_frames
    if im.size != (SIZE, SIZE):
        raise SystemExit(f"{path.name}: size {im.size}, expected {(SIZE, SIZE)}")
    if not 24 <= n <= 36:
        raise SystemExit(f"{path.name}: {n} frames, expected 24–36")
    if n != frames:
        raise SystemExit(f"{path.name}: {n} frames, builder made {frames}")
    if im.format != "GIF":
        raise SystemExit(f"{path.name}: format {im.format}")
    duration = im.info.get("duration") or 0
    if duration <= 0:
        raise SystemExit(f"{path.name}: missing frame duration")
    print(f"{path.name:20} {im.size[0]}x{im.size[1]}  {n:2} frames  {duration:3} ms  {path.stat().st_size:7} bytes")


def main() -> None:
    if not Path(FONT_PATH).is_file():
        raise SystemExit(f"Missing font: {FONT_PATH}")
    jobs = (
        ("01_de_vs_li.gif", anim_de_vs_li, 32, 100),
        ("02_ren_ai.gif", anim_ren_ai, 30, 100),
        ("03_san_fan.gif", anim_san_fan, 36, 110),
        ("04_yu_xiong.gif", anim_yu_xiong, 32, 100),
        ("05_zun_yan.gif", anim_zun_yan, 30, 100),
    )
    for name, builder, count, duration in jobs:
        frames = builder(count)
        if len(frames) != count:
            raise SystemExit(f"{name}: built {len(frames)} frames")
        path = save_gif(frames, name, duration)
        verify(path, count)
    print("OK", OUT)


if __name__ == "__main__":
    main()
