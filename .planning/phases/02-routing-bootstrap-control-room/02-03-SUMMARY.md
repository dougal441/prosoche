---
phase: 02-routing-bootstrap-control-room
plan: 03
subsystem: automation
tags: [ios-shortcuts, plist-xml, control-flow, routing]

# Dependency graph
requires:
  - phase: 02-routing-bootstrap-control-room (plan 02-01)
    provides: "The router's outer If/Otherwise gate on Shortcut Input, and the declared-but-unpopulated Input Key variable name"
  - phase: 02-routing-bootstrap-control-room (plan 02-02)
    provides: "The Control Room Note's Automation A/B instructions naming the exact literal input strings OPEN and CLOSE"
provides:
  - "Input Key — the single normalised value (ExtensionInput -> Text -> trim -> uppercase) the router tests exactly once, never the raw Shortcut Input"
  - "The complete four-outcome router: MANUAL / OPEN / CLOSE / fail-safe, built entirely from nested single-condition If/Otherwise blocks — no Otherwise If anywhere in the file"
  - "OPEN and CLOSE branch anchors (Comment + Nothing, zero state mutation) ready for Phase 3's OPEN pipeline and Phase 4's CLOSE pipeline to fill in place"
  - "The inert fail-safe branch (BOOT-02): one Comment + exactly one Show Alert, structurally asserted to contain no file read/write, no dictionary mutation, no Note action, no Ask, no Wait"
  - "UA-07 in docs/BUILD-NOTES.md §6 — the Phase-2-gated on-device routing verification item (whitespace/absent-input composition, plus the three decision-table observations)"
affects: [02-04, phase-3, phase-4]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Shortcut Input is composed into a Text action via an ExtensionInput token attachment first, never fed straight into trimwhitespace/changecase — this is what makes the absent-input case (the very first run, before either automation exists) resolve to an empty string instead of risking a runtime error"
    - "is.workflow.actions.text.changecase wires its source via the `text` parameter key, not WFInput (CAP-34); is.workflow.actions.text.trimwhitespace uses WFInput (CAP-33) — the two immediately-adjacent actions in the same chain use different input keys, confirmed against the local ToolKit parameter catalog rather than assumed"
    - "Nested If/Otherwise router ladder: every nesting level gets its own freshly generated GroupingIdentifier; every plain Otherwise (WFControlFlowMode 1) carries zero condition fields, which is the entire mechanism that keeps this iOS-26-safe (a mode-1 action carrying WFCondition/WFConditionalActionString is an Otherwise If, macOS 27+ only)"
    - "A Comment immediately preceding a control-flow start must include a bulleted wiring list, not prose alone — enforced by the plugin's own PostToolUse validator hook, not just a style preference"

key-files:
  created: []
  modified:
    - src/PROSOCHE-Dumb.xml
    - docs/BUILD-NOTES.md

key-decisions:
  - "The raw-input Text action's output is chained directly by UUID/ActionOutput through trim -> changecase -> Set Variable \"Input Key\", with no intermediate named \"Raw Input\" variable — the plan's own Artifacts table states this plan 'introduces no new names' beyond Input Key, and the UUID-for-immediate-consumer pattern 02-01 already established (Config, Epoch Anchor, etc.) is the precedent this follows"
  - "WFCaseType is the literal string UPPERCASE, recovered from the local toolkit-v78-first-party-enum-cases.json catalog's com_apple_shortcuts_change_case_type entry (6 cases: UPPERCASE, lowercase, Capitalize Every Word, Capitalize with Title Case, Capitalize with sentence case, alternating case) rather than assumed from memory"
  - "The fail-safe alert's WFAlertActionTitle/WFAlertActionMessage use the WFTextTokenString display serialization with an empty attachmentsByRange, even though neither field interpolates any variable — the plan's action text explicitly requires this ('even if they interpolate nothing'), consistent with D-22/PITFALLS A2 treating Show Alert's two text fields as unconditionally display-serialized"
  - "UA-07 (not a reuse of UA-01..06) was created as the Phase-2-gated user-action item for routing-specific device-only facts (whitespace arrival, absent-input composition), then extended in place by Task 3 with the three decision-table observations, rather than opening a competing UA-08 — matching the plan's explicit instruction to extend rather than duplicate"
  - "Trim Whitespace's OutputName is recorded as \"Trimmed Text\" (the conventional Shortcuts UI label); this is cosmetic editor metadata only, referenced solely by UUID in the next action, and does not affect validator correctness or any acceptance criterion"

