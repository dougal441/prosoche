---
phase: 16-dimming-and-silence-as-distinct-device-proven-circles
reviewed: 2026-08-18T00:00:00Z
depth: standard
files_reviewed: 6
files_reviewed_list:
  - tools/build_state_engine.py
  - tools/build_sentient.py
  - docs/environmental_restore_check.py
  - docs/phase5_self_check.py
  - docs/phase9_self_check.py
  - docs/retired_clause_check.py
findings:
  critical: 1
  warning: 5
  info: 5
  total: 11
status: issues_found
---

# Phase 16: Code Review Report

**Reviewed:** 2026-08-18
**Depth:** standard (every finding below was reproduced by executing the code, not inferred)
**Files Reviewed:** 6
**Status:** issues_found

## Summary

The phase's central code change — `save_state()` inside the applying arm of `dimming()`/`silence()`
— is correct, and the mechanisms around it hold up under direct attack. Verified by execution, not
by reading:

- **`stable_uid()` is genuinely collision-free.** `SHOWNOTE_GATE_GROUP` does not appear in the first
  20 000 values of `uid()`'s counter sequence; the two namespaces are disjoint by construction.
- **The generators are idempotent and the committed artifact is not drifted.** Three consecutive
  `build_state_engine.main()` runs on a sandbox copy produced one byte-identical digest, and that
  digest equals the committed `src/PROSOCHE-Dumb.xml`.
- **`seed_settings_snapshot()` converges from both prior shapes.** A tree regressed to the build-j
  (three empty leaves) shape and one regressed to the pre-D-02 (three sentinel leaves) shape both
  converge in one pass to `{original_value}`, with every `attachmentsByRange` offset still landing
  on a `￼` and `verify_state_seed()` silent afterwards.
- **`docs/environmental_restore_check.py:286-287`'s `dim_target >= floor` assertion is intact and
  byte-identical**, as D-01 required. No other assertion in that file was weakened.
- **`docs/phase5_self_check.py`'s replacement CAP-08 assertion is load-bearing.** Patching
  `set_brightness()` in the generator to omit `WFBrightness` makes it raise. (A first attempt that
  mutated the built XML directly did *not* fail — because `phase5_self_check.main()` rebuilds the
  artifact via `subprocess` before inspecting it. Anyone re-testing that guard must patch the
  generator, not the artifact.)
- **`verify_group_identifier_uniqueness()` fires on the 2-start/2-end shape** that caused the
  original gate-A failure, and on an unclosed block.

What follows is what did not hold up. The one Critical and two of the Warnings are all the same
species: a *guard whose docstring claims a protection its code does not implement*. That is the
defect class this phase exists to fight, and three of its own new guards carry an instance of it.

## Critical Issues

### CR-01: `verify_capture_persistence()` clears the pending capture on a save that may never execute — and its docstring claims a per-group protection the code does not implement

**File:** `tools/build_state_engine.py:3836-3838` (clear), `:3798-3800` (the contradicting docstring)

**Issue — two defects in three lines.**

**(a) The clear is not arm-scoped, so the guard is bypassable by a nested save.** Captures are
correctly dropped when the walk leaves the arm they were written into (`:3827-3828`). The *clear* is
not: any `documentpicker.save` sourcing `State`, at any nesting depth, wipes the whole `pending`
map. So a save emitted inside a conditional arm *deeper* than the apply silently satisfies the
guard, even though at runtime that arm may not run and nothing reaches disk. Reproduced:

```
if_block("Captured Brightness", 2, number=0)
  set_value("settings_snapshot.brightness.original_value", ...)   # capture
  if_block("Something Else", 2, number=0)
      save_state()                                                # may not run
  end_if
  set_brightness(variable("Dim Target"))                          # applies anyway
end_if
```
→ `verify_capture_persistence()` returns **silently**. The identical fixture without the inner
`if_block` correctly raises. This is precisely the reordering the docstring says the guard exists to
catch ("the correct response is to move the save earlier, never to relax the guard"), and it is the
P0 restated: device changed, `state.json` still holds the sentinel, user stranded dim or silent.

