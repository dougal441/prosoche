# Roadmap: PROSOCHĒ — Nine Circles

## Overview

PROSOCHĒ ships as two forks of one Shortcuts action graph. The build starts by resolving four
independently-converged capability blockers (grayscale, brightness/volume read-back, Notes on
iOS, the `Use Model` On-Device literal) before any behavioural logic is authored, then lays down
routing/bootstrap/Control-Room onboarding, then proves the deterministic Heat/Gravity/Pressure
engine correct with stubbed primitives, then hardens the CLOSE/session-race protocol that contract
fidelity and exit learning both depend on. Only once that foundation is solid do the nine Circle
primitives and environmental safety floors get built, followed by exits, exit learning, and
contracts. The Dumb fork is then frozen, validated, signed, and on-device-verified as a complete
product in its own right — only after that does the Sentient fork add Apple On-Device Intelligence
as an additive, non-mutating wrap. The roadmap ends with both signed `.shortcut` files shipped
side by side, which is this project's definition of done.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 1: Capability Audit & Config Foundation** - Resolve all four capability blockers to VERIFIED/UNVERIFIED/NOT AVAILABLE with fallback designs and lock the tunable config block
- [x] **Phase 2: Routing, Bootstrap & Control Room Onboarding** - First-run bootstrap creates a valid state.json and Control Room Note; every invocation mode routes and self-heals safely
- [x] **Phase 3: Deterministic State Engine** - Heat, Gravity, Pressure, and Circle mapping compute correctly and demonstrably differ across all three profiles
- [x] **Phase 4: CLOSE Pipeline & Session Race Protocol** - Session duration is measured accurately and stays race-proof under rapid app switching
- [ ] **Phase 5: Nine Primitives & Environmental Safety** - All nine Circle primitives fire correctly with guaranteed safety floors and a model-free Circle IX
- [ ] **Phase 6: Exits, Exit Learning & Contracts** - Six exits are reachable and learned from; contracts are honoured and feed back into Heat
- [ ] **Phase 7: Control Room Manual Menu, Dumb Mirror Engine & Dumb Freeze** - Dumb implementation, validation, and signing are complete; real-iPhone first-run UAT remains pending
- [ ] **Phase 8: Sentient Fork & Dual Distribution** - On-Device AI wraps the untouched deterministic engine; both forks ship as signed, importable `.shortcut` files
- [x] **Phase 9: Dimming/Silence Stateful Restore** - Numeric-coercion fix merged for all 28 sites; device proof outstanding, carried by Phase 16
- [x] **Phase 10: Ship-readiness remainder and UX-lite pass** - Circle 0 silent band, OPEN notification removed, Control Room quieted, five new structural guards; device UAT deferred to Phase 19
- [ ] **Phase 11: Build Addendum 01 — Dante Circle names and the ten-primitive roster** - The rename lands once against BD-06's settled roster, with the dispatch-coverage guard written alongside it
- [ ] **Phase 12: State-shape sentinel gaps — exit_events and active_session** - The last two dotted-read crash risks are seeded and gated on leaf value; prerequisite for Phase 17
- [ ] **Phase 13: Red-operator conditionals and the WFItems List wrapper** - Donor 5 decrypted at last; the 14 red-operator sites and 2 blank-List sites fixed by class, with recurrence guards
- [ ] **Phase 14: Ash as real Color Filters grayscale** - The highest-evidence primitive stops being an alert box; restore leg is the deliverable
- [ ] **Phase 15: Circle 8 — the Voice primitive** - The product stops shipping eight working Circles out of nine
- [ ] **Phase 16: Dimming and Silence as distinct device-proven Circles** - Capture-and-restore proven as a closed loop under every ugly failure mode, or retired
- [ ] **Phase 17: Exile split and exit-route deepening** - Eject and Redirect become distinct Circles; the six exits stop being "open an app"
- [ ] **Phase 18: Persist state when CLOSE fires from a locked screen** - A locked-screen CLOSE stops stranding sessions and unrestored environmental changes
- [ ] **Phase 19: Device UAT — nine Circles and sequence switching** - The intervention layer converts from structurally-proven to actually-working on real hardware
- [ ] **Phase 20: UX optimisation — onboarding and in-run interaction cost** - The heavy UX round: funnel instrumentation, nine-Circle interaction cost, §29 voice, Note restructure
- [ ] **Phase 22: Cumulative state — lifetime and windowed attention aggregates** - The honest data layer under the receipt; metric definitions are the real work
- [ ] **Phase 23: The Attention Receipt** - A disposable, regenerated, screenshotable local Note — a receipt, not a scoreboard
- [ ] **Phase 24: Impact and reciprocity — sharing, then support** - Share first, pay-what-it-was-worth later; no account, no referral, no tracking

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
  2. Ash applies the audited visual-salience reduction or its documented Phase 1 fallback; Silence reduces media audio only when the original value can be captured and restored, otherwise degrades safely; Dimming reduces brightness only when reversible and never to zero, otherwise degrades safely — and across all primitives, brightness is never set to zero, volume is never increased or startling, any setting whose original value can't be captured is left unchanged, and pre-existing accessibility configuration is never blindly overridden.
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
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Capability Audit & Config Foundation | 5/5 | Complete | 2026-08-13 |
| 2. Routing, Bootstrap & Control Room Onboarding | 4/4 | Complete | 2026-08-13 |
| 3. Deterministic State Engine | 1/1 | Complete | 2026-08-13 |
| 4. CLOSE Pipeline & Session Race Protocol | 2/2 | In Progress|  |
| 5. Nine Primitives & Environmental Safety | 3/3 | Complete | 2026-08-13 |
| 6. Exits, Exit Learning & Contracts | 3/3 | Complete | 2026-08-13 |
| 7. Control Room Manual Menu, Dumb Mirror Engine & Dumb Freeze | 1/1 light | Human needed | - |
| 8. Sentient Fork & Dual Distribution | 3/3 | Human needed | - |

