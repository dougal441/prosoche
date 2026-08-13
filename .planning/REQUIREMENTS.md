# Requirements: PROSOCHĒ — Nine Circles

**Defined:** 2026-08-13
**Core Value:** When a user automatically reaches for a target app, PROSOCHĒ interrupts strongly enough that the user makes an actual choice — and the strength of that interruption adapts to their own recent behaviour.

## v1 Requirements

Requirements for the initial release: two importable, signed Shortcuts (Dumb and Sentient) plus retained unsigned XML source. Each maps to exactly one roadmap phase.

### Capability Audit (AUDIT)

The canonical strategy forbids fabricating an action because the strategy asks for it. These requirements make verification an explicit deliverable.

- [x] **AUDIT-01**: Every iOS action the build depends on is resolved to VERIFIED / UNVERIFIED / NOT AVAILABLE with its exact identifier and parameter shape, recorded in a build-notes document
- [x] **AUDIT-02**: Grayscale / Color Filters capability is resolved to a go/no-go decision, and the Ash primitive has a documented fallback design if no safe action exists
- [x] **AUDIT-03**: Brightness read-back capability is resolved; if no safe read path exists, Dimming is specified to degrade to a non-stateful variant rather than making an unrestorable change
- [x] **AUDIT-04**: Volume read-back capability is resolved; if no safe read path exists, Silence is specified to degrade to a non-stateful variant
- [x] **AUDIT-05**: Notes actions (Create Note, Append to Note, find/show a Note) are confirmed usable on the iOS target, since the Control Room is the only onboarding path
- [x] **AUDIT-06**: The `Use Model` On-Device selection literal is recovered by round-trip (select On-Device in Shortcuts, export unsigned XML, read the literal back) and recorded verbatim, OR the Sentient fork's On-Device guarantee is explicitly re-planned
- [x] **AUDIT-07**: Every deviation from the canonical strategy forced by an unverifiable action is recorded with the fallback taken, and the Shortcut remains runnable
- [x] **AUDIT-08**: Static configuration (profile threshold tables, sequence orderings, Ice cooldown durations, Heat coefficients) exists as a single editable block so prototype parameters can be tuned without restructuring the graph

### Routing & Bootstrap (BOOT)

- [x] **BOOT-01**: The Shortcut routes correctly on manual run (no input), `OPEN` input, and `CLOSE` input, using iOS-26-compatible nested If/Otherwise rather than macOS-only Otherwise-If
- [x] **BOOT-02**: Unrecognised or empty input fails safe — the Shortcut does not corrupt state and does not hang
- [x] **BOOT-03**: First manual run creates `state.json` with initial profile, fork, and config values from the import questions
- [x] **BOOT-04**: First manual run creates exactly one `PROSOCHĒ — Control Room` Note with a non-empty body
- [ ] **BOOT-05**: Later manual runs never overwrite existing state or create a duplicate Control Room Note
- [ ] **BOOT-06**: Missing `state.json` triggers self-healing bootstrap rather than failure, from any invocation mode
- [ ] **BOOT-07**: Corrupt or unparseable `state.json` triggers safe recovery rather than failure or silent wrong behaviour
- [ ] **BOOT-08**: A deleted Control Room Note is detected and safely recreated without crashing the run
- [x] **BOOT-09**: Import questions capture descent profile (Paradise/Limbo/Inferno, default Limbo) and voice permission; the Sentient fork additionally captures the on-device intelligence preference

### State Engine (STATE)

