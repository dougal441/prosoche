---
phase: 10-ship-readiness-remainder-and-ux-lite-pass
plan: 03
subsystem: infra
tags: [python, checker-scripts, build-guard, structural-assertion, read-only, bd-06-forward-compat]

# Dependency graph
requires:
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    plan: 01
    provides: the Circle-0 silent-band conditional and enclosing_groups(), both asserted against here
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    plan: 02
    provides: gate_control_room_shownote() and Manual Show Note Requested, restated here as a census invariant
provides:
  - docs/environmental_restore_check.py — pins the cancelled brightness/volume cut
  - docs/router_ui_census.py — per-arm UI inventory plus the Circle-0-shows-nothing invariant
  - docs/sequence_dispatch_check.py — sequence-to-dispatch coverage reporter, BD-06-proof, never a gate
  - KNOWN_ORPHANS, the accepted-orphan roster (currently the single Circle 8 Voice entry)
  - A green Dumb-fork check suite — nine scripts, all exit 0 in one run
affects:
  - 10-04-PLAN.md (rebuilds both forks; these nine checks are the regression net it runs against)
  - 10-05-PLAN.md (device UAT; the census table is the shipped-surface inventory it tests against)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Cancelled-cut guard — when a subtractive change is proposed and then reversed by
      decision, the reversal leaves no artifact. Write a checker whose docstring states the
      cancellation and its dates, and whose assertions name every symbol the cut would have
      removed, so the decision is enforced rather than merely recorded"
    - "Report-and-gate in one script — print the full inventory first, then assert only the
      handful of properties that are genuinely invariant, and say in a comment which counts
      are deliberately NOT asserted and why. A checker that pins everything it can measure
      turns every legitimate edit into a false failure"
    - "Code-to-strategy resolver — when a checker must survive a planned change to a magic
      constant, never filter on the constant. Collect unconditionally, resolve semantics per
      item from the item's own value, and return an explicit unknown outcome for anything a
      rule does not recognise"
    - "Structurally-derived exemption — an assertion that is false at HEAD for a
      by-construction reason gets a named helper whose docstring states the reason, located
      by the same structural handle the generator uses, never an index or a silent skip"

key-files:
  created:
    - docs/environmental_restore_check.py
    - docs/router_ui_census.py
    - docs/sequence_dispatch_check.py
  modified:
    - docs/phase6_self_check.py

key-decisions:
  - "The Circle-0 silence assertion carries exactly one exemption — the live-cooldown
    short-circuit's true arm — derived structurally from the conditional testing
    `Cooldown Until`, with the reason in a docstring. The assertion was NOT weakened to
    artifact-wide-optional, and the exempt surface was NOT suppressed: the 'Ice is active'
    menu runs before `Circle Next` exists and is the only Emergency Restore reachable
    during a cooldown."
  - "docs/environmental_restore_check.py deliberately pins NO coercion-aggrandizement count.
    The measured 18-of-28 split is an artifact of how each operand is sourced, not a safety
    property; docs/phase9_self_check.py already owns it. The measurement is recorded in a
    comment so a reader does not mistake the 10 uncoerced volume sites for a gap."
  - "docs/router_ui_census.py imports enclosing_groups() from the generator rather than
    copying it, so there is one definition of 'what encloses what' shared by the build guard
    and the census."
  - "Both condition codes appear in docs/sequence_dispatch_check.py only inside
    match_strategy(), as dispatch arms on a code read from a conditional. Neither exists as
    a module-level constant, so BD-06's move from contains to exact matching needs no edit
    to this file."
  - "docs/phase6_self_check.py's stale term was DROPPED with a comment citing
    normalize_open_apps() by name and line, and the diff is confined to that one assertion
    plus the comment — so the change is auditable as a correction, not a concession."

requirements-completed: [AUDIT-03, AUDIT-04, SESS-07, CIRC-03, CIRC-05, SAFE-01, SAFE-02, SAFE-03, SAFE-05]

# Metrics
duration: ~20 minutes
completed: 2026-08-17
tasks-completed: 3
tasks-total: 3
files-modified: 4
status: complete
---

# Phase 10 Plan 03: Guards — pinning the cancelled cut, the silent band, and the dispatch surface Summary

