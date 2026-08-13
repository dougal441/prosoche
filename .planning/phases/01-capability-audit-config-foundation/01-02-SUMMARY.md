---
phase: 01-capability-audit-config-foundation
plan: 02
subsystem: docs
tags: [shortcuts-playground, capability-audit, ios26, toolkit-lookup]

# Dependency graph
requires: ["01-01"]
provides:
  - "docs/BUILD-NOTES.md section 4 extended with 25 capability audit rows (CAP-01..06, CAP-25, CAP-11..15, CAP-21..24, CAP-28, CAP-S01..S08 minus S07 duplicate note) — table now holds 26 judged rows total"
  - "docs/BUILD-NOTES.md section 5 extended with DEV-02 (file-existence-check bootstrap substitute)"
  - "docs/BUILD-NOTES.md ### Confirmation-prompt risk paragraph under section 4 (no verdict — open on-device question for Phase 2)"
affects: [01-04, 01-05, phase-2, phase-5]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Every row re-runs the section-3 python3 lookup recipe live rather than copying STACK.md's verdicts, and records any divergence found (several rows corrected or strengthened STACK.md's prior findings)"
    - "Identifiers absent from all three toolkit-v*-tool-ids.json id arrays and the OS27 parameter-keys catalog can still be VERIFIED via the protocol's prose-doc/golden-XML secondary sources (is.workflow.actions.conditional, repeat.count/each, choosefrommenu) — this is a legitimate, protocol-sanctioned evidence path, not a downgrade"

key-files:
  created: []
  modified:
    - docs/BUILD-NOTES.md

key-decisions:
  - "CAP-S04 (If/Otherwise/End If) and CAP-S05 (Repeat) and CAP-12's choosefrommenu half resolved to VERIFIED despite being absent from all three ids-array snapshots and the parameter-keys JSON catalog, because CONTROL_FLOW.md's prose + real golden-XML wiring examples satisfy the section-3 binding citation rule (prose reference docs and golden-shortcut XMLs are named primary-equivalent evidence sources, not external corroboration)"
  - "CAP-03's Save File overwrite parameter (WFSaveFileOverwrite) and CAP-21's Speak Text text key (WFText) and CAP-23's Run Shortcut params (WFWorkflow/WFInput) and CAP-24's Wait duration key (WFDelayTime) all resolved stronger (full VERIFIED with confirmed param shape) than STACK.md's prior UNVERIFIED/unconfirmed findings on live re-lookup against the parameter-keys catalog"
  - "CAP-13's Open App parameter candidate WFAppIdentifier was found NOT to exist in the catalog — the real keys are WFSelectedApp/WFAppName — corrected rather than transcribed as-is from the plan's candidate list"

requirements-completed: [AUDIT-01, AUDIT-07]

coverage:
  - id: D1
    description: "14 audit rows for data/state/control-flow actions (CAP-01..06, CAP-25, CAP-S01..S06, CAP-S08) added to BUILD-NOTES.md section 4, each with a live-relookup Evidence cell and a DEV entry (DEV-02) for the one non-trivial gap found (file-existence check)"
    requirement: "AUDIT-01"
    verification:
      - kind: other
        ref: "grep-based structural verify command in 01-02-PLAN.md task 1 (DATA-GROUP-OK)"
        status: pass
    human_judgment: false
  - id: D2
    description: "11 audit rows for interaction/output/ancillary actions (CAP-11..15, CAP-21..24, CAP-28, CAP-S07) added to BUILD-NOTES.md section 4; table reaches the required 26-row minimum; Confirmation-prompt risk paragraph added"
    requirement: "AUDIT-01"
    verification:
      - kind: other
        ref: "grep-based structural verify command in 01-02-PLAN.md task 2 (INTERACTION-GROUP-OK rows=26)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Every row cites at least one real ToolKit JSON file, prose reference doc, or golden-shortcut XML filename per the section-3 binding citation rule; no candidate identifier was written in without being independently found by a live lookup"
    requirement: "AUDIT-07"
    verification:
      - kind: other
        ref: "manual review of all 25 added Evidence cells during authoring; each names specific files, line numbers, or python3 lookup results"
        status: pass
    human_judgment: true
    rationale: "Whether an Evidence cell's citation is sufficiently traceable is a judgment a human reviewer should spot-check, particularly the CAP-S04/CAP-S05/CAP-12-choosefrommenu rows that rely on prose+XML evidence rather than the ids-array JSON snapshots."

duration: ~35min
completed: 2026-08-13
status: complete
---

