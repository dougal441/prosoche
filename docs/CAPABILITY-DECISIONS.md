# PROSOCHĒ — Capability Decisions

Decisions in this document are numbered `BD-NN` ("blocker decision"). They are **binding on later phases** — once recorded, a later plan does not silently re-litigate a BD entry; it either builds against it or raises a new, explicitly-flagged architectural question through the normal deviation process. `BD-01`..`BD-05` correspond to the five blockers named in `.planning/phases/01-capability-audit-config-foundation/01-CONTEXT.md`.

## Table of contents

| Decision | Title | Owning plan |
|---|---|---|
| BD-01 | Ash / Color Filters | 01-01 (this plan) |
| BD-02 | Dimming / brightness read-back | 01-04 |
| BD-03 | Silence / volume read-back | 01-04 |
| BD-04 | Use Model On-Device literal | 01-05 |
| BD-05 | Notes actions on the iOS target | 01-04 |

---

## BD-01 — Ash / Color Filters

**Question:** The Ash primitive (canonical strategy §11 Primitive B: "Grayscale where iOS can apply and restore it safely. Passive reduction of visual salience.") requires a system-level grayscale/Color Filters toggle. The capability audit (CAP-20 in `docs/BUILD-NOTES.md`) found no such action verified available to Shortcuts.app on iPhone. D-08 requires deciding Ash's fate among three named options. What should Ash do on the iOS build?

**Evidence:** CAP-20 in `docs/BUILD-NOTES.md` §4, and its supporting `DEV-01` entry in §5. Summary: `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` is the only Color-Filters-adjacent action found anywhere in the bundled ToolKit snapshots; it is present in the generic `toolkit-v63-tool-ids.json`/`toolkit-v78-tool-ids.json` snapshots but every parameter and its top-level platform tag in `toolkit-v78-first-party-parameter-keys.json` reads `platforms: ["macOS 27"]` only, and it is entirely absent from the iOS-27-Simulator-specific `toolkit-v78-ios27-tool-ids.json` snapshot. No grayscale read-back mechanism exists in any bundled snapshot. This is corroborated independently by `.planning/research/STACK.md` §3 row 10 and `.planning/research/PITFALLS.md` C3/C4.

**Options considered** (verbatim from D-08):

1. **Substitute a different visual-salience reduction.** Replace the system grayscale toggle with a different, verifiably-available mechanism that still reduces visual salience — e.g. Set Brightness (CAP-08, `is.workflow.actions.setbrightness`, confirmed present on both iOS 27 Simulator and macOS 27) dimmed toward the prototype's Dimming value, or a Shortcuts-native full-screen overlay if a verified action for one exists. *Not chosen as the primary path*, because Dimming is already a separate, distinct primitive (Primitive E) in the same sequence — collapsing Ash into a second Dimming call would remove a primitive from the tested sequence rather than substitute one, contradicting D-13's instruction to keep the sequence table intact, and canonical strategy §12 already places Ash and Dimming as separately testable slots specifically to compare passive-friction primitives independently.
2. **Require user opt-in to a PROSOCHĒ-managed configuration.** Ask the user, at import time or via a one-time Control Room setup step, to manually enable Color Filters/grayscale in iOS Settings → Accessibility once, and have PROSOCHĒ never touch the toggle programmatically — Ash then becomes "confirm the user is in their own pre-configured grayscale mode" rather than "toggle grayscale." *Not chosen*, because there is no verified read-back action for Color Filters state either (same CAP-20 evidence), so PROSOCHĒ cannot even confirm the opt-in configuration is currently active — the primitive would degrade to firing blind, which is materially worse than an honestly-skipped intervention, and it introduces a manual per-user Settings dependency this phase's D-01 constraint (native Shortcuts only, no companion app) is meant to avoid multiplying.
3. **Degrade Ash to a non-environmental variant.** Keep Ash as a distinct sequence entry but redefine what it *does*: instead of a system-level display change, it becomes a verified, self-contained Shortcuts behaviour that produces the same passive-friction *effect* (a still, low-salience moment) without touching any system accessibility setting — e.g. a brief full-screen text/Show Result pause with intentionally desaturated, low-contrast static copy (no colour, no imagery, no urgency), using only verified actions (`is.workflow.actions.showresult`/`is.workflow.actions.alert`-class primitives already required elsewhere in the build). *Chosen* — see Decision below.

**Decision:** Option 3 — degrade Ash to a non-environmental variant. Ash keeps its position in all three sequence orderings and keeps producing a passive, low-salience moment, but it is implemented as a verified, self-contained in-Shortcut visual pause (deliberately colourless/low-contrast static content shown via a verified display action) rather than a system Color Filters toggle. The exact display action and copy are a Phase 2/5 authoring decision, not decided here; what is binding here is that Ash is *not* implemented as `UAToggleColorFiltersIntent` or any invented grayscale-toggle identifier, and it never reads or writes the device's actual accessibility state.

