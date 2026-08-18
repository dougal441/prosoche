---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
reviewed: 2026-08-18T00:00:00Z
depth: standard
review_scope: "waves 7-10 (gap closure), diff base 5421772"
files_reviewed: 12
files_reviewed_list:
  - tools/build_state_engine.py
  - tools/build_sentient.py
  - docs/environmental_restore_check.py
  - docs/note_identity_check.py
  - docs/phase9_self_check.py
  - docs/sentient_audit_check.py
  - docs/sentient_core_check.py
  - docs/BUILD-NOTES.md
  - docs/CAPABILITY-DECISIONS.md
  - artifacts/shortcuts/MANIFEST.md
  - src/PROSOCHE-Dumb.xml
  - src/PROSOCHE-Sentient.xml
findings:
  critical: 0
  warning: 4
  info: 3
  total: 7
earlier_review:
  scope: "waves 1-6, reviewed 2026-08-17, retained verbatim below"
  critical: 3
  warning: 15
  total: 18
  closed_by_waves_7_10: 8
  closed_elsewhere: 1
  still_open: 9
status: findings
---

# Phase 11: Code Review Report — waves 7–10 (gap closure)

**Reviewed:** 2026-08-18
**Depth:** standard
**Diff base:** `5421772` (the commit immediately before wave 7)
**Files reviewed:** 12 (both generated forks used only as evidence, never reviewed line by line)
**Status:** findings — 0 Critical, 4 Warning, 3 Info

## How this file was written

**I APPENDED.** The waves 1–6 review of 2026-08-17 is retained **verbatim and unedited** below,
under the heading `# ARCHIVE — waves 1–6 review (2026-08-17, retained verbatim)`. Nothing in it
was rewritten, renumbered or deleted. Only the YAML frontmatter above was replaced, and this
waves 7–10 section plus the disposition table were inserted ahead of it. New findings are
numbered from `WR-16` / `IN-01` so that no identifier collides with the earlier report's
`CR-01`–`CR-03` and `WR-01`–`WR-15`.

## Summary

**Waves 7–10 close all four of the code-level gaps `11-VERIFICATION.md` raised, and they close
them properly rather than cosmetically.** I re-ran every substantive claim rather than reading
the SUMMARYs: both builders are byte-idempotent and reproduce the shipped sources exactly
(`md5` identical across two consecutive rebuilds in an isolated `git archive` copy), all 13
structural checkers exit 0 on the tracked tree, and gate A
(`--target-macos 26 --target-platform all`) prints `Validation passed.` for both forks. The
`11-08` re-gate is correct at the plist level: 22 new `Outstanding … Original` conditionals per
fork, all at condition 2 with `WFNumberValue 0`, all carrying the axis-6
`WFCoercionVariableAggrandizement` / `WFNumberContentItem` and the axis-5 bare
`WFTextTokenAttachment` variable descriptor. `11-07`'s two `text.match` consumers now read
`Matches` through a `First Item` `getitemfromlist`, and `text` is corpus-attested as that
action's input key (8 occurrences). `11-09`'s second audit block lands inside the OPEN arm
(actions 1095 and 1413, OPEN arm 94→1627) and introduces **no** new duplicate `UUID` or
`GroupingIdentifier` — both forks carry the identical, already-tracked `792D1640…` pair and
nothing else. `11-10`'s import-question derivation is right: all three questions in both forks
resolve to a `gettext` that actually defines `WFTextActionText`.

I also confirmed the guards have teeth where they were claimed to. Reverting `dimming()`'s gate
to the container form fails the build with 22 named offenders. Renaming the Panic Escape emitter
variable and flipping its gate to condition 100 — the precise drift `WR-01` showed passing
silently — now exits 1. Deleting every Emergency Restore surface raises; wrapping one in a Panic
Escape conditional raises. Reverting `build_sentient.py` to first-marker insertion makes
`sentient_core_check.py` exit 1 with a derived-count message.

**Where this set falls short is one level down, and it is the same class the phase keeps
rediscovering: a guard that reports success because it resolved nothing.** Three of the four
warnings below are that shape, and I demonstrated each with a build, not by reading.

1. All three provenance-resolved guards route through one helper, `_read_variable_keys()`, which
   walks exactly the `getvalueforkey → gettext → setvariable` chain `read_value()` emits.
   **One extra `set_var` hop breaks it.** I reintroduced `CR-01` verbatim — `dimming()`'s whole
   body back in the never-taken arm of a permanently-true container gate — behind a single
   variable copy, and `verify_environmental_reachability()` (the guard 11-08 authored for
   exactly that shape), `environmental_restore_check.py` and `phase9_self_check.py` all stayed
   green with the build exiting 0. The same hop makes the Panic Escape bypass gate a condition-100
   existence test that both 11-10 guards ignore.
2. `docs/environmental_restore_check.py`'s `REQUIRED_SYMBOLS` asserts a guard is **defined and
   callable**, never that a builder **calls** it. Deleting `verify_environmental_reachability(actions)`
   and `verify_panic_escape_isolation(actions)` from both builders' `main()` leaves all 13
   checkers green — directly contradicting the comment added in the same wave, which says
   deleting the guard would be caught here.
3. The "one contract audit per OPEN-arm rendering" invariant — the whole of gap 3 — is enforced
   **only** by a standalone checker. `build_sentient.py` exits 0 with an audit missing, and
   `docs/sentient_audit_check.py` cannot see the defect at all (it reconciles blocks against
   models *within* the Aware fork, so one block and one model satisfies it).

None of this is a live defect in the shipped artifacts. Every one of them is a build guard that
will pass on the day the defect it was written for comes back in slightly different clothes,
which is precisely what `11-VERIFICATION.md` gap 4 was about.

**Evidence discipline in the prose changes is, by contrast, good.** `BUILD-NOTES.md` §31–§35 and
`CAPABILITY-DECISIONS.md` BD-02/03-A1 keep the rung distinction consistently: the simulator probe
result is labelled rung 2 and explicitly barred from anything in §9's ceiling list, the Use Model
path is stated as never having run on Apple-Intelligence hardware, and every section closes with
a "what this does NOT establish" block. I found no promotion of a structural result to a device
claim, and no restatement of the D-01-retired brightness-floor clause
(`docs/retired_clause_check.py` is clean on the tracked tree; its 4 failures at HEAD are the
known gitignored `graphify-out/` sites). The three Info items below are staleness and
completeness, not confidence inflation.

## Disposition of the waves 1–6 findings

Re-checked against HEAD, not transcribed from the SUMMARYs.

| ID | Disposition | Evidence |
|---|---|---|
| CR-01 dimming/silence unreachable | **CLOSED** (11-08) | Both gates now read `settings_snapshot.<g>.original_value` at condition 2; 22 gates/fork verified in both plists; reverting to the container form exits 1 with 22 offenders |
| CR-02 `text.match` wrong `OutputName` | **CLOSED** (11-07) | Both consumers read `Matches`; `ACTION_OUTPUT_NAMES` lists the identifier; 0 references carry the retired guess |
| CR-03 Aware audit on one rendering only | **CLOSED** (11-09) | 2 `askllm` at 1095/1413, both inside the OPEN arm; count derived from Core; first-marker revert makes `sentient_core_check` exit 1 |
| WR-01 name-coupled panic gate guard | **CLOSED** (11-10), residual → WR-16/WR-19 | Emitter rename + condition-100 flip now exits 1 |
| WR-02 `MINIMUM_TOKEN_STRINGS = 775` | **CLOSED** (11-10) | Now `1104`, equal to the measured Core count under `check_offsets()`'s own walk (Aware 1112) |
| WR-03 vacuous brightness assertion | **CLOSED elsewhere** (Phase 16) | `docs/phase5_self_check.py` untouched in this range; asserts operand presence, cites CAP-08 |
| WR-04 `PROFILE_NAMES` unreconciled | **OPEN** | Not addressed by waves 7–10 |
| WR-05 `THRESHOLDS` duplication | **OPEN** | `docs/state_engine_self_check.py` untouched in this range |
| WR-06 Note-copy constants unasserted | **OPEN** | Not addressed |
| WR-07 `plist_text_edit` divergent copy | **OPEN** | `tools/plist_text_edit.py` untouched in this range |
| WR-08 range `length` discarded | **OPEN** | same file, untouched |
| WR-09 code points vs UTF-16 offsets | **OPEN** | same file, untouched |
| WR-10 Aware runs a guard subset | **CLOSED** (11-09) | `verify_circle_zero_silence` and `verify_parameter_keys` now imported *and* called at `build_sentient.py:581,587` |
| WR-11 hard-coded import index | **CLOSED** (11-09) | Splice and `ActionIndex` both derive from the `Import Voice` anchor; all 3 questions in both forks resolve to a `gettext` |
| WR-12 bare `StopIteration`/`IndexError` | **OPEN** | Not addressed |
| WR-13 MANIFEST dispatch count stale by nine | **CLOSED** (11-07) | MANIFEST reads 99; `sequence_dispatch_check.py` independently reports 99 |
| WR-14 display names, three unlinked copies | **OPEN** | Not addressed |
| WR-15 T-11-22 has no standing checker | **CLOSED** (11-10) | `verify_panic_escape_isolation()` armed in both builders; raises on an enclosed surface *and* on zero surfaces |

