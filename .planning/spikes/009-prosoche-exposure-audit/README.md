---
spike: 009
name: prosoche-exposure-audit
type: standard
validates: "Given spike 006's taxonomy, when applied to every action PROSOCHĒ's generators actually emit, then the complete blocker list is known and each blocker either has a workaround or is confirmed unbuildable"
verdict: VALIDATED
related: [006, 007, 008]
tags: [capability-audit, blocker-analysis, generators, pickers, entity-references]
---

# Spike 009: PROSOCHĒ Exposure Audit

## What This Validates

**Given** spike 006's three-class taxonomy, **when** applied to every action
PROSOCHĒ's generators actually emit, **then** the complete blocker list is known and
each blocker either has a workaround or is confirmed unbuildable.

This is the spike the whole session was for. 006 established *what can* be
hand-selection-only; this one establishes *whether PROSOCHĒ hits any of it*.

## How to Run

Extract every first-party action identifier the generators emit, then look each one up in
the ToolKit parameter catalog and flag parameters typed `*_entity` or `*_parameter`:

```bash
grep -rhoE '"(is\.workflow\.actions|com\.apple)[A-Za-z0-9_.]*"' tools/*.py | tr -d '"' | sort -u
```

## Investigation Trail

**Inventory.** `tools/build_state_engine.py` and `tools/build_sentient.py` emit
**51 distinct first-party action identifiers**. Of those, 46 are in the v78 catalog and 5
are legacy control-flow rows the catalog omits entirely (`conditional`, `choosefrommenu`,
`repeat.count`, `repeat.each`, `filter.contentitems`) — a known gap already recorded in
CLAUDE.md's evidence hierarchy, and none of them takes an entity or picker parameter.

**Classification.** Of the 46 catalogued actions, **41 have only primitive parameters** —
no picker risk of any kind. `alert`, `ask`, `count`, `date`, `getdevicedetails`,
`getitemfromlist`, `math`, `notification`, `openapp`, `openurl`, `setbrightness`,
`setvolume`, `speaktext`, `text.match`, and the rest are all `str` / `bool` / `float` /
`int` / `DateTime` / `File` / `URL`.

**Exactly five actions carry an entity or enum-picker parameter.** All five are Notes or
Use Model:

| action | parameter | type | class | evidence |
|---|---|---|---|---|
| `com.apple.mobilenotes.SharingExtension` | `folder` | `com_apple_notes_folder_entity` | **A** | `Donor - notes` writes `applenotes:folder/DefaultFolder-CloudKit` — a readable URI, not a minted id |
| `is.workflow.actions.filter.notes` | `WFContentItemFilter` | `query_…note_entity` | **A** | a *query* type, not an entity reference. Donor 8 writes `Name contains "PROSOCHE"` — operator `99`, plain string |
| `is.workflow.actions.filter.notes` | `WFContentItemInputParameter` | enum | **A** | catalogued in `enum-cases.json` |
| `is.workflow.actions.shownote` | `target` | `com_apple_notes_note_entity` | **B** | Donor 8 feeds it from `filter.notes` output as a plain `WFTextTokenAttachment` |
| `is.workflow.actions.appendnote` | `entity` | `com_apple_notes_note_entity` | **B** | generator writes `entity=variable("Control Room Note")` |
| `is.workflow.actions.askllm` | `WFLLMModel` | uncatalogued enum | **A** | spike 008: `"Apple Intelligence on Device"`, donor ground truth |

**The Control Room Note path, traced end to end.** This was the one genuinely load-bearing
case — the entire Control Room design depends on it, and CLAUDE.md §3 item 5 calls Notes
*"the single most consequential trust-but-verify item in this audit."*

`tools/build_state_engine.py:1646` writes:

```python
action("is.workflow.actions.appendnote", operation="append",
       entity=variable("Control Room Note"), text=output(snapshot_id, "Text"))
```

`"Control Room Note"` is bound in **both** branches — the found branch (`filter.notes`
matching on name) and the created branch (`SharingExtension`) — and consumed everywhere as
a named variable. **No note identifier is ever written into the plist.** PROSOCHĒ finds its
note by name at runtime, which is textbook Class B and exactly the pattern Donor 8 proves
on real hardware.

## Results

**VALIDATED — no blockers. The answer to the motivating question is: nothing PROSOCHĒ
needs requires a hand selection in Shortcuts.app.**

Every one of the 51 emitted actions is authorable offline:

- **41 actions** — primitive parameters only. No exposure.
- **5 actions** — control-flow rows with no picker parameters.
- **4 entity/enum slots** resolved **Class A** (synthesizable from a donor-confirmed
  literal or a catalogued enum case).
- **2 entity slots** resolved **Class B** (fed by a runtime variable from a query action).
- **0 slots Class C.**

### Why the fear was reasonable but doesn't land

The worry was well-founded in kind — Shortcuts genuinely does have 1,305 entity-typed
parameters across 703 entity types, and many of those *are* hand-selection-only because
their families have no query action. Home accessories, Focus modes, Safari tabs, Mail
accounts, Wallet passes: all real Class C.

PROSOCHĒ simply doesn't touch any of them. Its surface is Notes, Files, six first-party
apps, system controls, and arithmetic. Notes is one of the 14 queryable families, so its
two entity slots resolve to Class B. Files is queryable too and PROSOCHĒ uses fixed paths
anyway. The six apps are first-party with a donor-confirmed team identifier.

### Two claims to promote out of spike-land

1. **`WFLLMModel = "Apple Intelligence on Device"`** (spike 008) — CLAUDE.md §3 item 15 and
   its summary-table row should move from "UNVERIFIED — do not guess" to VERIFIED (donor).
   This was the last uncatalogued enum picker in the entire first-party surface.
2. **The simulator cannot import a signed `.shortcut`** (spike 007) — CLAUDE.md §9 lists
   "import success" as a rung-2 capability. Measured, it is not, on a simulator with no
   iCloud account. The rung-2 row needs correcting.

### Standing caveats

- This audits what the generators **emit today**. Any future feature reaching into Home,
  Focus, Music, Photos, Safari tabs, or Mail re-opens the question — those families have no
  query action and are the genuine Class C residue. The predictive rule in spike 006 is the
  cheap check to run before adopting any new action.
- The audit is rung-1 (file + catalog + donor). It establishes that every value we need
  **can be written**. It does not re-litigate whether each action *behaves* correctly at
  runtime — that is what the project's existing device-evidence trail covers, and several
  of these actions already carry their own device verdicts.
