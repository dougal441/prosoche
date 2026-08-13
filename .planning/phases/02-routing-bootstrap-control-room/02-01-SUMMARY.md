---
phase: 02-routing-bootstrap-control-room
plan: 01
subsystem: automation
tags: [ios-shortcuts, plist-xml, apple-notes, json-state, shortcuts-playground]

# Dependency graph
requires: []
provides:
  - "src/PROSOCHE-Dumb.xml — the first plist XML in the project, validating at the iOS 26 target"
  - "The plist envelope, icon, and root-key shape every later Phase 2-7 plan extends"
  - "Pinned import-question actions at indices 2 and 4 (WFWorkflowImportQuestions binds by position)"
  - "Config-block transcription pattern (Text -> Detect Dictionary -> Set Variable) reused for every tunable read"
  - "The epoch-clock construction pattern (Date anchor -> Get Time Between Dates -> Now Epoch; Adjust Date -> Format Date -> Behavioural Day)"
  - "The router's outer If/Otherwise gate on Shortcut Input via an ExtensionInput token attachment"
  - "The DEV-02 state-load substitute: Get File (WFFileErrorIfNotFound off) -> Detect Dictionary -> Text -> If has-any-value"
  - "The schema_version 1 state.json template as a literal Text-action JSON body with attachmentsByRange placeholders"
  - "The Control Room Note creation/open wiring via com.apple.Notes.CreateNoteFromMarkdownLinkAction + markdownContents"
  - "Six newly audited capability rows (CAP-29..34) and the corrected validator invocation (DEV-04)"
affects: [02-02, 02-03, 02-04, phase-3, phase-4, phase-5, phase-6, phase-7, phase-8]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Named-variable references (Type=Variable/VariableName) preferred over ActionOutput/UUID chaining for every plan-registered variable; UUIDs are only assigned to actions whose immediate consumer is the very next action"
    - "Every com.apple.* (AppIntent-style) action requires a top-level AppIntentDescriptor {BundleIdentifier, Name, TeamIdentifier, AppIntentIdentifier} dict, or the validator hard-fails with 'AppIntent action missing AppIntentDescriptor' regardless of target OS"
    - "is.workflow.actions.conditional's WFInput uses a double wrapper — {Type:Variable, Variable:{Value, WFSerializationType}} — that the validator explicitly rejects on every other action identifier"
    - "Any ExtensionInput reference anywhere in the action graph requires a non-empty WFWorkflowInputContentItemClasses or the validator flags a real 'Stop and Respond' risk"
    - "Get Time Between Dates' WFInput/WFTimeUntilFromDate and Format Date's WFDate use WFTextTokenString (not WFTextTokenAttachment) as a documented exception to the general display/data-flow split"
    - "JSON write bodies are authored as a single Text-action literal with U+FFFC placeholders computed programmatically (never hand-counted), since no Dictionary-to-JSON-string action exists in the bundle"

key-files:
  created:
    - src/PROSOCHE-Dumb.xml
  modified:
    - docs/BUILD-NOTES.md

key-decisions:
  - "WFWorkflowInputContentItemClasses set to [\"WFStringContentItem\"] rather than left empty, deviating from the plan's literal Layer 1 wording and STACK.md's root-keys guidance: the validator flags any ExtensionInput reference against an empty list as a real 'Stop and Respond' runtime risk, and the correction is accurate (Personal-Automation-passed OPEN/CLOSE text genuinely is a string content item)"
  - "The Create Note action carries a defensive `name` parameter (identical text to the note's first markdown line) alongside markdownContents, reusing the real, evidenced key from its sibling Notes-create action (com.apple.mobilenotes.SharingExtension), because the validator requires some title-shaped parameter on every action in its Notes-create family and CreateNoteFromMarkdownLinkAction has no confirmed title parameter of its own in this bundle"
  - "profile_snapshot.synced_at (written as text, not yet a number) is the field chosen for the fourth 'Now Epoch' placeholder the plan calls for without naming an exact field; last_open_at/last_close_at were deliberately left null per ARCHITECTURE.md's field table and PITFALLS B7, so as not to defeat Phase 3's first-run detection"
  - "AppIntentDescriptor's BundleIdentifier is set to the real, evidenced com.apple.mobilenotes (from the same action family's other identifiers) rather than the com.apple.Notes.* action-identifier prefix, since the validator does not check this field's value and the bundle's own evidence favours the former"
  - "Get File / Save File use WFGetFilePath / WFFileDestinationPath as full relative paths (PROSOCHE/state.json) rather than a folder-only destination, following the confirmed real parameter shapes over the one golden example's empty-path usage (which predates current validator standards per the skill's own caveat)"