**(b) The docstring asserts a per-group save protection that does not exist.** `:3798-3800` reads
"Bookkeeping is per `<group>`, so a volume save cannot clear a pending brightness capture — the two
primitives render interleaved inside `primitive_dispatch()` and a shared flag would let one vouch
for the other." The *apply* check is per-group; the *clear* (`pending.clear()`) is global, so a
volume save clears a pending brightness capture exactly as described. Today that is harmless (a
`State` save persists both leaves), but a maintainer reading the docstring will believe a
cross-group barrier is in place, and (a) shows the clear is already the weak edge.

**Fix:** scope the clear the same way the drop is scoped, and correct the docstring to say what the
code does.

```python
elif identifier == "is.workflow.actions.documentpicker.save":
    if _save_source_dictionary(actions, index) == "State":
        # Only a save at or above the capture's own arm depth may vouch for it: a save
        # nested deeper sits on a branch that need not run, so it persists nothing on the
        # path that reaches the apply.
        for group in [g for g, scope in pending.items() if enclosing <= scope]:
            del pending[group]
```
and replace the "Bookkeeping is per `<group>`" sentence with: *a save of `State` persists every
snapshot leaf at once, so it clears every pending capture whose arm encloses it; the per-group
keying exists for the apply side, which must not be vouched for by the other primitive's capture.*

Add the nested-save fixture to `capture_persistence_negative_control()` — the current control only
exercises full removal of the pair, which is why this hole survived.

## Warnings

### WR-01: `verify_group_identifier_uniqueness()` is not armed on the Sentient fork, which has the more collision-prone identifier scheme

**File:** `tools/build_sentient.py:13-35` (import list), `:392-406` (verify chain), `:94` (`if_block`)

**Issue:** 16-01 added `verify_capture_persistence` and 16-04 added
`verify_no_removed_snapshot_leaf_reads` to `build_sentient.py`'s import list and verify chain, each
with a written per-fork justification. `verify_group_identifier_uniqueness` — the guard 16-01
created *for the GroupingIdentifier defect class* — is in neither. The omission is not argued
anywhere in the diff, so it reads as an oversight rather than a decision.

It matters more here than on Dumb. Sentient's `if_block` (`:94`) derives its group from
`uid(key)` with **`key="if"` as the default**: two call sites that both omit `key` emit two
structurally unrelated blocks holding one identifier — the project's #1 documented real-world
mistake — with nothing in the build to notice. All 11 current call sites pass distinct explicit
keys, so the fork is clean today; the next one added without a key is not.

**Fix:** add `verify_group_identifier_uniqueness` to the import block and call it in `main()`
alongside the other structural verifies. Consider also making `key` a required keyword argument on
`build_sentient.if_block` so a silent collision becomes a `TypeError`.

### WR-02: `verify_no_removed_snapshot_leaf_reads()` catches nothing `verify_state_seed()` did not already catch, and its only unique behaviour is a false positive

**File:** `tools/build_state_engine.py:3867-3915`, `:3853-3865` (`_is_removed_snapshot_leaf`)

**Issue:** the guard is documented as "the real deliverable of D-02". Measured against the shipped
Dumb artifact with an injected read, the pre-existing `verify_state_seed()` fires on every case the
new guard fires on:

| injected read | `verify_state_seed` | `verify_no_removed_snapshot_leaf_reads` |
|---|---|---|
| `read_value("settings_snapshot.brightness.changed_at", State)` | FIRED | FIRED |
| `get_value("settings_snapshot.brightness.changed_at", State)` | FIRED | FIRED |
| `read_value("changed_at", State)` (flat) | FIRED | FIRED |
| `get_value("changed_at", **"Previous Session"**)` | silent | **FIRED** |

The last row is the guard's only distinct behaviour, and it is a **false positive** — the exact case
`_is_removed_snapshot_leaf`'s own docstring promises to exclude: *"A foreign dictionary that
legitimately owns its own `changed_at` must not be flagged — a guard that cries wolf gets exempted,
and an exempted guard is not a guard."* The `len(parts) == 1` branch at `:3864` scopes by key shape
only, never by source dictionary, so a bare `changed_at` read from any dictionary is arraigned.

