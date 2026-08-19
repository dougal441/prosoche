# Roadmap: PROSOCHĒ — Nine Circles

## Overview

**Re-founded 2026-08-19 on canonical strategy v2 — the covenant model.** Phases 1–16 are the
delivered v1 foundation: capability audit, routing/bootstrap/Note onboarding, the deterministic
Heat/Gravity/Pressure engine, the race-proof CLOSE protocol, ten built primitives (including real
Color Filters grayscale and the Voice primitive), six exits with deterministic learning, the
Aware fork as an additive wrap, and the full build-guard discipline. Their detail sections below
are retained verbatim as the execution record — they describe work done under the v1 model and
are history, not live instruction; the live spec is canon v2, and historical `§N` citations
resolve through its Appendix A. Forward pointers inside those sections use the pre-overhaul
numbering — read them through this map: old 17 (Exile split) → absorbed by new 18; old 18
(locked-screen CLOSE) → 21; old 19 (device UAT) → 22; old 20 (heavy UX) → 24; old 21 (fork
decision) → 25; old 22 (aggregates) → 26; old 23 (receipt) → 27; old 24 (sharing/support) → 28.

Phases 17–28 are the covenant conversion and everything after it. The conversion order is
substrate → surfaces → onboarding → Aware (17–20), so the artifact is coherent at every commit;
then the device work (21–22) converts the whole model from structurally-proven to
actually-working; then variability research (23), the heavy UX round (24), the fork decision
(25), and the value/receipt/reciprocity arc (26–28). The shipped artifacts implement the v1
interaction model until Phases 17–20 land — a recorded build state, restated in the MANIFEST,
not a contradiction. Definition of done for the milestone: both signed `.shortcut` files
implementing canon v2, device-verified through Phase 22.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

**Delivered v1 foundation (execution record):**

- [x] **Phase 1: Capability Audit & Config Foundation** - All four capability blockers resolved with fallback designs; the tunable config block locked
- [x] **Phase 2: Routing, Bootstrap & Control Room Onboarding** - First-run bootstrap, the Note, and self-healing routing
- [x] **Phase 3: Deterministic State Engine** - Heat, Gravity, Pressure, and Circle mapping, demonstrably different across profiles
- [x] **Phase 4: CLOSE Pipeline & Session Race Protocol** - Race-proof session measurement (device UAT partial)
- [x] **Phase 5: Nine Primitives & Environmental Safety** - The primitive layer with safety floors and model-free Circle IX (device proof → Phase 22)
- [x] **Phase 6: Exits, Exit Learning & Contracts** - Six exits, deterministic learning, contracts feeding Heat (F-18 fix → Phase 17)
- [x] **Phase 7: Control Room Manual Menu, Dumb Mirror Engine & Dumb Freeze** - Core complete as a product; real-iPhone UAT pending
- [x] **Phase 8: Sentient Fork & Dual Distribution** - Aware as an additive wrap; both forks signed (DIST-03 pending)
- [x] **Phase 9: Dimming/Silence Stateful Restore** - Numeric-coercion fix merged for all 28 sites; device proof carried forward
- [x] **Phase 10: Ship-readiness remainder and UX-lite pass** - Circle 0 silent band, OPEN notification removed, structural guards
- [x] **Phase 11: Build Addendum 01** - Dante positional names, Core/Aware rename, exact-match dispatch, Panic Escape removability
- [x] **Phase 12: State-shape sentinel gaps** - exit_events and active_session seeded and leaf-gated
- [x] **Phase 13: Red-operator conditionals and the WFItems List wrapper** - The wrapper family fixed by class; the conditional family pinned as correct
- [x] **Phase 14: Ash as real Color Filters grayscale** - The real toggle with the unconditional restore leg
- [x] **Phase 15: Circle 8 — the Voice primitive** - Nine working Circles
- [x] **Phase 16: Dimming and Silence — persistence fix and D-01/D-02** - Capture persisted before the device changes; device proof → Phase 22

**The covenant conversion and beyond (canonical strategy v2):**

- [ ] **Phase 17: Covenant substrate** - Contract windows, the coverage gate, Core's deterministic verdict, recording — plus the engine fixes that block clean measurement
- [ ] **Phase 18: Bands and surfaces** - The pre-menu retired, Band B silent, one surface per OPEN, in-surface leave, slot table v2, Redirect built, exits deepened
- [ ] **Phase 19: Personalized descent** - Severity → profile, modality → sequence; onboarding asks feelings, not mythology
- [ ] **Phase 20: Aware verdict alignment** - The model verdict inside the deterministic envelope; no model on covered opens
- [ ] **Phase 21: Device debug and locked-screen CLOSE** - The deferred-intervention and Mirror-picker blockers, plus the locked-screen persistence investigation
- [ ] **Phase 22: Device UAT — bands, coverage, nine Circles, sequences** - The covenant model converts from structurally-proven to actually-working on real hardware
- [ ] **Phase 23: Variability against ritualisation** - Research and arm the deterministic spot check, after device evidence exists
- [ ] **Phase 24: UX optimisation — onboarding and in-run interaction cost** - Funnel instrumentation, latency, copy voice, Note restructure
- [ ] **Phase 25: One product or two — Core/Aware fork decision** - Settle the merge question with the capability-gate experiment
- [ ] **Phase 26: Cumulative state — lifetime and windowed attention aggregates** - The honest data layer, now including covered share and surfaces/day
- [ ] **Phase 27: The Attention Receipt** - A disposable, regenerated, screenshotable local Note — a receipt, not a scoreboard
- [ ] **Phase 28: Impact and reciprocity — sharing, then support** - Share first, pay-what-it-was-worth later; no account, no referral, no tracking

## Phase Details

### Phase 1: Capability Audit & Config Foundation

**Goal**: Every iOS action PROSOCHĒ depends on is resolved to VERIFIED / UNVERIFIED / NOT AVAILABLE with its exact identifier and parameter shape before any behavioural logic is authored, and the tunable static config exists as a single editable block.
**Mode:** mvp
**Depends on**: Nothing (first phase)
**Requirements**: AUDIT-01, AUDIT-02, AUDIT-03, AUDIT-04, AUDIT-05, AUDIT-06, AUDIT-07, AUDIT-08
**Success Criteria** (what must be TRUE):

  1. A build-notes document lists every dependent iOS action with VERIFIED/UNVERIFIED/NOT AVAILABLE status and exact identifier/parameter shape, and every deviation forced by an unverifiable action is recorded with the fallback taken while the Shortcut remains runnable.
  2. Grayscale/Color Filters capability has a documented go/no-go decision, with a documented fallback design for the Ash primitive if no safe action exists.
  3. Brightness and volume read-back capability are each resolved; if no safe read path exists, Dimming and Silence are specified to degrade to non-stateful variants rather than making an unrestorable change.
  4. Notes actions (Create Note, Append to Note, find/show a Note) are confirmed usable on the iOS target.
  5. The `Use Model` On-Device selection literal is recovered by round-trip (select On-Device in Shortcuts, export unsigned XML, read the literal back) and recorded verbatim, or the Sentient fork's On-Device guarantee is explicitly re-planned; a single editable Config block (profile threshold tables, sequence orderings, Ice cooldown durations, Heat coefficients) exists in the graph.

**Plans:** 5/5 plans executed

Plans:

- [x] 01-01-PLAN.md — Tracer: Ash / Color Filters end to end through all three Phase 1 artifacts, plus the do-not-fabricate and evidence protocols
- [x] 01-02-PLAN.md — Capability audit rows for the data, control-flow, interaction and output actions
- [x] 01-03-PLAN.md — The complete Config JSON literal, field reference, derived-value rules and transcription recipe
- [x] 01-04-PLAN.md — Notes on the iOS target (BD-05) and brightness/volume read-back (BD-02, BD-03)
- [x] 01-05-PLAN.md — Use Model On-Device literal (BD-04), the Phase 8 gate, coverage check and phase closure

### Phase 2: Routing, Bootstrap & Control Room Onboarding

**Goal**: A user can import the Shortcut, run it manually for the first time, and get a working state.json plus a fully instructive Control Room Note — and every subsequent invocation routes correctly and never corrupts or duplicates that foundation.
**Mode:** mvp
**Depends on**: Phase 1
**Requirements**: BOOT-01, BOOT-02, BOOT-03, BOOT-04, BOOT-05, BOOT-06, BOOT-07, BOOT-08, BOOT-09, STATE-12, ROOM-01, ROOM-02, ROOM-03, ROOM-04, ROOM-05, ROOM-06
**Success Criteria** (what must be TRUE):

  1. Running the Shortcut with no input, `OPEN` input, and `CLOSE` input each route to the correct branch using iOS-26-compatible nested If/Otherwise; unrecognised or empty input fails safe without corrupting state or hanging.
  2. First manual run creates a schema-valid, bounded, versioned state.json with initial profile, fork, and config values from the import questions, which capture descent profile (default Limbo), voice permission, and — Sentient only — the on-device intelligence preference.
  3. First manual run also creates exactly one non-empty `PROSOCHĒ — Control Room` Note containing READ THIS FIRST, exact steps for Automation A and Automation B, a plain statement that the Shortcut cannot self-install these automations and is bypassable, the essential-apps safety warning, and the editable `MY PHONE, ON PURPOSE` proforma.
  4. Later manual runs never overwrite existing state or create a duplicate Control Room Note.
  5. Missing or corrupt state.json, and a deleted Control Room Note, each trigger safe self-healing recovery rather than failure, from any invocation mode.

**Plans:** 4/4 plans executed

Plans:

- [x] 02-01-PLAN.md — Walking skeleton: import questions, config, run clock, MANUAL router, state.json bootstrap, Control Room Note created and opened, plus the manual wiring audit
- [x] 02-02-PLAN.md — The complete Control Room Note body and the empty-body trap gate
- [x] 02-03-PLAN.md — Input normalisation and the nested OPEN / CLOSE / fail-safe router ladder
- [x] 02-04-PLAN.md — Self-healing from any mode, corrupt-state recovery, Note-existence guard, idempotence, and phase closure

### Phase 3: Deterministic State Engine

**Goal**: Given any sequence of stubbed OPEN events and contract outcomes, the engine computes Heat, Gravity, Pressure, and the resulting Circle exactly as specified — reproducible and provably different across the three profiles.
**Mode:** mvp
**Depends on**: Phase 2
**Requirements**: STATE-01, STATE-02, STATE-03, STATE-04, STATE-05, STATE-06, STATE-07, STATE-08, STATE-09, STATE-10, STATE-11
**Success Criteria** (what must be TRUE):

  1. The behavioural day recorded for a test run equals (current date − 4h) stored as a date key; a rollover resets `opens_today` and Gravity while leaving Heat, recent sessions, and exit statistics untouched.
  2. Heat visibly decays with elapsed time since the last genuine target-app interaction, increments on a genuine OPEN with extra Heat for rapid reopening, and is adjusted up or down by the previous contract's outcome.
  3. Heat stays within its floor and cap in every test case; Gravity equals `floor(opens_today/6)` capped at 5.
  4. Pressure equals Heat plus Gravity, and maps to a Circle via the active profile's threshold table using ordered comparisons rather than equality.
  5. All three profiles (Paradise, Limbo, Inferno) produce demonstrably different Circles for the same test Pressure value; duplicate OPEN events from a single user action increment the open count only once.

**Plans:** 1/1 plans executed

### Phase 4: CLOSE Pipeline & Session Race Protocol

