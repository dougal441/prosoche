---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
plan: 09
subsystem: sentient fork / build guards / distribution
tags: [fork-identity, grouping-identifier-collision, derived-counts, gap-closure, wr-10, wr-11]
requires:
  - "11-08 (both forks and MANIFEST at their post-11-08 state; Core 4304 / Aware 4372)"
provides:
  - "One Use Model contract audit per OPEN-arm dispatch rendering, so removing the Panic Escape bypass no longer turns the Aware fork into Core"
  - "audit_block(ordinal) -- a per-rendering discriminator threaded through EVERY uid() call AND every if_block() key via a single aid() chokepoint"
  - "Structural OPEN-arm insertion derived from the router's own OPEN test, so a future rendering inside that arm is covered with no code change"
  - "Both Aware checkers derive the audit count from the Core fork and inspect every block"
  - "verify_circle_zero_silence + verify_parameter_keys armed on the Aware chain (WR-10)"
  - "Content-anchored import splice and ActionIndex, replacing two hard-coded integers (WR-11)"
affects:
  - "tools/build_sentient.py, src/PROSOCHE-Sentient.xml"
  - "docs/sentient_core_check.py, docs/sentient_audit_check.py"
  - "the signed Aware container and artifacts/shortcuts/MANIFEST.md"
  - "docs/BUILD-NOTES.md (new section 33)"
tech-stack:
  added: []
  patterns:
    - "A discriminator reaches identifiers through ONE nested chokepoint, so a missed call site is unrepresentable rather than merely unlikely"
    - "A checker DERIVES its expected count from the other fork rather than pinning a literal -- a literal is what let this checker agree with the defect"
    - "Every negative control run against the RETIRED checker as well as the new one, so 'it was invisible before' is an observation, not a claim"
    - "An anchor is resolved by content in the builder AND in the checker, so the two agree by construction rather than by both naming the same integer"
key-files:
  created: []
  modified:
    - "tools/build_sentient.py"
    - "src/PROSOCHE-Sentient.xml"
    - "docs/sentient_core_check.py"
    - "docs/sentient_audit_check.py"
    - "docs/BUILD-NOTES.md"
    - "artifacts/shortcuts/MANIFEST.md"
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut"
decisions:
  - "Insert into EVERY OPEN-arm rendering; recording 'audit only the Panic-Escape-enabled path' as a product decision was considered and explicitly REJECTED"
  - "Scope the insertion to the structurally derived OPEN arm, excluding the nine Test-a-Circle MANUAL-arm markers by construction rather than by index"
  - "The Core container was NOT re-signed -- verified by decrypt-comparison rather than assumed, since this plan touches build_sentient.py only"
  - "The pre-existing duplicate action UUID found by criterion 3 was NOT fixed -- it is in the Dumb builder, affects both forks, and is logged to deferred-items.md"
metrics:
  duration: "~50 min"
  completed: "2026-08-18"
  tasks: 3
  commits: 3
  action-delta: "Aware 4372 -> 4438 (+66, one audit block); Core 4304 unchanged"
status: complete
---

# Phase 11 Plan 09: One Contract Audit Per OPEN-Arm Rendering Summary

The Aware fork exists for one reason, and an unrelated setting deleted it — closed by inserting
the audit at every structurally derived OPEN-arm rendering, discriminating both identifier
routes through one chokepoint, and replacing two literal counts with counts derived from the
Core fork.

## What was wrong

`build_sentient.py` inserted the Use Model contract audit at the **first** contract marker in
document order and then `break`-ed. Before Build Addendum 01 "first marker" and "the OPEN-arm
marker" were the same action. Plan 11-05 added a **second** OPEN-arm dispatch rendering —
`universal_leaving()`'s otherwise arm, taken when the user has **removed the Panic Escape
bypass** — and the audit did not follow it there.

So a user who removed that bypass reached the Intention primitive with **no contract audit at
all**, on every open, with nothing observable on device to say so. Their install still presented
as Aware — its own name, icon, Note and `"fork": "Aware"` state seed — and simply *was* Core on
that path. Two features with no relationship to each other were coupled, and the coupling
removed the audit from the **harder** path, where it is most useful.

`docs/sentient_core_check.py:103` asserted the model count as a literal `1` — the count the
**missing** audit produces — so the checker **agreed with the defect** rather than reporting it,
and went on doing so across the three phases (12, 13, 16) that executed after the review named it.

## Evidence — measured against this plan's own base, never transcribed

| measure | Core | Aware before | Aware after |
|---|---:|---:|---:|
| actions | 4304 | 4372 | **4438** |
| contract markers, whole artifact | 11 | 11 | 11 |
| — **inside the OPEN arm** | **2** | **2** | **2** |
| — in the MANUAL Test-a-Circle submenu | 9 | 9 | 9 |
| `is.workflow.actions.askllm` | 0 | **1** | **2** |
| audit spans | — | 1 | **2**, disjoint |

