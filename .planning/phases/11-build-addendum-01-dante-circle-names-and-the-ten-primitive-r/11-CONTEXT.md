# Phase 11: Build Addendum 01 — Dante Circle names and the ten-primitive roster - Context

**Gathered:** 2026-08-17
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss)

<domain>
## Phase Boundary

Apply `PROSOCHE_Build_Addendum_01.md` in full, once, against the roster settled in
**BD-06** (`docs/CAPABILITY-DECISIONS.md`) — so the rename lands a single time rather than
being re-cut after each of the four in-flight Circle phases.

**BD-06 is already decided and is binding. Do not re-litigate it.** Its five load-bearing
decisions: Dante names are **positional** (Circle 1 = Limbo … Circle 9 = Treachery),
because three sequences order the interventions differently at the same Circle numbers, so
a name can only attach to the number; canonical Dante order is kept; the roster grows to
**ten primitives for nine slots** and each sequence picks nine; combined sequence entries
are abolished so dispatch moves from condition 99 ("contains") to **condition 4 (exact)**;
and the routed Exile lands the user directly rather than offering a menu.

**Deliverables.** Rename the interventions per Addendum §5 (Knock→Pause, Ash→Black and
White, Confession→Intention, Dimming→Dim, Voice→Loud Mirror, Ice→Frozen; Silence and Mirror
unchanged; Exile splits into **Eject** straight and **Redirect** routed). Apply BD-06
Decision 4's slot table to all three sequences. Rename the Apple Note from
`PROSOCHĒ — Control Room` to `PROSOCHĒ` — three string occurrences in the XML — while
keeping "Control Room" as the internal name (settled in `e84ee77`). Rename the variants
Dumb→**Core** and Sentient→**Aware**. Make Panic Escape deliberately removable per
Addendum §3: the removal path requires manually editing the setting in the Note plus
explicit confirmation. **Panic Escape is the `Leaving` option** in `universal_leaving()` —
the easy behavioural bypass offered before every primitive — **not** Emergency Restore,
which is a safety mechanism and must stay unconditionally available. Add the optional
hardening note at the end of the Note explaining a user may add Shortcuts.app itself to
their target list.

**Write the dispatch-coverage build guard as part of this phase, not after it** — every
distinct primitive name in any `sequences` array must have exactly one dispatch branch, and
every branch must be named by at least one sequence. A mass rename across three sequence
arrays and ten dispatch branches is precisely the operation that guard exists to catch, and
this defect class is invisible to the validator, the ToolKit catalog and the signed-artifact
decrypt.

**Intermediate state to respect.** `Redirect` has no implementation until Phase 17, so all
three sequences hold `Eject` at Circle 6 until then; Phase 17 flips Classic's and Ambient's
cells. Circle 8 gets a real branch here (interim: the Mirror) so the guard can be a hard
gate immediately; Phase 15 replaces it with the designed Voice.

**Severity:** major
**Requirements:** AUDIT-02, CIRC-02, CIRC-06, CIRC-08, ROOM-01, ROOM-02, DIST-01, DIST-02
**Depends on:** Phase 10

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — discuss phase was skipped per user setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide decisions.

### Binding constraints carried in from the project (not discretionary)
- BD-06 in `docs/CAPABILITY-DECISIONS.md` is settled and binding — do not re-cut the naming/roster table.
- `.claude/CLAUDE.md` "Generator authoring rules — the seven parameter-defect axes" apply to every plist edit.
- Rebuild provenance gate: `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` must pass before running `tools/build_state_engine.py` or `tools/build_sentient.py`.
- Validator invocation is `--target-macos 26 --target-platform all`.
- A validator pass is not "done" — archive + sign + verify non-zero bytes is the definition of done.

</decisions>

<code_context>
## Existing Code Insights

Codebase context will be gathered during plan-phase research.

</code_context>

<specifics>
## Specific Ideas

No specific requirements beyond the ROADMAP phase description above — discuss phase skipped.

</specifics>

<deferred>
## Deferred Ideas

None — discuss phase skipped.

</deferred>
