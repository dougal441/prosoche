---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
current_phase: 09
current_phase_name: Dimming/Silence Stateful Restore (Experimental Fork)
status: verifying
stopped_at: "09-02 Task 1 complete; Tasks 2-3 blocked on device access (checkpoint:human-verify)"
last_updated: "2026-08-16T10:09:29.989Z"
last_activity: 2026-08-16
last_activity_desc: Phase 09 execution started
progress:
  total_phases: 9
  completed_phases: 6
  total_plans: 20
  completed_plans: 20
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-08-13)

**Core value:** When a user automatically reaches for a target app, PROSOCHĒ interrupts strongly enough that the user makes an actual choice — and the strength of that interruption adapts to their own recent behaviour.
**Current focus:** Phase 09 — Dimming/Silence Stateful Restore (Experimental Fork)

## Current Position

Phase: 09 (Dimming/Silence Stateful Restore — Experimental Fork) — MERGED TO MAIN, DEVICE-PROVING OUTSTANDING
Plan: 2 of 2 (09-01 complete; 09-02 Task 1 complete, Tasks 2-3 never run)
Status: Coercion fix merged to main UNTESTED by explicit user decision 2026-08-16 — see `docs/BUILD-NOTES.md` §18. Dimming/Silence writes now execute where they previously no-opped, which makes `restore_managed_settings()` load-bearing on a path with zero device evidence. `09-UAT.md` (12 tests) is authored and ready; only test 1 (coercion chip not red) passed. Also outstanding: Phase 8 awaiting real-iPhone import / Manual UAT; Phase 4 UAT tests 1, 3-6 reopened.
Last activity: 2026-08-16 — Phase 9 merged to main untested; prior: quick task 260816-ukb stripped OPEN_BISECT debug breadcrumbs (Phase 4 UAT unblock)

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
| Phase 09 P01 | 25min | 3 tasks | 7 files |
| Phase 09 P02 | 7min | 1 tasks | 3 files |

## Accumulated Context

### Roadmap Evolution

- Phase 9 added: Reintroduce and validate Dimming/Silence stateful restore on an experimental fork (this branch). Runs in parallel with, and does not reverse, the main-line brightness/volume cut in `.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md`. See `.planning/todos/pending/2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md` for full context; `Donor 10.shortcut` (`.planning/debug/`) supplies the coercion-aggrandizement evidence needed to fix the 18 deferred sites.
- [Phase 9]: Research corrected the site count from 18 to 28 (`setbrightness`=14, `setvolume`=14) — `docs/BUILD-NOTES.md`'s original citation of "§8" was itself wrong; the real table is `.planning/debug/HANDOFF.md` §8, now corrected there, in ROADMAP.md criterion 1, and in the todo. Donor 10 (decrypted) confirms the action/parameter identifiers but contains no variable-fed `WFBrightness`/`WFVolume` example, so the coercion shape for this exact parameter position remains analogy-only (`WFNumberContentItem`, unverified) pending an on-device visual check or fresh donor. See `09-RESEARCH.md`.
- [Phase 9]: BD-02's "never zero, 10–15% band" brightness floor corrected — user-reported on-device observation is that iOS's practical brightness minimum is dim, not a literal black/unusable screen, so avoiding it was never itself the safety requirement. The safety mechanism is capture-and-restore reliability (Get Device Details → has-any-value guard → snapshot → restore on CLOSE/Emergency Restore), which BD-02 already specified and Phase 9 exists to prove under real failure modes. Scoped to this experimental fork only (`.claude/CLAUDE.md`, `docs/CAPABILITY-DECISIONS.md` BD-02 addendum, `.planning/ROADMAP.md` Phase 9 criterion 4) — main line's floor is untouched. Provisional until Phase 9's own on-device testing confirms it.

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
- [Phase ?]: Kept the numeric-coercion fix purely additive at the NUMERIC_OPERAND_FIELDS table per plan instruction; no other function edited.
- [Phase ?]: Fixed two pre-existing, unrelated stale self-check assertions (docs/state_engine_self_check.py gettimebetweendates count; docs/phase5_self_check.py router-gate ancestry) because the plan's own required verify chain needed both scripts to pass (Rule 1/3 deviation).
- [Phase ?]: [Phase 9]: 09-02 Task 1 complete (both forks re-signed with coercion fix, 09-UAT.md authored with 12 tests + DEV-06 first-principles write-up); Tasks 2-3 (device trials) blocked — zero iPhones connected, matching the open DIST-03 blocker. Did not auto-approve despite auto_advance=true, per do-not-fabricate rule.

### Pending Todos

Reorganized 2026-08-16 into todo / backlog / seed. Todo = worked directly. Backlog =
bare-minimum-to-working-product device verification, tracked as ROADMAP.md 999.x phases.
Seed = forward-looking, not yet triggered, tracked in `.planning/seeds/`.

**Todo (worked directly):**

