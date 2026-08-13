---
phase: 06-exits-exit-learning-contracts
plan: 01
subsystem: shortcuts-exits
tags: [shortcuts, plist, exits, ownership]
requires: [05-nine-primitives-environmental-safety]
provides: [universal-leaving, enabled-exit-routing, owned-exit-events]
affects: [07-control-room, 08-sentient]
tech-stack: {added: [], patterns: [semantic plist routing, full-state ownership reload]}
key-files: {created: [], modified: [tools/build_state_engine.py, src/PROSOCHE-Dumb.xml]}
key-decisions: ["Leaving wraps primitive dispatch after the initial session save."]
requirements-completed: [EXIT-01, EXIT-02, EXIT-03, EXIT-04, EXIT-05, EXIT-06, EXIT-07, EXIT-08, EXIT-09]
duration: 25min
completed: 2026-08-13
status: complete
---

# Phase 6 Plan 1: Universal Leaving Summary

**Universal, enabled-only Leaving routes record an owned bounded event before opening a safe first-party target.**

## Accomplishments

- Added the pre-dispatch Leaving wrapper and canonical enabled-exit filtering.
- Added ownership-gated event recording and safe Capture, Coordinate, Create, Connect, Consult, and Close routes.

## Task Commits

1. **Tasks 1–2:** `b67270e` (feat)

## Verification

- `plutil`, target-26/all validator, and `git diff --check` passed.

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check: PASSED
