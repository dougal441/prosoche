# Requirements: PROSOCHĒ — Nine Circles

**Defined:** 2026-08-13
**Re-founded:** 2026-08-19 on canonical strategy v2 (the covenant model). The v1 requirement families below are the delivered foundation — built, structurally verified, and carried forward; rows whose meaning changes under v2 carry an explicit `v2:` pointer. The new covenant families (COV, VERD, BAND, PERS, VARY, MET) define the conversion. v1 requirement IDs are stable so historical phase records remain resolvable.
**Core Value:** When use is intentional, PROSOCHĒ is invisible. When intention disappears, it interrupts exactly strongly enough to restore it — and an honest declaration buys back the silence.

## Delivered Foundation (v1 families, built)

### Capability Audit (AUDIT)

- [x] **AUDIT-01**: Every iOS action the build depends on is resolved to VERIFIED / UNVERIFIED / NOT AVAILABLE with its exact identifier and parameter shape, recorded in `docs/BUILD-NOTES.md`
- [x] **AUDIT-02**: Grayscale / Color Filters resolved — the iOS `AX*` intent is donor-confirmed and shipped (BD-01-R2); the kill switch `safety.ash_managed_color_filters` is the §21-lineage opt-in
- [x] **AUDIT-03**: Brightness read-back resolved; the stateful capture-and-restore path ships with a non-stateful per-run fallback; guarded by `docs/environmental_restore_check.py`
- [x] **AUDIT-04**: Volume read-back resolved; same shape as AUDIT-03
- [x] **AUDIT-05**: Notes actions confirmed usable on the iOS target
- [x] **AUDIT-06**: The `Use Model` On-Device literal recovered by device round-trip and pinned (`Apple Intelligence on Device`, BD-04-R2)
- [x] **AUDIT-07**: Every deviation forced by an unverifiable action is recorded with the fallback taken, Shortcut kept runnable
- [x] **AUDIT-08**: Static configuration exists as a single editable Config block

### Routing & Bootstrap (BOOT)

- [x] **BOOT-01**: Manual / `OPEN` / `CLOSE` routing via iOS-26-compatible nested If/Otherwise
- [x] **BOOT-02**: Unrecognised or empty input fails safe
- [x] **BOOT-03**: First manual run creates `state.json` from import-question values
- [x] **BOOT-04**: First manual run creates exactly one `PROSOCHĒ` Note with a non-empty body
- [x] **BOOT-05**: Later manual runs never overwrite state or duplicate the Note
- [x] **BOOT-06**: Missing `state.json` triggers self-healing bootstrap from any mode
- [x] **BOOT-07**: Corrupt `state.json` triggers safe recovery
- [x] **BOOT-08**: A deleted Note is detected and safely recreated
- [x] **BOOT-09**: Import questions capture profile and voice permission (Aware adds the AI preference) — *v2: the profile question becomes the plain-language severity question and a modality question is added; see PERS-01/02*

### State Engine (STATE)

- [x] **STATE-01**: Behavioural day = current date − 4h, stored as a date key
- [x] **STATE-02**: Rollover resets `opens_today` and Gravity; Heat, sessions, and exit stats survive
- [x] **STATE-03**: Heat decays with time since last genuine interaction
- [x] **STATE-04**: A genuine OPEN increments Heat with rapid-reopen bonuses — *v2: a covered reopen earns no rapid-return bonus; see COV-08*
- [x] **STATE-05**: Heat adjusts on the previous contract's outcome
- [x] **STATE-06**: Heat clamps to floor and cap
- [x] **STATE-07**: Gravity accumulates from the day's opens, capped
- [x] **STATE-08**: Pressure = Heat + Gravity
- [x] **STATE-09**: Pressure maps to a Circle via the profile's ascending threshold table, ordered comparisons only
- [x] **STATE-10**: All three profiles produce demonstrably different Circles for the same Pressure
- [x] **STATE-11**: Duplicate OPEN events debounce to one increment
- [x] **STATE-12**: Bounded, versioned JSON state — rolling windows, no unbounded arrays, no CSV

### Session Measurement (SESS)

- [x] **SESS-01**: Each OPEN creates a session with unique ID and start timestamp
- [x] **SESS-02**: CLOSE measures actual duration from that start
- [x] **SESS-03**: CLOSE reloads state and aborts if a newer OPEN owns the session
- [x] **SESS-04**: Rapid switching between tracked apps never corrupts state
- [x] **SESS-05**: CLOSE compares duration against the declared contract and records overrun — *v2: per-window accounting; see COV-06*
- [x] **SESS-06**: CLOSE clears the session and appends it to the rolling window
- [x] **SESS-07**: CLOSE restores every environmental setting PROSOCHĒ changed (`restore_managed_settings()`, guarded)

