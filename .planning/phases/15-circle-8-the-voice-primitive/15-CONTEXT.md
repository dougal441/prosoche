# Phase 15: Circle 8 — the Voice primitive - Context

**Gathered:** 2026-08-18
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss)

<domain>
## Phase Boundary

Build Circle 8. **The product ships eight working Circles, not nine** — at Circle 8 you get
the menu, tap Continue, and nothing happens. The escalation ladder goes quiet at exactly the
point before Ice, the second-strongest Circle in the design.

`primitive_dispatch()` iterates the nine primitive names but explicitly `continue`s past
`Voice`, and because the dispatch comparison is condition 99 ("contains"), the sequence entry
`"Voice"` matches no emitted branch and fails **silently**. Confirmed against the shipped
artifact, not inferred: every other primitive renders 10 dispatch branches; Voice renders 0.
Found by static comparison, never by testing — Circles 2–9 have never run on hardware.

**Decide the semantics first, and record the decision.** The likely intent, consistent with
§11 Primitive H: **Mirror (Circle 7)** shows the text and speaks it only if `voice_enabled`;
**Voice/Loud Mirror (Circle 8)** makes the spoken address *the* primitive — the escalation is
that the phone talks to you. Whether `voice_enabled = 0` degrades Circle 8 to a
Mirror-equivalent alert or skips it entirely is a real product decision, not an
implementation detail.

**Deliverables.** Emit a real Voice branch — either drop the `continue` and give
`mirror_and_voice()` a mode parameter, or split it into `mirror()` and `voice()` sharing the
template selector. **Watch the `Spoken This Run` guard**: if Circle 8 is reached in a run
where Mirror already spoke, the guard currently suppresses the second utterance.

**Sequencing note.** Phase 11 gives Circle 8 an interim branch (the Mirror) so the
dispatch-coverage guard can be a hard gate from the start, and moves dispatch to condition 4
(exact) per BD-06, which removes the "contains" fragility that hid this defect. This phase
replaces that interim branch with the designed primitive. Phase 10 already added
`docs/sequence_dispatch_check.py`, which currently **reports** the Voice orphan and exits 0;
once Voice dispatches, remove its `KNOWN_ORPHAN_ENTRIES` exemption rather than merely
satisfying it — after the rename the entry is `"Loud Mirror"`, so a stale exemption would
whitelist anything named `"Voice"` forever.

**Severity:** major
**Requirements:** CIRC-08, CIRC-09, CIRC-14, DIST-01
**Depends on:** Phase 11

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — discuss phase was skipped per user setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide decisions.

</decisions>

<code_context>
## Existing Code Insights

Codebase context will be gathered during plan-phase research.

</code_context>

<specifics>
## Specific Ideas

No specific requirements — discuss phase skipped. Refer to ROADMAP phase description and success criteria.

</specifics>

<deferred>
## Deferred Ideas

None — discuss phase skipped.

</deferred>