This does not make the removal unsafe — it is well covered — but the guard is not the backstop the
docstring describes, and the one thing it adds is the failure mode it was written to avoid.

**Fix:** either scope the bare-leaf branch by source dictionary (reuse `STATE_READ_SOURCE_VARIABLES`,
which `verify_state_seed` already resolves), or drop the guard and record in D-02's note that
`verify_state_seed()` is what keeps the no-reader precondition true. Do not leave it asserting a
protection it does not provide.

```python
def _is_removed_snapshot_leaf(key: str, source: str | None = None) -> bool:
    parts = key.split(".")
    if parts[-1] not in D02_REMOVED_SNAPSHOT_LEAVES:
        return False
    if len(parts) == 1:
        return source in STATE_READ_SOURCE_VARIABLES   # not any foreign dictionary
    return parts[0] == SNAPSHOT_ROOT
```

### WR-03: `retired_clause_check.py`'s `"10-15"` pattern fires on any ISO date in October, failing the whole repo gate

**File:** `docs/retired_clause_check.py:93` (`FAMILY_B`), `:235` (bare substring match)

**Issue:** `FAMILY_B` is matched as an unanchored, unscoped substring against every line of every
walked file, unlike `FAMILY_C` which is deliberately anchor-scoped for exactly this reason.
Reproduced — appending one ordinary sentence to `docs/BUILD-NOTES.md`:

```
A routine dated note: measured 2026-10-15 during the sweep.
```
→ `retired clause check: FAILED -- 1 live occurrence(s) of the retired brightness-floor clause
survive` ... `docs/BUILD-NOTES.md:3176  [10-15]`, exit 1.

This project stamps ISO dates into `docs/BUILD-NOTES.md`, `.planning/STATE.md` and every summary. Any
date in October 2026, any line range (`lines 10-15`), or any unrelated `10-15 minutes` red-lines the
gate with a message about the brightness floor. The gate's own source records the consequence
(`:98`, on why `FAMILY_C` is scoped): a check that cries wolf gets exempted, and the exemption is
what actually removes the protection.

**Fix:** scope `FAMILY_B` the way `FAMILY_C` already is — require a brightness/dim anchor within the
same window — and/or require the percent sign that the retired clause actually carried:

```python
FAMILY_B = ("10-15%", "10" + chr(8211) + "15%")
FAMILY_B_ANCHORS = ("brightness", "dim_target", "dim target")   # + a windowed check
```

### WR-04: `docs/phase9_self_check.py:56` states stale action totals as MEASURED, in a live checker

**File:** `docs/phase9_self_check.py:56`

**Issue:** the 16-01 docstring block reads *"+44 actions per fork (Dumb 4346 -> 4390, Sentient 4414
-> 4458) ... That non-movement was MEASURED against the rebuilt forks after the fix, not assumed."*
The shipped forks now hold **4302** and **4370** actions — 16-04's D-02 removal took 88 out of each,
after that paragraph was written. The site counts the file actually *asserts* (15/15, 15/4) are
still correct and still pass; it is the prose totals that are stale.

That is the precise failure mode `retired_clause_check.py` was created in the same phase to prevent
— a record drifting from the build it describes — sitting inside a live checker and labelled
"MEASURED".

**Fix:** update to `Dumb 4346 -> 4390 (4302 after 16-04's D-02 removal), Sentient 4414 -> 4458
(4370)`, or drop the totals and keep only the counts the file asserts. Totals that no assertion pins
will go stale again.

### WR-05: `verify_capture_persistence()` tracks captures written only into `State`, so a capture into any other dictionary is invisible

**File:** `tools/build_state_engine.py:3833-3835`

**Issue:** the pending flag is only raised when `WFDictionary` names `State`. A capture written into
`Reloaded State` (a dictionary `clear_snapshot()` already accepts as a parameter) followed by an
apply is not tracked at all, and a `Reloaded State` save correctly does not clear it — so the guard
is silent on both halves. Reproduced: `set_value(..., "Reloaded State")` followed by
`set_brightness()` inside one arm → guard silent, whereas the same fixture with `State` raises.