**Goal**: Session duration is measured accurately and safely even under rapid app switching or overlapping automation triggers, and CLOSE always leaves state consistent.
**Mode:** mvp
**Depends on**: Phase 3
**Requirements**: SESS-01, SESS-02, SESS-03, SESS-04, SESS-05, SESS-06, SESS-07
**Success Criteria** (what must be TRUE):

  1. Each OPEN creates a session with a unique ID and start timestamp recorded in state.
  2. CLOSE measures actual session duration from that recorded start timestamp, compares it against the declared contract, and records the overrun.
  3. A CLOSE that reloads state and finds a newer OPEN owning the active session aborts without mutating state.
  4. Rapid switching between two tracked apps in a test sequence never corrupts state or produces a phantom session.
  5. CLOSE clears the active session, appends the completed session to the rolling window, and restores any environmental setting PROSOCHĒ itself changed during the session.

**Plans:** 2/2 plans executed

Plans:

- [x] 04-01-PLAN.md — CLOSE pipeline generator: semantic anchor replacement, race-safe ownership check, bounded session history
- [x] 04-02-PLAN.md — Fix the WFConditionalActionString wiring defect class (close_pipeline ownership gate + 9 sibling sites) that made CLOSE a permanent no-op (G-04-1, G-04-3)
- [x] 04-03-PLAN.md — Add unconditional OPEN/CLOSE Notification confirmations and improve the Leaving menu's copy (G-04-4b)

### Phase 5: Nine Primitives & Environmental Safety

**Goal**: Every one of the nine intervention primitives fires correctly and safely — including Circle IX's guaranteed, model-free route-out — and no primitive makes an unrestorable environmental change.
**Mode:** mvp
**Depends on**: Phase 1, Phase 4
**Requirements**: CIRC-01, CIRC-02, CIRC-03, CIRC-04, CIRC-05, CIRC-06, CIRC-07, CIRC-08, CIRC-09, CIRC-10, CIRC-11, CIRC-12, CIRC-13, CIRC-14, SAFE-01, SAFE-02, SAFE-03, SAFE-04, SAFE-05, SAFE-06
**Success Criteria** (what must be TRUE):

  1. The Knock shows a brief, non-lecturing interruption carrying real telemetry; Confession asks for a free-text intention and then a time boundary (2/5/10/15/custom).
  2. Ash applies the audited visual-salience reduction or its documented Phase 1 fallback; Silence reduces media audio only when the original value can be captured and restored, otherwise degrades safely; Dimming reduces brightness only when reversible — only when the original has been captured **and durably persisted** — otherwise degrades safely; and across all primitives, every environmental change is captured and persisted before it is applied and is always restored, volume is never increased or startling, any setting whose original value can't be captured is left unchanged, and pre-existing accessibility configuration is never blindly overridden. (Both brightness clauses in this criterion were amended 2026-08-18 under user decision **D-01**; the volume and accessibility clauses are untouched — D-01 is brightness-only. Authority: `docs/CAPABILITY-DECISIONS.md` BD-02's Supersession note.)
  3. Exile routes immediately to an exit without a permission prompt and returning remains possible only as an affirmative act; the Mirror shows a precise behavioural reflection built only from recorded facts; the Voice speaks the Mirror at most once per run, only when voice is enabled, never at unsafe levels.
  4. Ice applies a deterministic cooldown whose duration varies by profile, decided entirely without the model; a target-app OPEN during Ice immediately ejects or redirects with remaining cooldown shown where practical; blocked attempts don't endlessly inflate Heat; Ice always expires, granting Heat relief and clearing the cooldown.
  5. Switching between Classic (default), Black Mirror, and Ambient sequences visibly changes which primitives each Circle invokes, including combined primitives, and a stronger Circle does not necessarily replay every weaker Circle's prompt; Emergency Restore clears cooldown, the active session, and recoverable brightness/volume/colour state, and is reachable even while in Ice.

**Plans**: 3/3 plans executed

- [x] 05-01-PLAN.md
- [x] 05-02-PLAN.md
- [x] 05-03-PLAN.md

### Phase 6: Exits, Exit Learning & Contracts

**Goal**: Every exit is reachable and honestly recorded, the system learns over time which exits actually get the user away from the phone, and every contract the user makes is honoured, recorded, and feeds back into Heat.
**Mode:** mvp
**Depends on**: Phase 4, Phase 5
**Requirements**: EXIT-01, EXIT-02, EXIT-03, EXIT-04, EXIT-05, EXIT-06, EXIT-07, EXIT-08, EXIT-09, LEARN-01, LEARN-02, LEARN-03, LEARN-04, LEARN-05, CONT-01, CONT-02, CONT-03, CONT-04, CONT-05, CONT-06
**Success Criteria** (what must be TRUE):

  1. All six exits route correctly: Capture to an idea-externalising target, Coordinate to a planning target, Create to a user-defined making target, Connect to a direct human-contact tool without initiating contact on the user's behalf, Consult to a menu covering web/maps/notes/reminders/calendar with a direct query-shaped search route, and Close to home or lock, treated as a first-class outcome.
  2. Leaving is always available at every Circle without being forced to complete an intervention; exits the user has disabled are never selected; each exit use is recorded with its type, timestamp, triggering app, Circle, and Heat.
  3. Time until the next tracked-app OPEN after an exit is measured and recorded as that exit's outcome; with few observations exits rotate roughly evenly across enabled exits; with sufficient observations, exits associated with longer time away are preferred with occasional exploration at a configuration-driven (not hardcoded) rate — all computed deterministically, never delegated to the model.
  4. A free-text intention of any wording, including deliberate leisure such as "watch stupid videos," is accepted, paired with a time boundary selectable from presets or entered as a custom value.
  5. A kept contract is recorded as respected, an exceeded contract is recorded with its overrun magnitude, that recorded outcome is available to the next OPEN's Heat calculation, and a time-overrun message is never shown when no contract existed.

**Plans**: 3/3 plans executed

- [x] 06-01-PLAN.md
- [x] 06-02-PLAN.md
- [x] 06-03-PLAN.md

### Phase 7: Control Room Manual Menu, Dumb Mirror Engine & Dumb Freeze

**Goal**: The Dumb fork becomes a complete, self-contained product — the Control Room manual menu exposes full control, the Mirror gives varied honest telemetry with no model involved, and the Dumb fork alone validates, signs, and imports cleanly on a real iPhone before any Sentient work begins.
**Mode:** mvp
**Depends on**: Phase 5, Phase 6
**Requirements**: ROOM-07, ROOM-08, ROOM-09, ROOM-10, ROOM-11, ROOM-12, DUMB-01, DUMB-02, DUMB-03, DUMB-04, DUMB-05, DUMB-06
**Success Criteria** (what must be TRUE):

  1. The Control Room Note shows current settings (fork, profile, sequence, voice, AI, enabled exits) and a human-readable state snapshot that refreshes on manual run, plus an Attention Ledger recording only meaningful events — Circle changes, contracts, redirects, rapid-return clusters, cool-downs, profile changes — not every internal calculation.
  2. The manual menu offers Status, Open Control Room, Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today, and Emergency Restore; Sync My Profile is the only path that extracts the proforma from the Note, and the OPEN path never parses it; Test a Circle runs any chosen Circle's behaviour without altering real Pressure.
  3. The Dumb fork has no Apple Intelligence dependency and runs fully on non-Apple-Intelligence iOS 26 iPhones.
  4. At least 30 Mirror templates exist, none inventing a fact, with template selection gated on which facts are actually available so no malformed or empty telemetry message is produced; Consult without a model offers Search Web, Search Maps, Open Notes, Open Reminders, Open Calendar, and Back; the intent gate accepts a blank or vague response without attempting to judge sincerity.
  5. Mirror output acknowledges success as well as lapses, so opening a target app does not always produce criticism; the Dumb fork alone passes the Shortcuts Playground validator, signs, and completes a first manual run on a real iPhone before any Sentient XML is authored.

**Plans**: TBD

### Phase 8: Sentient Fork & Dual Distribution

**Goal**: The Sentient fork adds Apple On-Device Intelligence as an additive contract-auditor wrap on top of the untouched deterministic engine, and both forks ship as signed, importable, documented `.shortcut` files.
**Mode:** mvp
**Depends on**: Phase 7
**Requirements**: SENT-01, SENT-02, SENT-03, SENT-04, SENT-05, SENT-06, SENT-07, SENT-08, SENT-09, SENT-10, SENT-11, SENT-12, SENT-13, SENT-14, SENT-15, DIST-01, DIST-02, DIST-03, DIST-04, DIST-05, DIST-06, DIST-07, DIST-08
**Success Criteria** (what must be TRUE):

  1. The On-Device model is invoked only across Circles II–VIII with increasing involvement, while Circle I stays fast and deterministic and Circle IX invokes no model and remains fully deterministic; model output is structured as ALLOW/CHALLENGE/DENY, parsed and validated, with malformed, empty, or slow output falling back to deterministic Dumb behaviour without breaking the run, and at most one challenge round ever occurs.
  2. DENY is available only at sufficiently high Circles and means redirect, never system-level punishment; the model audits contracts on specificity, boundedness, and consistency, never asserts the user is lying, and never claims to know what happened inside an app or what the user felt; a clearly bounded deliberate-leisure contract can receive ALLOW; prior contract consistency can inform a challenge using only recorded behavioural facts.
  3. The model never controls Heat, Gravity, Pressure, thresholds, timers, exit selection, or Ice; it receives only a compact local context window, never the whole Note, and no behavioural data leaves the device; the system instruction enforces the required tone and forbids banned vocabulary and diagnosis language; the Sentient fork adds no changes to the deterministic state engine inherited from Dumb.
  4. Both forks pass the Shortcuts Playground validator at the iOS 26 target, sign successfully into importable `.shortcut` files, and complete a first manual run on a real iPhone; the two forks are named unambiguously and distinguishable at import.
  5. Unsigned XML source is retained in the repository for both forks; build notes document unsupported actions, deviations, fallbacks taken, and known iOS limitations; repository documentation states plainly that data stays on-device, there is no external analytics, model output can be wrong, and the system is self-directed and bypassable; core functionality has no external network dependency.

**Plans**: 3/3 plans executed

- [x] 08-01-PLAN.md
- [x] 08-02-PLAN.md
- [x] 08-03-PLAN.md

## Progress

**Execution Order:**
Delivered: 1 → … → 16 (see the checklist above). Conversion: 17 → 18 → {19, 20} → 22, with 21
runnable beside 17–20 whenever a device session exists; then 23 and 24 after 22; 25 after 24;
26 → 27 → 28 (26 can start any time after 17).

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Capability Audit & Config Foundation | 5/5 | Complete | 2026-08-13 |
| 2. Routing, Bootstrap & Control Room Onboarding | 4/4 | Complete | 2026-08-13 |
| 3. Deterministic State Engine | 1/1 | Complete | 2026-08-13 |
| 4. CLOSE Pipeline & Session Race Protocol | 3/3 | Complete (device UAT partial) | 2026-08-14 |
| 5. Nine Primitives & Environmental Safety | 3/3 | Complete | 2026-08-13 |
| 6. Exits, Exit Learning & Contracts | 3/3 | Complete | 2026-08-13 |
| 7. Control Room Manual Menu, Dumb Mirror Engine & Dumb Freeze | 1/1 light | Complete (human verify open) | 2026-08-14 |
| 8. Sentient Fork & Dual Distribution | 3/3 | Complete (DIST-03 open) | 2026-08-14 |
| 9. Dimming/Silence Stateful Restore | 2/2 | Complete | 2026-08-16 |
| 10. Ship-readiness remainder and UX-lite pass | 5/5 | Complete | 2026-08-17 |
| 11. Build Addendum 01 | 10/10 | Complete | 2026-08-18 |
| 12. State-shape sentinel gaps | 5/5 | Complete | 2026-08-18 |
| 13. Red operators & WFItems wrapper | 4/4 | Complete | 2026-08-18 |
| 14. Ash as real Color Filters grayscale | 3/3 | Complete | 2026-08-19 |
| 15. Circle 8 — the Voice primitive | 5/5 | Complete | 2026-08-19 |
| 16. Dimming/Silence persistence & D-01/D-02 | 6/6 | Complete | 2026-08-18 |
| 17–28 (covenant conversion and beyond) | 0 | Not started | - |