Three properties that were true but unguarded are now automated checks — the cancelled brightness/volume machinery, the Circle-0 silent band's enclosure of every OPEN-arm surface, and the Config-sequences-to-dispatch coverage — and the one checker that was red at `HEAD` is repaired, leaving the nine-script Dumb-fork suite green in a single run.

## What Was Built

**Task 1 — `docs/environmental_restore_check.py`** (commit `b18d415`)

A read-only guard in the `docs/phase7_self_check.py` house skeleton — `from __future__` annotations, `ROOT` from `parents[1]`, a local `require()` raising `AssertionError`, one printed passed line, the standard name-guard — that loads the generator by `importlib` spec so its assertions inspect real module attributes rather than grep strings. No `subprocess`, no rebuild.

Its docstring states the reason it exists in plain terms: the brightness/volume cut was **proposed and cancelled by user decision on 2026-08-16, reaffirmed 2026-08-17**; Dimming and Silence stay as distinct Circles with working capture-and-restore; this file makes a re-attempt fail loudly. It cites **BD-02** and **BD-03**.

*Source-level, against the imported module:*

| Assertion | Detail |
|---|---|
| Ten symbols exist and are callable | `device_detail`, `set_brightness`, `set_media_volume`, `clear_snapshot`, `restore_managed_settings`, `dimming`, `silence`, `seed_settings_snapshot`, `verify_state_seed`, `verify_restore_gates` |
| `NUMERIC_OPERAND_FIELDS` entries | `is.workflow.actions.setbrightness → WFBrightness` and `is.workflow.actions.setvolume → WFVolume` — the exact exemption the cut would have introduced, whose absence reintroduces the Phase 9 silent-no-op defect |
| SAFE-05 | `inspect.getsource(manual_emergency_restore)` contains `restore_managed_settings` |
| SESS-07 | `inspect.getsource(close_pipeline)` contains `restore_managed_settings` |

*Artifact-level, against the parsed `src/PROSOCHE-Dumb.xml`:*