- [ ] **STATE-01**: Behavioural day is computed as current date minus 4 hours and stored as a date key
- [ ] **STATE-02**: Behavioural-day rollover resets `opens_today` and Gravity, and does not reset Heat, recent sessions, or exit statistics
- [ ] **STATE-03**: Heat decays with time since the last genuine target-app interaction
- [ ] **STATE-04**: A genuine OPEN increments Heat, with additional Heat for rapid reopening
- [ ] **STATE-05**: Heat is adjusted by the previous contract's outcome — increased on substantial overrun, decreased when the boundary was respected
- [ ] **STATE-06**: Heat is clamped to its floor and cap
- [ ] **STATE-07**: Gravity accumulates from the day's open count and is capped
- [ ] **STATE-08**: Pressure is computed as Heat plus Gravity
- [ ] **STATE-09**: Pressure maps to a Circle via the active profile's threshold table, using ordered comparisons rather than equality
- [ ] **STATE-10**: All three profiles produce demonstrably different Circles for the same Pressure value
- [ ] **STATE-11**: Duplicate OPEN events from a single user action are debounced and increment the open count only once
- [x] **STATE-12**: State is persisted as a bounded, versioned JSON document with rolling windows for sessions, contracts, and per-exit aggregates — no unbounded arrays, no CSV

### Session Measurement (SESS)

- [ ] **SESS-01**: Each OPEN creates a session with a unique ID and start timestamp recorded in state
- [ ] **SESS-02**: CLOSE measures actual session duration from the recorded start timestamp
- [ ] **SESS-03**: CLOSE reloads state and aborts without mutating it if a newer OPEN owns the active session
- [ ] **SESS-04**: Rapid switching between two tracked apps does not corrupt state or produce a phantom session
- [ ] **SESS-05**: CLOSE compares actual duration against the declared contract and records the overrun
- [ ] **SESS-06**: CLOSE clears the active session and appends the completed session to the rolling window
- [ ] **SESS-07**: CLOSE restores any environmental setting PROSOCHĒ itself changed during the session

### Circles & Primitives (CIRC)

- [ ] **CIRC-01**: The Knock shows a brief, non-lecturing interruption carrying real telemetry
- [ ] **CIRC-02**: Ash applies the audited visual-salience reduction, or its documented fallback if no safe action exists
- [ ] **CIRC-03**: Silence reduces media audio only when the original value can be captured and restored, otherwise degrades safely
- [ ] **CIRC-04**: Confession asks for a free-text intention and then a time boundary (2/5/10/15/custom)
- [ ] **CIRC-05**: Dimming reduces brightness only when reversible, never to zero, otherwise degrades safely
- [ ] **CIRC-06**: Exile immediately routes to an exit without a permission prompt, and returning remains possible as an affirmative act
- [ ] **CIRC-07**: The Mirror shows a precise behavioural reflection built only from recorded facts
- [ ] **CIRC-08**: The Voice speaks the Mirror at most once per run, only when voice is enabled, never at unsafe levels
- [ ] **CIRC-09**: Ice applies a deterministic cooldown whose duration varies by profile, decided entirely without the model
- [ ] **CIRC-10**: During Ice, a target-app OPEN immediately ejects or redirects, and remaining cooldown is shown where practical
- [ ] **CIRC-11**: Blocked attempts during Ice do not endlessly inflate Heat
- [ ] **CIRC-12**: Ice always expires, granting Heat relief and clearing the cooldown — the user is never permanently trapped
- [ ] **CIRC-13**: All three sequences (Classic default, Black Mirror, Ambient) are selectable and change which primitives each Circle invokes, including combined primitives
- [ ] **CIRC-14**: A stronger Circle does not necessarily replay every weaker Circle's prompt

### Contracts (CONT)

- [ ] **CONT-01**: A free-text intention of any wording is accepted, including deliberate leisure such as "watch stupid videos"
- [ ] **CONT-02**: A time boundary is selectable from presets or entered as a custom value
- [ ] **CONT-03**: A kept contract is recorded as respected
- [ ] **CONT-04**: An exceeded contract is recorded with its overrun magnitude
- [ ] **CONT-05**: Recorded contract outcomes are available to the next OPEN's Heat calculation
- [ ] **CONT-06**: A time-overrun message is never shown when no contract existed

### Exits (EXIT)

