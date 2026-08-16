---
phase: 10-ship-readiness-remainder-and-ux-lite-pass
plan: 01
subsystem: infra
tags: [python, shortcuts-plist-generator, control-flow, build-guard, ux-copy, thresholds]

# Dependency graph
requires:
  - phase: 09-reintroduce-and-validate-dimming-silence-stateful-restore-on
    provides: the post-merge Dumb generator lineage this plan patches in place
provides:
  - Circle 0, a silent band in which behavioural state accumulates and persists but nothing is shown
  - Raised threshold curves for all three profiles (band widths preserved, entry into Circle 1 delayed)
  - verify_circle_zero_silence(), a build guard making the silent band structural rather than incidental
  - enclosing_groups(), a reusable structural enclosure walker over GroupingIdentifier stacks
  - Deletion of the unconditional OPEN notification (the CLOSE confirmation survives)
  - A Leaving/Continue prompt that names what is being left and what continuing costs
  - Canonical strategy section 10.6 recording the band
affects:
  - 10-02-PLAN.md (Control Room Status/Note copy must gloss a bare circle value of 0)
  - 10-03-PLAN.md (docs/router_ui_census.py asserts against the silent-band conditional)
  - 10-04-PLAN.md (ships the artifact)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Structural enclosure test — walk WFWorkflowActions once maintaining a stack of open
      GroupingIdentifiers across conditional / repeat.count / repeat.each / choosefrommenu,
      so a build guard can assert 'action X is inside control-flow block Y' without any
      action index, which shifts on every rebuild"
    - "Arm-scoped invariant — derive an arm's span from input_key_tests() + flow_index()
      and assert only within it, with the exemption and its by-construction reason stated
      in the docstring, rather than writing an artifact-wide assertion that would raise on
      legitimate sibling call sites"
    - "Threshold rise by first-band-width — raising every entry of an ascending threshold
      array by that array's own first band width preserves every band width exactly and
      delays only entry, which is a strictly weaker change than re-tuning the curve"

key-files:
  created: []
  modified:
    - src/PROSOCHE-Dumb.xml
    - tools/build_state_engine.py
    - docs/state_engine_self_check.py
    - PROSOCHE_Nine_Circles_Canonical_Strategy.md

key-decisions:
  - "Circle 0 was promoted as a first-class value of the existing `circle` field rather than
    added as a parallel `silent` boolean — one source of truth for 'did anything happen',
    no schema_version bump, no migration (a widened value range needs none)."
  - "save_state() deliberately stays OUTSIDE the silent-band gate while universal_leaving()
    moves inside it. The band suppresses surfaces, never accumulation."
  - "verify_circle_zero_silence() property (c) is scoped to the OPEN arm. The nine MANUAL-arm
    Test-a-Circle sequences reads are exempt by construction and the docstring says so, so a
    future reader cannot mistake the scope for an oversight and 'tighten' it into a build break."
  - "Section 10.5's printed threshold arrays were left stale rather than silently rewritten —
    the plan scoped Task 3 to recording the band only. Logged as a deferred item below."

requirements-completed: [CIRC-01, CIRC-13, CIRC-14]

# Metrics
duration: ~5 minutes
completed: 2026-08-17
tasks-completed: 3
tasks-total: 3
files-modified: 4
status: complete
---

# Phase 10 Plan 01: Circle 0 — the silent band Summary

A genuine OPEN whose Pressure is below the active profile's entry threshold now resolves to Circle 0 and shows nothing at all — no notification, no menu, no primitive — while still computing and persisting behavioural day, Heat, Gravity, Pressure, open count and the active session; a build guard makes that property structural.

## What Was Built

**Task 1 — the end-to-end silent band** (commit `6b2decb`)

Four edits, one commit, because the Config literal and its `docs/` mirror are two copies of one table:

1. **`src/PROSOCHE-Dumb.xml` action 7** — every threshold entry raised by that profile's own first band width, so band widths are preserved exactly and only entry into Circle 1 is delayed:

   | Profile | Was | Now | Shift |
   |---|---|---|---|
   | Paradise | `1, 4, 7, 10, 13, 16, 19, 22, 25` | `4, 7, 10, 13, 16, 19, 22, 25, 28` | +3 |
   | Limbo | `1, 3, 5, 7, 9, 11, 14, 17, 20` | `3, 5, 7, 9, 11, 13, 16, 19, 22` | +2 |
   | Inferno | `1, 2, 4, 6, 8, 10, 12, 14, 16` | `2, 3, 5, 7, 9, 11, 13, 15, 17` | +1 |

   All three stay strictly ascending, stay nine entries, and keep their last entry below `heat.cap + gravity.cap` = 35, so Circle 9 stays reachable. Because `heat.open_base` is 1, a first open of a cold day now scores Pressure 1 and lands in the silent band under all three profiles.

   **These are prototype values for on-device tuning.** They are deliberately not commented inside the JSON — the literal is parsed by `detect.dictionary` and must stay valid JSON.