## Warnings

### WR-16: one `set_var` hop disarms all three provenance-resolved guards, including the one 11-08 wrote to make `CR-01` unrepresentable

**Files:**
`tools/build_state_engine.py:3925-3964` (`_read_variable_keys`),
`tools/build_state_engine.py:4394-4502` (`verify_environmental_reachability`, the `permanent` loop at `:4453-4466`),
`tools/build_state_engine.py:3317-3336` (`_panic_escape_variables`)

**Issue.** `_read_variable_keys()` recovers a variable's provenance by walking exactly one emitted
shape: `getvalueforkey` → `gettext` → `setvariable`. It has no transitive step, so a
`setvariable` whose `WFInput` is a plain `Type: "Variable"` descriptor — an ordinary
`set_var("Copy", variable("Original"))` — yields **no** provenance for `Copy`. Every guard that
resolves its targets through that helper therefore stops seeing the gate the moment an
intermediate variable is introduced. All three of this phase's provenance-resolved guards do.

I verified this by building, not by reading. Two controls, each on an isolated `git archive`
copy of HEAD:

*Control H — `CR-01` reintroduced behind one hop.* `dimming()` re-gated onto the
`settings_snapshot.brightness` **container** at condition 100 with the whole capture-and-apply
body back in the `otherwise` arm — the exact defect 11-08 exists to close — with the gate reading
a one-hop copy of the container variable:

```
python3 tools/build_state_engine.py        -> EXIT 0
python3 docs/environmental_restore_check.py -> "environmental restore check: passed", EXIT 0
python3 docs/phase9_self_check.py           -> EXIT 0
```

Compare the same revert **without** the hop, which is the control 11-08 actually ran:

```
an environmental read or write sits in the never-taken arm of a permanently-true
settings_snapshot container gate ... (22 total)         EXIT 1
```

*Control G — the Panic Escape bypass gate behind one hop.* `read_value(panic_escape_enabled, …,
"Panic Escape Enabled")` left intact (so `_panic_escape_variables()` still returns a non-empty
set and neither `if not guarded` raise fires), one `set_var("PE Gate", variable("Panic Escape
Enabled"))` added, and `universal_leaving()`'s gate moved to `if_block("PE Gate", 100)` — the
existence test both 11-10 guards forbid, on the gate that decides whether the user gets the
Leaving/Continue menu at all:

```
python3 tools/build_state_engine.py -> EXIT 0
python3 tools/build_sentient.py     -> EXIT 0
all 13 checkers                     -> EXIT 0
```

Measured on that artifact: `_panic_escape_variables()` = `{'Panic Escape Enabled', 'Panic Escape
Stored'}` (non-empty, so the vacuity assertion passes), resolved Panic-Escape groups = 2 (the two
write gates only), and the bypass gate at action 530 sits at condition 100, unseen.

`verify_panic_escape_seed()`'s own docstring states the property this disproves: *"The guarded
set is resolved BY PROVENANCE … and the set itself is asserted non-empty, so neither a rename nor
a disconnection can make this pass vacuously."* A disconnection can.

**Fix.** Make provenance transitive in the one helper, so all three guards inherit it:

```python
def _read_variable_keys(actions):
    ...
    # existing pass builds `keys` from the getvalueforkey -> gettext -> setvariable chain
    # NEW: propagate across variable -> variable copies until the map stops growing, so an
    # intermediate `set_var("Copy", variable("Original"))` cannot orphan a guard.
    changed = True
    while changed:
        changed = False
        for item in actions:
            if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.setvariable":
                continue
            parameters = item.get("WFWorkflowActionParameters", {})
            source = (parameters.get("WFInput") or {}).get("Value")
            if not isinstance(source, dict) or source.get("Type") != "Variable":
                continue
            inherited = keys.get(source.get("VariableName"))
            if not inherited:
                continue
            target = keys.setdefault(parameters.get("WFVariableName"), set())
            if not inherited <= target:
                target |= inherited
                changed = True
    return keys
```

Then re-run both controls above; both must exit 1.

---

### WR-17: `REQUIRED_SYMBOLS` proves a guard exists, never that a builder runs it — both guards added this wave can be silently disarmed with every checker green

**Files:**
`docs/environmental_restore_check.py:72` and `:84` (the two entries added by 11-08 and 11-10),
`docs/environmental_restore_check.py:181-186` (the assertion)

**Issue.** The loop at `:181` asserts only `hasattr(builder, name)` and `callable(...)`. The
comments added beside the two new entries claim more than that:

> *"Delete it and the primitives can silently return to doing nothing at all, with every count in
> this file still green."* (`:69-72`)
> *"Listed here for the same reason as the three above: deleting the guard is invisible at runtime
> and every count in this file would stay green."* (`:82-84`)

Both describe deleting the **guard**. What actually disarms a guard in this codebase is deleting
its **call**, and that is exactly what this file cannot see. Verified: on an isolated copy I
removed `verify_environmental_reachability(actions)` and `verify_panic_escape_isolation(actions)`
from `main()` in **both** `tools/build_state_engine.py` and `tools/build_sentient.py`, leaving the
function definitions untouched:

```
python3 tools/build_state_engine.py   -> EXIT 0
python3 tools/build_sentient.py       -> EXIT 0
docs/environmental_restore_check.py   -> EXIT 0
docs/phase9_self_check.py             -> EXIT 0
docs/sentient_core_check.py           -> EXIT 0   (+ every other checker)
```

The safety property SAFE-05 now rests on two guards whose removal from the build pipeline is
invisible to the file that exists to make their removal loud. `verify_capture_persistence` (Phase
16) carries the same weakness; this wave added two more instances rather than closing it.

**Fix.** Use the idiom this file already uses two dozen lines further down
(`inspect.getsource(builder.manual_emergency_restore)` at `:208`), applied to the builders' own
`main()`:

```python
CALLED_GUARDS = ("verify_environmental_reachability", "verify_panic_escape_isolation",
                 "verify_capture_persistence", "verify_restore_gates", "verify_state_seed")

for module, label in ((builder, BUILDER.name), (sentient, SENTIENT_BUILDER.name)):
    body = inspect.getsource(module.main)
    for name in CALLED_GUARDS:
        require(f"{name}(" in body,
                f"{label}'s main() no longer CALLS {name}() -- the function still exists, so "
                f"the symbol check above stays green while the guard is disarmed and the "
                f"primitives can silently return to a dead arm")
```

---

### WR-18: gap 3's invariant has no build guard, and the checker named as its second line of defence cannot detect the defect

**Files:**
`tools/build_sentient.py:340-359` (marker collection and insertion; no post-insertion assertion),
`docs/sentient_audit_check.py:22`, `:42-45`

**Issue.** `build_sentient.py` derives the OPEN arm structurally, collects every contract marker
inside it and inserts one `audit_block()` at each — which is the right fix. But nothing in
either builder then **asserts** that the number of `askllm` actions equals the number of OPEN-arm
renderings. The only thing that does is `docs/sentient_core_check.py`, a standalone script that
is not chained into either build.

Verified: reverting the insertion loop to the first marker only (`markers[:1]`) produces

```
python3 tools/build_sentient.py       -> "built src/PROSOCHE-Sentient.xml (e3ed3603…)", EXIT 0
python3 docs/sentient_audit_check.py  -> "sentient audit check: 1 block(s), …", EXIT 0
python3 docs/sentient_core_check.py   -> EXIT 1
```

