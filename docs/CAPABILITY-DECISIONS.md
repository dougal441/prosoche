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
| BD-06 | Circle naming, primitive roster, and slot allocation | Addendum 01 design pass (2026-08-16) |

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

**Addendum — floor corrected [Phase 9, experimental fork, 2026-08-16]:** The "never zero, 10–15% band" clause above was written on the premise that `WFBrightness = 0.0` produces a literal, unusable black screen, and treated avoiding that value as itself a safety requirement. User-reported on-device observation corrects this: iOS's practical brightness minimum is dim, not black — the screen stays visible at the floor. This does not change the has-any-value guard or the restore mechanism, which were always the actual safety-load-bearing parts of this decision (see Rationale above — SAFE-03 is satisfied by capture-and-restore, not by floor avoidance). It changes only the target value: on this experimental fork, Dimming may target the device's true minimum rather than an artificial 10–15% band, *contingent on Phase 9 device-proving the capture/restore loop* under real failure modes (force-quit, device restart, missed CLOSE, overlapping sessions) per `.planning/todos/pending/2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md`. This is a user report, not yet independently device-verified by this evidence chain — treat as provisional until Phase 9's own on-device testing confirms it (same evidence-hierarchy standard as the rest of this document: device ground truth first, but recorded and re-checked, not merely asserted). Main line (`docs/CAPABILITY-DECISIONS.md` as it stands on `main`) is unaffected; this addendum applies to this branch only.

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

> **Outcome superseded — see BD-04-R (constraint relaxed) and BD-04-R2 (Branch A reached: the
> literal *was* recovered, `Apple Intelligence on Device`).** The record below is retained
> unaltered: its reasoning — above all the refusal to guess the literal — is why the device
> round-trip happened, and it remains binding. Read BD-04-R2 before acting on the gate or the
> "what the product says instead" clause below. (The guarantee copy itself is unchanged; only
> the reason it is unchanged has moved.)

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
BD-01-R2 rests on tier-1 evidence: **three** donors exported from the owner's iPhone and
decrypted via the AEA1 round-trip — `.planning/debug/Set Colour Filters.shortcut` (On),
`.planning/debug/Donor 9.shortcut` (Toggle, plus an untouched instance), and
`.planning/debug/Donor 9.1.shortcut` (Off) — which between them pin every value CIRC-02
writes. Full workings: `.planning/spikes/005-ios-color-filters-identifier/README.md`.

**Action (corrected):**
`com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`

Not `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` — that is the
**macOS twin**. iOS ships the private `AX*` variant under an `AXSettingsShortcuts` container
mirroring the macOS `UASettingsShortcuts` one. The AX identifier is absent from all three
bundled ToolKit snapshots (v63, v78, v78-ios27); this is a catalog gap, and the donor is the
only local evidence of it. The Playground's own `APPINTENTS.md` line 116 already documents
this `AX*` / `UA*` split for two sibling accessibility toggles.

**Parameters (corrected) — `state` is a bool-as-integer; `operation` is a string that should be omitted:**

| Key | Serialized as | Values | Donor evidence |
|---|---|---|---|
| `state` | integer, **boolean-valued** | **`1` = On, `0` = Off** | `1` — Set Colour Filters, Donor 9. `0` — Donor 9.1 |
| `operation` | **string** (enum case id) | `toggle` when chosen; **elided when Turn** | `"toggle"` — Donor 9. Elided on both the On and Off donors |

`.planning/debug/Set Colour Filters.shortcut` emits `state` `<integer>1</integer>` with no
`operation`. `.planning/debug/Donor 9.shortcut` emits `operation` `<string>toggle</string>`
alongside `state` `<integer>1</integer>`, plus a second fully parameter-less instance.
`.planning/debug/Donor 9.1.shortcut` is that same instance (same UUID) configured **Off**, and
emits `state` `<integer>0</integer>` with no `operation`. Archived at
`.planning/spikes/005-ios-color-filters-identifier/`.

**`off` is `0`, not `2`, and Apple's own schema is misleading here.** The
`AccessibilityUtilities.framework` intentdefinition declares `state` as `Integer` with a
`State` enum of `on`=1 / `off`=2. Shortcuts does not use those indices — it renders a
`State`-typed enum as an On/Off switch and writes a plain boolean as an integer. The macOS
ToolKit catalog, which typed `state` as `bool` with trueString `On` / falseString `Off`, was
right all along. **Never take an `.intentdefinition`'s declared type or case indices as the
plist encoding**; it describes the intent's type system, not what Shortcuts writes.

**There is no `ShowWhenRun` parameter on the iOS intent.** BD-01-R's instruction to set it
`Off` applies only to the macOS catalog row. Do not author it.

