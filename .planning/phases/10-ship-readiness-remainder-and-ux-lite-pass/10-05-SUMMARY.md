---
phase: 10-ship-readiness-remainder-and-ux-lite-pass
plan: 05
subsystem: infra
tags: [uat, device-verification, dist-03, deferred-blocker, test-authoring]

# Dependency graph
requires:
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    plan: 01
    provides: Circle 0 and the raised thresholds — Tests 1 and 2's subject
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    plan: 02
    provides: the gated shownote, Setup Check and the reworded prompts — Tests 4, 5, 6 and 7's subject
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    plan: 03
    provides: docs/router_ui_census.py, whose per-arm table is embedded as the shipped-surface inventory
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    plan: 04
    provides: the signed Dumb artifact this file's header pins by SHA-256 and byte size
provides:
  - .planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md — ten device tests plus an unnumbered re-import step, runnable cold
  - A recorded, verbatim DIST-03 blocker for Phase 10, with every outcome field left blank
  - The predictive arithmetic table (heat/gravity/pressure/thresholds) a tester needs to predict a number before observing it
affects:
  - Phase seal — Phase 10 seals with this block explicitly outstanding
  - DIST-03, which stays unchecked in .planning/REQUIREMENTS.md

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Predict-then-observe UAT — embed the shipped arithmetic (thresholds, heat rules,
      gravity divisor) in the test document itself, so a tester computes the expected
      number before the device produces one. A test whose expectation is written after
      the observation cannot fail"
    - "Name the setup step the feature does not perform — Reset Today zeroes opens_today
      and gravity but NOT heat, so the cold-day precondition is stated as a measured
      gate on heat rather than assumed from the menu item's name"
    - "Blocked is a recorded outcome, not an absence — the standing note names the three
      substitutions that are forbidden (Mac import, simulator, decrypted-artifact
      inference) rather than merely omitting them"

key-files:
  created:
    - .planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md
  modified:
    - .planning/STATE.md
    - .planning/ROADMAP.md

