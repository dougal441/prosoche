---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
plan: 08
subsystem: generator / environmental primitives / distribution
tags: [reachability, dead-arm, capture-and-restore, build-guard, gap-closure, honesty-correction]
requires:
  - "11-07 (text.match output-name fix; both forks and MANIFEST at their post-11-07 state)"
provides:
  - "verify_environmental_reachability() -- a build guard making the dead-arm shape impossible in either builder, no exemption set"
  - "Reachable dimming()/silence() bodies: 44 environmental actions per fork moved out of a permanently-true gate's never-taken arm"
  - "A corrected T-11-*/T-16-* threat record: T-16-03 rescoped to the inner capture gate only, the outer gate reclassified under T-11-59"
  - "The execution claim corrected in MANIFEST.md and BUILD-NOTES.md section 18, per each file's own convention"
affects:
  - "tools/build_state_engine.py, tools/build_sentient.py"
  - "both shipped forks and both signed containers"
  - "docs/environmental_restore_check.py, docs/phase9_self_check.py (prose only)"
  - "docs/CAPABILITY-DECISIONS.md (BD-02/03-A1), docs/BUILD-NOTES.md section 18, artifacts/shortcuts/MANIFEST.md"
tech-stack:
  added: []
  patterns:
    - "Guard authored INERT, observed raising on the live defect, only then armed -- the 11-02 pattern, third use"
    - "A reachability guard tests the ARM, never the gate; correct-polarity analogs are then clean by construction rather than by exemption"
    - "Permanent truth DERIVED (existence gate over a settings_snapshot key nothing sentinel-writes), never assumed"
key-files:
  created: []
  modified:
    - "tools/build_state_engine.py"
    - "tools/build_sentient.py"
    - "src/PROSOCHE-Dumb.xml"
    - "src/PROSOCHE-Sentient.xml"
    - "docs/environmental_restore_check.py"
    - "docs/phase9_self_check.py"
    - "docs/BUILD-NOTES.md"
    - "docs/CAPABILITY-DECISIONS.md"
    - "artifacts/shortcuts/MANIFEST.md"
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut"
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut"
decisions:
  - "The gate fix landed in this build rather than being deferred to Phase 16 -- human-approved at the Task 2 checkpoint on the measured evidence"
  - "BD-02/03-A1 is a SEPARATE amendment from D-01's Supersession note: D-01 settled the floor VALUE, this settles the gate's REACHABILITY"
  - "ROADMAP.md's Phase 16 correction was NOT applied here -- the worktree contract forbids touching it; exact replacement text is handed to the orchestrator below"
metrics:
  duration: "~50 min"
  completed: "2026-08-18"
  tasks: 4
  commits: 3
  action-delta: "0 per fork (4304 Core / 4372 Aware, unchanged)"
status: complete
---

# Phase 11 Plan 08: The Dim/Silence Reachability Fix Summary

Two of the nine shipped interventions did nothing at all on device, and two later phases each
shipped believing otherwise — closed by re-gating the outer test onto the captured-original
leaf, and made unrepeatable by a build guard armed in both builders with no exemption set.

## What was wrong

`dimming()` and `silence()` opened on a `has any value` (condition 100) test over the
`settings_snapshot.<group>` **container**, with the entire capture-and-apply body — the device
read, the snapshot write, the environmental write, the `save_state()` Phase 16 had just placed
there, and even the *"could not be captured, so nothing was changed"* alert — in the arm taken
only when the container is **absent**.

`clear_snapshot()` writes the **leaf** and never the container. That is deliberate: it is what
keeps the bootstrap-seeded subtree a permanent invariant, and its own docstring says so. The
consequence is that the container is *always* present, the gate is *permanently true*, and the
body was **dead code**. A Circle configured to dim or quieten produced nothing: no change, no
state write, no alert, no error. Silent.

`restore_managed_settings()` opens on the **identical** container gate and is perfectly correct,
because its work sits in the **true** arm and its own numeric leaf gate decides inside it.
**Polarity, not the gate, was the entire defect** — which is why the new guard tests the arm and
never the gate.

## Evidence — measured against the shipped artifact, per fork