**Design (Phase 5, CIRC-02) — final, every value donor-confirmed:**
- Apply: `state = 1`. Omit `operation`.
- Restore on CLOSE, Emergency Restore, and cooldown expiry: `state = 0`. Omit `operation`.
- **Omit `operation` in both legs.** `turn` is its elided default — both the On and the Off
  donors write no `operation` key at all — so PROSOCHĒ never needs the `"turn"` literal,
  which is the one literal in this investigation no donor has ever emitted.
- Never `operation = "toggle"`: it depends on unknown prior state and can strand the user
  filtered. Unchanged from BD-01-R. (Donor 9 uses `toggle`; it is a probe, not a model.)

**No gate remains on the write path.** Both legs are donor-confirmed, so Phase 5 can build
and ship CIRC-02's apply and restore without further device evidence. The only outstanding
Color Filters question is the optional read-back enhancement below.

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

---

## BD-06 — Circle naming, primitive roster, and slot allocation

**Owning work:** the design pass preceding `PROSOCHE_Build_Addendum_01.md`'s application
(2026-08-16). Binding on the Ash rebuild, the Voice dispatch fix, the Dimming/Silence
distinct-Circle work, and the Exile split — all four of which independently claim Circle
positions and would otherwise each re-cut the same table.

**Question:** Addendum 01 §1 renames the nine Circles to Dante's *Inferno* and §5 binds each
Dante name to one intervention. Simultaneously, four in-flight todos change the intervention
roster: Ash becomes a real Color Filters toggle, Voice becomes its own dispatched primitive,
Dimming and Silence become distinct Circles in every sequence, and Exile splits in two. That
takes the roster to **ten primitives for nine slots**
(`.planning/todos/pending/2026-08-16-split-exile-into-two-circles.md` step 5, which names
this as "the single decision that blocks all three in-flight Circle todos"). What are the
Circles called, what is the roster, and which primitive fires where?

### Decision 1 — Dante names are *positional*, not intervention names

Circle 1 is **Limbo** and Circle 9 is **Treachery** regardless of which intervention fires
there. The Dante name labels the *depth*; the sequence table decides the *intervention*.

**Rationale — this is forced, not preferred.** PROSOCHĒ ships three sequences
(`Classic` / `BlackMirror` / `Ambient`, `src/CONFIG-BLOCK.md`) which deliberately order the
interventions differently at the same Circle numbers. A fixed name↔intervention binding
therefore cannot survive a sequence switch: under `Ambient`, Circle 1 is Black and White,
not Pause. Since Pressure resolves to a Circle *number* and the sequence array resolves that
number to an intervention, the only stable thing a Dante name can attach to is the number.

Addendum 01 §5's table is consequently read as **the `Classic` sequence expressed in renamed
intervention terms** — which is exactly what it is; see the verification under Decision 4.

### Decision 2 — the names keep Dante's canonical order

| Circle | Name |
|---|---|
| 1 | Limbo |
| 2 | Lust |
| 3 | Gluttony |
| 4 | Greed |
| 5 | Wrath |
| 6 | Heresy |
| 7 | Violence |
| 8 | Fraud |
| 9 | Treachery |

The user's instruction was "named as they are in the book… pick which ones you think fit
best, the order doesn't matter" — i.e. the ordering across positions was explicitly free.
Canonical order is chosen *because* it fits best, not by default: Dante's descent is itself
an escalation, which is the same shape as PROSOCHĒ's, and it puts the strongest single fit
at the position that matters most. **Circle 9 is Treachery — Cocytus, a frozen lake — and
Circle 9's intervention is Ice/Frozen in all three sequences.** Circle 1 is Limbo, the
circle with no torment, and Circle 1 is a bare factual knock. Circle 7 is Violence, which
in Dante includes violence against the self, and Circle 7 is the Mirror.

### Decision 3 — the roster is ten primitives; each sequence uses nine of them

Nothing is dropped from the product. `sequences` is already per-sequence and there has never
been a rule that every primitive appears in every ordering — with ten primitives, each
nine-slot sequence simply selects nine.

Intervention names follow Addendum 01 §5, extended for the Exile split:

| Internal primitive | Shipped name | Status entering this decision |
|---|---|---|
| Knock | **Pause** | built |
| Ash | **Black and White** | alert-only; real Color Filters to be built |
| Silence | **Silence** | built; restore device-unproven |
| Confession | **Intention** | built |
| Dimming | **Dim** | built; restore device-unproven |
| Exile (straight) | **Eject** | built (bare Home Screen) |
| Exile (routed) | **Redirect** | new — lands the user in a deterministically selected exit |
| Mirror | **Mirror** | built |
| Voice | **Loud Mirror** | dispatches nothing; to be built |
| Ice | **Frozen** | built |

`Eject` is this decision's own coinage; Addendum 01 §5 supplies every other name, and its
`Redirect` is taken as the *routed* Exile, which is what the word describes.

### Decision 4 — slot allocation

