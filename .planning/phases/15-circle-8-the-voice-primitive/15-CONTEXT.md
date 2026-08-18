# Phase 15: Circle 8 — the Voice primitive - Context

**Gathered:** 2026-08-18
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss); decisions D-01..D-06 confirmed with the user 2026-08-18 after research surfaced them

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

### Locked Decisions

All six were confirmed with the user on 2026-08-18, after `15-RESEARCH.md` surfaced them. They are
not open.

- **D-01 — Voice-off Circle 8 degrades, never skips** When `voice_enabled = 0`, Circle 8 shows a
  Mirror-equivalent alert. The alert is emitted before the speech gate, so the `otherwise` arm is
  `is.workflow.actions.nothing`. Rationale: a Circle that renders the menu, takes `Continue`, and does
  nothing is precisely the defect this phase exists to close — the cause being a user setting rather
  than a dispatch miss does not change what the user experiences. The import question ("May PROSOCHĒ
  speak to you at the highest circles?") is consent to be spoken to, not consent to have Circle 8.
  Accepted cost, recorded rather than papered over: with voice off, Circles 7 and 8 become
  indistinguishable to the user — CIRC-14 is satisfied by construction but not experienced. Distinct
  voice-off copy for Circle 8 was offered and declined; no requirement asks for it.
- **D-02 — Speech is removed from Circle 7** Circle 7 shows the reflection; Circle 8 speaks the same
  reflection. Grounded in canonical strategy §11 Primitive G (no speech in the Mirror's description)
  and §11 Primitive H ("the Mirror becomes spoken once"). This is what satisfies CIRC-14 and what
  makes Circle 8 an escalation at all. This is a visible behaviour change for existing
  `voice_enabled = 1` users — Circle 7 goes quiet. Accepted knowingly.
- **D-03 — The escalation is the modality, not the words** Circle 8 uses the same 30 fact-gated
  Mirror templates as Circle 7. No new copy, no longer copy.
- **D-04 — Axis-4 defect: discriminate early, then branch** The rung-2 alert-free simulator probe
  (shape in `15-RESEARCH.md` § Code Examples) runs early in the phase to identify which of
  `is.workflow.actions.list` / `getitemfromlist` / `speaktext` carries the unfilled picker. If the
  result is a one-line class fix, absorb it into this phase. If it is larger, record the finding and
  mark CIRC-08 device-unproven rather than silently implying otherwise. Doing the rewrite blind
  guarantees a rework, which is why the discrimination belongs here even if the fix does not.
- **D-05 — voice_enabled normalised to numeric, with a schema bump** The writer emits `1`/`0` and
  `schema_version` bumps. Bootstrap currently emits the unquoted JSON boolean `true`/`false` while
  `Toggle Voice` emits `1`/`0`, and boolean-to-`WFNumberContentItem` coercion is unaudited (nine-axes
  rule 6). Normalising the writer makes the open question moot rather than spending a device session
  to answer it.
- **D-06 — The Spoken This Run guard stays verbatim** The ROADMAP's warning about it is retired: the
  two OPEN-arm `primitive_dispatch()` renderings are mutually exclusive arms of the Panic Escape
  conditional, the nine MANUAL renderings are menu cases, and condition 4 matches exactly one branch —
  so Mirror and Loud Mirror can never both fire in one run. The guard *is* CIRC-08's "at most once per
  run".

### Claude's Discretion
All remaining implementation choices are at Claude's discretion — the discuss phase was
skipped per user setting. Use the ROADMAP phase goal, `15-RESEARCH.md`, and codebase
conventions to guide decisions.

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
