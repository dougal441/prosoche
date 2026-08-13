# Pitfalls Research: PROSOCHĒ — Nine Circles

**Domain:** Large stateful iOS 26 Shortcut implementing a behavioural intervention (Shortcuts Playground build)
**Researched:** 2026-08-13
**Confidence:** HIGH for Class A (verified against the Shortcuts Playground plugin on disk) and Class C action-availability findings (verified against the bundled ToolKit identifier lists); MEDIUM for Class B and Class D (grounded in the canonical strategy's own stated failure modes, not independently runtime-tested)

**Sources read on disk:**
`~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/{SKILL.md, BEST_PRACTICES.md, PLIST_FORMAT.md, VARIABLES.md, CONTROL_FLOW.md, ACTIONS.md, APPINTENTS.md, AUTOMATION_TRIGGERS.md, DATE_TIME.md}` and `PROSOCHE_Nine_Circles_Canonical_Strategy.md` §5, §21, §30, §31, §32.

---

## A. Shortcuts authoring pitfalls (highest priority)

These are extracted verbatim from the Shortcuts Playground plugin's own documented warnings, not invented. Playground states generated shortcuts get "roughly 90% of the way" (§5.3 of the strategy, quoting the plugin) and explicitly calls out variable and repeat-loop wiring as needing manual inspection — plist validity is necessary but not sufficient for runtime correctness.

### A1: UUID / OutputUUID wiring breaks silently

**What goes wrong:** Any action whose output is consumed later needs a `UUID` key. If it's missing, the consuming variable renders as **"Unknown"** in the Shortcuts UI rather than failing the import — this is a silent runtime defect that a plist validator can miss if it doesn't specifically check UUID→OutputUUID pairing.

**Why it happens:** PROSOCHĒ's OPEN/CLOSE handlers chain ~15-20 sequential steps (load JSON → decay Heat → increment → Gravity → Pressure → map Circle → persist), and every intermediate Text/Number/Math/Get Dictionary Value output that feeds a later step needs an explicit UUID (BEST_PRACTICES.md "Every action that will be referenced needs a UUID").

**Prevention:** After generating each handler, grep the plist for every `OutputUUID` reference and confirm a matching action `UUID` exists earlier in the same branch. Never leave a Text/Number/Math/Format Date/Get Dictionary Value output unconsumed (validator-enforced per BEST_PRACTICES.md "No unused outputs").

**Warning signs:** Any variable chip showing "Unknown" when the `.shortcut` is opened in the Shortcuts app on-device; validator passing while manual inspection shows an orphaned action.

**Phase:** Dumb state-engine build phase (OPEN/CLOSE handlers) — before first on-device import test.

### A2: Magic-variable vs named-variable (`WFTextTokenAttachment` vs `WFTextTokenString`) confusion

**What goes wrong:** Display parameters (text actually shown to the user — Show Alert message/title, Notification body/title, Show Result text, the Mirror/Knock/Confession copy) **must** use `WFTextTokenString` with a `￼` placeholder and `attachmentsByRange`, even for a single variable. Using `WFTextTokenAttachment` there causes the field to silently render **default or empty text at runtime** even though the plist is structurally valid — confirmed across all 46 Show Alert and 41 Notification instances in the plugin's 127-shortcut corpus. Data-flow parameters (`WFInput`, `WFDate`, `WFVariable`, `WFDictionary`) use the opposite convention.

**Why it happens:** PROSOCHĒ is copy-heavy — the Nine Circles primitives (Knock, Mirror, Confession, Voice) are almost entirely composed of dynamic display strings interpolating Heat/Pressure/Circle/telemetry variables. Every one of these is a place this bug can hide.

**Prevention:** Treat every user-facing string in Knock/Mirror/Confession/Voice/Notification/Control-Room-status as `WFTextTokenString` by rule, never `WFTextTokenAttachment`, regardless of whether it's "just one variable."

**Warning signs:** A Circle's message shows blank or a generic placeholder instead of the intended telemetry sentence when tested on-device — this will NOT be caught by the plist validator, only by an actual run.

**Phase:** Dumb Mirror-engine build phase (the ≥30 telemetry templates) and every Circle primitive that displays text.

### A3: `GroupingIdentifier` mismatches in If / Repeat / Menu blocks

**What goes wrong:** Every control-flow block (If/Otherwise/End If, Repeat Start/End, Choose from Menu/Case/End Menu) must share one `GroupingIdentifier` across all its parts, and nested blocks need distinct identifiers per level (verified working to depth 7 in the plugin's corpus). A missing End action, a mismatched identifier, or a `WFControlFlowMode` written as a string instead of `<integer>` breaks the block.

**Why it happens:** PROSOCHĒ has deep nesting by construction: profile → sequence → Circle (If/Otherwise-If ladder, 9-way) → primitive-specific branching → exit routing (6-way Menu) → explore/exploit (probability branch). This is exactly the "control-flow errors" risk the strategy itself calls out in §5.3.

**Prevention:** A Comment action documenting the wiring must precede every control-flow start (mandatory per BEST_PRACTICES.md comment-density rule: 8+ actions → 3 comments, 16+ → 4, 24+ → 5). Verify Case count in `WFMenuItems` exactly matches the six exits (Capture/Coordinate/Create/Connect/Consult/Close) in the same order, and that the Circle If-ladder has exactly nine mutually exclusive branches with a closing Otherwise/End If.

**Warning signs:** A Circle silently does nothing (falls through an unclosed If); a menu case executes the wrong exit; the same GroupingIdentifier reused across two logically separate blocks (e.g., the profile-selection If and the sequence-selection If sharing an ID).

**Phase:** Circle-ladder and exit-menu build phase; re-audit whenever the sequence (Classic/Black Mirror/Ambient) is made switchable, since that multiplies the branching.

### A4: Dictionary value type coercion (the JSON state round-trip)

**What goes wrong:** Reading `state.json` back through Detect Dictionary + Get Dictionary Value does **not** preserve JSON types faithfully:
- JSON booleans (`voice_enabled`, `ai_enabled`) coerce to numeric `1`/`0`, not the strings `"true"`/`"false"` — a `Contains "true"` check silently always fails.
- JSON `null` (e.g., `last_open_at: null` on first run) coerces to empty/nothing — comparing to the string `"null"` silently always fails.
- There is a documented Shortcuts bug: comparing a raw Dictionary Value directly inside an If condition can appear blank and fail; it must be routed through a Text action first, then the Text variable compared.
- Optional nested paths (e.g., `active_session.session_id` when `active_session` is null) must be guarded — reading a child key of a null parent breaks rather than returning empty.

**Why it happens:** `state.json`'s own schema (canonical strategy §16) is full of nullable fields (`last_open_at`, `last_close_at`, `active_session`, `cooldown_until`) by design — first-run and post-CLOSE states are exactly the states where these are null, which is precisely when the bootstrap/rollover/cooldown logic runs.

**Prevention:** For every boolean field read from `state.json`, branch on numeric `Is Greater Than 0` / `Equals 1`, never string "true"/"false". For every nullable field, guard with "Has Any Value" before reading a nested key. Route every Dictionary Value destined for an If comparison through an intermediate Text action first.

**Warning signs:** `voice_enabled` toggle appears to always be off/on regardless of setting; cooldown logic misfires on first run when `cooldown_until` is null; behavioural-day rollover check throws or silently no-ops when `last_open_at` is null on the very first OPEN.

**Phase:** JSON schema + bootstrap build phase, before Heat/Gravity/Pressure logic is written on top of it.

### A5: Number-vs-text coercion in threshold arithmetic

**What goes wrong:** There is **no numeric "equals" condition code** in the modern Shortcuts conditional (code `0` is "is less than," not "equals"). Pressure-to-Circle mapping and Heat-cap/floor checks (cap 30, floor 0; Gravity cap 5) require either an Any-of-two-bounds pattern (`is greater than or equal to N` AND `is less than or equal to N`) or a string-equality workaround — a naive `WFCondition = 0` used as "equals" will silently misfire. Separately, Math actions dividing/multiplying JSON-derived numeric strings (e.g., `opens_today / 6` for Gravity) require the numeric string to actually be a Number type, not raw Dictionary Value text — the cents-to-dollars division bug documented in BEST_PRACTICES.md ("if a Math action uses operand 100 on a cents value, the operator must be ÷, not + or −") is the same class of error that will bite `floor(opens_today/6)` if the divide/floor order is transposed.

**Why it happens:** Pressure = Heat + Gravity is compared against three different per-profile threshold tables (Paradise/Limbo/Inferno, 9 thresholds each = 27 comparison points), all of which are exact-boundary or range comparisons on values that started life as JSON dictionary text.

**Prevention:** Never use condition code `0`/`1`/`2`/`3` expecting "equals" semantics. Build the Pressure→Circle mapping as an explicit ordered If/Otherwise-If ladder using `is greater than or equal to` (code 3) on each descending threshold, not equality checks. Convert every JSON-sourced number through a Number action before Math/If use.

**Warning signs:** Pressure of exactly 5 (a documented Limbo threshold) fails to trigger Circle III; Gravity computed as a fraction instead of floored to an integer; profile switching (Paradise/Limbo/Inferno) produces identical Circle behavior because the threshold table read as text never numerically compared correctly.

**Phase:** Heat/Gravity/Pressure/Circle-mapping build phase — this is the arithmetic core the strategy calls "deterministic" and explicitly forbids the model from touching (§5.6, §32); it must be validated with unit-style manual test runs at every threshold boundary before Circle primitives are wired on top.

### A6: Date parsing and arithmetic (behavioural-day rollover, session timing)

**What goes wrong:** Format Date and Adjust Date are separate concerns that PROSOCHĒ needs simultaneously: the behavioural day (current date − 4 hours, §10.1) requires a raw Date value adjusted with **Adjust Date**, kept separate from the **Format Date**-produced string key (`"2026-08-13"`) used for JSON comparison and day-boundary detection. Get Time Between Dates (used for rapid-return/session-duration math) requires exactly one non-empty date operand and must not use the `CurrentDate` magic token directly — a Date action set to Current Date must be inserted first and referenced. `WFAdjustOperation` needs explicit Add/Subtract control (not the implicit default) when subtracting 4 hours.

**Why it happens:** PROSOCHĒ's entire day-boundary and session-duration model depends on getting this right: behavioural day, rapid-return Heat bonus, session duration for contract-fidelity, and CLOSE-time overrun calculation are four different date/duration computations sharing the same raw-Date discipline.

**Prevention:** Keep one raw Date variable per computation (current instant at OPEN, current instant at CLOSE, session start), format to string only at the point of JSON write or display. For "behavioural day = date − 4h," use Adjust Date with explicit Subtract, then Format Date `yyyy-MM-dd` on the adjusted value — never do string-level date math. For session duration, use Get Time Between Dates with the CLOSE-time Date and the stored session-start Date (loaded from JSON, not `CurrentDate`).

**Warning signs:** Behavioural day flips at midnight instead of 04:00 (the exact "obvious loophole" §10.1 says to avoid); rapid-return Heat bonus computed against wall-clock instead of the true prior-interaction timestamp; session duration reads as 0 or negative because `CurrentDate` was compared against a formatted string instead of a raw Date.

**Phase:** Behavioural-day and session-timing build phase, tested explicitly across a real 04:00 boundary and across app-switch timing before Heat/contract logic depends on it.

### A7: Fabricated action identifiers

**What goes wrong:** The plugin's own rule is explicit: "Do not invent identifiers or use OS 27-only parameters on macOS 26 targets... Avoid generating Unknown Action blocks." Common identifier gotchas the plugin flags by name: **Text** is `is.workflow.actions.gettext`, never `.text`; **Translate Text** is `.text.translate`, never `.translate`; **Send Email** is `.sendemail`, never `.sendmail`; there is no `.runscript` — only `.runapplescript`/`.runshellscript`/`.runsshscript`/etc.; **Podcast details** has no `.properties.podcastepisode`. `is.workflow.actions.input` (raw Shortcut Input action) should never be emitted — reference input via an `ExtensionInput` attachment instead.

**Why it happens:** The build agent is being asked to construct actions (Notes creation, Use Model, brightness/volume, Lock Screen, Color Filters) that the strategy *wants* to exist but that must be checked against the bundled ToolKit snapshot before use — several of the actions this project needs most (grayscale/Color Filters toggling, brightness/volume **readback**) do not appear anywhere in the plugin's identifier lists (see Class C below). The temptation to invent a plausible-sounding identifier is highest exactly where the product depends on it most.

**Prevention:** Every action identifier used must be cross-checked against `ACTIONS.md`, `APPINTENTS.md`, `THIRD_PARTY_ACTIONS.md`, or the bundled `data/toolkit-v*-tool-ids.json` snapshot before being written into the plist — this is the mandatory capability audit in strategy §31, and it is a hard gate, not a suggestion.

**Warning signs:** Validator reports "Unknown Action"; an action identifier resembles a documented one but with a plausible variant spelling (`.text` vs `.gettext`, `.sendmail` vs `.sendemail`).

**Phase:** Pre-build capability audit (strategy §31) — must complete and produce a documented pass/fail list for all ~24 actions the strategy names, before any handler is authored.

### A8: Action parameter shape drift across OS versions and targets

**What goes wrong:** Several parameters PROSOCHĒ needs are OS-version-gated. Use Model's `WFAllowWebSearch`/`FollowUp` are OS 27-only additions with no documented parameter for explicitly selecting **On-Device vs Private Cloud Compute vs Extension Model** in this ToolKit snapshot at all (see C7 below — this is a genuine capability gap, not just a version gate). Notes actions have a real parameter-name trap: `com.apple.Notes.CreateNoteFromMarkdownLinkAction` requires **camelCase** `markdownContents`, not `markdown` — using `markdown` can pass validation but silently produce an **empty note body at runtime**. `com.apple.mobilenotes.SharingExtension`'s `interpretAsMarkdown` toggle is OS 27+ only. Booleans across all of these (`ignoreWhitespace`, `interpretAsMarkdown`, `WFAllowWebSearch`, `FollowUp`) must be real plist booleans, never strings.

**Why it happens:** PROSOCHĒ targets iOS 26.x (per PROJECT.md constraints) but the plugin's richest AppIntent parameter documentation is OS 27-tilted; using an OS-27-only key on an iOS 26 target is a documented rejection case, and using the wrong Notes content key is a documented **validator false-pass** (valid plist, broken runtime note).

**Prevention:** Pin the validator target explicitly to the real iOS 26 target for every validation run (do not silently default to macOS/auto). For Notes creation specifically, use `markdownContents` and verify the created Note's body on-device, not just via validator pass, since this exact failure mode is silent.

**Warning signs:** Control Room Note created successfully (title present, folder correct) but body is empty on first launch — this is the single most damaging Class A failure for this product, because the Note is the entire onboarding UX (§18) and a silent empty-body failure means the user never sees the OPEN/CLOSE automation setup instructions at all.

**Phase:** Bootstrap phase (Control Room Note creation) — verify on a real device immediately, not just via plist validation, because this specific failure is a validator false-pass.

### A9: Validator false-passes — plist valid but shortcut broken at runtime

**What goes wrong:** The plugin is explicit that its validator "does not prove complex picker value serialization or runtime behavior" for AppIntent-style (`com.apple.*`) actions, and documents several specific import traps that pass validation but fail on-device:
- **Store Content** (`is.workflow.actions.setstoredcontent`): a bare/wrapped token attachment imports as an **empty Content placeholder**.
- **macOS 27 list-contains If**: repeatedly reassigning the same named list variable then testing it can show a **blank comparison chip** even though `WFConditionalActionString` is present in the underlying data.
- Comparing a raw **Dictionary Value** directly in an If (see A4) — imports fine, evaluates blank at runtime.
- `WFTextTokenAttachment` used for a **display** parameter (see A2) — imports fine, renders empty/default text at runtime.
- `markdown` vs `markdownContents` on Notes creation (see A8) — imports fine, note body empty at runtime.

**Why it happens:** The validator checks plist structure and known-identifier/parameter-shape rules; it cannot execute the Shortcut. Every one of the traps above is a case where the *shape* is legal XML/plist but the *runtime interpretation* on-device differs from what the shape implies.

**Prevention:** Treat "validator passes" as necessary, not sufficient. The strategy's own acceptance criteria (§32) require behavioural/state test cases beyond plist validity — every JSON-state-dependent branch, every display string, and the Control Room Note body must be manually exercised on a real iPhone before a phase is considered done, exactly as PROJECT.md's Active requirements demand ("Both forks pass the Shortcuts Playground validator, sign, and import" is listed as a separate, additional requirement from correctness).

**Warning signs:** Any of the specific traps above; more generally, any feature that "looks done" (validator green) immediately after generation without an on-device test run.

**Phase:** Every phase — this is a cross-cutting acceptance-criterion, not a single phase's job. It should gate phase completion throughout the build (see PROJECT.md's dominant-failure-mode framing: correctness is not optional even under time pressure).

### A10: Signing and import failures

**What goes wrong:** Duplicate shortcut names cause **silent import skips** — if `PROSOCHĒ — Nine Circles — Dumb` already exists in the library, `open -a Shortcuts` or `shortcuts run` on a freshly re-signed file silently does nothing; the `shortcuts` CLI has no `import`/`delete` subcommand, so the old copy must be manually deleted first. `shortcuts sign` can reject a plist-valid XML with "isn't in the correct format" even though `plutil -lint` passes — the fix is `plutil -convert binary1` before signing (the plugin's signer wrapper retries this automatically, but a manual signing step will not). Filenames must not carry a `_signed` suffix (canonical filename should match the intended shortcut name), and a `_signed` name surviving into the installed library should be treated as a failed install, not a naming quirk.

**Why it happens:** PROSOCHĒ explicitly ships two forks (Dumb, Sentient) that will be iterated and re-signed repeatedly during development, on the same test device, under the same or similar names — exactly the condition that triggers the silent-skip failure mode.

**Prevention:** Before every re-import during testing, explicitly delete the previous library copy of that fork by name. Use the bundled signer wrapper (not a raw manual `shortcuts sign` call) so the binary-plist retry happens automatically. Verify the installed name in the Shortcuts app matches the canonical fork name exactly, with no `_signed` suffix, after every install.

**Warning signs:** "Successful" sign/import in the terminal, but the on-device Shortcuts app shows no change, or shows a stale prior version silently continuing to run.

**Phase:** Distribution/signing phase for both forks — and every subsequent test cycle during earlier phases where the shortcut is being iteratively re-tested on-device.

---

## B. State and concurrency pitfalls

Grounded in strategy §20 (CLOSE handler), §21, §30 (Failure modes: "State races"), and PROJECT.md's Active requirements. Shortcuts has no transaction API, no locking primitive, and no atomic multi-step file write — every mitigation here is a workaround built from ordinary actions, not a platform guarantee.

### B1: Overlapping OPEN/CLOSE runs during rapid app switching

**What goes wrong:** If the user rapidly switches between two tracked apps (App A → App B → App A), Personal Automations can fire OPEN/CLOSE events in an order or overlap that a single shared `state.json` cannot serialize safely — a second OPEN's read-modify-write can race a first CLOSE's read-modify-write, and Shortcuts has no locking mechanism.

**Prevention:** Every CLOSE run must capture its own session ID and reload `state.json` immediately before committing (strategy §20 step 5-6: "if active session ID changed, a newer OPEN owns state — stop"). This makes CLOSE a no-op rather than a corrupting write when it's stale, which is the only safe outcome given no locking primitive exists.

**Warning signs:** `active_session` in JSON pointing at a session ID that doesn't match the app currently believed open; Heat/Gravity double-counted for a single real session; contract-fidelity recorded against the wrong session.

**Phase:** OPEN/CLOSE state-engine build phase — this must be built and manually stress-tested (rapid A→B→A switching on a real device) before Circle primitives are layered on top, since primitives read state the race can corrupt.

### B2: Duplicate OPEN triggers from a single user action

**What goes wrong:** A single app-open gesture can plausibly fire more than one automation event in edge cases (e.g., a brief app switch during a notification banner, or the automation re-triggering on app-foreground after a system interruption) — PROJECT.md explicitly lists debounce as a requirement, and strategy §19 step 5 names it directly ("debounce duplicate OPEN events").

**Prevention:** On every OPEN, compare the new timestamp against `last_open_at`; treat OPENs within an implausibly short window (sub-second to a few seconds) for the same app as a duplicate trigger and no-op rather than incrementing Heat/opens_today a second time.

**Warning signs:** `opens_today` incrementing by 2 for what the user experiences as one open; Heat spiking without a corresponding real reopening pattern.

**Phase:** OPEN handler build phase, alongside B1.

### B3: Partial/corrupt JSON writes

**What goes wrong:** Shortcuts' Save File / overwrite is not a transactional write — if the shortcut is killed, backgrounded, or interrupted mid-write (plausible given Personal Automations can be interrupted by the system), `state.json` can be left truncated or malformed. PROJECT.md explicitly requires "Corrupt or missing JSON... trigger safe recovery rather than failure."

**Prevention:** Every state-load path must run Detect Dictionary / Get Dictionary Value inside a guarded branch (Has Any Value / valid-parse check) with a defined recovery path — reconstruct a fresh default state rather than crashing the Shortcut, and log the recovery event to the Note rather than silently losing behavioural history context.

**Warning signs:** Get Dictionary Value returning nothing for a key that should always be present; the Shortcut failing silently on OPEN with no intervention shown at all (the single worst-case UX outcome for this product, since it means the safety-critical Circle IX ejection also silently fails).

**Phase:** Bootstrap/self-heal build phase — must be built and tested (deliberately corrupt the JSON file and confirm recovery) before relying on JSON state anywhere else.

### B4: iCloud sync latency on the state file and the Note

**What goes wrong:** Both `state.json` and the Control Room Note may sync via the user's iCloud depending on device configuration (strategy §27 acknowledges this explicitly for the Note). If the file location used for `state.json` is iCloud-backed (vs strictly local), a write on one device or a delayed sync could present stale state to a read shortly after — though for a single-device prototype this is a secondary risk, it's a real one if the user has iCloud Drive enabled for the Shortcuts data folder.

**Prevention:** Store `state.json` in a location and manner that favors local-first read/write consistency where the available Shortcuts file actions allow it; do not assume Save File / Get File round-trips instantaneously. Treat the Note strictly as human-readable, never re-parsed as authoritative machine state on the hot OPEN path (already a design decision in §5.4/§7.3) — this sidesteps most of the Note's own sync latency risk.

**Warning signs:** State read on OPEN reflecting a value from before the most recent CLOSE write, especially shortly after a device wake from background.

**Phase:** Bootstrap/state-storage build phase — decide and document the exact file location strategy before Heat/Gravity logic depends on read-after-write consistency.

### B5: Behavioural-day rollover at 04:00 while a session is active

**What goes wrong:** If a user opens a tracked app at 03:58 and the CLOSE fires at 04:05, the OPEN and CLOSE nominally belong to different behavioural days by the `date − 4h` rule (§10.1) — Heat/Gravity/opens_today attribution, and the day-key used for daily aggregate rollup, must be decided consistently (almost certainly: attribute the whole session to the day the OPEN occurred, not recompute at CLOSE).

**Prevention:** Compute and persist the behavioural-day key at OPEN time as part of the session record; CLOSE must reuse the persisted session's day key rather than recomputing behavioural day from the CLOSE timestamp, or a session can vanish from one day's aggregate and appear in the next day's Gravity count.

**Warning signs:** `opens_today` resetting mid-session; a session's contract-fidelity or duration attributed to the wrong day in the Note ledger.

**Phase:** Behavioural-day build phase (paired with A6), explicitly tested by simulating an OPEN just before 04:00 and a CLOSE just after.

### B6: Cooldown (Ice) attempts inflating Heat

**What goes wrong:** PROJECT.md and strategy §22 explicitly require that blocked attempts during Circle IX cooldown "don't endlessly inflate Heat" — a naive OPEN handler that always adds Heat on every OPEN would turn Ice into a Heat-runaway loop precisely when the user is most agitated and most likely to repeatedly retry.

**Prevention:** The OPEN handler must check cooldown state *before* running the standard Heat-increment logic, and route cooldown-active OPENs to a distinct, Heat-neutral "still in Ice" response rather than falling through the normal Heat pipeline.

**Warning signs:** Heat still climbing (or Circle still escalating) during an active Ice cooldown; cooldown never naturally expiring because it keeps getting re-triggered by its own blocked attempts extending `cooldown_until`.

**Phase:** Circle IX / Ice build phase — this is a deterministic, safety-relevant branch and should be unit-tested with repeated rapid OPENs during an artificially short test cooldown before shipping.

### B7: Heat decay computed from a stale or missing last-interaction timestamp

**What goes wrong:** Heat decay (§10.2: "-1 per ~10 minutes away") depends on `last_open_at`/`last_close_at` being present and correct; on first run these are null (see A4), and after a JSON-recovery event (B3) they may be reset to defaults that don't reflect true elapsed time — either case can produce a decay calculation against a wrong or missing baseline, either erroneously zeroing Heat or leaving it artificially stuck high.

**Prevention:** Decay logic must explicitly branch on "no prior timestamp exists" (first run / post-recovery) and treat it as zero elapsed time / zero decay rather than computing a Get Time Between Dates against a null or default epoch value.

**Warning signs:** Heat instantly at cap or instantly at floor immediately after a JSON-recovery event; first-ever OPEN after import showing non-zero Heat.

**Phase:** Heat/decay build phase, explicitly tested against both the true first-run state and a simulated post-recovery state.

### B8: Session ID collisions

**What goes wrong:** If session IDs are generated from a low-resolution source (e.g., a formatted timestamp with second precision, or a simple counter that can reset on JSON recovery), two sessions started in rapid succession — plausible during B1/B2's rapid-switching scenarios — could collide, defeating the exact CLOSE-handler safety mechanism (§20 step 6) built to prevent state races.

**Prevention:** Generate session IDs from a source with enough entropy/precision to be practically unique across rapid re-opens (e.g., a full timestamp with sub-second precision if available, or a timestamp combined with a random/incrementing component) — do not rely on whole-second timestamps alone given B1/B2's rapid-switching scenario is the exact case this needs to survive.

**Warning signs:** Two sessions in the recorded `recent_sessions` history sharing an identical session ID.

**Phase:** OPEN handler build phase, alongside B1/B2 — this is the mechanism B1's fix depends on, so it must be correct first.

### B9: The Shortcut invoked manually mid-session

**What goes wrong:** The Control Room manual menu (Status/Sync/Change Profile/Test a Circle/Emergency Restore, etc.) runs the same shortcut with no input, while an OPEN-triggered session may be conceptually "active" in JSON (`active_session` populated). A manual run must not silently clobber, duplicate, or terminate an in-progress tracked session's state — e.g., "Test a Circle" must not increment real Heat/Gravity/opens_today, and "Reset Today" must not corrupt an active session ID that a pending CLOSE is about to reload against.

**Prevention:** Route on input value early and explicitly: empty/no input → manual menu path (never touches Heat/Gravity/session fields except through the documented menu actions like Reset Today/Emergency Restore, which must explicitly clear `active_session` rather than leaving it dangling); `"OPEN"`/`"CLOSE"` → automation path. "Test a Circle" must render a Circle's UI without writing to the real state fields the OPEN/CLOSE handlers depend on.

**Warning signs:** Using "Test a Circle" from the menu changes real Heat/Pressure/Circle in a way that's visible on the next genuine OPEN; a manual "Reset Today" run while a tracked session is open leaves `active_session` pointing at a session ID CLOSE can never resolve.

**Phase:** Invocation-routing build phase (this is the very first branch point in the whole Shortcut, per strategy §18-19) — must be correct before any other handler is built on top of it, and re-verified once the manual menu (§18, "Second manual run") is added.

---

## C. iOS platform and safety pitfalls

This class is grounded in an actual capability audit of the plugin's bundled ToolKit identifier lists (`ACTIONS.md`, `APPINTENTS.md`), performed for this research. The findings below are load-bearing for the roadmap: several actions the canonical strategy assumes exist **could not be found** in the documented identifier catalog.

### C1: Brightness cannot be read back before being changed

**What goes wrong:** `ACTIONS.md`'s complete identifier list includes `setbrightness` but **no `getbrightness` or equivalent readback action anywhere in the bundled ToolKit catalog**. Strategy §21 requires: "Only change [brightness] if PROSOCHĒ can reliably restore... If the original state cannot be read, do not make a stateful brightness intervention." Taken literally against what's actually verifiable in this ToolKit, the Dimming primitive (Primitive E) **cannot safely be built as a stateful set-and-restore action** — there is no verified way to capture the user's actual current brightness before overwriting it.

**Prevention:** Do not fabricate a "Get Brightness" action. Apply the strategy's own fallback rule (§21, and the do-not-fabricate protocol below): either skip the Dimming primitive as a real device-brightness change entirely (safest), or scope it to a PROSOCHĒ-owned value the app never claims came from reading the user's real prior state, clearly framed to the user as "PROSOCHĒ does not attempt to dim your actual display" in the Control Room / build notes.

**Warning signs:** Any implementation that calls Set Brightness without an immediately preceding, verified-real Get Brightness action; a user reporting their brightness was left at a PROSOCHĒ-set value after Emergency Restore.

**Phase:** Capability-audit phase (must be flagged before Dimming is built at all) and Environmental-safety build phase.

### C2: Volume cannot be read back before being changed

**What goes wrong:** Identical situation to C1 — `setvolume` exists in the identifier catalog, but no `getvolume`/current-volume readback action was found. Strategy §21: "If changing volume for Silence, restore original value. If the original value cannot be captured reliably, skip the intervention."

**Prevention:** Same as C1 — do not fabricate a readback action. The Silence primitive (Primitive C) should default to muting/reducing **media playback** (which has better-supported, more reversible action shapes — e.g., pause/skip on the current media session) rather than claiming to snapshot-and-restore system volume, unless a genuine verified readback action is found during the capability audit.

**Warning signs:** Same pattern as C1: a Set Volume call with no verified preceding readback.

**Phase:** Capability-audit phase and Environmental-safety build phase.

### C3: Color Filters / grayscale toggling has no verified action at all

**What goes wrong:** No `colorfilter`, `grayscale`, or equivalent accessibility-display-filter action identifier appears anywhere in `ACTIONS.md` or `APPINTENTS.md`'s Accessibility sections (which otherwise enumerate 306/164 accessibility-related actions, mostly `OpenAccessibility*` deep links and `Ax*`/`UpdateAx*`/`ToggleAx*` entities — none matching Color Filters specifically). This means the Ash primitive (Primitive B, grayscale) as literally specified in the strategy — "Grayscale where iOS can apply and restore it safely" — has **no confirmed implementation path** in this ToolKit snapshot. (`nightshift.set` does exist, but Night Shift is a color-temperature warmth toggle, not grayscale, and is not a substitute.)

**Why it matters more here than a typical gap:** the strategy's own evidence base (§6.5) treats grayscale as one of the better-evidenced individual interventions (a 112-participant preregistered field experiment), so this is a case where a well-evidenced design idea collides directly with an unverified iOS capability — exactly the tension the do-not-fabricate protocol exists to resolve honestly rather than paper over.

**Prevention:** Treat Ash as **not implementable via a verified action** unless the capability audit turns up a real `Ax*`/`UpdateAx*`/`ToggleAx*` Color Filters entity this research did not locate. If none is found, apply the safest fallback: skip Ash as a system-level display change, substitute a passive non-system-altering equivalent (e.g., a full-screen dimming overlay drawn via the Shortcut's own UI rather than a system accessibility toggle, if such an action exists and is verified), and record the deviation and rationale in the build notes exactly as PROJECT.md requires ("Build notes documenting every unverified iOS action, deviation, and fallback taken").

**Warning signs:** Any plist action identifier resembling `.colorfilter`, `.grayscale`, or `.accessibility.colorfilters` that was not found in `ACTIONS.md`/`APPINTENTS.md` during this research — treat as fabricated until independently re-verified against the live ToolKit database on the actual build machine.

**Phase:** Capability-audit phase, first — this should be one of the first specific go/no-go findings reported back before Circle-sequence work assumes Ash exists as specified.

### C4: Accessibility settings clobbered by an intervention that can't detect them

**What goes wrong:** Because there's no verified readback for brightness, volume, or Color Filters (C1-C3), there's also no verified way to detect whether the user has *already* configured any of these deliberately for accessibility reasons (e.g., a user who already runs in grayscale or reduced brightness for a vision-related need). Strategy §30 names this directly: "Grayscale/brightness manipulation conflicts with user needs... never blindly override accessibility configuration."

**Prevention:** Direct consequence of C1-C3's fallback: if a stateful environmental change can't be safely read-and-restored, the correct behavior is to not make it at all, which also automatically avoids clobbering a pre-existing accessibility configuration. This makes C1-C3's conservative fallback doubly justified.

**Warning signs:** Same as C1-C3 — any environmental Set action without a verified paired readback.

**Phase:** Environmental-safety build phase, alongside C1-C3 and Emergency Restore.

### C5: Lock Screen availability and behaviour from an automation

**What goes wrong:** `lockscreen` (`is.workflow.actions.lockscreen`) does appear in the identifier catalog, so Circle IX's strongest ejection option is plausible — but the strategy itself hedges: "If native Lock Screen is available and verified, it may be used. Otherwise route to Close / Control Room / another strongest safe exit" (§11, Primitive I). Whether Lock Screen behaves correctly when invoked from within an automatically-running Personal Automation (as opposed to a manually tapped shortcut) is not established by the plugin's documentation and needs on-device verification — some system actions behave differently, or are blocked, when run from an automation context versus a foreground manual run.

**Prevention:** Verify Lock Screen's actual behavior when triggered by a real App-Is-Opened automation (not just a manual test run) before relying on it for Circle IX. Build the "otherwise route to Close" fallback regardless, since the strategy already anticipates this action may not be reliably available in the automation context.

**Warning signs:** Lock Screen working when the shortcut is run manually from the Shortcuts app but doing nothing (or erroring) when the same shortcut is triggered by the real OPEN automation.

**Phase:** Circle IX / Ice build phase — must include an on-device automation-triggered test, not just a manual-run test.

### C6: Automations that require confirmation instead of running automatically

**What goes wrong:** Strategy §5.1 notes Apple lists App automations "among the Personal Automations that can run automatically rather than requiring confirmation" — but this is a per-action property, not a blanket guarantee for the whole shortcut. Certain actions (particularly ones touching Notes, sensitive system settings, or new-permission-required capabilities) can force a "Ask Before Running" prompt the first time they're used inside an automation, or on every run, even when the automation itself is configured to run without confirmation. If any action inside PROSOCHĒ's OPEN handler triggers this, the entire "self-saucing," silent-interception design breaks — the automation stalls waiting for a tap the user may not see in time (or ever, if their phone is locked when it fires).

**Prevention:** During capability audit and early on-device testing, deliberately test the full OPEN handler end-to-end from a real backgrounded automation trigger (not a manual foreground run) and watch for any confirmation prompt. If one appears, identify which action triggered it and either find a version of that capability that doesn't require confirmation or restructure the handler so the confirmation-requiring action isn't on the fast OPEN path.

**Warning signs:** The automation appearing to "hang" or not fire visibly when the tracked app is opened for real, especially the first time after import; a system notification asking to allow the automation to run.

**Phase:** Capability-audit and OPEN-handler build phase — must be tested via a real automation trigger before the OPEN handler is considered functional, not just via manual shortcut runs during development (which don't reproduce this failure mode).

### C7: `Use Model` latency making early Circles feel broken

**What goes wrong:** Strategy §14.5 already anticipates this: "Do not force model inference onto every early OPEN if it makes the intervention visibly slow." Apple states the On-Device model "can handle simple requests without a network connection," but does not guarantee latency, and the strategy's own Circle-by-Circle design (§14.4) deliberately keeps Circle I fully deterministic and gates Circle II's model use on "cached/fast enough; otherwise deterministic" specifically because of this risk.

**Prevention:** Build and ship the deterministic fallback path for every Circle before wiring in the model call, so a slow/failed model call degrades to the Dumb-equivalent behavior rather than blocking the intervention. Never let a Circle I or II response wait on an unbounded model call.

**Warning signs:** Perceptible delay (more than roughly a second or two) between app-open and any PROSOCHĒ UI appearing at low Circles; user reports the early Circles feel laggy or broken compared to Dumb.

**Phase:** Sentient-fork build phase, specifically the Circle II-VIII model-integration work — must be built with the deterministic fallback first, model enhancement second, never the reverse.

### C8: `Use Model` silently falling back off On-Device — and no verified way to force it

**What goes wrong:** This is worse than a runtime fallback risk: the plugin's own documentation of `is.workflow.actions.askllm` (Use Model) lists exactly two verified parameters — `WFAllowWebSearch` (Use Broad World Knowledge) and `FollowUp` (Follow Up), both OS 27-only additions — and **no parameter for explicitly selecting On-Device vs Private Cloud Compute vs the ChatGPT/Extension Model** was found anywhere in `ACTIONS.md` or `APPINTENTS.md`. No golden-shortcut example using `askllm` exists in the plugin's reference corpus either. If model-source selection is a runtime UI toggle inside the action's editor sheet rather than a plist-serializable parameter, the build agent **cannot guarantee via the plist alone** that the shipped Shortcut is locked to On-Device — this is exactly the "Sentient must select On-Device... never ChatGPT... never Private Cloud Compute" hard constraint from PROJECT.md.

**Prevention:** Treat model-source selection as an unverified capability until proven otherwise on a real device — do not fabricate a `WFModelSource`-style key. If, on inspection of a real device's Shortcuts editor, model source turns out to be a manually-configured UI setting rather than a plist parameter, the build notes and Control Room Note must say so explicitly and instruct the user to manually verify/set On-Device in the action's configuration after import — this is a deviation that must be recorded and surfaced to the user, not silently assumed correct. Test a Model (the manual-menu diagnostic action, §18) should include an explicit on-device confirmation step (e.g., displaying whatever source-identifying output the action provides, if any) rather than only checking that a response was returned.

**Warning signs:** No `WFModelSource`/similar key found during the capability audit (confirmed absent from this research); inability to find any plist evidence that on-device-only is enforceable; a "Test Model" run that returns a plausible response but with no way to confirm which backend actually served it.

**Phase:** Capability-audit phase (flag this as a specific open question before Sentient work begins) and Sentient-fork build phase (the Test Model diagnostic must directly address this gap).

### C9: Malformed model output breaking the parse

**What goes wrong:** Apple's own documentation (quoted in strategy §5.6) warns "generative outputs may vary" — the ALLOW/CHALLENGE/DENY structured-output contract (§14.3) and the contract-auditor logic depend on parsing free-form model text into one of exactly three states. A model response that doesn't match the expected format exactly (extra text, different casing, a refusal, an empty response) will break naive string-equality parsing.

**Prevention:** PROJECT.md and strategy §32 already require "output is parsed/validated" and "malformed-output fallback" as explicit acceptance criteria. Build the parse as a tolerant match (contains-check on the expected keyword, not exact-equality) with an explicit "anything else defaults to ALLOW" (never a silent DENY or silent crash — a parse failure must never itself function as punishment) and always fall through to the deterministic Dumb-equivalent Circle behavior on parse failure.

**Warning signs:** A Sentient session producing a Circle-behavior that looks like neither ALLOW, CHALLENGE, nor DENY (e.g., the raw model text displayed to the user unprocessed); DENY appearing more often than the strategy's "DENY only at sufficiently high Circles" rule would predict, suggesting parse-failure is defaulting to DENY.

**Phase:** Sentient-fork build phase, contract-auditor implementation.

### C10: Notes actions prompting for permission mid-automation

**What goes wrong:** First-time access to Notes data from a Shortcut (Create Note, Append to Note, Find Notes) can trigger an iOS permission prompt the very first time it runs — and per C6, if that first run happens inside an automatically-triggered automation rather than the manual first-run bootstrap, the prompt can appear at an unexpected moment (mid-OPEN) rather than during the deliberate first-tap bootstrap flow the strategy designs for (§18).

**Prevention:** Ensure the very first Notes access of any kind happens during the manual first-run bootstrap flow (creating the Control Room Note), which the user is actively engaged with and can approve — never let the *first* Notes permission prompt be triggered by a later automatic OPEN/CLOSE automation run. Structure bootstrap so Control-Room-Note creation (and thus the permission grant) is guaranteed to happen before the user is instructed to create the OPEN/CLOSE automations.

**Warning signs:** A permission dialog appearing during a real automated app-open rather than during the manual bootstrap tap; the Note failing to append meaningful events post-bootstrap because a later, different Notes action (e.g., Find Notes for Sync My Profile) hits its own separate first-use prompt.

**Phase:** Bootstrap build phase — sequence every distinct Notes action type (Create, Append, Find) to have its first invocation happen during the guided manual flow, not the automated path.

### C11: The user simply disabling the Personal Automation

**What goes wrong:** This is named directly as the "dominant failure mode" in PROJECT.md and discussed at length in Class D below (see D2) — included here because it is also a pure platform fact, not just a product-design risk: Apple gives the user an always-available, one-tap way to disable either Personal Automation from the Shortcuts app, and PROSOCHĒ has and can have no way to detect, prevent, or be notified of this (PROJECT.md's Out of Scope: "Any claim of tamper-proofing").

**Prevention:** Design-level, not code-level: keep the product honest about this limitation in its own copy (never claim reliability it doesn't have), and treat every other pitfall in this document as contributing to or against the disablement risk — every unnecessary friction point, false positive, or broken interaction is a direct contributor to this specific, unfixable platform reality.

**Warning signs:** N/A at the code level — this is measured at the product level via the disable-rate metric strategy §23 already specifies.

**Phase:** Cross-cutting; explicitly acknowledged in the Control Room Note copy (bootstrap phase) and tracked as the headline product metric from the first friend-test onward.

---

## D. Behavioural / product pitfalls

Drawn from strategy §30 ("Failure modes") and the cited evidence base (§6). These are pitfalls in what gets *built*, not how it's coded — but they still need concrete detection and phase mapping, because a technically correct build can still fail the product.

### D1: Intervention fatigue and mechanical dismissal

**What goes wrong:** Repeated exposure to the same friction pattern trains the user to dismiss it without engaging — exactly the outcome the one sec field study's 36%-dismissal-rate and the strategy's "no repetitive lecture" rule (§30) are trying to avoid becoming the *whole* effect rather than a *partial* one.

**Detection:** Track (locally, per strategy §23) the trend of contract-fidelity and rapid-return-rate over calendar time per user — if early sessions show engagement (contracts filled thoughtfully, Circle escalation actually changing behavior) but later weeks show near-instant dismissal at every Circle with no behavior change, that's fatigue, not habituation to a stable equilibrium.

**Prevention:** Sequence variation (Classic/Black Mirror/Ambient, switchable per strategy §12) and template-bank size (≥30 Dumb Mirror templates, §13.1) exist specifically to slow this down — but the build must also ensure Sentient "avoids repeating the same Mirror" (§14.6) by actually checking `last_model_message` against the candidate response before display, not just generating fresh text and hoping it varies.

**Phase:** Mirror-engine and Sentient-message-selection build phases; revisit in a later phase once real usage data exists to check for the fatigue signature above.

### D2: Disablement as the dominant failure mode

**What goes wrong:** PROJECT.md states this explicitly: "the intervention becomes annoying enough that the user disables PROSOCHĒ. That is a product failure even if it blocks more openings." A build that optimizes purely for blocking rate (aggressive Circle escalation, minimal exits, DENY-heavy Sentient tuning) will look successful on the primary metric while actively driving the actual failure mode.

**Detection:** This cannot be detected from telemetry alone (a disabled automation produces no more events, which looks identical to "problem solved"). It must be actively asked about in friend/creator testing (§23: "ask whether the system was disabled and why"), and the Control Room / build notes should track this as a qualitative check at every milestone, not just a metric to compute later.

**Prevention:** Default to Limbo, not Inferno; make Paradise a genuinely gentle real option, not a token gesture; ensure every Circle escalation is conditional on actual measured Pressure, never a fixed schedule; keep exits genuinely low-friction so blocking never feels like a dead end.

**Phase:** Cross-cutting product-quality gate, explicitly checked at the end of the Dumb build phase (before Sentient work begins) and again after Sentient ships, via direct user conversation, not metrics alone.

### D3: Over-verbal design — the dismissal option, not the sentence, is the mechanism

**What goes wrong:** The one sec preregistered decomposition (§6.4) found that giving the user an easy dismissal option had the strongest effect — not the deliberation message itself. PROSOCHĒ's most distinctive creative surface (the Mirror's clever, uncanny sentences) is exactly the part of the mechanism the evidence says is *not* the primary driver. There's a real risk the build (and especially Sentient) over-invests engineering and design effort in message quality while under-investing in making the actual choice architecture (fast, easy, always-available exit) as frictionless as the evidence says it needs to be.

**Detection:** Audit time-to-exit at every Circle — if reaching Close/an exit requires more taps or more reading than reaching "just continue into the app," the choice architecture is inverted relative to the evidence. Also audit engineering effort allocation qualitatively: is the exit path (Consult routing, Close behavior, six-exit menu) as robustly built and tested as the Mirror/Voice copy generation?

**Prevention:** Build the exits (§8, all six) and Circle IX's "always a route out" guarantee (§22) with at least as much rigor as the Mirror engine — the strategy's own acceptance criteria (§32) already lists "all enabled exits can be invoked" and "always a route out" as hard requirements; do not let Sentient's more interesting engineering work (contract auditing, longitudinal memory, §15) crowd out exit-path polish in practice.

**Phase:** Exit-pathway build phase should be scheduled and resourced on equal footing with the Circle-primitive/Mirror-engine build phase, not treated as a lesser afterthought once the "interesting" AI work is done.

### D4: The model inventing facts or diagnosing the user

**What goes wrong:** Strategy §14.6 and §30 ("False psychological inference") are explicit: the model must never claim to know in-app content, never diagnose addiction, never assert the user is bored/anxious/lying. A structured-output contract that only constrains the ALLOW/CHALLENGE/DENY verdict but not the accompanying natural-language text leaves room for the model to hallucinate a plausible-sounding but fabricated behavioral claim inside an otherwise-valid response.

**Detection:** Manually review a sample of real Sentient outputs (not just structural parse-success) against the "what Sentient can/cannot know" list in §14.1 — specifically checking for any claim about in-app content, emotional state, or honesty that wasn't derivable from the supplied telemetry.

**Prevention:** The system prompt must enumerate the forbidden claim categories explicitly (as §14.6 already drafts), and the compact context window passed to the model (§28) must literally not contain any data the model could use to fabricate an in-app-content or emotional-state claim — if the data isn't in the context, a well-constrained model is far less likely to invent it, but this must still be spot-checked, not assumed from prompt wording alone.

**Phase:** Sentient system-prompt design and context-window build phase; spot-check review should recur each time the prompt or context shape changes.

### D5: A learned association that opening an app always produces criticism

**What goes wrong:** Strategy §29 states this directly as a design risk: "The product must not create a learned association that opening a target app always produces criticism." If positive-reinforcement messages (successful contract, cooled Heat, respected boundary) are implemented as an afterthought relative to the challenge/criticism templates, the lived experience skews punitive regardless of stated intent, which both increases fatigue (D1) and disablement risk (D2).

**Detection:** Audit the actual template bank / Sentient prompt for message-tone balance — count positive-acknowledgment templates against challenge/critical templates in the ≥30-template Dumb bank, and verify the Sentient prompt's example set (§29) includes as many "good" examples as cautionary "bad" examples (it does, in the strategy text — the build must preserve that balance, not just draw from the negative half more often in practice).

**Prevention:** Explicitly gate positive-acknowledgment messages on the same facts-only, no-invention rule as critical ones (a real respected boundary, a real cooling Heat trend) so they're just as evidence-based, and ensure the message-selection logic doesn't structurally favor challenge templates (e.g., by only checking for overrun/rapid-return facts and never checking for contract-success/cooling facts first).

**Phase:** Mirror-engine template-authoring phase (Dumb) and Sentient system-prompt phase — both need an explicit tone-balance check before shipping, not just individual message quality review.

### D6: PROSOCHĒ merely redirecting time into a different app rather than off the phone

**What goes wrong:** Strategy §30 names this directly ("Over-optimization for phone-based alternatives"): if the exit-learning system (§9) rewards *any* time away from the tracked app equally, it will happily learn to route the user into another phone app (e.g., a different feed) that also isn't what they actually wanted, and call that success because the tracked-app-return-time metric improved.

**Detection:** Compare exit-outcome quality qualitatively, not just by the primary metric — specifically check whether Close (phone-down) is ever winning the epsilon-greedy exploitation phase, or whether the learned policy has converged entirely on phone-based exits (Capture/Coordinate/Create/Connect/Consult) to the total exclusion of Close.

**Prevention:** Strategy §30's own mitigation is explicit: "Close is a first-class exit... exit-learning rewards time away from tracked apps" — the exit-learning implementation must not structurally disadvantage Close relative to app-based exits (e.g., Close's outcome-measurement window must not unfairly penalize it just because "time away from tracked apps" is easier to measure accurately for an app-based exit that leaves the phone actively in use and easier to end up under-measured for Close if the user locks the phone and the Shortcut has no way to observe what happens next).

**Phase:** Explore/exploit learning build phase — Close's reward-measurement path needs explicit design attention equal to the app-based exits, not an assumption that "time until next tracked OPEN" naturally works the same way for both.

### D7: Note growth

**What goes wrong:** Strategy §30 names this directly: "Control Room becomes huge." If Note-append logic isn't disciplined about what counts as "meaningful" (§17: "Do not append every tiny implementation detail... prefer meaningful entries"), the Note becomes slow to open, slow to scroll, and eventually the exact "growing rich-text Note" problem the JSON/Note split was designed to avoid (§5.4) — even though JSON remains the fast machine store, an enormous Note is still a real UX degradation for the human-readable side of the product.

**Detection:** Track Note length/entry-count growth rate during testing; check whether every OPEN/CLOSE cycle is producing a proportionate number of new lines or whether internal-calculation noise is leaking into the ledger.

**Prevention:** Gate every Note append behind an explicit "is this meaningful" check matching the §17 example list (Circle changes, contracts, redirects, rapid-return clusters, successful cool-downs, daily summaries, profile changes) — never append on every OPEN/CLOSE unconditionally, and treat daily/weekly summary compaction (mentioned as a future mitigation in §30) as a real backlog item once Note length is observed to be growing faster than that.

**Phase:** Note-logging build phase (paired with OPEN/CLOSE handlers) — the "what counts as meaningful" filter should be written and reviewed explicitly, not left as an implicit byproduct of whatever the handler happens to log.

### D8: False psychological inference from telemetry

**What goes wrong:** Beyond D4's model-specific framing, this also applies to Dumb's deterministic copy and to product-level interpretation of the data during testing/tuning: telemetry (Heat, rapid-return count, contract overrun) is a behavioral signal, not a mental-state signal, and both the shipped copy and the humans tuning the system during prototyping are at risk of over-interpreting it (e.g., treating a high-Heat user as "addicted" when designing thresholds, rather than treating Heat strictly as the operational intervention signal §10.2 defines it as).

**Detection:** Review both the Dumb template bank and any internal design notes/comments for language that crosses from behavioral description into diagnostic claim (the forbidden-word list in §14.6 — addiction, dopamine, weakness, lazy, failure, shame — is a useful audit checklist even for Dumb, which has no model to blame for the lapse).

**Prevention:** Apply the same "facts only, no diagnosis" discipline to Dumb's fixed copy that §14.6 mandates for Sentient's generated copy — this is a copywriting/product-review pass, not just a model-prompt-engineering concern.

**Phase:** Mirror-engine template-authoring phase (Dumb) — explicit copy review against the forbidden-language checklist before the template bank is considered final.

---

## "Do not fabricate" protocol

This is the single non-negotiable rule governing every gap identified in Class A and Class C above. It is restated here as a standalone, quotable block for the build agent.

> **When an iOS action or parameter the strategy requires cannot be verified in the Shortcuts Playground ToolKit (identifier not found in `ACTIONS.md`, `APPINTENTS.md`, `THIRD_PARTY_ACTIONS.md`, or the bundled `data/toolkit-v*-tool-ids.json` snapshot for the actual build target):**
>
> 1. **Do not invent the identifier or parameter shape.** A plausible-sounding action name is not evidence it exists. Fabricated actions either fail validation outright or — worse — produce a validator false-pass that only breaks at runtime (see A9).
> 2. **Use the safest available fallback**, chosen in this priority order:
>    a. A verified, documented alternative action that achieves a strictly weaker but real version of the same intent (e.g., pause media instead of a verified volume snapshot/restore).
>    b. Skipping the specific behavior entirely, if no safe verified alternative exists (this is explicitly correct, not a failure — PROJECT.md requires "skip any stateful change that cannot be restored" as a hard safety rule, not a last resort).
>    c. Never choose a fallback that could strand the user in an unrecoverable state (irreversible settings changes, no exit path, no route out of Ice) purely to preserve a "feature complete" appearance.
> 3. **Record the deviation.** Every unverified action, every fallback taken, and the reasoning must be written into the build notes deliverable (PROJECT.md: "Build notes documenting every unverified iOS action, deviation, and fallback taken") and, where it changes user-visible behavior or a safety guarantee, surfaced in the Control Room Note copy so the user isn't misled about what the Shortcut actually does.
> 4. **Keep the Shortcut runnable.** A missing capability must degrade gracefully — never let an unverified action block the OPEN/CLOSE path, corrupt state, or prevent Circle IX's "always a route out" guarantee. If in doubt, the deterministic, already-verified path always wins over an unverified enhancement.
>
> This applies with equal force to Dumb (deterministic actions) and Sentient (Use Model integration) — the Sentient fork does not get a looser standard for iOS-action verification just because model behavior is separately expected to be non-deterministic.

Findings from this research that already trigger this protocol and should be treated as pre-flagged for the capability audit: **brightness readback (C1), volume readback (C2), Color Filters/grayscale toggling (C3), and explicit On-Device model-source selection in the `Use Model` plist (C8)** — none of these were found in the bundled ToolKit identifier catalogs during this research and must be re-verified independently against the live ToolKit on the actual build machine before being assumed available or assumed absent.

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---|---|---|
| A1 UUID/OutputUUID wiring | Dumb state-engine build | Grep plist for orphaned OutputUUID refs; on-device "Unknown" chip check |
| A2 Magic vs named variable (display text) | Mirror-engine / Circle primitives | On-device visual check of every display string, not just validator |
| A3 GroupingIdentifier mismatches | Circle-ladder / exit-menu build | Manual trace of every If/Repeat/Menu block's Start→End pairing |
| A4 Dictionary value coercion | JSON schema + bootstrap | Force null/boolean edge cases; confirm guarded reads |
| A5 Number/text coercion in thresholds | Heat/Gravity/Pressure/Circle mapping | Manual test at every profile's 9 threshold boundaries |
| A6 Date parsing/arithmetic | Behavioural-day / session-timing | Test across a real 04:00 boundary and rapid app-switch timing |
| A7 Fabricated identifiers | Pre-build capability audit | Cross-check every action against ToolKit snapshot before authoring |
| A8 Parameter shape drift (OS26 vs 27, Notes markdown key) | Bootstrap (Note creation) | On-device: confirm Note body is non-empty, not just validator pass |
| A9 Validator false-passes | Cross-cutting, every phase | On-device behavioral test required before phase sign-off |
| A10 Signing/import failures | Distribution/signing + every re-test cycle | Confirm installed name has no `_signed` suffix; delete-before-reimport |
| B1 Overlapping OPEN/CLOSE runs | OPEN/CLOSE state-engine build | Rapid A→B→A app-switch stress test on device |
| B2 Duplicate OPEN triggers | OPEN handler build | Debounce-window test with rapid re-taps of the same app |
| B3 Partial/corrupt JSON writes | Bootstrap/self-heal build | Deliberately corrupt state.json and confirm recovery path |
| B4 iCloud sync latency | Bootstrap/state-storage build | Document file-location decision; test read-after-write |
| B5 04:00 rollover mid-session | Behavioural-day build | Simulate OPEN pre-04:00, CLOSE post-04:00 |
| B6 Cooldown attempts inflating Heat | Circle IX / Ice build | Repeated rapid OPENs during short test cooldown |
| B7 Heat decay from stale/missing timestamp | Heat/decay build | Test first-run and post-recovery decay separately |
| B8 Session ID collisions | OPEN handler build | Inspect recent_sessions history for duplicate IDs under rapid switching |
| B9 Manual invocation mid-session | Invocation-routing build (first phase) | Run "Test a Circle"/"Reset Today" while a real session is active |
| C1 Brightness readback unverified | Capability audit + environmental-safety build | Confirm no Get Brightness action exists; document fallback |
| C2 Volume readback unverified | Capability audit + environmental-safety build | Confirm no Get Volume action exists; document fallback |
| C3 Color Filters/grayscale unverified | Capability audit (first) | Confirm no grayscale action exists; document Ash fallback |
| C4 Accessibility settings clobbered | Environmental-safety build | Direct consequence of C1-C3 fallback; no separate build needed |
| C5 Lock Screen from automation context | Circle IX / Ice build | Test via real automation trigger, not manual run |
| C6 Actions forcing confirmation | Capability audit + OPEN-handler build | End-to-end automation-triggered test, not manual foreground run |
| C7 Use Model latency | Sentient-fork build | Build deterministic fallback first; measure perceptible delay |
| C8 Use Model On-Device selection unverifiable | Capability audit + Sentient-fork build | Confirm/deny plist-level model-source param; document deviation |
| C9 Malformed model output | Sentient-fork build (contract auditor) | Tolerant parse test with malformed/empty model responses |
| C10 Notes permission prompt mid-automation | Bootstrap build | Sequence first Notes use into manual bootstrap flow |
| C11 User disables automation | Cross-cutting; Control Room copy | Disable-rate tracked from first friend test onward |
| D1 Intervention fatigue | Mirror-engine + Sentient message selection | Trend-check contract-fidelity/rapid-return over calendar time |
| D2 Disablement as dominant failure | Cross-cutting product gate | Direct user conversation at end of Dumb and Sentient phases |
| D3 Over-verbal design vs dismissal-option | Exit-pathway build (equal priority to Mirror) | Audit time-to-exit at every Circle |
| D4 Model inventing facts/diagnosing | Sentient prompt + context-window build | Manual review of sample outputs against §14.1 known/unknown list |
| D5 Learned criticism association | Mirror-engine template authoring + Sentient prompt | Count positive vs critical templates; verify tone balance |
| D6 Redirecting into another app, not off-phone | Explore/exploit learning build | Check whether Close ever wins exploitation phase |
| D7 Note growth | Note-logging build (paired with OPEN/CLOSE) | Track Note length/entry growth rate during testing |
| D8 False psychological inference (Dumb copy) | Mirror-engine template authoring | Review Dumb templates against forbidden-language checklist |

---

## Sources

- `~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/BEST_PRACTICES.md` — variable wiring, display-vs-data-flow serialization, condition codes, comment discipline, known validator gaps (none currently exempted), signing/naming rules
- `~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/VARIABLES.md` — UUID/OutputUUID system, WFSerializationType rules, Aggrandizements
- `~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/CONTROL_FLOW.md` — GroupingIdentifier, control-flow modes, multi-condition Ifs, macOS 27 list-contains import trap, nesting depth
- `~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/PLIST_FORMAT.md` — root plist structure, action structure
- `~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/ACTIONS.md` — complete WF-namespace identifier list (used to confirm absence of getbrightness/getvolume/colorfilter/grayscale actions), askllm parameter list
- `~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/APPINTENTS.md` — AppIntent catalog, Accessibility section (306/164 actions enumerated, no Color Filters match found), Notes actions, Apple Intelligence/AppKit runtime actions
- `~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/AUTOMATION_TRIGGERS.md` — confirms "App opened" trigger requires user-local values (cannot be installed by a shared shortcut)
- `~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/DATE_TIME.md` — raw-Date-vs-formatted-string discipline, UNIX timestamp pattern
- `~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/SKILL.md` — Craig Loop validator protocol, "known validator gaps" policy
- `/Users/dougalhanson/Documents/Claude/Projects/Prosoche/PROSOCHE_Nine_Circles_Canonical_Strategy.md` §5 (technical viability), §21 (environmental safety), §30 (failure modes), §31 (build strategy), §32 (acceptance criteria)
- `/Users/dougalhanson/Documents/Claude/Projects/Prosoche/.planning/PROJECT.md` — Active requirements, Constraints, Context (dominant failure mode, hard iOS constraints)

---
*Pitfalls research for: PROSOCHĒ — Nine Circles (Shortcuts Playground build)*
*Researched: 2026-08-13*