- Site counts **14 / 14 / 20** (`setbrightness` / `setvolume` / `getdevicedetails`), with the derivation in a comment: four `restore_managed_settings()` expansions contribute one brightness plus one volume each; ten `primitive_dispatch()` renderings contribute one `dimming()` plus one `silence()` each, and those two supply all twenty device-detail reads.
- **SAFE-02 structurally:** every one of the 14 `setvolume` actions carries `WFVolumeSetting = "Media"`. Measured distribution: `Counter({'Media': 14})`.
- Every `getdevicedetails` reads only `Current Brightness` or `Current Volume`. Measured: 10 of each.
- The bootstrap template still seeds the `settings_snapshot` subtree with `brightness.original_value` and `volume.original_value` (parsed with `verify_state_seed()`'s own placeholder-substitution trick).
- **SAFE-01/SAFE-02 as configured:** `safety.dim_target` (0.12) is strictly positive and `>= safety.brightness_floor` (0.10); `safety.allow_volume_increase is False`. A comment records that **BD-02's Phase 9 addendum** relaxed the historical 10–15% band on this fork, which is why the assertion is strictly-positive-plus-floor rather than a pinned band, and that capture-and-restore is the safety mechanism rather than floor avoidance.
- Both the Config literal and the state template are located **by content**, not by action index.

*Cross-fork:* `tools/build_sentient.py` is loaded by spec, proving its twelve `verify_*` / `normalise_*` imports from `build_state_engine` all still resolve.

A comment records the deliberate non-assertion: 14 of 14 brightness sites and 4 of 14 volume sites carry a coercion aggrandizement, the other 10 volume sites being fed by the already-`Number`-typed `Silence Target` that `normalise_numeric_operands()` skips by design.

**Task 2 — `docs/router_ui_census.py`** (commit `169f233`)

Derives the three arm spans from control-flow structure only: the two mode-0 conditionals whose `WFInput` variable is `Input Key` and whose `WFConditionalActionString` is `OPEN` / `CLOSE`, then their matching mode-1 and mode-2 endpoints looked up by `GroupingIdentifier`. It fails with its own message if either conditional is missing, so a future router restructure surfaces here rather than producing a silently empty census. Measured spans at `HEAD`: OPEN `93–1217`, CLOSE `1220–1350`, MANUAL `1351–3716`.

Printed census (nine counted identifiers × three arms; `choosefrommenu` counted at mode 0 only):

```
identifier                                OPEN   CLOSE  MANUAL
is.workflow.actions.choosefrommenu          10       0      13
is.workflow.actions.ask                      6       0      18
is.workflow.actions.alert                    8       1      56
is.workflow.actions.notification             0       1       0
is.workflow.actions.choosefromlist           1       0       0
is.workflow.actions.speaktext                1       0       9
is.workflow.actions.shownote                 0       0       1
is.workflow.actions.filter.notes             0       0       1
com.apple.mobilenotes.SharingExtension       0       0       1
```

Five assertion groups: the CLOSE arm holds zero mode-0 menus, zero `ask` and zero `choosefromlist`; the OPEN arm emits zero notifications and the artifact holds exactly one, inside CLOSE; the MANUAL arm holds exactly one `shownote`, one `filter.notes` and one Notes-create; **every counted OPEN-arm surface is enclosed by the `Circle Next > 0` silent-band group**, reported on failure by identifier plus nearest preceding comment; and the MANUAL `shownote` is enclosed by a `Manual Show Note Requested` conditional. `enclosing_groups()` is imported from the generator rather than copied. A comment states that absolute OPEN/MANUAL counts are deliberately not pinned, because the Test-a-Circle submenu renders the full dispatch nine times and pinning that number would make every future primitive edit a check failure.

**Task 3 — `docs/sequence_dispatch_check.py` plus the `phase6` repair** (commit `a6e7663`)

*The reporter.* Collects every distinct component of every entry in every `sequences` array, splitting unconditionally on `+` (the split of a name with no `+` is the name itself, so no branch is needed today or after BD-06 Decision 5). Independently collects **every** mode-0 conditional whose `WFInput` variable is `Selected Primitive` — 80 of them, 8 distinct names — with no filtering by condition code, resolving each branch's matching rule from its own code through `match_strategy()`. Prints three labelled lists and a summary line, and **exits 0 in every case**:

```
dispatch surface: 80 branch(es) testing 'Selected Primitive', 8 distinct name(s); 9 distinct sequence component(s)

ORPHANS -- sequence entries that dispatch nothing:
  Voice: Classic (Circle 8), BlackMirror (Circle 8), Ambient (Circle 8) -- KNOWN OPEN DEFECT, owned by .planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md

UNREACHABLE -- dispatch branches no sequence entry names:
  (none)

UNKNOWN MATCH SEMANTICS -- branches whose condition code neither rule knows:
  (none)

sequence dispatch check: 1 orphan(s) (0 unexpected), 0 unreachable, 0 of unknown semantics -- reported, not gated
```

The docstring opens by stating that this is a reporting script and not a gate, why exiting 0 on the Voice orphan is required by the ROADMAP rather than a concession, and that a future phase may promote it to a build guard once the roster and matching strategy have settled under BD-06.

*The repair.* `docs/phase6_self_check.py:68` required `WFAppName` on every `openapp` route. `normalize_open_apps()` clears an `openapp` action's parameters outright and re-emits only `open_app()`'s two keys, `WFAppIdentifier` and `WFSelectedApp` — so the term contradicted the generator by construction. The term was dropped, the `WFSelectedApp` term kept, and a six-line comment cites `normalize_open_apps()` by name and line so the next reader can see the change is a correction rather than a weakening.

## Verification Evidence

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit 0 — run before every builder invocation |
| `python3 docs/sequence_dispatch_check.py` | exit 0, three labelled lists + summary |
| `python3 docs/phase6_self_check.py` | `phase6 self-check: passed` |
| `python3 docs/phase5_self_check.py` | `phase5 self-check: passed` |
| `python3 docs/phase7_self_check.py` | `phase7 self-check: passed` |
| `python3 docs/phase9_self_check.py` | `phase9 self-check: passed` (28/28 sites, 18 coerced, 10 correctly not) |
| `python3 docs/state_engine_self_check.py` | exit 0 |
| `python3 docs/sentient_audit_check.py` | `compact prompt, one challenge, bounded fallback` |
| `python3 docs/environmental_restore_check.py` | `environmental restore check: passed` |
| `python3 docs/router_ui_census.py` | census table + `router UI census: passed` |
| `import build_sentient` smoke test | `sentient import ok` |
| Two consecutive `router_ui_census.py` runs | byte-identical output |
| `grep -c subprocess` on all three new scripts | 0 |
| `grep -v '^#' … \| grep -c restore_managed_settings` (Task 1) | **6** (≥ 3 required) |
| `grep -v '^#' … \| grep -c GroupingIdentifier` (Task 2) | **8** (≥ 1 required) |
| `git diff --stat docs/phase6_self_check.py` | `1 file changed, 8 insertions(+), 1 deletion(-)` — the assertion line plus its comment, nothing else |
| `git status --short` after every control | `src/PROSOCHE-Dumb.xml` and `tools/build_state_engine.py` byte-identical to `HEAD` |

`docs/sentient_core_check.py` was **not** run as a gate, per the plan and the phase brief: it passes at the phase's starting `HEAD` and is red only transiently, from 10-01's first Dumb rebuild until 10-04 rebuilds Sentient from the same generator. Gating on it here would fail on a known, temporary fork skew.

### Negative controls

Every control was run against real files, and every restoration was confirmed green.

**Task 1, control A — the `setvolume` coercion table entry.** The `is.workflow.actions.setvolume` row was deleted from the real `NUMERIC_OPERAND_FIELDS` and reverted from a backup:

```
AssertionError: NUMERIC_OPERAND_FIELDS has no is.workflow.actions.setvolume entry --
a variable-fed Set Volume would lose its numeric coercion and silently no-op
EXIT=1
```

Restored → `environmental restore check: passed`.

**Task 1, control B — `restore_managed_settings` renamed.** `def restore_managed_settings(` became `def restore_managed_settings_RENAMED(`:

```
AssertionError: the brightness/volume cut is CANCELLED, but restore_managed_settings()
is gone from build_state_engine.py -- restore it or revert the change that removed it
```

Restored → `environmental restore check: passed`, and `git diff --stat tools/build_state_engine.py` empty.

**Task 2 — an OPEN-arm alert hoisted out of the silent band.** `open_pipeline()` was edited to pop the first `alert` out of `universal_leaving()` and emit it immediately *before* `silent_if`, then rebuilt:

```
AssertionError: OPEN-arm surface(s) outside the Circle-0 silent band, so a Circle-0
open would show something: is.workflow.actions.alert near 'Circle 0 is the silent
band: state has already been saved directly above, and nothing at all is shown below it.'
```

The failure names the identifier and the nearest preceding comment, as required. Generator and artifact were restored from backup, rebuilt (`BUILD OK`), and `git status --short` showed only the new untracked script — so the artifact returned byte-identical to `HEAD`. `router_ui_census.py`, `phase7`, `state_engine` and `phase9` all green again.

**Task 3 — an unmatched primitive name.** A scratch copy of the artifact was made with `"Knock"` renamed to `"Knokk"` in the `Classic` sequence, and the script pointed at it:

```
  Knokk: Classic (Circle 1) -- UNEXPECTED -- not in KNOWN_ORPHANS
  Voice: Classic (Circle 8), BlackMirror (Circle 8), Ambient (Circle 8) -- KNOWN OPEN DEFECT, owned by …
sequence dispatch check: 2 orphan(s) (1 unexpected), 0 unreachable, 0 of unknown semantics -- reported, not gated
EXIT=0 (main returned normally)
```

The unknown orphan is reported, clearly marked as unexpected, and the run still exits 0. The real source was never touched; re-running against it returned to `1 orphan(s) (0 unexpected)`.

### BD-06 forward compatibility — the three structural assertions

Run by importing `docs/sequence_dispatch_check.py` as a module:

| # | Assertion | Outcome |
|---|---|---|
| (i) | No module-level attribute equals the contains code as a bare int or holds it in a collection (recursive walk over ints, lists, tuples, sets and dicts, `bool` excluded) | **PASSED** — offender list empty |
| (ii) | The code→strategy resolver returns three distinct results, the third being the unknown outcome | **PASSED** — `match_strategy(99)='contains'`, `match_strategy(4)='exact'`, `match_strategy(1003)='unknown'` |
| (iii) | No conditional is excluded from collection on the basis of its code | **PASSED** — `collect_dispatch_branches()` returned **80**, equal to the 80 mode-0 conditionals whose `WFInput` variable is `Selected Primitive` |

### Manual review — every line containing either condition code

`grep -n -E '(^|[^0-9])(99|4)([^0-9]|$)' docs/sequence_dispatch_check.py` returns exactly three lines:

| Line | Text | Kind |
|---|---|---|
| 17 | ``` `primitive_dispatch()` from condition code 99 ("contains") to condition code 4 ("string ``` | Docstring prose citing BD-06 Decision 5. Not a comparison, not a constant — it explains why the file avoids presuming a code. |
| 68 | `    if code == 99:  # "contains": the tested string need only appear inside the entry` | **Dispatch arm on a code read from a conditional.** `code` is `WFCondition` taken off the artifact and passed in by `collect_dispatch_branches()`; the arm answers "what does *this* conditional mean", it does not assume any conditional carries 99. |
| 70 | `    if code == 4:   # "string is": the tested string must equal the entry exactly` | **Dispatch arm on a code read from a conditional**, identical reasoning. This is the arm BD-06 Decision 5 will start exercising. |

No line of the second kind (a comparison presuming a code) exists, so nothing needed rewriting.

## Deviations from Plan

**1. [Rule 3 - Blocking] The Circle-0 silence assertion needed one by-construction exemption**

- **Found during:** Task 2
- **Issue:** The plan specified the assertion as "every one of the counted user-facing actions inside the OPEN arm is enclosed by the silent-band conditional group." Measured at `HEAD`, that is false for exactly one action: the mode-0 `choosefrommenu` at index 171, the `"Ice is active"` menu emitted by `live_ice_redirect()`. Written literally, the assertion would have failed on the first run and there would have been no honest way to reach green except by weakening it.
- **Why it is legitimately exempt:** `install_cooldown_branches()` places `live_ice_redirect()` in the **true arm** of the conditional testing `Cooldown Until`, which short-circuits the run *before* any Heat/Pressure/Circle arithmetic. `Circle Next` does not exist yet on that path, so the silent band cannot enclose anything there. That menu is also the only route to Emergency Restore during an active cooldown, so suppressing it would strand a user left dim or silent — the precise SAFE-05 failure Task 1 guards against.
- **Fix:** a named helper, `live_cooldown_arm()`, returning the span from the `Cooldown Until` mode-0 conditional to its matching mode-1 endpoint. It is located by the tested variable name — the same structural handle `install_cooldown_branches()` uses — never by index, and its docstring states the reason in full. This is the same discipline 10-01 established for `verify_circle_zero_silence()`'s Test-a-Circle exemption: a documented, structurally-derived carve-out with the by-construction reason recorded, rather than a scope reduction. Measured: the exempt span holds exactly one counted surface, and with it excluded there are **zero** OPEN-arm surfaces outside the band.
- **Files modified:** `docs/router_ui_census.py`
- **Commit:** `169f233`

No other deviation. No CLAUDE.md rule forced an adjustment, no architectural decision (Rule 4) arose, no authentication gate or checkpoint was reached. The hard constraints held: the provenance guard passed before every builder invocation; `--target-platform ios` was never used; `timeout` was never invoked; `dimming()`, `silence()`, `restore_managed_settings()` and `settings_snapshot` were not removed or stubbed — this plan's whole purpose on that axis is to pin them; nothing was renamed (the two rename/delete edits were negative controls, both reverted and both verified byte-identical to `HEAD`); `verify_circle_zero_silence()` and `gate_control_room_shownote()` were not touched; and `docs/sentient_core_check.py` was neither weakened nor "fixed" by rebuilding Sentient, which 10-04 owns.

## Known Stubs

None. No placeholder, hardcoded-empty, `TODO` or `FIXME` value was introduced in any of the three new scripts.

`KNOWN_ORPHANS` is not a stub. It is a deliberate, ROADMAP-mandated roster of accepted defects owned elsewhere; its single entry points at
`.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md`, and an orphan absent from it is still reported and marked `UNEXPECTED`.

## Deferred Items

| Item | Where | Why deferred |
|---|---|---|
| Circle 8 dispatches nothing — the `"Voice"` entry matches no branch | `src/PROSOCHE-Dumb.xml` Config `sequences`, all three arrays at position 8 | Explicitly out of scope: the ROADMAP names it a known open defect a later phase fixes, and instructs any sequence/dispatch checker to record it rather than fail on it. Now reported by name with its Circle positions and its owning todo on every run, which is strictly better than the silence it had before. |
| `docs/sequence_dispatch_check.py` is a reporter, not a build guard | — | Promoting it requires the primitive roster and the matching strategy to settle under BD-06 Decisions 3–5. Under exact matching an unmatched entry becomes a build-time failure in the generator itself, at which point this script's gate role is largely absorbed. Stated in its docstring. |
| `docs/sentient_core_check.py` red | — | Transient fork skew only: green at the phase's starting `HEAD`, red from 10-01's Dumb rebuild until 10-04 rebuilds Sentient from the same generator. Deliberately excluded from this plan's gate; 10-04 owns it. Untouched. |
| Canonical strategy §10.5 still prints the pre-rise threshold arrays | `PROSOCHE_Nine_Circles_Canonical_Strategy.md:1178, 1184, 1190` | Carried forward from 10-01. Out of this plan's scope; worth a one-line correction in a later documentation pass. |

## Threat Flags

None. No file changed in this plan introduces a network endpoint, auth path, file-access pattern, or schema change at a trust boundary. All three new scripts are strictly read-only: no `subprocess`, no rebuild, no writes.

Register dispositions from the plan, as shipped:

- **T-10-14** (`restore_managed_settings()` removed from `manual_emergency_restore()`) — mitigated by source inspection with a demonstrated negative control (control B).
- **T-10-15** (removed from `close_pipeline()`) — mitigated by the same source-inspection assertion; control B's rename fires on the attribute assertion first, so both call-site assertions share the demonstrated failure path.
- **T-10-16** (`NUMERIC_OPERAND_FIELDS` losing an entry) — mitigated, both entries pinned, control A demonstrated on the volume entry specifically.
- **T-10-17** (ringer write, or a non-positive dim target) — mitigated structurally: all 14 volume writes measured `WFVolumeSetting = "Media"`; `dim_target` 0.12 asserted strictly positive and at or above `brightness_floor` 0.10.
- **T-10-18** (a surface reintroduced into the Circle-0 silent band) — mitigated with a demonstrated negative control that names the offending identifier and its nearest comment.
- **T-10-19** (a sequence entry that dispatches nothing) — **accepted as planned**: reported by name with its Circle positions and owning todo, exit 0 by design.
- **T-10-20** (a checker weakened to reach green) — mitigated: the `phase6` diff is 8 insertions / 1 deletion, confined to the one assertion plus a comment citing `normalize_open_apps()` by name and line, so the change is auditable as a correction.

## Notes for the Next Plan

- **10-04** runs the builder for both forks. The regression net is now **nine** scripts, and every one of them must be green after the Sentient rebuild — including `docs/sentient_core_check.py`, which 10-04 returns to green. `docs/phase9_self_check.py` audits **both** forks' 28 sites, so a Sentient rebuild that drops a coercion will surface there, and `docs/environmental_restore_check.py`'s cross-fork smoke test will catch a `build_sentient.py` import that stops resolving.
- **`docs/environmental_restore_check.py` will need its three site counts revisited only if the number of `restore_managed_settings()` call sites or `primitive_dispatch()` renderings changes** — the derivation is in a comment above `EXPECTED_SITES` precisely so a future editor changes the number for a stated reason rather than to make the check pass.
- **10-05**'s UAT can use the census table directly as the shipped-surface inventory: OPEN offers 10 menus / 6 prompts / 8 alerts, CLOSE shows exactly one alert and one notification and asks nothing, MANUAL is everything else. A device observation that contradicts a row in that table is a real finding, not a measurement error.
- **BD-06 work, whenever it lands,** should confirm `docs/sequence_dispatch_check.py` still runs unedited after the switch to condition 4 and the removal of the combined entries. Expected behaviour: the three combined `BlackMirror` entries disappear, `match_strategy()` starts returning `exact` for every branch, and the `Voice` orphan resolves once its branch is emitted — at which point `KNOWN_ORPHANS` should empty and the script becomes a candidate build guard.

## Self-Check: PASSED

- `docs/environmental_restore_check.py` — FOUND
- `docs/router_ui_census.py` — FOUND
- `docs/sequence_dispatch_check.py` — FOUND
- `docs/phase6_self_check.py` — FOUND
- commit `b18d415` — FOUND
- commit `169f233` — FOUND
- commit `a6e7663` — FOUND
