---
phase: 01-capability-audit-config-foundation
plan: 05
subsystem: docs
tags: [shortcuts-playground, use-model, apple-intelligence, capability-audit, on-device]

# Dependency graph
requires:
  - phase: 01-capability-audit-config-foundation (plans 01-01 through 01-04)
    provides: 34 judged CAP rows, BD-01/BD-02/BD-03/BD-05, and the complete src/CONFIG-BLOCK.md
provides:
  - CAP-26 (Use Model / askllm action, fully evidenced, cross-platform VERIFIED) and CAP-27 (WFGenerativeResultType structured output, VERIFIED) rows in docs/BUILD-NOTES.md
  - The On-Device model-source literal recorded as UNRECOVERED-LOCALLY after three named recovery attempts, per D-11/D-07 — no candidate enum string guessed
  - BD-04 in docs/CAPABILITY-DECISIONS.md — AUDIT-06 Branch B taken, the Sentient fork's On-Device guarantee explicitly re-planned with a concrete Phase 8 gate
  - UA-02 user action item (the on-device round-trip recovery path), gated on Phase 8 only
  - Section 7 (Coverage check) in docs/BUILD-NOTES.md — capability coverage table (all 28 canonical capabilities), CAP-S supplementary table, deviation index, runnability statement, requirement closure table, consistency pass, and ROADMAP success-criteria mapping
  - Cross-references between docs/BUILD-NOTES.md, docs/CAPABILITY-DECISIONS.md, and src/CONFIG-BLOCK.md
affects: [phase-02-routing-bootstrap, phase-08-sentient-fork]

# Tech tracking
tech-stack:
  added: []
  patterns: ["do-not-fabricate protocol applied to the highest-consequence literal in the project (Use Model On-Device pinning)", "phase-gating via explicit re-plan when a capability is unrecoverable, rather than blocking"]

key-files:
  created: []
  modified:
    - docs/BUILD-NOTES.md
    - docs/CAPABILITY-DECISIONS.md
    - src/CONFIG-BLOCK.md

key-decisions:
  - "BD-04: AUDIT-06 Branch B taken — the WFLLMModel On-Device enum literal is UNRECOVERED-LOCALLY (absent from toolkit-v78-first-party-enum-cases.json under any type name, absent from all 19 golden-shortcut XMLs, and the only reference-doc literal observed — 'Apple Intelligence' — predates the iOS 26 three-way model picker and is explicitly not recorded as the answer)."
  - "No candidate enum string was written anywhere in either document. Guessing was evaluated and rejected outright as Options-considered item 1 in BD-04, per D-07's rule that an invented literal is a defect, not a shortcut."
  - "Phase 8 gate: may build Use Model wired with evidenced parameters, the tolerant ALLOW/CHALLENGE/DENY parse, the deterministic fallback, the context window, and the system instruction now; may NOT write a WFLLMModel value or claim On-Device is enforced by the shipped file until UA-02 closes. Until then the product states the model source is user-configured post-import, not PROSOCHĒ-enforced (D-06/DIST-07)."
  - "Safety holds regardless of the open literal: DUMB-01 (Dumb fork has zero Apple Intelligence dependency), SENT-05 (every model call has a deterministic fallback), SENT-12 (model never controls Heat/Gravity/Pressure/thresholds/timers/exits/Ice) — a misconfigured model source can only degrade output quality/privacy posture, never corrupt state or strand the user."

requirements-completed: [AUDIT-01, AUDIT-06, AUDIT-07, AUDIT-08]

