# PROSOCHĒ — Build Notes

## Phase 8 distribution record (2026-08-13)

- Both unsigned forks pass `plutil -lint` and Shortcuts Playground with `--target-macos 26 --target-platform all`; signed files and dated unsigned archives are listed in `artifacts/shortcuts/MANIFEST.md`.
- Sentient uses the direct-device-evidenced `WFLLMModel = Apple Intelligence on Device` literal and `WFGenerativeResultType = Text`. The OS-27-only `WFAllowWebSearch` and `FollowUp` keys are absent.
- The model is a bounded advisory contract auditor only. A malformed, empty, or completed-but-slow result follows Dumb. The audit does not claim to catch an unavailable or indefinitely hung platform action.
- No external analytics or application/web-content access exists. Core deterministic functionality has no network dependency; users can bypass the experience or decline the optional audit.
- Device evidence is not fabricated: `xcrun devicectl list devices` found no connected iPhone. DIST-03 remains unchecked pending imports and first Manual runs on a qualifying Apple-Intelligence-capable iPhone.

## 1. Purpose and scope

This document is the durable capability record for the PROSOCHĒ build. Every later phase treats it as ground truth. It is **appended to, never rewritten** — once a row, deviation entry, or action item is recorded, later plans may only add new rows/entries or extend existing sections; they do not delete or silently reword what is already here.

It covers **iOS 26.x native Shortcuts only** (per D-01 — target iOS 26.x, native Shortcuts only, no companion app, no Screen Time blocking APIs, no private APIs).

**Cross-references:** This document is one of three Phase 1 artifacts, each pointing at the other two so a reader landing on any one finds the rest. The single editable tuning block (profile threshold tables, sequence orderings, Ice cooldown durations, Heat coefficients) lives at `src/CONFIG-BLOCK.md`, not here. The five blocker decisions (BD-01 through BD-05) this document's capability rows and deviations feed into live at `docs/CAPABILITY-DECISIONS.md`, not here.

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

### Simulator and probe observations — extension to the citation rule

The rule above admits file-level sources only, which leaves an agent who has actually *run* something with no legal way to cite it — so the finding is either dropped or laundered into a file-level citation it did not come from. Two further classes are admissible:

- **A simulator observation** — cite it by naming the shortcut run, the command used, and the runtime and device it ran against.
- **A probe observation** — the same three, plus the open question the probe was built to answer.

Both rank **below** the primary device evidence of §11 and §14, and **above** any ToolKit-catalog inference.

**Ceiling.** A simulator observation may raise a verdict above `UNVERIFIED` only for behaviour the simulator can actually exercise. It may **never** do so for the Notes path, Apple Intelligence, Personal Automation triggers, or environmental capture-and-restore — those stay device-gated no matter how cleanly the simulator ran.

**Recording duty.** A probe result is written back — into this document's device-evidence sections, and into `docs/CAPABILITY-DECISIONS.md` where it settles a capability question — rather than left in the transcript. A probe nobody recorded has to be run again.

The tooling inventory and the full four-rung evidence-escalation ladder live in `.claude/CLAUDE.md` §9, which is their single home. Nothing measured is restated here, so the two cannot drift.

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

This is exactly the reasoning chain that produced CAP-20's *original* Verdict (`NOT AVAILABLE`) and Evidence cell in §4 — present in the generic snapshots, macOS-27-only in the parameter catalog, absent from the iOS-27-simulator snapshot, no read-back mechanism found anywhere.

> **Retained as a methodology worked example only — its conclusion was wrong, twice over.** BD-01-R showed step 3's simulator absence is evidence about simulators, not iOS. BD-01-R2 then showed the whole chain was querying the wrong identifier: iOS ships `AXToggleColorFiltersIntent` under `com.apple.AccessibilityUtilities.AXSettingsShortcuts`, which is in **none** of the three snapshots, so no query over these files could ever have found it. Step 5 is also factually wrong — the enum cases *are* in `toolkit-v78-first-party-enum-cases.json`, nested under its top-level `types` key. The standing lesson: this chain establishes what the catalog says, never what the device does. Only a donor settles that.

### Validator and signer invocations (recorded here for all later phases)

Validate — **gate A, mandatory** (`Validation passed.`, exit 0):

```bash
validate-shortcut <file.xml> --target-macos 26 --target-platform all
```

Validate — **gate B, advisory** (exit 1 with exactly one waived line per fork):

```bash
validate-shortcut <file.xml> --target-macos 27 --target-platform all
```

Sign:

```bash
sign-shortcut <file.xml> --name "<name>"
```

**The rule is not restated here.** The two-gate rule, the waiver, gate B's advisory status and its false-acceptance limit are stated once, in `.claude/CLAUDE.md` §1 `### Exact validator invocation`. Measurements are in §22 below.