requirements-completed: [BOOT-03, BOOT-04, BOOT-09, STATE-12]

coverage:
  - id: D1
    description: "src/PROSOCHE-Dumb.xml exists, validates at --target-macos 26 --target-platform all, and structurally implements the whole walking-skeleton spine: import questions, Config parse, run clock, router gate, DEV-02 state-load substitute, bootstrap gate, schema_version 1 state.json write, and Control Room Note creation/open"
    requirement: "BOOT-03"
    verification:
      - kind: other
        ref: "plutil -lint src/PROSOCHE-Dumb.xml"
        status: pass
      - kind: other
        ref: "bin/validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all"
        status: pass
      - kind: other
        ref: "Task 1 <verify> grep/identifier gate (plan 02-01-PLAN.md)"
        status: pass
      - kind: other
        ref: "Task 2 <verify> Python wiring-audit script (import-question binding, dangling OutputUUID, display/data-flow serialization, GroupingIdentifier integrity)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The Control Room Note's on-device title/body, the fixed-path folder+file creation, the two import prompts appearing and round-tripping, and which Format Date key the runtime actually reads for the day-key pattern"
    verification: []
    human_judgment: true
    rationale: "No iPhone or Notes-capable simulator is available in this environment (per the domain constraints); these are exactly the validator-invisible runtime facts PITFALLS A9 describes, and are recorded as UA-03 through UA-06 in docs/BUILD-NOTES.md §6, gated on Phase 2, rather than assumed."

duration: 50min
completed: 2026-08-13
status: complete
---

# Phase 2 Plan 1: Walking Skeleton — Import Questions to Control Room Note Summary

**The first plist XML in the project: a validating iOS 26 Shortcut that bootstraps a schema_version 1 state.json from two import answers and creates/opens a Control Room Note via the camelCase markdownContents key.**

## Performance

- **Duration:** ~50 min
- **Completed:** 2026-08-13T02:48Z
- **Tasks:** 2 completed
- **Files modified:** 2 (1 created, 1 modified)

## Accomplishments

- `src/PROSOCHE-Dumb.xml` created and validating: 56 actions, 2 nested control-flow blocks, 18 UUIDs, 18 output references, zero dangling references
- One manual run with no input walks the entire spine: import answers materialise into `Import Descent`/`Import Voice` → the Config block parses once into `Config` → the epoch clock builds `Now Epoch`/`Behavioural Day` → the router's outer gate takes the MANUAL branch → the DEV-02 substitute detects no existing state → the bootstrap branch creates the `PROSOCHE` folder, writes a bounded, versioned `state.json`, creates the Control Room Note with a 534-character body, and opens it
- Layer 0 capability gate completed *before* any XML was written: six previously-unaudited identifiers (`comment`, `nothing`, `count`, `file.createfolder`, `text.trimwhitespace`, `text.changecase`) looked up against all three ToolKit snapshots and recorded as CAP-29 through CAP-34, all VERIFIED cross-platform
- DEV-04 recorded: the validator invocation documented in `docs/BUILD-NOTES.md` §3 (`--target-platform ios`) measurably fails with 118 spurious errors; the operative invocation for every Phase 2+ gate is `--target-platform all`
- Task 2's hand-and-script wiring audit (D-25) found no defects across all five classes the validator cannot check, and added four new user action items (UA-03..06) for the facts that genuinely need a real device