### Circles & Primitives (CIRC)

- [x] **CIRC-01**: Pause shows a brief, non-lecturing interruption carrying real telemetry — *v2: gains a small rotating copy bank (VARY-01)*
- [x] **CIRC-02**: Black and White applies the real Color Filters toggle with the unconditional off-leg at all four recovery paths
- [x] **CIRC-03**: Silence reduces media audio only when the original is captured and durably persisted, else degrades safely
- [x] **CIRC-04**: Intention asks for a free-text purpose and then a time boundary (2/5/10/15/custom) — *v2: the boundary is mandatory with a config default; the verdict routes the encounter (VERD-01); coverage begins on ALLOW (COV-01)*
- [x] **CIRC-05**: Dim reduces brightness only when the original is captured and durably persisted, else degrades safely — *v2: Dim is Band B soft friction, Ambient sequence only until device-proven; Blackout is parked (BAND-06)*
- [x] **CIRC-06**: Eject routes immediately without a permission prompt; returning stays possible as an affirmative act — *v2: Eject is Circle 7; Redirect (routed Exile) is built at Circle 6 per BAND-06*
- [x] **CIRC-07**: The Mirror shows a precise behavioural reflection built only from recorded facts — *v2: moves to Circle 5 with the three-route surface (BAND-05)*
- [x] **CIRC-08**: Loud Mirror speaks the reflection at most once per run, only with voice enabled, never at unsafe levels
- [x] **CIRC-09**: Frozen applies a deterministic cooldown varying by profile, decided entirely without the model
- [x] **CIRC-10**: During Frozen, a tracked OPEN immediately ejects/redirects with remaining cooldown shown where practical
- [x] **CIRC-11**: Blocked attempts during Frozen do not endlessly inflate Heat
- [x] **CIRC-12**: Frozen always expires, granting Heat relief — the user is never trapped
- [x] **CIRC-13**: Sequences are selectable and change which primitive each Circle fires — *v2: three band-invariant sequences per the BD-09 slot table; combined entries stay abolished (BAND-06)*
- [x] **CIRC-14**: A deeper Circle does not replay every shallower Circle's prompt

### Contracts (CONT)

- [x] **CONT-01**: A free-text intention of any wording is accepted, including deliberate leisure
- [x] **CONT-02**: A time boundary is selectable from presets or custom — *v2: mandatory, with `contract.default_boundary_minutes` on skip (COV-03)*
- [x] **CONT-03**: A kept contract is recorded as respected
- [x] **CONT-04**: An exceeded contract is recorded with its overrun magnitude
- [x] **CONT-05**: Recorded outcomes feed the next OPEN's Heat — *v2: and the verdict history (VERD-02)*
- [x] **CONT-06**: A time-overrun message is never shown when no contract existed

### Exits (EXIT)