**Rationale:** Canonical strategy §21's absolute rule for Grayscale/Color Filters states: "Accessibility settings may already be intentionally configured by the user. Do not blindly disable a pre-existing state. If Shortcuts cannot detect and restore the original condition safely, either: skip dynamic grayscale; or require the user to opt into a known PROSOCHĒ-managed configuration." CAP-20's evidence establishes Shortcuts cannot detect *or* restore the original Color Filters state on iOS at all (no read-back action found), which rules out any design that touches the real accessibility toggle — both the literal "toggle it live" reading of Primitive B and Option 2's opt-in-and-trust variant fail this test, because Option 2 still requires trusting an unconfirmable state. PITFALLS.md C4 independently names the same hazard: "a pre-existing accessibility configuration must never be blindly overridden," and notes there is no verified way to even detect whether a user already has grayscale on for a genuine vision-related need. Option 3 satisfies §21's "skip dynamic grayscale" branch precisely — it does not touch the system accessibility surface at all, so there is nothing to clobber and nothing that needs restoring — while still preserving Ash as a distinct, testable sequence entry rather than silently collapsing it into Dimming (which the sequence table treats as separately significant, per D-13's requirement to keep the sequences intact).

**Consequence for later phases:** Phase 5 (Circle primitive implementation) is explicitly gated on this decision. Phase 5 must build the primitive referenced here as **CIRC-02** to do exactly this: render a self-contained, low-salience visual pause using only actions verified elsewhere in this audit (e.g. `is.workflow.actions.showresult` / `is.workflow.actions.alert`-class display, deliberately colourless/low-contrast static copy, no imagery, no urgency framing) — CIRC-02 must **never** call `UAToggleColorFiltersIntent` or any other UniversalAccess accessibility-toggle identifier, and must never attempt to read the device's live accessibility configuration. If a future ToolKit snapshot or on-device test reveals a genuinely iOS-available, read-and-restore-capable grayscale action, that would be a new capability finding requiring a new deviation entry and a possible BD-01 revision — it is not assumed here.

**Requirement:** AUDIT-02

---

## BD-02 — Dimming and brightness read-back

**Question:** The Dimming primitive (canonical strategy §11 Primitive E: "Reduce display salience with safe brightness adjustment if reversible. Never set zero brightness. Never interfere with accessibility settings in a way that can strand the user.") requires both a way to change brightness and, per canonical strategy §21's absolute rule, a way to reliably read the original value back before changing it. `.planning/research/PITFALLS.md` C1 and `.planning/research/ARCHITECTURE.md` §9 both flagged, before this plan ran, that no brightness read-back action appeared anywhere in the earlier research pass. Per D-09, this could not be concluded before `Get Device Details` was actually checked directly against the bundled ToolKit data. What is Dimming's built form?

**Evidence:** CAP-16 and CAP-17 in `docs/BUILD-NOTES.md` §4. Summary: CAP-16 (`is.workflow.actions.setbrightness`, param `WFBrightness` float) is `VERIFIED`, cross-platform (`iOS 27 Simulator`, `macOS 27`), unchanged from the research base. CAP-17 (Get current brightness) is also `VERIFIED` — not `UNVERIFIED` as `.planning/research/STACK.md` §3 row 8, `.planning/research/PITFALLS.md` C1, and `.planning/research/ARCHITECTURE.md` §0/§9 all anticipated. The live re-run of the §3 evidence recipe queried `toolkit-v78-first-party-enum-cases.json` for the enum type (`getdevicedetails_wfdevice_detail`) backing `is.workflow.actions.getdevicedetails`'s (Get Device Details) single parameter (`WFDeviceDetail`) — a query none of the earlier research passes performed — and found a 12-case list that includes the literal case `Current Brightness`, cross-platform tagged `["iOS 27 Simulator","macOS 27"]`. This is real, local, bundled-file evidence, not the external-only Apple release-note corroboration the earlier research relied on; per the binding citation rule in `docs/BUILD-NOTES.md` §3, this is sufficient to promote CAP-17 above `UNVERIFIED`.

**Options considered:**

1. **Stateful capture-and-restore Dimming**, built directly on CAP-16 (Set Brightness) and CAP-17 (Get Device Details, `WFDeviceDetail = "Current Brightness"`), following the `settings_snapshot` pattern `.planning/research/ARCHITECTURE.md` §9 already designed for exactly this case (attempt the read; if it has any value, capture into `settings_snapshot` before applying the change; otherwise skip the stateful change for that run). *Chosen* — see Decision below.
2. **Message-only, non-stateful Dimming** (a Knock-style "the screen could be dimmer right now" text primitive, no system brightness change at all) — the fallback `.planning/research/ARCHITECTURE.md` §9 pre-designed for the case CAP-17 landed unresolved. *Not chosen as the default*, because CAP-17 carries genuine local ToolKit evidence of a usable read-back property, which is exactly the condition under which §21 permits a stateful change. Retained as the automatic per-run fallback whenever the read genuinely returns no value (see Decision) — this is not a discarded option, it is folded into the built form as its safety branch.
3. **Unconditional Set Brightness with no read-back at all** — not considered viable at any point; forbidden outright by §21's absolute rule regardless of any other consideration, including CAP-16's own strong identifier/parameter evidence.

**Decision:** Dimming is built as the stateful primitive described in Option 1, with Option 2 as its mandatory per-run safety branch, never as Option 3. Concretely: attempt `Get Device Details` with `WFDeviceDetail = "Current Brightness"`; if that read has any value, write `settings_snapshot.brightness = { original_value, changed_at: Now Epoch, changed_by_session_id: active_session.id }` — only if no un-restored snapshot already exists for that key, per `.planning/research/ARCHITECTURE.md` §9 — then apply `Set Brightness` at the prototype dim value (10–15% band, never zero, per CAP-16's Fallback cell). If the read returns no value on a given run, the brightness change is skipped entirely for that occurrence and Dimming's other, message-based friction (if any is authored into that Circle slot) carries it instead — a failed environmental read degrades one primitive to message-only for that run; it does not fail the whole Circle. This is a direct, evidence-driven consequence of CAP-17 landing `VERIFIED`: because a genuine, non-external, local-ToolKit-evidenced read-back path exists, §21's "if the original state cannot be read, do not make a stateful brightness intervention" clause is satisfied by wrapping every write in the has-any-value guard, not by refusing to write at all. Phase 5 must additionally add a defensive numeric-sanity check around the read (CAP-17's Fallback cell) — the exact output range/units of `Current Brightness` are not documented anywhere in this bundle, so a read that does not coerce to a plausible numeric value is treated identically to a missing read under the same guard.

**Rationale:** SAFE-03 ("any setting whose original value cannot be captured is left unchanged") is satisfied by the has-any-value guard around the Get Device Details read — the stateful branch only ever executes when a capturable original value was actually obtained; nothing is ever overwritten on the strength of an assumed or invented value. `.planning/research/PITFALLS.md` C4 (a user may already run reduced brightness deliberately for a vision-related need, with no way to detect that) is independently satisfied by the same guard: because Dimming's write is always preceded by a real capture into `settings_snapshot.brightness`, whatever the pre-existing value is — including a user's own deliberately-low setting — is what gets restored on CLOSE, Emergency Restore, or cooldown-natural-expiry, not silently discarded or overwritten with a PROSOCHĒ-chosen default. This is a materially different position from Ash/BD-01, where no read-back path was found at all (CAP-20, `NOT AVAILABLE`) and message-only was the only option consistent with SAFE-03/C4; here CAP-17's `VERIFIED` read path means the equivalent protection is achieved by restoration rather than by avoidance.

**Consequence for later phases:** Phase 5 builds CIRC-05 exactly as described above: Get Device Details read → has-any-value guard → `settings_snapshot` capture → Set Brightness (never zero, 10–15% band) → per-run skip-to-message-only if the read fails or fails its numeric-sanity check. Phase 4's CLOSE handler (SESS-07) restores `settings_snapshot.brightness` whenever present, per `.planning/research/ARCHITECTURE.md` §9's four restoration triggers (owning CLOSE, Emergency Restore, cooldown-natural-expiry; never a superseded CLOSE). SAFE-05 (Emergency Restore) must include this same restore step. Under this decision, `state.json`'s `settings_snapshot` field holds, at minimum, a `brightness` key (`{ original_value, changed_at, changed_by_session_id }`) whenever a Dimming write is currently outstanding — populated only when CAP-17's read actually returned a usable value for that specific run, and cleared to `{}` once every outstanding key has been restored; a restore step never runs for a value that was never captured. See the consistency note at the end of BD-03.

**Requirement:** AUDIT-03

---

## BD-03 — Silence and volume read-back

**Question:** The Silence primitive (canonical strategy §11 Primitive C: "Mute/reduce media audio only if PROSOCHĒ can safely capture and restore state. Never blast sound as punishment.") requires the same read-before-write discipline as Dimming, governed by the same §21 absolute rule. Per D-10, this could not be concluded before `Get Device Details` was actually checked for a usable volume property. What is Silence's built form?

**Evidence:** CAP-18 and CAP-19 in `docs/BUILD-NOTES.md` §4. Summary: CAP-18 (`is.workflow.actions.setvolume`) is `VERIFIED` with a confirmed, cross-platform two-parameter schema (`WFVolumeSetting` enum, cases `Media`/`Ringtone`; `WFVolume` float) — a positive divergence from `.planning/research/STACK.md` §3 row 9, which reported no schema found and treated the float parameter as a working assumption only. CAP-19 (Get current volume) is `VERIFIED` by the identical mechanism used for CAP-17: the same `getdevicedetails_wfdevice_detail` enum, looked up in `toolkit-v78-first-party-enum-cases.json`, includes the literal case `Current Volume` alongside `Current Brightness`, cross-platform tagged. This is real, local, bundled-file evidence, not the external-only corroboration `.planning/research/STACK.md` §3 row 9 and `.planning/research/PITFALLS.md` C2 relied on.

**Options considered:**

1. **Stateful capture-and-restore Silence**, built on CAP-18 (`Set Volume`, `WFVolumeSetting = "Media"`) and CAP-19 (`Get Device Details`, `WFDeviceDetail = "Current Volume"`), mirroring BD-02's structure exactly. *Chosen* — see Decision below.
2. **Weaker-but-real media-pause alternative**, evaluated per the do-not-fabricate protocol's priority order (`docs/BUILD-NOTES.md` §2, point 2a — a verified, documented alternative achieving a strictly weaker but real version of the same intent) before any consideration of skipping: `is.workflow.actions.pausemusic` (display name "Play/Pause"), params `WFPlayPauseBehavior` (enum `pausemusic_wfplay_pause_behavior`) and `WFMediaRoute` (`builtin_media_route`). Queried 2026-08-13: this identifier is present `True`/`True`/`True` across all three ToolKit id snapshots — the *only* capability audited across this entire document confirmed present in all three, including the iOS-27-Simulator snapshot — and its two-parameter schema is fully evidenced, cross-platform tagged, in `toolkit-v78-first-party-parameter-keys.json`. This is a genuinely verified action, cited because it was actually found, not invented. *Not chosen as the primary mechanism* because CAP-19 lands `VERIFIED` (a real, local, non-external read-back path exists for system volume itself), so the stronger stateful Silence primitive is permitted under §21 rather than required to fall back to a weaker one. Recorded here as a candidate secondary/companion action Phase 5 may layer alongside the volume-based primitive (an authoring decision, not decided here), since pausing playback reinforces the same intent — silencing the immediate audio trigger — through a second, independently-verified mechanism.
3. **Message-only Silence** (no volume manipulation at all) — the fallback `.planning/research/ARCHITECTURE.md` §9 pre-designed for a genuinely unresolved read path. *Not chosen as the default* for the same reason as BD-02's Option 2; retained as the mandatory per-run safety branch whenever the read returns no value.

**Decision:** Silence is built as the stateful primitive described in Option 1, with Option 3 as its mandatory per-run safety branch, never as an unconditional volume change. Concretely: attempt `Get Device Details` with `WFDeviceDetail = "Current Volume"`; if that read has any value, write `settings_snapshot.volume = { original_value, changed_at: Now Epoch, changed_by_session_id: active_session.id }` (same no-overwrite-of-a-true-original guard as BD-02) then apply `Set Volume` with `WFVolumeSetting = "Media"` (never `"Ringtone"`) and a target `WFVolume` that never exceeds the captured original value. If the read returns no value on a given run, the volume change is skipped entirely for that occurrence, matching BD-02's per-run degrade-to-message-only behaviour. Phase 5 may additionally invoke Option 2 (`pausemusic`) alongside the volume change as a second, independently-verified layer of the same intent, but that additional action is never a substitute for the has-any-value guard on the volume write itself.

**Rationale:** SAFE-02 ("volume is never increased and no startling output is produced") is enforced structurally by the decision's own constraint that the target `WFVolume` never exceeds the captured `original_value`, and by scoping every write to `WFVolumeSetting = "Media"` so the ringer is never touched. SAFE-03 is satisfied by the identical has-any-value guard used in BD-02 — the stateful branch only ever executes when a capturable original value was actually obtained, and whatever that original value is (including a level the user has deliberately set low, e.g. for a hearing-related reason, the volume analogue of `.planning/research/PITFALLS.md` C4) is exactly what gets restored, never silently discarded.

**Consequence for later phases:** Phase 5 builds CIRC-03 exactly as described above. Phase 4's CLOSE handler (SESS-07) restores `settings_snapshot.volume` whenever present, via the same four restoration triggers as BD-02 (`.planning/research/ARCHITECTURE.md` §9). SAFE-05 (Emergency Restore) must include this same restore step for volume. Under this decision, `state.json`'s `settings_snapshot` field holds a `volume` key (`{ original_value, changed_at, changed_by_session_id }`) whenever a Silence write is currently outstanding, populated only when CAP-19's read actually returned a usable value, cleared to `{}` once restored.

**Consistency note (binding on BD-01, BD-02, and BD-03 together):** All three of BD-01 (Ash), BD-02 (Dimming), and BD-03 (Silence) are governed by the identical canonical strategy §21 rule and all three write into and are restored via the same `settings_snapshot` / Emergency Restore machinery (`.planning/research/ARCHITECTURE.md` §9). BD-01 landed at the message-only end of that rule because CAP-20 found no read-back path *at all* for Color Filters, on any bundled snapshot, at any evidence tier. BD-02 and BD-03 land at the stateful capture-and-restore end because CAP-17 and CAP-19 each found a genuine, local-ToolKit-evidenced read-back path via Get Device Details that CAP-20's investigation had no equivalent of. All three decisions are the same rule applied honestly to three different evidentiary outcomes, not three different rules, and none of the three authorises a stateful environmental change whose original value cannot be captured on the specific run it fires.

**Requirement:** AUDIT-04

---

## BD-04 — Use Model On-Device selection literal

**Question:** The Sentient fork's central hard constraint (D-03: "Sentient uses the Apple On-Device model only. Never Private Cloud Compute, never ChatGPT, never a web API") requires hardcoding the `Use Model` action's `WFLLMModel` parameter to whatever plist enum string pins the On-Device source. Per D-11, this could not be concluded before the ToolKit's enum snapshots, the golden-shortcut corpus, and the prose reference docs were all actually checked for that literal. What is the built form of On-Device pinning?

**Evidence:** CAP-26 in `docs/BUILD-NOTES.md` §4, and its supporting `DEV-03` entry in §5. Summary: `is.workflow.actions.askllm` ("Use Model") and all five of its parameters — including `WFLLMModel`'s key and its typed-enum name `com_apple_shortcuts_wfask_llmmodel_parameter` — are fully evidenced and `VERIFIED`, present in all three bundled id snapshots including the iOS-27-Simulator-specific one (a stronger provenance signal than most other rows in this audit). Three recovery attempts were made for the enum's case list specifically: (1) `com_apple_shortcuts_wfask_llmmodel_parameter`, looked up as a key in `toolkit-v78-first-party-enum-cases.json`'s `types` object — absent, no matching key at all; a superficially similar key (`com_apple_generativeassistanttools_generative_assistant_extension_llmpartner`, 2 cases `chatGPT`/`other`) exists in that same file but belongs to an unrelated tool and was explicitly checked and rejected, not silently missed; (2) all 19 golden-shortcut XMLs searched for `WFLLMModel` and `askllm` — zero matches in any file, no real-world shortcut in the corpus uses this action; (3) the two worked `Use Model` examples in `EXAMPLES.md` both set `WFLLMModel` to the literal string `"Apple Intelligence"` — recorded, and explicitly labelled as **not** the answer, since it predates the iOS 26 three-way model picker (On-Device / Private Cloud Compute / Extension Model) that external corroboration (`.planning/research/STACK.md` §3 row 15, MacStories/TechCrunch/AppleInsider reporting, MEDIUM confidence, external-only) describes. No enum case list for the On-Device value exists anywhere in the bundled ToolKit snapshot.

**Options considered:**

1. **Guess a plausible enum string** (e.g. `"On-Device"`, `"On Device"`, an integer code) and hardcode it into the Sentient fork's `WFLLMModel` value. **Rejected outright, not merely deprioritised.** Per D-07, an invented identifier or literal is a defect, not a shortcut to a feature — and this specific literal is the single most consequential fabrication available in this project: it would pin a value into a signed, distributed Shortcut that a user believes routes their behavioural data entirely on-device (D-03's hard privacy constraint), when a wrong guess could just as easily route to Private Cloud Compute or the ChatGPT/Extension Model with no way for the user to detect the misconfiguration from the outside. No amount of plausibility (e.g. matching Apple's own UI copy) makes an unverified plist string safe to ship here.
2. **Wait for on-device confirmation before any Sentient-fork work begins**, blocking Phase 8 in its entirety until the round-trip happens. **Not chosen**, because AUDIT-06 explicitly permits a second, concrete, non-blocking outcome — re-planning the Sentient fork's On-Device guarantee around what the local toolchain has and has not established — and the do-not-fabricate protocol (`docs/BUILD-NOTES.md` §2, point 2b: "skipping the specific behavior entirely, if no safe verified alternative exists — this is explicitly correct, not a failure") directly supports building everything that does not depend on the literal now, rather than stalling all of Phase 8 on one unresolved value.
3. **Recover the literal by the on-device round-trip and re-plan the guarantee for whatever remains unresolved until that happens.** **Chosen** — see Decision below. This is Branch B of AUDIT-06's two permitted outcomes, combined with the exit path (Branch A) that closes it.

**Decision:** AUDIT-06's **Branch B** is taken: the literal was **not** recovered from the local toolchain (CAP-26's `UNRECOVERED-LOCALLY` token), and the Sentient fork's On-Device guarantee is **explicitly re-planned** rather than assumed or guessed. This re-plan is concrete:

**What Phase 8 may build now, before the literal exists** — none of the following depend on the model-source value, so all of them are unblocked: the `Use Model` action itself, wired with the parameters this audit has evidenced (`WFLLMPrompt`, `WFAllowWebSearch`, `FollowUp`, `WFGenerativeResultType="Text"`); the structured ALLOW/CHALLENGE/DENY parse (SENT-04) built as the tolerant contains-check CAP-27's Fallback cell and PITFALLS C9 require, defaulting unrecognised output to ALLOW, never DENY, never a crash; the deterministic Dumb-equivalent fallback path for every Circle II–VIII call (SENT-05); the compact local context window design (§28, SENT-13); and the system instruction (§14.6). Every one of these is buildable and testable today.

**What Phase 8 may not do until the literal exists** — write any plist value into `WFLLMModel` (leave the parameter unset/default rather than guess), and state anywhere in the product — Control Room Note, repository documentation, code comments — that On-Device is *enforced* by the shipped file. Neither is permitted while the literal remains `UNRECOVERED-LOCALLY`.

**What the product says instead, given D-03 and D-06:** because the Sentient fork cannot enforce the model source from the plist alone, the Control Room Note and the repository documentation (DIST-07) must say so plainly — in substance: "PROSOCHĒ's Sentient fork is designed to use Apple's On-Device model only. The shipped file cannot force this setting from outside; after import, open the Use Model action's own configuration and confirm the Model picker is set to On-Device." This is exactly D-06's requirement that PROSOCHĒ never claim a guarantee it does not have, applied to the one place in this build where the plist genuinely cannot enforce what the strategy wants — and it is what DIST-07 requires the repository documentation to state.