requirements-completed: [BOOT-01, BOOT-02]

coverage:
  - id: D1
    description: "The router is built entirely from nested single-condition If/Otherwise blocks: the outer has-any-value gate on Input Key, then OPEN (string-equals), then CLOSE (string-equals), each with a freshly generated GroupingIdentifier — no Otherwise If (mode 1 carrying condition fields) exists anywhere in the file"
    requirement: "BOOT-01"
    verification:
      - kind: other
        ref: "Task 2 <verify> ROUTER-SHAPE-OK script (plan 02-03-PLAN.md) — checked live against src/PROSOCHE-Dumb.xml"
        status: pass
      - kind: other
        ref: "Task 3 <verify> DEPTH-AUDIT-OK script (plan 02-03-PLAN.md) — full re-audit at 73 actions / 4 control-flow blocks"
        status: pass
      - kind: other
        ref: "bin/validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all"
        status: pass
    human_judgment: false
  - id: D2
    description: "Input Key is computed exactly once (ExtensionInput -> Text -> trim -> uppercase) and is the only value all three router conditions test; the outer gate's WFInput is repointed from raw ExtensionInput to Input Key with its has-any-value condition and GroupingIdentifier unchanged"
    requirement: "BOOT-01"
    verification:
      - kind: other
        ref: "Task 1 <verify> NORMALISATION-OK script (plan 02-03-PLAN.md)"
        status: pass
    human_judgment: false
  - id: D3
    description: "The fail-safe branch (BOOT-02) is structurally inert: the region between the CLOSE block's Otherwise and its End If contains exactly one Comment and exactly one is.workflow.actions.alert, and none of Save File, Get File, Set Dictionary Value, Create Folder, Create Note, Append to Note, Ask for Input, Wait, or Wait to Return"
    requirement: "BOOT-02"
    verification:
      - kind: other
        ref: "Task 2 <verify> ROUTER-SHAPE-OK script's BANNED-action-set check over the fail-safe region"
        status: pass
    human_judgment: false
  - id: D4
    description: "All four decision-table rows trace to a single, correct, non-overlapping entry point when the plist is read action-index by action-index: empty Input Key enters the MANUAL branch only through the outer gate's own Otherwise; OPEN executes only its two-action anchor; CLOSE executes only its two-action anchor; unrecognised non-empty input executes only the fail-safe Comment + Alert"
    requirement: "BOOT-01"
    verification:
      - kind: other
        ref: "Hand-trace against the action-index dump, recorded in this SUMMARY's Decision Table Trace section"
        status: pass
    human_judgment: false
  - id: D5
    description: "On a real device: a manual tap with no input actually lands in the Control Room; a real automation-triggered OPEN reaches the OPEN branch with no visible alert; and an automation passing unrecognised input shows exactly the one diagnostic alert authored here and leaves state.json/the Control Room Note unchanged"
    verification: []
    human_judgment: true
    rationale: "No iPhone or Shortcuts-capable simulator is available in this environment. The structural proof (D1-D4) establishes the plist can only route each input class to one place, but whether the runtime actually executes that shape — including whether the alert renders and whether a real Personal Automation's input text round-trips unmodified — is exactly the class of validator-invisible fact PITFALLS A9 describes. Recorded as UA-07 (extended) in docs/BUILD-NOTES.md §6, gated on Phase 2."

# Metrics
duration: ~20min
completed: 2026-08-13
status: complete
---

# Phase 2 Plan 3: The Complete Four-Outcome Router Summary

**`src/PROSOCHE-Dumb.xml`'s router expanded from a single input-present gate into a full nested If/Otherwise ladder — normalised `Input Key`, then OPEN, CLOSE, and an inert fail-safe branch, structurally proven against a four-row decision table.**

## Performance

- **Duration:** ~20 min
- **Completed:** 2026-08-13T03:21:32Z
- **Tasks:** 3 completed
- **Files modified:** 2 (0 created, 2 modified)

## Accomplishments