## Backlog

Unsequenced items that are genuinely new work rather than verification of an already-built
phase. (The six device-UAT items formerly listed here were reclassified 2026-08-16 — they
verify claims Phases 4/5/6/7 already make, so they now live as `{N}-UAT.md` files in those
phase directories, tracked via `/gsd-verify-work {phase}` and rolled up by
`/gsd-audit-uat`, not as roadmap phases.) Promote with `/gsd-review-backlog` when ready to
sequence.

### Phase 999.3: Grayscale / Ash capability donor test — **RETIRED 2026-08-19** (was BACKLOG)

**RETIRED, not promoted and not abandoned — every step of it is discharged.** Closed by
decision **D-14-03** when Phase 14 landed. Step accounting, from this item's own outcome block:

| Step | State | Discharged by |
|---|---|---|
| 1. Decrypt the donor already on disk | ✅ complete | Spike 005 decrypted **three** donors, not one — On, Off and Toggle |
| 2. Settle the §21 / BD-01 read-back question | ✅ complete | **No `Get*`/`Query*` intent exists for any accessibility setting** across all 35 intents in the framework. That is the finding, and it is why the remedy is disclosure plus a kill switch rather than detection |
| 3. Close CAP-20 as absent-on-iOS | **n/a** | The action *does* exist on iOS — the branch this step was conditioned on never opened |
| 4. Update the audit trail | ✅ complete | `docs/CAPABILITY-DECISIONS.md` **BD-01-R2**, which supersedes BD-01-R's build recipe and now carries a phase-14 IMPLEMENTED note |
| 5. Decide whether to rebuild Ash | ✅ complete | **This is Phase 14.** Decided yes, and built: 15 `AXToggleColorFiltersIntent` sites per fork, both forks re-signed 2026-08-19 |
| 6. Never guess the identifier or enum cases | ✅ complete | Nothing was guessed; every literal in the shipped emitter traces to a donor, and a build guard fails the build on any unverified parameter key |

**Closing evidence:** Phase 14 above, and its three summaries — `14-01-SUMMARY.md`,
`14-02-SUMMARY.md`, `14-03-SUMMARY.md`.

**Severity:** minor
**Requirements:** AUDIT-02 (via Phase 14)
**Plans:** 0 plans — retired without being promoted

Plans:

- [x] Retired 2026-08-19 per D-14-03; step 5 is Phase 14

Full context (retained): `.planning/phases/999.3-grayscale-ash-capability-donor-test/2026-08-16-grayscale-ash-capability-donor-test.md`

### Phase 9: Dimming/Silence Stateful Restore (Experimental Fork)

**Goal:** On this experimental branch only, finish the stateful capture-and-restore design
for Dimming (§11 Primitive E) and Silence (§11 Primitive C) — fix the 28 uncoerced
`setbrightness`/`setvolume` sites left over from the cycle-14 type audit and the later
Test-a-Circle menu unroll (corrected 2026-08-16 from the stale 18 figure — see criterion 1
and `09-RESEARCH.md`), then prove
capture → apply → restore as a closed loop on a real device, including force-quit,
device-restart, CLOSE-never-fires, and overlapping-session failure modes. Deliver a
verdict (works safely / does not) that the main-line cut in
`.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md` can be judged against —
this phase does not reverse that cut, which proceeds independently on main.
**Requirements**: RESTORE-01, RESTORE-02, RESTORE-03, RESTORE-04, RESTORE-05, RESTORE-06, RESTORE-07 (proposed during `/gsd-plan-phase 9`, one per success criterion below; not part of the v1 REQUIREMENTS.md traceability set — this is an experimental fork phase)
**Depends on:** Phase 7 (branches from the device-confirmed Dumb build/freeze lineage)
**Success Criteria** (what must be TRUE):

  1. All 28 deferred `setbrightness.WFBrightness` (14) / `setvolume.WFVolume` (14) sites
     — corrected 2026-08-16 from the stale "18" figure in `docs/BUILD-NOTES.md` §8; the
     Test-a-Circle 9-way menu unroll added 10 more call sites after that table was written,
     see `09-RESEARCH.md` "Site count correction" — carry the correct coercion
     aggrandizement, with `CoercionItemClass` established from donor or corpus evidence
     (Donor 10 confirms the action/parameter identifiers but not a variable-fed coercion
     shape at this exact parameter position — an on-device visual check or fresh donor is
     required, not assumed by analogy) — never guessed — and the numeric-audit build guard
     (`verify_numeric_operands()`) no longer exempts them.

  2. On device: reading current brightness/volume via `Get Device Details` returns a real,
     non-empty, correctly-typed value; the has-any-value guard correctly skips the change
     when the read returns nothing.

  3. On device: the original value is restored exactly on CLOSE.
  4. Force-quit mid-session, device restart mid-session, CLOSE never firing, and two
     overlapping sessions each either restore correctly or leave the user at a device-safe
     state — never silent-forever, never loud, and never *stuck* at a changed brightness/
     volume with no path back to the original value (§21, §32). Brightness may target the
     device's true minimum, not an artificial floor — corrected 2026-08-16 per
     user on-device report that the practical minimum is dim, not a literal black/unusable
     screen (see `docs/CAPABILITY-DECISIONS.md` BD-02 addendum); the safety mechanism is
     capture-and-restore reliability (criteria 2–3, 5), not floor avoidance.
     **Amended 2026-08-18 (phase 16 plan 05).** This criterion was already substantively
     right; what it lacked was the main-line settlement. The 2026-08-16 correction it cites
     was *provisional* and scoped to the experimental fork when written. User decision
     **D-01** (LOCKED 2026-08-17) settles it on the **main line** — `safety.brightness_floor`
     and `safety.dim_target` are both `0`, shipped by plan 16-03. The criterion's meaning and
     its 2026-08-16 date are unchanged; only its status is. Authority: BD-02's Supersession
     note. The retired band wording was removed rather than restated, because a live file
     that quotes the clause it retires still carries the clause.

  5. Emergency Restore recovers from every failure mode found above.
  6. DEV-06 (restore-ownership check) is re-evaluated live on this fork now that the cut
     it was conditioned on does not apply here.

  7. A written verdict exists: either stateful environmental friction is demonstrated safe
     with device evidence, or it is retired with the evidence that justifies the main-line
     cut.

**Plans:** 2/2 plans executed

Plans:
**Wave 1**