This is the same wrong-dictionary mechanism (T-16-04) that `dimming()`'s docstring calls
load-bearing, and it is the one variant the guard cannot see.

**Fix:** raise the pending flag for a capture into *any* dictionary, and clear it only on a save
sourcing that same dictionary:

```python
target = (parameters.get("WFDictionary") or {}).get("Value", {}).get("VariableName")
if isinstance(target, str):
    pending[key.split(".")[1]] = (target, enclosing)
...
saved = _save_source_dictionary(actions, index)
for group in [g for g, (dictionary, scope) in pending.items()
              if dictionary == saved and enclosing <= scope]:
    del pending[group]
```

## Info

### IN-01: with `brightness_floor = 0`, nothing constrains the floor itself

**File:** `docs/environmental_restore_check.py:283-287`

`dim_target >= 0` is now fully subsumed by `dim_target >= floor` while `floor` is `0`, and no
assertion places any bound on `brightness_floor`. `floor = -5, dim_target = 0` passes both. The
relaxation is correct per D-01 and the pair is not vacuous (a negative or non-numeric `dim_target`
still fails), but if the intent is that the floor is a real floor, add
`require(isinstance(floor, (int, float)) and floor >= 0, ...)`.

### IN-02: the "TWO SURFACES" rationale is inverted, and a composite key bypasses both

**File:** `tools/build_state_engine.py:3890-3899`

Surface (2) — the flat `getvalueforkey` `WFDictionaryKey` scan — subsumes surface (1) entirely,
because `read_value()` also emits a `getvalueforkey` carrying the same literal key; surface (1) is
the redundant one, not the load-bearing one the comment describes. Separately, both surfaces require
`isinstance(key, str)`, so a `text_token()`-built composite key (the `exit_stats.<type>.<field>`
idiom already in the codebase) bypasses both. That case is backstopped by `verify_state_seed()`'s
unresolvable-composite branch, so it is not an open hole — but the comment should say so rather than
claim two independent surfaces.

### IN-03: `.planning/phases/` is excluded, and phase PLANS are the gate's own worst-case carrier

**File:** `docs/retired_clause_check.py:133-143`

The exclusion is documented and its tradeoff is stated honestly. Measured: every current occurrence
under `.planning/phases/` describes the retirement, and `16-UAT.md` — the live device instrument — is
D-01-correct throughout. The residual concern is structural rather than present: the gate's stated
harm model is *"a live instruction to build something the build does not do"*, and a future phase's
PLAN is exactly that kind of instruction, filed in the one tree the gate will not read. Worth a
follow-up narrowing the exclusion to `*-SUMMARY.md` / `*-CONTEXT.md` / `*-RESEARCH.md` and leaving
`*-PLAN.md` and `*-UAT.md` in scope.

### IN-04: `gate_control_room_shownote()`'s re-stamp walk can re-stamp a foreign block

**File:** `tools/build_state_engine.py:4660-4666`

The forward walk re-stamps every action holding `stale` and breaks only on the first mode-2. If a
colliding regenerated block's *start* (mode 0) sits at `index + 1`, the walk re-stamps that block
instead of stopping, leaving the wrapper's own End If on the stale value — the failure the comment
above it says a global pass would cause. `verify_group_identifier_uniqueness()` catches the result
loudly, so it fails safe on Dumb; on Sentient it would not (see WR-01). Bound the walk to the
wrapper's own three actions explicitly (`actions[index + 1: index + 3]`) rather than to a
content-dependent break.

### IN-05: the new CAP-08 assertion runs against Dumb only

**File:** `docs/phase5_self_check.py:16` (`SOURCE = ROOT / "src/PROSOCHE-Dumb.xml"`), `:147`

`phase5_self_check.py` inspects one fork. The CAP-08 hazard it now pins — an absent `WFBrightness`
silently applying 50% with no captured original — is therefore unasserted on Sentient, which is
built by a separate script that inserts its own actions. Sentient inherits these actions verbatim
today, so this is coverage shape rather than an open defect; note it beside the assertion, or run
the loop over both forks.

---

_Reviewed: 2026-08-18_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard — all eleven findings reproduced by execution_