## Backlog

Unsequenced items that are genuinely new work rather than verification of an already-built
phase. (The six device-UAT items formerly listed here were reclassified 2026-08-16 — they
verify claims Phases 4/5/6/7 already make, so they now live as `{N}-UAT.md` files in those
phase directories, tracked via `/gsd-verify-work {phase}` and rolled up by
`/gsd-audit-uat`, not as roadmap phases.) Promote with `/gsd-review-backlog` when ready to
sequence.

### Phase 999.3: Grayscale / Ash capability donor test (BACKLOG)

**Goal:** Decrypt the already-on-disk `Set Colour Filters.shortcut` donor to settle,
with device evidence rather than catalog inference, whether Ash's grayscale toggle
(§6.5's strongest-evidence primitive) is actually buildable on iOS 26 with safe
read-back — and only then decide whether to rebuild Ash as designed.
**Severity:** minor
**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /gsd-review-backlog when ready)

Full context: `.planning/phases/999.3-grayscale-ash-capability-donor-test/2026-08-16-grayscale-ash-capability-donor-test.md`

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
     device's true minimum, not an artificial 10–15% floor — corrected 2026-08-16 per
     user on-device report that the practical minimum is dim, not a literal black/unusable
     screen (see `docs/CAPABILITY-DECISIONS.md` BD-02 addendum); the safety mechanism is
     capture-and-restore reliability (criteria 2–3, 5), not floor avoidance.

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
**Plans:** 6/6 plans executed

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
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 12 to break down)

### Phase 13: Red-operator conditionals and the WFItems List wrapper

**Goal:** Settle and fix two defect families carried unchanged through every cycle of the closed
`open-routing-sequence-error` session because both sit past breadcrumb J. Both are now safe
to pick up, and both are **device-visible defects that no file-level analysis can detect**.

**1. The 14 `WFConditionalActionString` red-operator sites ("Donor 5" family).** A variable
is placed directly into a conditional's TEXT-slot operand as a template. This is a
structurally different slot from the already-fixed `WFInput.Variable` envelope defect, so
that evidence does not transfer. Zero golden-corpus coverage, zero catalog coverage
(`is.workflow.actions.conditional` is absent from the ToolKit catalog entirely), zero device
coverage. **`.planning/debug/Donor 5.shortcut` was captured specifically to settle this and
has never been analysed** — decrypt it first (`aea decrypt` + `aa extract`, recipe in
`.claude/CLAUDE.md` §8) and read the real operand shape before touching any site. A concrete
starting site: `if_block("Previous Respected", 4, ...)`, seen rendering fully RED including
the operator picker in `.planning/debug/Screenshot 2026-08-14 at 11.55.12 pm.png`.

**2. The `WFItems` List wrapper (2 confirmed instances).** iOS wraps a variable-bearing List
row as `{"WFItemType": 0, "WFValue": <WFTextTokenString>}`; this artifact omits the wrapper,
so rows render blank. The same screenshot shows a List action rendering nine consecutive
rows as empty placeholders. The correct shape was already recovered from
`.planning/debug/Donor 4.shortcut` and `Donor 4.1.shortcut` but never applied.

**Deliverables.** Decrypt Donor 5, cross-check the recovered shape against the concrete site
before generalising, then sweep all 14 by class. Apply the Donor-4 wrapper shape to both List
sites, re-located by content. Add build-time recurrence guards for both, with sensitivity
demonstrated against a synthetically reverted artifact. Fold both newly-confirmed axes into
`.claude/CLAUDE.md`'s numbered axis list, together with the `read_value()`/`get_value()`
distinction and the `pending_exit` container/leaf pattern — do all three doc updates in one
pass.

