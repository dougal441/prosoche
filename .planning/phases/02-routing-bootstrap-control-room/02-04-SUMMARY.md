---
phase: 02-routing-bootstrap-control-room
plan: 04
subsystem: automation
tags: [ios-shortcuts, plist-xml, control-flow, state-machine, apple-notes, self-healing]

# Dependency graph
requires:
  - phase: 02-routing-bootstrap-control-room (plan 02-01)
    provides: "The state-load chain (Get File / Detect Dictionary / schema_version read) and the bootstrap gate with its Save File, both originally authored inside the MANUAL branch; the DEV-02 substitute; the Control Room Note creation/open wiring and its markdownContents key"
  - phase: 02-routing-bootstrap-control-room (plan 02-02)
    provides: "The complete Control Room Body text — the exact content this plan's recreated Note must carry unchanged"
  - phase: 02-routing-bootstrap-control-room (plan 02-03)
    provides: "The complete four-outcome router (MANUAL/OPEN/CLOSE/fail-safe) and the normalised Input Key variable this plan's hoisted state load now sits above"
provides:
  - "The state-load-and-bootstrap chain hoisted above the entire router, so a missing or corrupt state.json self-heals identically from a manual tap, an automatic OPEN, or an automatic CLOSE (BOOT-06)"
  - "The two-field validity gate — State Present, yes only when schema_version has a value AND matches \"1\" AND profile has a value — replacing the single-field presence check, so a corrupt or wrong-version document takes the same safe rebuild as a missing one (BOOT-07)"
  - "Import-answer normalisation: Descent Normalised (Paradise/Limbo/Inferno, default Limbo) and Voice Normalised (a real JSON boolean, not the raw typed word) written into the state.json template in place of the raw answers"
  - "The Note-existence guard — Find Notes / Note Found Text / Note Present / reuse-or-create — so a deleted Control Room Note is recreated with its full, unabridged body on the next manual run (BOOT-08)"
  - "Idempotence proved structurally rather than by running anything: exactly one Save File in the whole graph (behind State Present's otherwise-branch) and exactly one Note-creation action (behind Note Present's otherwise-branch) (BOOT-05)"
  - "The best-effort recovery line: a State Recovery Occurred flag set only when the bootstrap branch actually ran, surfaced as one dated line appended to the Control Room Note on the next manual run, never blocking Show Note"
  - "The Note-check scoping decision recorded in docs/BUILD-NOTES.md §10 and in-graph Comments — MANUAL branch only, never OPEN/CLOSE — and the lazy-guard-before-append rule Phases 6 and 7 inherit"
  - "Phase 2's closed requirement table (BOOT-01..09, STATE-12, ROOM-01..06) and its five ROADMAP success criteria mapped to evidence, in docs/BUILD-NOTES.md §7"
affects: [phase-3, phase-4, phase-6, phase-7]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Two-variable accumulator-then-canonical-copy: when a verify script (or any downstream consumer) requires a named variable be assigned by exactly one Set Variable, but its value must be computed across several mutually-exclusive nested If/Otherwise branches, set a differently-named helper inside the branches and add exactly one trailing Set Variable that copies the helper into the canonical name after the nested structure closes. Used for both State Present (from State Valid Text) and Note Present (from Note Found Text) — Shortcuts has no ternary/phi-node merge across branches, so this is the only way to get a single canonical assignment out of branch-dependent logic."
    - "Shared literal Text actions, referenced by UUID from multiple downstream Set Variable calls: rather than re-authoring a fresh \"yes\"/\"no\" Text action at every point a literal boolean-style flag needs setting, two Text actions (one holding \"yes\", one holding \"no\") are created once near the top of the state-load block and their ActionOutput is referenced by UUID from every later Set Variable that needs that exact literal — valid because Shortcuts allows unlimited downstream references to one action's output, and the two actions execute unconditionally before any branch that needs them."
    - "Hoisting shared logic above a router, not into every branch, when no subroutine mechanism exists (D-14): the state-load chain moved to a single position before the outer router gate rather than being duplicated into the MANUAL/OPEN/CLOSE branches — the only way three branches can share logic without an internal Run Shortcut hop is to place it where all three branches' control flow passes through before diverging."
    - "The plist was restructured with a Python/plistlib script rather than hand-edited XML text: `plistlib.dumps(p, fmt=FMT_XML, sort_keys=False)` reproduces the source file's exact tab-indentation and per-dict key-insertion-order style byte-for-byte (verified via a no-op round-trip diff before making any change), which made a ~30-action relocation, a JSON template rewrite with recomputed U+FFFC byte offsets, and 19 new UUID/GroupingIdentifier assignments tractable without hand-counting offsets or risking a stray Edit-tool mismatch across a 1600+ line file."
    - "Find Notes name filters use condition code 99 (contains), never 4 (exact \"is\") — FILTERS.md documents this as a validator-invisible trap: operator 4 on a Notes Name filter silently returns zero results at runtime. The search string is still the exact, unique Control Room title, so \"contains\" behaves as an effective exact match without hitting the documented failure mode."