**Amended 2026-08-17 (quick task `260817-ewg`).** The paragraph this replaced closed with the claim that `--target-platform ios` is required to admit iOS-only rows and reject macOS-only rows that would otherwise leak in as falsely "available." **That premise is retired: it does not hold.** Measured, the `ios` setting excludes every `macOS 27`-tagged catalog entry — dropping all four Notes actions out of parameter-key and enum-case checking — and, paired with `--target-macos 26`, admits no snapshot at all. The controlling variable is `--target-macos`, not `--target-platform`. See §22.

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
| CAP-20 | Color Filters / grayscale (Ash) | **iOS 26 (operative): `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`** — donor-confirmed. macOS twin (not for this build): `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` | `state` — integer, **boolean-valued**: **`1` = On, `0` = Off** (both donor-confirmed). `operation` — **string** enum case id (`"toggle"` donor-confirmed), **elided when Turn**, so authoring omits it entirely and never needs the `"turn"` literal. **Do not read the intentdefinition's declared types or case indices as the plist encoding** — it declares `state` as `Integer` with a `State` enum of `on`=1/`off`=2, but Shortcuts renders a `State`-typed enum as an On/Off switch and writes a plain boolean; the macOS catalog's `typePythonName: bool` was the accurate description. **No `ShowWhenRun` on the iOS intent.** Case names/indices from Apple's own `AccessibilityUtilities.framework` `Intents.intentdefinition`, archived at `.planning/spikes/005-ios-color-filters-identifier/AXToggleColorFilters-intentdefinition.txt` | VERIFIED | **Superseded evidence, 2026-08-16 — donor ground truth, two donors.** `.planning/debug/Set Colour Filters.shortcut` and `.planning/debug/Donor 9.shortcut`, both exported from the owner's iPhone and decrypted via the AEA1 round-trip (`.claude/CLAUDE.md` §8). The first is one action: the `AX*` identifier above with `<key>state</key><integer>1</integer>` and no other parameter. The second is two actions on the same identifier — one carrying `<key>operation</key><string>toggle</string>` plus `<key>state</key><integer>1</integer>`, one with no parameters at all — establishing that `operation` is a string. `.planning/debug/Donor 9.1.shortcut` is that same parameter-less action (identical UUID) configured **Off**, and emits `<key>state</key><integer>0</integer>` with no `operation` — establishing that `state` is a plain bool-as-integer and that `turn` is the elided default. Between them the three donors pin every value CIRC-02 writes. The `AX*` identifier is absent from **all three** bundled ToolKit snapshots (v63 / v78 / v78-ios27) — a genuine catalog gap, matching the `AX*`-private / `UA*`-public split the Playground's own `APPINTENTS.md` line 116 documents for sibling accessibility toggles. A sweep of all 35 intents in that framework found **no `Get*`/`Query*` read-back intent for any accessibility setting**, so §21's read-back problem stands; however every `Toggle*` intent declares a `state` *response* parameter, an untested lead recorded in BD-01-R2. *Correction to the original row:* its claim that the `operation` enum had "no case list found in `toolkit-v78-first-party-enum-cases.json`" was wrong — the cases are present under that file's top-level `types` key, the exact lookup gotcha `.planning/spikes/CONVENTIONS.md` documents. *Original catalog-only evidence (2026-08-13), retained:* the `UA*` identifier is present in `toolkit-v63-tool-ids.json` and `toolkit-v78-tool-ids.json`, absent from `toolkit-v78-ios27-tool-ids.json`, with its parameter record tagged `platforms: ["macOS 27"]`. BD-01-R established that absence from an **iOS Simulator** snapshot is evidence about simulators, not iOS; this donor confirms that reasoning empirically. | see BD-01-R2 (supersedes BD-01-R, which supersedes BD-01) |
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
| CAP-11 | Ask for Input | `is.workflow.actions.ask` | `WFAskActionPrompt`, `WFInputType`, `WFAskActionDefaultAnswer`, `WFAskActionDefaultAnswerNumber`, `urlAnswer`, `WFAskActionDefaultAnswerURL`, `WFAskActionDefaultAnswerDate`, `WFAskActionDefaultAnswerTime`, `WFAskActionDefaultAnswerDateAndTime`, `WFAskActionAllowsDecimalNumbers`, `WFAskActionAllowsNegativeNumbers`, `WFAllowsMultilineText`, `ShowWhenRun` — platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters` returns the 13-parameter record above. `WFInputType` enum values Text/Number/URL/Date/Date and Time documented in `PARAMETER_TYPES.md` §WFInputType; full working example in `EXAMPLES.md` Example 2. No divergence from STACK.md §3 row 6. | n/a. This backs Confession's free-text intention and its custom time boundary. |
| CAP-12 | Choose from Menu / Choose from List | `is.workflow.actions.choosefrommenu`; `is.workflow.actions.choosefromlist` | choosefrommenu: control-flow modes 0/1/2, `WFMenuPrompt`, `WFMenuItems` (array), one mode-1 case per item with `WFMenuItemTitle` matching exactly and in identical order; choosefromlist: `WFInput`, `WFChooseFromListActionPrompt`, `WFChooseFromListActionSelectMultiple`, `WFChooseFromListActionSelectAll` | VERIFIED | Queried 2026-08-13. `choosefromlist` present True/True/True with `lookup_parameters` confirming the 4-parameter record above (iOS27Sim+macOS27). `choosefrommenu` shows the same absence-from-JSON pattern as CAP-S04/CAP-S05 — zero matches across all three id snapshots and `None` from `lookup_parameters` — but is exhaustively documented in `CONTROL_FLOW.md` (lines 554-642, "verified from 127 real shortcuts analysis") with full worked XML for menu-definition mode 0 (`WFMenuItems` array) and per-item mode-1 cases (`WFMenuItemTitle`), plus the explicit rule at lines 639-642: "WFMenuItemTitle must match exactly... Order must match." `ACTIONS.md` line 356 lists `choosefrommenu` in the complete 365-identifier list. No divergence from STACK.md §3 row 6 on the identifiers. | n/a. Top documented real-world failure mode: `WFMenuItemTitle` values must match the corresponding `WFMenuItems` entries exactly (case-sensitive) and in identical order — this backs both the six-exit menu and the Control Room's manual menu. |
| CAP-13 | Open App | `is.workflow.actions.openapp` | `WFSelectedApp`, `WFAppName`, `WFWindowingFormat` (OS27-only) — platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters` returns `WFSelectedApp`/`WFAppName`/`WFWindowingFormat` — **not `WFAppIdentifier`** as this plan's candidate list and STACK.md §3 row 7 both name; a genuine divergence caught by the live re-run: the real iOS27-parameter-catalog keys are `WFSelectedApp` (app reference) and `WFAppName` (display name). `ACTIONS.md` line 159 confirms `WFWindowingFormat` is the "New" OS27 Window Location & Size parameter (values `Full Screen`/`Left`/`Right`/`Top`/`Bottom`/etc.). | n/a. Per D-01, omit `WFWindowingFormat` at the iOS 26 target; use `WFSelectedApp`/`WFAppName` to reference the target app, not the previously-assumed `WFAppIdentifier` key. |
| CAP-14 | Open URLs / web search | `is.workflow.actions.openurl`; `is.workflow.actions.searchweb` | openurl: `WFInput`; searchweb: `WFSearchWebDestination`, `WFInputText` — platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Both present True/True/True across all three id snapshots. `lookup_parameters("is.workflow.actions.searchweb")` returns `WFSearchWebDestination`/`WFInputText`, not a bare `WFInput` as this plan's candidate list assumed — divergence noted. `openurl` confirms `WFInput` as expected. | n/a. If `searchweb`'s provider behaviour (which search engine/app it opens via `WFSearchWebDestination`) proves unsuitable on-device, the substitute is Open URL to a query-shaped search URL (e.g. `https://www.google.com/search?q=`). |
| CAP-15 | Maps search | `is.workflow.actions.searchmaps`; `is.workflow.actions.getmapslink`; `is.workflow.actions.getdirections` | searchmaps: `WFInput`, `WFSearchMapsActionApp`; getmapslink: `WFInput`; getdirections: `WFLocation`, `WFDestination`, `WFGetDirectionsActionApp`, `WFGetDirectionsActionMode` — all platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. All three identifiers present True/True/True across all three id snapshots. `lookup_parameters` confirms the records above for each. No divergence from STACK.md §3 row 7. | n/a. |
| CAP-21 | Speak Text | `is.workflow.actions.speaktext` | `WFSpeakTextWait`, `WFSpeakTextRate`, `WFSpeakTextPitch`, `WFSpeakTextLanguage`, `WFSpeakTextVoice`, `WFText` — platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters` returns the 6-parameter record above, including `WFText` as the text-input parameter key. **Positive divergence from STACK.md §3 row 11**, which reported the text-input key as "commonly WFText/WFSpeakTextText... not spelled out in this plugin's docs beyond identifier presence" — the live re-run of the parameter-keys catalog finds `WFText` confirmed. Per this plan's instruction, since the parameter shape IS evidenced, the verdict is full `VERIFIED`, not `VERIFIED (identifier only)`. | n/a. Safety constraint: the Voice primitive never raises volume and never produces startling output — wire `WFText` to the Mirror/Voice message text as `WFTextTokenString` (display-parameter rule) and leave `WFSpeakTextRate`/`WFSpeakTextPitch` at their defaults rather than tuning for emphasis. |
| CAP-22 | Lock Screen | `is.workflow.actions.lockscreen` | Zero parameters (confirmed: empty `parameters` array) | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters("is.workflow.actions.lockscreen")` returns `parameterCount: 0`, empty `parameters` array, platforms `["iOS 27 Simulator","macOS 27"]` — cross-platform confirmed, zero-parameter action. Distinguished from two look-alikes, both separately queried: `is.workflow.actions.lock.app` (Lock App — present True/True/True, params `WFLockAppOperation`/`WFApp`, platforms `["iOS 27 Simulator","macOS 27"]` — locks a *specific app*, not the screen) and `com.apple.controlcenter.LockScreenIntent` (present in v63/v78 generic snapshots but **absent** from `toolkit-v78-ios27-tool-ids.json`, and tagged `platforms: ["macOS 27"]` only in the parameter catalog — a Control-Center-specific, macOS-27-scoped intent, not evidenced for iOS). `ACTIONS.md` line 388 lists `lock.app`/`lockscreen` as adjacent-but-distinct identifiers. No divergence from STACK.md §3 row 12. | n/a for the identifier/parameter shape (zero-param, cross-platform). Open question from PITFALLS C5: whether Lock Screen behaves correctly when invoked from an automatically-triggered Personal Automation, rather than a manual foreground run, is not established by this bundle and must be confirmed on-device in Phase 5. Named fallback per canonical strategy §11 Primitive I: route to Close, the Control Room, or another strongest safe exit if Lock Screen proves unreliable in the automation context. |
| CAP-23 | Run Shortcut | `is.workflow.actions.runworkflow`; `com.apple.shortcuts.RunShortcutIntent` | runworkflow: `WFWorkflow`, `WFInput` (platforms `["iOS 27 Simulator","macOS 27"]`); RunShortcutIntent: `shortcut` (platforms `["macOS 27"]` only, absent from the iOS 27 Simulator snapshot's parameter provenance) | VERIFIED | Queried 2026-08-13. `is.workflow.actions.runworkflow` present True/True/True across all three id snapshots; `lookup_parameters` returns `WFWorkflow`/`WFInput`, both tagged iOS27Sim+macOS27. **Positive divergence from STACK.md §3 row 13's** "UNVERIFIED exact parameter keys" finding — the live re-run of the parameter-catalog lookup DOES find a confirmed 2-parameter shape. `com.apple.shortcuts.RunShortcutIntent` present in all three id snapshots but its parameter-catalog record (`shortcut` key) is tagged `platforms: ["macOS 27"]` only, absent from the iOS27-Simulator parameter provenance — the weaker-evidenced of the two mechanisms for this project. | n/a via `runworkflow`. PROSOCHĒ ships as a single monolithic action graph per fork, so this action is not on the critical path and is audited only because canonical strategy §31 lists it. |
| CAP-24 | Wait | `is.workflow.actions.delay`; `is.workflow.actions.waittoreturn` | delay: `WFDelayTime` (bare `float`, seconds); waittoreturn: zero parameters — both platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Both present True/True/True across all three id snapshots. `lookup_parameters("is.workflow.actions.delay")` returns exactly one parameter, `WFDelayTime`, `typePythonName: "float"`. **Positive divergence from STACK.md §3 row 14's** "parameter keys not detailed" finding — the live re-run finds a confirmed shape, and it is a **bare float (seconds)**, not the `Magnitude`/`Unit` `WFQuantityFieldValue` pattern this plan's own candidate text speculated. `lookup_parameters("is.workflow.actions.waittoreturn")` returns `parameterCount: 0`, matching STACK.md. | n/a. The CLOSE handler's app-switch race brief-wait step (canonical strategy §20 step 4) can be built directly against `WFDelayTime` as a plain float-seconds value rather than needing on-device Craig-Loop confirmation of an assumed Magnitude/Unit shape. |
| CAP-28 | Get App & Website Data | `com.apple.intelligenceplatform.IntelligencePlatform.IntelligencePlatformDataActionsAppIntentsExtension.CalculateAppUsageIntent` | `during`, `selectedDevice`, `activityType`, `startTime`, `endTime` — platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters` confirms the 5-parameter record above, cross-platform iOS27Sim+macOS27. No divergence from STACK.md §3 row 16. | n/a. Explicitly out of scope for v1 — audited for canonical strategy §31 completeness only, so nothing in v1 depends on the `during`/`activityType` enum case values (not separately confirmed in `toolkit-v78-first-party-enum-cases.json` during this pass). |
| CAP-S07 | Show Alert / Show Result / Show Notification | `is.workflow.actions.alert`; `is.workflow.actions.showresult`; `is.workflow.actions.notification` | alert: `WFAlertActionTitle`, `WFAlertActionMessage`, `WFAlertActionCancelButtonShown`; showresult: `Text`; notification: `WFNotificationActionTitle`, `WFNotificationActionBody`, `WFNotificationActionSound`, `WFInput` — all platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. `search_ids(["alert","showresult","notification"])` finds `is.workflow.actions.alert`, `is.workflow.actions.showresult`, `is.workflow.actions.notification` present True/True/True across all three id snapshots. `lookup_parameters` confirms the three records above, all iOS27Sim+macOS27. | n/a. Highest-consequence authoring rule in the whole build: display-facing text parameters (`WFAlertActionTitle`/`WFAlertActionMessage`, `WFNotificationActionTitle`/`WFNotificationActionBody`, showresult's `Text`) must use `WFTextTokenString` with an object-replacement placeholder and `attachmentsByRange`, even for a single bare variable; data-flow parameters use `WFTextTokenAttachment`. `VARIABLES.md` reports this as runtime-verified across "all 46 Show Alert and 41 Notification instances" in the 127-shortcut corpus. Using the attachment form on a display parameter validates and imports cleanly but renders empty/default text at runtime — this will NOT be caught by the plist validator, only by an on-device run. |
| CAP-07 | Notes search / find (Find Notes) — Control Room, per D-12/AUDIT-05 | `is.workflow.actions.filter.notes` | `WFContentItemFilter` (`query_com_apple_notes_note_entity`, complex predicate type, serialized as `WFContentPredicateTableTemplate`), `WFContentItemSortProperty` (`com_apple_notes_note_entity_wfcontent_item_sort_property`), `WFContentItemSortOrder` (`str`), `WFContentItemLimitEnabled` (`bool`, On/Off), `WFContentItemLimitNumber` (`float`), `WFCompoundType` (`com_apple_notes_note_entity_wfcompound_type`), `WFContentItemInputParameter` (`com_apple_notes_note_entity_wfcontent_item_input_parameter`, name "note") — all 7 parameters and the action's top-level record individually tagged `platforms: ["macOS 27"]` in `toolkit-v78-first-party-parameter-keys.json` | VERIFIED | Queried 2026-08-13 via the §3 python3 recipe, re-run live rather than transcribed from research. `search_ids` for `filter.notes`/`notes` substrings: `is.workflow.actions.filter.notes` is **present** in `toolkit-v63-tool-ids.json` (generic pre-OS27 snapshot — the operative iOS-availability signal for a pre-existing, long-standing action per §3) and **present** in `toolkit-v78-tool-ids.json`; **absent** from `toolkit-v78-ios27-tool-ids.json`. Notably, an unfiltered substring search across that one file for any `com.apple.Notes.*`/`filter.notes`/`appendnote`/`shownote` identifier returns **zero matches of any kind** — the entire Notes namespace is missing from this one narrow iOS-27-Simulator capture, not just this action, which is the strongest possible form of the "bundled-data completeness gap, not evidence of macOS-exclusivity" case §3 already names Notes as the paradigm example of. `lookup_parameters("is.workflow.actions.filter.notes")` returns the 7-parameter record above from `toolkit-v78-first-party-parameter-keys.json`, tagged `platforms: ["macOS 27"]` throughout — a provenance fact about which build captured the catalog, per §3's own description of this file, not by itself proof of iOS exclusivity. Cross-corroborated by two independent prose citations, `BEST_PRACTICES.md` lines 175 and 299, giving the actual on-the-wire serialization shape: `WFContentItemFilter` must be `WFContentPredicateTableTemplate` with non-empty `WFActionParameterFilterTemplates`; the Name filter row uses `Values.String`/`WFTextTokenString`, the Folder filter row uses `Values.Enumeration`/`WFLinkDynamicOptionSubstitutableState`. This is the same identifier/prose-fills-JSON-gap evidentiary pattern already used for CAP-S04/CAP-S05 elsewhere in this document, both of which landed full `VERIFIED` on weaker JSON id-snapshot presence (zero of three) than this row has (two of three, plus a documented and explained absence from the third). No divergence from `.planning/research/STACK.md` §3 row 5 on the identifier itself. | n/a for the identifier/parameter shape (VERIFIED). Group-wide note, recorded identically on all four CAP-07..CAP-10 rows per this plan's binding instruction: `interpretAsMarkdown` — exposed on CAP-08 (Create Note) and CAP-09 (Append to Note), not a parameter of this action — is an OS27-gated boolean and must not be set when validating at the iOS 26 target (per D-01); every boolean on these four actions must be serialized as a real plist boolean, never a string. On-device confirmation of Find Notes' actual iOS behaviour is tracked as UA-01 (§6), gating Phase 2. |
| CAP-08 | Create Note (Control Room bootstrap) — per D-12/AUDIT-05 | `com.apple.mobilenotes.SharingExtension` (primary candidate, display name "Create Note"); `com.apple.Notes.CreateNoteFromMarkdownLinkAction` (markdown-specific alternate) | SharingExtension: `name` (`str`), `contents` (`AttributedString`), `folder` (`com_apple_notes_folder_entity`), `interpretAsMarkdown` (`bool`, On/Off), `OpenWhenRun` (`bool`, On/Off) — all 5 tagged `platforms: ["macOS 27"]` in `toolkit-v78-first-party-parameter-keys.json`. CreateNoteFromMarkdownLinkAction: absent from that same OS27 parameter-keys catalog entirely (`lookup_parameters` returns `None`); its content-parameter key is instead independently documented, twice, in prose: `BEST_PRACTICES.md` line 121 — "For `com.apple.Notes.CreateNoteFromMarkdownLinkAction`, use `markdownContents` (camelCase) as the content parameter key — this is the official AppIntent parameter name from the toolkit and the runtime-required key. Do not use `markdown` as a substitute; it can pass older validation but produce an empty note body at runtime." — and `CHANGELOG.md` line 447 — "Root cause: `com.apple.Notes.CreateNoteFromMarkdownLinkAction` uses `markdownContents` (camelCase) as its content parameter, not `markdown`. The validator accepts `markdown` but the runtime produces an empty note." | VERIFIED | Queried 2026-08-13. `com.apple.mobilenotes.SharingExtension` present in `toolkit-v63-tool-ids.json` and `toolkit-v78-tool-ids.json`, absent from `toolkit-v78-ios27-tool-ids.json` (same whole-namespace-absent pattern as CAP-07, non-disqualifying per §3). `lookup_parameters` returns the 5-parameter record above, tagged `platforms: ["macOS 27"]`. `com.apple.Notes.CreateNoteFromMarkdownLinkAction` is present **only** in `toolkit-v63-tool-ids.json` (True/False/False) — absent from the v78 generic snapshot too, not just the iOS-27-simulator one, meaning `lookup_parameters` returns `None` for it; its shape is recoverable only via the two independent prose citations named in the Parameter shape cell, the same CAP-S04/CAP-S05 prose-fills-JSON-gap pattern used elsewhere in this document. **This is the single highest-consequence authoring trap in the whole build**: `markdown` (the shorter, plausible-looking key) passes the Playground's own validator but produces an empty note body at runtime, per the CHANGELOG's explicit root-cause note; the camelCase key `markdownContents` is the runtime-correct one, recorded here verbatim. Since the Control Room Note is the entire onboarding surface, using the wrong key silently ships a Shortcut whose first-run note is empty — the user never sees the setup instructions at all. No divergence from `.planning/research/STACK.md` §3 row 5 on either identifier. | n/a for the identifier/parameter shape (VERIFIED). The runtime-correct content key is `markdownContents` (camelCase) on `com.apple.Notes.CreateNoteFromMarkdownLinkAction` — the failure mode of the wrong key (`markdown`) is a validator false-pass with an empty note body at runtime, not a build-time error, so `validate-shortcut` will not catch it; UA-01 (§6) must specifically confirm the Control Room Note actually contains its body text after import. `interpretAsMarkdown` on `com.apple.mobilenotes.SharingExtension` is an OS27-gated boolean and must not be set when validating at the iOS 26 target (per D-01); prefer `com.apple.Notes.CreateNoteFromMarkdownLinkAction` + `markdownContents` for the markdown-formatted Control Room body at the iOS 26 target rather than `SharingExtension` + `interpretAsMarkdown`. |
| CAP-09 | Append to Note (Attention Ledger growth) — per D-12/AUDIT-05 | `is.workflow.actions.appendnote` | `operation` (`com_apple_notes_append_operation`, append or prepend), `entity` (`com_apple_notes_note_entity`), `text` (`AttributedString`), `section` (`str`), `ignoreWhitespace` (`bool`, On/Off), `interpretAsMarkdown` (`bool`, On/Off) — all 6 tagged `platforms: ["macOS 27"]` in `toolkit-v78-first-party-parameter-keys.json` | VERIFIED | Queried 2026-08-13. Present True/True/False across the three id snapshots (v78-ios27 absent — same whole-namespace gap as CAP-07/CAP-08). `lookup_parameters("is.workflow.actions.appendnote")` returns the 6-parameter record above. Independently cross-corroborated in `ACTIONS.md`'s "OS 26 to 27 Updated Parameters" table: `section`/`ignoreWhitespace`/`interpretAsMarkdown` documented as the new/updated parameters, `operation` (accepting `append` or `prepend`) as the pre-existing key. No divergence from `.planning/research/STACK.md` §3 row 5 on the identifier or parameter names. | n/a for the identifier/parameter shape (VERIFIED). `interpretAsMarkdown` is an OS27-gated boolean and must not be set when validating at the iOS 26 target (per D-01; `ACTIONS.md`'s own "OS 26 to 27 Updated Parameters" heading confirms this whole table's params are target-gated). This is the action the ATTENTION LEDGER's append-only growth (canonical strategy §5.4, PITFALLS D7) depends on; on-device confirmation of its own separate first-use permission prompt is tracked as UA-01 (§6). |
| CAP-10 | Show / open a Note (Control Room manual-menu "Open Control Room") — per D-12/AUDIT-05 | `is.workflow.actions.shownote` | `target` (`com_apple_notes_note_entity`) — 1 parameter, tagged `platforms: ["macOS 27"]` in `toolkit-v78-first-party-parameter-keys.json` | VERIFIED | Queried 2026-08-13. Present True/True/False across the three id snapshots (same whole-namespace-absent-from-iOS27-sim pattern as CAP-07/08/09). `lookup_parameters("is.workflow.actions.shownote")` returns the single-parameter record above. `APPINTENTS.md` line 2726 independently confirms `is.workflow.actions.shownote` (alongside `appendnote` and `filter.notes`) is a WF-namespace action documented in `ACTIONS.md`, not an AppIntent — consistent classification, no divergence from `.planning/research/STACK.md` §3 row 5. | n/a for the identifier/parameter shape (VERIFIED). Group-wide note: `interpretAsMarkdown` — not a parameter of this action — is OS27-gated on the two Notes actions that do carry it (CAP-08, CAP-09) and must not be set at the iOS 26 target. This is the action the Control Room manual menu's "Open Control Room" item depends on; on-device confirmation is tracked as UA-01 (§6). |
| CAP-16 | Set Brightness (Dimming, Primitive E) — per D-09/AUDIT-03 | `is.workflow.actions.setbrightness` | `WFBrightness` (`float`), `ShowWhenRun` (`bool`, On/Off) — both tagged `platforms: ["iOS 27 Simulator","macOS 27"]` in `toolkit-v78-first-party-parameter-keys.json` | VERIFIED | Queried 2026-08-13. `search_ids(["brightness"])` finds `is.workflow.actions.setbrightness` present True/True/True across all three id snapshots — the identifier is confirmed present in all three, including the iOS-27-Simulator snapshot (unlike every Notes action above), one of the few system-control actions in the whole audit with direct iOS-snapshot confirmation. `lookup_parameters` returns the 2-parameter record above, both tagged cross-platform `["iOS 27 Simulator","macOS 27"]` — confirmed provenance, not merely a macOS27-only tag. No divergence from `.planning/research/STACK.md` §3 row 8 or `.planning/research/ARCHITECTURE.md` §0's grounding audit on the Set side. | n/a. **⚠ Section 21's floor clause is SUPERSEDED on the main line by D-01** (user decision LOCKED 2026-08-17, recorded 2026-08-18 by phase 16 plan 05; see §30 for the record and `docs/CAPABILITY-DECISIONS.md` BD-02's **Supersession** note, which is the governing authority). The bound this cell asserted until that date is **cited there and deliberately not restated here** — this cell declares itself binding on Phase 5's CIRC-05, so a stale instruction here is not a note, it is a live order. The canonical strategy is retained unmodified as the original design input. **What binds CIRC-05 now:** `WFBrightness` is written only when the original brightness has been captured **and durably persisted** first, and it is always restored; a run whose read returns nothing changes nothing (SAFE-03). The value written is `safety.dim_target` in `src/CONFIG-BLOCK.md`, at or above `safety.brightness_floor` — both `0` as shipped by plan 16-03 — a relationship `docs/environmental_restore_check.py` pins structurally. Per **CAP-08** the parameter is OPTIONAL, so the real hazard at this action is an **absent** `WFBrightness`, which silently applies an unrequested default with no captured original behind it; `docs/phase5_self_check.py` asserts its presence. See BD-02 for whether/when this action may fire at all. |
| CAP-17 | Get current brightness (Dimming read-back) — per D-09/AUDIT-03 | `is.workflow.actions.getdevicedetails` (display name "Get Device Details") | `WFDeviceDetail` (enum type `getdevicedetails_wfdevice_detail`) — 1 parameter, tagged `platforms: ["iOS 27 Simulator","macOS 27"]`; enum case list (12 cases, same platform tag) inspected in `toolkit-v78-first-party-enum-cases.json` includes the literal case `Current Brightness` | VERIFIED | Per D-09, this was not concluded before Get Device Details was actually checked. Queried 2026-08-13: `search_ids(["devicedetails","getdevicedetails"])` finds `is.workflow.actions.getdevicedetails` present True/True/True across all three id snapshots, including the iOS-27-Simulator snapshot. `lookup_parameters("is.workflow.actions.getdevicedetails")` returns exactly one parameter, `WFDeviceDetail`, typed `getdevicedetails_wfdevice_detail`, cross-platform tagged. Per this plan's binding instruction, that enum type was then looked up directly: `lookup_enum("getdevicedetails_wfdevice_detail")` against `toolkit-v78-first-party-enum-cases.json` returns a populated 12-case list — `Device Name`, `Device Hostname`, `Device Model`, `Device Is Watch`, `System Version`, `System Build Number`, `Screen Width`, `Screen Height`, `Current Volume`, **`Current Brightness`**, `Current Appearance`, `Device Is Locked` — itself tagged `platforms: ["iOS 27 Simulator","macOS 27"]`. A brightness case **does exist** in this enum, read directly out of a named bundled JSON file, not asserted from external corroboration. This is a genuine, positive divergence from `.planning/research/STACK.md` §3 row 8, `.planning/research/PITFALLS.md` C1, and `.planning/research/ARCHITECTURE.md` §0/§9, all three of which report no brightness-readback evidence anywhere in the Playground bundle and treat Apple's "Get Device Details... now rounds numbers, including the current battery level, volume, and brightness" release-note claim as external-only, UNVERIFIED corroboration — none of those research passes queried `toolkit-v78-first-party-enum-cases.json` for this specific enum type, which the live re-run of the §3 recipe did. That external claim is recorded here for context only; the verdict rests on the local file evidence above, per the binding citation rule, not on the external claim. | n/a for the identifier/parameter shape and the confirmed literal case value (VERIFIED). One residual item this local toolchain cannot settle: the exact numeric format/range Get Device Details returns for `Current Brightness` (e.g. a 0–1 float matching `WFBrightness`'s own input range, versus a 0–100 percentage) is not documented anywhere in this bundle — no prose doc gives a Get Device Details output-format table. Phase 5 (BD-02, CIRC-05) must add a defensive numeric-sanity/coercion check around this read rather than assuming the two actions' numeric ranges match; a read that fails that sanity check is treated identically to a read with no value under the `settings_snapshot` has-any-value guard (`.planning/research/ARCHITECTURE.md` §9). |
| CAP-18 | Set Volume (Silence, Primitive C) — per D-10/AUDIT-04 | `is.workflow.actions.setvolume` | `WFVolumeSetting` (enum type `setvolume_wfvolume_setting`, cases `Media`/`Ringtone`), `WFVolume` (`float`) — both tagged `platforms: ["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. `search_ids(["volume"])` finds `is.workflow.actions.setvolume` present True/True/True across all three id snapshots. `lookup_parameters("is.workflow.actions.setvolume")` returns a 2-parameter record — `WFVolumeSetting` (enum) and `WFVolume` (float) — both cross-platform tagged. `lookup_enum("setvolume_wfvolume_setting")` returns a 2-case list, `Media` and `Ringtone`, also cross-platform tagged. **This is a positive divergence from `.planning/research/STACK.md` §3 row 9**, which reported "No parameter schema for setvolume was found in the v78 catalog... treat the conventional WFVolume-style float parameter as the working assumption pending on-device confirmation" — the live re-run of the parameter-keys catalog finds a confirmed, cross-platform, two-key schema, not merely a plausible-assumption placeholder. `WFVolumeSetting = "Media"` is the literal that scopes the change to media-playback volume rather than the ringer (`Ringtone`). | n/a. Section 21/SAFE-02 constraints, binding on Phase 5's CIRC-03: `WFVolumeSetting` must always be `"Media"`, never `"Ringtone"`; volume is never increased and no startling output is produced — the target `WFVolume` value must never exceed the captured original. See BD-03 for the read-back-gated build form. |
| CAP-19 | Get current volume (Silence read-back) — per D-10/AUDIT-04 | `is.workflow.actions.getdevicedetails` (same action as CAP-17) | `WFDeviceDetail` (enum type `getdevicedetails_wfdevice_detail`, the same 12-case list inspected for CAP-17) includes the literal case `Current Volume` | VERIFIED | Same Get Device Details investigation as CAP-17, recorded with the same discipline, queried 2026-08-13. `lookup_enum("getdevicedetails_wfdevice_detail")` against `toolkit-v78-first-party-enum-cases.json` — the same 12-case list inspected for CAP-17 — includes the literal case **`Current Volume`** (alongside `Current Brightness`), tagged `platforms: ["iOS 27 Simulator","macOS 27"]`. A volume case does exist in this enum, read directly out of the named file. Positive divergence from `.planning/research/STACK.md` §3 row 9, `.planning/research/PITFALLS.md` C2, and `.planning/research/ARCHITECTURE.md` §0/§9 for the same reason as CAP-17 — none queried this enum-cases file for this type. | n/a for the identifier/parameter shape and confirmed literal case value (VERIFIED). Same residual item as CAP-17: the exact numeric format/range of the `Current Volume` reading is not documented anywhere in this bundle and needs the same Phase 5 defensive numeric-sanity check before being fed back into `WFVolume`, under the same `settings_snapshot` has-any-value guard. |
| CAP-26 | Use Model / On-Device model — per D-11/AUDIT-06 | `is.workflow.actions.askllm` (display name "Use Model") | `WFLLMPrompt` (`str`, name "Request"), `WFLLMModel` (typed enum `com_apple_shortcuts_wfask_llmmodel_parameter`, name "Model"), `WFAllowWebSearch` (`bool`, name "Use Broad World Knowledge", trueString `On`/falseString `Off`, OS27-gated per D-01 — omit at iOS 26 target), `FollowUp` (`bool`, name "Follow Up", trueString `On`/falseString `Off`, OS27-gated — omit), `WFGenerativeResultType` (`str`, name "Output") — all five confirmed present, tagged `platforms: ["iOS 27 Simulator","macOS 27"]` at both the top level and per-parameter. Confirms this plan's candidate five-parameter list exactly; no divergence. | VERIFIED | Queried 2026-08-13 via the §3 python3 recipe, re-run live. `search_ids(["askllm","usemodel","llm"])` finds `is.workflow.actions.askllm` present True/True/True across all three id snapshots, including the iOS-27-Simulator snapshot — direct iOS confirmation, not merely a generic-snapshot presence. `lookup_parameters("is.workflow.actions.askllm")` returns the 5-parameter record recorded in the Parameter shape cell, `pythonName: "com_apple_shortcuts_use_model"`, `toolType: "action"`. The action's own identifier and parameter shape are therefore fully evidenced — this row's Verdict covers the action, not the model-source literal (recorded separately below per this plan's binding instruction). **On-Device literal recovery — three attempts, in order, per this plan's binding instruction:** (1) **Enum-type lookup**: `WFLLMModel`'s `typePythonName` is `com_apple_shortcuts_wfask_llmmodel_parameter`; queried as a key (lowercased) against `toolkit-v78-first-party-enum-cases.json`'s `types` object — **absent**, no matching key found. A superficially similar key, `com_apple_generativeassistanttools_generative_assistant_extension_llmpartner` (2 cases: `chatGPT`/`other`, display name "LLM Partner", `platforms: ["macOS 27"]` only), does exist in that same file, but it belongs to a different tool (`com.apple.generativeassistanttools.GenerativeAssistantExtension`), not to `is.workflow.actions.askllm` — it is recorded here explicitly to show it was checked and rejected as unrelated, not silently missed. The enum cases for the picker `WFLLMModel` actually uses are not present in this bundled snapshot at all — this is the finding, not a lookup failure. (2) **Golden shortcut corpus search**: `grep -rl "WFLLMModel"` and `grep -rl "askllm"` across all 19 XMLs under `skills/shortcuts-playground/golden-shortcuts/xml/` — zero matches for either string in any file. No real-world shortcut in the corpus uses the Use Model action at all, so no real-world literal value is available from this source. (3) **Reference-doc search**: `EXAMPLES.md` contains two worked `Use Model` examples (lines ~326-337 "Example 3: AI Query", and ~620-631 inside a larger master example) — both set `<key>WFLLMModel</key><string>Apple Intelligence</string>` verbatim, identically. `SKILL.md` line 163 and `VARIABLES.md` line 467 reference the action/parameter but record no model-source literal. Per this plan's binding instruction and `.planning/research/STACK.md` §3 row 15's own finding, the observed string `Apple Intelligence` predates the iOS 26 three-way model picker (On-Device / Private Cloud Compute / Extension Model) described by external corroboration (MacStories/TechCrunch/AppleInsider reporting, cited in STACK.md §3 row 15 as MEDIUM-confidence external-only evidence) and **is explicitly recorded here as not being the answer** — it is not the On-Device case value and must not be treated as one. **Literal status as at 2026-08-13, from the bundle alone: `UNRECOVERED-LOCALLY`** (superseded — see the next sentence; retained because it remains an accurate statement about what the bundle contains, and it is why a device export was needed). Per D-11 and D-07, that was the correct recorded outcome given the bundle evidence above — no candidate enum string for the On-Device case was written anywhere in this document. **Literal status now: `ROUND-TRIP-CONFIRMED` — `WFLLMModel` = `Apple Intelligence on Device`** (exact string, verbatim). Evidence: `docs/device-evidence/UseModel-OnDevice.xml` line 17, a plist recovered from a shortcut built and exported on the owner's own iPhone (iOS 26) with On-Device selected manually in the Model picker; recorded in §11 of this document and committed in `013a217`. This is tier-1 device evidence and outranks every bundle inference above it. The literal is already hardcoded at `tools/build_sentient.py:29`. Nothing here was guessed: the three bundle attempts genuinely came up empty, and the value came from the device, exactly as UA-02 required. | n/a for the action identifier/parameter shape (VERIFIED). For the model-source literal: `ROUND-TRIP-CONFIRMED` as of 2026-08-13 — see §11, DEV-03 below (closed), UA-02 in §6 (closed), and BD-04-R2 in `docs/CAPABILITY-DECISIONS.md`. **One item remains open and is not closed by the literal:** the literal proves what the *file* asks for, not what the *runtime* does. Confirming on device that `Use Model` actually runs with no network available — so it cannot silently fall back to Private Cloud Compute — is still outstanding and needs an Apple-Intelligence-capable iPhone (15 Pro or later). Until that passes, no user-facing copy may claim the on-device guarantee is verified. |
| CAP-27 | Model structured output (ALLOW/CHALLENGE/DENY parsing) — per AUDIT-06 | `is.workflow.actions.askllm` (same action as CAP-26), parameter `WFGenerativeResultType` | `WFGenerativeResultType` (`typePythonName: "str"`, name "Output") — a bare string parameter, not itself a named enum type, tagged `platforms: ["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. `lookup_parameters("is.workflow.actions.askllm")` (same query as CAP-26) confirms `WFGenerativeResultType` is typed `str`, not an enum — so, unlike `WFLLMModel`, there is no enum type name to look up in `toolkit-v78-first-party-enum-cases.json` for this parameter; its absence from that file is expected given its type, not a gap. Observed literal value: `EXAMPLES.md`'s two worked `Use Model` examples (same locations as CAP-26) both set `<key>WFGenerativeResultType</key><string>Text</string>` verbatim, identically — confirming the research base's reported literal. Searched `EXAMPLES.md`, `VARIABLES.md`, `ACTIONS.md`, `SKILL.md`, `APPINTENTS.md` for any `JSON`-adjacent mention tied to `askllm`/`WFGenerativeResultType`/"generative" — no JSON or other structured-output literal value is evidenced anywhere in this bundle; the only observed value for this parameter, in either worked example, is `Text`. | Per PITFALLS C9, binding on Phase 8's contract-auditor parse (SENT-04): the ALLOW/CHALLENGE/DENY parse of the model's free-form `Text` output must be a tolerant contains-check on the expected keyword, never exact string equality; anything unrecognised defaults to `ALLOW`, never a silent `DENY` or crash; and a parse failure must never itself function as punishment — always fall through to the deterministic Dumb-equivalent Circle behaviour on parse failure. |
| CAP-29 | Comment (section header / documentation marker, no runtime effect) | `is.workflow.actions.comment` | `WFCommentActionText` (`str`) — platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13 via the §3 python3 lookup recipe against all three id snapshots. Present True/True/True in `toolkit-v63-tool-ids.json`, `toolkit-v78-tool-ids.json`, and `toolkit-v78-ios27-tool-ids.json`. `lookup_parameters("is.workflow.actions.comment")` against `toolkit-v78-first-party-parameter-keys.json` returns the single-parameter record above, cross-platform iOS27Sim+macOS27. | n/a. |
| CAP-30 | Nothing (well-formed no-op action, used to keep a control-flow branch non-empty) | `is.workflow.actions.nothing` | Zero parameters (confirmed: empty `parameters` array) — platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters("is.workflow.actions.nothing")` confirms a zero-parameter record, cross-platform iOS27Sim+macOS27. | n/a. |
| CAP-31 | Count (item/character/word/line count of a list or piece of text) | `is.workflow.actions.count` | `WFCountType` (enum type `count_wfcount_type`), `Input` (content item) — both platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters("is.workflow.actions.count")` returns the 2-parameter record above. `SKILL.md` rule 30 additionally documents that the editor UI expects both `WFInput` and `Input` set to the same variable for the selected-list chip to render, though only `Input` appears in the OS27 parameter catalog. | n/a. |
| CAP-32 | Create Folder (fixed-path folder creation) | `is.workflow.actions.file.createfolder` | `WFFilePath` (`str`), `WFFolder` (`File`) — both platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters("is.workflow.actions.file.createfolder")` returns the 2-parameter record above, cross-platform iOS27Sim+macOS27. | n/a. |
| CAP-33 | Trim Whitespace | `is.workflow.actions.text.trimwhitespace` | `WFInput` (`str`) — platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters("is.workflow.actions.text.trimwhitespace")` returns the single-parameter record above, cross-platform iOS27Sim+macOS27. | n/a. |
| CAP-34 | Change Case | `is.workflow.actions.text.changecase` | `text` (`str` — the lowercase key, not `WFInput`; SKILL.md rule 47 names this exact gotcha: "Change Case and Split Text use `text`"), `WFCaseType` (enum type `com_apple_shortcuts_change_case_type`), `ShowWhenRun` (`bool`, On/Off) — all platforms `["iOS 27 Simulator","macOS 27"]` | VERIFIED | Queried 2026-08-13. Present True/True/True across all three id snapshots. `lookup_parameters("is.workflow.actions.text.changecase")` returns the 3-parameter record above, confirming the lowercase `text` input key rather than `WFInput`. | n/a. |

### Confirmation-prompt risk

Per PITFALLS C6: certain actions can force an "Ask Before Running" confirmation prompt the first time they run inside an automation, even when the automation itself is configured to run without confirmation — this is a per-action property, not a blanket guarantee for the whole shortcut. This has not been, and cannot be, resolved by this local ToolKit lookup: none of the bundled JSON snapshots or prose docs expose which specific actions trigger the OS-level confirmation prompt, and the Playground's own validator has zero visibility into runtime confirmation behavior (it checks plist structure only, per `TOOLKIT_SNAPSHOT.md`). On the OPEN fast path, the actions most likely to trigger this per PITFALLS C6/C10 are: any first-touch Notes action (Create Note / Append to Note / Find Notes — first Notes access must happen during the guided manual bootstrap flow per PITFALLS C10, never the first automated OPEN); Get Current App (CAP-01) invoked from within an automatically-triggered context rather than a manual run; and any environmental system-setting action (Set Brightness/Set Volume/Lock Screen — CAP-22) the first time it executes inside an automation. This is not assigned a verdict — it is not a capability question the local toolchain can settle, it is a runtime behaviour. Phase 2 must test the full OPEN handler end-to-end from a real backgrounded automation trigger (not a manual foreground run) and watch for any confirmation prompt, per PITFALLS C6's own prevention guidance, before the OPEN handler is considered functional.

## 5. Deviation log

Numbered entries `DEV-01`, `DEV-02`, ... Each entry carries exactly five labelled fields: `Capability`, `Wanted`, `Verified`, `Substituted`, `Runnability`.

### DEV-01 — WITHDRAWN

> **Withdrawn by BD-01-R, corrected by BD-01-R2** (`docs/CAPABILITY-DECISIONS.md`). CAP-20 is
> now **VERIFIED**: Color Filters exists on iOS 26 as
> `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`, confirmed by
> decrypting the donor `.planning/debug/Set Colour Filters.shortcut`
> (`.planning/spikes/005-ios-color-filters-identifier/`). Ash needs no deviation. The original
> entry is retained below unedited as the historical record of the catalog-only verdict.

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

### DEV-03

- **Capability:** CAP-26 — Use Model / On-Device model, specifically the `WFLLMModel` model-source selection literal (canonical strategy §14, D-03, D-11).
- **Wanted:** The exact plist enum string that pins the `Use Model` action's Model picker to On-Device, so the Sentient fork's `askllm` calls can be hardcoded to never select Private Cloud Compute or the ChatGPT/Extension Model.
- **Verified:** The action itself (`is.workflow.actions.askllm`) and all five of its parameters, including `WFLLMModel`'s key and typed-enum name (`com_apple_shortcuts_wfask_llmmodel_parameter`), are fully evidenced and `VERIFIED` (CAP-26). The enum's case list is not present under that type name, or any name, in `toolkit-v78-first-party-enum-cases.json`; no golden shortcut in the 19-file corpus uses the action at all; the only literal value observed anywhere in the reference docs is the string `"Apple Intelligence"` (`EXAMPLES.md`, two occurrences), which predates the iOS 26 three-way model picker and is not evidence of the On-Device case value.
- **Substituted:** Per BD-04 in `docs/CAPABILITY-DECISIONS.md`, the model-source literal is recorded as `UNRECOVERED-LOCALLY` rather than guessed. The exit path is UA-02 in §6 below — a human on-device round-trip (select On-Device in Shortcuts.app's Model picker, export unsigned XML, read `WFLLMModel` back verbatim) gated on Phase 8. No candidate enum string is written into this document or into `docs/CAPABILITY-DECISIONS.md`.
- **Runnability:** No Dumb-fork path and no deterministic Circle depends on this literal — the Dumb fork has no `Use Model` dependency at all (DUMB-01), and every Sentient-fork model call has a deterministic fallback (SENT-05) — so the Shortcut, and the entire Dumb fork, remain fully runnable. Only the Sentient fork's On-Device *guarantee* is affected, and BD-04 gates that guarantee explicitly rather than assuming it.
- **CLOSED — 2026-08-13 (recorded 2026-08-17).** The deviation is withdrawn: the literal was recovered by device round-trip and is `WFLLMModel` = `Apple Intelligence on Device`. Evidence: `docs/device-evidence/UseModel-OnDevice.xml` line 17, §11 of this document, commit `013a217`. The substitution described above (record `UNRECOVERED-LOCALLY` rather than guess) is no longer in force — the Sentient fork writes the confirmed literal, hardcoded at `tools/build_sentient.py:29`. The three bundle-recovery attempts recorded in CAP-26 stand as written; they were accurate about the bundle and are why a device export was needed. See BD-04-R2 in `docs/CAPABILITY-DECISIONS.md`. **Not closed by this:** the runtime no-network check (that `Use Model` cannot silently fall back to Private Cloud Compute) is a separate, still-open item requiring an Apple-Intelligence-capable iPhone — it is tracked in UA-02's closure note in §6 and is the single remaining open item on this capability.

### DEV-04

- **Capability:** §3's evidence protocol — the recorded validator invocation.
- **Wanted:** A single, correct validator invocation for every Phase 2+ authoring gate, matching the one already recorded in §3 (`validate-shortcut <file.xml> --target-macos 26 --target-platform ios`) so later plans could copy it verbatim without re-deriving it.
- **Verified:** Plan 02-01 re-ran the recorded invocation against a freshly-authored, otherwise-plausible shortcut and it failed with 118 spurious `requires macOS 27+` errors on long-standing, VERIFIED actions. Root-caused by reading `load_packaged_toolkit_ids` in `skills/shortcuts-playground/scripts/validate_shortcut.py` (re-confirmed directly against the installed plugin copy, not merely cited secondhand): it filters the bundled ToolKit snapshots by two independent gates — `_toolkit_snapshot_min_macos_major` (a minimum target-macOS-major check) and `_snapshot_matches_target_platform` (a platform-label check). `toolkit-v63-tool-ids.json` — the generic, non-platform-segmented snapshot that most of this project's long-standing, pre-OS27 actions are evidenced against in §4 — carries a `macOS` platform label internally, so `--target-platform ios` excludes it entirely. `toolkit-v78-ios27-tool-ids.json` — the one genuinely iOS-labelled snapshot — is itself excluded by `--target-macos 26`, since it is a ToolKit v78/iOS 27 capture. The two flags together therefore admit **no snapshot at all**, leaving only the validator's hardcoded control-flow and HealthKit exception sets to validate against — which is why nearly every ordinary action reads as unavailable. Measured, same file, same validator, only the platform flag differing: `--target-macos 26 --target-platform ios` → 118 `requires macOS 27+` errors; `--target-macos 26 --target-platform all` → 0; `--target-macos 26 --target-platform macos` → 0. (Full derivation and the SKELETON.md §4 table this summarises: `.planning/phases/02-routing-bootstrap-control-room/SKELETON.md` §4.)
- **Substituted:** The operative invocation for every Phase 2+ authoring gate is `validate-shortcut <file.xml> --target-macos 26 --target-platform all`. `--target-macos 26` is unchanged from §3 and remains load-bearing for the reason §3 originally recorded it: it is what keeps the OS27 first-party parameter catalog — and its OS27-gated keys — out of the allowlist at this project's actual iOS 26.x target (D-01). Only the platform flag changes, from `ios` to `all`.
- **Runnability:** This is a build-tooling correction, not a product-behaviour change — no action, parameter, or state-document field is affected. Every plan from 02-01 onward runs the corrected invocation directly; §3's original text is left in place per this document's append-only rule, and this entry supersedes it for invocation purposes.
- **Amended 2026-08-17 (quick task `260817-ewg`).** The measurement above stands entirely — the 118-error result, the `load_packaged_toolkit_ids` two-gate root cause, and the substituted invocation, which is now **gate A** and unchanged. What is amended is the same generalisation amended in §13 DEV-01: the controlling variable is `--target-macos`, not `--target-platform`. DEV-04's own final sentence — "Only the platform flag changes, from `ios` to `all`" — is why the second, catalog-loading gate went unnoticed for so long: at target 26 no platform setting loads the parameter-key or enum-case catalogs, so no amount of platform-flag tuning could have surfaced them. **Gate B** (`--target-macos 27 --target-platform all`) is adopted as advisory. See §13 DEV-01's amendment and §22.

## 6. User action items

_Owner: appended to by plans 01-04 and 01-05. Entries are numbered `UA-01`, `UA-02`, ... each with the labelled fields `What`, `Why only a human can do it`, `Exact steps`, `What to record on completion`, `Which phase is gated`._

### UA-01

- **What:** On-device first-use confirmation of the four Notes actions the Control Room depends on (CAP-07 Find Notes, CAP-08 Create Note, CAP-09 Append to Note, CAP-10 Open Note), performed on a real iPhone running iOS 26.x during the manual Control Room bootstrap run described in canonical strategy §18.
- **Why only a human can do it:** This local ToolKit lookup can confirm an identifier's presence and its documented parameter shape, but it cannot execute a Shortcut — it has no visibility into runtime-only failures (PITFALLS A9), the first-use Notes permission prompt (PITFALLS C10), or whether a given action is genuinely reachable on a real device rather than merely present in a bundled snapshot. Only a human tapping through the actual bootstrap flow on real hardware can observe these.
- **Exact steps:** During the deliberate, manually-initiated first-run bootstrap (never inside an automatically-triggered OPEN or CLOSE, where a permission prompt could appear at a moment the user will not see, per PITFALLS C10): (1) run the action built on CAP-08 (Create Note, using `com.apple.Notes.CreateNoteFromMarkdownLinkAction` with the `markdownContents` key) and confirm both that no unexpected permission-prompt stall occurs and that the resulting Control Room Note actually contains its body text — an empty note body is the specific, validator-invisible failure mode this action is known to risk; (2) separately run the action built on CAP-09 (Append to Note) at least once and confirm it does not trigger its own distinct first-use permission prompt outside the bootstrap flow; (3) separately run the action built on CAP-10 (Open Note) from the manual menu and confirm it opens the correct note without a permission stall; (4) separately run the action built on CAP-07 (Find Notes) — used by Sync My Profile — and confirm it locates the Control Room Note without a permission stall. Each of the four actions gets its own first invocation inside this one guided run; none may have its first invocation deferred to a later automated OPEN/CLOSE. **Extended by plan 02-02 (Task 2), as the acceptance evidence for BOOT-04:** within step (1), specifically confirm all four of the following once the one manual bootstrap run completes — the Control Room Note exists (a Note titled `PROSOCHĒ — Control Room` is present in the Notes app); its on-device title matches, character for character, the exact string plan 02-04's `Find Notes` action is given to search for (UA-03 separately tracks what that title mechanically resolves to if it diverges from the authored string); its body is populated with the full Note text plan 02-02 authored, not empty; and the `#`/`##`/`###` markdown headings in that body render as actual Notes-app headings rather than as literal hash characters on screen.
- **What to record on completion:** For each of the four actions — whether it ran without error, whether any permission prompt appeared and was granted, and (for CAP-08 specifically) whether the Note body was populated with the expected setup text rather than empty. **Extended by plan 02-02 (Task 2):** for CAP-08 specifically, record all four Phase 2 observations as the acceptance evidence for BOOT-04 — (a) the Note exists, (b) its on-device title matches the authored string exactly, (c) its body is non-empty and matches the authored content, and (d) its markdown headings render as headings, not literal hash characters.
- **Which phase is gated:** Phase 2.
- **Fallback trigger (BD-05), added by plan 02-02 (Task 2):** if any of the four observations above comes back negative — most importantly, if the Note is created but its body reads empty, or if any of the four Notes actions fails or stalls on a permission prompt during this guided bootstrap run — that is the exact signal BD-05 names to fall back to the file-based Control Room. What changes: the same `Control Room Body` text is written through the already-audited Save File path (CAP-03) to a file (e.g. `PROSOCHE/control-room.md`) instead of to a Note, and presented via an audited display action instead of `Show Note`/`Find Notes`. Adopting the fallback costs the losses BD-05 already enumerates — Save File has no selective-append mode, so the ATTENTION LEDGER would move from one Append action to a full read-modify-write cycle per event, and Sync My Profile would re-parse the whole file via Detect Text on every sync instead of a scoped Find/Append. Recorded here so a future executor who hits this failure has the decision already made rather than making one under pressure.
- **Extended by plan 02-04 (Task 3), as the on-device half of BOOT-05 and BOOT-08:** once Phase 7 signs and imports this fork, record two further outcomes against this same item, both on the same guided bootstrap run this item already covers: (e) tap the Shortcut a second time and confirm no duplicate Control Room Note appears and `state.json` is unchanged — this is the same on-device observation UA-04 already names for the state file's own side of BOOT-05, so record it once and cross-reference it here rather than re-describing it; (f) delete the Control Room Note from the Notes app, then tap the Shortcut once more, and confirm the Note comes back with its full body — the same body plan 02-02 authored, not a lesser placeholder — because plan 02-04's Note-existence guard (`Find Notes` → `Note Present` → reuse-or-create) is structurally proven from the plist (the IDEMPOTENCE-OK check in `02-04-SUMMARY.md`) but whether a real device actually re-creates the Note correctly after a genuine deletion is exactly the class of runtime-only fact this item exists to close. Observation (f) is a new fact no earlier UA item names; observation (e) is recorded here only as a cross-reference so BOOT-05's two stores (state file, Note) are both traceable from one place without duplicating UA-04's own wording.

### UA-02

- **What:** Recover the `Use Model` action's On-Device selection literal (the `WFLLMModel` plist value) by a manual on-device round-trip, per D-11/AUDIT-06/BD-04, since three independent recovery attempts against the local ToolKit snapshots (CAP-26 in §4) found no enum case list for this parameter anywhere in the bundle.
- **Why only a human can do it:** The enum cases for `WFLLMModel`'s picker are absent from every bundled ToolKit snapshot this local toolchain has access to (`toolkit-v78-first-party-enum-cases.json` has no matching type key, under this name or any other), and no golden-shortcut example or reference doc records a post-iOS-26 literal. A signed `.shortcut` file is an AEA1-encrypted archive and cannot be read back as plaintext, so even a manually-configured shortcut cannot be inspected without first exporting it unsigned. There is no programmatic path to this value from the build machine — only a real Apple-Intelligence-capable device running the actual Model picker UI can produce it.
- **Exact steps:** On an Apple-Intelligence-capable iPhone (iPhone 15 Pro or later) running iOS 26 or later: (1) in Shortcuts.app, add a `Use Model` action to any shortcut (a new throwaway shortcut is fine — this does not need to be a PROSOCHĒ shortcut); (2) tap the action's Model field to open its Model picker; (3) select **On-Device**; (4) save the shortcut; (5) open the shortcut's details, tap Share, then tap Copy; (6) paste the copied content into a plain `.xml` file (this is the unsigned plist export — do not attempt this via a signed `.shortcut` file, which cannot be read back as plaintext).
- **What to record on completion:** Open the resulting `.xml` file and locate the `Use Model` action's `WFWorkflowActionParameters` dictionary; read the string value under the `WFLLMModel` key and record it verbatim in `docs/BUILD-NOTES.md`'s CAP-26 row, replacing the `UNRECOVERED-LOCALLY` token with `ROUND-TRIP-CONFIRMED` and the recovered literal. Then update `docs/CAPABILITY-DECISIONS.md`'s BD-04 record to note that Branch A was subsequently reached, citing this UA-02 completion as the evidence.
- **Which phase is gated:** Phase 8 only. This does not block Phase 1's completion, does not block Phases 2 through 7, and the Dumb fork — which has no Apple Intelligence dependency at all (DUMB-01) — ships completely without it. Phase 8 itself is not fully blocked either: per BD-04, everything except the literal's hardcoding and the "On-Device is enforced" claim can be built before UA-02 is complete.
- **CLOSED — completed 2026-08-13 by the project owner; audit trail reconciled 2026-08-17.**
  - **What was recovered, verbatim:** `WFLLMModel` = `Apple Intelligence on Device`, alongside `WFWorkflowActionIdentifier` = `is.workflow.actions.askllm`.
  - **How:** a shortcut containing a single `Use Model` action was built on the owner's iPhone (iOS 26) with **On-Device** selected manually in the Model picker, then exported and recovered here. The route taken differed from the "Exact steps" above in one respect worth recording: the export was a **signed `.shortcut`**, recovered by `aea decrypt` + `aa extract` (procedure in §11). This **falsifies the "Why only a human can do it" claim above** that a signed `.shortcut` "cannot be read back as plaintext" — it can, without the private key, because the archive is signed rather than encrypted. That sentence is left in place as the record of what was believed at the time; §11 is the correction. The human step that genuinely could not be automated was the picker selection on an Apple-Intelligence-capable device, and that part of the reasoning holds.
  - **Recorded at:** `docs/device-evidence/UseModel-OnDevice.xml`, §11 of this document, commit `013a217`. Consumed at `tools/build_sentient.py:29`. CAP-26's token is now `ROUND-TRIP-CONFIRMED`; DEV-03 is withdrawn; BD-04-R2 in `docs/CAPABILITY-DECISIONS.md` records that Branch A was reached.
  - **THE ONE REMAINING OPEN ITEM — the runtime no-network check.** The recovered literal proves what the shipped *file* asks for. It does **not** prove what the *runtime* does. Nobody has yet confirmed on device that the `Use Model` action actually runs with **no network available** — i.e. that it cannot silently fall back to Private Cloud Compute despite the On-Device literal. This requires an Apple-Intelligence-capable iPhone (iPhone 15 Pro or later): run a Sentient model call with Wi-Fi and cellular both off, and confirm the action completes rather than erroring or routing out. **Until that passes, the user-facing on-device guarantee copy — README, the Control Room Note, any release text — stays exactly as D-06/DIST-07 required, unchanged.** A literal that validates but silently falls back to PCC would be worse than making no claim at all. This is *not* to be described as verified.

### UA-03

- **What:** On-device confirmation of the Control Room Note's title, extending UA-01 rather than duplicating it. UA-01 already covers whether `com.apple.Notes.CreateNoteFromMarkdownLinkAction`'s body is populated; this item covers the separate question of what the created note is actually *named*. Plan 02-01 writes the note's first markdown line as `# PROSOCHĒ — Control Room` on the theory that this action has no confirmed title/name parameter of its own and Notes derives the visible title from the first line. As a defensive measure — because a structural check treats every Notes-create action alike and expects some name-shaped parameter to be present — the action also carries a `name` parameter set to the identical string, even though no evidence in this bundle confirms `CreateNoteFromMarkdownLinkAction` reads it.
- **Why only a human can do it:** Whether the note's on-device title comes from the first markdown line, from the `name` parameter, or from neither, is exactly the class of runtime-only fact PITFALLS A9 describes — the plist validates cleanly under any of the three outcomes and only an on-device import can distinguish them.
- **Exact steps:** During the same guided manual bootstrap run as UA-01: after the Control Room Note is created, open Notes.app directly (not through the shortcut) and read the note's title as Notes.app displays it in the notes list. Separately, note whether the title carries the em dash and macron exactly as authored (`PROSOCHĒ — Control Room`) or whether either character was altered/dropped.
- **What to record on completion:** The exact on-device title string observed, and whether it matches `PROSOCHĒ — Control Room` byte-for-byte. If it does not match, record the actual title so plan 02-04's `Find Notes` lookup (BOOT-04) can be pointed at the real string rather than the assumed one.
- **Which phase is gated:** Phase 2, specifically plan 02-04's Note-existence guard, which must search for whatever title the note actually carries.

### UA-04

- **What:** On-device confirmation that the bootstrap write actually lands at the fixed path. Plan 02-01 creates a folder named `PROSOCHE` via `is.workflow.actions.file.createfolder` with only a bare `WFFilePath`, then separately reads via `is.workflow.actions.documentpicker.open` with `WFGetFilePath = "PROSOCHE/state.json"` and writes via `is.workflow.actions.documentpicker.save` with `WFFileDestinationPath = "PROSOCHE/state.json"` — three actions that must all resolve the same relative path against the same implicit root for the read-after-write cycle to work at all.
- **Why only a human can do it:** None of `WFFilePath`, `WFGetFilePath`, or `WFFileDestinationPath` carry any documented base-folder semantics in this bundle (no `WFFolder` value is set on any of the three actions, so each relies on whatever default root Shortcuts substitutes) — this is exactly the kind of implicit, undocumented default PITFALLS A9 warns validates cleanly and can only be confirmed by watching the actual file appear (or fail to appear) in the Files app / Shortcuts folder on a real device.
- **Exact steps:** During the guided manual bootstrap run: after the run completes, open the Files app, navigate to the Shortcuts folder in iCloud Drive, and confirm a `PROSOCHE` folder exists there containing a `state.json` file. Re-run the shortcut manually a second time and confirm the bootstrap branch is *not* re-entered (no duplicate write, no duplicate Note) — this is the direct on-device test of BOOT-05.
- **What to record on completion:** Whether the folder and file appear at the expected Files-app location, and whether a second manual run correctly takes the "existing setup" branch instead of re-bootstrapping.
- **Which phase is gated:** Phase 2, specifically plan 02-04's load-and-do-not-overwrite path, which is only meaningful if bootstrap itself is confirmed to write to a stable, re-readable location.

### UA-05

- **What:** On-device confirmation that the two pinned import questions actually appear during import and that typed (or default) answers reach `Import Descent`/`Import Voice` and, from there, into the written `state.json`.
- **Why only a human can do it:** STACK.md §7 and this document's §3 both record that `scripts/validate_shortcut.py` has zero references to `WFWorkflowImportQuestions` — the validator cannot execute an import, so a question bound to the wrong `ActionIndex`, or a question that silently fails to prompt, is invisible to every automated check this project has.
- **Exact steps:** Import the unsigned XML (after signing, per the Phase 7/8 signing step) on a real device and confirm both prompts appear in order, with the documented default values (`Limbo`, `yes`) pre-filled; answer at least one run with non-default values (e.g. `Paradise`, `no`); complete the guided manual bootstrap run; then open the written `state.json` (via the Files app) and confirm `profile` and `voice_enabled` hold exactly the typed answers.
- **What to record on completion:** Whether both prompts appeared, whether the pre-filled defaults matched, and whether the typed answers round-tripped into the written file unchanged.
- **Which phase is gated:** Phase 2. This is the on-device half of BOOT-09; plan 02-04's normalisation step (mapping an unrecognised descent answer to `Limbo`, mapping the voice answer to a real JSON boolean) is only meaningful once the raw answers are confirmed to actually arrive.

### UA-06

- **What:** Resolve, on-device, which of two conflicting documented behaviours governs `is.workflow.actions.format.date`'s custom-pattern field: `BEST_PRACTICES.md` and `SKILL.md` (both "Mandatory") say to set `WFDateFormatStyle=Custom`, `WFDateFormat=Custom`, and put the actual pattern in `WFDateFormatString`; a `CHANGELOG.md` debugging entry ("WFDateFormat vs WFDateFormatString," dated earlier) instead reports that the runtime reads `WFDateFormat` for the pattern and ignores `WFDateFormatString`, recommending both keys be set to the identical pattern string. Plan 02-01 follows the two "Mandatory" documents (`WFDateFormat="Custom"`, pattern in `WFDateFormatString`) as the more current, converged, explicitly-prioritised source, per this project's own "BEST_PRACTICES.md wins on conflict" rule — but this is a plist-valid choice either way, so the two behaviours cannot be distinguished without running the action.
- **Why only a human can do it:** Both interpretations produce a structurally valid, validator-passing plist; the difference is purely in which key the Shortcuts runtime actually reads, which is not observable without executing the action on-device (PITFALLS A9's class of failure).
- **Exact steps:** During the guided manual bootstrap run, after `state.json` is written, read the `behavioural_day` field back (via the Files app or a throwaway "Get File → Detect Dictionary → Get Dictionary Value" test shortcut) and confirm it holds a real `yyyy-MM-dd`-shaped date string rather than a raw/default-formatted date or the literal text `Custom`.
- **What to record on completion:** The actual value observed. If it is not a `yyyy-MM-dd` string, update the `format.date` action to also set `WFDateFormat` to the literal pattern (mirroring `WFDateFormatString`) and record that correction as a new deviation entry.
- **Which phase is gated:** Phase 2. `behavioural_day` is read by every later phase's day-rollover comparison (D-17), so this must be confirmed before Phase 3 builds Heat/Gravity logic on top of it.

### UA-07

- **What:** On-device confirmation of two routing-normalisation facts introduced by plan 02-03's `Input Key` chain: (1) whether a Personal Automation's `Run Shortcut` input (`OPEN`/`CLOSE`) ever arrives with leading/trailing whitespace in practice, and (2) whether a genuinely absent Shortcut Input (a plain manual tap) composes cleanly through the `ExtensionInput` token attachment inside a `Text` action into an empty string, rather than raising a runtime error before the trim/uppercase chain ever runs.
- **Why only a human can do it:** The local ToolKit lookup and the plist validator can confirm that `is.workflow.actions.text.trimwhitespace`/`is.workflow.actions.text.changecase` are real, evidenced actions with the documented parameter shapes (CAP-33, CAP-34) and that the resulting plist is structurally valid, but neither can execute the Shortcut. Whether a real Personal Automation ever hands `Run Shortcut` literal input text with incidental surrounding whitespace, and whether Shortcuts' own runtime coerces a truly-absent `ExtensionInput` into an empty string inside a `Text` action rather than erroring, are both PITFALLS A9-class runtime-only facts. The trim step is defensive regardless of the answer to (1); confirming it tells a future maintainer whether that defensiveness is load-bearing or precautionary. The answer to (2) is the one this plan's entire empty-input-reaches-MANUAL argument rests on.
- **Exact steps:** During the same guided manual bootstrap run as UA-01/UA-04/UA-05: (1) run the Shortcut with a plain manual tap (no input at all) and confirm it reaches the Control Room without any error dialog or stall — this is the direct on-device test that an absent `ExtensionInput` composes as an empty string rather than raising; (2) once Automation A and Automation B exist (built per the Control Room Note, after Phases 3/4 fill the OPEN/CLOSE branches), open each automation's Run Shortcut action in the Shortcuts app editor and visually inspect its configured input text field for stray leading/trailing spaces, since this is observable in the editor without needing to trigger a real run. **Extended by plan 02-03 (Task 3), as the on-device half of the router's four-row decision table** (the structural half is proved in `02-03-SUMMARY.md` by tracing the plist directly, action index by action index, without running anything): (3) confirm the plain manual tap in step (1) above lands specifically in the Control Room (the MANUAL branch), not merely "no error"; (4) once Automation A exists, trigger a real app-open event and confirm the run reaches the OPEN branch silently — no diagnostic alert, no visible detour — since the router's structural proof shows the OPEN branch as inert (Comment + Nothing) in this plan and any user-visible alert on a real OPEN would mean the router misrouted; (5) deliberately mis-configure a throwaway Run Shortcut call (or edit Automation A's input text) to pass a value that is neither `OPEN` nor `CLOSE` and confirm it produces exactly the one diagnostic alert this plan authored and changes nothing observable in `state.json` or the Control Room Note afterward.
- **What to record on completion:** Whether the manual (no-input) run reached the Control Room without error, and whether either automation's configured input text carried incidental whitespace. **Extended by plan 02-03 (Task 3):** whether the manual tap specifically reached the Control Room (not just error-free); whether a real OPEN-triggered run stayed silent (no alert); and whether an unrecognised-input run showed the one expected alert with no observable state change.
- **Which phase is gated:** Phase 2.

### Audit outcome — plan 02-01, task 2

**What was checked:** All five wiring classes named in this task's action — import-question `ActionIndex`/`ParameterKey` binding against the actual target actions; every `OutputUUID` reference against every action `UUID`; every display-facing text parameter (`WFTextActionText`, the Control Room Note's `markdownContents`) for `WFTextTokenString` serialization versus every data-flow parameter for `WFTextTokenAttachment`; both `GroupingIdentifier` blocks for correct mode-0/mode-1/mode-2 sequencing, no interleaving, and no condition fields on a mode-1 action; and every Dictionary Value reaching an `If` condition for an intervening `Text` action — plus a byte-level check that all 11 `attachmentsByRange` entries in the file point at an in-bounds, single-character placeholder. The structural check in this task's `<verify>` block, plus the supplementary hand-checks above, both exit clean against the file plan 02-01 produced.

**What was found:** No wiring defects. Two decisions made during authoring were not fully settled by the available evidence and are recorded as user action items above rather than guessed past: the Control Room Note's actual on-device title (UA-03) and which of two documented `format.date` behaviours is correct at runtime (UA-06, a genuine documentation conflict between two files this project treats as "Mandatory" and one `CHANGELOG.md` entry — resolved in favour of the two converging Mandatory sources, per this project's own conflict-priority rule, but not verifiable without a device).

**What was deferred to §6:** UA-03 (Note title), UA-04 (folder/file creation at the fixed path, and the no-duplicate-bootstrap guarantee), UA-05 (import prompts appearing and round-tripping), and UA-06 (the `format.date` pattern-field ambiguity) — none of these block any build-machine task in this phase; all four require a real device to settle and are gated on Phase 2 as shown.

## 7. Coverage check

_Owner: finalised by plan 01-05._

### A. Capability coverage table

One row per capability named in `.planning/phases/01-capability-audit-config-foundation/01-CONTEXT.md`'s "Capability audit must cover, at minimum (§31)" list — the operative superset of canonical strategy §31's list. All 28 map cleanly to `CAP-01` through `CAP-28`, by construction: this document's CAP numbering was assigned in that exact order across plans 01-01, 01-02, 01-04, and this plan.

