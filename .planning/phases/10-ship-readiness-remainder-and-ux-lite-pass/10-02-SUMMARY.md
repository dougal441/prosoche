---
phase: 10-ship-readiness-remainder-and-ux-lite-pass
plan: 02
subsystem: infra
tags: [python, shortcuts-plist-generator, control-flow, idempotent-patch-pass, ux-copy, menu, self-check]

# Dependency graph
requires:
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    plan: 01
    provides: Circle 0 (the silent band), which is why both Circle displays now need a gloss
provides:
  - gate_control_room_shownote(), an idempotent patch pass gating the single shownote on an explicit request
  - Manual Show Note Requested, the flag that gives "Open Control Room" a real effect
  - A tenth manual menu item, Setup Check, reporting Personal Automation status from state already recorded
  - Manual Setup Check Requested plus two derived verdict variables, all from flat reads and numeric gates
  - A manual menu prompt that explains what the menu is and why the run reached it
  - A Circle-0 gloss on both the Note CURRENT STATE snapshot and the Status alert
  - Three new structural assertions and a ten-item MENU in docs/phase7_self_check.py
affects:
  - 10-03-PLAN.md (docs/router_ui_census.py counts menu items and user-facing surfaces)
  - 10-04-PLAN.md (ships the artifact and its manifest)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Positional idempotency probe — a patch pass that INSERTS actions cannot probe a
      parameter for prior application, so it probes its own inserted neighbour instead:
      'is actions[index-1] already the mode-0 conditional I would insert?'"
    - "Derived status without new state — answer a user-facing question ('did my automations
      fire?') by reading epochs the engine already writes, rather than adding a state key,
      a bootstrap-template edit and a schema_version bump for a fact already implied"
    - "Honest-limitation copy — when a derivation is sufficient but not necessary evidence,
      put the asymmetry in the shipped alert string, not in a source comment the user
      will never see"

key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - src/PROSOCHE-Dumb.xml
    - docs/phase7_self_check.py
    - .planning/REQUIREMENTS.md

key-decisions:
  - "The shownote was gated; filter.notes and Create Note were deliberately left outside the
    gate. The note keeps being found or created on every manual run, so BOOT-08's
    deleted-note self-heal survives and manual_note_refresh() keeps a bound Control Room
    Note variable to append to."
  - "Setup Check derives its verdicts from last_open_at and last_close_at rather than adding
    automation_a_seen / automation_b_seen keys — no schema_version bump, no bootstrap edit,
    no migration, and the reads are flat so they cannot hard-error on legacy state."
  - "The Setup Check derivation is sufficient but not necessary evidence, so the limitation
    ships inside the alert message itself: a 'seen' verdict is never wrong, a 'not seen yet'
    verdict can be."
  - "The prompt names the fall-through case in words rather than restructuring the router.
    verify_router_shape() hard-fails all three drift modes, and the CLOSE arm provably
    contains no menu; the remaining half of the reported symptom is a device diagnosis
    deferred to 10-05."
  - "The Circle-0 gloss is unconditional literal text inside the existing text_token() part
    lists, not a new conditional — so it is honest at every Circle value and adds no
    control flow to a display path."

requirements-completed: [ROOM-01, ROOM-02, ROOM-03, ROOM-10]

# Metrics
duration: ~12 minutes
completed: 2026-08-17
tasks-completed: 3
tasks-total: 3
files-modified: 4
status: complete
---

# Phase 10 Plan 02: Control Room gating and the Setup Check item Summary

The Control Room Note now opens only when `Open Control Room` was chosen instead of after every manual menu choice; the manual menu explains what it is and why a run reached it; and a tenth item, `Setup Check`, tells a user whether either Personal Automation has ever been recorded firing — derived from epochs the engine already writes, with no new state key and no schema bump.

## What Was Built

**Task 1 — the Note stops opening uninvited** (commit `e5b415e`)

Two coupled edits in `tools/build_state_engine.py`:

1. **The flag.** `manual_emergency_restore()`'s `Open Control Room` case was
   `action("is.workflow.actions.nothing")` — a bare no-op whose entire effect came from an
   unconditional tail it did not own. It is now `*number(1, "Manual Show Note Requested")`,
   the same device-proven shape as `Manual Status Requested`: `number()` emits
   `is.workflow.actions.number` + `set_var`, so the variable is already Number-typed and
   `_already_numeric()` makes `normalise_numeric_operands()` leave it alone. The CYCLE 14
   checkpoint comment above the case block was extended with a PHASE 10 amendment recording
   that `Open Control Room` is *still* read-only with respect to the Note — no
   `Manual Refresh Requested`, no append — but now carries its own request flag.

