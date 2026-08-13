---
phase: 02-routing-bootstrap-control-room
verified: 2026-08-13T15:00:00Z
status: passed
score: 5/5 must-haves verified
behavior_unverified: 0
overrides_applied: 0
---

# Phase 2: Routing, Bootstrap & Control Room Onboarding Verification Report

**Phase Goal:** A user can import the Shortcut, run it manually for the first time, and get a working state.json plus a fully instructive Control Room Note — and every subsequent invocation routes correctly and never corrupts or duplicates that foundation.

**Verified:** 2026-08-13T15:00:00Z
**Status:** passed
**Re-verification:** No — initial verification

**Domain note:** This is a Shortcuts-plist project with no build/test tooling. `validate-shortcut` is the test runner and passes, but a green validator only proves plist structure/parameter-shape correctness, never runtime behaviour (per DEV-04/PITFALLS A9). All findings below come from directly parsing `src/PROSOCHE-Dumb.xml` with `plistlib` and walking its `GroupingIdentifier`/`WFControlFlowMode` control-flow structure programmatically — not from trusting SUMMARY.md prose. No iPhone or Notes-capable simulator is available in this environment, so the on-device-only facts the project itself already tracks as `UA-01` through `UA-07` in `docs/BUILD-NOTES.md` §6 are reported as pre-existing, correctly-scoped, non-blocking context below, per the domain instructions — not re-flagged as gaps or as human-verification items.

## Goal Achievement

