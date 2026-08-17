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

## From plan 11-06 (the rename)

Both items below are **pre-existing** copy defects that the rename made more visible without
causing. Neither is load-bearing: no automation target, no state key, no lookup predicate.
Plan 11-06 deliberately did not widen its change surface to either.

- **The header comment still says "Dumb fork".** `WFWorkflowActions[0]`'s `WFCommentActionText`
  opens `PROSOCHE - Nine Circles (Dumb fork).` in **both** forks -- it is generator-authored and
  inherited verbatim by the fork, so the Aware build has always carried it too. It is visible in
  the Shortcuts editor but in no user-facing run. Fixing it properly means either accepting that
  the Aware fork's header would read `Core fork`, or adding a **fourth** site to
  `fix_fork_strings()` and a fourth entry to `docs/sentient_core_check.py`'s `FORK_STRINGS` -- a
  real, if small, widening of the divergence surface, which is why it was not done inside a plan
  whose divergence set was enumerated in advance.

- **The Aware Note's static settings block reads `- AI: not used by this fork`.** That literal
  lives twice: in the hand-authored Note body, and in `tools/build_state_engine.py`'s
  `manual_note_refresh()` snapshot template (measured 2026-08-17 at `:1926`), which is **shared**
  by both forks and re-appends the block on every state-changing manual run. Correcting only the
  Note body would leave the two disagreeing after the first manual run, so the fix is a
  fork-aware snapshot template, not a string edit -- new design work, and outside a rename plan.
  Plan 11-06 *did* fix the fork **label** on the adjacent line (`- Fork:`), because that one is
  load-bearing state.