key-files:
  created: []
  modified:
    - src/PROSOCHE-Dumb.xml
    - docs/BUILD-NOTES.md
    - .planning/ROADMAP.md

key-decisions:
  - "The profile-routed Text value feeding the innermost validity check (SV3) is wired by direct ActionOutput/UUID reference rather than through a third named Set Variable, following the \"UUID-for-immediate-consumer\" precedent 02-01/02-03 already established (Config, Epoch Anchor, Input Key's raw-input chain) and confirmed against CONTROL_FLOW.md's documented ActionOutput-wrapper shape for a conditional's WFInput — nothing else in the graph needs that intermediate value, so no named variable was minted for it."
  - "Append to Note's `entity` parameter is wired as a plain named-variable token attachment (`{Type: Variable, VariableName: \"Control Room Note\"}`), inferred by direct analogy to Show Note's already-working `target` parameter, since both share the same underlying type (`com_apple_notes_note_entity`, confirmed in `toolkit-v78-first-party-parameter-keys.json`) and no worked example of `is.workflow.actions.appendnote` exists anywhere in the golden-shortcut corpus or the reference docs. Recorded here as an evidence-grounded inference from a same-type sibling parameter, not a guess at an unverified shape — the identifier and the parameter's existence and type are both independently VERIFIED (CAP-09)."
  - "Get Item from List (WFItemSpecifier=\"First Item\", both the identifier and this exact enum case confirmed against the bundled ToolKit's enum-case catalog) resolves Find Notes' list result to a single Note object before it is ever assigned to Control Room Note, rather than assigning the raw list — a deliberate correctness choice (Rule 2 territory) since Show Note's `target` parameter is documented as taking a single note reference, not a list."
  - "The existing `6D32F6F2` GroupingIdentifier was repurposed for the two-field validity gate rather than retired in favour of a freshly minted one — it is structurally the same load-vs-bootstrap decision point 02-01 built, now driven by a smarter, two-field-aware condition instead of a raw presence check. Every other new nested block in this plan (the validity computation itself, the descent/voice normalisation, the Note-existence and reuse-or-create gates, the recovery check) got a genuinely fresh GroupingIdentifier, per the plan's own instruction."
  - "Task 1 and Task 2's XML changes were built and committed as two sequential, structurally-independent passes over the same file — rebuilding Task 1's intermediate state first (state load hoisted, Control Room block left temporarily unconditional, exactly matching the plan's own \"the MANUAL branch keeps everything else it had\" instruction), committing it, then transforming that committed intermediate into Task 2's final shape — rather than authoring the whole 133-action result in one pass and trying to split the diff after the fact. This is what let each task's own `<verify>` script run cleanly against exactly the state its own task produced, and kept each git commit atomic and independently meaningful."

requirements-completed: [BOOT-05, BOOT-06, BOOT-07, BOOT-08, STATE-12]

