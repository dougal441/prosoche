---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
current_phase: 17
current_phase_name: Covenant substrate
status: re-founded
stopped_at: The covenant overhaul (2026-08-19) re-founded the project on canonical strategy v2 — coverage as a routing axis, four fixed bands, verdicts in both forks, personalized descent, deterministic variability (BD-09..BD-12). PROJECT.md, REQUIREMENTS.md, ROADMAP.md rewritten; v1 planning state at git tag pre-covenant-overhaul; licence now PolyForm Noncommercial 1.0.0 going forward. Phases 14/15 remain verification-deferred on device access. Next step is /gsd-plan-phase 17 (covenant substrate); the standing device sitting (14-UAT beside 16-UAT, 15-UAT cold-runnable with its schema-ordering constraint) is unchanged and now lives under Phases 21–22.
last_updated: "2026-08-19T12:00:00.000Z"
last_activity: 2026-08-19
last_activity_desc: Covenant overhaul — canon v2 written, planning docs re-founded, BD-09..BD-12 recorded, roadmap renumbered 17–28, licence changed to PolyForm Noncommercial 1.0.0
progress:
  total_phases: 28
  completed_phases: 16
  total_plans: 60
  completed_plans: 60
---

# Project State

## Project Reference

See: .planning/PROJECT.md (re-founded 2026-08-19)

**Core value:** When use is intentional, PROSOCHĒ is invisible. When intention disappears, it interrupts exactly strongly enough to restore it — and an honest declaration buys back the silence.
**Current focus:** The covenant conversion — Phase 17 (covenant substrate) is next to plan

## Current Position

**RE-FOUNDED 2026-08-19 — the covenant overhaul.** The project was re-founded on canonical
strategy **v2.0 (the covenant model)**: contract coverage is a routing axis above the Circle
ladder, four fixed bands (Silent 0 / Ambient 1–3 / Ask 4–6 / Rescue 7–9), ALLOW/CHALLENGE/DENY
verdicts in both forks inside a deterministic envelope, personalized descent, and deterministic
anti-ritualisation variability. Decisions **BD-09..BD-12** in `docs/CAPABILITY-DECISIONS.md`;
v1 planning state preserved in full at git tag **`pre-covenant-overhaul`** (commit `10305e6`);
canon v2 Appendix A maps every historical §N citation. PROJECT.md, REQUIREMENTS.md and
ROADMAP.md were rewritten the same day: phases 1–16 are the delivered foundation (execution
record retained), phases 17–28 are the conversion and beyond. **The shipped artifacts still
implement the v1 interaction model until Phases 17–20 land** — a recorded build state, not a
contradiction. The licence moved MIT → **PolyForm Noncommercial 1.0.0** going forward (BD-12,
not retroactive). Next step: `/gsd-plan-phase 17`.

Phase 15 (the last v1-foundation phase executed): 5/5 plans complete; verifier 25/27, 0 failed; the 2 outstanding are device-gated and abstained

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

~~**Phases 11-20 are scoped and queued but none is planned.**~~ **[SUPERSEDED 2026-08-19 by
the covenant overhaul — retained struck as the record of the pre-overhaul queue.]** Phases
11–16 of that queue are executed; the covenant conversion replaced the rest and renumbered
everything downstream (see the Roadmap Evolution entry below). The standing sequencing fact
that survives: Phase 13's blank-List/red-operator fixes landed, so a blank Circle in Phase 22's
device testing is a real finding rather than a known artifact.

**Standing device backlog**, all blocked on DIST-03 and best run in one session:
`16-UAT.md` (12 tests — dimming/silence capture-and-restore, **the highest-risk untested path
in the product**, and the instrument that **supersedes `09-UAT.md`**; its single recorded pass
does not carry forward, because plan 16-02 showed the coercion-chip gate carries no information
at a direct Set-action parameter), `12-UAT.md` Test 3 (the same brightness/volume restore
observation read from the SESS-07 side — run it once, record it in both files), `13-UAT.md`
(6 tests), `10-UAT.md` (10 tests), Phase 4 UAT tests 1 and 3-6, Phase 8's real-iPhone import,
the locked-screen CLOSE investigation (now **Phase 21** after the 2026-08-19 renumbering; it
owns the screen-locked case; `16-UAT.md` hands it over by reference rather than duplicating it),
and the full nine-Circle sweep (now **Phase 22**, re-scoped to cover the covenant model too).
Report the opens-to-first-interruption count from `10-UAT.md` Test 2 — it decides whether Phase
10's raised entry thresholds need tuning. `16-UAT.md`'s header carries the batching table.

