---
phase: 16-dimming-and-silence-as-distinct-device-proven-circles
fixed_at: 2026-08-18
review_path: .planning/phases/16-dimming-and-silence-as-distinct-device-proven-circles/16-REVIEW.md
iteration: 1
findings_in_scope: 6
fixed: 6
skipped: 0
status: all_fixed
---

# Phase 16: Code Review Fix Report

**Source review:** `16-REVIEW.md` (1 Critical, 5 Warnings in scope; 5 Info out of scope)
**Result:** 6 of 6 fixed, 0 skipped, 0 `no_change_needed`.

Every finding was reproduced by execution before it was touched, and every fix carries a
demonstration in **both** directions — that the guard now fires on the defect it targets, and
that it still passes on the legitimate shape. Three of the six fixes ship that demonstration as
a **permanent, on-every-run control** rather than an ephemeral one, because ephemeral proof at
fix time is what let two of these defects ship in the first place.

**No fork artifact changed.** All six fixes are to generators and checkers; both forks rebuild
byte-identical (`b3f8b9c…` Sentient), so no re-sign was needed and `manifest_check.py` stayed
green throughout. D-01 and D-02 were not touched.

## Summary

| ID | Severity | Status | Permanent control added |
|---|---|---|---|
| CR-01 | Critical | **fixed** | yes — `_nest_persisting_save()` |
| WR-01 | Warning | **fixed** | yes — guard armed on the fork + `key` made required |
| WR-02 | Warning | **fixed** | no (behaviour change, proven by measurement table) |
| WR-03 | Warning | **fixed** | yes — `family_b_control()`, 11 rows, every run |
| WR-04 | Warning | **fixed** | no (prose re-derived; see the honest note below) |
| WR-05 | Warning | **fixed** | yes — `_misdirect_capture_dictionary()` |

**Files changed:** `tools/build_state_engine.py`, `tools/build_sentient.py`,
`docs/phase9_self_check.py`, `docs/retired_clause_check.py`. +379 / −41.

---

## Fixed Issues

### CR-01 — `verify_capture_persistence()`: unscoped clear + false docstring contract

**Commit:** `766448d` · **Files:** `tools/build_state_engine.py`, `docs/phase9_self_check.py`

**(a) Scope defect — fixed.** `pending.clear()` was unconditional and global while captures are
recorded arm-scoped, so a save nested inside a conditional arm *deeper* than the apply
discharged the pending capture even though that branch need not run. The clear now mirrors the
drop: a save may only vouch for a capture whose arms enclose it (`enclosing <= scope`). Given
the drop has already removed every capture whose arms the walk has left, that reduces to
equality — stated as the subset test because that is the property being asserted.