**What makes the guarantee real anyway, even with the literal unresolved:** the Dumb fork has zero Apple Intelligence dependency and runs fully on non-Apple-Intelligence iOS 26 iPhones (DUMB-01) — nothing about the Dumb fork's completeness depends on this decision at all. Every Sentient model call has a deterministic fallback (SENT-05), so a misconfigured or absent model source degrades to Dumb-equivalent behaviour rather than breaking the run. The model never controls Heat, Gravity, Pressure, thresholds, timers, exit selection, or Circle IX (SENT-12) — so even in the worst case, a model-source misconfiguration can degrade output quality and privacy posture (the model call might route somewhere other than on-device) but it structurally cannot corrupt state, strand the user, or override the deterministic engine that governs every safety-critical decision. This is the same class of protection BD-01/BD-02/BD-03's consistency note already established for the environmental primitives: a missing or unconfirmed capability degrades gracefully rather than silently failing unsafe.

**Exit condition:** UA-02 in `docs/BUILD-NOTES.md` §6 — the on-device round-trip (select On-Device in the Use Model action's Model picker in Shortcuts.app, Share and Copy the shortcut, paste into a plain `.xml` file, read `WFLLMModel`'s value back verbatim). The moment UA-02 is completed: CAP-26's literal-status token in `docs/BUILD-NOTES.md` is updated from `UNRECOVERED-LOCALLY` to `ROUND-TRIP-CONFIRMED` with the recovered value recorded verbatim; this BD-04 record is updated to note Branch A was subsequently reached; and Phase 8 hardcodes the confirmed literal into `WFLLMModel`, recording it as a verified-on-device fact (obtained by direct device round-trip) rather than a Playground-bundle fact. Until that happens, Phase 8 builds and ships everything listed above, and the product states its guarantee exactly as described.