**DIST-03's blocked REASON, re-measured 2026-08-18 (plan 16-06):** ~~`xcrun devicectl list
devices` reports no connected devices~~ — that wording is **retired**, struck rather than
deleted so the correction has something to point at. Measured at execution time: a **paired**
iPhone 15 Pro (`iPhone16,1`) on **iOS 26.6**, `pairingState: paired`, **`tunnelState:
unavailable`**, `transportType: none`; the `State` column reads `unavailable`. So a device is
known but **there is no live tunnel and no active transport — no session to drive**, which is a
different fact from "no device exists" and is recorded as the different fact it is. The reason
has now moved twice: 2026-08-17 measured `tunnelState: disconnected` with `transport: wired`.
**Always branch on `tunnelState` read from `--json-output`, never on the `State` column** —
on 2026-08-17 the column read `available (paired)` while the tunnel was down. Two consequences
worth carrying: `iPhone16,1` is **Apple-Intelligence-capable**, so this hardware can exercise
the **Aware** fork when a session is arranged; and **iOS 26.6 is inside the declared `iOS 26.x`
target**, so an observation on it is same-major-version evidence rather than an extrapolation.
Personal Automations are user-created on the device regardless, so DIST-03 would gate this work
even with a live tunnel.

Last activity: 2026-08-18 — Phase 15 execution started

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
- [Phase 9] — **⚠ SUPERSEDED IN PLACE 2026-08-18 by D-01; see the [Phase 16] entry immediately below, which is the current record. Retained, not deleted: this log's value is that it shows what was believed when.** BD-02's brightness floor clause corrected (the retired wording is cited, not restated) — user-reported on-device observation is that iOS's practical brightness minimum is dim, not a literal black/unusable screen, so avoiding it was never itself the safety requirement. The safety mechanism is capture-and-restore reliability (Get Device Details → has-any-value guard → snapshot → restore on CLOSE/Emergency Restore), which BD-02 already specified and Phase 9 exists to prove under real failure modes. *Three claims in this entry are now false on this branch:* that the correction is scoped to this experimental fork only, that the main line's floor is untouched, and that it is provisional.
- [Phase 16]: **D-01 — the brightness floor is SETTLED ON THE MAIN LINE.** User decision, LOCKED 2026-08-17. `safety.brightness_floor` `0.10 → 0` and `safety.dim_target` `0.12 → 0` in both shipped forks — the target follows the floor down because a floor under an unchanged target would never bind. Plan **16-03** carried the code half (six code sites, including the emitted Shortcuts comment that shipped 11× per fork asserting a bound the same build set to zero); plan **16-05** carried the record half — 21 measured sites across nine files — and added `docs/retired_clause_check.py`, a repo-scoped gate that reports every surviving lexical occurrence with file and line. `PROSOCHE_Nine_Circles_Canonical_Strategy.md` is **frozen** as the original design input and is not edited; `docs/CAPABILITY-DECISIONS.md` BD-02's Supersession note records that §21's floor clause is superseded on main and is the authority where the two disagree. **The safety property is unchanged and was never the bound:** the original is captured **and durably persisted** before any change (made true by plan 16-01) and always restored. **Not settled by this decision:** the capture-and-restore loop is still device-unproven and the dim-not-black observation still rests on one unrepeated user report — both BLOCKED on DIST-03.

- Phase 10 added: Ship-readiness remainder and UX-lite pass. **The brightness/volume MVP cut is cancelled and is NOT part of this phase** — Dimming and Silence stay, each as its own distinct Circle, with working brightness and volume capture-and-restore (user decision 2026-08-16, reaffirmed 2026-08-17). Consequences: the SAFE-05 conflict resolves rather than deferring to milestone close, and DEV-06 is live again rather than moot. Research (`10-RESEARCH.md`, 925 lines) was salvaged from an abandoned branch and moved into the phase directory rather than regenerated; its Finding 2 and Pitfalls 2–3 cover the cancelled cut and are superseded, the rest stands.
- [Phase 10]: Circle 8 dispatching nothing (the `"Voice"` sequence entry matching no branch under condition-99 "contains") is a known open defect deliberately left for a later phase. Any sequence/dispatch checker added here must record the orphan rather than fail on it, and must not hard-code condition 99 or substring matching — BD-06 moves dispatch to condition 4 exact matching and abolishes combined entries.

- Phases 11-20 added 2026-08-17, scoped 1:1 from the remaining pending todos in the agreed execution order. Each goal is written to be plannable without this session's context. Order and prerequisites: 11 Addendum 01 (applies BD-06) → 12 sentinel gaps (**gates 17**) → 13 red operators + List wrapper (**should precede 19**) → 14 Ash grayscale → 15 Voice → 16 Dimming/Silence device proof → 17 Exile split → 18 locked-screen CLOSE → 19 device UAT → 20 heavy UX.
- [Phase 11+]: BD-06 (`docs/CAPABILITY-DECISIONS.md`) settles Circle naming, the ten-primitive roster and slot allocation, and is BINDING on phases 11, 14, 15, 16 and 17 — none of them re-cuts the table. Dante names are positional (Circle 1 = Limbo … 9 = Treachery); ten primitives fill nine slots per sequence; combined entries are abolished so dispatch moves to condition 4 exact matching; the routed Exile lands the user directly.
- [Todos]: #2 (iOS 26 automation onboarding), #5 (ship-readiness, absorbed by Phase 10), #12 (Use Model literal, closed as bookkeeping), #13 (dimming/silence experimental fork, absorbed) are closed. Ten remain pending, each now owned by a phase.

- Phase 21 added 2026-08-17: One product or two — Core/Aware fork decision and device eligibility. Gives SEED-006 (merge Dumb/Sentient) an owning phase and folds in the evidence that has accumulated since it was planted: spike 003 INVALIDATED auto-detection (`Device Model` returns bare `"iPhone"`; no try/catch exists), spike 008 VALIDATED `WFLLMModel = "Apple Intelligence on Device"` (closing SEED-006 blocker #2), and `tools/build_sentient.py` already ships the Aware delta as one gated additive insertion. The strategy amendment (§35/§5.7/§31/§13, §38 "document wins") and SEED-006 blocker #3 (provable determinism in a single graph) are what Phase 21 is for. If the answer is TWO products, the better deliverable is a *state* check (Settings → Apple Intelligence & Siri exists and has finished setting up) rather than a model list, since success tracks model presence not just chip class; the A17 Pro/A18 + 8 GB rule alone misleads, as the plain iPhone 15/15 Plus do not qualify while the 16e does. SEED-005 is a hard prerequisite if the merge is chosen.
- [Phase 21 / spike 004]: **verdict downgraded VALIDATED → PARTIAL, 2026-08-17.** Owner reported an iPhone 16e (capable, models downloaded) running the Capability Gate shortcut successfully; re-reading the spike in that light found two defects in its claim. (1) Its `askllm` omits `WFLLMModel` entirely — verified against `.planning/spikes/004-capability-gate/drafts/*.xml` — so neither device run exercised the pinned `"Apple Intelligence on Device"` path that `src/PROSOCHE-Sentient.xml` ships; the runs used the undocumented default model source. (2) The iPhone SE's error, *"support for selected model is downloading"*, is a **provisioning-state** message that cannot distinguish ineligible hardware from a capable device whose ~7 GB models have not landed — and the spike did not record which SE generation it was. Consequence for the merge: the failure window is **wider** than "users who answer the toggle wrongly on old hardware" — Apple Intelligence is on by default on capable devices since iOS 18.3 but its models download over Wi-Fi/power, so a merged product exposes the failure path to **new users on capable hardware at first run**. What survives: the toggle gates correctly both ways, and the ordering property held under one real observed failure. No try/catch remains confirmed — now by an Apple DTS engineer directly ("no way to detect an error from an action"). Four untested device states are tabulated in ROADMAP Phase 21 item 3. **[Renumbered 2026-08-19: the fork-decision phase is now Phase 25; the spike analysis above carries forward into it unchanged.]**

- **[Covenant overhaul, 2026-08-19]: the roadmap was re-founded on canonical strategy v2.** Phases 1–16 became the delivered-foundation record; the old unexecuted phases 17–24 were replaced by the conversion sequence 17–28: **17** covenant substrate (+ gravity floor, enabled_exits, recent_contracts) → **18** bands & surfaces (absorbs the old Exile-split phase; pre-menu retired; slot table v2) → **19** personalized descent → **20** Aware verdict alignment (absorbs SEED-005's refork) → **21** device debug & locked-screen CLOSE (old phase 18 + the two debug blockers) → **22** device UAT re-scoped to the covenant model (old phase 19) → **23** variability against ritualisation (new) → **24** heavy UX (old phase 20, reduced — SEED-009 items 1 and 4 were resolved by design in BD-09) → **25** fork decision (old 21) → **26** aggregates (old 22, + covenant metrics) → **27** Attention Receipt (old 23) → **28** impact & reciprocity (old 24, licence settled by BD-12). Old-numbered citations in phase records and UAT files resolve through this mapping.

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- **[Covenant overhaul, 2026-08-19] BD-09..BD-12 LOCKED**: the covenant model (coverage axis, four fixed bands, verdicts in both forks inside a deterministic envelope, slot table v2 superseding BD-06 Decision 4, pre-menu retired, Dim split with Blackout parked, canon v1 freeze superseded by the v2 rewrite with git-tag provenance); personalized descent (severity → profile, modality → sequence); deterministic anti-ritualisation variability (spot check Band-C-only, ships off, researched at Phase 23); licence PolyForm Noncommercial 1.0.0 going forward (MIT not retroactive; SEED-008's tension resolved toward pay-after-value)
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
bare-minimum-to-working-product device verification (the former ROADMAP 999.x mechanism —
retired; device verification now lives in phase-directory `*-UAT.md` files rolled up by
`audit-uat`, and Phase 22 owns the sweep). Seed = forward-looking, tracked in
`.planning/seeds/`.

**Ownership re-mapped 2026-08-19 by the covenant overhaul:** `recent_contracts` (F-2) and
`enabled_exits` (F-18) and the Gravity floor are owned by **Phase 17**; the deferred-intervention
(F-12) and Mirror-picker blockers by **Phase 21**; the split-Exile todo is absorbed by **Phase 18**
(BD-09 Decision 7); the apply-Addendum-01 todo was completed by Phase 11 and stays only as a
record; the UX todo's surviving scope is **Phase 24**. Old phase numbers inside todo bodies read
through STATE.md's renumbering entry above.

**Device-session blockers (captured 2026-08-19 from the 18/19 Aug device UAT — 23 findings):**

- [blocker] `enabled_exits()` filters nothing; disabled exits are offered, selectable and routed — `.planning/todos/pending/2026-08-19-enabled-exits-filters-nothing.md` (F-18; **prerequisite** to any exit-learning measurement — evidence gathered before this lands must be discarded)
- [blocker] An OPEN's intervention can be deferred by minutes and surface after the app is closed — `.planning/todos/pending/2026-08-19-deferred-open-intervention.md` (F-12; **severity raised major→blocker 2026-08-19**; route `/gsd-debug` — mechanism is a hypothesis)
- [blocker] Mirror primitive fails with an unfilled required picker — `.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md` (now halts Circle VIII/Voice as well as VII; route `/gsd-debug` — not localised)
- [major] Gravity is never floored; escalation off-spec on all three profiles — `.planning/todos/pending/2026-08-19-floor-gravity-to-match-spec.md` (one-line fix; land **before** the next Pressure-accumulation run or that run measures the defect)
- [major] `recent_contracts` is never written by any code path — `.planning/todos/pending/2026-08-19-recent-contracts-never-written.md` (F-2; scope decision first, then phase work; Phase 06 Test 8 is currently unpassable)

**Todo list re-derived 2026-08-19 (covenant overhaul hygiene).** Six former entries here had
already moved to `.planning/todos/completed/` (automation onboarding — quick 260817-au7;
red-operator/List-wrapper — Phase 13; ship-readiness — Phase 10; Use Model literal — quick
260817-2ng; Dimming/Silence experimental fork — Phase 9; Circle 8 Voice — Phase 15). The
current pending set:

**Still open, executed-but-device-unproven (files annotated; device proof owned by Phase 22):**

- Apply Build Addendum 01 — `.planning/todos/pending/2026-08-14-apply-build-addendum-01.md` (**completed by Phase 11**; retained as record)
- Close the state-shape sentinel gaps — `.planning/todos/pending/2026-08-15-close-state-shape-sentinel-gaps.md` (**executed by Phase 12**; device exit-path test outstanding)
- Build Ash as real Color Filters grayscale — `.planning/todos/pending/2026-08-16-build-ash-as-real-color-filters-grayscale.md` (**executed by Phase 14**; `14-UAT.md` blank)
- Dimming and Silence as distinct Circles, device-proven — `.planning/todos/pending/2026-08-16-dimming-and-silence-as-distinct-circles.md` (**built; the device-proven half is Phase 22 / `16-UAT.md`**)

**Still open, owned by covenant-conversion phases:**

- Optimise/streamline UX — `.planning/todos/pending/2026-08-16-optimise-ux-onboarding-and-functionality.md` (surviving scope → **Phase 24**; menu/order questions resolved by BD-09)
- Split Exile into two Circles — `.planning/todos/pending/2026-08-16-split-exile-into-two-circles.md` (**absorbed by Phase 18** under BD-09 Decision 7)

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
- **[Phase 16, 2026-08-18] DIST-03 — THE CURRENT RECORD. This entry supersedes the reason given in the three entries below it, which are retained as the record of what was measured when they were written.** Re-measured at plan 16-06 execution time: a **paired** iPhone 15 Pro (`iPhone16,1`) on **iOS 26.6**, `pairingState: paired`, **`tunnelState: unavailable`**, `transportType: none`, `State` column `unavailable`. **The blocker is real but its reason has changed: it is not that no device is known, it is that the known device has no live tunnel and no active transport — no session to drive.** The reason has moved twice now (2026-08-17 measured `tunnelState: disconnected`, `transport: wired`), which is why any executor must **branch on `tunnelState` read from `xcrun devicectl list devices --json-output`, never on the `State` column** — the column read `available (paired)` on 2026-08-17 while the tunnel was down. Recording "no devices found" today would be recording something false, which this project forbids exactly as firmly as a false pass. Outstanding and blocked on this: `16-UAT.md` (12 tests, all blank), `13-UAT.md` (6), `12-UAT.md` (incl. Test 3), `10-UAT.md` (10), Phase 4 tests 1 and 3-6, Phase 8's real-iPhone import, Phase 18's locked-screen investigation, Phase 19's nine-Circle sweep. **Everything Phase 16 shipped is structurally proven and behaviourally unproven** — the capture-and-restore loop has still never executed on hardware, and Emergency Restore has still never been tapped on a device.
- ~~DIST-03 real-iPhone import and first Manual UAT blocked: xcrun devicectl reports no connected devices.~~ **[reason superseded 2026-08-18 — see the Phase 16 entry above; the import and first Manual UAT are still outstanding]**
- Phase 9 Plan 02 Tasks 2-3 blocked: 09-UAT.md's 12 device-proving tests (coercion-chip gate, capture/restore, failure-mode trials, DEV-06 verdict) require a real Apple-Intelligence-capable iPhone on iOS 26.x. ~~xcrun devicectl reports zero connected devices~~ — **[reason superseded 2026-08-18, see above]**. Both re-signed .shortcut artifacts and the fully-authored 09-UAT.md are ready; resume via /gsd-verify-work 9 once a device is available. **[SUPERSEDED 2026-08-18 by Phase 16: `09-UAT.md` is superseded by `16-UAT.md`, which carries a build-identity header it lacks; its one recorded pass (the coercion-chip gate) does NOT carry forward, because plan 16-02 measured that the chip cannot discriminate at a direct Set-action parameter at all.]**
- ~~DIST-03 — no iPhone connected.~~ **[reason superseded 2026-08-18, see above]** All ten Phase 10 device tests (.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md) are outstanding with blank outcomes, as are Phase 9's UAT tests 2-12 (now carried by `16-UAT.md`) and Phase 4's UAT tests 1 and 3-6. Everything Phase 10 shipped is structurally proven and behaviourally unproven.
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
| 260818-ugp | Fix audit-uat's two silent under-reports (26→89 items); archive superseded Phase 06 verification; add OUTSTANDING.md for non-UAT-file items | 2026-08-18 | 9ce2302 | [260818-ugp-close-three-uat-tracking-gaps](./quick/260818-ugp-close-three-uat-tracking-gaps/) |

## Deferred Items

Items acknowledged and carried forward from previous milestone close:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| v2 | CTX-01..04 (contextual exit learning), VAL-01..04 (value measurement), OPT-01..02 (Sentient precomputed Mirror), PAY-01..02 (pay-after-value support) | Deferred to v2 | Requirements definition |

## Deferred Verification

| Phase | State | Resume |
|-------|-------|--------|
| 11 | verification_deferred_human | /gsd-verify-work 11 |
| 12 | verification_deferred_human | /gsd-verify-work 12 |
| 13 | verification_deferred_human | /gsd-verify-work 13 |
| 16 | verification_deferred_human | /gsd-verify-work 16 |
| 14 | verification_deferred_human | /gsd-verify-work 14 |
| 15 | verification_deferred_human | /gsd-verify-work 15 |

**Phase 14 (added 2026-08-19).** Executed clean — 3 plans, 9 tasks, 3 waves, all merged, both
forks re-signed. Verification scored **27/34, `human_needed`**: 27/27 structural must-haves
verified **against the decrypted signed artifacts**, not merely the source, and all 14
`docs/*.py` checkers green. The 7 abstentions are all `verification: backstop` truths that no
file-level analysis can reach — whether the screen actually goes greyscale, whether colour
actually returns on CLOSE / Emergency Restore / Ice expiry / the live-Ice redirect, whether the
forks import without an unfilled-parameter dialog, whether the Note disclosure renders, and
whether the kill switch really leaves Color Filters untouched. Each abstained as
`insufficient_spec` rather than inheriting a pass from the structure beneath it, which is the
correct outcome. `14-UAT.md` carries 6 tests, all blank, `status: blocked`.

**DIST-03 re-measured 2026-08-19 at execution time:** iPhone `dougal` (`iPhone16,1`),
`pairingState: paired`, **`tunnelState: unavailable`**, `transportType: none`. Same reason as the
Phase 16 entry below — a known device with no live tunnel and no active transport, so there is no
session to drive. Deferred by user decision 2026-08-19.

**What this phase makes cheap:** grayscale restore is routed through `restore_managed_settings()`
alongside brightness and volume, so **one device sitting proves all three environmental
primitives**. `14-UAT.md` is deliberately designed to be run beside `16-UAT.md`'s twelve
outstanding tests. The single highest-value observation in either file: force-quit mid-intervention
so no CLOSE can fire, then run Emergency Restore, and confirm colour comes back — with no snapshot
by design, that path is the only thing between a user and permanent greyscale.

**Accepted, not mitigated:** a user who already runs Color Filters has their own accessibility
setting switched off. There is no read-back for any accessibility setting on iOS. Backlogged at
`.planning/todos/pending/2026-08-19-ash-void-circle-when-user-already-uses-grayscale.md`; the
`safety.ash_managed_color_filters` kill switch is the only recourse until that lands.

**Phase 15 (added 2026-08-19).** All five plans executed; verifier scored **15/15 structural
must-haves, `human_needed`**, with zero structural gaps found. It is not `passed` for one honest
reason: **nothing in phase 15 has run on a phone.** Plan 15-02's rung-2 simulator probe (spike 011)
returned `not discriminated at rung 2` — none of `list` / `getitemfromlist` / `speaktext`
reproduced the device-observed axis-4 unfilled-picker defect — so it was correctly routed to D-04
Branch B with no speculative fix, and **CIRC-08 remains structurally proven and behaviourally
UNPROVEN**. `MANIFEST.md`, `docs/BUILD-NOTES.md` §36 and `15-UAT.md` each state this plainly and
independently. `15-UAT.md` is cold-runnable and digest-pinned to the shipped artifacts: 4 tests,
0 run. **DIST-03 is lifted**, so these are runnable in the next Mirroring session — expect Tests
1–3 to hit the known axis-4 error, which the instrument warns about at its head.

**Sequencing constraint from plan 15-03, carry this into the next device session:** install the
Phase 15 build **BEFORE** the Pressure-accumulation UAT, never after. `schema_version` moved 4 → 5,
and the first run of the new build rebuilds `state.json`, wiping `heat`, `gravity`, `pressure`, the
rolling windows, `exit_events` and every `exit_stats[*].samples`. Doing the accumulation first
throws that session away. A `.shortcut` re-install alone does **not** wipe `state.json` — only the
bump does.

**DIST-03 — the two entries above disagree, and the later measurement wins.** Phase 15's note
(written 2026-08-19) says DIST-03 is lifted; Phase 14 re-measured it at execution time the same
day and found iPhone `dougal` (`iPhone16,1`) `pairingState: paired` but **`tunnelState:
unavailable`, `transportType: none`** — a known device with no live tunnel and no session to
drive. Both statements were true when written: Mirroring was live during the 2026-08-17/18
session and the tunnel was down when Phase 14 ran. **Branch on `tunnelState` read from `xcrun
devicectl list devices --json-output`, never on the `State` column or on either of these notes.**
The practical consequence is unchanged for both phases: the device work is runnable the moment a
session is up, and neither phase's UAT has been run.

**Run 15-UAT.md and 14-UAT.md in the same sitting, and mind plan 15-03's ordering constraint:**
install the Phase 15 build **before** any Pressure-accumulation UAT, because `schema_version`
4 → 5 makes the first run rebuild `state.json` and wipe every accumulated counter. Phase 14
introduces no schema change and adds no ordering constraint of its own.

**Phase 11 (added 2026-08-18).** Gap-closure waves 7-10 executed, code-reviewed and fix-passed
twice; re-verification scored **18/21, `human_needed`**, with all five original gaps CLOSED and each
closure negative-controlled. It is not `passed` for one reason, and it is a good reason: plan 11-08
made **44 environmental actions per fork reachable for the first time**, and none has executed on
hardware — `Set Brightness` cannot run on a simulator at all, and the Note path needs an app the
simulator lacks. Structural fixes were deliberately not promoted into behavioural passes.
`11-UAT.md` records 6 items: 5 BLOCKED on DIST-03, 1 resolved without a device (the stale
`16-UAT.md` pin, re-pinned in `7352886`). Tests 1-2 overlap `16-UAT.md` and should be run in the
same session — run `16-UAT.md` first, it is the fuller instrument.

Phase 13's verifier returned `human_needed` at **25/27 must-haves verified, 0 failed**. The only two
outstanding are device-gated and were correctly abstained rather than promoted on structural
evidence: whether a wrapped List row actually renders non-blank on device, and what `Item At Index`
returns over a wrapped List (`verification: backstop`, research Open Question 1 / assumption A4).
`xcrun devicectl list devices` was run and reported no connected iPhone; `13-UAT.md` records six
tests, 0 passed, all BLOCKED. Same DIST-03 precedent as Phases 10 and 12. Resume with
`/gsd-verify-work 13` once an iPhone is connected — and note `13-UAT.md` Test 1 now asks the tester
to record *which* row was showing, because row 8 is a bare literal row after the CR-01 fix, so a
blank at Circle VIII would indict the literal path rather than the wrapper.

**Phase 13's code-review pass found a real defect in the phase's own fix — worth carrying forward.**
`_list_row()` discriminated on Python type (`isinstance(item, str)`) rather than on
attachment-bearing-ness, so 44 attachment-free (literal-by-content) rows shipped inside the
variable-row wrapper — a *second* unevidenced framing, invisible to the guard, the validator and the
decrypt, at row 8 / Circle VIII. Fixed and fully re-shipped at `365937e`; shipped census is now
**616 wrapped / 50 bare** per fork, not the 660/6 the plan SUMMARYs record. Any doc still citing
660/6 or artifacts `fe1bafdf…`/`bd1264d5…` is describing the superseded `737ce07` build.

Phase 12's verifier returned `human_needed`: 7 device-only exit-recording tests (already recorded
BLOCKED in `12-UAT.md` — `xcrun devicectl list devices` genuinely reported no connected iPhone, not a
fabricated result) plus two `verification: backstop` truths (A1's `repeat.each`-over-empty-array
assumption, and the JSON-null-leaf coercion assumption the option-a design choice structurally avoids
but doesn't device-confirm). All 27 other must-haves verified; all 12 checkers + gate A×2 pass at HEAD.
This mirrors Phase 10's precedent (DIST-03) — deferred, not treated as a gap, because no device is
available to an autonomous run. Resume with `/gsd-verify-work 12` once an iPhone is connected.

Phase 16's verifier returned `human_needed` at **73/81 must-haves verified, 8 abstained, 0 failed**.
The eight are `verification: backstop` truths that need real hardware and were correctly abstained
rather than promoted on structural evidence. `16-UAT.md` records 12 tests, 0 passed, all BLOCKED.

**The DIST-03 reason is NOT "no devices found" — that phrasing is retired.** Measured three times
this phase and it moved every time: session start returned no devices; planning measured
`pairingState: paired` / `tunnelState: disconnected` / `transportType: wired`; plan 16-06 and an
independent orchestrator re-check both measured `tunnelState: unavailable` / `transportType: none`.
Current true reason: **a paired iPhone 15 Pro (`iPhone16,1`) on iOS 26.6 is known to the host, but
there is no live tunnel and no transport, so there is no session to drive.** Any re-measurement MUST
branch on `tunnelState` from `--json-output`, never on the `State` column, which prints
`available (paired)` even with the tunnel down.

**What IS proven, so a later reader does not re-derive it:** the Phase 9 persistence P0 is closed —
22 exact `CAPTURE(State) → SAVE(source=State) → APPLY` triples per fork, covering all 11
`primitive_dispatch()` renderings including the 9 MANUAL `Test a Circle` cases. Both LOCKED user
decisions landed (D-01 floor and dim target both `0`; D-02 `changed_at` / `changed_by_session_id`
removed at 44 write sites per fork, with a two-surface no-reader guard). 13 checkers green including
the new `docs/retired_clause_check.py`; gate A clean on both forks; both artifacts re-signed and
decrypt-verified byte-identical to source.

**Two residual risks to hold when the session is arranged.** CAP-08 makes silent failure the default —
`setbrightness.WFBrightness` is OPTIONAL and defaults to 50%, so an unresolved operand applies an
unrequested 50% with no capture and no error; Test 1 must observe the *value applied*, never the
absence of an error. And `dim_target = 0` ships on one unrepeated user report — D-01 is a settled
*decision*, not a settled *device fact*.

Batch the session: `16-UAT.md` shares its setup with `12-UAT.md` Test 3, Phase 21 (locked-screen
CLOSE, which owns that case deliberately — renumbered from 18 on 2026-08-19), Phase 22 (the
covenant device UAT, renumbered from 19), `13-UAT.md` and `10-UAT.md`. Resume with
`/gsd-verify-work 16`.

## Session Continuity

Last session: 2026-08-16T15:53:05.418Z
Stopped at: 10-05 checkpoint (human-verify) — resolved 'blocked' on DIST-03; 10-UAT.md authored and unrun
Resume file: .planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md