| Circle | Name | Classic | BlackMirror | Ambient |
|---|---|---|---|---|
| 1 | Limbo | Pause | Pause | Black and White |
| 2 | Lust | Black and White | Intention | Silence |
| 3 | Gluttony | Silence | Black and White | Dim |
| 4 | Greed | Intention | Mirror | Pause |
| 5 | Wrath | Dim | Silence | Intention |
| 6 | Heresy | Redirect | Eject | Redirect |
| 7 | Violence | Mirror | Dim | Mirror |
| 8 | Fraud | Loud Mirror | Loud Mirror | Loud Mirror |
| 9 | Treachery | Frozen | Frozen | Frozen |

`Classic` and `Ambient` take **Redirect**; `BlackMirror` takes **Eject** — the colder,
unnegotiable ejection suits that sequence, and it gives every primitive at least one home.
Each column preserves its source ordering's identity: `Classic` is the reference escalation
from `src/CONFIG-BLOCK.md`, `Ambient` still leads with the three environmental primitives,
`BlackMirror` still surfaces the Mirror early (Circle 4).

**Verification against Addendum 01 §5.** The addendum's table reads Limbo=Pause,
Lust=Black and White, Gluttony=Silence, Greed=Intention, Wrath=Dim, Heresy=Redirect,
Violence=Mirror, Fraud=Loud Mirror, Treachery=Frozen. That is the `Classic` column above,
entry for entry. The addendum's own mapping is therefore *reproduced exactly* by this
decision rather than reinterpreted — independent confirmation that reading its table as
per-sequence is the intended reading.

### Decision 5 — combined sequence entries are abolished, and dispatch becomes an exact match

`BlackMirror` previously carried three combined entries — `Ash+Confession`,
`Silence+Mirror`, `Dimming+Mirror`. All three are gone: every slot in the table above names
exactly one primitive. This is what the user's "Dimming and Silence each as its own distinct
Circle" decision requires, and it buys a defect-class elimination for free.

`primitive_dispatch()` currently matches the sequence entry with **condition code 99
("contains")** solely to make the combined entries work. That choice is precisely why
Circle 8 shipped dead: the entry `"Voice"` contained no emitted branch name and silently
matched nothing, with no error
(`.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md`). With no combined
entries left, dispatch moves to **condition code 4 ("string is")** — an exact match, under
which an unmatched entry is a build-time failure rather than a silent runtime no-op.

**Binding build guard.** Every distinct primitive name appearing in any `sequences` array in
`src/CONFIG-BLOCK.md` must have exactly one matching dispatch branch in the generated
actions, and every dispatch branch must be named by at least one sequence entry. This is an
eighth class alongside the seven parameter-defect axes in `.claude/CLAUDE.md`, and it is
invisible to the validator, the ToolKit catalog, and the signed-artifact decrypt. It is
written **during the rename**, not after it, because a mass rename across three sequence
arrays and ten dispatch branches is exactly the operation it exists to catch.

### Decision 6 — the routed Exile lands the user directly

**User decision, 2026-08-16.** `Redirect` ejects *into* the deterministically selected exit
without offering a "Take suggested exit / Choose another" menu first. That is what makes it
a Circle rather than a second Leaving menu, and it keeps the involuntary path genuinely
involuntary. The exit is still recorded through `record_exit_and_route()`, so the
return-time sample is captured and the routed Circle feeds the same learning loop as the
voluntary path.

Selection remains deterministic — `select_exit()` unchanged, rotate-then-exploit with a
counter-modulo epsilon step. No `is.workflow.actions.number.random`, no shuffle, nowhere in
the exit path. This reaffirms the standing decision in `.planning/STATE.md` and extends it
across both Exile Circles.

**Consequence for later work:** the four in-flight Circle todos build against the table in
Decision 4 and do not re-cut it. The Circle matrix in
`.planning/todos/pending/2026-08-16-device-uat-nine-circles-and-sequence-switching.md` is
re-cut once, here, rather than after each of them.

**Requirement:** AUDIT-02 (extends), CIRC-02, CIRC-06, CIRC-08

---

## BD-04-R2 — Use Model model source: **Branch A was reached**

**Supersedes:** BD-04's *outcome* (Branch B — "the literal was not recovered") and BD-04-R's
contingency ("ship without the key if the literal is never recovered"). BD-04's **reasoning**
is not superseded and is not rewritten: refusing to guess the literal was correct, and it is
the reason a device export was needed at all. BD-04-R's still-binding rule — **never write a
guessed `WFLLMModel` value** — also stands unchanged, and is now moot in the good direction:
the value is not guessed, it is measured.

**Recorded 2026-08-17. The recovery itself happened 2026-08-13; only the audit trail was stale.**

**Branch A is reached.** BD-04's exit condition has been satisfied in full:

```
WFWorkflowActionIdentifier = is.workflow.actions.askllm
WFLLMModel                 = Apple Intelligence on Device      <- exact string, verbatim
```