**Rationale:** This decision is the do-not-fabricate protocol (`docs/BUILD-NOTES.md` §2) applied to the single highest-consequence literal in the whole project. Point 1 ("do not invent the identifier or parameter shape") is honoured by recording three genuine, named recovery attempts and refusing to write a candidate string when all three came up empty. Point 2b ("skipping the specific behavior entirely... is explicitly correct, not a failure") is honoured by re-planning Phase 8 around what is buildable now rather than stalling it. Point 3 ("record the deviation... surfaced in the Control Room Note copy so the user isn't misled") is honoured by the "what the product says instead" clause above, which is the DIST-07/D-06 obligation made concrete. Point 4 ("keep the Shortcut runnable") is satisfied because DUMB-01 and SENT-05 together mean nothing about this open item can strand the user or break a run — the deterministic, already-verified path always wins over the unverified enhancement, exactly as §2's closing sentence requires.

**Consequence for later phases:** Phase 8 (Sentient Fork & Dual Distribution) is directly gated on this decision. SENT-01 (On-Device only) is satisfied structurally, not by a plist guarantee, until UA-02 closes: Phase 8 must build the Sentient fork exactly as described in "What Phase 8 may build now," must not write a candidate `WFLLMModel` value, and must carry the "what the product says instead" copy into both the Control Room Note and the repository documentation (DIST-07) until UA-02 is recorded as complete. If UA-02 surfaces the literal, Phase 8 hardcodes it and the Control Room Note copy is updated to state the model source is enforced by the shipped file, no longer merely configured by the user after import.