- [x] 09-01-PLAN.md — Generator fix: two `NUMERIC_OPERAND_FIELDS` table entries, negative-control self-check, stale "18" doc correction (device-free, Wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 09-02-PLAN.md — Device-proving safety verdict: sign both forks, author and complete `09-UAT.md`, DEV-06 design write-up, written verdict (Wave 2, depends on 09-01)

Full context: `.planning/todos/pending/2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md`

### Phase 10: Ship-readiness remainder and UX-lite pass

**Goal:** Make Dumb quiet, predictable, and actually testable — no stray dialogs, no
unexplained prompts — while closing out the leftover ship-readiness chores. Two strands,
one phase.

**Strand A — ship-readiness remainder.** Items 2, 3 and 4 of
`.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md` (item 1, the
`BUILD_STAMP`/`ROUTER_TRACE`/`OPEN_BISECT` breadcrumb strip, is already DONE; item 5 is
superseded — see below): add a `.gitignore` for `.DS_Store`/`__pycache__`/`*.pyc`;
refresh `artifacts/shortcuts/MANIFEST.md` with the 2026-08-14/15 archive entries;
device-confirm the cycle-16 Control Room note-picker fix by tapping "Open Control Room".
Also repair the **three of six structural self-checks that already FAIL at `HEAD`**
(`10-RESEARCH.md` Finding 5c).

**Dimming and Silence are NOT cut — the brightness/volume MVP cut is cancelled.** User
decision 2026-08-16, reaffirmed 2026-08-17: both stay, each as its own distinct Circle,
**with working brightness and volume capture-and-restore**. Phase 9 merged the
numeric-coercion fix for all 28 `setbrightness`/`setvolume` sites to main (`2e2261e`).
This phase must keep `dimming()`, `silence()`, `restore_managed_settings()`, the
`settings_snapshot` subtree, and all 28 coerced sites; `verify_numeric_operands()` must
keep *not* exempting them. Two consequences: the **SAFE-05 conflict resolves** rather
than being deferred to milestone close, and **DEV-06** (restore-ownership,
`changed_at`/`changed_by_session_id`) is **live again** rather than moot, bringing the
`Session ID` scope defect back with it. `10-RESEARCH.md` Finding 2 and Pitfalls 2 and 3
document the cancelled cut and are **superseded — ignore them**; the rest of that
document stands.

**Strand B — UX lite, go quiet by default.** The product currently shows three surfaces
on every genuine OPEN — a `Circle X · pressure Y · heat Z` notification, the
`Leaving / Continue` menu, and the Circle-1 Knock alert — starting from the very first
open of the day. A user buried in pop-ups deletes the Shortcut, which is canonical
strategy §12's stated key failure. Deliverables:

- **Circle 0 silent band.** State still accumulates and saves exactly as now, but
  nothing is shown at all — no notification, no menu, no primitive. `Circle Next`
  currently floors at 1 and the threshold scan only raises it, so Circle 0 is
  unreachable; entry thresholds must rise (all three profiles start at `1` and
  `heat.open_base` is `1`, so any first open scores Circle 1). Shift each profile's
  curve up so band widths stay as designed and only entry is delayed. The numbers are
  explicitly for on-device tuning.

- **Remove the OPEN notification entirely.** Users learn their Circle because something
  happens, not because they are told a number.

- **Reword `Leaving / Continue`** so it says what is being left, what continuing means,
  and why it is being asked. It stays as §6.4's easy-dismissal mechanism wherever it
  fires; it simply no longer fires in the silent band.

- **Gate the ungated `shownote`** behind an explicit request flag, so only "Open Control
  Room" opens the Note instead of all nine menu items ending in the Notes app. The
  cycle-16 `filter.notes` picker fix is already applied in source — do not re-patch it.

- **Add a `Setup Check` menu item** reporting which of the two Personal Automations has
  ever fired, via a numeric `> 0` gate on the existing flat `last_open_at`/`last_close_at`
  keys. No new state, no schema bump, no migration.

- **Amend the canonical strategy** to record the silent band, since §Primitive A and
  §Circle I both currently prescribe the Knock as Circle 1's intervention.

**Deferred to the heavy UX round, not this phase:** funnel instrumentation in
`state.json`; the full nine-Circle interaction-cost and latency pass; rolling telemetry
into the Confession/Mirror headers; the §29 voice copy rewrite; the proforma deferral and
READ THIS FIRST shortening; the read-once-vs-return-to Note restructure coordinated with
the Build Addendum 01 rename; full fresh-import funnel re-verification.

**Known open defect deliberately NOT fixed here:** Circle 8 dispatches nothing — the
`"Voice"` sequence entry matches no branch under condition-99 "contains" matching. A
later phase fixes it. If this phase adds a sequence/dispatch checker, that checker must
**record** the orphan rather than fail on it, and must **not** hard-code condition 99 or
substring matching as an invariant: BD-06 moves dispatch to condition 4 exact matching
and abolishes combined entries.

**Severity:** major
**Requirements**: AUDIT-03, AUDIT-04, SESS-07, CIRC-01, CIRC-03, CIRC-05, CIRC-13, CIRC-14, ROOM-01, ROOM-02, ROOM-03, ROOM-10, SAFE-01, SAFE-02, SAFE-03, SAFE-05, DIST-01, DIST-02, DIST-03, DIST-04, DIST-05, DIST-06 (no new IDs expected — this phase touches existing ones)
**Depends on:** Phase 9
**Plans:** 5/5 plans executed

Plans:
**Wave 1**

- [x] 10-01-PLAN.md — Circle 0 silent band: raised thresholds, Circle floor of 0, silent-band gate, OPEN notification removed, `verify_circle_zero_silence()`, canonical-strategy amendment

**Wave 2** *(depends on 10-01)*

- [x] 10-02-PLAN.md — Control Room quieting: `gate_control_room_shownote()`, the `Setup Check` menu item and its read-only display, the reframed manual prompt, ROOM-10 amended

**Wave 3** *(depends on 10-01, 10-02)*

- [x] 10-03-PLAN.md — Guards: `environmental_restore_check.py` pins the cancelled brightness/volume cut, `router_ui_census.py` enforces Circle-0 silence, `sequence_dispatch_check.py` records the Voice orphan, `phase6_self_check.py` repaired

**Wave 4** *(depends on 10-01, 10-02, 10-03)*

- [x] 10-04-PLAN.md — Rebuild, validate, sign, AEA1 decrypt-verify both forks; `manifest_check.py`; MANIFEST refresh; BUILD-NOTES record and requirement resolutions

**Wave 5** *(depends on 10-04; blocked on DIST-03)*

- [x] 10-05-PLAN.md — Deferred device UAT: author `10-UAT.md` (ten tests) and gate on a human running it or recording the blocker

**Planning notes (2026-08-17):**

- `src/PROSOCHE-Dumb.xml` is both input and output of `tools/build_state_engine.py`, so every plan that runs a builder mutates it. That makes it a phase-wide mutex and is why the five plans are strictly sequential rather than parallelised.
- Two positions in this phase's brief were measured false at `HEAD` and are corrected in 10-04: the self-check baseline is one-of-seven red (only `phase6_self_check.py`), not three-of-six; and `sentient_core_check.py` passes at `HEAD` because `c6d8737` regenerated both forks, so it is kept green by rebuilding Sentient rather than left red.
- Strand A items 2 and 3 needed no work at planning time: `.gitignore` already covers `.DS_Store`, `__pycache__/` and `*.pyc`, and all six MANIFEST rows matched their artifacts exactly. The MANIFEST is refreshed in 10-04 only because this phase rebuilds.

### Phase 11: Build Addendum 01 — Dante Circle names and the ten-primitive roster

**Goal:** Apply `PROSOCHE_Build_Addendum_01.md` in full, once, against the roster settled in
**BD-06** (`docs/CAPABILITY-DECISIONS.md`) — so the rename lands a single time rather than
being re-cut after each of the four in-flight Circle phases.

**BD-06 is already decided and is binding. Do not re-litigate it.** Its five load-bearing
decisions: Dante names are **positional** (Circle 1 = Limbo … Circle 9 = Treachery),
because three sequences order the interventions differently at the same Circle numbers, so
a name can only attach to the number; canonical Dante order is kept; the roster grows to
**ten primitives for nine slots** and each sequence picks nine; combined sequence entries
are abolished so dispatch moves from condition 99 ("contains") to **condition 4 (exact)**;
and the routed Exile lands the user directly rather than offering a menu.

**Deliverables.** Rename the interventions per Addendum §5 (Knock→Pause, Ash→Black and
White, Confession→Intention, Dimming→Dim, Voice→Loud Mirror, Ice→Frozen; Silence and Mirror
unchanged; Exile splits into **Eject** straight and **Redirect** routed). Apply BD-06
Decision 4's slot table to all three sequences. Rename the Apple Note from
`PROSOCHĒ — Control Room` to `PROSOCHĒ` — three string occurrences in the XML — while
keeping "Control Room" as the internal name (settled in `e84ee77`). Rename the variants
Dumb→**Core** and Sentient→**Aware**. Make Panic Escape deliberately removable per
Addendum §3: the removal path requires manually editing the setting in the Note plus
explicit confirmation. **Panic Escape is the `Leaving` option** in `universal_leaving()` —
the easy behavioural bypass offered before every primitive — **not** Emergency Restore,
which is a safety mechanism and must stay unconditionally available. Add the optional
hardening note at the end of the Note explaining a user may add Shortcuts.app itself to
their target list.

**Write the dispatch-coverage build guard as part of this phase, not after it** — every
distinct primitive name in any `sequences` array must have exactly one dispatch branch, and
every branch must be named by at least one sequence. A mass rename across three sequence
arrays and ten dispatch branches is precisely the operation that guard exists to catch, and
this defect class is invisible to the validator, the ToolKit catalog and the signed-artifact
decrypt.

**Intermediate state to respect.** `Redirect` has no implementation until Phase 17, so all
three sequences hold `Eject` at Circle 6 until then; Phase 17 flips Classic's and Ambient's
cells. Circle 8 gets a real branch here (interim: the Mirror) so the guard can be a hard
gate immediately; Phase 15 replaces it with the designed Voice.

**Severity:** major
**Requirements**: AUDIT-02, CIRC-02, CIRC-06, CIRC-08, ROOM-01, ROOM-02, DIST-01, DIST-02
**Depends on:** Phase 10
**Plans:** 10/10 plans executed

**Gap closure (waves 7–10).** `11-VERIFICATION.md` scored 13/18 with three failed truths and two
partials. Plans `11-07` … `11-10` close all five and are strictly sequential, because every one of
them rebuilds and re-signs both forks. Two scope judgments were made explicitly rather than left to
drift: GAP 1 (`dimming()` / `silence()` bodies unreachable) is **closed here**, with the device
proof of the capture-and-restore loop deferred to **Phase 16 / DIST-03 / `16-UAT.md`'s twelve
tests** (`09-UAT.md` is superseded by `16-UAT.md` — see `.claude/CLAUDE.md`'s Blockers entry) —
the reasoning is in `11-08-PLAN.md`'s `<scope_judgment>`; and GAP 3 (the Aware fork's Use Model
audit on one rendering of two) is resolved by **auditing every OPEN-arm rendering**, with the
"deliberate product decision" alternative rejected and the rejection recorded in
`11-09-PLAN.md`'s `<gap3_resolution>`.

Plans:
**Wave 1**

- [x] 11-01-PLAN.md — Tracer: one primitive end to end, generator through plist to signed artifact; `tools/plist_text_edit.py` and `docs/note_identity_check.py` (wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 11-02-PLAN.md — Dispatch-coverage build guard, then BD-06's roster and exact-match dispatch in one commit (wave 2)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 11-03-PLAN.md — Note renamed to `PROSOCHĒ`, Dante's nine names surfaced positionally, optional hardening section (wave 3)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 11-04-PLAN.md — Blocking decision: `schema_version` disposition and old-signed-artifact disposition (wave 4, not autonomous)

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 11-05-PLAN.md — Panic Escape made deliberately removable and restorable; Emergency Restore provably untouched (wave 5)

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 11-06-PLAN.md — Dumb→Core / Sentient→Aware rename, Aware-side note divergence, ship and decrypt-verify (wave 6)

**Wave 7** *(gap closure — blocked on Wave 6, and on Phase 12 being quiescent: no `12-*-PLAN.md` without a matching `-SUMMARY.md`, and no `.claude/worktrees/agent-*` present. A clean `git status` is not sufficient — Phase 12 executes in worktrees and merges, so the main tree is clean between waves. Run `11-07` … `11-10` as a contiguous block, entirely before `12-04` or entirely after `12-05`.)*

- [x] 11-07-PLAN.md — GAP 2 tracer: the text-match output-name class fix, both sites plus the recurrence guard; consumption shape settled at rung 2 (wave 7)

**Wave 8** *(blocked on Wave 7 completion)*

- [x] 11-08-PLAN.md — GAP 1: Dim and Silence re-gated on the captured-original leaf so their bodies are reachable; a reachability build guard armed in both builders; the false capability claim corrected in the MANIFEST, the ROADMAP and the deviation log (wave 8, **not autonomous** — one blocking checkpoint between the guard's proof and the gate fix)

**Wave 9** *(blocked on Wave 8 completion)*

- [x] 11-09-PLAN.md — GAP 3: the Aware fork's Use Model audit on every OPEN-arm rendering, with per-rendering identifiers and two checkers that derive rather than pin (wave 9)

**Wave 10** *(blocked on Wave 9 completion)*

- [x] 11-10-PLAN.md — GAP 4 + GAP 5: the Panic Escape gate guard resolved by provenance; two decorative floors moved to measured values; both interim stand-ins recorded where the prohibition requires (wave 10)

### Phase 12: State-shape sentinel gaps — exit_events and active_session

**Goal:** Close the two remaining STATE-SHAPE + GATE-SEMANTICS gaps — `exit_events` and
`active_session` — using the container/leaf pattern already verified twice on
`settings_snapshot` and `pending_exit`.

**Why this is a live crash risk, not housekeeping.** Per the verified runtime semantics in
`.claude/CLAUDE.md`, a **dotted read raises a hard error if any segment is absent**.
`exit_events` is entirely missing from the bootstrap `state.json` template, and it sits on
`record_exit_and_route()` — so the first real exit against clean state will very likely
hard-error. `active_session` is the sole remaining entry in
`KNOWN_SENTINEL_EXISTENCE_GATES`; it was confirmed inert only for one specific device run,
which is a statement about what that run exercised, not a property of the defect. Both keys
live on the same code path, so a genuine session-plus-exit sequence will reach both in one
run.

**Deliverables.** Seed a permanent container for each in the bootstrap template mirroring
`seed_pending_exit()`. Add a `verify_*_seed()` build guard per key following
`verify_pending_exit_seed()`. Audit **every** read/write/clear site for both keys by
full-codebase sweep — `record_exit_and_route()`, `universal_leaving()`, and anything else
grep finds — and ensure clearing gates test **leaf value** (condition 5 against
`CLEARED_SENTINEL`) rather than **container existence** (condition 100). Remove both keys
from `KNOWN_SENTINEL_EXISTENCE_GATES` so the registry honestly reads zero remaining gaps.

**Fix whole classes, never site-by-site** — every defect in this project's debug history was
systematic (147, 367, 25, 20 and 8 sites). A read-then-`has any value` gate on a dotted path
is **unimplementable**: the read raises unless the key exists, and if it exists the gate is
true. Gate on a numeric `> 0` test or restructure to a flat read.

**Hard prerequisite for Phase 17**, whose Exile work sits directly on
`record_exit_and_route()`. Device-test the exit-recording path specifically — a real "leave
and confirm exit", not an OPEN. That path was never exercised by the closed OPEN-path debug
session, so treat it as new-risk surface.

**Severity:** major
**Requirements**: SESS-07, STATE-12, EXIT-01, EXIT-02, SAFE-01
**Depends on:** Phase 11
**Plans:** 5/5 plans executed

Plans:
**Wave 1**

- [x] 12-01-PLAN.md — Tracer: seed `exit_events` + `exit_selection_counter`, guard them, bump schema 3→4, arm on both forks

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 12-02-PLAN.md — Seed `active_session` as a permanent four-leaf container and guard it

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 12-03-PLAN.md — Convert every `active_session` gate/write/clear to leaf semantics; empty `KNOWN_SENTINEL_EXISTENCE_GATES`

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 12-04-PLAN.md — Decide and close `profile_snapshot.create_target_url`; generalise `verify_state_seed()` to every state read

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 12-05-PLAN.md — Sign both forks, refresh MANIFEST, gate B advisory read, `12-UAT.md` device exit-path test

### Phase 13: Red-operator conditionals and the WFItems List wrapper

> **Corrected 2026-08-17, on donor evidence — this section previously stated two counts that
> measurement REFUTED.** `.planning/debug/Donor 5.shortcut`, `Donor 4.shortcut` and
> `Donor 4.1.shortcut` were decrypted during this phase's research (Donor 5 for the first time
> ever), and every count was re-measured with `plistlib` against the artifacts at HEAD. The
> conditional family is **not** a defect and its site count is **zero**, not fourteen; the
> `WFItems` family is real and **33× larger** in actions and 330× larger in rows than recorded.
> The named "concrete starting site" was a **false lead** — it passes a raw literal and is not a
> member of the family — and the screenshot both this section and the originating todo cited
> **does not exist** in the worktree, the main checkout or git history. The full record, with
> the original claims preserved beside their measured replacements, is `docs/BUILD-NOTES.md`
> §28; the settled shapes are `docs/CAPABILITY-DECISIONS.md` `BD-07` and `BD-08`.

**Goal:** Settle two defect families carried unchanged through every cycle of the closed
`open-routing-sequence-error` session because both sit past breadcrumb J — and fix the one that
turned out to be real. Both are **device-visible defects that no file-level analysis can
detect**, which is exactly why both had to be settled by decrypted device donors rather than by
the validator or the ToolKit catalog.

**1. The `WFConditionalActionString` operand family ("Donor 5") — measured as ALREADY CORRECT,
zero defective sites.** Donor 5 shows iOS *itself* authoring the construct this phase suspected:
a variable in a conditional's TEXT-slot operand as a `WFTextTokenString` (a single `￼` string
plus an `attachmentsByRange` keyed `{0, 1}` holding a bare `{Type, VariableName}` dict),
alongside a `WFInput` carrying the *opposite* `WFTextTokenAttachment` envelope, with no coercion
aggrandizement on either side. `token()` emits a key-for-key identical shape. Measured per fork:
192 (Core) / 195 (Aware) mode-0 conditionals carry the slot, of which **20 / 20** are
variable-bearing (19 at condition 4, 1 at 99) and **all** match Donor 5, with 172 / 175 raw
literals and **zero** offenders. Sweeping would have replaced a device-confirmed shape with a
guess.

**2. The `WFItems` List wrapper — real, and 33× larger than recorded.** iOS wraps a
variable-bearing List row as `{"WFItemType": 0, "WFValue": <WFTextTokenString>}` while leaving
literal rows as bare strings; this artifact omitted the wrapper, so rows render blank on device
and the Mirror can select an empty template. Measured per fork: **66 defective List actions
carrying 660 unwrapped rows**, all originating from a single emitter, `mirror_text()`, unrolled
across the Circle dispatch — plus 6 correct bare-string rows that a blanket sweep would have
corrupted. The shape was recovered from `Donor 4.shortcut` and `Donor 4.1.shortcut` and applied
here for the first time.

**Deliverables.** For family 1: **pin, do not fix** — a positive build-time assertion inside
`verify_conditional_action_string()` that a variable-bearing comparison target *is* the
Donor-5 envelope, so a future pass cannot "repair" 20 correct sites, with the refutation carried
in the guard's own docstring. For family 2: one emitter fix (`_list_row()`, branching per row on
`isinstance(item, str)`) covering all 66 actions and 660 rows per fork, plus
`verify_list_item_wrappers()` as the recurrence guard, armed on both forks at both touch points.
Both guards sensitivity-demonstrated against a synthetically reverted artifact. Then the
documentation pass in one go: `.claude/CLAUDE.md`'s numbered axis list extended from seven to
nine (the `WFItems` row wrapper as a new **container** axis, and the
`read_value()`/`get_value()` distinction), axis 7 extended with the `pending_exit` container/leaf
pattern, `BD-07`/`BD-08` recorded, the Phase 13 `docs/BUILD-NOTES.md` section written, and the
refuted counts closed as a class across every project record. Finally: rebuild, gate A, sign
both forks, refresh MANIFEST, author the UAT.