**Evidence:** `docs/device-evidence/UseModel-OnDevice.xml` line 17 — the plist of a shortcut
built on the owner's own iPhone (iOS 26) with **On-Device** selected by hand in the Model
picker, exported and recovered here via the `aea decrypt` + `aa extract` procedure recorded in
`docs/BUILD-NOTES.md` §11. Committed in `013a217`. This is tier-1 device evidence — the highest
tier in this project's evidence hierarchy — not a ToolKit-bundle inference. CAP-26's literal
status token is `ROUND-TRIP-CONFIRMED`; DEV-03 is closed; UA-02 is closed.

**One incidental correction, worth recording.** UA-02's stated rationale included the claim
that a signed `.shortcut` "cannot be read back as plaintext." That is false — the AEA1 archive
is *signed*, not encrypted, and unlocks with the leaf certificate's public key. It is left in
place in `docs/BUILD-NOTES.md` §6 as the record of what was believed, with §11 as the
correction. The part of the rationale that held is the part that mattered: the picker selection
genuinely required an Apple-Intelligence-capable device.

**What this changes:**

- Phase 8 **writes** `WFLLMModel = Apple Intelligence on Device`. Already done —
  `tools/build_sentient.py:29`, annotated `# direct device-export evidence`.
- BD-04's prohibition on writing any `WFLLMModel` value is lifted **for this one measured
  literal only**. Any other value would still be a guess and is still forbidden.
- BD-04-R's relaxation to Private Cloud Compute is **no longer needed** to ship, though it
  remains authorised as a fallback if this key is ever rejected on an older device.
- BD-04's requirement of a deterministic fallback for every Sentient model call (SENT-05) is
  **unchanged and still mandatory**. Recovering the literal does not remove it: the model can
  still fail, stall, or return malformed output, and Sentient must degrade to Dumb-equivalent
  behaviour rather than break the run.

**What this does NOT change — the guarantee copy stays as it is.** The literal establishes what
the shipped **file requests**. It does not establish what the **runtime does**. No one has yet
confirmed on device that `Use Model` actually runs with **no network available** — that it
cannot silently fall back to Private Cloud Compute despite the On-Device literal. That check
needs an Apple-Intelligence-capable iPhone (15 Pro or later) with Wi-Fi and cellular both off,
and it is **the single remaining open item on this capability**.

Therefore BD-04's "what the product says instead" copy — and BD-04-R's "prefers on-device, user
selects the source after import" framing — **remain in force verbatim** in the Control Room
Note, the README, and any release text. Nothing user-facing may be upgraded to an enforced
on-device claim on the strength of the literal alone. Per D-06, PROSOCHĒ does not claim a
guarantee it has not demonstrated, and a literal that validates while silently routing to PCC
would be worse than making no claim at all. This is **not** to be described as verified.

**Requirement:** AUDIT-06 (now satisfied by its primary branch, not only the permitted alternative)

---

## BD-06-A1 — Purgatory replaces Limbo as the middle profile; Circle 0 is named The Indifferent

**User decision, 2026-08-17, taken mid-Phase-11 (wave 3 not yet dispatched).** This is an
**amendment to BD-06**, not a re-litigation of it. BD-06's five load-bearing decisions —
positional names, canonical Dante order, ten primitives for nine slots, combined entries
abolished with dispatch at condition 4, and the routed Exile landing directly — all stand
unchanged. Waves 1 and 2 shipped against them and are not revisited.

### Amendment 1 — the middle profile is renamed `Limbo` → `Purgatory`

**Why this is a correction and not a preference.** BD-06 made `Limbo` the positional name of
**Circle 1**. `Limbo` was already the name of the **middle profile**. One word therefore named
two different things at two different levels of the model — a depth and a pace — and BD-06
created that collision rather than inheriting it.

Renaming the profile dissolves the collision at the root instead of mitigating it in copy,
and it makes the three profiles the three *canticles* of the Commedia — **Paradise /
Purgatory / Inferno** — which is the more faithful reading. `Limbo` is a circle, not a
canticle; it was doing double duty. Circle 1 keeps the name `Limbo` per BD-06 Decision 4.

**Scope: rename everywhere.** The profile menu, both threshold key sets
(`thresholds.Limbo` → `thresholds.Purgatory`), both cooldown keys
(`cooldown_seconds.Limbo` → `cooldown_seconds.Purgatory`), the import-question prompt and
its default, the bootstrap normalisation fallback, `src/CONFIG-BLOCK.md`,
`docs/state_engine_self_check.py`'s threshold table, and `docs/BUILD-NOTES.md`. Both forks.

**Supersedes the plan-11-03 mitigation.** Plan `11-03` was authored to *disambiguate the two
Limbos in user copy and rename neither*, with an acceptance criterion asserting the profile
menu still read `['Paradise','Limbo','Inferno']`, and threat `T-11-16` mitigated by labelling.
That approach is withdrawn. The menu must now read `['Paradise','Purgatory','Inferno']` and
`T-11-16` is **eliminated rather than mitigated** — the two names no longer collide, so there
is nothing left to disambiguate.

