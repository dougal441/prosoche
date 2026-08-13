---
phase: 01-capability-audit-config-foundation
plan: 04
subsystem: capability-audit
tags: [shortcuts-playground, ios-shortcuts, notes-actions, brightness, volume, get-device-details, environmental-safety]

# Dependency graph
requires:
  - phase: 01-capability-audit-config-foundation
    provides: 26 judged CAP rows (plans 01-01/01-02) and the BD-01/BD-05 scaffold in docs/CAPABILITY-DECISIONS.md (plan 01-01)
provides:
  - Eight new judged capability rows (CAP-07..CAP-10, CAP-16..CAP-19) in docs/BUILD-NOTES.md §4, all landing VERIFIED
  - UA-01 user action item gating Phase 2 on an on-device Notes confirmation
  - BD-02 (Dimming/brightness read-back), BD-03 (Silence/volume read-back), BD-05 (Notes actions on iOS) written in full in docs/CAPABILITY-DECISIONS.md
affects: [phase-02-control-room-onboarding, phase-04-close-restore, phase-05-circle-primitives]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Get Device Details (is.workflow.actions.getdevicedetails) read via its WFDeviceDetail enum case literal, not a dedicated Get Brightness/Get Volume action"
    - "settings_snapshot has-any-value guard: a stateful environmental write only ever fires after a successful read, per-run, per ARCHITECTURE.md §9"

key-files:
  created: []
  modified:
    - docs/BUILD-NOTES.md
    - docs/CAPABILITY-DECISIONS.md

key-decisions:
  - "CAP-17/CAP-19 (Get current brightness/volume) land VERIFIED, not UNVERIFIED: toolkit-v78-first-party-enum-cases.json's getdevicedetails_wfdevice_detail enum contains the literal cases 'Current Brightness' and 'Current Volume', cross-platform (iOS 27 Simulator + macOS 27) — real local ToolKit evidence, not the external-only Apple release-note corroboration the prior research pass relied on."
  - "BD-02/BD-03: Dimming and Silence are built as stateful capture-and-restore primitives (Get Device Details read -> has-any-value guard -> settings_snapshot capture -> Set Brightness/Volume -> restore on CLOSE/Emergency Restore/cooldown-expiry), not degraded to message-only, because a genuine read-back path now exists for both settings."
  - "CAP-18 (Set Volume) picks up a confirmed WFVolumeSetting/WFVolume schema that .planning/research/STACK.md had reported as unconfirmed."
  - "CAP-07..CAP-10 (all four Notes actions) land VERIFIED via v63 generic-snapshot presence plus prose cross-corroboration, even though the entire Notes namespace is absent from the iOS-27-simulator snapshot — treated as the documented completeness gap docs/BUILD-NOTES.md §3 already names Notes as the paradigm example of, not a platform restriction."
  - "BD-05 authorises Phase 2 to build the Control Room on the four Notes actions now, gated by UA-01's on-device confirmation (never inside an automated OPEN/CLOSE), with a named file-based fallback (Save File + display action) if that gate fails."

patterns-established:
  - "Evidence cells must name the exact enum type inspected in toolkit-v78-first-party-enum-cases.json and state whether the target case exists, not just cite the parameter's presence"
  - "A macOS-27-only platform tag on a parameter-keys catalog entry is treated as a provenance fact, not proof of iOS exclusivity, when the identifier is also present in the generic pre-OS27 v63 snapshot and independently corroborated in prose"

requirements-completed: [AUDIT-03, AUDIT-04, AUDIT-05]

coverage:
  - id: D1
    description: "CAP-07..CAP-10 (Notes: Find, Create, Append, Show) judged VERIFIED with cited provenance, including the markdownContents-vs-markdown empty-note-body trap recorded verbatim"
    requirement: "AUDIT-05"
    verification:
      - kind: other
        ref: "grep -qE for each CAP-07..CAP-10 row plus markdownContents/appendnote/SharingExtension/toolkit-v63-tool-ids.json/UA-01 strings in docs/BUILD-NOTES.md (plan Task 1 automated verify)"
        status: pass
    human_judgment: false
  - id: D2
    description: "UA-01 user action item recorded, naming all four Notes actions individually and gating Phase 2 on the manual-bootstrap first-use confirmation"
    requirement: "AUDIT-05"
    verification:
      - kind: other
        ref: "grep -qE UA-01 in docs/BUILD-NOTES.md §6 (plan Task 1 automated verify)"
        status: pass
    human_judgment: false
  - id: D3
    description: "BD-05 written in full (all seven fields) authorising Phase 2's Control Room build on the Notes evidence, with a named VERIFIED-only fallback"
    requirement: "AUDIT-05"
    verification:
      - kind: other
        ref: "grep -q 'BD-05'/'AUDIT-05' in docs/CAPABILITY-DECISIONS.md (plan Task 1 automated verify)"
        status: pass
    human_judgment: false
  - id: D4
    description: "CAP-16..CAP-19 (Set/Get Brightness, Set/Get Volume) judged VERIFIED with the Get Device Details enum-case evidence for the two read-back rows"
    requirement: "AUDIT-03, AUDIT-04"
    verification:
      - kind: other
        ref: "grep -qE for each CAP-16..CAP-19 row plus setbrightness/setvolume/device details/toolkit-v78-first-party-enum-cases.json strings; row count >= 34 in docs/BUILD-NOTES.md (plan Task 2 automated verify)"
        status: pass
    human_judgment: false
  - id: D5
    description: "BD-02 and BD-03 written in full (all seven fields each), authorising Dimming/Silence as stateful capture-and-restore primitives bound by the settings_snapshot has-any-value guard, never an unconditional environmental change"
    requirement: "AUDIT-03, AUDIT-04"
    verification:
      - kind: other
        ref: "grep -q for BD-02/BD-03/AUDIT-03/AUDIT-04/SAFE-03/settings_snapshot strings in docs/CAPABILITY-DECISIONS.md (plan Task 2 automated verify)"
        status: pass
    human_judgment: false