**Why this gates the device UAT.** Blank text and red operators are exactly the two failure
modes Phase 19 is watching for. Fixing them first means a blank Circle in testing is a real
finding rather than a known artifact.

**Severity:** major
**Requirements**: CIRC-04, CIRC-07, ROOM-03, DIST-01, DIST-02
**Depends on:** Phase 12
**Plans:** 4/4 plans executed

Plans:
**Wave 1**

- [x] 13-01-PLAN.md — Tracer: wrap all 660 variable-bearing `WFItems` rows via `_list_row()`, add `verify_list_item_wrappers()`, arm it on both forks, rebuild to gate A, and demonstrate the guard is sensitive

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 13-02-PLAN.md — Pin the Donor-5-confirmed conditional operand shape inside `verify_conditional_action_string()`, sweep nothing, and demonstrate both raises with the ordering mask recorded

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 13-03-PLAN.md — The single-pass doc update: axis list to nine, `BD-07`/`BD-08`, the Phase 13 BUILD-NOTES record, the corrected ROADMAP prose, and the todo closed with a tombstone

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 13-04-PLAN.md — Ship: rebuild, gate A, gate B advisory read, sign both forks under their live display names, decrypt-verify, refresh every MANIFEST row, and author `13-UAT.md`

### Phase 14: Ash as real Color Filters grayscale

**Goal:** Build Ash as a **real Color Filters grayscale toggle**. It currently ships as an alert box
— on device, Circle 2 is indistinguishable from Circle 1: two alerts with different words.

**This is plausibly the highest-evidence primitive in the product.** Canonical strategy §6.5
cites a preregistered randomised field experiment (112 participants) finding grayscale
produced an immediate, significant, objectively-measured reduction in screen time — larger
and faster than goal-setting. It is the only primitive still not implemented as designed.

**The blocker that justified the cut is gone.** Spike 005
(`.planning/spikes/005-ios-color-filters-identifier/`, VALIDATED, merged `4d80176`) settled
it from decrypted device donors — tier-1 evidence. Identifier:
`com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` — an `AX*`
intent, **not** the `UA*` macOS twin. `state` is a **bool-as-integer**: `1` = On, `0` = Off.
`operation` is elided when Turn, so omit it. No `ShowWhenRun`. Both legs are donor-confirmed.
Two corrections the spike paid for and this phase must not re-pay: Apple's own
`.intentdefinition` declares `state` as Integer with `off` = case index **2**, and both are
wrong as plist encodings — **shipping `state = 2` for Off would leave users stuck in
grayscale**. An `.intentdefinition` describes the intent's type system, not the plist
encoding, and never outranks a donor.

**Expect the validator not to know the identifier** — it is absent from all three bundled
ToolKit snapshots. Record the deviation rather than letting a validator complaint trigger a
substitution back to `UA*`, which would ship a macOS action to an iPhone.

**The restore leg is the deliverable, not the apply leg.** A grayscale that does not restore
is strictly worse than no grayscale. **Wire `state = 0` unconditionally, once, at the top of
`restore_managed_settings()`** — one insertion reaching all four recovery paths for free: the
CLOSE pipeline, Emergency Restore, Ice expiry and the live-Ice redirect. It is emitted
**first** so no dotted read below it can hard-error and abort the run before colour comes
back, which is the exact failure whose symptom is a user stuck in grayscale. There is **no
snapshot, no capture, no marker of who changed it and no persist-before-apply ordering**: a
two-valued setting has no original to remember, so "restore" is unconditionally "set it off",
and the phase-16 capture machine keeps exactly the two groups it already had. *(The paragraph
that stood here instructed the opposite, routing colour through that machine as a third member.
It is **superseded by the scope reset below** and by `14-CONTEXT.md` decisions **D-14-A** and
**D-14-B**; its wording is cited by where it lived rather than restated here.)*

**There is no read-back** — no `Get*`/`Query*` intent exists for any accessibility setting
across all 35 intents in the framework — so §21's "do not clobber a pre-existing
accessibility state" cannot be satisfied by detection. **User decision 2026-08-17: default
ON, disclosed in onboarding.** Branch on `safety.ash_managed_color_filters` (already in
Config, dead code until this phase made it live): true → real toggle, false → **the Circle
fires a bare Nothing**, not BD-01's visual pause — per **D-14-C**, the alert that *was* Circle
2 is deleted rather than kept as a fallback, because the escalation from Circle 1 to Circle 2
is the escalation from interrupting with words to changing the environment without them. The
disclosure ships in the **Control Room Note**, not at import: it states plainly that PROSOCHĒ
turns Color Filters on and off, names the kill switch and its shipped default, and says where
to change it. The pre-existing-grayscale user is **accepted and backlogged, not solved**
(**D-14-D**) — `.planning/todos/pending/2026-08-19-ash-void-circle-when-user-already-uses-grayscale.md`.

Also correct `src/CONFIG-BLOCK.md`'s BD-01-R note, which asserted Ash *is* already a real
Color Filters change while a neighbouring note asserted its alert-only body was verbatim —
make it true or make it honest, but do not leave both. Closes spike 005 step 5 and retires
backlog phase 999.3.

**What shipped (2026-08-19).** Both forks re-signed under their exact display names and
decrypt-verified; **15 `AXToggleColorFiltersIntent` sites per fork** — 11 apply, 4
unconditional off. **Gate A now exits 1 permanently by construction** and the obligation is
`docs/gate_a_residue_check.py`, never the raw validator command (**D-14-01**, `DEV-08`).
**Nothing in this phase is device-proven:** `14-UAT.md` is the instrument, every test is
blank, and it is BLOCKED on `DIST-03`.

**Severity:** major
**UI hint**: no
**Requirements**: CIRC-02, SAFE-01, SAFE-02, SAFE-05, AUDIT-02
**Depends on:** Phase 11
**Plans:** 3/3 plans executed

> **⚠ SCOPE RESET — user, 2026-08-19. APPLIED: the goal prose above was corrected in place by
> plan 14-03 and now describes what shipped.** This banner is retained as the record of what
> was reset and when, per this project's convention of superseding by pointer rather than
> deleting. What it retired: routing colour through the phase-16 capture machine as a third
> member, with a marker of who changed it and the persist-then-apply ordering that machine
> needs. That was over-built. Grayscale has exactly **two** values, so there is nothing to
> remember — "restore" is unconditionally "set it off". `14-CONTEXT.md` decisions
> **D-14-A/B/C/D** are the binding scope and override the superseded wording wherever a reader
> meets it. The superseded six-plan, sixteen-task set is parked at `superseded/` in the phase
> directory and is **not** the plan list below.