- [cosmetic] Apply Build Addendum 01 — `.planning/todos/pending/2026-08-14-apply-build-addendum-01.md`
- [major] Repair iOS 26 automation onboarding — `.planning/todos/pending/2026-08-14-repair-ios-26-automation-onboarding.md`
- [major] Close the remaining state-shape sentinel gaps (exit_events, active_session) — `.planning/todos/pending/2026-08-15-close-state-shape-sentinel-gaps.md`
- [major] Fix the WFConditionalActionString red-operator sites and the WFItems List wrapper — `.planning/todos/pending/2026-08-15-fix-red-operator-and-list-wrapper-defects.md`
- [major] Ship-readiness cleanup for PROSOCHĒ Dumb — `.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md`
- [major] Recover the Use Model On-Device literal (UA-02) — `.planning/todos/pending/2026-08-16-recover-the-use-model-on-device-literal.md`
- [major] Optimise and streamline the UX — onboarding and in-run functionality — `.planning/todos/pending/2026-08-16-optimise-ux-onboarding-and-functionality.md`
- [major] Reintroduce and validate Dimming/Silence stateful restore on an experimental fork — `.planning/todos/pending/2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md` (⚠️ deliberately conflicts with ship-readiness item 5 — the cut proceeds on main in parallel)

**Backlog (genuinely new work; see ROADMAP.md `## Backlog`):**

- [minor] Phase 999.3 — Grayscale / Ash capability donor test — `.planning/phases/999.3-grayscale-ash-capability-donor-test/`

**Device UAT (verification of already-built phases, not new phases — reclassified 2026-08-16; run via `/gsd-verify-work {phase}`, rolled up by `/gsd-audit-uat`):**

- [blocker] Phase 4 UAT — CLOSE pipeline and session race — `.planning/phases/04-close-pipeline-session-race/04-UAT.md`
- [blocker] Phase 5 UAT — nine Circles, sequence switching, and Circle IX cooldown/route-out — `.planning/phases/05-nine-primitives-environmental-safety/05-UAT.md`
- [blocker] Phase 6 UAT — intention contracts, fidelity feedback, six exits, explore/exploit learning — `.planning/phases/06-exits-exit-learning-contracts/06-UAT.md`
- [blocker] Phase 7 UAT — manual Control Room menu and safety recovery — `.planning/phases/07-control-room-dumb-freeze/07-UAT.md`

**Seed (forward-looking, dormant until triggered; see `.planning/seeds/`):**

- SEED-001 — Physical unlock (QR scan or NFC tap) to exit Circle IX / Frozen — `.planning/seeds/SEED-001-physical-unlock-for-circle-ix-ice.md`
- SEED-002 — Open-source release readiness — `.planning/seeds/SEED-002-open-source-release-readiness.md`
- SEED-003 — Build the low-salience "Support PROSOCHĒ" contribution path — `.planning/seeds/SEED-003-support-prosoche-low-salience.md`
- SEED-004 — Build the VALUE / LIFE RETURNED functionality, incl. the Attention Receipt — `.planning/seeds/SEED-004-value-life-returned.md`
- SEED-005 — Re-fork Sentient now that Dumb's OPEN path is device-confirmed — `.planning/seeds/SEED-005-refork-sentient-post-openpath-fix.md`
- SEED-006 — Merge Dumb and Sentient into one fork, selected at onboarding — `.planning/seeds/SEED-006-merge-dumb-and-sentient-into-one-fork.md`

### Completed Todos

| Todo | Closed | Evidence |
|---|---|---|
| Fix OPEN routing and Test Circle sequence error | 2026-08-15 | Device-verified on build `2026-08-15o`; 16-cycle debug session archived at `.planning/debug/resolved/open-routing-sequence-error.md` |

### Blockers/Concerns

- [Phase 1]: Four capability blockers are unresolved pending live on-device verification — grayscale/Color Filters availability, brightness/volume read-back, the `Use Model` On-Device pinning literal, and Notes actions on iOS. All downstream phases assume these get resolved (favorably or via documented fallback) in Phase 1.
- DIST-03 real-iPhone import and first Manual UAT blocked: xcrun devicectl reports no connected devices.
- Phase 9 Plan 02 Tasks 2-3 blocked: 09-UAT.md's 12 device-proving tests (coercion-chip gate, capture/restore, failure-mode trials, DEV-06 verdict) require a real Apple-Intelligence-capable iPhone on iOS 26.x. xcrun devicectl reports zero connected devices — same underlying blocker as DIST-03. Both re-signed .shortcut artifacts and the fully-authored 09-UAT.md are ready; resume via /gsd-verify-work 9 once a device is available.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260814-kqm | Correct signed AEA1 `.shortcut` recovery instructions | 2026-08-14 | adc96a3 | [260814-kqm-correct-8-signed-aea1-shortcut-artifacts](./quick/260814-kqm-correct-8-signed-aea1-shortcut-artifacts/) |
| 260814-kut | Disambiguate deviation IDs and guard rebuild provenance | 2026-08-14 | 05f69fc | [260814-kut-disambiguate-the-cycle-3-speaktext-devia](./quick/260814-kut-disambiguate-the-cycle-3-speaktext-devia/) |
| 260816-ukb | Strip OPEN_BISECT/ROUTER_TRACE/BUILD_STAMP debug scaffolding | 2026-08-16 | 154b998 | [260816-ukb-strip-the-open-bisect-debug-breadcrumb-s](./quick/260816-ukb-strip-the-open-bisect-debug-breadcrumb-s/) |

## Deferred Items

Items acknowledged and carried forward from previous milestone close:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| v2 | CTX-01..04 (contextual exit learning), VAL-01..04 (value measurement), OPT-01..02 (Sentient precomputed Mirror), PAY-01..02 (pay-after-value support) | Deferred to v2 | Requirements definition |

## Session Continuity

Last session: 2026-08-16T10:09:29.978Z
Stopped at: 09-02 Task 1 complete; Tasks 2-3 blocked on device access (checkpoint:human-verify)
Resume file: .planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md