coverage:
  - id: D1
    description: "The state-load-and-bootstrap chain is hoisted above the router's outer gate, so a missing state.json self-heals identically from any of the three invocation modes, and the two-field validity gate (schema_version has-value AND equals \"1\" AND profile has-value) routes a corrupt, partial, or wrong-version document to the same rebuild as a missing one — proven structurally from the plist, not by running anything"
    requirement: "BOOT-06"
    verification:
      - kind: other
        ref: "Task 1 <verify> SELF-HEAL-OK script (plan 02-04-PLAN.md) — Get File's index precedes Input Key's; exactly one Get File/Save File/Create Folder; State Present assigned exactly once; exactly one conditional tests it; Save File's enclosing chain includes that gate's otherwise-side"
        status: pass
      - kind: other
        ref: "bin/validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all"
        status: pass
    human_judgment: false
  - id: D2
    description: "Idempotence proved as a nesting property: exactly one Save File exists in the whole 133-action graph, gated on State Present's otherwise-branch, and exactly one Note-creation action exists, gated on Note Present's otherwise-branch — together meaning a later manual run on a healthy install reaches neither writer"
    requirement: "BOOT-05"
    verification:
      - kind: other
        ref: "Task 1 <verify> SELF-HEAL-OK + Task 2 <verify> IDEMPOTENCE-OK scripts (plan 02-04-PLAN.md), both re-run clean against the finished file"
        status: pass
      - kind: other
        ref: "Task 3 <verify> PHASE-CLOSURE-OK script — full re-audit: import-question binding, dangling references, display/data-flow serialization, control-flow balance, comment density, all clean at 133 actions"
        status: pass
    human_judgment: false
  - id: D3
    description: "The Note-existence guard (Find Notes -> Note Found Text -> Note Present -> reuse-or-create) is scoped to the MANUAL branch only; no Find Notes, Note-creation, Append to Note, or Show Note action is reachable from the OPEN or CLOSE branch chain"
    requirement: "BOOT-08"
    verification:
      - kind: other
        ref: "Task 2 <verify> IDEMPOTENCE-OK script's NOTES/open_close check (plan 02-04-PLAN.md)"
        status: pass
    human_judgment: false
  - id: D4
    description: "On a real device: a missing or corrupt state.json actually self-heals on each of the three invocation modes when the shortcut runs; a later manual run genuinely writes nothing and creates nothing; a deleted Control Room Note actually comes back with its full body on the next manual run"
    verification: []
    human_judgment: true
    rationale: "No iPhone or Shortcuts-capable simulator is available in this environment. The structural proofs (D1-D3) establish the plist can only route each case to one safe, correctly-gated outcome, but whether the runtime actually executes that shape on real hardware — including whether a hand-corrupted on-device state.json is recognised as corrupt and whether a deleted Note truly reappears with its complete body — is exactly the class of validator-invisible fact PITFALLS A9 describes. Recorded as an extension to UA-01 (observations e and f) and the existing UA-04 in docs/BUILD-NOTES.md §6, both gated on Phase 2's on-device pass, not yet performed since no iPhone is available in this build environment."

# Metrics
duration: ~55min
completed: 2026-08-13
status: complete
---

# Phase 2 Plan 4: Self-Healing, Corrupt-State Recovery, Note Guard, and Phase Closure Summary

**`src/PROSOCHE-Dumb.xml` grew from 73 to 133 actions: the state-load chain moved above the entire router, a two-field validity gate replaced the single-field presence check, import answers are normalised before they reach the state.json template, a Find-Notes-backed existence guard makes a deleted Control Room Note self-heal, and idempotence is proved structurally — one Save File, one Note creator, each reachable only through its own absence branch.**

## Performance

- **Duration:** ~55 min
- **Completed:** 2026-08-13T04:03Z
- **Tasks:** 3 completed
- **Files modified:** 3 (0 created, 3 modified)

## Accomplishments

