---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
plan: 10
subsystem: build guards / structural checkers / recording duty
tags: [guard-repair, provenance-resolution, t-11-22, critical-threat, measured-floor, interim-record, gap-closure]
requires:
  - "11-09 (both forks and MANIFEST at their post-11-09 state; Core 4304 / Aware 4438)"
provides:
  - "verify_panic_escape_seed() assertion (3) resolved by PROVENANCE, covering 3 gates per fork instead of 1, with a non-empty guarded-set assertion"
  - "_panic_escape_variables() -- the shared provenance resolver both Panic Escape guards use, so no guard names a variable"
  - "verify_panic_escape_isolation() -- the standing executable guard for T-11-22, armed in BOTH builders, replacing a MANIFEST hand-measurement"
  - "MINIMUM_TOKEN_STRINGS moved 775 -> 1104 (the measured lower of the two forks) with a house-style derivation"
  - "docs/BUILD-NOTES.md 34 and 35 -- both interim stand-ins recorded where the 11-02 prohibition requires, and WR-03 recorded as already closed by Phase 16"
affects:
  - "tools/build_state_engine.py, tools/build_sentient.py"
  - "docs/note_identity_check.py, docs/environmental_restore_check.py"
  - "docs/BUILD-NOTES.md, artifacts/shortcuts/MANIFEST.md"
  - "NEITHER shipped fork -- no emitted action changed, both byte-identical to the 11-09 build"
tech-stack:
  added: []
  patterns:
    - "A guard resolves its targets through the SHARED CONSTANT they are read from, never through an emitted name -- a name is not a contract"
    - "Every provenance-resolved guard asserts its resolved set is NON-EMPTY, so a disconnection fails the build instead of passing clean"
    - "A safety guard fails in BOTH directions: when the invariant is violated AND when the thing it protects has disappeared"
    - "A measured floor is set from a measurement taken in the SAME SESSION as the edit, and carries its derivation beside it"
key-files:
  created: []
  modified:
    - "tools/build_state_engine.py"
    - "tools/build_sentient.py"
    - "docs/note_identity_check.py"
    - "docs/environmental_restore_check.py"
    - "docs/BUILD-NOTES.md"
    - "artifacts/shortcuts/MANIFEST.md"
decisions:
  - "docs/phase5_self_check.py deliberately NOT edited -- Phase 16 (16-02/16-03) already closed WR-03 with a better-evidenced fix; the finding is recorded as closed rather than re-fixed"
  - "The 11-02 prohibition was DISCHARGED as written, never amended to accept src/CONFIG-BLOCK.md as a satisfying location"
  - "verify_panic_escape_isolation uses FULL enclosure, not true-arm-only -- the opposite choice from verify_environmental_reachability, because this defect is enclosure of any kind rather than a polarity error"
  - "verify_panic_escape_isolation added to environmental_restore_check.py's REQUIRED_SYMBOLS (Rule 2 deviation) -- same anti-deletion move 11-08 made for its own guard"
metrics:
  duration: "~55 min"
  completed: "2026-08-18"
  tasks: 3
  commits: 3
  action-delta: "0 per fork (Core 4304 / Aware 4438, unchanged; both forks byte-identical to 11-09)"
status: complete
---

# Phase 11 Plan 10: The Guard That Could Not Fail Summary

A build guard that passed under exactly the drift it existed to catch is now resolved by
provenance and covers all three gates instead of one; the phase's only `critical` threat
traded a prose hand-measurement for an executable guard armed in both builders; and a floor
sitting a third below its own measurement was raised to it — six negative controls, no
emitted action changed.

## What was wrong

Three guard defects, each of a different kind.

**1. A guard resolved by a name that was not a contract.** `verify_panic_escape_seed()`'s third
assertion matched the bare literal `"Panic Escape Enabled"`. `universal_leaving()` carried its
**own copy** of that string forty lines away; the two shared no constant. Rename the emitter and
the guard inspects a name nothing emits — and reports success.

It was also **incomplete**. The literal named **one** of **three** mode-0 gates over the flag.
The two it missed are `panic_escape_branch()`'s `still_on_g` and `stored_off_g`, which decide
whether the flag is **written** — strictly the worse pair, because an existence test there writes
the bypass flag on a run where the user changed nothing, in either direction.