So a defective Aware fork is **built and written to disk** with a silent success, and one of the
two files the wave nominates as coverage passes it. `docs/sentient_audit_check.py` never opens
`src/PROSOCHE-Dumb.xml` (`:22` loads the Sentient fork only) and reconciles span count against
model count *within* Aware (`:42-45`), so one block plus one model is a clean run. The
corresponding claim in `11-09-SUMMARY.md` — *"Both Aware checkers derive the audit count from the
Core fork"* and *"count derived in the builder and both checkers, so one block cannot satisfy
it"* — is not true of that file and not true of the builder. `T-11-47` is therefore closed by a
single, unchained checker.

**Fix.** Assert it where the artifact is written, using values `main()` already has in hand:

```python
    for ordinal, index in reversed(list(enumerate(markers))):
        actions[index:index] = audit_block(ordinal)
    inserted = sum(1 for item in actions
                   if item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.askllm")
    if inserted != len(markers):
        raise SystemExit(
            f"{len(markers)} OPEN-arm dispatch rendering(s) but {inserted} Use Model action(s). "
            f"CONSEQUENCE: a rendering reaches Intention with no contract audit, so an Aware "
            f"install silently behaves as Core on that path with nothing observable on device.")
```

and either give `docs/sentient_audit_check.py` the same Core-derived expectation
`sentient_core_check.py` already computes, or drop the SUMMARY's claim that it carries one.

---

### WR-19: the two Panic Escape guards assert the resolved *variable* set is non-empty, never the resolved *gate* set

**Files:**
`tools/build_state_engine.py:3400-3408` (`verify_panic_escape_seed`, the `if not guarded` raise),
`tools/build_state_engine.py:3530-3541` (`verify_panic_escape_isolation`, `if not guarded` then
the `groups` comprehension)

**Issue.** Both guards raise when `_panic_escape_variables()` returns an empty set, which is the
right instinct and closes the rename case. Neither raises when the set is non-empty but **no
conditional tests any member of it** — at which point `verify_panic_escape_seed()`'s assertion (3)
iterates over nothing and `verify_panic_escape_isolation()` intersects the surfaces against an
empty `groups` set and reports isolation without having tested a single enclosure. This is the
concrete mechanism behind WR-16's Control G, and it is worth its own one-line fix because it also
catches partial disconnections (some gates re-routed, others not) that a transitive-provenance
fix alone would not flag as suspicious.

**Fix.** In `verify_panic_escape_isolation()`, immediately after the `groups` comprehension:

```python
    if not groups:
        raise SystemExit(
            f"{len(guarded)} variable(s) resolve to {PANIC_ESCAPE_KEY!r} by provenance but no "
            "mode-0 conditional tests any of them, so no Panic Escape group could be located "
            "and this guard would report Emergency Restore isolated without testing anything -- "
            "a gate reading an intermediate copy of the flag orphans both Panic Escape guards")
```

and the equivalent in `verify_panic_escape_seed()`: fail when the number of conditionals whose
tested variable is in `guarded` is zero.

## Info

### IN-01: `dimming()`'s already-dim short-circuit is unreachable under the shipped `dim_target = 0`, and MANIFEST states an unreachability claim wider than the new guard supports

**Files:** `tools/build_state_engine.py:741-748`; `artifacts/shortcuts/MANIFEST.md:90-91`

**Issue.** Inside `capture_g` (`Captured Brightness > 0`), `already_dim_g` tests
`Captured Brightness <= Dim Target`. The Config literal ships `"dim_target": 0` (action 7, both
forks, per D-01), so the two conditions are exact complements and `already_dim_g`'s TRUE arm — a
bare `Nothing` — cannot be reached in any of the 11 renderings per fork. `verify_environmental_reachability()`
cannot see it: it derives permanence only from `settings_snapshot`-rooted existence gates, and
this one is a numeric gate over a device reading. The behaviour is correct post-D-01 (a write of
`0` never brightens anything), so this is dead code rather than a defect — but MANIFEST's
`**0 actions per fork remain unreachable.**` is a stronger statement than the guard beneath it
can carry, in a file that ships beside the artifacts. The shipped Shortcuts comment bullet
*"Do not brighten an already dim screen"* likewise now describes a branch that never fires.

**Fix.** Narrow the MANIFEST sentence to what is measured — *"0 environmental actions per fork
remain in a dead arm"* — and either drop `already_dim_g` while `dim_target` is `0`, or leave it
with a one-line comment recording that it is inert until a non-zero dim target returns.

---

### IN-02: the Circle-6 `Eject` interim is not named as interim in the generator's comment text, though `BUILD-NOTES.md` §34 presents three agreeing records

**Files:** `tools/build_state_engine.py:977-991`; `docs/BUILD-NOTES.md` §34 (the three-record table)

**Issue.** Plan 11-02's prohibition requires each interim to be named as interim *in the
generator's own comment text* **and** in `docs/BUILD-NOTES.md`, with its replacing phase. §34
discharges the BUILD-NOTES half for both interims correctly. For Circle 8 the generator half is
genuinely present (`:982-987`, `DELIBERATE INTERIM`, `PHASE 15` named). For Circle 6 it is not:
`grep -n 'Redirect\|Phase 17\|PHASE 17' tools/build_state_engine.py` returns nothing, and §34's
table fills that cell with *"the same `primitive_dispatch()` tuple, which emits no `Redirect`
branch at all"* — an absence, not a comment. A reader working from the generator alone still has
no way to learn that `("Eject", exile)` occupying Circle 6 in `Classic` and `Ambient` is
temporary.

**Fix.** One comment line beside the branch tuple, matching the Circle-8 wording:

```python
    # "Eject" (Circle 6 in all three sequences) is a DELIBERATE INTERIM in Classic and Ambient:
    # BD-06 gives that slot to Redirect there, and Redirect has no implementation, so a branch
    # cannot be emitted before a sequence can name it.  PHASE 17 emits Redirect and flips
    # exactly two cells, Classic[5] and Ambient[5]; BlackMirror[5] is already correct.
```

---

### IN-03: the newest stated Aware action total in two shipped/reference files is 4372; the shipped fork is 4438

**Files:** `docs/phase9_self_check.py:114`; `artifacts/shortcuts/MANIFEST.md:93` (and `:160`)

**Issue.** Both figures are correctly dated to plan 11-08, and both files declare their totals as
dated measurements that no assertion pins — so neither is dishonest. But 11-09 added 66 actions
per Aware fork afterwards and neither figure was refreshed, so the most recent Aware total a
reader finds anywhere in either file is 68 short of the artifact on disk (measured: Core 4304,
Aware 4438). Given that this project's own convention treats stale counts as a defect class, the
gap is worth closing rather than inheriting.

**Fix.** Append the post-11-09 figures beside the dated ones (`Aware 4438 at 11-09`), or add the
totals to `docs/environmental_restore_check.py`'s asserted table so they cannot go stale again
without turning a checker red.

## What I verified and found clean

Recorded so a future reader knows what was actually exercised rather than assumed.

| Check | Result |
|---|---|
| Both builders byte-idempotent, reproduce shipped `src/` | `md5` identical across 2 rebuilds in an isolated `git archive` copy, both forks |
| 13 structural checkers on the tracked tree | 13/13 exit 0 (`retired_clause_check` clean; its 4 HEAD failures are the known gitignored `graphify-out/` sites) |
| Gate A, both forks | `Validation passed.`, exit 0 |
| 11-08 gate shape | 22 `Outstanding … Original` conditionals per fork, all condition 2 / `WFNumberValue 0`, all with `WFCoercionVariableAggrandizement` + `WFNumberContentItem` (axis 6) in a bare `WFTextTokenAttachment` slot (axis 5) |
| 11-08 dotted-read safety (axis 7) | `SNAPSHOT_SEED` still seeds `original_value` under both groups; `clear_snapshot()` writes the leaf only; `verify_sentinel_gates()` raises on a condition-100 gate over that leaf (control run, 11 offenders) |
| 11-07 consumption chain | Both `text.match` sites → `getitemfromlist` `First Item` (axis 4 literal) on `OutputName: "Matches"`; `text` is the corpus-attested input key (8 occurrences) |
| 11-09 identifier discrimination | Every `uid()` and every `if_block(key=)` in `audit_block()` routes through `aid()`; no new duplicate action `UUID` or `GroupingIdentifier` in either fork versus the pre-wave baseline |
| 11-09 audit placement | `askllm` at 1095 and 1413, both inside the OPEN arm (94→1627), one per Panic-Escape arm; 9 MANUAL-arm markers carry none |
| 11-09 WR-11 closure | All 3 import questions in both forks target a `gettext` that defines `WFTextActionText`; `Import Voice` anchor is unique |
| 11-10 `MINIMUM_TOKEN_STRINGS` | `1104` equals the measured Core count under the checker's own walk; Aware 1112 |
| T-11-22 guard, both directions | Deleting all 4 Emergency Restore surfaces raises; wrapping one in a Panic Escape conditional raises with the enclosing group named |
| WR-01 closure | Emitter rename + condition-100 flip now exits 1 naming the renamed variable |
| CR-01 closure | Container-gate revert exits 1 with 22 offenders |
| CR-03 closure | First-marker revert makes `sentient_core_check` exit 1 with the derived-count message |
| Retired D-01 clause | No restatement in any file changed by waves 7–10 |

