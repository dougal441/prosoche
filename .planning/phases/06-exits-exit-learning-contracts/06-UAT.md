---
status: testing
phase: 06-exits-exit-learning-contracts
source: [06-01-SUMMARY.md, 06-02-SUMMARY.md, 06-03-SUMMARY.md]
started: 2026-08-16T00:12:00.000Z
updated: 2026-08-16T00:12:00.000Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: 1
name: Resolve the Phase 6 verification conflict
expected: |
  06-VERIFICATION.md says passed; VERIFICATION.md says gaps_found with four failed
  entries. Determine which is current and record which one stands before running any
  device session against this phase.
awaiting: user response

## Context

This phase has the **highest known unfixed defect load in the product** and covers two
distinct feature areas that both depend on CLOSE (Phase 4) being verified first — run
`04-UAT.md` before this one.

**Contracts** (Confession / Intention Contract, §11 Primitive D) have never run on a
device. They're the mechanism the strategy leans on hardest: §6.7 names contract-fidelity
(intended vs. actual use) as potentially more informative than total screen time, and
§14.2 makes contract auditing — not lie detection — the entire basis of what Sentient is
allowed to do. If contracts don't work, the product degrades into a timer with dramatic
naming. Contracts are also the most *stateful* interaction in the product: free text in, a
duration choice in, both persisted across a session, compared against a CLOSE-measured
duration, then fed back into the next OPEN's Heat — every hop crosses a boundary this
project has already been burned at.

**Exits** carry the worst defect risk in the codebase: `exit_events` is **entirely absent**
from the bootstrap `state.json` template — the exact STATE-SHAPE class (axis 7) that
hard-errored on device twice already. It sits directly on `record_exit_and_route()` and
will very likely crash the first time a real exit is recorded against clean state.
`active_session` (the last remaining `KNOWN_SENTINEL_EXISTENCE_GATES` entry) is read on the
same path. **Both are tracked in the `close-state-shape-sentinel-gaps` todo — land that
first, before running any of the exit tests below.** Beyond crashes: if explore/exploit
learning doesn't actually work, PROSOCHĒ becomes a machine for changing which app consumes
the time (§30, §36 — explicitly not the goal).

Canonical strategy §11 Primitive D, §13.2, §6.1, §6.7, §8, §9, §16, §23, §27, §30, §32.

## Tests

### 1. Resolve the Phase 6 verification conflict
expected: read both `06-VERIFICATION.md` and `VERIFICATION.md`, determine which is
current, record the answer. Do not proceed against an unclear static baseline.
result: pass
note: "Resolved 2026-08-18 from git chronology — no device needed. Three commits, in order:
  a03f737 (18:14:14) 'docs(06): record verification gaps' wrote VERIFICATION.md with
  status gaps_found, 1/5 must-haves; e6ea081 (18:19:38) 'fix(06): close exit learning semantic
  gaps'; 4f28084 (18:23:17) 'docs(06): reverify exit learning phase' wrote 06-VERIFICATION.md
  with status passed, 5/5, whose own header calls itself a 'Gap-fix audit after e6ea081'.
  Each of the four gaps recorded in the older file maps to a truth marked VERIFIED in the newer
  one (Consult menu gained Notes/Reminders/Calendar/Back plus a user query; Create reloads and
  re-proves ownership; the selector picks exactly one canonical candidate; no-contract outcomes
  serialise distinctly and next-OPEN feedback is guarded on a positive declared duration).
  VERDICT: 06-VERIFICATION.md (passed, 5/5) is current and authoritative.
  The bare VERIFICATION.md has been renamed VERIFICATION-superseded.md so this conflict cannot
  be re-raised by a future /gsd-verify-work run."


### 2. Free-text intention accepted and persisted
expected: intention text is accepted and persisted verbatim — watch for silently-empty
fields (the axis-2 envelope defect presented exactly this way).
result: pending

### 3. Each contract duration option works
expected: 2 / 5 / 10 / 15 / Custom all work, including Custom's own input path.
result: pending

### 4. Deliberate leisure is accepted as a valid contract
expected: "watch stupid videos for ten minutes" is accepted, not treated as a challenge
trigger (§6.1, §32 — getting this wrong makes the product moralistic, §12's named killing
failure).
result: pending

### 5. Kept contract recorded and reduces next-OPEN Heat
expected: a contract kept within its bound is recorded as kept and reduces Heat on the next
OPEN (§10.2 rule 5).
result: pending

### 6. Overrun contract recorded with overrun amount and adds Heat
expected: a contract exceeded is recorded with its overrun, adding Heat per §10.2 rule 4
(>50% and >2 min).
result: pending

### 7. Blank/vague contract response handled per §13.2
expected: no attempt to parse sincerity; behaves per the documented Dumb intent gate.
result: pending

### 8. recent_contracts bounded window is correct
expected: state.json's `recent_contracts` holds the last ~10 per §16; fidelity figures are
arithmetically right — recompute by hand for at least two cases.
result: pending

### 9. No phantom contract-overrun Mirror message
expected: a time-overrun message is never shown when no contract existed (§13.1).
result: pending

### 10. Each of the six exits routes correctly
expected: Capture → Notes/Voice Memos/Camera; Coordinate → Reminders/Calendar; Create → the
user-defined target; Connect → Messages/Phone/FaceTime, never auto-contacting anyone
(§8.4); Consult → verify whether `searchweb` or an `openurl` fallback actually fires on
device and what it opens; Close → Home/Lock Screen/put device down, confirmed not degraded
(§8.6, §36).
result: pending

### 11. Exit outcomes recorded correctly
expected: exit type, timestamp, triggering app, Circle, Heat/Pressure, time of day, and —
the load-bearing field — time until the next target-app OPEN (§9.1). If that last field
isn't captured correctly, learning is decorative.
result: pending

### 12. Explore phase rotates across enabled exits only
expected: exploration never selects an exit the user has disabled.
result: pending

### 13. Exploit phase prefers historically stronger exits
expected: once `exits.exploit_min_observations` is met, exploitation prefers exits with
longer observed time-away; both `exploration_rate` and `exploit_min_observations`
(PROTOTYPE DEFAULT values) are reachable in realistic use, not just theoretically correct.
result: pending

### 14. Selection is deterministic, local, no model
expected: no model, no variable randomness source, no network involved in exit selection
(§9.3, §27).
result: pending

### 15. exit_stats stays bounded
expected: per-exit aggregates respect §16's rolling-window rule across a long test — no
unbounded growth.
result: pending

## Summary

total: 15
passed: 0
issues: 0
