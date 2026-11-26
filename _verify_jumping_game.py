#!/usr/bin/env python3
"""Verify My First Jumping Game – 3G26 (Neon Sky Docks)."""
import sys
import traceback

PASS = FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


TEACHER_BITS = (
    "encrypted-tbn0.gstatic.com",
    "ANd9GcRIxXcmjljDf1HN-kUkmPdzJU8cdcOrfRr_hibwaAFmzA",
)


def main():
    print("=== Constants & anti-copy ===")
    import my_first_jumping_game_3g26 as g

    check("WINDOW 400x300", g.WINDOW_W == 400 and g.WINDOW_H == 300)
    check("Title is 3G26", g.WINDOW_TITLE == "My First Jumping Game – 3G26", repr(g.WINDOW_TITLE))
    check("10+ layouts", len(g.LAYOUTS) >= 10, str(len(g.LAYOUTS)))
    check("Game/Player/Platform", all(hasattr(g, n) for n in ("Game", "Player", "Platform")))

    url_attrs = [getattr(g, n) for n in dir(g) if n.startswith("URL_")]
    blob = "\n".join(url_attrs)
    check("has 5+ image URLs", len(url_attrs) >= 5, str(len(url_attrs)))
    for bit in TEACHER_BITS:
        check(f"no teacher URL bit ({bit[:24]}…)", bit not in blob)
    check("forbidden list present", hasattr(g, "_FORBIDDEN_URL_BITS"))

    print("\n=== Asset load (real open-web URLs) ===")
    assets = g.load_all_assets()
    check("bg loaded", assets["bg"].size == (400, 300), str(assets["bg"].size))
    check("player stand right", assets["player_stand_r"] is not None)
    check("player stand left (FLIP)", assets["player_stand_l"] is not None)
    check("player run pose", assets["player_run_r"] is not None)
    check("platform tile", assets["platform_tile"] is not None)
    check("gold prop", assets["gold"] is not None)
    check("beacon prop", assets["beacon"] is not None)
    check("coin prop", assets.get("coin") is not None)
    # Flip integrity
    from PIL import Image
    flipped = assets["player_stand_r"].transpose(Image.FLIP_LEFT_RIGHT)
    check(
        "FLIP_LEFT_RIGHT matches left sprite",
        list(flipped.getdata()) == list(assets["player_stand_l"].getdata()),
    )

    print("\n=== GUI school steps ===")
    import tkinter as tk

    root = tk.Tk()
    game = g.Game(root)
    root.update()

    check("window title", root.title() == g.WINDOW_TITLE, root.title())
    check("canvas 400x300", int(game.canvas["width"]) == 400 and int(game.canvas["height"]) == 300)
    check("start state", game.state == "start")
    check("Start Game button", hasattr(game, "start_btn") and game.start_btn.winfo_exists())

    game._start_game()
    root.update()
    check("play state", game.state == "play")
    check("start UI hidden", not hasattr(game, "start_btn") or not game.start_btn.winfo_exists())
    check("player exists", game.player is not None)
    check("platforms >= 3", len(game.platforms) >= 3)

    print("\n=== Movement / facing / dash ===")
    p = game.player
    x0 = p.x
    game.keys.add("Right")
    p.apply_input(game.keys)
    p.physics(game.platforms)
    check("moves right", p.x > x0)
    check("faces right", p.facing_right)
    game.keys.clear()
    game.keys.add("Left")
    p.apply_input(game.keys)
    for _ in range(4):
        p.physics(game.platforms)
    check("faces left", not p.facing_right)
    game.keys.clear()

    p.on_ground = True
    check("jump works", p.jump())
    check("no infinite mid-air jump", p.jump() is False)
    p.on_ground = False
    p.dash_charges = 1
    check("air dash works", p.dash())
    check("dash consumes charge", p.dash_charges == 0)
    check("no spam dash", p.dash() is False)

    print("\n=== Platform landing / bounds / fall ===")
    plat = game.platforms[0]
    p.x = plat.x + 8
    p.y = plat.y - p.h - 25
    p.vy = 6
    p.on_ground = False
    for _ in range(40):
        p.physics(game.platforms)
        if p.on_ground:
            break
    check("lands", p.on_ground)
    check("no sink", abs((p.y + p.h) - plat.y) < 2, f"feet={p.y+p.h} plat={plat.y}")

    p.x = -40
    p.physics(game.platforms)
    check("left clamp", p.x >= 0)
    p.x = 999
    p.physics(game.platforms)
    check("right clamp", p.x + p.w <= g.WINDOW_W + 0.01)

    game._start_game()
    root.update()
    game.player.y = g.WINDOW_H + 20
    game._show_game_over(won=False)
    root.update()
    check("gameover", game.state == "gameover")
    found = False
    for item in game.ui_ids:
        try:
            if game.canvas.type(item) == "text" and game.canvas.itemcget(item, "text") == "GAME OVER":
                found = True
        except tk.TclError:
            pass
    check("GAME OVER text", found)
    check("Restart button", hasattr(game, "restart_btn") and game.restart_btn.winfo_exists())

    old_score = game.score = 99
    game._restart()
    root.update()
    check("restart → play", game.state == "play")
    check("score reset", game.score == 0, str(game.score))
    check("player on screen", game.player.y < g.WINDOW_H)

    print("\n=== Upgrades present ===")
    check("Particle", hasattr(g, "Particle"))
    check("dash signature", hasattr(game.player, "dash"))
    check("gold power-up hook", hasattr(game, "gold_id"))
    check("beacon goal", hasattr(game, "beacon_id"))

    root.destroy()
    print(f"\n=== RESULT: {PASS} passed, {FAIL} failed ===")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
