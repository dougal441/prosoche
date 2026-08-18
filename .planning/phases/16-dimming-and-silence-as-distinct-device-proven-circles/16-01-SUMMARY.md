---
phase: 16-dimming-and-silence-as-distinct-device-proven-circles
plan: 01
subsystem: shortcuts-generator
tags: [safety, capture-restore, build-guard, tracer, P0]
status: complete
requires:
  - "tools/build_state_engine.py::save_state, set_value, dimming, silence"
  - "docs/state_engine_self_check.py owner-arm span invariant (must survive unchanged)"
provides:
  - "tools/build_state_engine.py::verify_capture_persistence — build guard pinning persist-before-apply"
  - "tools/build_state_engine.py::_save_source_dictionary — resolves a save's source dictionary"
  - "tools/build_state_engine.py::stable_uid / SHOWNOTE_GATE_GROUP — counter-free identifiers for preserved blocks"
  - "tools/build_state_engine.py::verify_group_identifier_uniqueness — build guard against reused GroupingIdentifiers"
  - "docs/phase9_self_check.py::capture_persistence_negative_control — proves the guard load-bearing"
affects:
  - "src/PROSOCHE-Dumb.xml and src/PROSOCHE-Sentient.xml rebuilt (+44 actions each)"
  - "artifacts/shortcuts/MANIFEST.md now stale — docs/manifest_check.py RED by constraint D-MANIFEST until 16-05"
tech-stack:
  added: []
  patterns:
    - "guard-and-negative-control pairing (verify_* in the generator, control in docs/*_self_check.py)"
    - "docstring-states-the-defect"
    - "locate by content, never by index"
key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - tools/build_sentient.py
    - docs/environmental_restore_check.py
    - docs/phase9_self_check.py
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml
decisions:
  - "Persist in the APPLYING arm only, not the outer capture arm — resolves 16-RESEARCH Open Question 5"
  - "Preserved control-flow blocks get name-keyed stable_uid() identifiers, never counter-derived uid()"
metrics:
  duration: ~50m
  completed: 2026-08-18
  tasks: 3
  files: 6
requirements: [CIRC-03, CIRC-05, SAFE-03, SAFE-05]
---

# Phase 16 Plan 01: Persist the captured original before the device is changed — Summary

The capture/persist/apply loop is now structurally capable of restoring: `dimming()` and
`silence()` write the captured original to `state.json` before Set Brightness / Set Volume
runs, a build guard pins that ordering on both forks, and a negative control proves the guard
fires when the save is removed.

## What was built

The phase's tracer — one thin vertical slice through every layer the phase touches
(generator renderer → build guard → static negative control → rebuilt artifact).

**The P0 that was closed.** `dimming()`/`silence()` captured the device's current reading and
wrote it to `settings_snapshot.<group>.original_value` in the `State` dictionary, then changed
the device. `State` is never saved again after the OPEN arm's last save — every save from the
CLOSE pipeline onward sources `Reloaded State`, a different dictionary — so the captured
original never reached disk. CLOSE and Emergency Restore reloaded the file, found the cleared
sentinel, failed `restore_managed_settings()`'s numeric `> 0` gate, and skipped. The screen
dimmed and nothing in the product un-dimmed it. This was the live instance of threat T-16-01
and the reason SAFE-05's Emergency Restore was structurally ineffective.

One generator-level edit per primitive reaches all eleven `primitive_dispatch()` renderings
(nine Test-a-Circle submenu cases plus two in `universal_leaving()`), closing the MANUAL
`Test a Circle` half of the defect by construction rather than site-by-site.

## Measured evidence

### Pre-fix failure output (task 1 verify script, before the change)

```
Dumb: apply at [1035, 1122, 1291, 1378, 1585] reached with an unpersisted capture (24 total)
exit=1
```

The script fails on the first fork, so Sentient is unreported. Post-fix, both forks report
`no apply is reachable from an unpersisted capture` and the script exits 0.

### Action-count delta, with derivation