**2. The phase's only `critical` had no checker.** T-11-22 — Emergency Restore must never be
enclosed by a Panic Escape conditional — was verified by a hand-measurement in `MANIFEST.md`
prose. Correct when taken, and not re-run by the next change to `universal_leaving()` or
`panic_escape_branch()`. Plan **11-08**, in this same set, made the stranding state materially
more reachable: before it both `dimming()` and `silence()` sat in a dead arm, so no intervention
could actually dim a screen or quieten a device and there was nothing to be stranded *by*.

**3. A floor with no teeth.** `MINIMUM_TOKEN_STRINGS` was **775**, measured at the phase-11
baseline `ae0226c` and never revised while the artifacts grew past it — 329 units of slack
against the live measurement, so the check named parameter-defect axis 2 while tolerating roughly
a third of every token string in the artifact being flattened to a bare attachment.

## Tasks

| # | Task | Commit |
|---|---|---|
| 1 | Resolve the gate guard by provenance; give T-11-22 a standing guard | `ccc5acb` |
| 2 | Move the token-string floor from decorative to measured | `9cca1ff` |
| 3 | Record both interims where the prohibition requires; close the wave | `4c3e838` |

## Task 1 — provenance resolution, and the control that defeated the old guard

`_panic_escape_variables()` is the new shared resolver: every named variable whose
`_read_variable_keys()` provenance contains `PANIC_ESCAPE_KEY`. Both Panic Escape guards call it,
and **neither guard names a variable anywhere**. `grep -c '"Panic Escape Enabled"'` on the
generator went **3 → 2** — the two survivors are the emitter's own, and the deleted third was the
guard's copy. The deletion *is* the fix.

### Measured, per fork, before and after (identical on both)

| measure | Core | Aware |
|---|---:|---:|
| variables resolving to `panic_escape_enabled` by provenance | 2 | 2 |
| — the two names | `Panic Escape Enabled`, `Panic Escape Stored` | same |
| mode-0 gates over them, **all at condition 2** | **3** | **3** |
| gates the OLD name-literal guard inspected | **1** | **1** |
| Panic-Escape grouping identifiers | 3 | 3 |
| Emergency Restore surfaces (2 `WFMenuItems`, 2 case titles) | **4** | **4** |
| **enclosed** | **0** | **0** |

The 4/0 figures reproduce `11-VERIFICATION.md` item 12's independent measurement exactly, so the
new guard pins a state that was measured elsewhere rather than whatever the artifact happens to be.

### The negative controls — five for Task 1, all in an isolated sandbox tree

Every control ran in a scratch tree with its own `tools/`, `src/`, `docs/` and `artifacts/`, so
the repo's artifacts were never at risk. Verbatim outcomes:

**Control 0 — the pre-fix observation, both halves.** Rename only the emitter's variable
throughout `universal_leaving()` and flip its gate to condition 100, leaving the guard's literal
untouched, against the generator at `e5d3bab`:

```
pre-fix builder on the mutated generator: exit 0
message: (none)
artifact rewritten: True  sha256 947c5d8ae49f997b

  PASS state_engine_self_check   PASS phase5_self_check    PASS phase6_self_check
  PASS phase7_self_check         PASS phase9_self_check    PASS environmental_restore_check
  PASS router_ui_census          PASS sequence_dispatch_check   PASS note_identity_check
--- 9/9 green on the defective artifact
```

A defective build, silently produced, certified green by every checker that could see it. That is
the finding, and it reproduces the original review's exactly.

**Controls 1–3 — the repaired guard.** All exit **1**; the artifact is left **unchanged** in each
(every `verify_*` call runs before the single `SOURCE.write_bytes`, so a raising guard never
ships):

| control | exit | message (opening) |
|---|---:|---|
| emitter rename + existence gate | 1 | `... action 529: 'Panic Escape Bypass' at condition 100 ...` |
| orphaning — every read of the key removed | 1 | `no variable in the artifact resolves to 'panic_escape_enabled' by provenance ...` |
| stored-flag gate flipped to existence | 1 | `... action 4248: 'Panic Escape Stored' at condition 100 ...` |
| restore control — unmutated | **0** | (clean) |

