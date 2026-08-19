---
created: 2026-08-19T04:10:00.000Z
title: Every stored timestamp is offset by the device UTC offset — the CLOCK block's epoch anchor is timezone-naive
area: general
severity: minor
files:
  - tools/build_state_engine.py
  - src/PROSOCHE-Dumb.xml
---

## Problem

**Device-measured, 2026-08-18, Core `873fa3db…`.** Every epoch PROSOCHĒ writes to `state.json`
is `true_epoch + the device's UTC offset` — `+10 h` on the paired iPhone (AEST).

The mechanism is visible in the artifact's hand-authored CLOCK block
(`src/PROSOCHE-Dumb.xml`, actions 11–16):

```
Date · WFDateActionMode = "Specified Date" · WFDateActionDate = "1970-01-01 00:00:00"  -> Epoch Anchor
Date · WFDateActionMode = "Current Date"                                               -> Now Date
Get Time Between Dates · Seconds                                                       -> Now Epoch
```

`"1970-01-01 00:00:00"` is parsed in the **device's local time zone**, so the anchor sits
`offset` seconds before the true Unix epoch and every `Now Epoch` inherits that shift.

**How it was caught, which is also the strongest evidence:** `last_close_at` in a recovered
`state.json` read `1787081517`, while the file's own OS-level mtime was `1787045519` — a
difference of `35998 s ≈ +10 h`. Rendering the stored value as **UTC** reproduces the local wall
clock of the write to the second.

## Why the severity is `minor` and not lower

**Harmless where it is used most.** Every stored timestamp shares the same offset, so all
*differences* are exactly right — session duration, elapsed-since, cooldown comparison, exit
return-time samples. That is why 13 device sessions all recompute
`duration_seconds == ended_at - started_at` exactly.

**`behavioural_day` is unaffected.** It is derived from `Now Date` via Adjust Date −4 h and
Format Date, never from `Now Epoch`, so the day key is genuinely local and correct.

**The real failure mode is a change of offset while state is live** — a DST transition, or the
user travelling. The paired device's zone observes DST (AEST +10 → AEDT +11). Across that
boundary the anchor moves an hour while already-stored timestamps do not, so:

- a session opened before and closed after the transition records a `duration_seconds` wrong by
  `3600`, silently and plausibly;
- a `cooldown_until` written before it is evaluated an hour early or late;
- an exit's return-time sample — the field §9.1 calls load-bearing — is wrong by the same hour,
  and feeds exit learning.

**Secondary but real:** it makes `state.json` actively misleading to anyone reading it as a true
epoch, which is how this was found.

## Solution

Anchor the epoch in UTC rather than local time, or derive `Now Epoch` from a UTC-formatted
timestamp. One-action change in the CLOCK block; needs no device to implement.

**Verify by measurement, not inspection:** after the change, compare a freshly written
`last_close_at` against the file's mtime — they should agree to within a second or two. That
check is exactly what surfaced the defect and it costs nothing to keep.

Consider a build guard asserting the anchor string carries an explicit UTC marker, so a future
edit cannot silently reintroduce a local-parsed anchor.

## Evidence

`.planning/debug/device-state/README.md`, finding **F-5**. State files preserved beside it.