Plans:

- [x] 14-01-PLAN.md — TRACER: the Color Filters action on at Circle 2 with no alert, one unconditional off inside the restore expansion, guards registered only where they can fire, checkers taught (wave 1, D-14-A/B/C/D)
- [x] 14-02-PLAN.md — The gate-A disposition: the constitutional edit, the mechanical residue checker, and the deviation-log entry (wave 2, D-14-01)
- [x] 14-03-PLAN.md — Disclose the change in the Control Room Note, correct the config mirror, re-sign both forks, author `14-UAT.md`, retire backlog 999.3 (wave 3, D-14-03)

### Phase 15: Circle 8 — the Voice primitive

**Goal:** Build Circle 8. **The product ships eight working Circles, not nine** — at Circle 8 you get
the menu, tap Continue, and nothing happens. The escalation ladder goes quiet at exactly the
point before Ice, the second-strongest Circle in the design.

`primitive_dispatch()` iterates the nine primitive names but explicitly `continue`s past
`Voice`, and because the dispatch comparison is condition 99 ("contains"), the sequence entry
`"Voice"` matches no emitted branch and fails **silently**. Confirmed against the shipped
artifact, not inferred: every other primitive renders 10 dispatch branches; Voice renders 0.
Found by static comparison, never by testing — Circles 2–9 have never run on hardware.

**Decide the semantics first, and record the decision.** The likely intent, consistent with
§11 Primitive H: **Mirror (Circle 7)** shows the text and speaks it only if `voice_enabled`;
**Voice/Loud Mirror (Circle 8)** makes the spoken address *the* primitive — the escalation is
that the phone talks to you. Whether `voice_enabled = 0` degrades Circle 8 to a
Mirror-equivalent alert or skips it entirely is a real product decision, not an
implementation detail.

**Deliverables.** Emit a real Voice branch — either drop the `continue` and give
`mirror_and_voice()` a mode parameter, or split it into `mirror()` and `voice()` sharing the
template selector. **Watch the `Spoken This Run` guard**: if Circle 8 is reached in a run
where Mirror already spoke, the guard currently suppresses the second utterance.

**Sequencing note.** Phase 11 gives Circle 8 an interim branch (the Mirror) so the
dispatch-coverage guard can be a hard gate from the start, and moves dispatch to condition 4
(exact) per BD-06, which removes the "contains" fragility that hid this defect. This phase
replaces that interim branch with the designed primitive. Phase 10 already added
`docs/sequence_dispatch_check.py`, which currently **reports** the Voice orphan and exits 0;
once Voice dispatches, remove its `KNOWN_ORPHAN_ENTRIES` exemption rather than merely
satisfying it — after the rename the entry is `"Loud Mirror"`, so a stale exemption would
whitelist anything named `"Voice"` forever.

> **PLANNING CORRECTION, 2026-08-18 — the Goal text above is a historical statement of intent and
> six of its seven factual claims are now false.** It was written 2026-08-16, *before* Phase 11
> executed on 2026-08-18. Phase 11 already renamed the Circle-8 sequence entry `Voice` → `Loud
> Mirror` in all three sequences, emitted a real dispatch branch for it, moved dispatch from
> condition 99 ("contains") to condition 4 ("string is"), and promoted
> `docs/sequence_dispatch_check.py` to a hard gate with `KNOWN_ORPHANS = {}`. **Circle 8 is not
> silent — it currently runs the interim Mirror implementation. There is no `KNOWN_ORPHAN_ENTRIES`
> exemption to remove; that symbol does not exist and `KNOWN_ORPHANS` must stay empty. The
> `Spoken This Run` warning is retired** — exactly one dispatch branch fires per run under
> condition 4, so Mirror and Loud Mirror can never both speak (locked decision D-06). The residual
> work is replacing the interim with a designed `voice()`, plus the `voice_enabled` type
> normalisation and the guard set. `15-RESEARCH.md` § Pitfall 1 tabulates every stale claim. The
> Goal is struck rather than rewritten so the correction has something to point at.

**Severity:** major
**Requirements**: CIRC-08, CIRC-09, CIRC-14, DIST-01
**Depends on:** Phase 11
**Plans:** 5/5 plans executed

Plans:
**Wave 1**

- [x] 15-01-PLAN.md — TRACER: split `mirror_and_voice()` into `mirror()` (Circle 7 shows) and `voice()` (Circle 8 speaks), retarget the dispatch tuple, add `verify_speaktext_placement()`, rebuild and gate-A both forks
- [x] 15-02-PLAN.md — rung-2 simulator probe discriminating the inherited axis-4 unfilled picker across `list` / `getitemfromlist` / `speaktext`, then route the verdict per D-04

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 15-03-PLAN.md — normalise `voice_enabled` to numeric `1`/`0` at the bootstrap writer, bump `schema_version` 4→5, add `verify_voice_enabled_seed()` (D-05)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 15-04-PLAN.md — `verify_voice_gates()`, `verify_voice_path_volume_silence()`, and the "no two entry names are action-equal" assertion in `docs/sequence_dispatch_check.py`

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 15-05-PLAN.md — rebuild, sign and payload-assert both forks, re-derive MANIFEST, discharge the recording duty into BUILD-NOTES §36, author `15-UAT.md`

**Cross-cutting constraints:**

- Circle 9 still dispatches `Frozen` in all three sequences and `ice_start()` is untouched (CIRC-09).
- Two distinct sequence-entry names never resolve to action-equal dispatch branch bodies, so an escalation on paper is an escalation in emitted actions (CIRC-14, edge: adjacency).
- Every Mirror template list carries at least 9 rows so `WFItemIndex = Circle Next` (1..9) is always in range, and no user-facing surface — alert or speech — is reachable from a Circle-0 OPEN.

### Phase 16: Dimming and Silence as distinct device-proven Circles

**Goal:** Prove Dimming and Silence work as **distinct, device-verified Circles with reliable
capture-and-restore** — the outstanding half of Phase 9, which merged its code untested.

**Two things are true and the second is the risk.** They are built and merged: Phase 9
landed the numeric-coercion fix for all 28 `setbrightness` (14) / `setvolume` (14) operand
sites (`2e2261e`, artifacts in `c6d8737`), and Phase 10 pinned the whole surface with
`docs/environmental_restore_check.py` so it cannot be removed by accident. **But they have
never run on a phone, and the merge did NOT make them live** — the coercion fix was necessary
and not sufficient. Both bodies sat in the never-taken arm of a permanently-true
`settings_snapshot` container gate and were unreachable until plan 11-08, independently of and
prior to Phase 16's own persistence fix; 44 environmental actions per fork could not run. They
are reachable now, and the code that puts them back has still never once executed on hardware.
`09-UAT.md` has 12 tests; exactly one has passed — test 1, the static "coercion chip does not
render red" gate.

**The coercion shape itself is analogy-based, not donor-confirmed.**
`WFCoercionVariableAggrandizement` / `CoercionItemClass: WFNumberContentItem` is confirmed
for the Donor-4.1 *conditional operand* position; whether it is correct at a **direct
Set-action parameter** position is genuinely unknown. `Donor 10.shortcut` contains no
variable-fed `WFBrightness`/`WFVolume` example. If it proves wrong, follow `09-RESEARCH.md`'s
fresh-donor protocol — build a donor on device with a variable-fed Set Brightness and decrypt
it. **Do not guess a second `CoercionItemClass`.**

**Deliverables.** Run `09-UAT.md` tests 2–12 on a real iPhone. The closed-loop proof is what
matters: `Get Device Details` returns a real, correctly-typed value; the has-any-value guard
correctly *skips* the change when the read returns nothing; CLOSE restores the original
exactly. **Then the ugly cases** — app force-quit mid-session, device restart mid-session,
CLOSE never firing, two overlapping sessions, screen locked mid-session. Each must restore or
leave the user at a safe value. Never dark. Never silent forever. Never loud. Emergency
Restore must recover from every failure mode found, and it has itself never been tapped on a
device.

**DEV-06 is live again** — `changed_at` / `changed_by_session_id` are written at 20 sites and
read nowhere. That was recorded MOOT conditional on the cut proceeding; the cut is cancelled,
so DEV-06 and the `Session ID` scope defect both return. `docs/BUILD-NOTES.md` §17 reserves
the DEV-06 decision to the user — surface it, do not decide it unilaterally.

**The brightness floor was corrected, and the main-line decision has been TAKEN.** Phase 9
revised BD-02's floor clause — cited here, deliberately not restated, since a live file that
reproduces the clause it retires still carries it. The user's on-device observation is that
iOS's practical minimum is dim, not black, so avoiding a particular value was never itself the
safety property — capture-and-restore reliability is. That revision was scoped to the
experimental fork. **User decision D-01, LOCKED 2026-08-17, settles it on main:**
`safety.brightness_floor` and `safety.dim_target` are both `0`. Plan **16-03** carried the code
half (six code sites, incl. the emitted comment shipping 11× per fork); plan **16-05** carried
the record half (21 measured record sites) and the repo-scoped gate. Authority:
`docs/CAPABILITY-DECISIONS.md` BD-02's Supersession note.

Distinct-Circle allocation is already settled by **BD-06 Decision 4** — do not re-cut it.

**Planning correction (2026-08-17, plan-phase).** Research re-measured the artifact and found a P0
this goal did not know about: **the capture is never persisted.** A captured
`settings_snapshot.*.original_value` is written into the `State` dictionary, but the last `State`
save on the OPEN arm precedes `universal_leaving()` and every later save writes `Reloaded State` —
a different dictionary. CLOSE and Emergency Restore therefore find the cleared sentinel, fail the
numeric gate, and skip. The screen dims and nothing in the product un-dims it. So "run `09-UAT.md`
tests 2–12" is **not** the opening move: fix persistence first, re-sign, then instrument. `09-UAT.md`
is superseded by `16-UAT.md` (no build identity, pre-rename fork names, test list predates the
finding); its single recorded pass does not carry forward. Two user decisions locked before planning:
**D-01** floor and dim target both to `0`; **D-02** remove `changed_at` / `changed_by_session_id`.

**Severity:** major
**Requirements**: CIRC-03, CIRC-05, SAFE-01, SAFE-02, SAFE-03, SAFE-05, DIST-03
**Depends on:** Phase 12
**Plans:** 6/6 plans executed

Plans:
**Wave 1**

- [x] 16-01-PLAN.md — TRACER: persist the captured original before the device is changed; build guard + negative control (wave 1)
- [x] 16-02-PLAN.md — Aimed rung-2 coercion probe at a direct Set parameter; disposition the 11 uncoerced volume sites (wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 16-03-PLAN.md — D-01 code half: floor and dim target to zero; six measured code sites, incl. the 11×/fork emitted comment (wave 2)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 16-04-PLAN.md — D-02: remove the two dead snapshot leaves as one coordinated change; no-reader guard (wave 3)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 16-05-PLAN.md — D-01 record half: 21 measured record sites, the BD-02 §21 supersession note, and the repo-scoped gate (wave 4)

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 16-06-PLAN.md — Rebuild, re-sign, refresh manifest, author 16-UAT.md; device session BLOCKED-or-proceed (wave 5)

**Split 2026-08-18, user decision.** D-01's blast radius was under-counted four times (6 → 8 → 9 →
13+), so the record sweep was split out of 16-03 into its own plan: the safety-critical code fix
does not wait on it. The canonical strategy is **frozen** — BD-02 records the supersession instead.
The class is not purely lexical (`docs/phase5_self_check.py:117` encodes it as a value check with
none of the vocabulary), so 16-05 pairs a repo-scoped gate with an explicit human-reasoned list and
presents neither alone as complete.

