---
phase: 4
plan: 1
subsystem: shortcut-session-close
tags: [shortcuts, plist, session, race-safety]
requires: [OPEN-state-pipeline]
provides: [race-safe-close, bounded-session-history]
affects: [phase-5, phase-6]
status: complete
---

# Phase 4 Plan 1: CLOSE Pipeline & Session Race Summary

Semantic CLOSE-anchor replacement records completed sessions without letting an older CLOSE overwrite a newer OPEN.

## Completed

- OPEN records a timestamped, unique session ID.
- CLOSE captures its entry session, waits, reloads state, and has a Nothing-only loser branch when IDs differ.
- The owner computes duration and overrun, keeps the newest 20 records, clears `active_session`, exposes the Phase 5 restore hook, and saves the reloaded full dictionary once.

## Verification

- `python3 .../validate_shortcut.py src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` — passed.
- `python3 docs/state_engine_self_check.py` — passed; asserts no Save File occurs in the superseded loser branch.

## Deviations from Plan

None — merged context executed directly.

## Self-Check: PASSED

- CLOSE semantic anchor is replaced and no CLOSE stub remains.
- Windows ledger entries 1 and 2 are fixed.