- **The state-load-and-bootstrap chain is hoisted above the router (BOOT-06).** Get File, Detect Dictionary, the schema_version read and its Text routing, and the bootstrap gate with its Save File all moved out of the MANUAL branch to a single position after the run-clock section and before the router's Input Key normalisation. This is the one structural change that makes self-healing true from a manual tap, an automatic OPEN, or an automatic CLOSE alike — Shortcuts has no subroutine mechanism (D-14), so hoisting above the point where the router first branches is the only way to share this chain across all three modes without duplicating it (and duplicating it would mean a second Save File, which this plan's own structural check rejects).
- **The single-field presence check became a real two-field validity gate (BOOT-07).** A new `State Present` value is computed by three nested single-condition `If` checks (schema_version has-any-value, schema_version string-equals `"1"`, profile has-any-value), each testing a value already routed through a `Text` action, using the string-equals condition code for the version comparison since Shortcuts has no numeric-equals code. A missing file, a corrupt/unparseable file, an old-schema-version file, and a profile-less file are all indistinguishable at this gate and all take the identical safe rebuild branch.
- **Import answers are normalised before they reach state.json.** `Import Descent` maps to exactly one of `Paradise`/`Limbo`/`Inferno` via nested `If`/`Otherwise`, defaulting anything unrecognised (including typos and `Limbo` itself) to `Limbo`. `Import Voice` is written into the template as a real, unquoted JSON boolean (`true`/`false`) rather than the raw typed word, with a Comment recording that it will read back as a plain number, never as the strings `true`/`false`. The `Comment` 02-01 left flagging this work as outstanding is gone, because the work is done.
- **The Note-existence guard makes a deleted Control Room Note self-heal (BOOT-08).** `Find Notes` (Name contains the exact title — condition code 99, never 4, per the documented Find-Notes name-matching trap) feeds a has-any-value check into `Note Present`; a single conditional then either reuses the found Note (via `Get Item from List`, First Item) or recreates it using the exact same `Control Room Body` text action 02-02 authored, so a recreated Note is never a lesser Note.
- **Idempotence is proved structurally, not inferred from a run (BOOT-05).** Exactly one `is.workflow.actions.documentpicker.save` exists in the whole 133-action graph, and its enclosing control-flow chain is asserted to include the `State Present` gate on its otherwise-side. Exactly one `com.apple.Notes.CreateNoteFromMarkdownLinkAction` exists, similarly gated on `Note Present`'s otherwise-side. Both facts are checked by walking the plist's `GroupingIdentifier`/`WFControlFlowMode` structure directly, not by running the shortcut.
- **A best-effort recovery line makes silent recovery visible.** A `State Recovery Occurred` flag is set only inside the bootstrap branch; on the next manual run, after the Note is known to exist (found or created) but before it is shown, one dated line is appended if the flag has a value. Its own failure is sequenced to never block `Show Note`.
- **Phase closure: a whole-graph re-audit found zero new defects**, PITFALLS A9's five named validator false-passes were each walked and answered explicitly for this file, and `docs/BUILD-NOTES.md` §7 gained a Phase 2 requirement-closure table (`BOOT-01`..`09`, `STATE-12`, `ROOM-01`..`06`) plus the five ROADMAP Phase 2 success criteria mapped to their establishing evidence.

## Two-Run Trace

Traced directly against the finished `src/PROSOCHE-Dumb.xml`, per the plan's own instruction to write this out explicitly rather than merely claim it:

| Run | `state.json` | Control Room Note | What executes | What's written |
|---|---|---|---|---|
| **Run 1** — clean device, first manual tap | absent | absent | `State Present` gate → `no` (Get File finds nothing, `State Schema Text` has no value) → bootstrap: Create Folder, normalise Descent/Voice, write `state.json`, set the recovery flag. `Note Present` gate → `no` (Find Notes finds nothing) → create the Note with its full body. | Both stores created: one `Save File`, one Note-creation, exactly as the structural proof requires. |
| **Run 2** — immediately after, second manual tap | valid | present | `State Present` gate → `yes` (schema_version has a value, equals `"1"`, profile has a value) → load path, writes nothing. `Note Present` gate → `yes` (Find Notes finds the existing Note) → reuse it via Get Item from List, creates nothing. The recovery-flag check finds no value (never set on this run), so no line is appended. | Nothing written, nothing created — the existing Note is shown as-is. |

