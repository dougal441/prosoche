# PROSOCHĒ — Build Notes

## 1. Purpose and scope

This document is the durable capability record for the PROSOCHĒ build. Every later phase treats it as ground truth. It is **appended to, never rewritten** — once a row, deviation entry, or action item is recorded, later plans may only add new rows/entries or extend existing sections; they do not delete or silently reword what is already here.

It covers **iOS 26.x native Shortcuts only** (per D-01 — target iOS 26.x, native Shortcuts only, no companion app, no Screen Time blocking APIs, no private APIs).

## 2. Do-not-fabricate protocol

Reproduced as a blockquote so it is directly quotable by every later phase. Sourced from canonical strategy §31 and the standalone "Do not fabricate" protocol block in `.planning/research/PITFALLS.md`. **This protocol is binding (per D-07)** — it governs every capability row in §4 and every action any later phase authors.

> **When an iOS action or parameter the strategy requires cannot be verified in the Shortcuts Playground ToolKit** (identifier not found in `ACTIONS.md`, `APPINTENTS.md`, `THIRD_PARTY_ACTIONS.md`, or the bundled `data/toolkit-v*-tool-ids.json` snapshot for the actual build target):
>
> 1. **Do not invent the identifier or parameter shape.** A plausible-sounding action name is not evidence it exists. Fabricated actions either fail validation outright or — worse — produce a validator false-pass that only breaks at runtime.
> 2. **Use the safest available fallback**, chosen in this priority order:
>    a. A verified, documented alternative action that achieves a strictly weaker but real version of the same intent.
>    b. Skipping the specific behavior entirely, if no safe verified alternative exists — this is explicitly correct, not a failure.
>    c. Never choose a fallback that could strand the user in an unrecoverable state (irreversible settings changes, no exit path, no route out of Ice) purely to preserve a "feature complete" appearance.
> 3. **Record the deviation.** Every unverified action, every fallback taken, and the reasoning must be written into this document (§5, the deviation log) and, where it changes user-visible behavior or a safety guarantee, surfaced in the Control Room Note copy so the user isn't misled about what the Shortcut actually does.
> 4. **Keep the Shortcut runnable.** A missing capability must degrade gracefully — never let an unverified action block the OPEN/CLOSE path, corrupt state, or prevent Circle IX's "always a route out" guarantee. If in doubt, the deterministic, already-verified path always wins over an unverified enhancement.

**A capability recorded as `UNVERIFIED` or `NOT AVAILABLE` is a correct research outcome and does not block a phase; an invented action identifier is a defect.**

This protocol applies with equal force to the Dumb (deterministic actions) and Sentient (`Use Model` integration) forks — the Sentient fork does not get a looser standard for iOS-action verification just because model behavior is separately expected to be non-deterministic.

## 3. Evidence protocol

This section documents the exact reproducible lookup recipe every Evidence cell in §4 must be traceable to, so a later reader can re-derive any verdict without trusting the transcription.

### Plugin root and directories

Plugin root, verbatim: `/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/` — this is the **live** copy (`${CLAUDE_PLUGIN_ROOT}` resolves here at runtime); a second, functionally-identical marketplace mirror exists at `.../marketplaces/shortcuts-playground/claude/` but is not the operative copy.

- Skill docs directory: `skills/shortcuts-playground/`
- ToolKit data directory: `skills/shortcuts-playground/data/`

### The five primary evidence sources

Each is a JSON file under the ToolKit data directory. An Evidence cell must name the file and the internal key path queried.

