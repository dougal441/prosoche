---
phase: 14-ash-as-real-color-filters-grayscale
plan: 01
subsystem: shortcuts-generator
tags: [ios-shortcuts, accessibility, color-filters, grayscale, plist, build-guards, safe-05, circ-02]

# Dependency graph
requires:
  - phase: 11-dispatch-and-reachability
    provides: "the eleven-rendering primitive_dispatch() surface and verify_environmental_reachability(), both of which this plan's census arithmetic and guard ruling depend on"
  - phase: 16-environmental-capture-persistence
    provides: "restore_managed_settings()'s four call sites and the capture-and-restore machine this primitive deliberately does NOT join"
  - phase: spike-005-ios-color-filters-identifier
    provides: "the three decrypted device donors that are the only authority for the identifier and the parameter shape"
provides:
  - "Circle 2 (Black and White) emits the real iOS Color Filters grayscale toggle instead of an alert"
  - "one unconditional Set Color Filters (off) at the top of restore_managed_settings(), reaching all four recovery paths"
  - "safety.ash_managed_color_filters is live as a kill switch instead of dead Config"
  - "COLOR_FILTERS constant and set_color_filters(on) emitter, donor-exact"
  - "two build guards armed for the new identifier; four deliberate non-registrations recorded in source"
  - "docs/phase5_self_check.py asserts the AX identifier present and the macOS twin absent"
  - "docs/environmental_restore_check.py carries a derived colour census row"
affects: [14-02, 14-03, 14-UAT, phase-15-voice, ship-gate]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "guard registration decided from what each guard asserts, never by analogy to a neighbouring primitive"
    - "unconditional restore for a two-valued setting, emitted first so no dotted-read hard error below it can abort the run"
    - "asymmetric checker inversion: assert the new thing present, keep the old thing's absence assertion as the trap guard"

key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - docs/phase5_self_check.py
    - docs/environmental_restore_check.py
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml

key-decisions:
  - "The AX site census is 15 per fork = 11 primitive_dispatch() renderings (on) + 4 restore_managed_settings() call sites (off), derived from the built artifact with plistlib. It coincides numerically with the superseded snapshot design's 15/fork figure by entirely different arithmetic; the coincidence is recorded so it is not read as confirmation."
  - "SAFE-01's capture clause is ruled STRUCTURALLY INAPPLICABLE to this primitive — a two-valued setting has no original to capture and no read-back intent exists on iOS. The compliant substitute is an unconditional off leg reachable from the panic button. Recorded as a deviation, not silently treated as satisfied."
  - "The emitted action carries `state` only, with no UUID key. This matches the generator's own house style (setbrightness, setvolume and returntohomescreen all omit UUID unless an output is referenced) and the plan's automated verify accepts it. Emitting an unreferenced UUID would invent a value no consumer reads."
  - "The executor ruling above was deliberately NOT given a D-14-xx number: that series denotes the phase's USER decisions and D-14-02 is already taken by the superseded spike-011 probe decision."
  - "Both rewritten shipped comments were rewritten in full, including their first lines, after re-measuring that comment_index() has no caller anchoring on either prefix (plan A3)."

patterns-established:
  - "Recurrence-guard registration: an identifier may be registered in a guard that is silent today, when the shape the guard catches is exactly what a superseded design would have produced. Silent-but-armed is the correct state; its silence is not a reason to remove it."
  - "Named non-registration block: guards deliberately NOT registered are listed by symbol with a per-symbol mechanism, so a later reader cannot 'complete the set' by analogy."
  - "Census row with adjacent arithmetic and an explicit note when a new row's derivation differs in SHAPE from the rows beside it, even when the totals coincide."

requirements-completed: [CIRC-02, SAFE-01, SAFE-02, SAFE-05]

