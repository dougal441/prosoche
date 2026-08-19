---
phase: 14-ash-as-real-color-filters-grayscale
plan: 02
subsystem: build-tooling-and-records
tags: [validator, gate-a, waiver, checker, deviation-log, constitutional-edit, audit-02]

# Dependency graph
requires:
  - phase: 14-ash-as-real-color-filters-grayscale
    plan: "01"
    provides: "the emitted AX Color Filters sites whose count derives the waiver's line count, and the verbatim gate-A residue this plan re-measured and formalised"
  - phase: 16-environmental-capture-persistence
    provides: "docs/retired_clause_check.py — the model for deciding what is a live rule carrier and what is a frozen record, and for supersession-by-pointer"
provides:
  - "gate A's obligation is an exactly-enumerated residue, not a clean report — stated once in .claude/CLAUDE.md and mirrored in every live carrier"
  - "docs/gate_a_residue_check.py — the waiver as a script, loud when the residue grows OR shrinks, proven load-bearing by three negative controls"
  - "docs/BUILD-NOTES.md DEV-08 — the deviation, its reproduction commands, its measured residue, and an unmissable rejection of the macOS twin"
  - "the fourteenth docs/ checker joins the static suite"
affects: [14-03, 14-UAT, phase-15-voice, ship-gate, every-future-plan-that-names-gate-a]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "a waiver is executable or it is not a waiver: enumerate the permitted line families in code, scope them to one identifier by full string, and fail on anything else"
    - "assert a derived census in BOTH directions — a shrunk residue means emitted sites disappeared and would otherwise present as good news"
    - "a checker whose subject could not be examined FAILS; it never skips and never passes"
    - "an in-file classifier control, run on every invocation, proving the guard still catches the real thing and still rejects the near miss"

key-files:
  created:
    - docs/gate_a_residue_check.py
  modified:
    - .claude/CLAUDE.md
    - .claude/skills/spike-findings-prosoche/SKILL.md
    - .claude/skills/spike-findings-prosoche/references/evidence-and-probes.md
    - docs/BUILD-NOTES.md

key-decisions:
  - "The waiver enumerates BOTH validator line families, widening D-14-01 item 2's literal wording (which names only the unknown-identifier lines). Flagged assumption B1 in the plan authorised this and it was applied as written: a descriptor-less action emits both families per instance and the same decision forbids synthesising a descriptor, so a one-family waiver could never be satisfied and the checker would be permanently red — the one outcome the decision exists to prevent."
  - "The new deviation is numbered DEV-08. §5's own scheme runs DEV-01..DEV-04, but §13 and §15 reuse DEV-01/DEV-02/DEV-04 for different subjects and introduce DEV-05, DEV-06 and DEV-07. DEV-08 is the lowest number that is unambiguous across the whole file."
  - "A third negative control was added beyond the two the plan required — an unlocatable validator — because T-14-12 names exactly that false-reassurance path and asserting it costs one throwaway run."
  - "The classifier control's must-not-permit rows were chosen to be NEAR misses, not obvious ones: the macOS twin, an unrelated unknown identifier, a DIFFERENT finding on the SAME identifier, and a line with trailing text. An obvious control proves nothing about the widening this waiver is exposed to."
  - "No changelog line was added to .claude/CLAUDE.md or either skill file: measured, none of the three carries a changelog or revisions section. src/CONFIG-BLOCK.md is the file in this project that does, and it is out of this plan's scope."

patterns-established:
  - "Constitutional amendment by mirroring: when one gate already has the shape a second gate needs, copy that gate's structure — invocation, expected exit status, waiver table with one row per permitted line family, index-normalised — rather than inventing a second shape for the same idea."
  - "Narrowness stated as three separate numbered claims (scoped by name / count derived from the artifact / gap recorded with its authority) so no single one can be eroded by a careless reading of the others."
  - "Deviation entries that open with a READ-THIS-FIRST block naming the wrong fix, positioned before the fields, so a reader arriving from a red gate meets the authority before the temptation."

requirements-completed: [AUDIT-02]