duration: 45min
completed: 2026-08-13
status: complete
---

# Phase 1 Plan 4: Notes Actions and Environmental Read-Back Summary

**Resolved three of five capability blockers by re-running the live ToolKit lookup rather than trusting prior research: all four Control Room Notes actions and both brightness/volume read-back paths landed VERIFIED on real local evidence, so Dimming and Silence are authorised as stateful capture-and-restore primitives instead of degrading to message-only.**

## Performance

- **Duration:** ~45 min
- **Completed:** 2026-08-13T01:25:58Z
- **Tasks:** 2
- **Files modified:** 2 (`docs/BUILD-NOTES.md`, `docs/CAPABILITY-DECISIONS.md`)

## Accomplishments

- Judged CAP-07 (Find Notes), CAP-08 (Create Note, including the `markdownContents`-vs-`markdown` empty-note-body trap), CAP-09 (Append to Note), and CAP-10 (Open Note) — all four `VERIFIED`, closing D-12.
- Judged CAP-16 (Set Brightness), CAP-17 (Get current brightness), CAP-18 (Set Volume), and CAP-19 (Get current volume) — all four `VERIFIED`, closing D-09 and D-10. CAP-17 and CAP-19 are the headline finding: `Get Device Details`'s `WFDeviceDetail` enum, inspected directly in `toolkit-v78-first-party-enum-cases.json` (a query the prior research pass never ran), contains literal cases `Current Brightness` and `Current Volume`, cross-platform confirmed — real local evidence the prior research (`STACK.md`, `PITFALLS.md` C1/C2, `ARCHITECTURE.md` §0/§9) did not have.
- Section 4 of `docs/BUILD-NOTES.md` now holds 34 judged rows (26 carried in + 8 new).
- Added `UA-01`, the first entry in `docs/BUILD-NOTES.md` §6, gating Phase 2 on an on-device confirmation of all four Notes actions during the manual bootstrap run.
- Wrote `BD-02` (Dimming/brightness read-back), `BD-03` (Silence/volume read-back), and `BD-05` (Notes actions on iOS) in full in `docs/CAPABILITY-DECISIONS.md`, each with all seven labelled fields.
- BD-02/BD-03 authorise real stateful Dimming/Silence primitives (capture original value via Get Device Details, apply the change, restore on CLOSE/Emergency Restore/cooldown-expiry) instead of the message-only fallback the domain brief anticipated, because a genuine read-back path was found for both settings — while still enforcing canonical strategy §21's absolute rule via a mandatory has-any-value guard that degrades to message-only on any run where the read fails.
- BD-03 also records `is.workflow.actions.pausemusic` (Play/Pause) — the only capability in the entire audit confirmed present in all three ToolKit id snapshots including the iOS-27-simulator one — as the evaluated-but-not-required weaker media-pause alternative.
- BD-05 authorises Phase 2 to build the Control Room on the Notes evidence now (not a blocking wait), gated by UA-01, with a named file-based fallback (Save File + display action) if that gate ever fails, and an honest accounting of what the editable-proforma round-trip (ROOM-06/ROOM-11) loses under that fallback.

## Task Commits

Each task was committed atomically:

1. **Task 1: Notes actions on the iOS target — CAP-07..CAP-10 and BD-05** - `b6c7bce` (docs)
2. **Task 2: Brightness and volume read-back — CAP-16..CAP-19, BD-02 and BD-03** - `547ad85` (docs)

**Plan metadata:** pending (docs: complete plan)

## Files Created/Modified

