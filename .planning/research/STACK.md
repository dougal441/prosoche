# Stack Research

**Domain:** Native iOS 26 Shortcuts automation (adaptive-friction / digital-wellbeing), authored as Shortcuts plist XML via the Shortcuts Playground plugin, optional Apple On-Device Intelligence layer
**Researched:** 2026-08-13
**Confidence:** HIGH for toolchain/paths/validator/signing and most control-flow/variable-wiring facts (read directly from the installed plugin). MEDIUM for several action parameter shapes (present in the plugin's OS27/macOS-only schema catalog but not confirmed for iOS). LOW/UNVERIFIED explicitly flagged for `Use Model` model-source pinning and Get Device Details brightness/volume property names — these are NOT fabricated and must be confirmed empirically during build.

---

## 1. The installed Shortcuts Playground toolchain (ground truth)

There are two copies of the plugin on disk. **Both are functionally identical (v1.2.1)**; the `cache/` copy is what Claude Code actually executes.

| Location | Role |
|---|---|
| `/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/` | **Live plugin root** — this is what `${CLAUDE_PLUGIN_ROOT}` resolves to at runtime. All bin wrappers, skill docs, agents, hooks live here. |
| `/Users/dougalhanson/.claude/plugins/marketplaces/shortcuts-playground/claude/` | Marketplace source copy (mirror of the same files under `skills/`, `agents/`, `bin/`, `commands/`, `hooks/`). |
| `/Users/dougalhanson/.claude/plugins/data/shortcuts-playground-inline/` | Plugin data/config dir (userConfig storage), not reference docs. |

### Skill reference docs (read these, in this order, before authoring)

All at `/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/skills/shortcuts-playground/`:

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

**Bundled ground-truth data files** (`data/` subfolder — these are what the validator and `lookup_action_grounding.py` actually check against, not the prose docs):

| File | Contents |
|---|---|
| `data/toolkit-v63-tool-ids.json` | 1,794 identifiers from the original (pre-OS27) macOS ToolKit snapshot — the closest thing to an "OS 26" baseline allowlist |
| `data/toolkit-v78-tool-ids.json` | 2,731 identifiers from macOS 27 "Golden Gate" build 26A5353q — OS27-only additions |
| `data/toolkit-v78-ios27-tool-ids.json` | 1,206 identifiers from an **iOS 27.0 Simulator** ToolKit v78 database — the only platform-specific iOS snapshot bundled |
| `data/toolkit-v78-first-party-parameter-keys.json` | Parameter-key/type/platform-provenance catalog for `com.apple.*` and `is.workflow.actions.*` rows — **OS27-only; each entry lists which platform(s) it was observed on** |
| `data/toolkit-v78-first-party-enum-cases.json` | Picker enum values for OS27 parameter types |
| `golden-shortcuts/index.jsonl` + `golden-shortcuts/xml/*.xml` | 19 curated real-world shortcut XMLs (pre-OS27 vintage: client versions 700–1300) for wiring patterns |

**Critical gap discovered during this research:** the *only* iOS-specific ToolKit snapshot bundled (`toolkit-v78-ios27-tool-ids.json`) is missing several first-party actions that are unambiguously present on real iPhones (Notes actions: `appendnote`, `filter.notes`, `shownote`, `com.apple.mobilenotes.SharingExtension`). This is almost certainly an artifact of what the iOS 27 Simulator's local ToolKit database happened to expose (e.g. Notes app not fully provisioned in the simulator), not proof those actions don't exist on iOS — they are long-standing, widely-documented default Shortcuts actions. Treat identifier presence in `toolkit-v63` (the generic, non-platform-segmented snapshot) as the operative iOS-availability signal for pre-existing actions, and treat the iOS27-simulator snapshot's *absence* of a row as inconclusive, not disqualifying. This is flagged per-action in the capability table below.

### Agents, commands, hooks

| Component | Path |
|---|---|
| `shortcut-builder` agent | `.../1.2.1/agents/shortcut-builder.md` — owns design→build→validate→sign→archive for new shortcuts |
| `shortcut-remixer` agent | `.../1.2.1/agents/shortcut-remixer.md` — surgical diff on existing unsigned XML; **will refuse to touch a `.shortcut` file** (see §8) |
| `/shortcuts-playground:build` | `.../1.2.1/commands/build.md` |
| `/shortcuts-playground:remix` | `.../1.2.1/commands/remix.md` |
| `PostToolUse` validator hook | `.../1.2.1/hooks/hooks.json` + `hooks/auto-validate.sh` — auto-runs the Craig Loop validator on every Write/Edit that touches a Shortcuts plist |
| `shortcuts-playground-selftest` | `.../1.2.1/bin/shortcuts-playground-selftest` — 6-check health test (Python version, `shortcuts` CLI, plugin-root resolution, bundled data, validator-on-golden, full archive+sign round trip) |

### Exact validator invocation

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/shortcuts-playground/scripts/validate_shortcut.py" <file.xml|file.shortcut> \
  --target-macos 26 --target-platform ios
```
or via the PATH wrapper (identical, resolves `${CLAUDE_PLUGIN_ROOT}` and checks Python ≥3.10 first):
```bash
validate-shortcut /path/to/PROSOCHE.xml --target-macos 26 --target-platform ios
```

**Recommended target flags for this project: `--target-macos 26 --target-platform ios`** (or `SHORTCUTS_PLAYGROUND_TARGET_MACOS=26` / `SHORTCUTS_PLAYGROUND_TARGET_PLATFORM=ios`). Rationale:
- The plugin's default (`auto`/`macos`) targets whatever macOS the *build machine* runs and the macOS action surface — wrong for an iPhone-only shortcut.
- `--target-macos 26` (not `27`/`latest`) matters because the v78-first-party-parameter-keys catalog — which gates several Notes/Screen-Time/system-control actions to specific platforms — is **only loaded when targeting macOS/iOS 27+**. At target 26, those actions validate purely by identifier presence in the generic `toolkit-v63` allowlist, which is the more permissive and more accurate posture for an iOS 26 shortcut using long-standing actions. Do not use `--target-macos 27` for this project unless deliberately opting into an OS27-only action (there should be none — PROSOCHĒ must run on "iOS 26.x").
- `--target-platform ios` is required to allow the handful of iOS-only rows (e.g. `com.apple.HearingApp.MuteVolumeIntent`-style Settings intents) and to avoid false negatives from macOS-only rows leaking in as "available."

### Exact signing invocation

```bash
sign-shortcut /path/to/PROSOCHE.xml --name "PROSOCHĒ — Nine Circles — Dumb" \
  [--mode anyone|people-who-know-me] [--output-dir DIR]
```
Defaults: `--mode` from `$CLAUDE_PLUGIN_OPTION_SIGNING_MODE`, else `anyone` (use `anyone` for a free/open-source shortcut, per PROJECT.md distribution intent). `--output-dir` from `$CLAUDE_PLUGIN_OPTION_OUTPUT_DIR`, else `~/Documents/Shortcuts Playground`.

Underlying pipeline (what `sign-shortcut` wraps, verbatim from `bin/sign-shortcut`):
1. Copies the unsigned XML to `$OUTPUT_DIR/$(date +%F)/<name>-<HHMMSS>.xml` (the required raw-XML archive).
2. Copies it to a temp `.shortcut` path and runs `shortcuts sign --mode <mode> --input <tmp> --output <tmp2>`.
3. On failure with `plutil -lint` passing, retries once after `plutil -convert binary1` (a known Golden-Gate-era signer quirk).
4. Moves the signed result to `$OUTPUT_DIR/<name>.shortcut` (canonical name, **no `_signed` suffix** — a `_signed` filename is treated as a failed build).
5. Prints `{"archive":"...","signed":"...","mode":"..."}`.

`shortcuts sign` is the real signer (macOS-only, part of the `shortcuts` CLI). The CLI supports only `run`, `list`, `view`, `sign` — **no `import` or `delete` subcommand**. Duplicate shortcut names in the user's library cause silent no-op skips on import; PROSOCHĒ's build notes must tell testers to delete a prior version before re-importing.

### Definition of done (per the plugin's own rule)

A build is **not** complete when the plist validates. It's complete only after `sign-shortcut` has produced a non-zero-byte signed `.shortcut` file, verified to exist. "Valid XML, not yet signed" is not a stopping point — apply this to both PROSOCHĒ Dumb and Sentient.

---

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

**It doesn't, at the plist level.** There is no `WFWorkflowTypes` entry or root key that says "iOS only." Platform availability is entirely a property of *which action identifiers and parameter keys you use* — the OS decides at import/run time whether it recognizes them. `WFWorkflowTypes` governs *surfaces* (Watch complication, action extension, NC widget), not OS platform. This means:
- The Shortcuts **Playground validator's** `--target-platform` flag is a build-time simulation of what the real device will accept — it is Playground tooling, not a plist feature.
- The actual portability risk is per-action: an action identifier or parameter key gated to "macOS 27" in the bundled catalog (see the Color Filters and Notes findings below) may simply not exist as an option when authoring/running on iPhone.
- **Practical rule for this project:** validate with `--target-platform ios` and manually import-test on a real iPhone (Shortcuts Playground cannot execute or verify runtime behavior — its validator only checks structural/plist correctness, per `TOOLKIT_SNAPSHOT.md`).

---

## 3. Capability audit — verified action identifiers

Legend: **VERIFIED** = identifier and/or parameter shape found in the Playground's bundled ToolKit snapshot/reference docs, with the evidence stated. **VERIFIED (macOS-catalog only)** = identifier exists in Playground data but the only parameter-schema evidence found is tagged "macOS 27" — treat the *identifier* as safe to try, the *parameter shape* as needing on-device confirmation. **UNVERIFIED** = identifier exists but no parameter schema documented anywhere in the bundle; safest-fallback required per the plugin's own escalation rule. **NOT AVAILABLE** = no matching action found; a different mechanism is required.

| # | Capability | Verdict | Identifier / evidence | Notes for the build agent |
|---|---|---|---|---|
| 1 | Get Current App / current-app detection from an automation | **VERIFIED** | Two mechanisms: (a) standalone action `is.workflow.actions.getcurrentapp` (`WFGetCurrentAppAction`), present in `toolkit-v63` and the iOS27-simulator snapshot; (b) magic-variable `Type: "CurrentApp"` usable inline in any `WFTextTokenAttachment`, documented in `PARAMETER_TYPES.md` §"Current App" with `WFPropertyVariableAggrandizement` for name/bundle-ID | Use the magic-variable form to avoid an extra action; both return app metadata (aggrandize `Name`/`Bundle Identifier`). **Caveat (from canonical strategy §5.1, independently confirmed by domain knowledge, not by this plugin):** Personal Automations pass the triggering app's identity to the automation, not necessarily reliably re-derivable via Get Current App inside the invoked shortcut in every trigger context — the build agent must test this on-device for the OPEN automation specifically and fall back to trusting the automation's own app filter (i.e., "if this shortcut was invoked by the OPEN automation at all, the app IS the configured target") rather than depending on Get Current App as the source of truth. |
| 2 | Get File, Save File (with overwrite), file-existence checks in Shortcuts iCloud folder | **PARTIAL — VERIFIED for Get/Save, NOT AVAILABLE for existence check** | `is.workflow.actions.documentpicker.open` (`WFGetFileAction`/`WFSelectFilesAction`), `is.workflow.actions.documentpicker.save` (`WFSaveFileAction`); both in `toolkit-v63`. `BEST_PRACTICES.md` recommends `is.workflow.actions.file.select` for user-driven picking and Save File for writing, chained via **Set Name** (`is.workflow.actions.setitemname`, outputs "Renamed Item") when a specific filename/overwrite target is needed. | **No native "does file exist" boolean action or property is documented anywhere in the bundle** (searched `ACTIONS.md`, `FILTERS.md`, `PARAMETER_TYPES.md`, `APPINTENTS.md` — no `WFGetFileExists`, no filter predicate for existence). This is a known, real Shortcuts limitation, not a plugin gap. **Fallback (record as a deviation):** attempt **Get File** at the fixed `state.json` path; a missing file surfaces as a runtime error dialog in Shortcuts, which cannot be silently caught (Shortcuts has no try/catch). PROSOCHĒ's bootstrap must therefore not rely on a "check exists, then read" pattern — instead: always attempt **Get File**, treat any non-dictionary/empty result from the subsequent **Detect Dictionary** step as "state absent," and drive bootstrap off *that*. Save File's `WFSaveFileOverwrite`/ask-where-to-save behavior is likewise **UNVERIFIED** in this bundle — no schema found — confirm empirically and fall back to always using **Save File** with an explicit fixed path + explicit "replace existing" toggle if the Craig Loop / on-device import shows it's needed. |
| 3 | Dictionary creation, Get/Set Dictionary Value, JSON text ↔ dictionary conversion | **VERIFIED** | Create: `is.workflow.actions.dictionary` (`WFDictionaryAction`, `WFItems`/`WFDictionaryFieldValueItems`, documented in `PLIST_FORMAT.md`/`PARAMETER_TYPES.md` §"Dictionary Field Value"). Get: `is.workflow.actions.getvalueforkey` (in `toolkit-v63` complete list), key param `WFDictionaryKey` with **1-based dot notation** for nested access (`SKILL.md` rule 16, e.g. `results.tracks.items`). Set: `is.workflow.actions.setvalueforkey` (in `toolkit-v63`), requires `WFDictionary` wired explicitly (`BEST_PRACTICES.md`: "always connect the target dictionary via `WFDictionary`; do not rely on implicit input"). JSON text → dictionary: `is.workflow.actions.detect.dictionary` ("Detect Dictionary"), used in 3+ golden examples (`1be4dde9...xml`, `6a18b768...xml`, `ae59e10d...xml`) for parsing API/JSON responses. | Dictionary → JSON text direction: use a **Get Dictionary Value** on the whole dict wired into a **Text**/**JSON Text** action, or the dict's own text coercion — not separately documented as a distinct action; `state.json` writes should build the JSON body as a **Text** action template (per `BEST_PRACTICES.md` rule for "complex JSON fallback": use JSON Text + `WFRequestVariable`-style templating) rather than assuming a magic "Dictionary → JSON string" action exists as its own identifier. Known gotcha: comparing a **Dictionary Value** (text) directly in an **If** often renders blank — pass it through a **Text** action first, then compare the Text variable (`BEST_PRACTICES.md` §Lists & Dictionaries). |
| 4 | Date arithmetic (Adjust Date, Format Date, date difference in seconds) | **VERIFIED** | Adjust: `is.workflow.actions.adjustdate` (`WFDate` + non-empty `WFDuration` as `WFQuantityFieldValue{Magnitude,Unit}`, `WFAdjustOperation` for explicit Add/Subtract — `SKILL.md` rule 36, `BEST_PRACTICES.md`). Format: `is.workflow.actions.format.date` (`WFDate`, `WFDateFormatStyle`, custom pattern in `WFDateFormatString`, full UTS#35 pattern-character table in `DATE_TIME.md`). Difference: `is.workflow.actions.gettimebetweendates` (`WFTimeUntilAction`), `WFInput` + exactly one of `WFDate`/`WFTimeUntilCustomDate`/`WFTimeUntilFromDate`, `WFTimeUntilUnit` for the output unit (documented seconds/minutes/etc. via `WFQuantityFieldValue` unit table in `VARIABLES.md`) | For the "behavioural day = date − 4h" and Heat decay math, chain: **Date** (Current Date) → **Adjust Date** (subtract 4 hr / seconds since last interaction) → **Format Date** (custom `yyyy-MM-dd` for the day key) → **Get Time Between Dates** with `WFTimeUntilUnit = sec` for elapsed-seconds math feeding Heat decay. Never put a `CurrentDate` magic token directly into `WFTimeUntilFromDate`/`WFDate` fields expecting "now" — first materialize it via a **Date** action set to Current Date, then reference *that action's output* (`ACTIONS.md` §Get Time Between Dates, `BEST_PRACTICES.md`). |
| 5 | Notes: Create Note, Append to Note, Find Notes / Show Note | **VERIFIED (macOS-catalog only) — cross-checked, standard iOS actions** | Create Note: `com.apple.mobilenotes.SharingExtension` (params: `name`, `contents` [AttributedString], `folder`, `interpretAsMarkdown`, `OpenWhenRun`). Append: `is.workflow.actions.appendnote` (params: `operation` [append/prepend], `entity`, `text`, `section`, `ignoreWhitespace`, `interpretAsMarkdown`). Find: `is.workflow.actions.filter.notes` (`WFContentItemFilter` as `WFContentPredicateTableTemplate`; name filter uses `Values.String`/`WFTextTokenString`, folder filter uses `Values.Enumeration`/`WFLinkDynamicOptionSubstitutableState` — `BEST_PRACTICES.md` §Text & Parsing). Show/Open: `is.workflow.actions.shownote` (param: `target`). All four identifiers are present in `toolkit-v63` (the generic, non-platform-restricted snapshot). | **Flag:** the v78 first-party parameter catalog tags all four of these entries `"platforms": ["macOS 27"]` only — they are absent from the bundled iOS-27-Simulator snapshot entirely. Per the gap discussed in §1, treat this as a bundled-data completeness gap, not evidence these are macOS-exclusive: Notes actions (Create/Append/Find/Show) have been standard first-party iOS Shortcuts actions for years and are core to the canonical strategy's Control-Room-Note design; they are extremely unlikely to be genuinely unavailable on iPhone. **Still: verify all four empirically on a real iPhone during the first Dumb build** and record the outcome in build notes — this is the single most consequential "trust but verify" item in this audit because the entire Control Room design depends on it. `WFUrgent`/`interpretAsMarkdown` booleans, if used, are OS27-parameter-gated per `ACTIONS.md` — do not set them when validating at `--target-macos 26`. |
| 6 | Ask for Input (text and number), Choose from Menu, Choose from List | **VERIFIED** | Ask: `is.workflow.actions.ask` (`WFAskForInputAction`), `WFAskActionPrompt`, `WFInputType` ∈ `Text`/`Number`/`URL`/`Date`/`Date and Time` (`PARAMETER_TYPES.md` §WFInputType). Full working example in `EXAMPLES.md` Example 2. Choose from Menu: `is.workflow.actions.choosefrommenu`, control-flow modes 0/1/2, `WFMenuPrompt`, `WFMenuItems` array, one mode-1 case per item with matching `WFMenuItemTitle` in identical order (`CONTROL_FLOW.md`, exhaustively documented, "verified from 127 real shortcuts analysis"). Choose from List: `is.workflow.actions.choosefromlist` (in `toolkit-v63` list) | For PROSOCHĒ's Control Room manual menu (Status/Open Control Room/Sync Profile/... ) and Consult's 6-item picker, Choose from Menu is the right primitive — its wiring is the most rigorously documented control-flow pattern in the whole skill (menu-item-title matching is a hard requirement, order-sensitive). |
| 7 | Open App, Open URL, web search, Maps search deep link | **VERIFIED** | Open App: `is.workflow.actions.openapp` (`WFAppIdentifier`, optional OS27 `WFWindowingFormat` — skip on iOS26 target). Open URL: `is.workflow.actions.openurl` (`WFInput`). Web search: `is.workflow.actions.searchweb` (`WFSearchWebAction`, in `toolkit-v63`). Maps: `is.workflow.actions.searchmaps` (`WFSearchMapsAction`) and `is.workflow.actions.getmapslink` (deep-link generator), both in `toolkit-v63`; also `is.workflow.actions.getdirections`/`getdistance` for route-shaped Maps actions. | Consult's "route feed-shaped seeking to query-shaped seeking" (canonical strategy §8.5) maps directly: Ask for Input → If/Menu classify → Search Web (`searchweb`) or Search Maps (`searchmaps`) or Open URL to `https://www.google.com/search?q=` as the reliable generic web-search fallback if `searchweb`'s exact behavior (which search provider/app it opens) proves unsuitable on-device. |
| 8 | Set Brightness, get current brightness | **VERIFIED (Set) / UNVERIFIED-in-Playground (Get)** | Set: `is.workflow.actions.setbrightness` (also exposed as Siri intent `com_apple_shortcuts_set_brightness`), param `WFBrightness` (float), present in **both** `["iOS 27 Simulator","macOS 27"]` per the v78 parameter catalog — this is the one system-control action in the whole audit with confirmed iOS *and* macOS provenance. Get: **no native "get current brightness" action or property is documented anywhere in the Playground bundle** — not in `ACTIONS.md`'s Get Device Details entry, not in `PARAMETER_TYPES.md`. External corroboration (Apple's own "What's New in Shortcuts" release notes, via web search, not part of the Playground bundle): Apple states **Get Device Details** ("now rounds numbers, including the current battery level, volume, and brightness") does expose a brightness reading — but the exact `WFDeviceDetailsProperty` string is not documented in this plugin's reference files, so it counts as UNVERIFIED against the ground-truth source this research prioritizes. | For Circle "Dimming," Set Brightness (`WFBrightness`) is safe to use directly (never `0`, prototype value ~10–15% per canonical strategy §21). For *reading* the pre-dim brightness to restore it later, try **Get Device Details** with a property named `Brightness` (candidate value from external Apple docs) during the Craig Loop and confirm on import; if it cannot be confirmed working, the safest fallback per canonical strategy §21 is: **do not perform a stateful brightness change unless the original value can be reliably captured and restored** — i.e., skip the Dimming primitive's brightness manipulation and substitute a different passive-friction primitive, recording the deviation in build notes. |
| 9 | Set Volume, get current volume | **VERIFIED (Set) / UNVERIFIED-in-Playground (Get)** | Set: `is.workflow.actions.setvolume` (`WFSetVolumeAction`), in `toolkit-v63`, also `com.nick.Clic.SetVolumeIntent` (third-party, irrelevant). No parameter schema for `setvolume` was found in the v78 catalog (it's a legacy `is.workflow.actions.*` action so the OS27 schema-gating catalog doesn't cover it — per `TOOLKIT_SNAPSHOT.md`, "it does not apply broad unknown-key checks to regular `is.workflow.actions.*` actions"), so treat the conventional `WFVolume`-style float parameter as the working assumption pending on-device confirmation. Get: same situation as brightness — only external (non-Playground) evidence via Get Device Details' "current volume" property, exact key name unconfirmed. | Same guidance pattern as Brightness: use Set Volume for the "Silence" primitive only if the pre-change volume can be captured and restored (canonical strategy §21 hard requirement); if Get Device Details' volume property can't be confirmed working during the Craig Loop / on-device test, skip stateful volume manipulation for the prototype and record the deviation. |
| 10 | Set Color Filters / grayscale toggle, and whether current state can be READ back | **NOT AVAILABLE on iOS** | The only "Set Color Filters" action found anywhere in the bundle is `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` (params `operation`, `state` [bool On/Off], `ShowWhenRun`). Its v78 parameter-catalog entry is tagged **`"platforms": ["macOS 27"]` only**, and — critically, unlike the Notes case above — it is **absent from the bundled iOS-27-Simulator ToolKit snapshot entirely** (confirmed by direct lookup: `False`). The only accessibility-adjacent entries present in the iOS snapshot are `com.apple.Bridge.AccessibilityDeepLinks`/`OpenAccessibilityDeepLinks` — deep-link *openers* to Settings, not togglers. No grayscale action exists anywhere in the 365-identifier `ACTIONS.md` list either (`colorfilter`/`grayscale` do not appear as `is.workflow.actions.*` identifiers). There is **no read-back mechanism** for any of this, consistent with there being no set action to read back from. | This is a genuine, well-known iOS Shortcuts limitation (Color Filters/grayscale has never been exposed to Shortcuts.app on iPhone, unlike macOS's Universal Access AppIntents) — the Playground's own bundled data corroborates it rather than merely failing to document it. **Fallback for Circle "Ash":** cannot be implemented as a programmatic grayscale toggle. Options to record in build notes: (a) drop Ash as a distinct primitive and substitute Dimming/Silence/Knock earlier in the sequence, (b) deep-link the user to Settings → Accessibility via `com.apple.Bridge.OpenAccessibilityDeepLinks` as a *manual* one-tap suggestion (not an automatic toggle — breaks the "no permission prompt" design goal for Exile-class primitives), or (c) treat Ash as aspirational/Phase-E scope pending a future non-Shortcuts mechanism. Given canonical strategy §21's absolute rule ("if Shortcuts cannot detect and restore the original condition safely, skip dynamic grayscale"), **option (a) is the recommended default** for the prototype. |
| 11 | Speak Text | **VERIFIED** | `is.workflow.actions.speaktext` (`WFSpeakTextAction`), present in `toolkit-v63`'s complete identifier list | Straightforward; wire the Mirror/Voice message text as `WFTextTokenString` (display parameter rule from `VARIABLES.md`) into whatever the action's text-input key turns out to be (commonly `WFText`/`WFSpeakTextText` in real-world Shortcuts — not spelled out in this plugin's docs beyond identifier presence, so confirm the exact key via Craig Loop). |
| 12 | Lock Screen | **VERIFIED** | `is.workflow.actions.lockscreen` (`WFLockScreenAction` in class-mapping terms), **zero parameters**, and — unlike Color Filters — explicitly present in **both** `["iOS 27 Simulator","macOS 27"]` per the v78 catalog. (There is also `is.workflow.actions.lock.app` — "Lock App," a *different* action that locks a specific app via `WFLockAppOperation`/`WFApp`, and `com.apple.controlcenter.LockScreenIntent`, a macOS-27-only Control Center intent — do not confuse these three.) | Circle IX (Ice) can use `is.workflow.actions.lockscreen` directly as the strongest safe ejection primitive the canonical strategy anticipates (§11, §22) — this is one of the most solidly verified actions in the whole audit (no params, confirmed cross-platform). |
| 13 | Run Shortcut (shortcut-to-shortcut invocation and passing input) | **VERIFIED identifier / UNVERIFIED exact parameter keys in this bundle** | `is.workflow.actions.runworkflow` (`WFRunWorkflowAction`), present in `toolkit-v63`. Also documented as an AppIntent surface: `com.apple.shortcuts.RunShortcutIntent` ("Run Shortcut") and `com.apple.shortcuts.RunShortcutFromCollectionIntent` in `APPINTENTS.md`. **No parameter schema (`WFWorkflowName`/`WFInput`/output-handling keys) for `runworkflow` is spelled out anywhere in `ACTIONS.md`'s per-action detail sections** — it only appears in identifier lists. | PROSOCHĒ's design (per PROJECT.md) is a **single master shortcut with OPEN/CLOSE routing via Shortcut Input text**, not shortcut-to-shortcut invocation between Dumb/Sentient/etc. — so `runworkflow` is not on this project's critical path; it's audited here only because the strategy's capability list requested it. If it becomes needed later (e.g. Control Room menu items dispatching to helper shortcuts), confirm the conventional `WFWorkflowName` (target shortcut name, string) + `WFInput` (input to pass) shape empirically via the Craig Loop before relying on it. |
| 14 | Wait / Wait to Return | **VERIFIED identifiers / parameter keys not detailed** | `is.workflow.actions.delay` (`WFDelayAction`, "Wait") and `is.workflow.actions.waittoreturn` (`WFWaitToReturnAction`), both in `toolkit-v63`. Neither has a dedicated parameter section in `ACTIONS.md`; the conventional `WFWaitActionWaitTime` for Delay is not named in this bundle. | Needed for CLOSE handler's "brief wait if needed for app-switch race handling" (canonical strategy §20 step 4). Confirm the exact wait-duration key via Craig Loop/on-device import before finalizing; `WFQuantityFieldValue` (`Magnitude`+`Unit`, units `sec`/`min`/... per `VARIABLES.md`) is the general pattern this plugin uses for other duration parameters and is the best-effort guess if the field name can't be confirmed from `ACTIONS.md` alone. |
| 15 | `Use Model` (iOS 26 Apple Intelligence) — model-source selection, on-device pinning, structured/JSON output, consumption by later actions | **VERIFIED identifier and most parameters / UNVERIFIED model-source enum strings — do not guess** | `is.workflow.actions.askllm` (`WFAskLLMAction`, "Use AI Model"), full v78 parameter schema confirmed present on **both** `["iOS 27 Simulator","macOS 27"]`: `WFLLMPrompt` (str, the request text), `WFLLMModel` (typed enum `com_apple_shortcuts_wfask_llmmodel_parameter` — **no enum-case list found anywhere in the bundled `toolkit-v78-first-party-enum-cases.json`**; the only observed literal value across every example in `EXAMPLES.md`/`VARIABLES.md` is the string `"Apple Intelligence"`, which pre-dates the OS26 three-way model picker described by external sources), `WFAllowWebSearch` (bool, "Use Broad World Knowledge," OS27-gated — omit at target macOS 26), `FollowUp` (bool, OS27-gated — omit), `WFGenerativeResultType` (str, "Output" — observed literal value `"Text"` in every example; no evidence of a documented JSON/structured-output literal value in this bundle, though `WFGenerativeResultType` is clearly the intended structured-output switch). **External corroboration (web search, not part of Playground bundle, MEDIUM confidence):** Apple's own iOS 26 documentation and MacStories reporting confirm the Use Model action's UI picker offers exactly three sources — **On-Device**, **Private Cloud Compute**, and **Extension Model (ChatGPT/GPT-5)** — and that the action supports structured/deterministic output despite LLM non-determinism, and that inputs can include variables/outputs from previous actions. **Neither source gives the exact plist string Playground/Apple use for the On-Device enum case** (`"On-Device"`? `"On Device"`? an integer code?). | **This is the single most important UNVERIFIED item for the Sentient fork and must not be guessed.** PROJECT.md's hard constraint is "never claim to know" + "if it cannot be verified, use the safest fallback, record the deviation, keep the Shortcut runnable" — apply that literally here: (1) build the `Use Model` action with `WFLLMPrompt` + `WFGenerativeResultType="Text"` first and get it signing/importing; (2) on a real Apple-Intelligence-capable iPhone, open the imported action in Shortcuts.app, manually select **On-Device** in the Model picker, save, then **export the shortcut as unsigned XML** (Share → Copy → paste to `.xml`) and read back the resulting `WFLLMModel` literal — this is the only reliable way to obtain the true enum string, consistent with the plugin's own "paste a working example for me to mirror" escalation path (`shortcut-builder.md` line 118-120); (3) hardcode that confirmed literal into the Sentient build and record it in build notes as a verified-on-device fact, not a Playground-bundle fact. Until that round-trip is done, treat On-Device pinning as **unconfirmed** and gate all `Use Model` calls behind the `ai_enabled`/on-device-capability check the canonical strategy already requires, with a deterministic fallback path (§14.2–14.5) that never depends on the model literal being right. |
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

---

## 4. Control-flow primitives

Source: `CONTROL_FLOW.md` (777 lines, the most rigorously evidenced doc in the bundle — repeatedly cites "verified against an Apple-built sample shortcut" and "127 real shortcuts analysis").

- **If / Otherwise / End If**: all three are the *same* identifier, `is.workflow.actions.conditional`, distinguished only by `WFControlFlowMode` (`0`=If, `1`=Otherwise/Otherwise-If, `2`=End If) sharing one `GroupingIdentifier` per block. **Every** condition code (including 0–3, which older docs wrongly called "implicit input") requires an explicit `WFInput` wrapped as `{Type:"Variable", Variable:{...}}` — this was re-verified against an Apple-built sample and is a hard rule, not a style preference. Full condition-code table (0=less than, 1=≤, 2=greater than, 3=≥, 4=string is, 5=string is not, 8=begins with, 9=ends with, 99=contains, 100=has any value, 101=does not have any value, 999=does not contain, 1003=is between) is in both `CONTROL_FLOW.md` and `BEST_PRACTICES.md`, byte-for-byte consistent. **Common bug the docs specifically warn about:** code `0` is "is less than," not "equals" — there is no numeric-equals code; use string code `4` on text-coerced numbers or an Any-of-two (≥N AND ≤N) block instead.
- **Repeat (count)** and **Repeat with Each**: same two-endpoint (`0`/`2`) `GroupingIdentifier` pattern. Inside the loop, reference `Repeat Index`/`Repeat Item` as **named `Type: Variable`**, never as `ActionOutput` pointing at the end action's UUID — using `ActionOutput` is the single most emphasized "will silently fail at runtime, showing as Repeat Results in the UI" mistake across the whole doc set.
- **Choose from Menu**: mode 0 (menu def, `WFMenuItems` array) → N mode-1 cases (`WFMenuItemTitle`, exact string + exact order match to `WFMenuItems`) → mode 2 (end). Menu title mismatches or out-of-order cases are called out as the top real-world failure mode ("Important Notes from 127 real shortcuts analysis").
- **Nesting**: confirmed working to **depth 7** in a real production shortcut (`AppRedirect.xml`, cited in the corpus analysis). Every nesting level needs its own unique `GroupingIdentifier` — this is the exact "GroupingIdentifier/UUID wiring" warning PROJECT.md and the canonical strategy both flag as something the agent must inspect manually, and it is well-founded: it's the #1 documented "common mistake."
- **Multi-condition If** (Any/All): a *separate* serialization (`WFConditions` + `WFContentPredicateTableTemplate`, `WFActionParameterFilterPrefix` 0=Any/1=All) that must **not** be mixed with the single-condition `WFCondition`/`WFInput` pattern on the same action — the validator hard-rejects mixing them.
- **Otherwise If** (used as "middle" branch with its own condition) is not a new identifier — it's mode 1 *with* condition fields present, vs. plain Otherwise which is mode 1 with none.

**For PROSOCHĒ specifically:** the OPEN/CLOSE router (dispatch on Shortcut Input text), the nine-Circle dispatcher, the three-profile/three-sequence selection, and the six-exit Choose from Menu will all stack multiple control-flow blocks at meaningful nesting depth (Circle dispatch nested inside profile-branch nested inside OPEN/CLOSE routing). Depth-7 evidence says this is within Shortcuts' proven envelope, but every single block needs a *freshly generated, never-reused* `GroupingIdentifier` — this is exactly the kind of wiring the canonical strategy (§31) says must be manually inspected, not assumed correct because the plist validated.

---

## 5. Variable wiring

Source: `VARIABLES.md` (explicitly "from XML ground truth analysis of 127 real shortcuts" + runtime verification notes).

- **Named variables** (`Set Variable`/`is.workflow.actions.setvariable`, `WFVariableName` + `WFInput`) vs. **magic variables** (direct `ActionOutput` references via `OutputUUID`+`OutputName`, or special `Type` values `CurrentDate`/`Clipboard`/`Ask`/`ExtensionInput`/`DeviceDetails`/`CurrentApp` with no extra params). PROSOCHĒ's `state.json` fields (heat, gravity, pressure, circle, active_session, etc.) should mostly be named variables set once per OPEN/CLOSE pass and referenced by name, per `BEST_PRACTICES.md`'s "prefer inserting named variables directly into action input fields; avoid redundant Get Variable → next action hops."
- **`WFVariable` / `OutputUUID` / `OutputName` token structure:** every `attachmentsByRange` entry is `{OutputUUID, OutputName, Type: "ActionOutput"}` keyed by a `{position, length}` range into the string; `length` is always `1` (the `` U+FFFC placeholder is exactly one character). The **specific wiring mistake Playground says to inspect manually** is the **Display vs. Non-Display parameter distinction**, called out as "CRITICAL — runtime-verified" and backed by a stat ("all 46 Show Alert and 41 Notification instances across 127 real shortcuts use `WFTextTokenString`"): display-facing text (`WFAlertActionMessage`, `WFAlertActionTitle`, `WFNotificationActionBody`/`Title`, `Text` in Show Result) **must** use `WFTextTokenString` with a `` placeholder even for a single bare variable — using `WFTextTokenAttachment` there imports fine and validates fine but silently shows default/empty text at runtime. Non-display data-flow parameters (`WFInput`, `WFDate`, `WFVariable`, `WFDictionary`) can use the shorter `WFTextTokenAttachment` form.
- Other manually-inspect-worthy wiring bugs the docs name explicitly: `attachmentsByRange` positions must exactly match `` character offsets in the *final* string (a single later text edit invalidates all downstream offsets — "recompute positions if the surrounding text changes"); out-of-bounds ranges "can crash Shortcuts on import"; Repeat Index/Item must be `Type: Variable` not `ActionOutput` (repeated from §4 because it recurs as a top mistake in both docs).

---

## 6. Practical size/complexity limits

**No documented hard action-count ceiling exists** — confirmed independently by (a) `PROSOCHE_Nine_Circles_Canonical_Strategy.md` §5.3 itself ("Apple's documentation tells users to add as many actions as needed... No useful documented hard maximum... has been identified"), and (b) nothing in `SKILL.md`, `BEST_PRACTICES.md`, or the `shortcut-builder` agent's own escalation rules mentions a size limit — its only hard stop conditions are validator-iteration-count (max 5 Craig Loop fixes) and undocumented-parameter-schema escalation.

What the Playground documentation actually flags as breaking at scale, consistent with the canonical strategy's own risk list:
- **Runtime complexity / variable wiring correctness** — not size per se, but the *density* of wiring mistakes scales with action count; this is why the Craig Loop, the comment-density rule ("8+ actions require ≥3 comments, 16+ require ≥4, 24+ require ≥5"), and the mandatory pre-control-flow-block comment convention exist.
- **`GroupingIdentifier` collisions at depth** — the more nested control flow, the more places a copy-paste or reuse error can silently corrupt a block boundary (§4).
- **Comment-block bloat vs. readability** — `BEST_PRACTICES.md` recommends section-header Comments (`--- FETCH TASKS ---` style) for any shortcut over ~20 actions, which PROSOCHĒ (a large stateful single-shortcut design spanning bootstrap, OPEN, CLOSE, nine Circles, six exits, Control Room menu) will need extensively.
- **Model latency** (Sentient only) — canonical strategy's own §14.5 concern (don't force inference onto every early-Circle OPEN); not a Playground finding, a product-design one.
- **Notes parsing cost at scale** — again a canonical-strategy concern (§5.4), not a Playground one, and already correctly designed around (JSON hot path, Note as append-only ledger).

**Net assessment:** nothing in the ground-truth toolchain suggests PROSOCHĒ's scope (large, single, deeply-nested, stateful shortcut) is structurally infeasible. The real risk the Playground's own docs corroborate is **wiring-correctness at scale**, which is why its validator explicitly says "generated shortcuts get ~90% of the way" and mandates manual inspection of variable wiring and repeat loops — directly matching the caution already baked into PROJECT.md and the canonical strategy.

---

## 7. Import questions (`WFWorkflowImportQuestions`)

**Not documented in prose anywhere in the skill docs** (`PLIST_FORMAT.md` only lists the key as "Array, No, Import-time questions" with no sub-schema; the quick-start/EXAMPLES templates all use an empty array). The real schema was recovered by inspecting populated instances inside the bundled **golden-shortcuts XML corpus** (ground truth, not prose):

```json
{
  "ActionIndex": 2,
  "Category": "Parameter",
  "DefaultValue": "",
  "ParameterKey": "WFTextActionText",
  "Text": "Enter your Mastodon app access token. ..."
}
```
(4 real examples found across the 19 golden XMLs, targeting `WFTextActionText` on a Text action, `WFNumberActionNumber` on a Number action, and `WFURLActionURL` on a URL action.)

**Supported types (inferred from evidence, not asserted from a spec):** import questions bind to a **specific action's specific literal parameter field** by `ActionIndex` (position in `WFWorkflowActions`) + `ParameterKey` (the plist key inside that action, e.g. `WFTextActionText`/`WFNumberActionNumber`/`WFURLActionURL`), with `DefaultValue` pre-filling the field and `Text` as the import-time prompt shown to the user. This means import questions can only ask the user to fill in a **literal value on a Text/Number/URL-style action** — they cannot directly drive a Choose-from-Menu selection or set a boolean toggle by observed evidence in this corpus.

**Limits discovered:**
- **The validator does not check `WFWorkflowImportQuestions` at all** — `scripts/validate_shortcut.py` has zero references to the key. Correctness here is entirely the build agent's responsibility; a malformed import question will not be caught by the Craig Loop.
- Because each question targets one literal parameter field, PROJECT.md's Layer-A import questions ("Choose your descent: Paradise/Limbo/Inferno," "Use on-device intelligence? yes/no," "May PROSOCHĒ speak? yes/no") must each be implemented as: a **Text** action holding the literal default (e.g. `WFTextActionText = "Limbo"`) targeted by one import question with `Text` = the prompt, whose output is then read at bootstrap-time and mapped/validated (e.g. an If-chain matching the text against `Paradise`/`Limbo`/`Inferno`) rather than as a native yes/no or single-select import-time control. This is consistent with the canonical strategy's own instruction (§7.1) to "use `WFWorkflowImportQuestions` only for simple, robust parameters" — the plist evidence shows exactly why: it's a literal-text-prefill mechanism, not a rich form-builder.

---

## 8. Signing and the AEA1 constraint

- **What produces an importable `.shortcut`:** only `shortcuts sign --mode <anyone|people-who-know-me> --input <unsigned.shortcut-or-xml> --output <signed.shortcut>` (the real macOS `shortcuts` CLI, wrapped by `sign-shortcut`). Signing adds roughly 19KB and is what makes Shortcuts.app agree to import the file at all — an unsigned XML/`.shortcut` cannot be imported on-device.
- **AEA1 constraint on round-tripping:** a signed `.shortcut` is an **Apple Encrypted Archive** (magic bytes `AEA1`). It **cannot be read back as a plaintext plist** by `plutil`, `xxd`, `file`, or any other inspector — confirmed repeatedly across `README.md`, `CHANGELOG.md`, and both agent definitions, and enforced defensively by `shortcuts-playground-selftest` (which checks for `AEA1` magic bytes as proof of a successful sign). Practically: **`shortcut-remixer` refuses to operate on a `.shortcut` file** — it explicitly checks the file extension and the first 4 bytes, and if either matches signed/`AEA1`, it escalates asking the user to re-export as unsigned XML (Shortcuts.app → Share → Copy → paste into a `.xml` file) rather than attempting to parse it.
- **Consequence for PROJECT.md's "retain unsigned XML source" requirement:** the unsigned draft XML the build agent writes (before `sign-shortcut` runs) *is* the canonical, forkable, open-source, inspectable source artifact — this maps exactly to PROJECT.md's requirement ("Unsigned XML source retained for both forks... open-source, inspectable, forkable"). There is no way to regenerate that XML from the signed `.shortcut` other than the manual on-device Share→Copy export path; the repository must keep the pre-sign `.xml` alongside the signed `.shortcut`, not attempt to derive one from the other programmatically.
- **Filename discipline:** the signed output filename must equal the intended shortcut display name (no `_signed` suffix) — treating a `_signed`-suffixed library name as a failed build is an explicit rule (`BEST_PRACTICES.md` §Signing & Install Naming). For the two-fork deliverable, this means the two signed artifacts should literally be named `PROSOCHĒ — Nine Circles — Dumb.shortcut` and `PROSOCHĒ — Nine Circles — Sentient.shortcut`.
- **Known signer quirks** (both auto-retried by `sign-shortcut`, but worth knowing): `shortcuts sign` sometimes reports `Error: The file doesn't exist.` for a file that does exist (retry from a clean XML→`.shortcut` copy); sometimes reports `Error: ... isn't in the correct format.` even when `validate-shortcut`/`plutil -lint` both pass (retry after `plutil -convert binary1`). Both retries are built into `sign-shortcut` automatically.

---

## 9. Agent-side tooling and device-evidence channels

Which evidence channel to reach for when a runtime question is open, and which rung is too high or too low for that question. Tooling measured 2026-08-17.

| Tool | How it is reached | Availability |
|---|---|---|
| `/ponytail` | The `anthropic-skills` skill — laziest solution that actually works: YAGNI, standard library and native platform features before dependencies, minimal diffs | Sanctioned. Prefer the minimal change — but laziness never licenses skipping the seven parameter-defect axes under `## Conventions` or the do-not-fabricate protocol in `docs/BUILD-NOTES.md` §2. |
| iOS Simulator | `mcp__Claude_Code_iOS_Simulator__control` (actions `attach`, `launch`, `screenshot`, `tap`, `swipe`, `text`, `button`, `open_url`, `detach`), plus `xcrun simctl` from Bash | Always available on this Mac. |
| iPhone Mirroring | Real-device UAT on the owner's iPhone | Not always live; the user sets it up on request. |

**Measured simulator inventory (2026-08-17).** `xcrun simctl list runtimes` reports exactly one runtime, **iOS 26.5 (26.5 - 23F77)** — inside the project's declared "iOS 26.x" target, so a simulator observation is same-major-version evidence rather than a version extrapolation. `xcrun simctl list devices available` reports iPhone 17 Pro `79A84C29-DB62-40A2-AC3F-CCB5F8192F86` **Booted**, among five iPhones and five iPads. `xcrun simctl listapps 79A84C29-DB62-40A2-AC3F-CCB5F8192F86` reports 25 apps: `com.apple.shortcuts` **present**, `com.apple.mobilenotes` **absent**. Re-run all three to re-derive every simulator claim in this section.

### The evidence-escalation ladder

| Rung | Channel | Settles | Costs |
|---|---|---|---|
| 1 | File-level analysis — validator, ToolKit catalog, golden corpus, decrypted plist | Structure, identifier presence, parameter shape | Nothing |
| 2 | Simulator probe — the agent builds, signs, imports, runs and observes it itself | Import success, runtime variable resolution, control flow, operator/operand type validity, most parameter-key questions | Agent time only |
| 3 | Device probe over iPhone Mirroring — the agent drives the user's iPhone | Everything the simulator cannot | One connected session, requested from the user |
| 4 | User-run probe or donor export on the real device | Anything mirroring cannot reach, or that needs the user's own hands | The user's time — the scarcest input |

**The governing rule: never climb higher than the open question requires, and never skip a rung that would have caught a defect in the probe itself.** Both halves bite. Climbing early spends a scarce device session on something rung 1 or 2 would have settled for free; skipping a rung hands the device a probe that fails for a reason unrelated to the question it was built to answer.

This ladder **extends** the four-item `### Evidence hierarchy` under `## Conventions`, supplying the probe and simulator rungs that list omits. It does not replace it, and the donor's rank there is unchanged.

### Rung 2's ceiling — what a simulator pass may never close

A rung-2 pass may **not** raise a verdict on any of the following. Each is device-gated for a measured reason:

- **The Control Room Note path, in full.** `com.apple.mobilenotes` is absent from the booted simulator's 25 apps, measured above — so every `com.apple.mobilenotes.SharingExtension`, `appendnote`, `filter.notes` and `shownote` behaviour needs rung 3+.
- **Apple Intelligence.** The simulator is not Apple-Intelligence-capable hardware, so the Sentient `Use Model` / On-Device path (CAP-26, BD-04-R2) needs rung 3+.
- **Personal Automation triggers** (App Is Opened / Is Closed). They are user-created on the device and cannot be exercised on a simulator at any effort.
- **Real-hardware environmental behaviour** — brightness and volume capture-and-restore.

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
| Validator target | `--target-macos 26 --target-platform ios` | Correct availability gating for an iOS-26-only shortcut | See §1 rationale |

### Build sequencing recommendation (per project's own stated order)

1. Read `SKILL.md` → `BEST_PRACTICES.md` → `PLIST_FORMAT.md` → `ACTIONS.md`/`APPINTENTS.md` (targeted sections) → `VARIABLES.md`/`CONTROL_FLOW.md`/`FILTERS.md` before drafting.
2. Run `shortcuts-playground-selftest` once to confirm the local toolchain is healthy.
3. Build **Dumb** first (per PROJECT.md and canonical strategy §31): bootstrap, JSON state, Control Room Note, OPEN/CLOSE, Heat/Gravity/Pressure, all nine primitives except any Apple-Intelligence-gated ones, contracts, six exits, explore/exploit, restoration, cooldown, deterministic Mirror.
4. Validate with the Craig Loop (`validate-shortcut ... --target-macos 26 --target-platform ios`), max 5 iterations per pass, fix-and-rerun only after a real edit.
5. Sign with `sign-shortcut ... --name "PROSOCHĒ — Nine Circles — Dumb"`, verify non-zero-byte signed output exists.
6. **Import-test on a real iPhone before forking Sentient** — this is where the UNVERIFIED items in §3 (Notes actions, brightness/volume readback, Wait, Run Shortcut params) get resolved into either confirmed-working or documented-deviation.
7. Fork **Sentient**: add `Use Model`/`askllm`, resolve the On-Device model-literal round-trip (§3 item 15) before wiring any Circle to depend on it, add structured-output parsing + deterministic fallback, never alter the shared deterministic engine.

## Installation

There is nothing to `npm install` — this is not a JS/web stack. The only "installation" step is confirming the plugin and its dependencies are present:

```bash
python3 --version                                     # expect 3.10+
which shortcuts                                       # expect /usr/bin/shortcuts
claude plugin list | grep shortcuts-playground         # expect "shortcuts-playground@shortcuts-playground  Version: 1.2.1  ✔ enabled"
shortcuts-playground-selftest                          # expect "✔ All checks passed."
```

## What NOT to use

| Avoid | Why | Use instead |
|---|---|---|
| Fabricating an action identifier because the canonical strategy asks for it (e.g. inventing a "grayscale toggle" or "get current volume" action) | Both PROJECT.md and the Playground's own agent rules explicitly forbid this; several capability-audit items above have no verified schema | Follow the escalation path: safest fallback + record the deviation, or the on-device round-trip technique used for the Use Model literal (§3 item 15) |
| `WFTextTokenAttachment` on display-facing text fields (`WFAlertActionMessage`, `WFNotificationActionBody`/`Title`, Show Result `Text`) | Runtime-verified to silently render blank/default text even though it validates and imports fine | `WFTextTokenString` with a `` placeholder, even for a single bare variable |
| `ActionOutput` references to Repeat's end-action UUID for `Repeat Index`/`Repeat Item` | Shows up as "Repeat Results" in the UI and fails at runtime | Named `Type: Variable`, `VariableName: "Repeat Index"`/`"Repeat Item"` |
| Reusing a `GroupingIdentifier` across nested or sibling control-flow blocks | Silently corrupts block boundaries — the #1 documented real-world mistake in the corpus analysis | A freshly `uuidgen`'d, uppercase UUID per control-flow block, no exceptions |
| Reading a signed `.shortcut` file with `plutil`/`xxd`/`file`, or asking `shortcut-remixer` to diff one | It's an AEA1 encrypted archive; every plaintext inspector fails on it, and the remix agent will refuse and escalate | Always keep and diff the pre-sign unsigned XML archive |
| Targeting the validator at `--target-macos 27`/`latest` for this project | Loads OS27-only parameter-gating (`WFAllowWebSearch`, `FollowUp`, `interpretAsMarkdown`, etc.) that don't apply to an "iOS 26.x" shortcut and could produce false confidence or false rejections | `--target-macos 26 --target-platform ios` |
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

---
*Stack research for: native iOS 26 Shortcuts adaptive-friction automation (PROSOCHĒ — Nine Circles)*
*Researched: 2026-08-13*