### Observable Truths (ROADMAP Success Criteria)

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | No input, `OPEN`, and `CLOSE` each route to the correct branch using iOS-26-compatible nested If/Otherwise; unrecognised/empty input fails safe without corrupting state or hanging | ✓ VERIFIED | Direct plist walk of all 34 `is.workflow.actions.conditional` actions across 13 `GroupingIdentifier` blocks: every block is a well-formed `[0]`, `[0,1]`, or `[0,1,2]` sequence (open/otherwise/close), all 13 balance to an empty stack at EOF, and **zero** mode-1 (`Otherwise`) actions carry a `WFCondition`/`WFConditionalActionString` — i.e. zero `Otherwise If` (macOS-27-only) anywhere in the file. Traced the router by index: outer gate `F646324A` (has-any-value on `Input Key`, index 89) — TRUE branch (90-103) nests `FA045F2B` (`OPEN` string-equals, index 91) then `A2F7247B` (`CLOSE` string-equals, index 96) then the fail-safe (Comment+Alert, index 100-101); FALSE/Otherwise (104-131) is the Control Room path. Confirmed: empty `Input Key` → outer gate false → MANUAL/Control Room only; `OPEN` → indices 92-93 only (Comment+`Nothing`, zero state mutation); `CLOSE` → indices 97-98 only (Comment+`Nothing`, zero state mutation); anything else non-empty → indices 100-101 only (one `Comment` + exactly one `is.workflow.actions.alert`, confirmed to contain no Save/Get File, Set/Get Dictionary Value, Create Folder, Note action, Ask, or Wait in that region). Each of the four cases reaches exactly one, non-overlapping destination. |
| 2 | First manual run creates a schema-valid, bounded, versioned `state.json` with initial profile/fork/config from the import questions (descent default Limbo, voice permission) | ✓ VERIFIED | `WFWorkflowImportQuestions` binds to `ActionIndex` 2 and 4; both indices are confirmed `is.workflow.actions.gettext` actions carrying `WFTextActionText` (`ParameterKey`), i.e. the binding target is real and correctly typed — **this is the exact positional-binding fact most likely to have silently broken across 4 edit waves, and it is intact.** Default values `Limbo`/`yes` confirmed on the question dicts. The bootstrap-branch JSON template (index 75) is a literal `{...}` with `"schema_version": 1` (versioned), `recent_sessions: []`, `recent_contracts: []`, and all six `exit_stats[*].samples: []` (bounded — no unbounded arrays, no CSV). All 4 `attachmentsByRange` placeholders in this literal byte-verified against their `string` (every placeholder points at an actual U+FFFC char, placeholder-count == range-count, checked across **every** `WFTextTokenString` field in the file — zero mismatches file-wide) and resolve to `Descent Normalised`, `Voice Normalised`, `Behavioural Day`, `Now Epoch`. Descent normalisation (indices 54-65): `Paradise`→copy, `Inferno`→copy, else (including typos/`Limbo` itself)→literal `Limbo` (index 62). Voice normalisation (indices 68-72): `yes`→literal `true` (index 66), else→literal `false` (index 67) — written unquoted into `"voice_enabled": ￼` so it round-trips as a real JSON boolean, not a string. |
| 3 | First manual run creates exactly one non-empty `PROSOCHĒ — Control Room` Note with READ THIS FIRST, Automation A/B steps, cannot-self-install + bypassable statement, essential-apps warning, and the `MY PHONE, ON PURPOSE` proforma | ✓ VERIFIED | Read the full 5,121-char literal at index 120 directly (not the SUMMARY's paraphrase). Confirmed present verbatim: `## READ THIS FIRST` (explains what PROSOCHĒ does, states "This Shortcut cannot create its own automations" and "PROSOCHĒ is bypassable" unhedged); `### Automation A — OPEN` (10 numbered steps: App trigger, select apps, Is Opened, disable "Ask Before Running", Run Shortcut, exact name `PROSOCHĒ — Nine Circles — Dumb`, input `OPEN`); `### Automation B — CLOSE` (10 numbered steps, mirrored, `Is Closed`, input `CLOSE`, same shortcut name repeated identically); `## Do not target these apps` naming Phone, Messages, Maps, Wallet, an authenticator, a password manager (superset of the ROADMAP's essential-apps list); `## MY PHONE, ON PURPOSE` with all 6 sub-heading prompts, the 4th of which names all six exits (Capture, Coordinate, Create, Connect, Consult, Close). The action is `com.apple.Notes.CreateNoteFromMarkdownLinkAction` (the sole Note-creation action in the file, confirmed by full-file identifier count) using the camelCase key `markdownContents` (confirmed literally, not `markdown`), bound via its own `attachmentsByRange` entry to the `Control Room Body` variable — never empty. |
| 4 | Later manual runs never overwrite existing state or create a duplicate Control Room Note | ✓ VERIFIED | Whole-file identifier count: exactly **one** `is.workflow.actions.documentpicker.save` (index 79) in all 133 actions, and exactly **one** `com.apple.Notes.CreateNoteFromMarkdownLinkAction` (index 123). Control-flow-path trace (deep-copied stack, not aliased) confirms: Save File's path is `6D32F6F2:false` — i.e. it only executes on the Otherwise (no-value) side of the `State Present == "yes"` gate. Note-creation's path is `F646324A:false > D703FE92:false` — only on the Otherwise (no-value) side of the `Note Present == "yes"` gate, itself only reachable on the MANUAL branch. A second Save File or Note-creation action anywhere else in the graph would break this guarantee; none exists. |
| 5 | Missing/corrupt `state.json` and a deleted Control Room Note each trigger safe self-healing from any invocation mode | ✓ VERIFIED | The entire state-load-and-bootstrap chain (`Get File` index 23 through the `6D32F6F2` block's close at index 82) sits structurally **before** index 83's input-normalisation and the router's index-89 gate — confirmed by direct index-order comparison, with zero conditionals anywhere between index 0 and index 23. This chain therefore executes identically for MANUAL, OPEN, and CLOSE before routing ever branches. `Get File` (index 23) has `WFFileErrorIfNotFound: False` (DEV-02 substitute, confirmed). Corruption/absence is unified by a real 3-condition AND gate (indices 37/39/41: `schema_version` has-any-value AND `schema_version` string-equals `"1"` AND `profile` has-any-value) computed via the shared-literal accumulator pattern (default "no" set at index 35 before the nested chain; overridden to "yes" only if all three hold, at index 42; canonically copied to `State Present` at index 46, its only assignment) — a missing file, an unparseable file (Detect Dictionary yields no dictionary → key lookups yield empty), an old-schema file, and a profile-less file are all structurally indistinguishable and all take the identical rebuild branch. The Note-existence guard (`filter.notes` index 106, condition code 99/"contains" — not the documented exact-match trap, code 4 — on the exact title string) drives `Note Present` via the identical accumulator pattern, and reuse-vs-recreate (index 114) recreates using the **same** full 5,121-char `Control Room Body` literal, not a lesser placeholder. This guard is scoped to the MANUAL branch only (confirmed: `filter.notes`/`appendnote`/`shownote`/the Note-create action all trace to `F646324A:false`; none appear on the `F646324A:true` OPEN/CLOSE side), matching the documented cost/safety rationale in `docs/BUILD-NOTES.md` §10. |

**Score:** 5/5 truths verified (0 present, behavior-unverified)

### Structural Integrity Checks (whole-file, programmatic)

| Check | Method | Result |
|---|---|---|
| Control-flow balance | Deep stack-walk of all 34 conditional actions / 13 groups | 13/13 groups well-formed, 0 unbalanced, 0 `Otherwise If` |
| Dangling `OutputUUID` references | Cross-referenced every `UUID` field against every `OutputUUID` reference | 30 assigned, 30 referenced, 0 dangling |
| Dangling `VariableName` references | Cross-referenced every `WFVariableName` (set) against every `VariableName` (read) | 21 distinct variables set, 0 read-before-set |
| `attachmentsByRange` byte-integrity | Verified every `WFTextTokenString` field file-wide: placeholder count == range count, and each range points at an actual U+FFFC char | 0 mismatches across the state.json template, Note body, fail-safe alert, and Find Notes filter |
| `WFWorkflowImportQuestions` positional binding | Confirmed `ActionIndex` 2 and 4 are `is.workflow.actions.gettext` actions with `WFTextActionText` present | Intact |
| Validator | `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` (per DEV-04's corrected invocation, not the stale `--target-platform ios` in §3) | Passed, 0 errors |
| `plutil -lint` | Structural plist sanity | OK |
| Action/comment/block counts | `plistlib` count vs. SUMMARY claims | 133 actions, 34 comments, 34 conditional actions / 13 blocks — matches 02-04-SUMMARY's own count exactly |

### Integrity Check — Identifier ↔ BUILD-NOTES cross-reference

All 22 distinct `WFWorkflowActionIdentifier` values used anywhere in `src/PROSOCHE-Dumb.xml` (not just 4 spot-checked — every one) were grepped against `docs/BUILD-NOTES.md`:

| Identifier | Row in BUILD-NOTES §4/§7 | Match |
|---|---|---|
| `com.apple.Notes.CreateNoteFromMarkdownLinkAction` | CAP-08 | ✓ |
| `is.workflow.actions.filter.notes` | CAP-07 | ✓ |
| `is.workflow.actions.appendnote` | CAP-09 | ✓ |
| `is.workflow.actions.shownote` | CAP-10 | ✓ |
| `is.workflow.actions.getvalueforkey` | CAP-05 | ✓ |
| `is.workflow.actions.date`/`adjustdate`/`format.date`/`gettimebetweendates` | CAP-06 | ✓ |
| `is.workflow.actions.documentpicker.open`/`.save` | CAP-02/CAP-03 | ✓ |
| `is.workflow.actions.detect.dictionary` | CAP-04 | ✓ |
| `is.workflow.actions.getitemfromlist` | CAP-S06 | ✓ |
| `is.workflow.actions.setitemname` | CAP-S08 | ✓ |
| `is.workflow.actions.comment`/`nothing` | CAP-29/CAP-30 | ✓ |
| `is.workflow.actions.file.createfolder` | CAP-32 | ✓ |
| `is.workflow.actions.text.trimwhitespace`/`.changecase` | CAP-33/CAP-34 | ✓ |
| `is.workflow.actions.alert`/`conditional`/`gettext`/`setvariable` | CAP-S07/CAP-S04/CAP-S02/CAP-S01 | ✓ |

No identifier used in the graph is absent from the audit table — 0 blocking defects. Also spot-checked two evidence-cell claims directly against the graph: CAP-34's claim that Change Case wires via the lowercase `text` key (not `WFInput`) while the adjacent Trim Whitespace uses `WFInput` — confirmed exactly at indices 85/86; CAP-07's Find Notes "condition 99, never 4" trap — confirmed at index 106 (`Operator: 99`).

### Requirements Coverage

| Requirement | Status | Evidence |
|---|---|---|
| BOOT-01 | ✓ Satisfied | Truth 1 above |
| BOOT-02 | ✓ Satisfied | Truth 1 above (fail-safe region structurally inert) |
| BOOT-03 | ✓ Satisfied | Truth 2 above |
| BOOT-04 | ✓ Satisfied | Truth 3 above |
| BOOT-05 | ✓ Satisfied | Truth 4 above |
| BOOT-06 | ✓ Satisfied | Truth 5 above (hoisted state load) |
| BOOT-07 | ✓ Satisfied | Truth 5 above (3-condition AND validity gate) |
| BOOT-08 | ✓ Satisfied | Truth 5 above (Note-existence guard) |
| BOOT-09 | ✓ Satisfied | Truth 2 above (import questions + normalisation) |
| STATE-12 | ✓ Satisfied | Truth 2 above (versioned, bounded schema) |
| ROOM-01 through ROOM-06 | ✓ Satisfied | Truth 3 above (full Note body read directly) |

All 16 requirements REQUIREMENTS.md maps to Phase 2 are covered; none orphaned (cross-checked REQUIREMENTS.md's Traceability table — all 16 rows say "Phase 2 / Complete", matching the plan `requirements-completed` fields across all four SUMMARY.md files with no gaps).

### Anti-Patterns Found

Grepped `src/PROSOCHE-Dumb.xml` for `TBD|FIXME|XXX|TODO|HACK|not yet implemented|coming soon` — **zero matches**. The two "Known Stubs" the SUMMARY files self-report (OPEN/CLOSE branch anchors as `Comment`+`Nothing`; the Note body's `CURRENT STATE`/`ATTENTION LEDGER`/`VALUE-LIFE-RETURNED`/`SUPPORT-PROSOCHĒ` sections as static first-run text) are correctly and honestly documented, explicitly owned by Phase 3/4/7 per the ROADMAP, contain zero state mutation on the OPEN/CLOSE side, and do not block Phase 2's own goal — confirmed by direct read of both, not just by trusting the self-report label.

### Documentation bookkeeping note (non-blocking)

`.planning/ROADMAP.md`'s Progress table (bottom of file) still shows Phase 2's `Status` column as "In Progress" with an empty `Completed` date, even though the top-level phase checkbox and `Plans: 4/4` line are both marked complete and 02-04-SUMMARY.md's "Files Created/Modified" section claims "the Progress table's Phase 2 row all flipped to complete." Direct read of the table shows this specific claim is **not accurate** — the `Plans Complete` column (`4/4`) was updated but the `Status`/`Completed` columns were not. This is a documentation-bookkeeping gap in ROADMAP.md, not a defect in `src/PROSOCHE-Dumb.xml` or in any of the five ROADMAP success criteria, and does not affect this verdict — flagged here as an example of a SUMMARY claim that did not hold up under direct re-check, per this agent's adversarial mandate, and worth a one-line fix before Phase 3 starts.

### On-device-only facts (context, not gaps — per domain instructions)

`docs/BUILD-NOTES.md` §6 already tracks seven device-only facts (`UA-01`, `UA-03` through `UA-07`) this phase's structural proofs cannot close without a real iPhone: Note title/body rendering, fixed-path folder/file creation, import-prompt round-trip, the `format.date` custom-pattern ambiguity, and the two BOOT-05/BOOT-08 on-device confirmations. All seven are correctly gated on Phase 2, all are honestly labelled (not silently assumed), and none are claimed as closed anywhere in the four SUMMARY.md files. Per the domain instructions for this environment (no iPhone or Notes-capable simulator available), these are reported here as pre-existing, already-well-scoped context and are **not** listed as gaps or as new human-verification items — the project's own tracking of them is itself part of what makes Phase 2 correct.

## Gaps Summary

None. All five ROADMAP Phase 2 success criteria are structurally verified by direct `plistlib` inspection of `src/PROSOCHE-Dumb.xml` — not by trusting SUMMARY.md prose. Zero dangling references, zero unbalanced control-flow blocks, zero `Otherwise If` occurrences, zero duplicate writer actions, zero identifiers absent from the BUILD-NOTES audit table, zero debt markers. The one inaccurate claim found (the ROADMAP Progress-table row) is cosmetic bookkeeping, not a functional or requirements gap, and is noted above for a quick fix rather than blocking phase closure.

---

*Verified: 2026-08-13*
*Verifier: Claude (gsd-verifier)*