- `src/PROSOCHE-Dumb.xml` grew from 56 to 73 actions: 5 new actions for input normalisation (Comment, Text/ExtensionInput, Trim Whitespace, Change Case, Set Variable "Input Key") plus 12 new actions for the nested OPEN/CLOSE/fail-safe ladder (2 Comments + 1 If + 1 Comment + 1 Nothing per block, times two blocks, plus the fail-safe Comment + Alert)
- The outer routing gate's `WFInput` repointed from a raw `ExtensionInput` attachment to the named `Input Key` variable, with its has-any-value condition code (100) and its `GroupingIdentifier` (`F646324A-...`) left exactly as 02-01 authored them
- Two new nested `If`/`Otherwise` blocks (`FA045F2B-...` for OPEN, `A2F7247B-...` for CLOSE), each on its own freshly generated `GroupingIdentifier`, replace the TRUE-branch anchor 02-01 left in place — zero `Otherwise If` anywhere in the file, confirmed structurally
- The fail-safe branch (BOOT-02) is proven inert by construction: the region between its `Otherwise` and `End If` contains exactly one `Comment` and exactly one `is.workflow.actions.alert`, and a structural scan confirms none of Save File, Get File, Set Dictionary Value, Create Folder, Create/Append Note, Ask, Wait, or Wait to Return appear anywhere in that region
- All four decision-table rows (empty → MANUAL, `OPEN` → OPEN, `CLOSE` → CLOSE, anything else non-empty → fail-safe) were traced by hand against the actual action-index sequence — see Decision Table Trace below — confirming no input reaches two branches, none reaches zero, and the MANUAL branch has exactly one entry point (the outer gate's own `Otherwise`)
- `docs/BUILD-NOTES.md` §6 gained a new `UA-07` item (routing-specific device-only facts), later extended in the same task sequence with the three decision-table observations a device is needed to confirm — not folded into UA-01..06, and not a competing UA-08

## Decision Table Trace

Traced directly against `src/PROSOCHE-Dumb.xml`'s action array (0-based index) after Task 2, re-confirmed clean by Task 3's depth audit:

| `Input Key` after normalisation | Branch reached | Actions that execute (indices) |
|---|---|---|
| empty (absent input, or whitespace only) | MANUAL — outer gate's own `Otherwise` (index 42) | Index 27's has-any-value test is FALSE, so the entire OPEN/CLOSE/fail-safe region (28-41) is skipped entirely; execution resumes at index 42 and continues through the bootstrap-check/Control-Room path (43-71) to the outer gate's `End If` (72). This is the **only** path that ever reaches indices 43-71. |
| `OPEN` | OPEN branch | Index 27 TRUE → index 29's `OPEN` test (`FA045F2B`) is TRUE → indices 30-31 execute (Comment anchor + `Nothing`) → the `Otherwise` at index 32 and everything nested in it (33-40) is skipped → closes at indices 41/42/72. No alert, no MANUAL-branch content. |
| `CLOSE` | CLOSE branch | Index 27 TRUE → index 29's `OPEN` test is FALSE → index 32 `Otherwise` → index 34's `CLOSE` test (`A2F7247B`) is TRUE → indices 35-36 execute (Comment anchor + `Nothing`) → the fail-safe content (38-39) is skipped → closes at indices 40/41/42/72. |
| anything else, non-empty | fail-safe | Index 27 TRUE → index 29 FALSE → index 32 `Otherwise` → index 34 FALSE → index 37 `Otherwise` → indices 38-39 execute (Comment + exactly one `Show Alert`) → closes at indices 40/41/42/72. No file read, no dictionary write, no Note action. |

## Task Commits

Each task was committed atomically:

1. **Task 1: Normalise Shortcut Input once into Input Key** - `4957972` (feat)
2. **Task 2: The nested OPEN / CLOSE / fail-safe ladder** - `5a4823b` (feat)
3. **Task 3: Prove the decision table and re-audit the graph at its new depth** - `876cbec` (docs)

## Files Created/Modified

- `src/PROSOCHE-Dumb.xml` - Router expanded from one input-present gate to the complete four-outcome ladder (73 actions, 4 control-flow blocks, import-question binding at indices 2/4 re-verified intact after every insertion)
- `docs/BUILD-NOTES.md` - New `UA-07` (§6), extended in place by Task 3 with the three decision-table observations

## Decisions Made

See `key-decisions` in the frontmatter for the five decisions requiring the most justification. In brief: two were forced by real, evidenced constraints not fully spelled out in the plan's prose (the `text` vs `WFInput` key split between adjacent text-transform actions, and the plugin's own bulleted-wiring-list comment rule caught by the auto-validate hook — documented as a deviation below); the other three are implementation choices made under genuine but narrow ambiguity (no new variable name for the raw-input holder, the `UPPERCASE` enum literal, and `UA-07` as a new item rather than an extension of an existing one).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Added bulleted wiring lists to the two new control-flow Comments**
- **Found during:** Task 2, first `Write`/`Edit` of the OPEN and CLOSE `If` blocks
- **Issue:** The plugin's `PostToolUse` auto-validate hook rejected both new Comments (the ones immediately preceding the OPEN and CLOSE `If` starts) with `Control-flow Comment must include a bulleted wiring list`. The plan's action text asked for "a descriptive Comment" but did not spell out this specific validator rule (documented in `SKILL.md`'s "Comment Blocks" section, not in this plan's `read_first` list).
- **Fix:** Rewrote both Comments to keep their descriptive first line and add a short bulleted list describing the wiring in Shortcuts-UI wording (e.g. "- Input uses the Input Key variable set above."), matching the style already used by 02-01's two existing control-flow Comments.
- **Files modified:** `src/PROSOCHE-Dumb.xml`
- **Verification:** `validate-shortcut` passes; the hook raised no further errors on re-edit.
- **Committed in:** `5a4823b`