2. **The pass.** `gate_control_room_shownote(actions)` is modelled line-for-line on
   `fix_notes_filter_limit()`: scan by identifier, probe for idempotency, mutate, return.
   Two differences from that analog, both forced by the plan:
   - It *inserts* actions rather than editing parameters, so the idempotency probe is
     **positional**: if `actions[index - 1]` is already a mode-0 `conditional` with
     `WFCondition 2`, it returns untouched.
   - It authors its own five-bullet comment — reported symptom, mechanism, input, and the
     idempotency condition — so `main()`'s auto-comment pass does not insert its generic
     `"Control-flow check:"` filler in front of the gate.

   The replacement sequence is comment → `if_block("Manual Show Note Requested", 2, number=0)`
   → the original shownote object unchanged → `otherwise` → `nothing` → `end_if`. The
   conditional is built only through `if_block()`, the sole sanctioned producer of a
   conditional input (axis 5: the `WFInput` variable slot takes a bare attachment, and
   `verify_conditional_inputs()` fails the build on anything else).

   Registered in `main()` immediately after `fix_notes_filter_limit()`, so the shownote
   already carries the `WFInput` key `fix_shownote_key()` writes and the notes filter already
   carries its Donor-8 limit parameters. Neither was re-patched.

**Task 2 — Setup Check** (commit `0556efd`)

*Menu.* `"Setup Check"` appended to `choices`; its case emitted after the Emergency Restore
block's `save_state()` and before the closing mode-2 menu action, so case order matches
`WFMenuItems` order element for element. Case body is one flag: `*number(1, "Manual Setup
Check Requested")`.

*Display.* In `manual_note_refresh()`, two flat reads were added beside the existing
unconditional Snapshot reads:

```python
a += read_value("last_open_at", variable("State"), "Setup Last Open")
a += read_value("last_close_at", variable("State"), "Setup Last Close")
```

Both keys are single-segment, so per CLAUDE.md's verified runtime semantics a read cannot
hard-error even on a legacy `state.json` that predates them — a missing flat key returns
nothing. `read_value()` throughout; `get_value()` is reserved for `COMPOUND_STATE_KEYS` and
these are numeric leaves.

Two verdicts are then derived in a loop, each through `if_block(<read>, 2, number=0)` — a
numeric `> 0` test, never a condition-100 existence test. A numeric `> 0` reads false for a
JSON null, for the string `"null"` and for an empty string under every device-measured
coercion, and every value ever written to these keys is a strictly positive epoch. True arm
emits `gettext` + `set_var` carrying `"seen"`; otherwise arm the same pair with
`"not seen yet"`. Each conditional carries an authored four-bullet intent comment.

The display itself is gated on `Manual Setup Check Requested` with the same numeric shape and
contains exactly one `alert()`:

> Automation A — App Is Opened, passing OPEN: ￼
> Automation B — App Is Closed, passing CLOSE: ￼
>
> This reports whether PROSOCHĒ has ever recorded a genuine open or an owning close. A close
> that a newer open superseded, or an open during a cool-down, records nothing — so a "not
> seen yet" verdict can be wrong, but a "seen" verdict never is.

`Automation A` / `Automation B` are the Control Room Note's own section headings (`### Automation A — OPEN`,
`### Automation B — CLOSE`), read out of the built artifact rather than invented, so the check
and the instructions agree word for word as ROOM-02 and ROOM-03 require.

No `appendnote`, no `Manual Refresh Requested`, no new state key, no bootstrap edit, no
`schema_version` bump.

**Task 3 — prompt, gloss, checks, requirement** (commit `0faa1c7`)

*Prompt.* The bare product name became a 258-character plain `str` (correct for `WFMenuPrompt`
when nothing is interpolated — the `Choose profile` and `Choose sequence` submenus use the
same form):

> This is PROSOCHĒ's manual control menu. You are here because the Shortcut was run by hand,
> or because an automation passed it something other than OPEN or CLOSE. If you did not mean
> to be here, choose Open Control Room — that Note has the setup instructions.

*Circle gloss.* Both display literals were extended inside their existing `text_token()` part
lists, so `attachmentsByRange` offsets were recomputed by `text_token()` and nothing was
hand-edited in the plist:

| Site | Now reads |
|---|---|
| Note `## CURRENT STATE` | `- Circle (0 means the silent band: PROSOCHĒ recorded the open and showed nothing) — ￼` |
| Status alert | `Circle (0 means the silent band: recorded, nothing shown): ￼` |

No conditional was added, so the gloss is honest at every Circle value.

*Checks.* `docs/phase7_self_check.py` gained `"Setup Check"` in `MENU` (message updated from
"nine" to "ten"), plus three `require()` assertions in the house idiom: exactly one shownote
whose immediately preceding action is a mode-0 `WFCondition 2` conditional testing
`Manual Show Note Requested`; both flat setup keys present among the literal `WFDictionaryKey`
values; and a `setvariable` naming `Manual Setup Check Requested`.