coverage:
  - id: D1
    description: "Circle 2 emits the donor-exact Color Filters action set on, gated only on safety.ash_managed_color_filters, with no alert, notification or menu"
    requirement: "CIRC-02"
    verification:
      - kind: integration
        ref: "plan 14-01 Task 1 tracer verify — plistlib parse of both forks: AX 15, on 11, state values {0,1} only, keys ['state'], twin 0, no synthesised descriptor"
        status: pass
      - kind: integration
        ref: "python3 docs/sequence_dispatch_check.py — 0 orphans, 0 unreachable, 0 unknown, 0 duplicates"
        status: pass
      - kind: unit
        ref: "inspect.getsource(ash()) scanned for alert/notification/menu emitter calls — no executable hit"
        status: pass
    human_judgment: false
  - id: D2
    description: "restore_managed_settings() opens with one unconditional Set Color Filters (off), rendering at exactly 4 sites — CLOSE pipeline, Emergency Restore, Ice expiry, live-Ice redirect"
    requirement: "SAFE-05"
    verification:
      - kind: integration
        ref: "plan 14-01 Task 1 tracer verify — off == 4 in both forks; the check fails on any other count"
        status: pass
      - kind: integration
        ref: "python3 docs/environmental_restore_check.py — EXPECTED_SITES[COLOR_FILTERS] == 15 in the built artifact"
        status: pass
    human_judgment: false
  - id: D3
    description: "settings_snapshot stays at exactly two groups; no ownership marker, no save_state(), no persist-before-apply ordering imported into this primitive"
    requirement: "SAFE-01"
    verification:
      - kind: integration
        ref: "plan 14-01 Task 2 verify — bootstrap state template in both forks parses as JSON with settings_snapshot == ['brightness', 'volume']"
        status: pass
      - kind: unit
        ref: "source scan — the AX identifier and 'color_filters' appear nowhere in verify_capture_persistence(), verify_restore_gates() or SNAPSHOT_SEED"
        status: pass
    human_judgment: false
  - id: D4
    description: "The two guards that can fire over this action are armed; the parameter-key guard is proven load-bearing by negative control"
    requirement: "SAFE-01"
    verification:
      - kind: unit
        ref: "negative control — one extra parameter on the emitter aborts the build: \"unverified parameter keys emitted: ... -> ['operation'] (15 total)\", exit 1; scratch change discarded"
        status: pass
    human_judgment: false
  - id: D5
    description: "Pinned brightness/volume/device-details counts and the 15/4 coercion split are unmoved"
    requirement: "SAFE-02"
    verification:
      - kind: integration
        ref: "plan 14-01 Task 1 pinned-count check — setbrightness 15, setvolume 15, getdevicedetails 22 in both forks"
        status: pass
      - kind: integration
        ref: "python3 docs/phase9_self_check.py — site_audit: 30/30 sites audited, 19 coerced, 11 correctly not"
        status: pass
    human_judgment: false
  - id: D6
    description: "The screen actually turns black and white when Circle 2 fires, and colour actually comes back at CLOSE and through Emergency Restore after a force-quit"
    requirement: "CIRC-02"
    verification: []
    human_judgment: true
    rationale: "Device-gated by construction. The simulator cannot execute this class of environmental action (CLAUDE.md §9 'Rung 2's ceiling'), and a simulator reading is never promotable above UNVERIFIED. Nothing in this plan is device-proven; behavioural coverage belongs to 14-UAT.md (plan 14-03) and is BLOCKED on DIST-03."

# Metrics
duration: 42min
completed: 2026-08-19
status: complete
---

# Phase 14 Plan 01: Ash as real Color Filters grayscale Summary

**Circle 2 stopped talking about a visual pause and started turning the phone black and white: the donor-exact iOS Color Filters action on at eleven dispatch renderings, one unconditional off at all four recovery paths, and the alert that made Circle 2 indistinguishable from Circle 1 deleted rather than replaced.**

## Performance

- **Duration:** ~42 min
- **Tasks:** 3 of 3
- **Files modified:** 5 (3 source, 2 generated)
- **Commits:** 4

## Accomplishments