Control 1's message names the **renamed** variable: the guard found it through the key, which is
precisely what makes the rename survivable. Control 3 exercises a site the previous guard could
not see at all — a new capability, not a re-demonstration.

**One Panic-Escape-adjacent gate is deliberately outside the set, as the plan anticipated.**
`Manual Panic Escape Requested` gates `panic_escape_branch()`'s outer block but is set from a
**menu selection**, never read from the Panic Escape state key, so it has no provenance here. Its
exclusion is safe: it is already numeric (`if_block(..., 2, number=0)`), and adding it back by a
bare name literal would reintroduce exactly the coupling this rewrite removes.

### `verify_panic_escape_isolation()` — T-11-22 given a standing guard

Armed in **both** builders. It resolves the Panic-Escape grouping identifiers from the same
provenance set, locates every Emergency Restore surface via `enclosing_groups()`, and asserts in
**both** directions. Two negative controls, both run:

| control | exit | outcome |
|---|---:|---|
| A. one surface **enclosed** by a Panic Escape conditional | 1 | names **both** the `WFMenuItems` declaration (action 177) and the case title (action 180), inside the synthetic group, with the stranding consequence spelled out |
| B. **every** surface removed | 1 | `no 'Emergency Restore' menu surface exists anywhere in the artifact -- SAFE-05's safety hatch has been removed ...` |
| restore control | **0** | clean |

Control A catching both surface kinds matters: hiding the row removes the tap target, enclosing
the case makes the tap do nothing. Control B is the direction a naive guard gets wrong — a guard
that reports clean when the safety hatch is gone converts a removal into a green build.

The guard uses **full** enclosure, not true-arm-only — the opposite choice from
`verify_environmental_reachability()`, which tests the arm because *its* defect is a polarity
error. Here the defect is enclosure of any kind: a surface in either arm is unreachable to the
users in the other one.

## Task 2 — the floor, and the slack that was the point

Re-measured with `check_offsets()`'s **own** walk, in the same session as the edit, so the
constant and the check cannot disagree about what is being counted:

| fork | count |
|---|---:|
| `src/PROSOCHE-Dumb.xml` (Core) | **1104** |
| `src/PROSOCHE-Sentient.xml` (Aware) | **1112** |

Floor set to the **lower** of the two, `1104`, so one constant serves both forks. Aware forks the
built Core source and only ever adds, so Core is the lower bound by construction — but both were
measured, never inferred. The derivation is written beside the constant in
`environmental_restore_check.py`'s `EXPECTED_SITES` house style.

**Control, on a scratch copy of the Core artifact.** Flatten exactly **one** token string to a
bare `WFTextTokenAttachment`, dropping the count to 1103:

```
NEW floor (1104)  exit 1: Dumb: only 1103 WFTextTokenString values found, below the measured floor
OLD floor  (775)  exit 0: ... 1112 token strings, 0 attachment-offset mismatches
```

The old floor passes the identical mutation, and would have passed 329 of them. That gap is what
the control exists to show.

**`docs/phase5_self_check.py` was read and not edited.** `git diff --stat -- docs/phase5_self_check.py`
is **empty for the whole plan**. Confirmed by reading `:107-151`: the assertion tests
`"WFBrightness" in params` — operand **presence**, not a numeric band — with a comment naming
PHASE 16 (plan 16-03) and citing **CAP-08**'s simulator-measured finding that an absent
`WFBrightness` silently applies an unrequested 50% rather than raising. The review's WR-03 is
closed by a different phase for a different and better reason; touching it again would be
guard-for-guard's-sake churn.

## Task 3 — the record where the prohibition asked for it

Plan 11-02's prohibition requires both interims named in the generator's comment text **and in
`docs/BUILD-NOTES.md`**, each with its replacing phase. Measured before this edit:
`grep -c 'Eject' docs/BUILD-NOTES.md` = **0**; `Loud Mirror` = **1**, and that one occurrence was
a count inside an evidence table, not an interim record.

**Discharged as written, never amended** — `git diff --numstat -- .../11-02-PLAN.md` is empty.

| criterion | before | after |
|---|---:|---:|
| `grep -c 'Eject' docs/BUILD-NOTES.md` | 0 | **8** |
| `grep -c 'Loud Mirror' docs/BUILD-NOTES.md` | 1 | **5** |
| `grep -c 'CAP-08' docs/BUILD-NOTES.md` | 11 | **12** |
| `CONFIG-BLOCK.md` / `primitive_dispatch` cross-references present | — | yes / yes |

