"""GOLDAUTOCLICKER — Python rebuild of the gold WeAreDevs Autoclicker UI.

Same layout and palette as the patched Tauri exe. Clicking runs on a dedicated
thread with Event start/stop and perf_counter scheduling so CPS stays on target
and the UI never freezes. CTRL+E uses RegisterHotKey once at startup (no React
useEffect race).
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes
import json
import sys
import threading
import time
import winsound
from pathlib import Path

import tkinter as tk

from clickhotkey import HotkeyBridge, MOD_CONTROL, VK_E

# --- palette (from patched index CSS / JS) ---
GOLD = "#FCBC24"
GOLD_BG = "#FCD241"
GOLD_SOFT = "#FDE861"
GOLD_BTN_ON = "#FCE96B"
INK = "#0B0905"
RED = "#C0170B"

DEFAULT_CPS = 10
MAX_CPS = 1500
SETTINGS_PATH = Path(__file__).with_name("settings.json")

# --- SendInput left click ---
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
ULONG_PTR = ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (
        ("dx", ctypes.wintypes.LONG),
        ("dy", ctypes.wintypes.LONG),
        ("mouseData", ctypes.wintypes.DWORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    )


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("mi", MOUSEINPUT),)

    _anonymous_ = ("u",)
    _fields_ = (("type", ctypes.wintypes.DWORD), ("u", _INPUT))


_SendInput = ctypes.windll.user32.SendInput
_SendInput.argtypes = (ctypes.wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
_SendInput.restype = ctypes.wintypes.UINT


def click_left() -> None:
    bundle = (INPUT * 2)()
    bundle[0].type = INPUT_MOUSE
    bundle[0].mi.dwFlags = MOUSEEVENTF_LEFTDOWN
    bundle[1].type = INPUT_MOUSE
    bundle[1].mi.dwFlags = MOUSEEVENTF_LEFTUP
    _SendInput(2, bundle, ctypes.sizeof(INPUT))


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def elevate_or_exit() -> None:
    if is_admin():
        return
    script = str(Path(__file__).resolve())
    params = f'"{script}"'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)


def load_cps() -> int:
    try:
        data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        cps = int(data.get("clickRate", DEFAULT_CPS))
        return max(0, min(MAX_CPS, cps))
    except Exception:
        return DEFAULT_CPS


def save_cps(cps: int) -> None:
    try:
        SETTINGS_PATH.write_text(
            json.dumps({"clickRate": int(cps), "alwaysontop": False}, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


class GoldAutoclicker:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("GOLDAUTOCLICKER")
        self.root.geometry("420x280")
        self.root.resizable(False, False)
        self.root.configure(bg=GOLD_BG)
        self.root.attributes("-topmost", False)

        self.run = threading.Event()
        self.cps = float(load_cps())
        self.click_count = 0
        self._cps_lock = threading.Lock()
        self._drag_x = 0
        self._drag_y = 0

        self._build_chrome()
        self._build_body()
        self._build_mini()

        threading.Thread(
            target=self._click_loop, daemon=True, name="click-loop"
        ).start()

        keys = HotkeyBridge(self.root, self.flip, self._show_keys)
        keys.add("CTRL+E", MOD_CONTROL, VK_E)
        keys.start()

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind("<Escape>", lambda _e: self.close())

    # ----- UI (1:1 with SettingsContainer / WindowTopBar / miniinfo) -----

    def _build_chrome(self) -> None:
        bar = tk.Frame(self.root, bg=GOLD, height=28)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        title = tk.Label(
            bar,
            text="GOLDAUTOCLICKER",
            bg=GOLD,
            fg=INK,
            font=("Segoe UI", 10),
            anchor="w",
            padx=4,
        )
        title.pack(side="left", fill="both", expand=True)

        close = tk.Label(
            bar,
            text="X",
            bg=GOLD,
            fg=INK,
            font=("Segoe UI", 10),
            padx=10,
            cursor="hand2",
        )
        close.pack(side="right")
        close.bind("<Button-1>", lambda _e: self.close())
        close.bind("<Enter>", lambda _e: close.configure(bg=RED, fg=GOLD_SOFT))
        close.bind("<Leave>", lambda _e: close.configure(bg=GOLD, fg=INK))

        for w in (bar, title):
            w.bind("<Button-1>", self._start_drag)
            w.bind("<B1-Motion>", self._on_drag)

        try:
            self.root.overrideredirect(True)
        except Exception:
            pass

    def _build_body(self) -> None:
        body = tk.Frame(self.root, bg=GOLD_BG)
        body.pack(fill="both", expand=True, pady=(18, 28))

        self.hint = tk.Label(
            body,
            text="Press ctrl + e to enable",
            bg=GOLD_BG,
            fg=INK,
            font=("Segoe UI", 14),
        )
        self.hint.pack(pady=(0, 10))

        self.btn = tk.Button(
            body,
            text="Paused\n",
            bg=INK,
            fg=GOLD_SOFT,
            activebackground=INK,
            activeforeground=GOLD_SOFT,
            disabledforeground=GOLD_SOFT,
            font=("Segoe UI", 12),
            relief="solid",
            bd=1,
            highlightthickness=0,
            width=14,
            height=2,
            cursor="hand2",
            command=self.flip,
        )
        self.btn.pack(pady=6)

        row = tk.Frame(body, bg=GOLD_BG)
        row.pack(pady=10)
        tk.Label(
            row,
            text="Clicks per second: ",
            bg=GOLD_BG,
            fg=INK,
            font=("Segoe UI", 11),
        ).pack(side="left")
        self.cps_var = tk.StringVar(value=str(int(self.cps)))
        self.cps_entry = tk.Entry(
            row,
            textvariable=self.cps_var,
            font=("Segoe UI", 11),
            width=6,
            justify="center",
            bg=GOLD_BTN_ON,
            fg=INK,
            insertbackground=INK,
            relief="solid",
            bd=1,
        )
        self.cps_entry.pack(side="left")
        self.cps_var.trace_add("write", self._on_cps_edit)

        self.count_lbl = tk.Label(
            body,
            text="Clicks: 0",
            bg=GOLD_BG,
            fg=INK,
            font=("Segoe UI", 11),
        )
        self.count_lbl.pack(pady=4)

    def _build_mini(self) -> None:
        self.mini = tk.Label(
            self.root,
            text="",
            bg=INK,
            fg=GOLD_SOFT,
            font=("Segoe UI", 9),
            anchor="center",
        )
        self.mini.place(relx=0, rely=1.0, anchor="sw", relwidth=1.0)

    def _start_drag(self, event) -> None:
        self._drag_x = event.x_root - self.root.winfo_x()
        self._drag_y = event.y_root - self.root.winfo_y()

    def _on_drag(self, event) -> None:
        x = event.x_root - self._drag_x
        y = event.y_root - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    def _show_keys(self, text: str, colour: str) -> None:
        self.mini.configure(text=text, fg=colour)

    def _on_cps_edit(self, *_args) -> None:
        raw = self.cps_var.get().strip()
        if raw == "":
            return
        try:
            value = int(raw)
        except ValueError:
            return
        value = max(0, min(MAX_CPS, value))
        with self._cps_lock:
            self.cps = float(value) if value > 0 else 0.0
        save_cps(value)
        # grow entry width like the original ch-based css
        self.cps_entry.configure(width=max(4, len(raw) + 2))

    def _read_cps(self) -> float:
        with self._cps_lock:
            return self.cps if self.cps > 0 else 0.0

    def flip(self) -> None:
        """Single toggle path for button + CTRL+E (Tk thread only)."""
        if self.run.is_set():
            self.run.clear()
            self.btn.configure(
                text="Paused\n",
                bg=INK,
                fg=GOLD_SOFT,
                activebackground=INK,
                activeforeground=GOLD_SOFT,
            )
            self.hint.configure(text="Press ctrl + e to enable")
            self.root.attributes("-topmost", False)
        else:
            self.click_count = 0
            self._paint_count()
            self.btn.configure(
                text="Clicking\n",
                bg=GOLD_BTN_ON,
                fg=INK,
                activebackground=GOLD_BTN_ON,
                activeforeground=INK,
            )
            self.hint.configure(text="Press ctrl + e to disable")
            self.root.attributes("-topmost", True)
            self.run.set()
        try:
            winsound.MessageBeep(winsound.MB_OK)
        except Exception:
            pass

    def _paint_count(self) -> None:
        self.count_lbl.configure(text=f"Clicks: {self.click_count}")

    def _sleep_until(self, deadline: float) -> bool:
        """Sleep until deadline while still running. Returns False if stopped."""
        while self.run.is_set():
            left = deadline - time.perf_counter()
            if left <= 0:
                return True
            if left > 0.002:
                time.sleep(min(0.01, left - 0.001))
            else:
                while self.run.is_set() and time.perf_counter() < deadline:
                    pass
                return self.run.is_set()
        return False

    def _click_loop(self) -> None:
        while True:
            self.run.wait()
            if not self.run.is_set():
                continue
            next_t = time.perf_counter()
            while self.run.is_set():
                cps = self._read_cps()
                if cps <= 0:
                    # 0 CPS = idle but still "Clicking" until toggled off
                    time.sleep(0.05)
                    next_t = time.perf_counter()
                    continue
                interval = 1.0 / cps
                click_left()
                self.click_count += 1
                if self.click_count % 10 == 0:
                    self.root.after(0, self._paint_count)
                next_t += interval
                now = time.perf_counter()
                if now - next_t > interval:
                    # fell behind — resync so we don't burst to catch up
                    next_t = now
                if not self._sleep_until(next_t):
                    break

    def close(self) -> None:
        self.run.clear()
        save_cps(int(self._read_cps()) if self._read_cps() > 0 else int(load_cps()))
        self.root.destroy()


def main() -> None:
    elevate_or_exit()
    root = tk.Tk()
    GoldAutoclicker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