- **The highest-evidence primitive in the product now exists.** `ash()` emits `AXToggleColorFiltersIntent` with `state = 1`, gated only on the `safety.ash_managed_color_filters` kill switch. The alert that *was* Circle 2 is gone, not supplemented — per D-14-C the escalation from Circle 1 to Circle 2 is the escalation from interrupting with words to changing the environment without them.
- **The restore leg — the actual deliverable — reaches all four recovery paths from one insertion.** A single unconditional `set_color_filters(False)` at the top of `restore_managed_settings()` renders at the CLOSE pipeline, Emergency Restore, Ice expiry and the live-Ice redirect. It is emitted **first** so that no dotted read below it can hard-error and abort the run before colour is restored — the exact failure mode whose symptom is a user stuck in grayscale.
- **`safety.ash_managed_color_filters` stopped being dead code.** Read through the numeric `> 0` gate (a string compare would silently never match, because safety booleans read back as numeric 1/0). False makes the Circle fire a bare Nothing — the only recourse a colour-blind, migraine or low-vision user has until the backlogged detection item ships.
- **Guard registration was decided per guard, not by analogy.** Two armed, four deliberately abstained from and named in source with their mechanisms. The parameter-key guard was then *proven* load-bearing by negative control rather than assumed.
- **The build's own self-check now asserts what ships instead of its opposite** — while keeping the half that protects against the macOS-twin substitution, which is precisely the trap a permanently-red gate A creates.

## Task Commits

1. **Task 1 (TRACER): the AX action on at Circle 2, off in the restore expansion, both forks building green** — `ca0bbea` (feat)
2. **Task 2: register the identifier where a guard can actually fire, record the four deliberate abstentions** — `698187e` (chore)
3. **Task 3: invert the phase-5 assertion asymmetrically, give the artifact checker a derived colour census** — `57a0c8b` (test)
4. **Correction: stop labelling the SAFE-01 ruling with a colliding decision ID** — `796cb2a` (docs)

## Files Created/Modified

- `tools/build_state_engine.py` — `COLOR_FILTERS` constant and `set_color_filters(on)` emitter; `ash()` rewritten; `restore_managed_settings()` gains the unconditional off leg; `VERIFIED_PARAMETER_KEYS` and `ENVIRONMENTAL_IDENTIFIERS` entries; `DELIBERATE_NON_REGISTRATIONS` block.
- `docs/phase5_self_check.py` — the both-absent Color Filters assertion split into AX-present-at-a-derived-count and twin-still-absent; `EXPECTED_COLOR_FILTER_SITES` with its arithmetic.
- `docs/environmental_restore_check.py` — `COLOR_FILTERS` constant, `EXPECTED_SITES` census row at 15, `REQUIRED_SYMBOLS` gains `set_color_filters` and `ash`, deliberate-omission comment on the bootstrap-seed group loop.
- `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` — rebuilt, unsigned. Re-signed in plan 14-03.

## The derived AX census and its arithmetic

**15 per fork, identical in Dumb and Sentient.** Derived from the built artifact with `plistlib`, not transcribed:

| Leg | Count | Derivation |
|---|---:|---|
| On (`state = 1`) | 11 | one per `primitive_dispatch()` rendering — nine Test-a-Circle submenu cases plus two in `universal_leaving()` |
| Off (`state = 0`) | 4 | one per `restore_managed_settings()` call site — `close_pipeline()`, `manual_emergency_restore()`, `ice_expiry()`, `live_ice_redirect()` |
| **Total** | **15** | |

**A coincidence worth naming so it is not mistaken for corroboration:** the superseded snapshot-based design also projected 15 per fork, by entirely different arithmetic. The agreement is accidental. This figure is derived; that one was not carried forward.

## Gate A — verbatim residue and exit code (recorded, chained into nothing)

Per D-GATE-A and D-14-01, gate A exits 1 from this plan onward, permanently, because the AX identifier is absent from all three bundled ToolKit snapshots. **This is not a defect and is not a reason to reach for the macOS twin.** It appears in no `&&` chain and in no success condition.

Command (run separately per fork):

```
validate-shortcut src/PROSOCHE-<fork>.xml --target-macos 26 --target-platform all
```

**`src/PROSOCHE-Dumb.xml` — EXIT=1.** Output was `Validation failed:`, a `First failing action: index 0 (is.workflow.actions.comment)` header line with a snippet of the fork's opening comment, then **exactly 30 error lines and nothing else** — two families, 15 lines each, one per AX instance:

- `AppIntent action missing AppIntentDescriptor at index N: com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` at N ∈ {176, 226, 1012, 1272, 1585, 1770, 2039, 2308, 2577, 2846, 3115, 3384, 3653, 3922, 4168}
- `Unknown AppIntent identifier at index N: com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` at the same 15 indices