coverage:
  - id: D1
    description: "No live carrier still asserts that gate A must produce a clean report or exit zero without a waiver qualifier"
    requirement: "AUDIT-02"
    verification:
      - kind: unit
        ref: "plan 14-02 Task 1 verify — line-scanning regex over all three live carriers, three retired-obligation families, zero hits"
        status: pass
      - kind: unit
        ref: "independent repository sweep, four search terms over the live-authority scope — no further live carrier found (search terms and scope recorded below)"
        status: pass
    human_judgment: false
  - id: D2
    description: ".claude/CLAUDE.md names the residue checker by path, names the one identifier the waiver is scoped to, and enumerates both validator line families; gate B and both anti-pattern rules intact"
    requirement: "AUDIT-02"
    verification:
      - kind: unit
        ref: "plan 14-02 Task 1 verify — needle assertions for gate_a_residue_check, AXToggleColorFiltersIntent, AppIntentDescriptor, waiver language, '#### Gate B', 'strictly dominates', 'empty allowlist'"
        status: pass
    human_judgment: false
  - id: D3
    description: "The waiver is mechanical: a checker fails on any line outside the two enumerated families and on any change to the permitted count in either direction"
    requirement: "AUDIT-02"
    verification:
      - kind: integration
        ref: "python3 docs/gate_a_residue_check.py — exit 0 at HEAD, 30 permitted lines per fork on both forks"
        status: pass
      - kind: integration
        ref: "negative control 1 — injected extra unknown identifier, exit 1 naming both injected lines verbatim"
        status: pass
      - kind: integration
        ref: "negative control 2 — deliberately wrong expected count, exit 1 in the shrink direction stating that emitted sites disappeared"
        status: pass
      - kind: integration
        ref: "negative control 3 (T-14-12) — unlocatable validator, exit 1 stating the residue was never examined"
        status: pass
    human_judgment: false
  - id: D4
    description: "A future reader meeting a red gate A finds the reason, the reproduction command, the donor authority and an explicit rejection of the macOS twin, before they find the temptation"
    requirement: "AUDIT-02"
    verification:
      - kind: unit
        ref: "plan 14-02 Task 3 verify — DEV-08 carries the identifier, both reproduction commands, the twin rejection and the checker pointer"
        status: pass
      - kind: unit
        ref: "git diff -U0 docs/BUILD-NOTES.md — four hunks, all inside the live §3 recipe, the §5 deviation log and the §7 deviation index; no dated numbered section touched"
        status: pass
    human_judgment: false
  - id: D5
    description: "Every script in docs/ except manifest_check.py exits 0, the new checker included"
    requirement: "AUDIT-02"
    verification:
      - kind: integration
        ref: "13 of 14 docs/*.py green (the new checker among them); manifest_check.py expected RED per D-MANIFEST until plan 14-03 re-signs"
        status: pass
    human_judgment: false
  - id: D6
    description: "The enumerated residue stays stable across a future Shortcuts Playground plugin update"
    requirement: "AUDIT-02"
    verification: []
    human_judgment: true
    rationale: "Out of this repository by construction — the bundled snapshots live in the plugin cache and are overwritten on update. The checker converts the event from silent drift into a loud failure (a snapshot that gains the identifier makes gate A exit 0, which the checker treats as a finding and reports with instructions), but the event itself cannot be verified here. Carried as a backstop, per the plan's must_haves."

# Metrics
duration: 38min
completed: 2026-08-19
status: complete
---

# Phase 14 Plan 02: Ash as real Color Filters grayscale Summary

**Gate A stopped demanding a clean report it can never produce again and started demanding a residue equal to exactly thirty enumerated lines — and that demand is now a script with three negative controls behind it, not a thing anybody has to remember.**

## Performance

- **Duration:** ~38 min
- **Tasks:** 3 of 3
- **Files modified:** 4 (1 created, 3 edited) + `docs/BUILD-NOTES.md`
- **Commits:** 3

## Accomplishments