## Explicitly not reported

Per the review brief, and confirmed present rather than assumed:

- `docs/retired_clause_check.py`'s 4 occurrences inside `.planning/graphs/` and `graphify-out/`
  (gitignored, pre-existing, separately tracked).
- The duplicate action `UUID` `792D1640-FEB7-5FAF-AD6D-0E66CC1A1075` on both forks, and the
  absence of an action-`UUID` uniqueness guard — both recorded in `deferred-items.md` with a
  stated reason I agree with (11-09 was required to leave `src/PROSOCHE-Dumb.xml` byte-identical).
  I confirmed the duplicate set is identical before and after this wave set.
- Gate B's single waived line per fork.
- `verify_output_names()` being unable to fire in either builder because
  `normalise_output_names()` runs first over the identical token set — `11-07-SUMMARY.md` and
  `BUILD-NOTES.md` §32 both state this explicitly, and the normaliser closes the class for every
  listed identifier, so the verifier's redundancy is documented rather than hidden.

## Device evidence

Nothing in this review is a device observation. `DIST-03` is open. Every result above is rung 1
(file-level analysis of the generators, the two built plists and the checkers) except the negative
controls, which are builds of mutated generator copies — still rung 1. The `11-07` probe result
recorded in `BUILD-NOTES.md` §31 is a rung-2 simulator observation and is labelled as such there;
I did not re-run it and I make no claim about it.

---

_Reviewed: 2026-08-18_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
_Scope: waves 7–10, diff base `5421772`_

---

# ARCHIVE — waves 1–6 review (2026-08-17, retained verbatim)

> Everything below this line is the original `11-REVIEW.md` body as written on 2026-08-17,
> unedited. Its frontmatter was replaced by the block at the top of this file; its finding
> dispositions as of 2026-08-18 are in the table above. Its `CR-`/`WR-` numbering is preserved,
> and the waves 7–10 findings deliberately start at `WR-16` / `IN-01` so nothing collides.

# Phase 11: Code Review Report

**Reviewed:** 2026-08-17
**Depth:** standard
**Files Reviewed:** 16
**Status:** issues_found

## Summary

The phase's own new guards are, on the whole, real guards. I ran negative controls against
`verify_dispatch_coverage()` (orphan entry, reverted condition-99 branch, unknown condition
code) and against `verify_panic_escape_seed()` (unseeded flag, condition-100 gate) — five of
six deliberate defects were caught with a correct message. `docs/sequence_dispatch_check.py`'s
promotion to a gate is genuine. `tools/build_state_engine.py` is byte-idempotent across two
runs (verified on an isolated copy). All twelve standing checkers pass, the working tree is
clean, and the Emergency Restore / Panic Escape separation (T-11-22) holds structurally: none
of the four Emergency Restore menus or case bodies is enclosed by any Panic Escape
conditional, in either fork.

That is where the good news stops. Three defects are shipping in the signed artifacts.

The most serious is not new to this phase but was re-certified by it: **`dimming()` and
`silence()` have unreachable bodies.** Both gate on the *container* `settings_snapshot.<x>`
with condition 100, with the entire capture-and-apply body in the OTHERWISE arm — and cycle
11's `seed_settings_snapshot()` made that container a permanent bootstrap invariant that
nothing ever removes. The gate is therefore permanently TRUE and both primitives take the
`Nothing` arm on every run. Two of BD-06's nine shipped interventions (`Dim`, `Silence`) are
silent no-ops on device, and this phase's `environmental_restore_check.py` / `phase9_self_check.py`
site tables and the MANIFEST's "15 / 15 / 22, 19 coerced" prose are auditing dead code.

Second, the new Panic Escape removal path references `is.workflow.actions.text.match`'s output
as `"Matched Text"`. The golden corpus is unanimous (15/15) on `"Matches"`, and this repo's own
`build_sentient.py` uses `"Matches"` for the identical action. `ACTION_OUTPUT_NAMES` does not
cover `text.match`, so `verify_output_names()` is blind to it. If the reference does not
resolve, the removal direction of Panic Escape is permanently dead and — by the branch's own
design — reports "Nothing was changed" rather than an error.

Third, the Aware fork's Use Model audit is inserted at the *first* `persist_contract()` marker
only. Phase 11 added a second OPEN-arm `primitive_dispatch()` rendering, so a user who removes
Panic Escape silently loses the entire Aware differentiator. `sentient_core_check.py`'s
`assert len(models) == 1` pins that defect rather than catching it.

Beyond those, the recurring theme is the one plan 11-04 already found once: **coupled literals
with no reconciliation.** The phase fixed the `schema_version` triple and then created or left
five more instances of the same shape, one of which (`PROFILE_NAMES` ↔ `thresholds.*` ↔ the
hand-authored bootstrap chain) has exactly the hard-error consequence BD-06-A1 itself names.

## Critical Issues

### CR-01: `dimming()` and `silence()` bodies are unreachable — the container existence gate can never read false

**File:** `tools/build_state_engine.py:576-595` (`dimming`), `tools/build_state_engine.py:598-618` (`silence`)
**Emitted at:** `src/PROSOCHE-Dumb.xml` actions 1027-1029 (Silence) and 1121-1123 (Dim), ×11 renderings each

**Issue:**

```python
a += read_value("settings_snapshot.brightness", variable("State"), "Brightness Snapshot")
snapshot_g, snapshot_if = if_block("Brightness Snapshot", 100)
a += [snapshot_if, action("is.workflow.actions.nothing"), otherwise(snapshot_g)]
a += device_detail("Current Brightness", "Captured Brightness")   # <-- OTHERWISE arm
```

The gate is `settings_snapshot.brightness` **has any value** → do nothing; otherwise → capture
and dim. But `seed_settings_snapshot()` (`:2481`) seeds that key as a permanent three-leaf
sub-dictionary, and `clear_snapshot()` (`:443`) deliberately clears only the *leaf*
`.original_value`, never the container — the docstring calls that a "PERMANENT invariant" and
`verify_sentinel_gates()` explicitly licenses container gates at condition 100 on those
grounds. Nothing in either fork ever removes the container. A read of a present, non-empty
sub-dictionary passes `has any value` (this project's own donor-measured semantics: present
but empty is already TRUE; a dict is present and non-empty).

Therefore the true arm — `Nothing` — fires on every run, and the *entire* body sits in the
unreachable otherwise arm: the Get Device Details capture, the three `settings_snapshot.*`
writes, the `Dim Target` read, the Set Brightness / Set Volume write, **and** the
"Brightness could not be captured, so nothing was changed" fallback alert. Circles configured
to `Dim` or `Silence` produce nothing at all on device — no dim, no alert, no state write, no
error. Two of the nine shipped primitives are silent no-ops.

This is the same class `verify_dispatch_coverage()` was built to prevent, one level deeper:
the branch is reached, the body is dead. Note the polarity contrast with
`restore_managed_settings()` (`:464`), where the identical always-true container gate is
*harmless* because the work is in the TRUE arm and the leaf gate then decides.

