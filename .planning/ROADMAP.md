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

**Plans:** 1/1 plans executed

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
| 4. CLOSE Pipeline & Session Race Protocol | 1/1 | Complete | 2026-08-13 |
| 5. Nine Primitives & Environmental Safety | 3/3 | Complete | 2026-08-13 |
| 6. Exits, Exit Learning & Contracts | 3/3 | Complete | 2026-08-13 |
| 7. Control Room Manual Menu, Dumb Mirror Engine & Dumb Freeze | 1/1 light | Human needed | - |
| 8. Sentient Fork & Dual Distribution | 3/3 | Human needed | - |