**Why this gates the device UAT.** Blank text and red operators are exactly the two failure
modes Phase 19 is watching for. Fixing them first means a blank Circle in testing is a real
finding rather than a known artifact.

**Severity:** major
**Requirements**: CIRC-04, CIRC-07, ROOM-03, DIST-01, DIST-02
**Depends on:** Phase 12
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 13 to break down)

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
is strictly worse than no grayscale. Wire `state = 0` everywhere the other environmental
primitives restore — CLOSE, Emergency Restore, Ice expiry, the live-Ice redirect — reusing
`restore_managed_settings()`'s ownership pattern, and track it in `settings_snapshot`
alongside brightness and volume so Emergency Restore has one uniform recovery surface.
Routing it through the same path means one device pass can prove all three environmental
primitives.

**There is no read-back** — no `Get*`/`Query*` intent exists for any accessibility setting
across all 35 intents in the framework — so §21's "do not clobber a pre-existing
accessibility state" cannot be satisfied by detection. **User decision 2026-08-17: default
ON, disclosed in onboarding.** Branch on `safety.ash_managed_color_filters` (already in
Config, currently dead code): true → real toggle, false → BD-01's non-environmental pause.
Onboarding must state plainly that PROSOCHĒ turns Color Filters on and off, so a user who
needs their own filter setting for colour-blindness, migraine or low vision can turn the flag
off.

Also correct `src/CONFIG-BLOCK.md`'s BD-01-R note, which currently asserts Ash *is* already a
real Color Filters change — make it true or make it honest, but do not leave both. Closes
spike 005 step 5.

**Severity:** major
**Requirements**: CIRC-02, SAFE-01, SAFE-02, SAFE-05, AUDIT-02
**Depends on:** Phase 11
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 14 to break down)

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

**Severity:** major
**Requirements**: CIRC-08, CIRC-09, CIRC-14, DIST-01
**Depends on:** Phase 11
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 15 to break down)

### Phase 16: Dimming and Silence as distinct device-proven Circles

**Goal:** Prove Dimming and Silence work as **distinct, device-verified Circles with reliable
capture-and-restore** — the outstanding half of Phase 9, which merged its code untested.

**Two things are true and the second is the risk.** They are built and merged: Phase 9
landed the numeric-coercion fix for all 28 `setbrightness` (14) / `setvolume` (14) operand
sites (`2e2261e`, artifacts in `c6d8737`), and Phase 10 pinned the whole surface with
`docs/environmental_restore_check.py` so it cannot be removed by accident. **But they have
never run on a phone, and the merge made them live** — before the coercion fix these actions
silently no-opped; now they actually change brightness and volume, and the code that puts
them back has never once executed on hardware. `09-UAT.md` has 12 tests; exactly one has
passed — test 1, the static "coercion chip does not render red" gate.

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

**The brightness floor was corrected and needs a decision on main.** Phase 9 revised BD-02's
"never zero, 10–15% band": the user's on-device observation is that iOS's practical minimum
is dim, not black, so avoiding zero was never itself the safety property — capture-and-restore
reliability is. That revision was scoped to the experimental fork; decide it for main here.

Distinct-Circle allocation is already settled by **BD-06 Decision 4** — do not re-cut it.

**Severity:** major
**Requirements**: CIRC-03, CIRC-05, SAFE-01, SAFE-02, SAFE-03, SAFE-05, DIST-03
**Depends on:** Phase 12
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 16 to break down)

### Phase 17: Exile split and exit-route deepening

**Goal:** Split Exile into two Circles and deepen the six exit routes so an involuntary ejection lands
somewhere real.

**User decision 2026-08-16, settled in BD-06.** **Eject** (straight) is the current
behaviour: immediate, no menu, no question, Home Screen — its virtue is that it is instant
and cannot be negotiated with. **Redirect** (routed) ejects *into* a deterministically
selected destination, reusing `select_exit()` and `record_exit_and_route()` unchanged so the
exit is recorded, the return-time sample captured, and the involuntary path feeds the same
learning loop as the voluntary one. **User decision 2026-08-17: Redirect lands the user
directly rather than offering the "Take suggested exit / Choose another" menu** — that is
what makes it a Circle rather than a second Leaving menu.

**Selection is settled — do not re-litigate.** Deterministic exit, or home. No
`is.workflow.actions.number.random`, no shuffle, nowhere in the exit path. `select_exit()`
already is the mechanism: rotate by a persisted counter under 10 observations, then exploit
the lowest average return-time, with a Config-driven epsilon step that is itself a
counter-modulo test.