The plan predicted 4302/4370; the real base was **4304/4372**, matching 11-08's Deviation 3
rather than the plan's stale `<measured_baseline>`. Surfaced, not absorbed.

## Tasks

| # | Task | Commit |
|---|---|---|
| 1 | Per-rendering identifiers + structural OPEN-arm insertion + WR-11 + two guards armed | `03ecdcf` |
| 2 | Both Aware checkers derive the count and inspect every block | `3f9bea5` |
| 3 | Re-sign Aware, decrypt-verify, refresh MANIFEST, record the resolution | `9e1e540` |

## The chosen resolution, and the one rejected

**Rejected: record "audit only the Panic-Escape-enabled path" as a product decision.** Written
out honestly it reads *"if you remove the easy exit, you also lose the on-device intelligence
audit"* — unpredictable, unwantable, and undoable only by restoring an unrelated setting. It
inverts the escalation, and it is the same silent-degradation class this phase's guard work
exists to eliminate, one level up: a fork that silently becomes the other fork.

**Chosen: insert into every OPEN-arm rendering, located structurally** — from the router's own
OPEN literal test and its `GroupingIdentifier`, the same derivation `verify_circle_zero_silence()`
uses. A future rendering added anywhere in that arm is covered with no code change, and the nine
Test-a-Circle markers are excluded **by construction**, so a model call can never land behind a
diagnostic menu item (T-11-51). Full reasoning: `docs/BUILD-NOTES.md` §33.

## The collision hazard: two routes, and the one the plan under-counted

This fork's `uid()` is a `uuid5` **name hash**, so a repeated literal is a *guaranteed*
collision. Two routes reach one:

- **14 bare `uid()` calls** — 10 in the tuple unpacking, **4 inline in the returned list**;
- **10 `if_block(key=)` arguments**, since `if_block()` derives its group from `uid(key)`.

Phase 16 made `key` **required**, closing the *omitted*-key hole; it could not close the
*repeated-literal* hole, because `audit_block()` passes fixed literals deliberately. A second
call would have collided on all ten groups just as surely, only by explicit argument instead of
omitted default. One required `ordinal` and a single nested `aid()` helper close both — there is
no route to an identifier that bypasses it.

**The plan said nine `if_block()` calls. Measured: ten.** Counted before and after; all ten
carry `key=aid(...)`, all five `uid(` code sites carry `uid(aid(...))`.

## Negative controls — including the one that found a real gap in the standing guards

**Control A — one bare `uid()`** (ordinal dropped from `scope-bounded-text`):

```
python3 tools/build_sentient.py                  -> built ..., EXIT 0     (!)
validate-shortcut --target-macos 26 ... all      -> Validation passed.    (!)
whole-artifact UUID count                        -> 1116 distinct of 1117, a NEW duplicate
```

**The build passed and gate A passed.** `verify_group_identifier_uniqueness()` asserts start/end
ownership of **`GroupingIdentifier`s**, so a collision on the action **`UUID`** axis is outside
it by construction; the validator does not check UUID uniqueness at all. Only the explicit
whole-artifact UUID count caught it. That is a real limit in the guard set, recorded in §33
rather than left implicit.

**Control B — one `if_block()` key** (`key="fast"`):

```
a GroupingIdentifier is not owned by exactly one control-flow block ...:
F05BC2CA-D66A-5B6F-981A-46C0EE877F8E: 2 start(s) at [1101, 1419] and 2 end(s) at [1132, 1450]
EXIT CODE: 1
```

Phase 16's guard fires and the build **fails closed** before writing — exactly the "next
insertion" its arming comment anticipated. Restored, the rebuild reproduced the pre-control
SHA-256 `c52edd93…` byte for byte.

**Both checkers shown failing on a defect invisible to them beforehand**, by running the retired
version alongside the new one on the same mutated artifact:

| mutation (scratch copy) | retired | new |
|---|---|---|
| delete one whole audit block | `sentient_core_check` **exit 0** | **exit 1**, naming the count mismatch |
| remove the latency gate from the **second** block only | `sentient_audit_check` **exit 0** | **exit 1**, naming block 1 |

**WR-11 control** — one filler action inserted upstream of the import prologue:

```
DERIVED  ActionIndex 7 -> is.workflow.actions.gettext 'yes'; next names 'Import AI'
RETIRED  ActionIndex 6 -> is.workflow.actions.setvariable   (no WFTextActionText at all)
```

The retired literal would have pointed `ParameterKey: "WFTextActionText"` at an action that does
not define that parameter — silently, per axis 1.