| # | Canonical capability | CAP ID | Verdict | Deviation |
|---|---|---|---|---|
| 1 | Get Current App | CAP-01 | VERIFIED | — |
| 2 | Get File | CAP-02 | VERIFIED | — |
| 3 | Save File / overwrite | CAP-03 | VERIFIED | DEV-02 (the related file-existence-check question) |
| 4 | Dictionary and JSON parsing | CAP-04 | VERIFIED | — |
| 5 | Get Dictionary Value | CAP-05 | VERIFIED | — |
| 6 | Date arithmetic | CAP-06 | VERIFIED | — |
| 7 | Notes search/find | CAP-07 | VERIFIED | — (UA-01 tracks on-device confirmation, not a deviation) |
| 8 | Create Note | CAP-08 | VERIFIED | — (UA-01) |
| 9 | Append to Note | CAP-09 | VERIFIED | — (UA-01) |
| 10 | Show/open note | CAP-10 | VERIFIED | — (UA-01) |
| 11 | Ask for Input | CAP-11 | VERIFIED | — |
| 12 | Choose from Menu/List | CAP-12 | VERIFIED | — |
| 13 | Open App | CAP-13 | VERIFIED | — |
| 14 | Open URLs / web search | CAP-14 | VERIFIED | — |
| 15 | Maps search | CAP-15 | VERIFIED | — |
| 16 | Set Brightness | CAP-16 | VERIFIED | — |
| 17 | Get current brightness | CAP-17 | VERIFIED | — |
| 18 | Set Volume | CAP-18 | VERIFIED | — |
| 19 | Get current volume | CAP-19 | VERIFIED | — |
| 20 | Color Filters / grayscale | CAP-20 | VERIFIED (donor-confirmed, iOS `AX*` identifier — BD-01-R2) | DEV-01 withdrawn |
| 21 | Speak Text | CAP-21 | VERIFIED | — |
| 22 | Lock Screen | CAP-22 | VERIFIED | — |
| 23 | Run Shortcut | CAP-23 | VERIFIED | — |
| 24 | Wait | CAP-24 | VERIFIED | — |
| 25 | Base64 if needed | CAP-25 | VERIFIED | — |
| 26 | Use Model / On-Device model | CAP-26 | VERIFIED (action + parameters); On-Device literal `ROUND-TRIP-CONFIRMED` = `Apple Intelligence on Device` (§11, `013a217`) | DEV-03 (closed) |
| 27 | Model structured output | CAP-27 | VERIFIED | — |
| 28 | Get App & Website Data | CAP-28 | VERIFIED | — |

Every ID from `CAP-01` through `CAP-28` is accounted for above — no gap was found, so none needed auditing fresh during this closure pass.

**Supplementary table — architecture-critical actions beyond the canonical §31 list.** These are actions the build depends on that canonical strategy §31 does not separately enumerate (control flow, data plumbing, and display primitives used throughout every Circle and the bootstrap/routing logic), audited by plans 01-01 and 01-02 for completeness because the build cannot function without them even though they fall outside the §31 capability list proper.

| CAP ID | Capability | Verdict | Deviation |
|---|---|---|---|
| CAP-S01 | Set Variable / Get Variable | VERIFIED | — |
| CAP-S02 | Text (Get Text) | VERIFIED | — |
| CAP-S03 | Number and Math | VERIFIED | — |
| CAP-S04 | If / Otherwise / End If | VERIFIED | — |
| CAP-S05 | Repeat with a count | VERIFIED | — |
| CAP-S06 | Get Item from List | VERIFIED | — |
| CAP-S07 | Show Alert / Show Result / Show Notification | VERIFIED | — |
| CAP-S08 | Set Name (rename before Save File) | VERIFIED | — |

### B. Deviation index

Every `DEV-NN` entry recorded in §5, indexed against the requirement it touches and the phase that owns resolving it, so nothing recorded in this document is lost between Phase 1 and the phase that closes it.

