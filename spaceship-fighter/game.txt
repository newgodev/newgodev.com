#!/usr/bin/env python3
"""
Nebula Strike — arcade spaceship fighter.
Evolved from a simple Moving Box demo into a full wave shooter.
"""

from __future__ import annotations

import math
import random
import sys
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Tuple

import pygame

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

WIDTH, HEIGHT = 960, 720
FPS = 60
TITLE = "Nebula Strike"

# Colors
VOID = (6, 8, 18)
NEON_CYAN = (80, 240, 255)
NEON_MAGENTA = (255, 70, 180)
NEON_LIME = (120, 255, 100)
NEON_GOLD = (255, 210, 70)
NEON_RED = (255, 70, 90)
NEON_BLUE = (90, 140, 255)
WHITE = (240, 245, 255)
DIM = (140, 150, 180)


class State(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def draw_text(
    surf: pygame.Surface,
    text: str,
    size: int,
    color: Tuple[int, int, int],
    center: Optional[Tuple[int, int]] = None,
    topleft: Optional[Tuple[int, int]] = None,
    bold: bool = True,
) -> pygame.Rect:
    font = pygame.font.SysFont("consolas,dejavusansmono,monospace", size, bold=bold)
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = center
    if topleft:
        rect.topleft = topleft
    surf.blit(img, rect)
    return rect


# ---------------------------------------------------------------------------
# Particles & FX
# ---------------------------------------------------------------------------

@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float
    color: Tuple[int, int, int]
    size: float
    gravity: float = 0.0

    def update(self, dt: float) -> bool:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        self.life -= dt
        return self.life > 0

    def draw(self, surf: pygame.Surface) -> None:
        t = self.life / self.max_life
        r = max(1, int(self.size * t))
        c = tuple(int(ch * t) for ch in self.color)
        pygame.draw.circle(surf, c, (int(self.x), int(self.y)), r)


@dataclass
class Star:
    x: float
    y: float
    speed: float
    size: int
    brightness: int


class Starfield:
    def __init__(self, n: int = 120) -> None:
        self.stars = [
            Star(
                random.uniform(0, WIDTH),
                random.uniform(0, HEIGHT),
                random.uniform(20, 180),
                random.choice([1, 1, 1, 2, 2, 3]),
                random.randint(80, 255),
            )
            for _ in range(n)
        ]

    def update(self, dt: float, boost: float = 1.0) -> None:
        for s in self.stars:
            s.y += s.speed * boost * dt
            if s.y > HEIGHT:
                s.y = -2
                s.x = random.uniform(0, WIDTH)

    def draw(self, surf: pygame.Surface) -> None:
        for s in self.stars:
            c = (s.brightness, s.brightness, min(255, s.brightness + 40))
            if s.size <= 1:
                surf.set_at((int(s.x) % WIDTH, int(s.y) % HEIGHT), c)
            else:
                pygame.draw.circle(surf, c, (int(s.x), int(s.y)), s.size)


# ---------------------------------------------------------------------------
# Entities
# ---------------------------------------------------------------------------

@dataclass
class Bullet:
    x: float
    y: float
    vx: float
    vy: float
    damage: int
    friendly: bool
    color: Tuple[int, int, int]
    radius: int = 4
    life: float = 3.0

    def update(self, dt: float) -> bool:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        return (
            self.life > 0
            and -40 < self.x < WIDTH + 40
            and -40 < self.y < HEIGHT + 40
        )

    def rect(self) -> pygame.Rect:
        r = self.radius
        return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)

    def draw(self, surf: pygame.Surface) -> None:
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y)), max(1, self.radius // 2))


class EnemyKind(Enum):
    SCOUT = auto()
    TANK = auto()
    ZIGZAG = auto()
    SNIPER = auto()
    BOSS = auto()


@dataclass
class Enemy:
    kind: EnemyKind
    x: float
    y: float
    hp: float
    max_hp: float
    score: int
    vx: float = 0.0
    vy: float = 80.0
    phase: float = 0.0
    shoot_cd: float = 1.0
    flash: float = 0.0
    radius: int = 18

    def update(self, dt: float, player_x: float) -> List[Bullet]:
        self.phase += dt
        self.flash = max(0.0, self.flash - dt)
        shots: List[Bullet] = []

        if self.kind == EnemyKind.SCOUT:
            self.y += self.vy * dt
            self.x += math.sin(self.phase * 3) * 40 * dt
        elif self.kind == EnemyKind.TANK:
            self.y += self.vy * 0.55 * dt
            self.x += math.sin(self.phase) * 20 * dt
        elif self.kind == EnemyKind.ZIGZAG:
            self.y += self.vy * 0.9 * dt
            self.vx = math.cos(self.phase * 4) * 220
            self.x += self.vx * dt
        elif self.kind == EnemyKind.SNIPER:
            self.y += min(self.vy * 0.35 * dt, max(0, 120 - self.y) * dt)
            self.x += (player_x - self.x) * 0.6 * dt
        elif self.kind == EnemyKind.BOSS:
            target_y = 110
            self.y += (target_y - self.y) * 1.5 * dt
            self.x = WIDTH / 2 + math.sin(self.phase * 0.7) * (WIDTH * 0.32)

        self.x = clamp(self.x, 30, WIDTH - 30)
        self.shoot_cd -= dt
        if self.shoot_cd <= 0 and self.y > 20:
            shots = self.fire(player_x)
        return shots

    def fire(self, player_x: float) -> List[Bullet]:
        shots: List[Bullet] = []
        if self.kind == EnemyKind.SCOUT:
            self.shoot_cd = 1.4
            shots.append(Bullet(self.x, self.y + 12, 0, 260, 1, False, NEON_RED, 3))
        elif self.kind == EnemyKind.TANK:
            self.shoot_cd = 1.8
            for a in (-0.35, 0, 0.35):
                shots.append(
                    Bullet(
                        self.x,
                        self.y + 14,
                        math.sin(a) * 120,
                        math.cos(a) * 220,
                        1,
                        False,
                        NEON_MAGENTA,
                        4,
                    )
                )
        elif self.kind == EnemyKind.ZIGZAG:
            self.shoot_cd = 1.1
            shots.append(Bullet(self.x, self.y + 10, 0, 300, 1, False, NEON_GOLD, 3))
        elif self.kind == EnemyKind.SNIPER:
            self.shoot_cd = 0.9
            dx = player_x - self.x
            dy = 400
            mag = math.hypot(dx, dy) or 1
            shots.append(
                Bullet(self.x, self.y + 10, dx / mag * 340, dy / mag * 340, 1, False, NEON_LIME, 3)
            )
        elif self.kind == EnemyKind.BOSS:
            self.shoot_cd = 0.45
            pattern = int(self.phase * 2) % 3
            if pattern == 0:
                for i in range(-3, 4):
                    shots.append(
                        Bullet(self.x + i * 18, self.y + 30, i * 40, 240, 1, False, NEON_RED, 5)
                    )
            elif pattern == 1:
                for a in range(0, 360, 30):
                    rad = math.radians(a + self.phase * 40)
                    shots.append(
                        Bullet(
                            self.x,
                            self.y,
                            math.cos(rad) * 180,
                            math.sin(rad) * 180,
                            1,
                            False,
                            NEON_MAGENTA,
                            4,
                        )
                    )
            else:
                for i in (-1, 0, 1):
                    shots.append(
                        Bullet(self.x + i * 40, self.y + 28, i * 30, 280, 1, False, NEON_GOLD, 5)
                    )
        return shots

    def hit(self, dmg: int) -> bool:
        self.hp -= dmg
        self.flash = 0.08
        return self.hp <= 0

    def rect(self) -> pygame.Rect:
        r = self.radius
        return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)

    def draw(self, surf: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)
        flash = self.flash > 0
        if self.kind == EnemyKind.SCOUT:
            col = WHITE if flash else NEON_RED
            pts = [(x, y + 16), (x - 14, y - 12), (x + 14, y - 12)]
            pygame.draw.polygon(surf, col, pts)
            pygame.draw.circle(surf, NEON_GOLD, (x, y), 4)
        elif self.kind == EnemyKind.TANK:
            col = WHITE if flash else (180, 80, 255)
            pygame.draw.rect(surf, col, (x - 20, y - 14, 40, 28), border_radius=6)
            pygame.draw.rect(surf, NEON_CYAN, (x - 8, y - 6, 16, 12))
        elif self.kind == EnemyKind.ZIGZAG:
            col = WHITE if flash else NEON_GOLD
            pts = [(x, y - 16), (x + 16, y), (x, y + 16), (x - 16, y)]
            pygame.draw.polygon(surf, col, pts)
        elif self.kind == EnemyKind.SNIPER:
            col = WHITE if flash else NEON_LIME
            pygame.draw.circle(surf, col, (x, y), 16, 2)
            pygame.draw.line(surf, col, (x, y - 18), (x, y + 18), 2)
            pygame.draw.line(surf, col, (x - 18, y), (x + 18, y), 2)
        elif self.kind == EnemyKind.BOSS:
            col = WHITE if flash else NEON_MAGENTA
            pygame.draw.ellipse(surf, col, (x - 70, y - 36, 140, 72))
            pygame.draw.ellipse(surf, VOID, (x - 50, y - 22, 100, 44))
            pygame.draw.circle(surf, NEON_CYAN, (x, y), 14)
            # HP bar
            bw = 160
            ratio = clamp(self.hp / self.max_hp, 0, 1)
            pygame.draw.rect(surf, (40, 40, 60), (x - bw // 2, y - 55, bw, 8), border_radius=3)
            pygame.draw.rect(
                surf, NEON_RED, (x - bw // 2, y - 55, int(bw * ratio), 8), border_radius=3
            )


class PowerKind(Enum):
    RAPID = auto()
    TRIPLE = auto()
    SHIELD = auto()
    HEALTH = auto()
    BOMB = auto()


POWER_COLORS = {
    PowerKind.RAPID: NEON_GOLD,
    PowerKind.TRIPLE: NEON_CYAN,
    PowerKind.SHIELD: NEON_BLUE,
    PowerKind.HEALTH: NEON_LIME,
    PowerKind.BOMB: NEON_MAGENTA,
}

POWER_LABELS = {
    PowerKind.RAPID: "R",
    PowerKind.TRIPLE: "T",
    PowerKind.SHIELD: "S",
    PowerKind.HEALTH: "+",
    PowerKind.BOMB: "B",
}


@dataclass
class PowerUp:
    kind: PowerKind
    x: float
    y: float
    vy: float = 90.0
    radius: int = 14
    spin: float = 0.0

    def update(self, dt: float) -> bool:
        self.y += self.vy * dt
        self.spin += dt * 4
        return self.y < HEIGHT + 30

    def rect(self) -> pygame.Rect:
        r = self.radius
        return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)

    def draw(self, surf: pygame.Surface) -> None:
        col = POWER_COLORS[self.kind]
        x, y = int(self.x), int(self.y)
        glow = abs(math.sin(self.spin)) * 4 + 12
        pygame.draw.circle(surf, col, (x, y), int(glow), 2)
        pygame.draw.circle(surf, col, (x, y), self.radius)
        draw_text(surf, POWER_LABELS[self.kind], 16, VOID, center=(x, y))


@dataclass
class Player:
    x: float = WIDTH / 2
    y: float = HEIGHT - 90
    speed: float = 340.0
    hp: int = 5
    max_hp: int = 5
    energy: float = 100.0
    fire_cd: float = 0.0
    rapid_t: float = 0.0
    triple_t: float = 0.0
    shield_t: float = 0.0
    invuln: float = 0.0
    radius: int = 16

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper) -> List[Bullet]:
        mx = my = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            mx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            mx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            my -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            my += 1

        boost = 1.0
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.energy > 0:
            boost = 1.7
            self.energy = max(0.0, self.energy - 35 * dt)
        else:
            self.energy = min(100.0, self.energy + 12 * dt)

        mag = math.hypot(mx, my) or 1.0
        self.x += (mx / mag) * self.speed * boost * dt
        self.y += (my / mag) * self.speed * boost * dt
        self.x = clamp(self.x, 24, WIDTH - 24)
        self.y = clamp(self.y, 40, HEIGHT - 24)

        self.fire_cd = max(0.0, self.fire_cd - dt)
        self.rapid_t = max(0.0, self.rapid_t - dt)
        self.triple_t = max(0.0, self.triple_t - dt)
        self.shield_t = max(0.0, self.shield_t - dt)
        self.invuln = max(0.0, self.invuln - dt)

        shots: List[Bullet] = []
        if keys[pygame.K_SPACE] or keys[pygame.K_z]:
            shots = self.try_fire()
        return shots

    def try_fire(self) -> List[Bullet]:
        if self.fire_cd > 0:
            return []
        delay = 0.12 if self.rapid_t > 0 else 0.22
        self.fire_cd = delay
        dmg = 2 if self.rapid_t > 0 else 1
        shots = [Bullet(self.x, self.y - 18, 0, -520, dmg, True, NEON_CYAN, 4)]
        if self.triple_t > 0:
            shots.append(Bullet(self.x - 12, self.y - 10, -90, -500, dmg, True, NEON_CYAN, 3))
            shots.append(Bullet(self.x + 12, self.y - 10, 90, -500, dmg, True, NEON_CYAN, 3))
        return shots

    def apply_power(self, kind: PowerKind) -> Optional[str]:
        if kind == PowerKind.RAPID:
            self.rapid_t = 8.0
            return "RAPID FIRE"
        if kind == PowerKind.TRIPLE:
            self.triple_t = 10.0
            return "TRIPLE SHOT"
        if kind == PowerKind.SHIELD:
            self.shield_t = 6.0
            return "SHIELD"
        if kind == PowerKind.HEALTH:
            self.hp = min(self.max_hp, self.hp + 1)
            return "HEALTH +1"
        if kind == PowerKind.BOMB:
            return "BOMB"
        return None

    def hurt(self) -> bool:
        if self.invuln > 0 or self.shield_t > 0:
            if self.shield_t > 0:
                self.shield_t = max(0.0, self.shield_t - 1.5)
            return False
        self.hp -= 1
        self.invuln = 1.2
        return self.hp <= 0

    def rect(self) -> pygame.Rect:
        r = self.radius
        return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)

    def draw(self, surf: pygame.Surface) -> None:
        if self.invuln > 0 and int(self.invuln * 20) % 2 == 0:
            return
        x, y = int(self.x), int(self.y)
        # Engine glow
        glow = 8 + int(abs(math.sin(pygame.time.get_ticks() * 0.02)) * 6)
        pygame.draw.circle(surf, (40, 120, 255), (x, y + 18), glow)
        # Hull
        pts = [(x, y - 22), (x - 18, y + 16), (x - 6, y + 8), (x + 6, y + 8), (x + 18, y + 16)]
        pygame.draw.polygon(surf, NEON_CYAN, pts)
        pygame.draw.polygon(surf, WHITE, pts, 1)
        pygame.draw.circle(surf, NEON_GOLD, (x, y - 2), 5)
        if self.shield_t > 0:
            a = int(100 + 80 * abs(math.sin(pygame.time.get_ticks() * 0.01)))
            shield = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(shield, (*NEON_BLUE, a), (30, 30), 28, 2)
            surf.blit(shield, (x - 30, y - 30))


