# PROSOCHĒ — Build Notes

## 1. Purpose and scope

This document is the durable capability record for the PROSOCHĒ build. Every later phase treats it as ground truth. It is **appended to, never rewritten** — once a row, deviation entry, or action item is recorded, later plans may only add new rows/entries or extend existing sections; they do not delete or silently reword what is already here.

It covers **iOS 26.x native Shortcuts only** (per D-01 — target iOS 26.x, native Shortcuts only, no companion app, no Screen Time blocking APIs, no private APIs).

## 2. Do-not-fabricate protocol

_Owner: completed by Task 2 of plan 01-01._

## 3. Evidence protocol

_Owner: completed by Task 2 of plan 01-01._

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