- [ ] **EXIT-01**: Capture routes to an idea-externalising target (notes, voice memo, or camera)
- [ ] **EXIT-02**: Coordinate routes to a planning target (reminders, calendar, or task list)
- [ ] **EXIT-03**: Create routes to a user-defined making target
- [ ] **EXIT-04**: Connect routes to a direct human-contact tool without initiating contact on the user's behalf
- [ ] **EXIT-05**: Consult asks what the user is trying to find and provides at least a direct query-shaped search route, with a menu covering web, maps, notes, reminders, and calendar
- [ ] **EXIT-06**: Close returns the user off the phone — home or lock — and is treated as a first-class outcome, not a fallback
- [ ] **EXIT-07**: Leaving is always available at every Circle; the user is never forced to complete an intervention to exit
- [ ] **EXIT-08**: Exits the user has disabled are never selected
- [ ] **EXIT-09**: Each exit use is recorded with its type, timestamp, triggering app, Circle, and Heat

### Exit Learning (LEARN)

- [ ] **LEARN-01**: Time until the next tracked-app OPEN after an exit is measured and recorded as that exit's outcome
- [ ] **LEARN-02**: With few observations, exits rotate roughly evenly across the user's enabled exits
- [ ] **LEARN-03**: With sufficient observations, exits associated with longer time away are preferred, with occasional exploration
- [ ] **LEARN-04**: The exploration rate is a configuration value, not a hardcoded constant
- [ ] **LEARN-05**: Exit selection is computed deterministically and never delegated to the model

### Control Room (ROOM)

- [x] **ROOM-01**: The Note opens with READ THIS FIRST explaining what PROSOCHĒ is and how to create both automations
- [x] **ROOM-02**: The Note gives exact steps for Automation A (App / selected apps / Is Opened / run automatically / Run Shortcut / pass input `OPEN`)
- [x] **ROOM-03**: The Note gives exact steps for Automation B (same apps / Is Closed / run automatically / Run Shortcut / pass input `CLOSE`)
- [x] **ROOM-04**: The Note states plainly that the Shortcut cannot install these automations itself and that PROSOCHĒ is bypassable
- [x] **ROOM-05**: The Note carries the safety warning not to target Phone, Maps, Wallet, authenticators, password managers, or other essential apps
- [x] **ROOM-06**: The Note contains the editable MY PHONE, ON PURPOSE proforma with all its prompts
- [ ] **ROOM-07**: The Note shows current settings — fork, profile, sequence, voice, AI, enabled exits
- [ ] **ROOM-08**: The Note shows a human-readable current-state snapshot refreshed on manual run
- [ ] **ROOM-09**: The Attention Ledger records meaningful events only — Circle changes, contracts, redirects, rapid-return clusters, cool-downs, profile changes — not every internal calculation
- [ ] **ROOM-10**: The manual menu offers Status, Open Control Room, Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today, and Emergency Restore
- [ ] **ROOM-11**: Sync My Profile extracts the human proforma from the Note into state, and the OPEN path never parses the Note
- [ ] **ROOM-12**: Test a Circle runs any chosen Circle's behaviour without altering real Pressure

### Safety & Restoration (SAFE)

- [ ] **SAFE-01**: Brightness is never set to zero
- [ ] **SAFE-02**: Volume is never increased and no startling output is produced
- [ ] **SAFE-03**: Any environmental setting whose original value cannot be captured is left unchanged rather than changed unrestorably
- [ ] **SAFE-04**: Pre-existing accessibility configuration is never blindly overridden
- [ ] **SAFE-05**: Emergency Restore clears cooldown, clears the active session, and restores recoverable brightness, volume, and colour settings
- [ ] **SAFE-06**: Emergency Restore is reachable even while in Ice

### Dumb Fork (DUMB)