# ---------------------------------------------------------------------------
# Game
# ---------------------------------------------------------------------------

@dataclass
class FloatingText:
    x: float
    y: float
    text: str
    color: Tuple[int, int, int]
    life: float = 1.0


@dataclass
class Game:
    screen: pygame.Surface
    clock: pygame.time.Clock
    state: State = State.MENU
    stars: Starfield = field(default_factory=Starfield)
    player: Player = field(default_factory=Player)
    bullets: List[Bullet] = field(default_factory=list)
    enemies: List[Enemy] = field(default_factory=list)
    powers: List[PowerUp] = field(default_factory=list)
    particles: List[Particle] = field(default_factory=list)
    floats: List[FloatingText] = field(default_factory=list)
    score: int = 0
    combo: int = 0
    combo_timer: float = 0.0
    wave: int = 0
    wave_timer: float = 0.0
    enemies_left: int = 0
    spawn_cd: float = 0.0
    boss_alive: bool = False
    shake: float = 0.0
    banner: str = ""
    banner_t: float = 0.0
    high_score: int = 0
    menu_pulse: float = 0.0

    def reset(self) -> None:
        self.player = Player()
        self.bullets.clear()
        self.enemies.clear()
        self.powers.clear()
        self.particles.clear()
        self.floats.clear()
        self.score = 0
        self.combo = 0
        self.combo_timer = 0.0
        self.wave = 0
        self.wave_timer = 0.0
        self.enemies_left = 0
        self.spawn_cd = 0.0
        self.boss_alive = False
        self.shake = 0.0
        self.banner = ""
        self.banner_t = 0.0
        self.state = State.PLAYING
        self.next_wave()

    def next_wave(self) -> None:
        self.wave += 1
        self.wave_timer = 0.0
        self.boss_alive = False
        if self.wave > 12:
            self.state = State.VICTORY
            self.high_score = max(self.high_score, self.score)
            return
        if self.wave % 4 == 0:
            self.enemies_left = 0
            self.spawn_boss()
            self.show_banner(f"BOSS WAVE {self.wave}")
        else:
            self.enemies_left = 6 + self.wave * 3
            self.spawn_cd = 0.4
            self.show_banner(f"WAVE {self.wave}")

    def show_banner(self, text: str) -> None:
        self.banner = text
        self.banner_t = 2.0

    def spawn_boss(self) -> None:
        hp = 80 + self.wave * 25
        self.enemies.append(
            Enemy(
                EnemyKind.BOSS,
                WIDTH / 2,
                -80,
                hp,
                hp,
                2000 + self.wave * 200,
                radius=55,
            )
        )
        self.boss_alive = True

    def spawn_enemy(self) -> None:
        kinds = [EnemyKind.SCOUT, EnemyKind.SCOUT, EnemyKind.ZIGZAG]
        if self.wave >= 2:
            kinds.append(EnemyKind.TANK)
        if self.wave >= 3:
            kinds.append(EnemyKind.SNIPER)
        kind = random.choice(kinds)
        x = random.uniform(40, WIDTH - 40)
        if kind == EnemyKind.SCOUT:
            e = Enemy(kind, x, -30, 2 + self.wave // 3, 2 + self.wave // 3, 100, vy=90 + self.wave * 4)
        elif kind == EnemyKind.TANK:
            e = Enemy(kind, x, -40, 8 + self.wave, 8 + self.wave, 250, vy=55, radius=22)
        elif kind == EnemyKind.ZIGZAG:
            e = Enemy(kind, x, -30, 3 + self.wave // 2, 3 + self.wave // 2, 150, vy=100 + self.wave * 3)
        else:
            e = Enemy(kind, x, -30, 4 + self.wave // 2, 4 + self.wave // 2, 180, vy=70, radius=17)
        self.enemies.append(e)

    def explode(self, x: float, y: float, color: Tuple[int, int, int], n: int = 18) -> None:
        for _ in range(n):
            ang = random.uniform(0, math.tau)
            spd = random.uniform(40, 280)
            self.particles.append(
                Particle(
                    x,
                    y,
                    math.cos(ang) * spd,
                    math.sin(ang) * spd,
                    random.uniform(0.3, 0.9),
                    0.9,
                    color,
                    random.uniform(2, 5),
                )
            )
        self.shake = max(self.shake, 0.25)

    def drop_power(self, x: float, y: float) -> None:
        if random.random() > 0.28:
            return
        kind = random.choices(
            list(PowerKind),
            weights=[22, 22, 18, 20, 10],
            k=1,
        )[0]
        self.powers.append(PowerUp(kind, x, y))

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == State.PLAYING:
                        self.state = State.PAUSED
                    elif self.state == State.PAUSED:
                        self.state = State.PLAYING
                    elif self.state in (State.MENU, State.GAME_OVER, State.VICTORY):
                        return False
                if event.key == pygame.K_p and self.state in (State.PLAYING, State.PAUSED):
                    self.state = State.PAUSED if self.state == State.PLAYING else State.PLAYING
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self.state in (State.MENU, State.GAME_OVER, State.VICTORY):
                        self.reset()
        return True

    def update(self, dt: float) -> None:
        self.menu_pulse += dt
        boost = 1.0
        keys = pygame.key.get_pressed()
        if self.state == State.PLAYING and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            boost = 1.4
        self.stars.update(dt, boost)

        if self.state != State.PLAYING:
            return

        self.banner_t = max(0.0, self.banner_t - dt)
        self.shake = max(0.0, self.shake - dt)
        self.combo_timer = max(0.0, self.combo_timer - dt)
        if self.combo_timer <= 0:
            self.combo = 0

        # Player
        self.bullets.extend(self.player.update(dt, keys))

        # Spawning
        if not self.boss_alive and self.enemies_left > 0:
            self.spawn_cd -= dt
            if self.spawn_cd <= 0:
                self.spawn_enemy()
                self.enemies_left -= 1
                self.spawn_cd = max(0.25, 1.1 - self.wave * 0.05)

        # Enemies
        new_shots: List[Bullet] = []
        alive_enemies: List[Enemy] = []
        for e in self.enemies:
            new_shots.extend(e.update(dt, self.player.x))
            if e.y > HEIGHT + 60:
                if e.kind != EnemyKind.BOSS:
                    # leaked — mild penalty
                    self.combo = 0
                continue
            alive_enemies.append(e)
        self.enemies = alive_enemies
        self.bullets.extend(new_shots)

        # Bullets
        self.bullets = [b for b in self.bullets if b.update(dt)]

        # Powers
        self.powers = [p for p in self.powers if p.update(dt)]

        # Particles / floats
        self.particles = [p for p in self.particles if p.update(dt)]
        next_floats: List[FloatingText] = []
        for f in self.floats:
            f.life -= dt
            f.y -= 40 * dt
            if f.life > 0:
                next_floats.append(f)
        self.floats = next_floats

        self.resolve_collisions()

        # Wave clear
        if (
            not self.enemies
            and self.enemies_left <= 0
            and not self.boss_alive
            and self.state == State.PLAYING
        ):
            self.wave_timer += dt
            if self.wave_timer > 1.2:
                self.next_wave()
        elif self.boss_alive and not any(e.kind == EnemyKind.BOSS for e in self.enemies):
            self.boss_alive = False
            self.wave_timer = 0.5

    def resolve_collisions(self) -> None:
        # Player bullets vs enemies
        remaining_bullets: List[Bullet] = []
        for b in self.bullets:
            if not b.friendly:
                remaining_bullets.append(b)
                continue
            hit = False
            for e in self.enemies:
                if b.rect().colliderect(e.rect()):
                    hit = True
                    if e.hit(b.damage):
                        self.on_enemy_killed(e)
                    else:
                        self.explode(b.x, b.y, NEON_CYAN, 6)
                    break
            if not hit:
                remaining_bullets.append(b)
        self.bullets = remaining_bullets

        # Enemy bullets vs player
        remaining_bullets = []
        for b in self.bullets:
            if b.friendly:
                remaining_bullets.append(b)
                continue
            if b.rect().colliderect(self.player.rect()):
                dead = self.player.hurt()
                self.explode(b.x, b.y, NEON_RED, 12)
                self.shake = 0.35
                if dead:
                    self.game_over()
                continue
            remaining_bullets.append(b)
        self.bullets = remaining_bullets

        # Enemy body vs player
        for e in list(self.enemies):
            if e.rect().colliderect(self.player.rect()):
                if e.kind != EnemyKind.BOSS:
                    self.on_enemy_killed(e)
                dead = self.player.hurt()
                self.explode(self.player.x, self.player.y, NEON_MAGENTA, 20)
                if dead:
                    self.game_over()

        # Powerups
        remaining_powers: List[PowerUp] = []
        for p in self.powers:
            if p.rect().colliderect(self.player.rect()):
                msg = self.player.apply_power(p.kind)
                if p.kind == PowerKind.BOMB:
                    self.trigger_bomb()
                if msg:
                    self.floats.append(
                        FloatingText(self.player.x, self.player.y - 30, msg, POWER_COLORS[p.kind])
                    )
            else:
                remaining_powers.append(p)
        self.powers = remaining_powers

    def on_enemy_killed(self, enemy: Enemy) -> None:
        if enemy in self.enemies:
            self.enemies.remove(enemy)
        self.combo += 1
        self.combo_timer = 2.0
        points = int(enemy.score * (1 + self.combo * 0.15))
        self.score += points
        self.floats.append(
            FloatingText(enemy.x, enemy.y, f"+{points}", NEON_GOLD if self.combo > 3 else WHITE)
        )
        color = {
            EnemyKind.SCOUT: NEON_RED,
            EnemyKind.TANK: NEON_MAGENTA,
            EnemyKind.ZIGZAG: NEON_GOLD,
            EnemyKind.SNIPER: NEON_LIME,
            EnemyKind.BOSS: NEON_MAGENTA,
        }[enemy.kind]
        self.explode(enemy.x, enemy.y, color, 40 if enemy.kind == EnemyKind.BOSS else 16)
        self.drop_power(enemy.x, enemy.y)
        if enemy.kind == EnemyKind.BOSS:
            self.show_banner("BOSS DOWN")
            self.score += 1000

    def trigger_bomb(self) -> None:
        for e in list(self.enemies):
            if e.kind != EnemyKind.BOSS:
                self.on_enemy_killed(e)
            else:
                e.hit(25)
                self.explode(e.x, e.y, NEON_MAGENTA, 30)
        self.bullets = [b for b in self.bullets if b.friendly]
        self.shake = 0.5
        self.show_banner("NOVA BOMB")

    def game_over(self) -> None:
        self.state = State.GAME_OVER
        self.high_score = max(self.high_score, self.score)
        self.explode(self.player.x, self.player.y, NEON_CYAN, 50)

    def draw_hud(self, surf: pygame.Surface) -> None:
        draw_text(surf, f"SCORE {self.score:08d}", 22, WHITE, topleft=(16, 12))
        draw_text(surf, f"WAVE {self.wave}/12", 20, NEON_CYAN, topleft=(16, 40))
        if self.combo > 1:
            draw_text(surf, f"COMBO x{self.combo}", 20, NEON_GOLD, topleft=(16, 66))

        # HP
        for i in range(self.player.max_hp):
            col = NEON_LIME if i < self.player.hp else (40, 50, 70)
            pygame.draw.rect(surf, col, (WIDTH - 28 - i * 26, 16, 20, 12), border_radius=3)

        # Energy
        pygame.draw.rect(surf, (30, 40, 60), (WIDTH - 170, 40, 150, 8), border_radius=3)
        pygame.draw.rect(
            surf,
            NEON_BLUE,
            (WIDTH - 170, 40, int(150 * self.player.energy / 100), 8),
            border_radius=3,
        )

        buffs = []
        if self.player.rapid_t > 0:
            buffs.append(f"RAPID {self.player.rapid_t:.0f}s")
        if self.player.triple_t > 0:
            buffs.append(f"TRIPLE {self.player.triple_t:.0f}s")
        if self.player.shield_t > 0:
            buffs.append(f"SHIELD {self.player.shield_t:.0f}s")
        if buffs:
            draw_text(surf, " | ".join(buffs), 16, NEON_GOLD, topleft=(16, HEIGHT - 28))

        if self.banner_t > 0:
            alpha = clamp(self.banner_t, 0, 1)
            draw_text(
                surf,
                self.banner,
                42,
                tuple(int(clamp(c * alpha, 40, 255)) for c in NEON_MAGENTA),
                center=(WIDTH // 2, HEIGHT // 3),
            )

    def draw_menu(self, surf: pygame.Surface) -> None:
        pulse = 0.7 + 0.3 * abs(math.sin(self.menu_pulse * 2))
        title_col = tuple(int(c * pulse) for c in NEON_CYAN)
        draw_text(surf, "NEBULA STRIKE", 64, title_col, center=(WIDTH // 2, HEIGHT // 3))
        draw_text(
            surf,
            "from Moving Box → full spaceship war",
            20,
            DIM,
            center=(WIDTH // 2, HEIGHT // 3 + 50),
        )
        draw_text(
            surf,
            "WASD / Arrows move · SPACE fire · SHIFT boost · P pause",
            18,
            WHITE,
            center=(WIDTH // 2, HEIGHT // 2 + 20),
        )
        draw_text(
            surf,
            "Press ENTER to launch",
            28,
            NEON_GOLD if int(self.menu_pulse * 3) % 2 == 0 else WHITE,
            center=(WIDTH // 2, HEIGHT // 2 + 80),
        )
        if self.high_score:
            draw_text(
                surf,
                f"HIGH SCORE {self.high_score}",
                20,
                NEON_MAGENTA,
                center=(WIDTH // 2, HEIGHT - 60),
            )

    def draw_overlay(self, surf: pygame.Surface, title: str, subtitle: str) -> None:
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 10, 160))
        surf.blit(veil, (0, 0))
        draw_text(surf, title, 56, NEON_MAGENTA, center=(WIDTH // 2, HEIGHT // 2 - 40))
        draw_text(surf, subtitle, 24, WHITE, center=(WIDTH // 2, HEIGHT // 2 + 20))
        draw_text(
            surf,
            "ENTER to play again · ESC quit",
            18,
            DIM,
            center=(WIDTH // 2, HEIGHT // 2 + 70),
        )

    def draw(self) -> None:
        # Shake offset
        ox = oy = 0
        if self.shake > 0 and self.state == State.PLAYING:
            ox = int(random.uniform(-6, 6) * self.shake * 4)
            oy = int(random.uniform(-6, 6) * self.shake * 4)

        layer = pygame.Surface((WIDTH, HEIGHT))
        layer.fill(VOID)
        self.stars.draw(layer)

        # Soft nebula wash
        for i, col in enumerate([(20, 10, 40), (10, 20, 50), (5, 30, 35)]):
            pygame.draw.circle(
                layer,
                col,
                (int(WIDTH * (0.2 + i * 0.3)), int(HEIGHT * (0.3 + 0.2 * math.sin(self.menu_pulse + i)))),
                180,
            )

        for p in self.powers:
            p.draw(layer)
        for e in self.enemies:
            e.draw(layer)
        for b in self.bullets:
            b.draw(layer)
        if self.state in (State.PLAYING, State.PAUSED):
            self.player.draw(layer)
        for part in self.particles:
            part.draw(layer)
        for f in self.floats:
            draw_text(layer, f.text, 18, f.color, center=(int(f.x), int(f.y)))

        if self.state in (State.PLAYING, State.PAUSED):
            self.draw_hud(layer)
        if self.state == State.MENU:
            self.draw_menu(layer)
        elif self.state == State.PAUSED:
            self.draw_overlay(layer, "PAUSED", "P to resume")
        elif self.state == State.GAME_OVER:
            self.draw_overlay(layer, "SHIP DOWN", f"Score {self.score}")
        elif self.state == State.VICTORY:
            self.draw_overlay(layer, "SECTOR CLEARED", f"Score {self.score}")

        self.screen.fill(VOID)
        self.screen.blit(layer, (ox, oy))
        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            running = self.handle_events()
            self.update(dt)
            self.draw()


def main() -> None:
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game(screen=screen, clock=clock)
    game.run()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