**Deepen the six routes — one design pass, then plan, then execute.** Every route is
currently just "open an app", and none has ever run on a device. For each, answer: what does
it open, what context crosses the boundary, and what does the user see one second after
landing? Leads, all against verified actions: **Capture** — create the note/reminder rather
than opening the app, seeded with the Intention text if one exists this session;
**Coordinate** — same, via the Reminders schemas in `PARAMETER_TYPES.md`; **Create** —
currently one saved URL for everyone, consider a small user-defined set; **Connect** —
opening Contacts cold is weak, and the no-send constraint is deliberate and stays;
**Consult** — already the strongest, it carries the query, use it as the model; **Close** —
the honest null option, keep it, do not decorate it.

**Hard prerequisite: Phase 12** (`exit_events` absent from the bootstrap template sits
directly on `record_exit_and_route()`; any device test of either Exile Circle hits it).

**Slot arithmetic is already resolved by BD-06** — ten primitives, nine slots per sequence,
each sequence picking nine. This phase flips Classic's and Ambient's Circle 6 from `Eject` to
`Redirect`; BlackMirror keeps `Eject` permanently. Do not re-open the roster question.

Canonical §30 and §36 are the reason the bare version is not enough: ejecting someone to a
Home Screen full of the same apps is a machine for changing *which* app consumes the time.

**Severity:** major
**Requirements**: EXIT-01, EXIT-02, EXIT-03, EXIT-04, CIRC-06, SESS-07
**Depends on:** Phase 12
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 17 to break down)

### Phase 18: Persist state when CLOSE fires from a locked screen

**Goal:** Make state survive a CLOSE that fires while the screen is locked.

Source: `.planning/todos/pending/2026-08-16-persist-state-when-close-fires-from-a-locked-screen.md`
— read it first; it is the authority on the observed symptom and is not summarised in full
here.

**Why it matters.** CLOSE is where session duration comes from, and therefore where every
restore-on-close behaviour is triggered: the contract outcome that feeds Heat, and the
brightness/volume/Color-Filters restore that Phases 14 and 16 make load-bearing. A CLOSE
that fires against a locked screen and fails to persist leaves an `active_session` no later
run owns, an unrestored environmental change, and a Heat value that never receives its
contract adjustment. This is the same failure family as the "screen locked mid-session" case
in `09-UAT.md`'s ugly-cases block, and the two should be investigated together rather than
twice.

**Approach.** Establish first what actually happens on device — whether the automation fires
at all, fires and cannot write, or fires and writes late — because the fix differs entirely
per case and this project's own evidence hierarchy puts device observation above inference.
Treat a file-level theory as a hypothesis to test, not a conclusion. `.planning/spikes/`
already holds two adjacent spikes worth reading before designing anything:
`001-device-is-locked-literal` and `002-close-automation-vs-screen-lock`.

**Safety framing.** Whatever the mechanism, the acceptance bar is the §21 one: never leave
the user dark, silent, or holding a session that cannot be closed. If persistence genuinely
cannot be guaranteed from a locked screen, the correct outcome may be a recovery path on the
next OPEN rather than a write at CLOSE time — an honest degradation beats a lost write.

**Severity:** major
**Requirements**: SESS-01, SESS-07, STATE-12, SAFE-01, SAFE-05
**Depends on:** Phase 16
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 18 to break down)

### Phase 19: Device UAT — nine Circles and sequence switching

**Goal:** Prove all nine Circles fire on a real iPhone, in all three sequences. **This is the phase
that converts the whole intervention layer from structurally-proven to actually-working.**

**Exactly one Circle has ever executed on real hardware** — Circle 1, once, build
`2026-08-15o`. Circles 2 through 9 have never run. No sequence other than the default has
ever been selected. Every Phase 5 "passed" verdict is static analysis of the action graph,
and graph well-formedness has repeatedly failed to predict device behaviour here: the seven
parameter-defect axes in `.claude/CLAUDE.md` were each discovered by a device run after a
clean validation, and **each was invisible to the sweep that caught the previous one**.

The nine primitives are the most heterogeneous code in the product — an alert, an
accessibility intent, two Get-Device-Details capture-and-restore loops, an Ask + Menu +
persisted contract, a Home Screen call, a 30-template selector, a speech action, and a
profile-aware cooldown writer. There is no reason Circle 1 working predicts anything about
Circle 6.

**Run in this order; each stage is a real gate.** (1) **Fix the instrument first** —
`Test a Circle` is the harness everything depends on and was itself broken on device once.
(2) Sweep all nine in Classic, recording per-Circle, not one verdict: does the intervention
appear, is the copy correct and **non-empty**, is there a reachable dismiss path, does
control return cleanly. (3) Switch sequence and re-sweep — BlackMirror and Ambient.
(4) Prove the environmental primitives as closed loops (`09-UAT.md` tests 2–12, the highest
risk in the matrix). (5) Give Ice its own scrutiny: it is the only Circle leaving a
*persistent* state — confirm the cooldown deadline is written, a live cooldown short-circuits
the next OPEN, **Emergency Restore works from inside Ice**, expiry applies Heat relief, and
profile durations (60/180/300 s) are right. (6) **Then verify Pressure actually drives
Circle** — `Test a Circle` bypasses the arithmetic, so the real question is whether repeated
opens escalate as the thresholds say.