| File | Internal structure | What it proves |
|---|---|---|
| `toolkit-v63-tool-ids.json` | Object with an `ids` key: a flat array of **1,794** identifier strings | The original (pre-OS27) macOS ToolKit snapshot — the generic, non-platform-segmented baseline; treated as the operative iOS-availability signal for pre-existing, long-standing actions |
| `toolkit-v78-tool-ids.json` | Same shape, `ids` array of **2,731** identifiers | macOS 27 "Golden Gate" additions on top of v63 |
| `toolkit-v78-ios27-tool-ids.json` | Same shape, `ids` array of **1,206** identifiers | The **only platform-specific iOS snapshot bundled** — from an iOS 27.0 Simulator ToolKit v78 database. **Absence of a row here is inconclusive, not disqualifying** — the simulator snapshot does not expose several long-standing first-party actions (e.g. the Notes actions, confirmed present in `toolkit-v63` and standard on iPhone for years) that are unquestionably available on a real device. Treat non-presence here as a signal to weigh alongside the other sources, never as a standalone `NOT AVAILABLE` verdict on its own. |
| `toolkit-v78-first-party-parameter-keys.json` | Object with a `tools` key mapping identifier string → record with `displayName`, `parameterCount`, a `parameters` array of `{key, typePythonName, name, sortOrder, platforms, ...}`, and a top-level `platforms` array | Parameter-key/type/platform-provenance catalog for `com.apple.*` and `is.workflow.actions.*` rows. **OS27-only scoped** — a `macOS 27`-only tag on an entry is a *provenance fact about which build the catalog was captured from*, not proof the action is macOS-exclusive (see the Notes-actions caveat in `.planning/research/STACK.md` §3 row 5, which applies the same reasoning this document applies to CAP-20). |
| `toolkit-v78-first-party-enum-cases.json` | Object with a `types` key mapping a lowercased enum type name → its case list | Where a picker's literal enum values live. A `typePythonName` named in the parameter catalog that has **no matching key here** means the literal cannot be recovered from the local toolchain and must be treated as `UNVERIFIED` for its exact string value even if the parameter's existence is `VERIFIED`. |

### The three secondary sources