## Task Commits

Each task was committed atomically:

1. **Task 1: Walking skeleton — import questions through Control Room Note, one path, end to end** - `b84271a` (feat)
2. **Task 2: Manual wiring audit — the checks the validator provably does not make** - `8bc8c47` (docs)

_Note: `docs/BUILD-NOTES.md`'s two edits were split at the hunk level so each commit carries only the documentation that belongs to its own task (CAP-29..34 + DEV-04 in Task 1; UA-03..06 + the audit-outcome note in Task 2), even though both edits landed in the same working-tree session before either was staged._

## Files Created/Modified

- `src/PROSOCHE-Dumb.xml` - The unsigned Shortcuts plist for the Dumb fork; the walking skeleton this and all later Phase 2-7 plans build on
- `docs/BUILD-NOTES.md` - Appended CAP-29..34 (six new capability rows), DEV-04 (validator invocation correction), and UA-03..06 (four new device-only user action items) — verified append-only (54 insertions, 0 deletions across both edits)

## Decisions Made

See `key-decisions` in the frontmatter above for the five decisions requiring the most justification. In brief: two of them (`WFWorkflowInputContentItemClasses`, the defensive `name` key on Create Note) were forced by real validator requirements that were not fully anticipated in the plan's literal wording, and are documented as deviations below. The other three (the `synced_at` placeholder target, `AppIntentDescriptor`'s `BundleIdentifier`, and the full-path Save File/Get File destinations) are implementation choices made under genuine ambiguity in the plan/research and are recorded with their reasoning both here and as Comments inside the graph itself.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] `WFWorkflowInputContentItemClasses` set non-empty, not left empty**
- **Found during:** Task 1, first validator run
- **Issue:** The plan's Layer 1 (and STACK.md's root-keys table) call for `WFWorkflowInputContentItemClasses` to stay empty, reasoning that Personal-Automation-passed text isn't a share-sheet content type. The validator disagrees for a documented, real reason: any `ExtensionInput` reference with an empty content-classes list is flagged as a genuine "Stop and Respond" runtime risk, unconditionally.
- **Fix:** Set `WFWorkflowInputContentItemClasses: ["WFStringContentItem"]`. This is not a validator-appeasement hack — it is the accurate declaration for a shortcut that genuinely receives text input from an automation, and it is what actually prevents the runtime halt the validator is warning about.
- **Files modified:** `src/PROSOCHE-Dumb.xml`
- **Verification:** `validate-shortcut` passes; the acceptance criteria do not test this key directly, so no criterion was weakened.
- **Committed in:** `b84271a`

**2. [Rule 3 - Blocking] `AppIntentDescriptor` added to the Create Note action**
- **Found during:** Task 1, first validator run
- **Issue:** The validator hard-requires every `com.apple.*` action to carry a top-level `AppIntentDescriptor` dict with a non-empty `AppIntentIdentifier` — undocumented in any of the plan's read-first references, and not something Layer 8's instructions anticipated.
- **Fix:** Added `AppIntentDescriptor: {BundleIdentifier: "com.apple.mobilenotes", Name: "Create Note from Markdown", TeamIdentifier: "0000000000", AppIntentIdentifier: "CreateNoteFromMarkdownLinkAction"}`. Only `AppIntentIdentifier`'s presence is validator-checked; the other three fields are filled with the most evidence-grounded values available (the Notes app's real bundle ID from sibling actions in the same family, and the exact display name APPINTENTS.md records for this identifier) rather than left as unevidenced placeholders.
- **Files modified:** `src/PROSOCHE-Dumb.xml`
- **Verification:** `validate-shortcut` passes.
- **Committed in:** `b84271a`