Consequence for this phase's own artifacts: `docs/environmental_restore_check.py`'s
`EXPECTED_SITES = {15, 15, 22}`, `docs/phase9_self_check.py`'s 30-site / 19-coerced audit, and
MANIFEST.md's "Dimming and Silence writes now execute where they previously no-opped" all
certify code that cannot run.

**Fix:** Gate on the *leaf*, numerically, mirroring `restore_managed_settings()`'s own
established rule ("only a strictly positive reading counts as a real capture"), and invert the
polarity so the capture happens when no original is recorded:

```python
# dimming()
a += read_value("settings_snapshot.brightness.original_value", variable("State"),
                "Brightness Original")
# already captured (> 0) -> leave the existing unrestored snapshot alone
snapshot_g, snapshot_if = if_block("Brightness Original", 2, number=0)
a += [snapshot_if, action("is.workflow.actions.nothing"), otherwise(snapshot_g)]
a += device_detail("Current Brightness", "Captured Brightness")
...
```

The leaf is seeded with the cleared sentinel `"null"`, which coerces to a false `> 0` test
(Donor 6.1), so the otherwise arm is reachable on a fresh install and closed once a real
original is captured. Apply the identical change to `silence()` for
`settings_snapshot.volume.original_value`.

Then add a build guard in the same commit — the existing `verify_sentinel_gates()` cannot see
this because the container is not sentinel-written. Assert that every `setbrightness` /
`setvolume` write is *reachable*: i.e. that no condition-100 gate whose variable is read from a
`settings_snapshot` **container** key encloses (in either arm) a `getdevicedetails` or a
`setbrightness`/`setvolume`. And correct the site tables in
`docs/environmental_restore_check.py` and `docs/phase9_self_check.py` only after the bodies are
live, not before.

---

### CR-02: the new Panic Escape branch reads `text.match` through a wrong `OutputName`, silently killing the removal direction

**File:** `tools/build_state_engine.py:2030-2032` (new this phase); same defect pre-existing at `tools/build_state_engine.py:1968` (Sync My Profile)

**Issue:**

```python
action("is.workflow.actions.text.match", UUID=match_id,
       WFMatchTextPattern=PANIC_ESCAPE_SECTION_PATTERN,
       text=output(note_id, "Text")),
action("is.workflow.actions.gettext", UUID=section_id,
       WFTextActionText=output(match_id, "Matched Text")),   # <-- wrong output name
```

Measured against the bundled golden corpus (19 shipped shortcuts, all
`ActionOutput` references resolved back to their producing identifier):

| producing action | `OutputName` observed | count |
|---|---|---:|
| `is.workflow.actions.text.match` | `Matches` | 15 |
| `is.workflow.actions.text.match.getgroup` | `Group from Matched Text` | 1 |
| `is.workflow.actions.text.match.getgroup` | `Text` | 7 |

`"Matched Text"` never appears for `text.match` in the corpus. This repo's own
`tools/build_sentient.py:153-159` uses `output(matches, "Matches")` for the same identifier —
so the artifact carries two contradictory names for one action. `ACTION_OUTPUT_NAMES`
(`:3256`) covers only `getrichtextfrommarkdown`, so `normalise_output_names()` /
`verify_output_names()` — the machinery built for exactly this defect class — cannot see it.

The consequence is worse here than at the Sync site because of how the branch is written. If
the reference does not resolve, `Panic Escape Section` is empty, the condition-99 "contains"
test against `- Panic Escape: OFF` is always false, and control falls to the otherwise arm,
whose own comment says: *"Anything else … can only ever restore, never remove."* The user then
sees `"The Note says ON and Panic Escape is already available. Nothing was changed."` — a
confident, wrong, unlogged success message. The entire removal feature this phase shipped is
dead with no error anywhere.

The Sync My Profile instance is equally silent: it would store an empty
`profile_snapshot.proforma` forever.

**Fix:** Use the corpus-attested name at both sites and add the entry to the recurrence guard
so a third site cannot repeat it:

```python
# tools/build_state_engine.py
ACTION_OUTPUT_NAMES = {
    "is.workflow.actions.getrichtextfrommarkdown": "Rich Text from Markdown",
    "is.workflow.actions.text.match": "Matches",   # golden corpus 15/15
}
```

`normalise_output_names()` then rewrites both sites automatically and `verify_output_names()`
fails the build on any regression. Note the residual shape question — `text.match`'s output is
a *list* of matches, so `gettext` over it stringifies a one-element list; if the on-device
round trip shows that is not the value wanted, use
`is.workflow.actions.getitemfromlist` with `WFItemSpecifier="First Item"` between them, exactly
as `build_sentient.py:159` already does.

---

### CR-03: in the Aware fork the Use Model audit only exists on the Panic-Escape-enabled path

**File:** `tools/build_sentient.py:265-271`; interaction with `tools/build_state_engine.py:1014-1020`

**Issue:**

```python
for index, item in enumerate(actions):
    value = item.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "")
    if value.startswith("Reload before writing a contract."):
        actions[index:index] = audit_block()
        break        # <-- first marker only
```

Before this phase there was one OPEN-arm `primitive_dispatch()` rendering, so "first marker"
and "the OPEN-arm marker" coincided. Plan 11-05 added a second OPEN-arm rendering (the
`panic_escape_enabled == 0` otherwise arm of `universal_leaving()`), rendered *after* the
Continue arm in document order. Measured on the shipped `src/PROSOCHE-Sentient.xml`:

```
dispatch renderings:  998, 1328, 1842, 2115, ... (11 total)
persist_contract:    1150, 1414, 1926, 2199, ... (11 total)
audit marker:        1084   <-- inside rendering #1 (Continue) only
askllm:              1108   <-- exactly one, same place
```

So an Aware user who removes Panic Escape reaches the `Intention` (Confession) primitive with
**no contract audit at all** — the entire reason the Aware fork exists disappears because of an
unrelated bypass setting, silently and with no fork-level difference the user can observe.

`docs/sentient_core_check.py:102-103` asserts `len(models) == 1`, which locks this in rather
than detecting it, and `build_sentient.py` does not run `verify_circle_zero_silence()` or any
per-rendering coverage guard that would notice.

**Fix:** Insert the audit into every OPEN-arm rendering, and assert the count rather than
pinning it to one. Locate the OPEN arm structurally (the same way
`verify_circle_zero_silence()` does), then:

```python
open_index, open_end = open_arm_bounds(actions)          # reuse the router-shape locator
targets = [i for i in range(open_index, open_end)
           if actions[i].get("WFWorkflowActionParameters", {})
              .get("WFCommentActionText", "").startswith("Reload before writing a contract.")]
if not targets:
    raise SystemExit("semantic Confession contract marker not found in the OPEN arm")
for index in reversed(targets):                          # reverse so earlier indexes stay valid
    actions[index:index] = audit_block()
```

`audit_block()` calls `uid(name)` with fixed literal keys, so multiple renderings would collide
on `GroupingIdentifier`/`UUID` — `uid()` must take a per-rendering discriminator
(`uid(f"{ordinal}/{name}")`) or the second rendering will reuse the first's grouping
identifiers, which `.claude/CLAUDE.md` §4 names as the top real-world failure mode. Then change
`docs/sentient_core_check.py:103` from `== 1` to the measured OPEN-arm rendering count, with a
comment deriving it.

If the intended decision is instead "audit only the Panic-Escape path", that is a product
decision that must be written down in `docs/CAPABILITY-DECISIONS.md` and surfaced in the Note,
because it makes an unrelated setting silently switch forks.

## Warnings

### WR-01: `verify_panic_escape_seed()`'s gate check is coupled to a magic variable name and silently passes when it drifts

**File:** `tools/build_state_engine.py:2702-2705`

**Issue:** The third assertion matches conditionals by
`VariableName == "Panic Escape Enabled"` — a bare literal that appears nowhere as a shared
constant (the emitter uses its own literal at `:991-992`). I demonstrated the gap: rename the
variable to `PE` *and* flip the gate to condition 100, and the guard passes clean. It also does
not cover the two `"Panic Escape Stored"` gates in `panic_escape_branch()` (`:2043`, `:2071`),
which decide whether the flag is written and are subject to the identical axis-7 trap.

**Fix:** Resolve the tested variable by provenance instead of by name — `_read_variable_keys()`
already maps variables to the literal key they were read from — and cover *every* variable read
from `panic_escape_enabled`:

```python
reads = _read_variable_keys(actions)
guarded = {name for name, keys in reads.items() if PANIC_ESCAPE_KEY in keys}
...
if name in guarded and parameters.get("WFCondition") not in NUMERIC_CONDITION_CODES:
    existence.append((index, parameters.get("WFCondition")))
```

Additionally assert `guarded` is non-empty, so a rename that orphans the gate entirely fails
rather than passes vacuously.

---

### WR-02: `MINIMUM_TOKEN_STRINGS = 775` is ~36% below the measured value, so the floor guard has 430 units of slack

**File:** `docs/note_identity_check.py:84`

**Issue:** The docstring says the floor was "Measured at the phase-11 baseline (`ae0226c`) and
re-measured on the decrypted payload of both signed containers." Measured now with the file's
own counting method: **1205 (Dumb) / 1209 (Sentient)**. MANIFEST.md:173-174 states the
pre-phase baseline was 1105/1109. 775 matches neither. The named defect — parameter-defect
axis 2, string-typed parameters converted to bare `WFTextTokenAttachment` — could hit 430 sites
and still pass.

**Fix:** Set the floor to the measured value and derive it in a comment the way
`environmental_restore_check.py`'s site table does:

```python
# Measured 2026-08-17 on both shipped forks: 1205 (Dumb) / 1209 (Sentient).
# The floor is the LOWER of the two so one constant serves both.
MINIMUM_TOKEN_STRINGS = 1205
```

---

### WR-03: the brightness-floor assertion in `phase5_self_check.py` is vacuous

**File:** `docs/phase5_self_check.py:117`

**Issue:**

```python
require(params.get("WFBrightness") not in (0, "0", 0.0), "brightness may reach zero")
```

`set_brightness()` (`build_state_engine.py:433`) always passes a `variable(...)` dict.
Measured: all 15 `WFBrightness` values in each fork are `dict`. The comparison can never be
true, so this line has never had the capacity to fail. It reads as a safety assertion and is
decoration.

**Fix:** Either delete it (BD-02's Phase 9 addendum removed the absolute floor anyway, so the
real invariant is capture-and-restore, which `environmental_restore_check.py` owns), or make it
test something real — that the write's operand is a variable read from `safety.dim_target` or
`settings_snapshot.*.original_value` and never a literal:

```python
value = params.get("WFBrightness")
require(isinstance(value, dict) and value.get("Value", {}).get("Type") == "Variable",
        "a Set Brightness write carries a literal target instead of a captured/config variable")
```

---

### WR-04: nothing reconciles `PROFILE_NAMES` with the Config key paths or the hand-authored bootstrap chain — five copies, hard-error consequence

**File:** `tools/build_state_engine.py:56`; `src/PROSOCHE-Dumb.xml` actions 2, 7, 55-65

**Issue:** `build_state_engine.py:53-55`'s own comment states the stakes exactly: *"a profile
name is a live Config key path (`thresholds.<profile>`, `cooldown_seconds.<profile>`), and a
dotted read with a missing segment is a HARD ERROR in this runtime, so a partial rename here is
a crash rather than a degradation."* There is no guard.

The profile vocabulary exists in five independent, unlinked places:

1. `PROFILE_NAMES` (`:56`) — drives the Change Profile submenu, which writes `profile` directly;
2. the Config literal's `thresholds` keys (action 7) — read as `thresholds.<profile>`;
3. the Config literal's `cooldown_seconds` keys — read as `cooldown_seconds.<profile>`;
4. the **hand-authored** import normalisation chain (actions 55-65: literals `Paradise`,
   `Inferno`, fallback gettext `Purgatory`) — the only thing that decides the first-run value;
5. the import-question default and its Text action (action 2).

Only (1) is generated. Renaming a profile in `PROFILE_NAMES` without editing (2)-(5) — or vice
versa — builds, signs, imports, and then hard-errors on the first OPEN with "could not evaluate
the key path". This is structurally the same defect `verify_dispatch_coverage()` exists to
catch on the sequences side, on a path with a worse failure mode.

**Fix:** Add `verify_profile_coverage()` beside `verify_dispatch_coverage()` and run it in both
builders:

```python
def verify_profile_coverage(actions):
    config = json.loads(<the Config literal, located as verify_dispatch_coverage does>)
    for table in ("thresholds", "cooldown_seconds"):
        keys = set(config.get(table, {}))
        if keys != set(PROFILE_NAMES):
            raise SystemExit(
                f"profile coverage: Config.{table} names {sorted(keys)} but PROFILE_NAMES is "
                f"{sorted(PROFILE_NAMES)} -- `{table}.<profile>` is a DOTTED read, so a name "
                "that no key matches is a hard 'could not evaluate the key path' error on the "
                "next OPEN, after active_session was already written")
    # every literal the bootstrap chain and the profile menu can ever write must be a key
    written = {p["WFTextActionText"] for p in (a.get("WFWorkflowActionParameters", {})
               for a in actions) if isinstance(p.get("WFTextActionText"), str)
               and p["WFTextActionText"] in set(PROFILE_NAMES) | keys}
    ...
```

The minimum useful version is the first half: `set(config["thresholds"]) ==
set(config["cooldown_seconds"]) == set(PROFILE_NAMES)`.

---

### WR-05: `state_engine_self_check.THRESHOLDS` duplicates the Config literal with no assertion, and this pair has already drifted once

**File:** `docs/state_engine_self_check.py:15-19`