| measure | before | after |
|---|---:|---:|
| environmental actions in the never-taken arm | **44** | **0** |
| — `getdevicedetails` | 22 | 0 |
| — `setbrightness` | 11 | 0 |
| — `setvolume` | 11 | 0 |
| permanently-true `settings_snapshot` container gates | 30 | 8 (restore side only) |
| captured-original leaf gates at `WFCondition==2, WFNumberValue==0` | 8 | **30** |
| restore-side writes wrongly flagged | **0** | **0** |

44 is *every* Get Device Details in the artifact and every non-restore environmental write.
Both forks reported identical figures at every step.

## Tasks

| # | Task | Commit |
|---|---|---|
| 1 | Author the guard inert; prove it raises on the live defect | `b9bab04` |
| 2 | Blocking human checkpoint — approved | — |
| 3 | Re-gate both primitives on the leaf; arm the guard in both builders | `11c71fd` |
| 4 | Correct the claim everywhere; record the decision; re-sign | `5b944c6` |

## Task 1 — the guard's three proofs, run before anything was fixed

Verbatim, against the then-unfixed artifacts:

```
Dumb guard raised: an environmental read or write sits in the never-taken arm of a permanently-true settings_snapshot container gate -- ... : action 1019: is.workflow.actions.getdevicedetails; action 1033: is.workflow.actions.setvolume; action 1103: is.workflow.actions.getdevicedetails; action 1118: is.workflow.actions.setbrightness; action 1271: is.workflow.actions.getdevicedetails (44 total)

Sentient guard raised: ... action 1021: is.workflow.actions.getdevicedetails; action 1035: is.workflow.actions.setvolume; action 1171: is.workflow.actions.getdevicedetails; action 1186: is.workflow.actions.setbrightness; action 1339: is.workflow.actions.getdevicedetails (44 total)
```

1. **Raised on the live defect**: 44 per fork, 22/11/11.
2. **False-positive control**: the 8 `restore_managed_settings()` writes, located independently
   (writes fed by `Restore Brightness`/`Restore Volume`) at `[186, 205, 235, 254, 1577, 1596,
   4087, 4106]` (Core) and `[188, 207, 237, 256, 1645, 1664, 4155, 4174]` (Aware) — **none**
   named by the guard, on either fork.
3. **Second false-positive control**: `verify_capture_persistence()` clean on both forks,
   establishing the baseline Task 3 diffs against.

**Inertness proved by containment, with a control**: `inspect.getsource(main)` reported
`verify_environmental_reachability` **absent** and `verify_dispatch_coverage` **present** — the
second half is what shows the assertion can distinguish the two states. `grep -c` on
`build_sentient.py` returned `0`. Both builders rebuilt and left `git status --short src/`
**empty**: authoring an uncalled function changed no artifact byte.

## Task 3 — the fix, and the negative control that proves the armed guard fails closed

Both capture sites now read `settings_snapshot.<group>.original_value` and gate it on numeric
`> 0` — the shape `restore_managed_settings()` already used, so capture and restore finally
agree on what counts as a real outstanding original. The shape is forced by device-measured
coercion rather than chosen for symmetry: `"null"` and `""` **both** coerce to a false `> 0`
test (Donor 6.1 test 2, Donor 6 action 8), while a code-5 string test closes the sentinel case
and leaves the empty case open.

The bodies are otherwise untouched — `capture_g`, the already-dim/already-quiet comparisons, the
snapshot write, Phase 16's `save_state()` placement, the environmental write and the fallback
alert are all exactly as written.

**Negative control, run and recorded.** Reverting *only* `dimming()`'s outer gate to the
container form and running the armed builder:

```
an environmental read or write sits in the never-taken arm of a permanently-true settings_snapshot container gate -- ... (22 total)
EXIT CODE: 1
```

22 = exactly `dimming()`'s half of the 44. Restored, build exits **0**.

**Compatibility with Phase 16, proved rather than assumed.** `verify_capture_persistence()`
reports **0 offenders on both rebuilt forks**. The re-gate changes which arm the capture write
and its apply sit in *relative to each other* not at all — both remain inside the same arm,
only the gate enclosing both of them changed.

## Every number re-measured, none reconciled