**Requirement:** AUDIT-06

---

## BD-05 — Notes actions on the iOS target

**Question:** The entire Control Room onboarding path (canonical strategy §18) depends on four Notes actions — Find Notes, Create Note, Append to Note, and Open Note — none of which appear in the one platform-specific snapshot this ToolKit bundle carries (`toolkit-v78-ios27-tool-ids.json`). Per D-12, does the Control Room resolve as buildable on these four actions for the iOS target, and if the local toolchain cannot fully settle that, what is Phase 2 authorised to build on?

**Evidence:** CAP-07, CAP-08, CAP-09, CAP-10 in `docs/BUILD-NOTES.md` §4. Summary, re-run live against the bundled ToolKit rather than transcribed from `.planning/research/STACK.md`: all four identifiers (`is.workflow.actions.filter.notes`, `com.apple.mobilenotes.SharingExtension` and `com.apple.Notes.CreateNoteFromMarkdownLinkAction`, `is.workflow.actions.appendnote`, `is.workflow.actions.shownote`) are present in `toolkit-v63-tool-ids.json` — the generic, non-platform-segmented, pre-OS27 snapshot that `docs/BUILD-NOTES.md` §3 designates "the operative iOS-availability signal for pre-existing, long-standing actions" — and each has a documented parameter shape, either in the OS27 parameter-keys catalog (tagged `platforms: ["macOS 27"]`, a provenance fact about the capture build rather than proof of exclusivity, per §3's own description of that file) or, for `CreateNoteFromMarkdownLinkAction`, in independently cross-corroborating prose (`BEST_PRACTICES.md` line 121, `CHANGELOG.md` line 447). A direct, unfiltered substring search of `toolkit-v78-ios27-tool-ids.json` for any `com.apple.Notes.*`/`filter.notes`/`appendnote`/`shownote` identifier returns zero matches of any kind — the entire Notes namespace, not merely these four actions, is absent from that one narrow simulator capture, which `docs/BUILD-NOTES.md` §3 already names as the paradigm example of a bundled-data completeness gap rather than a genuine iOS restriction, distinct from CAP-20's Color Filters finding (BD-01) where the action was absent from the iOS snapshot *and* had no long-standing precedent as a real iOS action *and* independent domain knowledge confirms Color Filters has never been exposed to Shortcuts.app on iPhone. Notes actions, by contrast, have been standard first-party iOS Shortcuts actions for years and are independently well known to work on iPhone.

**Options considered:**

1. **Proceed on the CAP-07..CAP-10 evidence, gated by an on-device confirmation step.** Build the Control Room on the four Notes actions now, treating the v63/prose evidence as sufficient to authorise the build, but require the first live confirmation of all four actions (and specifically the CAP-08 `markdownContents`-vs-`markdown` empty-body risk) to happen during the deliberate manual bootstrap run, recorded as UA-01 (`docs/BUILD-NOTES.md` §6) and gating Phase 2. *Chosen* — see Decision below.
2. **Wait for on-device confirmation before any Phase 2 work begins.** Treat the absence from `toolkit-v78-ios27-tool-ids.json` as disqualifying pending a real-device test, blocking Phase 2 entirely until that test happens. *Not chosen*, because the identifier/parameter evidence for these four actions (long-standing generic-snapshot presence, prose cross-corroboration, and `docs/BUILD-NOTES.md` §3's own explicit acknowledgment that Notes actions are "unquestionably available on a real device") is considerably stronger than a bare absence-from-one-snapshot reading would suggest, and stalling the only onboarding path on a precaution the evidence does not actually support would cost real build time for no corresponding safety gain — the honest position is "authorised, but confirm early," not "blocked."
3. **File-based Control Room fallback**, built entirely from capabilities already carrying a `VERIFIED` row in this document: write the Control Room content to a file (e.g. `control-room.md`) alongside `state.json` using the audited Save File action (CAP-03, `is.workflow.actions.documentpicker.save`, confirmed `WFSaveFileOverwrite` boolean) and present it via an audited display action (e.g. CAP-S07's Show Result, or CAP-13's Open App pointed at the Files app). Evaluated honestly: the editable proforma round-trip ROOM-06 and ROOM-11 depend on survives only in degraded form. A user can still open and edit the file (in the Files app or any text editor), and PROSOCHĒ can still read it back via the already-established Get File + Detect Dictionary/Text pattern (CAP-02, CAP-04, DEV-02) — so the round-trip itself is not lost outright. What *is* lost: the native Notes-app ergonomics the whole design leans on (canonical strategy §5.4 — a human opens an app they already use daily, rather than navigating Files.app for a document they have to know to look for); the automatic iCloud-visible surfacing Notes provides "for free"; and, most concretely, Append to Note's true append semantics (CAP-09) — Save File has no selective-append mode (only whole-file overwrite, per CAP-03's evidence), so the ATTENTION LEDGER's continuously-growing append pattern (canonical strategy §5.4, `docs/BUILD-NOTES.md` PITFALLS-adjacent D7 concern) would require a full read-modify-write cycle on every single OPEN/CLOSE event instead of one Append action, and Sync My Profile (ROOM-11) would need to re-parse the entire document via Detect Text on every sync instead of a scoped Find/Append. *Not chosen as the primary path* given the strength of Options 1's evidence, but retained as the named fallback if UA-01's on-device confirmation surfaces a genuine failure.

**Decision:** Phase 2 is authorised to build the Control Room on the four Notes actions (CAP-07..CAP-10), on the strength of the v63 generic-snapshot presence, the documented parameter shapes (JSON catalog and/or cross-corroborating prose), and this document's own explicit, pre-existing acknowledgment that these are long-standing, unquestionably-real iOS actions — not stalled pending a blocking on-device wait. This authorisation is honest about its own limit: identifier presence in a bundled snapshot, even reinforced by prose cross-corroboration, is not the same thing as a confirmed on-device run, and this local toolchain cannot execute a Shortcut to close that gap itself. That gap is closed structurally, not assumed away, by UA-01 (`docs/BUILD-NOTES.md` §6): the first invocation of each of the four actions must happen inside the manual bootstrap run the user is actively engaged with, and Phase 2's build is not considered complete until UA-01's on-device confirmation — especially of CAP-08's `markdownContents`/empty-note-body risk — has been recorded. If UA-01 surfaces a genuine on-device failure of any of the four actions, Phase 2 falls back to Option 3 (the file-based Control Room), at the costs to the append-ledger pattern and native-app ergonomics described above.

**Rationale:** This decision applies the do-not-fabricate protocol's own escalation discipline (`docs/BUILD-NOTES.md` §2, points 3–4): the deviation risk here (Notes turning out to be genuinely unusable) is recorded and surfaced via UA-01 rather than assumed away, and a concrete, already-verified fallback exists so the Shortcut can never be stranded without an onboarding path even in the worst case. `.planning/research/PITFALLS.md` C10 (Notes actions prompting for permission mid-automation) is the specific mechanism UA-01's "first invocation inside the manual bootstrap run" requirement is designed against — sequencing every distinct Notes action's first use into the guided flow the user is present for, never into an automatic OPEN/CLOSE where the prompt could appear unseen.

**Consequence for later phases:** Phase 2 (Control Room build) is directly gated on this decision. ROOM-01 through ROOM-06 all depend on the Note existing and being writable; ROOM-02 and ROOM-03 (the automation setup instructions) depend specifically on CAP-08 producing a non-empty note body; ROOM-06 (the editable proforma) and, in Phase 7, ROOM-11 (Sync My Profile's extraction of the proforma back into state) depend on CAP-07/CAP-09's find-and-append mechanics remaining reliable across the Note's lifetime. If UA-01 surfaces a failure, Phase 2 must rebuild the onboarding surface on Option 3's file-based fallback, accepting the round-trip and ledger-append degradation described above.

**Requirement:** AUDIT-05

---

# REVISIONS — 2026-08-13, user correction

These supersede the decisions above where they conflict. Two Phase 1 conclusions were wrong or over-constrained.

## BD-01-R — Ash / Color Filters: SUPERSEDES BD-01

**Supersedes:** BD-01 (which degraded Ash to a non-environmental visual pause).
**New verdict for CAP-20:** **VERIFIED — usable on iOS.**

**Action:** `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` — display name **"Set Color Filters"**.

**Parameters** (from `toolkit-v78-first-party-parameter-keys.json`):

| Key | Type | Values |
|---|---|---|
| `operation` | enum `com_apple_universal_access_uasettings_shortcuts_operation` | `turn` (title "Turn") \| `toggle` (title "Toggle") |
| `state` | bool | trueString `On` / falseString `Off` |
| `ShowWhenRun` | bool | trueString `On` / falseString `Off` — set `Off` |

**Why BD-01 was wrong.** BD-01 read the entry's `platforms: ["macOS 27"]` tag and its absence from `toolkit-v78-ios27-tool-ids.json` as proof of macOS exclusivity. Both signals are artefacts, not facts:

1. `docs/BUILD-NOTES.md` §3 (the evidence-protocol table, row for the parameter-keys catalog) **already states** that a `macOS 27`-only tag is "a *provenance fact about which build the catalog was captured from*, not proof the action is macOS-exclusive." That reasoning was applied to the Notes actions (BD-05) and not to CAP-20. Applying it consistently reverses the verdict.
2. `toolkit-v78-ios27-tool-ids.json` is an **iOS Simulator** snapshot — 1206 ids versus 2731 in the full macOS snapshot. Simulators do not install the UniversalAccess accessibility extension. Confirmed independently: the iOS 26.5 simulator runtime on this machine contains no `UASettingsShortcuts` bundle and no `UniversalAccess.framework` at all, while still shipping a working Shortcuts.app. Absence from a simulator snapshot is therefore evidence about simulators, not about iOS.
3. On real iOS hardware the Accessibility section of the Shortcuts action list contains "Set Color Filters"; a grayscale toggle is among the most widely used community shortcuts. Asserted by the project owner and consistent with 1 and 2.

**Ash is therefore a real environmental primitive, and a fully restorable one.** `operation: turn` with an explicit `state` is a *set*, not a blind toggle — PROSOCHĒ never has to infer the current value to restore it.

**Design (Phase 5, CIRC-02):**
- Apply: `operation = turn`, `state = On`, `ShowWhenRun = Off`.
- Restore on CLOSE, Emergency Restore, and cooldown expiry: `operation = turn`, `state = Off`.
- Never use `operation = toggle` — a toggle depends on unknown prior state and can strand the user filtered.

**Canonical §21 compliance.** There is still no read-back for Color Filters, so PROSOCHĒ cannot detect a pre-existing user-configured filter and would clear it on restore. §21 explicitly permits the remedy: *"require the user to opt into a known PROSOCHĒ-managed configuration."* Ash is therefore opt-in via `safety.ash_managed_color_filters` (default `true`), and the Control Room Note states that PROSOCHĒ manages Color Filters and will leave them off after an intervention. A user who has deliberately configured Color Filters sets the flag `false` and Ash falls back to BD-01's non-environmental visual pause, which remains implemented as the fallback branch.

**Consequence:** `DEV-01` is withdrawn — Ash needs no deviation. Phase 5 builds CIRC-02 on the real action with the opt-in guard and the BD-01 pause as fallback.

**Requirement:** AUDIT-02

## BD-04-R — Model source: SUPERSEDES BD-04's hard constraint

**Supersedes:** BD-04's requirement that Sentient must be On-Device or make no claim.
**Change authorised by the project owner:** the hard On-Device-only privacy constraint is **relaxed**. Private Cloud Compute is acceptable.

**What this changes:**
- Sentient may ship with the model source unset in the plist, and On-Device *preferred* rather than *required*.
- Private Cloud Compute is an acceptable runtime outcome. ChatGPT / third-party extension models remain excluded — they are a different trust boundary and the strategy's exclusion of them stands.
- Phase 8 is **no longer gated** on recovering the `WFLLMModel` literal. UA-02 is downgraded from a gate to an optional improvement: if the literal is recovered by round-trip, pin On-Device; otherwise ship without the key and instruct the user in the Note.
- The still-binding rule from BD-04 is unchanged and is the important one: **do not write a guessed `WFLLMModel` value.** An invented enum could silently route somewhere unintended. Omitting the key is safe; guessing it is not.

**Product copy consequence:** Sentient says it prefers Apple's on-device model and that the user selects the model source after import — not that on-device is enforced.

**Requirement:** AUDIT-06

## BD-01-R2 — Ash / Color Filters: SUPERSEDES BD-01-R's build recipe

**Supersedes:** BD-01-R's **Action**, **Parameters**, and **Design** sections. BD-01-R's
*conclusion* — that Ash is a real, restorable environmental primitive on iOS — is upheld
and strengthened; only the identifier and parameter serialization it prescribed were wrong.

**Verdict for CAP-20:** **VERIFIED — donor-confirmed on iOS 26.**

**Evidence tier upgrade.** BD-01 reached `NOT AVAILABLE` from catalog data. BD-01-R
reversed that from catalog *reasoning* (simulator-artefact argument) plus owner assertion.
BD-01-R2 rests on tier-1 evidence: `.planning/debug/Set Colour Filters.shortcut`, exported
from the owner's iPhone and decrypted via the AEA1 round-trip, plus Apple's own
`AccessibilityUtilities.framework` intentdefinition. Full workings:
`.planning/spikes/005-ios-color-filters-identifier/README.md`.

**Action (corrected):**
`com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`

Not `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` — that is the
**macOS twin**. iOS ships the private `AX*` variant under an `AXSettingsShortcuts` container
mirroring the macOS `UASettingsShortcuts` one. The AX identifier is absent from all three
bundled ToolKit snapshots (v63, v78, v78-ios27); this is a catalog gap, and the donor is the
only local evidence of it. The Playground's own `APPINTENTS.md` line 116 already documents
this `AX*` / `UA*` split for two sibling accessibility toggles.

**Parameters (corrected) — integers, not enum-id strings and not bools:**

| Key | Type | Cases | Notes |
|---|---|---|---|
| `state` | Integer (enum `State`) | `unknown` = 0, **`on` = 1**, **`off` = 2** | Donor emits `<integer>1</integer>` |
| `operation` | Integer (enum `Operation`) | `unknown` = 0, **`turn` = 1**, **`toggle` = 2** | Donor **omits** it (elided default) |

Case indices are from Apple's own `Intents.intentdefinition`
(`/System/Library/PrivateFrameworks/AccessibilityUtilities.framework/Versions/A/Resources/Base.lproj/`),
archived at `.planning/spikes/005-ios-color-filters-identifier/AXToggleColorFilters-intentdefinition.txt`.

**There is no `ShowWhenRun` parameter on the iOS intent.** BD-01-R's instruction to set it
`Off` applies only to the macOS catalog row. Do not author it.

**Note that OFF is `2`, not `0` and not `<false/>`.** A bool intuition — the shape BD-01-R
prescribed — gets the restore write wrong, which is the failure mode that strands a user
filtered.

**Design (Phase 5, CIRC-02) — corrected:**
- Apply: `state = 1`. Mirror the donor exactly and omit `operation` (donor-verified shape),
  or set `operation = 1` (`turn`) explicitly — Apple-schema-verified, but not donor-verified
  in serialization.
- Restore on CLOSE, Emergency Restore, and cooldown expiry: `state = 2`.
- Never `operation = 2` (`toggle`) as the apply/restore mechanism — it depends on unknown
  prior state and can strand the user filtered. Unchanged from BD-01-R.

**Canonical §21 compliance — unchanged, with one new lead.** No `Get*`/`Query*` intent for
any accessibility setting exists anywhere in the framework's 35 intents, so there is still
no non-destructive pre-read of Color Filters state. BD-01-R's remedy therefore stands
verbatim: Ash is opt-in via `safety.ash_managed_color_filters` (default `true`), the Control
Room Note discloses that PROSOCHĒ manages Color Filters and leaves them off after an
intervention, and a user who deliberately runs Color Filters sets the flag `false` to get
BD-01's non-environmental visual pause instead.

*New lead, not a capability:* all 24 `Toggle*` intents declare a `state` **response**
parameter (Integer, enum `State`). If Shortcuts surfaces it as a consumable action output on
iOS, a `toggle`-then-`turn` probe could read prior state back at the cost of one visible
flicker. Unverified — it is a post-operation read, and whether the response is exposed at all
is untested. Recorded as the next donor test in spike 005; **must not** be built against
until a donor confirms it.

**Consequence:** DEV-01 stays withdrawn (BD-01-R). Phase 5 builds CIRC-02 on the corrected
identifier and integer parameters, with the opt-in guard and the BD-01 pause as fallback.

**Requirement:** AUDIT-02
