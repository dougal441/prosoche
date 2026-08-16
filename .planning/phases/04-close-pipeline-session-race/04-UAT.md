---
status: complete
phase: 04-close-pipeline-session-race
source: [04-01-SUMMARY.md]
started: 2026-08-16T00:10:00.000Z
updated: 2026-08-16T09:15:00.000Z
---

## Current Test

[testing complete]

## Context

Phase 4 is marked `passed` in `04-VERIFICATION.md`, but that verdict is **static analysis
of the generated graph only** — the CLOSE path has never executed on a real iPhone. The
closed `open-routing-sequence-error` debug session device-verified the OPEN critical path
(breadcrumbs A–J, build `2026-08-15o`) and nothing else; the closing device report covers
one OPEN reaching Circle 1, full stop.

This matters more than any other UAT gap because **CLOSE is where session duration comes
from**, and session duration is the input to contract fidelity (Phase 6), exit-learning
outcomes (Phase 6), rapid-return detection, and the Heat adjustments that depend on all
three. If CLOSE is wrong, every downstream behavioural number is wrong in a way that looks
plausible. Two other known-open defects sit on or near this path: the `exit_events`/
`active_session` state-shape gaps (todo `2026-08-15-close-state-shape-sentinel-gaps.md` —
**hard prerequisite, land first**) and the `WFItems`/red-operator defects.

Keep `OPEN_BISECT` breadcrumb scaffolding ON for this work — do not strip it until CLOSE is
confirmed; bisection is the only tool that localises a failure to a span in one device
round trip. Coordinate with the ship-readiness-cleanup todo so stripping happens after, not
before.

Canonical strategy §20 (CLOSE handler, 17 steps), §30 (state races), §32 (OPEN/CLOSE
acceptance criteria).

## Tests

### 1. Simple OPEN → wait → CLOSE records a plausible session
expected: state.json's `recent_sessions` gets a new entry with a plausible duration after
open → wait → close.
result: issue
reported: "i can now see a session id in the state.json but declared duration seconds is
  :0 so maybe that didn't work, so valid session yes, but is going to have to be fixed
  later down the line"
severity: major

### 2. CLOSE with no active session does not corrupt state or error
expected: closing when nothing is open produces no error dialog and no state corruption.
result: pass

### 3. The session race — rapid switching between two tracked apps (§20 steps 2–6)
expected: open A, open B, close A, close B (scripted deliberately, not left to chance) —
if the active session ID changed, the newer OPEN owns state and the older CLOSE aborts
without mutating state. This is the single most important case and the hardest to trigger
by hand.
result: issue
reported: "doesnt look like the session id has changed once. i switched a to b to a close.
  open b to a to b. it kind of looks like it gets open, and gets close (because i get a
  menu popup) and then it's not doing next open? but, it's also hard to tell because we
  still have the test hardware pre-circles."
severity: major

### 4. CLOSE after device lock / app switch away
expected: this different trigger path also records correctly and does not corrupt state.
result: skipped
reason: "User: couldn't test — no reliable indicator of experiencing a Circle (which would
  confirm OPEN or CLOSE ran). Blocked on Ship-readiness cleanup for PROSOCHĒ Dumb
  (post-OPEN-path-closure, todo backlog item) to remove trace breadcrumbs first. While
  investigating, user also hit a confusing 'Leaving / Continue' menu popup and was unsure
  what it indicated — see Gaps G-04-4b."

### 5. Behavioural-day boundary (§10.1, 04:00 rollover) crossed mid-session
expected: a session spanning the rollover is handled correctly, not double-counted or
dropped.
result: skipped
reason: "Session paused (user + Claude decision): no reliable on-device indicator that a
  Circle/OPEN/CLOSE actually fired (see G-04-4b). Deferred until Ship-readiness cleanup
  restores observability."

### 6. Verify the numbers in state.json, not just absence of errors
expected: after each case above, `recent_sessions`, `last_close_at`, and the cleared
`active_session` hold exactly what §20 says they should. "No error dialog" is not a pass —
recompute by hand for at least two cases.
result: skipped
reason: "Session paused (user + Claude decision): same observability gap as Test 5 (see
  G-04-4b) — cannot reliably verify individual case numbers without confirming OPEN/CLOSE
  fired."

## Summary

total: 6
passed: 1
issues: 2
pending: 0
skipped: 3

## Gaps

- gap_id: G-04-1
  truth: "state.json's recent_sessions gets a new entry with a plausible duration after
    open → wait → close."
  status: failed
  reason: "User reported: session ID is recorded but declared duration_seconds is 0
    instead of a plausible elapsed duration."
  severity: major
  test: 1
  artifacts: []
  missing: []

- gap_id: G-04-3
  truth: "open A, open B, close A, close B — if the active session ID changed, the newer
    OPEN owns state and the older CLOSE aborts without mutating state."
  status: failed
  reason: "User reported: session id does not appear to change across rapid A/B switches;
    behavior after the first open/close pair looks like it stops registering subsequent
    OPENs. Observation made on pre-Circles test hardware, so confidence is limited."
  severity: major
  test: 3
  artifacts: []
  missing: []

- gap_id: G-04-4b
  truth: "OPEN/CLOSE behaviour should be observable/confirmable during manual testing
    without ambiguity."
  status: failed
  reason: "User reported: no reliable on-device indicator confirms a Circle actually
    fired (i.e. that OPEN or CLOSE ran) now that breadcrumbs are pending removal. During
    testing user encountered a 'Leaving / Continue' menu popup and could not tell what it
    signified. Blocks reliable UAT of Tests 3-6. Related todo: Ship-readiness cleanup for
    PROSOCHĒ Dumb (post OPEN-path closure) — do this before continuing device UAT on this
    phase."
  severity: major
  test: 4
  artifacts: []
  missing: []
