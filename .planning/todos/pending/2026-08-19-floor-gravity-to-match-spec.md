---
created: 2026-08-19T02:57:30.109Z
title: Gravity is never floored — escalation is off-spec on all three descent profiles
area: general
severity: major
files:
  - tools/build_state_engine.py:1705
---

> **COVENANT OVERHAUL (2026-08-19):** Owned by Phase 17, folded into the covenant substrate; land before any Pressure-accumulation run. Profile names read Paradise / Purgatory / Inferno since BD-06-A1.


## Problem

Canonical strategy §10.3 specifies:

    gravity = floor(opens_today / 6)   capped at 5

`open_pipeline()` divides, compares the raw quotient against the cap, and stores the **unfloored**
value (`tools/build_state_engine.py:1705-1707` — anchor on the `Gravity Raw` symbol, the line
numbers move on every edit):

    math("Opens Today Next", variable("Opens Per Gravity"), "Gravity Raw", "÷")
    if Gravity Raw > Gravity Cap  -> set gravity = Gravity Cap
    otherwise                     -> set gravity = Gravity Raw      # never floored

**Every other division in the same file is floored** through the `round_down()` helper — decay
intervals, exit-stat averages, the exploration threshold. Gravity is the single exception, which is
what makes this look like an omission rather than a decision.

**It is visible in the first device reading the product ever produced.** Pressure `0.166666666666667`
on a first-ever open is exactly 1 ÷ 6, where spec says Gravity should be 0 and Pressure should be 0.

**Consequence.** `pressure = heat + gravity` is compared against the ascending integer threshold
lists in Config (`thresholds.<profile>.<n>`). Every fractional carry pushes Pressure over a
threshold earlier than the profile intends, so **Paradise, Limbo and Inferno are all currently
mistuned** — and mistuned by an amount that grows with `opens_today`, not by a constant.

**Why it matters more now than when it was first recorded.** The stated next high-value step is to
accumulate Pressure to Inferno's Circle-1 entry in order to unlock the ~30 tests gated behind
reaching the intervention surface. Doing that against unfloored Gravity means the threshold is
crossed on a number the spec says should be lower — so any escalation timing observed in that
session measures the defect, not the design. This should land **before** the next Pressure-
accumulation run, not after.

## Solution

Route: **`/gsd-quick`, or fold into the next phase that touches `open_pipeline()`.** It needs no
investigation — the helper already exists and is used correctly five lines above.

1. Wrap `Gravity Raw` in `round_down()` before the cap comparison, matching the decay-interval
   pattern in the same function:

       math(...,"Gravity Raw","÷") + round_down("Gravity Raw", "Gravity Floored")

   then compare and store `Gravity Floored`. Keep the cap comparison after the floor, not before.
2. **Check the cap comparison still reads correctly** against a now-integer operand — this project
   has been bitten repeatedly by numeric conditionals on text-typed operands (axis 6), and changing
   what produces the operand is exactly when that class reappears. The coercion aggrandizement rule
   applies to the new variable.
3. **Add it to the numeric-audit guard** so a later refactor cannot silently drop the floor again.
4. **Re-derive the profile threshold tables afterwards, or explicitly confirm they still hold.**
   The Config thresholds were authored against a spec-correct Gravity; if any tuning has been done
   by observing the current behaviour, that tuning was against the defect.
5. Note that this changes observed behaviour on device — the silent band (Circle 0) will persist for
   more opens than it does today. That is the correct behaviour, but it will look like a regression
   to anyone testing without knowing, so record it in the phase summary.

## Related

- Canonical strategy §10.3 (Gravity), §10.4 (Pressure), §10.5 (the three profiles).
- `src/CONFIG-BLOCK.md` — the threshold tables this affects.
- `2026-08-16-device-uat-nine-circles-and-sequence-switching.md` step 7 — records the same defect as
  a note; that todo tests escalation and is the one most directly invalidated by leaving this open.
- `.planning/debug/device-state/README.md` — the 0.1667 reading.
