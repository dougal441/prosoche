---
phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
plan: 05
subsystem: infra
tags: [shortcuts, plist, signing, aea1, manifest, device-uat, build-notes, ship-gate]

# Dependency graph
requires:
  - phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
    plan: "12-04"
    provides: "profile_snapshot.create_target_url seeded and gated; verify_state_seed() generalised to every literal State/Reloaded State read; all three chartered state-shape sentinel gaps closed at the source level"
provides:
  - "Both forks rebuilt from a clean tree, gate A clean, gate B advisory-read and recorded, signed under their exact live display names (Core / Aware, no _signed suffix)"
  - "All six artifacts/shortcuts/MANIFEST.md rows refreshed and python3 docs/manifest_check.py passing — the twelfth checker, previously red pending re-signing, now green"
  - "Both signed artifacts decrypted via the AEA1 recipe and confirmed to carry schema_version 4, a four-leaf active_session, and exit_events == [] in the recovered bootstrap template"
  - "12-UAT.md — a cold-runnable seven-test device UAT for the exit-recording path, honestly BLOCKED (DIST-03, no connected device), with a tracked pending todo carrying both artifacts' SHA-256s"
  - "docs/BUILD-NOTES.md §27 — the phase's full recording duty: A1/A2/A3/A5 assumptions, PD-1/PD-2/PD-3 decisions, four measured research corrections, and both forks' verbatim gate B baselines"
affects: [ship-gate, DIST-03, phase-13-and-later]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "AEA1 decrypt-and-inspect as a Craig-Loop-adjacent post-sign verification step: recover the leaf certificate, aea decrypt, aa extract, plutil-convert, then assert the bootstrap template's shape against what actually shipped rather than trusting the unsigned source plus a file mtime"
    - "A blocked device UAT still produces a durable artifact: a cold-runnable test document plus a pending todo carrying the exact artifact hashes it was written against, so a later run can confirm build identity before trusting any recorded outcome"

key-files:
  created:
    - ".planning/phases/12-state-shape-sentinel-gaps-exit-events-and-active-session/12-UAT.md"
    - ".planning/todos/pending/2026-08-17-phase-12-exit-recording-device-uat.md"
  modified:
    - "artifacts/shortcuts/MANIFEST.md"
    - "docs/BUILD-NOTES.md"

key-decisions:
  - "MANIFEST.md's Bytes column switched from comma-thousands formatting to plain digits, so the plan's own automated verify block (which checks str(size) as a literal substring) and manifest_check.py (which already strips commas) both pass unambiguously without a parsing special-case"
  - "The plan's acceptance criterion asking for the recovered plist's WFWorkflowName to equal the artifact basename is unsatisfiable as literally stated — the signer strips WFWorkflowName entirely, a fact already measured and recorded in Phase 11 (CLAUDE.md §8, this MANIFEST's own prose). Verified instead via filename discipline (exact display name, no suffix), which is CLAUDE.md's own stated rule that the filename is the sole carrier of display name"
  - "12-UAT.md's verdict is BLOCKED, following the Phase 10/Phase 9 no-fabrication precedent exactly: xcrun devicectl list devices reported \"No devices found.\", so no simulator run, decrypted-artifact inference, or Mac import was substituted for a device observation"
  - "docs/CAPABILITY-DECISIONS.md left untouched: Task 2's UAT never ran on a device, so no capability question was settled; an empty capability record is correct here, not a gap"

patterns-established:
  - "Post-sign AEA1 decrypt-and-inspect as the final structural proof step before a build is considered shipped, distinct from and stronger than trusting the pre-sign unsigned XML"

requirements-completed: [SESS-07, STATE-12, EXIT-01, EXIT-02, SAFE-01]

