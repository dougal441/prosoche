---
phase: 16-dimming-and-silence-as-distinct-device-proven-circles
plan: 04
subsystem: shortcuts-generator
tags: [D-02, DEV-06, state-shape, build-guard, dead-state-removal, SAFE-03, CIRC-03, CIRC-05]
status: complete
requires:
  - "16-01: the capture is persisted to disk — the consequence that made D-02 timely"
  - "16-CONTEXT.md D-02 (LOCKED user decision) — this plan implements it, does not re-litigate it"
  - "tools/build_state_engine.py::_read_variable_keys — the existing read-key index, reused not replaced"
provides:
  - "tools/build_state_engine.py::verify_no_removed_snapshot_leaf_reads — build guard making the no-reader property permanent, on both forks"
  - "tools/build_state_engine.py::_is_removed_snapshot_leaf — scoped predicate, so a foreign dictionary's changed_at is not falsely flagged"
  - "tools/build_state_engine.py::D02_REMOVED_SNAPSHOT_LEAVES — one list shared by the recogniser and the guard"
  - "tools/build_state_engine.py::SNAPSHOT_SEEDED_D02 — convergence recogniser for the already-shipped three-leaf sentinel shape"
  - "docs/BUILD-NOTES.md §17: DEV-06 CLOSED, site count corrected 20 → 44 with derivation"
affects:
  - "src/PROSOCHE-Dumb.xml and src/PROSOCHE-Sentient.xml rebuilt (−88 actions each)"
  - "artifacts/shortcuts/MANIFEST.md still stale — docs/manifest_check.py RED by constraint D-MANIFEST until 16-06"
  - "the shipped state shape: settings_snapshot.<group> is now a one-leaf container"
tech-stack:
  added: []
  patterns:
    - "guard-and-negative-control pairing (verify_* in the generator, firing demonstrated on an injected read)"
    - "docstring-states-the-defect"
    - "supersede in place, never delete — the retired paragraph is quoted inside its own replacement"
    - "locate by content, never by index"
    - "seeder and recogniser reasoned about separately"
key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - tools/build_sentient.py
    - docs/phase5_self_check.py
    - docs/BUILD-NOTES.md
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml
decisions:
  - "SNAPSHOT_SEEDED_EMPTY left byte-identical; a SECOND recogniser added for the shipped shape — without it the removal never reaches the artifact at all"
  - "The guard covers two read surfaces, because get_value() emits no setvariable terminator and surface one alone would be blind to it"
metrics:
  duration: ~40m
  completed: 2026-08-18
  tasks: 2
  commits: 2
  files: 6
requirements: [CIRC-03, CIRC-05, SAFE-03]
---

# Phase 16 Plan 04: D-02 — retire `changed_at` and `changed_by_session_id` Summary

Both leaves are gone from the writes, the bootstrap seed and the phase5 assertion as one
coordinated generator change, and a build guard now fails any future build that reads one of
them — which is the only thing that made removing a seeded leaf safe in the first place.

## The MEASURED pre-removal write count

Measured 2026-08-18 by a `plistlib` key scan over both built forks immediately before the
removal — **not transcribed from research**:

| Leaf | `Dumb` | `Sentient` |
|---|---:|---:|
| `settings_snapshot.brightness.changed_at` | 11 | 11 |
| `settings_snapshot.brightness.changed_by_session_id` | 11 | 11 |
| `settings_snapshot.volume.changed_at` | 11 | 11 |
| `settings_snapshot.volume.changed_by_session_id` | 11 | 11 |
| **total per fork** | **44** | **44** |

**It matched the research figure exactly** — `16-RESEARCH.md`'s DEV-06 table gives the same
11-per-leaf, 44-per-fork breakdown. It also matches the independent derivation: 2 leaves × 2
groups × **11** `primitive_dispatch()` renderings per fork. Two ways of arriving at the number
agree, which is what lets the record state it as measured rather than counted once.

Post-removal, asserted against the **rebuilt** artifact: **0** on both forks.