Section **34** records each interim with what ships, what BD-06 specifies, why the stand-in exists
rather than nothing, and what the replacing phase changes **concretely** — Phase 15 decides the
`voice_enabled = 0` semantics, emits a real Voice branch and resolves the `Spoken This Run` guard;
**Phase 17 flips exactly two cells**, `Classic[5]` and `Ambient[5]`, `Eject` → `Redirect`
(`BlackMirror[5]` is already correct). A table names all three record locations for each interim
so a reader can reach any from any other. The same section records WR-03 as already closed by
Phase 16. Section **35** records this plan's own work and closes with what it does not establish.

**MANIFEST.md** carries a wave-closing block that adds **no hash row**, because no hash moved.
That is a measurement, not an expectation: `git status --short -- src/` empty after a full
rebuild of both forks, the Aware source re-serialising to the same SHA-256 `c52edd93…`, and
`manifest_check.py` green **with no exception**.

## Every number re-measured, none reconciled

| measure | Core | Aware |
|---|---|---|
| action total | 4304 | **4438** |
| `src/` after full rebuild | byte-identical to 11-09 | byte-identical to 11-09 |
| Aware source SHA-256 | — | `c52edd93…` (unchanged) |
| gate A (`--target-macos 26 --target-platform all`) | `Validation passed.` | `Validation passed.` |
| thirteen structural checkers | 13/13 green | 13/13 green |

Gate B was **never invoked** — advisory, permanently waivered, and it appears in no command in
this plan.

## Deviations from Plan

### 1. [Rule 1 — stale plan baseline] Aware's action total is 4438, not the 4372 the dispatch prompt carried

- **Found during:** Task 1 baseline measurement.
- **Issue:** The dispatch context stated action totals of **4304 Core / 4372 Aware** and warned
  that plans written before wave 7 say 4302/4370. Measured at this plan's actual base
  (`e5d3bab`): **4304 / 4438**. Core matches; **Aware is +66**.
- **Cause:** Plan **11-09**'s second Use Model contract audit block, which its own SUMMARY records
  as `Aware 4372 -> 4438 (+66, one audit block); Core 4304 unchanged`. It predates this plan
  entirely.
- **Resolution:** Surfaced rather than absorbed. No criterion in this plan pins an action total,
  and this plan moved both by **zero**. The token-string counts show the same drift and were
  handled the same way: the plan's `<measured_baseline>` predicted 1104/1108, and Aware measured
  **1112** for the same reason. The floor was set from the fresh measurement, exactly as the plan
  instructed, never from the baseline line.

### 2. [Rule 2 — anti-recurrence] `verify_panic_escape_isolation` added to `REQUIRED_SYMBOLS`

- **Found during:** Task 1.
- **Issue:** `docs/environmental_restore_check.py` exists to make a re-attempted cut of the
  environmental primitives fail loudly, and its `REQUIRED_SYMBOLS` already lists
  `verify_restore_gates`, `verify_capture_persistence` and (added by 11-08)
  `verify_environmental_reachability`. The new isolation guard was not listed, so a future
  subtractive pass could delete the phase's only `critical`-threat guard with every count in that
  file still green — and its absence is invisible at runtime.
- **Why that file is the right home:** its own docstring names **SAFE-05** — Emergency Restore —
  as one of the two requirements the cancelled cut would have broken, and Emergency Restore is
  only a safety mechanism while a user can reach it. The stranding scenario is precisely a dimmed
  screen or a silenced device.
- **Fix:** One tuple entry plus a comment naming why. It changes no artifact and no count.
- **Commit:** `ccc5acb`

### 3. [scope, no action taken] The pre-existing duplicate action `UUID` was not touched

- `792D1640-FEB7-5FAF-AD6D-0E66CC1A1075` is carried by two actions on **both** forks. It is
  documented in full in `deferred-items.md`, is pre-existing at HEAD `224e68a8`, and is owned by a
  separate task. This plan did not cause it and did not fix it. Relevant only as a caution already
  recorded there: `verify_group_identifier_uniqueness()` covers `GroupingIdentifier`s and gate A
  checks no UUID uniqueness at all. The new isolation guard operates on `GroupingIdentifier`s, not
  action UUIDs, so it neither depends on nor is affected by that gap.

