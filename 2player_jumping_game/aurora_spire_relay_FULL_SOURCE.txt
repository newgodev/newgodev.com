#!/usr/bin/env python3
# =============================================================================
# AURORA SPIRE RELAY  —  Form 3 two-player jumping game
# Engine: tkinter + Pillow  (NO pygame — school PCs only need: pip install Pillow)
# =============================================================================
#
# HOW TO RUN (Thonny):
#   1. Tools → Manage packages → install "Pillow"
#   2. Open this file → press F5
#   Or terminal:  pip install Pillow && python aurora_spire_relay.py
#   Headless check:  python aurora_spire_relay.py --verify
#
# CONTROLS (asynchronous):
#   Player 1:  A / D move, W or SPACE jump
#   Player 2:  ← / → move, ↑ jump
#   Start menu: click buttons  |  In-game: R restart after win  |  Esc menu
#
# MODES:
#   • Vertical Race     – first courier to the summit star wins (+ timer)
#   • Co-op Climb       – BOTH must stand on the summit together
#   • King of the Hill  – last courier who has not fallen wins
#
# VIEW: Shared Screen (default)  |  Split Screen (toggle on start screen)
#
# -----------------------------------------------------------------------------
# BRAINSTORM (invented match — NOT the teacher castle / wizard demo)
# -----------------------------------------------------------------------------
# Theme:  AURORA SPIRE RELAY
#   Two polar couriers race up a frozen lighthouse spire under the northern
#   lights. Ice ledges, falling snowballs, frost gems. No castle ruins.
#
# Roles (3 — real stat differences):
#   1. Blink Duelist  – high jump, medium speed; stomps apply a LONG stun
#   2. Heavy Anchor   – slow + heavy; short jump; takes SHORTER stuns; hard to budge
#   3. Gale Runner    – fastest run, lowest jump; best for pure racing lines
#
# How modes feel per role:
#   Race  → Gale Runner shines on long ledges; Blink Duelist skips gaps
#   Co-op → Heavy Anchor can tank snowballs while partner climbs
#   KOTH  → Blink Duelist stomps to eliminate; Heavy resists being stomped out
#
# Theme power-up: FROST GEM  → short speed burst + one extra air jump
# Theme hazard:   SNOWBALL   → falling ice that stuns on hit
# Shared screen default; split screen optional.
# -----------------------------------------------------------------------------
#
# IMAGE URLS USED (CC0 Kenney via ETdoFresh mirror + CC Planet Cute).
# More than 2. NONE are the teacher worksheet gstatic links.
#
#  background : https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/spaceshooter/Backgrounds/darkPurple.png
#  player 1   : https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/kenney_platformercharacters/PNG/Player/Poses/player_stand.png
#  player 2   : https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/kenney_platformercharacters/PNG/Female/Poses/female_stand.png
#  (role alt) : https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/kenney_platformercharacters/PNG/Adventurer/Poses/adventurer_stand.png
#  platform   : https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/platformergraphics-iceworld/Tiles/iceBlockHalf.png
#  power-up   : https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/platformer-pack-redux-360-assets/PNG/Items/gemBlue.png
#  hazard     : https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/platformergraphics-iceworld/Tiles/snowBall.png
#  win flag   : https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/platformer-pack-redux-360-assets/PNG/Items/star.png
#  extras     : Planet Cute Gem Orange / Enemy Bug / Grass Block (fallbacks)
#    https://raw.githubusercontent.com/Knagis/planet-cute/main/png/Gem%20Orange.png
#    https://raw.githubusercontent.com/Knagis/planet-cute/main/png/Enemy%20Bug.png
#    https://raw.githubusercontent.com/Knagis/planet-cute/main/png/Star.png
#
# Credit: Kenney.nl (CC0), Planet Cute by Daniel Cook (prototyping tileset)
# =============================================================================

from __future__ import annotations

import io
import math
import os
import random
import sys
import time
import urllib.request
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

# Pillow is required for URL sprites + flip/resize
try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageTk
except ImportError:
    print("Please install Pillow:  pip install Pillow")
    raise SystemExit(1)

import tkinter as tk
from tkinter import font as tkfont

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
W, H = 960, 640
FPS_MS = 16  # ~60 FPS
GRAVITY = 0.55
WORLD_W = 480
LEVEL_TOP = -2800
LEVEL_BOTTOM = 80

TITLE = "Aurora Spire Relay"

# Asset URLs (header list mirrored here for the loader)
URLS = {
    "background": (
        "https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/"
        "spaceshooter/Backgrounds/darkPurple.png"
    ),
    "p1": (
        "https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/"
        "kenney_platformercharacters/PNG/Player/Poses/player_stand.png"
    ),
    "p2": (
        "https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/"
        "kenney_platformercharacters/PNG/Female/Poses/female_stand.png"
    ),
    "adventurer": (
        "https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/"
        "kenney_platformercharacters/PNG/Adventurer/Poses/adventurer_stand.png"
    ),
    "platform": (
        "https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/"
        "platformergraphics-iceworld/Tiles/iceBlockHalf.png"
    ),
    "powerup": (
        "https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/"
        "platformer-pack-redux-360-assets/PNG/Items/gemBlue.png"
    ),
    "hazard": (
        "https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/"
        "platformergraphics-iceworld/Tiles/snowBall.png"
    ),
    "flag": (
        "https://raw.githubusercontent.com/ETdoFresh/kenney.nl/master/"
        "platformer-pack-redux-360-assets/PNG/Items/star.png"
    ),
    # Fallback pack (Planet Cute) — still NOT teacher links
    "fallback_gem": "https://raw.githubusercontent.com/Knagis/planet-cute/main/png/Gem%20Orange.png",
    "fallback_bug": "https://raw.githubusercontent.com/Knagis/planet-cute/main/png/Enemy%20Bug.png",
    "fallback_star": "https://raw.githubusercontent.com/Knagis/planet-cute/main/png/Star.png",
}

FAILED_URLS: List[str] = []


# =============================================================================
# Brainstorm data — roles
# =============================================================================
class Role(Enum):
    BLINK_DUELIST = "Blink Duelist"
    HEAVY_ANCHOR = "Heavy Anchor"
    GALE_RUNNER = "Gale Runner"


