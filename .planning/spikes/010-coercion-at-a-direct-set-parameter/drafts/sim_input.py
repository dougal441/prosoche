#!/usr/bin/env python3
"""Synthesized tap and scroll against the booted iOS Simulator, from the build Mac.

THIS IS THE INSTRUMENT THAT CLOSED RESEARCH ASSUMPTION A5, so it is recorded rather than
thrown away.  `16-RESEARCH.md` Finding 3 proved the Shortcuts import SHEET renders for a
signed artifact delivered by `xcrun simctl openurl "file://…"`, and left one step open:
"completing the import requires one synthesized tap on Add Shortcut."  Spike 007 had
recorded, and the skill repeated as a standing constraint, that the simulator cannot
import a signed `.shortcut` through any channel.  Both are now measured to be wrong, and
this file is how.

WHAT DID NOT WORK, so nobody re-walks these:

  * `mcp__Claude_Code_iOS_Simulator__control` — the tap tool CLAUDE.md §9 names is not
    exposed to a subagent with a restricted tool list, so it was unavailable here.
  * `osascript` / AppleScript System Events — "osascript is not allowed assistive
    access. (-1728)".
  * `idb`, `cliclick` — not installed on this Mac.
  * `xcrun simctl` — has no tap/touch verb at all; `simctl ui` is appearance only.
  * `shortcuts://import-shortcut?url=file://…&silent=true` — "Import Failed. The
    shortcut URL provided was invalid."  Same rejection spike 007 measured for an http
    URL; the scheme wants an iCloud link and `silent=true` does not bypass that, because
    the URL is rejected before the flag is ever consulted.

WHAT WORKED: post the click straight into the window server with Quartz `CGEventPost`.
That path needed no Accessibility grant on this Mac, which is exactly why it succeeded
where AppleScript did not.

ONE PRECONDITION THAT IS EASY TO MISS.  A simulator booted by `simctl` alone has NO
on-screen window — `CGWindowListCopyWindowInfo` returns nothing for it, and a click has
nothing to land on.  Run `open -a Simulator` first and let the window appear.

COORDINATES ARE FRACTIONS, NEVER PIXELS.  Read the target's position off a
`simctl io … screenshot` as a fraction of the device screen, then map it through the
window rect measured at run time.  A hardcoded pixel constant breaks the moment the
window moves, the display scale changes, or the device type differs -- and it breaks
silently, by clicking the wrong thing.

Usage:
    python3 sim_input.py tap    <fx> <fy>          # fractions of the device screen, 0..1
    python3 sim_input.py scroll <lines>            # negative scrolls the content up
"""

import sys
import time

import Quartz


def simulator_window():
    """The Simulator window rect, measured now.  Never cached, never assumed."""
    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    for window in windows:
        if "Simulator" in str(window.get("kCGWindowOwnerName")):
            bounds = dict(window.get("kCGWindowBounds"))
            return bounds["X"], bounds["Y"], bounds["Width"], bounds["Height"]
    raise SystemExit(
        "no on-screen Simulator window. A simctl-booted simulator is headless -- "
        "run `open -a Simulator` first and wait for the window to appear.")


def tap(fx, fy):
    wx, wy, ww, wh = simulator_window()
    x, y = wx + fx * ww, wy + fy * wh
    for kind in (Quartz.kCGEventMouseMoved,
                 Quartz.kCGEventLeftMouseDown,
                 Quartz.kCGEventLeftMouseUp):
        Quartz.CGEventPost(
            Quartz.kCGHIDEventTap,
            Quartz.CGEventCreateMouseEvent(None, kind, (x, y), Quartz.kCGMouseButtonLeft))
        time.sleep(0.12)
    print(f"tapped ({fx:.3f}, {fy:.3f}) -> screen ({x:.1f}, {y:.1f})")


def scroll(lines, fx=0.5, fy=0.5):
    """Scroll requires the pointer to be OVER the simulator window first."""
    wx, wy, ww, wh = simulator_window()
    x, y = wx + fx * ww, wy + fy * wh
    Quartz.CGEventPost(
        Quartz.kCGHIDEventTap,
        Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y),
                                       Quartz.kCGMouseButtonLeft))
    time.sleep(0.1)
    step = 3 if lines > 0 else -3
    for _ in range(abs(int(lines)) // 3 or 1):
        Quartz.CGEventPost(
            Quartz.kCGHIDEventTap,
            Quartz.CGEventCreateScrollWheelEvent(None, Quartz.kCGScrollEventUnitLine, 1, step))
        time.sleep(0.05)
    print(f"scrolled {lines} lines at ({x:.1f}, {y:.1f})")


def swipe(fx, fy_from, fy_to, steps=14, settle=0.012):
    """A drag, which the Simulator translates into a touch swipe.

    Scroll-wheel events do NOT scroll the simulated device -- measured this session, the
    Shortcuts action list did not move at all under `kCGScrollEventUnitLine`.  A drag
    does.

    KEEP IT FAST AND KEEP IT NEAR AN EDGE.  In the Shortcuts editor a SLOW drag starting
    on an action card picks the card up and REORDERS the shortcut, which would silently
    corrupt the very artifact under observation.  Short per-step sleeps and an x well
    left of the card body keep it a scroll.
    """
    wx, wy, ww, wh = simulator_window()
    x = wx + fx * ww
    y0, y1 = wy + fy_from * wh, wy + fy_to * wh
    post = lambda kind, py: Quartz.CGEventPost(
        Quartz.kCGHIDEventTap,
        Quartz.CGEventCreateMouseEvent(None, kind, (x, py), Quartz.kCGMouseButtonLeft))
    post(Quartz.kCGEventMouseMoved, y0)
    time.sleep(0.05)
    post(Quartz.kCGEventLeftMouseDown, y0)
    for i in range(1, steps + 1):
        post(Quartz.kCGEventLeftMouseDragged, y0 + (y1 - y0) * i / steps)
        time.sleep(settle)
    post(Quartz.kCGEventLeftMouseUp, y1)
    print(f"swiped x={fx:.3f} from y={fy_from:.3f} to y={fy_to:.3f}")


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "tap":
        tap(float(sys.argv[2]), float(sys.argv[3]))
    elif len(sys.argv) >= 3 and sys.argv[1] == "scroll":
        scroll(float(sys.argv[2]),
               *(float(a) for a in sys.argv[3:5]) if len(sys.argv) >= 5 else ())
    elif len(sys.argv) >= 5 and sys.argv[1] == "swipe":
        swipe(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
    else:
        raise SystemExit(__doc__)