**Issue:** The comment says "This table is a duplicate of the Config literal at
`src/PROSOCHE-Dumb.xml` action 7 and must be changed in the same commit as it." Nothing
enforces it, and `src/CONFIG-BLOCK.md:164` records that this exact pair *did* silently drift
through Phase 10 ("the pre-existing `thresholds` drift, where this mirror still showed the
pre-Phase-10 curve"). Phase 11 edited the table again (`Limbo` → `Purgatory`) and still did not
add the reconciliation. `structural_check()` in the same file already parses the artifact, so
the data is one line away.

**Fix:** In `structural_check()`, parse the Config literal and assert equality:

```python
config = json.loads(next(p["WFTextActionText"] for p in
                         (a.get("WFWorkflowActionParameters", {}) for a in actions)
                         if isinstance(p.get("WFTextActionText"), str)
                         and '"config_version"' in p["WFTextActionText"]))
assert config["thresholds"] == THRESHOLDS, (
    f"THRESHOLDS mirror {THRESHOLDS} disagrees with the shipped Config literal "
    f"{config['thresholds']} -- this file's arithmetic then verifies a curve nothing ships")
```

---

### WR-06: three generator constants are coupled to hand-authored Note copy with no assertion

**File:** `tools/build_state_engine.py:1979` (`PANIC_ESCAPE_OFF_LINE`), `:1984` (`PANIC_ESCAPE_SECTION_PATTERN`), `:47-48` (`CIRCLE_NAMES`)

**Issue:** The Note body is a hand-authored `WFTextTokenString` in the artifact, edited through
`plist_text_edit.py`. Three separate generator constants depend on its exact wording, and
nothing checks any of them:

- `PANIC_ESCAPE_SECTION_PATTERN` requires `## PANIC ESCAPE` to exist and to be followed by
  `## MY PHONE, ON PURPOSE`. Reordering or renaming either heading yields an empty match, which
  the branch (by design, `:2039`) treats as "restore only, never remove" — the feature dies
  with no error.
- `PANIC_ESCAPE_OFF_LINE` (`- Panic Escape: OFF`) must be the exact mirror of the Note's live
  `- Panic Escape: ON` line, including the leading `- ` and the capitals. A copy edit to
  `— Panic Escape: OFF` or `Panic Escape — OFF` kills removal silently.
- `CIRCLE_NAMES` is described in its own comment as "ONE SOURCE OF TRUTH", but the Note carries
  a **fourth, hand-written copy** of the nine names (`- Circle 1 · Limbo` … `- Circle 9 ·
  Treachery`, Note offset 5149). Renaming a Circle in the tuple leaves the Note stale.

**Fix:** Extend `docs/note_identity_check.py` — it already locates the Note body by content and
already parses both forks — with three assertions:

```python
body = <the Note body string, already located>
require(body.count("## PANIC ESCAPE") == 1 and
        body.index("## PANIC ESCAPE") < body.index("## MY PHONE, ON PURPOSE"),
        "the PANIC ESCAPE section is missing or no longer precedes MY PHONE, ON PURPOSE -- "
        "the bounded text.match returns nothing and Panic Escape can then only ever restore")
require(re.search(r"^- Panic Escape: (ON|OFF)$", body, re.M),
        "the Note's Panic Escape setting line no longer matches the '- Panic Escape: <WORD>' "
        "shape PANIC_ESCAPE_OFF_LINE mirrors")
for n, name in enumerate(CIRCLE_NAMES, 1):          # import from the generator
    require(f"- Circle {n} · {name}" in body,
            f"the Note's Circle list is stale: it does not name Circle {n} as {name!r}")
```

---

### WR-07: `plist_text_edit.py` is declared the trusted path but the generator keeps a divergent private copy, and four of the module's six exports have no caller

**File:** `tools/plist_text_edit.py:71,81,156,179`; `tools/build_state_engine.py:2453-2478`

**Issue:** The module docstring presents a six-step method and says step 1 — "Prove a no-op
`plistlib.dumps` is byte-identical to the source → `assert_noop_roundtrip()`" — "licenses every
later structured edit." Grep across `tools/` and `docs/` shows the only importer is
`build_sentient.py:12`, and it imports only `find_action` and `replace_in_token`. `load()`,
`assert_noop_roundtrip()`, `replace_in_plain()` and `save()` have no caller anywhere. Step 1 of
the module's own method is never executed by any automated path.

Meanwhile `build_state_engine.py` keeps `_replace_in_token()` — a second, materially different
implementation used for all four bootstrap-template edits, including this phase's new
`seed_panic_escape()`:

| | `plist_text_edit.replace_in_token` | `build_state_engine._replace_in_token` |
|---|---|---|
| occurrences replaced | all, with an asserted count | **first only** (`string.find`) |
| offset strategy | rebuild from a rescan of placeholders | shift by `delta` where `offset > at` |
| pre-edit offset validation | yes (`assert_offsets_match`) | no |
| placeholder-count invariant | asserted | not asserted |

The shift predicate `offset > at` is also subtly wrong for an attachment landing inside the
replaced span (it would be shifted rather than rejected); no current call site hits that, but
the divergence means the "trusted path" claim is not true of the code that does the most
editing.

**Fix:** Delete `_replace_in_token()` and have `seed_settings_snapshot()`,
`seed_pending_exit()`, `seed_panic_escape()` and `fix_state_rebind()` call
`plist_text_edit.replace_in_token(inner, old, new, expected_count=1)`. Then either wire
`assert_noop_roundtrip()` into `main()` (`data, raw = plist_text_edit.load(SOURCE)` at the top,
`assert_noop_roundtrip(data, raw)` immediately after) or delete `load`/`assert_noop_roundtrip`/
`save`/`replace_in_plain` and correct the docstring so it stops describing steps no caller
runs.

---

### WR-08: `plist_text_edit` discards the length component of every range key and silently rewrites it to 1

**File:** `tools/plist_text_edit.py:61-68, 97-116, 151-152`

**Issue:** `_key_offset()` matches `{offset, length}` but returns only `group(1)`.
`assert_offsets_match()` compares offsets only. `replace_in_token()` then emits every key as
`f"{{{offset}, 1}}"`. So a key of `{5478, 3}` passes the "offsets match" assertion and is
silently rewritten to `{5478, 1}` — an edit the module never reports. The docstring at `:42`
asserts "which is why every `attachmentsByRange` key has length 1" but no code enforces it.
(Measured: all 1654 / 1664 keys in the shipped forks currently have length 1, so this is
latent, not live.)

**Fix:** Assert the invariant where it is claimed:

```python
def _key_range(key: str) -> tuple[int, int]:
    match = RANGE_KEY.match(key)
    if not match:
        raise SystemExit(...)
    offset, length = int(match.group(1)), int(match.group(2))
    if length != 1:
        raise SystemExit(
            f"attachmentsByRange key {key!r} has length {length}, not 1 -- a U+FFFC "
            "placeholder is exactly one character, so a longer range already spans unrelated "
            "prose and this module would silently rewrite it to 1")
    return offset, length
```

---

### WR-09: offsets are computed as Python code points, not UTF-16 units, with no assertion that the difference is nil

**File:** `tools/plist_text_edit.py:111, 145`; `docs/note_identity_check.py:146`

**Issue:** `enumerate(string)` yields code-point indices. `attachmentsByRange` keys are NSRange
offsets into an `NSAttributedString`, i.e. **UTF-16 code units**. For everything currently in
the artifact the two agree — I scanned both forks and found **zero** characters above U+FFFF
(`Ē` U+0112, `—` U+2014, `·` U+00B7, `⚠` U+26A0 are all BMP). But the module is explicitly
positioned as the sanctioned path for *future* Note copy edits, and a single emoji (U+1F600+)
placed upstream of an attachment would shift every subsequent iOS offset by one per astral
character while this code computes it unshifted — producing exactly the out-of-bounds range the
module exists to prevent.

**Fix:** Make the assumption explicit and enforced, so the failure is a build error rather than
a device crash:

```python
def _assert_bmp_only(string: str, where: str) -> None:
    astral = sorted({c for c in string if ord(c) > 0xFFFF})
    if astral:
        raise SystemExit(
            f"{where}: the string contains non-BMP character(s) {astral} -- this module "
            "computes offsets as Python code points, but attachmentsByRange keys are UTF-16 "
            "NSRange offsets, so every attachment after such a character would be off by one "
            "per astral character and an out-of-bounds range can crash Shortcuts on import")
```

Call it from `assert_offsets_match()` and from `replace_in_token()` on both the old and new
strings. Add the same scan to `note_identity_check.check_offsets()`.

---

### WR-10: `build_sentient.py` runs a hand-maintained subset of the generator's verify chain, omitting both guards added this phase

**File:** `tools/build_sentient.py:281-313`

**Issue:** The file's own comments justify running each guard per fork ("asserted per fork,
never inferred"). Six guards `build_state_engine.main()` runs are absent from the Aware chain:

- `verify_parameter_keys`
- `verify_conditional_action_string`
- `verify_pending_exit_seed`
- `verify_panic_escape_seed` — added this phase
- `verify_compound_value_reads`
- `verify_circle_zero_silence`

The last two matter most. Sentient *inserts actions into the OPEN arm* (`audit_block()`, which
adds conditionals, a `returntohomescreen` and an `exit`), so `verify_circle_zero_silence()`'s
four properties are precisely the ones a Sentient-only insertion could break, and the fork is
the only artifact where they are not asserted. `verify_panic_escape_seed()` is skipped even
though `verify_state_seed()` is run with the rationale "it proves the subtree survived the
fork" — and `verify_panic_escape_seed()`'s own docstring records that `verify_state_seed()`
does not cover the panic field.

There is also no mechanism preventing further drift: adding a guard to `main()` does not add it
here.

**Fix:** Export the chain as data from `build_state_engine.py` and have both builders consume
it, so a new guard is armed in both by construction:

```python
# build_state_engine.py
VERIFIERS = (verify_parameter_keys, verify_string_envelopes, verify_output_names,
             verify_required_pickers, verify_conditional_inputs,
             verify_conditional_action_string, verify_numeric_operands,
             verify_state_seed, verify_pending_exit_seed, verify_panic_escape_seed,
             verify_restore_gates, verify_sentinel_gates, verify_compound_value_reads,
             verify_router_shape, verify_circle_zero_silence, verify_dispatch_coverage)

def verify_all(actions):
    for check in VERIFIERS:
        check(actions)
```

If any single guard genuinely cannot apply to the fork, exclude it by name with a written
reason rather than by omission.

---

### WR-11: `build_sentient.py` addresses the import-preference insertion by a hard-coded action index

**File:** `tools/build_sentient.py:258-262`

**Issue:**

```python
actions[6:6] = [action("is.workflow.actions.gettext", UUID=import_id, WFTextActionText="yes"),
                set_var("Import AI", output(import_id, "Text"))]
root["WFWorkflowImportQuestions"].append({"ActionIndex": 6, ...})
```

`build_state_engine.py`'s module docstring states the rule: *"Anchors are found by their branch
comments, never by mutable action indexes."* This is the one place that breaks it, and it
breaks it twice — the splice position and the `ActionIndex` both hard-code 6.
`build_state_engine.main()` pins only actions 0-4 (`pinned = actions[:5]`) and
`phase5_self_check` pins `ids[:5]`, so actions 5 and 6 are *unpinned*. A future generator change
that inserts an action at index 5 would move the third import question onto an unrelated
parameter with no error from either builder; `sentient_core_check.py:109-110` would then catch
it, but only after the fork is built.

**Fix:** Locate the insertion point by content and derive the index:

```python
anchor = next(i for i, a in enumerate(actions)
              if a.get("WFWorkflowActionParameters", {}).get("WFVariableName") == "Import Voice")
at = anchor + 1
actions[at:at] = [...]
root["WFWorkflowImportQuestions"].append({"ActionIndex": at, ...})
```

and extend `build_state_engine.main()`'s pin from `actions[:5]` to cover the full frozen import
prologue.

---

### WR-12: seed helpers raise bare `StopIteration` / `IndexError` instead of the project's SystemExit-with-consequence convention

**File:** `tools/build_state_engine.py:2590` (`seed_pending_exit`), `:2658` (`seed_panic_escape`), `:2477` (`_replace_in_token`)

**Issue:** Both new-generation seeders locate their anchor line with an unguarded `next()`:

```python
line = next(text for text in inner["string"].splitlines() if PANIC_ESCAPE_ANCHOR in text)
```

If `'"ai_enabled": false,'` ever moves or is reformatted, this raises a bare `StopIteration`
with no message — against the file's own stated failure convention ("every guard raises
`SystemExit` with a message naming the CONSEQUENCE"), and inside a generator expression, which
in some contexts is swallowed rather than propagated. `seed_settings_snapshot()` gets this right
(`:2489` returns early when the anchor is absent). Separately, `_replace_in_token()`'s
post-shift validation `inner["string"][offset] != "￼"` can raise `IndexError` when a shrinking
edit pushes an offset past the end of the new string.

**Fix:**

```python
line = next((text for text in inner["string"].splitlines() if PANIC_ESCAPE_ANCHOR in text), None)
if line is None:
    raise SystemExit(
        f"the bootstrap template no longer contains the anchor {PANIC_ESCAPE_ANCHOR!r}, so "
        f"{PANIC_ESCAPE_KEY} cannot be seeded -- universal_leaving()'s gate would then read a "
        "key that is not there and the Panic Escape removal path is dead on every device")
```

and in `_replace_in_token()` bounds-check before indexing:

```python
if offset >= len(inner["string"]) or inner["string"][offset] != "￼":
    raise SystemExit(f"attachment offset {offset} is out of bounds or no longer points at a "
                     "placeholder -- an out-of-bounds range can crash Shortcuts on import")
```

---

### WR-13: MANIFEST.md's dispatch-branch count is stale by nine

**File:** `artifacts/shortcuts/MANIFEST.md:223-224`

**Issue:** "All nine shipped names are proven present in the generator tuple, in all three
`sequences` arrays, **on all ninety emitted dispatch branches** and in the decrypted payload of
both signed containers, and every one of those branches is proven to carry condition code 4."

Measured on the shipped artifacts: **99** branches per fork (9 names × 11 renderings), not 90.
The eleventh rendering is this phase's own Panic Escape change, described correctly elsewhere in
the same document (`docs/environmental_restore_check.py`'s table and BUILD-NOTES §24.3 both moved
to eleven). MANIFEST.md is described in `manifest_check.py`'s docstring as "the only
human-readable claim this repository makes about what shipped"; a wrong count in it is a false
provenance claim of exactly the kind that check exists to prevent, and `manifest_check.py`
validates only the table rows, not the prose.

**Fix:** Change "ninety" to "ninety-nine (nine names × eleven `primitive_dispatch()`
renderings)" and cross-check the same paragraph against BUILD-NOTES §24.3's rendering-count
derivation, which is correct.

