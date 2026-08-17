# Phase 12: State-shape sentinel gaps — exit_events and active_session - Context

**Gathered:** 2026-08-17
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss)

<domain>
## Phase Boundary

Close the two remaining STATE-SHAPE + GATE-SEMANTICS gaps — `exit_events` and
`active_session` — using the container/leaf pattern already verified twice on
`settings_snapshot` and `pending_exit`.

**Why this is a live crash risk, not housekeeping.** Per the verified runtime semantics in
`.claude/CLAUDE.md`, a **dotted read raises a hard error if any segment is absent**.
`exit_events` is entirely missing from the bootstrap `state.json` template, and it sits on
`record_exit_and_route()` — so the first real exit against clean state will very likely
hard-error. `active_session` is the sole remaining entry in
`KNOWN_SENTINEL_EXISTENCE_GATES`; it was confirmed inert only for one specific device run,
which is a statement about what that run exercised, not a property of the defect. Both keys
live on the same code path, so a genuine session-plus-exit sequence will reach both in one
run.

**Deliverables.** Seed a permanent container for each in the bootstrap template mirroring
`seed_pending_exit()`. Add a `verify_*_seed()` build guard per key following
`verify_pending_exit_seed()`. Audit **every** read/write/clear site for both keys by
full-codebase sweep — `record_exit_and_route()`, `universal_leaving()`, and anything else
grep finds — and ensure clearing gates test **leaf value** (condition 5 against
`CLEARED_SENTINEL`) rather than **container existence** (condition 100). Remove both keys
from `KNOWN_SENTINEL_EXISTENCE_GATES` so the registry honestly reads zero remaining gaps.

**Fix whole classes, never site-by-site** — every defect in this project's debug history was
systematic (147, 367, 25, 20 and 8 sites). A read-then-`has any value` gate on a dotted path
is **unimplementable**: the read raises unless the key exists, and if it exists the gate is
true. Gate on a numeric `> 0` test or restructure to a flat read.

**Hard prerequisite for Phase 17**, whose Exile work sits directly on
`record_exit_and_route()`. Device-test the exit-recording path specifically — a real "leave
and confirm exit", not an OPEN. That path was never exercised by the closed OPEN-path debug
session, so treat it as new-risk surface.

**Severity:** major
**Requirements:** SESS-07, STATE-12, EXIT-01, EXIT-02, SAFE-01
**Depends on:** Phase 11

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — discuss phase was skipped per user setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide decisions.

Binding project constraints that are NOT discretionary (from `.claude/CLAUDE.md`):
- Build provenance gate: `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` must pass before running `tools/build_state_engine.py` or `tools/build_sentient.py`.
- Two-gate validation: gate A (`--target-macos 26 --target-platform all`) is mandatory and must pass clean; gate B (`--target-macos 27 --target-platform all`) is advisory with exactly one permitted waived line per fork.
- Never fabricate an action identifier, parameter key, or enum literal. If it cannot be verified, use the safest fallback and record the deviation.
- Signed artifacts must carry the exact display names `PROSOCHĒ — Nine Circles — Dumb.shortcut` / `— Sentient.shortcut`, no `_signed` suffix.

</decisions>

<code_context>
## Existing Code Insights

Codebase context will be gathered during plan-phase research. Known anchors named by the
ROADMAP goal, to be located and confirmed during research rather than assumed:
`seed_pending_exit()`, `verify_pending_exit_seed()`, `KNOWN_SENTINEL_EXISTENCE_GATES`,
`record_exit_and_route()`, `universal_leaving()`, `CLEARED_SENTINEL`.

</code_context>

<specifics>
## Specific Ideas

No specific requirements beyond the ROADMAP phase description — discuss phase skipped.

</specifics>

<deferred>
## Deferred Ideas

None — discuss phase skipped.

</deferred>
