---
spike: 006
name: picker-serialisation-taxonomy
type: standard
validates: "Given all 16 project donors plus the 19-shortcut golden corpus, when every parameter that could carry a device-minted value is decrypted and classified, then each falls into synthesizable / runtime-derivable / hand-selection-only, and a rule exists for predicting the class from the catalog alone"
verdict: VALIDATED
related: [005, 007, 008, 009]
tags: [capability-audit, evidence-hierarchy, entity-references, pickers, donor, blocker-analysis]
---

# Spike 006: Picker Serialisation Taxonomy

## What This Validates

**Given** all 16 project donors (`.planning/debug/*.shortcut`) plus the 19-shortcut
golden corpus, **when** every parameter that could carry a device-minted value is
decrypted and classified, **then** each falls into one of three classes —
synthesizable / runtime-derivable / hand-selection-only — and a rule exists for
predicting the class from the ToolKit catalog alone.

The motivating fear: some Shortcuts constructs may only be authorable by tapping a
picker inside Shortcuts.app on a real device, because the value written is an opaque
identifier that only the owning app can mint. If such a construct sits on PROSOCHĒ's
critical path, the entire offline build-and-sign pipeline is blocked for that feature,
and the only route is hand-author → export → decrypt.

## Research

Three evidence sources, in this project's own hierarchy order:

1. **Donors** (tier 1) — all 16 `.shortcut` files in `.planning/debug/`, decrypted via
   the AEA1 round-trip (CLAUDE.md §8). All 16 decrypted cleanly, zero failures.
2. **Golden corpus** (tier 2) — the 19 real-world shipped shortcuts bundled with
   Shortcuts Playground v1.2.1.
3. **ToolKit catalog** (tier 3) — `toolkit-v78-first-party-parameter-keys.json`
   (2,585 tools) and `toolkit-v78-first-party-enum-cases.json` (2,180 enum types).

`sweep.py` (in this folder) walks every action's parameter tree across sources 1 and 2
and flags any value that looks device-minted: bare UUIDs outside structural slots,
URI-shaped identifiers, app-identity fields, and any binary or base64 blob.

## How to Run

```bash
python3 .planning/spikes/006-picker-serialisation-taxonomy/sweep.py <donor-xml-dir> <golden-xml-dir>
```

Donor XML is recovered with the AEA1 round-trip in CLAUDE.md §8. Three decrypted
donors central to the verdict are archived in `donor-xml/` for reference.

## What to Expect

A hit list of every candidate device-minted value, grouped by action identifier and
parameter path, with distinct-value counts.

## Investigation Trail

**Pass 1 — targeted heuristic sweep.** 35 hits across 35 shortcuts. Every single hit
was a **human-readable string**. Zero bare-UUID entity references. The only structural
UUIDs present were `UUID` / `GroupingIdentifier` / `OutputUUID` / `VariableUUID` —
all values *we* mint at build time, not values the device mints.

**Pass 2 — broadened sweep**, in case the pass-1 regexes were too narrow. Enumerated
every `WFSerializationType` in use, every dict-valued parameter slot, and any binary or
base64 payload.

- **Serialization types in use: 8.** All already documented and authorable —
  `WFTextTokenString` (239), `WFTextTokenAttachment` (192), `WFDictionaryFieldValue` (24),
  `WFContentPredicateTableTemplate` (3), `WFNumberSubstitutableState` (3),
  `WFQuantityFieldValue` (2), `WFTimeOffsetValue` (2), `WFArrayParameterState` (1).
- **Opaque blobs: NONE.** No security-scoped bookmarks, no binary payloads, no base64.
  This was the single most feared shape and it does not appear anywhere in 35 shortcuts.
- **Only three entity-slot shapes exist** in the whole evidence base:
  `AppIntentDescriptor`, `WFSelectedApp`, and `WFNoteGroup`/`folder`.

**Pass 3 — the escape hatch.** Pass 1 and 2 establish that the *evidence base* is clean,
but the evidence base does not exercise Home, Focus, Music, Photos, Safari tabs, or Mail.
So the question became: what makes an entity-typed parameter authorable at all?

`Donor 8` answers it on real hardware. It wires **Find Notes → Show Note**:

| step | action | how the entity is supplied |
|---|---|---|
| 0 | `is.workflow.actions.filter.notes` | predicate: `Name` **contains** `"PROSOCHE"` — operator `99`, a plain `Values.String`. Fully authorable offline. |
| 1 | `is.workflow.actions.shownote` | `WFInput` = plain `WFTextTokenAttachment` → `ActionOutput` of step 0 |

**No note identifier appears anywhere in the file.** The entity-typed slot is satisfied
by a runtime variable, and the query that produces that variable is a pure string
predicate. This is the general escape hatch, confirmed at tier 1.

**Pass 4 — catalog-side generalisation.** Classified all 8,087 parameters across the
2,585 first-party tools by `typePythonName`:

| kind | count | authorability |
|---|---:|---|
| primitive (`str`, `bool`, `float`, `int`, `DateTime`, `File`, `URL`, …) | 6,256 | always synthesizable |
| **entity** (`*_entity`, 703 distinct types) | 1,305 | Class A or B — see rule |
| **enum picker** (`*_parameter`, 526 distinct types) | 526 | Class A if catalogued |