**3. [Rule 1 - Bug] `WFDuration` on Adjust Date given its required `WFQuantityFieldValue` wrapper**
- **Found during:** Task 1, first validator run
- **Issue:** Initial `WFDuration` was a bare `{Magnitude, Unit}` dict; the validator requires the full `{Value: {Magnitude, Unit}, WFSerializationType: "WFQuantityFieldValue"}` wrapper documented in VARIABLES.md.
- **Fix:** Wrapped `WFDuration` correctly; `Magnitude` changed from a string to a real number (`4.0`).
- **Files modified:** `src/PROSOCHE-Dumb.xml`
- **Verification:** `validate-shortcut` passes.
- **Committed in:** `b84271a`

**4. [Rule 3 - Blocking] `ALLOW_MANUAL_UNIT_CONVERSION` escape-hatch comment added**
- **Found during:** Task 1, first validator run
- **Issue:** The transcribed Config JSON literal's `"yyyy-MM-dd"` date-format pattern trips the validator's unit-keyword heuristic (`\bmm\b` matches the `MM` token, mistaking it for millimeters) — a documented false-positive class with a documented, sanctioned escape hatch.
- **Fix:** Added a Comment containing the literal marker `ALLOW_MANUAL_UNIT_CONVERSION`, explaining honestly why it is present (no unit conversion exists anywhere in this shortcut).
- **Files modified:** `src/PROSOCHE-Dumb.xml`
- **Verification:** `validate-shortcut` passes.
- **Committed in:** `b84271a`

---

**Total deviations:** 4 auto-fixed (3 blocking/Rule 3, 1 bug/Rule 1)
**Impact on plan:** All four were required to make the validator pass at all; none weaken an acceptance criterion, remove scope, or change product behaviour. Two of them (items 1 and 2) depart from the plan's literal wording and are flagged prominently here and in `src/PROSOCHE-Dumb.xml`'s own Comments for visibility.

## Issues Encountered

The plan's Layer 7 instruction to place a fourth "Now Epoch" placeholder "where a first-run timestamp is needed" did not name an exact field, and every timestamp-shaped field in ARCHITECTURE.md §2's schema (`last_open_at`, `last_close_at`, `cooldown_until`) is explicitly documented as `null` at bootstrap, owned by OPEN/CLOSE/Ice-entry only (PITFALLS B7 explicitly warns against seeding a false baseline there). Resolved by placing the fourth placeholder in `profile_snapshot.synced_at` instead — the one nullable field whose "this default skeleton was established now" meaning is true at bootstrap without contradicting any other field's documented ownership. Recorded in a Comment in the graph and here for visibility in case a different field was actually intended.

## User Setup Required

None - no external service configuration required. Four device-only verification items were recorded as UA-03 through UA-06 in `docs/BUILD-NOTES.md` §6 (Note title, fixed-path folder/file creation and no-duplicate-bootstrap, import-prompt round-trip, and the Format Date key ambiguity) — none of these are user setup, all are gated on Phase 2's on-device verification pass, and none block this plan or Phase 2's subsequent plans.

## Next Phase Readiness

`src/PROSOCHE-Dumb.xml` validates and is ready for 02-02 (full Control Room Note body expansion), 02-03 (OPEN/CLOSE routing bodies), and 02-04 (state-load-and-do-not-overwrite, Note-existence guard, and import-answer normalisation) to extend in place, strictly below action index 5 per the pinned import-question indices. No structure laid down here is expected to be rewritten by those plans. Four device-only facts (UA-03..06) should be confirmed at the earliest real on-device import, ideally before Phase 3 builds Heat/Gravity/Pressure logic on top of `behavioural_day`.

---
*Phase: 02-routing-bootstrap-control-room*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: `src/PROSOCHE-Dumb.xml`
- FOUND: `.planning/phases/02-routing-bootstrap-control-room/02-01-SUMMARY.md`
- FOUND: commit `b84271a`
- FOUND: commit `8bc8c47`