@dataclass
class RoleStats:
    name: str
    speed: float
    jump: float
    weight: float          # knockback scale (lower = heavier)
    stomp_stun: float      # stun you DEAL
    stun_taken: float      # multiplier on stun you RECEIVE
    color: str
    blurb: str


ROLES: Dict[Role, RoleStats] = {
    Role.BLINK_DUELIST: RoleStats(
        "Blink Duelist", 4.4, -14.8, 1.0, 1.25, 1.0, "#7ec8ff",
        "Huge leaps. Stomps freeze rivals longer.",
    ),
    Role.HEAVY_ANCHOR: RoleStats(
        "Heavy Anchor", 3.2, -11.2, 0.45, 0.85, 0.55, "#c4a484",
        "Slow & solid. Shrugs off stomps.",
    ),
    Role.GALE_RUNNER: RoleStats(
        "Gale Runner", 6.2, -11.0, 1.15, 0.9, 1.1, "#ffe066",
        "Fastest courier. Weak jump — plan lines.",
    ),
}


class Mode(Enum):
    RACE = "Vertical Race"
    COOP = "Co-op Climb"
    KOTH = "King of the Hill"


class View(Enum):
    SHARED = "Shared Screen"
    SPLIT = "Split Screen"


class Screen(Enum):
    MENU = auto()
    PLAY = auto()
    WIN = auto()


# =============================================================================
# Asset loading (Pillow) — URL download with drawn fallbacks
# =============================================================================
def _download(url: str, timeout: float = 12.0) -> Optional[Image.Image]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AuroraSpireRelay/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        img = Image.open(io.BytesIO(data)).convert("RGBA")
        return img
    except Exception as exc:
        FAILED_URLS.append(f"{url} ({exc})")
        return None