Then checked enum-picker coverage against the enum-cases catalog:

> **525 of 526 distinct enum-picker types are catalogued.**
> **Exactly one is not: `com_apple_shortcuts_wfask_llmmodel_parameter`** — the `Use Model`
> model picker, which is precisely the item CLAUDE.md §3 item 15 flags as "the single most
> important UNVERIFIED item for the Sentient fork."

That one is settled by donor in **spike 008** (`WFLLMModel = "Apple Intelligence on Device"`),
which empties the class.

**Pass 5 — which entity families are queryable.** An entity slot is runtime-derivable only
if the owning app ships a query action whose predicate is expressible in primitives. The
legacy filter family in `toolkit-v63` gives the definitive list — **14 queryable families**:

```
apps  articles  calendarevents  contacts  displays  eventattendees  files
images  locations  music  notes  photos  reminders  windows
```

Entity families with **no** query action (Home accessories, Focus modes, Safari tabs, Mail
accounts, Podcasts episodes, Wallet passes, Freeform boards, TV devices, …) are the genuine
Class C residue. None is exercised by any donor, and — pending spike 009's formal audit —
none appears on PROSOCHĒ's critical path.

## Results

**VALIDATED.** The taxonomy holds, and it has three classes:

### Class A — Synthesizable offline
The value is a public, stable string we can write from documentation alone.

| shape | donor-confirmed value | notes |
|---|---|---|
| `WFAppIdentifier` | `com.apple.mobilenotes` | bare bundle id |
| `WFSelectedApp` | `{BundleIdentifier, Name, TeamIdentifier}` | first-party `TeamIdentifier` is always `0000000000`; third-party is spike 007's question |
| `AppIntentDescriptor` | `{AppIntentIdentifier, BundleIdentifier, Name, TeamIdentifier}` | `CreateNoteLinkAction`, `NoteEntity`, `OpenNoteLinkAction` observed |
| `WFNoteGroup` / `folder` | `applenotes:folder/DefaultFolder-CloudKit` | a readable URI, **not** a UUID; `folder`'s siblings are pure display chrome (title/subtitle/SF Symbol) |
| catalogued enum pickers | 525 of 526 types | look up in `toolkit-v78-first-party-enum-cases.json` — descend into `types` first (CONVENTIONS.md gotcha) |

### Class B — Runtime-derivable
An entity-typed slot fed by a query action's `ActionOutput`. Requires **both**:
1. a query/filter action exists for that entity family (14 of them), **and**
2. the predicate is expressible in primitives (string / number / date).

Donor 8 proves the pattern end-to-end for Notes. This is the class that makes the
Control Room Note buildable offline — PROSOCHĒ never needs to know a note's identifier,
it finds the note by name at runtime.

### Class C — Hand-selection-only
An entity-typed slot with **no** query action for its family, or whose only query
predicate is itself an entity. **Currently empty for PROSOCHĒ's action surface** — and
now empty in general for enum pickers, since spike 008 settled the last uncatalogued one.

### The predictive rule (answers the "from the catalog alone" half)

```
look up the parameter's typePythonName in toolkit-v78-first-party-parameter-keys.json
  primitive (str/bool/float/int/DateTime/File/URL/…)  → Class A, write it directly
  *_parameter (enum picker)                           → Class A if in enum-cases.json
                                                        else donor / .intentdefinition
  *_entity                                            → Class B if the family has a
                                                        filter.* action, else Class C
```

### Surprises

1. **The feared shape does not exist in this evidence base.** Zero opaque blobs, zero
   bare-UUID entity references, across 35 real shortcuts. Every identifier written by a
   real device is human-readable. Going in, security-scoped file bookmarks looked like the
   likeliest hard blocker; they simply never appear.
2. **The whole "uncatalogued picker" problem reduced to exactly one parameter** out of 526
   — and it is the one this project had already independently flagged as its top unknown.
   Two entirely different lines of reasoning converged on the same single item, which is a
   good sign the taxonomy is not missing a category.
3. **`AppIntentDescriptor` is decorative-looking but ubiquitous.** It appears on all three
   Notes actions and is fully synthesizable. Worth writing rather than omitting, since every
   donor carries it.
4. **`folder` carries display chrome, not data.** `title`/`subtitle`/`symbol` are localisation
   keys and an SF Symbol name — Shortcuts UI state, not semantics. `identifier` is the only
   load-bearing field.

### Limits of this verdict

- The evidence base does not exercise Home, Focus, Music, Photos, Safari-tab, Mail, or
  Wallet pickers. Class C is asserted **empty for PROSOCHĒ's surface**, not empty in general.
  Spike 009 does the formal exposure audit.
- Class A's third-party `TeamIdentifier` case is unproven — all six `WFSelectedApp` donors
  are first-party. Spike 007 tests it.
- This is rung-1 evidence throughout (file-level analysis + donors). It settles *structure*.
  It does not settle whether an offline-authored picker renders correctly in Shortcuts.app —
  that is spike 007's rung-2 question.
