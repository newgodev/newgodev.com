#!/usr/bin/env python3
"""
My First Jumping Game – 3G26
Form 3 ICT — 1-player jumping game (tkinter + Pillow). Thonny-ready.

=============================================================================
BRAINSTORM (chosen direction — implemented below, not leftover notes)
=============================================================================
Theme ........ Neon Sky Docks — cargo platforms floating above a night city.
Player ....... Astro-Courier (green slime in a bubble helmet). NOT a wizard.
Signature .... AIR DASH (Shift or X) — a short mid-air burst for gaps.
Power-up ..... Gold Core — unlocks a second dash charge until you land.
Goal ......... Reach the top dock beacon.
Layouts ...... 10 neon dock arrangements (gaps matter — don't fall!).
Extras ....... Dock coins, coyote-time jumps, walk frames, floating props.

Why cooler than a plain classroom demo?
  Original cyber-night vibe, a skill move beyond basic jump, free CC0 art
  from Kenney (not the worksheet's 2 teacher image links), and a goal that
  rewards climbing instead of only "don't die".

IMAGE URLS USED (CC0 — Kenney.nl via GitHub mirrors; more than 2 links):
  1. Background (wide):
     https://raw.githubusercontent.com/shorepine/kenney/main/2d/Background%20Elements%20Remastered/Backgrounds/backgroundColorForest.png
  2. Background fallback:
     https://raw.githubusercontent.com/steven-wertz/hackathon_2026/main/project/kenney_background-elements-remastered/Backgrounds/backgroundCastles.png
  3. Player stand (right-facing source):
     https://raw.githubusercontent.com/shorepine/kenney/main/2d/Pixel%20Platformer/Tiles/Characters/tile_0000.png
  4. Player run / second pose:
     https://raw.githubusercontent.com/shorepine/kenney/main/2d/Pixel%20Platformer/Tiles/Characters/tile_0001.png
  5. Player stand backup mirror:
     https://raw.githubusercontent.com/CodingQuests/godot-platformer-controller/main/assets/kenney_pixel-platformer/Tiles/Characters/tile_0000.png
  6. Platform tile (neon teal):
     https://raw.githubusercontent.com/shorepine/kenney/main/2d/Pixel%20Platformer/Tiles/tile_0057.png
  7. Platform accent / ice strip:
     https://raw.githubusercontent.com/shorepine/kenney/main/2d/Pixel%20Platformer/Tiles/tile_0033.png
  8. Extra prop — Gold Core power-up:
     https://raw.githubusercontent.com/shorepine/kenney/main/2d/Pixel%20Platformer/Tiles/tile_0011.png
  9. Extra prop — dock beacon gem:
     https://raw.githubusercontent.com/shorepine/kenney/main/2d/Pixel%20Platformer/Tiles/tile_0073.png
 10. Extra prop — dock coin / crate sparkle:
     https://raw.githubusercontent.com/shorepine/kenney/main/2d/Pixel%20Platformer/Tiles/tile_0028.png

  Left-facing frames are made with PIL Image.transpose(Image.FLIP_LEFT_RIGHT).
  Teacher worksheet gstatic URLs are intentionally NOT used.

Controls: ←/→ or A/D move | ↑ or Space jump | Shift or X air-dash
Requires: Python 3 + tkinter + Pillow   (pip install Pillow)
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
    from PIL import Image, ImageTk, ImageDraw, ImageEnhance
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow is required.\n"
        "Thonny: Tools → Manage packages → install Pillow\n"
        "Or: pip install Pillow"
    ) from exc

try:
    _RESAMPLE = Image.Resampling.LANCZOS
    _NEAREST = Image.Resampling.NEAREST
except AttributeError:  # older Pillow / some Thonny builds
    _RESAMPLE = Image.LANCZOS
    _NEAREST = Image.NEAREST


# ---------------------------------------------------------------------------
# Window size — NOT locked tiny anymore
# Worksheet base design is 400x300. SCALE makes the real window bigger.
#   SCALE = 2   →  800 x 600
#   SCALE = 2.5 → 1000 x 750   (default — comfortable)
#   SCALE = 3   → 1200 x 900
# Drag the window corners to resize. Press F11 for fullscreen.
# ---------------------------------------------------------------------------
SCALE = 2.5
BASE_W, BASE_H = 400, 300
WINDOW_W = int(BASE_W * SCALE)
WINDOW_H = int(BASE_H * SCALE)
WINDOW_TITLE = "My First Jumping Game – 3G26"  # class code 3G26


def S(v):
    """Scale a base-400x300 number up to the real window size."""
    return int(round(v * SCALE))


GRAVITY = 0.55 * SCALE
JUMP_VELOCITY = -9.0 * SCALE
JUMP_CUT = 0.45          # release jump early → shorter hop
MOVE_SPEED = 3.3 * SCALE
DASH_SPEED = 7.5 * SCALE
DASH_FRAMES = 10
COYOTE_FRAMES = 6        # jump briefly after walking off a dock
JUMP_BUFFER_FRAMES = 6   # press jump slightly early — still counts
TICK_MS = 16             # ~60 FPS with root.after()
PLATFORM_H = max(14, S(14))
TILE_PX = max(18, S(18))
SPRITE_ZOOM = max(2, int(round(2 * SCALE)))  # pixel-art upscale

# --- Image URLs (never the teacher's 2 worksheet links) ---
URL_BG_PRIMARY = (
    "https://raw.githubusercontent.com/shorepine/kenney/main/2d/"
    "Background%20Elements%20Remastered/Backgrounds/backgroundColorForest.png"
)
URL_BG_FALLBACK = (
    "https://raw.githubusercontent.com/steven-wertz/hackathon_2026/main/"
    "project/kenney_background-elements-remastered/Backgrounds/backgroundCastles.png"
)
URL_PLAYER_STAND = (
    "https://raw.githubusercontent.com/shorepine/kenney/main/2d/"
    "Pixel%20Platformer/Tiles/Characters/tile_0000.png"
)
URL_PLAYER_RUN = (
    "https://raw.githubusercontent.com/shorepine/kenney/main/2d/"
    "Pixel%20Platformer/Tiles/Characters/tile_0001.png"
)
URL_PLAYER_STAND_MIRROR = (
    "https://raw.githubusercontent.com/CodingQuests/godot-platformer-controller/"
    "main/assets/kenney_pixel-platformer/Tiles/Characters/tile_0000.png"
)
URL_PLATFORM = (
    "https://raw.githubusercontent.com/shorepine/kenney/main/2d/"
    "Pixel%20Platformer/Tiles/tile_0057.png"
)
URL_PLATFORM_ICE = (
    "https://raw.githubusercontent.com/shorepine/kenney/main/2d/"
    "Pixel%20Platformer/Tiles/tile_0033.png"
)
URL_GOLD_CORE = (
    "https://raw.githubusercontent.com/shorepine/kenney/main/2d/"
    "Pixel%20Platformer/Tiles/tile_0011.png"
)
URL_BEACON = (
    "https://raw.githubusercontent.com/shorepine/kenney/main/2d/"
    "Pixel%20Platformer/Tiles/tile_0073.png"
)
URL_COIN = (
    "https://raw.githubusercontent.com/shorepine/kenney/main/2d/"
    "Pixel%20Platformer/Tiles/tile_0028.png"
)

LAYOUT_NAMES = [
    "Starter Climb", "Wide Gaps", "Zigzag", "Twin Towers", "Narrow Steps",
    "Long Mid Dock", "Left Wall Climb", "Sky Marathon", "Cascade", "Mirror Run",
]

# Hard block: if these substrings appear, we refuse them (teacher worksheet).
_FORBIDDEN_URL_BITS = (
    "encrypted-tbn0.gstatic.com",
    "ANd9GcRIxXcmjljDf1HN-kUkmPdzJU8cdcOrfRr_hibwaAFmzA",
)

# Dock layouts in BASE 400x300 coords — scaled with S() when building
LAYOUTS = [
    # 0 — starter climb
    [(20, 270, 100), (140, 225, 80), (260, 185, 90), (80, 140, 80),
     (220, 100, 90), (60, 60, 80), (160, 25, 110)],
    # 1 — wide gaps (dash helps)
    [(10, 275, 90), (160, 235, 70), (300, 200, 80), (40, 155, 70),
     (200, 115, 80), (320, 75, 70), (120, 30, 120)],
    # 2 — zigzag
    [(30, 270, 80), (200, 240, 90), (50, 195, 80), (250, 155, 90),
     (80, 110, 80), (240, 70, 90), (140, 28, 120)],
    # 3 — twin towers
    [(20, 270, 70), (310, 270, 70), (60, 220, 70), (270, 220, 70),
     (100, 160, 70), (230, 160, 70), (150, 100, 100), (160, 35, 100)],
    # 4 — narrow steps
    [(40, 275, 60), (120, 235, 55), (200, 195, 55), (280, 155, 55),
     (180, 115, 60), (80, 75, 60), (180, 30, 110)],
    # 5 — long mid dock
    [(0, 275, 100), (150, 240, 140), (40, 185, 80), (260, 150, 90),
     (100, 105, 90), (250, 65, 80), (130, 25, 130)],
    # 6 — left wall climb
    [(10, 275, 120), (20, 230, 70), (30, 185, 70), (40, 140, 70),
     (120, 100, 90), (240, 65, 90), (150, 25, 120)],
    # 7 — sky marathon
    [(30, 270, 80), (150, 245, 60), (260, 210, 70), (100, 170, 60),
     (220, 130, 70), (50, 90, 70), (180, 55, 80), (140, 22, 120)],
    # 8 — cascade (step down then up)
    [(20, 270, 90), (130, 250, 70), (240, 220, 70), (320, 180, 60),
     (200, 140, 80), (80, 100, 80), (200, 60, 90), (150, 22, 120)],
    # 9 — mirror run
    [(20, 275, 80), (300, 275, 80), (80, 230, 70), (250, 230, 70),
     (40, 175, 70), (290, 175, 70), (120, 120, 80), (200, 70, 80),
     (140, 25, 120)],
]


# ===========================================================================
# Asset helpers — download real open-web PNGs, never teacher links
# ===========================================================================
def _assert_not_teacher_url(url):
    low = url.lower()
    for bit in _FORBIDDEN_URL_BITS:
        if bit.lower() in low:
            raise ValueError("Refusing teacher worksheet image URL: " + url)


def fetch_image(urls, label="asset"):
    """Try each URL in order. Return PIL Image or None."""
    if isinstance(urls, str):
        urls = [urls]
    last_err = None
    for url in urls:
        try:
            _assert_not_teacher_url(url)
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 (Form3-ICT-3G26)"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
            img = Image.open(io.BytesIO(data))
            img.load()
            return img.convert("RGBA")
        except Exception as err:
            last_err = err
            print(f"[warn] {label} failed: {url} -> {err}")
    print(f"[warn] all URLs failed for {label}; last error: {last_err}")
    return None


def neon_tint_background(img, width, height):
    """Turn a daytime Kenney backdrop into a neon night sky-docks scene."""
    img = img.convert("RGB").resize((width, height), _RESAMPLE)
    # Darken + cool shift
    img = ImageEnhance.Brightness(img).enhance(0.35)
    img = ImageEnhance.Color(img).enhance(1.4)
    # Cyan/magenta night wash
    overlay = Image.new("RGB", (width, height), (10, 20, 55))
    img = Image.blend(img, overlay, 0.45)
    draw = ImageDraw.Draw(img)
    # Distant neon windows
    random.seed(26)
    for _ in range(40):
        x = random.randint(0, width - 2)
        y = random.randint(40, height - 40)
        colour = random.choice([(0, 255, 200), (255, 60, 180), (80, 180, 255)])
        draw.rectangle([x, y, x + 1, y + 2], fill=colour)
    # Soft horizon glow
    for y in range(height - 50, height):
        t = (y - (height - 50)) / 50.0
        shade = int(20 + 40 * t)
        draw.line([(0, y), (width, y)], fill=(shade, 10, shade + 20))
    return img.convert("RGBA")


def drawn_neon_background(width, height):
    """Last-resort original backdrop if every remote URL fails."""
    img = Image.new("RGBA", (width, height), (8, 12, 40, 255))
    d = ImageDraw.Draw(img)
    for y in range(height):
        t = y / max(height - 1, 1)
        d.line([(0, y), (width, y)], fill=(8, 12 + int(30 * t), 40 + int(50 * t), 255))
    for i in range(8):
        x = 20 + i * 48
        h = 40 + (i * 17) % 90
        d.rectangle([x, height - h, x + 30, height], fill=(15, 25, 60, 255))
        d.rectangle([x + 6, height - h + 8, x + 10, height - h + 14], fill=(0, 255, 200, 255))
    d.ellipse([300, 20, 360, 70], fill=(200, 220, 255, 180))
    return img


def drawn_courier(size=36):
    """Original placeholder courier if character URLs fail."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([6, 4, size - 6, size - 8], fill=(40, 220, 160, 255), outline=(20, 120, 100, 255))
    d.ellipse([10, 8, size - 10, size - 14], fill=(180, 255, 240, 120))
    d.rectangle([14, 16, 18, 20], fill=(20, 40, 40, 255))
    d.rectangle([22, 16, 26, 20], fill=(20, 40, 40, 255))
    return img