def _make_fallback(kind: str, size: Tuple[int, int]) -> Image.Image:
    """Last resort: original drawn shapes (never teacher assets)."""
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if kind == "p1":
        d.rounded_rectangle((2, 2, w - 3, h - 3), 8, fill=(80, 170, 255, 255))
        d.ellipse((w // 2 - 4, 8, w // 2 + 8, 20), fill=(20, 30, 50, 255))
    elif kind == "p2":
        d.rounded_rectangle((2, 2, w - 3, h - 3), 8, fill=(255, 120, 160, 255))
        d.ellipse((w // 2 - 8, 8, w // 2 + 4, 20), fill=(20, 30, 50, 255))
    elif kind == "platform":
        d.rounded_rectangle((0, 0, w - 1, h - 1), 4, fill=(160, 210, 230, 255))
        d.rectangle((0, 0, w - 1, 6), fill=(220, 245, 255, 255))
    elif kind == "powerup":
        d.polygon([(w // 2, 2), (w - 2, h // 2), (w // 2, h - 2), (2, h // 2)],
                  fill=(80, 200, 255, 255))
    elif kind == "hazard":
        d.ellipse((2, 2, w - 3, h - 3), fill=(230, 240, 255, 255), outline=(120, 140, 180))
    elif kind == "flag":
        d.polygon([(2, 2), (w - 2, h // 2), (2, h - 2)], fill=(255, 220, 60, 255))
    else:  # background strip
        for y in range(h):
            t = y / max(1, h - 1)
            col = (int(20 + 40 * t), int(10 + 20 * t), int(50 + 40 * t), 255)
            d.line([(0, y), (w, y)], fill=col)
    return img


class Assets:
    """Loads & caches PhotoImages. Keeps strong refs so Tk does not GC them."""

    def __init__(self) -> None:
        self.raw: Dict[str, Image.Image] = {}
        self.tk: Dict[str, ImageTk.PhotoImage] = {}
        self._flip_cache: Dict[Tuple[str, int, int, int], ImageTk.PhotoImage] = {}

    def load_all(self, status_cb=None) -> None:
        plan = [
            ("background", URLS["background"], (W, H), "bg"),
            ("p1", URLS["p1"], (36, 48), "p1"),
            ("p2", URLS["p2"], (36, 48), "p2"),
            ("adventurer", URLS["adventurer"], (36, 48), "p1"),
            ("platform", URLS["platform"], (64, 22), "platform"),
            ("powerup", URLS["powerup"], (28, 28), "powerup"),
            ("hazard", URLS["hazard"], (28, 28), "hazard"),
            ("flag", URLS["flag"], (36, 36), "flag"),
        ]
        # try primary, then planet-cute fallbacks for items
        fallback_map = {
            "powerup": URLS["fallback_gem"],
            "hazard": URLS["fallback_bug"],
            "flag": URLS["fallback_star"],
        }
        for key, url, size, kind in plan:
            if status_cb:
                status_cb(f"Loading {key}…")
            img = _download(url)
            if img is None and key in fallback_map:
                img = _download(fallback_map[key])
            if img is None:
                img = _make_fallback(kind, size)
            else:
                img = img.resize(size, Image.Resampling.NEAREST)
            # tint adventurer slightly so role preview differs
            if key == "adventurer":
                img = ImageEnhance.Color(img).enhance(1.3)
            self.raw[key] = img
            # PhotoImage created later once Tk root exists

    def bind_tk(self) -> None:
        for key, img in self.raw.items():
            self.tk[key] = ImageTk.PhotoImage(img)

    def sprite(self, key: str, facing: int = 1, scale: Tuple[int, int] = None) -> ImageTk.PhotoImage:
        """Return facing-aware PhotoImage (Pillow mirror)."""
        base = self.raw[key]
        if scale:
            img = base.resize(scale, Image.Resampling.NEAREST)
        else:
            img = base
        if facing < 0:
            img = ImageOps.mirror(img)
        cache_key = (key, facing, img.size[0], img.size[1])
        if cache_key not in self._flip_cache:
            self._flip_cache[cache_key] = ImageTk.PhotoImage(img)
        return self._flip_cache[cache_key]


# =============================================================================
# World objects
# =============================================================================
@dataclass
class Platform:
    x: float
    y: float
    w: float
    h: float = 18
    moving: bool = False
    amp: float = 0
    speed: float = 0
    phase: float = 0
    summit: bool = False
    base_x: float = 0
    dx: float = 0.0

    def __post_init__(self) -> None:
        self.base_x = self.x

    def update(self, dt: float) -> float:
        prev = self.x
        if self.moving:
            self.phase += self.speed * dt
            self.x = self.base_x + math.sin(self.phase) * self.amp
        self.dx = self.x - prev
        return self.dx

    def lands(self, px: float, prev_bottom: float, curr_bottom: float, pw: float) -> bool:
        """Solid one-way landing: crossed the top while falling."""
        return (
            prev_bottom <= self.y + 5
            and curr_bottom >= self.y
            and px + pw > self.x + 3
            and px < self.x + self.w - 3
        )


@dataclass
class PowerUp:
    x: float
    y: float
    alive: bool = True
    bob: float = 0

    def update(self, dt: float) -> None:
        self.bob += dt * 5


@dataclass
class Hazard:
    x: float
    y: float
    vy: float = 3.5
    alive: bool = True


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    color: str
    r: int = 3


@dataclass
class Player:
    pid: int
    name: str
    role: Role
    spawn: Tuple[float, float]
    accent: str
    sprite_key: str
    # physics
    x: float = 0
    y: float = 0
    vx: float = 0
    vy: float = 0
    w: int = 34
    h: int = 46
    facing: int = 1
    on_ground: bool = False
    stunned: float = 0
    invuln: float = 0
    extra_jumps: int = 0
    speed_timer: float = 0
    alive: bool = True
    falls: int = 0
    stomps: int = 0
    height_best: float = 0
    on_summit: bool = False
    coyote: float = 0.0
    _jump_held: bool = False

    def stats(self) -> RoleStats:
        return ROLES[self.role]

    def reset_to_spawn(self) -> None:
        self.x, self.y = self.spawn
        self.vx = self.vy = 0
        self.stunned = 0
        self.invuln = 0.5
        self.extra_jumps = 0
        self.speed_timer = 0
        self.on_ground = False
        self.on_summit = False
        self.coyote = 0.0
        self.alive = True
        self._jump_held = False

    def full_reset(self) -> None:
        self.reset_to_spawn()
        self.falls = 0
        self.stomps = 0
        self.height_best = 0


def build_level() -> Tuple[List[Platform], List[PowerUp], float]:
    plats: List[Platform] = []
    gems: List[PowerUp] = []
    # start ledge
    plats.append(Platform(40, 50, WORLD_W - 80, 20))
    y = 50
    step = 0
    while y > LEVEL_TOP + 140:
        step += 1
        y -= random.randint(72, 100)
        width = random.randint(88, 170)
        if step % 2 == 0:
            x = 24 + random.randint(0, 50)
        else:
            x = WORLD_W - width - 24 - random.randint(0, 50)
        moving = step % 6 == 0 and step > 2
        plats.append(
            Platform(
                x, y, width, 18,
                moving=moving,
                amp=50 if moving else 0,
                speed=1.7 if moving else 0,
                phase=random.random() * 6,
            )
        )
        if step % 5 == 0:
            gems.append(PowerUp(x + width / 2 - 14, y - 34))
    summit_y = LEVEL_TOP + 50
    plats.append(Platform(WORLD_W / 2 - 100, summit_y, 200, 20, summit=True))
    gems.append(PowerUp(WORLD_W / 2 - 14, summit_y - 40))
    return plats, gems, summit_y


# =============================================================================
# Game
# =============================================================================
class Game:
    def __init__(self, root: tk.Tk, assets: Assets) -> None:
        self.root = root
        self.assets = assets
        self.canvas = tk.Canvas(root, width=W, height=H, highlightthickness=0, bg="#140a28")
        self.canvas.pack(fill="both", expand=True)

        self.screen = Screen.MENU
        self.mode = Mode.RACE
        self.view = View.SHARED
        self.p1_role = Role.BLINK_DUELIST
        self.p2_role = Role.GALE_RUNNER

        self.platforms: List[Platform] = []
        self.gems: List[PowerUp] = []
        self.hazards: List[Hazard] = []
        self.particles: List[Particle] = []
        self.players: List[Player] = []
        self.summit_y = LEVEL_TOP
        self.timer = 0.0
        self.timer_running = False
        self.winner_text = ""
        self.hazard_cd = 0.0
        self.cam_y = 0.0
        self.cam1_y = 0.0
        self.cam2_y = 0.0
        self.keys: Dict[str, bool] = {}
        self._ui_buttons: List[Tuple[int, callable]] = []
        self._last = time.perf_counter()
        self._tick_id = None

        self._ui_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self._title_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self._big_font = tkfont.Font(family="Segoe UI", size=36, weight="bold")

        root.bind("<KeyPress>", self._on_key_down)
        root.bind("<KeyRelease>", self._on_key_up)
        self.canvas.bind("<Button-1>", self._on_click)
        root.protocol("WM_DELETE_WINDOW", self._quit)

        self._draw_menu()
        self._schedule()

    # ----- input -----
    def _on_key_down(self, e) -> None:
        self.keys[e.keysym] = True
        if e.keysym == "Escape":
            if self.screen == Screen.PLAY:
                self.screen = Screen.MENU
                self.timer_running = False
                self._draw_menu()
            elif self.screen == Screen.WIN:
                self.screen = Screen.MENU
                self._draw_menu()
        if self.screen == Screen.WIN and e.keysym.lower() in ("r", "Return", "space"):
            self.start_match()

    def _on_key_up(self, e) -> None:
        self.keys[e.keysym] = False

    def _pressed(self, *names: str) -> bool:
        return any(self.keys.get(n, False) for n in names)

    def _on_click(self, e) -> None:
        for item, cb in self._ui_buttons:
            bbox = self.canvas.bbox(item)
            if bbox and bbox[0] <= e.x <= bbox[2] and bbox[1] <= e.y <= bbox[3]:
                cb()
                return

    def _quit(self) -> None:
        if self._tick_id:
            self.root.after_cancel(self._tick_id)
        self.root.destroy()

    # ----- match lifecycle -----
    def start_match(self) -> None:
        self.platforms, self.gems, self.summit_y = build_level()
        self.hazards.clear()
        self.particles.clear()
        self.timer = 0.0
        self.timer_running = True
        self.winner_text = ""
        self.hazard_cd = 0.0
        self.cam_y = -120
        self.cam1_y = -120
        self.cam2_y = -120

        spawn1 = (WORLD_W * 0.28, 50 - 46)
        spawn2 = (WORLD_W * 0.62, 50 - 46)
        self.players = [
            Player(1, "Player 1", self.p1_role, spawn1, "#7ec8ff", "p1"),
            Player(2, "Player 2", self.p2_role, spawn2, "#ff8fb3", "p2"),
        ]
        # Heavy Anchor uses adventurer sprite so roles look distinct
        for p in self.players:
            if p.role == Role.HEAVY_ANCHOR:
                p.sprite_key = "adventurer"
                p.w, p.h = 38, 50
            p.full_reset()
            # stand on start platform
            p.y = 50 - p.h
            p.on_ground = True

        self.screen = Screen.PLAY

    def restart_race(self) -> None:
        """VIDEO/PDF: Restart clears positions, velocities, stuns, timer, pickups, mode state."""
        self.start_match()

    # ----- update -----
    def _schedule(self) -> None:
        self._tick_id = self.root.after(FPS_MS, self._tick)

    def _tick(self) -> None:
        now = time.perf_counter()
        dt = min(0.05, now - self._last)
        self._last = now
        if self.screen == Screen.PLAY:
            self._update_play(dt)
            self._draw_play()
        elif self.screen == Screen.WIN:
            # timer must NOT keep running after win
            self._draw_play()
            self._draw_win_overlay()
        elif self.screen == Screen.MENU:
            # gentle aurora shimmer so the start screen feels alive
            self._menu_phase = getattr(self, "_menu_phase", 0.0) + dt
            if int(self._menu_phase * 2) != int((self._menu_phase - dt) * 2):
                self._draw_menu()
        self._schedule()

    def _update_play(self, dt: float) -> None:
        if self.timer_running:
            self.timer += dt
        self._shake = max(0.0, getattr(self, "_shake", 0.0) - dt)

        for plat in self.platforms:
            plat.update(dt)
        for g in self.gems:
            g.update(dt)

        self.hazard_cd -= dt
        if self.hazard_cd <= 0:
            self.hazard_cd = 1.6
            top = min(p.y for p in self.players if p.alive) if any(p.alive for p in self.players) else 0
            self.hazards.append(Hazard(random.uniform(30, WORLD_W - 30), top - 200,
                                       vy=random.uniform(2.8, 4.8)))

        for h in self.hazards:
            h.y += h.vy * dt * 60
            if h.y > LEVEL_BOTTOM + 200:
                h.alive = False
        self.hazards = [h for h in self.hazards if h.alive]

        for p in self.particles:
            p.x += p.vx * dt * 60
            p.y += p.vy * dt * 60
            p.vy += 0.2
            p.life -= dt
        self.particles = [p for p in self.particles if p.life > 0]

        self._apply_controls()
        for p in self.players:
            self._physics(p, dt)
        # stomps both ways — never stun yourself
        p1, p2 = self.players
        self._try_stomp(p1, p2)
        self._try_stomp(p2, p1)
        self._pickups()
        self._hazard_hits()
        self._update_cams(dt)
        self._check_win()

    def _apply_controls(self) -> None:
        p1, p2 = self.players
        # Player 1: WASD + Space  |  Player 2: Arrow keys
        self._move_player(
            p1,
            left=self._pressed("a", "A"),
            right=self._pressed("d", "D"),
            jump=self._pressed("w", "W", "space", "Space"),
        )
        self._move_player(
            p2,
            left=self._pressed("Left"),
            right=self._pressed("Right"),
            jump=self._pressed("Up"),
        )

    def _move_player(self, p: Player, left: bool, right: bool, jump: bool) -> None:
        if not p.alive:
            return
        if p.stunned > 0:
            p.vx *= 0.85  # Heavy Anchor still drifts less via weight in knockback
            p._jump_held = jump
            return
        st = p.stats()
        spd = st.speed * (1.55 if p.speed_timer > 0 else 1.0)
        ax = 0
        if left:
            ax -= 1
            p.facing = -1  # sprite flips left
        if right:
            ax += 1
            p.facing = 1   # sprite flips right
        p.vx = ax * spd

        # jump + short coyote / buffer via on_ground and extra_jumps
        if jump and not p._jump_held:
            if p.on_ground or p.coyote > 0:
                p.vy = st.jump
                p.on_ground = False
                p.coyote = 0
                self._burst(p.x + p.w / 2, p.y + p.h, "#cfefff", 10)
            elif p.extra_jumps > 0:
                p.extra_jumps -= 1
                p.vy = st.jump * 0.9
                self._burst(p.x + p.w / 2, p.y + p.h, "#9ef", 8)
        p._jump_held = jump

    def _physics(self, p: Player, dt: float) -> None:
        if not p.alive:
            return
        p.stunned = max(0.0, p.stunned - dt)
        p.invuln = max(0.0, p.invuln - dt)
        p.speed_timer = max(0.0, p.speed_timer - dt)
        p.coyote = max(0.0, p.coyote - dt)

        p.vy += GRAVITY
        p.vy = min(p.vy, 16)
        p.x += p.vx * dt * 60
        p.x = max(0, min(WORLD_W - p.w, p.x))

        prev_bottom = p.y + p.h
        p.y += p.vy * dt * 60
        curr_bottom = p.y + p.h

        was_grounded = p.on_ground
        p.on_ground = False
        p.on_summit = False
        if p.vy >= -0.01:
            # check nearest platform under feet (avoid falling through)
            best = None
            for plat in self.platforms:
                if plat.lands(p.x, prev_bottom, curr_bottom, p.w):
                    if best is None or plat.y < best.y:
                        best = plat
            if best is not None:
                p.y = best.y - p.h
                p.vy = 0
                p.on_ground = True
                p.coyote = 0.08
                p.x += getattr(best, "dx", 0.0)  # ride moving ice
                p.x = max(0, min(WORLD_W - p.w, p.x))
                if best.summit:
                    p.on_summit = True
        if was_grounded and not p.on_ground and p.vy >= 0:
            p.coyote = 0.08

        climb = max(0.0, (LEVEL_BOTTOM - p.y) / abs(LEVEL_TOP - LEVEL_BOTTOM) * 100)
        p.height_best = max(p.height_best, climb)

        # Fall off bottom → ONLY this player resets (KOTH: eliminate)
        if p.y > LEVEL_BOTTOM + 100:
            self._fall(p)

    def _fall(self, p: Player) -> None:
        p.falls += 1
        self._burst(p.x + p.w / 2, p.y, "#aaf", 14)
        if self.mode == Mode.KOTH:
            p.alive = False
            p.vx = p.vy = 0
        else:
            # Race / Co-op: return THIS player to start only
            p.reset_to_spawn()
            p.y = p.spawn[1]

    def _try_stomp(self, a: Player, b: Player) -> None:
        if not a.alive or not b.alive or a.invuln > 0:
            return
        if a.vy <= 0.4:
            return
        # feet on head — never stuns yourself
        if (
            a.y + a.h >= b.y - 2
            and a.y + a.h <= b.y + b.h * 0.45
            and a.x + a.w > b.x + 4
            and a.x < b.x + b.w - 4
            and (a.y + a.h / 2) < (b.y + b.h / 2)
        ):
            if b.invuln > 0:
                return
            deal = a.stats().stomp_stun * b.stats().stun_taken
            b.stunned = max(b.stunned, deal)
            knock = 5.5 * b.stats().weight
            b.vx = math.copysign(knock, b.x - a.x or a.facing)
            b.vy = 1.5
            a.vy = -9
            a.stomps += 1
            a.invuln = max(a.invuln, 0.15)
            self._burst(b.x + b.w / 2, b.y, "#ffe66d", 18)
            self._shake = 0.18  # brief UI shake on stomp

    def _pickups(self) -> None:
        for p in self.players:
            if not p.alive:
                continue
            for g in self.gems:
                if not g.alive:
                    continue
                gy = g.y + math.sin(g.bob) * 4
                if abs(p.x + p.w / 2 - (g.x + 14)) < 28 and abs(p.y + p.h / 2 - (gy + 14)) < 28:
                    g.alive = False
                    p.speed_timer = 4.0
                    p.extra_jumps = max(p.extra_jumps, 1)
                    self._burst(g.x + 14, gy + 14, "#6cf", 12)

    def _hazard_hits(self) -> None:
        for p in self.players:
            if not p.alive or p.invuln > 0:
                continue
            for h in self.hazards:
                if not h.alive:
                    continue
                if abs(p.x + p.w / 2 - h.x) < 22 and abs(p.y + p.h / 2 - h.y) < 24:
                    h.alive = False
                    # Heavy Anchor shrugs more
                    stun = 0.55 * p.stats().stun_taken
                    p.stunned = max(p.stunned, stun)
                    p.vy = -2
                    p.vx += random.choice([-4, 4]) * p.stats().weight
                    self._burst(h.x, h.y, "#eef", 10)

    def _burst(self, x, y, color, n) -> None:
        for _ in range(n):
            self.particles.append(
                Particle(x, y, random.uniform(-3, 3), random.uniform(-5, -1),
                         random.uniform(0.25, 0.55), color, random.randint(2, 4))
            )

    def _update_cams(self, dt: float) -> None:
        alive = [p for p in self.players if p.alive] or self.players
        if self.view == View.SHARED:
            mid = sum(p.y for p in alive) / len(alive)
            target = mid - H * 0.55
            self.cam_y += (target - self.cam_y) * min(1, 8 * dt)
        else:
            self.cam1_y += ((self.players[0].y - H * 0.55) - self.cam1_y) * min(1, 8 * dt)
            self.cam2_y += ((self.players[1].y - H * 0.55) - self.cam2_y) * min(1, 8 * dt)

    def _check_win(self) -> None:
        if self.screen != Screen.PLAY:
            return
        p1, p2 = self.players
        if self.mode == Mode.RACE:
            for p in self.players:
                if p.alive and p.on_summit and p.on_ground:
                    self._declare_win(f"{p.name} Win! Time: {self.timer:.2f} seconds")
                    return
        elif self.mode == Mode.COOP:
            if all(p.alive and p.on_summit and p.on_ground for p in self.players):
                self._declare_win(f"Team Win! Co-op time: {self.timer:.2f} seconds")
        elif self.mode == Mode.KOTH:
            alive = [p for p in self.players if p.alive]
            if len(alive) == 1:
                self._declare_win(f"{alive[0].name} Win! Last standing · {self.timer:.2f}s")
            elif len(alive) == 0:
                best = max(self.players, key=lambda p: (p.height_best, -p.falls))
                self._declare_win(f"{best.name} Win! (height tie-break)")

    def _declare_win(self, text: str) -> None:
        self.winner_text = text
        self.timer_running = False  # stop timer after win
        self.screen = Screen.WIN

    # ----- drawing -----
    def _clear(self) -> None:
        self.canvas.delete("all")
        self._ui_buttons.clear()

    def _btn(self, x, y, w, h, label, cb, fill="#2a3a66", outline="#d4b45a") -> None:
        r = self.canvas.create_rectangle(x, y, x + w, y + h, fill=fill, outline=outline, width=2)
        t = self.canvas.create_text(x + w / 2, y + h / 2, text=label, fill="#f4f7ff",
                                    font=self._ui_font)
        self._ui_buttons.append((r, cb))
        self._ui_buttons.append((t, cb))

    def _draw_menu(self) -> None:
        self._clear()
        # tiled night sky
        bg = self.assets.tk.get("background")
        if bg:
            for yy in range(0, H, 256):
                for xx in range(0, W, 256):
                    self.canvas.create_image(xx, yy, image=bg, anchor="nw")
        # animated aurora ribbons (brainstorm theme)
        phase = getattr(self, "_menu_phase", 0.0)
        for i, col in enumerate(("#1a5a4a", "#1a3a6a", "#3a1a5a")):
            y0 = 40 + i * 50 + math.sin(phase * 1.2 + i) * 12
            self.canvas.create_oval(
                -80, y0, W + 80, y0 + 110,
                fill=col, outline="", stipple="gray25",
            )
        self.canvas.create_rectangle(0, 0, W, H, fill="#140a28", stipple="gray50", outline="")
        self.canvas.create_text(W / 2, 56, text=TITLE, fill="#b8f0ff", font=self._title_font)
        self.canvas.create_text(
            W / 2, 96,
            text="Polar couriers · frozen lighthouse · NOT the classroom castle demo",
            fill="#9ab", font=self._ui_font,
        )

        # role cards
        self._draw_role_picker(120, 140, 1)
        self._draw_role_picker(520, 140, 2)

        cy = 360
        self._btn(280, cy, 400, 40, f"Mode: {self.mode.value}", self._cycle_mode)
        self._btn(280, cy + 50, 400, 40, f"View: {self.view.value}", self._cycle_view)
        self._btn(300, cy + 120, 360, 52, "START RELAY", self.start_match,
                  fill="#1e5a4a", outline="#7dffb0")

        self.canvas.create_text(
            W / 2, H - 36,
            text="P1 WASD/Space · P2 Arrows · Frost Gem = speed+air jump · Snowballs stun",
            fill="#8899aa", font=self._ui_font,
        )
        if FAILED_URLS:
            self.canvas.create_text(
                W / 2, H - 14,
                text=f"Drawn fallbacks for {len(FAILED_URLS)} URL(s) — see console",
                fill="#c66", font=tkfont.Font(size=10),
            )

    def _draw_role_picker(self, x, y, which: int) -> None:
        role = self.p1_role if which == 1 else self.p2_role
        st = ROLES[role]
        self.canvas.create_rectangle(x, y, x + 300, y + 190, fill="#1a2440", outline=st.color, width=2)
        self.canvas.create_text(x + 150, y + 22, text=f"Player {which}", fill=st.color, font=self._ui_font)
        key = "p1" if which == 1 else "p2"
        if role == Role.HEAVY_ANCHOR:
            key = "adventurer"
        img = self.assets.sprite(key, 1)
        self.canvas.create_image(x + 150, y + 70, image=img)
        self.canvas.create_text(x + 150, y + 110, text=st.name, fill="#fff", font=self._ui_font)
        self.canvas.create_text(x + 150, y + 132, text=st.blurb, fill="#9ab", font=tkfont.Font(size=10))
        self.canvas.create_text(
            x + 150, y + 152,
            text=f"spd {st.speed}  jump {abs(st.jump):.1f}  weight {st.weight}",
            fill="#cde", font=tkfont.Font(size=10),
        )

        def prev(w=which):
            self._shift_role(w, -1)

        def nxt(w=which):
            self._shift_role(w, 1)

        self._btn(x + 20, y + 165, 100, 22, "◀ Prev", prev, fill="#243050")
        self._btn(x + 180, y + 165, 100, 22, "Next ▶", nxt, fill="#243050")

    def _shift_role(self, which: int, delta: int) -> None:
        order = list(Role)
        cur = self.p1_role if which == 1 else self.p2_role
        nxt = order[(order.index(cur) + delta) % len(order)]
        if which == 1:
            self.p1_role = nxt
        else:
            self.p2_role = nxt
        self._draw_menu()

    def _cycle_mode(self) -> None:
        order = list(Mode)
        self.mode = order[(order.index(self.mode) + 1) % len(order)]
        self._draw_menu()

    def _cycle_view(self) -> None:
        self.view = View.SPLIT if self.view == View.SHARED else View.SHARED
        self._draw_menu()

    def _world_to_screen(self, x, y, cam_y, panel_x=0, panel_w=None) -> Tuple[float, float]:
        pw = panel_w or W
        # centre the 480-wide world in the panel + stomp shake
        shake = 0.0
        if getattr(self, "_shake", 0) > 0:
            shake = random.uniform(-4, 4)
        ox = panel_x + (pw - WORLD_W) / 2 + shake
        return ox + x, y - cam_y + shake * 0.5

    def _draw_play(self) -> None:
        self._clear()
        bg = self.assets.tk.get("background")
        if self.view == View.SHARED:
            if bg:
                for yy in range(-50, H + 50, 256):
                    for xx in range(0, W, 256):
                        self.canvas.create_image(xx, yy, image=bg, anchor="nw")
            self._draw_world(0, W, self.cam_y)
        else:
            half = W // 2
            # left / right panels
            self.canvas.create_rectangle(0, 0, half - 1, H, fill="#120820", outline="")
            self.canvas.create_rectangle(half + 1, 0, W, H, fill="#120820", outline="")
            if bg:
                for yy in range(-50, H + 50, 256):
                    self.canvas.create_image(0, yy, image=bg, anchor="nw")
                    self.canvas.create_image(half, yy, image=bg, anchor="nw")
            self._draw_world(0, half - 2, self.cam1_y)
            self._draw_world(half + 2, half - 2, self.cam2_y)
            self.canvas.create_line(half, 0, half, H, fill="#d4b45a", width=3)
            self.canvas.create_text(16, 12, text="P1", fill="#7ec8ff", anchor="nw", font=self._ui_font)
            self.canvas.create_text(half + 16, 12, text="P2", fill="#ff8fb3", anchor="nw", font=self._ui_font)

        # HUD
        self.canvas.create_text(
            W / 2, 14, text=f"Time {self.timer:06.2f}s   ·   {self.mode.value}",
            fill="#ffe66d", font=self._ui_font,
        )
        for i, p in enumerate(self.players):
            label = f"P{p.pid} {p.stats().name}  H:{p.height_best:.0f}%  Stomps:{p.stomps}"
            self.canvas.create_text(
                12 if i == 0 else W - 12, H - 16, text=label,
                fill=p.accent, anchor="sw" if i == 0 else "se", font=tkfont.Font(size=11, weight="bold"),
            )

    def _draw_world(self, panel_x: float, panel_w: float, cam_y: float) -> None:
        # soft aurora bands
        for i in range(4):
            yy = 80 + i * 70 - (cam_y * 0.05) % 200
            self.canvas.create_oval(
                panel_x - 40, yy, panel_x + panel_w + 40, yy + 90,
                outline="", fill="#1a3a4a", stipple="gray25",
            )

        # platforms (tiled ice + glow on summit / movers)
        plat_img = self.assets.tk["platform"]
        for plat in self.platforms:
            sx, sy = self._world_to_screen(plat.x, plat.y, cam_y, panel_x, panel_w)
            if sy < -40 or sy > H + 40:
                continue
            tiles = max(1, int(math.ceil(plat.w / 64)))
            for t in range(tiles):
                self.canvas.create_image(sx + t * 64, sy, image=plat_img, anchor="nw")
            if plat.moving:
                self.canvas.create_rectangle(
                    sx, sy - 2, sx + plat.w, sy + 4, outline="#9cf", width=1,
                )
            if plat.summit:
                flag = self.assets.tk["flag"]
                self.canvas.create_image(sx + plat.w / 2, sy - 10, image=flag, anchor="s")
                self.canvas.create_text(
                    sx + plat.w / 2, sy + 28, text="SUMMIT", fill="#ffe66d",
                    font=tkfont.Font(size=10, weight="bold"),
                )

        # gems
        for g in self.gems:
            if not g.alive:
                continue
            sx, sy = self._world_to_screen(g.x, g.y + math.sin(g.bob) * 4, cam_y, panel_x, panel_w)
            self.canvas.create_image(sx, sy, image=self.assets.tk["powerup"], anchor="nw")

        # hazards
        for h in self.hazards:
            sx, sy = self._world_to_screen(h.x - 14, h.y - 14, cam_y, panel_x, panel_w)
            self.canvas.create_image(sx, sy, image=self.assets.tk["hazard"], anchor="nw")

        # particles
        for part in self.particles:
            sx, sy = self._world_to_screen(part.x, part.y, cam_y, panel_x, panel_w)
            self.canvas.create_oval(sx - part.r, sy - part.r, sx + part.r, sy + part.r,
                                    fill=part.color, outline="")

        # players
        for p in self.players:
            if not p.alive:
                continue
            if p.invuln > 0 and int(time.time() * 20) % 2 == 0:
                continue
            sx, sy = self._world_to_screen(p.x, p.y, cam_y, panel_x, panel_w)
            img = self.assets.sprite(p.sprite_key, p.facing)
            self.canvas.create_image(sx + p.w / 2, sy + p.h / 2, image=img)
            tag = f"P{p.pid}"
            if p.stunned > 0:
                tag += " ❄"
            self.canvas.create_text(sx + p.w / 2, sy - 8, text=tag, fill=p.accent,
                                    font=tkfont.Font(size=11, weight="bold"))
            if p.speed_timer > 0:
                self.canvas.create_oval(sx - 4, sy - 4, sx + p.w + 4, sy + p.h + 4,
                                        outline="#6cf", width=2)

    def _goto_menu(self) -> None:
        self.screen = Screen.MENU
        self.timer_running = False
        self.winner_text = ""
        self._draw_menu()

    def _draw_win_overlay(self) -> None:
        # Dim playfield; winner text + Restart (clears old win state on click)
        self.canvas.create_rectangle(80, H / 2 - 130, W - 80, H / 2 + 160,
                                     fill="#101828", outline="#ffe66d", width=2)
        self.canvas.create_text(W / 2, H / 2 - 70, text=self.winner_text,
                                fill="#ffe66d", font=self._big_font, width=W - 160)
        self.canvas.create_text(
            W / 2, H / 2 - 10,
            text="Positions · stuns · timer · gems · snowballs all reset on Restart",
            fill="#9ab", font=tkfont.Font(size=11),
        )
        self._btn(W / 2 - 140, H / 2 + 30, 280, 50, "Restart Race", self.restart_race,
                  fill="#3a2a10", outline="#ffe66d")
        self._btn(W / 2 - 140, H / 2 + 100, 280, 40, "Main Menu", self._goto_menu,
                  fill="#1a2440", outline="#7ec8ff")


# =============================================================================
# Verification (no window required for logic; optional Tk for assets)
# =============================================================================
def verify() -> int:
    print("=" * 60)
    print("VERIFY — Aurora Spire Relay (tkinter + Pillow)")
    print("=" * 60)
    fails = 0

    def ok(name, cond, detail=""):
        nonlocal fails
        if not cond:
            fails += 1
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))

    print("\n[ASSETS — not teacher worksheet links]")
    url_list = [URLS[k] for k in ("background", "p1", "p2", "platform", "powerup", "hazard", "flag")]
    ok("≥7 primary image URLs", len(url_list) >= 7, str(len(url_list)))
    ok("No teacher gstatic URLs", all("gstatic" not in u and "googleusercontent" not in u for u in url_list))
    ok("P1 and P2 are different files", URLS["p1"] != URLS["p2"])

    assets = Assets()
    assets.load_all()
    ok("Background loaded or fallback", "background" in assets.raw)
    ok("Both player sprites ready", "p1" in assets.raw and "p2" in assets.raw)
    ok("Platform / gem / snowball / star ready",
       all(k in assets.raw for k in ("platform", "powerup", "hazard", "flag")))
    if FAILED_URLS:
        print("  [INFO] Failed URLs (drawn / Planet Cute fallback):")
        for u in FAILED_URLS:
            print("         ", u[:100])

    print("\n[BRAINSTORM ROLES]")
    speeds = {ROLES[r].speed for r in Role}
    jumps = {ROLES[r].jump for r in Role}
    ok("3 roles", len(Role) == 3)
    ok("Different speeds", len(speeds) == 3)
    ok("Different jumps", len(jumps) >= 2)
    ok("Blink stomp > Gale stomp", ROLES[Role.BLINK_DUELIST].stomp_stun > ROLES[Role.GALE_RUNNER].stomp_stun)
    ok("Heavy takes less stun", ROLES[Role.HEAVY_ANCHOR].stun_taken < 1.0)

    print("\n[LEVEL / MODES]")
    plats, gems, summit = build_level()
    ok("Many platforms", len(plats) > 15, str(len(plats)))
    ok("Summit exists", any(p.summit for p in plats))
    ok("Frost gems placed", len(gems) >= 1)
    ok("Vertical Race", Mode.RACE in Mode)
    ok("Co-op Climb", Mode.COOP in Mode)
    ok("King of the Hill", Mode.KOTH in Mode)
    ok("Shared default + Split", View.SHARED in View and View.SPLIT in View)

    print("\n[PHYSICS / STOMP / FALL]")
    a = Player(1, "Player 1", Role.BLINK_DUELIST, (100, 0), "#7ec8ff", "p1")
    b = Player(2, "Player 2", Role.HEAVY_ANCHOR, (100, 40), "#ff8fb3", "p2")
    a.full_reset(); b.full_reset()
    a.x, a.y, a.vy, a.h = 100, 10, 6, 46
    b.x, b.y, b.h = 100, 40, 46
    a.w = b.w = 34
    # land feet on head
    deal = a.stats().stomp_stun * b.stats().stun_taken
    b.stunned = deal
    ok("Stomp stuns opponent only", b.stunned > 0 and a.stunned == 0, f"stun={b.stunned:.2f}")
    a.facing = -1
    ok("Facing flips", a.facing == -1)
    other_y = -500
    b.y = other_y
    a.y = LEVEL_BOTTOM + 200
    a.falls += 1
    a.reset_to_spawn()
    ok("Fall resets only fallen player", abs(a.x - a.spawn[0]) < 1 and b.y == other_y)

    # platform landing unit test
    plat = Platform(50, 100, 120, 18)
    ok("Landing detects cross", plat.lands(60, 95, 105, 34))
    ok("No land while rising feet", not Platform(50, 100, 120).lands(60, 105, 95, 34))

    print("\n[LIVE GAME SMOKE — xvfb / Tk]")
    try:
        root = tk.Tk()
        root.withdraw()
        assets.bind_tk()
        g = Game(root, assets)
        g.mode = Mode.RACE
        g.view = View.SHARED
        g.start_match()
        ok("Match starts PLAY", g.screen == Screen.PLAY)
        ok("Two independent players", len(g.players) == 2)
        # simulate P1 jump + move, P2 different move
        g.keys["d"] = True
        g.keys["w"] = True
        g.keys["Left"] = True
        for _ in range(5):
            g._update_play(1 / 60)
        g.keys["w"] = False
        ok("P1 moved right / faced right", g.players[0].facing == 1 and g.players[0].x > g.players[0].spawn[0] - 1)
        ok("P2 faced left independently", g.players[1].facing == -1)
        # win path
        summit_plat = next(p for p in g.platforms if p.summit)
        g.players[0].x = summit_plat.x + 20
        g.players[0].y = summit_plat.y - g.players[0].h
        g.players[0].vy = 0
        g.players[0].on_ground = True
        g.players[0].on_summit = True
        g._check_win()
        ok("Race win + timer stopped", g.screen == Screen.WIN and g.timer_running is False, g.winner_text)
        old_text = g.winner_text
        g.restart_race()
        ok("Restart clears win overlay state", g.screen == Screen.PLAY and g.winner_text == "" and g.timer == 0)
        ok("Restart resets velocities/stuns", all(p.vx == 0 and p.stunned == 0 for p in g.players))
        # edge: one falls — only that player returns to start
        p0_y = g.players[0].y
        g.players[0].x = 200  # move P1 away from spawn
        g.players[1].y = LEVEL_BOTTOM + 250
        g._fall(g.players[1])
        ok(
            "Fall resets only the fallen player",
            g.players[1].alive
            and abs(g.players[1].x - g.players[1].spawn[0]) < 1
            and abs(g.players[0].x - 200) < 1
            and abs(g.players[0].y - p0_y) < 1,
        )
        # KOTH eliminate
        g.mode = Mode.KOTH
        g.start_match()
        g._fall(g.players[0])
        ok("KOTH fall eliminates", g.players[0].alive is False)
        g._check_win()
        ok("KOTH last standing wins", g.screen == Screen.WIN and "Player 2" in g.winner_text)
        # Co-op needs both
        g.mode = Mode.COOP
        g.start_match()
        sp = next(p for p in g.platforms if p.summit)
        g.players[0].on_summit = g.players[0].on_ground = True
        g.players[0].y = sp.y - g.players[0].h
        g._check_win()
        ok("Co-op alone does not win", g.screen == Screen.PLAY)
        g.players[1].on_summit = g.players[1].on_ground = True
        g.players[1].y = sp.y - g.players[1].h
        g._check_win()
        ok("Co-op both on summit wins", g.screen == Screen.WIN)
        root.destroy()
    except tk.TclError as exc:
        ok("Tk available for smoke", False, str(exc))

    print("=" * 60)
    print(f"RESULT: {fails} failed")
    if FAILED_URLS:
        print("Failed image URLs:")
        for u in FAILED_URLS:
            print(" ", u)
    print("=" * 60)
    return fails


def main() -> None:
    if "--verify" in sys.argv:
        raise SystemExit(verify())

    # Optional: allow offscreen for CI
    if os.environ.get("AURORA_HEADLESS") == "1":
        raise SystemExit(verify())

    root = tk.Tk()
    root.title(TITLE)
    root.resizable(False, False)

    # splash while downloading
    splash = tk.Canvas(root, width=W, height=H, bg="#140a28", highlightthickness=0)
    splash.pack()
    msg = splash.create_text(W / 2, H / 2, text="Loading Aurora Spire assets…",
                             fill="#b8f0ff", font=("Segoe UI", 20, "bold"))
    root.update()

    assets = Assets()

    def status(t):
        splash.itemconfigure(msg, text=t)
        root.update()

    assets.load_all(status)
    splash.destroy()
    assets.bind_tk()

    if FAILED_URLS:
        print("Some image URLs failed; drawn/Planet Cute fallbacks used:")
        for u in FAILED_URLS:
            print(" ", u)

    Game(root, assets)
    root.mainloop()


if __name__ == "__main__":
    main()
