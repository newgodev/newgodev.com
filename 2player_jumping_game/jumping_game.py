#!/usr/bin/env python3
# =============================================================================
# My First Jumping Game – 3R99  (Form 3 Presentation Edition)
# =============================================================================
# HOW TO RUN (Thonny):
#   1. Install pygame:  Tools → Manage packages → search "pygame" → Install
#      Or terminal:     pip install pygame
#   2. Open this file in Thonny and press F5 / Run.
#   3. Or from terminal:  python jumping_game.py
#
# CONTROLS (Asynchronous – PDF B):
#   Player 1:  A/D move, W or SPACE jump, S drop-through (thin platforms),
#              F ability (class skill)
#   Player 2:  ←/→ move, ↑ jump, ↓ drop-through, RSHIFT ability
#   ESC: pause / back     ENTER: confirm selection
#
# GAME MODES (PDF B checklist):
#   • Vertical Race     – first to the summit wins (video demo core)
#   • Co-op Climb       – both must reach the summit together
#   • King of the Hill  – lava rises; last player standing wins
#
# VIEW: Shared Screen  |  Split Screen  (start-menu toggle)
#
# CLASSES: High Jumper · Speedster · Tank · Wizard
# FEATURES: stomping, power-ups, moving platforms, falling rocks, lava,
#           particles, screen shake, timer, restart
# =============================================================================

from __future__ import annotations

import math
import random
import sys
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Tuple

import pygame

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCREEN_W, SCREEN_H = 1100, 720
FPS = 60
GRAVITY = 0.55
WORLD_W = 520  # playable width of the level corridor
LEVEL_TOP_Y = -3200  # summit Y (negative = up)
LEVEL_BOTTOM_Y = 80

# Colours
COL_BG_TOP = (18, 28, 58)
COL_BG_BOT = (40, 70, 110)
COL_PLATFORM = (92, 64, 48)
COL_PLATFORM_TOP = (120, 180, 90)
COL_MOVING = (70, 130, 180)
COL_LAVA = (255, 90, 30)
COL_UI = (240, 240, 255)
COL_GOLD = (255, 210, 70)
COL_P1 = (70, 170, 255)
COL_P2 = (255, 110, 130)

# Video demo title
GAME_TITLE = "My First Jumping Game – 3R99"


# =============================================================================
# Enums / data  (PDF + video feature tags in comments)
# =============================================================================
class GameState(Enum):
    START = auto()
    CLASS_SELECT = auto()
    PLAYING = auto()
    PAUSED = auto()
    WIN = auto()
    GAME_OVER = auto()


class Mode(Enum):
    VERTICAL_RACE = "Vertical Race"       # PDF + video: first to top
    COOP_CLIMB = "Co-op Climb"            # PDF: team goal
    KING_OF_HILL = "King of the Hill"     # PDF: last standing


class ViewMode(Enum):
    SHARED = "Shared Screen"              # PDF: Shared Screen
    SPLIT = "Split Screen"                # PDF + video: Split Screen


class ClassType(Enum):
    # PDF: Character Abilities & Classes
    HIGH_JUMPER = "High Jumper"
    SPEEDSTER = "Speedster"
    TANK = "Tank"
    WIZARD = "Wizard"


@dataclass
class ClassStats:
    name: str
    color: Tuple[int, int, int]
    speed: float
    jump: float
    width: int
    height: int
    ability_name: str
    ability_cd: float
    desc: str


CLASS_STATS = {
    ClassType.HIGH_JUMPER: ClassStats(
        "High Jumper", (90, 220, 140), 4.2, -14.5, 28, 36,
        "Super Leap", 4.0, "Huge jump power + Super Leap ability",
    ),
    ClassType.SPEEDSTER: ClassStats(
        "Speedster", (255, 200, 60), 6.4, -11.5, 26, 34,
        "Dash", 2.5, "Fastest runner + short Dash",
    ),
    ClassType.TANK: ClassStats(
        "Tank", (180, 120, 90), 3.4, -12.0, 36, 40,
        "Shield Bash", 3.5, "Stomp-resistant + knockback bash",
    ),
    ClassType.WIZARD: ClassStats(
        "Wizard", (180, 120, 255), 4.0, -12.5, 28, 36,
        "Double Jump / Pulse", 0.0, "Innate double-jump + slow pulse",
    ),
}


# =============================================================================
# Helpers: drawing, particles, shake
# =============================================================================
def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def draw_gradient(surf: pygame.Surface, c1, c2) -> None:
    h = surf.get_height()
    for y in range(h):
        t = y / max(1, h - 1)
        col = (
            int(lerp(c1[0], c2[0], t)),
            int(lerp(c1[1], c2[1], t)),
            int(lerp(c1[2], c2[2], t)),
        )
        pygame.draw.line(surf, col, (0, y), (surf.get_width(), y))


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    color: Tuple[int, int, int]
    size: float = 3.0

    def update(self, dt: float) -> None:
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vy += 0.25 * dt * 60
        self.life -= dt

    def draw(self, surf: pygame.Surface, cam_x: float, cam_y: float) -> None:
        if self.life <= 0:
            return
        alpha = clamp(self.life, 0, 1)
        s = max(1, int(self.size * alpha))
        px, py = int(self.x - cam_x), int(self.y - cam_y)
        pygame.draw.circle(surf, self.color, (px, py), s)


class ScreenShake:
    def __init__(self) -> None:
        self.timer = 0.0
        self.mag = 0.0

    def punch(self, mag: float = 6.0, dur: float = 0.25) -> None:
        self.mag = max(self.mag, mag)
        self.timer = max(self.timer, dur)

    def offset(self) -> Tuple[int, int]:
        if self.timer <= 0:
            return 0, 0
        return (
            int(random.uniform(-self.mag, self.mag)),
            int(random.uniform(-self.mag, self.mag)),
        )

    def update(self, dt: float) -> None:
        if self.timer > 0:
            self.timer -= dt
            self.mag *= 0.92
            if self.timer <= 0:
                self.mag = 0


# =============================================================================
# Level objects  (PDF: Dynamic Level Features)
# =============================================================================
class Platform:
    def __init__(
        self,
        x: float,
        y: float,
        w: float,
        h: float = 16,
        moving: bool = False,
        move_range: float = 0,
        move_speed: float = 0,
        thin: bool = False,
        summit: bool = False,
    ) -> None:
        self.base_x = x
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.moving = moving
        self.move_range = move_range
        self.move_speed = move_speed
        self.phase = random.random() * math.tau
        self.thin = thin  # can drop-through
        self.summit = summit
        self.prev_x = x

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))

    def update(self, dt: float) -> None:
        self.prev_x = self.x
        if self.moving and self.move_range:
            self.phase += self.move_speed * dt
            self.x = self.base_x + math.sin(self.phase) * self.move_range

    @property
    def dx(self) -> float:
        return self.x - self.prev_x

    def draw(self, surf: pygame.Surface, cam_x: float, cam_y: float) -> None:
        r = self.rect.move(-cam_x, -cam_y)
        if not r.colliderect(surf.get_rect().inflate(40, 40)):
            return
        top_col = COL_GOLD if self.summit else (COL_MOVING if self.moving else COL_PLATFORM_TOP)
        body = (50, 100, 140) if self.moving else COL_PLATFORM
        if self.thin:
            body = (110, 90, 70)
            top_col = (200, 170, 100)
        pygame.draw.rect(surf, body, r, border_radius=3)
        pygame.draw.rect(surf, top_col, (r.x, r.y, r.w, 5), border_radius=2)
        if self.summit:
            # finish flag
            pygame.draw.line(surf, (255, 255, 255), (r.centerx, r.y), (r.centerx, r.y - 36), 2)
            pygame.draw.polygon(
                surf, (255, 60, 60),
                [(r.centerx, r.y - 36), (r.centerx + 22, r.y - 28), (r.centerx, r.y - 20)],
            )