---

### WR-14: the two display names exist as three unlinked hardcoded copies, and one assertion is a suffix test

**File:** `tools/build_sentient.py:38-39`; `docs/manifest_check.py:51-54, 130`; `docs/sentient_core_check.py:33-34, 51`

**Issue:** `CORE_NAME`/`AWARE_NAME`, `DISPLAY_NAMES`, and `CORE`/`AWARE` are three independent
literal pairs with no import relationship and no cross-assertion. `manifest_check.py:130` still
carries the stale comment `# "Dumb" / "Sentient"` on a line that now yields `"Core"`/`"Aware"`.
`sentient_core_check.py:51` asserts only `SENTIENT["WFWorkflowName"].endswith("Aware")`, which
passes for any string ending in those five characters. Nothing at all asserts the **Core** fork's
root `WFWorkflowName` — it is hand-set in `src/PROSOCHE-Dumb.xml` and never verified, even
though MANIFEST.md:186-192 makes the filename/display-name equality the load-bearing anti-dead-
install rule.

The Note↔`CORE_NAME` coupling *is* guarded, indirectly and well, by `fix_fork_strings()`'s
`expected_count=2`.

**Fix:** Put the pair in one place — `tools/build_sentient.py` already owns them — and import it
in both checkers (`docs/` scripts already add `tools/` to `sys.path` via
`environmental_restore_check.load_module`). Then tighten:

```python
# sentient_core_check.py
assert SENTIENT["WFWorkflowName"] == AWARE, SENTIENT["WFWorkflowName"]
assert DUMB["WFWorkflowName"] == CORE, DUMB["WFWorkflowName"]
```

and update `manifest_check.py:130`'s comment to `# "Core" / "Aware"`.

---

### WR-15: T-11-22 — the phase's only `critical` threat — has no standing checker

**File:** `artifacts/shortcuts/MANIFEST.md:89-93`; no corresponding `docs/*.py`

**Issue:** The separation of Panic Escape from Emergency Restore is described in
`universal_leaving()`'s docstring (`build_state_engine.py:958-964`) as threat T-11-22, "the only
`critical` in this phase". Its verification is a hand-measurement recorded in MANIFEST prose:
"Re-measured on the decrypted payloads … two menus offer Emergency Restore and two case bodies
implement it in each fork, and **none of the four is enclosed by any Panic Escape
conditional**."

I reproduced that measurement and it holds today (Dumb actions 171/174/1665/4229, Sentient
173/176/1733/4297, zero Panic Escape enclosures). But a hand-measurement recorded in a markdown
file is not a guard: the next change to `universal_leaving()` or `panic_escape_branch()` will not
re-run it. Every other invariant of comparable weight in this repo (dispatch coverage, restore
gates, sentinel gates, router shape, silent band) has an executable guard.

**Fix:** Add `verify_panic_escape_isolation()` to the shared `VERIFIERS` tuple — the enclosure
machinery already exists (`enclosing_groups()`, `:1487`):

```python
def verify_panic_escape_isolation(actions):
    panic = {p["GroupingIdentifier"] for p in (a.get("WFWorkflowActionParameters", {}) for a in actions)
             if p.get("WFControlFlowMode") == 0
             and _tested_variable(p) in ("Panic Escape Enabled", "Panic Escape Stored",
                                         "Manual Panic Escape Requested")}
    enclosure = enclosing_groups(actions)
    sites = [i for i, a in enumerate(actions)
             if a.get("WFWorkflowActionParameters", {}).get("WFMenuItemTitle") == "Emergency Restore"
             or "Emergency Restore" in (a.get("WFWorkflowActionParameters", {}).get("WFMenuItems") or [])]
    if not sites:
        raise SystemExit("no Emergency Restore surface found at all -- the safety hatch is gone")
    caught = [i for i in sites if set(enclosure[i]) & panic]
    if caught:
        raise SystemExit(
            f"Emergency Restore is enclosed by a Panic Escape conditional at actions {caught} -- "
            "T-11-22: a user who removed the bypass and cannot reach Emergency Restore is "
            "stranded inside an intervention with a dimmed screen or a silenced device")
```

Also note the interaction BD-06-A2 does not record: shortening the Note title to the bare
product name widened the `contains` lookup, so a wrong-Note binding is now more likely — and a
wrong Note has no `## PANIC ESCAPE` section, which makes the new removal path silently
unavailable (the same otherwise-arm behaviour as CR-02). Worth adding to BD-06-A2's recorded
consequences.

---

_Reviewed: 2026-08-17_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
