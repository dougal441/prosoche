---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
current_phase: 8
current_phase_name: Sentient Fork & Dual Distribution
status: verifying
stopped_at: Phase 08 Plan 03 awaiting real-iPhone DIST-03 UAT
last_updated: "2026-08-13T08:58:14.171Z"
last_activity: 2026-08-14
last_activity_desc: "Completed quick task 260814-kut: disambiguated deviations and guarded rebuild provenance"
progress:
  total_phases: 8
  completed_phases: 6
  total_plans: 18
  completed_plans: 18
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-08-13)

**Core value:** When a user automatically reaches for a target app, PROSOCHĒ interrupts strongly enough that the user makes an actual choice — and the strength of that interruption adapts to their own recent behaviour.
**Current focus:** Phase 8 — real-iPhone dual-fork UAT

## Current Position

Phase: 8 of 8 (Sentient Fork & Dual Distribution)
Plan: 3 of 3 complete
Status: Automated verification passed; awaiting real-iPhone import / Manual UAT
Last activity: 2026-08-14 — Completed quick task 260814-kut: disambiguated deviations and guarded rebuild provenance

Progress: [██████████] 100%

## Performance Metrics

**Velocity:**

- Total plans completed: 0
- Average duration: - min
- Total execution time: 0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| - | - | - | - |

**Recent Trend:**

- Last 5 plans: -
- Trend: -