coverage:
  - id: D1
    description: "CAP-26 (Use Model action + all 5 parameters) and CAP-27 (structured output) recorded as VERIFIED rows in docs/BUILD-NOTES.md §4, bringing the table to 36 judged rows"
    requirement: "AUDIT-01"
    verification:
      - kind: other
        ref: "grep -qE for CAP-26/CAP-27 rows with a four-value Verdict, plus askllm/WFLLMModel/WFGenerativeResultType/enum-cases-file citations, in docs/BUILD-NOTES.md (Task 1 <verify> block)"
        status: pass
    human_judgment: false
  - id: D2
    description: "On-Device selection literal recovery attempted via three named methods (enum-type lookup, golden-shortcut corpus search, reference-doc search); recorded as UNRECOVERED-LOCALLY with no candidate string guessed"
    requirement: "AUDIT-06"
    verification:
      - kind: other
        ref: "grep -qE 'UNRECOVERED-LOCALLY|ROUND-TRIP-CONFIRMED' docs/BUILD-NOTES.md; manual review confirms no bare 'On-Device'/'On Device' literal appears as a proposed WFLLMModel value anywhere in docs/BUILD-NOTES.md or docs/CAPABILITY-DECISIONS.md"
        status: pass
    human_judgment: false
  - id: D3
    description: "BD-04 written in docs/CAPABILITY-DECISIONS.md with all seven labelled fields, naming AUDIT-06 Branch B explicitly and citing SENT-05/SENT-12/DUMB-01/DIST-07 for why the safety guarantee holds"
    requirement: "AUDIT-06"
    verification:
      - kind: other
        ref: "grep -q for BD-04/AUDIT-06/DIST-07/SENT-05/DUMB-01/'phase 8'/WFLLMModel in docs/CAPABILITY-DECISIONS.md (Task 2 <verify> block)"
        status: pass
    human_judgment: false
  - id: D4
    description: "Section 7 Coverage check complete: all 28 canonical capabilities mapped to CAP-01..CAP-28, CAP-S supplementary table, deviation index with owning phases, runnability statement, requirement closure table (AUDIT-01..AUDIT-08), consistency pass, ROADMAP success-criteria mapping"
    requirement: "AUDIT-07"
    verification:
      - kind: other
        ref: "Task 3 <verify> block: per-ID CAP-01..CAP-28 presence loop, BD-01..BD-05 presence loop, AUDIT-01..AUDIT-08 reference loop, section-7/DEV-01/cross-reference greps, and src/CONFIG-BLOCK.md JSON parse+sequence-length assertion — all passed, PHASE-1-CLOSURE-OK rows=44"
        status: pass
    human_judgment: false
  - id: D5
    description: "src/CONFIG-BLOCK.md confirmed unchanged in structure (one fenced JSON block, three 9-entry sequences, thresholds.Limbo intact) and cross-referenced bidirectionally with docs/BUILD-NOTES.md"
    requirement: "AUDIT-08"
    verification:
      - kind: other
        ref: "python3 JSON-parse assertion embedded in Task 3 <verify> (CONFIG-STILL-OK)"
        status: pass
    human_judgment: false

# Metrics
duration: 45min
completed: 2026-08-13
status: complete
---

# Phase 1 Plan 5: Use Model On-Device Literal, Phase 8 Gate, Coverage Check & Phase Closure Summary

**The `Use Model` action and its 5 parameters are fully VERIFIED; the On-Device selection literal itself is UNRECOVERED-LOCALLY after three named recovery attempts, so BD-04 explicitly re-plans the Sentient fork's On-Device guarantee (AUDIT-06 Branch B) rather than guessing — and Phase 1 closes with all 28 canonical capabilities mapped, all 5 blocker decisions written, and all 8 AUDIT requirements satisfied.**

## Performance

- **Duration:** ~45 min
- **Completed:** 2026-08-13
- **Tasks:** 3/3 completed
- **Files modified:** 3 (`docs/BUILD-NOTES.md`, `docs/CAPABILITY-DECISIONS.md`, `src/CONFIG-BLOCK.md`)

## Accomplishments

