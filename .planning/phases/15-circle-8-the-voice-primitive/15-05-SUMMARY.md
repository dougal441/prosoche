---
phase: 15-circle-8-the-voice-primitive
plan: 05
subsystem: infra
tags: [shortcuts-plist-generator, ios-shortcuts, aea1-signing, manifest-provenance, build-notes]

# Dependency graph
requires:
  - phase: 15-circle-8-the-voice-primitive
    plan: 01
    provides: "mirror()/voice() split, verify_speaktext_placement()"
  - phase: 15-circle-8-the-voice-primitive
    plan: 02
    provides: "spike 011's rung-2 verdict (not discriminated), Branch B routing"
  - phase: 15-circle-8-the-voice-primitive
    plan: 03
    provides: "voice_enabled numeric normalisation, schema_version 4->5, verify_voice_enabled_seed()"
  - phase: 15-circle-8-the-voice-primitive
    plan: 04
    provides: "verify_voice_gates(), verify_voice_path_volume_silence(), the action-equality dispatch assertion"
provides:
  - "Both forks rebuilt, gate-A clean, re-signed under exact display names and asserted by AEA1 decrypt (11 speaktext, 15 setvolume, schema_version 5, both forks)"
  - "artifacts/shortcuts/MANIFEST.md's deliberate red (carried since wave 1) closed by re-signing and re-deriving, never by row editing"
  - "docs/BUILD-NOTES.md section 36 -- the phase's complete recording duty: six locked decisions, four declined alternatives, the rung-2 probe verdict with its evidence rung, measured counts, and CIRC-08's device status"
  - "A cold-runnable, digest-pinned device UAT instrument (15-UAT.md) with honest initial statuses"
  - "The superseded Circle-8 todo closed with its residue (the still-open axis-4 blocker) named"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "MANIFEST supersession discipline: the file's single live pipe-table is updated in place per rebuild; a superseded table is converted to prose (backtick-wrapped hash/byte mentions) rather than left as a second table, because docs/manifest_check.py scans every pipe-row in the whole document and would otherwise assert stale rows too"

key-files:
  created:
    - .planning/phases/15-circle-8-the-voice-primitive/15-UAT.md
  modified:
    - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut
    - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut
    - artifacts/shortcuts/MANIFEST.md
    - docs/BUILD-NOTES.md
    - .planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md (moved to completed/)

key-decisions:
  - "No code was changed by this plan. src/PROSOCHE-Dumb.xml and src/PROSOCHE-Sentient.xml rebuild byte-identical to the wave 1-3 committed state (git status --short -- src/ empty, measured, not assumed) -- this plan's job was exclusively to sign, assert, record and instrument what those three waves already built."
  - "The superseded MANIFEST table was converted to prose rather than deleted or left as a second live table, preserving this file's own convention that nothing is ever silently removed while keeping docs/manifest_check.py's row-scan correct."
  - "CAPABILITY-DECISIONS.md was left unchanged: spike 011's verdict (not discriminated at rung 2) settled no capability question, so nothing was added there per the plan's own instruction against logging a non-result as a result."

patterns-established: []

requirements-completed: [CIRC-08, CIRC-14, DIST-01]

coverage:
  - id: D1
    description: "Both forks are signed under their exact display names and the shipped payload is asserted by AEA1 decrypt, never inferred from an mtime"
    requirement: "DIST-01"
    verification:
      - kind: other
        ref: "validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all -> Validation passed."
        status: pass
      - kind: other
        ref: "validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all -> Validation passed."
        status: pass
      - kind: other
        ref: "aea decrypt + aa extract + plutil on both signed .shortcut files -> 11 speaktext, 15 setvolume, schema_version 5, both forks"
        status: pass
    human_judgment: false
  - id: D2
    description: "artifacts/shortcuts/MANIFEST.md carries a new block whose hashes/bytes are re-derived from the signed files, and docs/manifest_check.py exits 0"
    verification:
      - kind: other
        ref: "python3 docs/manifest_check.py -> manifest check: passed (6 rows verified against disk)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Every decision this phase made -- D-01 through D-06, the declined alternatives, and the probe verdict -- is recorded in docs/BUILD-NOTES.md"
    requirement: "CIRC-08"
    verification:
      - kind: other
        ref: "python3 -c \"... assert '## 36.' in b and all D-0N tokens present and Eject/Phase 17 untouched ...\" -> recording duty ok"
        status: pass
    human_judgment: false
  - id: D4
    description: "CIRC-08's device status is stated plainly: structurally proven, behaviourally unproven per plan 15-02's verdict"
    requirement: "CIRC-08"
    verification:
      - kind: other
        ref: "docs/BUILD-NOTES.md section 36.6, MANIFEST.md plan-15-05 block, 15-UAT.md head-of-file warning -- all three state it in the same words, in the same place as the claims they qualify"
        status: pass
    human_judgment: true
    rationale: "This is a documentation-honesty property, not a mechanically checkable one beyond string presence -- a human should confirm the three records agree and none implies a device pass."
  - id: D5
    description: "A cold-runnable device UAT instrument exists, pinned to this build's signed digests"
    requirement: "CIRC-08"
    verification:
      - kind: other
        ref: "python3 -c \"... 2 sha256 digests, Circle 8, Circle 7, Toggle Voice all present ...\" -> uat instrument ok"
        status: pass
    human_judgment: false
  - id: D6
    description: "All twelve docs/*.py checkers exit 0 in one run, including manifest_check.py"
    verification:
      - kind: other
        ref: "state_engine_self_check, phase5/6/7/9_self_check, sentient_audit_check, sentient_core_check, environmental_restore_check, router_ui_census, sequence_dispatch_check, note_identity_check, manifest_check -- all exit 0"
        status: pass
    human_judgment: false

