"""OS-level hotkeys via RegisterHotKey (not a low-level keyboard hook).

WH_KEYBOARD_LL hooks (pynput GlobalHotKeys) get silently dropped by Windows when
the callback overruns LowLevelHooksTimeout. RegisterHotKey posts WM_HOTKEY to a
message loop, so it cannot be starved by click load. MOD_NOREPEAT stops auto-
repeat from double-toggling. Widget updates always cross back through root.after.
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes
import threading

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_NOREPEAT = 0x4000
WM_HOTKEY = 0x0312

VK_E = 0x45


class HotkeyBridge:
    def __init__(self, root, on_fire, on_status):
        self.root = root
        self.on_fire = on_fire
        self.on_status = on_status
        self.combos = []

    def add(self, label, mods, vk):
        self.combos.append((label, mods, vk))

    def start(self):
        threading.Thread(target=self._pump, daemon=True, name="hotkey-pump").start()

    def _pump(self):
        user32 = ctypes.windll.user32
        got, lost = [], []
        for ident, (label, mods, vk) in enumerate(self.combos, start=1):
            if user32.RegisterHotKey(None, ident, mods | MOD_NOREPEAT, vk):
                got.append(label)
            else:
                lost.append(label)
        self._say(got, lost)
        if not got:
            return
        msg = ctypes.wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            if msg.message == WM_HOTKEY:
                self.root.after(0, self.on_fire)

    def _say(self, got, lost):
        if not got:
            text = "Hotkey blocked by another app — use the button: " + " / ".join(lost)
            colour = "#C0170B"
        elif lost:
            text = "Ready: " + " · ".join(got) + "  |  blocked: " + " / ".join(lost)
            colour = "#F6A30A"
        else:
            text = "Ready: " + " · ".join(got)
            colour = "#FDE861"
        self.root.after(0, lambda: self.on_status(text, colour))