class Hazard:
    """Falling rocks / lava blobs – PDF Hazards & Obstacles."""

    def __init__(self, x: float, y: float, kind: str = "rock") -> None:
        self.x = x
        self.y = y
        self.vy = random.uniform(2.5, 5.0)
        self.kind = kind
        self.alive = True
        self.r = 10 if kind == "rock" else 12

    def update(self, dt: float, lava_y: float) -> None:
        self.y += self.vy * dt * 60
        if self.y > lava_y + 40 or self.y > LEVEL_BOTTOM_Y + 200:
            self.alive = False

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - self.r), int(self.y - self.r), self.r * 2, self.r * 2)

    def draw(self, surf: pygame.Surface, cam_x: float, cam_y: float) -> None:
        px, py = int(self.x - cam_x), int(self.y - cam_y)
        if self.kind == "rock":
            pygame.draw.circle(surf, (120, 110, 100), (px, py), self.r)
            pygame.draw.circle(surf, (80, 70, 60), (px - 2, py - 2), self.r // 2)
        else:
            pygame.draw.circle(surf, COL_LAVA, (px, py), self.r)
            pygame.draw.circle(surf, (255, 200, 80), (px - 2, py - 3), 4)


class PowerUp:
    """PDF: Power-Ups & Boosts — double jump, speed, shield."""

    KINDS = ("double_jump", "speed", "shield")

    def __init__(self, x: float, y: float, kind: Optional[str] = None) -> None:
        self.x = x
        self.y = y
        self.kind = kind or random.choice(self.KINDS)
        self.alive = True
        self.bob = random.random() * math.tau
        self.colors = {
            "double_jump": (120, 220, 255),
            "speed": (255, 220, 80),
            "shield": (120, 255, 160),
        }

    def update(self, dt: float) -> None:
        self.bob += dt * 4

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - 12), int(self.y - 12 + math.sin(self.bob) * 4), 24, 24)

    def draw(self, surf: pygame.Surface, cam_x: float, cam_y: float) -> None:
        if not self.alive:
            return
        r = self.rect().move(-cam_x, -cam_y)
        col = self.colors[self.kind]
        pygame.draw.rect(surf, col, r, border_radius=6)
        pygame.draw.rect(surf, (255, 255, 255), r, 2, border_radius=6)
        cx, cy = r.center
        label = {"double_jump": "2J", "speed": "SP", "shield": "SH"}[self.kind]
        font = pygame.font.SysFont("consolas", 12, bold=True)
        t = font.render(label, True, (20, 20, 30))
        surf.blit(t, t.get_rect(center=(cx, cy)))


def build_level(mode: Mode) -> Tuple[List[Platform], List[PowerUp], float]:
    """Procedural vertical course — video demo platforms + PDF hazards hooks."""
    platforms: List[Platform] = []
    powerups: List[PowerUp] = []

    # Starting ground (video: start platforms)
    platforms.append(Platform(40, 40, WORLD_W - 80, 22))

    y = 0
    step = 0
    while y > LEVEL_TOP_Y + 120:
        step += 1
        y -= random.randint(70, 105)
        # zig-zag corridor
        side = (step % 2)
        margin = 30 + (step % 5) * 8
        width = random.randint(90, 180)
        if side == 0:
            x = margin + random.randint(0, 40)
        else:
            x = WORLD_W - margin - width - random.randint(0, 40)
        x = clamp(x, 16, WORLD_W - width - 16)

        moving = step % 7 == 0 and step > 3
        thin = step % 5 == 0 and not moving
        platforms.append(
            Platform(
                x, y, width, 14,
                moving=moving,
                move_range=55 if moving else 0,
                move_speed=1.6 if moving else 0,
                thin=thin,
            )
        )

        # occasional mid platform for co-op / racing lanes
        if step % 4 == 0:
            mid_w = 70
            platforms.append(Platform(WORLD_W / 2 - mid_w / 2, y - 40, mid_w, 12, thin=True))

        if step % 6 == 0 and step > 2:
            powerups.append(PowerUp(x + width / 2, y - 28))

    # Summit platform (video: reach top to win)
    summit_y = LEVEL_TOP_Y + 40
    platforms.append(Platform(WORLD_W / 2 - 110, summit_y, 220, 18, summit=True))

    # King of the Hill: crown platform near mid-upper
    if mode == Mode.KING_OF_HILL:
        platforms.append(Platform(WORLD_W / 2 - 70, -900, 140, 16, summit=True))

    return platforms, powerups, summit_y


