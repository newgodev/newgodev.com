# GOLDAUTOCLICKER (Python)

1:1 Python rebuild of the gold WeAreDevs Autoclicker UI (`GOLDAUTOCLICKER.exe`).

## Why this exists

The Tauri exe could stop accepting **CTRL+E** because the hotkey `useEffect` re-registered on every toggle/CPS keystroke and raced async register/unregister. Clicking then continued with no way to stop.

This rebuild:

- Registers **CTRL+E** once via `RegisterHotKey` (no hook timeout, no React race)
- Clicks on a **dedicated thread** with `threading.Event` start/stop
- Schedules CPS with `perf_counter` (sleep + short spin) so rate stays on target
- Keeps the gold UI: title bar, enable hint, Paused/Clicking button, CPS field, click count, mini status bar

## Run (Windows)

```bat
python gold_autoclicker.py
```

Accept the UAC prompt (admin is required so clicks reach games).

No pip packages — only stdlib (`tkinter`, `ctypes`).

## Controls

| Action | How |
|--------|-----|
| Start / stop | **CTRL+E** or the Paused/Clicking button |
| CPS | Number field (0–1500), saved to `settings.json` |
| Close | Title-bar **X** or Esc |

## Files

- `gold_autoclicker.py` — UI + click loop
- `clickhotkey.py` — `RegisterHotKey` bridge
- `settings.json` — created on first CPS edit (`clickRate`)