- [x] **EXIT-01**: Capture routes to an idea-externalising target
- [x] **EXIT-02**: Coordinate routes to a planning target
- [x] **EXIT-03**: Create routes to a user-defined making target
- [x] **EXIT-04**: Connect routes to a direct human-contact tool without initiating contact
- [x] **EXIT-05**: Consult provides a direct query-shaped search route (web/maps/notes/reminders/calendar in Core)
- [x] **EXIT-06**: Close returns the user off the phone — home or lock — as a first-class outcome
- [x] **EXIT-07**: Leaving is always available at every Circle — *v2: superseded in mechanism by BAND-04 (the leave affordance lives inside each interactive surface; Band B has no dialog to leave and Band D's moves are the leave); the principle — never forced to complete an intervention — stands*
- [x] **EXIT-08**: Disabled exits are never selected *(known open defect F-18/G-06-12: `enabled_exits()` currently filters nothing — fix owned by Phase 17)*
- [x] **EXIT-09**: Each exit use is recorded with type, timestamp, app, Circle, Heat

### Exit Learning (LEARN)

- [x] **LEARN-01**: Time to next tracked OPEN is each exit's recorded outcome
- [x] **LEARN-02**: Few observations → roughly even rotation across enabled exits
- [x] **LEARN-03**: Sufficient observations → longer-time-away exits preferred, with exploration
- [x] **LEARN-04**: Exploration rate is a Config value
- [x] **LEARN-05**: Exit selection is deterministic, never the model's

### Control Room (ROOM)

- [x] **ROOM-01..06**: The `PROSOCHĒ` Note opens with READ THIS FIRST, exact steps for both automations, the cannot-self-install and bypassable statements, the essential-apps warning, and the editable `MY PHONE, ON PURPOSE` proforma
- [x] **ROOM-07**: The Note shows current settings (fork, profile, sequence, voice, AI, enabled exits)
- [x] **ROOM-08**: The Note shows a human-readable state snapshot refreshed on manual run
- [x] **ROOM-09**: The Attention Ledger records meaningful events only
- [x] **ROOM-10**: The manual menu offers Status, Open Control Room, Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today, Emergency Restore, Setup Check — *v2: gains `Set an intention` (COV-07)*
- [x] **ROOM-11**: Sync My Profile is the only Note-parsing path; the OPEN path never parses the Note
- [x] **ROOM-12**: Test a Circle runs any Circle without altering real Pressure

### Safety & Restoration (SAFE)

- [x] **SAFE-01**: Brightness changes only after its original is captured **and durably persisted**, and is always restored (D-01; capture-and-restore reliability is the safety property)
- [x] **SAFE-02**: Volume is never raised and no startling output is produced
- [x] **SAFE-03**: Any setting whose original cannot be captured is left unchanged
- [x] **SAFE-04**: Pre-existing accessibility configuration is never blindly overridden (disclosure + kill switch)
- [x] **SAFE-05**: Emergency Restore clears cooldown and the active session and restores recoverable brightness, volume, and colour
- [x] **SAFE-06**: Emergency Restore is reachable even while in Frozen — and is never gated on any Note-editable setting

### Core Fork (DUMB — historical family name retained)

- [x] **DUMB-01**: Core has no Apple Intelligence dependency
- [x] **DUMB-02**: ≥30 Mirror templates, none inventing a fact
- [x] **DUMB-03**: Template selection is fact-gated; no malformed or empty telemetry
- [x] **DUMB-04**: Core Consult offers Search Web, Search Maps, Open Notes, Open Reminders, Open Calendar, Back
- [x] **DUMB-05**: The intent gate accepts blank or vague text without judging sincerity — *v2: reinforced by VERD-02 (Core's verdict is behavioural arithmetic, never text judgment)*
- [x] **DUMB-06**: Mirror output acknowledges success as well as lapses

### Aware Fork (SENT — historical family name retained)

- [x] **SENT-01**: On-Device model only; no cloud path required; PCC authorised fallback only
- [x] **SENT-02**: Model involvement scales with Circle while Circle 1 stays deterministic — *v2: the model appears only at the ask (Circles 4–6) and reflection surfaces (Mirror / Loud Mirror); never on covered opens; see VERD-03*
- [x] **SENT-03**: Circle 9 / Frozen invokes no model, ever
- [x] **SENT-04**: Output is structured ALLOW/CHALLENGE/DENY, parsed and validated — *v2: within the deterministic envelope (VERD-01)*
- [x] **SENT-05**: Malformed, empty, or slow output falls back to deterministic behaviour without breaking the run
- [x] **SENT-06**: At most one challenge round — no interrogation loop
- [x] **SENT-07**: DENY only at sufficiently deep Circles and means redirect, never punishment — *v2: DENY exists at Circle 6 only (VERD-04)*
- [x] **SENT-08**: The model audits specificity, boundedness, consistency; never asserts lying
- [x] **SENT-09**: The model never claims to know app contents or feelings
- [x] **SENT-10**: A clearly bounded deliberate-leisure contract can receive ALLOW
- [x] **SENT-11**: Prior contract consistency can inform a challenge, recorded facts only
- [x] **SENT-12**: The model never controls Heat, Gravity, Pressure, thresholds, timers, exit selection, coverage, or Frozen
- [x] **SENT-13**: The model receives only the compact context window; nothing leaves the device
- [x] **SENT-14**: The system instruction enforces tone and bans the vocabulary list
- [x] **SENT-15**: Aware adds no changes to the deterministic engine

### Distribution (DIST)

- [x] **DIST-01**: Both forks pass gate A via `docs/gate_a_residue_check.py`
- [x] **DIST-02**: Both forks sign into importable `.shortcut` files
- [ ] **DIST-03**: Both forks import onto a real iPhone and complete a first manual run — **the standing device blocker**
- [x] **DIST-04**: The two forks are named unambiguously (`— Core` / `— Aware`)
- [x] **DIST-05**: Unsigned XML source retained for both forks
- [x] **DIST-06**: Build notes document unsupported actions, deviations, fallbacks, limitations
- [x] **DIST-07**: Repository documentation states data stays on-device, no analytics, model output can be wrong, system is bypassable
- [x] **DIST-08**: Core functionality has no external network dependency
- [x] **DIST-09**: The repository LICENSE is **PolyForm Noncommercial 1.0.0** (changed from MIT 2026-08-19, not retroactive — everything published through tag `pre-covenant-overhaul` remains MIT); README and the canon state the noncommercial term plainly

## v2 Covenant Requirements

The conversion set. Each maps to exactly one roadmap phase (traceability below).

### Coverage (COV)

- [ ] **COV-01**: An open covered by a valid contract at a Circle below the ceiling shows no surface, sends no notification, makes no model call — and still runs and persists the full state engine
- [ ] **COV-02**: A contract covers a time window (`made_at` → `made_at + boundary`) across sessions, not a single session
- [ ] **COV-03**: The boundary is mandatory; declining the picker applies `contract.default_boundary_minutes` and says so in the confirmation
- [ ] **COV-04**: Coverage ends on window expiry, on opens-within-window exceeding `contract.max_opens_per_window`, or on rapid-return bonuses within the window exceeding `contract.max_rapid_returns_per_window`; the next uncovered open routes normally at its Circle
- [ ] **COV-05**: Coverage never applies at Circle ≥ `contract.coverage_ceiling_circle` (ships 7); a live cooldown always short-circuits before the coverage check
- [ ] **COV-06**: CLOSE accumulates `consumed_seconds` into the live window; settled outcomes (kept / overrun / invalidated, with magnitudes) land losslessly in `recent_contracts` and feed both Heat and the verdict history
- [ ] **COV-07**: A contract can be created voluntarily from the manual menu (`Set an intention`) with identical coverage semantics
- [ ] **COV-08**: A covered reopen earns `heat.open_base` and counts toward Gravity but earns no rapid-return bonus (`heat.covered_reopen_bonus`, PROTOTYPE INTERPRETATION)

### Verdicts (VERD)

- [ ] **VERD-01**: The verdict envelope is deterministic and identical in both forks: Circles 4–5 offer ALLOW/CHALLENGE; Circle 6 adds DENY; nothing else, anywhere
- [ ] **VERD-02**: Core's verdict is computed from recorded behaviour only (`recent_contracts` overrun/invalidation history against Config thresholds) — never from the intention's wording
- [ ] **VERD-03**: Aware's model verdict is accepted only inside the envelope; out-of-envelope, malformed, empty, or slow output silently falls back to Core's verdict; one CHALLENGE round maximum; covered opens make no model call
- [ ] **VERD-04**: DENY routes to Redirect and nothing else — no Heat surcharge, no settings change, no cooldown

### Bands & Surfaces (BAND)

- [ ] **BAND-01**: Band boundaries are fixed (0 / 1–3 / 4–6 / 7–9) and sequence-invariant; `bands.ask_entry` and `bands.rescue_entry` exist in Config (default 4 and 7) and are read, not hardcoded
- [ ] **BAND-02**: An uncovered Band B open shows no dialog — the environmental change is the whole encounter; Circle 1's single-tap Pause is the only Band B surface
- [ ] **BAND-03**: At most one interactive surface per OPEN, ever; the universal `Leaving / Continue` pre-menu is retired; no announcement precedes a primitive
- [ ] **BAND-04**: Every interactive surface carries a one-tap leave route (Panic Escape re-expressed); removing Panic Escape strips exactly those leave routes and nothing else; Emergency Restore is untouched by all of it
- [ ] **BAND-05**: The Mirror at Band C offers three routes — continue, leave, declare — and the declare route enters the ask
- [ ] **BAND-06**: The BD-09 slot table ships in three band-invariant sequences (Classic default; Frozen pinned at Circle 9; Redirect built at Circle 6; Dim in Ambient only; Blackout in no sequence); dispatch coverage remains a hard build gate

### Personalized Descent (PERS)

- [ ] **PERS-01**: The profile import question is the plain-language severity question, mapping to Paradise / Purgatory / Inferno
- [ ] **PERS-02**: A modality import question maps to the default sequence (Classic vs Ambient)
- [ ] **PERS-03**: The Note and Status name the profile and sequence in both vocabularies (the feeling chosen and the mythological name)
- [ ] **PERS-04**: Re-elicitation is possible at any time via Change Profile / Change Sequence without state loss

### Variability (VARY)

- [ ] **VARY-01**: All variability is counter-based and deterministic — persisted counters and modulo tests; `is.workflow.actions.number.random` appears nowhere in either fork
- [ ] **VARY-02**: The spot check, when armed (`variability.spot_check_interval > 0`), fires the ask in place of the slotted primitive only on eligible uncovered Band B opens at the counter interval; it ships at `0` (off)
- [ ] **VARY-03**: No variability of any kind touches Frozen, cooldown durations, coverage arithmetic, verdict envelopes, safety paths, or environmental changes; no downward Circle jumps exist
- [ ] **VARY-04**: Surface copy rotates deterministically (Pause bank; Mirror's existing template selector) so no interactive surface is lexically constant

### Covenant Metrics (MET)

- [ ] **MET-01**: Each recorded session carries whether its OPEN was covered, so covered-open share is computable from state
- [ ] **MET-02**: Surfaces-per-day is computable from recorded state (a surface counter on the day record)
- [ ] **MET-03**: Aggregates (Phase 26) define covered share, surfaces/day, and contract fidelity per canon §21 — "opens interrupted" excludes silent-band and covered opens

## v2-Later (deferred, tracked)

- **CTX-01..04**: Contextual exit learning (time of day, weekday, app, intention category)
- **VAL-01..04**: Value measurement (`Get App & Website Data` audit, personal counterfactual baselines, Estimated Attention Reclaimed, daily/weekly summaries)
- **OPT-01..02**: Aware precomputes the next Mirror on CLOSE; shown on next OPEN
- **PAY-01..02**: Pay-after-value prompt (local milestone trigger, never during an intervention; Support / Not now / Never ask again honoured permanently)
- **RE-ELICIT**: Gentle severity re-ask at the Attention Receipt moment

## Out of Scope

| Feature | Reason |
|---------|--------|
| Focus modes | Not required for the covenant engine; possible later environmental layer |
| NFC / physical commitment tokens | Future extension (SEED-001: physical unlock for Frozen) |
| Screen Time blocking APIs / companion app | Behavioural intervention, not secure access control |
| CSV or any second machine store | One JSON, one Note |
| ChatGPT, arbitrary web APIs, analytics | Different trust boundary; Aware is On-Device (PCC fallback only) |
| Remote A/B infrastructure | Sequences and knobs switch locally |
| Mid-session timers | No installable timer trigger exists; enforcement happens at the next event — never fabricate one |
| True randomness in strong interventions | Variability is deterministic; a punishment lottery breaks proportionality and trust |
| Tamper-proofing claims | Always bypassable, and the product says so |
| Model control of arithmetic, thresholds, timers, coverage, Frozen | Generative output varies; state and safety stay deterministic |
| Lie detection / addiction diagnosis / therapy intake | The model cannot observe content or minds; contract auditing replaces it |

## Traceability

| Requirement family | Phase | Status |
|-------------|-------|--------|
| AUDIT-01..08 | 1 | Complete |
| BOOT-01..09, ROOM-01..06, STATE-12 | 2 | Complete |
| STATE-01..11 | 3 | Complete |
| SESS-01..07 | 4 | Complete |
| CIRC-01..14, SAFE-01..06 | 5 (+9/10/11/14/15/16) | Complete (structural); device proof → Phase 22 |
| EXIT-01..09, LEARN-01..05, CONT-01..06 | 6 | Complete (F-18 fix → Phase 17) |
| ROOM-07..12, DUMB-01..06 | 7 | Complete |
| SENT-01..15, DIST-01..08 | 8 (+11/13/14/15/16) | Complete except DIST-03 |
| DIST-09 | Covenant overhaul (2026-08-19) | Complete |
| COV-01..08, VERD-01..02, MET-01..02 | 17 | Pending |
| BAND-01..06 | 18 | Pending |
| PERS-01..04 | 19 | Pending |
| VERD-03..04 | 20 | Pending |
| (device debug, locked-screen CLOSE) | 21 | Pending |
| (device UAT: bands, coverage, circles, environmental) | 22 | Pending |
| VARY-01..04 | 23 | Pending |
| MET-03 | 26 | Pending |

**Coverage:**

- Delivered v1 requirements: 117 (116 complete; DIST-03 pending on device access)
- v2 covenant requirements: 26 (25 pending; DIST-09 complete)
- Unmapped: 0 ✓

---
*Requirements defined: 2026-08-13; re-founded 2026-08-19 on canonical strategy v2*
