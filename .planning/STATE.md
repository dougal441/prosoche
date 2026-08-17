---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
current_phase: 13
current_phase_name: Red-operator conditionals and the WFItems List wrapper
status: ready-to-execute
stopped_at: Phase 13 planned (4 plans, 4 waves); Phase 12 verification deferred to /gsd-verify-work 12 (device-blocked)
last_updated: "2026-08-17T00:00:00.000Z"
last_activity: 2026-08-17
last_activity_desc: Phase 13 planned — 4 plans across 4 waves, plan-checker passed
progress:
  total_phases: 24
  completed_phases: 9
  total_plans: 42
  completed_plans: 33
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-08-13)

**Core value:** When a user automatically reaches for a target app, PROSOCHĒ interrupts strongly enough that the user makes an actual choice — and the strength of that interruption adapts to their own recent behaviour.
**Current focus:** Phase 13 — Red-operator conditionals and the WFItems List wrapper

## Current Position

Phase: 13 (Red-operator conditionals and the WFItems List wrapper) — READY TO EXECUTE
Plans: 4 (waves 1-4, fully sequential), plan-checker passed

**Phase 13 research rewrote the phase.** Donor 5 was decrypted for the first time and
**refuted family 1**: iOS itself authors a variable in a conditional's TEXT slot as a
`WFTextTokenString` template with `WFInput` alongside taking the opposite
`WFTextTokenAttachment` envelope — key-for-key identical to what `token()` emits. There are
**0 defective conditional sites, not 14**; the sites are already correct and must not be swept.
Family 1 becomes record-the-refutation plus a *pinning* guard so a later pass cannot "fix" a
device-confirmed shape.

**Family 2 is real and 33× larger than recorded** — **66 defective List actions carrying 660
unwrapped rows per fork, not 2**, all from one function, `mirror_text()`. Donors 4/4.1 confirm
the `{"WFItemType": 0, "WFValue": <WFTextTokenString>}` wrapper *and* that literal rows stay
bare strings, so the fix branches per row; a blanket sweep would corrupt `list_items(EXIT_NAMES, …)`.

Two further ROADMAP premises did not hold: the named "concrete starting site"
`if_block("Previous Respected", 4, …)` passes a raw literal and was never a family member, and
the cited `Screenshot 2026-08-14 at 11.55.12 pm.png` does not exist in the worktree, the main
checkout, or git history — no task depends on it.

**Stale constraint corrected before planning:** the forks were renamed Dumb/Sentient → **Core/Aware**
in Phase 11. `.claude/CLAUDE.md` §8 still names the old ones; signing to them would fail
`docs/manifest_check.py`'s DIST-04 assertion. Source XMLs and generator filenames are unchanged.

**Baseline measured green before execution:** 12/12 `docs/*.py` checkers pass, gate A clean on
both forks, gate B showing exactly the one permitted waived line each. Any red during execution
is therefore caused by the phase. `docs/manifest_check.py` is *deliberately* red in waves 1-3
(rebuilding stales the MANIFEST) and closed in 13-04 — stated as constraint D-04 in every
affected plan objective so an executor does not "fix" it by editing rows without re-signing.

**Phase 10 is executed.** Waves 1-4 landed; 10-05 is parked at its `checkpoint:human-verify`
resolved to the `blocked` branch (DIST-03, no connected iPhone). `10-UAT.md` is authored and
cold-runnable: 10 tests, 0 passed, 10 blocked — nothing was inferred from non-device evidence.
All eleven `docs/*.py` structural checks exit 0; both forks are rebuilt, signed under exact
display names, and decrypt-verified 9/9.

**Everything Phase 10 shipped is structurally proven and behaviourally unproven.** The
MANIFEST carries three stacked warnings saying so.

**Phases 11-20 are scoped and queued but none is planned.** They correspond 1:1 to the
remaining pending todos, in the agreed execution order: 11 Addendum 01 / 12 sentinel gaps /
13 red operators / 14 Ash grayscale / 15 Voice / 16 Dimming+Silence device proof / 17 Exile
split / 18 locked-screen CLOSE / 19 device UAT / 20 heavy UX. Each ROADMAP goal is written to
be plannable cold, without the session that produced it.

