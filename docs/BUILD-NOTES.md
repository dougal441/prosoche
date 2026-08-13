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

## 5. Deviation log

Numbered entries `DEV-01`, `DEV-02`, ... Each entry carries exactly five labelled fields: `Capability`, `Wanted`, `Verified`, `Substituted`, `Runnability`.

### DEV-01

- **Capability:** CAP-20 — Color Filters / grayscale (Ash primitive, canonical strategy §11 Primitive B).
- **Wanted:** The Ash primitive as literally specified in canonical strategy §11 Primitive B — "Grayscale where iOS can apply and restore it safely," a passive reduction of visual salience via a system-level grayscale toggle.
- **Verified:** `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` exists in the generic `toolkit-v63-tool-ids.json` and `toolkit-v78-tool-ids.json` snapshots, but its parameter-catalog record and every one of its three parameters are tagged `platforms: ["macOS 27"]` only, and the identifier does not appear at all in the iOS-27-Simulator-specific `toolkit-v78-ios27-tool-ids.json` snapshot. No grayscale/Color Filters action of any kind is confirmed available to Shortcuts.app on iPhone. No read-back mechanism for the current Color-Filters state exists in any bundled snapshot, consistent with there being no confirmed set action to read back from.
- **Substituted:** Per BD-01 in `docs/CAPABILITY-DECISIONS.md`, Ash is degraded to a non-environmental variant of Primitive B for the iOS build rather than a system-level Color Filters toggle. See BD-01 for the full rationale and the selected option among D-08's three named alternatives.
- **Runnability:** The Shortcut remains runnable because the Ash sequence slot (position 2 in Classic and Ambient, combined into "Ash + Confession" at position 3 in Black Mirror per canonical strategy §12) still resolves to a defined, safe, non-system-altering behaviour under BD-01's decision, and no OPEN-path routing depends on a grayscale action existing — per D-07 point 4 ("keep the Shortcut runnable... never let an unverified action block the OPEN/CLOSE path, corrupt state, or prevent Circle IX's always-a-route-out guarantee").

## 6. User action items

_Owner: appended to by plans 01-04 and 01-05. Entries are numbered `UA-01`, `UA-02`, ... each with the labelled fields `What`, `Why only a human can do it`, `Exact steps`, `What to record on completion`, `Which phase is gated`._

## 7. Coverage check

_Owner: finalised by plan 01-05._
