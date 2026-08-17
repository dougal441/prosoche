# Phase 16: Dimming and Silence as distinct device-proven Circles - Context

**Gathered:** 2026-08-17
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss)

<domain>
## Phase Boundary

Prove Dimming and Silence work as **distinct, device-verified Circles with reliable
capture-and-restore** — the outstanding half of Phase 9, which merged its code untested.

**Two things are true and the second is the risk.** They are built and merged: Phase 9
landed the numeric-coercion fix for all 28 `setbrightness` (14) / `setvolume` (14) operand
sites (`2e2261e`, artifacts in `c6d8737`), and Phase 10 pinned the whole surface with
`docs/environmental_restore_check.py` so it cannot be removed by accident. **But they have
never run on a phone, and the merge made them live** — before the coercion fix these actions
silently no-opped; now they actually change brightness and volume, and the code that puts
them back has never once executed on hardware. `09-UAT.md` has 12 tests; exactly one has
passed — test 1, the static "coercion chip does not render red" gate.

**The coercion shape itself is analogy-based, not donor-confirmed.**
`WFCoercionVariableAggrandizement` / `CoercionItemClass: WFNumberContentItem` is confirmed
for the Donor-4.1 *conditional operand* position; whether it is correct at a **direct
Set-action parameter** position is genuinely unknown. `Donor 10.shortcut` contains no
variable-fed `WFBrightness`/`WFVolume` example. If it proves wrong, follow `09-RESEARCH.md`'s
fresh-donor protocol — build a donor on device with a variable-fed Set Brightness and decrypt
it. **Do not guess a second `CoercionItemClass`.**

**Deliverables.** Run `09-UAT.md` tests 2–12 on a real iPhone. The closed-loop proof is what
matters: `Get Device Details` returns a real, correctly-typed value; the has-any-value guard
correctly *skips* the change when the read returns nothing; CLOSE restores the original
exactly. **Then the ugly cases** — app force-quit mid-session, device restart mid-session,
CLOSE never firing, two overlapping sessions, screen locked mid-session. Each must restore or
leave the user at a safe value. Never dark. Never silent forever. Never loud. Emergency
Restore must recover from every failure mode found, and it has itself never been tapped on a
device.

**DEV-06 is live again** — `changed_at` / `changed_by_session_id` are written at 20 sites and
read nowhere. That was recorded MOOT conditional on the cut proceeding; the cut is cancelled,
so DEV-06 and the `Session ID` scope defect both return. `docs/BUILD-NOTES.md` §17 reserves
the DEV-06 decision to the user — surface it, do not decide it unilaterally.

**The brightness floor was corrected and needs a decision on main.** Phase 9 revised BD-02's
"never zero, 10–15% band": the user's on-device observation is that iOS's practical minimum
is dim, not black, so avoiding zero was never itself the safety property — capture-and-restore
reliability is. That revision was scoped to the experimental fork; decide it for main here.

Distinct-Circle allocation is already settled by **BD-06 Decision 4** — do not re-cut it.

**Severity:** major
**Requirements:** CIRC-03, CIRC-05, SAFE-01, SAFE-02, SAFE-03, SAFE-05, DIST-03
**Depends on:** Phase 12

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — discuss phase was skipped per user
setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide
decisions.

### Explicitly NOT at Claude's discretion (carried from the ROADMAP goal)

- **DEV-06** (`changed_at` / `changed_by_session_id` written at 20 sites, read nowhere) is
  reserved to the user per `docs/BUILD-NOTES.md` §17. Surface it as a decision; do not
  resolve it unilaterally.
- **A second `CoercionItemClass`** must never be guessed. If `WFNumberContentItem` proves
  wrong at the direct Set-action parameter position, follow `09-RESEARCH.md`'s fresh-donor
  protocol instead.
- **Distinct-Circle allocation** is settled by BD-06 Decision 4 — do not re-cut it.

### Hard environmental constraint at plan time

`xcrun devicectl list devices` reports **No devices found** (checked 2026-08-17, this run).
The same DIST-03 blocker recorded against Phases 4, 9, 10 and 12 is still in force. The
device-proving half of this phase (09-UAT tests 2–12, the five failure-mode trials, the
Emergency Restore tap) **cannot be executed by an autonomous run**. Plans must:

1. Do all non-device work in full — static/structural proof, checker coverage, the UAT
   instrument itself, the decisions the ROADMAP reserves.
2. Record device-gated tests as BLOCKED with a real reason, never as passed or inferred.
   Precedent: Phase 10 DIST-03, Phase 12 `verification_deferred_human`.
3. Escalate no higher on the CLAUDE.md §9 evidence ladder than the open question requires —
   rung 1 (file-level) and rung 2 (simulator) work should be exhausted here so the eventual
   device session is not spent on questions a free rung could have settled.

</decisions>

<code_context>
## Existing Code Insights

Codebase context will be gathered during plan-phase research.

Known anchors from prior phases that this phase builds on:

- `09-UAT.md` — 12 tests, 1 passed (static coercion-chip gate), 11 outstanding.
- `09-RESEARCH.md` — carries the fresh-donor protocol for an unconfirmed `CoercionItemClass`.
- `docs/environmental_restore_check.py` — Phase 10 structural pin over the 28 operand sites.
- `docs/BUILD-NOTES.md` §17 — the DEV-06 reservation.
- `docs/CAPABILITY-DECISIONS.md` BD-02 (+ Phase 9 addendum) — the brightness-floor correction
  scoped to the experimental fork, pending a main-line decision here.
- `docs/CAPABILITY-DECISIONS.md` BD-06 Decision 4 — settled distinct-Circle allocation.
- `tools/build_state_engine.py`, `tools/build_sentient.py` — the two fork generators; the
  provenance guard (`git merge-base --is-ancestor 7ca8ebb HEAD`) gates both.

</code_context>

<specifics>
## Specific Ideas

No specific requirements — discuss phase skipped. Refer to ROADMAP phase description and
success criteria.

</specifics>

<deferred>
## Deferred Ideas

None — discuss phase skipped.

</deferred>