- **Prose reference docs** under `skills/shortcuts-playground/`: `SKILL.md`, `BEST_PRACTICES.md`, `ACTIONS.md`, `APPINTENTS.md`, `PLIST_FORMAT.md`, `VARIABLES.md`, `CONTROL_FLOW.md`, `DATE_TIME.md`, `PARAMETER_TYPES.md`, `AUTOMATION_TRIGGERS.md`, `TOOLKIT_SNAPSHOT.md`, `EXAMPLES.md`, `FILTERS.md`, `THIRD_PARTY_ACTIONS.md`, `ICONS_AND_COLORS.md`, `URL_SCHEMES.md`, `JAVASCRIPT_WEBPAGE.md`, `CHANGELOG.md`. Cite by filename and section/rule number.
- **Golden shortcut XMLs** under `skills/shortcuts-playground/golden-shortcuts/xml/` — 19 real-world shortcut plists, real-world ground truth for wiring and literal values not otherwise documented in prose (e.g. the `WFWorkflowImportQuestions` schema, recovered only by inspecting these files). Cite by filename.
- **Clearly-labelled external corroboration** (e.g. Apple's own release notes, third-party reporting) — may be recorded alongside a verdict for context, but may **never on its own raise a verdict above `UNVERIFIED`**.

### Binding citation rule

An Evidence cell that does not name at least one of the five ToolKit JSON files, one of the prose reference docs, or one golden-shortcut XML filename **is not acceptable**. A verdict resting only on external corroboration is recorded as `UNVERIFIED`, never higher.

### Runnable lookup snippet

Every plan re-runs this identical query rather than improvising a new one:

```python
import json

DATA_DIR = "/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/skills/shortcuts-playground/data"

def search_ids(filename, patterns):
    with open(f"{DATA_DIR}/{filename}") as f:
        ids = json.load(f)["ids"]
    return [i for i in ids if any(p.lower() in i.lower() for p in patterns)]

def lookup_parameters(identifier):
    with open(f"{DATA_DIR}/toolkit-v78-first-party-parameter-keys.json") as f:
        tools = json.load(f)["tools"]
    return tools.get(identifier)  # None => not in the OS27 parameter catalog

def lookup_enum(type_python_name):
    with open(f"{DATA_DIR}/toolkit-v78-first-party-enum-cases.json") as f:
        types = json.load(f)["types"]
    return types.get(type_python_name.lower())  # None => enum cases not recoverable locally

# Example: search all three id snapshots for a capability
for fname in ("toolkit-v63-tool-ids.json", "toolkit-v78-tool-ids.json", "toolkit-v78-ios27-tool-ids.json"):
    print(fname, search_ids(fname, ["colorfilter", "grayscale"]))
```

### Worked example — reproducing the CAP-20 Evidence cell

1. `search_ids("toolkit-v63-tool-ids.json", ["colorfilter", "grayscale", "greyscale", "universalaccess"])` → includes `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` (present).
2. Same query against `toolkit-v78-tool-ids.json` → present.
3. Same query against `toolkit-v78-ios27-tool-ids.json` → **no matches at all** (absent).
4. `lookup_parameters("com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent")` → returns a record with `parameters` = `operation` / `state` / `ShowWhenRun`, each individually tagged `"platforms": ["macOS 27"]`, and a top-level `"platforms": ["macOS 27"]`.
5. `lookup_enum("com_apple_universal_access_uasettings_shortcuts_operation")` → no matching key found in `toolkit-v78-first-party-enum-cases.json`.

This is exactly the reasoning chain that produced CAP-20's Verdict (`NOT AVAILABLE`) and Evidence cell in §4 — present in the generic snapshots, macOS-27-only in the parameter catalog, absent from the iOS-27-simulator snapshot, no read-back mechanism found anywhere.

### Validator and signer invocations (recorded here for all later phases)

Validate:

```bash
validate-shortcut <file.xml> --target-macos 26 --target-platform ios
```

Sign:

```bash
sign-shortcut <file.xml> --name "<name>"
```

**Why target 26, not 27:** the v78-first-party-parameter-keys catalog — which gates several Notes/Screen-Time/system-control actions to specific platforms, including CAP-20's `UAToggleColorFiltersIntent` — is only loaded by the validator when targeting macOS/iOS 27+. At target 26, actions validate purely by identifier presence in the generic `toolkit-v63` allowlist, which is the more permissive and more accurate posture for an iOS 26 shortcut (per D-01, PROSOCHĒ targets iOS 26.x) built from long-standing actions. `--target-platform ios` is required to admit iOS-only rows and reject macOS-only rows that would otherwise leak in as falsely "available."

**A validator pass is necessary but not sufficient.** The validator checks structural/plist correctness only — it cannot execute a Shortcut, so it cannot catch runtime-only failures (silent UUID/wiring breaks, `WFTextTokenAttachment` vs `WFTextTokenString` display bugs, `GroupingIdentifier` mismatches). On-device manual verification remains required wherever this document records a fact as needing device confirmation.

## 4. Capability audit table

### Verdict vocabulary (closed — exactly four values, no others)

| Value | Meaning |
|---|---|
| `VERIFIED` | Identifier **and** parameter shape both evidenced. |
| `VERIFIED (identifier only)` | Identifier evidenced, parameter shape not evidenced anywhere in the bundle. |
| `UNVERIFIED` | Identifier exists but no schema evidence, or only non-Playground external evidence. |
| `NOT AVAILABLE` | No matching action found in any bundled snapshot. |

### Row-format rule

- Every row begins `| CAP-` at column 1.
- The **Verdict** cell contains exactly one of the four vocabulary values above and nothing else.
- The **Evidence** cell names a real file path (and JSON key path or doc line reference) that a reader can re-check.
- The **Fallback** cell is `n/a` only when the Verdict is `VERIFIED`; otherwise it names a concrete substitute behaviour.

### Table

| ID | Capability | Identifier | Parameter shape | Verdict | Evidence | Fallback |
|---|---|---|---|---|---|---|
| CAP-20 | Color Filters / grayscale (Ash) | `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` | `operation` (`com_apple_universal_access_uasettings_shortcuts_operation`, enum type, no case list found in `toolkit-v78-first-party-enum-cases.json`), `state` (`bool`, trueString `On` / falseString `Off`), `ShowWhenRun` (`bool`, trueString `On` / falseString `Off`) — all three parameters tagged `platforms: ["macOS 27"]` only, per direct query of `toolkit-v78-first-party-parameter-keys.json` run 2026-08-13 | NOT AVAILABLE | Queried, 2026-08-13, via a `python3` lookup against the five ToolKit snapshots at `/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/skills/shortcuts-playground/data/` for case-insensitive substrings `colorfilter`, `grayscale`, `greyscale`, `universalaccess`. Result: the identifier `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` **is present** in `toolkit-v63-tool-ids.json` (`ids` array, 1794 entries, generic pre-OS27 snapshot) and **is present** in `toolkit-v78-tool-ids.json` (`ids` array, 2731 entries, macOS 27 additions), but **is absent** from `toolkit-v78-ios27-tool-ids.json` (`ids` array, 1206 entries, iOS 27 Simulator snapshot — zero matches for any of the four search substrings in this file). Its `toolkit-v78-first-party-parameter-keys.json` record (`tools` key, keyed by identifier) reports top-level `"platforms": ["macOS 27"]` and every one of its three parameters individually tagged `"platforms": ["macOS 27"]` — no `iOS` or `iOS 27 Simulator` tag anywhere on this entry. No `colorfilter`/`grayscale`/`greyscale` string appears as an `is.workflow.actions.*` identifier in any of the three `ids` arrays. This confirms, rather than merely repeats, the research base at `.planning/research/STACK.md` §3 row 10 and `.planning/research/PITFALLS.md` C3 — the executor's own re-run of the lookup found the identical three facts: present in v63/v78 generic snapshots, macOS-27-only in the parameter catalog, absent from the iOS-27-simulator snapshot. No divergence from the research base was found. | see BD-01 |
| CAP-01 | Get Current App / current-app detection | `is.workflow.actions.getcurrentapp` (standalone action); inline magic-variable `Type: "CurrentApp"` | `WFVisibleAppScope` (`toolkit-v78-first-party-parameter-keys.json`, one parameter, platforms `["iOS 27 Simulator","macOS 27"]`); magic-variable form aggrandized via `WFPropertyVariableAggrandizement` for `Name`/`Bundle Identifier`, documented in `PARAMETER_TYPES.md` §"Current App" | VERIFIED | Queried 2026-08-13 via the §3 python3 recipe. `is.workflow.actions.getcurrentapp` present in `toolkit-v63-tool-ids.json`, `toolkit-v78-tool-ids.json`, and `toolkit-v78-ios27-tool-ids.json` (True/True/True). `lookup_parameters("is.workflow.actions.getcurrentapp")` returns one parameter, `WFVisibleAppScope`, tagged `platforms: ["iOS 27 Simulator","macOS 27"]` — cross-platform iOS confirmation, unlike CAP-20's macOS-27-only tagging. No divergence from `.planning/research/STACK.md` §3 row 1. | n/a for the identifier/parameter shape. Automation-context caveat (canonical strategy §5.1): Personal Automations pass the triggering app's identity to the invoked shortcut, but whether Get Current App reliably re-derives that identity from *inside* an automation-invoked run (vs a manual foreground run) is not established by this ToolKit and needs on-device confirmation for the OPEN automation specifically. If unreliable, trust the automation's own app filter — "if this shortcut was invoked by the OPEN automation at all, the app IS the configured target" — rather than re-deriving the app via Get Current App. |
| CAP-02 | Get File (fixed-path read, e.g. `state.json`) | `is.workflow.actions.documentpicker.open` (class `WFGetFileAction`/`WFSelectFilesAction`) | `WFFileErrorIfNotFound` (bool On/Off), `WFGetFolderContents` (bool On/Off), `WFFile` (File), `WFGetFilePath` (str) — all four platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters` returns the 4-parameter record above. `ACTIONS.md` line 30 cross-maps `WFGetFileAction`/`WFSelectFilesAction` → `is.workflow.actions.documentpicker.open`. No divergence from STACK.md §3 row 2 (Get File portion). | n/a. Note: `WFFileErrorIfNotFound=Off` suppresses the runtime error dialog on a missing file — this is the mechanism DEV-02's bootstrap substitute depends on. |
| CAP-03 | Save File / overwrite, and the file-existence-check question | `is.workflow.actions.documentpicker.save` (class `WFSaveFileAction`) | `WFInput` (File), `WFFolder` (File), `WFAskWhereToSave` (bool On/Off), `WFFileDestinationPath` (str), `WFSaveFileOverwrite` (bool On/Off, display name "Overwrite If File Exists") — all platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters("is.workflow.actions.documentpicker.save")` returns the 5-parameter record above — critically `WFSaveFileOverwrite` is a confirmed boolean (display name "Overwrite If File Exists"), so the overwrite/replace-existing shape IS evidenced. **Divergence from STACK.md §3 row 2**, which reported the overwrite behavior as "likewise UNVERIFIED in this bundle — no schema found"; this live re-run of the parameter-keys catalog finds it. File-existence finding: searched all three `ids` arrays and `ACTIONS.md`/`FILTERS.md`/`PARAMETER_TYPES.md` for `exist`/"file exist" substrings 2026-08-13 — zero matches for any standalone existence-check action or filter predicate anywhere in the bundle. Confirmed: no such action exists, consistent with STACK.md's finding on this specific point. | n/a for Save File/overwrite (VERIFIED). For the missing existence check: see DEV-02 — the substitute is to always attempt Get File with `WFFileErrorIfNotFound=Off`, then treat a non-dictionary/empty result from the following Detect Dictionary step as "state absent." |
| CAP-04 | Dictionary creation and Detect Dictionary (JSON text → dictionary parse) | `is.workflow.actions.dictionary` (create); `is.workflow.actions.detect.dictionary` (parse) | dictionary: `WFItems`; detect.dictionary: `WFInput` — both platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Both present True/True/True across all three id snapshots. `lookup_parameters` confirms `WFItems` on `dictionary` and `WFInput` on `detect.dictionary`, both cross-platform iOS27Sim+macOS27. `PARAMETER_TYPES.md` §"Dictionary Field Value" documents the nested `WFItems`/`WFDictionaryFieldValueItems` serialization. Golden XMLs `1be4dde9...xml`, `6a18b768...xml`, `ae59e10d...xml` (present under `golden-shortcuts/xml/`) use `detect.dictionary` on real API/JSON responses. No dedicated dictionary-to-JSON-string action identifier was found in any of the three `ids` arrays or in `ACTIONS.md`'s complete identifier list (searched `json`, `dictionary`, `text.` substrings). No divergence from STACK.md §3 row 3 on the two identifiers audited here. | n/a for creation/parsing. No distinct Dictionary→JSON-string action is evidenced anywhere in the bundle, so `state.json` writes must build the JSON body as a Text action template (a `Text`/`WFTextActionText` action holding a literal JSON-shaped string with variable placeholders) rather than assuming a magic "Dictionary → JSON string" action exists, per `BEST_PRACTICES.md`'s "complex JSON fallback" guidance. |
| CAP-05 | Get Dictionary Value / Set Dictionary Value | `is.workflow.actions.getvalueforkey`; `is.workflow.actions.setvalueforkey` | getvalueforkey: `WFGetDictionaryValueType`, `WFDictionaryKey`, `WFInput`; setvalueforkey: `WFDictionaryKey`, `WFDictionaryValue`, `WFDictionary` — both platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Both present True/True/True across all three id snapshots. `lookup_parameters` confirms both records above. `SKILL.md` rule 16 documents `WFDictionaryKey`'s 1-based dot notation for nested access (e.g. `results.tracks.items`). `BEST_PRACTICES.md` §Lists & Dictionaries: "always connect the target dictionary via WFDictionary; do not rely on implicit input" for setvalueforkey. No divergence from STACK.md §3 row 3. | n/a. Coercion hazards from PITFALLS A4, binding on every `state.json` read: JSON booleans coerce to numeric `1`/`0`, not strings `"true"`/`"false"` — branch on `Is Greater Than 0`/`Equals 1`, never string comparison. JSON `null` coerces to empty — guard nullable fields with "Has Any Value" before reading a nested key on them; reading a child key of a null parent breaks rather than returning empty. A Dictionary Value compared directly inside an If can evaluate blank — always route it through a Text action first, then compare the Text variable. |
| CAP-06 | Date arithmetic (Adjust Date, Format Date, Get Time Between Dates) | `is.workflow.actions.date`; `is.workflow.actions.adjustdate`; `is.workflow.actions.format.date`; `is.workflow.actions.gettimebetweendates` | adjustdate: `WFDate`, `WFAdjustOperation`, `WFDuration` (as `WFQuantityFieldValue{Magnitude,Unit}` per `VARIABLES.md`); format.date: catalog keys `WFDateFormatStyle`, `WFRelativeDateFormatStyle`, `WFTimeFormatStyle`, `WFISO8601IncludeTime`, `WFDateFormat`, `WFDate`, `WFLocale`, plus `WFDateFormatString` (custom-pattern key, confirmed only in `DATE_TIME.md` prose, not itself listed in the JSON parameter catalog — set `WFDateFormatStyle`="Custom" and `WFDateFormat`="Custom" to activate it); gettimebetweendates: `WFInput`, exactly one of `WFDate`/`WFTimeUntilCustomDate`/`WFTimeUntilFromDate`, `WFTimeUntilUnit` | VERIFIED | Queried 2026-08-13. All four identifiers present True/True/True across all three id snapshots. `is.workflow.actions.adjustdate` param-catalog record confirms `WFDate`/`WFAdjustOperation`/`WFDuration` (iOS27Sim+macOS27); `lookup_enum("adjustdate_wfadjust_operation")` returns a populated case list in `toolkit-v78-first-party-enum-cases.json`, confirming an explicit Add/Subtract enum exists. `is.workflow.actions.format.date` param-catalog record lists `WFDateFormatStyle`/`WFRelativeDateFormatStyle`/`WFTimeFormatStyle`/`WFISO8601IncludeTime`/`WFDateFormat`/`WFDate`/`WFLocale` (iOS27Sim+macOS27); `WFDateFormatString` itself is documented only in `DATE_TIME.md` line 67 ("For custom formats, set WFDateFormatStyle to Custom, set WFDateFormat to Custom, and put the custom pattern in WFDateFormatString") — a genuine catalog/prose split, not a gap, since the prose doc is a valid §3 evidence source. `is.workflow.actions.gettimebetweendates` param catalog lists `WFTimeUntilFromDate`/`WFInput`/`WFTimeUntilUnit`; `WFTimeUntilCustomDate` and `WFDate` as alternate single-operand keys are confirmed in `BEST_PRACTICES.md` lines 70/170 and `SKILL.md` rule 39 ("set WFInput and exactly one non-empty date operand... WFDate or WFTimeUntilCustomDate or WFTimeUntilFromDate"). No divergence from STACK.md §3 row 4 on the identifiers; the `WFDateFormatString` catalog/prose split is a nuance STACK.md did not call out explicitly. | n/a. Discipline from PITFALLS A6, confirmed verbatim in `ACTIONS.md` line 264 and `SKILL.md` rule 39: never put a `CurrentDate` magic token directly into a date operand (`WFDate`/`WFTimeUntilFromDate`/`WFTimeUntilCustomDate`) — it imports as an empty/default date field. Materialise "now" with a Date action set to Current Date first, then reference that action's output. |
| CAP-25 | Base64 encoding | `is.workflow.actions.base64encode` | `WFEncodeMode`, `WFBase64LineBreakMode`, `WFInput` — platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. `search_ids(["base64"])` returns `is.workflow.actions.base64encode` from all three snapshots (True/True/True). `lookup_parameters` confirms the 3-parameter record above. | n/a, and per this plan's binding instruction: not on any critical path. The architecture stores `state.json` as plain JSON text (no binary-encoding step anywhere in the OPEN/CLOSE/bootstrap design), so this identifier is audited for canonical-strategy §31 completeness only — no deviation is forced by its presence or absence. |
| CAP-S01 | Set Variable / Get Variable | `is.workflow.actions.setvariable`; `is.workflow.actions.getvariable` | setvariable: `WFInput`, `WFVariableName`; getvariable: `WFVariable` (typed `com_apple_shortcuts_wfcontent_item`) — both platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Both present True/True/True across all three id snapshots. `lookup_parameters` confirms both records above. | n/a. |
| CAP-S02 | Text (Get Text) | `is.workflow.actions.gettext` | `WFTextActionText` — platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters` confirms `WFTextActionText`. Confirmed the identifier is exactly `gettext`, not a `.text` variant — per PITFALLS A7's named gotcha, `ACTIONS.md` line 380's complete identifier list spells it `gettext` and no `is.workflow.actions.text` identifier appears in any of the three id snapshots. | n/a. |
| CAP-S03 | Number and Math | `is.workflow.actions.number`; `is.workflow.actions.math` | number: `WFNumberActionNumber`; math: `WFInput`, `WFMathOperation`, `WFScientificMathOperation`, `WFMathOperand`, `WFScientificMathOperand` — both platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Both present True/True/True across all three id snapshots. `lookup_parameters` confirms both records above. | n/a. JSON-sourced numeric strings (Pressure/Heat/Gravity/opens_today read from `state.json`) must pass through a Number action before Math or If use — per PITFALLS A5, a raw Dictionary Value text is not guaranteed to behave as a numeric operand. |
| CAP-S04 | If / Otherwise / End If | `is.workflow.actions.conditional` | `WFControlFlowMode` (integer: 0=If, 1=Otherwise/Otherwise-If, 2=End If) sharing one `GroupingIdentifier` per block; every condition code requires an explicit `WFInput` wrapped as `{Type:"Variable", Variable:{...}}` | VERIFIED | Queried 2026-08-13. Notable finding: `search_ids(["conditional"])` returns ZERO matches in any of the three id snapshots, and `lookup_parameters("is.workflow.actions.conditional")` returns `None` — absent from the OS27 parameter-keys catalog too. However identifier and full parameter shape ARE evidenced through the §3 protocol's prose+XML secondary sources: `ACTIONS.md` line 356 lists `conditional` in the 365-identifier complete list; `CONTROL_FLOW.md` (777 lines, "verified against an Apple-built sample shortcut") documents complete worked XML for all three `WFControlFlowMode` values (lines 199, 237, 252, 279, 403+) and states at line 354 "ALL conditional codes require an explicit WFInput as a Type=Variable wrapper... verified against an Apple-built sample where every single is.workflow.actions.conditional action sets WFInput explicitly." Golden XML `332c12a0060043b388b22b806be7ab58.xml` (and 4 others, grep-confirmed) contain real `is.workflow.actions.conditional` blocks. The full condition-code table (`CONTROL_FLOW.md` line ~189, cross-checked byte-for-byte against `BEST_PRACTICES.md`): 0=is less than, 1=is less than or equal to, 2=is greater than, 3=is greater than or equal to, 4=string is, 99=contains, 100=has any value, 101=does not have any value — **no numeric-equals code exists at any value**. `### Otherwise If (macOS 27+)` (`CONTROL_FLOW.md` line 263, restated line 777) confirms `Otherwise If` (mode 1 with condition fields present) is macOS-27+ scoped in this catalog. | n/a. Per D-01 (iOS 26.x target): nested If/Otherwise is used throughout this build instead of `Otherwise If`, which `CONTROL_FLOW.md`'s own heading tags macOS-27+. Nesting is evidenced working to depth 7 (`CONTROL_FLOW.md` §Nesting, citing production shortcut `AppRedirect.xml` from the 127-shortcut corpus analysis) — every level needs its own fresh `GroupingIdentifier`. |
| CAP-S05 | Repeat with a count | `is.workflow.actions.repeat.count` (class `WFRepeatAction`), two-endpoint mode-0/mode-2 pattern sharing one `GroupingIdentifier` | `WFRepeatCount` on the mode-0 start action; Repeat Index referenced as `Type: Variable`, `VariableName: "Repeat Index"` — never `Type: ActionOutput` on the end action's UUID | VERIFIED | Queried 2026-08-13. `search_ids(["repeat"])` returns ZERO matches in any of the three id snapshots, and `lookup_parameters("is.workflow.actions.repeat.count")` returns `None` — same absence pattern as CAP-S04. Identifier and full parameter shape are evidenced via `ACTIONS.md` (lines 34-82, 102-178, 658-756: complete worked XML for `is.workflow.actions.repeat.count` including `WFRepeatCount`, and for `is.workflow.actions.repeat.each`) and golden XMLs `2e0fb675e45948aaacee7e534f910492.xml`/`71f0cacb0f604b399b76c5dcb7286e7c.xml` (grep-confirmed to contain `is.workflow.actions.repeat.count`/`.repeat.each`). `ACTIONS.md` line 82: "Repeat Index uses Type: Variable with VariableName: 'Repeat Index', NOT Type: ActionOutput referencing the end action's UUID. Using the wrong type causes the variable to appear as 'Repeat Results' in the UI and fails at runtime." | n/a. Repeat Index and Repeat Item must be referenced as a named `Type: Variable`, never as an `ActionOutput` pointing at the end action's UUID — the single most emphasized wiring rule for this action pair across the doc set. |
| CAP-S06 | Get Item from List (bounded 9-iteration Pressure→Circle threshold lookup) | `is.workflow.actions.getitemfromlist` | `WFItemSpecifier` (enum `getitemfromlist_wfitem_specifier`, confirmed 5 cases: `First Item`, `Last Item`, `Random Item`, `Item At Index`, `Items in Range`), `WFItemIndex` (int), `WFItemRangeStart`/`WFItemRangeEnd` (int), `WFInput` (List) — all platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. `search_ids(["getitemfromlist","itemfromlist"])` finds `is.workflow.actions.getitemfromlist` present True/True/True across all three snapshots. `lookup_parameters` returns the 5-parameter record above. `lookup_enum("getitemfromlist_wfitem_specifier")` returns the full 5-case list including `Item At Index` (`caseCount: 5`) — the exact literal the bounded 9-iteration Repeat/Get-Item Pressure→Circle threshold lookup (Architecture §7) needs to index the active profile's threshold array by `Repeat Index`. Golden XMLs `332c12a0060043b388b22b806be7ab58.xml`, `71f0cacb0f604b399b76c5dcb7286e7c.xml`, `ae59e10d409348f9bd33894f03f9beb4.xml` all use `getitemfromlist` in real wiring. This is load-bearing per this plan (Architecture §7's Pressure→Circle scan) — both the identifier and the exact enum literal needed for indexed lookup are confirmed. | n/a. No substitute was needed; the action, its index parameter, and its enum literal are all confirmed present. |
| CAP-S08 | Set Name (rename before Save File) | `is.workflow.actions.setitemname` | `WFName` (str), `WFDontIncludeFileExtension` (bool), `WFInput` — platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters` confirms the 3-parameter record above. `ACTIONS.md` cross-maps Set Name ("outputs 'Renamed Item'") as the filename-control action chained before Save File per `BEST_PRACTICES.md`. | n/a. |

## 5. Deviation log

Numbered entries `DEV-01`, `DEV-02`, ... Each entry carries exactly five labelled fields: `Capability`, `Wanted`, `Verified`, `Substituted`, `Runnability`.

### DEV-01

- **Capability:** CAP-20 — Color Filters / grayscale (Ash primitive, canonical strategy §11 Primitive B).
- **Wanted:** The Ash primitive as literally specified in canonical strategy §11 Primitive B — "Grayscale where iOS can apply and restore it safely," a passive reduction of visual salience via a system-level grayscale toggle.
- **Verified:** `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` exists in the generic `toolkit-v63-tool-ids.json` and `toolkit-v78-tool-ids.json` snapshots, but its parameter-catalog record and every one of its three parameters are tagged `platforms: ["macOS 27"]` only, and the identifier does not appear at all in the iOS-27-Simulator-specific `toolkit-v78-ios27-tool-ids.json` snapshot. No grayscale/Color Filters action of any kind is confirmed available to Shortcuts.app on iPhone. No read-back mechanism for the current Color-Filters state exists in any bundled snapshot, consistent with there being no confirmed set action to read back from.
- **Substituted:** Per BD-01 in `docs/CAPABILITY-DECISIONS.md`, Ash is degraded to a non-environmental variant of Primitive B for the iOS build rather than a system-level Color Filters toggle. See BD-01 for the full rationale and the selected option among D-08's three named alternatives.
- **Runnability:** The Shortcut remains runnable because the Ash sequence slot (position 2 in Classic and Ambient, combined into "Ash + Confession" at position 3 in Black Mirror per canonical strategy §12) still resolves to a defined, safe, non-system-altering behaviour under BD-01's decision, and no OPEN-path routing depends on a grayscale action existing — per D-07 point 4 ("keep the Shortcut runnable... never let an unverified action block the OPEN/CLOSE path, corrupt state, or prevent Circle IX's always-a-route-out guarantee").

### DEV-02

- **Capability:** CAP-03 — Save File / file-existence check (bootstrap's "does `state.json` already exist" question).
- **Wanted:** A direct, cheap way to test whether `state.json` already exists at the fixed Shortcuts-folder path before attempting to read it, so bootstrap can branch cleanly between "first run, create defaults" and "returning user, load state" without ever surfacing a runtime error dialog.
- **Verified:** No standalone file-existence-check action or filter predicate exists anywhere in the bundle — confirmed 2026-08-13 by searching all three `ids` snapshots and `ACTIONS.md`/`FILTERS.md`/`PARAMETER_TYPES.md` for `exist`/"file exist" substrings, zero matches. What IS verified: `is.workflow.actions.documentpicker.open` (CAP-02) carries a confirmed `WFFileErrorIfNotFound` boolean parameter (display name "Error If Not Found"), and `is.workflow.actions.detect.dictionary` (CAP-04) is a confirmed, evidenced parsing step.
- **Substituted:** Always attempt Get File at the fixed `state.json` path with `WFFileErrorIfNotFound=Off` (suppressing the uncatchable runtime error dialog on a missing file), then pipe the result through Detect Dictionary; treat a non-dictionary or empty result as "state absent" and drive the bootstrap-vs-load branch off that outcome rather than off a direct existence check. This is exactly the pattern `.planning/research/STACK.md` §3 row 2 and `.planning/research/PITFALLS.md` B3 already anticipated, now confirmed as the only available mechanism rather than one candidate among several, since no alternative existence-check action exists in this bundle.
- **Runnability:** The Shortcut remains runnable on both first run (no `state.json` yet) and every subsequent run, because the substitute never depends on an action that can throw an uncatchable dialog — `WFFileErrorIfNotFound=Off` plus the Detect Dictionary guard is a documented, evidenced combination (CAP-02, CAP-04), not a speculative one, and it degrades gracefully into the "reconstruct fresh default state" recovery path PITFALLS B3 already requires for corrupt/missing JSON.

## 6. User action items

_Owner: appended to by plans 01-04 and 01-05. Entries are numbered `UA-01`, `UA-02`, ... each with the labelled fields `What`, `Why only a human can do it`, `Exact steps`, `What to record on completion`, `Which phase is gated`._

## 7. Coverage check

_Owner: finalised by plan 01-05._
