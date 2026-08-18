---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
fixed_at: 2026-08-18T00:00:00Z
review_path: .planning/phases/11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r/11-REVIEW.md
iteration: 1
findings_in_scope: 7
fixed: 7
skipped: 0
status: all_fixed
---

# Phase 11: Code Review Fix Report

**Fixed at:** 2026-08-18
**Source review:** `.planning/phases/11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r/11-REVIEW.md`
**Iteration:** 1
**Scope:** WR-16, WR-17, WR-18, WR-19, IN-01, IN-03, plus IN-02 (judgment call — taken)

**Summary:**
- Findings in scope: 7
- Fixed: 7
- Skipped: 0

## Definition of done — measured, not asserted

| Gate | Result |
|---|---|
| `python3 <each>` for all 13 `docs/*.py` | **13/13 exit 0** |
| `docs/retired_clause_check.py` | exit 0 — the documented 4 gitignored `graphify-out/` occurrences are absent from the isolated worktree, so the expected 12/13 was in fact 13/13 |
| Gate A, `src/PROSOCHE-Dumb.xml` | `Validation passed.`, exit 0 |
| Gate A, `src/PROSOCHE-Sentient.xml` | `Validation passed.`, exit 0 |
| Gate B (advisory, non-blocking) | exactly **one** line per fork — the documented `com.apple.mobilenotes.SharingExtension` / `WFCreateNoteInput` waiver, indices 4148 (Core) and 4282 (Aware). No new finding. |
| Both builders re-run after every fix | exit 0, `md5` identical across consecutive rebuilds |
| `git status --short` | **empty** |

**No re-sign was performed, and none was needed.** Every fix is guard-, comment- or
prose-only. After all seven, both forks rebuild to `a8d712b0…` (Core) and `0dee5197…` (Aware) —
byte-identical to the shipped sources — and `git status --short` reports no change under `src/`.
Action totals are unchanged at **Core 4304 / Aware 4438**. Per the phase's own rule, re-signing
reflexively would have been wrong.

**Every guard fix was proven to fail closed**, on an isolated copy of the tree, never by
mutating the tracked tree. Before/after exit codes are recorded per finding below.

## Fixed Issues

### WR-19: the Panic Escape guards assert the resolved *variable* set, never the resolved *gate* set

**Files modified:** `tools/build_state_engine.py`
**Commit:** `902d735`
**Applied fix:** added a zero-gates raise to `verify_panic_escape_seed()` (a `gates` counter
incremented whenever a mode-0 conditional tests a member of `guarded`) and the matching
`if not groups` raise to `verify_panic_escape_isolation()`.

Fixed **before** WR-16 deliberately: once provenance is transitive, the fully-disconnected
state is much harder to construct, so the control had to be run against the un-fixed resolver
to mean anything.