*Requirement.* ROOM-10 amended to ten items with a clause naming what Setup Check reports.
Checkbox state left as-is. No other requirement touched.

## Verification Evidence

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit 0 — run before every builder invocation |
| `python3 tools/build_state_engine.py` | passes, all 16 verify passes green including `verify_circle_zero_silence()`, `verify_router_shape()`, `verify_sentinel_gates()`, `verify_conditional_inputs()`, `verify_string_envelopes()`, `verify_numeric_operands()` |
| Two consecutive builds | `src/PROSOCHE-Dumb.xml` byte-identical (`9653e8af…` after Task 1; re-confirmed after Tasks 2 and 3) |
| `python3 docs/phase7_self_check.py` | `phase7 self-check: passed` |
| `python3 docs/state_engine_self_check.py` | exit 0 |
| `python3 docs/phase5_self_check.py` | `phase5 self-check: passed` |
| `python3 docs/phase9_self_check.py` | `negative_control: passed`, `site_audit: passed (28/28 sites, 18 coerced, 10 correctly not)` |
| `validate-shortcut … --target-macos 26 --target-platform all` | `Validation passed.` |
| `import build_sentient` smoke test | ok |

Parsed from the built artifact:

- **shownote count 1**, at index 3680. Its immediately preceding action is a `conditional`,
  mode 0, `WFCondition 2`, `WFNumberValue 0`, `WFInput` variable `Manual Show Note Requested`.
  Followed within two actions by mode-1 and mode-2 conditionals carrying the same
  `GroupingIdentifier`.
- **Exactly one** conditional in the whole artifact tests `Manual Show Note Requested` — the
  positional probe is doing its job.
- `Manual Show Note Requested` is set once, preceded by `is.workflow.actions.number` with
  `WFNumberActionNumber 1`.
- `filter.notes` count **1**, `com.apple.mobilenotes.SharingExtension` count **1** — unchanged
  from HEAD, and `enclosing_groups()` reports **neither** is enclosed by the new gate group
  while the shownote **is**. BOOT-08 self-heal intact.
- `filter.notes` still carries `AppIntentDescriptor`, `WFContentItemLimitEnabled True`,
  `WFContentItemLimitNumber 1.0` — the cycle-16 fix untouched.
- **One** ten-entry `WFMenuItems` list; the ordered mode-1 `WFMenuItemTitle` values equal it
  element for element, ending with `Setup Check`.
- `getvalueforkey` actions exist for the literal keys `last_open_at` (×2) and `last_close_at`
  (×2) — the OPEN-arm pair from `open_pipeline()` plus the new MANUAL-arm pair. Neither key
  contains a dot.
- **Zero** conditionals in the Setup Check path use condition 100 or 101; all three
  (`Setup Last Open`, `Setup Last Close`, `Manual Setup Check Requested`) carry `WFCondition 2`
  and `WFNumberValue 0`.
- The `Manual Setup Check Requested` group encloses exactly **1** `alert` and **0**
  `appendnote`.
- The alert message contains `Automation A`, `Automation B`, `OPEN`, `CLOSE`, `can be wrong`
  and `never is`.
- The bootstrap state template is **byte-identical to HEAD** (compared via `git show
  HEAD:src/PROSOCHE-Dumb.xml`); `schema_version` still `2`.
- Menu prompt is a plain `str`, 258 characters, containing `run by hand`, `OPEN or CLOSE` and
  `Open Control Room`.
- Both glossed literals resolve through a `WFTextTokenString` whose `attachmentsByRange` entry
  count equals its `￼` count (9 and 7 respectively) — offsets recomputed correctly.

### Negative control (Task 3 acceptance criterion)

The shownote gate was reverted two ways at once — `gate_control_room_shownote()` given an
early `return`, and the already-baked gate actions stripped from the artifact (5 actions
removed) — because disabling the pass alone would leave the hand-authored region's existing
gate in place:

```
File ".../docs/phase7_self_check.py", line 20, in require
    raise AssertionError(message)
AssertionError: Show Note is not gated on a 'Manual Show Note Requested > 0' conditional
```

Both files were restored from backups and the check re-run:

```
phase7 self-check: passed
```

The assertion names the gate, as required, and the restoration is green.

## Deviations from Plan

**1. [Rule 1 - Bug] `docs/phase7_self_check.py` crashed on non-literal dictionary keys**