- **The constitutional clause was amended without being weakened.** Gate A stays mandatory. What changed is only what "satisfied" means: the residue must equal exactly the enumerated waiver, mirroring the structure gate B already had rather than inventing a second shape for the same idea. Gate B is untouched, and both validator anti-pattern rules — never pair the iOS platform flag with the macOS 26 target, never treat the macOS 27 target as the sole gate — keep their teeth verbatim.
- **The waiver is a script.** `docs/gate_a_residue_check.py` runs gate A on both forks, classifies every reported line against two patterns that each demand the full `AX*` identifier string, and fails on anything else. It also fails on a residue that has **shrunk**, with a message saying so — the direction a one-sided check would miss, and the one that would otherwise read as good news.
- **It was proven load-bearing before being declared done.** Three negative controls, all recorded verbatim below: an injected extra unknown identifier, a deliberately wrong expected count in the shrink direction, and an unlocatable validator.
- **The wrong fix is now rejected on four independent surfaces.** `DEV-08` opens with it, `.claude/CLAUDE.md`'s gate-A section and its new `What NOT to use` row name it, the checker's classifier control proves the waiver rejects it, and plan 14-01's `docs/phase5_self_check.py` assertion fails the build on any twin occurrence. T-14-08 is the phase's highest-severity spoofing threat precisely because the twin is the cheapest-looking fix.
- **No dated historical record was edited.** §12's 2026-08-13 assertion that the build emits neither Color Filters identifier is superseded **by pointer** from DEV-08 and left exactly as written; the superseded gate-A wording is cited by where it lived, never restated.

## Task Commits

1. **Task 1: the constitutional edit — amend the gate-A clause and every live mirror** — `2445c82` (docs)
2. **Task 2: the residue checker — make the waiver executable and loud in both directions** — `c020782` (test)
3. **Task 3: record the deviation where a future reader hits it before the wrong fix** — `69f6071` (docs)

## The independent repository sweep — search terms, scope, and what it found

**Stated plainly: this is a starting set given mechanical form by Task 2, not a claim of completeness.** The comparable clause class in this project (the retired brightness floor) was enumerated four times and undercounted four times; `docs/retired_clause_check.py`'s own header records that the base rate of a fifth undercount is not hypothetical. The plan's `<carrier_inventory>` was swept first, then the repository was swept independently.

**Search terms** (all case-insensitive, run with `grep -rn -i` from the repo root):

| Term | Rationale |
|---|---|
| `must pass clean` / `passes clean` / `pass clean` | The retired obligation's own literal wording |
| `Validation passed` | The expected-output form of the same obligation |
| `target-macos 26` | Every site that names the gate-A invocation at all — the widest net, 130+ files |
| `gate a` | The obligation stated by name rather than by command |
| `exit 0` (within the three live carriers) | The obligation stated as an exit-status expectation |

**Scope searched:** the whole repository, then filtered to the **live-authority set** — `.claude/CLAUDE.md`, `.claude/skills/spike-findings-prosoche/` (excluding `sources/`), `docs/`, `src/`, `tools/`, and `.planning/{PROJECT,ROADMAP,REQUIREMENTS,STATE}.md`. Excluded as frozen historical record, matching `docs/retired_clause_check.py`'s tier-1 allowlist: `.planning/phases/`, `.planning/spikes/`, `.planning/quick/`, `.planning/research/`, `.planning/todos/completed/`, `.planning/debug/`, `.claude/skills/spike-findings-prosoche/sources/`, `artifacts/`, `.claude/worktrees/`, `.git/`.

**What the sweep found beyond the plan's inventory — four sites, none needing this plan's edit:**

| Site | Verdict |
|---|---|
| `docs/phase5_self_check.py` (two sites) | **Already correct.** Wave 1 rewrote both to say gate A now fails permanently. No retired assertion survives. |
| `docs/note_identity_check.py` | **Not a carrier.** "validates at gate A, signs, and imports perfectly" describes a *mutation's* behaviour, not the gate's obligation. Still true. |
| `docs/phase9_self_check.py` | **False positive.** "the same fixture must now pass cleanly" is about a test fixture, unrelated to the validator. |
| `tools/build_state_engine.py:2658` | **Not a carrier, and out of scope.** A mechanism statement about which catalogs gate A loads. Still true; `tools/` is prohibited to this plan. |