coverage:
  - id: D1
    description: "Both forks rebuild clean, pass gate A, and are signed under their exact live display names with no _signed suffix, each a non-zero-byte AEA1 archive"
    requirement: "STATE-12"
    verification:
      - kind: integration
        ref: "provenance gate + python3 tools/build_state_engine.py + python3 tools/build_sentient.py + twelve docs/*.py checkers + validate-shortcut --target-macos 26 --target-platform all on both forks + python3 -c '...' asserting AEA1 magic bytes, non-zero size, no _signed suffix"
        status: pass
    human_judgment: false
  - id: D2
    description: "Gate B is read as a standalone advisory command per fork and shows exactly the one permitted com.apple.mobilenotes.SharingExtension / WFCreateNoteInput waiver line, nothing else"
    requirement: "STATE-12"
    verification:
      - kind: integration
        ref: "validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 27 --target-platform all (Core index 4192); validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 27 --target-platform all (Aware index 4260); both recorded verbatim in docs/BUILD-NOTES.md §27"
        status: pass
    human_judgment: false
  - id: D3
    description: "All six MANIFEST.md rows match disk (size + SHA-256 recomputed) and python3 docs/manifest_check.py exits 0"
    requirement: "STATE-12"
    verification:
      - kind: integration
        ref: "python3 docs/manifest_check.py — 'manifest check: passed (6 rows verified against disk)'"
        status: pass
    human_judgment: false
  - id: D4
    description: "Each signed artifact's decrypted payload (AEA1 -> aea decrypt -> aa extract -> plutil) confirms schema_version 4, a four-leaf active_session dict, and exit_events == [] in the recovered bootstrap template"
    requirement: "STATE-12"
    verification:
      - kind: integration
        ref: "python3 .aea-verify/check_recovered.py against both recovered Shortcut.xml payloads — schema_version 4, active_session four-leaf dict, exit_events [] on both forks"
        status: pass
    human_judgment: false
  - id: D5
    description: "12-UAT.md exists, is cold-runnable, carries an explicit BLOCKED verdict with the verbatim xcrun devicectl probe output, and leaves every result field blank rather than substituting non-device evidence"
    requirement: "SESS-07"
    verification:
      - kind: manual_procedural
        ref: ".planning/phases/12-state-shape-sentinel-gaps-exit-events-and-active-session/12-UAT.md — seven tests, all outcome fields blank, Verdict blank, pending todo opened carrying both artifacts' SHA-256s"
        status: unknown
    human_judgment: true
    rationale: "This deliverable is intentionally BLOCKED — it requires a real iPhone, which xcrun devicectl reported as unavailable. A human must run the actual seven device tests later; no automated check can substitute for that observation, which is the entire point of the no-fabrication rule this deliverable follows."
  - id: D6
    description: "docs/BUILD-NOTES.md carries a Phase 12 recording-duty section naming every assumption (A1-A3, A5), decision (PD-1-3), measured research correction, and gate B baseline, and docs/CAPABILITY-DECISIONS.md is correctly left untouched since the UAT never ran on device"
    requirement: "EXIT-01"
    verification:
      - kind: integration
        ref: "python3 -c '...' scanning docs/BUILD-NOTES.md for A1/A2/A3/PD-1/PD-2/PD-3/STATE_READ_SOURCE_VARIABLES/WFCreateNoteInput/Core/Aware and 'rung 2' — all present; twelve docs/*.py checkers re-verified green after the doc edit"
        status: pass
    human_judgment: false

# Metrics
duration: ~12 min
completed: 2026-08-17
status: complete
---

# Phase 12 Plan 05: Ship the phase — sign, verify, record Summary

**Both PROSOCHĒ forks rebuilt, gate-A-clean, gate-B-recorded, signed under their exact live display names and decrypt-verified to carry this phase's schema_version 4 shape; a cold-runnable seven-test device UAT authored and honestly BLOCKED on DIST-03; every assumption, decision and research correction this phase produced recorded in docs/BUILD-NOTES.md §27.**

## Performance

- **Duration:** ~12 min
- **Started:** 2026-08-17T16:14:00+10:00 (approx, from build log timestamps)
- **Completed:** 2026-08-17T16:23:49+10:00
- **Tasks:** 3
- **Files modified:** 8 (2 signed shortcuts, 2 dated archive XMLs, MANIFEST.md, 12-UAT.md, a pending todo, BUILD-NOTES.md)

## Accomplishments

