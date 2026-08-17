# Authoring Parameters

How to write any Shortcuts parameter correctly, offline, without guessing.

## Requirements

- **Never fabricate a literal.** If a value cannot be sourced from a donor, the enum-cases
  catalog, or an `.intentdefinition`, it is not known. Use the safest fallback and record
  the deviation.
- **Never write an entity identifier into a plist.** Find the entity at runtime.
- Every value PROSOCHĒ needs is authorable offline — this is proven, not assumed
  (spike 009). Keep it that way: run the three-class check before adopting any new action.

## How to Build It

### Step 1 — classify the parameter before writing it

Look up the parameter's `typePythonName` in
`~/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/skills/shortcuts-playground/data/toolkit-v78-first-party-parameter-keys.json`:

| `typePythonName` | Class | What to do |
|---|---|---|
| primitive — `str` `bool` `float` `int` `DateTime` `File` `URL` `AttributedString` | **A** | write it directly |
| `*_parameter` (enum picker) | **A** | look up cases in `toolkit-v78-first-party-enum-cases.json`; **525 of 526 are catalogued** |
| `*_entity` | **B** if the family has a `filter.*` action; **C** otherwise | B → feed from a query action's output. C → cannot be authored offline |

The **14 queryable entity families** (i.e. the ones that make Class B possible):

```
apps  articles  calendarevents  contacts  displays  eventattendees  files
images  locations  music  notes  photos  reminders  windows
```

Anything outside that list — Home accessories, Focus modes, Safari tabs, Mail accounts,
Wallet passes, Podcasts episodes, Freeform boards, TV devices — is **Class C**: it must be
hand-picked inside Shortcuts.app on a device and exported. Treat adopting such an action as
a design decision, not an implementation detail.

**Gotcha:** `toolkit-v78-first-party-enum-cases.json` nests everything one level under a
top-level `types` key. A top-level sweep finds nothing and produces a false "undocumented"
conclusion. Descend into `types` first. (This mistake is already recorded as a factual error
in `docs/BUILD-NOTES.md` CAP-20.)

### Step 2 — Class B: satisfy an entity slot with a variable

The reference pattern, donor-confirmed on hardware (`sources/006-.../donor-xml/Donor8-Shortcut.xml`):

```
[0] is.workflow.actions.filter.notes
      WFContentItemFilter → WFContentPredicateTableTemplate
         Operator 99 (contains), Property "Name", Values.String "PROSOCHE"
      WFContentItemLimitEnabled true, WFContentItemLimitNumber 1.0
      → outputs "Note"

[1] is.workflow.actions.shownote
      WFInput = { Value: {OutputUUID: <step 0 UUID>, OutputName: "Note",
                          Type: "ActionOutput"},
                  WFSerializationType: "WFTextTokenAttachment" }
```

No note identifier appears anywhere in the file. The generators already do this —
`entity=variable("Control Room Note")` at `tools/build_state_engine.py:1646`, with the
variable bound in both the found (`filter.notes`) and created (`SharingExtension`) branches.

### Step 3 — the seven parameter-defect axes still apply

Class A/B is about *whether the value is knowable*. The envelope is a separate question, and
every axis below was established by on-device failure. All are asserted by build guards in
`tools/build_state_engine.py`:

1. **Key names must match the catalog exactly.** `setvalueforkey` takes `WFDictionaryValue`,
   not `WFInput`. An undefined key is silently ignored and reads empty.
2. **`str`-typed parameters need `WFTextTokenString`** (`￼` placeholder + `attachmentsByRange`).
   A bare `WFTextTokenAttachment` resolves to empty at runtime.
3. **`AttributedString`-typed parameters need the same treatment** — e.g. `WFCreateNoteInput`.
   A type-scoped sweep looking only for `str` misses these.
4. **Required enum pickers must be present and hold a literal case.** Known instances:
   `count.WFCountType`, `getitemfromlist.WFItemSpecifier`. An unfilled picker reports
   "Please choose a value for each parameter in this action."
5. **Variable slots take the *opposite* envelope from string parameters.** `WFInput.Variable`
   requires a bare `WFTextTokenAttachment`. Rules 2 and 5 are inverses — check which position
   you are in first.
6. **Non-text parameters fed by a variable need an explicit coercion aggrandizement:**
   ```xml
   Aggrandizements = [{ Type: WFCoercionVariableAggrandizement,
                        CoercionItemClass: WFNumberContentItem }]
   ```
   Confirmed necessary for numeric comparison; confirmed **not** needed for date parameters.
   Booleans, files, dictionaries and entity references remain **unaudited** — establish each
   `CoercionItemClass` from a donor, never guess it.
7. **State shape must exist before it is read.** A dotted read raises if any segment is
   absent, so bootstrap must seed the full subtree.

### Step 4 — donor-confirmed literals you can use today

| Where | Literal | Source |
|---|---|---|
| `askllm.WFLLMModel` | `"Apple Intelligence on Device"` | spike 008 donor |
| `getdevicedetails.WFDeviceDetail` | `Device Model`, `Current Brightness`, `Current Volume`, `Current Appearance`, `Device Is Locked` | spike 001 (Donor 10) |
| `AXToggleColorFiltersIntent.state` | `1` = On, `0` = Off (bool-as-integer) | spike 005 donors |
| `AXToggleColorFiltersIntent.operation` | `"toggle"`; **omit entirely for Turn** | spike 005 donors |
| `SharingExtension.folder.identifier` / `WFNoteGroup.Identifier` | `applenotes:folder/DefaultFolder-CloudKit` | `Donor - notes` |
| `openapp.WFSelectedApp.TeamIdentifier` | `"0000000000"` (first-party apps) | `Donor - apps` |
| `filter.notes` name predicate | `Operator` `99` = contains | Donor 8 |