## Every acceptance criterion, measured

| criterion | result |
|---|---|
| Aware `askllm` == Core OPEN-arm markers | **2 == 2**, both printed, derived not pinned |
| audit spans disjoint | 2 spans, 10 distinct groups each, union **20** == sum **20**, intersection **∅** |
| `verify_group_identifier_uniqueness()` still in chain, build exits 0 | **yes** — third, independent confirmation |
| `grep -c verify_circle_zero_silence` / `verify_parameter_keys` | 3 / 2 (≥1 each) |
| `src/PROSOCHE-Dumb.xml` unchanged | `git status --short` **empty** |
| `grep -cE 'actions\[6:6\]\|"ActionIndex": 6'` | **0** |
| `grep -c 'len(models) == 1'` / `grep -cE 'sa\[6:8\]\|sa\[7\]'` | **0 / 0** |
| literal integer audit count in either checker | **0** — both computed from a parsed artifact |
| gate A, both forks | `Validation passed.`, exit 0 |
| AEA1 decrypt-verify, Aware | 4438 == 4438, `WFWorkflowActions` equal **== True**, `plutil -lint` OK |
| recovered `askllm` parameters | 2 of 2 carry `Apple Intelligence on Device` + `Text` |
| thirteen structural checkers | **13/13 green**, `manifest_check` included |
| `grep -c DIST-03 docs/BUILD-NOTES.md` | 13 → **14** |
| gate B | invoked in **no** command in this plan |

## Deviations from Plan

### 1. [Rule 1 — plan arithmetic wrong] The `/3` GroupingIdentifier criterion is not satisfiable

- **Found during:** Task 1 acceptance.
- **Issue:** The criterion asserts that distinct `GroupingIdentifier`s inside the audit spans
  equals occurrences **divided by three**, "start, otherwise-or-end, end are the only modes
  emitted". That assumes every block has three endpoints. **Six of the ten do not:** `enabled`,
  `circle-min`, `circle-max`, `found`, `scope-bounded` and `scope-consistency` have no Otherwise
  arm. Measured per block: **24 occurrences, 10 distinct** — and 24/3 = 8 ≠ 10. The criterion as
  written could never pass on a correct artifact.
- **Resolution:** Asserted the property the criterion was reaching for, in a strictly stronger
  form: per-block identifier sets are **disjoint** and their **union equals their sum** (20 = 20),
  with each block's size and the union printed. The arithmetic identity was dropped as unsound,
  not worked around.

### 2. [Rule 1 — pre-existing, out of scope] A duplicate action UUID exists on BOTH forks

- **Found during:** Task 1, by the whole-artifact uniqueness criterion — which is exactly what
  that criterion is for.
- **Issue:** `792D1640-FEB7-5FAF-AD6D-0E66CC1A1075` is carried by two unrelated actions on each
  fork: the bootstrap `detect.dictionary` producing `State` (Core 77) and the `getvalueforkey`
  reading `voice_enabled` (Core 3724).
- **Not caused by this plan:** present at HEAD `224e68a8` on **both** forks including **Core**,
  so it is emitted by `tools/build_state_engine.py` and merely inherited. Verified the duplicate
  set is **identical before and after**, and that **no audit-span identifier** participates in it.
- **Resolution:** **NOT fixed** — this plan modifies `build_sentient.py` only and is required to
  leave the Core source byte-identical. Logged to `deferred-items.md` with its mechanism (the
  same frozen-counter landmine Phase 16 documented in `stable_uid()`, one axis over), the
  measured fact that neither the guard nor gate A detects it, and a suggested fix shape.

### 3. [Rule 1 — stale plan baseline] Action totals were 4304/4372, not 4302/4370

- **Found during:** Task 1 baseline.
- **Issue:** The plan's `<measured_baseline>` was taken at HEAD `e6b96e3`, before 11-07 landed.
- **Resolution:** Re-derived rather than transcribed, as the plan itself instructs. Every
  acceptance criterion is index-free and asserts equalities between freshly measured counts, so
  nothing depended on the stale figures. The six "held" invariants (11 renderings, 11 markers, 2
  OPEN-arm markers per fork, 1 model call, and the Core/Aware totals) were confirmed fresh.

### 4. [Rule 2 — criterion satisfiable only by rewording] Two greps matched my own prose

- **Found during:** Tasks 1 and 2.
- **Issue:** `grep -cE 'actions\[6:6\]|"ActionIndex": 6'` and `grep -c 'len(models) == 1'` each
  returned 1 after the code change — the sole remaining match being the **explanatory comment
  quoting the retired form**.
- **Resolution:** Reworded both comments to describe the retired construct without reproducing it
  verbatim, preserving the explanation. Both greps now return 0. Consistent with this project's
  existing `docs/retired_clause_check.py` posture: a retired clause quoted verbatim is
  indistinguishable from a live one to any scanner.