key-decisions:
  - "The checkpoint resolved to the plan's own `blocked` branch. `xcrun devicectl list
    devices` returned `No devices found.`, so no test was run, every outcome field is
    blank, and DIST-03 stays unchecked. No Mac import, simulator run, or inference from
    10-04's decrypted artifact was substituted for a device observation."
  - "Test 1's setup was corrected against the generator rather than transcribed from the
    plan. `Reset Today` zeroes opens_today and gravity only — heat is untouched and decays
    at −1 per 600 s since last_close_at. The test therefore gates on a MEASURED heat value
    (heat <= 1 under Limbo) before the open, instead of assuming Reset Today produces a
    cold day. Written as the plan intended it would have produced a test that silently
    measured nothing on any device with warm heat."
  - "Test 1 reads state.json directly for heat, opens_today and active_session, because the
    Status alert does not carry them — it shows Fork, Profile, Sequence, Voice, Circle,
    Pressure and Cool-down only. The plan's 'expect Pressure and the open count to have
    moved' via Status is half unobservable there."
  - "Tests 9 and 10 were split as apply-and-capture / restore rather than merged, because a
    manual `Test a Circle` creates no session and therefore no CLOSE can ever reach the
    restore. Emergency Restore is the only recovery path from a manual dim, and the file
    says so — a merged test would have implied a round trip that cannot occur on that path."
  - "Circle 8 (Voice, Classic) is named in the header as a known open defect so a tester does
    not report the orphan as a UAT failure, and no test fires Circle 8."

requirements-completed: []

# Metrics
duration: ~20 minutes
completed: 2026-08-17
tasks-completed: 1
tasks-total: 2
files-modified: 3
status: blocked-at-checkpoint
---

# Phase 10 Plan 05: The deferred device-verification block Summary

Every device-dependent criterion Phase 10 produced now lives in one self-contained file — ten tests plus an unnumbered re-import step, each pinned to the exact signed artifact by SHA-256, each carrying its own failure evidence — and the checkpoint resolved to the plan's `blocked` branch, because `xcrun devicectl list devices` returned `No devices found.`

## What Was Built

### Task 1 — `10-UAT.md` (commit `c25656f`)

A 498-line, self-contained UAT document in the shape of the Phase 9 file, written so a human with the device in hand can run it cold without reading any other artifact in the repository.

**The header pins the build.** `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut`, **193,498 bytes**, `47957dbf429bd2d5671b69d87d8510b08abf70bbe1cfca8975a192c96bcb6324` — both values copied from the `Dumb signed` row of `artifacts/shortcuts/MANIFEST.md` and independently confirmed against disk with `shasum -a 256` and `stat -f%z` before writing. It states plainly that **every test is blocked on DIST-03 while no device is connected**, names the two Personal Automations and the exact literals they must pass (`OPEN` / `CLOSE`), and records that **no test in this file needs an Apple-Intelligence-capable iPhone** — the Dumb fork contains no `Use Model` call, so the 15 Pro-and-later requirement does not apply to any test here.

**Step 0 is a re-import step, deliberately not numbered as a test and carrying no outcome field.** It states that `state.json` and the Control Room Note both survive a re-import — neither lives inside the shortcut — so no test needs a fresh install and no accumulated behavioural state is lost. It also carries 10-04's measured fact as the diagnosis for a duplicate library entry: a signed `.shortcut` carries **no display name inside it**, so a second entry is always a filename problem, never a build problem.

**Four reference blocks were added so the tests are runnable cold**, each derived from the artifact or generator at this build rather than from memory:

1. **Where to read state** — `Files → iCloud Drive → Shortcuts → PROSOCHE → state.json`, from the generator's `WFFileDestinationPath`. Needed because the `Status` alert does *not* show `heat`, `opens_today` or `active_session`.
2. **The manual menu in shipped order**, all ten items.
3. **The arithmetic**, read out of the built Config literal: `pressure = heat + gravity`; `gravity = floor(opens_today / 6)` capped at 5; heat decay −1 per 600 s, `open_base` +1, exclusive reopen bonus +2 under 120 s / +1 under 600 s, floor 0 cap 30; and all three raised threshold arrays with their Circle-1 entry points. A tester can now predict the number before the device produces one.
4. **The shipped-surface census** from `docs/router_ui_census.py`, re-run at this build — OPEN 10 menus / 6 asks / 8 alerts / **0 notifications**; CLOSE **0 menus / 0 asks** / 1 alert / 1 notification; MANUAL the rest — with the standing instruction that a device observation contradicting a row is a real finding.

**The ten tests**, each with a setup, an exact tap or trigger sequence, an exact expected observation, the named failure evidence, and a blank `outcome:` field:

| # | Test | The claim it settles |
|---|---|---|
| 1 | Silent band, first open of a behavioural day | The phase's headline claim — nothing on screen, everything in the record |
| 2 | Band exit — how many opens | The tuning signal the raised thresholds exist to produce |
| 3 | No notification on OPEN | The removed unconditional OPEN notification |
| 4 | Control Room note-show, positive leg | The cycle-16 `filter.notes` fix's behavioural confirmation |
| 5 | Control Room note-show, negative leg | The new `shownote` gate's regression check |
| 6 | Setup Check | Whether the derived verdicts match `state.json` |
| 7 | Manual menu prompt | A human comprehension claim, recorded as judgement |
| 8 | No menu on CLOSE | The router fall-through diagnosis |
| 9 | Dimming and Silence, capture and apply | A smoke check on the re-signed Phase 9 path |
| 10 | Emergency Restore | SAFE-05's behavioural confirmation |

**Test 8's diagnostic is the point of Test 8.** It names the Automation B `Run Shortcut` input-field screenshot as the required failure evidence — verbatim, including trailing whitespace and autocorrect substitution — and states that the CLOSE arm provably contains no menu, so a menu there means the input did not match the literal and the run fell through to manual control **by design** (DEV-02).

**Test 9 links `09-UAT.md` and explicitly does not replace it.** It names all six outstanding failure-mode trials those twelve tests own (force-quit mid-session, restart mid-session, CLOSE never firing, overlapping sessions, the compound overlap-plus-force-quit, the DEV-06 cross-check) and states that passing the smoke check says nothing about any of them.

**The closing note forbids the three substitutions by name** — a Mac import, a simulator run, and any inference from 10-04's decrypted artifact — and gives the reason: the decrypt evidence proves **structure, never behaviour**, and Test 4's note picker is precisely the class of iOS interactive-fallback behaviour that is invisible to every file-level channel the project has (not the validator, not the ToolKit catalog, not AEA1 decryption).

**A results table** closes the file with one row per test and an empty Outcome column, plus a dedicated line for the Test 2 opens count, currently `_not measured_`.

### Task 2 — the checkpoint: `blocked`

`xcrun devicectl list devices` was run. Verbatim output:

```
No devices found.
```

This is the live DIST-03 blocker, unchanged since Phase 8 and identical to what stalled the Phase 9 UAT at one of twelve. Per the plan's own `how-to-verify` step 2, **no test was run.**

## Checkpoint Outcome — recorded, not worked around

Exactly one of the three sanctioned outcomes applies: **the device was unavailable and every outcome field is still blank, with the DIST-03 blocker recorded.**

- **No outcome field in `10-UAT.md` is filled.** All ten `outcome:` fields are blank, the results table's Outcome column is empty, the Test 2 opens count reads `_not measured_`, the Summary block reads `passed: 0 / blocked: 10`, and the Verdict section is an explicit placeholder.
- **DIST-03 remains unchecked** in `.planning/REQUIREMENTS.md` — `- [ ] **DIST-03**` at line 161, and `Pending` in the traceability table at line 331. Neither was touched by this plan.
- **No Mac import, simulator run, or decrypted-artifact inference was substituted for a device observation.** No shortcut was imported anywhere. No simulator was launched. 10-04's nine-of-nine structural assertions against the recovered plists were cited in the UAT header as the shipped-surface inventory's provenance, and explicitly disclaimed in the closing note as **not** device evidence. Nothing in this plan is device evidence.
- **No criterion was marked passed on non-device evidence.** This is the T-10-28 repudiation threat the plan registers at high severity, and the `blocked` branch is its mitigation, not its failure mode.

This is a legitimate, recorded outcome and is the precedent set by the 2026-08-16 breadcrumb-strip quick task (`.planning/quick/260816-ukb-strip-the-open-bisect-debug-breadcrumb-s/`, coverage item D5) and by Phase 9 Plan 02.

## Verification Evidence

| Check | Result |
|---|---|
| Precondition: signed Dumb artifact exists, non-empty, exact display name | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut`, `-rw-------`, **193,498 bytes**, no suffix |
| Independent `shasum -a 256` on that file | `47957dbf429bd2d5671b69d87d8510b08abf70bbe1cfca8975a192c96bcb6324` |
| Header SHA-256 and bytes vs the MANIFEST `Dumb signed` row | both present in `artifacts/shortcuts/MANIFEST.md`, exact string match |
| Plan's automated `<verify>` | `uat authored` |
| Numbered tests (`^### \d+\. `) | **10** |
| Re-import step numbered as a test | **No** — `### Step 0 — Re-import the artifact (setup, not a test)`, no outcome field |
| `DIST-03` present in the file | yes, in the header block and the closing note |
| `09-UAT.md` linked | yes, in Test 9 with its full path |
| `Expected` occurrences | 11 |
| Blank `outcome:` fields | 10, one per test |
| `xcrun devicectl list devices` | `No devices found.` |
| `python3 docs/router_ui_census.py` (source of the census table) | `router UI census: passed` |
| `python3 docs/environmental_restore_check.py` (Tests 9/10 provenance) | `environmental restore check: passed` |
| `--target-platform ios` | never invoked in this plan |
| `timeout` | never invoked in this plan |
| Guards from waves 1–4 | none touched — this plan changed no source file, no generator, no checker |