**Two hard prerequisites inside that order:** Phase 12 (`exit_events`) gates Phase 17, and
Phase 13 (blank Lists, red operators) should land before Phase 19 so a blank Circle in device
testing is a real finding rather than a known artifact.

**Standing device backlog**, all blocked on DIST-03 and best run in one session:
`10-UAT.md` (10 tests), `09-UAT.md` tests 2-12 (dimming/silence restore — the highest-risk
untested path in the product), Phase 4 UAT tests 1 and 3-6, Phase 8's real-iPhone import, and
Phase 19's full nine-Circle sweep. Report the opens-to-first-interruption count from
`10-UAT.md` Test 2 — it decides whether Phase 10's raised entry thresholds need tuning.

Last activity: 2026-08-17 — Phase 12 execution started

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
| Phase 10 P01 | 5m | 3 tasks | 4 files |
| Phase 10 P02 | ~12 minutes | 3 tasks | 4 files |
| Phase 10 P03 | ~20 min | 3 tasks | 4 files |
| Phase 10 P04 | ~35 minutes | 3 tasks | 8 files |
| Phase 10 P05 | ~20 minutes | 2 tasks | 3 files |

## Accumulated Context

### Roadmap Evolution

- Phase 9 added: Reintroduce and validate Dimming/Silence stateful restore on an experimental fork (this branch). Runs in parallel with, and does not reverse, the main-line brightness/volume cut in `.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md`. See `.planning/todos/pending/2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md` for full context; `Donor 10.shortcut` (`.planning/debug/`) supplies the coercion-aggrandizement evidence needed to fix the 18 deferred sites.
- [Phase 9]: Research corrected the site count from 18 to 28 (`setbrightness`=14, `setvolume`=14) — `docs/BUILD-NOTES.md`'s original citation of "§8" was itself wrong; the real table is `.planning/debug/HANDOFF.md` §8, now corrected there, in ROADMAP.md criterion 1, and in the todo. Donor 10 (decrypted) confirms the action/parameter identifiers but contains no variable-fed `WFBrightness`/`WFVolume` example, so the coercion shape for this exact parameter position remains analogy-only (`WFNumberContentItem`, unverified) pending an on-device visual check or fresh donor. See `09-RESEARCH.md`.
- [Phase 9]: BD-02's "never zero, 10–15% band" brightness floor corrected — user-reported on-device observation is that iOS's practical brightness minimum is dim, not a literal black/unusable screen, so avoiding it was never itself the safety requirement. The safety mechanism is capture-and-restore reliability (Get Device Details → has-any-value guard → snapshot → restore on CLOSE/Emergency Restore), which BD-02 already specified and Phase 9 exists to prove under real failure modes. Scoped to this experimental fork only (`.claude/CLAUDE.md`, `docs/CAPABILITY-DECISIONS.md` BD-02 addendum, `.planning/ROADMAP.md` Phase 9 criterion 4) — main line's floor is untouched. Provisional until Phase 9's own on-device testing confirms it.

- Phase 10 added: Ship-readiness remainder and UX-lite pass. **The brightness/volume MVP cut is cancelled and is NOT part of this phase** — Dimming and Silence stay, each as its own distinct Circle, with working brightness and volume capture-and-restore (user decision 2026-08-16, reaffirmed 2026-08-17). Consequences: the SAFE-05 conflict resolves rather than deferring to milestone close, and DEV-06 is live again rather than moot. Research (`10-RESEARCH.md`, 925 lines) was salvaged from an abandoned branch and moved into the phase directory rather than regenerated; its Finding 2 and Pitfalls 2–3 cover the cancelled cut and are superseded, the rest stands.
- [Phase 10]: Circle 8 dispatching nothing (the `"Voice"` sequence entry matching no branch under condition-99 "contains") is a known open defect deliberately left for a later phase. Any sequence/dispatch checker added here must record the orphan rather than fail on it, and must not hard-code condition 99 or substring matching — BD-06 moves dispatch to condition 4 exact matching and abolishes combined entries.