# Phase 1 Plan 2: Data, Control-Flow, Interaction, and Output Capability Audit Summary

**25 capability audit rows added to `docs/BUILD-NOTES.md` via live re-runs of the section-3 ToolKit lookup recipe, bringing section 4 to 26 total judged rows, with several rows correcting or strengthening `.planning/research/STACK.md`'s prior findings (CAP-03 overwrite, CAP-13 param names, CAP-21 Speak Text, CAP-23 Run Shortcut, CAP-24 Wait) rather than transcribing them unchecked.**

## Performance

- **Duration:** ~35 min
- **Completed:** 2026-08-13
- **Tasks:** 2
- **Files modified:** 1 (`docs/BUILD-NOTES.md`)

## Accomplishments

- Ran the section-3 `python3` lookup recipe live against all five ToolKit JSON snapshots for every one of the 25 candidate capabilities named in the plan, rather than copying `.planning/research/STACK.md`'s prior verdicts — every Evidence cell names the exact snapshot(s), parameter-catalog record, prose-doc line number, or golden-XML filename the verdict rests on.
- Added 14 rows for the data/state/control-flow group (Task 1): CAP-01 Get Current App, CAP-02 Get File, CAP-03 Save File/overwrite, CAP-04 Dictionary/Detect Dictionary, CAP-05 Get/Set Dictionary Value, CAP-06 date arithmetic (Adjust/Format Date, Get Time Between Dates), CAP-25 Base64, CAP-S01 Set/Get Variable, CAP-S02 Text, CAP-S03 Number/Math, CAP-S04 If/Otherwise/End If, CAP-S05 Repeat, CAP-S06 Get Item from List, CAP-S08 Set Name. All 14 resolved to full `VERIFIED`.
- Added 11 rows for the interaction/output/ancillary group (Task 2): CAP-11 Ask for Input, CAP-12 Choose from Menu/List, CAP-13 Open App, CAP-14 Open URL/Web Search, CAP-15 Maps, CAP-21 Speak Text, CAP-22 Lock Screen, CAP-23 Run Shortcut, CAP-24 Wait, CAP-28 Get App & Website Data, CAP-S07 Show Alert/Result/Notification. All 11 resolved to full `VERIFIED`.
- Discovered and recorded a protocol-relevant nuance: `is.workflow.actions.conditional`, `is.workflow.actions.repeat.count`/`.repeat.each`, and `is.workflow.actions.choosefrommenu` are **absent from all three `toolkit-v*-tool-ids.json` id arrays and the OS27 parameter-keys catalog**, yet are exhaustively documented with real worked XML in `CONTROL_FLOW.md`/`ACTIONS.md` and present in multiple golden-shortcut XMLs — resolved to `VERIFIED` via the section-3 protocol's prose-doc/golden-XML evidence path rather than downgraded, since that path is explicitly sanctioned as valid evidence (not "external corroboration").
- Found and corrected five divergences from STACK.md during the live re-run: CAP-03's Save File overwrite parameter (`WFSaveFileOverwrite`, confirmed present — STACK.md called it UNVERIFIED); CAP-13's Open App parameter names (`WFSelectedApp`/`WFAppName`, not the `WFAppIdentifier` both this plan and STACK.md assumed); CAP-21's Speak Text key (`WFText`, confirmed present — STACK.md called the exact key unconfirmed); CAP-23's Run Shortcut params (`WFWorkflow`/`WFInput`, confirmed present — STACK.md called them UNVERIFIED); CAP-24's Wait duration key (`WFDelayTime`, a bare `float` in seconds — not the `WFQuantityFieldValue{Magnitude,Unit}` shape STACK.md and this plan's candidate text both speculated).
- Added `DEV-02` documenting the CAP-03 file-existence-check gap: no standalone existence-check action or filter predicate exists anywhere in the bundle (confirmed by live search); the substitute is Get File with `WFFileErrorIfNotFound=Off` piped through Detect Dictionary, treating a non-dictionary/empty result as "state absent."
- Added the `### Confirmation-prompt risk` paragraph under section 4, recording the PITFALLS C6 open question (certain actions can force an "Ask Before Running" prompt inside an automation) as an unresolved runtime behaviour with no verdict, naming Phase 2 as the owner of the required on-device automation-triggered test.

## Task Commits

Each task was committed atomically:

1. **Task 1: Audit rows for the data, state, and control-flow actions** - `4c4ddd5` (docs)
2. **Task 2: Audit rows for the interaction, output, and ancillary actions** - `c4933ca` (docs)

