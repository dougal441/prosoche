# Spike Wrap-Up Summary

**Date:** 2026-08-17
**Spikes processed:** 9 (all, first wrap-up)
**Feature areas:** authoring-parameters, evidence-and-probes, sentient-and-capability-gating,
session-model-and-automations, environmental-primitives
**Skill output:** `./.claude/skills/spike-findings-prosoche/`

## Processed Spikes

| # | Name | Type | Verdict | Feature Area |
|---|------|------|---------|--------------|
| 001 | device-is-locked-literal | standard | VALIDATED | session-model-and-automations, environmental-primitives |
| 002 | close-automation-vs-screen-lock | standard | VALIDATED | session-model-and-automations |
| 003 | device-model-literal | standard | **INVALIDATED** | sentient-and-capability-gating |
| 004 | capability-gate | standard | **PARTIAL** (downgraded 2026-08-17, was VALIDATED) | sentient-and-capability-gating |
| 005 | ios-color-filters-identifier | standard | VALIDATED | environmental-primitives, authoring-parameters |
| 006 | picker-serialisation-taxonomy | standard | VALIDATED | authoring-parameters |
| 007 | unresolvable-picker-failure-mode | standard | PARTIAL | evidence-and-probes |
| 008 | use-model-picker-literal | standard | VALIDATED | sentient-and-capability-gating |
| 009 | prosoche-exposure-audit | standard | VALIDATED | authoring-parameters |

## Key Findings

**Nothing in PROSOCHĒ requires a hand selection in Shortcuts.app.** The class of
hand-selection-only parameters is real and large in general — 1,305 entity-typed parameters
across 703 entity types, and only 14 entity families are queryable — but PROSOCHĒ's 51-action
surface touches none of it. Six picker slots exist across the whole build; four are
synthesizable from donor-confirmed literals, two are fed by runtime variables, zero are
blockers.

**The last unknown literal is now known.** Of 526 distinct enum-picker types in the entire
first-party surface, exactly one was uncatalogued — `WFLLMModel` — and it is precisely the
item CLAUDE.md §3 item 15 called the top unknown for the Sentient fork. A donor that had sat
unanalysed in `.planning/debug/` settles it: **`"Apple Intelligence on Device"`**. None of the
three spellings the audit was weighing was right.

**The feared shape never appears.** Across 16 donors and 19 shipped shortcuts: zero opaque
blobs, zero security-scoped bookmarks, zero bare-UUID entity references. Every identifier a
real device writes is human-readable. Entity slots are satisfied by variables from a query
action, never by literals — Donor 8 proves it end to end for Notes, and the generators
already do exactly that.

**Hardware capability detection is architecturally impossible**, not merely unimplemented.
`Device Model` returns the bare literal `"iPhone"` on every device. No other detail, no OS
version, no build number, and no app-presence check substitutes; the real API is Swift-only
and ruled out by the no-companion-app constraint. Combined with the absence of try/catch
anywhere in Shortcuts, this forces the design to an explicit toggle plus an **ordering**
fail-safe.

**But the ordering fail-safe's ineligible-hardware behaviour is unproven** (spike 004
downgraded to PARTIAL, 2026-08-17). The device recorded as the ineligible test never had its
generation noted, the run omitted `WFLLMModel` so it exercised the undocumented default model
source rather than the pinned On-Device path that ships, and the error it produced —
*"Support for selected model is downloading"* — is a **provisioning** message, not an
eligibility rejection. An iPhone 16e later ran the same shortcut successfully once its models
had downloaded, which is what exposed the misattribution. The failure window is therefore
wider than assumed: it reaches **capable hardware at first run**, before a ~7 GB model
download completes — which under a merged product is the most fragile moment in the product.
What survives is the structural property: the core runs first, so any downstream halt is
contained, and that was observed once under a real failure.

**Screen lock fires CLOSE.** The session model needs no separate lock trigger and no
lock-state poll. The residual hazard is storage, not signalling: file-permission prompts
re-appear on essentially every automation run and cannot be granted while the screen is
locked.

**Ash is real on iOS**, under `AXToggleColorFiltersIntent` — an identifier absent from all
three bundled ToolKit snapshots, which is why two prior decisions argued the availability
question using the macOS twin. Both legs are donor-confirmed.

## Methodological lessons worth more than any single verdict

- **Precision is not rank.** Apple's `.intentdefinition` is precise, well-structured, and
  authoritative-looking — and it describes the intent's type system, not the plist encoding.
  Spike 005 ranked it above a donor twice and was wrong both times; the second error would
  have shipped a restore leg leaving users in grayscale.
- **A catalog miss is not an absence.** When a capability "doesn't exist" but users
  demonstrably do it on their phones, doubt the identifier.
- **Check whether the question is on the critical path before climbing the ladder.**
  Spike 007 stopped mid-probe when five lines of the generator showed its question was moot.
- **The evidence was already on disk.** Three of these nine spikes were settled by decrypting
  donors that had been sitting unanalysed in `.planning/debug/` — including the single most
  consequential unknown in the project.

## Corrections owed to project docs

1. `.claude/CLAUDE.md` §3 item 15 and its summary-table row — `WFLLMModel` from
   "UNVERIFIED — do not guess" to **VERIFIED (donor ground truth)**.
2. `.claude/CLAUDE.md` §9 — the rung-2 row lists "import success" as a simulator capability.
   Measured, it is not: the simulator cannot import a signed `.shortcut` through any channel
   tried. Rung 2 tests the build, not the import.
3. `docs/BUILD-NOTES.md` CAP-20 — the claim that `operation` has "no case list found" is
   stale; the list is under the enum-cases file's top-level `types` key.