### Phase 17: Covenant substrate

**Goal:** The covenant model's machine layer exists and is guarded: contract windows, the coverage
gate, Core's deterministic verdict, lossless recording — plus the three engine fixes that block
clean measurement of any of it. No surface changes in this phase: coverage silently gates the
*existing* v1 surfaces, so the artifact stays coherent at every commit and Phase 18 changes what
fires, not whether firing is decided correctly.

**Deliverables:**

- **`active_contract` container** seeded at bootstrap per axis-7 discipline (permanent container,
  flat leaf writes, sentinel/numeric gates, single-item-collapse aware), with `verify_*_seed()`
  guards and the `schema_version` bump decided deliberately. Leaves per canon §10.2: `made_at`,
  `expires_at`, `intention`, `boundary_seconds`, `opens_within`, `rapid_returns_within`,
  `consumed_seconds`, `status`.
- **The coverage gate** in `open_pipeline()` after the state save, before `universal_leaving()`:
  covered ∧ Circle < ceiling → no dispatch (COV-01/02/05). A live cooldown short-circuits first,
  unchanged.
- **Invalidation bookkeeping** on OPEN (`opens_within`, `rapid_returns_within`, expiry — COV-04)
  and **consumed-seconds accounting** on CLOSE with outcomes settled losslessly into
  `recent_contracts` (COV-06). This closes the `recent_contracts` never-written blocker (F-2,
  `.planning/todos/pending/2026-08-19-recent-contracts-never-written.md`) — the scope question it
  parked is answered by canon §7.4: window outcomes, rolling ~10.
- **Core's verdict function** (VERD-01/02): recorded-fact arithmetic against
  `verdict.challenge_overrun_count`, wired into `confession()`/`persist_contract()`; ALLOW starts
  coverage. DENY is not reachable until Phase 18 builds Redirect — the envelope constant ships,
  the Circle 6 arm stays dormant, and the dispatch-coverage guard keeps it honest.
- **Covered-reopen Heat rule** (COV-08, `heat.covered_reopen_bonus`) in the Heat pipeline.
- **MET-01/02 counters**: the session record carries a covered flag; the day record carries a
  surface counter.
- **Engine fixes folded in, one class each:** `round_down()` on `Gravity Raw`
  (`.planning/todos/pending/2026-08-19-floor-gravity-to-match-spec.md` — land before any
  Pressure-accumulation run); `enabled_exits()` actually filtering
  (`2026-08-19-enabled-exits-filters-nothing.md`, F-18/G-06-12 — prerequisite to any
  exit-learning measurement); the timezone-naive epoch anchor and single-item-collapse todos
  reviewed against the new keys so the new container does not re-import either defect.
- Config additions per canon §10.3 (`contract.*`, `verdict.*`, `bands.*`, `variability.*`,
  `heat.covered_reopen_bonus`), mirrored in `src/CONFIG-BLOCK.md` in the same commit, with
  `docs/retired_clause_check.py`'s record-matches-build invariant kept green.

**Severity:** major
**Requirements**: COV-01..08, VERD-01..02, MET-01..02, EXIT-08, STATE-04, CONT-02, CONT-05
**Depends on:** Phase 12 (state-shape discipline), Phase 16 (persistence fix)
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 17 to break down)

### Phase 18: Bands and surfaces

**Goal:** The interaction model becomes the covenant model. The universal `Leaving / Continue`
pre-menu is retired; Band B fires silently; every open shows at most one surface; every
interactive surface carries its own one-tap leave; the slot table becomes BD-09's; Redirect
exists; the exits land somewhere real.

**Deliverables:**

- **Pre-menu retirement** (BAND-03): `universal_leaving()` stops emitting the menu; dispatch runs
  directly inside the Circle > 0 band. `verify_circle_zero_silence()` and
  `docs/router_ui_census.py` re-derived for the new surface census.
- **Panic Escape re-expression** (BAND-04): the removable one-tap leave affordance moves *inside*
  the interactive surfaces — Pause's alert becomes a two-option surface (Leave / Continue), the
  ask carries "Take me somewhere better", the Mirror carries its leave route. The
  `panic_escape_enabled` flag, its seed, its Note-edit-plus-confirmation removal path, and the
  absolute separation from Emergency Restore all carry forward; removal now strips exactly the
  in-surface leave options and nothing else. SEED-009 item 3's `Exit / Stay` naming lands here as
  part of the copy, one pass, final.
- **Band B silence** (BAND-02): Black and White, Silence, and (Ambient) Dim fire with no dialog.
  Pause stays the single Band B surface.
- **The Mirror's three-route surface** (BAND-05) at Band C: continue / leave / declare, with the
  declare route entering the ask. Mirror templates gain covenant facts (declared vs consumed, the
  invalidation reason) — fact-gated as ever, and the ordinal-fact-binding todo
  (`2026-08-17-mirror-templates-ordinal-fact-binding.md`) is honoured in the same template pass.
- **Slot table v2** (BAND-06): the BD-09 table into all three sequences — Mirror to Circle 5,
  Redirect at 6, Eject at 7, Frozen pinned at 9, Dim in Ambient only, Blackout in none.
  `verify_dispatch_coverage()` remains the hard gate; `docs/sequence_dispatch_check.py` re-derived.
- **Redirect built** (absorbing the v1 Phase 17 Exile-split scope): lands the user directly in
  the deterministically selected exit — no menu (BD-06 Decision 6 reaffirmed by BD-09), reusing
  `select_exit()` and `record_exit_and_route()` unchanged so the involuntary path feeds the same
  learning loop. DENY (Circle 6) routes here (VERD-04).
- **Exit-route deepening** (carried from the v1 plan): for each exit — what opens, what context
  crosses, what the user sees one second after landing. Capture/Coordinate create the note or
  reminder seeded with the live intention rather than cold-opening an app; Consult keeps carrying
  its query; Close stays the honest null option, undecorated.
- **`Set an intention`** manual-menu item (COV-07) and the Pause copy bank (VARY-04's
  deterministic rotation, spot check still off).

**Severity:** major
**Requirements**: BAND-01..06, COV-07, VERD-04, VARY-04, CIRC-01, CIRC-06, CIRC-07, CIRC-13, EXIT-01..07
**Depends on:** Phase 17
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 18 to break down)

### Phase 19: Personalized descent

**Goal:** Onboarding asks about feelings and preferences, not mythology — and two people with
identical usage get the products they each asked for.

**Deliverables:** the severity import question mapping plain language to Paradise / Purgatory /
Inferno (PERS-01: "Mostly fine — keep a light touch" / "Somewhat concerned — balance it" /
"It's a real problem — be strict with me", default Purgatory); the modality import question
mapping to Classic vs Ambient (PERS-02); Note and Status naming both vocabularies (PERS-03);
Change Profile / Change Sequence re-elicitation confirmed lossless (PERS-04); the Note's
covenant paragraph (canon §15.2) and the refreshed READ THIS FIRST voice. Import questions are
literal-text prefill — the mapping stays an If-chain at bootstrap, within the mechanism's known
limits. `bands.ask_entry` / `bands.rescue_entry` exist from Phase 17; this phase documents them
as the reserved tuning knob and deliberately does not vary them per profile yet.

**Severity:** major
**Requirements**: PERS-01..04, BOOT-09, ROOM-01, ROOM-07
**Depends on:** Phase 18
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 19 to break down)

### Phase 20: Aware verdict alignment

**Goal:** Aware's model judgment operates inside the deterministic envelope, at the ask and the
reflections, and nowhere else — and the Aware artifact is rebuilt from the current Core rather
than patched.

**Deliverables:** rework `audit_block()` into the envelope verdict at Circles 4–6 (VERD-03):
model output accepted only within the Circle's available set, everything else silently falling
back to Core's verdict; one CHALLENGE maximum carried; DENY→Redirect only (VERD-04). Reflection
generation for Mirror / Loud Mirror unchanged in role, updated for covenant facts. **No model
call on covered opens** — the gate precedes the insertion point by construction, and
`docs/sentient_audit_check.py` re-derives the one-audit-per-rendering invariant against the new
graph. SENT-02's contract is restated: the model appears at the ask and the reflection surfaces,
never in Band A/B, never at Frozen, never under coverage. This is also the natural home of
**SEED-005** (re-fork Aware from the post-conversion Core) — a rebuild, not a patch, keeping
`docs/sentient_core_check.py` green.

**Severity:** major
**Requirements**: VERD-03..04, SENT-01..15 (re-verified against the new graph), DIST-01, DIST-02
**Depends on:** Phase 18 (Phase 19 can run in parallel; both precede 22)
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 20 to break down)

### Phase 21: Device debug and locked-screen CLOSE

**Goal:** Clear the device-behaviour blockers that would poison the Phase 22 sweep, and settle
locked-screen CLOSE persistence.

**The two open device blockers, routed `/gsd-debug`:**

- **Deferred OPEN intervention** (F-12, `2026-08-19-deferred-open-intervention.md`): an OPEN's
  intervention can surface minutes later, after the app closed — the mechanism is a hypothesis
  and must be established on device, because an interval-restoring product whose interruption
  arrives after the interval has closed is not degraded, it is absent.
- **Mirror's axis-4 unfilled picker** (`2026-08-18-mirror-primitive-unfilled-picker.md`): halts
  Circle VII and, post-15, the Voice path; spike 011 could not reproduce it at rung 2, so it is
  device-gated by construction.

**Locked-screen CLOSE** (carried from the v1 Phase 18 scope): establish on device whether the
CLOSE automation fires at all from a locked screen, fires and cannot write, or writes late —
the fix differs entirely per case. Spikes `001-device-is-locked-literal` and
`002-close-automation-vs-screen-lock` are the prior art; the todo
(`2026-08-16-persist-state-when-close-fires-from-a-locked-screen.md`) is the authority on the
symptom. The acceptance bar is canon §18's: never leave the user dark, silent, or holding an
unclosable session — if persistence cannot be guaranteed from a locked screen, an honest
recovery path on the next OPEN beats a lost write.

**Severity:** blocker (two entries), major (locked screen)
**Requirements**: SESS-01, SESS-07, STATE-12, SAFE-01, SAFE-05, CIRC-07, CIRC-08
**Depends on:** device access (DIST-03 tunnel); independent of 17–20 and can run beside them
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 21 to break down)

### Phase 22: Device UAT — bands, coverage, nine Circles, sequences

**Goal:** The covenant model converts from structurally-proven to actually-working on real
hardware. Exactly one Circle has ever executed on a phone; nothing of the covenant layer has.

**Run in this order; each stage is a real gate:**

1. **Fix the instrument** — `Test a Circle` is the harness and was itself once broken on device.
2. **The covenant scenarios** — the new model's own matrix: a covered open is fully silent; each
   invalidation trigger (expiry / open-count / rapid-return) ends coverage and the next open
   routes at its Circle; the ceiling holds at Circle 7; ALLOW/CHALLENGE route as specified;
   DENY lands in Redirect; the voluntary `Set an intention` covers identically.
3. **Nine Circles in Classic**, per-Circle verdicts: does it appear, is the copy non-empty, is
   the leave route reachable, does control return. Record **dismissibility** per SEED-009 item 2
   — what it cost to get past, in taps and seconds; a Circle waved through in under a second has
   not been verified in any sense that matters.