| Fork | Before | After | Delta |
|---|---:|---:|---:|
| Dumb | 4346 | 4390 | +44 |
| Sentient | 4414 | 4458 | +44 |

Derivation: 11 `dimming()` renderings + 11 `silence()` renderings = 22 new `save_state()`
calls per fork; `save_state()` emits one `setitemname` and one `documentpicker.save`, so
22 × 2 = 44 actions. Measured, not assumed — the delta matches the derivation exactly on both
forks. `documentpicker.save` totals moved 31 → 53 per fork (+22).

### CLOSE non-owner-arm disjointness — TRACED, not asserted

The span was recomputed exactly as `docs/state_engine_self_check.py` computes it (locate the
`--- CLOSE SESSION PIPELINE` comment, then the `Compare the reloaded active session` comment,
take the `GroupingIdentifier` of the conditional immediately after it, walk to that group's
mode-1 then mode-2).

| Fork | `close` | `owner` | `otherwise_index` | `owner_end` | Forbidden span |
|---|---:|---:|---:|---:|---|
| Dumb | 1512 | 1529 | **1625** | **1627** | `[1625, 1627)` |
| Sentient | 1580 | 1597 | **1693** | **1695** | `[1693, 1695)` |

Measured indices of every save this plan added:

- **Dumb (22):** 1036, 1125, 1296, 1385, 1793, 1882, 2062, 2151, 2331, 2420, 2600, 2689,
  2869, 2958, 3138, 3227, 3407, 3496, 3676, 3765, 3945, 4034
- **Sentient (22):** 1038, 1193, 1364, 1453, 1861, 1950, 2130, 2219, 2399, 2488, 2668, 2757,
  2937, 3026, 3206, 3295, 3475, 3564, 3744, 3833, 4013, 4102

**The two sets are disjoint on both forks** — no added save falls in `[otherwise_index,
owner_end)`. Nothing in `docs/state_engine_self_check.py` was relaxed, narrowed, deleted or
special-cased; the assertion and its span computation are byte-identical to their pre-plan
form. The halt-and-report path was therefore not needed.

### Guard offender count against a save-removed fixture

`verify_capture_persistence` reports **0** offenders against the real built artifact and
**22** against a hand-mutated copy with the persisting `setitemname`/`save` pairs removed
(44 actions deleted) — one offender per applying arm, exactly the sites the fix added a save
to. The pre-fix task-1 script reported 24 for the same defect because it is not arm-scoped and
additionally counts the two restore-side applies; the guard scopes by `_enclosing_if_arms()`,
so `restore_managed_settings()` is correct by construction rather than by exemption.

### Checker counts: MEASURED non-movement

No count moved, as predicted. `site_audit()` still reports 30/30 sites, 19 coerced, 11
correctly not; `expected_counts` stays 15/15 and `expected_coerced` stays 15/4;
`environmental_restore_check.py`'s `EXPECTED_SITES` is untouched. Mechanism: the fix adds only
`setitemname` and `documentpicker.save` actions and adds no `setbrightness`, `setvolume` or
`getdevicedetails` action, and changes no operand's source or coercion. **No number was
edited in any checker**, so no derivation comment was owed — the measured non-movement is
recorded in `docs/phase9_self_check.py`'s new PHASE 16 docstring paragraph instead, because a
reader who expects the totals to have shifted needs to find the reason they did not.

### Gates

| Gate | Dumb | Sentient |
|---|---|---|
| A — `--target-macos 26 --target-platform all` | `Validation passed.` exit 0 | `Validation passed.` exit 0 |
| B — `--target-macos 27 --target-platform all` (advisory) | exit 1, exactly the one waived `WFCreateNoteInput` line (index 4236) | exit 1, exactly the one waived line (index 4304) |

Gate B was run separately and never `&&`-chained. Its output is exactly the permitted waiver
on both forks — nothing outside the waiver was reported.