**Negative control** — all three Panic Escape gates (`universal_leaving()`'s bypass gate and
`panic_escape_branch()`'s two write gates) moved behind one `set_var` hop each, so `guarded`
stays non-empty and both existing vacuity raises stay silent:

| | before | after |
|---|---|---|
| `build_state_engine.py` | **exit 0** | **exit 1** — *"2 variable(s) resolve to `panic_escape_enabled` by provenance but no mode-0 conditional tests any of them, so assertion (3) below inspected zero gates…"* |
| `build_sentient.py` | exit 0 | not reached |
| substantive checkers | all exit 0 | — |

---

### WR-16: one `set_var` hop disarms all three provenance-resolved guards

**Files modified:** `tools/build_state_engine.py`
**Commit:** `8f558a5`
**Applied fix:** `_read_variable_keys()` now propagates its key sets across variable→variable
copies in a fixpoint loop until the map stops growing, so a chain of any length resolves rather
than only a direct read. Applied exactly as the review specified. Verified beforehand that
`is.workflow.actions.setvariable` is **not** in `STRING_ENVELOPE_PARAMS`, so the bare
`Type: "Variable"` descriptor the loop matches is the shape actually emitted and the fix is not
dead on arrival.

**Control H** — `CR-01` reintroduced verbatim (`dimming()` back on the
`settings_snapshot.brightness` container at condition 100, whole body in the `otherwise` arm)
with the gate reading a one-hop copy:

| | before | after |
|---|---|---|
| `build_state_engine.py` | **exit 0** | **exit 1** — the dead-arm message naming **22 offenders**, matching 11-08's own control exactly |
| `environmental_restore_check.py` | exit 0 | exit 0 (build already failed) |
| `phase9_self_check.py` | exit 0 | — |

**Control G** — `universal_leaving()`'s bypass gate behind one hop at condition 100, the two
write gates left connected so WR-19's new raise does *not* mask the result:

| | before | after |
|---|---|---|
| `build_state_engine.py` | **exit 0** | **exit 1** — *"a Panic Escape gate uses a non-numeric condition code action 530: 'PE Gate' at condition 100…"* |
| `build_sentient.py` | exit 0 | not reached |
| all 13 checkers | all exit 0 | — |

**One thing a human should confirm:** this widens what every provenance-resolved guard can see.
On the current tree it produces no false positive (13/13 checkers, both builds, byte-identical
artifacts), but a *legitimate* future `set_var` copy of a `settings_snapshot`- or
`panic_escape_enabled`-derived variable will now inherit that provenance and be held to the same
gate rules. That is the intended semantics, not a bug — but it is a semantic widening, not a
syntactic one, and worth knowing about before the next re-gating change.

---

### WR-17: `REQUIRED_SYMBOLS` proves a guard exists, never that a builder runs it

**Files modified:** `docs/environmental_restore_check.py`
**Commit:** `47cc720`
**Applied fix:** added `CALLED_GUARDS` (the five guards among `REQUIRED_SYMBOLS`) and a new
`call_site_check(builder, sentient)` that reads each builder's `main()` via
`inspect.getsource()` — the idiom the file already uses on `manual_emergency_restore` — and
requires each name to appear applied. `cross_fork_check()` now returns the already-loaded
Sentient module so no second load is needed. The docstring records the limit of a source read
honestly: it catches deletion, not a call commented out or moved behind a never-taken branch.
A runtime trace was rejected because this file is documented read-only and must never rebuild
an artifact.

**Negative control A** — both guard *calls* deleted from `main()` in **both** builders,
definitions untouched:

| | before | after |
|---|---|---|
| both builders | exit 0 | exit 0 (correct — this is a checker fix, not a build gate) |
| all 13 checkers | **13/13 exit 0** | `environmental_restore_check.py` **exit 1** — *"build_state_engine.py's main() no longer CALLS verify_environmental_reachability()…"* |

**Negative control B** — the Aware half alone, to prove the second arm of the loop is armed and
not just the Core one: `verify_panic_escape_isolation` call removed from `build_sentient.py`
only → **exit 1** naming `build_sentient.py`.

---

### WR-18: gap 3's invariant has no build guard, and the named second line of defence cannot see the defect

**Files modified:** `tools/build_sentient.py`, `.planning/phases/11-…/11-09-SUMMARY.md`
**Commit:** `5ee2586`
**Applied fix:** two parts.

1. An assertion in `build_sentient.py`'s `main()` immediately after the insertion loop,
   comparing the inserted `askllm` count against `len(markers)` and refusing to write the
   artifact on a mismatch — asserted where the artifact is written, as the review specified.
2. The false claim in `11-09-SUMMARY.md`, corrected in all three places it appears
   (`provides`, the Task 2 row, the T-11-47 threat row) **and preserved**: a new *Correction
   (phase-11 code review, WR-18)* section quotes all three original wordings verbatim, states
   precisely why each is wrong, and records the measurement. History corrected, not deleted.
   Frontmatter re-parsed as valid YAML after the edit.

**Negative control** — insertion loop reverted to `markers[:1]`:

| | before | after |
|---|---|---|
| `build_sentient.py` | **exit 0**, defective fork **written to disk** | **exit 1**, nothing written — *"2 OPEN-arm dispatch rendering(s) but 1 Use Model action(s)…"* |
| `docs/sentient_audit_check.py` | exit 0 (passes the defect) | unchanged — still cannot see it, which the SUMMARY now says |
| `docs/sentient_core_check.py` | exit 1 | exit 1 |

`docs/sentient_audit_check.py` was deliberately **not** given a Core-derived expectation. The
review offered that as an alternative to correcting the SUMMARY; correcting the SUMMARY was the
mandated half, and the builder assertion is strictly stronger than a second standalone checker
because it fires before the artifact reaches disk. Duplicating `sentient_core_check.py`'s
derivation into a third file would have added a second place for that derivation to drift.

---

### IN-01: an unreachability claim stated wider than its guard supports

**Files modified:** `artifacts/shortcuts/MANIFEST.md`, `tools/build_state_engine.py`
**Commit:** `ece61d2`
**Applied fix:** narrowed MANIFEST's `**0 actions per fork remain unreachable.**` to
`**0 environmental actions per fork remain in a dead arm.**`, with a paragraph naming the
surviving unreachable branch and why it is retained. `already_dim_g` kept, with a generator
comment recording that it is inert while `dim_target` is `0` and becomes live again the moment a
non-zero target returns.

**Verified before writing, not transcribed:** the shipped Config carries `"dim_target": 0` and
`"brightness_floor": 0`; `already_dim_g` is `Captured Brightness <= Dim Target` (condition 1)
nested inside `capture_g`'s `Captured Brightness > 0` (condition 2) — exact complements. Also
checked the parallel gate the review did not mention: `silence()`'s `quiet_g` uses a `0.10`
**literal** (`number(0.10, "Silence Target")`), not the config value, so it is reachable for any
captured volume in `(0, 0.10]` and is **not** affected. That distinction is recorded in both
files so a future reader does not "fix" the wrong one.

---

### IN-02: the Circle-6 `Eject` interim is not named as interim in the generator's comment text

**Files modified:** `tools/build_state_engine.py`
**Commit:** `c768493`
**Applied fix:** a comment beside the branch tuple, matching the Circle-8 `DELIBERATE INTERIM`
wording, naming Phase 17 and the exact two cells that flip.

**Taken rather than skipped**, because every factual claim in it was independently corroborated
before writing — no phase number or cell index was carried over from the review on trust:

- `ROADMAP.md:40` — *"Phase 17: Exile split and exit-route deepening"*
- `ROADMAP.md:461-462` — *"`Redirect` has no implementation until Phase 17, so all three sequences hold `Eject` at Circle 6 until then; Phase 17 flips Classic's and Ambient's"*
- `docs/CAPABILITY-DECISIONS.md:398` — BD-06's table row `| 6 | Heresy | Redirect | Eject | Redirect |`
- `docs/BUILD-NOTES.md:3672-3673` — *"exactly two cells — `Classic[5]` and `Ambient[5]` … `BlackMirror[5]` is already correct"*
- the shipped Config's `sequences` — `Eject` at index 5 in all three, confirmed by parsing the artifact

It is a Python comment, emits nothing, and changes no artifact byte. It discharges plan 11-02's
stated prohibition, which §34 had filled with an absence rather than a comment.

---

### IN-03: the newest stated Aware action total is 4372; the shipped fork is 4438

**Files modified:** `docs/phase9_self_check.py`, `artifacts/shortcuts/MANIFEST.md`
**Commit:** `23f69c5`
**Applied fix:** appended the post-11-09 figures beside the dated 11-08 ones at all three sites
(`phase9_self_check.py`'s totals paragraph, MANIFEST's 11-08 totals sentence, MANIFEST's 11-07
`+2` delta line), leaving each dated measurement readable as what it actually measured.

**Measured directly from the artifacts, not transcribed:** Core **4304**, Aware **4438**.

The review's alternative — pinning the totals in an asserted table — was **rejected with a
written reason**, now recorded in `phase9_self_check.py` itself: that file already documents a
deliberate choice to leave the totals unpinned, because pinning them turns every legitimate
action-count change into a red checker. Overturning that would have been a decision, not a fix.

## Skipped Issues

None.

## Explicitly out of scope, and confirmed untouched

- Every finding below `# ARCHIVE — waves 1–6 review` — covered by the review's own disposition
  table, files outside this diff range.
- The duplicate action `UUID` `792D1640-…` on both forks — recorded in `deferred-items.md`,
  deliberately unfixed, separately tracked.
- Gate B's single waived line per fork — advisory, never blocking; re-measured as still exactly
  one per fork.

---

_Fixed: 2026-08-18_
_Fixer: Claude (gsd-code-fixer)_
_Iteration: 1_