**Also outstanding and to be run in the same sessions:** `10-UAT.md` (10 tests, all blocked
on DIST-03), `09-UAT.md` tests 2–12, Phase 4 UAT tests 1 and 3–6, and Phase 8's real-iPhone
import. Report the **opens-to-first-interruption count** from `10-UAT.md` Test 2 — that
number decides whether Phase 10's raised entry thresholds need tuning.

**Known defect to watch:** `open_pipeline()` has no `round_down()` on `Gravity Raw`, so
escalation timing is currently off-spec — the 0.1667 in the one device reading is exactly
1 ÷ 6 unfloored.

**Device round trips are the scarce resource.** One class-wide fix per trip, never one site.
Read the error text, not just the symptom.

**Severity:** major
**Requirements**: CIRC-01 through CIRC-14, SAFE-01, SAFE-02, SAFE-03, SAFE-05, DIST-03
**Depends on:** Phase 18
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 19 to break down)

### Phase 20: UX optimisation — onboarding and in-run interaction cost

**Goal:** Optimise PROSOCHĒ as an *experience*. Everything shipped so far was authored to satisfy the
canonical strategy and survive the seven parameter-defect axes — not to be pleasant, fast, or
obvious to a first-time user.

**This is the heavy UX round.** Phase 10 did the "lite" pass — the Circle 0 silent band, the
OPEN notification removed, `Leaving / Continue` reworded, the `shownote` gated, a
`Setup Check` menu item. Everything below was explicitly deferred to here.

**1. Instrument the funnel before redesigning it.** Define the drop-off points explicitly
(import → first manual run → Note read → Automation A created → Automation B created → first
OPEN → first intervention completed) and decide what, if anything, `state.json` should record
locally about how far setup got. This is the only honest way to know whether a change helped.
Local-only per §27.

**2. Full interaction-cost pass over all nine Circles.** For each: count taps, count actions
on the path, measure perceived latency on device, and confirm the dismiss option is present,
obvious, and one tap away wherever the design allows. §6.4's field study is explicit that the
single strongest mechanism is **giving the user an easy way to dismiss the consumption
attempt** — stronger than the deliberation message. The current design risks over-investing
in message text and under-investing in choice architecture. §12's stated key failure is that
the intervention becomes so annoying the user disables PROSOCHĒ — a product failure even if
it blocks more opens.

**3. Rewrite copy to §29's voice** — concrete behavioural facts, no slogans, no exclamation
marks, no emoji. Retire or rewrite anything that reads as a lecture. Roll telemetry into
interruptions that were already intended (the Intention header, the Mirror) rather than
announcing numbers.

**4. Restructure the Note around read-once vs. return-to.** Setup instructions collapse or
move to the bottom once automations exist; settings and the ledger surface at the top. Defer
the `MY PHONE, ON PURPOSE` proforma out of the critical path — it is not needed until the
first Mirror/Contract Circle, and asking at minute one competes with automation setup. Shorten
READ THIS FIRST to the two automations plus the safety warning.

**Re-verify from a genuinely fresh import** — delete `state.json` and the Note first. A
returning-user run does not test onboarding.

**Runs last by design.** It depends on the renames (Phase 11), the nine Circles actually
firing (Phase 19), and correct onboarding instructions (already fixed in quick task
`260817-au7`), because copy authored against the old names or against Circles that do not
fire would have to be written twice.

**Severity:** major
**Requirements**: ROOM-01 through ROOM-10, BOOT-01, BOOT-09, CIRC-01, DIST-04, DIST-05
**Depends on:** Phase 19
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 20 to break down)

### Phase 21: One product or two — Core/Aware fork decision and device eligibility

**Goal:** Settle whether PROSOCHĒ ships as **one** product or **two** (Core / Aware, formerly
Dumb / Sentient), and — if two — make choosing between them require no knowledge the user
doesn't have.

**This phase closes a question that has been open since SEED-006 was planted (2026-08-16)
and is now largely answered by evidence already in the repository.** Three spikes and one
generator design bear on it directly:

- **Spike 003 (INVALIDATED)** — automatic hardware-capability detection is impossible.
  `Get Device Details → Device Model` returns the bare literal `"iPhone"` on every device;
  no other `WFDeviceDetail` case (all 12 confirmed) disambiguates hardware. Apple's real
  check (`SystemLanguageModel.default.availability`) is a Swift API, unreachable without a
  companion app. Shortcuts has no try/catch, so "attempt and recover" is also closed.