## Threat record reconciliation

| Threat | Disposition |
|---|---|
| **T-11-53** (tampering — the vacuous gate assertion) | **CLOSED.** Resolved by provenance; demonstrated failing on the exact drift that defeated its predecessor, with the pre-fix pass recorded beside it |
| **T-11-54** (EoP — the two uncovered stored-flag gates) | **CLOSED.** Covered by the same provenance set; demonstrated failing at action 4248, a site the previous guard could not see |
| **T-11-58** (EoP — Emergency Restore enclosed, T-11-22 recurrence) | **CLOSED as a structural property.** `verify_panic_escape_isolation()` armed in both builders, both negative controls run, no-surface-found branch included. Device behaviour remains unproven — see below |
| **T-11-55** (tampering — axis-2 token-string regression) | **CLOSED.** Floor at the measured value; the old floor demonstrably passes the mutation the new one catches |
| **T-11-57** (repudiation — interims readable as designed behaviour) | **CLOSED.** Recorded in the required file with replacing phases and three-way cross-references; the prohibition is unamended |
| **T-11-SC** (package-manager installs) | **N/A, as planned.** No dependency added, no install run, nothing for the legitimacy gate to audit |
| **T-11-46** (Emergency Restore weakened) | 11-08 left this as "still a measurement, not a guard — `verify_panic_escape_isolation()` is plan 11-10". **It is now a guard.** |

## Known Stubs

None.

## Device verification

**Nothing in this plan is device-verified, and nothing claims to be.** Every result is rung 1 —
file-level analysis of the generator and the built artifact — and nothing higher was attempted.

**Six negative controls fired in this plan. Each is proof about a guard, not about the device.**
A build-time assertion catching a mutation deliberately introduced to defeat it says nothing
about what the shipped Shortcut does on a phone.

Specifically **not** claimed: that Emergency Restore is reachable at run time; that its menu case
fires; that `restore_managed_settings()` restores the captured originals; that Emergency Restore
has **ever been tapped on a phone** — it has not; that Panic Escape's removal or restoration path
has ever run; that `Get Device Details` returns a real correctly-typed value on hardware.

`DIST-03` is **open** and nothing here narrows it. The device proof for the capture-and-restore
loop these guards protect remains Phase 16 / `16-UAT.md`'s twelve tests, none of which has ever
run.

## Worktree contract

No shared orchestrator artifact was modified. `.planning/STATE.md` and `.planning/ROADMAP.md` are
untouched by all three commits, and this plan had no acceptance criterion requiring an edit to
either — so, unlike 11-08's Deviation 1, there is **no handoff for the orchestrator to apply**.

## Self-Check: PASSED

- `tools/build_state_engine.py` — FOUND (`_panic_escape_variables`, repaired assertion (3),
  non-empty assertion, `verify_panic_escape_isolation` + helpers, armed in `main()`)
- `tools/build_sentient.py` — FOUND (import + armed call with per-fork justification)
- `docs/note_identity_check.py` — FOUND (`MINIMUM_TOKEN_STRINGS = 1104` with derivation;
  `grep -c 'MINIMUM_TOKEN_STRINGS = 775'` returns 0)
- `docs/environmental_restore_check.py` — FOUND (`verify_panic_escape_isolation` in
  `REQUIRED_SYMBOLS`)
- `docs/BUILD-NOTES.md` — FOUND (sections 34 and 35 appended, +267 lines)
- `artifacts/shortcuts/MANIFEST.md` — FOUND (wave-closing block prepended, no hash row added)
- `docs/phase5_self_check.py` — CONFIRMED UNTOUCHED (`git diff --stat` empty)
- `.planning/phases/11-.../11-02-PLAN.md` — CONFIRMED UNTOUCHED (`git diff --numstat` empty)
- `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` — byte-identical to the 11-09 build after
  a full rebuild
- Commit `ccc5acb` — FOUND
- Commit `9cca1ff` — FOUND
- Commit `4c3e838` — FOUND
- All thirteen structural checkers exit 0, `manifest_check` included; gate A passes on both forks