### Amendment 2 — Circle 0 is named **The Indifferent**, in documentation only

Circle 0 is PROSOCHĒ's silent band: state accumulates, nothing is shown. It had no name.
It is now named **The Indifferent**, after Dante's *ignavi* — the uncommitted, who are
refused by both Heaven and Hell and are placed in the vestibule of the Inferno, **before**
Circle 1. That is exactly Circle 0's position in this model, so the name is positionally
correct in the same sense BD-06 Decision 1 requires of Circles 1–9.

**Scope: this decision record and build documentation only.** The name does **not** reach any
user-facing surface this phase — not the Control Room Note, not the Mirror or status
telemetry, not the Test-a-Circle menu. `verify_circle_zero_silence()` in
`tools/build_state_engine.py` structurally enforces that Circle 0 shows nothing at all on the
OPEN path, and that guard stays green and unmodified. Naming the band is not the same as
surfacing it.

### Amendment 3 — there is no installed base to protect

**User statement, 2026-08-17:** PROSOCHĒ is to be treated as a **new, as-yet-undeployed
product**. The only existing installs are the owner's own testing. Old `state.json` files are
explicitly not a consideration.

**Why this is recorded here rather than assumed.** Renaming a profile changes live Config key
paths, and this project's verified runtime semantics are that a **dotted read with any missing
segment is a hard error**, not a silent miss (`.claude/CLAUDE.md`). A device holding
`profile: "Limbo"` would therefore hard-error on `thresholds.Purgatory` at its next OPEN. That
consequence is real; it is **accepted** because there is no population it can harm.

**Consequence for plan `11-04`.** `11-04` exists to stop on the `schema_version` 2→3 question,
rated `one-way` because a bump discards every installed device's accumulated heat, gravity,
pressure, rolling windows and exit-learning record. That premise no longer holds: there is no
accumulated record to discard. The question is **answered by this amendment** — a bump is free,
and no migration, dual-key alias, or read-time normalisation is to be built. `11-04` remains as
a recording task and no longer carries a blocking one-way gate.

**No behavioural claim.** DIST-03 is still open and no iPhone is connected. Nothing in this
amendment is device-verified; it is a naming and scope decision recorded before the work.

**Requirement:** AUDIT-02 (extends), CIRC-02, ROOM-01, ROOM-02

---

## BD-06-A2 — the Find-Notes lookup operator is RETAINED at `contains` after the title shortened

**Recorded 2026-08-17, plan 11-03 wave 3. This is a deviation record, not a new decision:**
it records that a proposed change was **declined**, why, and what evidence would reverse it.

### What changed, and what it widened

Build Addendum 01 §4 shortens the Apple Note's user-facing title from
`PROSOCHĒ — Control Room` to the bare product name `PROSOCHĒ`, at all three sites that
decide the Note's identity — the Find-Notes lookup predicate, the body's H1 heading, and the
Create Note `name` parameter. All three moved in one commit; `docs/note_identity_check.py`
asserts them against a single `EXPECTED_TITLE` constant so they cannot drift apart.

The lookup predicate is a `WFContentPredicateTableTemplate` row on the Notes `Name` property
with `Operator: 99` — **"contains"** — bounded by `WFContentItemLimitEnabled: true` /
`WFContentItemLimitNumber: 1` and consumed by a Get Item From List "First Item".

Shortening the title **widens what that substring lookup can match**. `contains "PROSOCHĒ"`
matches *any* note whose name contains the product name — including a leftover
`PROSOCHĒ — Control Room` from an earlier install, and including anything a user has named
e.g. `PROSOCHĒ (old)`. With a limit of 1 plus First Item, PROSOCHĒ would bind to whichever
such note the store returned first and append its ledger there **permanently and silently**.

### Why the operator was retained rather than tightened

`.planning/phases/11-.../11-RESEARCH.md` §6.2 recommended moving the operator to `4`
("string is") in the same edit. **It was not moved.** Two independent reasons, either
sufficient on its own:

1. **The current value is a recorded decision, not an oversight.** `docs/BUILD-NOTES.md`'s
   BOOT-08 row records the Find-Notes lookup shape as a deliberate choice made against the
   documented Notes name-matching trap. Reversing a recorded decision requires evidence, not
   a preference.
2. **The alternative is UNVERIFIED for this filter template.** The condition-code table in
   `.claude/CLAUDE.md` §4 documents `4` = "string is" for `WFCondition` on **conditionals**.
   Whether `Operator: 4` is accepted in a `WFContentPredicateTableTemplate` on the Notes
   `Name` property specifically is **not** established anywhere in the bundled catalog, the
   golden corpus, or any donor this project holds. This project's capability rule is
   explicit: when something cannot be verified, use the safest fallback, record the
   deviation, and keep the Shortcut runnable. Writing `4` here would be inference against a
   recorded decision — the exact move the rule forbids.