def drawn_platform_tile(size=18):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, size - 1, size - 1], fill=(20, 160, 140, 255), outline=(10, 60, 70, 255))
    d.rectangle([1, 1, size - 2, 4], fill=(80, 255, 210, 255))
    return img


def drawn_gold_core(size=18):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([1, 1, size - 2, size - 2], fill=(255, 200, 40, 255), outline=(160, 100, 20, 255))
    d.ellipse([5, 5, size - 6, size - 6], fill=(255, 255, 200, 255))
    return img


def load_all_assets():
    """
    Download every remote asset we need.
    Comments which URLs were tried if we must draw placeholders.
    """
    assets = {"tried": []}

    # 1) Background
    bg = fetch_image([URL_BG_PRIMARY, URL_BG_FALLBACK], "background")
    assets["tried"].extend([URL_BG_PRIMARY, URL_BG_FALLBACK])
    if bg is not None:
        assets["bg"] = neon_tint_background(bg, WINDOW_W, WINDOW_H)
    else:
        assets["bg"] = drawn_neon_background(WINDOW_W, WINDOW_H)

    # 2–3) Player stand + run (flip later for left)
    stand = fetch_image([URL_PLAYER_STAND, URL_PLAYER_STAND_MIRROR], "player_stand")
    assets["tried"].extend([URL_PLAYER_STAND, URL_PLAYER_STAND_MIRROR])
    run = fetch_image([URL_PLAYER_RUN], "player_run")
    assets["tried"].append(URL_PLAYER_RUN)
    if stand is None:
        stand = drawn_courier(36)
    if run is None:
        run = stand.copy()
    # Scale up pixel art crisply (grows with SCALE)
    stand = stand.resize(
        (stand.width * SPRITE_ZOOM, stand.height * SPRITE_ZOOM), _NEAREST,
    )
    run = run.resize(
        (run.width * SPRITE_ZOOM, run.height * SPRITE_ZOOM), _NEAREST,
    )
    assets["player_stand_r"] = stand
    assets["player_run_r"] = run
    # Step 3 — facing left via FLIP_LEFT_RIGHT
    assets["player_stand_l"] = stand.transpose(Image.FLIP_LEFT_RIGHT)
    assets["player_run_l"] = run.transpose(Image.FLIP_LEFT_RIGHT)

    # 4) Platform tiles
    plat = fetch_image([URL_PLATFORM, URL_PLATFORM_ICE], "platform")
    assets["tried"].extend([URL_PLATFORM, URL_PLATFORM_ICE])
    ice = fetch_image([URL_PLATFORM_ICE], "platform_ice")
    assets["tried"].append(URL_PLATFORM_ICE)
    if plat is None:
        plat = drawn_platform_tile(18)
    if ice is None:
        ice = plat.copy()
    assets["platform_tile"] = plat.resize((TILE_PX, TILE_PX), _NEAREST)
    assets["ice_tile"] = ice.resize((TILE_PX, TILE_PX), _NEAREST)

    # 5) Extra props
    gold = fetch_image([URL_GOLD_CORE], "gold_core")
    assets["tried"].append(URL_GOLD_CORE)
    beacon = fetch_image([URL_BEACON, URL_GOLD_CORE], "beacon")
    assets["tried"].extend([URL_BEACON, URL_GOLD_CORE])
    coin = fetch_image([URL_COIN, URL_GOLD_CORE], "dock_coin")
    assets["tried"].extend([URL_COIN, URL_GOLD_CORE])
    if gold is None:
        gold = drawn_gold_core(18)
    if beacon is None:
        beacon = gold.copy()
    if coin is None:
        coin = gold.copy()
    assets["gold"] = gold.resize((S(20), S(20)), _NEAREST)
    assets["beacon"] = beacon.resize((S(22), S(22)), _NEAREST)
    assets["coin"] = coin.resize((S(16), S(16)), _NEAREST)
    return assets