2. **The Circle floor** — `number(1, "Circle Next")` became `number(0, "Circle Next")` in `open_pipeline()`. The scan's heading phrase is byte-identical (`docs/state_engine_self_check.py` asserts on that prefix); its first bullet now names Circle 0 as the starting point, and a fourth bullet names the silent band.

3. **The gate and the notification** — the unconditional OPEN `notification()` and its three-line comment were deleted together as one block. `save_state()` now sits outside a new `if_block("Circle Next", 2, number=0)`; `universal_leaving()` sits inside it, with an authored comment explaining the band, the fact that state is already saved above, and the dotted-read hazard — authored so `main()`'s auto-comment pass does not insert its generic filler.

4. **`docs/state_engine_self_check.py`** — `THRESHOLDS` replaced verbatim, `circle()`'s seed changed from 1 to 0, the Limbo assertion updated from `[1, 2, 9, 9]` to `[0, 1, 8, 9]`, and three assertions added: silent band per profile (Limbo 2, Paradise 3, Inferno 1 all yield 0); nine entries and strictly ascending; last entry below 35. The pre-existing three-distinct-profiles assertion at Pressure 8 still holds — it now yields Paradise 2, Limbo 3, Inferno 4.

**Task 2 — making it structural** (commit `1598306`)

`verify_circle_zero_silence(actions)` follows `verify_router_shape()`'s shape exactly and is registered in `main()` immediately after it. Four properties, each with its own `SystemExit` message:

- **(a)** exactly one number-seeded `Circle Next` set-variable exists and its `WFNumberActionNumber` is `0`;
- **(b)** the mode-0 `choosefrommenu` whose `WFMenuItems` is `["Leaving", "Continue"]` is enclosed by a mode-0 conditional carrying `WFCondition 2`, `WFNumberValue 0` and a `Circle Next` variable input;
- **(c)** every `getvalueforkey` **inside the OPEN arm** whose `WFDictionaryKey` addresses the `sequences.` subtree is enclosed by that same group — the property that actually keeps the dotted read away from index 0;
- **(d)** the OPEN arm contains zero `notification` actions.

Two supporting helpers were added: `enclosing_groups(actions)`, a single-pass GroupingIdentifier stack walk, and `_is_silent_band_conditional()` / `_dictionary_key_string()`. The OPEN arm's boundaries are derived structurally via the existing `input_key_tests()` and `flow_index()`, never by action index, and the guard fails with a distinct message if the OPEN conditional cannot be found — a future router restructure surfaces here rather than silently emptying the checked span.

The `universal_leaving()` prompt was rebuilt with `text_token()`:

> You just opened a tracked app. PROSOCHĒ is at Circle ￼.
>
> Leaving: PROSOCHĒ suggests somewhere better to go and takes you there.
> Continue: you go into the app, after this Circle's intervention.

192 characters, exactly one attachment naming `Circle Next` at the correct offset. Both item titles stay byte-identical, so `select_exit()` and `primitive_dispatch()` still hang off them. The G-04-4b comment now records this as revision 2 and gives the reason the copy can afford to be longer: the menu no longer fires in the silent band.

**Task 3 — the canonical strategy** (commit `9ab0f31`)

New `## 10.6 Circle 0 — the silent band` between 10.5 and section 11, plus one sentence each in the section 11 preamble, Primitive A, and the section 12 preamble. `git diff --stat` shows **24 insertions, 0 deletions** — nothing was rewritten or renamed.

## Verification Evidence

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit 0 — provenance guard passed before every builder run |
| `python3 tools/build_state_engine.py` | passes, running all 16 in-process verify passes including the new one |
| `python3 docs/state_engine_self_check.py` | exit 0 |
| `python3 docs/phase5_self_check.py` | `phase5 self-check: passed` |
| `python3 docs/phase7_self_check.py` | `phase7 self-check: passed` (builder still idempotent across two runs) |
| `python3 docs/phase9_self_check.py` | `negative_control: passed`, `site_audit: passed (28/28 sites, 18 coerced, 10 correctly not)` |
| `validate-shortcut … --target-macos 26 --target-platform all` | `Validation passed.` |
| `import build_sentient` smoke test | ok — all 10 `verify_*` imports still resolve |

Parsed from the built artifact:

- `thresholds` = the three raised arrays; all ascending, all length 9, all last entries < 35 (cap read from the same literal as `heat.cap + gravity.cap` = 35).
- Exactly one number-seeded `Circle Next` set-variable, seed `0`.
- `notification` count **1**, down from 2. Index 1338 lies between the CLOSE conditional (1219) and its Otherwise (1350). The OPEN arm contains zero.
- The single `["Leaving", "Continue"]` menu (index 520) is inside the OPEN arm and enclosed by silent-band group `4AC9BA5C-…`.
- **Scoping proof:** ten `sequences.`-addressing `getvalueforkey` actions. Index 997 is in the OPEN arm and inside the silent band; indices 1467, 1699, 1931, 2163, 2395, 2627, 2859, 3091, 3323 are in the MANUAL arm and enclosed by no `Circle Next` conditional. The build passes with all nine in that state — property (c) is OPEN-arm-scoped and correctly does not raise on them.
- `setbrightness` 14, `setvolume` 14, `getdevicedetails` 20 — all unchanged from HEAD. The brightness/volume cut stays cancelled.
- `grep -c 'def verify_circle_zero_silence'` = 1; `grep -c 'verify_circle_zero_silence(actions)'` = 2.

### Negative controls

Both were run against the real builder, and both restorations were confirmed green.

**Control A — Circle floor.** Seed reverted to `number(1, "Circle Next")`:

```
Circle floor: the Circle scan seeds at 1, must be 0 -- a seed of 1 abolishes the silent
band and shows a surface on the very first open of the day
EXIT=1
```

`src/PROSOCHE-Dumb.xml` was **not** written — the guard runs before `SOURCE.write_bytes()`, so a failed build leaves the artifact untouched. Restored to `0`; build exit 0.

**Control B — silent-band enclosure.** `universal_leaving()` moved outside the conditional:

```
silent band: the Leaving/Continue menu is not enclosed by a 'Circle Next > 0' conditional,
so a Circle-0 OPEN would show a menu and reach every primitive
EXIT=1
```

Restored; build exit 0.

## Deviations from Plan

None — the plan executed exactly as written. No auto-fixes were needed; no CLAUDE.md rule required an adjustment; no authentication gate or checkpoint was reached.

The tracer feedback gate on Task 1 was evaluated under auto mode: the tracer's `<verify>` chain was re-run end-to-end and passed, so expansion to Tasks 2 and 3 proceeded without a human checkpoint.

## Known Stubs

None. No placeholder, hardcoded-empty, or TODO value was introduced.

## Deferred Items

| Item | Where | Why deferred |
|---|---|---|
| Canonical strategy §10.5 still prints the pre-rise threshold arrays (`1, 4, 7, …` etc.) | `PROSOCHE_Nine_Circles_Canonical_Strategy.md:1178, 1184, 1190` | Task 3's action was explicitly scoped to "record the band; do not rewrite anything else", and its acceptance criterion required deletions confined to the insertion points. §10.6 records the shipped entry values (Paradise 4, Limbo 3, Inferno 2) and §10.5 already labels its numbers "prototype parameters", so the document is not self-contradictory, only under-specific. Worth a one-line correction in a later documentation pass. |
| `docs/phase6_self_check.py` red | `docs/phase6_self_check.py:68` | Pre-existing and unrelated (`WFAppName` assertion vs `normalize_open_apps()`); repaired in 10-03 by design. Out of scope, untouched. |
| `docs/sentient_core_check.py` red | — | Sentient is stale at `2026-08-14k`; re-forking is SEED-005, out of phase scope. Untouched. |

## Threat Flags

None. No file changed in this plan introduces a network endpoint, auth path, file-access pattern, or schema change at a trust boundary. T-10-01 and T-10-02 (the dotted-read and list-index hard errors at Circle 0) are both mitigated by the gate plus properties (b) and (c) with a demonstrated negative control; T-10-03 by the three new array invariants asserted in both the reference implementation and against the parsed artifact; T-10-04 by the unchanged 14/14/20 counts; T-10-05 by changing the Config literal and its `docs/` mirror in the same commit.

## Notes for the Next Plan

- **10-02** must gloss `circle` at 0 wherever `manual_note_refresh()` surfaces `Snapshot Circle` — the Status alert and the Note's CURRENT STATE block will otherwise render a bare `0` with no explanation.
- **10-03**'s `docs/router_ui_census.py` can reuse `enclosing_groups()` and the OPEN-arm derivation verbatim; both are now module-level in `tools/build_state_engine.py`.
- **On-device UAT for this change is one observation:** a first open of a cold day must produce no visible reaction at all, and `state.json` must still show `heat` 1, `pressure` 1, `circle` 0, an incremented `opens_today`, and a live `active_session`.

## Self-Check: PASSED

- `src/PROSOCHE-Dumb.xml` — FOUND
- `tools/build_state_engine.py` — FOUND
- `docs/state_engine_self_check.py` — FOUND
- `PROSOCHE_Nine_Circles_Canonical_Strategy.md` — FOUND
- commit `6b2decb` — FOUND
- commit `1598306` — FOUND
- commit `9ab0f31` — FOUND