### The evidence that would settle it

**A donor export of a Find Notes action configured by hand on the owner's iPhone with the
`Name` filter set to "is" rather than "contains"**, exported as a signed `.shortcut` and
recovered via the `aea decrypt` + `aa extract` procedure in `.claude/CLAUDE.md` §8. Read back
the `Operator` literal the device actually writes. That is tier-1 device evidence and it
would settle the question in one round trip. Until it exists, the operator does not move.

This is a rung-3/4 question by `.claude/CLAUDE.md` §9's ladder — it needs the Notes app, and
`com.apple.mobilenotes` is absent from the booted simulator, so rung 2 cannot reach it.

### Interim mitigation, in copy

A paragraph was added to the Note body's `## READ THIS FIRST` section instructing the user to
delete or rename any note left under the old two-part title before continuing, and stating
that PROSOCHĒ finds its note by name. That is the whole mitigation; it is a user instruction,
not a mechanism, and it is recorded here as such.

The operator itself is **pinned** by `docs/note_identity_check.py`'s `EXPECTED_NAME_OPERATOR`
constant, whose comment names BOOT-08 and this record. Any future change to it is therefore a
deliberate, visible edit to a named constant rather than a silent side effect of a copy change.

### Second-order collision, pre-existing

**Both forks create a note with the same title.** This is not introduced here — Dumb and
Sentient both wrote `PROSOCHĒ — Control Room` before this change — but it is **sharper now**,
because a shorter title under a `contains` operator has a wider match surface. A user who
installs both forks has one note and two writers. Recorded, not fixed: fixing it means giving
the two forks different note titles, which is a product decision that belongs with the
Dumb→Core / Sentient→Aware rename in plan `11-06`, not with a copy change.

**No behavioural claim.** DIST-03 is open, no iPhone is connected, and nothing above has been
observed running. Every statement here is about what the file says, not what the device does.

**Requirement:** ROOM-01, ROOM-02

---

## BD-06-A3 — `schema_version` is bumped 2→3 this phase; the old-named signed artifacts are deleted

**Recorded 2026-08-17, plan `11-04` wave 4.** This record exists to fix two dispositions so that
plans `11-05` and `11-06` implement them without re-deriving or re-asking. It implements nothing
itself: no generator edit, no template edit, no rebuild is made by this plan.

`11-04` was authored as a **blocking `checkpoint:decision`** rated `one-way`. It is
**discharged** — not skipped, and not auto-approved by an agent. The developer answered it in
**BD-06-A1, Amendment 3** (2026-08-17), which is the input this record consumes.

### Decision 1 — take the bump: `schema_version` moves 2 → 3

The chosen option, verbatim from the plan's option table:

> **`bump`** — *"Bump the version so the seed changes reach installed devices."*

**Why the question existed.** A stored `state.json` that satisfies the three-check validity gate
(`schema_version` present, string-equals the accepted literal, `profile` non-empty) is **reused
forever**. A change to the bootstrap seed template is therefore invisible on any device that
already holds a file. `schema_version` is the only lever that forces the rebuild branch, and it
was used for exactly this purpose once before, 1→2.

Two seed changes in this phase need that lever:

- plan `11-05` adds a new bootstrap field (the Panic Escape flag). Without a bump, the removal
  path `11-05` builds is **dead** on an installed device — the flag it reads is simply absent.
- plan `11-06` changes an existing seed value (the `fork` label). Without a bump, the device
  keeps reporting the old fork name in its status line and in the Note's settings block after
  the rename, which reads as a bug of unknown origin.

**The cost that was accepted — stated in full, because it is the reasoning that made the answer
free, not the answer itself.** There is **no field-preserving migration**. Shortcuts provides no
mechanism for one, and this project has never built one. A device whose stored version is no
longer accepted rebuilds `state.json` from the template on its very next run, discarding
**accumulated heat, gravity, pressure, the rolling windows (`recent_sessions`,
`recent_contracts`), the session record, and the exit-learning history (`exit_stats[*].samples`)**.
That loss is unrecoverable: the Apple Note retains the human-readable ledger, but the machine
state is gone. Had a real installed base existed, this would have been a data migration with no
safe path, which is precisely why `11-04` was gated rather than decided inside a plan.

**Why it is free here.** BD-06-A1 Amendment 3 records the developer's statement that PROSOCHĒ is
a **new, as-yet-undeployed product**, that the only existing installs are the owner's own
testing, and that old `state.json` files are **explicitly not a consideration**. The `one-way`
rating rested entirely on destroying a real accumulated behavioural record. There is no such
record to destroy, so nothing irrecoverable is discarded and the gate is discharged.