**One genuine carrier found and deliberately NOT edited:** `artifacts/shortcuts/MANIFEST.md` asserts at four sites that both forks pass gate A clean. It is a **signed-artifact provenance record**, `artifacts/` is prohibited to this plan, and its rows are already stale for an independent reason (wave 1 rebuilt both forks, which is why `docs/manifest_check.py` is expected red). **Plan 14-03 owns it** — it re-signs and refreshes the manifest, and must correct these four gate-A cells in the same pass. This is recorded here so 14-03 does not have to re-derive it.

**Changelog lines:** none of the three edited carriers carries a changelog or revisions section — measured, not assumed. `src/CONFIG-BLOCK.md` is this project's file that does, and it is out of this plan's scope. Each amendment therefore carries its own inline dated note (`Amended 2026-08-19`) instead, which is the convention `docs/BUILD-NOTES.md` already uses.

## The normalised residue, re-measured on both forks

Re-measured 2026-08-19 at wave 2, **identical to plan 14-01's recording** — the wave-1 measurement was the input and it still holds.

Both forks: **exit 1**, `Validation failed:` plus a `First failing action: index 0 (is.workflow.actions.comment)` header with a snippet, then **exactly 30 error lines and nothing else** — two families × 15 instances, both families at the same 15 indices within a fork.

| Line family (indices normalised to `N`) | Per fork |
|---|---:|
| `- Unknown AppIntent identifier at index N: com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` | 15 |
| `- AppIntent action missing AppIntentDescriptor at index N: com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` | 15 |

- **Core (`src/PROSOCHE-Dumb.xml`)** — `N` ∈ {176, 226, 1012, 1272, 1585, 1770, 2039, 2308, 2577, 2846, 3115, 3384, 3653, 3922, 4168}
- **Aware (`src/PROSOCHE-Sentient.xml`)** — `N` ∈ {178, 228, 1014, 1340, 1719, 1904, 2173, 2442, 2711, 2980, 3249, 3518, 3787, 4056, 4302}

Nothing outside these two families was reported on either fork. The checker's own passing output, verbatim:

```
gate A residue check: passed -- residue equals exactly the enumerated waiver on 2 fork(s)
(Core (src/PROSOCHE-Dumb.xml): 30 permitted; Aware (src/PROSOCHE-Sentient.xml): 30 permitted);
2 line families scoped to com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent;
8 classifier control rows. Gate A exits 1 by construction -- that is the expected result, and
this script, not the raw validator command, is the gate-A obligation.
```

## Negative controls — recorded verbatim

### Control 1 — an injected extra unknown identifier turns the checker red

A scratch copy of `src/PROSOCHE-Dumb.xml` was written **outside the repository** (into the session scratchpad, so `git status` never saw it) with action index 500's identifier replaced by `com.apple.fabricated.NegativeControlIntent`, and `FORK_SOURCES` was pointed at it in a throwaway run. **EXIT=1**, verbatim:

```
gate A residue check: FAILED -- NEGCONTROL scratch copy of Core: gate A reported 2 line(s) OUTSIDE the enumerated waiver. Each one is a real finding and must be investigated -- never waived, never 'fixed' by substituting com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent:
    AppIntent action missing AppIntentDescriptor at index 500: com.apple.fabricated.NegativeControlIntent
    Unknown AppIntent identifier at index 500: com.apple.fabricated.NegativeControlIntent
```

Both injected lines are named verbatim, and note that the injected identifier produced **both** families too — independent confirmation of why a one-family waiver would be unsatisfiable. The scratch copy was never in the repository; `git status --short` after the run showed only the intended new file.

### Control 2 — the shrink direction

`AX_SITES_PER_FORK` was set to `16` in a throwaway run against the real, unmodified forks, so the true 30-line residue reads as **smaller** than the asserted 32. **EXIT=1**, verbatim:

```
gate A residue check: FAILED -- Core (src/PROSOCHE-Dumb.xml): the permitted residue is 30 line(s), expected exactly 32 (16 emitted AX sites x 2 line families). Per family: Unknown AppIntent identifier=15, AppIntent action missing AppIntentDescriptor=15. A SMALLER residue means emitted AX sites DISAPPEARED -- colour may no longer be applied at a Circle, or restored at a recovery path, and this is why the count is asserted in both directions. Do NOT relax this check to accept fewer lines.
```

### Control 3 — an unlocatable validator fails, never passes (T-14-12, beyond the plan's requirement)

`VALIDATOR` and `PLUGIN_FALLBACK` were both pointed at non-existent paths in a throwaway run. **EXIT=1**, verbatim:

```
gate A residue check: FAILED -- 'validate-shortcut-that-does-not-exist' is not on PATH and the Shortcuts Playground fallback /nonexistent/bin/validate-shortcut does not exist, so gate A could not be run at all. This is a FAILURE, not a skip: the residue was never examined, so nothing about it is known
```

## The deviation entry — DEV-08

The new entry is **`DEV-08`**, in `docs/BUILD-NOTES.md` §5's deviation log, with a matching row in §7's deviation index naming **Phase 14** as owner and **AUDIT-02** as the requirement touched. **Plan 14-03 should cite it as `DEV-08`.**

Numbering rationale, recorded because the file's scheme is not linear: §5 runs `DEV-01`..`DEV-04`, but §13 and §15 independently reuse `DEV-01`, `DEV-02` and `DEV-04` for entirely different subjects and introduce `DEV-05`, `DEV-06`, `DEV-07` and `DEV-C3-03`. `DEV-08` is the lowest number unambiguous across the whole file.

