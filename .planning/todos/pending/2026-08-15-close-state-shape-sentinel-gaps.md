---
created: 2026-08-15T21:05:00.000Z
title: Close the remaining state-shape sentinel gaps (exit_events, active_session)
area: general
severity: major
files:
  - tools/build_state_engine.py
---

## Problem

The `open-routing-sequence-error` debug session's cycle 16 closed a live STATE-SHAPE +
GATE-SEMANTICS defect on `pending_exit` (entirely absent from the bootstrap
`state.json` template, hard-erroring on a flat read; the pre-existing clearing gate also
tested container-existence instead of leaf-value). Two siblings in the exact same
family are known and NOT yet fixed:

1. **`exit_events`** — still entirely absent from the bootstrap `state.json` template
   (same STATE-SHAPE gap `pending_exit` had). Sits on the exit-recording path
   (`record_exit_and_route()`), not the OPEN critical path A–J, so it did not block the
   just-closed device measurement — but it is a live crash risk the first time that path
   actually executes with a fresh/clean state.
2. **`active_session`** — the sole remaining entry in `KNOWN_SENTINEL_EXISTENCE_GATES`
   after cycle 16. Confirmed SAFELY INERT on the closing device run specifically (the run
   reached breadcrumb I without touching any `active_session` read on the direct
   `open_pipeline()` A–J sequence), but that is a statement about what THIS run
   exercised, not a permanent property of the defect — the session's own cycle-16
   lesson was explicitly that "latent" only means "not yet reached by a device run."
   `active_session` IS read on `record_exit_and_route()`'s path (the same path
   `exit_events` sits on), so a genuine active session + exit sequence will very likely
   reach both gaps in the same run.

`HANDOFF.md` §6 explicitly suggests bundling both into one future cycle since they are
the same family and live on the same code path.

## Solution

Apply the exact container/leaf pattern already verified twice this session
(`settings_snapshot`, then `pending_exit`) to both remaining keys:

1. For each of `exit_events` and `active_session`: seed a permanent container in the
   bootstrap `state.json` template (mirroring `seed_pending_exit()`'s shape), and add a
   `verify_*_seed()` build guard following `verify_pending_exit_seed()`'s pattern.
2. Audit every read/write/clear site for both keys (`record_exit_and_route()`,
   `universal_leaving()`, and any other consumer found by a full-codebase grep — per
   this session's own hard rule, fix whole classes via a systematic sweep, not
   site-by-site) and ensure clearing gates test leaf-value (condition 5 against
   `CLEARED_SENTINEL`) rather than container-existence (condition 100), per cycle 12's
   already-proven invariant.
3. Remove both keys from `KNOWN_SENTINEL_EXISTENCE_GATES` once fixed, so the registry
   accurately reflects zero remaining known gaps.
4. Regenerate, validate, sign, decrypt-verify (both forks — check whether the Sentient
   re-fork todo has landed first, since it will pick this up for free if run after).
5. Device-test specifically the exit-recording path (a real "leave and confirm exit,"
   not just an OPEN) — this is the path that was NEVER exercised by the closed OPEN-path
   debug session, so treat it as new-risk surface, not a re-confirmation.
6. `DEV-06` (the `changed_at`/`changed_by_session_id` restore-ownership check, written at
   20 sites and read nowhere) is explicitly moot if the brightness/volume MVP cut (see
   the ship-readiness todo) proceeds — check that decision first before spending effort
   wiring DEV-06's read side.

## Related

- `.planning/debug/resolved/open-routing-sequence-error.md` — cycle 16 root cause,
  cycle 10–12's original container/leaf pattern for `settings_snapshot`.
- `.planning/debug/HANDOFF.md` §6 items 7 and 9 — this todo's origin.