- Phases 11-20 added 2026-08-17, scoped 1:1 from the remaining pending todos in the agreed execution order. Each goal is written to be plannable without this session's context. Order and prerequisites: 11 Addendum 01 (applies BD-06) → 12 sentinel gaps (**gates 17**) → 13 red operators + List wrapper (**should precede 19**) → 14 Ash grayscale → 15 Voice → 16 Dimming/Silence device proof → 17 Exile split → 18 locked-screen CLOSE → 19 device UAT → 20 heavy UX.
- [Phase 11+]: BD-06 (`docs/CAPABILITY-DECISIONS.md`) settles Circle naming, the ten-primitive roster and slot allocation, and is BINDING on phases 11, 14, 15, 16 and 17 — none of them re-cuts the table. Dante names are positional (Circle 1 = Limbo … 9 = Treachery); ten primitives fill nine slots per sequence; combined entries are abolished so dispatch moves to condition 4 exact matching; the routed Exile lands the user directly.
- [Todos]: #2 (iOS 26 automation onboarding), #5 (ship-readiness, absorbed by Phase 10), #12 (Use Model literal, closed as bookkeeping), #13 (dimming/silence experimental fork, absorbed) are closed. Ten remain pending, each now owned by a phase.

- Phase 21 added 2026-08-17: One product or two — Core/Aware fork decision and device eligibility. Gives SEED-006 (merge Dumb/Sentient) an owning phase and folds in the evidence that has accumulated since it was planted: spike 003 INVALIDATED auto-detection (`Device Model` returns bare `"iPhone"`; no try/catch exists), spike 008 VALIDATED `WFLLMModel = "Apple Intelligence on Device"` (closing SEED-006 blocker #2), and `tools/build_sentient.py` already ships the Aware delta as one gated additive insertion. The strategy amendment (§35/§5.7/§31/§13, §38 "document wins") and SEED-006 blocker #3 (provable determinism in a single graph) are what Phase 21 is for. If the answer is TWO products, the better deliverable is a *state* check (Settings → Apple Intelligence & Siri exists and has finished setting up) rather than a model list, since success tracks model presence not just chip class; the A17 Pro/A18 + 8 GB rule alone misleads, as the plain iPhone 15/15 Plus do not qualify while the 16e does. SEED-005 is a hard prerequisite if the merge is chosen.
- [Phase 21 / spike 004]: **verdict downgraded VALIDATED → PARTIAL, 2026-08-17.** Owner reported an iPhone 16e (capable, models downloaded) running the Capability Gate shortcut successfully; re-reading the spike in that light found two defects in its claim. (1) Its `askllm` omits `WFLLMModel` entirely — verified against `.planning/spikes/004-capability-gate/drafts/*.xml` — so neither device run exercised the pinned `"Apple Intelligence on Device"` path that `src/PROSOCHE-Sentient.xml` ships; the runs used the undocumented default model source. (2) The iPhone SE's error, *"support for selected model is downloading"*, is a **provisioning-state** message that cannot distinguish ineligible hardware from a capable device whose ~7 GB models have not landed — and the spike did not record which SE generation it was. Consequence for the merge: the failure window is **wider** than "users who answer the toggle wrongly on old hardware" — Apple Intelligence is on by default on capable devices since iOS 18.3 but its models download over Wi-Fi/power, so a merged product exposes the failure path to **new users on capable hardware at first run**. What survives: the toggle gates correctly both ways, and the ordering property held under one real observed failure. No try/catch remains confirmed — now by an Apple DTS engineer directly ("no way to detect an error from an action"). Four untested device states are tabulated in ROADMAP Phase 21 item 3.

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
- [Phase ?]: Exit selection remains deterministic and Config-driven without model, random, or network actions. **Reaffirmed and extended 2026-08-16 (user decision):** the Exile split offers deterministic exit *or* home, and nothing else — no random exits. Both Exile Circles are bound by this, not just the voluntary Leaving path. No `number.random`, shuffle, or other nondeterminism enters the exit path.
- [Phase ?]: Sentient uses the device-evidenced Apple Intelligence on Device model literal; no OS-27-only keys. **Reconciled 2026-08-17 (quick task 260817-2ng):** this line was the accurate one — the literal was recovered by device round-trip on 2026-08-13 (`docs/device-evidence/UseModel-OnDevice.xml`, commit `013a217`) and is hardcoded at `tools/build_sentient.py:29`. CAP-26's `UNRECOVERED-LOCALLY` token was the stale one and now reads `ROUND-TRIP-CONFIRMED`; DEV-03 and UA-02 are closed; BD-04-R2 records that Branch A was reached. **Still open:** the runtime no-network check (that `Use Model` cannot silently fall back to Private Cloud Compute) needs an Apple-Intelligence-capable iPhone; until it passes, no user-facing on-device guarantee copy changes.
- [Phase ?]: Completed-slow, empty, or malformed audit output falls through to Dumb; hung model cancellation is unavailable at target 26.
- [Phase ?]: Kept the numeric-coercion fix purely additive at the NUMERIC_OPERAND_FIELDS table per plan instruction; no other function edited.
- [Phase ?]: Fixed two pre-existing, unrelated stale self-check assertions (docs/state_engine_self_check.py gettimebetweendates count; docs/phase5_self_check.py router-gate ancestry) because the plan's own required verify chain needed both scripts to pass (Rule 1/3 deviation).
- [Phase ?]: [Phase 9]: 09-02 Task 1 complete (both forks re-signed with coercion fix, 09-UAT.md authored with 12 tests + DEV-06 first-principles write-up); Tasks 2-3 (device trials) blocked — zero iPhones connected, matching the open DIST-03 blocker. Did not auto-approve despite auto_advance=true, per do-not-fabricate rule.
- [Phase ?]: Circle 0 promoted as a first-class value of the existing circle field (0..9) rather than a parallel silent flag — one source of truth, no schema_version bump
- [Phase ?]: Threshold curves raised by each profile's own first band width, preserving band widths and delaying only entry into Circle 1 (Paradise 4, Limbo 3, Inferno 2)
- [Phase ?]: Gated the single shownote on Manual Show Note Requested; filter.notes and Create Note stay unconditional so BOOT-08 self-heal survives
- [Phase ?]: Setup Check derives automation status from last_open_at/last_close_at flat reads with numeric > 0 gates — no new state key, no schema bump
- [Phase ?]: Cancelled-cut guard: when a subtractive change is proposed and then reversed by decision, write a checker whose docstring states the cancellation and its dates and whose assertions name every symbol the cut would have removed
- [Phase ?]: Structurally-derived exemption: an assertion false at HEAD for a by-construction reason gets a named helper located by the same structural handle the generator uses, never an index or a silent skip
- [Phase ?]: docs/sequence_dispatch_check.py never filters on a condition code; semantics are resolved per branch from the branch's own code, so BD-06's contains-to-exact move needs no edit
- [Phase ?]: Sentient rebuilt rather than left stale, keeping docs/sentient_core_check.py green — the brief's 'leave it red' directive had inverted, since the check passed at the phase's starting HEAD and honouring it would have meant deliberately introducing the fork skew the check detects (DEV-P10-02). A rebuild, not a re-fork; SEED-005 untouched.
- [Phase ?]: A signed .shortcut carries no display name internally — measured by decryption: auth-data holds only SigningCertificateChain and the signer strips WFWorkflowName. The filename is the sole carrier, so signed-name discipline is load-bearing, not cosmetic.
- [Phase ?]: The plan's 'eleven consumers' figure for the widened circle domain was not reproducible, so the consumer surface was measured from the artifact instead (75 actions, five distinct sites) rather than transcribed — BUILD-NOTES section 2's do-not-fabricate protocol applies to its own record.
- [Phase ?]: Phase 10 device UAT resolved to the plan's blocked branch: xcrun devicectl list devices returned 'No devices found.', so all ten tests in 10-UAT.md stay blank and DIST-03 stays unchecked. No Mac import, simulator run, or decrypted-artifact inference was substituted for a device observation.

### Pending Todos

Reorganized 2026-08-16 into todo / backlog / seed. Todo = worked directly. Backlog =
bare-minimum-to-working-product device verification, tracked as ROADMAP.md 999.x phases.
Seed = forward-looking, not yet triggered, tracked in `.planning/seeds/`.

**Todo (worked directly):**

- [cosmetic] Apply Build Addendum 01 — `.planning/todos/pending/2026-08-14-apply-build-addendum-01.md`
- [major] Repair iOS 26 automation onboarding — `.planning/todos/pending/2026-08-14-repair-ios-26-automation-onboarding.md`
- [major] Close the remaining state-shape sentinel gaps (exit_events, active_session) — `.planning/todos/pending/2026-08-15-close-state-shape-sentinel-gaps.md`
- [major] Fix the WFConditionalActionString red-operator sites and the WFItems List wrapper — `.planning/todos/pending/2026-08-15-fix-red-operator-and-list-wrapper-defects.md`
- [major] Ship-readiness cleanup for PROSOCHĒ Dumb — `.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md` (item 1 done; **item 5 SUPERSEDED 2026-08-16 — the brightness/volume cut is cancelled**)
- [major] Recover the Use Model On-Device literal (UA-02) — `.planning/todos/pending/2026-08-16-recover-the-use-model-on-device-literal.md`
- [major] Optimise and streamline the UX — onboarding and in-run functionality — `.planning/todos/pending/2026-08-16-optimise-ux-onboarding-and-functionality.md`
- [major] ~~Reintroduce and validate Dimming/Silence stateful restore on an experimental fork~~ — `.planning/todos/pending/2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md` (**ABSORBED** — experiment ran as Phase 9 and merged to main; device proof moved to the successor below)

**Circle build-out (captured 2026-08-16 — the intervention layer is thinner than the nine-Circle design):**

- [major] Build Circle 8 — the Voice primitive dispatches nothing — `.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md`
- [major] Build Ash as real Color Filters grayscale — `.planning/todos/pending/2026-08-16-build-ash-as-real-color-filters-grayscale.md` (unblocked by spike 005: `AXToggleColorFiltersIntent`, both legs donor-confirmed)
- [major] Dimming and Silence as distinct Circles, device-proven — `.planning/todos/pending/2026-08-16-dimming-and-silence-as-distinct-circles.md` (successor to the two entries above it; ⚠️ writes are live on main with zero device evidence)
- [major] Split Exile into two Circles — straight-to-home and routed-exit — `.planning/todos/pending/2026-08-16-split-exile-into-two-circles.md` (**owns the nine-slots-vs-ten-primitives decision that gates the other three**)

**Backlog (genuinely new work; see ROADMAP.md `## Backlog`):**

- [minor] ~~Phase 999.3 — Grayscale / Ash capability donor test~~ — `.planning/phases/999.3-grayscale-ash-capability-donor-test/` (steps 1–4 resolved by spike 005; step 5 "rebuild Ash" promoted to the todo above)

**Device UAT (verification of already-built phases, not new phases — reclassified 2026-08-16; run via `/gsd-verify-work {phase}`, rolled up by `/gsd-audit-uat`):**

- [blocker] Phase 4 UAT — CLOSE pipeline and session race — `.planning/phases/04-close-pipeline-session-race/04-UAT.md`
- [blocker] Phase 5 UAT — nine Circles, sequence switching, and Circle IX cooldown/route-out — `.planning/phases/05-nine-primitives-environmental-safety/05-UAT.md` (rolled up by the **running** meta todo `.planning/todos/pending/2026-08-16-device-uat-nine-circles-and-sequence-switching.md` — keep the Circle matrix there current; 1 of 9 Circles has ever fired on device)
- [blocker] Phase 9 UAT — Dimming/Silence stateful capture-and-restore — `.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md` (1 of 12 tests passed; the other 11 gate a path that is live on main)
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
- DIST-03 — no iPhone connected. All ten Phase 10 device tests (.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md) are outstanding with blank outcomes, as are Phase 9's UAT tests 2-12 and Phase 4's UAT tests 1 and 3-6. Everything Phase 10 shipped is structurally proven and behaviourally unproven.
- The repaired iOS 26 automation onboarding (quick task 260817-au7, docs/BUILD-NOTES.md §20) is correct as written but device-unproven end to end in this form. The INPUT PROBE proved the Text → Run Shortcut handoff mechanism, not these rendered steps; confirming them belongs with the outstanding device UAT.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260814-kqm | Correct signed AEA1 `.shortcut` recovery instructions | 2026-08-14 | adc96a3 | [260814-kqm-correct-8-signed-aea1-shortcut-artifacts](./quick/260814-kqm-correct-8-signed-aea1-shortcut-artifacts/) |
| 260814-kut | Disambiguate deviation IDs and guard rebuild provenance | 2026-08-14 | 05f69fc | [260814-kut-disambiguate-the-cycle-3-speaktext-devia](./quick/260814-kut-disambiguate-the-cycle-3-speaktext-devia/) |
| 260816-ukb | Strip OPEN_BISECT/ROUTER_TRACE/BUILD_STAMP debug scaffolding | 2026-08-16 | 154b998 | [260816-ukb-strip-the-open-bisect-debug-breadcrumb-s](./quick/260816-ukb-strip-the-open-bisect-debug-breadcrumb-s/) |
| 260817-2ng | Reconcile stale Use Model On-Device literal audit trail (CAP-26/DEV-03/UA-02/BD-04) | 2026-08-17 | 1732448 | [260817-2ng-use-model-literal-reconciliation](./quick/260817-2ng-use-model-literal-reconciliation/) |
| 260817-au7 | Repair the iOS 26 Personal Automation onboarding in both forks; rebuild, re-sign, decrypt-verify | 2026-08-17 | c961af9 | [260817-au7-ios26-automation-onboarding](./quick/260817-au7-ios26-automation-onboarding/) |
| 260817-d9m | Record agent-side tooling and the four-rung evidence-escalation ladder (CLAUDE.md §9); sync STACK.md AEA1 drift; admit simulator/probe evidence in BUILD-NOTES §3 | 2026-08-17 | 5e0a895 | [260817-d9m-record-agent-side-tooling-and-device-evi](./quick/260817-d9m-record-agent-side-tooling-and-device-evi/) |
| 260817-ewg | Reconcile the validator-invocation rule across 7 standing-instruction sites; adopt the two-gate posture (26/all mandatory + 27/all advisory); no shipped defect found | 2026-08-17 | eb87f62 | [260817-ewg-reconcile-validator-invocation-rule](./quick/260817-ewg-reconcile-validator-invocation-rule/) |
| 260817-fae | Downgrade spike 004 to PARTIAL — the ineligible-hardware leg was never tested; propagate to skill, CONVENTIONS, spike 008, wrap-up | 2026-08-17 | c7b834b | [260817-fae-downgrade-spike-004-to-partial-ineligibl](./quick/260817-fae-downgrade-spike-004-to-partial-ineligibl/) |

## Deferred Items

Items acknowledged and carried forward from previous milestone close:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| v2 | CTX-01..04 (contextual exit learning), VAL-01..04 (value measurement), OPT-01..02 (Sentient precomputed Mirror), PAY-01..02 (pay-after-value support) | Deferred to v2 | Requirements definition |

## Deferred Verification

| Phase | State | Resume |
|-------|-------|--------|
| 12 | verification_deferred_human | /gsd-verify-work 12 |

Phase 12's verifier returned `human_needed`: 7 device-only exit-recording tests (already recorded
BLOCKED in `12-UAT.md` — `xcrun devicectl list devices` genuinely reported no connected iPhone, not a
fabricated result) plus two `verification: backstop` truths (A1's `repeat.each`-over-empty-array
assumption, and the JSON-null-leaf coercion assumption the option-a design choice structurally avoids
but doesn't device-confirm). All 27 other must-haves verified; all 12 checkers + gate A×2 pass at HEAD.
This mirrors Phase 10's precedent (DIST-03) — deferred, not treated as a gap, because no device is
available to an autonomous run. Resume with `/gsd-verify-work 12` once an iPhone is connected.

## Session Continuity

Last session: 2026-08-16T15:53:05.418Z
Stopped at: 10-05 checkpoint (human-verify) — resolved 'blocked' on DIST-03; 10-UAT.md authored and unrun
Resume file: .planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md