| measure | Core | Aware |
|---|---|---|
| `verify_environmental_reachability` | 0 offenders | 0 offenders |
| `verify_capture_persistence` | 0 offenders | 0 offenders |
| captured-original leaf gates, all `WFCondition==2 / WFNumberValue==0` | 30 | 30 |
| setbrightness / setvolume / getdevicedetails | 15 / 15 / 22 | 15 / 15 / 22 |
| coercion split | 15 of 15, 4 of 15 | 15 of 15, 4 of 15 |
| action total | 4304 | 4372 |
| Emergency Restore surfaces / enclosed | 4 / **0** | 4 / **0** |
| gate A (`--target-macos 26 --target-platform all`) | `Validation passed.` | `Validation passed.` |
| AEA1 decrypt-verify vs source | `== True` | `== True` |

`git diff --numstat` on both checker files: **35/0 and 34/0** — purely additive prose, so no
numeric literal could have changed. The stillness of 15/15/22 is itself the evidence that the
fix re-gates existing actions and emits none.

**Emergency Restore enclosure** was re-derived two ways. A narrow derivation (gates whose tested
variable resolves via `_read_variable_keys()` to `panic_escape_enabled`) found 3 gated groups; a
broadened one (adding gates merely *named* like a Panic Escape variable — broadening can only
add groups, so a 0-enclosed result strictly dominates) found **5**, reproducing
`11-VERIFICATION.md` item 12 exactly. Both report **4 surfaces, 0 enclosed**, per fork.

**Builders byte-idempotent**: two consecutive full rebuilds produced identical SHA-256 on both
forks and left `git status --short src/` empty.

**Gate B was never invoked** — advisory, permanently waivered, and it appears in no command in
this plan.

## Deviations from Plan

### 1. [Rule 3 — worktree contract vs. plan] `.planning/ROADMAP.md` was NOT edited; the exact edit is handed off

- **Found during:** Task 4
- **Issue:** Task 4 requires a scoped edit correcting ROADMAP.md Phase 16's "the merge made them
  live", with acceptance `grep -c 'the merge made them live' == 0`. The worktree contract states
  twice — in the original objective and again in the checkpoint-resolution message — **do NOT
  touch STATE.md or ROADMAP.md**, because the orchestrator owns those writes after the wave.
- **Resolution:** The contract wins; a worktree agent editing a shared orchestrator artifact
  risks the merge. `grep -c 'the merge made them live' .planning/ROADMAP.md` therefore still
  returns **1** and that acceptance criterion is **NOT met by this plan**.
- **Handoff — the exact edit, at `.planning/ROADMAP.md:768-772`.** Current text:

  > **But they have never run on a phone, and the merge made them live** — before the coercion
  > fix these actions silently no-opped; now they actually change brightness and volume, and the
  > code that puts them back has never once executed on hardware.

  Replacement:

  > **But they have never run on a phone, and the merge did NOT make them live** — the coercion
  > fix was necessary and not sufficient. Both bodies sat in the never-taken arm of a
  > permanently-true `settings_snapshot` container gate and were unreachable until plan 11-08,
  > independently of and prior to Phase 16's own persistence fix; 44 environmental actions per
  > fork could not run. They are reachable now, and the code that puts them back has still never
  > once executed on hardware.

  Leave Phase 16's deliverables, requirement list and brightness-floor paragraph untouched.

### 2. [Rule 2 — anti-recurrence] The new guard added to `REQUIRED_SYMBOLS`

- **Found during:** Task 3
- **Issue:** `docs/environmental_restore_check.py` exists to make the cancelled cut of these
  primitives fail loudly, and its `REQUIRED_SYMBOLS` already lists `verify_restore_gates` and
  (added by Phase 16) `verify_capture_persistence`. The new guard was not listed, so a future
  subtractive pass could delete it silently with every count in that file still green.
- **Fix:** `verify_environmental_reachability` added to `REQUIRED_SYMBOLS`, with a comment
  naming why its absence is the one of the three that is invisible at runtime. Same move Phase
  16 made for its own guard.
- **Commit:** `11c71fd`

### 3. [Rule 1 — stale plan baseline] Action totals were 4304/4372, not the plan's 4302/4370

- **Found during:** Task 1
- **Issue:** The plan's `<measured_baseline>` was taken at HEAD `e6b96e3`, before plan 11-07
  landed, and states 4302 Core / 4370 Aware. Measured at this plan's actual base: **4304 /
  4372**.