**The gate reinstates itself.** This is a conditional discharge, not a permanent one. If a real
installed base ever exists, the cost above applies again unchanged, this decision returns to
`one-way`, and the blocking `checkpoint:decision` must be reinstated before any further
`schema_version` move. Threat `T-11-19` is marked `not applicable` for the same conditional
reason and returns to `high` under the same trigger.

**A second, independent reason the bump is the correct disposition this phase — not merely a free
one.** BD-06-A1 Amendment 1 renames the middle profile `Limbo` → `Purgatory`, which moves the
live Config key paths `thresholds.Limbo` → `thresholds.Purgatory` and
`cooldown_seconds.Limbo` → `cooldown_seconds.Purgatory`. This project's verified runtime
semantics are that a **dotted read with any missing segment is a hard error**, not a silent miss
(`.claude/CLAUDE.md` § *Verified iOS Shortcuts runtime semantics*). A device still holding
`profile: "Limbo"` would therefore hard-error at its next OPEN. BD-06-A1 **accepted** that
consequence on the grounds that no population can be harmed by it. A `schema_version` bump does
better than accept it: by forcing the rebuild branch, it reseeds `profile` from the new template,
so the stale value that would trigger the hard error is replaced rather than tolerated. This is a
file-level argument about which branch the generator's control flow takes — **it is not a
device-verified claim**, and it is offered as a reason the bump is well-aimed, not as evidence
that any device behaves this way.

**What was deliberately NOT built.** BD-06-A1 forbids all three by name, and none was built:

| Not built | Why it was excluded |
|---|---|
| A migration path | No field-preserving migration is possible, and with no installed base there is nothing to migrate |
| A dual-key Config alias (accepting both `Limbo` and `Purgatory`) | Would permanently encode a name collision BD-06-A1 renamed the profile specifically to dissolve |
| A read-time profile normalisation | Same objection, plus it would hide the stale value rather than replace it |

### The implementation surface — so plan `11-05` does not rediscover it

`fix_state_rebind()` in `tools/build_state_engine.py` is a **code** edit, not a data edit. Measured
2026-08-17: the function spans `:3255-3315`. **Anchor on the symbol, not the line numbers — they
shift on every edit.** (`11-RESEARCH.md` Pitfall 7 cites `:3022-3084` for this function; that
citation is **stale** as of this commit and should be read as naming the symbol, not the span.)

It hardcodes **three** literals, not two, and they must all move in the **same commit**:

| # | Site (measured) | Current | Role |
|---:|---|---|---|
| 1 | `:3283-3284` — `_replace_in_token(inner, '"schema_version": 1,', '"schema_version": 2,')` | `1,` → `2,` | The **bootstrap template seed** — the value a rebuilt `state.json` is written with |
| 2 | `:3291` — `parameters.get("WFConditionalActionString") in ("1", "2")` | `("1", "2")` | The **recognition tuple** the transformer uses to locate the existing version-check conditional |
| 3 | `:3296` — `version_check["WFConditionalActionString"] = "2"` | `"2"` | The **runtime validity-gate literal** the device compares its stored `schema_version` against |

**Why these are one edit and not three.** Sites 1 and 3 are the pair the plan named: move the
template without the gate literal and every device rebuilds forever; move the gate literal without
the template and every device — including a clean install — **fails its validity gate immediately**,
because the file it just wrote does not satisfy the check it is about to be measured by. Site 2 is
the coupling that is easiest to miss: it is what makes the transformer **idempotent**. Once site 3
writes `"3"`, a *subsequent* build no longer recognises the conditional, `version_check` stays
`None`, and the build aborts at `raise SystemExit("schema version check conditional not found")`.
The tuple must therefore admit the new value or the *next* rebuild fails — not this one, which is
what makes it a delayed and confusing failure.

### Decision 2 — the old-named signed artifacts are **deleted**, not retained

After plan `11-06` renames the forks, these two files at `artifacts/shortcuts/` become orphans and
are to be **removed** in the same commit that writes the new-named signed artifacts:

- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut`
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut`

**Why deletion rather than retention.** Three reasons, measured:

1. **`docs/manifest_check.py` cannot see an orphan.** It asserts only the rows `MANIFEST.md`
   gives it (`:47`), hashing and sizing each declared path from disk. A file no row names is
   invisible to it. Retention would therefore be an **unchecked** state — the one thing this
   project's twelve structural checks exist to prevent.
2. **Two plausible "current" imports side by side is exactly the confusion the signed-name
   discipline exists to prevent** (`.claude/CLAUDE.md` §8: the signed filename must equal the
   intended display name). A user browsing the directory after the rename would find four signed
   files and no way to tell which two are current.
3. **Nothing unrecoverable is lost.** Both files are **git-tracked** (verified via
   `git ls-files`), so `git show` recovers the exact bytes at any later point.