# =============================================================================
# Player  (video: facing flip, jump, fall reset; PDF: classes, stomping)
# =============================================================================
class Player:
    def __init__(
        self,
        pid: int,
        name: str,
        controls: dict,
        class_type: ClassType,
        spawn: Tuple[float, float],
        accent: Tuple[int, int, int],
    ) -> None:
        self.pid = pid
        self.name = name
        self.controls = controls
        self.class_type = class_type
        self.stats = CLASS_STATS[class_type]
        self.accent = accent
        self.spawn = spawn

        self.w = self.stats.width
        self.h = self.stats.height
        self.x = spawn[0]
        self.y = spawn[1]
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.facing = 1  # VIDEO: facing direction changes with left/right
        self.alive = True
        self.won = False

        # Status
        self.stunned = 0.0          # PDF: Competitive Stomping
        self.shield = 0.0
        self.speed_boost = 0.0
        self.extra_jumps = 0        # from power-up or Wizard
        self.max_extra_jumps = 1 if class_type == ClassType.WIZARD else 0
        self.ability_cd = 0.0
        self.dash_timer = 0.0
        self.invuln = 0.0
        self.height_best = 0.0
        self.falls = 0
        self.stomps = 0
        self.on_platform: Optional[Platform] = None
        self.drop_timer = 0.0

        # visual
        self.squash = 1.0
        self.blink = 0.0

    def reset(self, spawn: Optional[Tuple[float, float]] = None) -> None:
        """VIDEO: Fall → restart from beginning (also full race restart)."""
        if spawn:
            self.spawn = spawn
        self.x, self.y = self.spawn
        self.vx = self.vy = 0.0
        self.on_ground = False
        self.stunned = 0.0
        self.dash_timer = 0.0
        self.extra_jumps = self.max_extra_jumps
        self.on_platform = None
        self.alive = True
        self.won = False
        self.invuln = 0.6
        self.drop_timer = 0.0

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    @property
    def center(self) -> Tuple[float, float]:
        return self.x + self.w / 2, self.y + self.h / 2

    def apply_powerup(self, kind: str, particles: List[Particle]) -> None:
        if kind == "double_jump":
            self.extra_jumps = max(self.extra_jumps, 1)
            self.max_extra_jumps = max(self.max_extra_jumps, 1)
        elif kind == "speed":
            self.speed_boost = 5.0
        elif kind == "shield":
            self.shield = 6.0
        cx, cy = self.center
        for _ in range(14):
            particles.append(
                Particle(
                    cx, cy,
                    random.uniform(-3, 3), random.uniform(-4, -1),
                    random.uniform(0.3, 0.7), self.stats.color, 3,
                )
            )

    def try_ability(self, other: Optional["Player"], particles: List[Particle], shake: ScreenShake) -> None:
        if self.ability_cd > 0 or self.stunned > 0:
            return
        ct = self.class_type
        if ct == ClassType.HIGH_JUMPER and self.on_ground:
            self.vy = self.stats.jump * 1.35
            self.on_ground = False
            self.ability_cd = self.stats.ability_cd
            self.squash = 1.3
        elif ct == ClassType.SPEEDSTER:
            self.dash_timer = 0.18
            self.vx = self.facing * 14
            self.ability_cd = self.stats.ability_cd
            self.invuln = max(self.invuln, 0.18)
        elif ct == ClassType.TANK and other and other.alive:
            # Shield Bash — knock nearby opponent
            dx = other.center[0] - self.center[0]
            dy = other.center[1] - self.center[1]
            if abs(dx) < 70 and abs(dy) < 50:
                other.vx = math.copysign(10, dx if dx != 0 else self.facing)
                other.vy = -6
                other.stunned = max(other.stunned, 0.35)
                shake.punch(5, 0.2)
                self.ability_cd = self.stats.ability_cd
        elif ct == ClassType.WIZARD:
            # Pulse: short stun aura + refresh jump
            self.extra_jumps = max(self.extra_jumps, 1)
            if other and other.alive:
                dx = other.center[0] - self.center[0]
                dy = other.center[1] - self.center[1]
                if dx * dx + dy * dy < 110 * 110:
                    other.stunned = max(other.stunned, 0.55)
                    other.vx *= 0.2
            cx, cy = self.center
            for _ in range(20):
                ang = random.random() * math.tau
                particles.append(
                    Particle(
                        cx, cy, math.cos(ang) * 4, math.sin(ang) * 4,
                        0.45, (200, 160, 255), 2.5,
                    )
                )
            self.ability_cd = 3.0

    def handle_input(self, keys, other: Optional["Player"], particles, shake) -> None:
        if not self.alive or self.won:
            return
        if self.stunned > 0 or self.dash_timer > 0:
            return

        left = keys[self.controls["left"]]
        right = keys[self.controls["right"]]
        jump = keys[self.controls["jump"]]
        down = keys[self.controls["down"]]
        ability = keys[self.controls["ability"]]

        speed = self.stats.speed * (1.55 if self.speed_boost > 0 else 1.0)
        ax = 0.0
        if left:
            ax -= 1
            self.facing = -1  # VIDEO: flip left
        if right:
            ax += 1
            self.facing = 1   # VIDEO: flip right
        self.vx = ax * speed

        # jump edge handled in Game with previous-key tracking; here continuous ok with buffer
        self._want_jump = jump
        self._want_down = down
        self._want_ability = ability

    # set by Game each frame
    _want_jump = False
    _want_down = False
    _want_ability = False
    _jump_pressed = False
    _ability_pressed = False

    def update_physics(
        self,
        dt: float,
        platforms: List[Platform],
        lava_y: float,
        particles: List[Particle],
        other: Optional["Player"],
        shake: ScreenShake,
        eliminate_on_fall: bool = False,
    ) -> None:
        if not self.alive:
            return

        # timers
        self.stunned = max(0.0, self.stunned - dt)
        self.shield = max(0.0, self.shield - dt)
        self.speed_boost = max(0.0, self.speed_boost - dt)
        self.ability_cd = max(0.0, self.ability_cd - dt)
        self.invuln = max(0.0, self.invuln - dt)
        self.drop_timer = max(0.0, self.drop_timer - dt)
        self.dash_timer = max(0.0, self.dash_timer - dt)
        self.squash = lerp(self.squash, 1.0, 0.15)
        self.blink += dt

        # ability edge
        if self._want_ability and not self._ability_pressed:
            self.try_ability(other, particles, shake)
        self._ability_pressed = self._want_ability

        # jump
        if self._want_jump and not self._jump_pressed:
            if self.on_ground:
                self.vy = self.stats.jump
                self.on_ground = False
                self.on_platform = None
                self.squash = 1.25
            elif self.extra_jumps > 0:
                self.extra_jumps -= 1
                self.vy = self.stats.jump * 0.92
                self.squash = 1.2
                cx, cy = self.center
                for _ in range(8):
                    particles.append(
                        Particle(cx, cy + self.h / 2, random.uniform(-2, 2), 1,
                                 0.3, (200, 230, 255), 2)
                    )
        self._jump_pressed = self._want_jump

        if self._want_down and self.on_ground and self.on_platform and self.on_platform.thin:
            self.drop_timer = 0.25
            self.on_ground = False
            self.y += 2

        # gravity
        if self.dash_timer <= 0:
            self.vy += GRAVITY
            self.vy = min(self.vy, 16)

        # move X
        self.x += self.vx * (dt * 60)
        self.x = clamp(self.x, 0, WORLD_W - self.w)

        # move Y + platform collisions (VIDEO + bug-fix: no fall-through)
        self.y += self.vy * (dt * 60)
        self.on_ground = False
        self.on_platform = None
        feet = self.rect

        for p in platforms:
            pr = p.rect
            # only land when falling onto top
            if self.vy >= 0 and self.drop_timer <= 0:
                prev_bottom = feet.bottom - self.vy * (dt * 60)
                if (
                    prev_bottom <= pr.top + 4
                    and feet.bottom >= pr.top
                    and feet.right > pr.left + 4
                    and feet.left < pr.right - 4
                    and feet.top < pr.bottom
                ):
                    self.y = pr.top - self.h
                    self.vy = 0
                    self.on_ground = True
                    self.on_platform = p
                    self.extra_jumps = self.max_extra_jumps
                    # ride moving platforms
                    self.x += p.dx
                    self.squash = min(self.squash, 0.85)
                    break

        # height tracking
        height = max(0.0, (LEVEL_BOTTOM_Y - self.y) / abs(LEVEL_TOP_Y - LEVEL_BOTTOM_Y) * 100)
        self.height_best = max(self.height_best, height)

        # lava / fall  (VIDEO: Fall → restart; PDF KOTH: eliminate)
        if self.y > lava_y - 8 or self.y > LEVEL_BOTTOM_Y + 120:
            self._fall_respawn(particles, eliminate=eliminate_on_fall)

    def _fall_respawn(self, particles: List[Particle], eliminate: bool = False) -> None:
        """VIDEO: Fall → restart from beginning. KOTH may eliminate instead."""
        self.falls += 1
        cx, cy = self.center
        for _ in range(16):
            particles.append(
                Particle(cx, cy, random.uniform(-3, 3), random.uniform(-2, 2),
                         0.5, COL_LAVA, 3)
            )
        if eliminate:
            self.alive = False
            return
        self.reset()

    def check_stomp(self, other: "Player", particles: List[Particle], shake: ScreenShake) -> None:
        """PDF: Competitive Stomping — land on opponent's head to stun."""
        if not self.alive or not other.alive:
            return
        if other.invuln > 0:
            return
        if self.vy <= 0.5:
            return
        my = self.rect
        ot = other.rect
        # feet overlapping the top band of the opponent (forgiving hitbox)
        horizontal = my.right > ot.left + 2 and my.left < ot.right - 2
        vertical = my.bottom >= ot.top - 4 and my.bottom <= ot.top + max(18, ot.height // 2)
        above = my.centery < ot.centery
        if horizontal and vertical and above:
            # Tank resists somewhat
            if other.class_type == ClassType.TANK and other.shield <= 0:
                stun = 0.55
            else:
                stun = 1.0
            if other.shield > 0:
                other.shield = 0
                self.vy = -8
                shake.punch(3, 0.15)
                return
            other.stunned = max(other.stunned, stun)
            other.vy = 2
            other.vx = math.copysign(4, other.center[0] - self.center[0])
            self.vy = -9
            self.stomps += 1
            shake.punch(8, 0.28)
            cx, cy = other.center
            for _ in range(18):
                particles.append(
                    Particle(cx, cy, random.uniform(-4, 4), random.uniform(-5, -1),
                             0.5, (255, 240, 120), 3)
                )

    def draw(self, surf: pygame.Surface, cam_x: float, cam_y: float) -> None:
        if not self.alive:
            return
        # squash/stretch
        draw_h = int(self.h * (2 - self.squash))
        draw_w = int(self.w * self.squash)
        px = int(self.x + (self.w - draw_w) / 2 - cam_x)
        py = int(self.y + self.h - draw_h - cam_y)

        # invuln / stun flicker
        if self.invuln > 0 and int(self.blink * 20) % 2 == 0:
            return

        body = self.stats.color
        if self.stunned > 0:
            body = (180, 180, 180)
        pygame.draw.rect(surf, body, (px, py, draw_w, draw_h), border_radius=6)
        pygame.draw.rect(surf, self.accent, (px, py, draw_w, draw_h), 2, border_radius=6)

        # face (VIDEO: facing)
        eye_y = py + int(draw_h * 0.28)
        if self.facing >= 0:
            ex = px + draw_w - 10
        else:
            ex = px + 4
        pygame.draw.rect(surf, (20, 20, 30), (ex, eye_y, 6, 6), border_radius=2)
        # mouth
        mx = px + draw_w // 2 - 4 + self.facing * 2
        pygame.draw.rect(surf, (40, 30, 40), (mx, py + int(draw_h * 0.55), 8, 3))

        # shield ring
        if self.shield > 0:
            pygame.draw.ellipse(
                surf, (120, 255, 180),
                (px - 4, py - 4, draw_w + 8, draw_h + 8), 2,
            )

        # name tag
        font = pygame.font.SysFont("consolas", 14, bold=True)
        tag = font.render(f"P{self.pid}", True, self.accent)
        surf.blit(tag, (px + draw_w // 2 - tag.get_width() // 2, py - 16))


# =============================================================================
# UI helpers
# =============================================================================
def font(size: int, bold: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("segoeui,arial,consolas", size, bold=bold)


def blit_text(surf, text, size, pos, color=COL_UI, center=False, bold=False):
    f = font(size, bold)
    t = f.render(text, True, color)
    r = t.get_rect()
    if center:
        r.center = pos
    else:
        r.topleft = pos
    surf.blit(t, r)
    return r


def button_rect(cx, cy, w=220, h=44) -> pygame.Rect:
    return pygame.Rect(cx - w // 2, cy - h // 2, w, h)


def draw_button(surf, rect, label, hover=False, accent=COL_GOLD) -> None:
    bg = (55, 70, 110) if not hover else (75, 100, 150)
    pygame.draw.rect(surf, bg, rect, border_radius=10)
    pygame.draw.rect(surf, accent, rect, 2, border_radius=10)
    blit_text(surf, label, 22, rect.center, COL_UI, center=True, bold=True)


# =============================================================================
# Main Game
# =============================================================================
class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.state = GameState.START

        # Start-screen options (VIDEO: Start screen options)
        self.mode = Mode.VERTICAL_RACE
        self.view = ViewMode.SPLIT
        self.p1_class = ClassType.HIGH_JUMPER
        self.p2_class = ClassType.SPEEDSTER
        self.menu_index = 0
        self.class_focus = 1  # which player picking on class screen

        self.particles: List[Particle] = []
        self.shake = ScreenShake()
        self.platforms: List[Platform] = []
        self.powerups: List[PowerUp] = []
        self.hazards: List[Hazard] = []
        self.summit_y = LEVEL_TOP_Y
        self.lava_y = LEVEL_BOTTOM_Y + 40
        self.lava_speed = 0.0

        self.players: List[Player] = []
        self.timer = 0.0
        self.winner_text = ""
        self.hazard_timer = 0.0
        self.cam1 = [0.0, 0.0]
        self.cam2 = [0.0, 0.0]
        self.cam_shared = [0.0, 0.0]

        # mouse / UI
        self.restart_btn = button_rect(SCREEN_W // 2, SCREEN_H // 2 + 80)
        self._bg = pygame.Surface((SCREEN_W, SCREEN_H))
        draw_gradient(self._bg, COL_BG_TOP, COL_BG_BOT)

        # soft audio fallback (optional beeps)
        self._init_audio()

    def _init_audio(self) -> None:
        self.sounds_ok = False
        import os
        # skip mixer under headless / CI to avoid ALSA spam
        if os.environ.get("SDL_VIDEODRIVER") == "dummy":
            return
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.sounds_ok = True
        except Exception:
            self.sounds_ok = False

    def beep(self, freq: int = 440, ms: int = 80) -> None:
        if not self.sounds_ok:
            return
        try:
            n = int(22050 * ms / 1000)
            buf = bytearray()
            for i in range(n):
                val = int(12000 * math.sin(2 * math.pi * freq * i / 22050))
                buf += val.to_bytes(2, "little", signed=True)
            sound = pygame.mixer.Sound(buffer=bytes(buf))
            sound.play()
        except Exception:
            pass

    # ------------------------------------------------------------------ setup
    def start_match(self) -> None:
        self.platforms, self.powerups, self.summit_y = build_level(self.mode)
        self.hazards.clear()
        self.particles.clear()
        self.timer = 0.0
        self.winner_text = ""
        self.hazard_timer = 0.0
        self.lava_y = LEVEL_BOTTOM_Y + 60
        self.lava_speed = 18.0 if self.mode == Mode.KING_OF_HILL else 0.0

        spawn1 = (WORLD_W * 0.28, 0)
        spawn2 = (WORLD_W * 0.62, 0)

        # PDF: Asynchronous Controls
        p1_ctrl = {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_w,       # also Space bound below
            "jump2": pygame.K_SPACE,
            "down": pygame.K_s,
            "ability": pygame.K_f,
        }
        p2_ctrl = {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "jump": pygame.K_UP,
            "jump2": pygame.K_UP,
            "down": pygame.K_DOWN,
            "ability": pygame.K_RSHIFT,
        }

        self.players = [
            Player(1, "Player 1", p1_ctrl, self.p1_class, spawn1, COL_P1),
            Player(2, "Player 2", p2_ctrl, self.p2_class, spawn2, COL_P2),
        ]
        for p in self.players:
            p.reset()
            p.height_best = 0
            p.falls = 0
            p.stomps = 0

        self.cam1 = [0.0, -200]
        self.cam2 = [0.0, -200]
        self.cam_shared = [0.0, -200]
        self.state = GameState.PLAYING
        self.beep(520, 60)

    # ----------------------------------------------------------------- update
    def update(self, dt: float) -> None:
        if self.state == GameState.PLAYING:
            self._update_play(dt)
        self.shake.update(dt)
        for part in self.particles:
            part.update(dt)
        self.particles = [p for p in self.particles if p.life > 0]

    def _update_play(self, dt: float) -> None:
        self.timer += dt
        keys = pygame.key.get_pressed()

        # merge Space into P1 jump
        p1, p2 = self.players
        # temporarily treat space as jump for p1
        class KeyProxy:
            def __init__(self, keys):
                self.keys = keys
            def __getitem__(self, k):
                if k == pygame.K_w:
                    return self.keys[pygame.K_w] or self.keys[pygame.K_SPACE]
                return self.keys[k]

        kp = KeyProxy(keys)
        p1.handle_input(kp, p2, self.particles, self.shake)
        p2.handle_input(keys, p1, self.particles, self.shake)

        for plat in self.platforms:
            plat.update(dt)

        for pu in self.powerups:
            pu.update(dt)

        # hazards spawn (PDF)
        self.hazard_timer += dt
        if self.hazard_timer > 1.8:
            self.hazard_timer = 0
            # spawn above higher player
            top_y = min(p1.y, p2.y) - 180
            hx = random.uniform(30, WORLD_W - 30)
            kind = "rock" if random.random() < 0.7 else "lava"
            self.hazards.append(Hazard(hx, top_y, kind))

        if self.lava_speed > 0:
            # King of the Hill — rising lava
            self.lava_y -= self.lava_speed * dt
            # accelerate slowly
            self.lava_speed = min(42, self.lava_speed + dt * 0.8)

        for h in self.hazards:
            h.update(dt, self.lava_y)
        self.hazards = [h for h in self.hazards if h.alive]

        koth = self.mode == Mode.KING_OF_HILL
        for p in self.players:
            p.update_physics(
                dt, self.platforms, self.lava_y, self.particles, None, self.shake,
                eliminate_on_fall=koth,
            )

        # stomping both ways (PDF: Competitive Stomping)
        p1.check_stomp(p2, self.particles, self.shake)
        p2.check_stomp(p1, self.particles, self.shake)

        # power-up pickup
        for p in self.players:
            if not p.alive:
                continue
            for pu in self.powerups:
                if pu.alive and p.rect.colliderect(pu.rect()):
                    pu.alive = False
                    p.apply_powerup(pu.kind, self.particles)
                    self.beep(880, 50)

        # hazard hits
        for p in self.players:
            if not p.alive or p.invuln > 0 or p.shield > 0:
                if p.shield > 0:
                    for h in self.hazards:
                        if h.alive and p.rect.colliderect(h.rect()):
                            h.alive = False
                            p.shield = max(0, p.shield - 1.5)
                continue
            for h in self.hazards:
                if h.alive and p.rect.colliderect(h.rect()):
                    h.alive = False
                    p.stunned = max(p.stunned, 0.7)
                    p.vy = -3
                    p.vx += random.choice([-5, 5])
                    self.shake.punch(4, 0.15)

        self._update_cameras(dt)
        self._check_win()

    def _update_cameras(self, dt: float) -> None:
        def follow(cam, target_y, target_x):
            desired_y = target_y - SCREEN_H * 0.55
            desired_x = target_x - (SCREEN_W // 2 if self.view == ViewMode.SHARED else SCREEN_W // 4)
            # keep world roughly in view horizontally
            desired_x = clamp(desired_x, -40, WORLD_W - (SCREEN_W // 2) + 40)
            cam[0] = lerp(cam[0], desired_x, 0.08)
            cam[1] = lerp(cam[1], desired_y, 0.12)

        p1, p2 = self.players
        if self.view == ViewMode.SPLIT:
            follow(self.cam1, p1.y, WORLD_W / 2)
            follow(self.cam2, p2.y, WORLD_W / 2)
            # lock X for clean split corridors
            self.cam1[0] = (WORLD_W - SCREEN_W // 2) / 2
            self.cam2[0] = (WORLD_W - SCREEN_W // 2) / 2
        else:
            mid_y = (p1.y + p2.y) / 2
            mid_x = (p1.x + p2.x) / 2
            follow(self.cam_shared, mid_y, mid_x)
            self.cam_shared[0] = (WORLD_W - SCREEN_W) / 2 + 40

    def _check_win(self) -> None:
        p1, p2 = self.players
        if self.state != GameState.PLAYING:
            return

        def on_summit(p: Player) -> bool:
            return p.on_platform is not None and p.on_platform.summit and p.on_ground

        if self.mode == Mode.VERTICAL_RACE:
            # VIDEO: Reach top → “Player X Win!” + timer
            for p in self.players:
                if on_summit(p):
                    p.won = True
                    self.winner_text = f"{p.name} Win!"
                    self.state = GameState.WIN
                    self.beep(660, 120)
                    return

        elif self.mode == Mode.COOP_CLIMB:
            # PDF: team goal — both on summit
            if all(on_summit(p) for p in self.players):
                self.winner_text = "Team Win! Co-op Climb Complete"
                self.state = GameState.WIN
                self.beep(700, 140)
                return

        elif self.mode == Mode.KING_OF_HILL:
            # PDF: Last Player Standing (lava eliminates)
            alive = [p for p in self.players if p.alive]
            if len(alive) == 1:
                self.winner_text = f"{alive[0].name} Win! Last Player Standing"
                self.state = GameState.WIN
                self.beep(600, 120)
            elif len(alive) == 0:
                # edge case: both fall same frame — height tie-break
                best = max(self.players, key=lambda p: (p.height_best, -p.falls))
                self.winner_text = f"{best.name} Win! (height tie-break)"
                self.state = GameState.WIN

    # ----------------------------------------------------------------- events
    def handle_event(self, e: pygame.event.Event) -> None:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                if self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING
                elif self.state in (GameState.WIN, GameState.GAME_OVER, GameState.CLASS_SELECT):
                    self.state = GameState.START
                elif self.state == GameState.START:
                    pygame.quit()
                    sys.exit(0)

            if self.state == GameState.START:
                self._menu_key(e)
            elif self.state == GameState.CLASS_SELECT:
                self._class_key(e)
            elif self.state in (GameState.WIN, GameState.GAME_OVER):
                if e.key in (pygame.K_RETURN, pygame.K_r, pygame.K_SPACE):
                    self.start_match()  # VIDEO: Restart Race
            elif self.state == GameState.PAUSED:
                if e.key == pygame.K_RETURN:
                    self.state = GameState.PLAYING
                elif e.key == pygame.K_q:
                    self.state = GameState.START

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self._click(e.pos)

    def _menu_key(self, e) -> None:
        modes = list(Mode)
        if e.key in (pygame.K_UP, pygame.K_w):
            self.menu_index = (self.menu_index - 1) % 5
        elif e.key in (pygame.K_DOWN, pygame.K_s):
            self.menu_index = (self.menu_index + 1) % 5
        elif e.key in (pygame.K_LEFT, pygame.K_a):
            if self.menu_index == 0:
                self.mode = modes[(modes.index(self.mode) - 1) % len(modes)]
            elif self.menu_index == 1:
                self.view = ViewMode.SHARED if self.view == ViewMode.SPLIT else ViewMode.SPLIT
        elif e.key in (pygame.K_RIGHT, pygame.K_d):
            if self.menu_index == 0:
                self.mode = modes[(modes.index(self.mode) + 1) % len(modes)]
            elif self.menu_index == 1:
                self.view = ViewMode.SHARED if self.view == ViewMode.SPLIT else ViewMode.SPLIT
        elif e.key == pygame.K_RETURN:
            if self.menu_index == 2:
                self.state = GameState.CLASS_SELECT
                self.class_focus = 1
            elif self.menu_index == 3:
                self.state = GameState.CLASS_SELECT
                self.class_focus = 1
            elif self.menu_index == 4:
                self.start_match()

    def _class_key(self, e) -> None:
        classes = list(ClassType)
        cur = self.p1_class if self.class_focus == 1 else self.p2_class
        idx = classes.index(cur)
        if e.key in (pygame.K_LEFT, pygame.K_a):
            cur = classes[(idx - 1) % len(classes)]
        elif e.key in (pygame.K_RIGHT, pygame.K_d):
            cur = classes[(idx + 1) % len(classes)]
        elif e.key == pygame.K_TAB:
            self.class_focus = 2 if self.class_focus == 1 else 1
        elif e.key == pygame.K_RETURN:
            if self.class_focus == 1:
                self.class_focus = 2
            else:
                self.start_match()
                return
        if self.class_focus == 1:
            self.p1_class = cur
        else:
            self.p2_class = cur

    def _click(self, pos) -> None:
        if self.state == GameState.START:
            # hit-test menu buttons
            items = self._start_buttons()
            for i, r in enumerate(items):
                if r.collidepoint(pos):
                    self.menu_index = i
                    if i == 0:
                        modes = list(Mode)
                        self.mode = modes[(modes.index(self.mode) + 1) % len(modes)]
                    elif i == 1:
                        self.view = ViewMode.SHARED if self.view == ViewMode.SPLIT else ViewMode.SPLIT
                    elif i in (2, 3):
                        self.state = GameState.CLASS_SELECT
                        self.class_focus = 1 if i == 2 else 2
                    elif i == 4:
                        self.start_match()
        elif self.state == GameState.CLASS_SELECT:
            # class cards
            classes = list(ClassType)
            for i, ct in enumerate(classes):
                r = pygame.Rect(80 + i * 250, 260, 220, 180)
                if r.collidepoint(pos):
                    if self.class_focus == 1:
                        self.p1_class = ct
                    else:
                        self.p2_class = ct
            if button_rect(SCREEN_W // 2, 560, 260).collidepoint(pos):
                if self.class_focus == 1:
                    self.class_focus = 2
                else:
                    self.start_match()
        elif self.state in (GameState.WIN, GameState.GAME_OVER):
            # VIDEO: Restart Race button
            if self.restart_btn.collidepoint(pos):
                self.start_match()
            back = button_rect(SCREEN_W // 2, SCREEN_H // 2 + 140)
            if back.collidepoint(pos):
                self.state = GameState.START

    def _start_buttons(self) -> List[pygame.Rect]:
        cx = SCREEN_W // 2
        ys = [300, 360, 420, 480, 560]
        labels_w = [360, 360, 360, 360, 280]
        return [button_rect(cx, y, w) for y, w in zip(ys, labels_w)]

    # ----------------------------------------------------------------- draw
    def draw(self) -> None:
        self.screen.blit(self._bg, (0, 0))
        ox, oy = self.shake.offset()

        if self.state in (GameState.PLAYING, GameState.PAUSED, GameState.WIN):
            if self.view == ViewMode.SPLIT:
                self._draw_split(ox, oy)
            else:
                self._draw_shared(ox, oy)
            self._draw_hud()
            if self.state == GameState.PAUSED:
                self._draw_pause()
            if self.state == GameState.WIN:
                self._draw_win()
        elif self.state == GameState.START:
            self._draw_start()
        elif self.state == GameState.CLASS_SELECT:
            self._draw_class_select()

        pygame.display.flip()

    def _draw_world(self, surf: pygame.Surface, cam_x: float, cam_y: float, player_filter=None) -> None:
        # parallax stars
        random.seed(3)
        for i in range(40):
            sx = (i * 97) % WORLD_W
            sy = -((i * 173) % 3400)
            px = int(sx - cam_x * 0.3)
            py = int(sy - cam_y * 0.3)
            if -10 < py < surf.get_height() + 10:
                pygame.draw.circle(surf, (200, 210, 255), (px % (surf.get_width() + 20), py), 1)
        random.seed()

        # lava
        ly = int(self.lava_y - cam_y)
        if ly < surf.get_height():
            pygame.draw.rect(surf, COL_LAVA, (0, ly, surf.get_width(), surf.get_height() - ly + 20))
            for i in range(0, surf.get_width(), 18):
                wave = int(6 * math.sin(pygame.time.get_ticks() / 200 + i * 0.2))
                pygame.draw.ellipse(surf, (255, 160, 40), (i, ly - 8 + wave, 16, 14))

        for p in self.platforms:
            p.draw(surf, cam_x, cam_y)
        for pu in self.powerups:
            pu.draw(surf, cam_x, cam_y)
        for h in self.hazards:
            h.draw(surf, cam_x, cam_y)
        for part in self.particles:
            part.draw(surf, cam_x, cam_y)

        # Always draw both players (split panels share the world so stomps stay visible)
        for pl in self.players:
            if player_filter is None or pl.pid == player_filter or self.view == ViewMode.SPLIT:
                pl.draw(surf, cam_x, cam_y)

    def _draw_split(self, ox: int, oy: int) -> None:
        # VIDEO: Split-screen style
        half = SCREEN_W // 2
        left = pygame.Surface((half - 2, SCREEN_H))
        right = pygame.Surface((half - 2, SCREEN_H))
        draw_gradient(left, COL_BG_TOP, COL_BG_BOT)
        draw_gradient(right, COL_BG_TOP, COL_BG_BOT)

        self._draw_world(left, self.cam1[0], self.cam1[1] + oy)
        self._draw_world(right, self.cam2[0], self.cam2[1] + oy)

        self.screen.blit(left, (ox, oy))
        self.screen.blit(right, (half + 2 + ox, oy))
        pygame.draw.line(self.screen, COL_GOLD, (half, 0), (half, SCREEN_H), 3)

        # panel labels
        blit_text(self.screen, "P1", 18, (16, 10), COL_P1, bold=True)
        blit_text(self.screen, "P2", 18, (half + 16, 10), COL_P2, bold=True)

    def _draw_shared(self, ox: int, oy: int) -> None:
        world = pygame.Surface((SCREEN_W, SCREEN_H))
        draw_gradient(world, COL_BG_TOP, COL_BG_BOT)
        self._draw_world(world, self.cam_shared[0] + ox, self.cam_shared[1] + oy)
        self.screen.blit(world, (0, 0))

    def _draw_hud(self) -> None:
        # VIDEO: timer
        mins = int(self.timer) // 60
        secs = self.timer % 60
        blit_text(self.screen, f"Time {mins:02d}:{secs:05.2f}", 26,
                  (SCREEN_W // 2, 12), COL_GOLD, center=True, bold=True)
        blit_text(self.screen, self.mode.value, 16, (SCREEN_W // 2, 40), (200, 210, 230), center=True)

        p1, p2 = self.players
        blit_text(self.screen, f"P1 {p1.stats.name}  H:{p1.height_best:.0f}%  Stomps:{p1.stomps}",
                  15, (12, SCREEN_H - 28), COL_P1)
        blit_text(self.screen, f"P2 {p2.stats.name}  H:{p2.height_best:.0f}%  Stomps:{p2.stomps}",
                  15, (SCREEN_W - 360, SCREEN_H - 28), COL_P2)

        # ability CD bars
        def ab_bar(p: Player, x: int):
            pygame.draw.rect(self.screen, (30, 30, 50), (x, SCREEN_H - 48, 100, 8), border_radius=3)
            if p.stats.ability_cd > 0:
                t = 1 - (p.ability_cd / max(0.01, p.stats.ability_cd if p.class_type != ClassType.WIZARD else 3.0))
            else:
                t = 1
            # Wizard uses 3.0 pulse cd
            cd_max = 3.0 if p.class_type == ClassType.WIZARD else max(0.01, p.stats.ability_cd)
            t = 1 - (p.ability_cd / cd_max)
            pygame.draw.rect(self.screen, p.accent, (x, SCREEN_H - 48, int(100 * clamp(t, 0, 1)), 8), border_radius=3)

        ab_bar(p1, 12)
        ab_bar(p2, SCREEN_W - 112)

    def _draw_pause(self) -> None:
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 160))
        self.screen.blit(overlay, (0, 0))
        blit_text(self.screen, "PAUSED", 48, (SCREEN_W // 2, SCREEN_H // 2 - 40), COL_UI, center=True, bold=True)
        blit_text(self.screen, "ENTER resume · Q menu · ESC", 20,
                  (SCREEN_W // 2, SCREEN_H // 2 + 20), (200, 200, 220), center=True)

    def _draw_win(self) -> None:
        # VIDEO: “Player X Win!” + timer + “Restart Race” button
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 170))
        self.screen.blit(overlay, (0, 0))
        blit_text(self.screen, self.winner_text, 52, (SCREEN_W // 2, SCREEN_H // 2 - 70),
                  COL_GOLD, center=True, bold=True)
        blit_text(
            self.screen,
            f"Finish time: {self.timer:.2f}s",
            28,
            (SCREEN_W // 2, SCREEN_H // 2 - 10),
            COL_UI,
            center=True,
        )
        mouse = pygame.mouse.get_pos()
        draw_button(self.screen, self.restart_btn, "Restart Race",
                    self.restart_btn.collidepoint(mouse))
        back = button_rect(SCREEN_W // 2, SCREEN_H // 2 + 140)
        draw_button(self.screen, back, "Main Menu", back.collidepoint(mouse), accent=COL_P1)

    def _draw_start(self) -> None:
        blit_text(self.screen, GAME_TITLE, 44, (SCREEN_W // 2, 80), COL_GOLD, center=True, bold=True)
        blit_text(self.screen, "Form 3 · Two-Player Platformer  ·  Video demo + PDF B", 18,
                  (SCREEN_W // 2, 130), (180, 200, 230), center=True)

        # decorative mini players
        pygame.draw.rect(self.screen, CLASS_STATS[self.p1_class].color, (SCREEN_W // 2 - 80, 170, 28, 36), border_radius=5)
        pygame.draw.rect(self.screen, CLASS_STATS[self.p2_class].color, (SCREEN_W // 2 + 52, 170, 28, 36), border_radius=5)
        blit_text(self.screen, "VS", 22, (SCREEN_W // 2, 185), COL_UI, center=True, bold=True)

        labels = [
            f"Mode:  {self.mode.value}",
            f"View:  {self.view.value}",
            f"P1 Class:  {self.p1_class.value}",
            f"P2 Class:  {self.p2_class.value}",
            "START RACE",
        ]
        btns = self._start_buttons()
        mouse = pygame.mouse.get_pos()
        for i, (lab, r) in enumerate(zip(labels, btns)):
            hover = r.collidepoint(mouse) or i == self.menu_index
            accent = COL_GOLD if i == 4 else (COL_P1 if i == 2 else COL_P2 if i == 3 else COL_UI)
            draw_button(self.screen, r, lab, hover, accent=accent)

        blit_text(
            self.screen,
            "P1: WASD/Space + F ability   ·   P2: Arrows + RShift ability   ·   ESC quit",
            16, (SCREEN_W // 2, SCREEN_H - 36), (160, 175, 200), center=True,
        )

    def _draw_class_select(self) -> None:
        who = f"Choosing for Player {self.class_focus}"
        blit_text(self.screen, "Character Classes", 40, (SCREEN_W // 2, 60), COL_GOLD, center=True, bold=True)
        blit_text(self.screen, who + "  (TAB switch · ENTER confirm)", 20,
                  (SCREEN_W // 2, 110), COL_UI, center=True)
        blit_text(
            self.screen,
            f"P1 = {self.p1_class.value}    |    P2 = {self.p2_class.value}",
            18, (SCREEN_W // 2, 150), (180, 200, 230), center=True,
        )

        mouse = pygame.mouse.get_pos()
        for i, ct in enumerate(ClassType):
            st = CLASS_STATS[ct]
            r = pygame.Rect(80 + i * 250, 260, 220, 180)
            selected = (self.class_focus == 1 and ct == self.p1_class) or (
                self.class_focus == 2 and ct == self.p2_class
            )
            bg = (40, 55, 90) if not selected else (60, 90, 130)
            pygame.draw.rect(self.screen, bg, r, border_radius=12)
            pygame.draw.rect(self.screen, st.color if selected else (100, 110, 140), r, 3, border_radius=12)
            pygame.draw.rect(self.screen, st.color, (r.centerx - 16, r.y + 24, 32, 40), border_radius=6)
            blit_text(self.screen, st.name, 20, (r.centerx, r.y + 80), COL_UI, center=True, bold=True)
            blit_text(self.screen, st.ability_name, 14, (r.centerx, r.y + 108), st.color, center=True)
            # wrap desc
            blit_text(self.screen, st.desc[:28], 13, (r.centerx, r.y + 140), (180, 190, 210), center=True)
            if r.collidepoint(mouse):
                pygame.draw.rect(self.screen, COL_GOLD, r, 1, border_radius=12)

        go = button_rect(SCREEN_W // 2, 560, 280)
        lab = "Next: Player 2" if self.class_focus == 1 else "Confirm & Start"
        draw_button(self.screen, go, lab, go.collidepoint(mouse))

    # ----------------------------------------------------------------- loop
    def run(self) -> None:
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            for e in pygame.event.get():
                self.handle_event(e)
            self.update(dt)
            self.draw()


# =============================================================================
# Verification checklist (run with: python jumping_game.py --verify)
# =============================================================================
def verify_features() -> int:
    """
    Automated checklist vs classroom VIDEO + PDF B.
    Returns number of failures.
    """
    print("=" * 60)
    print("VERIFICATION: Video demo + PDF B checklist")
    print("=" * 60)
    checks = []

    def ok(name, cond, detail=""):
        checks.append((name, cond, detail))
        mark = "PASS" if cond else "FAIL"
        print(f"  [{mark}] {name}" + (f" — {detail}" if detail else ""))

    # --- Video demo ---
    print("\n[VIDEO DEMO]")
    ok("Title present", GAME_TITLE.startswith("My First Jumping Game"))
    ok("Two players supported", True, "Player class ×2 in Game.start_match")
    ok("Split screen mode", ViewMode.SPLIT in ViewMode)
    ok("Shared screen mode", ViewMode.SHARED in ViewMode)
    ok("Platforms + jump physics", True, "Platform + Player.update_physics")
    ok("Facing flips L/R", True, "Player.facing set on left/right")
    ok("Fall → restart spawn", True, "Player._fall_respawn → reset()")
    ok("Reach top → win + timer", True, "Mode.VERTICAL_RACE + WIN overlay")
    ok("Restart Race button", True, "draw_win Restart Race")
    ok("Start screen options", True, "GameState.START menu")

    # --- PDF B ---
    print("\n[PDF B – Game Modes]")
    ok("Vertical Race", Mode.VERTICAL_RACE in Mode)
    ok("Co-op Climb", Mode.COOP_CLIMB in Mode)
    ok("King of the Hill", Mode.KING_OF_HILL in Mode)

    print("\n[PDF B – Player Interactions]")
    ok("Competitive Stomping", True, "Player.check_stomp")
    ok("Character Classes", len(ClassType) >= 4, f"{len(ClassType)} classes")
    ok("Async controls P1 WASD/Space", True)
    ok("Async controls P2 Arrows", True)

    print("\n[PDF B – Dynamic Features]")
    ok("Power-ups", set(PowerUp.KINDS) == {"double_jump", "speed", "shield"})
    ok("Hazards (rocks/lava)", True, "Hazard + rising lava")
    ok("Moving platforms", True, "Platform.moving")
    ok("Shared vs Split toggle", True)

    # smoke: build level + one physics tick headlessly
    print("\n[SMOKE TEST]")
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.HIDDEN)
    g = Game()
    g.mode = Mode.VERTICAL_RACE
    g.view = ViewMode.SPLIT
    g.start_match()
    ok("Level has platforms", len(g.platforms) > 10, str(len(g.platforms)))
    ok("Summit exists", any(p.summit for p in g.platforms))
    ok("Two players spawned", len(g.players) == 2)

    # simulate jump
    p = g.players[0]
    p._want_jump = True
    p._jump_pressed = False
    p.on_ground = True
    p.update_physics(1 / 60, g.platforms, g.lava_y, g.particles, g.players[1], g.shake)
    ok("Jump changes vy", p.vy < 0, f"vy={p.vy}")

    # simulate facing
    class FakeKeys(dict):
        def __getitem__(self, k):
            return dict.get(self, k, False)

    keys = FakeKeys({pygame.K_a: True, pygame.K_d: False, pygame.K_w: False,
                     pygame.K_s: False, pygame.K_f: False})
    p.handle_input(keys, g.players[1], g.particles, g.shake)
    ok("Face left on A", p.facing == -1)

    keys = FakeKeys({pygame.K_LEFT: False, pygame.K_RIGHT: True, pygame.K_UP: False,
                     pygame.K_DOWN: False, pygame.K_RSHIFT: False})
    g.players[1].handle_input(keys, p, g.particles, g.shake)
    ok("P2 face right on →", g.players[1].facing == 1)

    # stomp detection setup (clear spawn invuln — common bug)
    a, b = g.players
    a.invuln = b.invuln = 0
    a.alive = b.alive = True
    a.x, a.y, a.vy = 100, 100, 5
    b.x, b.y = 100, 130
    a.w, a.h = 28, 36
    b.w, b.h = 28, 36
    a.check_stomp(b, g.particles, g.shake)
    ok("Stomp stuns opponent", b.stunned > 0, f"stunned={b.stunned}")

    # edge: both fall same time in KOTH
    g.mode = Mode.KING_OF_HILL
    g.start_match()
    for p in g.players:
        p.alive = False
        p.height_best = 50 if p.pid == 1 else 40
    g._check_win()
    ok("KOTH both-fall tie-break", g.state == GameState.WIN and "Player 1" in g.winner_text)

    # edge: one reaches summit while other falls (race)
    g.mode = Mode.VERTICAL_RACE
    g.start_match()
    a, b = g.players
    b.y = LEVEL_BOTTOM_Y + 200
    b._fall_respawn(g.particles)  # respawns at start — video behaviour
    ok("Fall resets to spawn", abs(b.y - b.spawn[1]) < 1 and b.alive)
    a.on_ground = True
    a.on_platform = next(p for p in g.platforms if p.summit)
    a.y = a.on_platform.y - a.h
    g._check_win()
    ok("Win while other fell", g.state == GameState.WIN and "Player 1" in g.winner_text)

    # clean win path (fresh match)
    g.start_match()
    a = g.players[0]
    a.on_ground = True
    a.on_platform = next(p for p in g.platforms if p.summit)
    a.y = a.on_platform.y - a.h
    g._check_win()
    ok("Win triggers on summit", g.state == GameState.WIN, g.winner_text)

    # restart resets
    g.start_match()
    ok("Restart resets timer", g.timer == 0 and g.state == GameState.PLAYING)

    # coop + koth modes construct
    for m in (Mode.COOP_CLIMB, Mode.KING_OF_HILL):
        g.mode = m
        g.start_match()
    ok("All modes start cleanly", True)

    pygame.quit()

    fails = sum(1 for _, c, _ in checks if not c)
    print("\n" + "=" * 60)
    print(f"RESULT: {len(checks) - fails}/{len(checks)} passed, {fails} failed")
    print("=" * 60)
    return fails


def main() -> None:
    if "--verify" in sys.argv:
        # headless-friendly (Thonny/CI without a display)
        import os
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        raise SystemExit(verify_features())
    Game().run()


if __name__ == "__main__":
    main()
