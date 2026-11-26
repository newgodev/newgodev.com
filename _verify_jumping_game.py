#!/usr/bin/env python3
"""Automated verification for My First Jumping Game – 3R99 (PDF + video)."""
import sys
import traceback

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


def main():
    print("=== Import & constants ===")
    import my_first_jumping_game_3r99 as g

    check("WINDOW_W == 400", g.WINDOW_W == 400)
    check("WINDOW_H == 300", g.WINDOW_H == 300)
    check(
        "Title exact",
        g.WINDOW_TITLE == "My First Jumping Game – 3R99",
        repr(g.WINDOW_TITLE),
    )
    check("BG_URL present", "encrypted-tbn0.gstatic.com" in g.BG_URL)
    check("LAYOUTS >= 2", len(g.LAYOUTS) >= 2)
    check("Game/Player/Platform classes", all(
        hasattr(g, n) for n in ("Game", "Player", "Platform")
    ))

    print("\n=== Background loader (URL or fallback) ===")
    bg = g.load_background(400, 300)
    check("bg size 400x300", bg.size == (400, 300), str(bg.size))
    check("bg mode RGB", bg.mode in ("RGB", "RGBA"))

    print("\n=== Sprite flip (PDF Step 3) ===")
    from PIL import Image
    right = g.make_wizard_sprite(True)
    left = g.make_wizard_sprite(False)
    check("sprites same size", right.size == left.size)
    # Flipped right should match left (within drawing tolerance)
    flipped = right.transpose(Image.FLIP_LEFT_RIGHT)
    check("FLIP_LEFT_RIGHT equals left sprite", list(flipped.getdata()) == list(left.getdata()))

    print("\n=== Launch GUI under virtual display ===")
    import tkinter as tk

    root = tk.Tk()
    root.update_idletasks()
    game = g.Game(root)
    root.update()
    root.update_idletasks()

    check("root title exact", root.title() == g.WINDOW_TITLE, root.title())
    # Geometry may include chrome; canvas must be exact
    check("canvas width 400", int(game.canvas["width"]) == 400)
    check("canvas height 300", int(game.canvas["height"]) == 300)
    check("state == start", game.state == "start")
    check("Start Game button exists", hasattr(game, "start_btn") and game.start_btn.winfo_exists())
    check("start UI items present", len(game.ui_ids) > 0)

    print("\n=== Start Game hides title/button (PDF Step 1) ===")
    game._start_game()
    root.update()
    check("state == play", game.state == "play")
    check("start button destroyed", not hasattr(game, "start_btn") or not game.start_btn.winfo_exists())
    check("player spawned", game.player is not None)
    check("platforms spawned", len(game.platforms) >= 3)
    check("ui cleared after start", len(game.ui_ids) == 0)

    print("\n=== Movement + facing (PDF Steps 2–3) ===")
    p = game.player
    start_x = p.x
    game.keys.add("Right")
    p.apply_input(game.keys)
    p.physics(game.platforms)
    root.update()
    check("moves right", p.x > start_x, f"x={p.x}")
    check("faces right", p.facing_right is True)
    game.keys.clear()
    game.keys.add("Left")
    p.apply_input(game.keys)
    for _ in range(5):
        p.physics(game.platforms)
    root.update()
    check("faces left after Left", p.facing_right is False)
    game.keys.clear()

    print("\n=== Jump + no double-jump until power-up (PDF Step 4) ===")
    # Force grounded
    p.vy = 0
    p.on_ground = True
    check("jump from ground works", p.jump() is True)
    check("now airborne", p.on_ground is False)
    check("no accidental double jump", p.jump() is False)
    p.can_double_jump = True
    check("double jump when unlocked", p.jump() is True)

    print("\n=== Platform landing (no sink) ===")
    # Place above a known platform and fall onto it
    plat = game.platforms[0]
    p.x = plat.x + 10
    p.y = plat.y - p.h - 20
    p.vy = 5
    p.on_ground = False
    for _ in range(30):
        prev = p.on_ground
        p.physics(game.platforms)
        if p.on_ground:
            break
    check("lands on platform", p.on_ground is True)
    check("feet on top (no sink)", abs((p.y + p.h) - plat.y) < 1.5, f"feet={p.y+p.h} plat={plat.y}")

    print("\n=== Left/right boundaries (PDF Step 5) ===")
    p.x = -50
    p.vx = -5
    p.physics(game.platforms)
    check("clamped left >= 0", p.x >= 0, f"x={p.x}")
    p.x = 500
    p.vx = 5
    p.physics(game.platforms)
    check("clamped right", p.x + p.w <= g.WINDOW_W + 0.01, f"x={p.x}")

    print("\n=== Fall → GAME OVER + Restart (PDF Step 5) ===")
    # Re-enter play cleanly
    game._start_game()
    root.update()
    game.player.y = g.WINDOW_H + 20
    game.player.vy = 5
    # Drive one loop iteration of fall check
    game.state = "play"
    # Manually trigger the fall branch by running loop body logic:
    if game.player.y > g.WINDOW_H + 5:
        game._show_game_over(won=False)
    root.update()
    check("state gameover", game.state == "gameover")
    check("Restart Game button exists", hasattr(game, "restart_btn") and game.restart_btn.winfo_exists())
    # Find GAME OVER text on canvas
    found_go = False
    for item in game.ui_ids:
        try:
            if game.canvas.type(item) == "text":
                if game.canvas.itemcget(item, "text") == "GAME OVER":
                    found_go = True
        except tk.TclError:
            pass
    check("GAME OVER label visible", found_go)

    game._restart()
    root.update()
    check("restart → play", game.state == "play")
    check("player reset on screen", game.player.y < g.WINDOW_H)

    print("\n=== Win condition ===")
    top = g.LAYOUTS[game.layout_index][-1]
    game.player.x = top[0] + 10
    game.player.y = top[1] - game.player.h
    game.player.vy = 0
    game.player.on_ground = True
    # Simulate win check once
    feet_y = game.player.y + game.player.h
    on_top = (
        abs(feet_y - top[1]) < 3
        and game.player.x + game.player.w > top[0] + 4
        and game.player.x < top[0] + top[2] - 4
    )
    check("win detect on top platform", on_top)
    if on_top:
        game._show_game_over(won=True)
    root.update()
    check("state win", game.state == "win")

    print("\n=== Score / high score / particles / power-up upgrades ===")
    check("score attribute", hasattr(game, "score"))
    check("high_score attribute", hasattr(game, "high_score"))
    check("Particle class", hasattr(g, "Particle"))
    check("star power-up photo", game.star_photo is not None)

    root.destroy()
    print(f"\n=== RESULT: {PASS} passed, {FAIL} failed ===")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
