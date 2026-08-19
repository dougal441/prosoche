---
created: 2026-08-19T04:12:00.000Z
title: A one-item Shortcuts list serialises as a bare item, not a one-element array — and seeding [] does not prevent it
area: general
severity: minor
files:
  - tools/build_state_engine.py
---

## Problem

**Device-observed, 2026-08-18/19, Core `873fa3db…`.** When a Shortcuts List holding **exactly one
item** is written into `state.json`, it stores as the **bare item**, not as a one-element array.
Three independent containers did it, and two were then watched recovering:

| container | at n = 1 | at n = 2 |
|---|---|---|
| `recent_sessions` | bare object | **proper 2-element array** ✔ |
| `exit_events` | bare object | **proper 2-element array** ✔ |
| `exit_stats.<Exit>.samples` | bare scalar (`253`) | **not yet observed** |

## What this corrects, and it is the point of the todo

`seed_exit_events()` (phase 12) seeds `exit_events: []` precisely to prevent a degraded shape.
**The fresh bootstrap did carry `exit_events: []`, and the very first exit still wrote a bare
object.** So seeding an empty array prevents only the *unseeded read* — it does **not** prevent
the collapse. The collapse is a property of how a one-item list serialises, not of the seed.

`seed_exit_events()`'s docstring should be amended to say so. While editing it, also settle its
own open question: it records the pre-seed failure mode as `[ASSUMED]` (assumption **A1**) —
*"whether that is a zero-iteration no-op or a type error is [ASSUMED]"* — and marks it settleable
only at rung 2. **It is now settled at rung 4, in the direction the docstring hoped for:** the
recovered pre-install `state.json` shows the unseeded case producing a **silent single-object
overwrite** — no crash, no zero-iteration no-op. Promote A1 from assumed to measured and cite the
evidence.

## Why `minor`, with one exception that is not

For `recent_sessions` and `exit_events` the severity really is low: every downstream consumer
observed tolerated the n=1 object and produced a correct array at n=2, so the shape self-heals
after the first write and nothing was seen to break.

**The exception is `exit_stats.<Exit>.samples`.** It has not been observed at n ≥ 2, and it is
the one §16 trims as a rolling window and the one exploit-phase averaging consumes. A trim or an
average over a bare scalar is the plausible break, and it is exactly the `COMPOUND_STATE_KEYS`
hazard `.claude/CLAUDE.md` axis 9 already describes — note that `exit_stats.<name>.samples` is
recorded there as real but *dynamically keyed*, so the literal-key guard cannot see it.

## Solution

1. Amend `seed_exit_events()`'s docstring (both corrections above).
2. Record the runtime semantic where it belongs — already added to `.claude/CLAUDE.md`'s
   *Verified iOS Shortcuts runtime semantics* table.
3. **Settle the one that matters:** drive two exits of the *same* type and read
   `exit_stats.<Exit>.samples` at n = 2. If it becomes a proper array, this closes as
   documentation. If it does not, the rolling-window trim needs a real fix and the severity
   rises. One short device session, no Notes and no Apple Intelligence needed.
4. Everywhere a check verifies one of these containers, read the **flat dotted key**, not the
   nested subtree — see the same CLAUDE.md table.

## Evidence

`.planning/debug/device-state/README.md`, findings **F-3** and **F-20**.