- **Found during:** Task 3
- **Issue:** The first draft of the Setup Check key assertion built a set directly from every
  `WFDictionaryKey` value: `{value.get("WFDictionaryKey") for value in params}`. Some of this
  artifact's dictionary keys are `text_token()`-built dicts (the dynamic
  `exit_stats.<name>.samples` keys), which are unhashable — `TypeError: unhashable type: 'dict'`.
- **Fix:** Filter to literal string keys before building the set, with a comment stating why.
  This is also the semantically correct scope: the assertion is about two literal flat keys.
- **Files modified:** `docs/phase7_self_check.py`
- **Commit:** `0faa1c7`

No other deviation. No CLAUDE.md rule forced an adjustment, no architectural decision (Rule 4)
arose, and no authentication gate or checkpoint was reached. The hard constraints held: the
provenance guard passed before every builder run, `--target-platform all` was used throughout,
`timeout` was never invoked, `dimming()` / `silence()` / `restore_managed_settings()` / the
`settings_snapshot` subtree were untouched, nothing was renamed, `schema_version` was not
bumped, the router was not restructured, `filter.notes` was not re-patched, and
`verify_circle_zero_silence()` never fired.

## Known Stubs

None. No placeholder, hardcoded-empty, TODO or FIXME value was introduced. The one
`is.workflow.actions.nothing` added per new conditional is the project's standard balanced
otherwise-arm idiom, not a stub.

## Deferred Items

| Item | Where | Why deferred |
|---|---|---|
| The "a menu appeared on close" symptom is only half-addressed | `manual_emergency_restore()` prompt | The in-scope half — naming the fall-through case so a user who lands here unintentionally understands why — is done. The other half is a device diagnosis: the CLOSE arm provably contains no menu, so if a menu really appeared on close, the automation passed something other than `CLOSE`. Deferred to 10-05 by plan scope. |
| `docs/phase6_self_check.py` red | `docs/phase6_self_check.py:68` | Pre-existing `WFAppName` assertion vs `normalize_open_apps()`; repaired in 10-03 by design. Untouched. |
| `docs/sentient_core_check.py` red | — | Sentient is stale at `2026-08-14k`; re-forking is SEED-005, out of phase scope. Untouched. |

## Threat Flags

None. No file changed here introduces a network endpoint, an auth path, a file-access pattern
or a schema change at a trust boundary.

Register dispositions from the plan, as shipped:

- **T-10-07** (gating the wrong action) — mitigated and asserted: `filter.notes` and Create
  Note counts are 1/1, unchanged from HEAD, and `enclosing_groups()` confirms neither is
  inside the gate group.
- **T-10-08** (double-wrapping) — mitigated and demonstrated: positional probe; two
  consecutive builds byte-identical; exactly one conditional tests the flag.
- **T-10-09** (existence gate on state) — mitigated: flat reads and numeric `> 0` gates only;
  zero condition-100/101 conditionals anywhere in the Setup Check path;
  `verify_sentinel_gates()` green.
- **T-10-10** (alert contents) — accepted as planned: two booleans derived from local epochs
  plus static copy.
- **T-10-11** (overstating automation status) — mitigated in the shipped string, not in a
  comment.
- **T-10-12** (menu case-order drift) — mitigated: case titles compared element for element
  against `WFMenuItems`, and `docs/phase7_self_check.py` now pins the ten-item list.
- **T-10-13** (router restructuring) — mitigated: only the prompt string changed;
  `verify_router_shape()` passes on every build.

## Notes for the Next Plan

- **10-03**'s `docs/router_ui_census.py` should expect **ten** menu items, and should count
  the shownote as a *gated* surface rather than an unconditional one. `enclosing_groups()` is
  the right tool for that assertion and is already module-level in
  `tools/build_state_engine.py`.
- **10-04** ships an artifact whose `src/PROSOCHE-Dumb.xml` hash changed three times in this
  plan; regenerate `artifacts/shortcuts/MANIFEST.md` from the final build, not from any
  intermediate.
- **On-device UAT for this plan is three observations:** (1) choosing any menu item other than
  `Open Control Room` must not launch the Notes app; (2) `Open Control Room` still must; and
  (3) `Setup Check` must report `seen` for whichever automation has actually run — the fastest
  proof is to open a tracked app once, then run the Shortcut by hand and choose Setup Check.
  Deleting the Control Room Note and re-running manually must still recreate it, which is the
  BOOT-08 regression this gate was most at risk of breaking.

## Self-Check: PASSED

- `tools/build_state_engine.py` — FOUND
- `src/PROSOCHE-Dumb.xml` — FOUND
- `docs/phase7_self_check.py` — FOUND
- `.planning/REQUIREMENTS.md` — FOUND
- `.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-02-SUMMARY.md` — FOUND
- commit `e5b415e` — FOUND
- commit `0556efd` — FOUND
- commit `0faa1c7` — FOUND