4. **Sequence switching** — BlackMirror and Ambient sweeps.
5. **Environmental closed loops** — `16-UAT.md`'s twelve tests and `14-UAT.md`'s six, run beside
   each other in one sitting: capture → persist → apply → restore, then the ugly cases
   (force-quit, restart, CLOSE-never-fires, overlap, locked screen via Phase 21's findings).
   The single highest-value observation: force-quit mid-intervention, run Emergency Restore,
   confirm colour and brightness return. `setbrightness.WFBrightness` is OPTIONAL with a 50%
   default — verify the **value applied**, never the absence of an error.
6. **Frozen's own scrutiny** — cooldown written, live cooldown short-circuits (before the
   coverage check), Emergency Restore works from inside it, expiry relieves Heat, profile
   durations honoured.
7. **Pressure actually drives Circle** — repeated real opens escalate as the thresholds say
   (`Test a Circle` bypasses the arithmetic). Report opens-to-first-interruption per profile —
   the tuning signal for the raised entry thresholds and the severity mapping.

**Also outstanding and batched into the same sessions:** `13-UAT.md`, `12-UAT.md` Test 3,
`10-UAT.md`, Phase 4 UAT tests 1 and 3–6, Phase 8's real-iPhone import (Aware has never been
installed), `15-UAT.md` (mind its install-ordering constraint: any schema-bumping build installs
**before** Pressure-accumulation tests, because the first run rebuilds `state.json`).

**Device round trips are the scarce resource.** One class-wide fix per trip. Read the error
text, not just the symptom. Branch on `tunnelState` from `xcrun devicectl list devices
--json-output`, never on the `State` column.

**Severity:** blocker
**Requirements**: DIST-03, COV-01..08, VERD-01..04, BAND-01..06, PERS-01..02, CIRC-01..14, SAFE-01..06
**Depends on:** Phases 18, 20, 21 (19 strongly preferred first so onboarding is tested once)
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 22 to break down)

### Phase 23: Variability against ritualisation

**Goal:** Research, arm, and tune the deterministic spot check — after the covenant model has
device evidence, never before.

The failure mode is canon §13's: a surface repeated identically trains its own dismissal
(Epictetus' deferred-attention habit; the observed fate of Screen Time prompts). The mechanism
shipped dormant in Phases 17–18: `variability.spot_check_interval = 0`, the persisted
`variability_counter`, and the Band-C-only jump semantics (VARY-02/03). This phase: define the
proxies **before** tuning (contract specificity over time, fidelity trends, dismissal cost from
Phase 22's observations, self-report — and record what these cannot see); arm the spot check at a
candidate interval; compare against the dormant baseline; decide the shipped default. Also
evaluate whether surface rotation (VARY-04) is varied *enough* — lexical variation that reads as
the same prompt in different clothes buys nothing. Invariants re-asserted, not re-decided:
counter-based only, Band C jumps only, nothing touches Frozen/safety/environmental/coverage,
and the silent band stays silent.

**Severity:** minor (research; the product is complete without arming it)
**Requirements**: VARY-01..04
**Depends on:** Phase 22
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 23 to break down)

### Phase 24: UX optimisation — onboarding and in-run interaction cost

**Goal:** Optimise PROSOCHĒ as an *experience*, with the covenant model settled and device-proven
underneath it.

The v1 heavy-UX questions that the covenant redesign already answered — the announcement menu
(retired by BAND-03) and the Circle-order tuning (settled by BD-09's table) — are out. What
remains:

1. **Instrument the funnel** before redesigning it: import → first manual run → Note read →
   Automation A → Automation B → first OPEN → first intervention completed; decide what
   `state.json` records locally about how far setup got (local-only, canon §26).
2. **Latency**: measure perceived on-device delay per surface — an intervention arriving after
   the user is already scrolling has missed the interval the product exists to create.
3. **Copy voice** (canon §19): concrete facts, no slogans; retire anything that lectures; roll
   telemetry into surfaces that already fire rather than announcing numbers.
4. **Note restructure** around read-once vs return-to: setup collapses once automations exist;
   settings and ledger surface; the proforma defers out of the critical path.
5. **Re-verify from a genuinely fresh import** — delete `state.json` and the Note first.

**Severity:** major
**Requirements**: ROOM-01..12, BOOT-01, BOOT-09, DIST-04, DIST-05, MET-02
**Depends on:** Phase 22
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 24 to break down)

### Phase 25: One product or two — Core/Aware fork decision and device eligibility

**Goal:** Settle whether PROSOCHĒ ships as one product or two, and — if two — make choosing
require no knowledge the user doesn't have.

The accumulated evidence (all still standing): **spike 003 INVALIDATED** automatic capability
detection (`Device Model` returns bare `"iPhone"`; no try/catch exists — confirmed by Apple DTS);
**spike 008 VALIDATED** the `WFLLMModel = "Apple Intelligence on Device"` literal; **spike 004 is
PARTIAL** — the toggle gates correctly both ways and the ordering property held under one real
failure, but its `askllm` omitted `WFLLMModel`, so the pinned path was never exercised, and the
observed "downloading" halt cannot distinguish ineligible hardware from an unprovisioned capable
device. **New since the seed: Phase 20 shrinks the Aware delta further** — with verdicts shared
and only the model call differing, the merge case strengthens (SEED-006).

**What the phase does:** (1) amend or uphold canon v2 §25's two-fork answer as a recorded
decision; (2) re-run the capability gate with the pinned literal across the four device states
(capable+provisioned / capable+downloading / capable+AI-off / genuinely ineligible), asking one
question each time — graceful halt or hang/partial write; if any state hangs, the merge is off
on safety grounds; (3) resolve determinism provability in a single graph (what replaces the
fork-skew check); (4) if two products: ship the **state check** instruction ("Settings → Apple
Intelligence & Siri exists and has finished setting up → choose Aware") — it covers ineligible
and unprovisioned with one instruction, which a model list cannot; the model-list trap stands
(iPhone 15/15 Plus do not qualify; the 16e does); (5) if one product: SEED-005's refork is a hard
prerequisite, then a full re-run of the device UAT in both AI modes.

**Severity:** major
**Requirements**: DIST-03, DIST-04, DIST-07, BOOT-01, ROOM-01
**Depends on:** Phase 24 (and SEED-005 via Phase 20 if the merge is chosen)
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 25 to break down)

### Phase 26: Cumulative state — lifetime and windowed attention aggregates

**Goal:** Give PROSOCHĒ the ability to say what it has actually done — the honest data layer
under the Attention Receipt and, later, the support ask. No user-facing display in this phase.

**The engineering risk is the schema, not the arithmetic.** Canon §10 mandates bounded rolling
windows; every new key is seeded with a build guard; the STATE-SHAPE axis has bitten three times
on device. Two shapes: bounded windows for per-period figures, monotonic lifetime counters for
"since installing." Decide the `schema_version` bump and migration deliberately.

**Metric definitions are the real work, each one a recorded decision (MET-03):**

- **"Automatic opens interrupted"** counts only opens where something was actually shown —
  silent-band opens are *observed*, covered opens are *honoured*; counting either would inflate
  the number into the self-congratulatory telemetry canon §19 forbids.
- **Covered-open share** and **surfaces per day** — the covenant's own success curve, from
  MET-01/02's recording.
- **"Most effective exit"** reuses `exits.exploit_min_observations` as its confidence floor —
  never name a winner from two samples.
- **"Contracts kept"** reports from `recent_contracts` as a ratio with its window stated.

Estimates stay governed by canon §26: observed metrics may be stated directly; any estimated
attention reclaimed must be labelled an estimate, personally baselined on rolling medians,
lower-bounded at zero, and is its own later decision (VAL-02/03).

**Severity:** major
**Requirements**: MET-03, VAL-01, VAL-02, STATE-12, SESS-07, SAFE-01
**Depends on:** Phase 17 (schema discipline); display depends on Phase 27
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 26 to break down)

### Phase 27: The Attention Receipt

**Goal:** A separate, local, disposable Note the user asks for and PROSOCHĒ regenerates from
`state.json`: daily, 7-day, and lifetime views. The artifact a person might genuinely screenshot
and send to someone.

**Shape:** distinct from the durable `PROSOCHĒ` Note — regenerated, never accumulated. Three
cadences, one generator. It names depth in the Dante vocabulary (`PEAK DEPTH — CIRCLE VII`) and
now also speaks the covenant's language: contracts kept, attention declared and honoured. Ends
with `Spend your attention on purpose.`

**The design risk that must not be waved through: depth as achievement inverts the incentive.**
Peak Circle VII is a bad day. Render depth as a fact that reads as a confession, never a trophy,
never a congratulatory verb — **a receipt, not a scoreboard: no streaks, no scores, no shame**
(SEED-004). The covenant metrics help here: *kept covenants* are the shareable pride, and that
incentive points the right way.

**Privacy surface:** a shared screenshot is published. No app names, no timestamps, nothing that
fingerprints a routine; every proposed field faces "would the user knowingly publish this?"
**Provenance:** the receipt carries its own quiet attribution — a name and a source, not a
watermark (SEED-008's attribution half). **Honesty:** observed metrics only unless labelled
estimates; suppress figures below their confidence floors; **never shown while the user is being
blocked.**

**Severity:** major
**Requirements**: VAL-03, VAL-04, ROOM-04, ROOM-05, DIST-04
**Depends on:** Phase 26 (and Phase 11's names, long since landed)
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 27 to break down)

### Phase 28: Impact and reciprocity — sharing, then support

**Goal:** Turn the receipt into the two loops that let PROSOCHĒ spread and sustain itself —
**sharing first, support second** — without an account, a referral scheme, or a tracker.

**Impact loop, after meaningful value:** *Someone you care about might want some of this time
back too.* → Share PROSOCHĒ. No incentive, no tracking, no credit — the recommendation stays
uncorrupted by benefit to the recommender, and that absence is what makes it credible.
**Reciprocity loop, later:** the same local evidence, a different moment: *free forever; if it
has been worth something, pay what you think it was worth.* Sharing before payment states the
project's priorities without claiming them.

**Growth is decentralised by construction:** person A sends a link; person B downloads their own
copy. No account, no feed, no subscription, not even an app.

**The §26-inherited prohibitions are absolute:** never display the ask while the user is being
blocked; never guilt; never threaten functionality; never transmit attention history — the
trigger computes locally and the user only ever *chooses* to open a link. Support / Not now /
Never ask again, with `Never ask again` permanent and honoured, persisted with a build guard.

**Licence — settled 2026-08-19:** the repository moved from MIT to **PolyForm Noncommercial
1.0.0** going forward (not retroactive: everything published through tag
`pre-covenant-overhaul` remains MIT-licensed as published). This resolves SEED-008's central
tension in the pay-after-value direction: commercial redistribution of future versions is not
licensed, while personal use, forking, and noncommercial sharing stay free — so the voluntary
support ask is no longer undercut by the licence itself. SEED-008's remaining scope (provenance
declaration, attribution mechanics) folds into this phase and Phase 27's provenance line. The
outbound payment destination is settled with the project owner before any surface ships.

**Removal stays clean:** the whole support path sits behind a single generator toggle, so forks
can strip it.

**Successor:** the marketing and distribution phase, added once the receipt's real shape is
known.

**Severity:** major
**Requirements**: PAY-01, PAY-02, DIST-04..07, ROOM-04
**Depends on:** Phase 27
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 28 to break down)