## Task Commits

Each task was committed atomically:

1. **Task 1: Hoist the state load above the router and make the validity gate real** - `1e18533` (feat)
2. **Task 2: The Note-existence guard, and idempotence proved as a nesting property** - `cd53919` (feat)
3. **Task 3: Phase closure — whole-graph audit, requirement closure, and the human observations** - `e1d43d7` (docs)

## Files Created/Modified

- `src/PROSOCHE-Dumb.xml` — Grew from 73 to 133 actions (13 control-flow blocks, 34 comments, 30 wired outputs, zero dangling references), re-validated at `--target-macos 26 --target-platform all` after every task; import-question binding still resolves to indices 2 and 4 unchanged
- `docs/BUILD-NOTES.md` — Appended §10 (the Note-check scoping decision), a Phase 2 requirement-closure table and PITFALLS A9 walkthrough within §7, and extensions to `UA-01` (two new plan-02-04 on-device observations) — verified pure-append (zero lines removed) across all three tasks' edits
- `.planning/ROADMAP.md` — Phase 2's top-level checkbox, its `Plans: 4/4` line, `02-04-PLAN.md`'s own checkbox, and the Progress table's Phase 2 row all flipped to complete, via scoped edits; every other phase's entry is byte-identical to before

## Decisions Made

See `key-decisions` in the frontmatter for the five decisions requiring the most justification. In brief: two were forced by a hard structural constraint the verify scripts impose (the two-variable accumulator-then-canonical-copy pattern, needed because "exactly one Set Variable assigns State Present/Note Present" cannot otherwise coexist with genuinely nested If/Otherwise branch logic); one is an evidence-grounded inference from a same-type sibling parameter (Append to Note's `entity`, modelled on Show Note's already-working `target`); one is a defensive correctness addition (Get Item from List before treating a Find Notes result as a single Note); and one is a build-methodology choice (restructuring via a Python/plistlib script, verified byte-for-byte round-trip-faithful to the source file's own formatting before any change was made, given the scale of relocation this plan required).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrected the OPEN-branch anchor Comment, made stale by this plan's own hoist**
- **Found during:** Task 1, while relocating the state-load chain above the router
- **Issue:** 02-03 authored the OPEN-branch anchor Comment anticipating that "plan 02-04 inserts the shared bootstrap check here first, ahead of everything else" — i.e., inside the OPEN branch itself. Task 1's actual, explicit instruction is the opposite: hoist the chain above the *entire* router, never duplicate it into the OPEN or CLOSE branches. Left uncorrected, the Comment would tell Phase 3 to expect a bootstrap check inside the OPEN branch that was never placed there.
- **Fix:** Rewrote the Comment to state what is actually true after this plan: the shared setup check now runs once, above the whole router, so Phase 3 does not need to repeat or expect it inside this branch.
- **Files modified:** `src/PROSOCHE-Dumb.xml`
- **Verification:** `validate-shortcut` passes; the phase-closure audit confirms the Comment still immediately precedes the OPEN branch's `Nothing` anchor with no structural change.
- **Committed in:** `1e18533`

**2. [Rule 2 - Missing Critical] Extended `UA-01` and `UA-04` cross-references rather than leaving the two new on-device facts untracked**
- **Found during:** Task 3, while walking the whole-graph audit and Task 3's own `<human-check>` block
- **Issue:** Plan 02-04's own human-check names two device-only facts (no-duplicate-on-second-tap, a deleted Note recreated with its full body) that no existing `UA-NN` item names verbatim, and the plan's action text explicitly instructs recording them "against UA-01."
- **Fix:** Extended `UA-01` with both observations, cross-referencing the already-existing `UA-04` for the state-file half of the no-duplicate check rather than duplicating its wording, per the project's own extend-not-duplicate discipline (matching the precedent 02-02 and 02-03 already set for `UA-01` and `UA-07`).
- **Files modified:** `docs/BUILD-NOTES.md`
- **Verification:** Confirmed pure-append via `git diff` (zero lines removed across the whole document).
- **Committed in:** `e1d43d7`

---

**Total deviations:** 2 auto-fixed (1 bug/Rule 1, 1 missing-critical/Rule 2)
**Impact on plan:** Both were necessary to keep the graph's own Comments and the project's device-fact tracking honest and internally consistent after this plan's restructuring. Neither weakens an acceptance criterion, removes scope, or changes routing/state behaviour.

## Known Stubs

No new stubs were introduced by this plan. The OPEN and CLOSE branch anchors (`Comment` + `Nothing`, inside the `FA045F2B`/`A2F7247B` blocks) remain exactly as 02-03 left them, unchanged by this plan's edits — already recorded as ledger entries 1 and 2 in `.planning/WINDOWS.md` (owned by Phase 3 and Phase 4 respectively). This plan's own new content — the two-field validity gate, the import normalisation, the Note-existence guard, and the recovery line — is fully wired with no placeholder values, no hardcoded empty outputs, and no deferred logic.

## Issues Encountered

The original single-pass build (all of Task 1 and Task 2's XML changes constructed together) had to be discarded and rebuilt as two sequential passes once it became clear a single combined diff could not be split cleanly into two atomic, independently-verifiable commits matching the plan's task boundaries. Resolved by rebuilding Task 1's own intermediate state first (verified against its own `<verify>` script and committed), then transforming that committed state into Task 2's final shape (verified against its own `<verify>` script and committed) — no broken or half-verified state was ever committed.

## User Setup Required

None - no external service configuration required. This plan's on-device-only facts are covered by the extended `UA-01` (observations e and f) and the existing `UA-04` in `docs/BUILD-NOTES.md` §6, gated on Phase 2's on-device confirmation pass, same as every other Phase 2 UA item — none of these block this plan or any later phase's build work.

## Next Phase Readiness

`src/PROSOCHE-Dumb.xml` validates at `--target-macos 26 --target-platform all` with 133 actions and is, per this plan's own phase-closure audit, feature-complete for Phase 2's entire scope: every requirement Phase 2 owns (`BOOT-01` through `BOOT-09`, `STATE-12`, `ROOM-01` through `ROOM-06`) is now mapped to specific structural evidence or a named on-device observation in `docs/BUILD-NOTES.md` §7, and `.planning/ROADMAP.md` reflects Phase 2 as complete. Phase 3 (Deterministic State Engine) inherits a stable, self-healing foundation to read and write `State` through — the nullable-parent guard rule (six fields: `last_open_at`, `last_close_at`, `last_app`, `active_session`, `cooldown_until`, and every key beneath `active_session`) is recorded in-graph at the point Phase 3 will first need it. Phase 6 and Phase 7 inherit the lazy-guard-before-append rule for their own future Note appends from the OPEN/CLOSE path, recorded in `docs/BUILD-NOTES.md` §10. The open items are the same class already open across Phase 2 — `UA-01` (extended), `UA-03` through `UA-07` — all gated on Phase 2's single on-device bootstrap-and-automations pass, not yet performed since no iPhone is available in this build environment; nothing about them blocks Phase 3.

---
*Phase: 02-routing-bootstrap-control-room*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: `src/PROSOCHE-Dumb.xml`
- FOUND: `docs/BUILD-NOTES.md`
- FOUND: `.planning/ROADMAP.md`
- FOUND: `.planning/phases/02-routing-bootstrap-control-room/02-04-SUMMARY.md`
- FOUND: commit `1e18533`
- FOUND: commit `cd53919`
- FOUND: commit `e1d43d7`