**`src/PROSOCHE-Sentient.xml` — EXIT=1.** Identical structure, identical two families, 30 lines, at N ∈ {178, 228, 1014, 1340, 1719, 1904, 2173, 2442, 2711, 2980, 3249, 3518, 3787, 4056, 4302}.

Both families appear because the action is descriptor-less and synthesising a descriptor is forbidden — which is why D-14-01's waiver had to enumerate both families to be satisfiable at all. **Nothing outside these two families was reported on either fork.** The residue checker that formalises this is plan 14-02's, not this plan's.

## Negative control — the parameter-key guard is load-bearing, not assumed

On a scratch copy of the generator, `set_color_filters()` was made to emit one extra parameter (`operation="turn"` — the key both Turn donors elide, so it is the exact fabrication the entry exists to forbid). `python3 tools/build_state_engine.py` aborted, **EXIT=1**, verbatim:

```
unverified parameter keys emitted: action 176 com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent -> ['operation']; action 226 com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent -> ['operation']; action 1012 com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent -> ['operation']; action 1272 com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent -> ['operation']; action 1585 com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent -> ['operation'] (15 total)
```

The scratch change was reverted from a pre-mutation copy and is not on disk; `git status --short tools/` showed only the intended edit, and the post-revert rebuild reproduced the pre-mutation artifact hash exactly.

## The `comment_index()` anchor re-measurement (plan A3)

Re-measured 2026-08-19 against the generator at HEAD. `comment_index()` is called from exactly seven places, and the prefixes reaching it are: `ROUTE_FALLBACK_MARKER`, `MANUAL_MARKER`, `LIVE_ICE_MARKER`, `EXPIRY_MARKER`, `"--- OPEN STATE ENGINE ---"`, `"--- CLOSE SESSION PIPELINE ---"`, `"--- CONTROL ROOM: confirm"`, `"Check whether this run had to rebuild the setup file"` and `"Short-circuit a live cooldown"`.

**Neither rewritten comment's first line is among them.** `"Black and White is the validator-clean…"` and `"Restore managed settings only when a captured original exists:"` are both free, so both comments were rewritten in full — which mattered, because both first lines were exactly the text that became false. This confirms the plan's own measurement and supersedes `14-PATTERNS.md`'s instruction to hold the `ash()` first line stable. `dimming()`'s first line **is** load-bearing (16-03 anchors on it) and was not touched; the finding here does not generalise to it.

## Decisions Made

- **`state` only, no UUID key on the emitted action.** The donors carry a UUID because Shortcuts.app assigns one to every action it authors, but this generator emits a UUID only when an action's output is referenced downstream — measured: `setbrightness` emits `{ShowWhenRun, WFBrightness}`, `setvolume` emits `{ShowWhenRun, WFVolume, WFVolumeSetting}`, `returntohomescreen` emits nothing at all. Emitting an unreferenced UUID here would invent a value with no consumer and depart from a house style that is device-proven across phases 11–16. The plan's automated verify accepts this (it pops `UUID` with a default); the prose acceptance criterion assumed the key present, so the divergence is recorded rather than glossed.
- **The `DELIBERATE_NON_REGISTRATIONS` block lives beside `ENVIRONMENTAL_IDENTIFIERS`**, with a pointer to it from the `VERIFIED_PARAMETER_KEYS` entry. The two constants sit ~2000 lines apart; one block plus one cross-reference beats two divergent copies.
- **`verify_restore_gates()`'s abstention reason is recorded as the loop-head identifier filter**, per the plan's W-2 correction — the action is discarded at the *first* `continue`, before operand resolution, not at the later literal-target `continue`. The verdict is the same; the mechanism is what a future reader would act on.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] A decision-ID collision in shipped source comment text**

- **Found during:** Task 3 review, after Task 1 had already been committed
- **Issue:** `ash()`'s docstring recorded the SAFE-01 structural-inapplicability ruling as "deviation D-14-02". D-14-02 is already the phase's locked (and now superseded) spike-011 probe decision, and the `D-14-xx` series denotes the phase's **user** decisions. Labelling an executor ruling with a user-decision ID misattributes its authority and would collide with a real, differently-scoped decision in every future search of that series.
- **Fix:** The docstring now points at this SUMMARY and at plan 14-01's flagged assumption A1, and states explicitly why no `D-14-xx` number was taken.
- **Files modified:** `tools/build_state_engine.py`
- **Verification:** Rebuilt both forks (artifact hash unchanged — comment text is Python-level, not emitted here); `docs/phase5_self_check.py` and `docs/environmental_restore_check.py` re-run green.
- **Committed in:** `796cb2a`

