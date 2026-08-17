# Phase 11 — deferred items

Discovered during execution, out of scope for the plan that found them. Not fixed.

## From plan 11-01 (tracer)

- **`src/CONFIG-BLOCK.md:36-38` threshold drift.** The doc mirror still shows the pre-Phase-10
  curve (`Paradise: [1, 4, 7, 10, 13, 16, 19, 22, 25]`, and the matching `Limbo` / `Inferno`
  rows) while the live Config literal in `src/PROSOCHE-Dumb.xml` action 7 carries the Phase-10
  raised curve. `docs/state_engine_self_check.py:10-17` carries the *current* values and is
  green, so the artifact is right and the doc is stale — it is a documentation defect, not a
  behavioural one.

  Flagged by `11-RESEARCH.md` §3.4, which measured it with a three-way diff and states plainly
  that it is "not this phase's bug". Plan 11-01 edited a different block of the same file (the
  `sequences` array) and deliberately did not widen its change surface to an unrelated
  pre-existing drift. Whoever next edits `CONFIG-BLOCK.md`'s `thresholds` block should fix it in
  the same pass; the correct values are in `docs/state_engine_self_check.py:10-17`.