`docs/BUILD-NOTES.md` §17's recorded figure of **20** was stale by more than a factor of two —
the same staleness class as the 18-vs-28 correction `09-RESEARCH.md` had to make, with the same
two causes (the `Test a Circle` unroll, and Phase 11's eleventh dispatch rendering).

### Action-count delta, with its derivation

| Fork | Before | After | Delta |
|---|---:|---:|---:|
| Dumb | 4390 | **4302** | −88 |
| Sentient | 4458 | **4370** | −88 |

**−88, not −44, and the doubling is explained rather than accepted.** Measured by identifier:
`setvalueforkey` 163 → 119 (−44) *and* `setvariable` 788 → 744 (−44). The second half is
`normalize_setters()`, which appends exactly one `set_var` rebind per `setvalueforkey` — so
every removed `set_value` removes **two** actions. 44 × 2 = 88, exact on both forks.

Independent corroboration of the same figure: gate B's waived-line action index moved
4236 → **4148** (Dumb) and 4304 → **4216** (Sentient) — precisely −88 on each.

**No number was edited in any checker.** `EXPECTED_SITES`, `expected_counts` and
`expected_coerced` are untouched, and none of them moved: this change adds and removes no
`setbrightness`, `setvolume` or `getdevicedetails` action. `site_audit` still reports 30/30
sites, 19 coerced, 11 correctly not.

## The convergence recogniser — the decision, and why it was not optional

This is the part a "just shrink `SNAPSHOT_SEED`" reading gets wrong, and it was found by
reasoning rather than by a failing test — nothing would have failed.

**`main()` re-parses its own previous output as `SOURCE`, and `seed_settings_snapshot()` is
idempotent on `SNAPSHOT_EMPTY`.** On every tree built since the seed first landed the template
is *already* seeded, `SNAPSHOT_EMPTY` is absent, the seeder returns early — and shrinking
`SNAPSHOT_SEED` alone would have changed **nothing in the shipped artifact**. The build would
have gone green, the writes would have gone, and the seed would have quietly kept both retired
leaves forever.

Two separate decisions were therefore taken and both are recorded inline at the constants:

**`SNAPSHOT_SEEDED_EMPTY` — LEFT BYTE-IDENTICAL.** It is a *recogniser*, not a seed: it holds
the literal text a **build-j** tree carries. Build j is a finished historical fact and it wrote
three empty leaves. Editing this string to two leaves would simply stop it matching the only
shape it exists to match, and the build-j convergence path would die silently — the exact
failure mode the plan warned costs nothing at build time and everything later. Its *replacement*
text is derived from `SNAPSHOT_SEED` rather than written out, so it followed the seed down to one
leaf on its own. That is the wanted behaviour: a build-j tree now converges **straight to the
post-D-02 shape in one step**, rather than to an intermediate shape a second pass would re-correct.

**`SNAPSHOT_SEEDED_D02` — ADDED.** A new recogniser for the already-shipped three-leaf *sentinel*
shape, which neither existing branch matches. Derived from `CLEARED_SENTINEL` and
`D02_REMOVED_SNAPSHOT_LEAVES` rather than spelled out, so it cannot drift from the constants it
must agree with. It runs after the build-j pass, as a `while` loop, so it corrects both groups.

Every edit went through `_replace_in_token()`, never a hand-edit of the template string — it
shifts each `attachmentsByRange` offset and re-asserts each still lands on a U+FFFC placeholder.

### The seed, before and after, read out of the built artifact

```
before: "settings_snapshot": {
          "brightness": {"original_value": "null", "changed_at": "null", "changed_by_session_id": "null"},
          "volume": {"original_value": "null", "changed_at": "null", "changed_by_session_id": "null"}
        },

after:  "settings_snapshot": {
          "brightness": {"original_value": "null"},
          "volume": {"original_value": "null"}
        },
```

**Container and both group sub-dictionaries survive, and `original_value` is still seeded under
each.** Only leaves were removed. Removing a *group* would reintroduce the cycle-10 defect where
the next dotted read of `.original_value` runs against a string parent and hard-errors — that is
recorded in `clear_snapshot()`'s docstring and is why the prohibition exists.

## The no-reader guard, and the demonstration that it fires

`verify_no_removed_snapshot_leaf_reads` is the real deliverable. The deletion is the easy half.

It reuses `_read_variable_keys()` — the existing read-key index — and re-implements nothing.
Asserted by source inspection: the guard's source contains `_read_variable_keys(actions)`, and
contains none of `OutputUUID`, `key_by_uuid`, `text_by_uuid`, `attachmentsByRange`,
`subprocess`, `os.system`, `os.popen` or `check_output`. The backwards UUID walk lives in the
helper and stays there.

**It covers two surfaces, because covering one would have been decoration.**

| Surface | What emits it | Why surface 1 alone is insufficient |
|---|---|---|
| 1 — `read_value()`'s `getvalueforkey → gettext → setvariable` chain | `read_value()` | — |
| 2 — every `getvalueforkey`'s literal `WFDictionaryKey`, scanned flat | `get_value()` | `get_value()` emits no `setvariable` terminator, so the read-key index cannot see it **at all** |

Surface 2 is a *different* surface, not a second copy of the walk.

### The firing demonstration — run, not asserted

Against a deep copy of the real `Dumb` action list:

```
control: real Dumb artifact passes
surface 2 FIRED: a read targets a snapshot leaf that decision D-02 REMOVED from the state shape …
surface 1 FIRED: a read targets a snapshot leaf that decision D-02 REMOVED from the state shape …
negative control: foreign-dictionary changed_at correctly NOT flagged
```

- **Surface 2** injected a flat `getvalueforkey` for
  `settings_snapshot.brightness.changed_by_session_id` → `SystemExit`.
- **Surface 1** injected a full `read_value("settings_snapshot.volume.changed_at", …)` chain →
  `SystemExit`.
- **Negative control:** a `profile_snapshot.changed_at` read is **not** flagged. This matters —
  `_is_removed_snapshot_leaf()` scopes to `settings_snapshot`-rooted or bare names deliberately.
  A guard that cries wolf gets exempted, and an exempted guard is not a guard.

Both forks pass the guard against their real artifacts.

## No gate changed — proved by diff and positively

`git diff afff67b..HEAD -- tools/build_state_engine.py` contains **exactly one** line matching
any gate vocabulary, and it is **prose inside a docstring**, not code:

```
+    already guarded without consulting identity or time.  if_block("<group> Snapshot", 100)
```

Positively, all four gates are present and appear in the diff only as unchanged context:

```
:724  snapshot_g, snapshot_if = if_block("Brightness Snapshot", 100)   # container, condition 100
:727  capture_g,  capture_if  = if_block("Captured Brightness", 2, number=0)   # numeric capture
:780  snapshot_g, snapshot_if = if_block("Volume Snapshot", 100)
:783  capture_g,  capture_if  = if_block("Captured Volume", 2, number=0)
```

**CIRC-03 and CIRC-05 are empty as authored:** the has-any-value container gate and the numeric
capture gate are byte-identical to their pre-plan form in both primitives. **SAFE-03 is empty:**
the alert branch still runs when the device-details read returns nothing — the `otherwise(capture_g)`
arm carrying `alert("Dim", "Brightness could not be captured, so nothing was changed.")` and its
`silence()` twin are untouched. This plan deletes writes; it touched no gate and no branch.

The `save_state()` call plan 16-01 added is likewise intact in both applying arms.

## What was changed, by site

| Site | File | Change |
|---|---|---|
| (a) writes | `tools/build_state_engine.py::dimming`, `::silence` | two `set_value` calls removed from each capture arm — 4 generator calls, 44 rendered sites per fork |
| (b) seed | `tools/build_state_engine.py` `SNAPSHOT_SEED` | `("original_value", "changed_at", "changed_by_session_id")` → `("original_value",)`, both groups |
| (b′) recogniser | `tools/build_state_engine.py` | `SNAPSHOT_SEEDED_EMPTY` unchanged with its reason recorded; `SNAPSHOT_SEEDED_D02` added; `seed_settings_snapshot()` gains the second convergence pass |
| (c) assertion | `docs/phase5_self_check.py` | the two bare leaf names dropped; both dotted `original_value` keys and `cooldown_until` retained |
| (d) comment | `tools/build_state_engine.py::clear_snapshot` | docstring paragraph rewritten **in place** |
| (e) guard | `tools/build_state_engine.py`, `tools/build_sentient.py` | `verify_no_removed_snapshot_leaf_reads` + `_is_removed_snapshot_leaf` + `D02_REMOVED_SNAPSHOT_LEAVES`; registered in `main()` and in the Sentient import list and verify sequence |
| (f) record | `docs/BUILD-NOTES.md` §17 | appended, never rewritten |

### The superseded paragraph survives its own removal

`clear_snapshot()`'s docstring now records DEV-06 as **DECIDED 2026-08-18 as removal**, and
**quotes the retired paragraph verbatim inside its replacement** rather than deleting it, then
judges its three claims: `READ AT NONE` held and is exactly what licensed the removal; `20 sites`
was stale (44 measured); `deliberately left` is now false. The history of the deferral is worth
more than the space it costs.

`verify_state_seed()` needed no edit — its `wanted` set is derived from `SNAPSHOT_SEED`, so it
shrank on its own.

## Verification

| Check | Result |
|---|---|
| build provenance guard (`7ca8ebb` ancestor of HEAD) | exit 0, run before either generator |
| `python3 tools/build_state_engine.py` | exit 0 |
| `python3 tools/build_sentient.py` | exit 0, `b3f8b9cb…` |
| Task 1 artifact script, both forks | passed — 0 removed-leaf writes; container, both groups and both `original_value` leaves intact; neither name in the seed template |
| Task 2 script, both forks | passed — guard callable, registered in `main()`, passes on both artifacts |
| guard firing demonstration | passed — both surfaces raise `SystemExit`; negative control correctly silent |
| `python3 docs/phase5_self_check.py` | `phase5 self-check: passed` |
| `python3 docs/state_engine_self_check.py` | `negative_control: passed`, exit 0 |
| `python3 docs/phase9_self_check.py` | exit 0 — `site_audit: passed (30/30, 19 coerced, 11 correctly not)` |
| `python3 docs/environmental_restore_check.py` | `environmental restore check: passed` |
| **Gate A** `--target-macos 26 --target-platform all` | `Validation passed.` exit 0 on **both** forks |
| **Gate B** `--target-macos 27 --target-platform all` (advisory, chained into nothing) | exit 1 with **exactly the one permitted waived line** per fork — `WFCreateNoteInput` at index 4148 (Dumb) / 4216 (Sentient) |
| `python3 docs/manifest_check.py` | **RED as expected** (D-MANIFEST): `MANIFEST declares 2901248 bytes, src/PROSOCHE-Dumb.xml is 2854976 bytes`. No MANIFEST row edited. |
| build determinism | a third consecutive rebuild leaves both artifacts byte-identical (`e2da2742…` / `b3f8b9cb…`) |

Gate B was run separately and never `&&`-chained — it is permanently exit 1 and structurally
incapable of being a definition of done. Nothing outside the waiver was reported on either fork.

Task 2 is a pure assertion plus a record change, so **both fork artifacts are byte-identical
across it** — `git status` showed no `src/` modification after the task-2 rebuild.

## Threat mitigations applied

- **T-16-16 (critical, DoS — a dotted read of a removed leaf):** closed by
  `verify_no_removed_snapshot_leaf_reads`, on both forks, reusing the read-key index rather than
  a grep, and **demonstrated to fire** on an injected read of each surface.
- **T-16-17 (critical, tampering with the seed container):** the container, both group
  sub-dictionaries and both `original_value` leaves are asserted present in the rebuilt template
  by the task-1 script. Only leaves were removed.
- **T-16-18 (high, tampering with the gates):** proved by `git diff` — the only gate-vocabulary
  line in the whole plan's diff is docstring prose — and positively, by the four gates still
  standing unchanged.
- **T-16-19 (medium, repudiation — the stale §17 count):** corrected to the measured 44 with its
  derivation and a note that a larger delta means a regression rather than a recount, **appended**
  so the reservation history survives.
- **T-16-20 (medium, EoP — a smuggled ownership check):** none implemented. The prohibition was
  honoured, and the reason a naive field-equality check is the documented wrong answer is recorded
  in both `clear_snapshot()`'s docstring and §17.
- **T-16-21 (low, tampering with the convergence recogniser):** reasoned about separately from the
  seed, decided deliberately in both directions (one unchanged, one added), and recorded inline
  with the mechanism that makes the second necessary.
- **T-16-SC (low, accepted):** no external package installed. Python usage is stdlib only
  (`plistlib`, `pathlib`, `copy`, `inspect`, `json`, `sys`).

## Prohibitions honoured

- The `settings_snapshot` container and both group sub-dictionaries were **not** removed or
  altered; `original_value` remains seeded under each. Asserted positively, not assumed.
- **No ownership or field-equality check** was implemented.
- No seeded leaf was removed without first proving by a **static index of read keys** — not a grep
  — that nothing reads it. That proof is now permanent, not a one-time observation.
- D-02 was **not** re-opened or re-litigated. It is a LOCKED user decision; this plan implements it.
- No MANIFEST row was edited (D-MANIFEST).
- `STATE.md` and `ROADMAP.md` were not modified — this is a parallel worktree executor and the
  orchestrator owns those writes.

## Deviations from Plan

None. Both tasks executed exactly as written; no auto-fix rule was invoked and no architectural
question arose. No file outside the plan's declared six was modified.

The `GroupingIdentifier` collision that plan 16-01 armed **did not recur**, despite this plan
shifting the action count by −88. `verify_group_identifier_uniqueness` ran green on every build,
and gate A accepted both forks first time — 16-01's `stable_uid()` fix held, which is the first
independent test it has had.

## Authentication Gates

None.

## Known Stubs

None. No stub, placeholder, TODO, skipped test or unrun `<verify>` was introduced. Both task
verify blocks were run in full and passed.

## Device-gated work NOT done here (recorded, not inferred)

This plan is entirely rung-1 (file-level) work and claims nothing about hardware.

The plan's one `backstop` truth (SAFE-03, unclassified edge): **on a device that already holds a
`state.json` seeded with the removed leaves, the leaves persist harmlessly and no run reads them,
so no migration is required.** The static half is proven here — nothing reads them, permanently,
on both forks. The device half is a claim about a real file on a real phone and **only a device
session can confirm it**. It remains **BLOCKED on DIST-03**: paired device present,
`tunnelState: disconnected`, no live session to drive. Surfaced, not dismissed.

The reasoning that makes it low-risk is structural rather than observed: the removal deletes
writes and shrinks the seed; it adds no read, changes no gate, and leaves the container and both
`original_value` leaves in place — so an older, larger state file is a strict superset of what the
new build touches.

## Follow-up for later plans in this phase

- **16-05** owns the record half of D-01. §17 is now closed by this plan and is not 16-05's to
  edit; its ship-checklist items 4 and 5 are both resolved.
- **16-06** re-signs and refreshes the six MANIFEST rows. `docs/manifest_check.py` stays RED until
  then; do not fix it by editing rows. The `src/` artifacts are now **−88 actions** per fork
  relative to the signed archives, on top of 16-01's +44.
- Any future plan that wants an ownership or freshness field on a snapshot must add it as a **new**
  name and seed it — re-adding `changed_at` or `changed_by_session_id` will trip
  `verify_no_removed_snapshot_leaf_reads` the moment it is read, by design.

## Self-Check: PASSED

Files claimed modified, verified present on disk: `tools/build_state_engine.py`,
`tools/build_sentient.py`, `docs/phase5_self_check.py`, `docs/BUILD-NOTES.md`,
`src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml`.

Commits claimed, verified in `git log`: `3b0d368` (task 1), `e90a58a` (task 2). Neither commit
deleted a tracked file (`git diff --diff-filter=D` empty for both).

New symbols verified callable and registered by source inspection:
`verify_no_removed_snapshot_leaf_reads` (in `main()`, in `build_sentient.py`'s import list and
call sequence, passing on both built forks, demonstrated to raise `SystemExit` on an injected read
of each of its two surfaces), `_is_removed_snapshot_leaf`, `D02_REMOVED_SNAPSHOT_LEAVES`,
`SNAPSHOT_SEEDED_D02`.

Working tree clean after each commit.