### 5. [contract] The plan's expectation that both controls fail BOTH detectors is not achievable

- **Found during:** Task 1 negative controls.
- **Issue:** The criterion asks that dropping the ordinal from a `uid()` call **and** from an
  `if_block()` key each make **both** `verify_group_identifier_uniqueness()` and the
  duplicate-identifier assertion fail. The guard asserts start/end ownership of
  `GroupingIdentifier`s **by design**, so it is structurally incapable of seeing a bare-`uid()`
  action-UUID collision.
- **Resolution:** Both controls were run and reported exactly as measured — control B fails the
  guard (build exits 1), control A passes the guard **and gate A** and is caught only by the
  whole-artifact UUID count. This is a finding, not a shortfall: it is the concrete justification
  for that criterion existing as a separate check, and it is recorded in §33.

## Threat record

| Threat | Disposition |
|---|---|
| **T-11-47** (spoofing — Aware silently behaving as Core) | **CLOSED.** Audit on every OPEN-arm rendering; count derived in the builder and both checkers, so one block cannot satisfy it |
| **T-11-48** (duplicate identifiers across audit blocks) | **CLOSED** for the blocks this plan emits — disjoint sets, union == sum, no new duplicate UUID, two negative controls (one per route), plus Phase 16's standing guard |
| **T-11-49** (the duplicated model prompt) | Unchanged and asserted per block: the second block is the same bounded prompt, and `sentient_audit_check` now checks the bounded-prompt property in **every** block |
| **T-11-50** (a second model call) | **accept**, unchanged — the renderings are mutually exclusive at run time; the eight-second latency gate is asserted per block |
| **T-11-51** (a model call behind a diagnostic) | **CLOSED.** OPEN-arm scoping excludes the nine Test-a-Circle markers by construction |
| **T-11-52** (structural result recorded as device observation) | **CLOSED.** §33 and the MANIFEST both close with an explicit no-behavioural-claim section |
| **T-16-01 (adjacent)** | Confirmed passing on the modified fork; also surfaced its blind spot on the UUID axis (Deviation 2) |

## Known Stubs

None.

## Device verification

**Nothing in this plan is device-verified, and nothing claims to be.** Specifically NOT claimed:
that any Use Model call in either audit block has **ever** run on Apple-Intelligence-capable
hardware — it has not, in this plan or any before it; that the model returns a parseable first
token; that it completes inside the eight-second gate; that the pinned on-device source is
honoured at run time; that the `CHALLENGE` revision or high-circle `DENY` redirect behave as
designed.

**A simulator can never settle any of it.** Apple Intelligence is inside `.claude/CLAUDE.md` §9's
explicit "Rung 2's ceiling" list, so this is a rung-3+ question — it was therefore **not
attempted**, rather than attempted and reported inconclusive. The `WFLLMModel` literal is
donor-confirmed (BD-04-R2): a fact about what a device **writes**, not about what this artifact
**does**. **DIST-03 stays open.** This plan changes *how many renderings the eventual device test
will cover* — two instead of one — and nothing about its outcome.

## Notes for the orchestrator

- **No shared artifact was touched.** `.planning/STATE.md` and `.planning/ROADMAP.md` are
  unmodified, per the worktree contract. This plan's acceptance criteria required no edit to
  either, so unlike 11-08 there is **no handoff text** to apply.
- `docs/retired_clause_check.py` is **green** in this worktree (13/13). The dispatch note
  described it as pre-existing red from gitignored `graphify-out/` content; that content is not
  present here, which is consistent with the stated cause. No action taken either way.

## Self-Check: PASSED

- `tools/build_sentient.py` — FOUND (ordinal + aid() chokepoint, structural insertion, WR-11, two guards armed)
- `src/PROSOCHE-Sentient.xml` — FOUND, 2936286 bytes, 4438 actions, SHA-256 `c52edd93…`
- `docs/sentient_core_check.py` — FOUND (derived count, N-span excision, content-anchored prologue)
- `docs/sentient_audit_check.py` — FOUND (every span, per-block assertions)
- `docs/BUILD-NOTES.md` — FOUND (§33; `DIST-03` count 13 → 14)
- `artifacts/shortcuts/MANIFEST.md` — FOUND (block prepended, three Aware rows recomputed)
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — FOUND, 238095 bytes
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — FOUND, 231148 bytes, not re-signed (verified equal by decrypt)
- `deferred-items.md` — FOUND (the pre-existing duplicate UUID recorded)
- Commits `03ecdcf`, `3f9bea5`, `9e1e540` — all FOUND
- All thirteen structural checkers exit 0, `manifest_check` included