def build_platform_surface(tile_img, width_px, height_px=None):
    """Tile a small PNG across a platform width."""
    if height_px is None:
        height_px = PLATFORM_H
    tile = tile_img.resize((TILE_PX, height_px), _NEAREST)
    surf = Image.new("RGBA", (max(width_px, TILE_PX), height_px), (0, 0, 0, 0))
    x = 0
    while x < width_px:
        surf.paste(tile, (x, 0), tile)
        x += tile.width
    return surf.crop((0, 0, width_px, height_px))


def scaled_layout(index):
    """Turn a base 400x300 layout into real pixel coords for this SCALE."""
    return [(S(x), S(y), S(w)) for (x, y, w) in LAYOUTS[index]]


# ===========================================================================
# Platform  (school step 4)
# ===========================================================================
class Platform:
    def __init__(self, canvas, x, y, w, tile_photo, h=14):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.id = canvas.create_image(x, y, image=tile_photo, anchor="nw")
        self.photo = tile_photo  # keep reference so Tk does not GC it

    def destroy(self, canvas):
        canvas.delete(self.id)


# ===========================================================================
# Particles — jump dust (cool upgrade)
# ===========================================================================
class Particle:
    def __init__(self, canvas, x, y, colour):
        self.canvas = canvas
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-1.6, 1.6)
        self.vy = random.uniform(-2.8, -0.4)
        self.life = random.randint(10, 20)
        self.r = random.randint(1, 3)
        self.id = canvas.create_oval(
            x - self.r, y - self.r, x + self.r, y + self.r,
            fill=colour, outline="",
        )

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.canvas.delete(self.id)
            return False
        self.vy += 0.22
        self.x += self.vx
        self.y += self.vy
        self.canvas.coords(
            self.id,
            self.x - self.r, self.y - self.r,
            self.x + self.r, self.y + self.r,
        )
        return True