**One precision, because the obvious argument for deletion is wrong.** The dated archives under
`artifacts/shortcuts/2026-08-*/` do **not** contain signed `.shortcut` files — verified: every
file under `2026-08-17/` is an unsigned `.xml`, and a repo-wide `find` locates signed artifacts
only at the two canonical paths above. So the dated archives preserve the **XML build input**
under the old name, not a signed artifact. Deletion is recoverable through **git**, not through
the archive directory. The dated archives themselves are historical records and are **left
untouched** either way, per the precedent set by quick task `260817-au7`.

No claim is made that re-signing a preserved XML reproduces byte-identical signed output; the
recoverability claimed here is git's, and only git's.

### No behavioural claim

**DIST-03 is open. No iPhone is connected, and no device has run either build.** Nothing in this
record is device-evidenced. Every statement above concerns what the files say and which branch the
generator's control flow takes — not what any device does. In particular, the claim that a bump
causes an installed device to rebuild its `state.json` is a reading of the generator and the
validity gate, and it is **not** verified on hardware.

**Requirement:** AUDIT-02 (extends), DIST-02
---

## BD-06-A4 — the Dumb→Core / Sentient→Aware rename is a BREAKING CHANGE for any existing install

**Recorded 2026-08-17, plan `11-06` wave 6.** Build Addendum 01's product rename shipped this
plan: `PROSOCHĒ — Nine Circles — Dumb` became `PROSOCHĒ — Nine Circles — Core`, and
`PROSOCHĒ — Nine Circles — Sentient` became `PROSOCHĒ — Nine Circles — Aware`. This record
exists for one reason: **the rename is a breaking change for any existing install, it cannot be
made non-breaking, and that must be stated rather than smoothed over.**

### The mechanism, measured on this build

A signed `.shortcut` carries **no display name inside it**. Both containers shipped by this plan
were decrypted through the AEA1 recipe in `.claude/CLAUDE.md` §8, and neither recovered
`Shortcut.wflow` contains a `WFWorkflowName` key at all — the signer strips it, and the AEA1
auth-data plist holds only `SigningCertificateChain`. The display name therefore lives in the
**filename** and nowhere else.

A user's two Personal Automations (App Is Opened → `OPEN`, App Is Closed → `CLOSE`) reference
the shortcut by that library name. Consequently:

1. Importing the renamed build does **not** replace the old library entry — it adds a second one.
2. Both existing automations keep pointing at the **old** entry.
3. **There is no mechanism able to re-point them.** iOS exposes no API for editing a Personal
   Automation, this product has no companion app, and a Shortcut cannot create or modify an
   automation — `.planning` records that constraint from Phase 2 onward and the Note's own
   `## READ THIS FIRST` has always stated it.

The residual risk is therefore **accepted, not mitigated**: the only remedy is manual, by the
user, in the Shortcuts app — open each automation, tap its Run Shortcut action, select the new
name, then delete the old shortcut.

### Where it is stated, so a user and a future phase both see it

| Surface | What it says |
|---|---|
| The Control Room Note, `## READ THIS FIRST` | The product was renamed; an earlier install leaves a stale library entry; both Personal Automations must be re-pointed by hand, and nothing can do it for them |
| `README.md` | The two new artifact names, the previous names, and the breaking-change statement with its mechanism |
| `artifacts/shortcuts/MANIFEST.md` | A dedicated ⚠ block, plus the deletion disposition of the two old-named signed files |
| `docs/BUILD-NOTES.md` §25 | The full record: the measurement, §9's discharge, the deliberate non-rename of the source filenames, the Aware-side divergence, and the closing evidence table |

### What was deliberately NOT built

| Not built | Why |
|---|---|
| A compatibility shim shipping under the old name | It would reinstate exactly the "two plausible current imports" confusion the signed-name discipline exists to prevent, and BD-06-A3 Decision 2 already deleted the old-named artifacts for that reason |
| Any attempt to detect a stale install from inside the Shortcut | A Shortcut cannot read, enumerate or edit Personal Automations; there is nothing to detect it with |
| Softened wording that implies the upgrade is seamless | It is not seamless, and a user who believes it is will conclude PROSOCHĒ silently stopped working |

### Scope of the harm, and why it is acceptable here

The same ground as BD-06-A1 Amendment 3 and BD-06-A3: the developer has recorded that PROSOCHĒ
is a **new, as-yet-undeployed product** whose only installs are the owner's own testing.
**The reasoning is conditional, and reinstates itself:** if a real installed base ever exists,
a rename of a shipped display name becomes a decision with a real population behind it and must
be gated again rather than taken inside a plan.

### No behavioural claim

**DIST-03 is open. No iPhone is connected, and no device has run either renamed build.** That
the rename breaks an existing install is a **reasoned consequence** of the stripped-
`WFWorkflowName` measurement plus the absence of any automation-editing API — it is not an
observation of a device failing, and no one has yet followed the renamed automation steps end
to end. Every claim in this record is structural.

**Requirement:** ROOM-02, DIST-01, DIST-02