## Deviations from Plan

**1. [Rule 1 - Bug] Test 1's setup as written would have measured nothing on a warm device**

- **Found during:** Task 1, writing Test 1.
- **Issue:** The plan directed "With state reset for today via the manual menu's Reset Today, open a tracked app once." Read from the generator, `Reset Today` zeroes `opens_today` and `gravity` and **nothing else** — `heat` is untouched and only ever decays, at −1 per full 600 s since `last_close_at`. On a device with `heat` at, say, 5, a post-`Reset Today` open lands at `pressure` 6 and produces Circle 3 under Limbo, so the test would have shown a surface and been recorded as a silent-band failure when the band was working correctly.
- **Fix:** Test 1's setup now reads `heat` out of `state.json` and gates on it — under Limbo the test is only meaningful at `heat ≤ 1` — with an explicit wait instruction (`10 × (heat − 1)` minutes) and a fallback to recording the actual starting heat and adjusting the predicted pressure. It also adds a `cooldown_until == null` precondition, because a live cool-down short-circuits the OPEN pipeline before any Heat arithmetic and would likewise make the test measure nothing.
- **Files modified:** `.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md`
- **Commit:** `c25656f`

**2. [Rule 2 - Missing critical functionality] Test 1's observations were split between the Status alert and `state.json`**

