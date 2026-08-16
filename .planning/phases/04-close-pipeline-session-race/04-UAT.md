---
status: testing
phase: 04-close-pipeline-session-race
source: [04-01-SUMMARY.md]
started: 2026-08-16T00:10:00.000Z
updated: 2026-08-16T00:10:00.000Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: 1
name: Simple OPEN → wait → CLOSE records a plausible session
expected: |
  state.json shows a plausible session duration in recent_sessions after a normal
  open/wait/close cycle.
awaiting: user response

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
result: pending

### 2. CLOSE with no active session does not corrupt state or error
expected: closing when nothing is open produces no error dialog and no state corruption.
result: pending

### 3. The session race — rapid switching between two tracked apps (§20 steps 2–6)
expected: open A, open B, close A, close B (scripted deliberately, not left to chance) —
if the active session ID changed, the newer OPEN owns state and the older CLOSE aborts
without mutating state. This is the single most important case and the hardest to trigger
by hand.
result: pending

### 4. CLOSE after device lock / app switch away
expected: this different trigger path also records correctly and does not corrupt state.
result: pending

### 5. Behavioural-day boundary (§10.1, 04:00 rollover) crossed mid-session
expected: a session spanning the rollover is handled correctly, not double-counted or
dropped.
result: pending

### 6. Verify the numbers in state.json, not just absence of errors
expected: after each case above, `recent_sessions`, `last_close_at`, and the cleared
`active_session` hold exactly what §20 says they should. "No error dialog" is not a pass —
recompute by hand for at least two cases.
result: pending

## Summary

total: 6
passed: 0
issues: 0
