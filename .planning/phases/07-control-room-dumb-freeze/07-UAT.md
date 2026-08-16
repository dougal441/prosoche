---
status: testing
phase: 07-control-room-dumb-freeze
source: [07-LIGHT-SUMMARY.md]
started: 2026-08-16T00:15:00.000Z
updated: 2026-08-16T00:15:00.000Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: 1
name: Status shows real numbers
expected: |
  The Status menu item shows real numbers, not blanks — the axis-2 empty-field defect
  presented exactly as plausible-looking blank text.
awaiting: user response

## Context

Exactly one manual-menu item has any device evidence — `Open Control Room` — and even that
is **partial**: the closing device report of the `open-routing-sequence-error` session did
not explicitly confirm the `filter.notes` fix (Finding 2), so "does a note picker still
appear?" remains locally verified only. Every other menu item is untested on iPhone.

The menu is the product's entire administrative surface (§18): Status, Open Control Room,
Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today,
Emergency Restore (plus Toggle On-Device AI / Test Model, out of scope here — Sentient
only).

Two items carry outsized risk. **Emergency Restore** is the designed escape hatch (§21) —
if it doesn't work, every other safety argument in the product is void, since it's what
makes stateful friction defensible at all. **Test a Circle** is the harness Phase 5's UAT
depends on, and it was itself broken on device once (the `sequence` Set Dictionary Value
error) — confirm it here before trusting it there.

This UAT also owns §32's **Safety** acceptance criteria that are recovery-shaped rather
than menu-shaped: corrupt/missing `state.json` and a deleted Control Room Note must each
self-heal rather than fail, from all three invocation modes (manual, OPEN, CLOSE).

Do this before stripping debug scaffolding, so failures stay localisable.

Canonical strategy §18 (manual run/menu), §21 (Emergency Restore), §17 (Note structure),
§7.3 (profile sync), §32 (Bootstrap and Safety acceptance criteria).

## Tests

### 1. Status shows real numbers
expected: real numbers, not blanks (watch for the axis-2 empty-field defect).
result: pending

### 2. Open Control Room — no stray note picker
expected: opens the Note directly; explicitly confirm no note picker / list of every note
appears (the outstanding Finding-2 check).
result: pending

### 3. Sync My Profile extracts correctly and stays scoped
expected: extracts the `MY PHONE, ON PURPOSE` section and mirrors it into state.json
(§7.3); confirm it does not parse the whole Note on this path.
result: pending

### 4. Change Profile persists and changes Circle mapping
expected: persists, and demonstrably changes subsequent Circle mapping (cross-check
against Phase 5's UAT).
result: pending

### 5. Change Sequence persists and changes Circle mapping
expected: persists, and demonstrably changes which primitives fire per Circle
(cross-check against Phase 5's UAT).
result: pending

### 6. Toggle Voice persists and gates The Voice
expected: setting persists and actually gates whether The Voice primitive speaks.
result: pending

### 7. Test a Circle — all nine selectable and firing
expected: all nine fire on demand without altering real Pressure.
result: pending

### 8. Reset Today resets counters without destroying history
expected: behavioural day's counters reset; historical data (contracts, sessions, etc.) is
not destroyed.
result: pending

### 9. Emergency Restore — while in Ice
expected: clears cooldown, clears active session, restores any managed setting — tested
*while actually in Ice*, not from a clean state (a clean state proves nothing).
result: pending

### 10. Emergency Restore — while a session is active
expected: same guarantees hold when triggered mid-session.
result: pending

### 11. Idempotence across repeated manual runs
expected: running the menu repeatedly never overwrites existing state or creates a second
Control Room Note — exactly one Note exists afterward.
result: pending

### 12. Recovery — deleted Control Room Note
expected: next run recreates it, populated, without crashing.
result: pending

### 13. Recovery — malformed JSON state.json
expected: safe recovery, not a hard error.
result: pending

### 14. Recovery — valid-JSON-but-wrong-schema state.json
expected: safe recovery, not a hard error.
result: pending

### 15. Recovery — state.json deleted entirely
expected: bootstrap re-runs cleanly.
result: pending

### 16. Recovery cases hold across all three invocation modes
expected: tests 12–15 each re-verified from manual, OPEN, and CLOSE invocation — the
self-healing chain was deliberately hoisted above the router for exactly this reason.
result: pending

## Summary

total: 16
passed: 0
issues: 0
