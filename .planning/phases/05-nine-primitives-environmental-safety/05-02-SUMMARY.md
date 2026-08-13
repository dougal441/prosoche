---
phase: 05-nine-primitives-environmental-safety
plan: 02
subsystem: shortcuts-cooldown-dispatch
tags: [shortcuts, plist, ice, restoration]
requires: [05-01]
provides: [config-sequence-routing, deterministic-ice, close-and-expiry-restore]
affects: [phase-5-plan-03, phase-6, phase-7]
tech-stack:
  added: []
  patterns: [config-driven exact primitive selection, guarded restoration]
key-files:
  modified: [tools/build_state_engine.py, src/PROSOCHE-Dumb.xml]
key-decisions:
  - "Circle dispatch selects only the configured sequence entry, including combined entries."
requirements-completed: [CIRC-06, CIRC-07, CIRC-08, CIRC-09, CIRC-10, CIRC-11, CIRC-12, CIRC-13, CIRC-14]
duration: 20min
completed: 2026-08-13
status: complete
---

# Phase 5 Plan 2: Config Dispatch and Ice Summary

**Classic, Black Mirror, and Ambient dispatch exact primitive entries while Ice redirects, expires, and restores safely.**

## Accomplishments

- Reads the active sequence and Circle from State, then dispatches only the matching Config entry; combined entries invoke their named primitives.
- Adds deterministic Exile, factual Mirror, Voice-once gating, profile-based Ice, live-Ice redirect, and expiry Heat relief.
- CLOSE, expiry, and recovery restore captured brightness and Media volume from the latest full State dictionary.

## Task Commits

1. Task 1/2/3: dispatch, Ice, and restoration wiring — `5d74935` (feat; landed with the dependent production slice)

## Verification

- `python3 docs/phase5_self_check.py` — passed.
- `plutil -lint src/PROSOCHE-Dumb.xml` — passed.
- `validate_shortcut.py ... --target-macos 26 --target-platform all` — passed.

## Deviations from Plan

None — the dependent production slice was committed atomically with Plan 05-01 because all three Plan 05 implementations modify one semantic plist builder and one generated artifact.

## Self-Check: PASSED