- **Spike 004 (PARTIAL — downgraded 2026-08-17, was VALIDATED)** — a single artifact with
  an opt-in import question **is buildable**, and the toggle gates the branch correctly in
  both directions on real hardware. But the safety claim is **not** established. The spike's
  `askllm` omitted `WFLLMModel`, so neither device run exercised the pinned
  `"Apple Intelligence on Device"` path Sentient actually ships; and the failure it observed
  ("support for selected model is downloading") is a **provisioning-state** message that
  cannot distinguish ineligible hardware from a capable device whose ~7 GB of models have
  not downloaded yet. Owner's iPhone 16e — capable, models present — ran the same shortcut
  successfully, which is what forced the re-read. What survives: **the ordering property
  held under one real failure** (core completed before the halt).

- **Spike 008 (VALIDATED, donor ground truth)** — `WFLLMModel = "Apple Intelligence on
  Device"`. SEED-006's blocker #2 ("the On-Device literal is unrecovered, and in a merged
  world it blocks everyone") is closed.

- **`tools/build_sentient.py`** — the Aware delta is already *one* additive insertion
  (~56 actions) plus two toggle actions and one import question, all gated on
  `Import AI == "yes"`. Structurally, a merged product is close to what already exists.

**What this phase must actually decide and do:**

1. **Amend or uphold the canonical strategy.** §35 (`AI | Two product forks`), §5.7 (split
   justified on hardware capability), §31 (two signed `.shortcut` files as the deliverable)
   and §13 (Core must not be a degraded afterthought). Per §38 the document wins unless
   amended — so the first deliverable is a **recorded decision**, not code. §13/§33 Q4 want
   Core as a scientific control baseline; a recorded, stable runtime toggle preserves that
   comparison, and that argument must be made explicitly rather than assumed.

2. **Resolve SEED-006's blocker #3 — determinism must be provably untouched.** In a merged
   artifact both paths live in one graph, which makes the "additive, non-mutating wrap"
   claim harder to assert. `docs/sentient_core_check.py` and the shared build guards are
   the existing lever; decide what replaces the fork-skew check when there is no fork.

3. **Re-run the capability gate properly — this is the phase's gating experiment.** Spike
   004's downgrade leaves the merge's entire safety argument untested. Rebuild the gate with
   `WFLLMModel = "Apple Intelligence on Device"` (the shipped config, which spike 004 never
   used) and run it across four states, recording device model, iOS version, whether Apple
   Intelligence is enabled, and whether model download has completed:

   | State | Device | Why it matters |
   |---|---|---|
   | Capable, models downloaded | iPhone 16e / 15 Pro | Known-good baseline |
   | Capable, **models still downloading** | freshly-enabled capable device | **The merge's real risk** — new user at first run |
   | Capable, **Apple Intelligence switched off** | same device, toggled off | Ordinary user state, never tested |
   | Genuinely ineligible | a *recorded* SE / pre-15-Pro model | The case spike 004 claimed but did not establish |

   The question in every case is the same: is the failure a **graceful halt** (contained by
   ordering) or a hang / partial write? If any state hangs or writes partial state, the
   merge is off on safety grounds alone.

4. **Audit the Aware block's ordering against the fail-safe.** The audit block is inserted
   immediately *before* `persist_contract()`'s reload-and-save, so a `Use Model` halt there
   costs the contract write. The core arithmetic save (`build_state_engine.py:1116`) happens
   earlier in `open_pipeline()`, so the core loop looks protected — confirm on device. Note
   the reframed exposure: under two forks only a deliberate Aware downloader reaches that
   halt; under one product **a new user on fully capable hardware reaches it whenever the
   models haven't landed yet.**

5. **If the answer is TWO products: make the choice trivial.** The user's own framing —
   *a list of iPhone models, classified by a rule.* The rule: **A17 Pro or A18-class chip
   and ≥8 GB RAM** → iPhone 15 Pro, 15 Pro Max, the iPhone 16 family **including the 16e**
   (A18, 8 GB — owner-confirmed working), and everything since. The trap that makes a bare
   rule insufficient: the plain **iPhone 15 / 15 Plus do NOT qualify** (A16, 6 GB) despite
   the shared generation and identical iOS. So the deliverable is an explicit **model list**,
   not a chip rule the user has to apply — verified against Apple's own current support page
   at the time of writing, not against this roadmap entry.

   **Better than a model list: the self-check the user can actually perform.** The 16e
   evidence shows `Use Model` success tracks whether the models are *present*, not merely
   whether the chip qualifies. So the honest instruction is a state check, not a hardware
   lookup: *open Settings → Apple Intelligence & Siri; if it exists and has finished setting
   up, choose Aware.* That covers the ineligible-hardware case and the
   capable-but-not-provisioned case with one instruction, which a model list cannot do.