# ===========================================================================
# Player  (school steps 2 & 3) + air dash signature move
# ===========================================================================
class Player:
    def __init__(self, canvas, photos):
        """
        photos keys: stand_r, stand_l, run_r, run_l  (PhotoImage)
        Left frames were built with Image.transpose(FLIP_LEFT_RIGHT).
        """
        self.canvas = canvas
        self.photos = photos
        self.w = photos["stand_r"].width()
        self.h = photos["stand_r"].height()

        self.x = 40.0
        self.y = 200.0
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.facing_right = True

        # Signature move: air dash
        self.dash_charges = 1          # 1 by default; Gold Core → 2
        self.dash_charges_max = 1
        self.dash_left = 0             # frames remaining in a dash
        self.dash_dir = 1

        # Feel upgrades — coyote time + jump buffer (still no infinite jump)
        self.coyote = 0
        self.jump_buffer = 0
        self.jump_held = False

        self.anim_tick = 0
        self.use_run_frame = False
        self.id = canvas.create_image(
            self.x, self.y, image=photos["stand_r"], anchor="nw",
        )

    def reset(self, x, y, keep_power=False):
        self.x, self.y = float(x), float(y)
        self.vx = self.vy = 0.0
        self.on_ground = False
        self.facing_right = True
        self.dash_left = 0
        self.coyote = 0
        self.jump_buffer = 0
        self.jump_held = False
        self.anim_tick = 0
        self.use_run_frame = False
        if not keep_power:
            self.dash_charges_max = 1
        self.dash_charges = self.dash_charges_max
        self._set_image(self.photos["stand_r"])
        self._sync()

    def _set_image(self, photo):
        self.canvas.itemconfigure(self.id, image=photo)

    def set_facing(self, right):
        # School step 3 — facing must visibly change
        if right == self.facing_right:
            return
        self.facing_right = right
        self._refresh_sprite()

    def _refresh_sprite(self):
        moving = abs(self.vx) > 0.1 or self.dash_left > 0
        if moving:
            self.anim_tick += 1
            if self.anim_tick >= 6:
                self.anim_tick = 0
                self.use_run_frame = not self.use_run_frame
        else:
            self.use_run_frame = False
            self.anim_tick = 0
        if self.facing_right:
            key = "run_r" if self.use_run_frame else "stand_r"
        else:
            key = "run_l" if self.use_run_frame else "stand_l"
        # While airborne prefer the run pose (looks like a leap)
        if not self.on_ground and self.dash_left == 0:
            key = "run_r" if self.facing_right else "run_l"
        self._set_image(self.photos[key])

    def request_jump(self):
        """Queue a jump (buffer) — actual jump may fire this frame or soon."""
        self.jump_buffer = JUMP_BUFFER_FRAMES
        return self._try_jump()

    def _try_jump(self):
        can = self.on_ground or self.coyote > 0
        if not can:
            return False
        self.vy = JUMP_VELOCITY
        self.on_ground = False
        self.coyote = 0
        self.jump_buffer = 0
        self.jump_held = True
        return True

    def release_jump(self):
        """Variable jump height — let go early to hop shorter."""
        self.jump_held = False
        if self.vy < 0:
            self.vy *= JUMP_CUT

    def jump(self):
        # Kept for tests / simple call sites
        return self.request_jump()

    def dash(self):
        """Signature move — mid-air horizontal burst (no infinite spam)."""
        if self.on_ground:
            return False
        if self.dash_charges <= 0 or self.dash_left > 0:
            return False
        self.dash_charges -= 1
        self.dash_left = DASH_FRAMES
        self.dash_dir = 1 if self.facing_right else -1
        self.vy = min(self.vy, -1.5)  # slight lift so dash feels snappy
        return True

    def apply_input(self, keys):
        if self.dash_left > 0:
            self.vx = self.dash_dir * DASH_SPEED
            self._refresh_sprite()
            return

        self.vx = 0.0
        if "Left" in keys or "a" in keys or "A" in keys:
            self.vx = -MOVE_SPEED
            self.set_facing(False)
        if "Right" in keys or "d" in keys or "D" in keys:
            self.vx = MOVE_SPEED
            self.set_facing(True)
        self._refresh_sprite()

    def physics(self, platforms):
        if self.coyote > 0:
            self.coyote -= 1
        if self.jump_buffer > 0:
            self.jump_buffer -= 1
            if self._try_jump():
                pass

        if self.dash_left > 0:
            self.dash_left -= 1
        else:
            self.vy += GRAVITY
            max_fall = 12 * SCALE
            if self.vy > max_fall:
                self.vy = max_fall

        # Horizontal + left/right edges (school step 5)
        self.x += self.vx
        if self.x < 0:
            self.x = 0
        if self.x + self.w > WINDOW_W:
            self.x = WINDOW_W - self.w

        prev_bottom = self.y + self.h
        was_grounded = self.on_ground
        self.y += self.vy
        self.on_ground = False

        # Land on platform tops only when falling (fixes tunneling / sinking)
        if self.vy >= 0:
            feet = self.y + self.h
            for p in platforms:
                if prev_bottom <= p.y + 3 and feet >= p.y:
                    if self.x + self.w > p.x + 2 and self.x < p.x + p.w - 2:
                        self.y = p.y - self.h
                        self.vy = 0
                        self.on_ground = True
                        self.dash_charges = self.dash_charges_max
                        self.coyote = COYOTE_FRAMES
                        break

        # Just walked off a ledge → start coyote timer
        if was_grounded and not self.on_ground and self.vy >= 0:
            self.coyote = COYOTE_FRAMES

        self._sync()

    def _sync(self):
        self.canvas.coords(self.id, self.x, self.y)

    def feet_xy(self):
        return (self.x + self.w / 2, self.y + self.h)

    def destroy(self):
        self.canvas.delete(self.id)