*Updated after each plan completion*
**Per-Plan Metrics:**

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| Phase 01 P01 | 15min | 2 tasks | 3 files |
| Phase 01 P03 | ~20min | 2 tasks | 1 files |
| Phase 01 P02 | ~35min | 2 tasks | 1 files |
| Phase 01 P04 | 45min | 2 tasks | 2 files |
| Phase 01 P05 | 45min | 3 tasks | 3 files |
| Phase 02 P01 | 50min | 2 tasks | 2 files |
| Phase 02 P02 | 10min | 2 tasks | 2 files |
| Phase 02 P03 | 20min | 3 tasks | 2 files |
| Phase 02 P04 | 55min | 3 tasks | 3 files |
| Phase 05 P01 | 35min | 2 tasks | 3 files |
| Phase 05 P02 | 20min | 3 tasks | 2 files |
| Phase 05 P03 | 15min | 2 tasks | 5 files |
| Phase 06-exits-exit-learning-contracts P01 | 25min | 2 tasks | 2 files |
| Phase 06-exits-exit-learning-contracts P02 | 15min | 2 tasks | 2 files |
| Phase 06-exits-exit-learning-contracts P03 | 20min | 3 tasks | 3 files |
| Phase 08-sentient-fork-dual-distribution P01 | 20m | 2 tasks | 3 files |
| Phase 08-sentient-fork-dual-distribution P02 | 12m | 2 tasks | 3 files |
| Phase 08-sentient-fork-dual-distribution P03 | 10m | 1 tasks | 10 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Roadmap]: Capability audit (Phase 1) must resolve four hard blockers — no verified grayscale action, no brightness/volume read-back, unverified `Use Model` On-Device literal, unconfirmed Notes-on-iOS actions — before any phase that depends on primitives, the Control Room Note, or the model.
- [Roadmap]: Dumb fork must be fully built, validated, signed, and on-device-verified (Phase 7) before Sentient work (Phase 8) begins; Sentient is an additive wrap that must not alter the deterministic engine.
- [Roadmap]: CLOSE/session-race handling (Phase 4) lands before contracts and exit learning (Phase 6), because contract fidelity and exit outcomes both depend on trustworthy session duration.
- [Roadmap]: The final phase (Phase 8) delivers both signed `.shortcut` files — the project's definition of done.
- [Phase 1]: BD-01: Ash degraded to a non-environmental variant (self-contained visual pause) rather than a system Color Filters toggle — no iOS read-back mechanism exists in any bundled ToolKit snapshot
- [Phase 1]: CAP-20 verdict set to NOT AVAILABLE, confirmed by a live re-run of the ToolKit lookup
- [Phase ?]: heat.reopen_bonus_mode = "exclusive" (PROTOTYPE INTERPRETATION): a reopen matching both rapid-return bands earns only the tighter bonus, not both stacked; Phase 3 owns STATE-04 against this value
- [Phase ?]: config_version, heat.ice_expiry_relief, exits.exploration_rate, exits.exploit_min_observations labelled PROTOTYPE DEFAULT: canonical strategy requires each field to exist but states no number
- [Phase ?]: 25 capability audit rows resolved to VERIFIED via live ToolKit re-lookup, correcting 5 STACK.md param-shape findings (CAP-03, CAP-13, CAP-21, CAP-23, CAP-24)
- [Phase ?]: CAP-17/CAP-19 (brightness/volume read-back) VERIFIED via Get Device Details' WFDeviceDetail enum, promoting BD-02/BD-03 to stateful capture-and-restore Dimming/Silence instead of message-only
- [Phase ?]: BD-05: Phase 2 authorised to build the Control Room on CAP-07..CAP-10 (all VERIFIED), gated by UA-01's on-device confirmation, with a file-based fallback if that gate fails
- [Phase ?]: BD-04 (AUDIT-06 Branch B): the Use Model On-Device literal is UNRECOVERED-LOCALLY; the Sentient fork's On-Device guarantee is explicitly re-planned rather than guessed, gated on UA-02
- [Phase ?]: Phase 8 gate: may build Use Model with evidenced parameters and deterministic fallback now; may not write a WFLLMModel value or claim On-Device is enforced until UA-02 closes
- [Phase ?]: [Phase 2]: WFWorkflowInputContentItemClasses set to ["WFStringContentItem"] (not empty) — the validator flags any ExtensionInput reference against an empty list as a real Stop-and-Respond risk
- [Phase ?]: [Phase 2]: Create Note carries a defensive name parameter alongside markdownContents, reusing the evidenced key from its sibling Notes-create action, since the validator requires a title-shaped parameter on every Notes-create action
- [Phase ?]: [Phase 2]: profile_snapshot.synced_at (as text) is the field seeded with Now Epoch at bootstrap; last_open_at/last_close_at stay null per PITFALLS B7 so Phase 3's first-run detection is not defeated
- [Phase ?]: [Phase 2]: DEV-04 — validator invocation corrected to --target-platform all (not ios); the recorded ios invocation measured 118 spurious errors against a known-good file
- [Phase ?]: Automation B written as its own full ten-step list (mirroring Automation A) rather than a delta paragraph, so the shortcut name PROSOCHĒ — Nine Circles — Dumb appears identically in both automation sections
- [Phase ?]: New docs/BUILD-NOTES.md §9 records the canonical Dumb-fork signing name so Phase 7's signer agrees with what the Control Room Note tells the user to look for
- [Phase ?]: BD-05's fallback trigger recorded as a new field inside the existing UA-01 entry, not a separate item, so the trigger sits next to the observation that would raise it
- [Phase ?]: CURRENT STATE / ATTENTION LEDGER / VALUE-LIFE-RETURNED / SUPPORT-PROSOCHĒ left as honest first-run placeholders per canonical strategy §17 and Phase 7's ROOM-08, not embellished with invented content
- [Phase ?]: [Phase 2]: Router's OPEN/CLOSE/fail-safe ladder built entirely from nested If/Otherwise, a fresh GroupingIdentifier per nesting level, no Otherwise If anywhere (macOS 27+ only, unusable at the iOS 26 target)
- [Phase ?]: [Phase 2]: Fail-safe branch (BOOT-02) is structurally inert by construction -- one Comment + one Show Alert only, no file/dictionary/Note action -- so unrecognised input can never be mistaken for a real OPEN/CLOSE event
- [Phase ?]: Hoisted the state-load-and-bootstrap chain above the router (not into each branch) so BOOT-06 self-healing works from manual, OPEN, and CLOSE alike, since Shortcuts has no subroutine mechanism to share it otherwise
- [Phase ?]: Two-field validity gate (schema_version has-value AND equals "1" AND profile has-value) replaces the single-field presence check, computed via a two-variable accumulator-then-canonical-copy pattern so State Present is still assigned by exactly one Set Variable while genuinely nested If/Otherwise blocks drive it
- [Phase ?]: Note-existence guard (Find Notes with condition code 99, never 4, per the documented Notes name-matching trap) recreates a deleted Control Room Note with its full original body, scoped to the MANUAL branch only for both cost and Notes-permission-prompt safety reasons
- [Phase ?]: Phase 5 uses semantic plist markers plus deterministic UUID5 generation, so the full shortcut rebuild is idempotent without numeric action indices.
- [Phase ?]: Ash remains a validator-clean non-environmental pause; Dimming and Silence act only after capturing a restorable original.
- [Phase ?]: Leaving wraps primitive dispatch only after the initial session save.
- [Phase ?]: Exit selection remains deterministic and Config-driven without model, random, or network actions.
- [Phase ?]: Sentient uses the device-evidenced Apple Intelligence on Device model literal; no OS-27-only keys.
- [Phase ?]: Completed-slow, empty, or malformed audit output falls through to Dumb; hung model cancellation is unavailable at target 26.

### Pending Todos

**Device UAT (blocker — nothing past the first OPEN has ever run on an iPhone):**