What it carries: the five labelled fields the log's own header mandates (`Capability`, `Wanted`, `Verified`, `Substituted`, `Runnability`); a **READ THIS FIRST** block rejecting the macOS twin, positioned *before* the fields; both reproduction commands; the index-normalised residue table with the measured `N` values for both forks; the derived 15-site census; the measurement that **signing is unaffected**, so the artifact remains shippable and only the validator's verdict changed; the donor authority named twice (§4's CAP-20 row and `docs/CAPABILITY-DECISIONS.md` BD-01-R2); the three rejected alternatives worst-disguised-first; the supersession-by-pointer note for §12; and the consequence for every later plan.

## Decisions Made

- **The two-family widening was applied as written and is visible, not assumed.** D-14-01 item 2 names only the unknown-identifier lines. The plan's flagged assumption B1 authorised widening to both families, and the measurement backs it: both families appear at the same 15 indices, and control 1's injected identifier reproduced the pairing independently. The widening stays inside the decision's stated intent (residue equals exactly the enumerated waiver) and remains scoped to one identifier.
- **`docs/gate_a_residue_check.py` shells out, which no other repo checker does for this purpose.** `docs/environmental_restore_check.py` states "It never shells out" as policy and `docs/phase6_self_check.py` shells out only to rebuild. Here the validator's verdict *is* the subject, so capturing and parsing its output is the only possible implementation. The structural idioms — `ROOT = Path(__file__).resolve().parents[1]`, `require()`, `main()` raising `AssertionError`, the stderr failure convention — are copied from `docs/retired_clause_check.py` so it reads as one of the family.
- **The classifier control runs on every invocation rather than once at fix time.** `docs/retired_clause_check.py`'s `family_b_control()` records why: ephemeral proof at fix time is exactly what let a broken pattern ship. Its must-not-permit rows are deliberately *near* misses — the twin, an unrelated unknown identifier, a different finding on the same identifier, and a line with trailing text — because an obvious control proves nothing about the widening this waiver is actually exposed to.
- **Per-family counts are asserted separately, not just the total.** 30 total could be reached by 20 + 10. The two families must move together because a descriptor-less action emits both per instance, so a split count is itself a finding.
- **A gate-A exit of 0 is treated as a finding, not a pass.** If a future plugin snapshot gains the identifier, or the AX action stops being emitted, gate A exits 0 and the checker fails with instructions naming both possibilities. That is the mechanism by which the backstop in D6 above becomes loud rather than silent.

## Deviations from Plan

### Auto-fixed Issues

None. No bug, missing critical functionality or blocking issue was encountered; nothing required a Rule 1–3 fix.

### Additions beyond the plan (recorded, not auto-fixes)

**1. A third negative control.** The plan required two. A third — an unlocatable validator — was added because T-14-12 in this plan's own threat register names exactly that false-reassurance path as a mitigate-disposition threat, and asserting it costs one throwaway run. Recorded verbatim above.

**2. Two live sites amended slightly beyond the literal inventory.** `.claude/CLAUDE.md` gained a companion row in `## What NOT to use` (the plan said "may want a companion row"), and `docs/BUILD-NOTES.md` §3's "The rule is not restated here" sentence was updated to say **both** waivers rather than "the waiver", which had become ambiguous once gate A acquired one. Both are inside the plan's stated surfaces.

---

**Total deviations:** 0 auto-fixed. 2 recorded additions, both within scope.
**Impact on plan:** None. No prohibition was touched: no emitted action changed, no descriptor was synthesised, the plugin's bundled catalog was not vendored or patched, gate B and both anti-pattern rules are intact, the waiver enumerates both families, the residue check fails on a shrink, no dated historical record was edited, the superseded wording is cited rather than quoted, and `git status --short` shows no change under `tools/`, `src/`, `artifacts/`, `.planning/research/` or `.planning/spikes/`.

## Issues Encountered

- **`docs/manifest_check.py` is red, expected, and deliberately not fixed.** Per D-MANIFEST it stays red until plan 14-03 re-signs and refreshes the manifest. Closing it by editing MANIFEST rows without re-signing would falsify a provenance record. **13 of 14 checkers green, manifest expected red** — the count moved from 12/13 because this plan added the fourteenth checker.
- **`artifacts/shortcuts/MANIFEST.md` carries four stale gate-A cells** and could not be corrected here (prohibited scope). Handed to plan 14-03 above.

## What this plan does NOT establish

- **That the enumerated residue survives a Shortcuts Playground plugin update.** The bundled snapshots are outside this repository and are overwritten on update. The checker makes the event loud; it cannot prevent it. Carried as a backstop.
- **Anything device-proven.** This plan touches only records and build tooling. Circle 2's behavioural coverage — that the screen actually turns black and white and that colour actually returns — is `14-UAT.md`'s and remains BLOCKED on DIST-03.
- **CIRC-02, SAFE-01, SAFE-02 and SAFE-05.** All four came back `unclassified`/`unresolved` from the spec-less edge probe and are carried as flagged backstops with their owning plans named in this plan's `must_haves.truths`. None is dropped; none is this plan's to close.

## Known Stubs

None. No placeholder, TODO or unwired data path was introduced.

## User Setup Required

None — no external service configuration required.

## Self-Check: PASSED

Files asserted present:

- `docs/gate_a_residue_check.py` — FOUND (contains `AXToggleColorFiltersIntent`, `UAToggleColorFiltersIntent`, both family strings, `PROSOCHE-Dumb`, `PROSOCHE-Sentient`, `parents[1]`, `EXPECTED_PERMITTED_LINES`)
- `.claude/CLAUDE.md` — FOUND (gate-A waiver table, `gate_a_residue_check` named by path, `#### Gate B` intact, `strictly dominates` and `empty allowlist` intact)
- `.claude/skills/spike-findings-prosoche/SKILL.md` — FOUND (two-gate block amended)
- `.claude/skills/spike-findings-prosoche/references/evidence-and-probes.md` — FOUND (two-gate paragraph amended)
- `docs/BUILD-NOTES.md` — FOUND (`DEV-08` in §5, its §7 index row, the live §3 recipe redirected)

Commits asserted present: `2445c82`, `c020782`, `69f6071` — all FOUND in `git log`.
