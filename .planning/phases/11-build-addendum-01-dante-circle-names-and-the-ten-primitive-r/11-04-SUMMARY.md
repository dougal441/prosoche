---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
plan: 04
subsystem: build-decisions
tags: [decision-record, schema-version, state-migration, signed-artifacts, checkpoint-discharge]
requires:
  - "BD-06-A1 Amendment 3 — the user statement that there is no installed base"
  - "11-03 (wave 3) — appended BD-06-A2 immediately above this record"
provides:
  - "BD-06-A3 — the schema_version 2→3 disposition, binding on plans 11-05 and 11-06"
  - "BD-06-A3 — the old-named signed-artifact deletion disposition, binding on plan 11-06"
  - "The three-literal implementation surface in fix_state_rebind(), measured"
affects:
  - "11-05 — implements the bump alongside the Panic Escape seed field"
  - "11-06 — implements the bump alongside the fork rename, and deletes the old signed files"
tech-stack:
  added: []
  patterns: ["append-only numbered decision records in docs/CAPABILITY-DECISIONS.md"]
key-files:
  created: []
  modified:
    - "docs/CAPABILITY-DECISIONS.md — appended BD-06-A3 (143 lines, 0 deletions)"
decisions:
  - "Take the bump: schema_version moves 2 → 3. Free because BD-06-A1 records there is no installed base."
  - "Delete the old-named signed .shortcut files after the 11-06 rename rather than retain them."
  - "Build no migration, no dual-key Config alias, and no read-time profile normalisation — BD-06-A1 forbids all three by name."
  - "Record three coupled literals in fix_state_rebind(), not the two the plan and RESEARCH named."
metrics:
  duration: ~25 min
  completed: 2026-08-17
  tasks: 2
  files: 1
status: complete
---

# Phase 11 Plan 04: Schema-version and old-artifact disposition Summary

Recorded `BD-06-A3`, fixing the `schema_version` 2→3 bump and the deletion of the old-named signed artifacts, as an append-only decision that plans 11-05 and 11-06 implement without re-litigating.

## What Was Done

This plan was authored as a blocking `checkpoint:decision` rated `one-way`. It arrived **already discharged** by `BD-06-A1` Amendment 3 (user decision, 2026-08-17), and the `autonomous` flag had been flipped `false` → `true` in the plan's own amendment header. The developer was not re-asked, and the checkpoint was not reinstated.

### Task 1 — read the discharged disposition (no diff)

A read task by construction; it produces no artifact and therefore has no commit of its own. Read `BD-06-A1` Amendment 3, which records that PROSOCHĒ is a new, as-yet-undeployed product, that the only existing installs are the owner's own testing, and that old `state.json` files are explicitly not a consideration. That statement removes the entire basis of the `one-way` rating — the rating rested on destroying a real accumulated behavioural record, and there is no such record.

The answer carried into Task 2: **a bump is free**, and no migration, dual-key alias, or read-time normalisation is to be built.

### Task 2 — record the decision (commit `c4e7ec1`)

Appended `BD-06-A3` to `docs/CAPABILITY-DECISIONS.md`. The record contains, as the plan's action required:

| Required element | Where it lands in the record |
|---|---|
| The chosen option, verbatim, and the date | Decision 1 — `bump`, quoted from the plan's option table, dated 2026-08-17 |
| The concrete cost accepted | "The cost that was accepted" — heat, gravity, pressure, `recent_sessions`, `recent_contracts`, the session record, `exit_stats[*].samples`, all unrecoverable, with no field-preserving migration available |
| The exact implementation surface | A three-row table naming each literal in `fix_state_rebind()` and why they are one edit |
| The old-signed-artifact disposition | Decision 2 — deleted, with the `manifest_check.py` blindness noted |
| That `DIST-03` is open and nothing is device-evidenced | Closing "No behavioural claim" section |

## Key Decisions

**Bump chosen over `hold` and `hold-and-document`.** Beyond BD-06-A1 making it free, the record states a second, independent reason it is well-aimed: BD-06-A1 Amendment 1 moves the live Config key paths `thresholds.Limbo` → `thresholds.Purgatory`, and this project's verified runtime semantics make a dotted read with a missing segment a **hard error**. BD-06-A1 *accepted* that a device holding `profile: "Limbo"` would hard-error. A bump does better than accept it — the forced rebuild reseeds `profile` from the new template. This is stated in the record explicitly as a file-level reading of the generator's control flow, **not** as a device-verified claim.

**Old-named signed artifacts deleted.** Three measured reasons: `docs/manifest_check.py` asserts only the rows `MANIFEST.md` gives it (`:47`), so an orphan is invisible to the checks; two plausible "current" imports side by side is the exact confusion the signed-name discipline exists to prevent; and both files are git-tracked, so the bytes recover via `git show`.

**The original reasoning is preserved, not discarded.** The record states what a bump would have cost had an installed base existed, and states that the gate **reinstates itself** — this returns to `one-way` and the blocking checkpoint must be restored if a real installed base ever appears. `T-11-19` carries the same conditional marking. A record that said only "it was free" would have lost the reasoning that made it free.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 — missing critical information] The implementation surface is three literals, not two**