- **Found during:** Task 1, writing Test 1.
- **Issue:** The plan directed "choose Status; expect Pressure and the open count to have moved". The `Status` alert carries Fork, Profile, Sequence, Voice, Circle, Pressure and Cool-down — it does **not** carry `heat`, `opens_today` or `active_session`. Half the carried-forward observation ("`state.json` shows `heat` 1, `pressure` 1, `circle` 0, an incremented `opens_today`, and a live `active_session`") is simply not visible from Status.
- **Fix:** the header gained a "Where to read state" block naming the exact `state.json` path from the generator's `WFFileDestinationPath`, and Test 1 splits its expected observation into the Status alert (Circle 0 with its gloss, Pressure) and the file (`heat`, `gravity`, `pressure`, `circle`, `opens_today`, `last_open_at`, `active_session`). Tests 6, 9 and 10 use the same block.
- **Files modified:** `.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md`
- **Commit:** `c25656f`

**3. [Rule 2 - Missing critical functionality] Tests 9 and 10 were split rather than merged, because a manual `Test a Circle` has no restore path except Emergency Restore**

- **Found during:** Task 1, writing Test 9.
- **Issue:** The plan directed Test 9 to "fire the Dimming Circle and then the Silence Circle, and confirm the device returns to its original brightness and volume afterwards." `restore_managed_settings()` has exactly four call sites: the CLOSE path (against `Reloaded State`), the live-Ice branch, the cool-down-expiry branch on OPEN, and manual `Emergency Restore`. A manual `Test a Circle` creates no session, so no CLOSE will ever own it and no restore fires on its own. Written as directed, Test 9 would have failed on a correctly behaving device.
- **Fix:** Test 9 covers apply-and-capture (including the `settings_snapshot.*.original_value` typed-capture check that Phase 9 test 3 owns) and states plainly that the change is deliberately left outstanding; Test 10 is the recovery via Emergency Restore, which is also SAFE-05's confirmation and the plan's own Test 10. The session-driven round trip is named as Phase 9 UAT test 5's job.
- **Files modified:** `.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md`
- **Commit:** `c25656f`

**4. [Rule 2 - Missing critical functionality] The Circle 8 orphan was named in the header so it is not reported as a UAT failure**

- **Found during:** Task 1, writing the sequence reference block.
- **Issue:** Under Classic, Circle 8 is `Voice`, which dispatches nothing — a known open defect owned by `.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md` and reported by `docs/sequence_dispatch_check.py` on every run. A tester using `Test a Circle` on Circle 8 would observe nothing and reasonably file it as a new failure.
- **Fix:** a callout in the header names the defect, names its owning todo, and states that no test in this file fires Circle 8.
- **Files modified:** `.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md`
- **Commit:** `c25656f`

No other deviation. No architectural decision (Rule 4) arose, no authentication gate was reached, and no package-manager install was attempted.

**Hard constraints, as held:** `--target-platform ios` was never invoked (no validator run was needed — this plan changed no plist); `timeout` appears in no command; nothing was renamed; no guard from waves 1–4 was weakened or touched; DIST-03 was not marked complete.

## Known Stubs

None in code — this plan created one markdown file and changed no source, no generator and no checker.

The ten blank `outcome:` fields in `10-UAT.md` are **not** stubs. They are the recorded state of an unrun device test, and filling them without a device is the exact repudiation threat (T-10-28) the file exists to prevent. They are tracked below as a deferred item, not as a defect.

## Deferred Items

