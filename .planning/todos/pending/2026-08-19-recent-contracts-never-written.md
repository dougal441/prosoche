---
created: 2026-08-19T02:57:30.109Z
title: recent_contracts is never written by any code path — decide the scope, then close §16
area: general
severity: major
files:
  - tools/build_state_engine.py
  - .planning/phases/06-exits-exit-learning-contracts/06-UAT.md
---

## Problem

**Device-confirmed 2026-08-18/19, finding F-2.** `recent_contracts` is `[]` in `state.json` on a
device that also holds a fully-evaluated contract in `recent_sessions` (declared 120 s, respected,
−99 s overrun).

This is not a device fluke and needs no further investigation:

    grep -c 'set_value("recent_contracts"' tools/build_state_engine.py   ->   0

The key is seeded `[]` by the bootstrap template and **no generator path ever appends to it**.
Contract outcomes are instead folded into the `recent_sessions` record as
`declared_duration_seconds` / `overrun_seconds` / `respected`.

**Two things follow, and they are different in kind.**

1. **A test that cannot pass on any build.** Phase 06 Test 8 asserts *"state.json's
   `recent_contracts` holds the last ~10 per §16"*. No build satisfies that, and none ever has.
   Leaving it pending forever misrepresents the backlog.
2. **A canonical-schema gap.** §16 names `recent_contracts` as one of the bounded rolling windows,
   alongside `recent_sessions`. Either the design was superseded when contract data was folded into
   the session record — in which case §16 and the test both need restating — or the window is
   genuinely unimplemented and should be built.

**The capability is probably intact either way.** Contract fidelity (§6.7's `actual / intended`,
the metric the strategy calls potentially more informative than screen time) is computable from
`recent_sessions` today. What is missing is the named container, not necessarily the information.
Confirm that before choosing, because it decides whether this is a rename or a build.

**This is a scope call, not a device question.** It should not be resolved by an agent alone.

## Solution

Route: **a decision first, then phase work.** Do not open `/gsd-debug` — there is nothing to
diagnose.

1. **Establish what is actually lost.** Enumerate what §15 and §28's model-context design need
   (median planned vs actual duration, per-intention-type consistency, "the last four sessions you
   called quick replies") and check each against what `recent_sessions` already carries. If every
   consumer is satisfiable from the session window, the container is redundant.
2. **Then choose, explicitly, one of:**
   - **(a) Retire it.** Amend §16 to drop `recent_contracts`, restate Phase 06 Test 8 against
     `recent_sessions`, and keep the key seeded `[]` only if something still reads it (it does not
     today — check before removing, since a dotted read of a missing key is a hard error, axis 7).
   - **(b) Build it.** Append a bounded ~10-record contract window at the same CLOSE site that
     writes `recent_sessions`, seeded at bootstrap with its own `verify_*_seed()` guard per the
     state-shape discipline. Cheap, and it keeps the strategy honest as written.
3. **Whichever is chosen, record it as a decision**, not a silent edit — this is the second time a
   canonical-schema field has turned out to be unimplemented, and the pattern is worth tracking.
4. **Update Phase 06 Test 8** so the UAT backlog stops carrying an unpassable item.

## Related

- `.planning/debug/device-state/README.md` — finding **F-2**.
- Canonical strategy §16 (JSON state design — the bounded windows), §6.7 (contract fidelity as the
  better behavioural signal), §15 (longitudinal memory), §28 (model-context design).
- `.planning/phases/06-exits-exit-learning-contracts/06-UAT.md` Test 8 — the unpassable test.