- **Closed the last red checker.** `docs/manifest_check.py` was the only structural check still failing at the start of this plan (three of six rows stale, matching Phase 10's precedent of measuring rows wrong before a re-sign). All twelve `docs/*.py` checkers are now green.
- **Both forks signed under their exact live display names.** `PROSOCHĒ — Nine Circles — Core.shortcut` (229903 bytes) and `PROSOCHĒ — Nine Circles — Aware.shortcut` (234118 bytes), both AEA1 archives, no `_signed` suffix anywhere in `artifacts/shortcuts/`.
- **Verified what actually shipped, not just what was built.** Recovered both signed payloads via the `aea decrypt` + `aa extract` + `plutil` workflow and confirmed the recovered bootstrap templates carry `schema_version` 4, a four-leaf `active_session`, and `exit_events == []` — the phase's three chartered fixes, proven in the artifact a user would actually import, not only in `src/`.
- **Gate B read and recorded, never chained.** Both standalone advisory runs (`--target-macos 27 --target-platform all`) show exactly the one permitted `com.apple.mobilenotes.SharingExtension` / `WFCreateNoteInput` waiver and nothing else — confirming Plan 12-03's nine moved emission sites introduced no parameter-key or picker-literal regression.
- **Authored a cold-runnable device UAT for the exit-recording path** — the highest-risk untested surface in this phase, since the closed OPEN-path debug session never touched exit recording. Ran the reachability probe honestly: `xcrun devicectl list devices` → "No devices found." → **BLOCKED**, every one of the seven tests' result fields left blank, matching the Phase 10/Phase 9 no-fabrication precedent exactly. Opened a pending todo carrying both artifacts' SHA-256s so a later run can confirm build identity before trusting any recorded outcome.
- **Discharged the recording duty in full.** `docs/BUILD-NOTES.md` §27 records all four carried assumptions (A1, A2, A3, A5) with their status and settling rung, all three planner decisions (PD-1, PD-2, PD-3) with rationale, four measured corrections to the phase's research (the `STATE_READ_SOURCE_VARIABLES` filter-not-deletion finding with measured per-source counts, `route_exit()`'s Create branch needing no change, `open_pipeline()`'s fourth leaf, and the Core/Aware display-name correction), and both forks' gate B baselines verbatim.

## Task Commits

Each task was committed atomically:

1. **Task 1: Sign both forks under their live display names, refresh MANIFEST, and take the gate B advisory read** — `ea7a0f4` (feat)
2. **Task 2: Author a cold-runnable 12-UAT.md for the exit-recording path and record the device-reachability verdict** — `6c04711` (docs)
3. **Task 3: Discharge the recording duty — deviations, assumptions and decisions into BUILD-NOTES and CAPABILITY-DECISIONS** — `f85151b` (docs)

## Files Created/Modified

- `artifacts/shortcuts/MANIFEST.md` — all six rows refreshed (size + SHA-256 recomputed from disk); Bytes column reformatted to plain digits.
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut`, `— Aware.shortcut` — regenerated signed artifacts, this phase's shape.
- `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Core-161458.xml`, `— Aware-161508.xml` — new dated pre-sign archives.
- `.planning/phases/12-state-shape-sentinel-gaps-exit-events-and-active-session/12-UAT.md` — new, seven-test device UAT, BLOCKED.
- `.planning/todos/pending/2026-08-17-phase-12-exit-recording-device-uat.md` — new pending todo tracking the blocked UAT.
- `docs/BUILD-NOTES.md` — new §27, the phase's recording-duty section.

## Decisions Made

- **MANIFEST.md's Bytes column reformatted to plain digits (no thousands commas).** The plan's own automated verify block checks `str(size) in man` as a literal substring; a comma-separated `"229,903"` does not contain the substring `"229903"`. `manifest_check.py`'s own parser already strips commas either way, so plain digits satisfy both checks unambiguously.
- **`WFWorkflowName`-equals-basename criterion treated as unsatisfiable-as-written, not as a failure.** Both recovered payloads show `WFWorkflowName` absent entirely — the signer strips it, a fact already measured and documented in Phase 11 (`.claude/CLAUDE.md` §8, this same MANIFEST's own prose: "a signed artifact carries no display name internally"). Verified the equivalent claim instead — filename discipline, which CLAUDE.md itself names as the actual carrier — rather than treating the plan's literal wording as blocking.
- **`docs/CAPABILITY-DECISIONS.md` left untouched.** Per the plan's own instruction, a record is added only if the device UAT actually observed something new. It did not — BLOCKED, zero device evidence — so nothing was added, and BUILD-NOTES §27 says so explicitly.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] MANIFEST.md byte-count formatting did not satisfy the plan's own automated verify block**

- **Found during:** Task 1, running the plan's `<verify>` block after the initial comma-formatted refresh
- **Issue:** The refreshed MANIFEST rows used comma-thousands formatting (`2,831,994`) matching the file's pre-existing convention. The plan's own verify script asserts `str(p.stat().st_size) in man` — a literal digit-string substring check — which fails against a comma-separated number.
- **Fix:** Reformatted all six Bytes cells to plain digits with no thousands separator. `docs/manifest_check.py`'s parser already strips commas (`size_text = unfence(size_cell).replace(",", "")`), so this remains compatible with the standing checker while also satisfying the plan's own verify block.
- **Files modified:** `artifacts/shortcuts/MANIFEST.md`
- **Verification:** Both `python3 docs/manifest_check.py` and the plan's own verify script pass after the reformat.
- **Committed in:** `ea7a0f4` (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 bug — a formatting mismatch between the plan's own verify script and the file's pre-existing comma convention)
**Impact on plan:** Formatting-only change to a table already being rewritten by this task. No scope creep, no behaviour change, no loosened check.

## Issues Encountered

None beyond the deviation above. No guard fired unexpectedly, no build aborted for an unplanned reason, no fix-attempt limit approached. The `aea`/`aa` decrypt-and-verify workflow (step 5 of Task 1) succeeded on first attempt for both forks — no fallback deviation needed there.

## Verification Results

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebb… HEAD` (D-01 provenance gate) | exit 0 |
| `python3 tools/build_state_engine.py` | exit 0 |
| `python3 tools/build_sentient.py` | exit 0, digest `f33ca7a000ac0ab0f4cc9a74aa281396de0f415f4766b12a5add880b6b3dcf8a` |
| Twelve `docs/*.py` checkers | all exit 0 (state_engine, phase5/6/7/9, sentient_audit, sentient_core, environmental_restore, router_ui_census, sequence_dispatch, note_identity, manifest) |
| Gate A, Core fork (`--target-macos 26 --target-platform all`) | `Validation passed.`, exit 0 |
| Gate A, Aware fork | `Validation passed.`, exit 0 |
| Gate B, Core fork (`--target-macos 27 --target-platform all`, standalone, never chained) | exit 1, exactly one line — `WFCreateNoteInput` waiver at index 4192 |
| Gate B, Aware fork | exit 1, exactly one line — identical waiver at index 4260 |
| Both signed artifacts | AEA1 magic bytes, non-zero size, no `_signed` suffix in `artifacts/shortcuts/` |
| Decrypted Core payload | `schema_version` 4, `active_session` four-leaf dict, `exit_events == []` |
| Decrypted Aware payload | same three assertions hold |
| `python3 docs/manifest_check.py` | `manifest check: passed (6 rows verified against disk)` |
| `xcrun devicectl list devices` | `No devices found.` — recorded verbatim in `12-UAT.md` |
| `12-UAT.md` verify script | `12-UAT.md is cold-runnable and carries a recorded verdict` |
| `docs/BUILD-NOTES.md` §27 verify script | `recording duty discharged` |
| Twelve checkers re-verified after documentation edits | all exit 0 |
| No file deletions in any of the three task commits | `git diff --diff-filter=D --name-only HEAD~3 HEAD` empty |

## Known Stubs

None. No hardcoded empty value, placeholder text, or unwired component was introduced. `12-UAT.md`'s blank result fields are not stubs — they are the deliberate, documented outcome of a device-gated test the plan's own `must_haves.prohibitions` forbids fabricating a pass for.

## Threat Flags

None beyond what the plan's own `<threat_model>` already names and this plan's verify blocks close out: T-12-24 (wrong-filename dead install) mitigated by the AEA1 magic-byte + no-`_signed`-suffix assertion; T-12-25 (stale MANIFEST hash) mitigated by recomputing all six rows, not only the presumed-changed ones; T-12-26 (shipped-vs-validated drift) mitigated by the decrypt-and-inspect step; T-12-27 (fabricated device evidence) mitigated by the BLOCKED verdict and blank result fields; T-12-28 (gate B regression from Plan 12-03's moved sites) mitigated by the recorded single-waiver-line confirmation on both forks; T-12-29 (data leaving the device) — structurally impossible, unchanged. T-12-SC (package legitimacy) is n/a — this plan installed no package.

## User Setup Required

None — no external service configuration required. A real iPhone is required to close `12-UAT.md`, tracked via the pending todo this plan opened.

## Next Phase Readiness

**Phase 12 is complete at the source-and-artifact level.** `KNOWN_SENTINEL_EXISTENCE_GATES` reads `()`, `exit_events` and `active_session` are permanent seeded invariants, `profile_snapshot.create_target_url` is resolved, and both signed artifacts carry this shape, decrypt-verified.

**Carried forward, not a blocker for the next phase:** the exit-recording path's device evidence remains at rung 1 (file-level and decrypted-artifact evidence only). `12-UAT.md` and its tracked pending todo
(`.planning/todos/pending/2026-08-17-phase-12-exit-recording-device-uat.md`) own closing that gap whenever a device becomes reachable — this rides alongside the other outstanding device-UAT backlog (09-UAT.md, 10-UAT.md, Phase 4/5/6/7 UAT) already tracked in `.planning/STATE.md`.

## Self-Check: PASSED

- `artifacts/shortcuts/MANIFEST.md` — FOUND, `python3 docs/manifest_check.py` passes
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — FOUND, AEA1
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — FOUND, AEA1
- `.planning/phases/12-state-shape-sentinel-gaps-exit-events-and-active-session/12-UAT.md` — FOUND
- `.planning/todos/pending/2026-08-17-phase-12-exit-recording-device-uat.md` — FOUND
- `docs/BUILD-NOTES.md` §27 — FOUND
- Commit `ea7a0f4` — FOUND in `git log`
- Commit `6c04711` — FOUND in `git log`
- Commit `f85151b` — FOUND in `git log`
- Working tree clean after all three task commits (`git status --short` empty)
- No file deletions in any commit (`git diff --diff-filter=D --name-only HEAD~3 HEAD` empty)

---
*Phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session*
*Completed: 2026-08-17*
