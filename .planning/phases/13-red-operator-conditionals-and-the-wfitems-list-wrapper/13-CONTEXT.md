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
  not a stopping point; signed filenames must equal the exact display names.
  **Corrected 2026-08-17 (research finding):** the canonical display names are
  `PROSOCHĒ — Nine Circles — Core.shortcut` and `PROSOCHĒ — Nine Circles — Aware.shortcut`.
  Phase 11 renamed the forks from Dumb/Sentient; `.claude/CLAUDE.md` §8 still carries the old
  names and is stale on this point. Verified at HEAD: `artifacts/shortcuts/` holds exactly
  `PROSOCHĒ — Nine Circles — Core.shortcut` and `PROSOCHĒ — Nine Circles — Aware.shortcut`,
  and `docs/manifest_check.py` asserts the canonical names as DIST-04. Signing to
  Dumb/Sentient would fail that check. Fork *internals* are still built by
  `tools/build_state_engine.py` (Core) and `tools/build_sentient.py` (Aware).
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

**Scope correction (2026-08-17, from `13-RESEARCH.md` — authoritative over the ROADMAP prose
above, which was written before the donors were decrypted):**

- **Family 1 is refuted, not fixed.** Donor 5 was decrypted for the first time and shows iOS
  itself authoring exactly the construct the ROADMAP suspected — a variable in a conditional's
  TEXT slot as a `WFTextTokenString` template, with `WFInput` alongside taking the opposite
  `WFTextTokenAttachment` envelope. `token()` emits a key-for-key identical shape, so the
  variable-bearing conditional sites are already correct. The deliverable becomes: record the
  refutation and add a *pinning* guard so a later pass cannot "fix" a device-confirmed shape.
  Do not sweep them.
- **Family 2 is real and far larger than recorded.** Not 2 instances — 66 defective List
  actions carrying 660 unwrapped rows per fork, all from one function, `mirror_text()`. Only
  variable-bearing rows take the wrapper; literal rows stay bare strings, so a blanket sweep
  would corrupt `list_items(EXIT_NAMES, …)`.
- **Every count in the ROADMAP prose is wrong** (14 conditional sites → 0 defective; 2 List
  sites → 66). Plan against the measured numbers in RESEARCH.md.
- **The named concrete site is not a member of the family.** `if_block("Previous Respected", 4, …)`
  passes a raw literal, never a `token()`.
- **The cited screenshot does not exist** anywhere in the worktree, the main checkout, or git
  history. No task may depend on reading it.
- The ROADMAP phase section should be corrected to match these measurements as part of this
  phase, so the record does not keep asserting refuted counts.

</specifics>

<deferred>
## Deferred Ideas

None — discuss phase skipped.

</deferred>
