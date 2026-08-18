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

## From plan 11-09 (one audit per OPEN-arm rendering)

- **Two unrelated actions share one action `UUID`, on BOTH forks, and nothing in the build or
  either validator gate can see it.** Measured 2026-08-18 while running plan 11-09's
  whole-artifact uniqueness criterion, which is how it surfaced at all.

  `792D1640-FEB7-5FAF-AD6D-0E66CC1A1075` is carried by two actions on each fork: the bootstrap
  `is.workflow.actions.detect.dictionary` that produces `State` (Core index 77, Aware 79) and
  the `is.workflow.actions.getvalueforkey` reading `voice_enabled` (Core 3724, Aware 3858).
  It is **pre-existing at HEAD `224e68a8`** — present in the committed artifacts before plan
  11-09 changed anything, on the **Core** fork as well as Aware, so it is emitted by
  `tools/build_state_engine.py` and merely inherited by the fork. Plan 11-09 modifies
  `build_sentient.py` only and is required to leave `src/PROSOCHE-Dumb.xml` byte-identical, so
  fixing it here was out of scope and was not attempted. Verified not caused by 11-09: the
  duplicate set is identical before and after, and no audit-span identifier participates in it.

  **It is the same landmine class Phase 16 documented in `stable_uid()`'s docstring, one axis
  over.** `build_state_engine.uid()` is a positional COUNTER, so a region preserved across
  builds freezes its identifiers at whatever counter value first created them, and a
  regenerated block can later land on that value. Phase 16 fixed the instance it hit and armed
  `verify_group_identifier_uniqueness()` — but that guard asserts start/end ownership of
  **`GroupingIdentifier`s only**, so the identical collision on the action **`UUID`** axis is
  outside it.

  **Nothing currently detects it.** Measured, not assumed: `verify_group_identifier_uniqueness()`
  passes, gate A (`--target-macos 26 --target-platform all`) prints `Validation passed.` and
  exits 0, and all thirteen structural checkers are green. Plan 11-09's negative control A
  reproduced exactly this shape deliberately (a second duplicate action UUID) and confirmed
  **both** the guard and gate A stay silent — only an explicit whole-artifact UUID count sees it.

  **Why it is not yet known to be harmful, and why that is not reassurance.** A duplicate UUID
  matters when it is *referenced*: `output(uuid, name)` builds an `ActionOutput` magic-variable
  token by `OutputUUID`, so a reference to one of the two could resolve to the other. Whether
  either of these two is referenced anywhere was **not** investigated — establishing that is the
  first step of the fix, not a claim being made here. Like Phase 16's instance, it is harmless
  exactly until an unrelated change shifts the counter, and re-armable by any future phase.

  **Suggested shape of the fix**, by analogy with the settled precedent rather than as new
  design: take the preserved identifier out of the counter sequence via `stable_uid()`, and
  extend the guard (or add its sibling) to assert action-`UUID` uniqueness alongside
  `GroupingIdentifier` ownership, so the collision becomes unrepresentable rather than unlikely.
  Both forks would need rebuilding and re-signing, which is why this is a plan of its own.