- `docs/BUILD-NOTES.md` - Added CAP-07..CAP-10 (Notes) and CAP-16..CAP-19 (brightness/volume) rows to §4, and UA-01 to §6.
- `docs/CAPABILITY-DECISIONS.md` - Wrote BD-02, BD-03, and BD-05 in full, replacing their `_Owner: plan 01-04._` stub placeholders.

## Decisions Made

- **CAP-17/CAP-19 promoted to VERIFIED, not UNVERIFIED as anticipated.** The domain brief and prior research (STACK.md, PITFALLS C1/C2, ARCHITECTURE §0/§9) all treated brightness/volume read-back as resting on external-only Apple corroboration. The live re-run of the §3 evidence recipe queried `toolkit-v78-first-party-enum-cases.json` for `getdevicedetails_wfdevice_detail` — a query none of those prior passes performed — and found the literal cases `Current Brightness`/`Current Volume` present, cross-platform. Per the binding citation rule (a verdict resting only on external corroboration is capped at `UNVERIFIED`, but this is not external-only), this promotes both rows to `VERIFIED`.
- **BD-02/BD-03 authorise stateful Dimming/Silence, not message-only.** Because a genuine local-evidenced read path exists for both settings, canonical strategy §21's absolute rule ("if the original state cannot be read, do not make a stateful intervention") is satisfied by wrapping every write in a has-any-value guard around the Get Device Details read, not by refusing to write at all. A failed read on any individual run still degrades that one primitive to message-only for that run — the safety guarantee is preserved per-run, not assumed away by the overall VERIFIED verdict.
- **CAP-07..CAP-10 graded VERIFIED despite total absence from the iOS-27-simulator snapshot.** `docs/BUILD-NOTES.md` §3 already names Notes actions as the paradigm example of a bundled-data completeness gap rather than a genuine platform restriction ("unquestionably available on a real device"); combined with v63 generic-snapshot presence and independent prose cross-corroboration (`BEST_PRACTICES.md`, `CHANGELOG.md`, `APPINTENTS.md`), this is the same identifier/prose-fills-JSON-gap pattern already used for CAP-S04/CAP-S05 elsewhere in the document. The residual on-device-confirmation gap this cannot close locally is handled structurally via UA-01, not by suppressing the verdict.
- **BD-05 authorises Phase 2 to proceed now, not to wait.** Given the strength of the evidence, blocking Phase 2 entirely pending an on-device test would cost real build time without a corresponding safety gain; the honest position given the evidence is "authorised, but confirm early via UA-01," with a concrete VERIFIED-only fallback named for the case that confirmation fails.

## Deviations from Plan

None — plan executed exactly as written. All eight new capability rows landed `VERIFIED` on real evidence (a result the plan's own text anticipated as possible: "Check whether Get Device Details... exposes a usable property before concluding NOT AVAILABLE"), so no new `DEV-NN` entries were required per the plan's own conditional instruction ("Append DEV entries... for every one of these four rows whose Verdict is not VERIFIED"). This is a genuinely different outcome than the domain brief's framing anticipated (which expected some rows to land degraded), but it followed directly and only from the mandated live re-run of the ToolKit evidence rather than from any deviation in process.

## Issues Encountered

None. The two task commits were made atomic by temporarily isolating each task's diff (staging Task 1's Notes-related content alone, committing, then restoring and committing Task 2's brightness/volume content) since both tasks touch the same two append-only documents.

## User Setup Required

None - no external service configuration required. UA-01 records a Phase-2-gating on-device confirmation step (not a setup step for this plan) — see `docs/BUILD-NOTES.md` §6.

## Next Phase Readiness

- Phase 2 (Control Room onboarding) is authorised to build on CAP-07..CAP-10 and BD-05, gated by UA-01's first-use confirmation during the manual bootstrap run — must specifically verify the CAP-08 `markdownContents` note-body risk.
- Phase 5 (Circle primitives) has a fully specified build form for CIRC-03 (Silence) and CIRC-05 (Dimming): Get Device Details read -> has-any-value guard -> settings_snapshot capture -> Set Volume/Brightness -> per-run message-only fallback if the read fails, plus a required numeric-sanity check Phase 5 must still add (the exact output format/range of Get Device Details' brightness/volume readings is not documented anywhere in the bundle).
- Phase 4 (CLOSE/restore) and SAFE-05 (Emergency Restore) now have a concrete `settings_snapshot.brightness`/`settings_snapshot.volume` shape to restore from, consistent with BD-01's Ash decision and the same restoration machinery.
- Remaining blocker for this phase: BD-04 (Use Model On-Device literal), owned by plan 01-05.

---
*Phase: 01-capability-audit-config-foundation*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: docs/BUILD-NOTES.md
- FOUND: docs/CAPABILITY-DECISIONS.md
- FOUND: .planning/phases/01-capability-audit-config-foundation/01-04-SUMMARY.md
- FOUND commit: b6c7bce
- FOUND commit: 547ad85