- [ ] **DUMB-01**: The Dumb fork has no Apple Intelligence dependency and runs fully on non-Apple-Intelligence iOS 26 iPhones
- [ ] **DUMB-02**: At least 30 Mirror templates exist and none invents a fact
- [ ] **DUMB-03**: Template selection is gated on which facts are actually available, producing no malformed or empty telemetry messages
- [ ] **DUMB-04**: Consult without a model offers Search Web, Search Maps, Open Notes, Open Reminders, Open Calendar, and Back
- [ ] **DUMB-05**: The intent gate accepts a blank or vague response without attempting to judge sincerity
- [ ] **DUMB-06**: Mirror output acknowledges success as well as lapses, so opening a target app does not always produce criticism

### Sentient Fork (SENT)

- [ ] **SENT-01**: The Sentient fork uses the Apple On-Device model only, with no cloud, no Private Cloud Compute, and no ChatGPT path
- [ ] **SENT-02**: The model is invoked across Circles II–VIII with increasing involvement, while Circle I stays fast and deterministic
- [ ] **SENT-03**: Circle IX invokes no model and remains fully deterministic
- [ ] **SENT-04**: Model output is structured as ALLOW, CHALLENGE, or DENY, and is parsed and validated
- [ ] **SENT-05**: Malformed, empty, or slow model output falls back to the deterministic Dumb behaviour without breaking the run
- [ ] **SENT-06**: At most one challenge round occurs — no interrogation loop
- [ ] **SENT-07**: DENY is available only at sufficiently high Circles and means redirect, never system-level punishment
- [ ] **SENT-08**: The model audits contracts on specificity, boundedness, and consistency, and never asserts the user is lying
- [ ] **SENT-09**: The model never claims to know what happened inside an app or what the user felt
- [ ] **SENT-10**: A clearly bounded deliberate-leisure contract can receive ALLOW
- [ ] **SENT-11**: Prior contract consistency can inform a challenge, using only recorded behavioural facts
- [ ] **SENT-12**: The model never controls Heat, Gravity, Pressure, thresholds, timers, exit selection, or Ice
- [ ] **SENT-13**: The model receives only a compact local context window, never the whole Note, and no behavioural data leaves the device
- [ ] **SENT-14**: The system instruction enforces the required tone and forbids the banned vocabulary and diagnosis language
- [ ] **SENT-15**: The Sentient fork adds no changes to the deterministic state engine inherited from Dumb

### Distribution (DIST)

- [ ] **DIST-01**: Both forks pass the Shortcuts Playground validator at the iOS 26 target
- [ ] **DIST-02**: Both forks sign successfully into importable `.shortcut` files
- [ ] **DIST-03**: Both forks import onto a real iPhone and complete a first manual run
- [ ] **DIST-04**: The two forks are named unambiguously and distinguishable at import
- [ ] **DIST-05**: Unsigned XML source is retained in the repository for both forks
- [ ] **DIST-06**: Build notes document unsupported actions, deviations, fallbacks taken, and known iOS limitations
- [ ] **DIST-07**: Repository documentation states plainly that data stays on-device, there is no external analytics, model output can be wrong, and the system is self-directed and bypassable
- [ ] **DIST-08**: Core functionality has no external network dependency

## v2 Requirements

Deferred to a future release. Tracked but not in the current roadmap.

### Contextual Learning

- **CTX-01**: Exit success is conditioned on time of day
- **CTX-02**: Exit success is conditioned on weekday versus weekend
- **CTX-03**: Exit success is conditioned on target app and current Circle
- **CTX-04**: Exit success is conditioned on the declared intention category

### Value Measurement

- **VAL-01**: `Get App & Website Data` schema and runtime granularity are audited on a real iPhone
- **VAL-02**: Personal counterfactual baselines are computed from rolling personal medians
- **VAL-03**: Estimated Attention Reclaimed is displayed, always labelled as an estimate
- **VAL-04**: Daily and weekly summaries are written to the Note

### Sentient Optimisation

- **OPT-01**: The next likely Mirror is precomputed on CLOSE and cached in state
- **OPT-02**: A cached Mirror is shown immediately on the next OPEN and updated with deterministic facts

