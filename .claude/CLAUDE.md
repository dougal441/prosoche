<!-- GSD:project-start source:PROJECT.md -->

## Project

**PROSOCHĒ — Nine Circles**

PROSOCHĒ is a free, open-source iPhone Shortcut that restores the missing interval between the impulse to open a habit-forming app and the act of consuming it. It watches user-selected apps through native iOS Personal Automations (App Is Opened / Is Closed), accumulates behavioural **Pressure** from clustered and repeated openings, and escalates the user through nine progressively stronger friction "Circles." It ships as two forks from one engine: **Dumb** (fully deterministic, broad iOS 26 support) and **Sentient** (same deterministic engine plus Apple's **On-Device** Intelligence model as an attention mirror).

It is not a screen-time blocker and not a parental-control system. It is an adaptive friction system for self-directed behaviour change.

**Core Value:** **When a user automatically reaches for a target app, PROSOCHĒ interrupts strongly enough that the user makes an actual choice — and the strength of that interruption adapts to their own recent behaviour.**

If everything else fails, the OPEN → Heat/Gravity/Pressure → Circle → intervention loop must work reliably on a real iPhone without corrupting state.

### Constraints

- **Platform**: iOS 26.x, native Shortcuts only — no companion app, no private APIs
- **Tech stack**: Shortcuts plist XML built and signed via Shortcuts Playground; one `state.json`; one Apple Note
- **AI**: Apple On-Device Intelligence via the iOS 26 `Use Model` action, Sentient fork only — never cloud, never PCC, never ChatGPT
- **Privacy**: no behavioural data leaves the device; Sentient receives only a compact local context window, never the whole Note
- **Capability**: every iOS action identifier and parameter shape must be verified before use — if it cannot be verified, use the safest fallback, record the deviation, and keep the Shortcut runnable. Never fabricate an action because the strategy asks for it.
- **Build provenance**: before running `tools/build_state_engine.py` or `tools/build_sentient.py`, require `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD`; abort the rebuild if it fails. The former `codex/prosochedebug1` and `codex/round1` refs were stale at pre-cycle-1 commit `efb5a79` and are archived locally as `codex/archive-stale-*-pre-cycle1`.
- **Safety**: no unsafe or startling volume, no accessibility-stranding state, Emergency Restore always available. Every environmental change (brightness, volume) must be captured **and durably persisted** before it is applied and reliably restored, and any setting whose original cannot be captured is left unchanged — capture-and-restore reliability is the safety mechanism, not avoidance of a particular value. **[Decision D-01 — SETTLED ON MAIN, LOCKED 2026-08-17, recorded 2026-08-18]** The prior absolute brightness floor is retired: iOS's practical minimum is dim, not a literal black/unusable screen, per user on-device report. `safety.brightness_floor` and `safety.dim_target` are both `0` in both shipped forks (plan 16-03). This supersedes the Phase 9 addendum's *provisional* and *experimental-fork-only* framing — that framing was true when written and is no longer. Canonical strategy §21's floor clause is superseded on the main line by D-01; the canon is retained unmodified as the original design input and **`docs/CAPABILITY-DECISIONS.md` BD-02's Supersession note is the authority where the two disagree**. **Still outstanding, and not settled by D-01:** the capture-and-restore loop is **device-unproven**. Plan 16-01 made the capture persist before the device is changed, which is what makes the property satisfiable at all, but no run of it has happened on a phone; the underlying dim-not-black observation also rests on one unrepeated user report. Both are tracked by phase 16's UAT instrument and remain BLOCKED on DIST-03. Nothing in phase 16 makes the loop device-proven — do not read the settled decision as a settled device fact.
- **Determinism**: the model never controls arithmetic, thresholds, timers, Circle IX, or any safety decision
- **Device split**: Dumb targets all iOS 26 iPhones; Sentient requires Apple Intelligence-capable hardware (iPhone 15 Pro and later)

<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->

## Technology Stack

## 1. The installed Shortcuts Playground toolchain (ground truth)

| Location | Role |
|---|---|
| `/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/` | **Live plugin root** — this is what `${CLAUDE_PLUGIN_ROOT}` resolves to at runtime. All bin wrappers, skill docs, agents, hooks live here. |
| `/Users/dougalhanson/.claude/plugins/marketplaces/shortcuts-playground/claude/` | Marketplace source copy (mirror of the same files under `skills/`, `agents/`, `bin/`, `commands/`, `hooks/`). |
| `/Users/dougalhanson/.claude/plugins/data/shortcuts-playground-inline/` | Plugin data/config dir (userConfig storage), not reference docs. |

### Skill reference docs (read these, in this order, before authoring)

| File | What it covers | Size |
|---|---|---|
| `SKILL.md` | Entry point, quick reference table, Craig Loop protocol, 47 numbered "Key Rules" | 466 lines |
| `BEST_PRACTICES.md` | Mandatory rules; source of truth if it conflicts with anything else; per-action wiring gotchas; full If-condition-code table | 357 lines |
| `PLIST_FORMAT.md` | Root plist keys, icon config, action structure | 296 lines |
| `ACTIONS.md` | 365 `WF*Action` identifiers, OS27 ToolKit v78 additions, complete identifier list, per-action parameter notes | 713 lines |
| `APPINTENTS.md` | `com.apple.*` AppIntent-style actions (Notes, Safari, Home, System Controls, Screen Time/Intelligence Platform, etc.) | 2,760 lines |
| `AUTOMATION_TRIGGERS.md` | OS27 `WFWorkflowTriggers` metadata (not needed — PROSOCHĒ's Personal Automations are user-created, not shortcut-embedded) | 133 lines |
| `CONTROL_FLOW.md` | If/Repeat/Menu wiring, condition codes, multi-condition Ifs, nesting depth evidence | 777 lines |
| `VARIABLES.md` | `WFTextTokenString`/`WFTextTokenAttachment`, `attachmentsByRange`, `Type` values, aggrandizements, `WFQuantityFieldValue` | 569 lines |
| `DATE_TIME.md` | Date format recipes, UNIX timestamp pattern, ISO 8601/RFC 2822, custom format strings | 75 lines |
| `PARAMETER_TYPES.md` | All serialization types, `WFInputType`, math operators, Reminders schemas | 1,117 lines |
| `FILTERS.md` | `WFContentPredicateTableTemplate` filter shapes (Photos, Files, Notes, Reminders, Health) | 697 lines |
| `HEALTHKIT.md` | Not relevant to PROSOCHĒ | 317 lines |
| `THIRD_PARTY_ACTIONS.md` | Third-party app actions (not needed — PROSOCHĒ is first-party-only) | 77 lines |
| `TOOLKIT_SNAPSHOT.md` | **Explains the validator's target-gating model** — read this to understand `--target-macos`/`--target-platform` | 62 lines |
| `EXAMPLES.md` | Full working plist examples (Ask for Input, Use Model, Menu, HTTP) | 738 lines |
| `ICONS_AND_COLORS.md`, `URL_SCHEMES.md`, `JAVASCRIPT_WEBPAGE.md`, `CHANGELOG.md` | Supporting | — |
| File | Contents |
|---|---|
| `data/toolkit-v63-tool-ids.json` | 1,794 identifiers from the original (pre-OS27) macOS ToolKit snapshot — the closest thing to an "OS 26" baseline allowlist |
| `data/toolkit-v78-tool-ids.json` | 2,731 identifiers from macOS 27 "Golden Gate" build 26A5353q — OS27-only additions |
| `data/toolkit-v78-ios27-tool-ids.json` | 1,206 identifiers from an **iOS 27.0 Simulator** ToolKit v78 database — the only platform-specific iOS snapshot bundled |
| `data/toolkit-v78-first-party-parameter-keys.json` | Parameter-key/type/platform-provenance catalog for `com.apple.*` and `is.workflow.actions.*` rows — **OS27-only; each entry lists which platform(s) it was observed on** |
| `data/toolkit-v78-first-party-enum-cases.json` | Picker enum values for OS27 parameter types |
| `golden-shortcuts/index.jsonl` + `golden-shortcuts/xml/*.xml` | 19 curated real-world shortcut XMLs (pre-OS27 vintage: client versions 700–1300) for wiring patterns |

### Agents, commands, hooks

| Component | Path |
|---|---|
| `shortcut-builder` agent | `.../1.2.1/agents/shortcut-builder.md` — owns design→build→validate→sign→archive for new shortcuts |
| `shortcut-remixer` agent | `.../1.2.1/agents/shortcut-remixer.md` — surgical diff on existing unsigned XML; it refuses a signed `.shortcut` directly, so recover `Shortcut.wflow` and convert it to XML first (see §8) |
| `/shortcuts-playground:build` | `.../1.2.1/commands/build.md` |
| `/shortcuts-playground:remix` | `.../1.2.1/commands/remix.md` |
| `PostToolUse` validator hook | `.../1.2.1/hooks/hooks.json` + `hooks/auto-validate.sh` — auto-runs the Craig Loop validator on every Write/Edit that touches a Shortcuts plist |
| `shortcuts-playground-selftest` | `.../1.2.1/bin/shortcuts-playground-selftest` — 6-check health test (Python version, `shortcuts` CLI, plugin-root resolution, bundled data, validator-on-golden, full archive+sign round trip) |

### Exact validator invocation

**This section is the single canonical home of the two-gate rule and the mechanism behind it.** Everything a reader needs to invoke the validator correctly is here; no other file needs to be opened. Measurements and reproduction commands live in `docs/BUILD-NOTES.md` §22 — that is the only other file involved, and it records evidence, never the rule.

#### What each flag actually controls

- The plugin's default (`auto`/`macos`) targets whatever macOS the *build machine* runs and the macOS action surface — wrong for an iPhone-only shortcut.
- **`--target-platform` selects which bundled ToolKit snapshot the validator consults.** It changes nothing in the plist and nothing about where the shortcut runs. It is Playground tooling, not a device-target declaration. Internally `all`/`any`/`latest` all normalise to "no platform filter"; `ios`/`ipados`/`iphone`/`ipad` normalise to `ios`; anything else to `macos`.
- **`--target-macos` is the controlling variable.** It gates two independent things: the snapshot minimum-version filter, and — separately — whether the v78 first-party **parameter-key** and **enum-case** catalogs load *at all*. Below target 27 neither catalog is loaded, on any platform setting. This is why the second gate exists.

#### Gate A — mandatory, residue must equal exactly the enumerated waiver

```bash
validate-shortcut <file.xml> --target-macos 26 --target-platform all
```

Expect **exit 1** with **exactly 30 error lines per fork** — the waiver table below and nothing else. This is the **identifier / availability baseline at the project's real target**. It is the gate every plan, todo and `docs/*.py` checker names. It performs **zero** parameter-key or picker-literal checks — measured, not inferred.

**Amended 2026-08-19 (phase 14, decision D-14-01 item 1).** Gate A previously demanded a clean report; that wording is retired and is **cited, not restated** — it lived in this sub-heading, in the paragraph directly beneath this command block (which additionally claimed the gate was unchanged, a second assertion that also stops being true), and in the `Validator target` row of the Recommended Stack table below. All three are amended here. The reason: phase 14 ships `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`, which is absent from **all three** bundled ToolKit snapshots, and the validator offers no allowlist, no ignore flag, no waiver file and no environment override — measured, not assumed. Gate A can therefore never exit zero again. The obligation becomes the one gate B already models: **the residue must equal exactly the enumerated waiver**, and anything outside it is a real finding.

Two line families are permitted, both scoped to that one identifier by its full string, index-normalised so a future run can diff against it:

| Waived line (indices normalised to `N`) | Count per fork | Why waived |
|---|---:|---|
| `- Unknown AppIntent identifier at index N: com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` | 15 | **A genuine catalog gap, not a project error.** The identifier is device-donor-established from three decrypted exports off the owner's iPhone; the two records that establish it are `docs/BUILD-NOTES.md` §4's CAP-20 row and `docs/CAPABILITY-DECISIONS.md` BD-01-R2. A tool that lacks a fact does not overrule the evidence that has it. |
| `- AppIntent action missing AppIntentDescriptor at index N: com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` | 15 | Follows from the same gap: with the identifier unknown, no `AppIntentDescriptor` resolves for it. Synthesising one is forbidden by D-14-01 — it fabricates three field values no donor supplies **and** does not silence the other family anyway. |

**A descriptor-less action emits BOTH families, once per instance.** A waiver naming only one would be permanently unsatisfiable — which is precisely the outcome the decision exists to prevent — so both are enumerated.

**Three things keep this narrow. They are stated separately so none is eroded one reading at a time:**

1. **The waiver is scoped to one identifier by name.** Every *other* unknown identifier, every missing parameter key and every availability failure still fails gate A exactly as before. A waiver broad enough to swallow a second unknown identifier would gut the gate for every other action in the build.
2. **The line count is derived from the emitted site count, not chosen.** 15 AX sites per fork × 2 families = 30. A site that stops being emitted *shrinks* the residue, and a shrunk residue fails as loudly as a grown one: silent loss of an emitted site is the failure mode a one-sided waiver would miss, and it would otherwise present as good news.
3. **The catalog gap is recorded where a red gate sends a reader.** `docs/BUILD-NOTES.md` §5 `DEV-08` carries the reproduction command, the measured residue on both forks, and an explicit rejection of the `UA*` macOS twin — so the authority arrives before the temptation.

**The waiver is mechanical, not remembered: `python3 docs/gate_a_residue_check.py`.** It runs gate A on both forks, classifies every reported line, permits exactly the two families above for exactly that one identifier, and exits non-zero on anything else *and* on any change to the permitted count in either direction. If it fires, investigate the new line. Never widen the waiver, and never substitute `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` — the macOS twin buys a green check by shipping an action that does nothing on an iPhone.

#### Gate B — advisory, waivered, never blocking

```bash
validate-shortcut <file.xml> --target-macos 27 --target-platform all
```

Expect **exit 1** with **exactly one** error line per fork. This is the **parameter-key and picker-literal check** — the only mode that loads the v78 catalogs. The single permitted line, index-normalised so a future run can diff against it:

| Waived line (indices normalised to `N`) | Count per fork | Why waived |
|---|---:|---|
| `Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index N: WFCreateNoteInput. ToolKit v78 expects: OpenWhenRun, contents, folder, interpretAsMarkdown, name.` | 1 | Device-donor ground truth outranks the `macOS 27`-tagged catalog entry — `docs/BUILD-NOTES.md` §14; deliberately retained in `tools/build_state_engine.py` — enforced entry `STRING_ENVELOPE_PARAMS["com.apple.mobilenotes.SharingExtension"]`, donor-evidence comment in the CYCLE 4 block immediately above it. **Anchor on the symbol, not the line: these shift on every edit.** Measured 2026-08-17: comment `:1961-1966`, entry `:1982`. |

**Anything gate B reports outside that waiver is a real finding and must be investigated before the affected artifact ships.**

**Gate B is advisory and must never be chained into a definition of done.** Because its waiver is permanent it can never exit 0, so it is structurally incapable of being an `&&`-linked build gate. A plan authored before 2026-08-17 that asserts `--target-macos 27` appears nowhere in the commands it runs **remains fully satisfied by gate A alone** — nothing about that plan is now wrong.

**Gate B's own limit — why A stays mandatory.** At `--target-macos 27` the validator may *accept* an OS27-only parameter key that iOS 26 does not offer. Gate B can therefore produce false acceptances. It supplements gate A; it never replaces it.

**Companion note, added 2026-08-19: gate A now joins gate B in never being an `&&`-linked build gate.** Both waivers are permanent, so neither raw invocation can ever exit zero, and either one chained into a success condition makes that definition of done permanently unsatisfiable. The two gates keep their different statuses — A mandatory, B advisory — and only the mechanism of satisfying A changes: **a plan satisfies its gate-A obligation by running `python3 docs/gate_a_residue_check.py`, never by chaining the raw validator command.** The checker is named here by path so the replacement is unambiguous. A plan authored before 2026-08-19 whose commands chain the raw gate-A invocation is satisfied by running the checker in its place; nothing else about such a plan is now wrong.

#### Why the earlier rule went wrong

The failure was never "`ios` is wrong for an iPhone project." It was the **pairing** of the iOS platform flag with `--target-macos 26`: `toolkit-v63` is macOS-labelled and is filtered out by the platform gate, the only iOS snapshot is a v78/27 capture and is filtered out by the version gate, and the result is an **empty allowlist that rejects everything** — 3675 of 3675 actions, including `is.workflow.actions.comment` and `is.workflow.actions.nothing`. A check that fails 100% of its inputs carries zero signal. The controlling variable is `--target-macos`, not `--target-platform`.

#### Why gate B does not use the iOS platform flag

`--target-macos 27 --target-platform all` **strictly dominates** `--target-macos 27 --target-platform ios` on this project's artifacts, measured:

- It enum-checks **1105** identifiers versus **455** — a superset, +659.
- Of the picker parameters the forks actually emit, `all` checks **14** `(identifier, key)` pairs versus **13**: the `ios` setting drops `is.workflow.actions.appendnote` / `operation`.
- The `ios` setting excludes **every `macOS 27`-tagged catalog entry**, which removes all four Notes actions (Create/Append/Find/Show) from parameter-key and enum-case checking entirely — the actions this project depends on most.
- It produces **zero** of the five spurious identifier rejections the `ios` variant generates, because it never applies the platform-label filter that creates them.

Measurements, the six `validate_shortcut.py` source citations, the four-invocation table, and the synthetic-mutation control that proves gate B has teeth: `docs/BUILD-NOTES.md` §22.

### Exact signing invocation

### Definition of done (per the plugin's own rule)

## 2. Plist format contract

### Root keys (from `PLIST_FORMAT.md`, cross-checked against golden XML headers)

| Key | Type | Required | PROSOCHĒ guidance |
|---|---|---|---|
| `WFWorkflowActions` | Array | Yes | The action list |
| `WFWorkflowClientVersion` | String | Yes | Metadata only — Shortcuts.app rewrites this on save/import; not a hard OS gate. Golden examples range 700–1306; the Playground's own quick-start template uses `"2700.0.4"` (an OS27-era value). **No documented iOS-26-specific canonical value exists in this plugin's bundled reference** — treat as a non-enforced field and don't over-invest in getting the exact string "right"; let the agent emit its default and confirm on-device import works. |
| `WFWorkflowMinimumClientVersion` / `...String` | Integer / String | Yes | `900` is the value used across the entire golden-shortcut corpus and the Playground's own templates — use `900` unless a specific action forces higher. |
| `WFWorkflowIcon` (`WFWorkflowIconGlyphNumber`, `WFWorkflowIconStartColor`) | Dict | Yes | Always set via `resolve-icon --prompt "..."` |
| `WFWorkflowImportQuestions` | Array | No | See §7 — real schema found in golden XMLs, not documented in prose |
| `WFWorkflowInputContentItemClasses` | Array | No | Leave empty for PROSOCHĒ (it receives `OPEN`/`CLOSE` as **Shortcut Input** text from Personal Automations, not as share-sheet content types) |
| `WFWorkflowOutputContentItemClasses` | Array | No | Leave empty |
| `WFWorkflowTypes` | Array | No | Leave empty (empty = ordinary Shortcut; values like `WatchKit` or `ActionExtension` opt into other surfaces PROSOCHĒ doesn't need) |
| `WFWorkflowHasOutputFallback` | Bool | No | `false` |
| `WFWorkflowIsDisabledOnLockScreen` | Bool | No | Not needed; PROSOCHĒ is invoked by Personal Automations and manual taps, not Lock Screen widgets |

### How a shortcut declares iOS-only vs macOS actions

- The Shortcuts **Playground validator's** `--target-platform` flag selects which bundled ToolKit snapshot is consulted — it is Playground tooling, not a plist feature, and it declares nothing about where the shortcut runs.
- The actual portability risk is per-action: an action identifier or parameter key gated to "macOS 27" in the bundled catalog (see the Color Filters and Notes findings below) may simply not exist as an option when authoring/running on iPhone.
- **Practical rule for this project:** run the **two-gate rule** — gate A mandatory, gate B advisory, both defined in full in §1 `### Exact validator invocation`, which is the only place that rule is stated — and then manually import-test on a real iPhone (Shortcuts Playground cannot execute or verify runtime behavior — its validator only checks structural/plist correctness, per `TOOLKIT_SNAPSHOT.md`).

## 3. Capability audit — verified action identifiers

| # | Capability | Verdict | Identifier / evidence | Notes for the build agent |
|---|---|---|---|---|
| 1 | Get Current App / current-app detection from an automation | **VERIFIED** | Two mechanisms: (a) standalone action `is.workflow.actions.getcurrentapp` (`WFGetCurrentAppAction`), present in `toolkit-v63` and the iOS27-simulator snapshot; (b) magic-variable `Type: "CurrentApp"` usable inline in any `WFTextTokenAttachment`, documented in `PARAMETER_TYPES.md` §"Current App" with `WFPropertyVariableAggrandizement` for name/bundle-ID | Use the magic-variable form to avoid an extra action; both return app metadata (aggrandize `Name`/`Bundle Identifier`). **Caveat (from canonical strategy §5.1, independently confirmed by domain knowledge, not by this plugin):** Personal Automations pass the triggering app's identity to the automation, not necessarily reliably re-derivable via Get Current App inside the invoked shortcut in every trigger context — the build agent must test this on-device for the OPEN automation specifically and fall back to trusting the automation's own app filter (i.e., "if this shortcut was invoked by the OPEN automation at all, the app IS the configured target") rather than depending on Get Current App as the source of truth. |
| 2 | Get File, Save File (with overwrite), file-existence checks in Shortcuts iCloud folder | **PARTIAL — VERIFIED for Get/Save, NOT AVAILABLE for existence check** | `is.workflow.actions.documentpicker.open` (`WFGetFileAction`/`WFSelectFilesAction`), `is.workflow.actions.documentpicker.save` (`WFSaveFileAction`); both in `toolkit-v63`. `BEST_PRACTICES.md` recommends `is.workflow.actions.file.select` for user-driven picking and Save File for writing, chained via **Set Name** (`is.workflow.actions.setitemname`, outputs "Renamed Item") when a specific filename/overwrite target is needed. | **No native "does file exist" boolean action or property is documented anywhere in the bundle** (searched `ACTIONS.md`, `FILTERS.md`, `PARAMETER_TYPES.md`, `APPINTENTS.md` — no `WFGetFileExists`, no filter predicate for existence). This is a known, real Shortcuts limitation, not a plugin gap. **Fallback (record as a deviation):** attempt **Get File** at the fixed `state.json` path; a missing file surfaces as a runtime error dialog in Shortcuts, which cannot be silently caught (Shortcuts has no try/catch). PROSOCHĒ's bootstrap must therefore not rely on a "check exists, then read" pattern — instead: always attempt **Get File**, treat any non-dictionary/empty result from the subsequent **Detect Dictionary** step as "state absent," and drive bootstrap off *that*. Save File's `WFSaveFileOverwrite`/ask-where-to-save behavior is likewise **UNVERIFIED** in this bundle — no schema found — confirm empirically and fall back to always using **Save File** with an explicit fixed path + explicit "replace existing" toggle if the Craig Loop / on-device import shows it's needed. |
| 3 | Dictionary creation, Get/Set Dictionary Value, JSON text ↔ dictionary conversion | **VERIFIED** | Create: `is.workflow.actions.dictionary` (`WFDictionaryAction`, `WFItems`/`WFDictionaryFieldValueItems`, documented in `PLIST_FORMAT.md`/`PARAMETER_TYPES.md` §"Dictionary Field Value"). Get: `is.workflow.actions.getvalueforkey` (in `toolkit-v63` complete list), key param `WFDictionaryKey` with **1-based dot notation** for nested access (`SKILL.md` rule 16, e.g. `results.tracks.items`). Set: `is.workflow.actions.setvalueforkey` (in `toolkit-v63`), requires `WFDictionary` wired explicitly (`BEST_PRACTICES.md`: "always connect the target dictionary via `WFDictionary`; do not rely on implicit input"). JSON text → dictionary: `is.workflow.actions.detect.dictionary` ("Detect Dictionary"), used in 3+ golden examples (`1be4dde9...xml`, `6a18b768...xml`, `ae59e10d...xml`) for parsing API/JSON responses. | Dictionary → JSON text direction: use a **Get Dictionary Value** on the whole dict wired into a **Text**/**JSON Text** action, or the dict's own text coercion — not separately documented as a distinct action; `state.json` writes should build the JSON body as a **Text** action template (per `BEST_PRACTICES.md` rule for "complex JSON fallback": use JSON Text + `WFRequestVariable`-style templating) rather than assuming a magic "Dictionary → JSON string" action exists as its own identifier. Known gotcha: comparing a **Dictionary Value** (text) directly in an **If** often renders blank — pass it through a **Text** action first, then compare the Text variable (`BEST_PRACTICES.md` §Lists & Dictionaries). |
| 4 | Date arithmetic (Adjust Date, Format Date, date difference in seconds) | **VERIFIED** | Adjust: `is.workflow.actions.adjustdate` (`WFDate` + non-empty `WFDuration` as `WFQuantityFieldValue{Magnitude,Unit}`, `WFAdjustOperation` for explicit Add/Subtract — `SKILL.md` rule 36, `BEST_PRACTICES.md`). Format: `is.workflow.actions.format.date` (`WFDate`, `WFDateFormatStyle`, custom pattern in `WFDateFormatString`, full UTS#35 pattern-character table in `DATE_TIME.md`). Difference: `is.workflow.actions.gettimebetweendates` (`WFTimeUntilAction`), `WFInput` + exactly one of `WFDate`/`WFTimeUntilCustomDate`/`WFTimeUntilFromDate`, `WFTimeUntilUnit` for the output unit (documented seconds/minutes/etc. via `WFQuantityFieldValue` unit table in `VARIABLES.md`) | For the "behavioural day = date − 4h" and Heat decay math, chain: **Date** (Current Date) → **Adjust Date** (subtract 4 hr / seconds since last interaction) → **Format Date** (custom `yyyy-MM-dd` for the day key) → **Get Time Between Dates** with `WFTimeUntilUnit = sec` for elapsed-seconds math feeding Heat decay. Never put a `CurrentDate` magic token directly into `WFTimeUntilFromDate`/`WFDate` fields expecting "now" — first materialize it via a **Date** action set to Current Date, then reference *that action's output* (`ACTIONS.md` §Get Time Between Dates, `BEST_PRACTICES.md`). |
| 5 | Notes: Create Note, Append to Note, Find Notes / Show Note | **VERIFIED (macOS-catalog only) — cross-checked, standard iOS actions** | Create Note: `com.apple.mobilenotes.SharingExtension` (params: `name`, `contents` [AttributedString], `folder`, `interpretAsMarkdown`, `OpenWhenRun`). Append: `is.workflow.actions.appendnote` (params: `operation` [append/prepend], `entity`, `text`, `section`, `ignoreWhitespace`, `interpretAsMarkdown`). Find: `is.workflow.actions.filter.notes` (`WFContentItemFilter` as `WFContentPredicateTableTemplate`; name filter uses `Values.String`/`WFTextTokenString`, folder filter uses `Values.Enumeration`/`WFLinkDynamicOptionSubstitutableState` — `BEST_PRACTICES.md` §Text & Parsing). Show/Open: `is.workflow.actions.shownote` (param: `target`). All four identifiers are present in `toolkit-v63` (the generic, non-platform-restricted snapshot). | **Flag:** the v78 first-party parameter catalog tags all four of these entries `"platforms": ["macOS 27"]` only — they are absent from the bundled iOS-27-Simulator snapshot entirely. Per the gap discussed in §1, treat this as a bundled-data completeness gap, not evidence these are macOS-exclusive: Notes actions (Create/Append/Find/Show) have been standard first-party iOS Shortcuts actions for years and are core to the canonical strategy's Control-Room-Note design; they are extremely unlikely to be genuinely unavailable on iPhone. **Still: verify all four empirically on a real iPhone during the first Dumb build** and record the outcome in build notes — this is the single most consequential "trust but verify" item in this audit because the entire Control Room design depends on it. `WFUrgent`/`interpretAsMarkdown` booleans, if used, are OS27-parameter-gated per `ACTIONS.md` — do not set them when validating at `--target-macos 26`. |
| 6 | Ask for Input (text and number), Choose from Menu, Choose from List | **VERIFIED** | Ask: `is.workflow.actions.ask` (`WFAskForInputAction`), `WFAskActionPrompt`, `WFInputType` ∈ `Text`/`Number`/`URL`/`Date`/`Date and Time` (`PARAMETER_TYPES.md` §WFInputType). Full working example in `EXAMPLES.md` Example 2. Choose from Menu: `is.workflow.actions.choosefrommenu`, control-flow modes 0/1/2, `WFMenuPrompt`, `WFMenuItems` array, one mode-1 case per item with matching `WFMenuItemTitle` in identical order (`CONTROL_FLOW.md`, exhaustively documented, "verified from 127 real shortcuts analysis"). Choose from List: `is.workflow.actions.choosefromlist` (in `toolkit-v63` list) | For PROSOCHĒ's Control Room manual menu (Status/Open Control Room/Sync Profile/... ) and Consult's 6-item picker, Choose from Menu is the right primitive — its wiring is the most rigorously documented control-flow pattern in the whole skill (menu-item-title matching is a hard requirement, order-sensitive). |
| 7 | Open App, Open URL, web search, Maps search deep link | **VERIFIED** | Open App: `is.workflow.actions.openapp` (`WFAppIdentifier`, optional OS27 `WFWindowingFormat` — skip on iOS26 target). Open URL: `is.workflow.actions.openurl` (`WFInput`). Web search: `is.workflow.actions.searchweb` (`WFSearchWebAction`, in `toolkit-v63`). Maps: `is.workflow.actions.searchmaps` (`WFSearchMapsAction`) and `is.workflow.actions.getmapslink` (deep-link generator), both in `toolkit-v63`; also `is.workflow.actions.getdirections`/`getdistance` for route-shaped Maps actions. | Consult's "route feed-shaped seeking to query-shaped seeking" (canonical strategy §8.5) maps directly: Ask for Input → If/Menu classify → Search Web (`searchweb`) or Search Maps (`searchmaps`) or Open URL to `https://www.google.com/search?q=` as the reliable generic web-search fallback if `searchweb`'s exact behavior (which search provider/app it opens) proves unsuitable on-device. |
| 8 | Set Brightness, get current brightness | **VERIFIED (Set) / UNVERIFIED-in-Playground (Get)** | Set: `is.workflow.actions.setbrightness` (also exposed as Siri intent `com_apple_shortcuts_set_brightness`), param `WFBrightness` (float), present in **both** `["iOS 27 Simulator","macOS 27"]` per the v78 parameter catalog — this is the one system-control action in the whole audit with confirmed iOS *and* macOS provenance. Get: **no native "get current brightness" action or property is documented anywhere in the Playground bundle** — not in `ACTIONS.md`'s Get Device Details entry, not in `PARAMETER_TYPES.md`. External corroboration (Apple's own "What's New in Shortcuts" release notes, via web search, not part of the Playground bundle): Apple states **Get Device Details** ("now rounds numbers, including the current battery level, volume, and brightness") does expose a brightness reading — but the exact `WFDeviceDetailsProperty` string is not documented in this plugin's reference files, so it counts as UNVERIFIED against the ground-truth source this research prioritizes. | For Circle "Dimming," Set Brightness (`WFBrightness`) is safe to use directly at the configured `safety.dim_target` (`0` as shipped). The bound this cell named until 2026-08-18 came from canonical strategy §21 and is **superseded on the main line by decision D-01** — the citation stands, the canon is retained unmodified, and `docs/CAPABILITY-DECISIONS.md` BD-02's Supersession note is the authority where the two disagree. The retired wording is cited, not restated. Per **CAP-08** the parameter is OPTIONAL, so the real hazard here is an **absent** `WFBrightness`, which silently applies an unrequested default with no captured original behind it. For *reading* the pre-dim brightness to restore it later, try **Get Device Details** with a property named `Brightness` (candidate value from external Apple docs) during the Craig Loop and confirm on import; if it cannot be confirmed working, the safest fallback per canonical strategy §21 is: **do not perform a stateful brightness change unless the original value can be reliably captured and restored** — i.e., skip the Dimming primitive's brightness manipulation and substitute a different passive-friction primitive, recording the deviation in build notes. |
| 9 | Set Volume, get current volume | **VERIFIED (Set) / UNVERIFIED-in-Playground (Get)** | Set: `is.workflow.actions.setvolume` (`WFSetVolumeAction`), in `toolkit-v63`, also `com.nick.Clic.SetVolumeIntent` (third-party, irrelevant). No parameter schema for `setvolume` was found in the v78 catalog (it's a legacy `is.workflow.actions.*` action so the OS27 schema-gating catalog doesn't cover it — per `TOOLKIT_SNAPSHOT.md`, "it does not apply broad unknown-key checks to regular `is.workflow.actions.*` actions"), so treat the conventional `WFVolume`-style float parameter as the working assumption pending on-device confirmation. Get: same situation as brightness — only external (non-Playground) evidence via Get Device Details' "current volume" property, exact key name unconfirmed. | Same guidance pattern as Brightness: use Set Volume for the "Silence" primitive only if the pre-change volume can be captured and restored (canonical strategy §21 hard requirement); if Get Device Details' volume property can't be confirmed working during the Craig Loop / on-device test, skip stateful volume manipulation for the prototype and record the deviation. |
| 10 | Set Color Filters / grayscale toggle, and whether current state can be READ back | **NOT AVAILABLE on iOS** | The only "Set Color Filters" action found anywhere in the bundle is `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` (params `operation`, `state` [bool On/Off], `ShowWhenRun`). Its v78 parameter-catalog entry is tagged **`"platforms": ["macOS 27"]` only**, and — critically, unlike the Notes case above — it is **absent from the bundled iOS-27-Simulator ToolKit snapshot entirely** (confirmed by direct lookup: `False`). The only accessibility-adjacent entries present in the iOS snapshot are `com.apple.Bridge.AccessibilityDeepLinks`/`OpenAccessibilityDeepLinks` — deep-link *openers* to Settings, not togglers. No grayscale action exists anywhere in the 365-identifier `ACTIONS.md` list either (`colorfilter`/`grayscale` do not appear as `is.workflow.actions.*` identifiers). There is **no read-back mechanism** for any of this, consistent with there being no set action to read back from. | This is a genuine, well-known iOS Shortcuts limitation (Color Filters/grayscale has never been exposed to Shortcuts.app on iPhone, unlike macOS's Universal Access AppIntents) — the Playground's own bundled data corroborates it rather than merely failing to document it. **Fallback for Circle "Ash":** cannot be implemented as a programmatic grayscale toggle. Options to record in build notes: (a) drop Ash as a distinct primitive and substitute Dimming/Silence/Knock earlier in the sequence, (b) deep-link the user to Settings → Accessibility via `com.apple.Bridge.OpenAccessibilityDeepLinks` as a *manual* one-tap suggestion (not an automatic toggle — breaks the "no permission prompt" design goal for Exile-class primitives), or (c) treat Ash as aspirational/Phase-E scope pending a future non-Shortcuts mechanism. Given canonical strategy §21's absolute rule ("if Shortcuts cannot detect and restore the original condition safely, skip dynamic grayscale"), **option (a) is the recommended default** for the prototype. |
| 11 | Speak Text | **VERIFIED** | `is.workflow.actions.speaktext` (`WFSpeakTextAction`), present in `toolkit-v63`'s complete identifier list | Straightforward; wire the Mirror/Voice message text as `WFTextTokenString` (display parameter rule from `VARIABLES.md`) into whatever the action's text-input key turns out to be (commonly `WFText`/`WFSpeakTextText` in real-world Shortcuts — not spelled out in this plugin's docs beyond identifier presence, so confirm the exact key via Craig Loop). |
| 12 | Lock Screen | **VERIFIED** | `is.workflow.actions.lockscreen` (`WFLockScreenAction` in class-mapping terms), **zero parameters**, and — unlike Color Filters — explicitly present in **both** `["iOS 27 Simulator","macOS 27"]` per the v78 catalog. (There is also `is.workflow.actions.lock.app` — "Lock App," a *different* action that locks a specific app via `WFLockAppOperation`/`WFApp`, and `com.apple.controlcenter.LockScreenIntent`, a macOS-27-only Control Center intent — do not confuse these three.) | Circle IX (Ice) can use `is.workflow.actions.lockscreen` directly as the strongest safe ejection primitive the canonical strategy anticipates (§11, §22) — this is one of the most solidly verified actions in the whole audit (no params, confirmed cross-platform). |
| 13 | Run Shortcut (shortcut-to-shortcut invocation and passing input) | **VERIFIED identifier / UNVERIFIED exact parameter keys in this bundle** | `is.workflow.actions.runworkflow` (`WFRunWorkflowAction`), present in `toolkit-v63`. Also documented as an AppIntent surface: `com.apple.shortcuts.RunShortcutIntent` ("Run Shortcut") and `com.apple.shortcuts.RunShortcutFromCollectionIntent` in `APPINTENTS.md`. **No parameter schema (`WFWorkflowName`/`WFInput`/output-handling keys) for `runworkflow` is spelled out anywhere in `ACTIONS.md`'s per-action detail sections** — it only appears in identifier lists. | PROSOCHĒ's design (per PROJECT.md) is a **single master shortcut with OPEN/CLOSE routing via Shortcut Input text**, not shortcut-to-shortcut invocation between Dumb/Sentient/etc. — so `runworkflow` is not on this project's critical path; it's audited here only because the strategy's capability list requested it. If it becomes needed later (e.g. Control Room menu items dispatching to helper shortcuts), confirm the conventional `WFWorkflowName` (target shortcut name, string) + `WFInput` (input to pass) shape empirically via the Craig Loop before relying on it. |
| 14 | Wait / Wait to Return | **VERIFIED identifiers / parameter keys not detailed** | `is.workflow.actions.delay` (`WFDelayAction`, "Wait") and `is.workflow.actions.waittoreturn` (`WFWaitToReturnAction`), both in `toolkit-v63`. Neither has a dedicated parameter section in `ACTIONS.md`; the conventional `WFWaitActionWaitTime` for Delay is not named in this bundle. | Needed for CLOSE handler's "brief wait if needed for app-switch race handling" (canonical strategy §20 step 4). Confirm the exact wait-duration key via Craig Loop/on-device import before finalizing; `WFQuantityFieldValue` (`Magnitude`+`Unit`, units `sec`/`min`/... per `VARIABLES.md`) is the general pattern this plugin uses for other duration parameters and is the best-effort guess if the field name can't be confirmed from `ACTIONS.md` alone. |
| 15 | `Use Model` (iOS 26 Apple Intelligence) — model-source selection, on-device pinning, structured/JSON output, consumption by later actions | **VERIFIED identifier and most parameters / UNVERIFIED model-source enum strings — do not guess** | `is.workflow.actions.askllm` (`WFAskLLMAction`, "Use AI Model"), full v78 parameter schema confirmed present on **both** `["iOS 27 Simulator","macOS 27"]`: `WFLLMPrompt` (str, the request text), `WFLLMModel` (typed enum `com_apple_shortcuts_wfask_llmmodel_parameter` — **no enum-case list found anywhere in the bundled `toolkit-v78-first-party-enum-cases.json`**; the only observed literal value across every example in `EXAMPLES.md`/`VARIABLES.md` is the string `"Apple Intelligence"`, which pre-dates the OS26 three-way model picker described by external sources), `WFAllowWebSearch` (bool, "Use Broad World Knowledge," OS27-gated — omit at target macOS 26), `FollowUp` (bool, OS27-gated — omit), `WFGenerativeResultType` (str, "Output" — observed literal value `"Text"` in every example; no evidence of a documented JSON/structured-output literal value in this bundle, though `WFGenerativeResultType` is clearly the intended structured-output switch). **External corroboration (web search, not part of Playground bundle, MEDIUM confidence):** Apple's own iOS 26 documentation and MacStories reporting confirm the Use Model action's UI picker offers exactly three sources — **On-Device**, **Private Cloud Compute**, and **Extension Model (ChatGPT/GPT-5)** — and that the action supports structured/deterministic output despite LLM non-determinism, and that inputs can include variables/outputs from previous actions. **Neither source gives the exact plist string Playground/Apple use for the On-Device enum case** (`"On-Device"`? `"On Device"`? an integer code?). | **This is the single most important UNVERIFIED item for the Sentient fork and must not be guessed.** PROJECT.md's hard constraint is "never claim to know" + "if it cannot be verified, use the safest fallback, record the deviation, keep the Shortcut runnable" — apply that literally here: (1) build the `Use Model` action with `WFLLMPrompt` + `WFGenerativeResultType="Text"` first and get it signing/importing; (2) on a real Apple-Intelligence-capable iPhone, open the imported action in Shortcuts.app, manually select **On-Device** in the Model picker, save, then either export the signed `.shortcut` and recover its plist via §8 or use Share → Copy for unsigned XML, then read back the resulting `WFLLMModel` literal; (3) hardcode that confirmed literal into the Sentient build and record it in build notes as a verified-on-device fact, not a Playground-bundle fact. Until that round-trip is done, treat On-Device pinning as **unconfirmed** and gate all `Use Model` calls behind the `ai_enabled`/on-device-capability check the canonical strategy already requires, with a deterministic fallback path (§14.2–14.5) that never depends on the model literal being right. |
| 16 | Get App & Website Data (Screen Time telemetry) | **VERIFIED identifier and parameter schema** | `com.apple.intelligenceplatform.IntelligencePlatform.IntelligencePlatformDataActionsAppIntentsExtension.CalculateAppUsageIntent`, display name **"Get App & Website Activity."** Present in `toolkit-v63` (the generic/pre-OS27 snapshot) **and** the v78 first-party parameter catalog with full schema, tagged available on **both** `["iOS 27 Simulator","macOS 27"]`: `during` (temporal-options enum), `selectedDevice` (device-activity-device entity), `activityType` (app-usage-activity-options enum), `startTime` (DateTime), `endTime` (DateTime). | Matches canonical strategy §24's "Get App & Website Data" reference almost exactly (identical concept, Apple's actual action name is "Get App & Website Activity"). Per PROJECT.md this is explicitly **out of scope for v1** ("research/measurement only, later phase") — audited here for completeness. Because it's present in the generic v63 snapshot, it should be available at the project's `--target-macos 26` validation target; the `activityType`/`during` enum case values were not found in the enum-cases catalog and would need Craig-Loop/on-device confirmation whenever Phase B picks this up. |

### Summary table

| Capability | Verdict |
|---|---|
| Get Current App | VERIFIED |
| Get File / Save File | VERIFIED (existence check: NOT AVAILABLE) |
| Dictionary / JSON | VERIFIED |
| Date arithmetic | VERIFIED |
| Notes (Create/Append/Find/Show) | VERIFIED (macOS-catalog only, standard iOS action — verify on-device) |
| Ask for Input / Choose from Menu / Choose from List | VERIFIED |
| Open App / Open URL / Web Search / Maps | VERIFIED |
| Set Brightness | VERIFIED |
| Get current brightness | UNVERIFIED (external evidence only, no Playground schema) |
| Set Volume | VERIFIED (identifier only, schema unconfirmed) |
| Get current volume | UNVERIFIED (external evidence only) |
| Set Color Filters / grayscale + readback | **NOT AVAILABLE on iOS** |
| Speak Text | VERIFIED (identifier) |
| Lock Screen | VERIFIED (zero-param, cross-platform confirmed) |
| Run Shortcut | VERIFIED (identifier only, params unconfirmed) |
| Wait / Wait to Return | VERIFIED (identifiers only, params unconfirmed) |
| Use Model — action & most params | VERIFIED |
| Use Model — On-Device model-source literal | **UNVERIFIED — do not guess, confirm via device round-trip** |
| Get App & Website Data | VERIFIED (out of scope for v1) |

## 4. Control-flow primitives

- **If / Otherwise / End If**: all three are the *same* identifier, `is.workflow.actions.conditional`, distinguished only by `WFControlFlowMode` (`0`=If, `1`=Otherwise/Otherwise-If, `2`=End If) sharing one `GroupingIdentifier` per block. **Every** condition code (including 0–3, which older docs wrongly called "implicit input") requires an explicit `WFInput` wrapped as `{Type:"Variable", Variable:{...}}` — this was re-verified against an Apple-built sample and is a hard rule, not a style preference. Full condition-code table (0=less than, 1=≤, 2=greater than, 3=≥, 4=string is, 5=string is not, 8=begins with, 9=ends with, 99=contains, 100=has any value, 101=does not have any value, 999=does not contain, 1003=is between) is in both `CONTROL_FLOW.md` and `BEST_PRACTICES.md`, byte-for-byte consistent. **Common bug the docs specifically warn about:** code `0` is "is less than," not "equals" — there is no numeric-equals code; use string code `4` on text-coerced numbers or an Any-of-two (≥N AND ≤N) block instead.
- **Repeat (count)** and **Repeat with Each**: same two-endpoint (`0`/`2`) `GroupingIdentifier` pattern. Inside the loop, reference `Repeat Index`/`Repeat Item` as **named `Type: Variable`**, never as `ActionOutput` pointing at the end action's UUID — using `ActionOutput` is the single most emphasized "will silently fail at runtime, showing as Repeat Results in the UI" mistake across the whole doc set.
- **Choose from Menu**: mode 0 (menu def, `WFMenuItems` array) → N mode-1 cases (`WFMenuItemTitle`, exact string + exact order match to `WFMenuItems`) → mode 2 (end). Menu title mismatches or out-of-order cases are called out as the top real-world failure mode ("Important Notes from 127 real shortcuts analysis").
- **Nesting**: confirmed working to **depth 7** in a real production shortcut (`AppRedirect.xml`, cited in the corpus analysis). Every nesting level needs its own unique `GroupingIdentifier` — this is the exact "GroupingIdentifier/UUID wiring" warning PROJECT.md and the canonical strategy both flag as something the agent must inspect manually, and it is well-founded: it's the #1 documented "common mistake."
- **Multi-condition If** (Any/All): a *separate* serialization (`WFConditions` + `WFContentPredicateTableTemplate`, `WFActionParameterFilterPrefix` 0=Any/1=All) that must **not** be mixed with the single-condition `WFCondition`/`WFInput` pattern on the same action — the validator hard-rejects mixing them.
- **Otherwise If** (used as "middle" branch with its own condition) is not a new identifier — it's mode 1 *with* condition fields present, vs. plain Otherwise which is mode 1 with none.

## 5. Variable wiring

- **Named variables** (`Set Variable`/`is.workflow.actions.setvariable`, `WFVariableName` + `WFInput`) vs. **magic variables** (direct `ActionOutput` references via `OutputUUID`+`OutputName`, or special `Type` values `CurrentDate`/`Clipboard`/`Ask`/`ExtensionInput`/`DeviceDetails`/`CurrentApp` with no extra params). PROSOCHĒ's `state.json` fields (heat, gravity, pressure, circle, active_session, etc.) should mostly be named variables set once per OPEN/CLOSE pass and referenced by name, per `BEST_PRACTICES.md`'s "prefer inserting named variables directly into action input fields; avoid redundant Get Variable → next action hops."
- **`WFVariable` / `OutputUUID` / `OutputName` token structure:** every `attachmentsByRange` entry is `{OutputUUID, OutputName, Type: "ActionOutput"}` keyed by a `{position, length}` range into the string; `length` is always `1` (the `` U+FFFC placeholder is exactly one character). The **specific wiring mistake Playground says to inspect manually** is the **Display vs. Non-Display parameter distinction**, called out as "CRITICAL — runtime-verified" and backed by a stat ("all 46 Show Alert and 41 Notification instances across 127 real shortcuts use `WFTextTokenString`"): display-facing text (`WFAlertActionMessage`, `WFAlertActionTitle`, `WFNotificationActionBody`/`Title`, `Text` in Show Result) **must** use `WFTextTokenString` with a `` placeholder even for a single bare variable — using `WFTextTokenAttachment` there imports fine and validates fine but silently shows default/empty text at runtime. Non-display data-flow parameters (`WFInput`, `WFDate`, `WFVariable`, `WFDictionary`) can use the shorter `WFTextTokenAttachment` form.
- Other manually-inspect-worthy wiring bugs the docs name explicitly: `attachmentsByRange` positions must exactly match `` character offsets in the *final* string (a single later text edit invalidates all downstream offsets — "recompute positions if the surrounding text changes"); out-of-bounds ranges "can crash Shortcuts on import"; Repeat Index/Item must be `Type: Variable` not `ActionOutput` (repeated from §4 because it recurs as a top mistake in both docs).

## 6. Practical size/complexity limits

- **Runtime complexity / variable wiring correctness** — not size per se, but the *density* of wiring mistakes scales with action count; this is why the Craig Loop, the comment-density rule ("8+ actions require ≥3 comments, 16+ require ≥4, 24+ require ≥5"), and the mandatory pre-control-flow-block comment convention exist.
- **`GroupingIdentifier` collisions at depth** — the more nested control flow, the more places a copy-paste or reuse error can silently corrupt a block boundary (§4).
- **Comment-block bloat vs. readability** — `BEST_PRACTICES.md` recommends section-header Comments (`--- FETCH TASKS ---` style) for any shortcut over ~20 actions, which PROSOCHĒ (a large stateful single-shortcut design spanning bootstrap, OPEN, CLOSE, nine Circles, six exits, Control Room menu) will need extensively.
- **Model latency** (Sentient only) — canonical strategy's own §14.5 concern (don't force inference onto every early-Circle OPEN); not a Playground finding, a product-design one.
- **Notes parsing cost at scale** — again a canonical-strategy concern (§5.4), not a Playground one, and already correctly designed around (JSON hot path, Note as append-only ledger).

## 7. Import questions (`WFWorkflowImportQuestions`)

- **The validator does not check `WFWorkflowImportQuestions` at all** — `scripts/validate_shortcut.py` has zero references to the key. Correctness here is entirely the build agent's responsibility; a malformed import question will not be caught by the Craig Loop.
- Because each question targets one literal parameter field, PROJECT.md's Layer-A import questions ("Choose your descent: Paradise/Limbo/Inferno," "Use on-device intelligence? yes/no," "May PROSOCHĒ speak? yes/no") must each be implemented as: a **Text** action holding the literal default (e.g. `WFTextActionText = "Limbo"`) targeted by one import question with `Text` = the prompt, whose output is then read at bootstrap-time and mapped/validated (e.g. an If-chain matching the text against `Paradise`/`Limbo`/`Inferno`) rather than as a native yes/no or single-select import-time control. This is consistent with the canonical strategy's own instruction (§7.1) to "use `WFWorkflowImportQuestions` only for simple, robust parameters" — the plist evidence shows exactly why: it's a literal-text-prefill mechanism, not a rich form-builder.

## 8. Signing and AEA1 round-tripping

- **What produces an importable `.shortcut`:** only `shortcuts sign --mode <anyone|people-who-know-me> --input <unsigned.shortcut-or-xml> --output <signed.shortcut>` (the real macOS `shortcuts` CLI, wrapped by `sign-shortcut`). Signing adds roughly 19KB and is what makes Shortcuts.app agree to import the file at all — an unsigned XML/`.shortcut` cannot be imported on-device.
- **Signed artifacts are recoverable:** a signed `.shortcut` is an **Apple Encrypted Archive** (magic bytes `AEA1`). `plutil`, `xxd`, and `file` cannot inspect the outer container as a plist, but agents **may and should** recover its payload when the signed artifact is the available or authoritative evidence. The AEA1 auth-data bplist contains its `SigningCertificateChain`; extract the leaf certificate's public key, run `aea decrypt`, then unwrap the Apple Archive with `aa extract`. This was proven with `.planning/debug/Donor - notes.shortcut`, exported from the owner's iPhone.

  ```bash
  signed_shortcut="/absolute/path/to/Signed.shortcut"
  inspection_dir="$(mktemp -d)"
  python3 -c 'import struct,plistlib,pathlib,sys; d=pathlib.Path(sys.argv[1]).read_bytes(); sz=struct.unpack_from("<I",d,8)[0]; pathlib.Path(sys.argv[2]).write_bytes(plistlib.loads(d[12:12+sz])["SigningCertificateChain"][0])' "$signed_shortcut" "$inspection_dir/leaf.der"
  openssl x509 -inform DER -in "$inspection_dir/leaf.der" -noout -pubkey > "$inspection_dir/pub.pem"
  aea decrypt -i "$signed_shortcut" -o "$inspection_dir/payload.aa" -sign-pub "$inspection_dir/pub.pem"
  mkdir -p "$inspection_dir/unwrapped"
  aa extract -i "$inspection_dir/payload.aa" -d "$inspection_dir/unwrapped"
  plutil -convert xml1 -o "$inspection_dir/Shortcut.xml" "$inspection_dir/unwrapped/Shortcut.wflow"
  ```

- **Remixing and source retention:** `shortcut-remixer` still refuses a signed `.shortcut` directly; give it the recovered `Shortcut.xml` instead. Keep the pre-sign unsigned XML as the canonical editable source because it preserves the authored build input and exact source history, but do not treat its absence as making a signed artifact opaque or unrecoverable.
- **Filename discipline:** the signed output filename must equal the intended shortcut display name (no `_signed` suffix) — treating a `_signed`-suffixed library name as a failed build is an explicit rule (`BEST_PRACTICES.md` §Signing & Install Naming). For the two-fork deliverable, this means the two signed artifacts should literally be named `PROSOCHĒ — Nine Circles — Dumb.shortcut` and `PROSOCHĒ — Nine Circles — Sentient.shortcut`.
- **Known signer quirks** (both auto-retried by `sign-shortcut`, but worth knowing): `shortcuts sign` sometimes reports `Error: The file doesn't exist.` for a file that does exist (retry from a clean XML→`.shortcut` copy); sometimes reports `Error: ... isn't in the correct format.` even when `validate-shortcut`/`plutil -lint` both pass (retry after `plutil -convert binary1`). Both retries are built into `sign-shortcut` automatically.

## 9. Agent-side tooling and device-evidence channels

Which evidence channel to reach for when a runtime question is open, and which rung is too high or too low for that question. Tooling measured 2026-08-17.

| Tool | How it is reached | Availability |
|---|---|---|
| `/ponytail` | The `anthropic-skills` skill — laziest solution that actually works: YAGNI, standard library and native platform features before dependencies, minimal diffs | Sanctioned. Prefer the minimal change — but laziness never licenses skipping the nine parameter-defect axes under `## Conventions` or the do-not-fabricate protocol in `docs/BUILD-NOTES.md` §2. |
| iOS Simulator | `mcp__Claude_Code_iOS_Simulator__control` (actions `attach`, `launch`, `screenshot`, `tap`, `swipe`, `text`, `button`, `open_url`, `detach`), plus `xcrun simctl` from Bash | Always available on this Mac. |
| iPhone Mirroring | Real-device UAT on the owner's iPhone | Not always live; the user sets it up on request. |

**Measured simulator inventory (2026-08-17).** `xcrun simctl list runtimes` reports exactly one runtime, **iOS 26.5 (26.5 - 23F77)** — inside the project's declared "iOS 26.x" target, so a simulator observation is same-major-version evidence rather than a version extrapolation. `xcrun simctl list devices available` reports iPhone 17 Pro `79A84C29-DB62-40A2-AC3F-CCB5F8192F86` **Booted**, among five iPhones and five iPads. `xcrun simctl listapps 79A84C29-DB62-40A2-AC3F-CCB5F8192F86` reports 25 apps: `com.apple.shortcuts` **present**, `com.apple.mobilenotes` **absent**. Re-run all three to re-derive every simulator claim in this section.

### The evidence-escalation ladder

| Rung | Channel | Settles | Costs |
|---|---|---|---|
| 1 | File-level analysis — validator, ToolKit catalog, golden corpus, decrypted plist | Structure, identifier presence, parameter shape | Nothing |
| 2 | Simulator probe — the agent builds, signs, imports, runs and observes it itself | Import success, runtime variable resolution, control flow, operator/operand type validity, most parameter-key questions | Agent time only |

**The rung-2 row above is CONFIRMED, and its 2026-08-17 narrowing is RETIRED — measured by spike `010-coercion-at-a-direct-set-parameter`, 2026-08-18.** Spike 007 had concluded the booted simulator cannot import a signed `.shortcut` through any channel, and narrowed "import success" out of this row. It was wrong, and this row as originally written was right. The working channel:

```bash
open -a Simulator                                          # a simctl-booted sim has NO window until this
xcrun simctl openurl <udid> "file:///abs/path.shortcut"    # → the Shortcuts import sheet
# then ONE synthesized tap on "Add Shortcut" completes the import
```

Spike 007's `file://` row was measured against the **MCP simulator tool's scheme allowlist**, not against `simctl`. Its other four rows stand: `shortcuts://import-shortcut` genuinely does require an iCloud link (re-measured 2026-08-18 — a `file://` URL with `silent=true` is still rejected, because the URL is refused before the flag is consulted), Files never surfaces "On My iPhone", iCloud Drive needs an Apple Account. `openurl` with a plain file URL never goes through the `shortcuts://` scheme at all.

Two things that cost real time and are invisible until hit: coordinates must be **fractions of the device screen mapped through the window rect measured at run time**, never pixels; and **`Show Alert` modals accept neither a synthesized tap nor a hardware Return** — the run wedges permanently at the first one, while ordinary in-app UI (buttons, scrolling) takes taps normally. Build simulator-bound probes with **no blocking UI**. Instrument and every dead end: `.planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/sim_input.py`.
| 3 | Device probe over iPhone Mirroring — the agent drives the user's iPhone | Everything the simulator cannot | One connected session, requested from the user |
| 4 | User-run probe or donor export on the real device | Anything mirroring cannot reach, or that needs the user's own hands | The user's time — the scarcest input |

**The governing rule: never climb higher than the open question requires, and never skip a rung that would have caught a defect in the probe itself.** Both halves bite. Climbing early spends a scarce device session on something rung 1 or 2 would have settled for free; skipping a rung hands the device a probe that fails for a reason unrelated to the question it was built to answer.

This ladder **extends** the four-item `### Evidence hierarchy` under `## Conventions`, supplying the probe and simulator rungs that list omits. It does not replace it, and the donor's rank there is unchanged.

### Rung 2's ceiling — what a simulator pass may never close

A rung-2 pass may **not** raise a verdict on any of the following. Each is device-gated for a measured reason:

- **The Control Room Note path, in full.** `com.apple.mobilenotes` is absent from the booted simulator's 25 apps, measured above — so every `com.apple.mobilenotes.SharingExtension`, `appendnote`, `filter.notes` and `shownote` behaviour needs rung 3+.
- **Apple Intelligence.** The simulator is not Apple-Intelligence-capable hardware, so the Sentient `Use Model` / On-Device path (CAP-26, BD-04-R2) needs rung 3+.
- **Personal Automation triggers** (App Is Opened / Is Closed). They are user-created on the device and cannot be exercised on a simulator at any effort.
- **Real-hardware environmental behaviour** — brightness and volume capture-and-restore. **Sharpened 2026-08-18 by spike `010-coercion-at-a-direct-set-parameter`: `Set Brightness` cannot succeed on a simulator AT ALL** — it returns *"There was a problem setting the brightness"* — and `Get Device Details → Current Brightness` reads **`0`** there. So whether an operand is actually *consumed* by these actions is device-gated no matter how good the import channel is. A simulator brightness/volume reading is never promotable above `UNVERIFIED`.

Two findings from the same spike that change how these questions must be asked:

- **The "coercion chip does not render red" gate does NOT work at a direct Set-action parameter.** A conditional's operator picker is populated from the operand's static type, so a mismatch renders red; **`Set Brightness` has no operator picker**, so coerced and uncoerced operands render **identically**. A green chip there is not weak evidence, it is *no* evidence. The gate remains valid for conditionals (`## Conventions`, "Operator/operand type validity is invisible in the plist") and only there.
- **`setbrightness.WFBrightness` is OPTIONAL and defaults to 50%.** An absent operand renders as "Set brightness to 50%" and does **not** raise the unfilled-parameter error. So an unresolved operand fails **silently**, applying an unrequested 50% rather than halting. Any device test of these actions must verify **the value applied**, never merely the absence of an error.

### Rung 3's ceiling — what iPhone Mirroring may never close

Rung 2 has had a written ceiling for a while. **Rung 3 has one too, and it went unrecorded until
a session ran into it**, so it is stated here rather than rediscovered.

- **Every brightness observation.** Measured 2026-08-19 on the paired iPhone 15 Pro over
  Mirroring, with a two-action probe built on the phone: `Get Device Details → Current Brightness`
  reads **`0`**, while `Current Volume` reads correctly (`1`) and `Device Is Locked` reads
  **`No`**. So the `0` is *not* attributable to a locked device; the leading explanation is that
  the phone's physical display is off while mirrored, and that is itself untested. The practical
  consequence is absolute: `dimming()`'s numeric `> 0` capture gate can never pass over Mirroring,
  so **Dimming always short-circuits and no brightness behaviour is observable at this rung** —
  no matter how good the instrument is. **A brightness reading taken over Mirroring is never
  promotable above `UNVERIFIED`, and must never be written up as "brightness cannot be captured
  on iOS 26".** That claim needs rung 4: the user, phone in hand, unmirrored.
- **Volume carries no such restriction.** The full capture → persist → apply → restore → clear
  cycle was proven at rung 3 for volume (`1` → `0.1` → `1`, both restore paths). Do not
  generalise the brightness ceiling to the whole environmental class.
- **Anything that needs the Mac awake.** Mirroring cannot run behind the macOS login window, so a
  long-running or overnight rung-3 session dies the moment the Mac locks — silently, from the
  agent's point of view, since `state.json` stays readable through iCloud the whole time. Arm
  `sudo pmset -a sleep 0 displaysleep 0` before any unattended session, or run at rung 4.

Evidence for all of the above: `.planning/debug/device-state/README.md`, findings F-13, F-14 and
F-23.

**One instrument-scope note that belongs with these.** The Control Room's `Test a Circle` menu
exercises a primitive's **UI** but not its **session-dependent state**: with no live session,
`persist_contract()` correctly declines to write, so no contract test can be settled that way.
Reaching the primitive from a real OPEN is the only route for anything that touches
`active_session` (finding F-17).

### Probes and donors

A **donor** is evidence the user already happens to have. A **probe shortcut** is evidence we deliberately manufacture, so it can be aimed at precisely the open question rather than at whatever the donor happened to contain. Both are first-class instruments; they differ in provenance and in aim.

A genuinely-open rung-2 target today: the **unaudited `CoercionItemClass` values for boolean, file, dictionary and entity-reference operands** (`## Conventions` rule 6). Pure runtime operand-type resolution — it needs no Notes, no model and no real hardware, which is exactly what makes it a rung-2 question rather than a rung-3 one.

### Two standing policies

- **Probes are simulator-tested before they reach the user's iPhone**, wherever the scope is small enough for the simulator to exercise them. Handing over an untested probe is a defect, not a shortcut. A probe that fails on import, or fails for a reason unrelated to the question it was built to answer, burns a device round trip and teaches nothing — and `## Conventions` ("Read the error text, not just the letter") already records that misattributed failures cost this project multiple cycles.
- **Maximise UAT over iPhone Mirroring.** When mirroring is live the agent drives the device itself rather than issuing the user a list of taps. Requesting the session is unchanged — the agent must still ask for it, and must name specifically what needs to be observed — but once connected, exhaust what can be observed before handing the session back.

### The recording duty

A probe's result is **recorded, not consumed**: into `docs/BUILD-NOTES.md`'s device-evidence sections, and into `docs/CAPABILITY-DECISIONS.md` where it settles a capability question. Probes are cheap to build and expensive to re-run; the record is the whole return on them.

## Recommended Stack

### Core toolchain

| Component | Version | Purpose | Why |
|---|---|---|---|
| Shortcuts Playground plugin | v1.2.1 (installed) | Skill docs, agents, validator, signer, hooks | The only tool on this machine capable of authoring, validating, and signing `.shortcut` files; ground-truthed against Apple's own ToolKit databases |
| `shortcuts` CLI (macOS built-in) | whatever ships with the build Mac's OS | `shortcuts sign` — the real signer | No substitute exists; signing is macOS-only |
| Python | ≥3.10 | Runs `validate_shortcut.py` (uses PEP 604 `X | None` syntax) | Hard requirement of the bundled validator; check via `shortcuts-playground-selftest` |
| Validator target | Gate A (mandatory): `--target-macos 26 --target-platform all`, satisfied by `python3 docs/gate_a_residue_check.py`. Gate B (advisory): `--target-macos 27 --target-platform all` | Gate A is the identifier/availability baseline at the project's real target; since 2026-08-19 its obligation is that the **residue equal exactly the enumerated waiver** (two line families, one identifier, 30 lines per fork), not that the report be empty. Gate B is the parameter-key and picker-literal read, waivered and never blocking | The **two-gate rule**, both waivers and their mechanism are stated once, in §1 `### Exact validator invocation` |

### Build sequencing recommendation (per project's own stated order)

## Installation

## What NOT to use

| Avoid | Why | Use instead |
|---|---|---|
| Fabricating an action identifier because the canonical strategy asks for it (e.g. inventing a "grayscale toggle" or "get current volume" action) | Both PROJECT.md and the Playground's own agent rules explicitly forbid this; several capability-audit items above have no verified schema | Follow the escalation path: safest fallback + record the deviation, or the on-device round-trip technique used for the Use Model literal (§3 item 15) |
| `WFTextTokenAttachment` on display-facing text fields (`WFAlertActionMessage`, `WFNotificationActionBody`/`Title`, Show Result `Text`) | Runtime-verified to silently render blank/default text even though it validates and imports fine | `WFTextTokenString` with a `` placeholder, even for a single bare variable |
| `ActionOutput` references to Repeat's end-action UUID for `Repeat Index`/`Repeat Item` | Shows up as "Repeat Results" in the UI and fails at runtime | Named `Type: Variable`, `VariableName: "Repeat Index"`/`"Repeat Item"` |
| Reusing a `GroupingIdentifier` across nested or sibling control-flow blocks | Silently corrupts block boundaries — the #1 documented real-world mistake in the corpus analysis | A freshly `uuidgen`'d, uppercase UUID per control-flow block, no exceptions |
| Treating `plutil`/`xxd`/`file` failure on the outer signed `.shortcut` as proof that its plist is unrecoverable | Those tools see the AEA1 container, not the plist payload | Use §8's `aea decrypt` → `aa extract` workflow, convert `Shortcut.wflow` to XML, then inspect or pass that XML to `shortcut-remixer` |
| Treating `--target-macos 27` as the sole or mandatory gate | At target 27 the validator may *accept* an OS27-only parameter key that iOS 26 does not offer, so it can produce false acceptances. It is a supplement, never a replacement | Gate A mandatory + gate B advisory — the **two-gate rule**, §1 `### Exact validator invocation` |
| Pairing the iOS platform flag with `--target-macos 26` | Both bundled snapshots are filtered out — one by the platform gate, one by the version gate — leaving an empty allowlist that rejects 3675 of 3675 actions. A check that fails 100% of its inputs carries zero signal | Gate A: `--target-macos 26 --target-platform all` |
| Chaining the **raw** gate-A validator command into an `&&` success condition, or "fixing" its non-zero status by widening the waiver, by synthesising an `AppIntentDescriptor`, by patching the plugin's bundled ToolKit snapshot, or by substituting `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` | Since 2026-08-19 gate A carries a permanent two-family waiver and can never exit zero, so a raw chain is permanently unsatisfiable. Each listed "fix" is worse than the red gate: a wider waiver guts the gate for every other action, a synthesised descriptor fabricates values no donor supplies, a patched snapshot lives outside the repo and is lost on the next plugin update, and the macOS twin buys a green check by shipping an action that does nothing on an iPhone | `python3 docs/gate_a_residue_check.py` — it *is* the gate-A obligation in executable form; investigate any line it reports |
| Treating a validator pass as "done" | The plugin's own explicit rule: "A valid XML draft without a signed `.shortcut` is not a useful stopping point" | Always complete the archive+sign+verify-non-zero-bytes step |
| A CSV or second machine-readable store alongside `state.json` | Explicitly out of scope per PROJECT.md; also has no bearing on the Shortcuts toolchain — not a capability question, a design one, reaffirmed here because Get/Save File audit (§3 item 2) shows Shortcuts' file actions are perfectly adequate for one JSON | One `state.json`, rolling-window arrays, one Apple Note |

## Version Compatibility

| Component | Compatible with | Notes |
|---|---|---|
| Shortcuts Playground v1.2.1 | Claude Code (plugin system, `/plugin` command) | Installed at `~/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/` |
| `validate_shortcut.py` | Python 3.10+ (PEP 604 union syntax) | System `/usr/bin/python3` on older macOS may be 3.9.x — verify via `shortcuts-playground-selftest` |
| Validator `--target-macos 26` data | `data/toolkit-v63-tool-ids.json` (generic snapshot) | Does **not** load the v78 OS27-only parameter-key/enum catalogs — this is deliberate and correct for this project |
| Signed `.shortcut` output | Apple `shortcuts` CLI on the build Mac | Signing is macOS-only; cannot be done on Linux/CI without a Mac in the loop |
| `Use Model` (`askllm`) On-Device pinning | Apple-Intelligence-capable iPhone (15 Pro+) running iOS 26+ | Cannot be verified or tested on the build Mac alone — requires the on-device round-trip described in §3 item 15 |

## Sources

- `/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/skills/shortcuts-playground/{SKILL,BEST_PRACTICES,PLIST_FORMAT,ACTIONS,APPINTENTS,CONTROL_FLOW,VARIABLES,DATE_TIME,PARAMETER_TYPES,FILTERS,TOOLKIT_SNAPSHOT,EXAMPLES}.md — read in full or targeted-grep, HIGH confidence (installed ground truth)
- `/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/skills/shortcuts-playground/data/{toolkit-v63-tool-ids,toolkit-v78-tool-ids,toolkit-v78-ios27-tool-ids,toolkit-v78-first-party-parameter-keys,toolkit-v78-first-party-enum-cases}.json — queried directly via Python, HIGH confidence
- `/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/skills/shortcuts-playground/golden-shortcuts/{index.jsonl,xml/*.xml}` — 19 real shortcuts, used to recover the `WFWorkflowImportQuestions` schema, HIGH confidence
- `/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/{bin/validate-shortcut,bin/sign-shortcut,agents/shortcut-builder.md,agents/shortcut-remixer.md,README.md,INSTALL.md,CHANGELOG.md}` — HIGH confidence
- Apple Support, "What's new in Shortcuts" (support.apple.com/en-us/101583) — via web search snippet only, MEDIUM confidence, cited for Get Device Details brightness/volume properties (exact key names unconfirmed)
- MacStories/TechCrunch/AppleInsider coverage of the iOS 26 "Use Model" action's three-way model picker (On-Device / Private Cloud Compute / ChatGPT) — MEDIUM confidence, cited for model-source existence only; exact plist enum literal NOT obtained from any source and must be confirmed via on-device XML export before Sentient depends on it

<!-- GSD:stack-end -->

## Conventions

### Generator authoring rules — the nine parameter-defect axes

Every rule below is asserted by a build guard in `tools/build_state_engine.py`, and each axis
was invisible to the sweep that caught the previous one. **Violating any of these produces
a plist that validates, signs, imports, and then fails at runtime** — usually with a
misleading message attributed to the outermost caller.

**Provenance differs per axis, and the difference is load-bearing.** Reading them all as
on-device evidence promotes a file-level inference to a device observation, which is the exact
inversion the evidence hierarchy exists to prevent:

- **Axes 1–7** — established by **on-device failure** during the 2026-08-13/14 OPEN-path debug
  session.
- **Axis 9** (compound value) — established by **device error** at cycle 15 ("Get Dictionary
  Value failed because Shortcuts couldn't convert Text to Dictionary").
- **Axis 8** (`WFItems` row wrapper) — established by **device-authored donor decrypt** (Donors
  4 and 4.1, 2026-08-17), which is rung 1 of the evidence ladder read against rung-4 artifacts.
  It is **structurally proven and NOT yet device-observed in this project's own artifact**:
  `13-UAT.md` is recorded `BLOCKED`, `MANIFEST.md` and `docs/BUILD-NOTES.md` §28 say the same,
  and the visible symptom it predicts — a Mirror alert whose body is empty — has never been
  looked at on a phone. Do not cite axis 8 as device evidence.

1. **Parameter key names** must match the ToolKit catalog exactly.
   `setvalueforkey` takes `WFDictionaryValue`, not `WFInput`. A key the action does not
   define is silently ignored and the field reads empty.
2. **String-typed parameters** (catalog type `str`) require a `WFTextTokenString`
   (`￼` placeholder + `attachmentsByRange`). A bare `WFTextTokenAttachment` resolves to
   empty at runtime.
3. **`AttributedString`-typed parameters** — e.g. `WFCreateNoteInput` — need the same
   `WFTextTokenString` treatment. `AttributedString` is a text type; a type-scoped sweep
   that only looks for `str` will miss it.
4. **Required picker (enum) parameters** must be present and hold a literal enum case.
   `count.WFCountType` and `getitemfromlist.WFItemSpecifier` are the known instances. An
   unfilled picker reports as "Please choose a value for each parameter in this action."
5. **Variable slots take the opposite envelope from string parameters.**
   `WFInput.Variable` requires a bare `WFTextTokenAttachment` wrapping a Type-bearing
   descriptor. A `WFTextTokenString` there is not a variable reference and cannot resolve.
   Rules 2 and 5 are inverses; check which position you are in before choosing.
6. **Non-text parameters fed by a variable reference require an explicit coercion
   aggrandizement.** This is the most general and most under-applied rule:

   ```xml
   Aggrandizements = [{ Type: WFCoercionVariableAggrandizement,
                        CoercionItemClass: WFNumberContentItem }]
   ```

   Without it the operand is untyped or text-typed. Confirmed necessary for numeric
   comparison; confirmed **missing** for date parameters (`gettimebetweendates.WFInput`,
   `WFTimeUntilFromDate`, `adjustdate.WFDate`, `format.date.WFDate`). Booleans, files,
   dictionaries and entity references are **unaudited**. Establish each `CoercionItemClass`
   from donor or corpus evidence — never guess it.
7. **State shape must exist before it is read.** See the runtime semantics below: a dotted
   read raises if any segment is absent, so bootstrap must seed the full subtree.

   **The container/leaf refinement, `pending_exit` (cycle 16, generalised Phase 12–13).**
   Seeding is only half the rule; the other half is never destroying what was seeded. Seed
   the **container** as a **permanent invariant** at bootstrap, then write and clear only its
   **leaves** — never the container itself. Replacing a container wholesale with a sentinel
   string is what reintroduces this axis one run later: the next dotted read runs against a
   string parent and hard-errors, presenting as a regression rather than as the same defect.
   Gate on a string is-not-sentinel test (condition code 5) or on a numeric greater-than-zero
   test; **never** on a condition-100 existence test over the container. A read-then-existence
   gate on a dotted path is unimplementable — the read raises on any missing segment, so the
   gate is either unreachable or trivially true. `seed_pending_exit()` establishes the
   container and `clear_snapshot()`'s docstring states the same rule for
   `settings_snapshot.<key>.original_value`, both in `tools/build_state_engine.py`.
8. **A `WFItems` List row takes one of exactly two shapes, and the wrapper is the ROW's
   framing rather than the value's envelope.** A **literal** row is emitted as a bare string
   directly in the `WFItems` array. A **variable- or attachment-bearing** row is wrapped as
   `{"WFItemType": 0, "WFValue": <the complete, unchanged WFTextTokenString>}`. A raw
   `WFTextTokenString` placed directly into `WFItems` validates, signs and imports perfectly,
   and then renders as an **empty row** on device — so a Get Item From List selection over
   that array can land on a blank template.

   **This is a CONTAINER defect and therefore a distinct axis, not an instance of axis 2.**
   At a defective site the envelope inside `WFValue` is *already correct*; what is missing is
   the row framing around it. A type-scoped sweep hunting a wrong or absent string envelope
   cannot see this class at all, because there is no wrong envelope to find.

   Evidence: `.planning/debug/Donor 4.shortcut` and `.planning/debug/Donor 4.1.shortcut` —
   device-authored, decrypted in Phase 13, byte-identical on this action, and showing **both**
   row kinds mixed in one array (`"Circle"`, a wrapped `Dictionary Value` token, `"follows"`).
   **Discriminate on attachment-bearing-ness, NOT on Python type.** This is the correction that
   cost a full re-ship in Phase 13: an `isinstance(item, str)` discriminator wraps every non-`str`,
   including a `WFTextTokenString` built from a template with no `￼` placeholder and therefore an
   **empty `attachmentsByRange`**. That is a literal row by content, encoded as a variable row — a
   second unevidenced framing, invisible to the guard, the validator and the decrypt, and it
   shipped. A row is LITERAL when it carries no attachment, whatever its Python type; only an
   attachment-bearing row takes the wrapper. Sweeping every row likewise corrupts the legitimate
   bare-string literals.

   Build guard: `verify_list_item_wrappers()` in `tools/build_state_engine.py`, armed on both
   forks. It asserts the whole row contract — the `WFItemType` **key is present** and never which
   value it holds, `WFValue` is present and well-shaped, and a wrapped row's
   `WFValue.Value.attachmentsByRange` is **non-empty** (the inverse assertion that catches the
   defect above). Anchor on the symbol, not the line.

   Boundary: only `WFItemType` `0`, a **text** row, is donor-observed. Neither donor exercises
   a number, dictionary or file row, so any other value must be established from evidence and
   must never be inferred from `0`.
9. **A COMPOUND state value consumed as a List is read with `get_value()`; a SCALAR used in a
   text or numeric comparison is read with `read_value()`.** `read_value()`'s extra Get Text
   step is the correct coercion for a scalar headed into a comparison, and exactly wrong for a
   compound value: the array collapses into one Text blob before any List consumer sees it, so
   a Repeat With Each iterates wrong or not at all and a Get Item From List returns that blob
   instead of a genuine Dictionary item. The downstream Get Dictionary Value then fails with
   "couldn't convert from Text to Dictionary" — device-confirmed at cycle 15, breadcrumb E→F,
   at `recent_sessions`.

   `COMPOUND_STATE_KEYS` in `tools/build_state_engine.py` names the four literal members:
   `recent_sessions`, `recent_contracts`, `exit_events` and `profile_snapshot.enabled_exits`.
   A fifth instance, `exit_stats.<name>.samples`, is real but dynamically keyed, so it cannot
   be matched by a literal-key scan and is recorded beside the frozenset rather than inside
   it. Build guard: `verify_compound_value_reads()`, which deliberately does **not** flag a
   compound value read only for text DISPLAY — the defect is the structural consumer
   downstream, not the read alone.

### Verified iOS Shortcuts runtime semantics

Established by user-built donor shortcuts on the target iPhone. These are **not** in the
Playground bundle and cannot be derived from the plist.

| construct | behaviour |
|---|---|
| flat read of a **missing** key | returns nothing, no error → `has any value` **false** |
| flat read of a **present but empty** value | → `has any value` **true** |
| **dotted** read (`a.b`) with any missing segment | **hard error**, "could not evaluate the key path" |
| **dotted WRITE** (`set` `a.b`) | creates a **literal flat top-level key** `"a.b"`; the nested subtree is left untouched |
| **dotted read** when a literal `"a.b"` key exists | returns **that flat key's value**; no traversal happens, so the nested subtree is shadowed |
| a Shortcuts List of **exactly one item**, serialised into the dictionary | stores as the **bare item**, not a one-element array; becomes a real array at n ≥ 2 |
| `"null"` or `""` coerced to `WFNumberContentItem` | **false**, no error |

**The last three rows were established 2026-08-18/19** — the write/read pair by analysing a
`state.json` the device itself wrote, then re-confirmed live on the shipped build; the
single-item collapse by watching `recent_sessions`, `exit_events` and
`exit_stats.<Exit>.samples` each do it independently. Evidence:
`.planning/debug/device-state/README.md`, findings F-4 and F-20.

**Why the write/read pair matters more than it looks.** The two halves agree, so the state
engine is self-consistent and correct — this is not a bug to chase. What it changes is **where
you look**. Any check that reads a nested container to confirm a write landed will report a
**false negative**: the value is in the flat key and the nested block still holds its bootstrap
sentinel forever. That very nearly cost this project a wrong verdict on phase 16's central
test. When verifying a dotted write on device, read the **flat top-level key**.

It also refines axis 7 rather than replacing it. Seeding the container is still required — it is
what the **first** read falls back to, before any flat key exists, and without it that read
traverses a missing segment and hard-errors. But the axis-7 phrasing "write and clear only its
**leaves**" describes an intent the runtime does not implement: the leaves being written are flat
keys, not leaves of the seeded container. Seeding also does **not** prevent the single-item
collapse — `exit_events` was correctly seeded `[]` and the first exit still wrote a bare object.

**Consequence — a read-then-`has any value` gate on a dotted path is unimplementable.**
The read raises unless the final key exists; if it exists, the gate is true. There is no
state in which the gate reads false without the read having already thrown. No sentinel
value fixes this. Gate on a numeric `> 0` test, or restructure to a flat read.

### Operator/operand type validity is invisible in the plist

Shortcuts offers comparison operators based on the **left** operand's resolved type:

- **Dictionary Value** (uncoerced) → only `has any value` / `does not have any value`
- **text-coerced** → the eight string operators only
- **Number-coerced** → numeric comparators available

A numeric `WFCondition` on a text-typed operand renders **red** in the UI, is structurally
valid in the file, and fails at runtime. **No file-level analysis can detect this** — not
the validator, not the catalog, not decrypting the signed artifact. Inspecting the
imported shortcut on device is a first-class evidence channel here, not a fallback.

### Evidence hierarchy

When sources disagree, prefer in this order:

1. **Device ground truth** — user-built donor shortcuts, decrypted, and probe results
   observed on the real iPhone (§9 rungs 3–4)
2. **Simulator observation** — a probe the agent built and ran itself (§9 rung 2).
   Authoritative for runtime behaviour the simulator can actually exercise, and **never
   above `UNVERIFIED`** for anything inside §9's "Rung 2's ceiling" list
3. **The golden-shortcut corpus** — real-world shipped plists
4. **Apple's `.intentdefinition` files on the build Mac** —
   `/System/Library/PrivateFrameworks/<Framework>.framework/Versions/A/Resources/Base.lproj/Intents.intentdefinition`,
   read via `plutil -convert xml1`, then `INIntents` / `INEnums`. Authoritative for **what
   exists** — exact parameter names, types, enum case ids and their integer indices — but
   **not for plist encoding**: Shortcuts serializes through its own UI rendering and the two
   do not match. Use a donor to learn what actually gets written
5. **The ToolKit catalog** — incomplete; carries no required/optional bit, and the
   control-flow identifiers (`conditional`, `choosefrommenu`, `repeat.*`) are absent from
   it entirely, so catalog-driven sweeps are blind to them
6. Inference — last resort, and record it as a deviation

This list and §9's ladder are complements, not rivals: **this hierarchy ranks authority when
sources conflict; §9's ladder ranks cost and reach when a question is open.** A donor outranks
a simulator probe here, while a simulator probe is reached for first there — both are correct.
A donor is evidence the user already happens to have; a probe is evidence we manufacture, so it
can be aimed at precisely the open question (§9, "Probes and donors").

### Signed `.shortcut` files ARE recoverable

See §8. `aea decrypt` + `aa extract` recovers the plist from the AEA1 container. Use it to
verify what actually shipped rather than trusting the unsigned source plus a file mtime.

### Debugging technique

- **Breadcrumb bisection** — flag-gated alerts at control-flow base depth localise a
  failure to a span in one device run. Keep them in across cycles: a second defect then
  reports as a *later letter* rather than an ambiguous repeat.
- **Read the error text, not just the letter.** Three times this session a correct fix
  looked refuted because the letter was unchanged while the error text had changed
  completely.
- **Fix whole classes, never site-by-site.** Bisection only ever reveals the earliest
  remaining site, so incremental fixing costs one device round trip per site. Every defect
  found this session was systematic: 147, 367, 25, 20 and 8 sites respectively.

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

- **Spike findings for PROSOCHĒ** (donor-confirmed literals, the three-class picker rule, the evidence ladder, Sentient gating, session-model behaviour, environmental-primitive recipes) → `Skill("spike-findings-prosoche")`
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `$gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `$gsd-debug` for investigation and bug fixing
- `$gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `$gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