| DEV ID | Capability | Requirement touched | Owning phase | How it resolves |
|---|---|---|---|---|
| DEV-01 | CAP-20 — Color Filters / grayscale (Ash, Primitive B) | AUDIT-02 | Phase 5 | BD-01 degrades Ash to a verified, self-contained, non-environmental low-salience visual pause (CIRC-02) — never `UAToggleColorFiltersIntent`, never a read of live accessibility state. Phase 5 builds CIRC-02 exactly as BD-01 specifies; resolved by construction, not by a future capability discovery. |
| DEV-02 | CAP-03 — Save File / the missing file-existence-check action (bootstrap's "does `state.json` already exist" question) | AUDIT-01 | Phase 2 | Phase 2's bootstrap (BOOT-01 through BOOT-04) implements the substitute directly: Get File with `WFFileErrorIfNotFound=Off`, piped through Detect Dictionary, treating a non-dictionary/empty result as "state absent." Resolved by construction; no further capability discovery needed. |
| DEV-03 | CAP-26 — Use Model / the `WFLLMModel` On-Device selection literal | AUDIT-06 | Phase 8 | **CLOSED 2026-08-13 (reconciled 2026-08-17).** UA-02 was the exit path and it completed: the round-trip recovered `WFLLMModel` = `Apple Intelligence on Device` (`docs/device-evidence/UseModel-OnDevice.xml`, §11, commit `013a217`), so CAP-26's token is now `ROUND-TRIP-CONFIRMED` and BD-04 **Branch A** was reached — see BD-04-R2 in `docs/CAPABILITY-DECISIONS.md`. Phase 8 hardcodes the literal (`tools/build_sentient.py:29`). This index now has **no open deviation**. The one item still open on this capability is *not* a deviation: the runtime no-network check (that the action cannot silently fall back to Private Cloud Compute) needs an Apple-Intelligence-capable iPhone, is tracked in UA-02's closure note in §6, and until it passes the user-facing guarantee copy stays as D-06/DIST-07 required. |

### C. Runnability statement

Per AUDIT-07's second clause and D-07 point 4 ("keep the Shortcut runnable"), the following four claims are asserted and checked against the deviation index above:

1. **No OPEN or CLOSE path depends on an action whose verdict is `NOT AVAILABLE`.** As of BD-01-R2 there is **no `NOT AVAILABLE` row left** in this document — CAP-20 is `VERIFIED`. Claim holds a fortiori. *(Original text: the only `NOT AVAILABLE` row was CAP-20; BD-01 degraded Ash to a substitute built from `VERIFIED` display actions, CIRC-02, and nothing on the OPEN or CLOSE path called a Color Filters action or read live accessibility state.)*
2. **Every primitive occupying a slot in a sequence ordering has a defined behaviour under its decision record.** `src/CONFIG-BLOCK.md`'s three `sequences` arrays name nine primitives each (Knock, Ash, Silence, Confession, Dimming, Exile, Mirror, Voice, Ice, plus the combined `Ash+Confession`/`Silence+Mirror`/`Dimming+Mirror` entries in Black Mirror). Ash is defined by BD-01, Silence by BD-03, Dimming by BD-02; the remaining six (Knock, Confession, Exile, Mirror, Voice, Ice) rest on `VERIFIED` actions audited elsewhere in §4 (CAP-S07 display primitives, CAP-11 Ask for Input, CAP-21 Speak Text, CAP-22 Lock Screen and the exit-routing actions in CAP-13/14/15) with no open deviation against any of them. Claim holds.
3. **Circle IX's guaranteed route-out does not depend on any unverified action.** Circle IX (Ice) is deterministic per D-04/SENT-12 — the model never touches it — and its cooldown/eject/redirect mechanics rest on `VERIFIED` actions only (CAP-22 Lock Screen, CAP-24 Wait, the exit-routing actions). It has no dependency on CAP-20 (Ash is not part of Ice's own mechanics) and no dependency on CAP-26 (Use Model plays no role in Circle IX at all, per canonical strategy §14.4's own Circle IX = "No model. Deterministic Ice."). Claim holds.
4. **The Dumb fork has no dependency on any item still open.** Of the two items this document leaves open past Phase 1 — UA-01 (Notes on-device confirmation) and UA-02/DEV-03 (the Use Model literal) — UA-01 is scoped entirely to Phase 2's own guided bootstrap run and closes within that phase's build, not deferred past it; DEV-03/UA-02 is scoped exclusively to the Sentient fork (Phase 8) and DUMB-01 establishes the Dumb fork has zero Apple Intelligence dependency. Neither open item is a dependency of the Dumb fork. Claim holds. **Update 2026-08-13 (reconciled 2026-08-17): DEV-03/UA-02 is closed** — the literal was recovered by device round-trip (§11). The claim holds a fortiori: one fewer item is open, and the item that replaced it (the runtime no-network check) is likewise Sentient-only and likewise not a Dumb-fork dependency.

All four claims hold as stated; no exception needed to be recorded.

### D. Requirement closure table

| Requirement | Where satisfied | Status |
|---|---|---|
| AUDIT-01 | §4 (36 judged CAP rows, `CAP-01`–`CAP-28` plus `CAP-S01`–`CAP-S08`, each with identifier, parameter shape, verdict, evidence) | Complete |
| AUDIT-02 | `docs/CAPABILITY-DECISIONS.md` BD-01 (Ash / Color Filters go/no-go and fallback design) | Complete |
| AUDIT-03 | `docs/CAPABILITY-DECISIONS.md` BD-02 (brightness read-back, Dimming's stateful-with-safety-branch form) | Complete |
| AUDIT-04 | `docs/CAPABILITY-DECISIONS.md` BD-03 (volume read-back, Silence's stateful-with-safety-branch form) | Complete |
| AUDIT-05 | `docs/CAPABILITY-DECISIONS.md` BD-05 (Notes actions authorised for the iOS target, gated on UA-01) | Complete |
| AUDIT-06 | `docs/CAPABILITY-DECISIONS.md` BD-04 — **Branch B taken at Phase 1** (the literal was not recovered locally; the Sentient fork's On-Device guarantee is explicitly re-planned, per the alternative outcome AUDIT-06 itself permits), with UA-02 recorded as the then-open exit path to Branch A. **Update 2026-08-13 (reconciled 2026-08-17): UA-02 completed and Branch A was subsequently reached** — the literal is `Apple Intelligence on Device` (§11, `013a217`, BD-04-R2). AUDIT-06 is therefore now satisfied by its *primary* branch, not only the alternative. | Complete (Branch A, reached after the Phase-1 Branch B record) |
| AUDIT-07 | §5 (deviation log, three `DEV-NN` entries) plus §7.B (deviation index with owning phases) plus §7.C (the runnability statement above) | Complete |
| AUDIT-08 | `src/CONFIG-BLOCK.md` (single fenced JSON block, nine sibling top-level keys, field reference, derived-value rules) | Complete |

### Consistency pass

Checked 2026-08-13 as part of this plan's closure:

- `docs/CAPABILITY-DECISIONS.md` contains all five records `BD-01` through `BD-05`, each with all seven labelled fields (`Question`, `Evidence`, `Options considered`, `Decision`, `Rationale`, `Consequence for later phases`, `Requirement`) and each naming a requirement ID (`AUDIT-02`, `AUDIT-03`, `AUDIT-04`, `AUDIT-06`, `AUDIT-05` respectively). Confirmed by direct read of the file.
- Every Verdict cell in §4 holds exactly one of the four vocabulary values (`VERIFIED`, `VERIFIED (identifier only)`, `UNVERIFIED`, `NOT AVAILABLE`) and nothing else. At the original closure pass the only non-`VERIFIED` row was CAP-20 (`NOT AVAILABLE`) with a matching `DEV-01` entry in §5. **As of BD-01-R2, CAP-20 is `VERIFIED` and DEV-01 is withdrawn — every row in §4 is now `VERIFIED`.**
- `src/CONFIG-BLOCK.md` still contains exactly one fenced `json` block, it parses as valid JSON, and all three `sequences` orderings (`Classic`, `BlackMirror`, `Ambient`) each still hold exactly nine entries — verified by direct parse during this plan's own verification step.
- Cross-reference lines are in place: this document's §1 now points at `src/CONFIG-BLOCK.md` (the config deliverable) and `docs/CAPABILITY-DECISIONS.md` (the decision record); `src/CONFIG-BLOCK.md` carries the matching prose cross-reference back to this document (added by this plan, outside its fenced JSON block).

### Closing subsection — ROADMAP Phase 1 success criteria

Each of the five Phase 1 success criteria in `.planning/ROADMAP.md`, mapped to concrete content in these three files:

1. *"A build-notes document lists every dependent iOS action with VERIFIED/UNVERIFIED/NOT AVAILABLE status and exact identifier/parameter shape, and every deviation forced by an unverifiable action is recorded with the fallback taken while the Shortcut remains runnable."* — Satisfied by §4 (36 judged rows) and §5 (three `DEV-NN` entries), with §7.C's runnability statement confirming the Shortcut remains runnable.
2. *"Grayscale/Color Filters capability has a documented go/no-go decision, with a documented fallback design for the Ash primitive if no safe action exists."* — Satisfied, now on stronger evidence: CAP-20 is `VERIFIED` (donor-confirmed, BD-01-R2) and the go decision is BD-01-R2, with BD-01's non-environmental variant (CIRC-02) retained as the documented fallback for users who opt out via `safety.ash_managed_color_filters`.
3. *"Brightness and volume read-back capability are each resolved; if no safe read path exists, Dimming and Silence are specified to degrade to non-stateful variants rather than making an unrestorable change."* — Satisfied by CAP-16/CAP-17 and BD-02 (Dimming), CAP-18/CAP-19 and BD-03 (Silence); both resolved to the stronger stateful-with-safety-branch form because the read-back path was found `VERIFIED`, which is a stronger outcome than the criterion's own fallback-only framing anticipated — the message-only degrade path is retained as each primitive's mandatory per-run safety branch, not discarded.
4. *"Notes actions (Create Note, Append to Note, find/show a Note) are confirmed usable on the iOS target."* — Satisfied by CAP-07 through CAP-10 (all `VERIFIED`) and BD-05, which authorises Phase 2 to build on this evidence while gating final on-device confirmation on UA-01 — met by the alternative branch AUDIT-05's own evidentiary standard permits (authorise-and-confirm-early, not block-and-wait), stated plainly rather than overstated as a completed on-device test.
5. *"The `Use Model` On-Device selection literal is recovered by round-trip... and recorded verbatim, or the Sentient fork's On-Device guarantee is explicitly re-planned; a single editable Config block... exists in the graph."* — At Phase 1 the literal was **not** recovered (CAP-26, then-token `UNRECOVERED-LOCALLY`); the guarantee was explicitly re-planned by BD-04 Branch B, which AUDIT-06 permits as an equally-satisfying outcome — met by the alternative branch, stated plainly, not overstated as a completed round-trip. **Update 2026-08-13 (reconciled 2026-08-17):** the round-trip was subsequently completed and the literal *is* recovered and recorded verbatim — `WFLLMModel` = `Apple Intelligence on Device` (§11, `docs/device-evidence/UseModel-OnDevice.xml`, `013a217`) — so this criterion is now met by its first clause as well as its second. The separate runtime no-network check remains open (UA-02 closure note, §6) and no user-facing guarantee copy has been changed on the strength of the literal alone. The Config block half of this criterion is satisfied by `src/CONFIG-BLOCK.md` (single fenced JSON block, nine sibling top-level keys, confirmed parsing and intact sequence orderings in this plan's own verification step).

---

### Phase 2 requirement closure (plan 02-04)

_Owner: finalised by plan 02-04, task 3 — the same closure discipline established for Phase 1 above, applied now that all four of Phase 2's plans are complete. `src/PROSOCHE-Dumb.xml` stands at 133 actions, 13 control-flow blocks, 34 comments, re-audited end to end by this task._

#### E. Phase 2 requirement closure table

| Requirement | Where satisfied | Status |
|---|---|---|
| BOOT-01 | The nested `If`/`Otherwise` router (`F646324A`/`FA045F2B`/`A2F7247B` blocks), built by 02-01/02-03 and structurally unchanged by this plan; this plan's own phase-closure audit re-confirms zero `Otherwise If` anywhere in the finished 133-action file and every control-flow block balanced | Complete |
| BOOT-02 | The fail-safe branch (`is.workflow.actions.alert` behind `A2F7247B`'s innermost otherwise), audited inert by 02-03 task 2 and untouched by this plan | Complete |
| BOOT-03 | The bootstrap otherwise-branch of the (repurposed) `6D32F6F2` gate — `Create Folder`, the `Default State JSON` template now interpolating `Descent Normalised`/`Voice Normalised` in place of the raw import answers, `Set Name`, `Save File` | Complete — extended by this plan (normalisation) |
| BOOT-04 | The single `com.apple.Notes.CreateNoteFromMarkdownLinkAction` behind the `Note Present` gate's otherwise-branch, using the same `Control Room Body` text action (UUID `56EB40A5-...`) 02-02 authored, confirmed byte-identical by this plan's own construction | Complete structurally; on-device half is `UA-01` |
| BOOT-05 | The SELF-HEAL-OK check (exactly one `Save File`, gated on `State Present`'s otherwise-branch) and the IDEMPOTENCE-OK check (exactly one Note-creation action, gated on `Note Present`'s otherwise-branch), both re-run clean against the finished file | Complete structurally; on-device half is `UA-04` (state) and `UA-01`'s plan-02-04 extension, observation (e) (Note) |
| BOOT-06 | The entire state-load-and-bootstrap block sits above the router's outer gate (`F646324A`), confirmed by the SELF-HEAL-OK check's index ordering (`Get File`'s index precedes `Input Key`'s); the MANUAL, OPEN, and CLOSE paths all execute it identically before the router ever branches | Complete |
| BOOT-07 | The nested `SV1`→`SV2`→`SV3` `If` chain computing `State Present` from `schema_version` has-any-value AND `schema_version` string-equals `"1"` AND `profile` has-any-value; a missing file, a corrupt/unparseable file, an old-version file, and a profile-less file all fail this same gate identically and take the identical rebuild branch | Complete structurally; a genuinely malformed on-device file has not been hand-tested (no device available in this build environment) — named honestly, not asserted |
| BOOT-08 | `Find Notes` (Name contains the exact title, operator 99 per the documented Find-Notes name-matching trap) → `Note Found Text` has-any-value gate → `Note Present` → the reuse-or-create gate, confirmed by IDEMPOTENCE-OK | Complete structurally; on-device half is `UA-01`'s plan-02-04 extension, observation (f) |
| BOOT-09 | Import questions pinned at indices 2/4 (unchanged); `Descent Normalised` (nested `If`/`Otherwise`, default `Limbo`) and `Voice Normalised` (real JSON boolean) computed in the bootstrap branch | Complete — raw capture established 02-01, normalisation completed by this plan; on-device half is `UA-05` (unchanged scope) |
| STATE-12 | The `state.json` schema (schema_version 1, capped `recent_sessions`/`recent_contracts`/`exit_stats[*].samples`) — unchanged by this plan | Complete (carried from 02-01) |
| ROOM-01 | READ THIS FIRST section of the Control Room Note body — unchanged by this plan, only relocated | Complete (carried from 02-01/02-02) |
| ROOM-02 | Automation A build steps in the Note body — unchanged by this plan, only relocated | Complete (carried from 02-01/02-02) |
| ROOM-03 | Automation B build steps in the Note body — unchanged by this plan, only relocated | Complete (carried from 02-01/02-02) |
| ROOM-04 | The "cannot self-install" / "is bypassable" statements in the Note body — unchanged by this plan, only relocated | Complete (carried from 02-01/02-02) |
| ROOM-05 | The essential-apps safety warning in the Note body — unchanged by this plan, only relocated | Complete (carried from 02-01/02-02) |
| ROOM-06 | The editable `MY PHONE, ON PURPOSE` proforma in the Note body — unchanged by this plan, only relocated | Complete (carried from 02-01/02-02) |

#### F. PITFALLS A9 walkthrough for `src/PROSOCHE-Dumb.xml`

A green validator checks plist structure and known parameter shapes; it does not execute the Shortcut. Each of PITFALLS A9's five named validator false-passes, answered explicitly for this file rather than left as an unchecked assumption:

1. **The Store Content placeholder trap** (`is.workflow.actions.setstoredcontent`). This identifier is not used anywhere in `src/PROSOCHE-Dumb.xml` — confirmed by a direct scan of every `WFWorkflowActionIdentifier` in the 133-action array. Cannot hit this trap because the action is absent.
2. **The macOS 27 list-contains If, blank comparison chip.** This trap requires repeatedly reassigning the same named list variable and then testing it with a list-contains condition. This file's only list-typed value is the `Find Notes` result, and it is tested exactly once (the `Note Found Text` has-any-value gate) and never reassigned. No list-contains condition (`WFCondition` 99 against a list) is used anywhere; every string-contains-style comparison in this file (the exact-match checks) is a plain string-equals (code 4) or has-any-value (code 100) test on a `Text`-typed value. Cannot hit this trap because the pattern it depends on is not present.
3. **A Dictionary Value compared directly inside an `If`.** Every dictionary-derived value this file compares — `schema_version` and `profile`, both read via `Get Dictionary Value` from `State` — is routed through an `is.workflow.actions.gettext` action first (indices 27–29 and 31–32), and it is the routed `Text` output, never the raw `Get Dictionary Value` output, that reaches the `SV1`/`SV2`/`SV3` conditionals. This is what stops it: the mandatory Text-routing step is structurally present for both fields, confirmed by the phase-closure audit's coercion-discipline pass.
4. **`WFTextTokenAttachment` used for a display parameter.** The phase-closure audit's automated scan checks every `WFAlertActionTitle`/`WFAlertActionMessage`/`WFNotificationActionTitle`/`WFNotificationActionBody`/`Text` parameter across all 133 actions for the data-flow serialization and finds none — the fail-safe `Alert`'s title/message (unchanged from 02-03), the recovery line appended to the Note, and the Find Notes name filter's `Values.String` all use `WFTextTokenString`. This is what stops it: the serialization-discipline check itself, re-run clean against the finished file.
5. **`markdown` vs `markdownContents` on Notes creation.** `com.apple.Notes.CreateNoteFromMarkdownLinkAction` (the sole Note-creation action in the file) still uses the camelCase `markdownContents` key, unchanged from 02-01 and re-confirmed byte-identical by this plan's own relocation of that action into the `Note Present` gate's otherwise-branch. Cannot hit this trap because the correct key was never altered.

#### G. Closing subsection — ROADMAP Phase 2 success criteria

Each of the five Phase 2 success criteria in `.planning/ROADMAP.md`, mapped to the plan and check that establishes it:

1. *"Running the Shortcut with no input, `OPEN` input, and `CLOSE` input each route to the correct branch using iOS-26-compatible nested If/Otherwise; unrecognised or empty input fails safe without corrupting state or hanging."* — Established structurally by 02-03 (the four-outcome router, its Decision Table Trace) and re-verified intact by this plan's phase-closure audit (zero `Otherwise If`, every block balanced); the on-device half is `UA-07`.
2. *"First manual run creates a schema-valid, bounded, versioned state.json with initial profile, fork, and config values from the import questions, which capture descent profile (default Limbo), voice permission, and — Sentient only — the on-device intelligence preference."* — Established structurally by 02-01 (the schema, the bootstrap write) and completed by this plan (BOOT-03/BOOT-09's normalisation — `Descent Normalised`, `Voice Normalised`); the on-device half is `UA-05`.
3. *"First manual run also creates exactly one non-empty PROSOCHĒ — Control Room Note containing READ THIS FIRST, exact steps for Automation A and Automation B, a plain statement that the Shortcut cannot self-install these automations and is bypassable, the essential-apps safety warning, and the editable MY PHONE, ON PURPOSE proforma."* — Established structurally by 02-01 (creation/open wiring) and 02-02 (the full body) and re-verified byte-identical by this plan's relocation into the `Note Present` gate; the on-device half is `UA-01`.
4. *"Later manual runs never overwrite existing state or create a duplicate Control Room Note."* (BOOT-05) — This plan's own deliverable, proven structurally by the SELF-HEAL-OK and IDEMPOTENCE-OK checks (task 1 and task 2's own `<verify>` scripts); the on-device half is `UA-04` and `UA-01`'s plan-02-04 extension, observation (e).
5. *"Missing or corrupt state.json, and a deleted Control Room Note, each trigger safe self-healing recovery rather than failure, from any invocation mode."* (BOOT-06/07/08) — This plan's own deliverable: the hoisted state load (BOOT-06), the two-field validity gate (BOOT-07), and the `Find Notes`/`Note Present` existence guard (BOOT-08). Established structurally; the on-device half is `UA-01`'s plan-02-04 extension, observation (f), for the Note, and remains an honestly-named gap for a genuinely malformed on-device `state.json`, since no device is available in this build environment to hand-corrupt a file and observe the recovery.

---

## 8. Revisions — 2026-08-13 (user correction)

| Row | Was | Now | Authority |
|---|---|---|---|
| CAP-20 Color Filters / grayscale | `NOT AVAILABLE` | **`VERIFIED`** — `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` ("Set Color Filters"), params `operation` (`turn`\|`toggle`), `state` (bool On/Off), `ShowWhenRun` (bool) | BD-01-R — *identifier and params corrected by BD-01-R2, see §9* |
| CAP-26 Use Model, On-Device pinning | Hard gate on Phase 8 | Gate removed — PCC acceptable, On-Device preferred not required | BD-04-R |
| DEV-01 | Open deviation for Ash | **Withdrawn** — Ash needs no deviation | BD-01-R |
| UA-02 | Blocking gate on Phase 8 | Optional improvement | BD-04-R |

The CAP-20 correction turns on a distinction §3 of this document already drew but §4 failed to apply: a `platforms: ["macOS 27"]` tag records which build the catalog was captured from, and `toolkit-v78-ios27-tool-ids.json` is an **iOS Simulator** snapshot (1206 ids vs 2731) that omits the UniversalAccess extension entirely. Verified independently on this machine: the iOS 26.5 simulator runtime ships Shortcuts.app but contains no `UniversalAccess.framework` and no `UASettingsShortcuts` bundle. Neither signal is evidence about real iOS.

See `docs/CAPABILITY-DECISIONS.md` → REVISIONS for the full decisions.

---

## 9. Control Room Note — canonical signing name (plan 02-02)

Plan 02-02 expanded the `Control Room Body` `Text` action in `src/PROSOCHE-Dumb.xml` into the full Control Room Note. Its Automation A and Automation B build steps both instruct the user, identically, to pick the Run Shortcut target named exactly:

`PROSOCHĒ — Nine Circles — Dumb`

This is the same string already recorded as `WFWorkflowName` in `src/PROSOCHE-Dumb.xml` and as the intended signing name in `.planning/research/STACK.md` (`sign-shortcut ... --name "PROSOCHĒ — Nine Circles — Dumb"`). Phase 7's signing step must sign the Dumb-fork artifact under this exact string — em dash, macron, and the trailing " — Dumb" suffix all literal — so the entry the user selects from the Shortcuts app's Run Shortcut picker matches what the Note tells them to look for. Any future rename of the shipped shortcut requires updating both of this Note's automation sections to match; the Note is written first here and the signer must agree with it, not the reverse.

---

## 10. Note-check scoping decision (plan 02-04)

Plan 02-04 task 2 added the Note-existence guard (`Find Notes` → `Note Present` → reuse-or-create) that makes a deleted Control Room Note self-heal on the next manual run. That guard runs **only on the MANUAL branch** of `src/PROSOCHE-Dumb.xml` — never on the OPEN or CLOSE automation path — for two independent reasons, both already in the project's record rather than invented for this plan:

1. **Cost.** `.planning/research/ARCHITECTURE.md` §3's "When to run the Note-existence check" paragraph is explicit: an extra `Find Notes` call on every automatic app-open buys nothing, because the fast OPEN/CLOSE path never needs the Note at all (§5.4/§7.3 of the canonical strategy — the Note is write-only from the hot path's perspective). Paying a note-search cost on every tracked-app open for a check the hot path structurally cannot use would be pure overhead.
2. **Safety.** `.planning/research/PITFALLS.md` C10, read together with `UA-01` in §6 above, is equally explicit: a Notes action's very first invocation must happen inside a deliberate, watched manual run, never inside an unattended automation — because the first-use Notes permission prompt can appear at a moment the user is not looking at the screen if it fires from an automatic OPEN or CLOSE. Scoping the guard to the MANUAL branch guarantees every Notes action's first use in this file happens during the guided bootstrap flow.

**The rule Phases 6 and 7 inherit.** Neither reason above is specific to the bootstrap guard itself — both apply equally to any future Note append from the OPEN or CLOSE path (the Attention Ledger writer, Phase 6/7). The binding rule for those later phases, already stated in `.planning/research/ARCHITECTURE.md` §3: guard **lazily, immediately before the append**, not once per run and not up front — check existence right at the moment a specific append is about to happen, recreate the Note only if that specific check finds it missing, then make the append. This ties the repair cost to the moment it is actually needed rather than paying it on every single OPEN or CLOSE. Phase 6 and Phase 7 must not add a second, hot-path `Find Notes` call to satisfy this same guarantee — they reuse this exact lazy-guard shape at their own append site instead.

Structurally checked by plan 02-04 task 2's own `<verify>` (the IDEMPOTENCE-OK script): no `Find Notes`, Note-creation, `Append to Note`, or `Show Note` action sits inside the `OPEN` or `CLOSE` conditional's chain anywhere in the file.

---

## 11. Device evidence — 2026-08-13 (exports from the owner's iPhone, iOS 26)

Two shortcuts were built on a real iPhone, exported, and decrypted here. This is **primary device evidence** and outranks every ToolKit snapshot inference in this document. Raw plists: `docs/device-evidence/UseModel-OnDevice.xml`, `docs/device-evidence/SetColorFilters.xml`.

Recovery method (reproducible): a shared `.shortcut` is an AEA1 archive at profile 0 (`hkdf_sha256_hmac__none__ecdsa_p256` — signed, **not** encrypted). The leaf signing certificate is in a plaintext bplist at byte offset 12 under `SigningCertificateChain`. Extract it, take its public key, and the archive unlocks:

```
python3 -c "import plistlib;raw=open('X.shortcut','rb').read();open('/tmp/c.der','wb').write(plistlib.loads(raw[12:2216])['SigningCertificateChain'][0])"
openssl x509 -inform DER -in /tmp/c.der -pubkey -noout > /tmp/c.pub
aea decrypt -i X.shortcut -o /tmp/X.aa -sign-pub /tmp/c.pub
aa extract -i /tmp/X.aa -d /tmp/X          # yields Shortcut.wflow (binary plist)
```

This supersedes the project-wide assumption that a signed `.shortcut` can never be read back. It can, without the private key.

### CAP-26 — `Use Model` On-Device literal: **RECOVERED**

```
WFWorkflowActionIdentifier = is.workflow.actions.askllm
WFLLMModel                 = Apple Intelligence on Device      <- exact string
```

Supersedes BD-04 and BD-04-R's "unrecovered" branch. `UNRECOVERED-LOCALLY` is withdrawn; UA-02 is closed. Phase 8 **must** write `WFLLMModel = Apple Intelligence on Device`. On-Device is now enforceable in the shipped file, so the relaxation to PCC in BD-04-R is no longer needed — though it remains authorised as a fallback if the key is ever rejected on an older device.

### CAP-20 — Color Filters on iOS: **the identifier was wrong**

```
WFWorkflowActionIdentifier = com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent
state                      = <integer>1</integer>              <- 1 = On, 0 = Off
```

The iOS action is **`AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`**, not `UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent`. The `UniversalAccess` identifier is the **macOS** action. The iOS one is absent from **all three** bundled ToolKit snapshots (v63, v78, v78-ios27) — confirmed by direct search for `AXSett` and `AccessibilityUtilities`, zero hits in each.

Consequences:
- BD-01-R's chosen identifier is wrong and is corrected here. Phase 5 uses the `AX…` identifier above.
- There is **no `operation` key** on the iOS action — a bare `state` integer is the whole parameter set. Set `1` to apply Ash, `0` to restore. Still an explicit set, so restoration remains exact.
- The validator will not recognise this identifier (it is in no snapshot). Expect a Craig-Loop failure at that action and handle it as a documented, evidence-backed override rather than by substituting a different action.

### Incidental fact

`WFWorkflowClientVersion` on real iOS 26 exports is `4711` (both files). The project currently emits an OS27-era default; harmless per `PLIST_FORMAT.md` (the field is metadata Shortcuts rewrites on save), but `4711` is the observed-true value.

---

## 12. Phase 5 environmental safety (2026-08-13)

The shipped Phase 5 graph uses a validator-clean Ash fallback: a self-contained low-salience pause. It deliberately emits neither Color Filters identifier because the mandatory bundled validator has no waivable unknown-action exception. Brightness and Media volume are changed only after `Get Device Details` captures their originals under `settings_snapshot`; an existing unrestored snapshot is never overwritten. Dimming skips an already-dim display and uses `Config.safety.dim_target`, so it cannot brighten the display or set zero. Silence never writes non-Media volume or a value above its captured original.

`python3 docs/phase5_self_check.py` verifies semantic markers, the nine configuration entries, snapshot/restore safety, control-flow balance, pinned imports, unsupported-action exclusion, and two identical builder hashes. The project-wide validator command is `--target-macos 26 --target-platform all`: it passes. The plan's literal `--target-platform ios` command is retained as device-target evidence but presently reports every pre-existing core action from index 0 as a macOS-27 catalog false negative; it is not used to waive a Phase 5 action.

> **Amended 2026-08-17 (quick task `260817-ewg`).** The false-negative observation above was of the `--target-macos 26` **plus** `--target-platform ios` *pairing*, and remains correct as such. §12's operative command is gate A, `--target-macos 26 --target-platform all`, **unchanged** — nothing in Phase 5 moves. What §22 supersedes is the generalisation that the iOS platform flag as such is what produced the false negatives: it was the pairing with target 26, which admits no snapshot at all.

---

## 13. Recorded deviations — 2026-08-14 (debug cycle 3, session `open-routing-sequence-error`)

### DEV-01 — validator invocation: `--target-platform ios` is not used

`.claude/CLAUDE.md` mandates `--target-macos 26 --target-platform ios`. **The project builds with `--target-macos 26 --target-platform all` instead.** This is a deliberate, now-measured deviation, not an inherited assumption.

Measurement: at `--target-platform ios` the validator rejects **every action in the file** — 3675 of 3675 on the pre-cycle-3 Dumb build — including `is.workflow.actions.comment` and `is.workflow.actions.nothing`, both of which are *present* in the bundled iOS-27 snapshot the flag claims to consult. Rejection is therefore not driven by identifier presence. The snapshots are independently demonstrably incomplete: `is.workflow.actions.conditional` is absent from **both** the iOS-27 and v63 snapshots.

Consequence: the flag carries zero signal. A check that fails 100% of its inputs cannot conceal a real failure among them, so nothing is being waived by not running it. `--target-platform all` passes cleanly for both forks and is the invocation of record. Re-evaluate if a future plugin release ships a corrected iOS snapshot.

#### DEV-01 amendment — 2026-08-17 (quick task `260817-ewg`)

DEV-01's original text above is preserved verbatim. This amendment separates what held from what did not, measured against Playground 1.2.1 and recorded in §22.

**Holds, unchanged:**

- The `--target-macos 26` **plus** `--target-platform ios` pairing is vacuous. Its 3675-of-3675 measurement is correct and is reproduced by §22's mechanism reading: `toolkit-v63` is macOS-labelled and filtered out by the platform gate, the only iOS snapshot is a v78/27 capture and filtered out by the version gate, leaving an empty allowlist.
- Building on `--target-macos 26 --target-platform all` was the right call. It is now gate A, mandatory and unchanged.

**Does not hold:**

- **The generalisation that the iOS platform flag *as such* carries zero signal.** The controlling variable is `--target-macos`, not `--target-platform`. Below target 27 the validator loads neither the parameter-key catalog nor the enum-case catalog, on *any* platform setting — so gate A's blindness to parameter keys and picker literals was never attributable to the platform flag at all.
- **The closing expectation that this becomes re-evaluable only when a future plugin release ships a corrected iOS snapshot.** No new plugin was needed. Only a corrected pairing: raising the macOS target to 27 while keeping `--target-platform all`.

**Adopted:** `--target-macos 27 --target-platform all` as **gate B — advisory, waivered, never blocking**. Defined in `.claude/CLAUDE.md` §1; measured in §22.

**What gate B found in the shipped forks: no defect.** It reports exactly one line per fork, the `WFCreateNoteInput` parameter-key divergence, which is device-donor ground truth (§14) deliberately retained by the builder — a pre-adjudicated deviation, not a new finding. Gate B's value therefore does not rest on a discovery here; it rests on §22.4's synthetic-mutation control, which demonstrates it catches an invalid picker literal that gate A passes clean.

**Cross-reference: §5 `DEV-04`** recorded the same measurement from the Phase 2 side and is amended by identical reasoning — the measurement stands, the generalisation about the platform flag does not.

### DEV-02 — router no longer distinguishes "no input" from "unrecognised input"

The router was restructured to route on positive identification (`OPEN` / `CLOSE` / else MANUAL) rather than on absence of input. The former `Input Key has any value` gate and its "Unrecognised Input" fail-safe alert are removed.

Rationale: gating manual invocation on the normalised input being *empty* only worked while the Trim/Change Case chain was silently discarding its input. Once those parameters were given the text serialization iOS actually reads, the empty case stopped being empty, the gate passed, and **every manual tap was rejected as unrecognised input** — a device-visible regression. Absence is not a reliable signal; presence is.

What is lost: a mis-typed automation now reaches the manual menu instead of an explicit rejection alert. What is preserved: the safety property. The menu is inert until the person chooses an item, so a stray caller still injects no phantom event into Heat or Pressure. Both automation comparisons are byte-identical to before; only their enclosing level changed.

Guard: `verify_router_shape()` fails the build if the absence gate reappears, if the `Input Key` tests drift from exactly `OPEN` then `CLOSE`, or if the MANUAL arm leaves the CLOSE `Otherwise` branch. It runs in both fork builders.

### DEV-C3-03 — `speaktext` parameter key remains unverified

`is.workflow.actions.speaktext` is emitted with `WFInput` (10 sites). The ToolKit v78 catalog lists **no parameters at all** for that identifier, so there is no verified replacement key. Left unchanged deliberately: inventing a key would violate the project's no-fabrication rule. Needs its own device probe.

### Scaffolding debt (must be resolved before ship)

| Item | Where | Purpose |
|---|---|---|
| `BUILD_STAMP` in the manual menu prompt | `tools/build_state_engine.py` | Discriminates a stale duplicate install from a failed fix |
| `ROUTER_TRACE` alert on the MANUAL arm | `tools/build_state_engine.py` | Measures what an absent Shortcut Input normalises to on device |

Both are single-constant strips (`ROUTER_TRACE = False`; remove the stamp from the prompt) and both are intentionally visible rather than silent. Do not ship either.

## 14. Recorded deviations and device evidence — 2026-08-14 (debug cycle 4, session `open-routing-sequence-error`)

### CAP-05a — Notes body parameters are `AttributedString`, and `AttributedString` needs the text envelope

Cycle 2 established that a parameter iOS types as a plain string must carry a `WFTextTokenString` (a `￼` placeholder plus `attachmentsByRange`); a bare `WFTextTokenAttachment` imports cleanly, passes the bundled validator, and **resolves to empty at run time**. That rule was implemented against catalog type `str` only.

The ToolKit v78 catalog types the two Notes body parameters as **`AttributedString`** — `com.apple.mobilenotes.SharingExtension.contents` and `is.workflow.actions.appendnote.text`. `AttributedString` is a text type, not a content item, and it obeys the same rule. Because the cycle-2 allowlist keyed on `str`, both parameters were invisible to the normaliser **and to its recurrence guard**.

Consequence on device: the Control Room Note was **created with an empty body** — the create call succeeds, only the body parameter resolves to nothing. The manual Control Room refresh appended empty content for the same reason.

Evidence, in order of authority:

1. **Device donor, target iPhone.** `.planning/debug/"Donor - notes.shortcut"` (an Apple-signed Create Note shortcut exported from the owner's own iPhone, decrypted 2026-08-14 — see the decrypt recipe below) serialises `WFCreateNoteInput` as `{"string": "￼", "attachmentsByRange": {"{0, 1}": <token>}}` with `WFSerializationType` `WFTextTokenString`. This build emitted a bare attachment. Ground truth from the target device, not catalog inference.
2. **Golden corpus + donor agree on the output name.** Golden shortcut `f44f5caf5e3e48d4817e73af450c4404.xml` action 14 and the device donor both reference `is.workflow.actions.getrichtextfrommarkdown`'s output as **`Rich Text from Markdown`**. This build said `Rich Text`.
3. **Internal control group.** The artifact already carried one `appendnote` whose `text` was a `WFTextTokenString` (the state-recovery line, a composite template) beside one carrying a bare attachment (the Control Room refresh snapshot) — the same natural experiment that settled cycle 2.
4. **Runtime-confirmed mechanism.** Symptom 2 (`Set Dictionary Value` / key `sequence`) passed on device in cycle 3 precisely because its bare attachment became a `WFTextTokenString`.

Verified correct and deliberately unchanged: `is.workflow.actions.getrichtextfrommarkdown.WFInput` is catalog-typed `com_apple_shortcuts_wfcontent_item`, and both the device donor and golden `f44f5caf` action 13 pass it as a **bare attachment**. A content-item parameter must not be given the text envelope.

Guards: `STRING_ENVELOPE_PARAMS` now covers both Notes parameters, so `verify_string_envelopes()` fails the build if either regresses. A new `verify_output_names()` fails the build if a magic-variable reference carries an output name that differs from the producing action's real one. Both run in both fork builders.

### DEV-04 — the device donor's `folder` / `WFNoteGroup` parameters are not emitted

The donor's Create Note carries `folder` and `WFNoteGroup` (both naming the default iCloud `Notes` folder). This build emits neither, and also emits a `name` parameter the donor does not have.

Left as-is deliberately. The note demonstrably **is** created without `folder`/`WFNoteGroup`, so they are not blocking, and adding unproven parameters to an AppIntent payload is exactly how the resolved `unsupported-device-import` session's import blocker was created. `name` is not implicated in an empty *body*, and removing it would risk the Find-Notes reuse path that looks the note up by name. Revisit only if the note body is still empty after the `AttributedString` envelope fix.

### Device evidence — reading a signed `.shortcut` back (new capability, 2026-08-14)

`.claude/CLAUDE.md` and the plugin docs both record that a signed `.shortcut` is an AEA1 archive that "cannot be read back as a plaintext plist." That is true of `plutil`/`xxd`/`file`, but the archive **can** be opened with the signing certificate that travels inside its own header:

```bash
# 1. auth data at offset 12 is a bplist holding SigningCertificateChain
python3 -c 'import struct,plistlib,pathlib,sys; d=pathlib.Path(sys.argv[1]).read_bytes(); \
  sz=struct.unpack_from("<I",d,8)[0]; \
  pathlib.Path("leaf.der").write_bytes(plistlib.loads(d[12:12+sz])["SigningCertificateChain"][0])' "Signed.shortcut"
# 2. the leaf certificate's public key, in PEM (aea rejects raw/DER here, PEM works)
openssl x509 -inform DER -in leaf.der -noout -pubkey > pub.pem
# 3. decrypt, then unwrap the Apple Archive to Shortcut.wflow
aea decrypt -i "Signed.shortcut" -o out.aa -sign-pub pub.pem
aa extract -i out.aa -d out/          # -> out/Shortcut.wflow, a normal binary plist
```

This is how the target-iPhone donor was read, and it closes a verification gap that stood through cycles 1–3: the build side could previously only confirm freshness from the *unsigned* XML plus file mtime. The signed cycle-4 Dumb artifact was decrypted and confirmed to carry 3674 actions, `WFCreateNoteInput` as `WFTextTokenString`, both `appendnote.text` as `WFTextTokenString`, and the stamp `PROSOCHĒ · build 2026-08-14e`. Retain this recipe — it makes "did the device get the artifact we think it got" answerable from the shipped file itself.

### Automation-wrapper design record — one shared automation is correct

PROSOCHĒ's master shortcut consumes **no app identity**: `CurrentApp` appears zero times in either fork, and `.planning/research/ARCHITECTURE.md` §5 states the design decision explicitly — "Heat, Gravity, Pressure, Circle, and `active_session` are GLOBAL across all tracked apps, not per-app… there is exactly one `active_session` pointer at a time." The only thing the shortcut needs from the automation is the literal text `OPEN` or `CLOSE`.

Therefore **one App automation covering all watched apps is correct**, and splitting per-app is unnecessary. What must stay split is OPEN from CLOSE: two automations, one per trigger, because they pass different literals. This matches the shipped Control Room copy (Automation A / Automation B).

Operational hazard recorded: **deleting the shortcut orphans the automation's Run Shortcut reference.** Every clean-install debug cycle deletes and re-imports the shortcut, which leaves the Personal Automation's Run Shortcut action with no target selected — and a Run Shortcut with no target selected produces exactly `"…encountered an error: Please choose a value for each parameter in this action."` Re-point the Run Shortcut action after every re-import.

### Scaffolding debt (carried forward, unchanged)

`BUILD_STAMP` (now `build 2026-08-14e`) and `ROUTER_TRACE` both remain ON while the session iterates. See §13's debt table; neither ships.

## 15. Recorded deviations and capability findings — 2026-08-14 (debug cycle 5, session `open-routing-sequence-error`)

### CAP-06 — required picker (enum) parameters must be PRESENT and must hold a LITERAL enum case

The third axis on which an emitted parameter can be wrong, after the key-name axis (cycle 1) and the value-envelope axis (cycles 2 and 4). A parameter whose ToolKit type is a picker enum must carry a **plain literal string** naming one of its cases. If it is **absent**, or if it holds a **variable / attachment token**, Shortcuts renders an unfilled picker and iOS refuses to run the action with:

> Please choose a value for each parameter in this action.

Two sites violated this, and they were the only two in either fork:

| Site | Defect | Corpus evidence |
|---|---|---|
| `is.workflow.actions.count` → `WFCountType` | **missing entirely** (1 Dumb, 2 Sentient) | 11/11 golden-corpus `count` actions emit it; 0 omit it |
| `is.workflow.actions.getitemfromlist` → `WFItemSpecifier` | held a **variable token** at 31/33 sites, with `WFItemIndex` absent | every corpus instance uses a literal (`First Item` / `Item At Index` / `Items in Range`) and puts the dynamic index in `WFItemIndex`; golden `332c12a0060043b388b2` does exactly that with a `Repeat Index` variable |

The artifact contained its own control group: eight picker classes already carried literal enum cases (`searchweb` `Google`, `text.changecase` `UPPERCASE`, `getdevicedetails` `Current Volume`/`Current Brightness`, `setvolume` `Media`, `gettimebetweendates` `Seconds`, `round` `Ones Place`, `searchmaps` `Maps`, and `getitemfromlist` `First Item` at the two sites the generator authored with a literal). Only the two above deviated — in both forks.

**Why it surfaced only in cycle 5.** The OPEN branch had never once executed on device. Before the cycle-2 envelope fix, `Input Key` resolved empty, so every automation run took the MANUAL arm and skipped the OPEN pipeline entirely. Build `d` was the first build ever to *enter* the OPEN branch. Note this also refutes whole-shortcut pre-flight validation: the 2026-08-13 build carried these identical picker defects and ran from the automation all the way to the MANUAL menu. iOS errors on the action it reaches, not on load.

**Recurrence guard:** `REQUIRED_PICKER_PARAMS` + `verify_required_pickers()` in `tools/build_state_engine.py`, run by both fork builders. It fails the build if any of nine picker classes is missing or non-literal. Verified sensitive: it rejects the pre-fix artifacts naming the exact sites (32 Dumb / 33 Sentient), and it caught a genuine second `count` defect in the Sentient-only insertion path (`build_sentient.py:140`) that the Dumb pass could not see.

### DEV-C3-03 — **CLOSED.** `speaktext` uses `WFText`, not `WFInput`

§13 recorded that `speaktext` "lists no parameters at all" in the catalog and that no verified replacement key existed. **That premise was wrong.** The ToolKit v78 first-party catalog defines six parameters for `is.workflow.actions.speaktext`: `WFSpeakTextWait`, `WFSpeakTextRate`, `WFSpeakTextPitch`, `WFSpeakTextLanguage`, `WFSpeakTextVoice`, and **`WFText`** (type `str`, display name `Text`). `WFInput` is not among them, so the spoken text was never being read. All 10 sites now emit `WFText`, and because it is `str`-typed it is registered in `STRING_ENVELOPE_PARAMS` and takes the `WFTextTokenString` envelope per CAP-05/CAP-05a. No fabrication was required.

### DEV-05 — `math.WFMathOperation` is deliberately left absent at 25 sites — **CLOSED on device evidence (cycle 7)**

This looked like the leading candidate for the same defect class: a required enum picker (`Operation`) missing wherever the generator's `math()` helper is called with `op=None` or `op="+"`. It is **refuted by the corpus**, which outranks catalog inference under the cycle-2 `openurl` precedent: golden shortcut `2e0fb675e459` (client `1146.11.1`, minimum client `900` — our exact vintage) omits `WFMathOperation` with our exact key shape (`WFInput` + `WFMathOperand`). Addition is genuinely the implicit default. `math` is therefore **excluded** from `REQUIRED_PICKER_PARAMS`, deliberately and with the reason recorded in source.

**Settled affirmatively 2026-08-14 (cycle 7).** Cycle 6 had re-scored the corpus evidence as a weak 1-of-2 split and reopened this. Device donor 3 (`docs/device-evidence/Donor3-NumericConstructs.xml`, built in Shortcuts.app on the target iPhone and decrypted with §14's recipe) closes it: a Calculate action left at its **default** operation serialises as `WFInput` + `WFMathOperand`, both bare `WFTextTokenAttachment`, with `WFMathOperation` **absent entirely**. Omitting it is what iOS itself does. No generator change is owed.

### DEV-07 — numeric literals are emitted as plist `<integer>`; iOS never does (open, under test)

Neither the 19-shortcut golden corpus nor device donor 3 ever serialises a numeric literal parameter as plist `<integer>` — iOS uses `<real>` or `<string>` without a single exception. Donor 3 writes `number.random`'s `WFRandomNumberMinimum`/`Maximum` as `<string>` and `repeat.count`'s `WFRepeatCount` as `<real>`; the corpus writes `conditional.WFNumberValue` as `<real>` 4/4. This generator emits `<integer>` at 78 sites.

The axis is **not broadly guilty**: `number.WFNumberActionNumber` as `<integer>` executed successfully on device inside the "Open Control Room" menu case, and `conditional.WFNumberValue` as `<integer>` executed in the Control Room refresh block on the same pass. It survives at exactly two sites that are uniquely on the OPEN path, have zero corpus precedent, zero device coverage, and a donor that contradicts them — `number.random` and the nine-step `repeat.count`. Both are **deliberately left unchanged** pending the cycle-7 bisection result, so the measurement is not confounded. See `.planning/debug/open-routing-sequence-error.md` cycle-7 checkpoint.

Recurrence-guard gap this exposes, independent of the outcome: the generator asserts invariants on parameter **key**, value **envelope** and picker **literal**, but has none on the plist **type** of an emitted parameter. Six cycles of sweeps believed to be exhaustive never modelled it.

### DEV-06 — `openapp` legacy `WFAppIdentifier` retained; `WFWindowingFormat` deliberately omitted

`is.workflow.actions.openapp` emits a legacy `WFAppIdentifier` alongside the donor-verified `WFSelectedApp`, and omits `WFWindowingFormat`. Both left unchanged: extra undefined keys are provably inert in this artifact (`WFShowFilePicker`, `ShowWhenRun` and `WFAppIdentifier` all coexist on device-proven working paths), and `WFWindowingFormat` is OS27-gated, so emitting it would violate the iOS-26 target. Likewise `count` retains an undefined `WFInput` beside the catalog-defined `Input` so the input binds whichever key iOS actually reads.

### Correction to `.claude/CLAUDE.md` §8 — **APPLIED**

§8 previously stated that a signed `.shortcut` "cannot be read back as a plaintext plist". It now permits and documents the verified `aea decrypt` → `aa extract` workflow, including conversion of `Shortcut.wflow` to XML for inspection or remixing.

### Repository provenance guard — stale pre-cycle-1 branches archived

Cycle 6 found the checkout on `codex/prosochedebug1` / `efb5a79`, before every cycle 1–5 generator fix. The equally stale `codex/round1` ref pointed at the same commit. Both risky names are now archived locally as `codex/archive-stale-prosochedebug1-pre-cycle1` and `codex/archive-stale-round1-pre-cycle1`; the active checkout is `codex/automation-parameter-diagnosis` on the verified `7ca8ebb` lineage.

Before either generator runs, enforce `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD`. A nonzero result means the checkout predates the verified cycle-5 baseline: abort without regenerating or signing anything.

### Scaffolding debt (carried forward, unchanged)

`BUILD_STAMP` (now `build 2026-08-14g`), `ROUTER_TRACE` and — added in cycle 7 — `OPEN_BISECT` all remain ON while the session iterates. See §13's debt table; none of them ships. `OPEN_BISECT = False` strips all ten OPEN-path breadcrumb alerts; nothing else depends on them, and with them removed the artifact is byte-identical to build `14f` across all 3,674 actions apart from the two display-only stamp strings.

---

## 15. CAP-06 — operator/operand TYPE validity is a UI-only signal (debug cycle 8 addendum, 2026-08-14)

**The finding.** Six user screenshots (`.planning/debug/IMG_5624.jpg` … `IMG_5629.jpg`) show five
`If` actions whose **operator chip renders in RED** — rejected by Shortcuts — while the plist
that produced them is, by every static check this project can run, correct.

| action | condition | code | operand variable |
|---|---|---|---|
| 170 | is greater than | 2 | `Cooldown Until` |
| 377 | is greater than | 2 | `Previous Declared Duration` |
| 384 | is greater than | 2 | `Previous Overrun` |
| 409 | is greater than | 2 | `Heat Clamped` |
| 579 | is less than | 0 | `Stats Count` |

All five carry `WFSerializationType = WFTextTokenAttachment` with `WFNumberValue` present —
**the shape Donor 3 proved correct on this exact device.** Nothing in the file is wrong by any
catalog, corpus or donor comparison available here.

**Mechanism.** The operand variables are **text-typed** (the cooldown deadline is, in the
generator's own comment, "routed through text"). Shortcuts types the operand from its
provenance, and a text-typed operand offers only eight operators:

> `is` · `is not` · `has any value` · `does not have any value` · `contains` ·
> `does not contain` · `begins with` · `ends with`

No numeric comparator is offered, so condition codes 0/1/2/3/1003 have **no valid case to
render** and the chip shows red. Donor 3 is the contrast case: its operands came from **Number**
actions, and the identical envelope rendered numeric comparators correctly.

`.claude/CLAUDE.md` anticipated this trap for **equality** — *"there is no numeric-equals code;
use string code 4 on text-coerced numbers"* — but the generator walked into it for **ordering**
comparisons, which that guidance does not cover.

### Why this matters beyond the immediate bug

**Operator/operand-type validity is visible in the Shortcuts UI and INVISIBLE in the plist
file.** Every static sweep across eight debug cycles was blind to it *by construction* — not
through oversight, but because the signal does not exist in the artifact being swept. The
validator cannot see it, the ToolKit catalog cannot express it, and decrypting the signed
artifact does not reveal it either.

**Therefore: the on-device eyeball is a first-class evidence channel for this project**, ranking
alongside device donors and above catalog inference. When an action's correctness depends on the
*type* of a value flowing into it rather than on the serialisation of the value itself, only the
UI can adjudicate. Ask the user to look, and treat what they see as ground truth.

This is the fifth distinct parameter-defect axis found in one session, after key name, value
envelope (`str`), value envelope (`AttributedString`), and required picker enum. Each was
invisible to the sweep that caught the previous one.

**Status:** ~~not fixed at time of writing~~ — **FIXED in build 2026-08-14i (debug cycle 9).**
See §16.

---

## 16. CAP-07 — a numeric conditional operand must be TYPED, not re-materialised (debug cycle 9, 2026-08-14)

§15 named the axis (a Text-typed operand offers only string operators, so a numeric comparator
renders red) but left the **construct** open, because all 18 defective operands per fork are
**dictionary values** and `.claude/CLAUDE.md` warns that *"comparing a Dictionary Value (text)
directly in an If often renders blank — pass it through a Text action first."* Donor 3 did not
cover it: its operands came from `Number` actions, not dictionary values.

### Device ground truth — Donor 4.1

`.planning/debug/"Donor 4.1.shortcut"`, built in Shortcuts.app on the target iPhone and decrypted
with §14's recipe. It is exactly the construct in question — a Get Dictionary Value output
compared numerically:

| # | action | parameter |
|---|---|---|
| 0 | `is.workflow.actions.dictionary` | `{"heat": "42"}` |
| 1 | `is.workflow.actions.getvalueforkey` | key `heat` → output `Dictionary Value` |
| 2 | `is.workflow.actions.conditional` | `WFCondition 2`, `WFNumberValue "10"`, operand as below |

```json
"WFInput": {"Type": "Variable", "Variable": {
    "Value": {"Type": "ActionOutput", "OutputName": "Dictionary Value", "OutputUUID": "…",
              "Aggrandizements": [{"Type": "WFCoercionVariableAggrandizement",
                                   "CoercionItemClass": "WFNumberContentItem"}]},
    "WFSerializationType": "WFTextTokenAttachment"}}
```

**iOS inserts no `Number` action and changes no read chain. It types the variable reference in
place**, with a coercion aggrandizement, in the conditional's own input slot.

**The control case ships in the same donor pair.** `Donor 4` is the identical shortcut before the
type was set: same descriptor, **no** `Aggrandizements`, and a `WFCondition 100` test instead. The
only delta between the two is the coercion plus the numeric condition — which isolates the
coercion as the thing that makes a numeric operator legal on a dictionary value.

**The UI action is photographed.** `.planning/debug/IMG_5636.jpg` is the type list for a
`Dictionary Value` chip — Contact / Date / Dictionary / … / **Number** / PDF. Choosing *Number*
emits the aggrandizement. The fix is the plist form of a tap the user made and recorded.

**It attaches to named variables too**, which is the form our operands take: golden shortcut
`332c12a0060043b388b22b806be7ab58` carries `WFCoercionVariableAggrandizement` on both
`{Type: Variable, VariableName: …}` and `{Type: ActionOutput, …}` descriptors — 24 instances
corpus-wide. The aggrandizement is a property of the descriptor, not of the ActionOutput form.

### The apparent conflict with the project rule was never real

The `.claude/CLAUDE.md` rule — materialise a Dictionary Value before comparing it — is untouched
by this fix, because **the read chain is not modified at all**. What was missing was never the
materialisation; it was the **type declaration on the reference at the point of comparison**.

### A corpus-composed fix was built and discarded — the discard is the lesson

Before the donors arrived, a fix was composed from corpus evidence: golden
`2e0fb675e45948aaacee7e534f910492` actions 12 → 13 → 15 feed a Get Dictionary Value **straight
into `is.workflow.actions.number`** and consume the `Number` output in a numeric slot. A
`read_number()` helper was written on that basis, with a `WFCondition 100` null guard because
`cooldown_until` is JSON `null` on a fresh `state.json`. It validated, signed and measured clean.

It was discarded when Donor 4.1 arrived. **Device evidence outranks corpus composition.** The
corpus construct is real — it is the shape for *materialising a number into the data flow* — but
it is not the shape for *typing a conditional operand*, and chaining two separately-evidenced
links into an unobserved sequence is inference, not evidence.

The coercion is also better on every axis that matters:

| | coercion (shipped) | Number action (discarded) |
|---|---|---|
| actions added | **0** | ~250 |
| breadcrumb positions | **unchanged** — next device report directly comparable | shifted; re-indexing required |
| existing read chains | **byte-identical** | rewritten at 20 sites |
| behaviour on a JSON `null` | absent stays absent, comparison false | **unevidenced** — needs a guard, and the guard's premise was itself unproven |

That last row collapsed a two-condition AND-gate at action 170 into one condition.

### A distinct sub-class: mixed-typed variable NAMES

Shortcuts types a named variable from **all** of its `Set Variable` definitions. One Text-typed
definition anywhere poisons **every** numeric comparison of that name — *including comparisons on
an arm the Text definition can never reach*. This is why 20 sites are coerced where a hand trace
following each conditional's immediate feeding action found 18: `Pressure Next`, `Overrun Seconds`
and `Circle Next` are mixed-typed names.

### Passes

`normalise_numeric_operands()` attaches the coercion to any numeric-code conditional operand that
is not already Number-typed; `verify_numeric_operands()` asserts the resulting invariant. Both run
in **both** forks' builders and share one provenance resolver, so they cannot disagree. Operands
already fed by a numeric source (`number`, `number.random`, `math`, `round`,
`calculateexpression`, `gettimebetweendates`, `getdevicedetails`, `count`, `ask` with
`WFInputType = Number`, or the built-in `Repeat Index`) are deliberately left untouched, so
numeric conditionals that have executed on device stay byte-identical.

The generator now asserts five axes: **key name · value envelope · picker literal · variable slot ·
operand type.**

### Settled as a side effect — the variable-bearing `WFItems` List shape

Donor 4 / 4.1 action 5 is a `list` whose `WFItems` mixes bare strings with a variable-bearing
entry, and iOS **wraps** that entry:

```json
"WFItems": ["Circle",
            {"WFItemType": 0,
             "WFValue": {"Value": {"string": "￼", "attachmentsByRange": {…}},
                         "WFSerializationType": "WFTextTokenString"}},
            "follows"]
```

This artifact puts the `{Value, WFSerializationType}` object into the array **directly**, with no
`{WFItemType, WFValue}` wrapper. §15's addendum recorded that our shape matched neither golden
List action; it does not match the device shape either. **Not fixed in this cycle** — it sits past
breadcrumb J and cannot affect the measurement in flight — but there is now a device precedent to
conform to, and no donor request is owed.

### Carried forward, not fixed in this cycle

- **`Session ID` scope — safety-relevant, 18 sites.** `Session ID` is assigned once (ancestry:
  OPEN → not-in-cooldown → genuine-open). Only 2 of the 20
  `settings_snapshot.*.changed_by_session_id` writes share that ancestry; the other **18** sit
  under a different depth-1 branch where `Session ID` is never assigned, so brightness/volume
  snapshots taken outside the genuine-OPEN dispatch record an **empty owner** and the ownership
  check guarding restore cannot match. Deserves its own cycle so it can be measured alone.
- **`Spoken This Run` — investigated and dismissed.** Its tests use `WFCondition 101` ("does not
  have any value"), so `if not set → speak → set` is the correct once-per-run latch, not a defect.

---

## 17. DEV-06 — restore-ownership check DEFERRED by explicit user decision (2026-08-14)

**Status: DEFERRED, decided. Not a bug to be fixed silently — a design decision with a recorded
owner and a ship gate.**

### The finding

`settings_snapshot.brightness.changed_at`, `settings_snapshot.brightness.changed_by_session_id`,
`settings_snapshot.volume.changed_at` and `settings_snapshot.volume.changed_by_session_id` are
**written at 20 sites and read NOWHERE in either fork.**

`changed_by_session_id` exists so the restore path can verify it **owns** a change before
reverting it. Nothing reads it, so **that ownership check is not implemented at all.**

### The decision

Put to the user with four options — implement the check / drop the unused fields / leave as-is
and decide before ship / explain the risk first. The user chose:

> **"Leave as-is for now, decide before ship."**

So: **keep** writing `changed_at` and `changed_by_session_id`; do **not** implement an ownership
check; do **not** remove the fields.

### Residual risk, stated plainly

`.claude/CLAUDE.md` capability-audit items 8 and 9 require that a stateful brightness/volume
change be reliably captured and restorable. That guarantee is currently **half-implemented**: an
original value is captured and restored, but **nothing verifies that the restoring session owns
the change it is reverting.**

Exposure is narrow — it requires two overlapping runs where one restores what the other
captured — and is acceptable while the OPEN path does not yet complete end-to-end. It stops
being acceptable the moment the OPEN path ships.

### Consequence for the `Session ID` scope defect — PRIORITY DROPPED

`Session ID` is assigned only under [OPEN → not-in-cooldown → genuine-open]; only 2 of the 20
`settings_snapshot.*.changed_by_session_id` writes share that ancestry, so the other 18 record an
empty owner. **Correcting that scope only matters if something reads the owner** — and by the
decision above, nothing will.

The scope defect therefore **stays recorded as open but drops in priority**, tied to this same
deferred decision. **If the ownership check is implemented before ship, the scope fix becomes a
prerequisite, not a surprise.** Do not spend a cycle on the scope alone while DEV-06 is deferred.

### SHIP CHECKLIST — must all be resolved before release

| # | Item | Where |
|---|---|---|
| 1 | `BUILD_STAMP` — strip | `tools/build_state_engine.py` (single constant) |
| 2 | `ROUTER_TRACE` — strip | `tools/build_state_engine.py` (single constant) |
| 3 | `OPEN_BISECT` — strip the ten breadcrumb alerts | `OPEN_BISECT = False` |
| 4 | **DEV-06 — decide the ownership check** | this entry |
| 5 | **`Session ID` scope fix — REQUIRED IF AND ONLY IF item 4 resolves to "implement"** | tied to item 4 |

Items 1–3 are mechanical. **Items 4 and 5 are a judgement call the user has explicitly reserved
to themselves, and item 5 is conditional on item 4.** Neither may be resolved by an agent acting
alone.

**Addendum (2026-08-17):** the premise this entry rests on — that a proposed cut of the
brightness/volume machinery might remove the mechanism and make the question moot — is void; the
cut was cancelled, so DEV-06 and the `Session ID` scope defect are both live again. See §19.8. The
decision itself is unchanged and still reserved to the user; this line points forward only.

### Addendum (2026-08-18) — DEV-06 is CLOSED. Decided by the user: **REMOVAL.**

Everything above this heading is the record as it stood, retained unedited. This addendum
supersedes it on three points and closes the entry. Phase 16, plan 16-04, decision **D-02**
(LOCKED, see `.planning/phases/16-*/16-CONTEXT.md`).

**1. The site count above is STALE. Measured: 44 per fork, not 20.**

Measured 2026-08-18 by a `plistlib` key scan over both built forks, immediately before the
removal:

| Leaf | Write sites, `Dumb` | Write sites, `Sentient` |
|---|---:|---:|
| `settings_snapshot.brightness.changed_at` | 11 | 11 |
| `settings_snapshot.brightness.changed_by_session_id` | 11 | 11 |
| `settings_snapshot.volume.changed_at` | 11 | 11 |
| `settings_snapshot.volume.changed_by_session_id` | 11 | 11 |
| **total** | **44** | **44** |

Derivation: **2 leaves × 2 groups × 11 `primitive_dispatch()` renderings per fork = 44.** The
eleven renderings are nine `Test a Circle` submenu cases plus the two in `universal_leaving()`.
The figure is arrived at two independent ways — counted off the artifact and derived off the
rendering count — and they agree exactly.

This is the same staleness class as the 18-vs-28 correction `09-RESEARCH.md` had to make, and
it has the same two causes: the `Test a Circle` unroll, and Phase 11's eleventh dispatch
rendering. **A delta LARGER than the rendering count explains would mean a regression — a write
emitted somewhere `primitive_dispatch()` does not reach — not a recount.**

`§17`'s companion figure moves with it: "only 2 of the 20 … the other 18 record an empty owner"
becomes **4 of 22 `changed_by_session_id` writes carried a real owner, and 18 recorded an empty
one.** The "18" survives only by coincidence. Post-removal both figures are **0**, asserted
against the rebuilt artifact.

**2. DEV-06 — DECIDED by the user, 2026-08-18: drop the unused fields.**

Of the four options `§17` put to the user, the second was chosen: **remove
`changed_at` and `changed_by_session_id` entirely.** Ship-checklist item 4 is therefore
**CLOSED**.

The reasoning that made removal correct, recorded so it is not re-litigated:

- **Zero consumers.** No read of state targeted either field anywhere in either fork — not
  through `read_value()`'s chain, not through a flat `get_value()`.
- **The two guards that actually protect the overlap case consult neither identity nor time.**
  `if_block("<group> Snapshot", 100)` short-circuits a second session on snapshot *presence*, so
  it never overwrites a live original; and every restore path gates on `original_value > 0`.
  The exposure `§17` described as "narrow" was in fact already closed, by structure rather than
  by ownership.
- **A naive field-equality check would have been worse than nothing.** It would block the
  legitimate case where the last CLOSE restores the first capture — the case `09-UAT.md`'s
  first-principles write-up traced. Removal avoids introducing that defect at all.

**3. Why the decision became timely exactly now — the consequence plan 16-01 created.**

Before plan 16-01, these fields were written into the `State` dictionary, which is never saved
after the OPEN arm's last save. They therefore **did not survive the run that wrote them**: any
ownership check would have been reading a leaf no run could populate. 16-01 made the capture
persist to `state.json` — which is precisely what would have given these fields consequences for
the first time. Retiring dead state one plan *after* the fix that would have made it real is the
whole reason D-02 sits in this phase and in this order.

**Ship-checklist item 5 — the `Session ID` scope defect — is RESOLVED BY REMOVAL, not deferred.**
Item 5 was conditional on item 4 resolving to "implement". It resolved to "remove", so there is
no longer a field whose scope could be wrong. Both rows are closed; items 1–3 are unaffected.

**What enforces this going forward.** The removal is safe **only because there is no reader** —
`.claude/CLAUDE.md`'s verified runtime semantics make a dotted read of a missing segment a *hard*
runtime error, and Shortcuts has no `try`/`catch`. `tools/build_state_engine.py::
verify_no_removed_snapshot_leaf_reads` fails the build if any read ever targets one of these
names again, on **both** forks, reusing the existing read-key index rather than a grep. It was
demonstrated to fire on an injected read of each surface before being accepted (T-16-16).

---

## 9. Revisions — 2026-08-16 (donor ground truth)

| Row | Was (BD-01-R) | Now | Authority |
|---|---|---|---|
| CAP-20 identifier | `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` | **`com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`** — the `UA*` row is the macOS twin | BD-01-R2 |
| CAP-20 parameters | `operation = turn` (string), `state = On` (bool), `ShowWhenRun = Off` | **Substantially right.** `operation` is a string — and should be **omitted**, since `turn` is its elided default. `state` is a bool, serialized as an integer: **`1` = On, `0` = Off**. **No `ShowWhenRun` on the iOS intent.** | BD-01-R2 |
| CAP-20 verdict basis | Catalog reasoning + owner assertion | **Tier-1 donor ground truth** — `.planning/debug/Set Colour Filters.shortcut`, decrypted | BD-01-R2 |
| CAP-20 `operation` enum cases | "no case list found" (§4, original row) | Present all along, under the enum-cases file's top-level `types` key | BD-01-R2 |

**BD-01-R got one thing wrong: the identifier.** It prescribed the macOS `UA*` twin, which on
iOS would import as an unavailable action. Its parameter model — `operation` a string enum
case id, `state` a bool — was correct, as was its reasoning about why the catalog said
otherwise. The only other changes are dropping `ShowWhenRun` (not on the iOS intent) and
omitting `operation` (its `turn` default is elided by the device, so the literal is never
needed).

**Method note worth carrying forward.** Two intermediate revisions of this row asserted
integer enum *indices* from Apple's `AccessibilityUtilities.framework` intentdefinition —
first for `operation`, then `state = 2` for Off. Both were wrong. The intentdefinition is
genuinely useful (it named the parameters, the `turn`/`toggle` cases, and established that no
read-back intent exists) but it describes the intent's type system, not what Shortcuts writes
to the plist. Had `state = 2` shipped, Ash's restore leg would have failed and left users in
grayscale. It was caught by Donor 9.1, built to order. **A new, precise-looking evidence
source does not outrank a donor** — see `.claude/CLAUDE.md` "Evidence hierarchy".

All three donors are archived at `.planning/spikes/005-ios-color-filters-identifier/`.

Read-back is unchanged: no `Get*` intent for any accessibility setting exists among the
framework's 35 intents, so §21's opt-in remedy still governs. One untested lead is recorded
in BD-01-R2 — every `Toggle*` intent declares a `state` *response* parameter.

Full workings: `.planning/spikes/005-ios-color-filters-identifier/README.md`.

See `docs/CAPABILITY-DECISIONS.md` → BD-01-R2 for the binding decision.
## 18. Dimming/Silence coercion fix merged to main UNTESTED — live-path risk (2026-08-16, explicit user decision)

Phase 9 added `is.workflow.actions.setbrightness` (`WFBrightness`) and
`is.workflow.actions.setvolume` (`WFVolume`) to `NUMERIC_OPERAND_FIELDS` in
`tools/build_state_engine.py`, closing the axis-6 coercion gap at all 28 sites
(14 `setbrightness` + 14 `setvolume`; 18 receive the aggrandizement, 10 `Silence Target`
sites are already numeric via `number()` and correctly do not). This was merged to main by
explicit user decision on 2026-08-16 **without any on-device verification**.

### What this changes behaviourally — read before touching Circles

Prior to this fix the operands were text-typed. Per §15/§16 and `.claude/CLAUDE.md`'s axis-6
rule, a numeric parameter fed a text-typed operand is structurally valid in the file, passes
the validator, signs, imports — **and fails at runtime**. The practical consequence is that
Dimming and Silence almost certainly *no-opped* on device: no brightness or volume change
occurred, therefore no restore was ever required. The defect was inert.

After this fix those writes should actually execute. That means:

1. **Brightness and volume will genuinely change** when Circles carrying Dimming (Primitive E)
   or Silence (Primitive C) fire.
2. **`restore_managed_settings()` becomes load-bearing for the first time** — the four
   restoration triggers (owning CLOSE, live-Ice Emergency Restore, `ice_expiry()`,
   manual-menu Emergency Restore) now guard real state rather than an empty snapshot.
3. **That restore loop has never executed on a real device.** Per
   `.planning/phases/05-nine-primitives-environmental-safety/05-UAT.md`, exactly one Circle has
   ever fired on hardware (Circle 1, once, build `2026-08-15o`). Dimming and Silence have never
   run. Zero device evidence exists for capture, restore, or any failure mode.

**Net effect: this fix converted a dead defect into a live, unproven safety-critical path.**
That is the inverse of the §21 rule ("if the original value cannot be captured and restored
reliably, do not make the change at all"), and it was merged in full knowledge of that.

### Untested failure modes (all of them)

None of the following has ever been observed on hardware. Each was scripted as a numbered test
in `.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md`
and none was run:

| # | Untested behaviour |
|---|---|
| 3 | `Get Device Details` capture returns a real, non-empty, correctly-typed value |
| 4 | `WFBrightness = 0.0` is dim rather than black (BD-02 addendum rests on a user report, not a measurement) |
| 5 | Capture → apply → restore returns the exact original value on CLOSE |
| 6 | Force-quit mid-session does not strand the device dim/quiet |
| 7 | Device restart mid-session does not strand the device |
| 8 | CLOSE never firing does not strand the device |
| 9 | Two overlapping sessions restore the correct original |
| 10 | Compound: overlap + force-quit of the winning session |
| 11 | Emergency Restore recovers from each failure mode above |

Only test 1 (coercion chip does not render red in Shortcuts.app) was checked, by user
spot-inspection rather than an exhaustive pass over all ~3,500 actions.

### What to do before trusting this path

Run `09-UAT.md` end to end on an Apple-Intelligence-capable iPhone (15 Pro+, iOS 26.x). It is
fully authored and ready. Until it passes, treat any Circle carrying Dimming or Silence as
capable of leaving the device dimmed or muted with Emergency Restore as the only recovery —
and note that Emergency Restore's own effectiveness on this path (test 11) is equally unproven.

**DEV-06 (restore-ownership check) remains open and is unaffected by this merge.** §17 stands:
the decision is reserved to the user. `09-UAT.md`'s DEV-06 write-up argues from code trace that
the current no-ownership-check design is already correct for the two-session overlap case and
that a naive equality check would regress it — that argument is a trace, not device evidence,
and tests 9/10/12 exist to check it.

### ADDENDUM 2026-08-18 (Phase 11, plan 11-08) — the "live-path risk" this section names did not exist yet

**What §18 asserted.** That merging the coercion fix made the Dimming and Silence writes
execute where they previously no-opped, turning them into a live path on a device with no
evidence behind it — hence this section's whole framing as a live-path *risk*, and hence the
`09-UAT.md` battery above.

**What was actually the case.** The coercion fix was real, correct and necessary. It was also
**not sufficient**, and the writes did not become live. `dimming()` and `silence()` opened on a
condition-100 existence gate over the `settings_snapshot.<group>` **container**, with the entire
capture-and-apply body in the `otherwise` arm. `clear_snapshot()` writes the **leaf** and never
the container — deliberately, so the seeded subtree stays a permanent bootstrap invariant — so
that gate could never read false and the body was unreachable. Measured against the shipped
artifact: **44 environmental actions per fork** stranded in the never-taken arm (22 Get Device
Details, 11 Set Brightness, 11 Set Volume). Every UAT test listed above would have observed
nothing happening, and would have been read as a passing "no stranding" result. The eight
restore-side writes were never affected: `restore_managed_settings()` opens on the identical
container gate but puts its work in the **true** arm and lets its own numeric leaf gate decide.
Polarity, not the gate, was the entire defect.

**How it was found.** The Phase 11 review (`11-REVIEW.md`, CR-01, 2026-08-17) identified the
shape by inspection; it survived Phases 12, 13 and 16 and was re-measured against HEAD before
being fixed. It is worth naming why Phase 16 did not catch it despite being devoted to these
two functions: 16-01 filed **both** the outer container gate and the inner numeric capture gate
under one threat, T-16-03, described both as input validation over the `Get Device Details`
reading, and deliberately left both alone. That is accurate for the inner gate and wrong for the
outer one, which is evaluated **before** `Get Device Details` runs and therefore validates
nothing. Believing the broken gate was load-bearing is what protected it.

**What closed it.** Plan 11-08 re-gated both onto `settings_snapshot.<group>.original_value`
with the numeric `> 0` test the restore side already used, and armed
`verify_environmental_reachability()` in both builders with no exemption set — proven raising on
the live 44-site defect, proven silent on the 8 correct-polarity restore writes, and proven to
fail the build on a deliberate revert. Phase 16's `verify_capture_persistence()` is a separate
guard for a separate property (ordering once the body runs, not whether it runs) and was
verified clean both before and after.

**The device-proving tests referenced above remain untested, and this addendum does not change
that.** They were untested before and they are untested now; the fix is structural, not
behavioural. What changed is that they will now be testing a live loop rather than a dead one.
Ownership of that proof sits with **Phase 16 / DIST-03 / `16-UAT.md`'s twelve tests**, which
supersede this section's `09-UAT.md` battery as the current instrument. **No device was observed
in plan 11-08.**

---

## 19. Phase 10 — ship readiness and the UX lite pass (2026-08-17)

Phase 10 shipped four behavioural changes, three new guards, one checker repair and one refreshed
manifest, and it corrected two written positions it had inherited. Everything below was measured
at the phase's final `HEAD`; nothing here is device evidence, and §18's warning still governs.

Section numbering note: this file contains **two** sections numbered 15 (the debug-cycle-5
deviations and the CAP-06 addendum) and a stray duplicate `## 9` at the 2026-08-16 revisions
block. Number by the highest *value* present, not by position in the file. The highest was 18,
so this is 19.

### 19.1 Circle 0 — the silent band

A genuine OPEN whose Pressure falls below the active profile's first threshold now resolves to
Circle **0** and shows nothing at all: no notification, no menu, no primitive. Behavioural day,
Heat, Gravity, Pressure, open count and the active session are still computed and still
persisted. The band suppresses **surfaces**, never accumulation — `save_state()` deliberately
sits *outside* the gate and `universal_leaving()` inside it.

Every threshold entry was raised by that profile's own **first band width**, quoted verbatim
from the Config literal at `src/PROSOCHE-Dumb.xml` action 7:

| Profile | Was | Now | Shift |
|---|---|---|---|
| Paradise | `1, 4, 7, 10, 13, 16, 19, 22, 25` | `4, 7, 10, 13, 16, 19, 22, 25, 28` | +3 |
| Limbo | `1, 3, 5, 7, 9, 11, 14, 17, 20` | `3, 5, 7, 9, 11, 13, 16, 19, 22` | +2 |
| Inferno | `1, 2, 4, 6, 8, 10, 12, 14, 16` | `2, 3, 5, 7, 9, 11, 13, 15, 17` | +1 |

The derivation matters because it bounds what changed. Adding an array's own first band width to
every entry preserves **every band width exactly** and delays only *entry* into Circle 1 — a
strictly weaker change than re-tuning the curve, and one that cannot reorder or compress the
Circles relative to each other. All three arrays remain strictly ascending, remain nine entries,
and keep their last entry below `heat.cap + gravity.cap` = 35, so Circle 9 stays reachable.
Because `heat.open_base` is 1, a first open of a cold day now scores Pressure 1 and lands in the
silent band under all three profiles.

**These are prototype values for on-device tuning.** They are deliberately not commented inside
the JSON, because the literal is parsed by `detect.dictionary` and must stay valid JSON.

**The one load-bearing safety fact.** The silent band is enforced by a structural enclosure and a
build guard, *not* by copy, and the reason is a device-verified runtime semantic recorded in
`.claude/CLAUDE.md`: a **dotted** read whose final segment is absent is a **hard error** ("could
not evaluate the key path"), not a null. `primitive_dispatch()` reads
`sequences.<Sequence>.<Dispatch Circle>` as a dotted key. At `Dispatch Circle == 0` that final
segment does not exist, so the read throws — and it would throw *after* `active_session` was
already written, leaving a session no CLOSE will ever own. There is no sentinel value and no
"check then read" gate that avoids this, because the check itself is the read. The only fix is
never to reach the read at Circle 0, which is what the enclosure does and what
`verify_circle_zero_silence()` fails the build over.

The guard asserts four properties, each with its own message: (a) the Circle scan seeds at 0, not
1; (b) the `Leaving`/`Continue` menu — the OPEN path's sole entry point to every primitive — is
enclosed by the silent-band conditional; (c) every `sequences`-addressing dotted read **inside the
OPEN arm** is enclosed by that same group; (d) the OPEN arm emits no notification. Property (c) is
OPEN-arm-scoped on purpose: the nine MANUAL-arm reads from the Test-a-Circle submenu copy
`Dispatch Circle` from `Test Circle`, which is always 1–9, so index 0 is unreachable there by
construction. Rewriting (c) as an artifact-wide invariant would raise on the very first build.

### 19.2 The Circle identity change — a widened domain, not a new field

Circle 0 was promoted as a first-class value of the **existing** `circle` field rather than added
as a parallel `silent` boolean. The persisted domain widened from one-through-nine to
zero-through-nine. **No `schema_version` bump and no migration**, because a widened value range
needs neither: every legacy `state.json` holds a value that is still in range, and nothing
persisted changed shape. One source of truth for "did anything happen" was worth more than a
second field that could disagree with the first.

The consumer surface was measured directly against the built artifact rather than counted from
memory. Seventy-five actions reference `Circle Next`, resolving to **five distinct consumer
sites** when grouped by their nearest preceding comment:

| Consumer site | Actions |
|---|---|
| State persistence and the Circle-derived text (`setvalueforkey`, `gettext`, the 20 exit-stat list/index pairs) | 43 |
| The silent-band conditional itself | 1 |
| The Phase 6 universal Leaving menu | 1 |
| Knock's ten factual-interruption alerts | 10 |
| Mirror's template selection (10 list/index pairs) | 20 |

**Two of those would have hard-errored at Circle 0 had the gate been omitted**, and both are
invisible to `validate_shortcut.py`:

1. `primitive_dispatch()`'s dotted `sequences.<Sequence>.<Dispatch Circle>` read — the hard error
   described in §19.1. Verified: `Dispatch Circle` is set at artifact index 996 on the OPEN path
   with no `Test Circle` source, and at nine MANUAL-arm sites from `Test Circle`.
2. `mirror_text()`'s **Get Item From List** at `WFItemSpecifier = "Item At Index"`, indexing a
   ten-element list by `Circle Next` (artifact index 1155). At 0 the index is out of range.

Both sit downstream of the `Leaving`/`Continue` menu, which is why enclosing that single menu
closes both paths at once.

### 19.3 The OPEN notification removed, and the Leaving prompt reframed

The **unconditional OPEN `notification()`** and its three-line comment were deleted together as
one block. The artifact-wide notification count went from 2 to 1; the survivor is the CLOSE
confirmation, which is correct and stays. Measured on the shipped build: the OPEN arm contains
**zero** notifications.

The `Leaving`/`Continue` prompt was rebuilt to name what is being left and what continuing costs:

> You just opened a tracked app. PROSOCHĒ is at Circle ￼.
>
> Leaving: PROSOCHĒ suggests somewhere better to go and takes you there.
> Continue: you go into the app, after this Circle's intervention.

192 characters, exactly one attachment naming `Circle Next` at the correct offset, both item
titles byte-identical so `select_exit()` and `primitive_dispatch()` still hang off them.

**This is the second revision of that prompt; G-04-4b was the first.** Recording the sequence
matters because the two revisions had opposite constraints. G-04-4b had to keep the copy short
because the menu fired on *every* open, including the trivial ones. Revision 2 can afford to be
longer precisely because §19.1 stopped it firing in the silent band — the copy budget changed
because the trigger changed, not because the earlier judgement was wrong.

### 19.4 The gated Control Room note-show, and the tenth menu item

`Open Control Room` was previously an `is.workflow.actions.nothing` no-op whose entire effect came
from an **unconditional tail it did not own** — so the Note opened after *every* manual menu
choice, and the one item nominally responsible for opening it did nothing. It now sets
`Manual Show Note Requested`, and `gate_control_room_shownote()` wraps the single `shownote` in a
numeric `> 0` conditional on that flag.

`filter.notes` and Create Note were deliberately left **outside** the gate. The Note keeps being
found or created on every manual run, so BOOT-08's deleted-note self-heal survives and
`manual_note_refresh()` keeps a bound Note variable to append to. Measured: `filter.notes` 1,
Create Note 1, both unchanged and neither enclosed by the gate group, while the `shownote` is.

The gate is an *inserting* pass, so it cannot probe a parameter for prior application; its
idempotency probe is **positional** — "is `actions[index - 1]` already the mode-0 conditional I
would insert?". Two consecutive builds are byte-identical and exactly one conditional in the whole
artifact tests the flag.

A tenth manual menu item, **`Setup Check`**, reports whether either Personal Automation has ever
been recorded firing. It derives both verdicts from `last_open_at` and `last_close_at` — epochs
the engine already writes — rather than adding `automation_a_seen` / `automation_b_seen` keys: no
schema bump, no bootstrap edit, no migration. Both reads are **flat**, so per the same runtime
semantics as §19.1 they cannot hard-error on a legacy `state.json` that predates them, and both
gates are numeric `> 0` rather than condition-100 existence tests.

**The honest limitation ships in the alert copy, not in a source comment the user will never
see.** The derivation is sufficient but not necessary evidence: a close that a newer open
superseded, or an open during a cool-down, records nothing. So the alert says outright that a
**"not seen yet" verdict can be wrong, while a "seen" verdict never is**. That asymmetry is the
whole truth value of the feature and hiding it would have made the check worse than nothing.

### 19.5 Two corrections to positions this phase inherited

Both are recorded as deviations because both reverse something previously written down, and in
each case the reversal came from a measurement rather than from a judgement call.

#### DEV-P10-01 — the self-check baseline was not three-of-six red

- **The written position:** `10-RESEARCH.md` §5c recorded "three of six already FAIL at `HEAD`" —
  `phase5_self_check.py`, `phase6_self_check.py` and `sentient_core_check.py` — and the phase
  brief was shaped around it.
- **The measurement that reversed it:** that baseline was taken at commit `2e85aa3`. At the
  phase's actual starting `HEAD` (`0c9aace`), with both forks already regenerated from the
  post-merge generator by commit `c6d8737`, **six of seven `docs/*.py` scripts pass**. Only
  `docs/phase6_self_check.py` genuinely failed, on a stale `WFAppName` assertion that
  `normalize_open_apps()` contradicts by construction. `phase5_self_check.py` and
  `sentient_core_check.py` both passed.
- **What was done:** plan 10-03 repaired the one genuine failure — the assertion was dropped with
  a comment citing `normalize_open_apps()` by name and line, so the diff (8 insertions, 1
  deletion) reads as a correction rather than a weakening.
- **Why it is recorded:** a stale baseline is more dangerous than a red check, because it licenses
  ignoring failures that are real. The lesson is that a self-check baseline must be re-measured at
  the commit a phase actually starts from, not carried across from research.

#### DEV-P10-02 — `sentient_core_check.py` was kept green by rebuilding Sentient, not left red

- **The written position:** the research, the pattern map and the phase brief all directed that
  `docs/sentient_core_check.py` stay red this phase, on the stated basis that the Sentient fork
  was stale at `2026-08-14k` and re-forking is SEED-005, out of scope.
- **The measurement that reversed it:** commit `c6d8737` had already regenerated **and re-signed
  both forks** from the post-merge generator, and the check **passed** at the phase's starting
  `HEAD`. It was red only *transiently* — from 10-01's first Dumb rebuild until Sentient was
  rebuilt to match.
- **Why the brief's instruction had inverted:** honouring it literally would have meant *making*
  the check red, by changing Dumb and then refusing to rebuild Sentient. That converts a green
  invariant into a red one, which is the opposite of what the instruction was for. The check
  exists to detect fork skew; deliberately introducing skew to satisfy a stale expectation is the
  failure it was written to catch.
- **What was done:** plan 10-04 rebuilt Sentient from the same generator run as Dumb. All ten
  checkers, including `sentient_core_check.py`, exit 0 in a single run.
  `tools/build_sentient.py` needed **no edit**, because the cancelled brightness/volume cut leaves
  all ten of its imported `verify_*` names intact.
- **Scope, stated so it is not misread:** this is a **rebuild**, not a re-fork. SEED-005's re-fork
  question is untouched and remains out of scope.

### 19.6 Two ROADMAP Strand A items that needed no work

Recorded so a later reader does not go looking for changes that were correctly never made.

- **`.gitignore` already covers the build-noise patterns.** Verified by reading it: it excludes
  `.planning/debug/*.{jpg,jpeg,png,heic}` (personal device photos), `*.DS_Store`, `__pycache__/`,
  `*.pyc`, `.planning/graphs/` and `graphify-out/`. No addition was needed and none was made.
- **The MANIFEST rows were correct at the start of the phase.** The research's §5d drift table —
  three wrong Sentient rows — was measured at the older commit `2e85aa3`, before `c6d8737`
  refreshed them. Re-verified this phase by hashing every declared path out of the phase's
  starting tree (`0c9aace`): all six rows matched on both size and SHA-256. The manifest was
  refreshed in 10-04 **only because this phase rebuilt**, not because it was stale, and
  `docs/manifest_check.py` now makes that class of drift a failing check rather than a reading
  exercise.

### 19.7 The Circle 8 Voice orphan — a known open defect, reported not blocked

Config's `sequences` arrays name `Voice` at position 8 in all three profiles
(`Classic`, `BlackMirror`, `Ambient`), and **no dispatch branch matches it**, so Circle 8
currently dispatches nothing. This is a pre-existing defect owned by
`.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md`, and the ROADMAP explicitly
instructs any sequence/dispatch checker to record it rather than fail on it.

`docs/sequence_dispatch_check.py` now reports it by name with its Circle positions and its owning
todo on every run, and exits 0 by design. An orphan **not** on the `KNOWN_ORPHANS` roster is still
reported and marked `UNEXPECTED` — the roster suppresses nothing, it only distinguishes accepted
from novel.

The reporter is deliberately built to survive **BD-06 Decision 5**'s planned move from condition
code 99 ("contains") to code 4 ("string is"). It collects *every* mode-0 conditional testing
`Selected Primitive` with no filtering by condition code, and resolves each branch's matching rule
from that branch's own code via `match_strategy()`. Neither code exists as a module-level
constant, so the file needs no edit when BD-06 lands. Verified structurally: 80 branches collected,
equal to the 80 such conditionals in the artifact; `match_strategy()` returns three distinct
results including an explicit `unknown` outcome.

### 19.8 DEV-06 is live again — a consequence of the cancellation, not a new finding

**§17** records the restore-ownership check — the `settings_snapshot.brightness.changed_at`,
`.changed_by_session_id`, `volume.changed_at` and `.changed_by_session_id` leaves, written at 20
sites and read nowhere — as **DEFERRED by explicit user decision** ("leave as-is for now, decide
before ship"). §17 rests that deferral on a stated premise: that a proposed cut of the
brightness/volume machinery might remove the mechanism entirely and make the question moot.

**That premise is void.** The cut was **proposed and cancelled by user decision** (2026-08-16,
reaffirmed 2026-08-17). `dimming()`, `silence()`, `restore_managed_settings()` and the
`settings_snapshot` subtree all stay, and `docs/environmental_restore_check.py` now pins them so a
re-attempt fails loudly. The mechanism therefore ships, and **DEV-06 is live again** — along with
the `Session ID` **scope defect** tied to it: `Session ID` is assigned only under
[OPEN → not-in-cooldown → genuine-open], so only 2 of the 20 `changed_by_session_id` writes share
that ancestry and the other 18 record an empty owner. §17 dropped that defect in priority
*because* nothing would read the owner; if the ownership check is ever implemented, the scope fix
becomes a prerequisite rather than a surprise.

Three things stated plainly, because each is a way this entry could be misread:

1. **This reactivation is a consequence of the cancellation, not a new finding.** Nothing was
   discovered about the ownership check in Phase 10. The only thing that changed is that the
   escape route §17 hypothesised — the mechanism disappearing — is closed.
2. **The decision itself remains reserved to the user, exactly as §17 records.** Implementing or
   even *designing* the ownership check was therefore correctly out of scope for Phase 10. §17's
   ship checklist items 4 and 5 stand unchanged, and item 5 stays conditional on item 4.
3. **No Phase 10 work was done on it.** Nothing in this phase should be read as having settled,
   narrowed, or pre-empted the question. No design is proposed here and none should be inferred.

§17 carries a dated one-line addendum pointing here. Its body was **appended to, never revised** —
it records a user decision, and editing the premise in place would rewrite that record.

---

## 20. iOS 26 automation onboarding repaired (quick task `260817-au7`, 2026-08-17)

The Control Room Note's Automation A and Automation B build steps could not produce the
automations they described. Three defects, all in copy, none structural:

1. **Step 10 was impossible as written.** "Set the Run Shortcut action's input to the text
   `OPEN`" — `Run Shortcut`'s Input parameter accepts a **variable**, not typed literal
   text. There is no field in which those four letters can be typed.
2. **The app-trigger screen is a shortcut picker.** Selecting PROSOCHĒ there produces a
   **no-input** automation, so every trigger arrives with an absent `ExtensionInput`,
   composes as an empty string, and falls through the router to the MANUAL branch.
3. **Step 7 carried the stale `Ask Before Running` label.** iOS 26 presents a
   `Run After Confirmation` / `Run Immediately` choice instead.

### The replacement flow, and why it is trusted

Both sections now instruct: on the shortcut-picker screen tap **Create New Shortcut**; add
a **Text** action holding the literal; add **Run Shortcut** below it; confirm its Input is
the preceding Text magic variable, using **Choose Variable** if it is not auto-filled; save.

This is **device-proven at the mechanism level**. The `open-routing-sequence-error` debug
session drove a purpose-built INPUT PROBE — a signed shortcut echoing its Shortcut Input
verbatim — from a wrapper built exactly this way. It reported `RAW [OPEN]` and
`NORMALISED [OPEN]`. A screenshot of the user's own automation confirmed the two-action
wrapper renders with both the shortcut reference and the Input magic variable bound.

**What is proven is the handoff, not this rendered text.** No one has yet followed these
specific twelve steps on a device and arrived at a working automation. That confirmation
belongs with the outstanding device UAT and is recorded as such in the closed todo.

### Two additions beyond the literal fix

- **The exact-literal warning**, placed at the point the literal is entered rather than in a
  trailing caveat. During Phase 4 UAT this user's CLOSE automation was typed `CLOSED`; the
  router's exact match never fired, it fell to MANUAL, and **nothing on screen indicated a
  problem**. Silent failure is the reason the warning is inline.
- **"One automation covers every watched app."** `CurrentApp` appears zero times in either
  fork and Heat/Gravity/Pressure/Circle/`active_session` are global (§14's automation-wrapper
  design record). Without saying so, a user reasonably builds one pair per app.

### Where the text lives — measured, not assumed

The Note body is **authored in the XML, not generated**. `tools/build_state_engine.py`
contains no copy of this prose; it reads `src/PROSOCHE-Dumb.xml`, patches by comment-marker
anchor, and writes it back, so a hand edit to the body survives every rebuild.

The body is a `is.workflow.actions.gettext` whose `WFTextActionText` is a
**`WFTextTokenString`** carrying two attachments — `Import Descent` and `Import Voice` —
positioned **after** the edited region. Lengthening the automation sections shifts both.
`attachmentsByRange` was therefore **recomputed from the new placeholder offsets**
(`{4389, 1}`/`{4420, 1}` → `{5478, 1}`/`{5509, 1}`) rather than left in place; stale ranges
here are out-of-bounds ranges, which `VARIABLES.md` records as able to crash Shortcuts on
import. A plain text substitution in the XML would have shipped exactly that.

Sentient inherits the corrected body from the built Dumb source via `tools/build_sentient.py`
and was not edited by hand.

### Carried forward, deliberately untouched

Both sections still name `PROSOCHĒ — Nine Circles — Dumb` as the Run Shortcut target, in
both forks — §9 pins that string to the Dumb signing name, and Sentient's inherited body
therefore names the wrong fork. That is a **pre-existing** fork-naming defect, older than
this task and independent of it, and it belongs with Build Addendum 01 rather than a copy
repair. Recorded here so it is not mistaken for something this change introduced.

---

## 21. The guarded plist round trip, made executable, and the twelfth checker (phase 11 plan 01, 2026-08-17)

Phase 11 is a mass rename: nine primitive names, three sequence arrays, ten dispatch
renderings, two forks and eleven checkers. Its single largest risk is that a change
**validates, signs, imports cleanly and is still wrong**. This plan was the tracer against
that risk — one name, `Knock` → `Pause`, driven the whole length of the pipeline before any
other name moved — and it leaves behind the two instruments the remaining plans depend on.

**Everything below is structural.** `DIST-03` — device verification — is **open**: no iPhone
has been connected, so no statement in this section is device evidence, and none is offered
as any. Nothing in this phase has been observed running.

### 21.1 §20's method was prose; it is now a module

§20 above records the six-step round trip that quick task `260817-au7` used to edit the
Control Room Note body without shipping stale `attachmentsByRange` offsets. It records the
method **and no script** — the next person needing it had to re-derive it from a paragraph.
`tools/plist_text_edit.py` is that paragraph, executable. Standard library only
(`plistlib`, `pathlib`, `re`); no third-party import, deliberately.

Public API, in the order the six steps use it:

| Name | Step | What it guarantees |
|---|---|---|
| `load(path)` → `(data, original_bytes)` | — | The bytes that were parsed are returned, not re-read, so the equality below compares against exactly what was loaded |
| `assert_noop_roundtrip(data, original_bytes)` | 1 | `plistlib.dumps(..., fmt=FMT_XML, sort_keys=False)` is byte-identical to the source. Until this holds, no later diff can be attributed to the intended change |
| `assert_offsets_match(token)` | 2, 6 | Every `attachmentsByRange` key's leading integer equals a real `U+FFFC` offset in that token's own `string`, in document order |
| `replace_in_token(token, old, new, *, expected_count)` | 2–5 | Asserts the old offsets, asserts the match count, refuses a replacement containing `U+FFFC`, replaces, **rebuilds the ranges from the new placeholder offsets in document order** preserving each attachment's own value dict, then re-asserts |
| `replace_in_plain(action, key, old, new, *, expected_count)` | 3 | The same count-guarded replacement for a parameter that is a bare `str` — the Config literal is one — and refuses a token envelope outright |
| `save(path, data)` | — | Exactly one serialisation, exactly one write, mirroring the generator's own `main()` |
| `find_action(actions, predicate)` | — | Locates by **content**, and requires **exactly one** match: action numbers shift on every rebuild, and a second match means an arbitrary choice between candidates the caller did not know existed |

Failure convention follows `tools/build_state_engine.py`'s `verify_*` family: `SystemExit`
with a message naming the **consequence**. `expected_count` is not ergonomics — an edit that
matched fewer or more sites than intended is the exact shape of a silent partial rename.

### 21.2 The twelfth checker — `docs/note_identity_check.py`

Two invariants, one file, because they fail together.

**Note identity.** Three separate places in each fork spell the Control Room Note's name, and
nothing in the repository made them agree: the `is.workflow.actions.filter.notes` predicate
that looks the Note up, the H1 heading at the top of the body, and the `name` parameter of
`com.apple.mobilenotes.SharingExtension` that sets the title. All three are now asserted
against a single module constant, `EXPECTED_TITLE`, and each is located **by content, never
by index**, with exactly one of each required so a duplicate cannot hide. The predicate's
`Operator` is pinned too (currently `99`, "contains"), because RESEARCH §6.2 proposes moving
it to `4` alongside the title shortening: under `contains`, a shortened title would also
match a leftover Note from an earlier install, and with the filter's limit of 1 plus First
Item the wrong Note would be bound. Plan 11-03's rename is therefore a **one-line edit** to
`EXPECTED_TITLE`, and a change to the matching rule is a visible edit rather than a silent
one. "Control Room" remains the internal name everywhere in code and docs, per `e84ee77`.

**Attachment offsets.** The checker also walks every nested dict in both whole documents and
requires that any value carrying both a `string` and an `attachmentsByRange` has range keys
equal to its own `U+FFFC` offsets. It is armed **before** any Note copy is edited, and it is
global rather than scoped to the three sites above — a checker that only looked where it
expected damage would not catch the class. A floor of 775 token strings is asserted as well,
because a **drop** in the count means string-typed parameters were converted to bare
`WFTextTokenAttachment` values: parameter-defect axis 2, which validates and imports cleanly
and then resolves to empty text.

**Proven to fail.** A copy of `src/PROSOCHE-Dumb.xml` with one `attachmentsByRange` key
shifted by one (`{0, 1}` → `{1, 1}`) was fed to the checker. It exited **1** with:

> `Dumb: token string #1 declares attachment offsets [1] but its U+FFFC placeholders sit at [0] -- a range that does not land on a placeholder points into unrelated prose, and an out-of-bounds range can crash Shortcuts on import`

The sabotage was applied to a temporary copy; the repository artifact was never written.

### 21.3 Evidence table — every row structural, not one of them run on hardware

| # | Claim | Measured | Kind |
|---:|---|---|---|
| 1 | No-op `plistlib` round trip byte-identical before any edit | 2,260,491 in == 2,260,491 out (Dumb) | structural |
| 2 | Provenance gate `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit **0** (checked before each builder run) | structural |
| 3 | `tools/build_state_engine.py` | exit **0** | structural |
| 4 | `tools/build_sentient.py`, run from the fresh Dumb source | exit **0** | structural |
| 5 | Hand edit survives the generator | second consecutive build leaves `src/PROSOCHE-Dumb.xml` at `efad0819…`, unchanged; `git status --short` clean | structural |
| 6 | Retired name in the built sources | `Knock`: **0** lines in Dumb, **0** in Sentient | structural |
| 7 | New name in the built sources | `Pause`: **43** lines in each fork — 3 `sequences` cells + 10 dispatch renderings × 3 sites + the 10 pre-existing `Ash` alert bodies that already carried the word | structural |
| 8 | New name in the Config literal specifically | `Pause` in exactly **3** cells (`Classic[0]`, `BlackMirror[0]`, `Ambient[3]`), retired name absent, JSON still parses | structural |
| 9 | Attachment keys vs recomputed offsets, `src/` | Dumb **775/775** match, Sentient **779/779** match, **0** mismatches | structural |
| 10 | `plutil -lint src/PROSOCHE-Dumb.xml` after the guarded edit | **OK** | structural |
| 11 | Validator, Dumb, `--target-macos 26 --target-platform all` | `Validation passed.` exit **0** | structural |
| 12 | Validator, Sentient, same invocation | `Validation passed.` exit **0** | structural |
| 13 | Signed artifact sizes, canonical names, no suffix | `PROSOCHĒ — Nine Circles — Dumb.shortcut` **193,836 B**; `… — Sentient.shortcut` **198,150 B** | structural |
| 14 | Dated archive SHA-256 equals its `src/` counterpart | Dumb `efad0819…` == `efad0819…`; Sentient `8d9c6105…` == `8d9c6105…` | structural |
| 15 | `plutil -lint` on both recovered plists | **OK**, **OK** | structural |
| 16 | Retired name in the **decrypted** payloads | `Knock`: **0** lines in each; recovered `sequences` hold it in **0** cells | structural |
| 17 | New name in the **decrypted** payloads | `Pause`: **43** lines in each; recovered `sequences` hold it in exactly **3** cells per fork | structural |
| 18 | Attachment keys vs recomputed offsets, **decrypted** payloads | Dumb **775**, Sentient **779**, **0** mismatches | structural |
| 19 | The eleven pre-existing `docs/*.py` checks | all exit **0** | structural |
| 20 | The twelfth, `docs/note_identity_check.py` | exit **0**, and exit **1** on a deliberately shifted offset | structural |

Rows 15–18 are the only non-device channel this project has for "what actually shipped": the
signed `.shortcut` is an AEA1 container, recovered via the §8 recipe. They say the bytes on
disk carry the intended name. They do **not** say a Circle-1 open reaches the renamed
dispatch branch on a phone — that is behavioural, `DIST-03` is open, and it is not claimed
here or anywhere else in this phase.

### 21.4 Deliberate non-changes

- **`knock()` keeps its Python identifier.** The dispatch tuple carries the *shipped* name and
  the function carries the *internal* one. `docs/environmental_restore_check.py:55-56` imports
  generator functions **by name**; renaming any of them is a separate, unrelated breakage.
- **The Circle-8 `Voice` orphan is left exactly as found.** `docs/sequence_dispatch_check.py`
  still reports it as a known open defect and still exits 0. Plan 11-02 authors the
  dispatch-coverage guard and needs the orphan live to prove the guard has teeth.
- **The condition-99 → condition-4 dispatch move did not happen here.** It is coupled to
  abolishing the three combined entries and belongs with the rest of the roster, in 11-02.

---

## 22. Validator invocation — measured evidence for the two-gate rule (quick task `260817-ewg`, 2026-08-17)

Rung-1 file-level evidence per §9's escalation ladder, satisfying §3's binding citation rule.
**This section records measurements only. The rule itself lives in `.claude/CLAUDE.md` §1 and
is deliberately not restated here** — same one-home discipline §3 line 83 already applies to
the §9 tooling inventory.

Plugin under test: `~/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1`.
Artifacts: `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` as shipped. Nothing was
rebuilt or re-signed to produce any figure below.

### 22.1 The mechanism, read from the validator source

All citations are `skills/shortcuts-playground/scripts/validate_shortcut.py` in plugin 1.2.1:

| Lines | Symbol | What it establishes |
|---|---|---|
| `:864-889` | `resolve_target_platform` | `all`/`any`/`latest` → Python `None`; `ios`/`ipados`/`iphone`/`ipad` → `"ios"`; everything else → `"macos"` |
| `:892-1019` | snapshot loading | Snapshots filtered by **two independent gates** — a minimum target-macOS-major check and a platform-label check. `toolkit-v63` is macOS-labelled; `toolkit-v78-ios27` is a v78/27 capture. So `--target-macos 26 --target-platform ios` admits **no snapshot at all** |
| `:265` | `TOOLKIT_PARAMETER_CATALOG_MIN_MACOS_MAJOR = 27` | Consumed at `:1086`, `:1162`, `:1223`. **Below target-macOS 27 the parameter-key and enum-case catalogs are not loaded at all**, on any platform setting |
| `:1039-1046` | `_catalog_platforms_match_target` | Returns `True` immediately when the target platform is `None` (i.e. `all`) |
| `:1048-1055` | `_catalog_platform_name_matches_target` | `ios` matches only platform names beginning `iOS`. Every catalog entry tagged `macOS 27`-only is therefore **excluded from parameter-key and enum-case checking** under `--target-platform ios` |
| `:1144-1211` | `load_toolkit_parameter_enum_cases` | Applied at `:2311-2314` |

### 22.2 The four invocations, measured

| Invocation | Dumb | Sentient |
|---|---|---|
| `--target-macos 26 --target-platform all` | `Validation passed.` **exit 0** | `Validation passed.` **exit 0** |
| `--target-macos 27 --target-platform all` | **exit 1**, exactly **1** error | **exit 1**, exactly **1** error |
| `--target-macos 27 --target-platform ios` | **exit 1**, exactly **5** errors | **exit 1**, exactly **5** errors |
| `--target-macos 26 --target-platform ios` | rejects essentially every action (empty allowlist) | not re-run |

### 22.3 Enum-case coverage, measured directly from the loader

`load_toolkit_parameter_enum_cases(skill_dir, macos_major, platform)` returns this many
enum-checked identifiers:

| target | identifiers |
|---|---:|
| macOS 26, any platform | **0** |
| macOS 27, platform `all` (→ `None`) | **1105** |
| macOS 27, platform `macos` | **886** |
| macOS 27, platform `ios` | **455** |

Of the picker parameters **the forks actually emit**, `27 all` enum-checks **14**
`(identifier, key)` pairs and `27 ios` enum-checks **13** — `ios` loses
`is.workflow.actions.appendnote` / `operation`, because that action's catalog entry is
`macOS 27`-tagged. Both forks give identical sets.

### 22.4 Synthetic-mutation control — proof the second gate has teeth

A scratch copy of the Dumb fork with a single `is.workflow.actions.count` `WFCountType`
changed from `Items` to `Bananas`:

- `--target-macos 26 --target-platform all` → **`Validation passed.`** — blind to it.
- `--target-macos 27 --target-platform all` → **caught it**:
  `Invalid ToolKit enum value for is.workflow.actions.count.WFCountType at index 574: 'Bananas'. ToolKit v78 allows: 'Characters', 'Items', 'Lines', 'Sentences', 'Words'.`

`src/` was never modified; the mutation lived only in the scratch directory.

### 22.5 The waiver, index-normalised

| Waived line (indices normalised to `N`) | Count per fork | Why waived |
|---|---:|---|
| `Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index N: WFCreateNoteInput. ToolKit v78 expects: OpenWhenRun, contents, folder, interpretAsMarkdown, name.` | 1 | Device-donor ground truth outranks the `macOS 27`-tagged catalog entry — §14; deliberately retained in `tools/build_state_engine.py` — enforced entry `STRING_ENVELOPE_PARAMS["com.apple.mobilenotes.SharingExtension"]`, donor-evidence comment in the CYCLE 4 block immediately above it. **Anchor on the symbol, not the line.** Measured 2026-08-17: comment `:1961-1966`, entry `:1982` |

Real indices at the time of measurement: **Dumb `3619`, Sentient `3687`**. They shift on
rebuild, which is why the waiver is recorded index-normalised.

Normalisation command a future run diffs against:

```bash
"$PLUG/bin/validate-shortcut" "$f" --target-macos 27 --target-platform all 2>&1 \
  | grep '^- ' \
  | sed -E 's/ at index [0-9]+:/ at index N:/' \
  | sort | uniq -c
```

### 22.6 The headline, stated plainly

**The empirical check did not reveal a shipped defect.** Both forks pass the mandatory gate
clean. The second gate surfaces exactly one line per fork, and that line is a known,
already-adjudicated, deliberately-retained deviation (§14) — not a new finding.

**Gate B added no new information about the current forks.** Its one line is pre-adjudicated.
Its demonstrated value rests entirely on the synthetic-mutation control in §22.4 — a measured
demonstration that it catches a class of defect gate A passes clean — and not on any discovery
in these artifacts. Both things are true and neither should be inflated.

### 22.7 Deliberately uncited concurrent work

`.planning/spikes/006-picker-serialisation-taxonomy/`, `007-*` and `008-*` were untracked and
being written by a concurrent session while this task ran. **Handling: reference without
dependency.** No claim in this section rests on them — every figure above, including the
enum-coverage counts in §22.3 that 006 would otherwise have been cited for, was measured
directly here against the loader. They are noted as adjacent concurrent work, nothing more.

---

## 23. The Note rename, the Dante name surface, and the Purgatory profile (phase 11 plan 03, 2026-08-17)

The **user-facing** half of Build Addendum 01 — §1 (the nine Circle names), §3 (the optional
hardening instruction) and §4 (the Note title) — plus **BD-06-A1**, a user decision taken the
same day, mid-phase, which renamed the middle descent profile.

**Every row in this section is STRUCTURAL.** `DIST-03` is open, no iPhone is connected, and
nothing recorded here has been observed running. Where this section says "verified" it means
*verified in the file, or in the decrypted payload of the signed container* — never on device.

### 23.1 What moved

| Change | Sites | Mechanism |
|---|---:|---|
| Apple Note title `PROSOCHĒ — Control Room` → `PROSOCHĒ` | 3 per fork | `tools/plist_text_edit.py` guarded round trip |
| `## READ THIS FIRST` stale-note instruction | 1 per fork | same |
| `## THE NINE CIRCLES` legend | 1 per fork | same |
| `## OPTIONAL HARDENING` section | 1 per fork | same |
| `CIRCLE_NAMES` + `circle_menu_title()` | new, generator | `tools/build_state_engine.py` |
| Test-a-Circle items **and** case titles | 9 + 9 per fork | derived from that one constant |
| Profile `Limbo` → `Purgatory` | 9 per fork + 4 files | class sweep, see §23.4 |

The Note's three identity sites are the `is.workflow.actions.filter.notes` lookup predicate,
the body's H1, and `com.apple.mobilenotes.SharingExtension`'s `name` parameter. They must move
together: if the predicate and the title disagree, PROSOCHĒ creates a Note it can never find
again and appends its ledger to a fresh one on every state-changing run, silently.
`docs/note_identity_check.py` asserts all three against one `EXPECTED_TITLE` constant.

The **internal** name is unchanged everywhere, per commit `e84ee77`: the `Open Control Room`
menu item (asserted by `docs/phase7_self_check.py`), the `Control Room Note` variable, the
`MANUAL_MARKER` and refresh comment anchors, and the `gate_control_room_shownote()` /
`fix_shownote_key()` / `fix_notes_filter_limit()` function names.

### 23.2 Deviation 1 — the Find-Notes operator was RETAINED at `contains`

`.planning/phases/11-.../11-RESEARCH.md` §6.2 recommended moving the `Name` filter row's
`Operator` from `99` ("contains") to `4` ("string is") in the same edit that shortened the
title, because a shorter title under `contains` also matches a leftover Note from an earlier
install — and with `WFContentItemLimitNumber: 1` plus a Get Item From List "First Item",
PROSOCHĒ would bind to that Note and append its ledger there permanently.

**The operator was not moved.** Two independent reasons:

1. The current value is `BOOT-08`'s **recorded decision**, taken against the documented
   Find-Notes name-matching trap. Reversing a recorded decision needs evidence.
2. Whether `Operator: 4` is accepted in a `WFContentPredicateTableTemplate` on the Notes
   `Name` property is **UNVERIFIED** — the condition-code table in `.claude/CLAUDE.md` §4
   documents `4` for `WFCondition` on *conditionals*, and no donor, golden shortcut or
   catalog entry in this project covers the filter-template case. Writing it would be
   inference against a recorded decision, which the project's capability rule forbids.

**Evidence that would close it:** a donor export of a Find Notes action configured by hand on
the owner's iPhone with the `Name` filter set to "is", recovered via the §8 / §11 AEA1 recipe,
read for the `Operator` literal the device actually writes. Rung 3–4 by `.claude/CLAUDE.md`
§9's ladder — `com.apple.mobilenotes` is absent from the booted simulator, so rung 2 cannot
reach it.

**Interim mitigation:** a `## READ THIS FIRST` paragraph asking the user to delete or rename
an old-titled Note. That is a user instruction, not a mechanism, and it is recorded as such.
The operator is **pinned** by `docs/note_identity_check.py`'s `EXPECTED_NAME_OPERATOR`, whose
comment names BOOT-08 and the decision record, so a future change is a deliberate edit to a
named constant rather than a silent side effect of a copy change. Full record:
`docs/CAPABILITY-DECISIONS.md` **BD-06-A2**.

**Second-order, pre-existing:** both forks create a Note with the same title. Not introduced
here — both wrote `PROSOCHĒ — Control Room` before — but sharper now that the title is shorter.
Giving the forks distinct Note titles is a product decision that belongs with the Dumb→Core /
Sentient→Aware rename in plan `11-06`.

### 23.3 Deviation 2 — `## OPTIONAL HARDENING` is not at the tail

Build Addendum 01 §3 says the optional hardening instruction goes "at the end of the Note".
It was placed **immediately after `## Do not target these apps`** instead, and `## THE NINE
CIRCLES` was placed before the `## MY PHONE, ON PURPOSE` proforma rather than after it.

**Reason:** `manual_note_refresh()` appends a fresh `## CURRENT SETTINGS` / `## CURRENT STATE`
/ `## ATTENTION LEDGER` block to the **end** of the Note on every state-changing manual run
(`appendnote`, `operation="append"`). The Note therefore grows monotonically, and anything
placed at the tail is progressively buried under machine-appended duplicates. A section a user
is meant to read once and act on cannot live where the machine writes. The hardening section is
also topically the same subject as the do-not-target guidance — both are about which apps go
into the automation — so the placement is better copy as well as more durable.

Final heading order, asserted in both forks and in both decrypted payloads:
`## Do not target these apps` → `## OPTIONAL HARDENING` → `## THE NINE CIRCLES` →
`## MY PHONE, ON PURPOSE`.

### 23.4 BD-06-A1 — the middle profile is `Purgatory`

BD-06 made `Limbo` the positional name of **Circle 1**, while `Limbo` was already the name of
the **middle profile** — one word naming a depth and a pace. The user's decision renames the
profile rather than disambiguating the copy, which also makes the three profiles the three
canticles of the Commedia: **Paradise / Purgatory / Inferno**. Circle 1 keeps `Limbo`.

**The rename had to be total, and that is a runtime fact, not a tidiness preference.** A
profile name is a live dotted Config key path — `thresholds.<profile>`,
`cooldown_seconds.<profile>` — and this project's verified runtime semantics record that **a
dotted read with any missing segment is a hard error**, not a silent miss. A surviving
`thresholds.Limbo` read against a `Purgatory` profile value would be a crash. Swept by class
in one commit:

- the Change Profile menu's `WFMenuItems` and its three case titles (generator, `PROFILE_NAMES`)
- `thresholds.Limbo` → `thresholds.Purgatory`, array unchanged at `[3, 5, 7, 9, 11, 13, 16, 19, 22]`
- `cooldown_seconds.Limbo` → `cooldown_seconds.Purgatory`, value unchanged at `180`
- the import question's `DefaultValue` and its prompt text
- the bootstrap normalisation fallback (unrecognised answer → `Purgatory`), comment and Text action
- `docs/state_engine_self_check.py`'s `THRESHOLDS` table and its two assertions
- `src/CONFIG-BLOCK.md` — literal, two field-reference rows, the transcription-recipe example, change log

**No migration, dual-key alias or read-time normalisation was built.** BD-06-A1 forbids all
three by name: PROSOCHĒ is a new, as-yet-undeployed product, the only installs are the owner's
own testing, and old `state.json` files are explicitly not a consideration. A device holding
`profile: "Limbo"` would hard-error at its next OPEN; that consequence is real and is
**accepted** because there is no population it can harm.

**Verified per fork, on the shipped payload:** `Limbo` survives on exactly **three** sites in
each — the Test-a-Circle item, its matching case title, and the Note legend line — and every
one is a `Circle 1 · Limbo` label. None is a profile, threshold, cooldown or menu occurrence.
No disambiguation line was written, because the two names no longer collide; threat `T-11-16`
is **eliminated**, not mitigated.

**Circle 0 is named "The Indifferent"** after Dante's *ignavi*, who are placed in the vestibule
**before** Circle 1 — exactly Circle 0's position. Recorded in `docs/CAPABILITY-DECISIONS.md`
BD-06-A1 and here, and **nowhere else**: the name reaches no user-facing surface this phase.
The Note's legend still lists **nine** Circles, the Test-a-Circle menu still offers nine, and
`verify_circle_zero_silence()` — which structurally enforces that Circle 0 shows nothing at all
on the OPEN path — is unmodified and green. Naming the band is not surfacing it.

**Every `Limbo` occurrence earlier in this file is a historical profile reference**, written
when that was the profile's name, and is superseded by this section. `docs/BUILD-NOTES.md` is
append-only, so those records are left standing as what was true when they were written rather
than rewritten to say something they did not.

### 23.5 Evidence table

| Check | Result |
|---|---|
| Provenance gate `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit **0**, before every builder run |
| `tools/build_state_engine.py` / `tools/build_sentient.py` | exit **0**, three times each |
| Idempotence | a second consecutive build leaves both sources byte-identical (`1e5bf2bd…` / `567befdb…`) |
| No-op `plistlib` round trip before each guarded edit | 2,667,477 == 2,667,477; 2,667,711 == 2,667,711 |
| Twelve `docs/*.py` checks | all exit **0**, at all three task commit boundaries |
| Note identity, both forks | three sites agree on `PROSOCHĒ`, Name operator **99** |
| Attachment invariant, `src/` | **1,105** (Dumb) / **1,109** (Sentient) token strings, **0** offset mismatches |
| Attachment invariant, decrypted payloads | same counts, **0** mismatches |
| Test-a-Circle submenu | `WFMenuItems` == the nine case titles, element for element, both forks and both payloads |
| Note-body heading order | do-not-target < OPTIONAL HARDENING < THE NINE CIRCLES < MY PHONE, both forks |
| Profile menu | `['Paradise', 'Purgatory', 'Inferno']`, both forks and both payloads |
| Config literal keys | `thresholds` and `cooldown_seconds` keyed by exactly the three canticles; `Limbo` absent from both |
| Surviving `Limbo` | **3** sites per fork, every one a `Circle 1 · Limbo` label |
| Validator (gate A) ×2, `--target-macos 26 --target-platform all` | `Validation passed.`, exit 0 |
| Signed artifacts | 219,923 B / 224,186 B, canonical basenames, no suffix |
| Dated archive SHA-256 == `src/` counterpart | `1e5bf2bd…` == `1e5bf2bd…`; `567befdb…` == `567befdb…` |
| Decrypt-verify, both containers | `plutil -lint` **OK** ×2; `THE NINE CIRCLES` and `OPTIONAL HARDENING` present in each |
| `docs/manifest_check.py` after each refresh | passed, 6 rows verified against disk |
| `--target-macos 27`, `--target-platform ios`, `timeout` | never invoked |

**`DIST-03` is OPEN.** No iPhone is connected. Not one row above is behavioural evidence.

---

## 24. Panic Escape made removable, and the three-literal schema bump (phase 11 plan 05, 2026-08-17)

Build Addendum 01 §3. Panic Escape — the `Leaving` case of the menu PROSOCHĒ shows before an
intervention — is now removable, and the removal is reversible. Nothing about the safety
mechanism moved.

### 24.1 The distinction this plan exists to hold

**Panic Escape is not Emergency Restore, and conflating them is the failure the whole plan is
written to prevent.**

- **Panic Escape** is a *comfort*: the easy behavioural bypass offered before every primitive,
  in every sequence and every Circle. Some people find the option to leave is itself the thing
  they reach for automatically. It can be given up.
- **Emergency Restore** is a *safety mechanism*: it is what restores a screen a run left dim or
  a media volume a run left down. It is a manual menu item and one of the two options inside
  the live-cooldown redirect.

`panic_escape_enabled` **does not represent Emergency Restore, does not gate it, and no
conditional introduced by this plan encloses it.** That is threat `T-11-22`, the only
`critical` in this phase: a user with the bypass removed *and* Emergency Restore unreachable is
stranded inside an intervention. The separation is asserted structurally in the build, and
**re-asserted against both decrypted payloads** — measured there, not inferred from `src/`.

### 24.2 The mechanism chosen, and what it cost

**Mechanism A — gate the whole menu.** `universal_leaving()` now reads the flag and wraps its
existing block:

```
If Panic Escape Enabled > 0
    <the existing Leaving/Continue menu, unchanged>
Otherwise
    primitive_dispatch()          # the eleventh rendering
End If
```

The alternative — hoisting the dispatch out of the menu and terminating the `Leaving` path with
`is.workflow.actions.exit` — would have kept the rendering count at ten, but it restructures
the OPEN arm's control flow, which `verify_circle_zero_silence()`, `verify_router_shape()` and
`docs/router_ui_census.py` all reason about, and whether a trailing `exit` after
`record_exit_and_route()`'s own routing is needed or harmful was **unverified**. Mechanism A
touches the least structure, and this project's entire guard suite is built on structural
stability.

**Why gating preserves the invariant.** `verify_circle_zero_silence()` property (b) requires
**exactly one** `["Leaving","Continue"]` menu in the artifact, enclosed by the `Circle Next > 0`
silent band. Only the enabled arm emits it, so the count is still one.
`universal_leaving()` is called from inside the band, so **both** arms inherit the enclosure —
which is what keeps property (c) and the OPEN-arm surface census green for the otherwise arm's
new dotted `sequences.` read.

**The cost, paid deliberately: one extra `primitive_dispatch()` rendering — roughly 200
actions, and both environmental site-count tables move.**

### 24.3 The site counts — measured, and one number research got wrong

| Table | Before (10 renderings) | After (11 renderings) | Delta | What explains it |
|---|---:|---:|---:|---|
| `EXPECTED_SITES[setbrightness]` | 14 | **15** | +1 | one more `dimming()` |
| `EXPECTED_SITES[setvolume]` | 14 | **15** | +1 | one more `silence()` |
| `EXPECTED_SITES[getdevicedetails]` | 20 | **22** | +2 | one `Current Brightness` + one `Current Volume` |
| `expected_coerced[setbrightness]` | 14 | **15** | +1 | `Dim Target` is `read_value()`-sourced (Text), so every site needs the coercion |
| `expected_coerced[setvolume]` | 4 | **4** | **0** | `Silence Target` is `number()`-sourced, already Number-typed, so all 11 stay uncoerced |

`11-RESEARCH.md` §8.2 projected the coerced pair as **15 / 5**. The artifact measures
**15 / 4**. The projection was not supported by `docs/phase9_self_check.py`'s own derivation
comment, which already recorded `Silence Target x10 left uncoerced` — an eleventh rendering adds
an eleventh *uncoerced* volume site, not a coerced one. **The tables carry the measurement.**
Every delta above was read off the rebuilt forks and checked against the one thing that
changed; a delta larger than one rendering explains is a regression, and both files now say so
in their derivation comments.

The composite split moved 28 → **30** sites, 18 → **19** coerced.

### 24.4 The removal path — two acts, and why it lives where it does

Addendum §3 requires a manual edit **in the Note** plus an explicit confirmation. Neither act
alone changes anything.

1. **The Note.** A stable `## PANIC ESCAPE` section, inserted immediately before
   `## MY PHONE, ON PURPOSE`. That position is load-bearing: `manual_note_refresh()` **appends**
   a fresh `## CURRENT SETTINGS` block on every state-changing manual run, so a setting placed
   in an appended region would be shadowed by its own duplicates. The section carries exactly
   one editable line, `- Panic Escape: ON`, and prose that names Emergency Restore as
   unaffected.
2. **The confirmation.** A new eleventh manual menu item, `Panic Escape`, reads that one bounded
   section, compares it with the stored flag, and shows a two-item confirmation. Only the
   confirm case writes the flag, saves state and appends one ledger line. If the Note and the
   flag already agree, nothing is written and nothing is recorded.
3. **The restore direction is required, not optional.** Putting the word back to `ON` and
   choosing the same item offers the mirrored confirmation and writes the flag back to 1. A
   bypass a user cannot get back is not a choice they made.

**A measured correction to the plan's own reading.** The plan cited the `Sync My Profile`
branch as the precedent for putting the `gettext → text.match → set_value` chain *in the menu
case*. It is not there. `Control Room Note` is bound by the Find Notes / Create Note pair that
sits **after** the entire manual menu block, so a menu case cannot read the Note at all — and
`Sync My Profile` does not: its case body only raises `Manual Sync Requested`, and the parse
runs later in `manual_note_refresh()`. The Panic Escape branch is wired the same way, via
`Manual Panic Escape Requested`. Reading the Note from the menu case would have shipped a
runtime failure that no validator, catalog lookup or decrypt could see.

**Why not the OPEN arm.** §10 of this file makes it binding that OPEN and CLOSE never parse the
Note, on both cost and Notes-permission-prompt grounds, and `docs/router_ui_census.py` fails any
new OPEN-arm surface outside the silent band. A confirmation dialog on an app open is both.
Measured after the change: **no Note-parsing action entered the OPEN or CLOSE arm in either
fork.** (Sentient's OPEN arm does carry one pre-existing `text.match` — the Use Model output
token parse, `(ALLOW|CHALLENGE|DENY)`. It reads the model's reply, never the Note.)

**The match is bounded and unambiguous.** Pattern
`(?s)## PANIC ESCAPE.*?(?=## MY PHONE, ON PURPOSE)`, then condition **99** ("contains") over
that short section against the exact literal `- Panic Escape: OFF`. The leading `- ` and the
capitals are load-bearing, and the section's prose deliberately says *"change the word ON … to
OFF"* rather than quoting the whole line, so no prose sentence can trip the test. A missing or
reworded section yields an empty match, which fails the contains test and takes the otherwise
arm — so an unreadable Note can only ever **restore**, never remove.

### 24.5 Why the flag is flat and the gate is numeric

Both choices are forced by this project's verified runtime semantics (`.claude/CLAUDE.md`), not
chosen for style:

- **Flat, top-level.** A **dotted** read whose final segment is absent is a **hard error**. A
  nested `settings.panic_escape_enabled` could not be gated at all on a `state.json` written
  before the field existed — the read would raise before any conditional saw it. A **flat** read
  of a missing key returns nothing, no error.
- **Numeric `> 0`.** An existence gate (condition 100/101) reads **TRUE** for the string
  `"null"` and for `""` — exactly the states that must read as *removed*. That is the axis-7
  gate-semantics trap `verify_sentinel_gates()` exists to prevent. `> 0` reads false for `0`,
  missing, `null` and `""` under every device-measured coercion. Same idiom as Setup Check's two
  epoch keys.

**A new guard, `verify_panic_escape_seed()`,** asserts the seed value at the top level, forbids
any dotted read of the flag, and forbids a non-numeric condition code on it. It exists because
of a measurement: the plan asserted that `verify_state_seed()` covers every state read with a
seeded counterpart, and it does **not** — its read-side scan is scoped to keys rooted at
`settings_snapshot`, so an unseeded `panic_escape_enabled` would have passed the build and been
dead on every device.

**Deviation, recorded.** The plan instructed the seed be added to `src/PROSOCHE-Dumb.xml`
through `tools/plist_text_edit.py`. It was instead added by an idempotent **generator** pass,
`seed_panic_escape()`, matching the two existing precedents for the same template
(`seed_settings_snapshot()`, `seed_pending_exit()`). The edit mechanism is equivalent —
`_replace_in_token()` shifts every downstream attachment offset and re-asserts each lands on a
`U+FFFC` placeholder, which is the same guarded round trip — and `docs/note_identity_check.py`
independently re-verifies every offset in both forks. The gain is that the invariant is
re-established on every build rather than resting on a one-time hand edit. The Note body edit
**did** use `tools/plist_text_edit.py`, as instructed: the body is hand-authored source the
generator only reads.

### 24.6 The schema bump — three coupled literals, not two

`schema_version` moves **2 → 3**, implementing `docs/CAPABILITY-DECISIONS.md` **BD-06-A3**
Decision 1 verbatim. Without it the new bootstrap field never reaches a device that already
holds a valid `state.json`, and the removal path is dead there.

`fix_state_rebind()` hardcodes **three** literals, and they must move in the same commit:

| # | Literal | Role | What omitting it does |
|---:|---|---|---|
| 1 | template seed text | the value a rebuilt `state.json` is written with | every device rebuilds forever |
| 2 | the **recognition tuple** | how the transformer *locates* the version-check conditional | the **next** build aborts at `schema version check conditional not found` |
| 3 | the runtime validity-gate literal | what the device compares its stored version against | even a clean install fails the check it just wrote its file for |

Site 2 is the one plan 11-04 measured and that neither the plan nor `11-RESEARCH.md` Pitfall 7
had recorded — both described the bump as two literals. It fails **late**: the build that
performs the bump succeeds, and the one after it fails, pointing at a missing conditional rather
than at the bump. All three now derive from named constants (`SCHEMA_VERSION`,
`SCHEMA_VERSION_PREVIOUS`, `SCHEMA_VERSION_ACCEPTED`) so they cannot drift apart again, and the
template is asserted to carry an accepted version after the pass rather than assumed to.

**No migration, dual-key alias or read-time normalisation was built** — BD-06-A1 forbids all
three by name. The cost accepted is real and unrecoverable: a device that rebuilds discards
accumulated heat, gravity, pressure, `recent_sessions`, `recent_contracts`, the session record
and `exit_stats[*].samples`. It is free here only because BD-06-A1 Amendment 3 records that
PROSOCHĒ is undeployed. **The gate reinstates itself** if a real installed base ever exists.

### 24.7 Evidence table

Every row is **structural**. `DIST-03` is **OPEN**.

| Check | Result | Kind |
|---|---|---|
| Provenance gate `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit **0**, before every builder run | structural |
| `tools/build_state_engine.py` / `tools/build_sentient.py` | exit **0** | structural |
| Idempotence | a second and third consecutive build leave `src/PROSOCHE-Dumb.xml` byte-identical | structural |
| No-op `plistlib` round trip before the Note-body edit | byte-identical, asserted by `plist_text_edit.assert_noop_roundtrip()` | structural |
| Twelve `docs/*.py` checks | all exit **0** at the final commit (`manifest_check` after the refresh) | structural |
| Exactly one `["Leaving","Continue"]` menu | **1** per fork, in `src/` and in both decrypted payloads | structural |
| Emergency Restore surfaces | **2** menus + **2** case bodies per fork, **none enclosed by a Panic Escape conditional**, measured on both payloads | structural |
| `Emergency Restore` literal occurrences | **7** at the phase baseline → **14** per fork; increased, never reduced | structural |
| `panic_escape_enabled` seeded flat, top level, `== 1` | asserted by `verify_panic_escape_seed()` and read back from the template JSON | structural |
| Every Panic Escape gate's condition code | **2** (greater than); zero condition-100/101 gates | structural |
| Dotted reads of the flag | **0** | structural |
| Both write directions | **2** `setvalueforkey` writes, in **2** distinct control-flow groups, per fork | structural |
| Manual menu | **11** items; every `choosefrommenu` group's `WFMenuItems` == its ordered case titles, both forks | structural |
| Note section order | `## PANIC ESCAPE` precedes `## MY PHONE, ON PURPOSE`; `Emergency Restore` **689** characters after the heading | structural |
| Note-parsing actions in the OPEN / CLOSE arms | **0** in both forks | structural |
| Attachment invariant, `src/` and payloads | **1,205** (Dumb) / **1,209** (Sentient) token strings, **0** offset mismatches | structural |
| Note-body attachment offsets after the 1,157-character insert | 6982 / 7013 → **8139 / 8170**, exactly the inserted length | structural |
| Site counts | **15 / 15 / 22**, coerced **15 / 4**, in `src/` and both payloads | structural |
| `schema_version` | template **3**; runtime validity-gate literal **"3"**; both present in both payloads | structural |
| Validator (gate A) ×2, `--target-macos 26 --target-platform all` | `Validation passed.`, exit **0** | structural |
| Signed artifacts | **233,976 B** / **238,171 B**, canonical basenames, no suffix | structural |
| Dated archive SHA-256 == `src/` counterpart | `7ddd94b7…` == `7ddd94b7…`; `c04f7364…` == `c04f7364…` | structural |
| Decrypt-verify, both containers | `plutil -lint` **OK** ×2; `## PANIC ESCAPE` ×5 and `panic_escape_enabled` ×7 in each | structural |
| `docs/manifest_check.py` after the refresh | passed, 6 rows verified against disk | structural |
| `--target-macos 27`, `--target-platform ios`, `timeout` | never invoked | — |

**What is NOT established.** No iPhone is connected and no device has run either build. That a
user editing the setting line and confirming actually removes the bypass; that the restore
direction actually restores it; that the bounded `text.match` binds to the intended section on a
Note carrying appended `## CURRENT SETTINGS` blocks; that the numeric `> 0` gate resolves as
intended against a Text-coerced operand on device; and that a device holding
`"schema_version": "2"` takes the rebuild branch — **all unobserved**. Structural proof is not
behavioural proof.
---

## 25. The Dumb→Core / Sentient→Aware rename, and the first Aware-side divergence (phase 11 plan 06, 2026-08-17)

Build Addendum 01's product rename, landed at every site where the name is load-bearing, and
the closing rebuild of phase 11. **Pure append: this section adds text and deletes none.**

### The two canonical display names

| Was | Is |
|---|---|
| `PROSOCHĒ — Nine Circles — Dumb` | **`PROSOCHĒ — Nine Circles — Core`** |
| `PROSOCHĒ — Nine Circles — Sentient` | **`PROSOCHĒ — Nine Circles — Aware`** |

**The filename is the sole carrier of a shortcut's display name — re-measured on this build,
not inherited from the record.** Both signed containers were decrypted through the AEA1 recipe
in `.claude/CLAUDE.md` §8, and neither recovered `Shortcut.wflow` contains a `WFWorkflowName`
key at all, though both `src/*.xml` files set one: the signer strips it, and the AEA1 auth data
holds only `SigningCertificateChain`. Everything else about this rename follows from that one
measurement. A suffixed or mismatched basename would import as a second, differently named
library entry that the user's two Personal Automations do not reference — a silently dead
install. `sign-shortcut --name` was therefore passed the exact display name for each fork; left
to itself the signer defaults to the INPUT basename, which here would have produced
`PROSOCHE-Dumb`.

### §9 is discharged, not overridden

`docs/BUILD-NOTES.md` §9 binds any rename of the shipped shortcut to updating **both** of the
Control Room Note's automation sections, and states that the signer must agree with the Note
rather than the reverse. Both sections were updated first, in `src/PROSOCHE-Dumb.xml`, through
`tools/plist_text_edit.py`'s offset-recomputing round trip; the signer was then given the same
string. The Note's own `## READ THIS FIRST` gained one paragraph stating the rename, the stale
library entry it leaves behind, and that both automations must be re-pointed by hand.

### The `src/*.xml` source filenames are deliberately NOT renamed

They still read `PROSOCHE-Dumb.xml` and `PROSOCHE-Sentient.xml`. Ten code files and roughly
seventy planning documents reference them, every historical plan's reproducibility depends on
them, and Build Addendum 01 renames the **products**, not the sources. Recorded here so a later
phase reads the mismatch as a decision rather than an oversight.

### The first Aware-side content divergence, and the proof that survived it

Before this plan, `tools/build_sentient.py` made exactly three kinds of change to the forked
Dumb source — the icon and import question, `WFWorkflowName`, and the audit-block insertion —
and touched neither the Note body, the Note title nor the `"fork"` seed. **The measured
consequence was a defect that shipped in every previous Sentient build:** its Note named the
Dumb fork's shortcut in both automation steps and its settings block read `- Fork: Dumb`. The
defect was recorded as a Deferred Item by quick task `260817-au7` and explicitly assigned to
this phase.

`fix_fork_strings(actions)` closes it. Three sites, each with an expected occurrence count so
that a missed or duplicated site fails the build rather than shipping: the Note's two Run
Shortcut targets, the Note's settings-block fork label, and the bootstrap `state.json` fork
seed. It runs **before** the `normalise_*` / `verify_*` chain, so the rewritten token strings
pass the same envelope, output-name and offset guards as everything else, and it mutates the
forked copy only — the frozen-source assertion still holds. It does **not** touch the Note
title, which is identical in both forks on purpose and out of this plan's scope. The failure
path was exercised deliberately: reducing one expected count from 2 to 1 makes
`tools/build_sentient.py` exit non-zero naming the dead-install consequence, and the count was
then restored.

That divergence makes `docs/sentient_core_check.py`'s whole-list equality
`sa[:6] + sa[8:marker] + sa[end + 1:] == da` false **by design**. It was not deleted — deleting
it would discard the only proof that nothing *else* diverged. It was replaced by a
**fork-normalised** equality: the inverse substitution is applied to a deep copy of the Sentient
action list, with an exact expected count per site, recomputing every `attachmentsByRange`
offset because `Aware` is one character longer than `Core` and sits upstream of every
attachment in both edited strings. A bounded, counted normalisation cannot absorb an unrelated
drift. It is paired with a **positive** assertion — the Aware Note names the Aware display name
at least twice and the Core display name exactly zero times, and its fork seed reads `Aware` —
so the normalisation cannot mask a genuine defect by quietly rewriting one. The file carries a
comment naming this plan and saying why the stricter form must not be restored.

### The offset asymmetry, stated because it is the trap

`Dumb` → `Core` is length-neutral, so the bootstrap seed's four attachment offsets survive that
edit **by luck**. `Core` → `Aware` is one character longer and sits upstream of all four, so
the same seed's offsets **do** move on the Sentient side. Both edits were therefore made
through the offset-recomputing round trip rather than reasoning about which happened to be
safe. A second trap sits next to it: the bootstrap seed is a `WFTextTokenString` **dict** with
four attachments and real `U+FFFC` placeholders, while the Config literal is a plain `str` with
zero placeholders — opposite envelopes, adjacent in the same file. A plain-`str` filter finds
the Config literal and misses the seed entirely.

### The old-named signed artifacts were deleted

Per `docs/CAPABILITY-DECISIONS.md` BD-06-A3 Decision 2, applied rather than re-decided:
`PROSOCHĒ — Nine Circles — Dumb.shortcut` and `PROSOCHĒ — Nine Circles — Sentient.shortcut`
were removed in the same commit that wrote the new-named signed artifacts.
`docs/manifest_check.py` cannot see an orphaned file, so retention would have been an unchecked
state; both deleted files were git-tracked, so `git show` recovers their exact bytes. The dated
archives under `artifacts/shortcuts/2026-08-*/` keep their old names as history and were not
touched.

### Closing evidence table — phase 11 plan 06

Every row **structural**. `DIST-03` is open: no iPhone is connected and no build in this phase
has run on a device.

| Evidence | Result | Kind |
|---|---|---|
| Provenance gate `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit **0**, before every builder run | structural |
| Twelve `docs/*.py` checks, baseline before any edit | **12/12 green** | structural |
| Twelve `docs/*.py` checks, final | **12/12 green** | structural |
| Builder idempotence | a second consecutive `build_state_engine.py` + `build_sentient.py` leaves both sources byte-identical (`12bbfe31…`, `ef431b5d…`) | structural |
| Root `WFWorkflowName` | Core source `PROSOCHĒ — Nine Circles — Core`; Aware source `PROSOCHĒ — Nine Circles — Aware` | structural |
| Core Note, decrypted payload | Core display name **×2**, Aware **×0**, `Dumb` **×0**, `Sentient` **×0** | structural |
| Aware Note, decrypted payload | Aware display name **×2**, Core **×0**, `Dumb` **×0**, `Sentient` **×0** | structural |
| Fork seeds, decrypted payloads | `"fork": "Core"` ×1 / `"fork": "Aware"` ×1 | structural |
| `WFWorkflowName` in either recovered payload | **absent** — the signer strips it; the filename is the sole carrier | structural |
| Phase deliverables in both payloads | `Loud Mirror` ×25, `PANIC ESCAPE` ×5, `THE NINE CIRCLES` ×1 | structural |
| `fix_fork_strings` failure path | expected count 2 → 1 makes `build_sentient.py` exit **1** naming the dead-install consequence; restored | structural |
| `docs/note_identity_check.py` | **0** attachment-offset mismatches; 1,205 (Core) / 1,209 (Aware) token strings | structural |
| Validator gate A ×2 | `Validation passed.`, exit **0** | structural |
| Signed artifacts | **234,370 B** / **238,668 B**, basenames exactly the two canonical display names, no suffix | structural |
| Dated archive SHA-256 == `src/` counterpart | `12bbfe31…` == `12bbfe31…`; `ef431b5d…` == `ef431b5d…` | structural |
| Decrypt-verify | `plutil -lint` **OK** ×2 | structural |
| `artifacts/shortcuts/*.shortcut` | exactly **2** files, both canonical | structural |
| `docs/manifest_check.py` after the refresh | passed, 6 rows verified against disk | structural |
| `git status --short -- artifacts/shortcuts/2026-08-` | empty — the dated historical archives were not touched | structural |
| `--target-macos 27`, `--target-platform ios`, `timeout` | never invoked | structural |

### What this does NOT establish

**DIST-03 is open.** Nobody has imported either renamed build, followed the renamed automation
steps, or re-pointed a Personal Automation from an old entry to a new one. That the rename is a
breaking change is a **reasoned consequence** of the stripped-`WFWorkflowName` measurement, not
an observation of a device failing. Structural proof is not behavioural proof, and nothing here
is device-verified.

## 26. Phase 12 — the third key nobody named: `profile_snapshot.create_target_url` (plan 12-04, 2026-08-17)

`12-RESEARCH.md`'s full-codebase sweep generalised beyond the two chartered keys
(`exit_events`, `active_session`) and found a third: `route_exit()`'s Create branch performs
a **dotted** read of `profile_snapshot.create_target_url` from `Reloaded State`, and that leaf
was not part of the bootstrap seed even though `profile_snapshot` itself is (`goal`,
`phone_purpose`, `reclaim_for`, `deliberate_leisure_definition`, `enabled_exits`,
`synced_at`, `note_content_hash`). Choosing Create on a clean install hard-errors at that
read, **after** `exit_events`, both `pending_exit` leaves and `exit_selection_counter` have
already been written and `save_state("Reloaded State")` has already run — the single most
likely first-exit crash in the phase surface (`T-12-18`).

**Decision, Task 1 checkpoint (`gate="blocking"`, resolved `option-a`):** sentinel seed
(`CLEARED_SENTINEL`) plus a condition-5 leaf gate — the planner's own recommendation (PD-2).
Recorded at
`.planning/phases/12-state-shape-sentinel-gaps-exit-events-and-active-session/.create-target-url-option`.

**Why option A, not B or C.** The Create branch's first gate is a has-any-value
(condition-100) test over the value read from state. If the seed were a JSON `null` (option
B) and `read_value()` — `getvalueforkey` followed by `gettext` — resolved that leaf to the
text `"null"` rather than no-value, the gate would read TRUE and `openurl` the literal string
`"null"` on every clean-install Create exit, silently, with no error message. Nothing in this
repository settles whether a JSON-null leaf coerces to no-value or to the text `"null"` under
a has-any-value test; `.claude/CLAUDE.md`'s verified runtime-semantics table documents
`"null"` coerced to a **Number** as false, but says nothing about `null` coerced to **Text**
under `has any value`. Settling it needs a rung-2+ probe this phase declined to spend.
Option A avoids the bet entirely: every element it uses is already device-verified in this
repository — a dotted read of an existing string leaf resolves to the string
(`pending_exit.type` does exactly this on the OPEN critical path), and condition 5 ("string
is not" `CLEARED_SENTINEL`) is this project's standard set/unset gate, demonstrated at
`complete_pending_exit()`. Option C (defer under a named exemption) was rejected because it
would leave a known dotted read of an unseeded leaf on the exact exit path this phase exists
to make survivable, one plan after `KNOWN_SENTINEL_EXISTENCE_GATES` was emptied to zero.

**Implementation.** `CREATE_TARGET_URL_SEED = CLEARED_SENTINEL`; `seed_create_target_url()`
inserts `"create_target_url": "null",` immediately **before** the `"note_content_hash": null`
line (`profile_snapshot`'s trailing, comma-less final key), so the object stays valid JSON
without a second edit to add or remove a comma. Registered in `main()` before
`fix_state_rebind()`, alongside `seed_exit_events()` and `seed_active_session()`.
`route_exit()`'s **first** Create-branch gate (over the state read) converts from
`if_block("Create Target URL", 100)` to `if_block("Create Target URL", 5,
string=CLEARED_SENTINEL)`; the **second** gate (over the Ask action's `Provided Input`, a
transient user input whose unset representation is genuinely empty) is left at condition 100,
untouched, with an inline comment naming why the two gates in one branch now carry different
condition codes. The `Create Owner ID` condition-4 ownership compare and its
`WFConditionalActionString` idiom are unmodified.

**Verified:** exactly 4 mode-0 conditionals test `Create Target URL` per fork (`route_exit()`
renders twice, two gates per render) — 2 carry condition 5, 2 carry condition 100, resolved
via `_tested_variable()`; the emitted `profile_snapshot.create_target_url` equals
`CLEARED_SENTINEL` on both `src/PROSOCHE-Dumb.xml` and `src/PROSOCHE-Sentient.xml`;
`docs/phase6_self_check.py` exits 0 (six exit routes survive, double build byte-idempotent);
gate A (`--target-macos 26 --target-platform all`) prints `Validation passed.` on both forks.

## 27. Phase 12 — the recording duty: assumptions, decisions and the ship gate (plan 12-05, 2026-08-17)

The closing plan of this phase. Everything below discharges `.claude/CLAUDE.md` §9's recording
duty — "a probe's result is recorded, not consumed" — for every assumption carried, decision
taken, and research correction measured across plans 12-01 through 12-05. This section is
this phase's single point of reference; nothing here is repeated elsewhere in this document
except by cross-reference to §26 above, which already carries `create_target_url`'s full
decision record.

### Assumptions carried, each with its status and settling rung

- **A1** — `is.workflow.actions.repeat.each` over an **empty** array. `[ASSUMED]` a
  zero-iteration no-op. **Unsettled at the close of this phase.** Settleable at evidence
  rung 2 — a simulator probe; needs no Notes app, no Apple Intelligence, no Personal
  Automation, no real hardware. **Planner decision PD-1 (below): deliberately not spent.**
  `seed_exit_events()` fixes the ABSENT case either way a probe might resolve, so a rung-2
  probe could not change one line of shipped code — it would only change how severely A1's
  entry here is framed. Recorded as reasoning, not just verdict, so a later reader does not
  reopen it as an oversight rather than a considered pass.
- **A2** — a dotted read whose **final** segment is missing raises identically to one whose
  **intermediate** segment is missing. HIGH confidence, but this is inference from two
  written records — `.claude/CLAUDE.md`'s "any missing segment" runtime-semantics wording,
  and the generator's own comment at the `sequences.<Sequence>.<Dispatch Circle>` read site —
  not a fresh device measurement made in this phase. It is what makes
  `profile_snapshot.create_target_url` (§26) a genuine defect rather than tidying: without A2,
  there would be no basis to expect the Create branch's dotted read to hard-error on a leaf
  the container-level key already has neighbours for. Still unsettled at any rung above
  inference at the close of this phase.
- **A3** — "no installed base to protect" (`docs/CAPABILITY-DECISIONS.md` BD-06-A1
  Amendment 3, `:550`) was re-confirmed as this phase's schema-bump precondition before Plan
  12-01 moved `schema_version` 3→4 — Amendment 3 is unchanged from the value Plan 12-01 read
  it at, and this phase added no new instance of the assumption; it merely spent the one
  Phase 11 already banked. What the bump costs if that record is ever wrong: heat, gravity,
  pressure, the rolling windows and every `exit_stats[*].samples`, with no migration, no
  dual-key alias and no read-time normalisation — all three forbidden by name in this
  project's stated conventions. Recorded here because this is the phase that spent it, not
  because this phase re-measured it.
- **A5** — `set_value` on a dotted key whose leaf does not yet exist creates the leaf. Already
  relied on in shipped builds before this phase (`persist_contract()`'s renders, among
  others). The four-leaf `active_session` seed (Plan 12-02) removes the dependency on this
  specific assumption for every `active_session.*` write this phase touches — the four leaves
  now always pre-exist before any `set_value` reaches them — but the assumption itself
  remains load-bearing elsewhere in the generator and is not independently re-verified here.

### Decisions taken by the planner, each with its rationale

- **PD-1** — no simulator probe spent on A1 (above). `.claude/CLAUDE.md` §9's own rule:
  "never climb higher than the open question requires." A1's fix is byte-identical whichever
  way the empty-array question resolves, so a rung-2 probe would answer a question with no
  code consequence, at the cost of building, signing and importing a probe artifact that is
  itself a new defect surface.
- **PD-2** — `create_target_url`'s seed value and gate shape, resolved at Plan 12-04's Task 1
  checkpoint to **option-a** (sentinel seed plus a condition-5 leaf gate), the planner's own
  recommendation. Full comparison against options B and C, the implementation, and the
  verified evidence are recorded in full at §26 above — this entry exists only so the phase's
  decision inventory is complete from this section alone; §26 remains the canonical record.
  This is a **one-way** decision: `route_exit()`'s Create branch now assumes the sentinel
  shape permanently, and reverting it would require a fresh schema consideration rather than
  a bare code revert.
- **PD-3** — the Aware fork's pre-existing verifier gap was closed **completely**, not
  partially, in Plan 12-01: `verify_pending_exit_seed`, `verify_panic_escape_seed`,
  `verify_compound_value_reads` and `verify_conditional_action_string` were armed in
  `tools/build_sentient.py` alongside the two new guards this phase introduced
  (`verify_exit_events_seed`, `verify_active_session_seed`). Measured outcome: **all five
  passed** on first arming, and the Aware fork's digest was byte-identical before and after —
  direct evidence the newly-armed guards are pure assertions, not transforms. "Fix whole
  classes, never site-by-site" (`.claude/CLAUDE.md`, Debugging technique) applied to a
  verifier-coverage gap, not only to a generator defect.

### Measured corrections to the phase research

- **`verify_state_seed()`'s generalisation is not a pure deletion.** Both `12-RESEARCH.md`
  and `12-PATTERNS.md` described the change as "delete the `settings_snapshot` root filter."
  Measured against the live tree in Plan 12-04: that filter was doing two jobs at once —
  scoping to one key family **and** scoping to reads of the right dictionary. Deleting it
  alone would have tested 74 legitimate `Config` and `Previous Session` reads against the
  bootstrap seed and failed the build. The correct change **adds** a source-variable filter,
  `STATE_READ_SOURCE_VARIABLES = ("State", "Reloaded State")`, filtering by the measured
  `WFInput.Value.VariableName` accessor path, alongside deleting the old key-root filter.
  Measured per-source read counts at that commit: **`State`** 141 literal / 6 composite,
  **`Reloaded State`** 44 literal, **`Config`** 30 literal / 23 composite, **`Previous
  Session`** 3 literal. Only the first two source variables are in scope for the generalised
  guard; `Config` and `Previous Session` reads are excluded by dictionary identity, not by key
  name.
- **`route_exit()`'s Create branch needed no gate change under the new container-as-invariant
  shape.** `12-RESEARCH.md` flagged the branch's bare `active_session.id` dotted read,
  followed by a condition-4 ownership compare, as missing an enclosing existence gate under
  the *old* shape (where `active_session` could be JSON `null`). Once Plan 12-03 made the
  container a seeded, permanent invariant, that same bare read became the **correct** target
  shape — the exact idiom every other owner site converged on — and "fixing" it would have
  been a regression. Plan 12-03 made zero code changes at this site and recorded the reason
  explicitly at the site and in its own commit body; recorded again here so a later reader
  does not "fix" it back a second time.
- **`open_pipeline()` writes four leaves, not three.** The bootstrap research's plan for the
  container→leaf write conversion enumerated `.id`, `.started_at`,
  `.declared_duration_seconds`. Plan 12-03 added a fourth: `.intention` is explicitly cleared
  in the same write block even though nothing reads it today, specifically to reproduce the
  old wholesale-replace semantics exactly — the former container write destroyed any prior
  `.intention` on every OPEN, and leaving the fourth leaf unwritten would let stale
  cross-session data survive as unintentional drift the container write never permitted.
- **The product display names are `Core` / `Aware`, not `Dumb` / `Sentient`.**
  `.claude/CLAUDE.md` was not updated at Phase 11 plan 06's rename and carried the stale
  literals forward into `12-CONTEXT.md`. This phase's own artifacts — `MANIFEST.md`,
  `docs/manifest_check.py`'s `DISPLAY_NAMES`, both signed `.shortcut` basenames, and this
  BUILD-NOTES section — all use the live names. No functional code was affected; this is a
  planning-document correction only.

### Gate B baselines — verbatim, indices as measured at this plan's rebuild

Both runs are standalone, advisory, never `&&`-chained into anything (`.claude/CLAUDE.md`
§1). Each shows **exactly one** line — the permitted `com.apple.mobilenotes.SharingExtension`
/ `WFCreateNoteInput` waiver — and nothing else, confirming Plan 12-03's nine moved emission
sites introduced no parameter-key or picker-literal regression.

```
$ validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 27 --target-platform all
Validation failed:
First failing action: index 0 (is.workflow.actions.comment)
- Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index 4192:
  WFCreateNoteInput. ToolKit v78 expects: OpenWhenRun, contents, folder, interpretAsMarkdown,
  name.
```

```
$ validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 27 --target-platform all
Validation failed:
First failing action: index 0 (is.workflow.actions.comment)
- Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index 4260:
  WFCreateNoteInput. ToolKit v78 expects: OpenWhenRun, contents, folder, interpretAsMarkdown,
  name.
```

Both indices moved down from Plan 12-01's own recorded baseline (Core 4302, Aware 4370) —
consistent with, though not independently attributed to, Plan 12-03's net action-count
reduction from converting eleven `persist_contract()` renders, two `record_exit_and_route()`
renders and `close_pipeline()`'s reload gate from a flat-read-plus-existence-gate pair to a
single leaf read, and from replacing `open_pipeline()`'s wholesale container write with four
leaf writes (a net reduction of three actions there alone). The waiver text itself is
unchanged and remains the single permitted finding on either fork. Gate B stays advisory and
is never `&&`-chained into any definition of done, per `.claude/CLAUDE.md` §1.

### `docs/CAPABILITY-DECISIONS.md`

**Untouched by this plan.** Plan 12-05 Task 2's device UAT (`12-UAT.md`) resolved
**BLOCKED** — `xcrun devicectl list devices` reported "No devices found." on 2026-08-17, the
same DIST-03 gap that blocked `09-UAT.md` and `10-UAT.md` — so no device observation exists
for this phase to settle a capability question with. An empty capability record is the
correct outcome here, not a speculative one: nothing about the exit-recording path's
real-device behaviour is known beyond what Plan 12-05 Task 1's decrypted-artifact inspection
proved structurally (schema_version 4, a four-leaf `active_session`, `exit_events == []` in
both recovered bootstrap templates).

## 28. Phase 13 — the recording duty: three decrypts, a refutation, and two guards (plan 13-03, 2026-08-17)

The closing documentation plan of this phase. Everything below discharges
`.claude/CLAUDE.md` §9's recording duty — "a probe's result is recorded, not consumed" — for
the donor decrypts, the measured inventories, the refutation of two recorded counts, and both
guards' verbatim sensitivity evidence produced across plans 13-01 and 13-02. Nothing here is
re-derived: every figure and every quoted message is transcribed from `13-01-SUMMARY.md`,
`13-02-SUMMARY.md` or `13-RESEARCH.md`'s measured tables.

**Why this section exists at all.** This phase was blocked for three cycles, and the reason was
not difficulty: the donor evidence was on disk the whole time and nobody ran the decrypt. Once
it was run, the failure mode shifted from "nobody looked" to "somebody reads the stale record
and re-litigates it". That is what this section, and the tombstones it points at, exist to
prevent.

### The decrypts

All three donors were decrypted with the `.claude/CLAUDE.md` §8 recipe (`python3` auth-data
extraction → `openssl x509` public key → `aea decrypt` → `aa extract` → `plutil -convert xml1`).
**All three succeeded on the first attempt.**

| Donor | Status before | Result | What it settles |
|---|---|---|---|
| `.planning/debug/Donor 5.shortcut` | on disk since cycle 14, **never analysed** | 196-line plist | The conditional TEXT-slot operand envelope — settles it as **already correct** |
| `.planning/debug/Donor 4.shortcut` | shape "recovered" but never applied | 224-line plist | The `WFItems` row wrapper, the `WFItemType` integer, and the bare-string row case |
| `.planning/debug/Donor 4.1.shortcut` | shape "recovered" but never applied | 235-line plist | The same wrapper, byte-identical on that action, plus the numeric-conditional RHS slot and the coercion aggrandizement |

Both shapes are recorded as first-class decision records in `docs/CAPABILITY-DECISIONS.md` —
`BD-07` (Donor 5) and `BD-08` (Donors 4 / 4.1) — so they are recoverable from `docs/` alone
without this phase's planning directory.

### The measured site inventory, per fork

Every figure below was measured by loading `src/PROSOCHE-Dumb.xml` (Core) and
`src/PROSOCHE-Sentient.xml` (Aware) with `plistlib` and walking the action array — first at the
pinned phase-start SHA `698ab99`, then again after each fix.

**Family 1 — `WFConditionalActionString` (the "Donor 5" family).** No site was changed by this
phase; the pre- and post-fix columns are identical *by design*, and a difference in either
would have been a failure of plan 13-02 rather than evidence of its success.

| Measure | Core (pre → post) | Aware (pre → post) |
|---|---|---|
| Total actions in artifact | 4346 | 4414 |
| Mode-0 conditionals carrying `WFConditionalActionString` | 192 → 192 | 195 → 195 |
| …variable-bearing `WFTextTokenString` (the Donor 5 family) | **20 → 20** | **20 → 20** |
| …condition-code split of those | 19 × code 4, 1 × code 99 | 19 × code 4, 1 × code 99 |
| …raw-literal comparison targets | 172 → 172 | 175 → 175 |
| Bare abandoned `"￼"` placeholders (the already-guarded defect) | 0 → 0 | 0 → 0 |
| Sites failing the Donor-5 shape | **0 → 0** | **0 → 0** |

**Family 2 — the `WFItems` List row wrapper.** One emitter changed; every figure below moved as
a consequence of that single branch. The figures are identical on both forks at every stage,
because Aware forks the *built* Core source and inherits the whole Mirror block unchanged.

**Three stages, not two.** 13-01 fixed the missing wrapper; the phase code review (CR-01) then
found that 13-01's `isinstance(item, str)` discriminator had over-wrapped in the other
direction, and a third stage corrected it. Reporting only "pre → post" is what made CR-01
invisible to a reader auditing the record rather than the artifact, so all three stages are
carried here.

| Measure | phase start | after 13-01 | after CR-01 (**what ships**) |
|---|---|---|---|
| `is.workflow.actions.list` actions | 67 | 67 | 67 |
| `WFItems` rows, total | 666 | 666 | 666 |
| …**raw `WFTextTokenString`** rows (no framing at all) | **660** | **0** | **0** |
| …rows wrapped `{WFItemType: 0, WFValue: …}` | 0 | 660 | **616** |
| …of those, **attachment-bearing** (correctly wrapped) | 0 | 616 | **616** |
| …of those, **attachment-free** (wrongly wrapped, CR-01) | 0 | **44** | **0** |
| …bare `<string>` literal rows | 6 | 6 | **50** |
| Per-action row counts | `[6] + [10]*66` | unchanged | unchanged |

**The 660 figure was described as "variable-bearing" and it was not.** 44 of the 660 rows 13-01
wrapped carry an **empty** `attachmentsByRange` — they are literal rows by content, and Donors 4
and 4.1 write a literal row as a bare `<string>`. The inventory was numerically right and
semantically wrong. The correct statement of what 13-01 did is **"660 rows wrapped, of which 616
were attachment-bearing and 44 were attachment-free literals"**; the correct statement of what
ships is **"616 wrapped + 50 bare"**. The 44 all sat at row position 8 — the row
`getitemfromlist` selects at **Circle VIII** on both the success and the lapse family.

### The refutation, stated plainly

Two figures carried in the project record are wrong. Both are **REFUTED** by direct measurement
of the artifacts at HEAD, and this subsection is the durable record of that.

| Family | The recorded claim | Measured | Verdict |
|---|---|---|---|
| 1 | 14 `WFConditionalActionString` sites are defective and need a by-class sweep | 192 / 195 slots, of which 20 / 20 are variable-bearing and **all** match Donor 5 | **REFUTED — zero defective sites.** The deliverable inverted from a sweep into a pin |
| 2 | the `WFItems` wrapper affects "2 confirmed instances" | **66 defective actions carrying 660 unwrapped rows, per fork** | **REFUTED — under-counted actions by 33× and rows by 330×** |

Two further corrections belong to the same refutation and must not be smoothed over:

- **The site the ROADMAP named as a concrete starting point is not a member of the family.**
  `if_block("Previous Respected", 4, ...)` passes a **raw Python literal** (`string="true"` /
  `string="false"`), never a `token()`, so it has no variable in the text slot at all. Its left
  operand is genuinely Text-typed (`getvalueforkey` → `gettext` → `setvariable`, which is
  `read_value()`'s chain), and a Text left operand with condition 4 is the *valid* pairing per
  `.claude/CLAUDE.md` § "Operator/operand type validity". Variable definedness was checked
  too: `Previous Respected` is set at action index 368 and all 44 uses occur at index 375 or
  later, so **zero** uses precede the set and there is no dangling reference to render red.
  This is a **corrected attribution**, not a discovered second defect — the "concrete starting
  site" was a false lead, and the todo's own hedge ("*very likely* one of the already-catalogued
  sites") was a guess that measurement falsifies.
- **The screenshot both records cite does not exist.** `.planning/debug/Screenshot 2026-08-14 at
  11.55.12 pm.png` is absent from this worktree, absent from the main checkout, and absent from
  git history (`git log --all -- '*.png'` returns only the initial refactor commit) — verified
  three ways. Its recorded filename also contains a **U+2060 word joiner** between `11.55.12`
  and `pm`, so this is not merely a path-quoting problem. **No task in this phase depended on
  reading it.** Both defects it allegedly showed were established independently and more
  precisely — family 2 by direct measurement, family 1 by donor refutation — so nothing is
  lost. If the user still holds the image it is a rung-4 item worth requesting for the
  historical record only, never as a gate.

Every record that asserted either count has been corrected in place or annotated with a dated
tombstone: the ROADMAP milestone checklist bullet and the Phase 13 section prose,
`.planning/debug/HANDOFF.md` at five sites (originals preserved as history), and the pending
todo, closed into `.planning/todos/completed/` carrying a standalone tombstone. The closure was
proven by a whole-tree sweep over six literal phrasings across `.planning/` and `docs/`, not by
an enumeration of remembered sites — a section-scoped edit measurably leaves sites uncorrected,
which is precisely how a refuted count survives to be re-litigated.

**Three exemptions, not two — and the third was found by the phase's own verifier, not by the
sweep.** The declared exemptions are `.planning/todos/completed/` and `.planning/phases/13-*/`,
where the historical wording must survive in order to *be* the tombstone. The verifier then found
**nine** further assertions of the 14-site count in `.planning/debug/resolved/open-routing-sequence-error.md`
— lines 810, 931, 1037, 1044, 1197, 1203, 1270, 1277, 4667 — phrased `THE 14 WFConditionalActionString
SITES` and `at 14 sites`, which none of the six chosen literals matches. `.planning/debug/resolved/`
is hereby the **third declared exemption**, on the same rationale as the first two: it holds closed,
archived audit trails, and each of those nine lines is a per-cycle historical record of what was
*believed at that cycle* ("carried forward unchanged from cycle 8"). Annotating them individually
would rewrite the audit trail the refutation's credibility rests on. A single dated `REFUTED` banner
has been added at the head of that file instead, so a cold reader meets the correction before the
history.

**The honest lesson, recorded because it cost nothing here and could cost a cycle later:** a
literal-phrasing sweep closes only the phrasings it enumerates. Six literals left nine sites
standing in a file the phase goal names by name. The sweep is a floor, not a proof of closure —
which is exactly the failure mode it was built to prevent, reappearing one level up.

### The two guards

| Guard | File | Asserts | Registered | Armed on |
|---|---|---|---|---|
| `verify_list_item_wrappers()` | `tools/build_state_engine.py` | The **whole row contract**: no `WFItems` row is a dict lacking a `WFItemType` key (the **key's presence only**, never its value); `WFValue` is present and well-shaped; and a wrapped row's `WFValue.Value.attachmentsByRange` is **non-empty** — the inverse assertion added during the 13 code-review pass, which catches an attachment-free (literal-by-content) token wrongly encoded as a variable row. Census-pinned at `67` List actions / `616` wrapped / `50` bare per fork | `main()`'s verify chain, after `verify_conditional_action_string()` and before `verify_numeric_operands()`, strictly above the single `SOURCE.write_bytes()` — **anchor on the symbol, not the line**: the AST call-precedes-write relation is the invariant, and the specific line numbers move on every edit (measured `4448` < `4472` after the code-review fixes; an earlier revision of this table recorded `4248` < `4272` and went stale by 200 within the same phase) | **both forks** — new to this phase |
| `verify_conditional_action_string()` | `tools/build_state_engine.py` | *(pre-existing)* no comparison target holds the abandoned bare `￼` placeholder; **and, new in 13-02,** every variable-bearing target positively *is* a `WFTextTokenString` with a `￼` in `Value.string` and a non-empty `Value.attachmentsByRange` | already in `main()`'s chain since Phase 12 | **both forks** — already armed |

**The Aware fork needed two new touch points for the new guard and none for the extended one,**
and both facts are recorded deliberately rather than left to inference. `tools/build_sentient.py`
has *two* independent arming sites — the `from build_state_engine import (...)` list and a
separate bare-call guard block — and Phase 12 regressed by editing only one. Plan 13-01 hit
both for `verify_list_item_wrappers` (added in alphabetical position between
`verify_exit_events_seed` and `verify_numeric_operands`). Plan 13-02 added **zero** new touch
points, because `verify_conditional_action_string` was already imported and already invoked,
armed by Phase 12's PD-3 sweep; only its per-fork justification comment changed. An unstated
absence would read exactly like the two-touch-point regression Phase 12 actually committed —
hence it is stated.

Both armings were proven by **AST assertion**, not by `grep -c verify_`: the guard name must
appear in the `ImportFrom` names for `build_state_engine` **and** as a bare
`Expr(Call(Name(...)))` statement. A raw count is only a lower bound here, because the per-fork
justification comments also match `verify_`.

### Sensitivity demonstrations — the verbatim `SystemExit` texts

A guard that cannot fail proves nothing. Every `SystemExit` message below is transcribed
verbatim from the plan commit bodies; every demonstration mutation was temporary and restored
via `git checkout --`, with the fork digests confirmed byte-identical afterwards. Both guards
raise `SystemExit` and never `assert` — the project's convention, asserted by AST over each
guard body (zero `ast.Assert` nodes; one raise in `verify_list_item_wrappers()`, exactly two in
`verify_conditional_action_string()`).

**Reference digests, both forks, unchanged across every demonstration in this phase:**

| Fork | Source | SHA-256 before → after |
|---|---|---|
| Core | `src/PROSOCHE-Dumb.xml` | `99388cad597417685eb8624a0b4b34e18a6bd30805ac38beb2f3188026c3e679` → identical |
| Aware | `src/PROSOCHE-Sentient.xml` | `d01154b3e1b5990e5d3bc6d92e8dd895b92d0448217356772d077022e5215666` → identical |

The demonstration subject was a **pinned absolute SHA**, `698ab99`, never a relative ref, and
its defectiveness (exactly 660 unwrapped rows) was asserted *before* it was used, so a
demonstration could not silently succeed against the wrong artifact. Its pre-fix Core blob is
2831992 bytes, `589ee121…`.

**`verify_list_item_wrappers()` — three ways (plan 13-01).**

Direct call against `698ab99:src/PROSOCHE-Dumb.xml`, raising `SystemExit`:

```
List rows carry a raw WFTextTokenString instead of the iOS {WFItemType, WFValue} wrapper
(renders blank on device): action 1141 row 0, action 1141 row 1, action 1141 row 2,
action 1141 row 3, action 1141 row 4 (660 total)
```

Full-build revert on **Core** — `mirror_text()`'s `WFItems` argument reverted to `list(items)`,
then `python3 tools/build_state_engine.py` exited **1** with the byte-identical message, and
`src/PROSOCHE-Dumb.xml`'s sha256 was **unchanged across the failed build** — the empirical proof
the raise preceded `SOURCE.write_bytes()` rather than following it.

Full-build revert on **Aware** — `src/PROSOCHE-Dumb.xml` overwritten in the working tree only
with the pre-fix blob from `698ab99`, then `python3 tools/build_sentient.py` alone exited **1**
with the same prose and the same `660 total`, at the Aware fork's **own** indices:

```
… action 1209 row 0, action 1209 row 1, action 1209 row 2, action 1209 row 3,
action 1209 row 4 (660 total)
```

**The differing index is positive evidence, not a discrepancy.** Aware inserts its own actions
ahead of the Mirror block, so `1209` is the Aware fork's own index for the same first offending
List action; an inherited-from-Core failure would have carried Core's `1141`. That is exactly
what a per-fork arming assertion has to prove. `src/PROSOCHE-Sentient.xml`'s sha256 was
unchanged across that failed build too.

**Non-vacuity:** in the same process that captured the failures, the same guard returned
**without raising** on both post-fix forks.

**`verify_conditional_action_string()` — four variants plus a full build (plan 13-02).**

The pin isolated — one variable-bearing target replaced with the opposite
`WFTextTokenAttachment` envelope:

```
variable-bearing conditional comparison targets have LOST the device-confirmed Donor 5
WFTextTokenString envelope (a single ￼ string plus a non-empty attachmentsByRange); this
assertion PINS a shape iOS itself authors, so the change that tripped it is the defect, not
the shape: actions 158 (1 total)
```

The **pre-existing** assertion, proven still to have teeth after the extension — one target
replaced with the bare `U+FFFC` string:

```
conditional comparison targets hold the abandoned bare placeholder character instead of a
wired token() reference: actions 158 (1 total)
```

Full-build revert on Core — `token()` temporarily returned the `WFTextTokenAttachment`
envelope, and `python3 tools/build_state_engine.py` exited **1** naming the whole
variable-bearing family:

```
… actions 158, 546, 635, 660, 691 (20 total)
```

The **pin itself** was the guard that raised in that full build; no earlier guard in `main()`'s
chain claimed the failure, so no fallback to the direct-call result was needed and the chain
order was never touched. `src/PROSOCHE-Dumb.xml`'s sha256 was unchanged across the failed build.
Non-vacuity: the same guard, same process, returned without raising on both shipped forks.

### The ordering mask, recorded rather than engineered around

`verify_conditional_action_string()` now carries **two** raises, and the first masks the second.
Tripping both in one action list — action 158 mutated to the bare placeholder, action 159
mutated to lose the envelope — produces **only the first raise's message**, byte-identical to
the legacy text quoted above:

```
conditional comparison targets hold the abandoned bare placeholder character instead of a
wired token() reference: actions 158 (1 total)
```

The pin's offender is **entirely invisible**, and the `(1 total)` is the *legacy* count, not a
combined one. The two messages are textually distinct, which is what makes the mask
diagnosable at all. **Neither `main()`'s verify chain order nor the order of the two raises
inside the function was changed** — reordering either to make a demonstration convenient is the
weakening this phase's prohibitions forbid. `verify_list_item_wrappers()` introduces **no**
ordering mask of its own: it was the guard that raised in both of 13-01's full-build reverts,
confirming empirically what its placement asserted.

### Deviations and open assumptions

No deviation rule was invoked in either implementation plan; no auto-fix was required. **Five**
assumptions remain **open**, each with its risk — A1 through A4 from plan 13-03, and **A5 added
by the phase code review (CR-02)**, which also **restates A3**:

- **A1 — the cause of the 2026-08-14 red render.** `[ASSUMED]` that it was a then-current
  binding since changed by cycles 14–16 and Phases 9–12. **Unprovable now:** the build is not
  retained and the screenshot does not exist. Risk: **low** — the site is provably valid at
  HEAD on every axis file-level analysis can reach, so no action is available regardless, and a
  red chip at Phase 19 UAT would be a **new** finding with a live artifact to inspect.
- **A2 — `WFItemType` values other than `0`.** Left **unaudited by choice**. Neither donor
  exercises a number, dictionary or file row. Risk: **none for this phase** — only text rows
  are emitted. The guard asserts only that the key is *present*, never that it equals `0`,
  because asserting `== 0` would encode the same unaudited claim one level down. Do not infer
  any other value from `0`.
- **A3 — an all-wrapped array is a configuration no donor exhibits. RESTATED AND PARTLY CLOSED
  by the phase code review (CR-01); the original wording is preserved below because it is the
  reason the defect survived the plan.** As written in 13-03, A3 noticed the adjacent fact and
  framed it as a *mix* question rated low risk: "Donors 4 and 4.1 show bare and wrapped rows
  **mixed** in one device-authored array, which is close to VERIFIED for the mix; this phase's
  fix nonetheless produces arrays that are entirely wrapped. Risk: **low**, listed only because
  the exact configuration shipped is not the exact configuration observed."

  **What that wording missed.** The arrays were not merely all-wrapped; **44 of the wrapped rows
  were literal by content** — an empty `attachmentsByRange` — so the shipped encoding
  contradicted axis 8's own stated rule rather than merely going beyond the donors' observed
  configuration. A reader auditing the record could not have learned that from A3. This is a
  *stronger* claim than "no donor exhibits it": a donor exhibits the **opposite**.

  **Status now.** CR-01 moved those 44 rows to the bare `<string>` form both donors show, so the
  two Mirror families (success and lapse) now ship **mixed** arrays — 9 wrapped rows and 1 bare
  row each — which is exactly the donor-observed configuration. The 22 baseline arrays remain
  entirely wrapped, because all ten baseline templates genuinely carry placeholders; that
  residue is the only part of A3 still open, and it is open for the original, weaker reason
  (an all-wrapped array is unobserved, not contradicted). Risk: **low**. Device-only, owned by
  Phase 19 UAT alongside A4.
- **A4 — wrapping does not change what `getitemfromlist` returns.** No donor chains a *wrapped*
  List into `getitemfromlist`. The file-level half **is** verified: row count and ordering per
  List action are unchanged (`[6] + [10]*66`), `WFItemSpecifier` and `WFItemIndex` are
  untouched, and no arithmetic and no `uid()` call was introduced. Risk: **medium** — if iOS
  treats a wrapped row differently on extraction, the Mirror text could change shape. **Device-
  only; owned by Phase 19 UAT,** which must assert "Mirror renders non-empty text".

- **A5 — the numeric conditional's right-hand slot, `WFNumberValue`. Added by the phase code
  review (CR-02); BD-08 previously recorded this as CONFIRMED and that confirmation is
  RETRACTED.** Two axes are `UNVERIFIED`, both re-measured independently. (i) **Encoding:**
  `if_block()` assigns the raw Python value, so `plistlib` emits an `<integer>` at **90 (Core) /
  97 (Aware)** sites; re-decrypting `.planning/debug/Donor 4.1.shortcut` reads
  `<key>WFNumberValue</key>` → `<string>10</string>`. The generator diverges from the donor.
  (ii) **A fourth, uncovered case:** **32** conditionals per fork hold a *dict* in
  `WFNumberValue` — a bare `WFTextTokenAttachment` variable reference over eleven distinct
  variables (`Best Average`, `Dim Target`, `Exploit Minimum`, `Exploration Threshold`, `Gravity
  Cap`, `Heat Cap`, `Heat Floor`, `Now Epoch`, `Overrun Minimum`, `Silence Target`,
  `Threshold`). **No donor covers a variable in `WFNumberValue` at all.** Risk: **medium** —
  this project's recorded failure mode for a non-literal comparison slot is "Please choose a
  value for each parameter in this action", which is a hard runtime stop, not a degradation.
  **The artifact was deliberately NOT changed:** moving 90/97 live operands on a build no
  device can run would settle nothing and would close at best half the finding, since the 32
  dict sites stay unevidenced either way. **Device-only; owned by the outstanding device UAT,**
  which must observe a numeric-gated Circle actually firing — the `> 0` panic-escape gate and
  any Heat/Pressure threshold comparison are the cheapest witnesses. A donor exercising a
  *variable* right-hand operand would settle (ii) at rung 4 without a full UAT.

**Installed-base note for Phase 19.** A user who already imported the previous signed build
keeps the blank-row Mirror until they **re-import**. That is inherent to Shortcuts distribution
and needs no migration — but Phase 19 UAT must therefore test a **re-imported** build rather
than a stale install, or it will observe the old defect and attribute it to a fix that did land.

### Regression protection — CIRC-04 and ROOM-03

**Neither requirement has a defect site in either family, and no work was invented to make them
look addressed.** CIRC-04's time-boundary picker is a `choosefrommenu`, not an
`is.workflow.actions.list`; ROOM-03's Note body is a hand-authored text template with no
conditional operand and no List row. Both are **regression-protection** requirements, satisfied
by `docs/phase5_self_check.py` (CIRC-04) and `docs/note_identity_check.py` (ROOM-03) staying
green through the rebuild — both exited 0 after every rebuild in plans 13-01 and 13-02, as did
`docs/sequence_dispatch_check.py` for the Mirror dispatch path. Eleven of the twelve
`docs/*.py` checkers are green; `docs/manifest_check.py` is **expected red** for the D-04
reason below.

`docs/manifest_check.py` fails with `AssertionError: row 'Core source': MANIFEST declares
2831992 bytes, src/PROSOCHE-Dumb.xml is 2916560 bytes` — the expected consequence of
regenerating the sources in plan 13-01. It was **not** silenced, and MANIFEST rows were **not**
edited without re-signing, which is exactly the prohibition that forbids it. Plan 13-04 owns the
re-sign.

### Gate B advisory read and signed-artifact provenance (plan 13-04, 2026-08-17)

*This subsection was reserved and left deliberately empty by plan 13-03, which ran no build, no
validator gate and no signer. Plan 13-04 fills it with what it actually measured.*

**Rebuild and provenance.** `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678
HEAD` exited **0** before either generator ran. `tools/build_state_engine.py` and
`tools/build_sentient.py` were then run in that order, and the rebuild was **byte-idempotent**:
`git status --porcelain` was empty afterwards, so both sources carried the wave-2 digests
`99388cad…` (Core) and `d01154b3…` (Aware) **as of this 13-04 run**. Those two source digests were
superseded by the CR-01 re-ship at `365937e`; they are recorded here as the wave-2 measurement, not
as current. (These are `src/*.xml` digests, not signed-artifact digests — nobody imports a source
XML, and `artifacts/shortcuts/MANIFEST.md` remains the authoritative live record.) The operative
claim is unaffected and was re-verified after the re-ship: the rebuild is byte-idempotent. That
matters beyond tidiness — it means a re-run
after an interruption converges on the same digests rather than producing a new set, so the
hashes in `artifacts/shortcuts/MANIFEST.md` are reproducible rather than run-specific
(threat T-13-26).

**Checker baseline before signing.** All eleven non-manifest checkers exited **0** *before*
anything was signed, deliberately: a signed artifact built from a source that fails a checker is
a false provenance claim. `docs/manifest_check.py` was the expected twelfth red at that point,
failing with the byte-identical D-04 message plans 13-01 through 13-03 each recorded —
`AssertionError: row 'Core source': MANIFEST declares 2831992 bytes, src/PROSOCHE-Dumb.xml is
2916560 bytes`. It exits **0** at the end of this plan; D-04 is closed by re-signing and
recomputing every row, **not** by editing byte counts to match a stale artifact.

**Gate A — mandatory, clean on both forks.**

| Command | Result |
|---|---|
| `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` | `Validation passed.`, exit **0** |
| `validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all` | `Validation passed.`, exit **0** |

**Gate B — advisory read only, run standalone per fork.** Each command below was issued on its
own. Neither appears in any `&&` chain, in either task's `<verify>` block, or in any definition
of done — gate B's waiver is permanent, so it can never exit 0 and is therefore structurally
incapable of being a gate (`.claude/CLAUDE.md` §1). Both exited **1**, which is the expected
outcome, and each reported **exactly one** finding line.

Verbatim, `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 27 --target-platform all`:

```
Validation failed:

First failing action: index 0 (is.workflow.actions.comment)
Snippet: {'WFCommentActionText': 'PROSOCHE - Nine Circles (Dumb fork). This shortcut is the whole product: it reads two setup answers from import, checks for a saved setup file, creates one on first run along with a setup note, and opens that not...

- Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index 4192: WFCreateNoteInput. ToolKit v78 expects: OpenWhenRun, contents, folder, interpretAsMarkdown, name.
```

Verbatim, `validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 27 --target-platform all`:
identical but for the action index, which reads `4260`.

Index-normalised, so a future run can diff against it without the index churn every edit causes:

```
Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index N: WFCreateNoteInput. ToolKit v78 expects: OpenWhenRun, contents, folder, interpretAsMarkdown, name.
```

**Exactly one such line per fork, and nothing else.** That is the single permanent waiver
recorded in `.claude/CLAUDE.md` §1 and in §14 — device-donor ground truth outranks the
`macOS 27`-tagged catalog entry, and `STRING_ENVELOPE_PARAMS["com.apple.mobilenotes.SharingExtension"]`
retains it on purpose. The `First failing action: index 0` line is the validator's own framing
of *where it stopped*, not a second finding. **This was the run most likely to surface a real
regression** — the phase moved 660 row serializations, and gate B is the only channel that
checks parameter keys and picker literals at all. It surfaced none, so no finding was
investigated because none was reported. Note gate B's own limit, unchanged: at
`--target-macos 27` it may *accept* an OS27-only parameter key iOS 26 does not offer, so it
supplements gate A and never replaces it.

**Signing — the two canonical display names, no suffix.**

> **SUPERSEDED — the digests, sizes and census in this plan-13-04 subsection describe the
> `737ce07` build, which no longer exists on disk.** The code-review pass that followed execution
> found CR-01: `_list_row()` discriminated on Python type, so 44 attachment-free
> (literal-by-content) rows shipped inside the variable-row wrapper — a second unevidenced framing,
> at row 8, the row selected at Circle VIII. The fix and full re-ship landed in `365937e`. The
> **current** shipped artifacts are Core `233802 B` / `b07497ba…` and Aware `237842 B` /
> `212598cf…`, and the census is **616 wrapped / 50 bare**, not 660/6. The figures below are
> retained as the record of what was signed at 13-04 time; do not read them as current. The
> authoritative live values are the six rows of `artifacts/shortcuts/MANIFEST.md`, proven against
> disk by `python3 docs/manifest_check.py`.

| Fork | Source | Signed basename | Bytes | SHA-256 |
|---|---|---|---:|---|
| Core *(superseded)* | `src/PROSOCHE-Dumb.xml` | `PROSOCHĒ — Nine Circles — Core.shortcut` | 234830 | `fe1bafdf53f872a3e149734456899d1be0987706551d7b8fa7b50f81b8a913b7` |
| Aware *(superseded)* | `src/PROSOCHE-Sentient.xml` | `PROSOCHĒ — Nine Circles — Aware.shortcut` | 239184 | `bd1264d502891c9afeeccb66134dceaf66288a1da890133498605538aa75ba19` |

Both begin with the `AEA1` magic and both are non-zero. `artifacts/shortcuts/` holds exactly
those two `.shortcut` files and no other basename of any kind. Neither known signer quirk fired:
both `shortcuts sign` invocations succeeded on the first attempt, so `sign-shortcut`'s two
auto-retries were not exercised. The dated pre-sign archives are
`artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Core-184943.xml` and
`— Aware-184954.xml`, each byte-identical to its `src/` counterpart, which is what makes an
archive a pre-sign record rather than a copy of something else.

**`.claude/CLAUDE.md` §8's filename-discipline examples are stale, and the rule is not.** §8
names the forks `Dumb`/`Sentient`; Phase 11 renamed the *products* to `Core`/`Aware` and
`docs/manifest_check.py` hard-codes the live names as DIST-04, so signing to the §8 example
names would fail that checker. The *source* filenames deliberately remain `PROSOCHE-Dumb.xml`
and `PROSOCHE-Sentient.xml`. The discipline itself is load-bearing rather than cosmetic and was
re-confirmed on this build: neither recovered `Shortcut.wflow` contains a `WFWorkflowName` key
at all (measured — `'WFWorkflowName' in plist` is `False` for both) even though both `src/*.xml`
set it, so the signer strips it and **the filename is the sole carrier of the display name**. A
suffixed file imports as a second, differently named library entry that the user's two Personal
Automations do not reference — a silently dead install.

**Decrypt-verification — what actually shipped.** Both containers were recovered through the
full AEA1 workflow rather than inferred from the unsigned source plus a file mtime: the leaf
certificate was extracted from the auth-data plist's `SigningCertificateChain` (779 DER bytes,
both forks), its public key taken with `openssl x509`, then `aea decrypt` (exit 0), `aa extract`
(exit 0) and `plutil -convert xml1` (exit 0). Measured on the **recovered** plists, not on
`src/`:

| Measurement | Core | Aware |
|---|---:|---:|
| Total actions | 4346 | 4414 |
| `is.workflow.actions.list` actions | 67 | 67 |
| `WFItems` rows, total | 666 | 666 |
| Rows wrapped as `{WFItemType: 0, WFValue: …}` | **660** | **660** |
| Bare-string rows (the six exit names) | **6** | **6** |
| Dict rows missing `WFItemType` | **0** | **0** |
| `WFWorkflowName` present | `False` | `False` |

This is the only check that would catch a row altered between source and shipped artifact
(threat T-13-23), and it is what licenses the claim that the wrapper fix *shipped* rather than
merely *built*. `aea` and `aa` were both available at `/usr/bin`, so no tooling deviation was
recorded.

**MANIFEST.** All six rows — two sources, two new dated archives, two signed artifacts — were
recomputed from disk in one pass rather than only the rows believed to have moved; Phase 10
measured three of six wrong at once (threat T-13-22). `docs/manifest_check.py` exits **0**, and
all twelve `docs/*.py` checkers are green at the end of this plan. `docs/phase5_self_check.py`
(CIRC-04) and `docs/note_identity_check.py` (ROOM-03) are among them, which is the whole of what
those two regression-protection requirements needed — proven unregressed against the artifact
that actually ships, with no work invented for either.

**Device verdict — BLOCKED, and recorded as observed.** `xcrun devicectl list devices` reported
`No devices found.` on 2026-08-17, so nothing in this subsection is device evidence and
**DIST-03 remains open**, unchanged since Phase 10. `13-UAT.md` is authored cold-runnable with
six tests and every outcome left **blank** and marked `BLOCKED`. No simulator run, no decrypted-artifact
inference and no plausible-looking pass was substituted for a device observation. The booted
simulator could not settle these questions in any case — it lacks `com.apple.mobilenotes` and
cannot import a signed `.shortcut` at all — and the plist is already proven correct at file
level, which is exactly what a device observation neither adds to nor subtracts from.

**Re-import note for Phase 19.** A user holding any previously signed build keeps the blank-row
Mirror until they **re-import**. That is inherent to Shortcuts distribution and needs no
migration, but Phase 19 must therefore test a **re-imported** build rather than a stale install,
or it will observe the old defect and attribute it to a fix that did land. The artifact to
import is `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` at SHA-256
**`b07497ba…`** (the `365937e` re-ship); anything else is the wrong build. **SUPERSEDED:** an
earlier revision of this sentence named `fe1bafdf…`, the `737ce07` build that carried the CR-01
defect. Importing that one would test the defect rather than the fix.

---

## 29. Phase 16 — the coercion probe: a rung-2 channel opened, a chip gate retired, and an inference refuted (plan 16-02, 2026-08-18)

**Channel: SIMULATOR, rung 2.** iPhone 17 Pro, iOS 26.5 (23F77), udid
`79A84C29-DB62-40A2-AC3F-CCB5F8192F86`. **None of this is device evidence.** No physical-device
tunnel was live; nothing below may be read as device ground truth, and every claim inside
`.claude/CLAUDE.md` §9's "Rung 2's ceiling" is recorded **UNVERIFIED** regardless of how clean the
observation looked. Spike: `.planning/spikes/010-coercion-at-a-direct-set-parameter/`, verdict
**PARTIAL**, 14 archived screenshots.

### 29.1 The rung-2 import channel is real — spike 007's claim is RETIRED

`xcrun simctl openurl <udid> "file:///abs/path.shortcut"` renders the Shortcuts import sheet, and
**one synthesized tap on "Add Shortcut" completes the import.** Measured this session; the editor
opened on the imported probe. This closes `16-RESEARCH.md` assumption **A5** — the open half was
whether the tap lands, and the answer is **yes**.

Spike 007 recorded, and the `spike-findings-prosoche` skill repeated as a standing constraint, that
*"the booted simulator cannot import a signed `.shortcut` through any channel."* That generalisation
was drawn from five failed channels **without the sixth having been tried**: its `file://` row was
measured against the **MCP simulator tool's scheme allowlist**, not against `simctl`. Every other row
stands — re-measured 2026-08-18, `shortcuts://import-shortcut?url=file://…&silent=true` still returns
*"Import Failed. The shortcut URL provided was invalid."*, because the `shortcuts://` scheme wants an
iCloud link and rejects the URL before `silent=true` is ever consulted. `openurl` with a plain file
URL does not go through that scheme at all.

**Consequence for the ladder:** `.claude/CLAUDE.md` §9's original rung-2 row was **right**, and spike
007's narrowing of it was wrong. Rung 2 reaches the **editor and the runtime**, not merely the build.
Both §9 and the skill's `evidence-and-probes.md` are corrected accordingly, each citing
`010-coercion-at-a-direct-set-parameter` as the measuring spike.

Instrument, preserved with every dead end recorded so nobody re-walks them:
`.planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/sim_input.py`. What did **not** work:
the tap tool §9 names (`mcp__Claude_Code_iOS_Simulator__control`) is not exposed to a subagent with a
restricted tool list; `osascript` is refused assistive access (`-1728`); `idb` and `cliclick` are not
installed; `simctl` has no tap verb. What works is `CGEventPost` straight to the window server, which
needed no Accessibility grant. Two preconditions that cost real time: a `simctl`-booted simulator has
**no on-screen window** until `open -a Simulator`, and coordinates must be **fractions of the device
screen mapped through the window rect measured at run time**, never pixels.

### 29.2 CAP-06 addendum — the chip gate CANNOT discriminate at a direct Set-action parameter

§15 (CAP-06) established that operator/operand type validity is a UI-only signal: a numeric
conditional on a text-typed operand renders **red**, is structurally valid in the file, and fails at
runtime. That remains true **for conditionals**. It does **not** generalise to a direct Set-action
parameter, and this is the finding that matters most here.

Measured: a `Set Brightness` fed by a named variable **with** the Number coercion, and an otherwise
identical one **without** it, **render identically** in the editor. Neither is red. Neither is
degraded.

The mechanism is simple once seen. A conditional's operator picker is populated **from the operand's
static type**, so a mismatch has no case to render and the chip goes red. **`Set Brightness` has no
operator picker.** There is nothing for a type mismatch to break in the UI.

**Therefore `09-UAT.md` Test 1 — "the coercion chip does not render red" — is not a valid instrument
for `WFBrightness`/`WFVolume`.** Its single recorded pass was never evidence about these sites. A
green chip at a direct Set parameter is not weak evidence; it is **no** evidence. The uncoerced
control leg is what exposed this — without it, "leg A rendered fine" would have been recorded as a
pass, and the pass would have been vacuous.

### 29.3 CAP-08 — `setbrightness.WFBrightness` is OPTIONAL and defaults to 50%

**New capability finding, and it is a safety finding.** A `Set Brightness` authored with
`WFBrightness` **entirely absent** renders in the editor as **"Set brightness to 50%"**. The
parameter is optional with a default; omitting it does **not** produce an unfilled-parameter state.

**Why this matters for SAFE-01 / CIRC-05.** If the coercion were ever wrong in a way that left the
operand unresolved, `Set Brightness` would **not** halt and would **not** report *"Please choose a
value for each parameter in this action."* It would silently apply **50% brightness** — an
unrequested environmental change, with no capture, and no error to attribute it to. That is strictly
worse than a halt, because Shortcuts has no try/catch and a halt is at least visible.

**Direct requirement on the device instrument:** the eventual device test must verify **the
brightness value actually applied**, not merely that the action did not error. A "no error" device
result is fully consistent with a completely broken operand.

### 29.4 The refuted inference — recorded because the refutation is the useful part

Running the coerced leg on the simulator produced **"Could Not Run Set Brightness — There was a
problem setting the brightness."** That is a **capability** failure, not the **parameter** failure
§15 names as the signature of an operand-type defect. The tempting inference was: *Shortcuts got past
parameter validation and reached the OS call, so the coerced operand resolved.*

**A negative control refuted it.** A one-action probe holding a `Set Brightness` with no operand at
all produced **the same** message. Both reach the OS call; both fail identically because the
simulator has no backlight. **The channel cannot distinguish a resolved operand from an absent one**,
so no run on a simulator can show whether the coerced operand was consumed.

This is `.claude/CLAUDE.md`'s *"read the error text, not just the letter"* doing its job, and the
negative-control idiom from `docs/phase9_self_check.py::negative_control()` doing its job. The
control cost one small artifact and overturned the conclusion the spike was about to record.

### 29.5 What this probe did NOT settle — the negative record, stated in full

A record that only holds successes is not a record. **Recorded UNVERIFIED, all inside §9's rung-2
ceiling:**

- **Whether `Set Brightness` actually CONSUMES a Number-coerced named-variable operand at run time.**
  `Set Brightness` cannot succeed on a simulator at all. This is not partially answered — it is
  **untouched, and now known to be unreachable at rung 2**, which is worth recording because it means
  no further simulator effort will help and the device session must carry it.
- **Whether `Get Device Details → Current Brightness` returns a usable, correctly typed value on real
  hardware.** The simulator returns **`0`**. Informative for probe design, **not promotable**.
- **Real-hardware environmental behaviour** — whether the screen physically dims and un-dims, and
  what `WFBrightness = 0.0` looks like. Untouched. Personal Automations, the Control Room Note path
  and Apple Intelligence likewise untouched.

**`WFNumberContentItem` is neither confirmed nor refuted at this position.** Nothing observed
contradicts it; the fresh-donor protocol is **NOT** triggered; no replacement `CoercionItemClass`
appears anywhere in the spike, and `drafts/assert_probe_shape.py` fails if one ever does.

### 29.6 A2 CONFIRMED by name-scoped provenance — the 11 uncoerced `setvolume` sites are correct

`16-RESEARCH.md` assumption **A2** is the claim the volume disposition rests on, and its own risk
note said the existing evidence was a count, not a name-scoped check. Run properly, read-only, on
both shipped forks (`drafts/audit_silence_target_sourcing.py`, 2026-08-18):

| | Dumb | Sentient |
|---|---:|---:|
| `Set Variable "Silence Target"` assignments | **11** | **11** |
| …**Number-sourced** (`is.workflow.actions.number`) | **11** | **11** |
| …**not** Number-sourced | **0** | **0** |
| `setvolume` sites | 15 | 15 |
| …fed by `Silence Target` | **11** | **11** |
| …carrying a coercion | 4 | 4 |

**The arithmetic closes exactly:** 11 fed by `Silence Target` + 4 coerced = 15. The 11 uncoerced
sites are precisely the 11 fed by a variable whose **every** definition is `number()`-sourced. **A2
holds**, now on provenance rather than on a count.

**The asymmetry — 15/15 brightness coerced vs 4/15 volume — is a SOURCING ARTIFACT, not a gap.**
Brightness operands are `gettext`-sourced (`read_value()` = get + gettext → Text) and need the
coercion; the silence target is `number()`-sourced and already Number-typed, so
`normalise_numeric_operands()` correctly skips it via `_already_numeric()`, leaving device-proven
sites byte-identical. The four coerced `setvolume` sites are the **restore** operands, which come
back out of state through `read_value()` and are therefore Text — the same reason brightness needs
it. `docs/environmental_restore_check.py` deliberately asserts **no** coercion count for exactly this
reason and says so in its own comments.

**Do not "fix" the asymmetry by pattern-matching brightness.** Coercing an already-Number operand
would change 11 device-untested sites for no benefit, in a build whose safety argument rests on not
disturbing what already works.

The failure mode the name-scoped check rules out is one this project has already paid for: Shortcuts
variables are global to a run and last-write-wins, so **one** text-sourced `Set Variable "Silence
Target"` anywhere in either fork would poison all 11 operands, and the count-based `site_audit()`
would still pass. That is exactly how `Circle Next` became mixed-typed and produced 30 real
offenders (the CYCLE 14 note above `NUMERIC_OPERAND_FIELDS`).

**This plan changed no generator or checker code.** `python3 docs/phase9_self_check.py` and
`python3 docs/environmental_restore_check.py` both exit 0 — `site_audit: passed (30/30 sites audited,
19 coerced, 11 correctly not)`. Acting on the probe's verdict in the generator belongs to a later
phase, with its own guard.

### 29.7 Free-ride — spike 007 resolved, PARTIAL → VALIDATED

The channel was open and the recording duty applies to whatever is observed, so spike 007's
still-unrun `App Picker Probe` was imported and inspected. Recorded in **spike 007**; summarised here
because leg E is a general lesson about fabricated values, which is this project's central discipline.

| leg | authored | renders as |
|---|---|---|
| A | Calendar, donor-exact complete descriptor | **"Open [Calendar]"** — normal, control passes |
| B | Reminders — **first-party, INSTALLED**, `WFSelectedApp` **omitted** | **"Open [App]"** — EMPTY |
| C | Contacts — correct bundle id, **fabricated** name + nonsense team id | **"Open [ZZZ WRONG NAME ZZZ]"** — the editor **trusts the stored Name** and never re-resolves it |
| D | Instagram — third-party, not installed, bare identifier | **"Open [App]"** — empty, identical to B |
| E | TikTok — third-party, not installed, **fabricated** descriptor | **"Open [AirDrop]"** in **RED** — mis-resolved to a different, real app |

**An unresolvable picker renders silently EMPTY, and a fabricated one renders silently WRONG.**
Nothing fails at import; nothing warns. Leg E produces a confident, fully-populated chip naming an app
the author never mentioned. That is the silent-wrong-behaviour class the do-not-fabricate rule exists
to prevent, now demonstrated end to end rather than argued — and it generalises spike 005's lesson
from parameter literals to **entity descriptors**: a plausible-looking fabricated descriptor is not a
degraded correct one, it is a *different* one.

**Leg B is the one that touches this project's code:** `WFAppIdentifier` alone is **not** sufficient
even for an installed first-party app. **PROSOCHĒ is unaffected** — `open_app()` emits the full
`WFSelectedApp` triple for all six apps, which is leg A's shape exactly — but spike 006's Class-A
verdict for `Open App` holds **because the descriptor is written**, not because the bundle id would
have carried it. Leg C adds the cost of a wrong Name: the editor would display it indefinitely.

**Still not settled:** launch behaviour. Every observation is authoring-time render, which is what the
probe was built for. What legs D and E do when actually launched is untouched, and is off PROSOCHĒ's
critical path.
---

## 30. Phase 16 — D-01 recorded: CAP-16's Fallback cell stops asserting a bound (plan 16-05, 2026-08-18)

**What changed.** CAP-16's `Fallback` cell in §4 asserted a lower bound on the `WFBrightness` write and
declared itself **binding on Phase 5's CIRC-05**. `safety.brightness_floor` and `safety.dim_target` are
both `0` in both shipped forks as of plan 16-03, so that cell had become an instruction to build
something the build does not do. It is corrected in place.

**The retired clause is CITED, never restated — and that is a mechanical requirement, not a stylistic
one.** `docs/retired_clause_check.py` (new in this plan) greps live files for the retired vocabulary and
fails on every survivor. A supersession note that reproduces the clause it retires *is* a survivor: the
false assertion is still sitting in the file, now wearing a correction's clothes. Where the clause lived
is recorded — BD-02's original Decision paragraph in `docs/CAPABILITY-DECISIONS.md`, and canonical
strategy §21 — and that is the whole record anyone needs to follow it.

**The canonical strategy is FROZEN and was not edited.** `PROSOCHE_Nine_Circles_Canonical_Strategy.md`
is a historical design input, not a living spec (user decision, 2026-08-18). §21's floor clause stays
exactly as written there. `docs/CAPABILITY-DECISIONS.md` BD-02's **Supersession** note carries the
correction instead and is **the authority where the two disagree**. That note is load-bearing rather
than decorative: three amended sites across the repo keep citing §21 as their authority — both `safety`
rows in `src/CONFIG-BLOCK.md`, the CAP-16 cell above, and the Set Brightness capability-audit row in
`.claude/CLAUDE.md` — and without it each reads as amended text pointing at an unamended source.

**What binds CIRC-05 now.** The property, not a value: the original brightness is captured **and
durably persisted** before any change and is always restored; a run whose read returns nothing changes
nothing. The durable-persistence half became true in plan 16-01 — before it, the capture was written
into a dictionary that was never saved, so the property could not have been satisfied by any build.
That is what makes this restatement a correction rather than a weakening.

**Per CAP-08 the hazard at this action moved rather than disappeared.** `WFBrightness` is OPTIONAL
(simulator-measured, plan 16-02): an **absent** operand does not raise the unfilled-parameter error, it
silently applies an unrequested default with no captured original behind it. `docs/phase5_self_check.py`
asserts the operand's presence — the assertion plan 16-03 put in place of the retired value check, which
was the one site in the whole class that carried **none** of the retired vocabulary and could only ever
have been found by reading the code.

**Scope.** Brightness only. §17's DEV-06 record (closed by plan 16-04) is untouched, `allow_volume_increase`
stays `false`, and Silence's Media-only scoping stands — SAFE-02 is unchanged by D-01.


## 31. Phase 11 — the text.match consumption shape: SETTLED at rung 2, and the probe defect that first hid it (plan 11-07 Task 2, 2026-08-18)

> **This section was rewritten on 2026-08-18 after the probe was re-run.** Its first version
> recorded the question OPEN and blamed an install failure. **That reason was false and is
> retracted below.** The corpus tally and the fallback rationale are unchanged and are retained;
> the verdict and the account of the first run are not.

**The question.** `is.workflow.actions.text.match` publishes a **list** ("Matches"). When that
list-valued output is consumed, which shape yields the matched section as a usable string?

- **Shape A** — what `panic_escape_branch()` did: `text.match` → `gettext` → the string.
- **Shape B** — the in-repo precedent in `tools/build_sentient.py`'s `audit_block()`:
  `text.match` → `getitemfromlist` with `WFItemSpecifier="First Item"` → the extracted item.

**The corpus tally, re-taken over all 19 shipped golden XMLs rather than transcribed.** Every
`ActionOutput` token was resolved back to its producing identifier:

| measure | result |
|---|---|
| output name `Matches` | **15** occurrences, across 3 of the 19 files |
| the label this engine used to guess | **0** |
| consumer `text.match.getgroup` | 7 |
| consumer `conditional` | 5 |
| consumer `setvariable` | 1 |
| consumer `count` | 1 |
| consumer `detect.text` | 1 |
| consumer `gettext` | **0** |
| consumer `getitemfromlist` | **0** |

The tally settles the **name** decisively (15 versus 0 — see §32). It does **not** settle the
**shape**: the corpus contains zero observations of *either* candidate chain, so rung 1 is
genuinely exhausted and a probe was the correct instrument.

### The result — rung 2, booted iOS 26.5 simulator, 2026-08-18

The corrected probe was imported and run. Verbatim clipboard payload:

```
PROBE-BEGIN
[SHAPE_A]<<## PANIC ESCAPE
Panic Escape: OFF
Set this line to ON to restore it.
>>
[SHAPE_B]<<## PANIC ESCAPE
Panic Escape: OFF
Set this line to ON to restore it.
>>
[CONTAINS]<<TRUE - Shape A output contains the removed-position line>>
PROBE-END
```

Three things are established, and nothing beyond them:

1. **`Matches` resolves at run time.** The name the class fix installed in `ACTION_OUTPUT_NAMES`
   is correct in practice, not merely by corpus tally.
2. **Shape A and Shape B are equivalent for a single-match list** — byte-identical output. The
   adopted Shape B is confirmed safe; Shape A would also have worked. The fallback was a correct
   choice made for a reason that has now been replaced by a measurement.
3. **The load-bearing gate passes.** `[CONTAINS]` is TRUE — the exact condition-99 contains test
   `panic_escape_branch()` runs finds the removed-position line.

**The boundary, stated because the fixture does not cross it.** The fixture yields exactly ONE
match. Single-match is the operative case — `PANIC_ESCAPE_SECTION_PATTERN` is bounded and matches
once — but **the multi-match case is untested**, and it is precisely where stringifying a list and
taking its first item would diverge. First-item is retained for that reason. Do not read this
entry as covering a loosened pattern.

**Rung discipline.** This is a **simulator** observation and is never promotable above `UNVERIFIED`
for anything in §9's "Rung 2's ceiling" list. It touches no Note, no model, no automation and no
real-hardware behaviour, which is exactly why it sits inside rung 2's competence. **It says nothing
about device behaviour; DIST-03 remains open.**

### Retraction: why the first run taught nothing

The first version of this section stated the probe "could **not** be installed" — that
`xcrun simctl openurl` against a `file://` URL hung and produced no import sheet on two attempts.
**That is false.** Re-measured 2026-08-18: `simctl openurl` produced the Shortcuts import sheet on
the first attempt, from a space-bearing path, and one tap on **Add Shortcut** completed the import.
**`.claude/CLAUDE.md` §9's account of this channel is correct and needs no narrowing.**

The real cause was in the probe itself, and it is a reusable lesson:

**`build()` returns RAW actions, and the generator never ships raw actions.** `main()` in
`tools/build_state_engine.py` runs a normalisation pipeline first. The probe's `main()` skipped it.
`output()` returns a bare `WFTextTokenAttachment`; at a string-typed parameter — and
`gettext.WFTextActionText` is one, listed in `STRING_ENVELOPE_PARAMS` — a bare attachment resolves
to **empty** at run time (axis 2). So the probe injected an axis-2 defect at **both** consumption
sites, upstream of the shape question and blinding it completely.

Measured on that first run: `[SHAPE_A]<<>>` and `[SHAPE_B]<<>>`, **identically blank**, while the
report action — built via `text_token()`, correctly enveloped — resolved its three chips perfectly.
**Two identical blanks were the tell**: a genuine shape difference produces different results, not
the same blank twice. The run also surfaced three blocking prompts (one text-entry prompt per
unresolved parameter, then the clipboard grant), which is what an unattended run silently died on.

**The rule this earns:** *a probe must run the generator's own pipeline, or it measures itself.*
`text_match_consumption_probe.py` now calls `normalise_string_envelopes()`,
`normalise_output_names()` and `normalise_numeric_operands()`, then **asserts**
`verify_string_envelopes()` before writing, so this class cannot silently return.

**A finding for every future simulator probe:** `is.workflow.actions.setclipboard` triggers a
one-time *"Allow ... to copy to the clipboard?"* modal. The clipboard readout was chosen precisely
to avoid blocking UI (§9, spike 010: `Show Alert` accepts neither a synthesized tap nor a hardware
Return), and it **still has one blocking gate on first use**. It is dismissible by a synthesized
tap — unlike `Show Alert` — so the channel remains the right one, but a probe run must budget for
that tap rather than assume a fully unattended run.

### The fallback adopted, and why — retained as originally recorded

**Shape B is adopted at both sites**: `panic_escape_branch()`'s section read, and
`manual_note_refresh()`'s Sync My Profile proforma extraction — the identical defect, closed in the
same pass rather than left as the next site to be found. Its consumer writes straight into a state
key, so Shape A there stored a **stringified list** rather than the real extracted proforma.

Three reasons Shape B was the safe fallback rather than a coin toss: it is the **in-repo
precedent**, already shipping in `audit_block()`; it is **deterministic about which element is
taken**, where a list-to-text coercion is not; and taking the first item of a one-element list
**cannot be worse** than stringifying that list. The `WFItemSpecifier` picker carries the literal
enum case `First Item` at both new sites, per axis 4.

**Retained for re-running.** The probe generator, its validated XML and its signed containers stay
under `.planning/debug/probes/`. The v2 container is the corrected one; the original is kept beside
it as the artifact that carries the axis-2 defect this section documents.

## 32. Phase 11 — the output-name class fix: one table entry, two sites, and a guard that can now see them (plan 11-07, 2026-08-18)

**The corpus tally that identified the class.** Re-taken this session across all 19 shipped
golden XMLs, resolving every `ActionOutput` token back to its producing identifier:
`is.workflow.actions.text.match` publishes **`Matches` 15 times** and the label this engine had
guessed **0 times**. A second, independent source agreed: `tools/build_sentient.py`'s
`audit_block()` had been reading the same identifier's output by the real name all along. One
artifact was therefore shipping **two contradictory names for one identifier** — the condition
`ACTION_OUTPUT_NAMES`'s own header comment names as the trigger for normalising ("where two
independent sources give the real name, normalise to it rather than keep the guess").

**Both sites closed in one pass**, per this project's standing rule that bisection only ever
reveals the earliest remaining site and site-by-site fixing costs one device round trip each:

| site | consumer | what the wrong name cost |
|---|---|---|
| `panic_escape_branch()` section read | condition-99 contains test | Section reads empty → test always false → the otherwise arm reports **"Nothing was changed."** on the path meant to remove the user's bypass |
| `manual_note_refresh()` Sync My Profile | `set_value("profile_snapshot.proforma", …)` | An unresolved reference written straight into a state key |

**Why it survived three phases.** Nothing errors. The reference does not resolve, and every
downstream step behaves exactly as it would if the user had simply chosen not to remove the
bypass. There is no error, no log, and — because the Note append that records the change never
runs — no audit trail either. This is the T-11-36/T-11-37 pair in the plan's threat register:
a spoofed success and an unloggable repudiation, arising from the same missing string.

**The table entry is the fix; the two corrected sites are only its consequence.**
`ACTION_OUTPUT_NAMES` now lists `is.workflow.actions.text.match`. That single entry arms the
whole chain for the identifier at **every present and future site**:
`_expected_output_names()` → `normalise_output_names()` rewrites every reference by producing-
action UUID → `verify_output_names()` fails the build on any survivor. While the identifier was
absent from that table, the guard built for exactly this defect class was **blind to both
sites** — which is why a review finding from Phase 11 was still live at HEAD after Phases 12,
13 and 16 had each landed on this codebase.

**The negative control, observed both ways.** One `text.match` reference's `OutputName` was
rewritten to a wrong string on a deep copy of the parsed Core action list, and
`verify_output_names()` called directly on it — not by editing a call site and rebuilding,
because `normalise_output_names()` runs *before* the verifier in `main()` and would silently
repair the regression first:

- **With the table entry removed** (reproducing the state before this plan): the call
  **returned normally**. Nothing raised. The guard was genuinely silent, not merely
  mutation-proof.
- **With the table entry present**: `SystemExit` — *"magic-variable references carry a wrong
  OutputName: action 4225 says 'Totally Wrong Name', real name is 'Matches' (1 total)"*.

The unmutated source then verified clean, confirming the control restored cleanly.

**The consumption-shape verdict: SETTLED at rung 2.** Recorded in full in §31. In short: the
probe was re-run on the booted simulator and **both shapes returned the bounded section
byte-identically**, with the condition-99 contains test reading TRUE — so `Matches` resolves at
run time and the adopted `First Item` chain is confirmed, not merely bounded. The single-match
case only; multi-match is untested and is why first-item is retained. **This section's earlier
claim that the probe "could not be installed" was false and is retracted in §31** — the probe
installs and runs; the first run was blinded by an axis-2 defect in the probe's own
construction. +2 actions per fork.

**Nothing here is device-verified, and none of it is claimed to be.** DIST-03 is open. The
repaired removal path has never run on a phone; what is proven is structural — the corpus
tally, the build guard and its negative control, gate A at the project target, and the AEA1
decrypt of both signed containers showing recovered action arrays equal to their sources with
`Matches` present and the retired guess absent. Whether the removal branch actually reaches its
confirmation menu on device remains exactly as unproven as it was before this plan.

---

## 33. Phase 11 — the fork that an unrelated setting deleted: one audit per OPEN-arm rendering (plan 11-09, 2026-08-18)

### The measurement that exposed it

Re-measured against this plan's own base rather than transcribed from the plan text, which was
written before 11-07 and 11-08 landed:

| measure | Core | Aware |
|---|---:|---:|
| actions | 4304 | 4438 (was 4372) |
| `persist_contract()` contract markers, whole artifact | 11 | 11 |
| — of those, **inside the OPEN arm** | **2** | **2** |
| — of those, in the MANUAL arm's Test-a-Circle submenu | 9 | 9 |
| `is.workflow.actions.askllm` | 0 | **2** (was **1**) |

Eleven dispatch renderings, eleven markers, **two of them in the OPEN arm** — and exactly
**one** model call on the shipped Aware fork. That gap is the defect. `universal_leaving()`
renders `primitive_dispatch()` twice: once inside the `Continue` case of the Leaving/Continue
menu, and once in the otherwise arm taken when the user has **removed the Panic Escape bypass**
(Mechanism A, plan 11-05). Each rendering reaches Intention, which calls `persist_contract()`,
which emits the marker. `build_sentient.py` inserted its audit at the **first** marker in
document order and then `break`-ed.

### What the user experienced, and why it is a spoofing defect rather than a missing feature

Remove the Panic Escape bypass — a setting with no relationship whatsoever to on-device
intelligence — and your Aware fork reaches the Intention primitive with **no contract audit at
all**, on every open, for as long as the bypass stays off. Nothing on device says so. The
install still presents as Aware: its own name, its own icon, its own Note, its own `"fork":
"Aware"` state seed. It simply *is* Core on that path. That is T-11-47, spoofing: the artifact
misrepresents itself to the person running it.

`docs/sentient_core_check.py` asserted the model count as a literal **1**. That is the count the
**missing** audit produces, so the checker agreed with the defect rather than reporting it — it
pinned the defect instead of detecting it, and went on doing so across the three phases (12, 13,
16) that executed after the original review named it.

### The two available resolutions, and why the other one was rejected

Both were legitimate and one had to be chosen.

**REJECTED — record "audit only the Panic-Escape-enabled path" as a deliberate product decision
in `docs/CAPABILITY-DECISIONS.md` and surface it in the Note.** Three reasons, and it is
recorded as *rejected* rather than merely *not taken* so that a future reader does not
rediscover it as an option:

1. **It is not a statable product rule.** Written out honestly it reads: *if you remove the easy
   exit, you also lose the on-device intelligence audit.* Those two features have nothing to do
   with each other. A user cannot predict it, cannot want it, and cannot undo one without the
   other. Recording it would be documenting a defect in the vocabulary of a feature.
2. **It inverts the escalation.** The bypass-removed path is the *harder* path: the user has
   deliberately given up their exit and goes straight into the intervention. That is precisely
   the moment a contract audit is most useful, and the behaviour removed it exactly there.
3. **It is the same silent-degradation class this phase's own guard work exists to eliminate** —
   two well-formed halves that stopped agreeing with each other and produced no error, one level
   up: a fork that silently becomes the other fork, with nothing on device to see.

**CHOSEN — insert into every OPEN-arm rendering, located structurally.** The OPEN arm is derived
from the router's own OPEN literal test and its `GroupingIdentifier`, the same derivation
`verify_circle_zero_silence()` uses, so a future rendering added anywhere inside that arm is
covered with no further code change. Scoping to the OPEN arm rather than sweeping every marker
in the file is also deliberate: the other nine are the Test-a-Circle diagnostic submenu in the
MANUAL arm, and auditing those would put an on-device model call behind a diagnostic menu item
(T-11-51). They are excluded **by construction**, not by an index.

### The hazard the choice created, both halves of it, and how each was closed

A second `audit_block()` call is only legal if its identifiers differ from the first's.
`.claude/CLAUDE.md` §4 names a reused `GroupingIdentifier` as this toolchain's **#1 documented
real-world mistake**: it validates, signs and imports perfectly and then silently corrupts a
block boundary at run time.

This fork's `uid()` is a `uuid5` **name hash**, not Dumb's positional counter, so a repeated
literal is a *guaranteed* collision rather than an unlucky one. There are **two** routes to one,
and the second is easy to miss:

* the **14 bare `uid()` calls** inside `audit_block()` — 10 in the tuple unpacking at the top and
  **4 inline inside the returned list**, which is where a sweep loses them;
* the **10 `if_block(key=)` arguments**, because `if_block()` derives its `GroupingIdentifier`
  from `uid(key)` too.

**Phase 16 (16-01) closed only the first half of the second route, and it is worth being exact
about what it did and did not do.** It made `if_block()`'s `key` argument **required** rather
than defaulted, which stops two call sites *omitting* it and silently deriving the same
identifier. It cannot stop two call sites *passing the same literal* — and `audit_block()`
passes fixed literals (`"enabled"`, `"circle-min"`, …) deliberately. So a second call to
`audit_block()` would have collided on all ten groups just as surely as before that change, only
now by explicit argument rather than by omitted default. Making the key required moved the
obligation from "remember to pass a key" to "remember the key must differ per rendering". This
plan satisfies the second obligation.

The mechanism is one required `ordinal` parameter and a single nested `aid()` helper that every
identifier in the function passes through — there is no route to an identifier that bypasses it,
which is what makes a missed call site unrepresentable rather than merely unlikely. The census is
stated as measured, and one figure in the plan was wrong: **10** `if_block()` calls, not the nine
the plan predicted.

### The negative controls, and the one that found a gap in the guards

Both routes were broken deliberately, one at a time, rebuilt, and observed.

**Control A — one bare `uid()` call** (`uid("scope-bounded-text")`, the ordinal dropped):

```
python3 tools/build_sentient.py                       -> built ..., EXIT 0     (!)
validate-shortcut ... --target-macos 26 ... all       -> Validation passed.    (!)
whole-artifact UUID count                             -> 1116 distinct of 1117, a NEW duplicate
```

**The build passed and gate A passed.** `verify_group_identifier_uniqueness()` asserts start/end
ownership of **`GroupingIdentifier`s**, so a collision on the action **`UUID`** axis is outside
it by construction, and the validator does not check UUID uniqueness at all. The **only** thing
that caught control A was an explicit whole-artifact UUID count. That is a real limit in the
standing guard set and is recorded here rather than left implicit.

**Control B — one `if_block()` key** (`key="fast"`, the ordinal dropped):

```
a GroupingIdentifier is not owned by exactly one control-flow block -- a reused identifier
silently corrupts block boundaries at runtime: F05BC2CA-D66A-5B6F-981A-46C0EE877F8E:
2 start(s) at [1101, 1419] and 2 end(s) at [1132, 1450] (1 total)
EXIT CODE: 1
```

Phase 16's guard fires and the build **fails closed** before writing an artifact — exactly the
"next insertion" its own arming comment anticipated. Restored, the rebuild reproduced the
pre-control SHA-256 byte for byte.

**Both checkers were also shown failing on a defect that was invisible to them beforehand**, by
running the retired version alongside the new one on the same mutated artifact:

| mutation, on a scratch copy | retired checker | new checker |
|---|---|---|
| delete one whole audit block | `sentient_core_check` **exit 0** | **exit 1**, naming the count mismatch |
| remove the latency gate from the **second** block only | `sentient_audit_check` **exit 0** | **exit 1**, naming block 1 |

### Two guards armed on the Aware chain, and one index defect closed

`verify_circle_zero_silence` and `verify_parameter_keys` were imported by the Dumb builder and
had **never** run on the Aware fork (WR-10, unresolved by Phases 12, 13 or 16). The first is
directly load-bearing for this change — its four properties are precisely the ones an OPEN-arm
insertion can break, and this fork is the only artifact that performs such an insertion. Both
were measured **clean on the pre-change Aware fork** before arming, so a future raise is a
finding about the insertion and must be investigated, never suppressed.

**WR-11, closed in the same pass.** The third import preference was spliced at a hard-coded
action index, and the appended import question repeated that same integer as its `ActionIndex` —
two literals free to drift apart, in a generator whose own module docstring forbids addressing an
anchor by a mutable index, at a position `build_state_engine.main()`'s pinned prologue (first
five actions) does not cover. Both now derive from one content anchor, the set-variable naming
the second import preference. Control, on a scratch copy: insert one filler action upstream of
the import prologue and rebuild.

```
DERIVED  ActionIndex 7 -> is.workflow.actions.gettext 'yes'; next names 'Import AI'
RETIRED  ActionIndex 6 -> is.workflow.actions.setvariable   (no WFTextActionText at all)
```

The retired literal would have pointed the question's `ParameterKey: "WFTextActionText"` at an
action that does not define that parameter — silently, with no error from either builder and no
finding at either validator gate. Per axis 1, a key an action does not define is ignored and
reads empty.

### What this does NOT establish

Stated separately and deliberately, because a structural result recorded as a behavioural one is
threat **T-11-52**, repudiation.

* **No Use Model call in either audit block has ever been made on Apple-Intelligence-capable
  hardware**, by anyone, at any point in this project. Not once. Not in this plan, and not in any
  plan before it.
* **A simulator can never settle it.** Apple Intelligence sits inside `.claude/CLAUDE.md` §9's
  explicit "Rung 2's ceiling" list — the simulator is not AI-capable hardware — so this is a
  rung-3+ question no amount of agent time can close. It was therefore not attempted, rather than
  attempted and reported inconclusive.
* **The audit's runtime behaviour is unproven** in every respect: whether the model returns a
  parseable first token, whether it completes inside the eight-second latency gate, whether the
  pinned on-device source is honoured at run time, and whether the `CHALLENGE` revision prompt
  and the high-circle `DENY` redirect behave as designed. The `WFLLMModel` literal itself is
  donor-confirmed (`"Apple Intelligence on Device"`, BD-04-R2) — that is a fact about what a
  device **writes**, not about what this artifact **does**.
* **DIST-03 is open**, and it is the blocker for all of the above. Nothing in this plan narrows
  it. What this plan changes is *how many renderings the eventual device test will cover* — two
  instead of one — and **nothing** about its outcome.

What **is** established is structural and only structural, at rung 1: two audit blocks exist, one
per OPEN-arm rendering; the count is derived at build time and in both checkers rather than
pinned; no identifier is shared between them; the nine MANUAL-arm markers carry no model call;
both forks pass gate A; and the Aware container decrypts to an action array equal to its source
with both model actions carrying the pinned on-device literal.
