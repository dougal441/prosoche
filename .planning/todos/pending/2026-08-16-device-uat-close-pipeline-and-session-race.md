---
created: 2026-08-16T00:10:00.000Z
title: Device UAT — CLOSE pipeline and session race
area: testing
severity: blocker
files:
  - tools/build_state_engine.py
  - .planning/phases/04-close-pipeline-session-race/04-VERIFICATION.md
---

## Problem

Phase 4 is marked `passed`, but that verdict is **static analysis of the generated graph
only**. The CLOSE path has never executed on a real iPhone. The closed
`open-routing-sequence-error` session device-verified the OPEN critical path (breadcrumbs
A–J, build `2026-08-15o`) and nothing else — the closing device report covers one OPEN
reaching Circle 1, full stop.

This matters more than the other UAT gaps because **CLOSE is where session duration comes
from**, and session duration is the input to contract fidelity, exit-learning outcomes,
rapid-return detection, and the Heat adjustments that depend on all three. If CLOSE is
wrong, every downstream behavioural number is wrong in a way that looks plausible.

The session also established that the axes which broke OPEN were invisible to static
analysis by construction — a validator-clean, signing-clean, importing-clean plist failed
at runtime nine distinct ways. There is no reason to expect the CLOSE path, authored by
the same generator under the same misunderstandings, to be cleaner. Two of the still-open
todos (`exit_events`/`active_session` state-shape gaps, and the `WFItems`/red-operator
defects) sit on or near this path.

Canonical strategy §20 defines the required behaviour and §32's OPEN/CLOSE acceptance
criteria define the pass bar.

## Solution

Run this as a proper device session, not an ad-hoc poke. Predict, then test, then record.

1. **Prerequisites.** Land `2026-08-15-close-state-shape-sentinel-gaps.md` first —
   `active_session` is read on the exit-recording path and is a known unfixed
   state-shape gap of exactly the class that hard-errored twice already on device.
2. **Keep breadcrumbs ON for this work.** Do not strip `OPEN_BISECT` scaffolding until
   the CLOSE path is confirmed; bisection is the only tool that localises a failure to a
   span in one device round trip. Coordinate with
   `2026-08-15-ship-readiness-cleanup.md` so the strip happens after, not before.
3. **Cases to prove on device**, from §20 and §32:
   - a simple OPEN → wait → CLOSE records a plausible session duration;
   - CLOSE with no active session does not corrupt state or error;
   - **the race case**: rapid switching between two tracked apps — §20 steps 2–6 require
     that if the active session ID changed, a newer OPEN owns state and the older CLOSE
     stops. This is the single most important case and the hardest to trigger by hand;
     script the sequence deliberately (open A, open B, close A, close B) rather than
     hoping to catch it;
   - CLOSE after a device lock / app switch away, which is a different trigger path;
   - the behavioural-day boundary (§10.1, 04:00 rollover) crossed mid-session.
4. **Verify the numbers, not just the absence of errors.** Read `state.json` back after
   each case and confirm `recent_sessions`, `last_close_at`, and the cleared
   `active_session` hold what §20 says they should. "No error dialog" is not a pass.
5. **Record results the way the closed session did** — predicted breadcrumb positions
   before the run, actual after, error text verbatim. Open a fresh debug session if a
   defect surfaces; do not reopen the archived one.

## Related

- Canonical strategy §20 (CLOSE handler, 17 steps), §30 (state races), §32 (OPEN/CLOSE
  acceptance criteria).
- `.planning/debug/HANDOFF.md` §4 (verified iOS runtime semantics), §7 (technique).
- `2026-08-15-close-state-shape-sentinel-gaps.md` — prerequisite.
- `2026-08-15-ship-readiness-cleanup.md` — do not strip breadcrumbs before this closes.