### Support

- **PAY-01**: A local milestone triggers a pay-after-value prompt, never during an intervention
- **PAY-02**: The prompt offers Support, Not now, and Never ask again, with no functionality gate

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Focus modes | Explored and deliberately removed from v1; not required for the Nine Circles engine |
| NFC / physical commitment tokens | Deliberately removed from v1; possible future physical-separation extension |
| Screen Time blocking APIs (FamilyControls / ManagedSettings / DeviceActivity) | PROSOCHĒ is a behavioural intervention, not a secure parental-control system |
| Companion iOS app | Would contradict the native-Shortcut-only premise and the free/open-source distribution model |
| CSV or any second machine store | One JSON for machine state, one Note for human history — a document store is not a transactional key-value store |
| ChatGPT, Private Cloud Compute, arbitrary web APIs, analytics services | Sentient is On-Device only; no behavioural data may leave the phone |
| Remote A/B testing infrastructure | Sequences are switchable locally for manual comparison; a remote experimentation platform is out of scope |
| Tamper-proofing or bypass prevention | The user can always disable the Personal Automation; the product must never claim otherwise |
| Model control of arithmetic, thresholds, timers, or Circle IX | Generative output varies; safety and state decisions must stay deterministic |
| Lie detection or addiction diagnosis | The model cannot observe in-app content or mental state; contract auditing replaces it |
| Therapy-intake onboarding or long survey | Import questions stay minimal; richer profile lives in the editable Note |

## Traceability

