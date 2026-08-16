---
status: testing
phase: 05-nine-primitives-environmental-safety
source: [05-01-SUMMARY.md, 05-02-SUMMARY.md, 05-03-SUMMARY.md]
started: 2026-08-16T00:11:00.000Z
updated: 2026-08-16T00:11:00.000Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: 1
name: Test a Circle harness itself works
expected: |
  Test a Circle (manual menu) fires without the sequence Set Dictionary Value error that
  broke it once already.
awaiting: user response

## Context

Phase 5's `passed` verdict is static analysis of the generated graph. Exactly **one**
Circle has ever fired on a real device: Circle 1, once, on build `2026-08-15o` (Pressure
0.1667, Heat 0). Circles 2–9 have never executed on iPhone.

The nine primitives are the most *heterogeneous* code in the product — each uses different
actions, several already known to behave differently on device than the plist implies:

- **Ash** ships as a degraded non-environmental pause (grayscale NOT AVAILABLE on iOS per
  CAP-20/BD-01) — on-device feel unknown, may be indistinguishable from The Knock. The
  separate grayscale-donor-test backlog item (Phase 999.3) may change what Ash is *before*
  this UAT runs — check its status first.
- **Dimming and Silence** carry 18 uncoerced `setbrightness`/`setvolume` numeric-operand
  sites deliberately deferred (axis 6b), subject to a pending MVP-cut decision.
- **The Voice** (`speaktext`) had its parameter key corrected late (DEV-C3-03, `WFText`
  not `WFInput`) and has never been heard on device.
- **Ice** (Circle IX) is covered by its own dedicated test group below — it's the only
  Circle that can leave the user in a *persistent* state, so it gets extra scrutiny.

Blank text is the specific failure to watch for: the `WFTextTokenString` envelope defect
(axis 2, 367 sites) presented exactly as silently-empty fields, and the `WFItems`
List-wrapper defect (still open in a separate todo) is known from a screenshot to render
list rows blank.

Canonical strategy §11 (nine primitives), §12 (sequences and testing philosophy), §21
(environmental state safety), §22 (Circle IX — Ice, and the route out), §14.4 (Circle IX
has no model), §32 (Circles acceptance criteria).

## Tests

### 1. Test a Circle harness itself works
expected: fires without the `sequence` Set Dictionary Value error that broke it once
already — confirm before trusting it as an instrument for everything below.
result: pending

### 2. All nine primitives fire, in all three sequences
expected: for each of the nine — intervention appears, copy is correct and non-empty
(watch for blank text specifically), exit/dismiss path present and reachable, returns
control cleanly.
result: pending

### 3. The three sequences (Classic / Black Mirror / Ambient) genuinely differ
expected: switching sequence visibly changes which primitives fire per Circle, following
the Config threshold tables per profile (§10.5). A sequence change that doesn't change what
the user sees is a silent failure.
result: pending

### 4. Composition, not just firing
expected: a stronger Circle does not necessarily replay every earlier Circle's prompt.
Count total taps at Circles 6–9 and sanity-check against §30's intervention-fatigue failure
mode.
result: pending

### 5. Safety floors (pass/fail, not observations)
expected: no zero brightness, no unsafe/startling volume, nothing that strands
accessibility, across every primitive fired. Any violation is stop-the-line regardless of
how the rest of the run went.
result: pending

### 6. Ice — deterministic cooldown applies on entry
expected: entering Ice applies the profile-configured cooldown (~60s Paradise / ~3m Limbo /
~5m Inferno, Config-tunable).
result: pending

### 7. Ice — target-app OPEN during cooldown ejects immediately
expected: a target-app OPEN while Ice is active ejects/redirects immediately, with
remaining cooldown shown where practical.
result: pending

### 8. Ice — blocked attempts don't inflate Heat
expected: repeated blocked attempts during Ice do not endlessly compound Heat (§22's
specific named runaway to check).
result: pending

### 9. Ice — expires on its own and clears state
expected: Ice expires unassisted, grants Heat relief, clears `cooldown_until`, and the next
OPEN afterward behaves normally.
result: pending

### 10. Ice — cooldown_until sentinel across the full cycle
expected: reading state.json at each stage shows unset → set with a real future timestamp
→ observed active → cleared on expiry. This sentinel was reasoned-about but never exercised
through a real cooldown cycle.
result: pending

### 11. Ice — interruption cases don't create a permanent trap
expected: device restart mid-cooldown, behavioural-day rollover mid-cooldown, and clock
change each still allow Ice to expire correctly — none leaves it unexpirable.
result: pending

### 12. Ice — Emergency Restore clears it
expected: triggering Emergency Restore while in Ice clears the cooldown (cross-checked
against Phase 7's UAT, which covers Emergency Restore functionally).
result: pending

### 13. Ice — no model involvement
expected: Circle IX invokes no model (§14.4), confirmed now and re-checked after any future
Sentient re-fork lands.
result: pending

## Summary

total: 13
passed: 0
issues: 0