# ===========================================================================
# Game — school steps 1–5 + cool upgrades
# ===========================================================================
class Game:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        # UNLOCKED — drag corners to resize; F11 = fullscreen
        self.root.resizable(True, True)
        self.root.minsize(BASE_W, BASE_H)
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self._fullscreen = False

        self.canvas = tk.Canvas(
            root, width=WINDOW_W, height=WINDOW_H,
            highlightthickness=0, bg="#0a1028",
        )
        self.canvas.pack(fill="both", expand=True)

        # Load open-web art (our URLs, not the teacher's)
        self.raw = load_all_assets()
        self.bg_photo = ImageTk.PhotoImage(self.raw["bg"])
        self.bg_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Keep PhotoImage refs alive
        self._photos = {
            "stand_r": ImageTk.PhotoImage(self.raw["player_stand_r"]),
            "stand_l": ImageTk.PhotoImage(self.raw["player_stand_l"]),
            "run_r": ImageTk.PhotoImage(self.raw["player_run_r"]),
            "run_l": ImageTk.PhotoImage(self.raw["player_run_l"]),
            "gold": ImageTk.PhotoImage(self.raw["gold"]),
            "beacon": ImageTk.PhotoImage(self.raw["beacon"]),
            "coin": ImageTk.PhotoImage(self.raw["coin"]),
        }
        self._plat_photos = []  # per-platform tiled images

        # Fonts scale with window so UI isn't tiny
        self.title_font = tkfont.Font(
            family="Helvetica", size=max(18, S(18)), weight="bold",
        )
        self.ui_font = tkfont.Font(
            family="Helvetica", size=max(11, S(11)), weight="bold",
        )
        self.small_font = tkfont.Font(
            family="Helvetica", size=max(9, S(9)),
        )

        self.keys = set()
        self.state = "start"  # start | play | gameover | win
        self.score = 0
        self.high_score = 0
        self.layout_index = 0
        self.max_height_bonus = 0
        self.has_gold_core = False
        self.tick = 0
        self.coins_collected = 0

        self.platforms = []
        self.player = None
        self.particles = []
        self.coins = []  # list of {id, base_x, base_y}
        self.gold_id = None
        self.gold_base = None
        self.beacon_id = None
        self.beacon_base = None
        self.top_platform = None
        self.star_ids = []
        self.float_msg_id = None
        self.float_msg_life = 0

        self.ui_ids = []
        self.hud_ids = []

        self._spawn_stars()
        self._bind_keys()
        self.root.bind("<F11>", self._toggle_fullscreen)
        self.root.bind("<Escape>", self._exit_fullscreen)
        self.root.bind("<Configure>", self._on_resize)
        self._show_start_screen()   # school step 1
        self._loop()

    def _toggle_fullscreen(self, _event=None):
        self._fullscreen = not self._fullscreen
        self.root.attributes("-fullscreen", self._fullscreen)

    def _exit_fullscreen(self, _event=None):
        if self._fullscreen:
            self._fullscreen = False
            self.root.attributes("-fullscreen", False)

    def _on_resize(self, event):
        """Keep canvas filling the window when you drag it bigger/smaller."""
        if event.widget is not self.root:
            return
        # Canvas already expand=True; stretch the backdrop image item's space
        w = max(event.width, BASE_W)
        h = max(event.height, BASE_H)
        self.canvas.config(width=w, height=h)

    def _spawn_stars(self):
        """Twinkling neon stars above the docks (canvas overlay)."""
        random.seed(99)
        for _ in range(28):
            x = random.randint(8, WINDOW_W - 8)
            y = random.randint(8, S(120))
            r = random.choice([1, 1, 2, 2, 3])
            colour = random.choice(["#ffffff", "#7ef9e0", "#ff7adc", "#a0c4ff"])
            sid = self.canvas.create_oval(
                x - r, y - r, x + r, y + r, fill=colour, outline="",
            )
            self.star_ids.append((sid, r, colour))

    # -------------------------------------------------------------- keys
    def _bind_keys(self):
        self.root.bind("<KeyPress>", self._on_key_down)
        self.root.bind("<KeyRelease>", self._on_key_up)
        self.canvas.focus_set()
        self.root.after(80, self.canvas.focus_set)

    def _on_key_down(self, event):
        key = event.keysym
        self.keys.add(key)
        if self.state == "play" and self.player:
            if key in ("Up", "space", "w", "W"):
                if self.player.request_jump():
                    fx, fy = self.player.feet_xy()
                    self._burst(fx, fy, "#7ef9e0")
            if key in ("Shift_L", "Shift_R", "x", "X"):
                if self.player.dash():
                    fx, fy = self.player.feet_xy()
                    self._burst(fx, fy - 8, "#ff4fd8", n=10)
                    self._toast("+ DASH")
            if key == "space":
                return "break"

    def _on_key_up(self, event):
        key = event.keysym
        self.keys.discard(key)
        if self.state == "play" and self.player:
            if key in ("Up", "space", "w", "W"):
                self.player.release_jump()

    # -------------------------------------------------- school step 1 UI
    def _show_start_screen(self):
        self.state = "start"
        self._clear_ui()
        self._clear_world()

        panel = self.canvas.create_rectangle(
            S(50), S(55), S(350), S(230),
            fill="#0d1228", outline="#00e6c0", width=2,
        )
        title = self.canvas.create_text(
            WINDOW_W // 2, S(85),
            text="Jumping Game", fill="#e8fff8", font=self.title_font,
        )
        sub = self.canvas.create_text(
            WINDOW_W // 2, S(112),
            text="Neon Sky Docks · Astro-Courier",
            fill="#7ec8ff", font=self.small_font,
        )
        tip = self.canvas.create_text(
            WINDOW_W // 2, S(138),
            text="← → move · Space jump · Shift dash · F11 fullscreen",
            fill="#8899bb", font=self.small_font,
        )
        class_tag = self.canvas.create_text(
            WINDOW_W // 2, S(158),
            text=WINDOW_TITLE + f"  ({WINDOW_W}x{WINDOW_H})",
            fill="#556688", font=self.small_font,
        )
        self.ui_ids.extend([panel, title, sub, tip, class_tag])

        self.start_btn = tk.Button(
            self.root, text="Start Game", font=self.ui_font,
            bg="#00c9a0", fg="#0a1028",
            activebackground="#5dffd0", activeforeground="#0a1028",
            relief="raised", bd=2, padx=14, pady=4, cursor="hand2",
            command=self._start_game,
        )
        self.start_btn_window = self.canvas.create_window(
            WINDOW_W // 2, S(195), window=self.start_btn,
        )
        self.ui_ids.append(self.start_btn_window)

        if self.high_score > 0:
            hs = self.canvas.create_text(
                WINDOW_W // 2, S(255),
                text=f"High Score: {self.high_score}",
                fill="#ffd76a", font=self.small_font,
            )
            self.ui_ids.append(hs)

    def _hide_start_ui(self):
        """Hide title + Start Game completely (school step 1)."""
        self._clear_ui()
        if hasattr(self, "start_btn") and self.start_btn.winfo_exists():
            self.start_btn.destroy()

    # ----------------------------------------------------------- gameplay
    def _start_game(self):
        self._hide_start_ui()
        self.state = "play"
        self.score = 0
        self.max_height_bonus = 0
        self.has_gold_core = False
        self.coins_collected = 0
        self.float_msg_life = 0
        if self.float_msg_id:
            self.canvas.delete(self.float_msg_id)
            self.float_msg_id = None
        self.layout_index = random.randrange(len(LAYOUTS))
        self._build_world()
        self._spawn_player()
        self._spawn_props()
        self._draw_hud()
        self.canvas.focus_set()

    def _build_world(self):
        self._clear_world(keep_player=False)
        self._plat_photos = []
        layout = scaled_layout(self.layout_index)
        for i, (x, y, w) in enumerate(layout):
            # Mix neon teal + ice accent strips
            tile = self.raw["ice_tile"] if i % 3 == 2 else self.raw["platform_tile"]
            surf = build_platform_surface(tile, w, PLATFORM_H)
            photo = ImageTk.PhotoImage(surf)
            self._plat_photos.append(photo)
            self.platforms.append(
                Platform(self.canvas, x, y, w, photo, PLATFORM_H),
            )
        self.top_platform = self.platforms[-1]

    def _spawn_player(self):
        if self.player:
            self.player.destroy()
        self.player = Player(self.canvas, self._photos)
        first = scaled_layout(self.layout_index)[0]
        self.player.reset(first[0] + S(16), first[1] - self.player.h)
        self.canvas.tag_raise(self.player.id)

    def _spawn_props(self):
        # Gold Core power-up on a mid dock
        layout = scaled_layout(self.layout_index)
        mid = layout[len(layout) // 2]
        self.gold_base = (mid[0] + mid[2] // 2 - S(10), mid[1] - S(24))
        self.gold_id = self.canvas.create_image(
            self.gold_base[0], self.gold_base[1],
            image=self._photos["gold"], anchor="nw",
        )
        # Goal beacon on the top platform
        top = layout[-1]
        self.beacon_base = (top[0] + top[2] // 2 - S(11), top[1] - S(26))
        self.beacon_id = self.canvas.create_image(
            self.beacon_base[0], self.beacon_base[1],
            image=self._photos["beacon"], anchor="nw",
        )
        # Dock coins on a few platforms (skip first + last)
        self.coins = []
        for plat in layout[1:-1:2]:
            cx = plat[0] + plat[2] // 2 - S(8)
            cy = plat[1] - S(20)
            cid = self.canvas.create_image(
                cx, cy, image=self._photos["coin"], anchor="nw",
            )
            self.coins.append({"id": cid, "base": (cx, cy)})

    def _toast(self, text):
        if self.float_msg_id:
            self.canvas.delete(self.float_msg_id)
        self.float_msg_id = self.canvas.create_text(
            WINDOW_W // 2, S(40), text=text, fill="#ff7adc", font=self.small_font,
        )
        self.float_msg_life = 40

    # ---------------------------------------------------------------- HUD
    def _draw_hud(self):
        for i in self.hud_ids:
            self.canvas.delete(i)
        self.hud_ids.clear()
        name = LAYOUT_NAMES[self.layout_index % len(LAYOUT_NAMES)]
        self.hud_ids.append(self.canvas.create_text(
            8, 6, anchor="nw",
            text=f"Score: {self.score}  coins:{self.coins_collected}",
            fill="#e8fff8", font=self.small_font,
        ))
        self.hud_ids.append(self.canvas.create_text(
            WINDOW_W - 8, 6, anchor="ne", text=f"Best: {self.high_score}",
            fill="#ffd76a", font=self.small_font,
        ))
        dash_txt = f"Dash x{self.player.dash_charges}" if self.player else ""
        if self.has_gold_core:
            dash_txt += " ★"
        self.hud_ids.append(self.canvas.create_text(
            WINDOW_W // 2, 6, anchor="n", text=dash_txt,
            fill="#ff7adc", font=self.small_font,
        ))
        self.hud_ids.append(self.canvas.create_text(
            WINDOW_W // 2, S(20), anchor="n",
            text=f"Dock: {name}   (F11 fullscreen · drag to resize)",
            fill="#667799", font=self.small_font,
        ))

    # ----------------------------------------- school step 5 game over
    def _show_game_over(self, won=False):
        self.state = "win" if won else "gameover"
        if self.score > self.high_score:
            self.high_score = self.score

        colour = "#5dffd0" if won else "#ff5c6a"
        border = "#00e6c0" if won else "#ff5c6a"
        msg = "DOCK REACHED!" if won else "GAME OVER"

        overlay = self.canvas.create_rectangle(
            S(50), S(75), S(350), S(225),
            fill="#0d1228", outline=border, width=2,
        )
        label = self.canvas.create_text(
            WINDOW_W // 2, S(110), text=msg, fill=colour, font=self.title_font,
        )
        score_txt = self.canvas.create_text(
            WINDOW_W // 2, S(145),
            text=f"Score: {self.score}   Best: {self.high_score}",
            fill="#e8fff8", font=self.small_font,
        )
        self.ui_ids.extend([overlay, label, score_txt])

        self.restart_btn = tk.Button(
            self.root, text="Restart Game", font=self.ui_font,
            bg="#00a884" if won else "#c0392b", fg="white",
            activebackground="#5dffd0" if won else "#e74c3c",
            activeforeground="#0a1028" if won else "white",
            relief="raised", bd=2, padx=12, pady=4, cursor="hand2",
            command=self._restart,
        )
        self.restart_btn_window = self.canvas.create_window(
            WINDOW_W // 2, S(185), window=self.restart_btn,
        )
        self.ui_ids.append(self.restart_btn_window)

    def _restart(self):
        """Full reset: position, velocity, score, power-up, layout."""
        if hasattr(self, "restart_btn") and self.restart_btn.winfo_exists():
            self.restart_btn.destroy()
        self._clear_ui()
        self.has_gold_core = False
        self._start_game()

    # ---------------------------------------------------------- particles
    def _burst(self, x, y, colour, n=7):
        for _ in range(n):
            self.particles.append(Particle(self.canvas, x, y, colour))

    def _bob(self, base_xy, phase):
        """Gentle up-down float for pickups."""
        bx, by = base_xy
        return (bx, by + math.sin(self.tick * 0.12 + phase) * 3)

    # ------------------------------------------------------- game loop
    def _loop(self):
        self.tick += 1

        # Twinkle stars (even on start screen)
        if self.tick % 12 == 0 and self.star_ids:
            sid, r, colour = random.choice(self.star_ids)
            try:
                self.canvas.itemconfigure(
                    sid, fill=colour if self.tick % 24 == 0 else "#334466",
                )
            except tk.TclError:
                pass

        # Float toast fade
        if self.float_msg_life > 0:
            self.float_msg_life -= 1
            if self.float_msg_life == 0 and self.float_msg_id:
                self.canvas.delete(self.float_msg_id)
                self.float_msg_id = None

        if self.state == "play" and self.player:
            was_grounded = self.player.on_ground
            self.player.apply_input(self.keys)
            self.player.physics(self.platforms)

            # Dash afterimage sparkles
            if self.player.dash_left > 0 and self.tick % 2 == 0:
                self._burst(
                    self.player.x + self.player.w / 2,
                    self.player.y + self.player.h / 2,
                    "#ff4fd8", n=2,
                )

            if self.player.on_ground and not was_grounded:
                fx, fy = self.player.feet_xy()
                self._burst(fx, fy, "#9aefe0", n=6)

            # Climb score
            height_score = max(0, int((WINDOW_H - self.player.y) // 10))
            if height_score > self.max_height_bonus:
                self.score += height_score - self.max_height_bonus
                self.max_height_bonus = height_score
                self._draw_hud()

            # Bobbing props
            if self.gold_id and self.gold_base:
                gx, gy = self._bob(self.gold_base, 0.0)
                self.canvas.coords(self.gold_id, gx, gy)
            if self.beacon_id and self.beacon_base:
                bx, by = self._bob(self.beacon_base, 1.2)
                self.canvas.coords(self.beacon_id, bx, by)
            for coin in self.coins:
                cx, cy = self._bob(coin["base"], 0.6)
                self.canvas.coords(coin["id"], cx, cy)

            # Gold Core pickup → double dash charges
            if self.gold_id and self.gold_base:
                gx, gy = self.canvas.coords(self.gold_id)
                gw, gh = S(20), S(20)
                if (
                    self.player.x < gx + gw
                    and self.player.x + self.player.w > gx
                    and self.player.y < gy + gh
                    and self.player.y + self.player.h > gy
                ):
                    self.canvas.delete(self.gold_id)
                    self.gold_id = None
                    self.has_gold_core = True
                    self.player.dash_charges_max = 2
                    self.player.dash_charges = 2
                    self.score += 30
                    self._burst(gx + 10, gy + 10, "#ffd76a", n=12)
                    self._toast("★ GOLD CORE — double dash!")
                    self._draw_hud()

            # Dock coin pickups
            kept = []
            cw = S(16)
            for coin in self.coins:
                cx, cy = self.canvas.coords(coin["id"])
                hit = (
                    self.player.x < cx + cw
                    and self.player.x + self.player.w > cx
                    and self.player.y < cy + cw
                    and self.player.y + self.player.h > cy
                )
                if hit:
                    self.canvas.delete(coin["id"])
                    self.score += 15
                    self.coins_collected += 1
                    self._burst(cx + 8, cy + 8, "#ffd76a", n=8)
                    self._draw_hud()
                else:
                    kept.append(coin)
            self.coins = kept

            # Win: stand on top dock near beacon
            top = self.top_platform
            if self.player.on_ground and top is not None:
                feet = self.player.y + self.player.h
                if (
                    abs(feet - top.y) < 3
                    and self.player.x + self.player.w > top.x + 4
                    and self.player.x < top.x + top.w - 4
                ):
                    self.score += 100 + self.coins_collected * 5
                    self._burst(
                        self.player.x + self.player.w / 2,
                        self.player.y, "#5dffd0", n=20,
                    )
                    self._show_game_over(won=True)

            # Fall below window → GAME OVER (only while still playing)
            if self.state == "play" and self.player.y > WINDOW_H + 5:
                self._show_game_over(won=False)

        alive = []
        for p in self.particles:
            if p.update():
                alive.append(p)
        self.particles = alive

        self.root.after(TICK_MS, self._loop)

    # ----------------------------------------------------------- cleanup
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

    def _clear_world(self, keep_player=False):
        for p in self.platforms:
            p.destroy(self.canvas)
        self.platforms.clear()
        self._plat_photos = []
        if self.gold_id:
            self.canvas.delete(self.gold_id)
            self.gold_id = None
        self.gold_base = None
        if self.beacon_id:
            self.canvas.delete(self.beacon_id)
            self.beacon_id = None
        self.beacon_base = None
        for coin in self.coins:
            try:
                self.canvas.delete(coin["id"])
            except tk.TclError:
                pass
        self.coins = []
        for p in self.particles:
            self.canvas.delete(p.id)
        self.particles.clear()
        if not keep_player and self.player:
            self.player.destroy()
            self.player = None
        self.top_platform = None


def main():
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()