---

**Total deviations:** 1 auto-fixed (blocking/Rule 3)
**Impact on plan:** Required to make the validator/hook pass at all; does not weaken any acceptance criterion, change routing behaviour, or add scope beyond what the plan's own Comment-density requirement (inherited from 02-01's established pattern) already implied.

## Known Stubs

The OPEN and CLOSE branches each contain only a `Comment` anchor plus a single `Nothing` action — this is the plan's own explicit, literal instruction ("For this phase it is a Comment anchor... plus a Nothing action so the branch is well-formed"), not an undocumented gap:

- OPEN branch (`src/PROSOCHE-Dumb.xml`, inside the `FA045F2B-...` block's TRUE branch) — Phase 3 fills this with the OPEN pipeline (Heat/Gravity/Pressure and the Circle mapping); plan 02-04 inserts the shared bootstrap check here first.
- CLOSE branch (inside the `A2F7247B-...` block's TRUE branch) — Phase 4 fills this with the CLOSE pipeline (session measurement and the overrun/race protocol).

Neither prevents this plan's own goal (a provably-shaped four-outcome router) since both branches are structurally well-formed, contain zero state mutation as required, and are correctly reached per the Decision Table Trace above.

## Issues Encountered

None that affected the committed result. (During authoring, an intermediate `Edit` transiently removed the outer gate's own `Otherwise`/TRUE-branch content while repointing its `WFInput`; this was caught and fully restored before running any `<verify>` script or making any commit, so no broken state was ever committed.)

## User Setup Required

None - no external service configuration required. This plan's on-device-only facts are covered by the new `UA-07` item in `docs/BUILD-NOTES.md` §6 (whitespace arrival, absent-input composition, and the three decision-table observations), gated on Phase 2's on-device confirmation pass, same as the existing UA-01/UA-03..06 items from 02-01/02-02.

## Next Phase Readiness

`src/PROSOCHE-Dumb.xml` still validates at `--target-macos 26 --target-platform all` and now has a complete, structurally-proven four-outcome router. Ready for 02-04 (state-load-and-do-not-overwrite, Note-existence guard, import-answer normalisation — including the shared bootstrap check plan 02-04 inserts inside the OPEN branch anchor this plan built) and, beyond this phase, for Phase 3's OPEN pipeline and Phase 4's CLOSE pipeline to fill their respective anchors in place. Nothing structural laid down here is expected to be rewritten by those plans. The open item is UA-07 (new) alongside the existing UA-01/03/04/05/06 — all gated on Phase 2's single on-device bootstrap-and-automations pass, not yet performed since no iPhone is available in this build environment.

---
*Phase: 02-routing-bootstrap-control-room*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: `src/PROSOCHE-Dumb.xml`
- FOUND: `docs/BUILD-NOTES.md`
- FOUND: `.planning/phases/02-routing-bootstrap-control-room/02-03-SUMMARY.md`
- FOUND: commit `4957972`
- FOUND: commit `5a4823b`
- FOUND: commit `876cbec`
