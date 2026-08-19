---
created: 2026-08-19T02:57:30.109Z
title: enabled_exits() filters nothing — disabled exits are offered, selectable and routed
area: general
severity: blocker
files:
  - tools/build_state_engine.py
  - .planning/debug/device-state/README.md
---

> **COVENANT OVERHAUL (2026-08-19):** Owned by Phase 17 (EXIT-08 fix folded into the covenant substrate), because Redirect (Phase 18) and DENY routing both land on `select_exit()` and inherit this defect until it is fixed.


## Problem

**Device-confirmed 2026-08-18/19, finding F-18 — the most severe functional defect found in that
session, and it is fully characterised.** `enabled_exits()` is a complete no-op.

Choosing *Leaving → Choose another* with the shipped profile (all six exits enabled) presented
**36 entries**: `Capture` ×6, `Coordinate` ×6, `Create` ×6, `Connect` ×6, `Consult` ×6, `Close` ×6.

**The controlled experiment settles the mechanism exactly.** `profile_snapshot.enabled_exits` was
edited on the device to `["Capture", "Close"]` — four exits disabled — and the menu re-triggered.
It then contained **12 entries**: every one of the six canonical exits, twice each.

That is `6 canonical × N enabled`, measured at two values of N (36 at N=6, 12 at N=2). The nested
Repeat With Each in `enabled_exits()` appends the outer `Canonical Exit` on *every* inner
iteration — its inner conditional (`Enabled Exit Candidate` *string is* `Canonical Exit`)
evaluates **TRUE unconditionally**.

**The duplication is the visible symptom; the real defect is underneath it.** `Coordinate`,
`Create`, `Connect` and `Consult` were all **disabled** and all still offered — and `Coordinate`
was **selected and fully routed**, presenting its `Reminders / Calendar` sub-menu. The filter is
not weak, it is absent: a disabled exit is offered, selectable and functional.

**Why this is a blocker rather than a defect to queue.**

1. It breaks a stated rule, not a nice-to-have. Canonical strategy §9.2: *"Do not randomize to an
   exit they explicitly disabled."* A user who turned off `Connect` because they do not want social
   pressure as an intervention is still being routed there.
2. **It silently corrupts every exit-learning observation taken until it is fixed.** `select_exit()`
   rotates by `Exit Selection Counter % Enabled Exit Count` and scores by `exit_stats.<exit>`
   averages — both computed over a 36-item list rather than the user's six. Any explore/exploit
   evidence gathered before this lands has to be discarded, so fixing it is a **prerequisite** to
   Phase 06's remaining UAT and to any Phase 19 exit measurement, not a parallel task.

## Solution

Route: **phase work, not `/gsd-debug`** — the mechanism is already established by measurement, so
there is nothing left to investigate. Fold into the next phase that touches the exit path (Phase 17
is the natural home; do not wait for it if Phase 06 UAT is being resumed sooner).

1. **Fix the inner conditional in `enabled_exits()`.** It compares `Enabled Exit Candidate` against
   `Canonical Exit` via `WFConditionalActionString = token("Canonical Exit")` with condition 4. Per
   Phase 13's Donor 5 finding, that envelope shape is *correct* on its own — so establish why the
   comparison evaluates true regardless before changing the envelope, or the fix will be a guess.
   The likely candidates, in order: the two Repeat loops share or collide on a variable name
   (`Canonical Exit` is set inside the outer loop and read inside the inner one), or the appended
   variable accumulates across iterations because `Enabled Exits` is never reset per outer pass.
2. **Add a build guard** asserting the output list length equals the enabled count, not
   `6 × enabled`. This class is invisible to the validator and to a decrypt — it is a runtime
   semantics defect, so the guard has to encode the invariant rather than the shape.
3. **Re-seed or discard `exit_stats`** once fixed. Counts and `sum_return_seconds` accumulated
   against the broken list are not meaningful; decide explicitly whether to zero them (clean, loses
   the little real signal there is) or leave them (keeps history, biases exploitation). Record the
   decision either way — it is a data-integrity call, not an implementation detail.
4. **Re-run the affected UAT** — Phase 06 Tests covering exit selection and routing, which cannot
   produce trustworthy results until this lands.

## Related

- `.planning/debug/device-state/README.md` — finding **F-18**, with the two-point measurement.
- Canonical strategy §8 (the six exits), §9.1–9.3 (explore/exploit, and the do-not-offer-disabled
  rule), §30 (over-optimization for phone-based alternatives).
- `.planning/phases/06-exits-exit-learning-contracts/06-UAT.md` — the tests this gates.
- `2026-08-16-split-exile-into-two-circles.md` (Phase 17) — the phase most likely to host this fix.
