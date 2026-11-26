#!/usr/bin/env python3
"""
My First Jumping Game – 3R99
Form 3 ICT worksheet (A. 1-player jumping game) + polished upgrades.

Requires: Python 3, tkinter, Pillow
  pip install Pillow
  (Thonny usually already has both)

Controls:
  Left / A  – move left
  Right / D – move right
  Up / Space – jump  (double-jump after collecting the ★ power-up)
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import io
import math
import random
import urllib.request
import tkinter as tk
from tkinter import font as tkfont

try:
    from PIL import Image, ImageTk, ImageDraw
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow is required. In Thonny: Tools → Manage packages → install Pillow\n"
        "Or run:  pip install Pillow"
    ) from exc

# Pillow 9 vs 10+ resampling compatibility (Thonny may ship either)
try:
    _RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:  # pragma: no cover
    _RESAMPLE = Image.LANCZOS


# ---------------------------------------------------------------------------
# Constants (PDF Step 1 – exact window size & title)
# ---------------------------------------------------------------------------
WINDOW_W = 400
WINDOW_H = 300
WINDOW_TITLE = "My First Jumping Game – 3R99"  # exact PDF title

BG_URL = (
    "https://encrypted-tbn0.gstatic.com/images?"
    "q=tbn:ANd9GcRIxXcmjljDf1HN-kUkmPdzJU8cdcOrfRr_hibwaAFmzA&s=10"
)

GRAVITY = 0.55
JUMP_VELOCITY = -9.2
MOVE_SPEED = 3.4
TICK_MS = 16  # ~60 FPS via root.after()

# Brown platform colours (classroom video style)
PLATFORM_FILL = "#8B5A2B"
PLATFORM_EDGE = "#5C3A1A"
PLATFORM_TOP = "#C4A484"

# Layouts: list of (x, y, width, height)  — y is top of platform
LAYOUTS = [
    # Layout 0 – classic climbing ruins (video style; gaps so you can fall)
    [
        (20, 275, 110, 16),     # start platform (walk off either side → fall)
        (150, 230, 90, 14),
        (280, 185, 90, 14),
        (100, 145, 90, 14),
        (240, 100, 90, 14),
        (60, 65, 90, 14),
        (150, 28, 120, 14),     # top / win platform
    ],
    # Layout 1 – staggered steps
    [
        (20, 270, 100, 14),
        (150, 230, 80, 14),
        (280, 200, 100, 14),
        (60, 160, 90, 14),
        (200, 120, 90, 14),
        (40, 80, 80, 14),
        (180, 40, 140, 14),
    ],
    # Layout 2 – wide islands with gaps
    [
        (0, 275, 110, 16),
        (160, 240, 80, 14),
        (300, 210, 100, 14),
        (80, 170, 90, 14),
        (250, 130, 80, 14),
        (40, 90, 100, 14),
        (200, 45, 120, 14),
    ],
]


# ===========================================================================
# PDF Step 1 helper – load background with urllib + PIL (fallback on failure)
# ===========================================================================
def load_background(width: int, height: int) -> Image.Image:
    """Download & resize the fantasy-ruins background; fallback to painted scene."""
    try:
        req = urllib.request.Request(
            BG_URL,
            headers={"User-Agent": "Mozilla/5.0 (compatible; Form3ICT/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read()
        img = Image.open(io.BytesIO(data)).convert("RGB")
        return img.resize((width, height), _RESAMPLE)
    except Exception:
        # Fallback: painted “ruins / dusk sky” so the game still runs offline
        img = Image.new("RGB", (width, height), (40, 55, 90))
        draw = ImageDraw.Draw(img)
        for y in range(height):
            t = y / max(height - 1, 1)
            r = int(40 + 80 * t)
            g = int(55 + 40 * t)
            b = int(90 + 20 * t)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        # Simple ruin silhouettes
        draw.rectangle([0, 220, 70, 300], fill=(55, 45, 40))
        draw.rectangle([330, 200, 400, 300], fill=(50, 42, 38))
        draw.polygon([(70, 220), (100, 160), (130, 220)], fill=(60, 50, 45))
        draw.ellipse([300, 30, 360, 80], fill=(240, 220, 160))  # moon
        return img


def make_wizard_sprite(facing_right: bool = True) -> Image.Image:
    """
    Draw a small wizard/staff character (classroom-video style).
    Returns a PIL RGBA image; caller flips for left-facing.
    """
    w, h = 28, 36
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Robe
    d.polygon([(8, 16), (20, 16), (24, 34), (4, 34)], fill=(70, 50, 140, 255))
    d.rectangle([10, 18, 18, 28], fill=(95, 70, 170, 255))
    # Head
    d.ellipse([9, 6, 19, 17], fill=(240, 205, 170, 255))
    # Hat
    d.polygon([(6, 10), (14, 0), (22, 10)], fill=(55, 35, 120, 255))
    d.ellipse([12, 1, 16, 5], fill=(220, 180, 60, 255))  # star tip
    # Eyes
    d.rectangle([11, 10, 13, 12], fill=(30, 20, 40, 255))
    d.rectangle([15, 10, 17, 12], fill=(30, 20, 40, 255))
    # Staff (right side by default)
    d.line([(22, 8), (24, 34)], fill=(160, 110, 50, 255), width=2)
    d.ellipse([20, 4, 26, 10], fill=(120, 200, 255, 255))

    if not facing_right:
        # PDF Step 3 – flip with PIL Image.transpose(FLIP_LEFT_RIGHT)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img


def make_star_icon() -> Image.Image:
    """Small gold star for the double-jump power-up."""
    size = 14
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy, r = size / 2, size / 2, size / 2 - 1
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=(255, 215, 60, 255), outline=(180, 130, 20, 255))
    return img


# ===========================================================================
# Platform class  (PDF Step 4)
# ===========================================================================
class Platform:
    """A solid brown rectangular platform the player can land on."""

    def __init__(self, canvas: tk.Canvas, x: int, y: int, w: int, h: int):
        self.x, self.y, self.w, self.h = x, y, w, h
        # Draw edge + fill + lighter top lip (video “brown brick” look)
        self.ids = [
            canvas.create_rectangle(
                x, y, x + w, y + h,
                fill=PLATFORM_FILL, outline=PLATFORM_EDGE, width=1,
            ),
            canvas.create_rectangle(
                x + 1, y, x + w - 1, y + 3,
                fill=PLATFORM_TOP, outline="",
            ),
        ]

    def bbox(self):
        return (self.x, self.y, self.x + self.w, self.y + self.h)

    def destroy(self, canvas: tk.Canvas):
        for i in self.ids:
            canvas.delete(i)


# ===========================================================================
# Particle (cool upgrade – jump / land sparkles)
# ===========================================================================
class Particle:
    def __init__(self, canvas, x, y, colour):
        self.canvas = canvas
        self.x, self.y = float(x), float(y)
        self.vx = random.uniform(-1.8, 1.8)
        self.vy = random.uniform(-3.0, -0.5)
        self.life = random.randint(12, 22)
        self.r = random.randint(1, 3)
        self.id = canvas.create_oval(
            x - self.r, y - self.r, x + self.r, y + self.r,
            fill=colour, outline="",
        )

    def update(self) -> bool:
        self.life -= 1
        if self.life <= 0:
            self.canvas.delete(self.id)
            return False
        self.vy += 0.25
        self.x += self.vx
        self.y += self.vy
        self.canvas.coords(
            self.id,
            self.x - self.r, self.y - self.r,
            self.x + self.r, self.y + self.r,
        )
        return True


# ===========================================================================
# Player class  (PDF Steps 2 & 3)
# ===========================================================================
class Player:
    """Controllable wizard with gravity, facing direction, and double-jump."""

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.w, self.h = 28, 36
        # Pre-build both facing sprites (PDF Step 3)
        right_pil = make_wizard_sprite(facing_right=True)
        left_pil = make_wizard_sprite(facing_right=False)
        self.photo_right = ImageTk.PhotoImage(right_pil)
        self.photo_left = ImageTk.PhotoImage(left_pil)
        self.facing_right = True

        self.x = 60.0
        self.y = 240.0
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.can_double_jump = False   # unlocked by power-up
        self.used_double_jump = False

        self.id = canvas.create_image(
            self.x, self.y, image=self.photo_right, anchor="nw",
        )

    def reset(self, x: float, y: float):
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.on_ground = False
        self.used_double_jump = False
        self.facing_right = True
        self.canvas.itemconfigure(self.id, image=self.photo_right)
        self._sync()

    def set_facing(self, right: bool):
        """PDF Step 3 – update sprite when direction changes."""
        if right == self.facing_right:
            return
        self.facing_right = right
        self.canvas.itemconfigure(
            self.id,
            image=self.photo_right if right else self.photo_left,
        )

    def jump(self) -> bool:
        """Return True if a jump (or double-jump) actually happened."""
        if self.on_ground:
            self.vy = JUMP_VELOCITY
            self.on_ground = False
            self.used_double_jump = False
            return True
        if self.can_double_jump and not self.used_double_jump:
            self.vy = JUMP_VELOCITY * 0.92
            self.used_double_jump = True
            return True
        return False

    def apply_input(self, keys: set):
        self.vx = 0.0
        if "Left" in keys or "a" in keys or "A" in keys:
            self.vx = -MOVE_SPEED
            self.set_facing(False)
        if "Right" in keys or "d" in keys or "D" in keys:
            self.vx = MOVE_SPEED
            self.set_facing(True)

    def physics(self, platforms: list):
        # Gravity
        self.vy += GRAVITY
        if self.vy > 12:
            self.vy = 12

        # Horizontal move + left/right boundary clamp (PDF Step 5)
        self.x += self.vx
        if self.x < 0:
            self.x = 0
        if self.x + self.w > WINDOW_W:
            self.x = WINDOW_W - self.w

        # Vertical move
        prev_bottom = self.y + self.h
        self.y += self.vy
        self.on_ground = False

        # Platform landing – only when falling onto the top surface
        # (fixes “fall through platform” / sinking bugs)
        if self.vy >= 0:
            feet = self.y + self.h
            for p in platforms:
                # Was above (or at) the platform top last frame, now overlapping
                if prev_bottom <= p.y + 2 and feet >= p.y:
                    # Horizontal overlap with a little margin
                    if self.x + self.w > p.x + 2 and self.x < p.x + p.w - 2:
                        self.y = p.y - self.h
                        self.vy = 0
                        self.on_ground = True
                        self.used_double_jump = False
                        break

        self._sync()

    def _sync(self):
        self.canvas.coords(self.id, self.x, self.y)

    def feet_xy(self):
        return (self.x + self.w / 2, self.y + self.h)

    def destroy(self):
        self.canvas.delete(self.id)


# ===========================================================================
# Game class – orchestrates PDF Steps 1–5 + upgrades
# ===========================================================================
class Game:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")

        self.canvas = tk.Canvas(
            root, width=WINDOW_W, height=WINDOW_H,
            highlightthickness=0, bg="#2a3550",
        )
        self.canvas.pack()

        # --- PDF Step 1: background from URL via urllib + PIL ---
        bg_pil = load_background(WINDOW_W, WINDOW_H)
        self.bg_photo = ImageTk.PhotoImage(bg_pil)
        self.bg_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.ui_font = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.small_font = tkfont.Font(family="Helvetica", size=9)

        self.keys: set = set()
        self.state = "start"  # start | play | gameover | win
        self.score = 0
        self.high_score = 0
        self.layout_index = 0
        self.max_height_bonus = 0

        self.platforms = []       # list of Platform
        self.player = None        # Player or None
        self.particles = []       # list of Particle
        self.powerup_id = None
        self.powerup_xy = None
        self.star_photo = ImageTk.PhotoImage(make_star_icon())

        self.ui_ids = []
        self.hud_ids = []

        self._bind_keys()
        self._show_start_screen()
        self._loop()

    # ------------------------------------------------------------------ keys
    def _bind_keys(self):
        self.root.bind("<KeyPress>", self._on_key_down)
        self.root.bind("<KeyRelease>", self._on_key_up)
        # Focus so arrow keys work in Thonny without clicking first
        self.canvas.focus_set()
        self.root.after(100, self.canvas.focus_set)

    def _on_key_down(self, event):
        key = event.keysym
        self.keys.add(key)
        if self.state == "play":
            if key in ("Up", "space", "w", "W"):
                jumped = self.player and self.player.jump()
                if jumped:
                    fx, fy = self.player.feet_xy()
                    self._burst(fx, fy, "#c8e6ff")
        # Prevent Space from scrolling / activating buttons unexpectedly
        if key == "space":
            return "break"

    def _on_key_up(self, event):
        self.keys.discard(event.keysym)

    # ---------------------------------------------------------- start screen
    # PDF Step 1 – centered title + Start Game button over background
    def _show_start_screen(self):
        self.state = "start"
        self._clear_ui()
        self._clear_world()

        # Semi-transparent-looking panel (solid, since Canvas has no alpha)
        panel = self.canvas.create_rectangle(
            60, 70, 340, 210, fill="#1a1a28", outline="#d4af37", width=2,
        )
        title = self.canvas.create_text(
            WINDOW_W // 2, 105,
            text="Jumping Game",
            fill="#f5e6c8", font=self.title_font,
        )
        subtitle = self.canvas.create_text(
            WINDOW_W // 2, 132,
            text="My First Jumping Game – 3R99",
            fill="#a0a8c0", font=self.small_font,
        )
        tip = self.canvas.create_text(
            WINDOW_W // 2, 155,
            text="← → move   Space / ↑ jump",
            fill="#8890a8", font=self.small_font,
        )
        self.ui_ids.extend([panel, title, subtitle, tip])

        # Start Game button (tk.Button placed over canvas, then fully hidden)
        self.start_btn = tk.Button(
            self.root,
            text="Start Game",
            font=self.ui_font,
            bg="#c9a227",
            fg="#1a1a28",
            activebackground="#e0bc40",
            activeforeground="#1a1a28",
            relief="raised",
            bd=2,
            padx=14,
            pady=4,
            cursor="hand2",
            command=self._start_game,
        )
        self.start_btn_window = self.canvas.create_window(
            WINDOW_W // 2, 185, window=self.start_btn,
        )
        self.ui_ids.append(self.start_btn_window)

        if self.high_score > 0:
            hs = self.canvas.create_text(
                WINDOW_W // 2, 250,
                text=f"High Score: {self.high_score}",
                fill="#d4af37", font=self.small_font,
            )
            self.ui_ids.append(hs)

    def _hide_start_ui(self):
        """PDF Step 1 – hide title and button completely on click."""
        self._clear_ui()
        if hasattr(self, "start_btn") and self.start_btn.winfo_exists():
            self.start_btn.destroy()

    # -------------------------------------------------------------- gameplay
    def _start_game(self):
        self._hide_start_ui()
        self.state = "play"
        self.score = 0
        self.max_height_bonus = 0
        self.layout_index = random.randrange(len(LAYOUTS))
        self._build_world()
        self._spawn_player()
        self._spawn_powerup()
        self._draw_hud()
        self.canvas.focus_set()

    def _build_world(self):
        self._clear_world(keep_player=False)
        layout = LAYOUTS[self.layout_index]
        for x, y, w, h in layout:
            self.platforms.append(Platform(self.canvas, x, y, w, h))

    def _spawn_player(self):
        if self.player:
            self.player.destroy()
        self.player = Player(self.canvas)
        # Start on first platform of the layout
        first = LAYOUTS[self.layout_index][0]
        px = first[0] + 20
        py = first[1] - 36
        self.player.reset(px, py)
        # Keep player above platforms visually (raise after platforms drawn)
        self.canvas.tag_raise(self.player.id)

    def _spawn_powerup(self):
        """Optional ★ power-up that unlocks double jump."""
        if self.powerup_id:
            self.canvas.delete(self.powerup_id)
            self.powerup_id = None
        # Place on a mid-height platform
        plats = LAYOUTS[self.layout_index]
        mid = plats[len(plats) // 2]
        self.powerup_xy = (mid[0] + mid[2] // 2 - 7, mid[1] - 18)
        self.powerup_id = self.canvas.create_image(
            self.powerup_xy[0], self.powerup_xy[1],
            image=self.star_photo, anchor="nw",
        )

    # --------------------------------------------------------------- HUD
    def _draw_hud(self):
        for i in self.hud_ids:
            self.canvas.delete(i)
        self.hud_ids.clear()
        self.hud_ids.append(
            self.canvas.create_text(
                8, 8, anchor="nw",
                text=f"Score: {self.score}",
                fill="#fff8e7", font=self.small_font,
            )
        )
        self.hud_ids.append(
            self.canvas.create_text(
                WINDOW_W - 8, 8, anchor="ne",
                text=f"Best: {self.high_score}",
                fill="#d4af37", font=self.small_font,
            )
        )
        if self.player and self.player.can_double_jump:
            self.hud_ids.append(
                self.canvas.create_text(
                    WINDOW_W // 2, 8, anchor="n",
                    text="★ Double Jump!",
                    fill="#7ec8ff", font=self.small_font,
                )
            )

    # ------------------------------------------------------- game over / win
    # PDF Step 5 – GAME OVER + Restart Game
    def _show_game_over(self, won: bool = False):
        self.state = "win" if won else "gameover"
        if self.score > self.high_score:
            self.high_score = self.score

        overlay = self.canvas.create_rectangle(
            50, 80, 350, 220, fill="#1a1a28", outline="#e07070", width=2,
        )
        msg = "YOU WIN!" if won else "GAME OVER"
        colour = "#7dcea0" if won else "#e74c3c"
        label = self.canvas.create_text(
            WINDOW_W // 2, 115,
            text=msg, fill=colour, font=self.title_font,
        )
        score_txt = self.canvas.create_text(
            WINDOW_W // 2, 145,
            text=f"Score: {self.score}   Best: {self.high_score}",
            fill="#f5e6c8", font=self.small_font,
        )
        self.ui_ids.extend([overlay, label, score_txt])

        self.restart_btn = tk.Button(
            self.root,
            text="Restart Game",
            font=self.ui_font,
            bg="#c0392b" if not won else "#27ae60",
            fg="white",
            activebackground="#e74c3c" if not won else "#2ecc71",
            activeforeground="white",
            relief="raised",
            bd=2,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self._restart,
        )
        self.restart_btn_window = self.canvas.create_window(
            WINDOW_W // 2, 185, window=self.restart_btn,
        )
        self.ui_ids.append(self.restart_btn_window)

    def _restart(self):
        """PDF Step 5 – reset character position, score, etc."""
        if hasattr(self, "restart_btn") and self.restart_btn.winfo_exists():
            self.restart_btn.destroy()
        self._clear_ui()
        # Full reset then go back to start screen (worksheet: Restart Game)
        # Also allow immediate replay:
        self._start_game()

    # -------------------------------------------------------------- particles
    def _burst(self, x, y, colour, n=8):
        for _ in range(n):
            self.particles.append(Particle(self.canvas, x, y, colour))

    # ---------------------------------------------------------------- loop
    def _loop(self):
        if self.state == "play" and self.player:
            was_grounded = self.player.on_ground
            self.player.apply_input(self.keys)
            self.player.physics(self.platforms)

            # Landing particles
            if self.player.on_ground and not was_grounded:
                fx, fy = self.player.feet_xy()
                self._burst(fx, fy, "#c4a484", n=6)

            # Score from climbing (higher = better)
            height_score = max(0, int((WINDOW_H - self.player.y) // 10))
            if height_score > self.max_height_bonus:
                self.score += height_score - self.max_height_bonus
                self.max_height_bonus = height_score
                self._draw_hud()

            # Power-up pickup
            if self.powerup_id and self.powerup_xy:
                px, py = self.powerup_xy
                if (
                    self.player.x < px + 14
                    and self.player.x + self.player.w > px
                    and self.player.y < py + 14
                    and self.player.y + self.player.h > py
                ):
                    self.canvas.delete(self.powerup_id)
                    self.powerup_id = None
                    self.player.can_double_jump = True
                    self.score += 25
                    self._burst(px + 7, py + 7, "#ffd93d", n=12)
                    self._draw_hud()

            # Win: land on the highest platform (last in layout) — video win area
            top = LAYOUTS[self.layout_index][-1]
            if self.player.on_ground:
                feet_y = self.player.y + self.player.h
                on_top = (
                    abs(feet_y - top[1]) < 3
                    and self.player.x + self.player.w > top[0] + 4
                    and self.player.x < top[0] + top[2] - 4
                )
                if on_top:
                    self.score += 100
                    self._show_game_over(won=True)

            # PDF Step 5 – fall below window → GAME OVER
            if self.player.y > WINDOW_H + 5:
                self._show_game_over(won=False)

        # Update particles always (even on game over for residual sparkle)
        alive = []
        for p in self.particles:
            if p.update():
                alive.append(p)
        self.particles = alive

        self.root.after(TICK_MS, self._loop)

    # --------------------------------------------------------------- cleanup
    def _clear_ui(self):
        for i in self.ui_ids:
            try:
                self.canvas.delete(i)
            except tk.TclError:
                pass
        self.ui_ids.clear()
        for i in self.hud_ids:
            try:
                self.canvas.delete(i)
            except tk.TclError:
                pass
        self.hud_ids.clear()

    def _clear_world(self, keep_player: bool = False):
        for p in self.platforms:
            p.destroy(self.canvas)
        self.platforms.clear()
        if self.powerup_id:
            self.canvas.delete(self.powerup_id)
            self.powerup_id = None
        for p in self.particles:
            self.canvas.delete(p.id)
        self.particles.clear()
        if not keep_player and self.player:
            self.player.destroy()
            self.player = None


# ===========================================================================
# Main
# ===========================================================================
def main():
    root = tk.Tk()
    # Ensure exact client size (some OSes pad for window chrome)
    root.title(WINDOW_TITLE)
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()