- [blocker] Device UAT — CLOSE pipeline and session race — `.planning/todos/pending/2026-08-16-device-uat-close-pipeline-and-session-race.md`
- [blocker] Device UAT — nine Circles and sequence switching — `.planning/todos/pending/2026-08-16-device-uat-nine-circles-and-sequence-switching.md`
- [blocker] Device UAT — intention contracts and fidelity feedback — `.planning/todos/pending/2026-08-16-device-uat-intention-contracts-and-fidelity-feedback.md`
- [blocker] Device UAT — six exits and explore/exploit learning — `.planning/todos/pending/2026-08-16-device-uat-six-exits-and-explore-exploit-learning.md`
- [blocker] Device UAT — Circle IX cooldown and the route out of Ice — `.planning/todos/pending/2026-08-16-device-uat-circle-ix-cooldown-and-route-out-of-ice.md`
- [blocker] Device UAT — manual Control Room menu and safety recovery — `.planning/todos/pending/2026-08-16-device-uat-manual-control-room-menu-and-safety-recovery.md`

**Build / defect work:**

- [cosmetic] Apply Build Addendum 01 — `.planning/todos/pending/2026-08-14-apply-build-addendum-01.md`
- [major] Repair iOS 26 automation onboarding — `.planning/todos/pending/2026-08-14-repair-ios-26-automation-onboarding.md`
- [major] Close the remaining state-shape sentinel gaps (exit_events, active_session) — `.planning/todos/pending/2026-08-15-close-state-shape-sentinel-gaps.md`
- [major] Fix the WFConditionalActionString red-operator sites and the WFItems List wrapper — `.planning/todos/pending/2026-08-15-fix-red-operator-and-list-wrapper-defects.md`
- [major] Re-fork Sentient now that Dumb's OPEN path is device-confirmed — `.planning/todos/pending/2026-08-15-fork-sentient-post-openpath-fix.md`
- [major] Ship-readiness cleanup for PROSOCHĒ Dumb — `.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md`
- [major] Reintroduce and validate Dimming/Silence stateful restore on an experimental fork — `.planning/todos/pending/2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md` (⚠️ deliberately conflicts with ship-readiness item 5 — the cut proceeds on main in parallel)
- [major] Recover the Use Model On-Device literal (UA-02) — `.planning/todos/pending/2026-08-16-recover-the-use-model-on-device-literal.md`
- [minor] Grayscale / Ash capability donor test — `.planning/todos/pending/2026-08-16-grayscale-ash-capability-donor-test.md`

**Product / scope:**

- [major] Optimise and streamline the UX — onboarding and in-run functionality — `.planning/todos/pending/2026-08-16-optimise-ux-onboarding-and-functionality.md`
- [major] Build the VALUE / LIFE RETURNED functionality, incl. the Attention Receipt — `.planning/todos/pending/2026-08-16-build-value-life-returned.md`
- [minor] Build the low-salience "Support PROSOCHĒ" contribution path — `.planning/todos/pending/2026-08-16-build-support-prosoche-low-salience.md`
- [major] Physical unlock (QR scan or NFC tap) to exit Circle IX / Frozen — `.planning/todos/pending/2026-08-16-physical-unlock-for-circle-ix-ice.md`
- [major] Merge Dumb and Sentient into one fork, selected at onboarding — `.planning/todos/pending/2026-08-16-merge-dumb-and-sentient-into-one-fork-selected-at-onboarding.md`
- [minor] Open-source release readiness — `.planning/todos/pending/2026-08-16-open-source-release-readiness.md`

### Completed Todos

| Todo | Closed | Evidence |
|---|---|---|
| Fix OPEN routing and Test Circle sequence error | 2026-08-15 | Device-verified on build `2026-08-15o`; 16-cycle debug session archived at `.planning/debug/resolved/open-routing-sequence-error.md` |

### Blockers/Concerns

- [Phase 1]: Four capability blockers are unresolved pending live on-device verification — grayscale/Color Filters availability, brightness/volume read-back, the `Use Model` On-Device pinning literal, and Notes actions on iOS. All downstream phases assume these get resolved (favorably or via documented fallback) in Phase 1.
- DIST-03 real-iPhone import and first Manual UAT blocked: xcrun devicectl reports no connected devices.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260814-kqm | Correct signed AEA1 `.shortcut` recovery instructions | 2026-08-14 | adc96a3 | [260814-kqm-correct-8-signed-aea1-shortcut-artifacts](./quick/260814-kqm-correct-8-signed-aea1-shortcut-artifacts/) |
| 260814-kut | Disambiguate deviation IDs and guard rebuild provenance | 2026-08-14 | 05f69fc | [260814-kut-disambiguate-the-cycle-3-speaktext-devia](./quick/260814-kut-disambiguate-the-cycle-3-speaktext-devia/) |

## Deferred Items

Items acknowledged and carried forward from previous milestone close:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| v2 | CTX-01..04 (contextual exit learning), VAL-01..04 (value measurement), OPT-01..02 (Sentient precomputed Mirror), PAY-01..02 (pay-after-value support) | Deferred to v2 | Requirements definition |

## Session Continuity

Last session: 2026-08-13T08:58:14.160Z
Stopped at: Phase 08 Plan 03 awaiting real-iPhone DIST-03 UAT
Resume file: docs/device-evidence/Phase8-DIST-03-BLOCKED.md
