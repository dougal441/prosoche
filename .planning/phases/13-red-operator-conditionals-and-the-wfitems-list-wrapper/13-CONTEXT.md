# Phase 13: Red-operator conditionals and the WFItems List wrapper - Context

**Gathered:** 2026-08-17
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss)

<domain>
## Phase Boundary

Settle and fix two defect families carried unchanged through every cycle of the closed
`open-routing-sequence-error` session because both sit past breadcrumb J. Both are now safe
to pick up, and both are **device-visible defects that no file-level analysis can detect**.

**1. The 14 `WFConditionalActionString` red-operator sites ("Donor 5" family).** A variable
is placed directly into a conditional's TEXT-slot operand as a template. This is a
structurally different slot from the already-fixed `WFInput.Variable` envelope defect, so
that evidence does not transfer. Zero golden-corpus coverage, zero catalog coverage
(`is.workflow.actions.conditional` is absent from the ToolKit catalog entirely), zero device
coverage. `.planning/debug/Donor 5.shortcut` was captured specifically to settle this and
has never been analysed — decrypt it first (`aea decrypt` + `aa extract`, recipe in
`.claude/CLAUDE.md` §8) and read the real operand shape before touching any site. A concrete
starting site: `if_block("Previous Respected", 4, ...)`, seen rendering fully RED including
the operator picker in `.planning/debug/Screenshot 2026-08-14 at 11.55.12 pm.png`.

**2. The `WFItems` List wrapper (2 confirmed instances).** iOS wraps a variable-bearing List
row as `{"WFItemType": 0, "WFValue": <WFTextTokenString>}`; this artifact omits the wrapper,
so rows render blank. The same screenshot shows a List action rendering nine consecutive
rows as empty placeholders. The correct shape was already recovered from
`.planning/debug/Donor 4.shortcut` and `Donor 4.1.shortcut` but never applied.

**Deliverables.** Decrypt Donor 5, cross-check the recovered shape against the concrete site
before generalising, then sweep all 14 by class. Apply the Donor-4 wrapper shape to both List
sites, re-located by content. Add build-time recurrence guards for both, with sensitivity
demonstrated against a synthetically reverted artifact. Fold both newly-confirmed axes into
`.claude/CLAUDE.md`'s numbered axis list, together with the `read_value()`/`get_value()`
distinction and the `pending_exit` container/leaf pattern — do all three doc updates in one
pass.

**Why this gates the device UAT.** Blank text and red operators are exactly the two failure
modes Phase 19 is watching for. Fixing them first means a blank Circle in testing is a real
finding rather than a known artifact.

**Severity:** major
**Requirements:** CIRC-04, CIRC-07, ROOM-03, DIST-01, DIST-02
**Depends on:** Phase 12

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — discuss phase was skipped per user
setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide
decisions.

### Non-negotiable project constraints that bind this phase
- **Never fabricate a parameter shape.** The Donor 5 decrypt is the evidence source for the
  conditional TEXT-slot operand; the Donor 4 / 4.1 decrypt is the evidence source for the
  `WFItems` row wrapper. If a donor does not settle a shape, record the deviation and use the
  safest fallback rather than guessing (`.claude/CLAUDE.md` § Capability, § Conventions).
- **Two-gate validator rule** (`.claude/CLAUDE.md` §1 `### Exact validator invocation`):
  gate A `--target-macos 26 --target-platform all` is mandatory and must pass clean; gate B
  `--target-macos 27 --target-platform all` is advisory, exits 1 with exactly one permitted
  waived line per fork, and must never be chained into a definition of done.
- **Build provenance guard:** `git merge-base --is-ancestor 7ca8ebbf... HEAD` must hold before
  running `tools/build_state_engine.py` or `tools/build_sentient.py`.
- **Definition of done includes signing.** A valid XML draft without a signed `.shortcut` is
  not a stopping point; signed filenames must equal the exact display names
  (`PROSOCHĒ — Nine Circles — Dumb.shortcut`, `… — Sentient.shortcut`).
- **Fix whole classes, never site-by-site** (`.claude/CLAUDE.md` § Debugging technique).
- **Guards must be sensitivity-demonstrated** against a synthetically reverted artifact — a
  guard that cannot fail proves nothing.

</decisions>

<code_context>
## Existing Code Insights

Codebase context will be gathered during plan-phase research. Known anchors:
- Generators: `tools/build_state_engine.py` (Dumb), `tools/build_sentient.py` (Sentient)
- Structural checkers: `docs/*.py` (all must exit 0)
- Donor evidence: `.planning/debug/Donor 5.shortcut` (unanalysed), `.planning/debug/Donor 4.shortcut`,
  `.planning/debug/Donor 4.1.shortcut`, `.planning/debug/Screenshot 2026-08-14 at 11.55.12 pm.png`
- Doc targets for the single-pass update: `.claude/CLAUDE.md` numbered axis list,
  `docs/BUILD-NOTES.md`, `docs/CAPABILITY-DECISIONS.md`

</code_context>

<specifics>
## Specific Ideas

No additional requirements beyond the ROADMAP phase description — discuss phase skipped.

</specifics>

<deferred>
## Deferred Ideas

None — discuss phase skipped.

</deferred>