6. **If the answer is ONE product:** SEED-005 (re-fork/rebuild Aware) is a hard prerequisite
   — merging a stale Aware would fold known-broken code into the artifact everyone gets.
   Then: onboarding import-question wording, fork-aware build-guard rework, and a **full
   re-run of the device-UAT set in both AI-on and AI-off modes** — a merged build inherits
   none of Core's device confirmation for free.

**Naming note:** Build Addendum 01 §2 renames Dumb → **Core** and Sentient → **Aware**. If
the merge happens, those stop being product names and become **mode** names — decide which
before Phase 20 writes any user-facing copy against them.

**Standing blocker either way:** DIST-03 (both forks import onto a real iPhone and complete
a first manual run) is still unchecked — no qualifying device was reachable on 2026-08-13.
Aware has never been device-tested in this project at all.

**Severity:** major
**Requirements**: DIST-03, DIST-04, DIST-07, BOOT-01, ROOM-01
**Depends on:** Phase 20 (and SEED-005 if the merge is chosen)
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 21 to break down)

### Phase 22: Cumulative state — lifetime and windowed attention aggregates

**Goal:** Give PROSOCHĒ the ability to say what it has actually done — the data layer under the
Attention Receipt and, later, under the support ask. **No user-facing display in this
phase.** It exists so the numbers exist and are honest.

**The engineering risk is not the arithmetic — it is the schema.** Canonical strategy §16
mandates bounded rolling windows, so "just keep more history" is not available. Every new
key must be seeded in the bootstrap template with a build guard: this project has hit the
STATE-SHAPE axis **three separate times on device**, and a dotted read with a missing
segment is a hard error, not a blank. **Hard prerequisite: Phase 12** (`exit_events` /
`active_session`) — do not add keys on top of a schema whose sentinel gaps are still open.

**Deliverables.** Audit what `state.json` already supports before adding anything —
`exit_stats`, `recent_sessions` and the day counters may already carry more than expected.
Then add what is genuinely missing, in two shapes: **bounded windows** for anything
per-period, and **monotonic lifetime counters** for the "since installing" figures. A
counter is O(1) and does not violate §16's bounded-history rule, but it is a *new* shape in
this schema and needs its own seed and guard. Decide the `schema_version` bump and the
migration path for existing installs deliberately — an existing user must not lose their
history or hard-error on first read.

**Metric definitions are the real work, and each one is a decision to record.** Three that
are already load-bearing and easy to get wrong:

- **"Automatic opens interrupted"** must mean *actually interrupted*. Since Phase 10, an
  open inside the Circle 0 silent band is **observed, not interrupted** — nothing is shown.
  Counting silent-band opens as interruptions would inflate the headline number and turn
  the receipt into the self-congratulatory telemetry §29's voice forbids. Define it against
  what the user actually saw.

- **"Most effective exit"** needs an effectiveness definition and a confidence floor.
  `select_exit()` already exploits lowest average return-time and already refuses to exploit
  below `exits.exploit_min_observations` (10). Reuse that threshold: do not name a winner
  from two samples.

- **"Contracts kept"** already exists as contract outcome feeding Heat — confirm it is
  recorded losslessly enough to report as a ratio, not just as a Heat delta.

**Estimates are governed by §24 and are deliberately out of scope here.** Observed metrics
may be stated directly. Any *estimated* attention reclaimed must be labelled an estimate,
use a **personal rolling-median counterfactual baseline** rather than a global assumption,
and be lower-bounded at zero. `100 blocked opens = X hours saved` is **explicitly
forbidden** without evidence. Ship observed metrics first; the estimate is its own decision.

Source: **SEED-004** (VALUE / LIFE RETURNED), whose trigger condition — "after the device-UAT
backlog closes and state-shape discipline is settled" — this phase's position honours.

**Severity:** major
**Requirements**: VAL-01, VAL-02, STATE-12, SESS-07, SAFE-01
**Depends on:** Phase 12
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 22 to break down)

### Phase 23: The Attention Receipt

**Goal:** Build the **Attention Receipt**: a separate, local, disposable Note the user asks for and
PROSOCHĒ regenerates from `state.json` each time. Daily, 7-day, and lifetime views. It is
the artifact a person might genuinely screenshot and send to someone.

**Shape.** A distinct Note from the Control Room — the Control Room is durable and
returned-to; the receipt is disposable and regenerated. Never accumulate receipts; regenerate
one. Three cadences sharing one generator: `ATTENTION RECEIPT` + date, `7 DAYS OF ATTENTION`,
`SINCE INSTALLING PROSOCHĒ`. Ends with `Spend your attention on purpose.` and two options,
Share and Done.