- Resolved CAP-26 (`is.workflow.actions.askllm` / "Use Model") to full `VERIFIED` — identifier present in all three ToolKit id snapshots including the iOS-27-Simulator-specific one, and all 5 parameters (`WFLLMPrompt`, `WFLLMModel`, `WFAllowWebSearch`, `FollowUp`, `WFGenerativeResultType`) confirmed via direct query of `toolkit-v78-first-party-parameter-keys.json`, matching the research base's candidate list exactly.
- Attempted On-Device literal recovery via all three methods the plan required, in order, each recorded whether it succeeded or failed: (1) `WFLLMModel`'s enum type `com_apple_shortcuts_wfask_llmmodel_parameter` looked up in `toolkit-v78-first-party-enum-cases.json` — absent (a superficially similar but unrelated enum, `...generative_assistant_extension_llmpartner`, was checked and explicitly rejected as belonging to a different tool); (2) all 19 golden-shortcut XMLs grepped for `WFLLMModel`/`askllm` — zero matches, no real-world shortcut in the corpus uses this action; (3) `EXAMPLES.md`'s two worked `Use Model` examples both set the literal `"Apple Intelligence"`, recorded and explicitly labelled as **not** the answer since it predates the iOS 26 three-way model picker. Literal status recorded as `UNRECOVERED-LOCALLY` — no candidate enum string was written anywhere.
- Resolved CAP-27 (`WFGenerativeResultType`, structured output) to `VERIFIED` — typed `str`, the only observed literal in the bundle is `"Text"`; recorded the PITFALLS C9 tolerant-parse rule (contains-check, default-to-ALLOW, parse failure never functions as punishment) in the Fallback cell for Phase 8's SENT-04 implementation.
- Wrote BD-04 in `docs/CAPABILITY-DECISIONS.md` with all seven labelled fields, naming **AUDIT-06 Branch B** explicitly: what Phase 8 may build now (the action wired with evidenced parameters, the tolerant ALLOW/CHALLENGE/DENY parse, the deterministic Circle fallback, the compact context window, the system instruction), what it may not do until the literal exists (write a `WFLLMModel` value; claim On-Device is enforced by the shipped file), what the product says instead (the user configures the model source post-import; PROSOCHĒ cannot enforce it — per D-06/DIST-07), and why the safety guarantee holds regardless (DUMB-01, SENT-05, SENT-12). Options considered explicitly rejects guessing an enum string.
- Added UA-02 to `docs/BUILD-NOTES.md` §6 — the exact on-device round-trip steps (Shortcuts.app Model picker → On-Device → Share/Copy → paste to `.xml` → read `WFLLMModel` verbatim), gated on Phase 8 only, with Phases 1–7 and the Dumb fork explicitly unaffected.
- Completed `## 7. Coverage check` in `docs/BUILD-NOTES.md`: a capability coverage table mapping all 28 canonical capabilities (from `01-CONTEXT.md`'s operative superset of canonical strategy §31) to `CAP-01` through `CAP-28`, a supplementary `CAP-S01`–`CAP-S08` table, a deviation index (`DEV-01`, `DEV-02`, `DEV-03`) each with an owning phase, a runnability statement asserting and justifying all four AUDIT-07 claims (all four hold, no exception needed), a requirement closure table for `AUDIT-01` through `AUDIT-08` (with `AUDIT-06` naming Branch B explicitly), a consistency pass confirming `BD-01`–`BD-05` completeness and `src/CONFIG-BLOCK.md`'s continued integrity, and a closing subsection mapping all five ROADMAP Phase 1 success criteria to concrete content.
- Added bidirectional cross-references between `docs/BUILD-NOTES.md` §1, `docs/CAPABILITY-DECISIONS.md`, and `src/CONFIG-BLOCK.md`.

## Task Commits

1. **Task 1: Use Model and structured output — CAP-26 and CAP-27, and the On-Device literal recovery attempt** - `6526144` (docs)
2. **Task 2: BD-04 and the Phase 8 On-Device gate** - `2325edf` (docs)
3. **Task 3: Coverage check, deviation index, and phase closure** - `3406aa3` (docs)

_No TDD tasks in this plan — this phase authors no plist XML, no package manifest, no test harness._

## Files Created/Modified

- `docs/BUILD-NOTES.md` - Added CAP-26/CAP-27 rows, DEV-03, UA-02, cross-reference line in §1, and completed §7 (Coverage check) in full.
- `docs/CAPABILITY-DECISIONS.md` - Added the complete BD-04 record.
- `src/CONFIG-BLOCK.md` - Added a prose cross-reference line to `docs/BUILD-NOTES.md`/`docs/CAPABILITY-DECISIONS.md`; no change to the JSON literal or field reference.

## Decisions Made

- **BD-04 (AUDIT-06 Branch B):** The Use Model On-Device literal is recorded as `UNRECOVERED-LOCALLY`, not guessed. The Sentient fork's On-Device guarantee is explicitly re-planned rather than assumed — Phase 8 builds everything not dependent on the literal now, and states the guarantee honestly (user-configured post-import, not shipped-file-enforced) until UA-02 closes the gap.
- Guessing a plausible enum string (`"On-Device"`, `"On Device"`, an integer code) was evaluated and rejected outright as the single most consequential fabrication available in this project — it would pin an unverified value into a signed, distributed Shortcut governing where a user's behavioural data is processed.
- The runnability statement's four claims (no OPEN/CLOSE path depends on a `NOT AVAILABLE` action; every sequence-slot primitive has a defined behaviour; Circle IX's route-out is model-free; the Dumb fork has no dependency on any open item) were checked against the deviation index and all four hold without exception — no claim needed to be weakened or an exception recorded.

## Deviations from Plan

None - plan executed exactly as written. `DEV-03` was added per the plan's own instruction (Task 1's binding action), not as an unplanned deviation from this plan's own scope.

## Issues Encountered

None.

## User Setup Required

None blocking. `UA-02` (the on-device round-trip to recover the `WFLLMModel` On-Device literal) is recorded in `docs/BUILD-NOTES.md` §6 as a Phase-8-gated user action item — it does not block Phase 1's completion, Phases 2 through 7, or the Dumb fork, which ships with zero Apple Intelligence dependency (DUMB-01).

## Next Phase Readiness

Phase 1 is fully closed: all 28 canonical capabilities plus 8 architecture-critical supplementary actions are judged, all five blocker decisions (BD-01 through BD-05) are written, all eight AUDIT requirements are satisfied (AUDIT-06 via the permitted alternative branch), and `src/CONFIG-BLOCK.md` is confirmed intact. Phase 2 (Routing, Bootstrap & Control Room Onboarding) can begin against a settled evidence base — its dependency on BD-05 (Notes actions, gated on UA-01) and DEV-02 (the file-existence-check substitute) is already recorded with concrete implementation guidance. No unrecorded assumptions remain.

---
*Phase: 01-capability-audit-config-foundation*
*Completed: 2026-08-13*

## Self-Check: PASSED

All created/modified files confirmed present on disk (`docs/BUILD-NOTES.md`, `docs/CAPABILITY-DECISIONS.md`, `src/CONFIG-BLOCK.md`, this SUMMARY). All three task commit hashes (`6526144`, `2325edf`, `3406aa3`) confirmed present in `git log --oneline --all`.