- **Cause:** 11-07's `text.match` consumption fix, +2 `getitemfromlist` per fork. It predates
  this plan and is recorded in 11-07's own SUMMARY.
- **Resolution:** Surfaced at the checkpoint before approval rather than absorbed silently.
  Task 3's "totals unchanged" criterion was read against 4304/4372 and **held exactly** —
  11-08 itself moved them by zero. `docs/phase9_self_check.py`'s stale-totals paragraph, which
  explicitly predicts its own staleness and declares itself a dated measurement, was left
  unedited and a fresh dated measurement appended beside it.

### 4. [Rule 2 — false claim in scope] The MANIFEST's retracted "could not be installed" line

- **Found during:** Task 4
- **Issue:** The MANIFEST's 11-07 top block still asserts the probe "could not be installed" and
  the consumption shape is "recorded OPEN". Both were retracted the same day in 11-07's SUMMARY
  and `docs/BUILD-NOTES.md` §31, but the MANIFEST was not updated.
- **Fix:** Corrected in the new prepended block as one of three named older claims, rather than
  edited in place — the file's own convention retains earlier blocks as historical record.
  Writing a block about honesty above a live false claim would have been its own defect.
- **Commit:** `5b944c6`

## Threat record reconciliation

| Threat | Disposition |
|---|---|
| **T-11-59** (DoS — the reachability defect) | **CLOSED.** Guard armed in both builders, no exemption; raised on 44, silent on the 8, fails closed on revert |
| **T-11-60** (repudiation — Phase 16's record) | **CLOSED.** BD-02/03-A1 names T-16-03's mischaracterisation explicitly rather than editing around it |
| **T-11-42** (capture empty, apply anyway) | Unchanged — `capture_g` untouched, degrade-to-message-only alert intact |
| **T-11-45** (distributable asserting a capability it lacks) | **CLOSED** in MANIFEST and BUILD-NOTES; **PARTIAL** in ROADMAP — see Deviation 1 |
| **T-11-46** (Emergency Restore weakened) | Re-measured 4/0 per fork. Still a measurement, not a guard — `verify_panic_escape_isolation()` is plan 11-10 |
| **T-16-01** (persistence ordering) | Unmodified and re-verified clean. Distinct from T-11-59 |
| **T-16-03** (the two gates) | **SCOPE CORRECTED.** Only `capture_g` is input validation; `snapshot_g` reclassified under T-11-59 |

## Known Stubs

None.

## Device verification

**Nothing in this plan is device-verified, and nothing claims to be.** Reachable is a structural
property established at rung 1 (file-level analysis) and nothing higher. Specifically NOT
claimed: that `Get Device Details` returns a real correctly-typed value on hardware; that the
original is restored exactly on CLOSE; that force-quit, restart, missed CLOSE, overlapping
sessions or lock-screen restore or leave a safe value; that Emergency Restore has ever been
tapped on a phone.

The device proof remains **Phase 16 / DIST-03 / `16-UAT.md`'s twelve tests**, none of which has
ever run. What this plan changes is **what that UAT will be testing** — a live loop rather than
a dead one — and **nothing about its outcome**. Had those twelve tests been run before this fix,
they would have observed nothing happening and could have been read as passing.

## Self-Check: PASSED

- `tools/build_state_engine.py` — FOUND (guard authored, both primitives re-gated, guard armed)
- `tools/build_sentient.py` — FOUND (import + armed call with per-fork justification)
- `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` — FOUND (rebuilt, byte-idempotent)
- `docs/environmental_restore_check.py` — FOUND (+35/−0, prose + `REQUIRED_SYMBOLS`)
- `docs/phase9_self_check.py` — FOUND (+34/−0, prose only)
- `docs/CAPABILITY-DECISIONS.md` — FOUND (+128/−0, `BD-02/03-A1` at line 1085, distinct from D-01's note at line 67)
- `docs/BUILD-NOTES.md` — FOUND (§18 addendum; `DIST-03` count 12 → 13)
- `artifacts/shortcuts/MANIFEST.md` — FOUND (block prepended, six rows recomputed from disk)
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — FOUND, 231148 bytes
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — FOUND, 235592 bytes
- Commit `b9bab04` — FOUND
- Commit `11c71fd` — FOUND
- Commit `5b944c6` — FOUND
- All thirteen structural checkers exit 0, `manifest_check` included