`python3 docs/manifest_check.py` is **RED as expected** per constraint D-MANIFEST
(`row 'Core source': MANIFEST declares 2901248 bytes, src/PROSOCHE-Dumb.xml is 2930442 bytes`).
No MANIFEST row was edited; 16-05 re-signs and refreshes it.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocking] Duplicate `GroupingIdentifier` exposed by the counter shift**

- **Found during:** Task 1, at the first gate-A run after the rebuild.
- **Issue:** Gate A rejected the Dumb fork with
  `Duplicate GroupingIdentifier '6219B3ED-727D-56FA-A9FB-787F84AEAE89' for start action at
  index 4383; first seen at index 3672`. The pre-fix artifact passed gate A, so this was
  introduced by this plan — but the root cause was a pre-existing landmine, not the fix.
- **Mechanism, traced rather than guessed:** `uid()` is a counter, so the Nth call always
  yields `uuid5(".../N")`. Most of the artifact is regenerated every build, so those
  identifiers move together. But `gate_control_room_shownote()` inserts its wrapper into the
  hand-authored find-or-create block and is idempotent by positional probe — it returned early
  when the wrapper was already present. That wrapper's `GroupingIdentifier` was therefore
  **frozen** into `src/PROSOCHE-Dumb.xml` at counter value **1310** by whichever historical
  build first created it. Adding 22 `save_state()` calls shifted every later `uid()` by +22, a
  `silence()` rendering landed on 1310, and two unrelated conditional blocks began sharing one
  identifier — which `.claude/CLAUDE.md` records as the project's #1 documented real-world
  mistake. Confirmed by reverse-mapping every counter-derived UUID in the artifact: the gate's
  was the **only** preserved one, and it was the only duplicate.
- **Fix:** `stable_uid(name)` — a name-keyed `uuid5` drawn from outside the counter sequence,
  so a preserved identifier is stable across builds (idempotency kept) and can never equal a
  counter-derived `uid()` (collision unrepresentable, not merely unlikely).
  `SHOWNOTE_GATE_GROUP` uses it, and `gate_control_room_shownote()` now re-stamps an
  already-wrapped artifact in place instead of merely returning.
- **Second-order defect caught during the fix:** the first re-stamp implementation replaced
  *every* action holding the stale identifier globally. That is wrong precisely because the
  stale value is duplicated — it re-stamped the innocent `silence()` block too and simply moved
  the collision onto the new identifier. The build guard caught it immediately
  (`10B58FD1-…: 2 start(s) at [3672, 4383]`). Re-scoped to walk forward from the gate's own
  Show Note to its own End If. Both the mechanism and the rejected global form are recorded in
  the code comment so the next reader does not retry it.
- **Files modified:** `tools/build_state_engine.py`
- **Commit:** `0465593`

**2. [Rule 2 — Missing critical functionality] `verify_group_identifier_uniqueness`**

- **Found during:** Task 1, while fixing deviation 1.
- **Issue:** The collision above was a landmine re-armable by any future phase that changes
  the action count, and *nothing in the build noticed it* — only the external validator did.
  A reused `GroupingIdentifier` silently corrupts control-flow block boundaries at runtime.
- **Fix:** A build guard asserting every `GroupingIdentifier` carries exactly one block start
  (mode 0) and one block end (mode 2). Middle arms (mode 1) are deliberately uncounted — an If
  has one Otherwise but a Choose from Menu has one per item, so a count there would be an
  arbitrary number rather than an invariant. Registered in `main()`. It demonstrably has teeth:
  it is what caught the over-broad re-stamp.
- **Files modified:** `tools/build_state_engine.py`
- **Commit:** `0465593`

Both deviations sit inside the plan's own files (`tools/build_state_engine.py`) and neither
touches a gate, a checker assertion, or a count.

## Key decisions