### Recorded rulings (not auto-fixes)

**A1 — SAFE-01's capture clause is structurally inapplicable to this primitive.** SAFE-01 requires an environmental change be captured and durably persisted before it is applied. Spike 005 established there is no read-back intent for **any** accessibility setting across all 35 intents in the framework, so the clause cannot be satisfied by detection here. The reading adopted, per plan A1 and D-14-A: a two-valued setting whose restore target is a constant has nothing to capture, so the clause does not bind, and the compliant substitute is an unconditional off leg reachable from the panic button. **This is recorded as a deviation rather than silently treated as satisfied by analogy to brightness.** It is written into `ash()`'s docstring so a later reader meets the reasoning at the code, not only here.

---

**Total deviations:** 1 auto-fixed (Rule 1), plus 1 recorded ruling.
**Impact on plan:** None on scope. The auto-fix corrected shipped comment text only. No prohibition was touched: `settings_snapshot` still has two groups, no ownership marker or `save_state()` was added, the off leg is ungated, no alert survives in `ash()`, the twin identifier appears nowhere, no descriptor was synthesised, `state = 2` was never emitted, `operation` is never written, and no pinned count moved.

## Issues Encountered

- **`manifest_check.py` is red, expected, and deliberately not fixed.** `row 'Core source': MANIFEST declares 2864203 bytes, src/PROSOCHE-Dumb.xml is 2914723 bytes`. Both forks were rebuilt, so their bytes no longer match the signed MANIFEST rows. Per D-MANIFEST this stays red until plan 14-03 re-signs and refreshes; closing it by editing MANIFEST rows without re-signing would be falsifying a provenance record. **12 of 13 checkers green, manifest expected red.**
- **Gate A is red and stays red permanently.** Covered in full above. Not a defect; plan 14-02 owns its disposition.

## What this plan does NOT establish

Stated plainly because every item here is device-gated and the phase's own must-haves classify them as backstops:

- **That the screen actually turns black and white on a real iPhone.** The simulator cannot execute this class of environmental action, and a simulator reading is never promotable above `UNVERIFIED` (CLAUDE.md §9, "Rung 2's ceiling"). Structural coverage lands here; behavioural coverage is `14-UAT.md`'s and is BLOCKED on DIST-03.
- **That colour actually comes back at CLOSE, or through Emergency Restore after a force-quit mid-intervention.** Emergency Restore has still never been tapped on a device.
- **That the AX action imports and runs on iOS 26 without an unfilled-parameter error.** Signing is measured unaffected by the unknown identifier; import and run behaviour is device-gated.
- **The pre-existing-grayscale-user case.** No detection is built (D-14-D); `safety.ash_managed_color_filters` is the entire remedy until the backlog item ships. T-14-06 is **accepted and disclosed, not mitigated** — plan 14-03 carries the onboarding disclosure.

## Known Stubs

None. No placeholder, TODO or unwired data path was introduced; the one `todos/pending/…` string in the diff is a citation of the backlog item in a docstring, not a stub marker.

## User Setup Required

None — no external service configuration required.

## Self-Check: PASSED

Files asserted present:

- `tools/build_state_engine.py` — FOUND (contains `COLOR_FILTERS`, `set_color_filters`, `DELIBERATE_NON_REGISTRATIONS`)
- `docs/phase5_self_check.py` — FOUND (contains `EXPECTED_COLOR_FILTER_SITES`, `AX_COLOR_FILTERS`, `UA_COLOR_FILTERS_MACOS_TWIN`)
- `docs/environmental_restore_check.py` — FOUND (contains `COLOR_FILTERS` in `EXPECTED_SITES`)
- `src/PROSOCHE-Dumb.xml` — FOUND (15 AX actions)
- `src/PROSOCHE-Sentient.xml` — FOUND (15 AX actions)

Commits asserted present: `ca0bbea`, `698187e`, `57a0c8b`, `796cb2a` — all FOUND in `git log`.