`AppIntentDescriptor` is `{AppIntentIdentifier, BundleIdentifier, Name, TeamIdentifier}` and
is fully synthesizable — observed identifiers `CreateNoteLinkAction`, `NoteEntity`,
`OpenNoteLinkAction`, all with `BundleIdentifier` `com.apple.mobilenotes`.

## What to Avoid

- **Do not treat an `.intentdefinition` as the plist encoding.** It declares the intent's
  *type system* — parameter names, enum case ids, response parameters. Shortcuts serializes
  through its own UI rendering, and the two do not match. Spike 005 got this wrong twice:
  read `Integer` storage as the encoding (wrong — `operation` writes a case-id **string**),
  then read the `State` enum's case indices as the values (wrong — `on`=1/`off`=2 in the
  schema, but Shortcuts writes a plain **bool as `0`/`1`**). The second error would have
  shipped a restore leg leaving users stuck in grayscale. **Use it to learn what parameters
  exist and what a picker's cases are called; use a donor to learn what gets written.**
  A precise-looking new source does not outrank a donor — precision is not rank.
- **Do not conclude "unavailable" from a catalog miss — doubt the identifier first.** iOS
  ships private `AX*Intent` twins of the public macOS `UA*Intent` accessibility actions
  (`com.apple.AccessibilityUtilities.AXSettingsShortcuts` ↔
  `com.apple.UniversalAccess.UASettingsShortcuts`). The `AX*` identifiers are in **none** of
  the three bundled ToolKit snapshots, so no catalog query can find them at any target
  setting. When a capability "doesn't exist" but users demonstrably do it on their phones,
  the identifier is the thing to doubt.
- **Do not read parameter absence as meaningless — but do not over-read it either.** Both
  Color Filters donors omit `operation` because `turn` is its default, so omitting is
  *better* than authoring an unconfirmed literal. But Donor 9 also contains a fully
  parameter-less instance of an action another donor writes with `state` set. Read absence
  across several donors before concluding anything.
- **Do not use a `has any value` gate on a dotted path.** The read hard-errors unless the
  final key exists; if it exists, the gate is true. There is no state in which the gate reads
  false without the read having already thrown. No sentinel value fixes this. Gate on a
  numeric `> 0` test, or restructure to a flat read.
- **Do not synthesize an `AppIntentDescriptor` for Create Note from the documented template
  pattern.** Spike 002 v1 tried it and the shortcut imported as "unknown action." Copy the
  donor's descriptor.
- **Do not reuse a UUID as both an action's `UUID` and a control-flow block's
  `GroupingIdentifier`.** Spike 002 v2 hit this live; it is the project's #1 documented
  real-world mistake.
- **Fix whole classes, never site-by-site.** Bisection only ever reveals the earliest
  remaining site, so incremental fixing costs one device round trip per site. Every defect
  found in the big debug session was systematic: 147, 367, 25, 20 and 8 sites respectively.

## Constraints

- **Operator/operand type validity is invisible in the plist.** Shortcuts offers comparison
  operators based on the **left** operand's resolved type: uncoerced Dictionary Value → only
  `has any value`; text-coerced → the eight string operators; Number-coerced → numeric
  comparators. A numeric `WFCondition` on a text-typed operand renders **red** in the UI, is
  structurally valid in the file, and fails at runtime. **No file-level analysis can detect
  this** — not the validator, not the catalog, not decrypting the signed artifact.
- **Verified runtime read semantics** (donor-established, not in the Playground bundle):

  | construct | behaviour |
  |---|---|
  | flat read of a **missing** key | returns nothing, no error → `has any value` **false** |
  | flat read of a **present but empty** value | → `has any value` **true** |
  | **dotted** read (`a.b`) with any missing segment | **hard error**, "could not evaluate the key path" |
  | `"null"` or `""` coerced to `WFNumberContentItem` | **false**, no error |

- **No file-existence check exists.** Use `WFFileErrorIfNotFound = false` on Get File — this
  is the real mechanism, cleaner than attempt-and-treat-as-absent.
- **State-dictionary presence check:** gate on whether `Detect Dictionary`'s output itself
  `has any value` (condition code `100`), never on reading a specific key.
- **Control-flow identifiers are absent from the ToolKit catalog entirely**
  (`conditional`, `choosefrommenu`, `repeat.*`, `filter.contentitems`), so catalog-driven
  sweeps are blind to them.
- Scale of the general problem: **1,305 entity-typed parameters across 703 entity types**;
  **526 enum-picker types**, of which exactly one was uncatalogued (`WFLLMModel`, now settled).

## Origin

Synthesized from spikes: 001, 005, 006, 008, 009
Source files: `sources/001-device-is-locked-literal/`, `sources/005-ios-color-filters-identifier/`,
`sources/006-picker-serialisation-taxonomy/`, `sources/008-use-model-picker-literal/`,
`sources/009-prosoche-exposure-audit/`