**(b) Contract defect — fixed by correcting the docstring, not by deleting the sentence.** The
prompt asked me to decide which was actually true. **The code was right and the docstring was
wrong:** a save of `State` writes the *whole* dictionary, so it genuinely persists every
snapshot leaf at once and a volume save genuinely does vouch for a pending brightness capture
in the same dictionary. The retired claim ("Bookkeeping is per `<group>`, so a volume save
cannot clear a pending brightness capture") was therefore the wrong half to keep. The docstring
now records that per-`<group>` keying is real but belongs to the **apply** side — it is what
stops a brightness capture arraigning a Set Volume — while the **clear** is scoped by arm depth
(and, after WR-05, by dictionary).

**Evidence — the reviewer's own fixture, both directions:**

| fixture | before | after |
|---|---|---|
| capture → **inner `if_block`** containing the save → apply | SILENT | **RAISED** |
| capture → save → apply (flat, the legitimate shape) | silent | silent |
| capture → apply, no save at all | RAISED | RAISED |

**Permanent control added,** as the review required. `capture_persistence_negative_control()`
gains `_nest_persisting_save()`, which sinks the **real** generator's emitted save pair one arm
deeper — content-located, not index-located, so it cannot drift. Proven load-bearing: with
`pending.clear()` restored the new assertion fails on `dimming()`; with the fix it passes.

### WR-01 — `verify_group_identifier_uniqueness()` not armed on Sentient

**Commit:** `234d73d` · **File:** `tools/build_sentient.py`

Two changes, closing the hole at author time and at build time:

- **`if_block(..., key=...)` is now a required keyword-only argument.** It defaulted to `"if"`,
  and `build_sentient.uid()` is a **uuid5 name hash**, not Dumb's counter — so two call sites
  that both omitted `key` collided *deterministically*, not unluckily. Verified: two
  `if_block(..., key="if")` calls returned the identical
  `32811598-4E78-5D5F-9908-879AF3021E1E`. Omitting it now raises
  `TypeError: missing 1 required keyword-only argument: 'key'`.
- **The guard is imported and invoked in `main()`**, with the per-fork reasoning recorded beside
  it in the same style 16-01 and 16-04 used for the two guards they did arm.

**Evidence:** changing one call site's key to duplicate another's now fails the Sentient build
with `876A8EC9-…: 2 start(s) at [1075, 1077] and 2 end(s) at [1133, 1134]`.

**One review number corrected by re-measurement:** the review says "all 11 current call sites".
Re-measured 2026-08-18 — there are **10**, all with distinct explicit keys. The fork is clean
today; this is armed against the next insertion, not a live defect.

### WR-02 — `verify_no_removed_snapshot_leaf_reads()`'s only unique behaviour was a false positive

**Commit:** `384f5fe` · **File:** `tools/build_state_engine.py`

`_is_removed_snapshot_leaf()`'s `len(parts) == 1` branch scoped by key shape only, so a bare
`changed_at` read out of *any* dictionary was arraigned — the exact case its own docstring
promised to exclude. The bare-leaf branch now requires `source in STATE_READ_SOURCE_VARIABLES`,
resolved through the same measured accessor path `verify_state_seed()` uses. The **dotted**
branch stays unscoped on purpose: `settings_snapshot.<group>.<leaf>` names this project's shape
wherever it is read from.

**Evidence — the review's table, re-measured against the shipped Dumb artifact with injected
reads, plus one row the review did not have:**

| injected read | `verify_state_seed` | this guard |
|---|---|---|
| `read_value settings_snapshot.brightness.changed_at` | FIRED | FIRED |
| `get_value  settings_snapshot.brightness.changed_at` | FIRED | FIRED |
| `read_value` flat `changed_at` (State) | FIRED | FIRED |
| `get_value` flat `changed_at` (Reloaded State) | FIRED | FIRED |
| `get_value` flat `changed_at` from a **foreign** dict | silent | **silent** ← was the FP |
| `read_value` flat `changed_at` from a **foreign** dict | silent | **silent** ← was the FP |
| `get_value settings_snapshot.volume.changed_by_session_id` from a **foreign** dict | silent | **FIRED** ← **new** |

**The last row is why the review's "or drop the guard" option is declined, with evidence.** The
guard now has a genuine *unique true positive* where before it had only a unique *false* one —
so it is the backstop D-02's note describes rather than decoration. Keeping it is the right
call.

**Out-of-scope overlap, declared:** this commit also corrects the "TWO SURFACES" comment
(**IN-02**). That was *strictly necessary*, not opportunistic: the commit changes
what the two surfaces mean. Surface (1) is now passed no source and covers the dotted form only,
and it is a provable strict **subset** of surface (2) by construction — every key it can report
came from a `getvalueforkey` carrying that literal key. Leaving the old comment would have left
the file claiming two independent nets immediately after making one of them narrower. The
comment now also records that composite keys bypass both and are backstopped by
`verify_state_seed()`'s unresolvable-composite branch. No other Info finding was touched.

### WR-03 — `retired_clause_check.py`'s `"10-15"` fires on any ISO date in October

**Commit:** `3f67b09` · **File:** `docs/retired_clause_check.py`

Reproduced first: appending `A routine dated note: measured 2026-10-15 during the sweep.` to
`docs/BUILD-NOTES.md` red-lined the whole repo gate with a message about the brightness floor.
`lines 10-15`, `10-15 minutes` and the threat id `T-10-15` did it too.

**The family is not deleted** — per the instruction, it is anchored to what the clause actually
*meant*, a brightness percentage band:

1. `FAMILY_B_PATTERN` requires the band as a **standalone numeric token**. The lookbehind
   rejects a preceding digit/dot/dash (kills `2026-10-15`, `T-10-15`, `110-155`); the lookahead
   rejects a trailing digit. Spaces around the dash are tolerated because prose wraps.
2. A match counts only if the **same line** carries the percent sign the clause carried, or a
   `brightness`/`dim` word. Line-scoped, and deliberately *tighter* than `FAMILY_C`'s ±6 window:
   `docs/BUILD-NOTES.md` is thick with ambient brightness prose, so a windowed anchor would have
   re-admitted every October date landing near it.

**Requiring the percent sign alone — one reading of the review's own suggested fix — was tried
and rejected on evidence.** Plan 16-05's negative-control probe line, *"the prototype dim value
sits in the 10-15 band."*, carries no percent sign and would have been silently dropped.

**Permanent control added.** `family_b_control()` runs on every invocation with **11 rows**: 5
must-fire (the clause as it actually appears in this repository, quoted from the canonical
strategy's §21 line and from 16-05) and 6 must-not-fire (the reproduced false positives,
including the sharp case of an October date on a line that *also* says "brightness"). The gate's
own success line now reports the row count.

**End-to-end evidence:** the three false-positive lines appended to a live walked file now
**pass**; `Prefer ~10–15% as a prototype dim value.` still **fails** the gate, reported as
`[10-15 band (brightness/dim-anchored)]`.

### WR-04 — stale action totals stated as MEASURED inside a live checker

**Commit:** `a621040` · **File:** `docs/phase9_self_check.py`

Per the standing rule, the numbers were **not copied forward from the review**. They were
re-derived by walking the four phase commits and counting `WFWorkflowActions` in each artifact,
and the derivation is now written into the file beside them:

| commit | | Dumb | Sentient |
|---|---|---|---|
| `0465593^` | pre-16-01 baseline | 4346 | 4414 |
| `0465593` | 16-01 persist fix | 4390 (+44) | 4458 (+44) |
| `8e2a676` | 16-03 floor / comment | 4390 (+0) | 4458 (+0) |
| `3b0d368` | 16-04 D-02 removal | **4302** (−88) | **4370** (−88) |

The −88 was **decomposed per identifier** rather than accepted as a lump: −44 `setvalueforkey`
(2 removed leaves × 22 renderings) and −44 `setvariable` (the now-unreferenced `Now Epoch` /
`Session ID` bindings, one pair per rendering). Independently confirmed against the shipped
artifacts: 4302 and 4370. The +44 was likewise re-confirmed by counting persist pairs directly:
22 per fork.

**The block now also says why it went stale** — no assertion in the file pins these totals — and
tells the reader to treat them as a dated measurement rather than a live invariant. This is the
one finding where I deliberately did **not** add a control: pinning a total that is expected to
move on every future phase would manufacture a checker that must be edited to stay green, which
is the failure mode the project's own conventions forbid. The counts the file *does* assert
(15/15, 15/4) were correct throughout and are untouched.

### WR-05 — captures into any dictionary other than `State` were invisible

**Commit:** `1680edc` · **Files:** `tools/build_state_engine.py`, `docs/phase9_self_check.py`

Bookkeeping is now keyed by `(<group>, <dictionary>)`: the capture is tracked into **any**
dictionary, and only a save sourcing that **same** dictionary discharges it. CR-01's arm scoping
is retained on top, and the two conditions are documented separately because each closes a
different hole.

**Evidence — the full matrix, measured before and after:**

| capture into | save sources | before | after |
|---|---|---|---|
| `State` | (none) | RAISE | RAISE |
| `Reloaded State` | (none) | **silent** | **RAISE** ← the hole |
| `Reloaded State` | `Reloaded State` | silent | pass |
| `Reloaded State` | `State` | **silent** | **RAISE** ← the hole |
| `State` | `Reloaded State` | RAISE | RAISE |
| `State` | `State` | pass | pass |
| `State` | `State`, nested deeper | RAISE | RAISE (CR-01 holds) |
| `Reloaded State` | `Reloaded State`, nested deeper | silent | RAISE |

**Permanent control added — and the review's suggested fixture was rejected on measurement.**
Re-pointing the *save* at `Reloaded State` was built first, and it **passed against every prior
version of the guard**: a `State` capture stayed pending when no `State` save followed, so that
direction was always covered. An assertion nobody has seen fail is not a control, so it was
discarded. `_misdirect_capture_dictionary()` moves the other side instead — it re-points the
real generator's *capture* at `Reloaded State` while leaving its own `State` save exactly where
it is, which is the actual hole and exercises **both** halves of the fix in one fixture. Proven
load-bearing: against the pre-WR-05 guard it fails on `dimming()`; with the fix it passes.

---

## Skipped Issues

None. All six in-scope findings were fixed.

Two *sub-recommendations* inside fixed findings were declined on evidence, and both are recorded
above rather than silently dropped:

- **WR-02's "or drop the guard" option** — declined. After scoping, the guard has a unique true
  positive (a `settings_snapshot`-rooted removed-leaf read out of a foreign dictionary) that
  `verify_state_seed()` does not catch.
- **WR-03's "require the percent sign" option, taken alone** — declined. It would have silently
  stopped the gate catching plan 16-05's own probe form of the clause, which carries no percent
  sign. The percent sign is used as *one of two* satisfiers instead.

## Out of scope, untouched

IN-01 (`brightness_floor` itself unbounded), IN-03 (`.planning/phases/` exclusion breadth),
IN-04 (`gate_control_room_shownote()`'s re-stamp walk bound), IN-05 (CAP-08 asserted on Dumb
only). IN-02's comment was corrected only because WR-02 changed what the two surfaces mean — see
WR-02 above.

**LOCKED decisions undisturbed.** D-01 (`safety.brightness_floor` and `safety.dim_target` both
`0`) and D-02 (`changed_at` / `changed_by_session_id` removed) were not touched by any commit;
no Config literal, seed shape or `docs/environmental_restore_check.py` assertion was edited.
Re-measured after the last fix: `brightness_floor=0`, `dim_target=0` in both built forks and in
`src/CONFIG-BLOCK.md`, and **0** removed-leaf writes remaining in either fork.

## Definition of done — re-run after the final commit

```
git merge-base --is-ancestor 7ca8ebb HEAD          provenance OK
python3 tools/build_state_engine.py                rc=0
python3 tools/build_sentient.py                    rc=0, b3f8b9cb…e548443 (unchanged)
all 13 docs/*.py checkers                          rc=0  (incl. manifest_check.py)
gate A  Dumb      --target-macos 26 --platform all Validation passed.  exit 0
gate A  Sentient  --target-macos 26 --platform all Validation passed.  exit 0
gate B  Dumb      --target-macos 27 --platform all exit 1, exactly 1 waived WFCreateNoteInput line
gate B  Sentient  --target-macos 27 --platform all exit 1, exactly 1 waived WFCreateNoteInput line
git status --short src/                            (empty — no artifact drift, no re-sign needed)
```

Gate B was run **separately** and is never `&&`-chained; both forks report exactly the one
permitted waived line and nothing else.

**MANIFEST:** untouched and green. Because no fork artifact changed, the D-MANIFEST closure from
plan 16-06 still holds and the signed artifacts under their existing display names
(`PROSOCHĒ — Nine Circles — Core.shortcut`, `PROSOCHĒ — Nine Circles — Aware.shortcut`) remain
the ones the manifest digests describe. No row was edited.

## Procedural note

This run executed in the existing GSD worktree `gsd-autonomous-16-084932` rather than creating a
nested one. That branch is checked out only here, no concurrent actor shares it, and both
`16-REVIEW.md` and `16-VERIFICATION.md` are **untracked** in it — a nested worktree cut from the
branch tip would not have contained the review being acted on, nor been able to deliver this
report to the phase directory. The isolation the protocol exists to provide was already in
place.

## What this does not prove

Nothing here is device evidence. Every fix is to a **build-time guard** or a **static checker**;
all six were verified at rung 1 of the CLAUDE.md §9 evidence ladder. The capture-and-restore
loop these guards protect remains **device-unproven** and DIST-03 remains **BLOCKED** for its
recorded reason ("paired device present, `tunnelState: disconnected`; no live session to
drive"). CR-01 in particular closes a hole through which the phase's own P0 could have
*re-entered the build unnoticed* — it does not add any evidence that the loop works on a phone.

---

_Fixed: 2026-08-18_
_Fixer: Claude (gsd-code-fixer)_
_Iteration: 1_