| Item | Where | Why deferred |
|---|---|---|
| **DIST-03 — all ten Phase 10 device tests** | `.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md` | `xcrun devicectl list devices` → `No devices found.` Every outcome blank; DIST-03 unchecked at `.planning/REQUIREMENTS.md:161`. |
| **Phase 9's twelve-test UAT — eleven still outstanding** | `.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md` | Only test 1 (the coercion-chip hard gate) has ever passed. Tests 2–12 own the dimming/silence failure-mode trials — clean baseline, typed capture, the `WFBrightness = 0.0` observed floor, the capture→apply→restore round trip, force-quit mid-session, restart mid-session, CLOSE never firing, two overlapping sessions, the compound overlap-plus-force-quit trial, Emergency Restore recovery from each, and the DEV-06 prediction cross-check. Same device blocker. Phase 10 Test 9 is a smoke check and explicitly does not replace them. |
| **Phase 4 UAT tests 1 and 3–6** | Phase 4's UAT record | Carried forward from earlier phases, same device blocker. Named here so the Phase 10 seal does not imply they were absorbed. |
| **The Test 2 opens count** | `10-UAT.md` results table | The on-device tuning signal the raised thresholds exist to produce. Until it is measured, the entry thresholds (Paradise 4 / Limbo 3 / Inferno 2) remain **prototype values**, exactly as `docs/BUILD-NOTES.md` §19.1 records them. |
| **Circle 8 dispatches nothing — the `Voice` orphan** | `.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md` | Known open defect, unchanged by this plan. Named in the UAT header so it is not misfiled as a device failure. |
| **DEV-06 — the restore-ownership check and the `Session ID` scope defect** | `docs/BUILD-NOTES.md` §17, §19.8 | Reserved to the user by §17's explicit record. Untouched. Phase 9 UAT test 12 is its cross-check. |
| **Canonical strategy §10.5 still prints the pre-rise threshold arrays** | `PROSOCHE_Nine_Circles_Canonical_Strategy.md:1178, 1184, 1190` | Carried forward from 10-01, 10-03 and 10-04. BUILD-NOTES §19.1 and now `10-UAT.md`'s arithmetic block both carry the correct arrays, so the authoritative record exists in two places. |

## Threat Flags

None. This plan created one markdown file. It introduces no network endpoint, no auth path, no file-access pattern and no schema change at any trust boundary.

Register dispositions from the plan, as shipped:

- **T-10-28** (a device criterion marked passed on non-device evidence) — **mitigated, and exercised.** The `blocked` branch was taken. Every outcome field is blank, the closing note forbids the three substitutions by name, and this SUMMARY states in words that none was made. The threat's realistic form — writing "pass" because the structural evidence looked convincing — was the live temptation here and was declined.
- **T-10-29** (Tests 9 and 10 leaving the device dim or silent) — **mitigated in the document, unexercised on device.** Test 10 is the recovery, and Test 9 and Test 10 both instruct the tester to restore manually through iOS Settings and **abandon the remaining tests** rather than pushing through. Test 9 additionally records that a manual `Test a Circle` has no CLOSE-driven restore path, so the tester is not left waiting for a restore that cannot come.
- **T-10-30** (testing against a stale library entry) — **mitigated.** Step 0 is a separate, explicit, unnumbered re-import step; the header pins the SHA-256 and byte size; and the duplicate-entry diagnosis names 10-04's measured fact that the signed container carries no display name at all.
- **T-10-31** (the Automation B input literal) — **accepted as planned.** It lives on the device and no repository-side control can constrain it. Test 8 diagnoses it: it names the verbatim input-field screenshot as the required evidence and states that the fall-through to manual control is deliberate (DEV-02).
- **T-10-32-SC** (package-manager installs) — **accepted as planned, and correct.** No install of any kind occurred.

## Notes for the Next Plan

- **Phase 10 seals with this block explicitly outstanding.** That is the designed outcome, not a shortfall: waves 1–4 completed and committed because the device-dependent criteria were collected here rather than scattered through them.
- **When a device does appear, `10-UAT.md` is runnable cold and should be run before anything else in this phase is trusted behaviourally.** Two tests are worth more than the other eight: Test 1 (a first open of a cold day must be completely silent while the record still moves) and Test 5 (Status, Toggle Voice and Reset Today must each leave the Notes app closed). Test 2's opens count is the number that decides whether the raised entry thresholds are right.
- **Run `10-UAT.md` and `09-UAT.md` in the same session.** They share a device, they share the dimming/silence path, and Phase 10 Test 9 is explicitly a smoke check on the artifact Phase 9's twelve tests were written against.
- **`docs/manifest_check.py` will go red on the next rebuild until the MANIFEST is refreshed.** `10-UAT.md`'s header hash is pinned to this exact build, so a rebuild also invalidates the UAT header — refresh both together, or the tester will be holding a file whose hash does not match anything.

## Self-Check: PASSED

- `.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md` — FOUND
- `.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-05-SUMMARY.md` — FOUND
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` — FOUND (193,498 bytes)
- `.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md` — FOUND (linked from Test 9)
- `.planning/REQUIREMENTS.md` — FOUND, DIST-03 unchecked at line 161
- commit `c25656f` — FOUND