Which phases cover which requirements. Populated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUDIT-01 | Phase 1 | Complete |
| AUDIT-02 | Phase 1 | Complete |
| AUDIT-03 | Phase 1 | Complete |
| AUDIT-04 | Phase 1 | Complete |
| AUDIT-05 | Phase 1 | Complete |
| AUDIT-06 | Phase 1 | Complete |
| AUDIT-07 | Phase 1 | Complete |
| AUDIT-08 | Phase 1 | Complete |
| BOOT-01 | Phase 2 | Complete |
| BOOT-02 | Phase 2 | Complete |
| BOOT-03 | Phase 2 | Complete |
| BOOT-04 | Phase 2 | Complete |
| BOOT-05 | Phase 2 | Pending |
| BOOT-06 | Phase 2 | Pending |
| BOOT-07 | Phase 2 | Pending |
| BOOT-08 | Phase 2 | Pending |
| BOOT-09 | Phase 2 | Complete |
| STATE-12 | Phase 2 | Complete |
| ROOM-01 | Phase 2 | Complete |
| ROOM-02 | Phase 2 | Complete |
| ROOM-03 | Phase 2 | Complete |
| ROOM-04 | Phase 2 | Complete |
| ROOM-05 | Phase 2 | Complete |
| ROOM-06 | Phase 2 | Complete |
| STATE-01 | Phase 3 | Pending |
| STATE-02 | Phase 3 | Pending |
| STATE-03 | Phase 3 | Pending |
| STATE-04 | Phase 3 | Pending |
| STATE-05 | Phase 3 | Pending |
| STATE-06 | Phase 3 | Pending |
| STATE-07 | Phase 3 | Pending |
| STATE-08 | Phase 3 | Pending |
| STATE-09 | Phase 3 | Pending |
| STATE-10 | Phase 3 | Pending |
| STATE-11 | Phase 3 | Pending |
| SESS-01 | Phase 4 | Pending |
| SESS-02 | Phase 4 | Pending |
| SESS-03 | Phase 4 | Pending |
| SESS-04 | Phase 4 | Pending |
| SESS-05 | Phase 4 | Pending |
| SESS-06 | Phase 4 | Pending |
| SESS-07 | Phase 4 | Pending |
| CIRC-01 | Phase 5 | Pending |
| CIRC-02 | Phase 5 | Pending |
| CIRC-03 | Phase 5 | Pending |
| CIRC-04 | Phase 5 | Pending |
| CIRC-05 | Phase 5 | Pending |
| CIRC-06 | Phase 5 | Pending |
| CIRC-07 | Phase 5 | Pending |
| CIRC-08 | Phase 5 | Pending |
| CIRC-09 | Phase 5 | Pending |
| CIRC-10 | Phase 5 | Pending |
| CIRC-11 | Phase 5 | Pending |
| CIRC-12 | Phase 5 | Pending |
| CIRC-13 | Phase 5 | Pending |
| CIRC-14 | Phase 5 | Pending |
| SAFE-01 | Phase 5 | Pending |
| SAFE-02 | Phase 5 | Pending |
| SAFE-03 | Phase 5 | Pending |
| SAFE-04 | Phase 5 | Pending |
| SAFE-05 | Phase 5 | Pending |
| SAFE-06 | Phase 5 | Pending |
| EXIT-01 | Phase 6 | Pending |
| EXIT-02 | Phase 6 | Pending |
| EXIT-03 | Phase 6 | Pending |
| EXIT-04 | Phase 6 | Pending |
| EXIT-05 | Phase 6 | Pending |
| EXIT-06 | Phase 6 | Pending |
| EXIT-07 | Phase 6 | Pending |
| EXIT-08 | Phase 6 | Pending |
| EXIT-09 | Phase 6 | Pending |
| LEARN-01 | Phase 6 | Pending |
| LEARN-02 | Phase 6 | Pending |
| LEARN-03 | Phase 6 | Pending |
| LEARN-04 | Phase 6 | Pending |
| LEARN-05 | Phase 6 | Pending |
| CONT-01 | Phase 6 | Pending |
| CONT-02 | Phase 6 | Pending |
| CONT-03 | Phase 6 | Pending |
| CONT-04 | Phase 6 | Pending |
| CONT-05 | Phase 6 | Pending |
| CONT-06 | Phase 6 | Pending |
| ROOM-07 | Phase 7 | Pending |
| ROOM-08 | Phase 7 | Pending |
| ROOM-09 | Phase 7 | Pending |
| ROOM-10 | Phase 7 | Pending |
| ROOM-11 | Phase 7 | Pending |
| ROOM-12 | Phase 7 | Pending |
| DUMB-01 | Phase 7 | Pending |
| DUMB-02 | Phase 7 | Pending |
| DUMB-03 | Phase 7 | Pending |
| DUMB-04 | Phase 7 | Pending |
| DUMB-05 | Phase 7 | Pending |
| DUMB-06 | Phase 7 | Pending |
| SENT-01 | Phase 8 | Pending |
| SENT-02 | Phase 8 | Pending |
| SENT-03 | Phase 8 | Pending |
| SENT-04 | Phase 8 | Pending |
| SENT-05 | Phase 8 | Pending |
| SENT-06 | Phase 8 | Pending |
| SENT-07 | Phase 8 | Pending |
| SENT-08 | Phase 8 | Pending |
| SENT-09 | Phase 8 | Pending |
| SENT-10 | Phase 8 | Pending |
| SENT-11 | Phase 8 | Pending |
| SENT-12 | Phase 8 | Pending |
| SENT-13 | Phase 8 | Pending |
| SENT-14 | Phase 8 | Pending |
| SENT-15 | Phase 8 | Pending |
| DIST-01 | Phase 8 | Pending |
| DIST-02 | Phase 8 | Pending |
| DIST-03 | Phase 8 | Pending |
| DIST-04 | Phase 8 | Pending |
| DIST-05 | Phase 8 | Pending |
| DIST-06 | Phase 8 | Pending |
| DIST-07 | Phase 8 | Pending |
| DIST-08 | Phase 8 | Pending |

**Coverage:**

- v1 requirements: 117 total
- Mapped to phases: 117
- Unmapped: 0 ✓

---
*Requirements defined: 2026-08-13*
*Last updated: 2026-08-13 after roadmap creation (8 phases, full coverage)*