duration: ~10min
completed: 2026-08-18
status: complete
---

# Phase 15 Plan 05: Ship the Phase -- Rebuild, Sign, Assert, Record, Instrument Summary

**Re-signed both forks after confirming byte-identical rebuilds (no code changed by this plan), decrypt-asserted 11 speaktext / 15 setvolume / schema_version 5 on each, re-derived MANIFEST.md's provenance block to close the deliberate red carried since wave 1, wrote docs/BUILD-NOTES.md section 36 recording all six locked decisions and the rung-2 probe's evidence-ranked verdict, authored a digest-pinned 15-UAT.md, and closed the superseded Circle-8 todo with its axis-4 residue named.**

## Performance

- **Duration:** ~10 min (Task 1 through Task 3 commits)
- **Started:** 2026-08-18T21:41:00+10:00 (approx, first build run)
- **Completed:** 2026-08-18T21:49:35+10:00
- **Tasks:** 3 completed
- **Files modified:** 5 (2 signed .shortcut artifacts, MANIFEST.md, BUILD-NOTES.md, plus 2 new dated archive XMLs) + 1 new file (15-UAT.md) + 1 moved file (the closed todo)

## Accomplishments

- Confirmed the build-provenance gate passes, rebuilt both forks, and measured `git status --short -- src/` empty afterward -- both forks were already at their final Phase 15 state from waves 1-3, so this plan changed no generator code and no emitted action
- Gate A clean on both forks (`--target-macos 26 --target-platform all`, `Validation passed.`, exit 0)
- Signed both forks under their exact display names with no `_signed` suffix (`.claude/CLAUDE.md` §8's Dumb/Sentient wording is stale; `docs/manifest_check.py`'s DIST-04 assertion is the authority, used correctly here)
- Recovered both signed payloads via the AEA1 workflow (`aea decrypt` → `aa extract` → `plutil -convert xml1`) and measured directly from the decrypted plist, not `src/`: 11 `speaktext` sites (was 22), 15 `setvolume` sites (unchanged), `schema_version` 5 (was 4) -- identical on both forks
- Added a new leading block to `artifacts/shortcuts/MANIFEST.md` with hashes/bytes re-derived from the signed files, stating plainly that the build is structurally proven and CIRC-08 is behaviourally unproven, and that this build is not the one currently installed on the developer's iPhone (which holds the older `b07497ba…` Core build)
- Converted the now-superseded live table (the six rows the file's earlier structure carried as its "current" table) to prose, so `docs/manifest_check.py` -- which scans every pipe-delimited row in the whole document -- asserts only this build's six rows; `python3 docs/manifest_check.py` now exits 0, closing the deliberate red every wave since wave 1 recorded
- Wrote `docs/BUILD-NOTES.md` §36: all six locked decisions (D-01 through D-06) with reasoning and measured consequence, D-01's accepted cost stated unpapered (Circles 7/8 indistinguishable with voice off, both mitigations offered and declined), the four declined alternatives (mode parameter, separate escalated templates, dual-type/dual-key schema fix, the five omitted `speaktext` parameters recorded as a do-not-fabricate deviation), the Status-line consequence of D-05, plan 15-02's rung-2 probe verdict transcribed with its evidence rung and rung-2-ceiling analysis, measured counts, and CIRC-08's device status stated plainly
- Added supersession pointers at §19.7 (naming Phase 11 as what closed the dispatch half and Phase 15 as what closed the design half) and §34 (a one-line pointer to §36); neither deleted a section heading, and §34's Circle-6 `Eject`/Phase 17 subsection is untouched
- Authored `.planning/phases/15-circle-8-the-voice-primitive/15-UAT.md`: a cold-runnable instrument pinned to both signed SHA-256 digests, instrumenting all four manual-only behaviours from `15-VALIDATION.md`, with a head-of-file warning stating Tests 1-3 are expected to fail with the known axis-4 error and a pointer to the still-pending blocker todo
- Closed `.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md` (moved to `completed/`) with a closing note naming Phase 15's delivering plans for each Solution step and explicitly carrying forward the still-open axis-4 blocker todo as residue -- left that todo untouched and pending, since plan 15-02 Branch A (a one-line generator fix) was never reached
- All twelve `docs/*.py` checkers exit 0 in one run

## Task Commits

Each task was committed atomically:

1. **Task 1: rebuild, validate, sign both forks, and assert the shipped payload** - `0870817` (feat)
2. **Task 2: the recording duty -- BUILD-NOTES §36 and the supersession notes** - `5dbde9a` (docs)
3. **Task 3: author the device UAT instrument and close out the superseded todo** - `a5377ae` (docs)

**Plan metadata:** (this commit, pending)

## Files Created/Modified

- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut`, `… — Aware.shortcut` -- re-signed, no `_signed` suffix
- `artifacts/shortcuts/2026-08-18/PROSOCHĒ — Nine Circles — Core-214110.xml`, `…-214122.xml` -- new dated pre-sign archives, byte-identical to `src/`
- `artifacts/shortcuts/MANIFEST.md` -- new leading block with re-derived hashes/bytes; the now-superseded live table converted to prose so the checker's document-wide row scan asserts only the current build
- `docs/BUILD-NOTES.md` -- new §36 (the phase's full recording duty); §19.7 and §34 gained supersession pointers, no heading deleted
- `.planning/phases/15-circle-8-the-voice-primitive/15-UAT.md` -- new, cold-runnable, digest-pinned, four tests, honest initial statuses
- `.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md` -- moved to `.planning/todos/completed/`, closing note added

## Decisions Made

- **No code changed.** This plan's `git status --short -- src/` measurement (empty, both times it was run) confirms plans 15-01/15-03/15-04 already left both forks at their final Phase 15 state; this plan's entire job was signing, provenance assertion, recording, and instrumenting.
- **The superseded MANIFEST table was converted to prose, not deleted.** `docs/manifest_check.py` scans every pipe-delimited row in the whole document for its coverage and per-row assertions, so leaving two live 6-row tables would have made it assert stale rows (4 signed rows found instead of 2, or a stale-hash failure). Converting the superseded table's values to the same backtick-wrapped prose form the file already uses for every earlier rebuild's history kept the record intact while giving the checker exactly one table to verify.
- **`docs/CAPABILITY-DECISIONS.md` left unchanged.** Spike 011's verdict (`not discriminated at rung 2`) named no identifier and settled no capability question -- per the plan's own instruction, a capability record that logs a non-result as a result is worse than no record.

## Deviations from Plan

None -- plan executed exactly as written. The plan itself anticipated that no code would change ("CIRC-08's honest status... unless plan 15-02's verdict identified a one-line class fix that was absorbed, Circle 8 inherits the axis-4 unfilled-picker defect") and that is exactly what plan 15-02's verdict (Branch B, no fix) produced.

## Issues Encountered

None requiring a fix. One structural discovery during Task 1: the MANIFEST file has exactly one live pipe-table (not one per rebuild) that every prior rebuild updated in place, with all history carried as prose paragraphs above and below it -- this was confirmed by scanning the whole document for pipe-rows before editing, rather than assumed, after `docs/manifest_check.py`'s document-wide row scan made the distinction load-bearing.

## User Setup Required

None -- no external service configuration required.

## Next Phase Readiness

- **Phase 15 is complete.** All five plans (15-01 through 15-05) are executed and committed. `docs/manifest_check.py` is green for the first time since wave 1 of this phase.
- **CIRC-08 remains device-unproven.** The Mirror primitive both `mirror()` and `voice()` are built on carries a device-reproduced axis-4 unfilled-picker defect that this phase did not close (`.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md`, still pending). `docs/BUILD-NOTES.md` §36, `artifacts/shortcuts/MANIFEST.md`'s plan-15-05 block, and `15-UAT.md`'s head-of-file warning all say so in the same words.
- **This signed build is not installed on the developer's iPhone.** The last device session ran against the older `b07497ba…` Core build. Per plan 15-03's recorded sequencing constraint (carried into `15-UAT.md`'s batching note), this Phase-15 build must be installed **before** the next Pressure-accumulation UAT session, never after -- the `schema_version` 4→5 bump wipes accumulated behavioural state on first run.
- **`15-UAT.md` joins the standing device backlog** (`16-UAT.md`, `12-UAT.md` Test 3, `13-UAT.md`, `10-UAT.md`, Phase 19's sweep), all blocked on DIST-03 (a paired iPhone with no live tunnel).
- No blockers for the next phase in the ROADMAP.

---
*Phase: 15-circle-8-the-voice-primitive*
*Completed: 2026-08-18*

## Self-Check: PASSED

- FOUND: 0870817 (Task 1 commit)
- FOUND: 5dbde9a (Task 2 commit)
- FOUND: a5377ae (Task 3 commit)
- FOUND: artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut
- FOUND: artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut
- FOUND: artifacts/shortcuts/MANIFEST.md
- FOUND: docs/BUILD-NOTES.md
- FOUND: .planning/phases/15-circle-8-the-voice-primitive/15-UAT.md
- FOUND: .planning/todos/completed/2026-08-16-build-circle-8-voice-primitive.md