## Files Created/Modified

- `docs/BUILD-NOTES.md` - Section 4 (Capability audit table) extended from 1 to 26 judged rows; section 5 (Deviation log) extended with `DEV-02`; a new `### Confirmation-prompt risk` paragraph added under the table.

## Decisions Made

- **Evidence-source hierarchy applied literally:** where the `ids` JSON arrays and the OS27 parameter-keys catalog were silent (conditional, repeat, choosefrommenu), the prose reference docs and golden-shortcut XMLs — explicitly named as valid evidence sources in BUILD-NOTES.md §3 — were used to reach full `VERIFIED` rather than downgrading to `UNVERIFIED` for lack of JSON-snapshot presence. This is a correct application of the protocol, not a shortcut: the citation rule only excludes "external corroboration" (non-Playground sources) from raising a verdict above `UNVERIFIED`, and prose/XML bundled with the ToolKit is not external.
- **All 25 rows resolved to VERIFIED, not "identifier only," UNVERIFIED, or NOT AVAILABLE.** This is a genuine outcome of the live lookups (the OS27 parameter-keys catalog turned out to be far more complete for this action set than for CAP-20's Color Filters case), not an assumption — every row's Evidence cell documents the specific query that produced this result, and several rows explicitly flag where the plan's own candidate parameter names were wrong and had to be corrected against the catalog.

## Deviations from Plan

### Auto-fixed Issues

None requiring code fixes — this is a documentation-only phase with no runnable code. The only "deviation" in the Rule 1-4 sense is the file-existence-check gap, which the plan itself anticipated and instructed to record as `DEV-02` (not an unplanned executor deviation).

### Environment blocker (transient, self-resolved)

Mid-execution, between committing Task 1 and staging Task 2, `git` itself stopped functioning system-wide (`git --version` failed with "You have not agreed to the Xcode license agreements... run 'sudo xcodebuild -license'"). This was caused by a background macOS Software Update process (confirmed via `ps aux` showing active `softwareupdated`/`MobileSoftwareUpdate` processes) that reset the Xcode CLT license-acceptance flag mid-session — unrelated to any action this plan took. Polled for recovery (~260s total across two bounded polling loops) rather than attempting a `sudo` workaround (no passwordless sudo available, and accepting an Xcode license non-interactively is out of scope for a docs executor). Git recovered on its own; Task 2's already-verified file edits were re-verified intact on disk before staging and committing. No commit was lost; no working-tree content was affected by the outage.

## Issues Encountered

The transient git/Xcode-license outage above. No other issues — the precondition (BUILD-NOTES.md sections 3-4 populated, ToolKit data directory readable) held for both tasks, and every candidate identifier in the plan was found by a real lookup (none had to be recorded `NOT AVAILABLE`).

## User Setup Required

None for this plan's own scope. Note for awareness: the environment's Xcode Command Line Tools license was reset by a background OS update during this session; if a future plan hits the same `git`/`xcodebuild` license error, running `sudo xcodebuild -license` once in an interactive terminal will resolve it (not required now — it self-resolved).

## Next Phase Readiness

- `docs/BUILD-NOTES.md` section 4 now holds 26 judged rows (CAP-20 plus the 25 this plan added) — plans 01-04 and 01-05 can extend it further (blocker-decision rows BD-02..BD-05, user action items UA-01+, coverage check) without needing to re-derive any of this plan's findings.
- Five corrected/strengthened parameter shapes (CAP-03, CAP-13, CAP-21, CAP-23, CAP-24) are now available to Phase 2/5 executors as confirmed facts rather than open Craig-Loop questions, reducing on-device confirmation burden for those five actions specifically.
- The `### Confirmation-prompt risk` paragraph gives Phase 2 an explicit, named acceptance gate (test the full OPEN handler from a real backgrounded automation trigger) that must be satisfied before the OPEN handler is considered functional.
- No plist XML, package manifest, lockfile, or test-runner configuration was created, consistent with this phase's scope boundary.

---
*Phase: 01-capability-audit-config-foundation*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: docs/BUILD-NOTES.md
- FOUND: .planning/phases/01-capability-audit-config-foundation/01-01-SUMMARY.md
- FOUND: 4c4ddd5 (Task 1 commit)
- FOUND: c4933ca (Task 2 commit)
- FOUND: 26 CAP rows in docs/BUILD-NOTES.md section 4
- FOUND: DEV-02 in docs/BUILD-NOTES.md section 5