**Persist in the applying arm, not the outer capture arm — resolves 16-RESEARCH Open Question 5.**
The cheaper placement (immediately after the `set_value` block, one save per rendering covering
both inner arms) is wrong: that arm also runs on the already-dim / already-quiet path, where no
Set Brightness / Set Volume fires. It would persist a snapshot for a change that never happened,
and a later CLOSE would pass the `> 0` gate and drive the device to it — so a user who raised
brightness by hand mid-session would have it pulled back down by a Circle that never touched it.
Persisting only on the applying path makes a snapshot mean exactly "a change is outstanding",
which is what every restore gate already assumes. This directly satisfies the CIRC-03 and
CIRC-05 adjacency truths: at Captured == Target the already-quiet/already-dim arm fires, no
apply runs, and no snapshot is persisted.

**Both `save_state()` calls take the default source `State`,** matching `set_value()`'s default
target. Naming `"Reloaded State"` would persist a dictionary that never received the capture —
the exact mechanism of the defect (T-16-04). The guard resolves each save's source and refuses
to let a non-`State` save clear a pending capture.

## Threat mitigations applied

- **T-16-01 (critical, tampering):** closed. The persist now strictly precedes the apply on
  every path that applies.
- **T-16-02 (high, DoS of device usability):** the persistence fix is the actual mitigation;
  residual device-failure-mode risk is deferred to 16-06's instrument, not inferred here.
- **T-16-03 (high):** the condition-100 container gate and the numeric `> 0` capture gate are
  **byte-identical to their pre-plan form** in both `dimming()` and `silence()`. This plan adds
  a save; it touched no gate.
- **T-16-04 (medium):** enforced by `_save_source_dictionary()` inside the new guard.
- **T-16-05 (medium):** no checker count moved, so no number was edited.
- **T-16-SC (low, accepted):** no external package was installed. Python usage is stdlib only
  (`plistlib`, `copy`, `inspect`, `pathlib`, `uuid`).

## Prohibitions honoured

- No brightness/volume apply on any path where the captured original has not reached disk —
  proven by the guard and the verify script on both forks.
- No gate weakened, removed or re-coded.
- The OPEN-path save above `universal_leaving()` was not relocated or duplicated.
- No checker's expected count was edited.
- `docs/state_engine_self_check.py`'s no-save-in-the-non-owner-arm assertion and its span
  computation are untouched.
- `silence()`'s emitted Shortcuts comment (SAFE-02, "never increase it") was not edited.
- `dimming()`'s emitted comment was not edited — it belongs to plan 16-03.

## Known Stubs

None. No stub, placeholder, TODO or skipped test was introduced.

## Device-gated work NOT done here (recorded, not inferred)

This plan is entirely rung-1 (file-level) work and claims nothing about hardware. The
persist-before-apply ordering is proven **structurally**; that state.json actually round-trips
a brightness value without precision loss on real hardware is the plan's one `backstop` truth
(CIRC-05 precision) and remains **BLOCKED on DIST-03** — paired device present,
`tunnelState: disconnected`, no live session to drive. It is 16-06's instrument to settle.

## Follow-up for later plans in this phase

- `docs/manifest_check.py` is RED until 16-05 re-signs and refreshes the six MANIFEST rows
  (constraint D-MANIFEST). Do not fix it by editing rows.
- The signed artifacts in `artifacts/shortcuts/` are now behind `src/*.xml` by +44 actions per
  fork.

## Self-Check: PASSED

Files claimed modified, verified present on disk: `tools/build_state_engine.py`,
`tools/build_sentient.py`, `docs/environmental_restore_check.py`, `docs/phase9_self_check.py`,
`src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml`.

Commits claimed, verified in `git log`: `0465593`, `44df498`, `2407986`.

New symbols verified callable and registered by source inspection:
`verify_capture_persistence` (in `main()`, in `build_sentient.py`'s import list and call
sequence, in `REQUIRED_SYMBOLS`), `_save_source_dictionary`, `stable_uid`,
`verify_group_identifier_uniqueness` (in `main()`), `capture_persistence_negative_control`
(in `phase9_self_check.main()`, calls the real `bse.verify_capture_persistence` and the real
`bse.dimming`/`bse.silence`, contains no re-implementation of the guard).

Build determinism verified: a second consecutive rebuild of both forks leaves the working tree
clean (byte-identical output), so the re-stamp and the fix are idempotent.