**It names the Circle in the Dante vocabulary** — `PEAK DEPTH — CIRCLE VII` — which is what
makes it shareable in a way "4h12m screen time" is not. **Depends on Phase 11**, which
settles those names; authoring receipt copy before the rename would mean writing it twice.

**The design risk that must not be waved through: this inverts the incentive.**
"How deep do you go?" is strong as a hook, and *I hit Circle VI today* is real social
currency — but the product's entire purpose is that you **don't**. Peak Circle VII is a bad
day. If the receipt renders depth as achievement, the user who wants an interesting receipt
is the user who wants to fail more, and the mechanism quietly starts working against its own
goal. SEED-004 already fixes the frame: **it is a receipt, not a scoreboard — no streaks, no
scores, no shame.** A receipt records what something cost. Render peak depth as a fact and
let it read as a confession, never as a trophy or a high score, and never with a
congratulatory verb.

**Sharing exports behavioural data by design, so the receipt's content is a privacy
surface.** Generating locally preserves §27 for *generation*, but a shared screenshot is
published. Therefore: **no app names, no timestamps, nothing that fingerprints a routine**.
The mock this phase derives from is already clean on that — keep it that way, and treat any
proposed field against the question "would the user knowingly publish this?"

**The receipt must carry its own provenance** — what made it and where to get it — because it
is the distribution artifact. That is a hard requirement, not decoration, and it is the same
attribution question **SEED-008** raises. Keep it quiet and factual: a name and a source, not
a watermark or an ad.

**Honesty rules inherited from §24 and Phase 22.** Only observed metrics unless an estimate
is explicitly labelled and personally baselined. Suppress any figure not yet supported by
enough observations rather than printing a confident-looking number — a receipt that
overclaims once is never trusted again.

**Never shown while the user is being blocked.** An intervention is not a surface for
displaying value (§25).

Source: **SEED-004**'s second deliverable.

**Severity:** major
**Requirements**: VAL-03, VAL-04, ROOM-04, ROOM-05, CIRC-01, DIST-04
**Depends on:** Phase 22
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 23 to break down)

### Phase 24: Impact and reciprocity — sharing, then support

**Goal:** Turn the receipt into the two loops that let PROSOCHĒ spread and sustain itself — **sharing
first, support second** — without an account, a referral scheme, or a tracker.

**Impact loop, after meaningful value:** *Someone you care about might want some of this time
back too.* → Share PROSOCHĒ. No incentive, no tracking, no credit. **Reciprocity loop,
later:** *PROSOCHĒ has helped you interrupt 500 automatic openings. It's free forever. If it
has been worth something, pay what you think it was worth.* Same local evidence, different
moment. **That order is the design** — sharing before payment states the project's priorities
without having to claim them.

**Growth is decentralised by construction.** Person A's copy helps them; they send a link;
Person B downloads their own copy. No centralised ecosystem mediates the relationship, and
there is no account to create. That is what earns the line *not another app* — and its
stronger form: **no account, no feed, no subscription, not even an app.**

**Never "refer a friend."** No referral credits, no incentive of any kind. The recommendation
must stay uncorrupted by benefit to the recommender — that absence is precisely what makes it
credible, and it is worth protecting as a product property rather than treating as a missing
feature.

**§25's four prohibitions are absolute:** never display the payment ask while the user is
being blocked; never use guilt; never threaten loss of functionality; **never transmit
attention history** — the trigger threshold is computed locally and the user only ever
*chooses* to open a link. The ask is three options — Support / Not now / Never ask again —
persisted with a build guard, and `Never ask again` must be permanent and honoured.

**Blocked on a decision outside this phase: the licence.** *Pay what you think it was worth*
presumes the author can be paid for value others derive, and the project is currently **MIT
licensed on a public repo** — which grants commercial use and forks with no royalty and no
product-facing attribution, irrevocably for everything already published. A voluntary
tip-jar is compatible with MIT; anything stronger is not. **SEED-008** holds that analysis and
the option map. Settle it before shipping a payment surface, and settle the outbound
destination with the project owner rather than assuming one.

**Removal must stay clean.** The product must remain forkable, so the whole support path
should come out behind a single generator toggle.

Source: **SEED-003** (low-salience support path), whose trigger — "after SEED-004 ships,
because pay-after-value is meaningless with no value display" — this phase's position
honours.

**Successor:** the marketing and distribution phase, which uses shared receipts as its
primary material. Not yet added — add it when the receipt's actual shape is known, rather
than designing the campaign against a mock.

**Severity:** major
**Requirements**: PAY-01, PAY-02, DIST-04, DIST-05, DIST-06, ROOM-04
**Depends on:** Phase 23
**Plans:** 0 plans

Plans:

- [ ] TBD (run /gsd-plan-phase 24 to break down)