- **Found during:** Task 2, while reading `fix_state_rebind()` to name the exact sites
- **Issue:** Both the plan (`key_links`, and the `<checkpoint_discharged>` briefing) and `11-RESEARCH.md` Pitfall 7 describe the bump as moving **two** coupled literals — the template replacement value and the runtime gate literal. Measured, there are **three**. `tools/build_state_engine.py:3291` also hardcodes the recognition tuple `("1", "2")` that the transformer uses to *locate* the version-check conditional. Once `:3296` writes `"3"`, a **subsequent** build no longer recognises it, `version_check` stays `None`, and the build aborts at `raise SystemExit("schema version check conditional not found")`.
- **Why this matters:** it is a delayed failure. The build that performs the bump succeeds; the *next* one fails, with an error that points at a missing conditional rather than at the bump. Recording only two literals would have handed 11-05 a landmine.
- **Fix:** the record's implementation-surface table names all three sites with their measured line numbers and distinct roles (template seed / recognition tuple / runtime gate literal), and explains the idempotency coupling explicitly.
- **Commit:** `c4e7ec1`

**2. [Rule 1 — factual correction] The dated archives contain no signed artifacts**

- **Found during:** Task 2, while substantiating the deletion argument
- **Issue:** The obvious argument for deleting the old signed files — "history is preserved in the dated archives under `artifacts/shortcuts/2026-08-*/`" — is **false**. Verified: every file under `2026-08-17/` is an unsigned `.xml`, and a repo-wide `find` locates signed `.shortcut` artifacts only at the two canonical top-level paths. The dated archives preserve the XML **build input**, not a signed artifact.
- **Fix:** the record states the correction explicitly under "One precision, because the obvious argument for deletion is wrong," and grounds recoverability in **git** (both files confirmed tracked via `git ls-files`) rather than in the archive directory. It also declines to claim that re-signing a preserved XML reproduces byte-identical output.
- **Commit:** `c4e7ec1`

**3. [Documentation accuracy] `11-RESEARCH.md`'s line citation for `fix_state_rebind()` is stale**

- **Found during:** Task 2
- **Issue:** Pitfall 7 and the Runtime State Inventory both cite `:3022-3084` for `fix_state_rebind()`. Measured 2026-08-17, the function spans `:3255-3315`.
- **Fix:** noted inside the record, with an instruction to anchor on the symbol rather than the span. `11-RESEARCH.md` itself was **not** edited — it is a phase research artifact, and editing it is outside this plan's single declared file.
- **Commit:** `c4e7ec1`

### Nothing Implemented

Per the plan's explicit instruction, no part of either decision was implemented here: no generator edit, no template edit, no rebuild, no artifact deletion. This plan produces a record; 11-05 and 11-06 consume it.

## Verification

| Check | Result |
|---|---|
| Plan's `<automated>` verification | **Pass** — `append-only check vs f4e47f9 : ['297', '0', ...]` → `decision recorded, append-only` |
| Own diff, measured independently | `143  0  docs/CAPABILITY-DECISIONS.md` — 143 added, **0 deleted** |
| Baseline-relative vs own diff | **Consistent, no disagreement.** 297 = 154 (BD-06-A1 + BD-06-A2, prior commits) + 143 (this commit). The plan warned the baseline-relative number could report deletions belonging to other commits; here it reports zero deletions and the two measurements reconcile exactly, so no discrepancy needed flagging. |
| `grep -c 'DIST-03'` | 2 → **3** (+1, satisfies "increases by at least 1") |
| Files outside `docs/CAPABILITY-DECISIONS.md` | **None.** `git status --short` listed only ` M docs/CAPABILITY-DECISIONS.md`; no `src/`, `tools/` or `artifacts/` path |
| Post-commit deletion check | `git diff --diff-filter=D HEAD~1 HEAD` → empty |
| Twelve structural checks, **before** the edit | 12/12 green |
| Twelve structural checks, **after** the edit | 12/12 green — no regression introduced |

Checks run: `state_engine_self_check`, `phase5_self_check`, `phase6_self_check`, `phase7_self_check`, `phase9_self_check`, `sentient_audit_check`, `sentient_core_check`, `environmental_restore_check`, `router_ui_census`, `sequence_dispatch_check`, `manifest_check`, `note_identity_check`.

## What This Does NOT Establish

**DIST-03 is open. No iPhone is connected and no device has run either build.** Nothing recorded by this plan is device-evidenced. In particular:

- That a `schema_version` bump causes an installed device to rebuild its `state.json` is a reading of the generator and the validity gate — **structural, not behavioural**.
- That the forced rebuild reseeds `profile` and thereby avoids the `thresholds.Purgatory` hard error is the same kind of claim, and the record labels it as such.
- Structural proof is not behavioural proof. Both statements above stand on what the files say.

## Known Stubs

None. This plan wrote one Markdown record and implemented nothing.

## Threat Flags

None. This plan modified one documentation file; it introduces no network endpoint, auth path, file-access pattern, or schema change at a trust boundary. `T-11-SC` (package-manager installs) was not triggered — no install command was run.

`T-11-20` (repudiation via a silent default) is **mitigated** as the plan required: the record names the chosen option, its cost, and its implementation surface, and the append-only property was asserted by measurement.
`T-11-21` (a status display showing the stale fork label) is **addressed by the chosen option** — the version moves, so the label follows on rebuild.
`T-11-19` is marked `not applicable` under BD-06-A1, with its reinstatement trigger recorded rather than deleted.

## Self-Check: PASSED

- `docs/CAPABILITY-DECISIONS.md` contains exactly one `BD-06-A3` heading — **FOUND**
- Commit `c4e7ec1` present in `git log --oneline --all` — **FOUND**
- Twelve structural checks green after the change — **VERIFIED**
