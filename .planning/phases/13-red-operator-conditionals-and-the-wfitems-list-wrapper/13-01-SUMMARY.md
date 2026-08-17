---
phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
plan: 01
subsystem: infra
tags: [shortcuts, plist, wfitems, list-wrapper, build-guards, generator, mirror, circ-07, donor-evidence]

# Dependency graph
requires:
  - phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
    plan: "12-02"
    provides: "the two-ways guard-sensitivity procedure (direct call + full-build revert, restore to a byte-identical digest) and the per-fork arming convention this plan copies"
provides:
  - "_list_row() -- the donor-fixed WFItems row discriminator: a bare str stays bare, anything else is nested verbatim under {WFItemType: 0, WFValue: ...}"
  - "mirror_text() emits all 660 Mirror rows in the iOS row wrapper, on both forks"
  - "verify_list_item_wrappers() -- build-time guard that aborts before SOURCE.write_bytes() if any WFItems row is a dict lacking WFItemType"
  - "the guard armed on the Aware fork at BOTH touch points (import list + bare call), the pair Phase 12 regressed by hitting only one"
  - "three verbatim SystemExit sensitivity transcripts, recorded in the Task 2 commit body for 13-03 to transcribe into docs/BUILD-NOTES.md section 28"
affects: [13-02, 13-03, 13-04, mirror_and_voice, Phase-19-device-UAT]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Two-kind WFItems row rule: a literal row is a bare string, an attachment-bearing row is {WFItemType: 0, WFValue: <WFTextTokenString>}; the wrapper nests the existing envelope verbatim so attachmentsByRange offsets cannot shift"
    - "Type-branching in an emitter helper (isinstance(item, str)) -- a NEW idiom for this codebase, fixed by donor evidence rather than by an in-file analog; 13-PATTERNS.md 'No Analog Found' records there is no isinstance-based literal/variable discriminator anywhere in :134-660"
    - "Per-row (action index, row position) offender tuples in a guard, extending the flat action-index accumulator every sibling guard uses, because the defect is per row and an action-level message would hide ten rows behind one number"
    - "Guard sensitivity demonstrated THREE ways -- direct call, full-build revert on Core, full-build revert on Aware -- because a two-way demonstration on Core alone cannot prove the per-fork arming works"
    - "A pinned ABSOLUTE phase-start SHA as the known-defective subject, never a relative ref, so the demonstration cannot silently retarget if the task lands as more than one commit"

key-files:
  created: []
  modified:
    - "tools/build_state_engine.py"
    - "tools/build_sentient.py"
    - "src/PROSOCHE-Dumb.xml"
    - "src/PROSOCHE-Sentient.xml"

key-decisions:
  - "Branch per ROW on isinstance(item, str), never sweep the WFItems= expression -- list_items() at :416-419 emits the byte-identical expression correctly, so an expression-level sweep would have wrapped its six EXIT_NAMES literal rows and produced an unforced EXIT-08 regression. The emitter cannot tell the two call sites apart; only the row value's Python type can."
  - "WFItemType is encoded ONLY as 0, and both the helper docstring and the guard docstring state explicitly that other values are deliberately unaudited and must not be guessed -- Donors 4 and 4.1 exercise only text rows, and a guess would enter the project record as evidence (prohibition P-01)."
  - "The guard asserts only that the WFItemType KEY is present, never which value it holds -- asserting == 0 would silently encode the same unaudited claim the prohibition forbids, one level down."
  - "WFValue nests the existing WFTextTokenString object verbatim: no deep copy, no rebuild, no re-serialization. That is what keeps every attachmentsByRange offset valid, and it is why the fix introduces no new uid() call and byte-idempotency survives."
  - "The guard is registered after verify_conditional_action_string() and before verify_numeric_operands(), strictly above the single SOURCE.write_bytes() -- no other guard fires on an unwrapped row, so this position introduces no ordering mask, which both full-build demonstrations then confirmed empirically."
  - "docs/manifest_check.py was left RED rather than 'fixed'. Its failure is the expected D-04 consequence of regenerating the sources; editing MANIFEST rows without re-signing would have been exactly the silencing prohibition P-02 forbids. Plan 13-04 owns the re-sign."
  - "Task 2 was committed with --allow-empty. Every mutation it makes is temporary and restored, so its only durable output is the recorded evidence, and the commit body IS the deliverable."

patterns-established:
  - "When an emitter helper and a correct sibling share a byte-identical expression, fix the VALUE not the EXPRESSION -- the discriminator belongs at the row level where the type difference actually lives"
  - "A per-fork guard demonstration must revert the fork's OWN input and run the fork's OWN generator; offender indices that differ between forks (1141 on Core, 1209 on Aware) are positive evidence the raise came from the fork's own traversal rather than being inherited"

requirements-completed: [CIRC-07, DIST-01]
requirements-regression-protected: [CIRC-04, ROOM-03]

coverage:
  - id: D1
    description: "Every variable-bearing row of every is.workflow.actions.list action in both forks is serialized as {WFItemType: 0, WFValue: <WFTextTokenString>} -- exactly 660 wrapped rows per fork, and zero rows left as a raw WFTextTokenString sitting directly in a WFItems array"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "plistlib walk over src/PROSOCHE-Dumb.xml and src/PROSOCHE-Sentient.xml: len(wrapped) == 660, len(unwrapped) == 0, per fork"
        status: pass
    human_judgment: false
  - id: D2
    description: "The six bare-string rows emitted by list_items(EXIT_NAMES, ...) remain bare string elements in both forks -- Donor 4 shows literal rows stay bare, so wrapping them would be an unforced EXIT-08 regression rather than a fix"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "len(bare) == 6 per fork in the same plistlib walk; git diff shows no hunk inside list_items() at tools/build_state_engine.py:416-419"
        status: pass
    human_judgment: false
  - id: D3
    description: "verify_list_item_wrappers() raises SystemExit (never assert) before src/PROSOCHE-Dumb.xml is written, and its message carries the prose cause, the first five offenders as action/row pairs, and the total count"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "AST: zero ast.Assert nodes and at least one ast.Raise in the guard body; max(guard call lineno) 4248 < min(write_bytes lineno) 4272 inside main(). Empirically: the Core full-build revert exited 1 with src/PROSOCHE-Dumb.xml's sha256 unchanged across the failed build"
        status: pass
    human_judgment: false
  - id: D4
    description: "The new guard is armed on BOTH forks -- verify_list_item_wrappers appears in tools/build_sentient.py's `from build_state_engine import (...)` list AND as a bare call statement in its guard block"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "AST assertion over tools/build_sentient.py: the name is in the ImportFrom names for module build_state_engine AND present as an Expr(Call(Name(...))) statement. A raw grep -c was deliberately NOT used -- the justification comment also matches `verify_`, making the count a lower bound"
        status: pass
    human_judgment: false
  - id: D5
    description: "The rebuild stays byte-idempotent -- a second consecutive build of each fork produces an identical SHA-256 -- because the wrapper change introduces no new uid() call"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "python3 docs/phase6_self_check.py exits 0 (builds twice, compares digests). Independently: both forks were rebuilt four separate times across the two tasks and every rebuild reproduced 99388cad... / d01154b3..."
        status: pass
    human_judgment: false
  - id: D6
    description: "The Confession flow is untouched by the wrapper fix: docs/phase5_self_check.py exits 0 after the rebuild and the number of is.workflow.actions.list actions per fork is still exactly 67"
    requirement: "CIRC-04"
    verification:
      - kind: integration
        ref: "python3 docs/phase5_self_check.py exit 0; len(lists) == 67 per fork in the plistlib walk. REGRESSION-PROTECTION ONLY -- this plan repairs no CIRC-04 site and claims no CIRC-04 implementation work"
        status: pass
    human_judgment: false
  - id: D7
    description: "_list_row() is applied element-wise, so a zero-row List yields an empty WFItems array and a one-row List yields a one-element array; the per-action row counts are exactly one action with 6 rows and 66 actions with 10 rows, identical to the pre-fix distribution"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "sorted(len(WFItems) for each list action) == [6] + [10]*66, asserted per fork"
        status: pass
    human_judgment: false
  - id: D8
    description: "Row offsets survive the wrapper unchanged: every wrapped row's WFValue.Value.string is BMP-only (no code point above U+FFFF) and every attachmentsByRange key {p, 1} indexes a U+FFFC placeholder at position p, so Python len()-derived offsets equal iOS UTF-16 code-unit offsets"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "per wrapped row: WFValue.WFSerializationType == 'WFTextTokenString'; max(ord(c)) <= 0xFFFF; s[p] == '\\ufffc' for every attachmentsByRange key -- all 660 rows, both forks"
        status: pass
    human_judgment: false
  - id: D9
    description: "The Note's Automation B steps are unregressed through the rebuild"
    requirement: "ROOM-03"
    verification:
      - kind: integration
        ref: "python3 docs/note_identity_check.py exit 0. REGRESSION-PROTECTION ONLY -- the Note body is a hand-authored text template with no defect site in this family"
        status: pass
    human_judgment: false
  - id: D10
    description: "Both forks pass the Shortcuts Playground validator at the iOS 26 target"
    requirement: "DIST-01"
    verification:
      - kind: integration
        ref: "validate-shortcut src/PROSOCHE-{Dumb,Sentient}.xml --target-macos 26 --target-platform all -- 'Validation passed.', exit 0 on both. Gate B was not run and appears in no chain"
        status: pass
    human_judgment: false
  - id: D11
    description: "Item At Index selection over a WRAPPED List returns the same row content it returned over an unwrapped List"
    requirement: "CIRC-07"
    verification:
      - kind: backstop
        ref: "Device-only (13-RESEARCH.md Open Question 1 / assumption A4) -- no donor chains a wrapped List into getitemfromlist. The file-level guarantee held here IS verified: row count and row ordering per List action are unchanged ([6] + [10]*66, identical to pre-fix), WFItemSpecifier and WFItemIndex are untouched, and no arithmetic and no uid() call was introduced. Extraction semantics are owned by Phase 19 device UAT"
        status: deferred
    human_judgment: true

# Metrics
duration: 30 min
completed: 2026-08-17
status: complete
---

# Phase 13 Plan 01: WFItems List row wrapper Summary

**All 660 variable-bearing Mirror rows in both forks now carry the donor-confirmed `{WFItemType: 0, WFValue: <WFTextTokenString>}` iOS row wrapper while the six literal rows stay bare, enforced by a new `verify_list_item_wrappers()` that aborts before the single write, armed on both forks at both touch points, and demonstrated to fire three separate ways — closing the CIRC-07 blank-Mirror defect that no validator, catalog or signed-artifact decrypt could ever have seen.**

## Performance

- **Duration:** ~30 min
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- **Fixed the real defect, at the one site that causes all 66 instances.** `mirror_text()` placed raw `WFTextTokenString` dicts directly into `WFItems`. Such a row validates, signs and imports perfectly and then renders as an **empty row** on device — so the Mirror's `Item At Index` selection can land on a blank template, which is precisely the failure CIRC-07 forbids. One branch in one emitter fixed all 66 actions and all 660 rows in each fork.
- **Reported the measured scale rather than the recorded one.** The ROADMAP claims "2 confirmed instances." Direct `plistlib` measurement of the phase-start artifact confirms **66 defective actions carrying 660 unwrapped rows per fork** — 33× more actions and 330× more rows. The measurement was re-derived independently here (not merely trusted from 13-RESEARCH.md) by asserting the pre-fix subject carried exactly 660 unwrapped rows before it was used as a demonstration subject.
- **Did not corrupt the correct sibling.** `list_items()` at `:416-419` emits the byte-identical `WFItems=list(items)` expression and is **correct** — its callers pass plain strings, and Donor 4 shows literal rows stay bare. `git diff` shows no hunk inside that function; the post-fix measurement confirms exactly 6 bare rows survive, which is the count an expression-level sweep would have destroyed.
- **Armed the guard on both forks at both touch points.** Phase 12 regressed here by editing only one of `build_sentient.py`'s two sites. Both were hit, and the proof is an **AST assertion** — the name must appear in the `ImportFrom` names for `build_state_engine` *and* as a bare `Expr(Call(Name(...)))` statement. The plan's warning against a raw `grep -c verify_` was honoured: the justification comment naming the guard also matches `verify_`, so a count is a lower bound, not an equality.
- **Demonstrated the guard is sensitive three ways, not two.** A direct call against the pre-fix artifact recovered from the pinned SHA; a full-build revert on Core; and a full-build revert on **Aware**, which is the half Phase 12 missed and the entire reason the per-fork arming exists. In both full-build reverts the source digest was **unchanged across the failed build** — the empirical proof the raise landed before `SOURCE.write_bytes()` rather than after it.
- **Proved the pass is non-vacuous.** In the same process that captured the failure, the same guard was called against both post-fix forks and returned without raising. A guard that never fires is false assurance (T-13-02, ASVS V7).

## Task Commits

Each task was committed atomically:

1. **Task 1 (tracer): wrap variable-bearing List rows in the donor-confirmed iOS WFItems envelope** — `fe2cbb6` (fix)
2. **Task 2: demonstrate `verify_list_item_wrappers()` is sensitive, three ways** — `cc93b3e` (test, `--allow-empty`)

## Files Created/Modified

- `tools/build_state_engine.py` — added `_list_row()` immediately above `mirror_text()`; changed `mirror_text()`'s `WFItems` argument to apply it element-wise; added `verify_list_item_wrappers()` beside `verify_conditional_action_string()`; registered the guard in `main()`'s verify chain.
- `tools/build_sentient.py` — added `verify_list_item_wrappers` to the `from build_state_engine import (...)` list in alphabetical position (between `verify_exit_events_seed` and `verify_numeric_operands`), and added the bare call to the guard block with a per-fork justification comment in the established Phase 12 style.
- `src/PROSOCHE-Dumb.xml` — regenerated Core fork, `99388cad597417685eb8624a0b4b34e18a6bd30805ac38beb2f3188026c3e679`.
- `src/PROSOCHE-Sentient.xml` — regenerated Aware fork, `d01154b3e1b5990e5d3bc6d92e8dd895b92d0448217356772d077022e5215666`.

## Decisions Made

- **Branch per row, never sweep the expression.** `mirror_text()` and `list_items()` emit a byte-identical `WFItems=list(items)` line; only the row *value's* Python type distinguishes them. The discriminator therefore belongs at the row, not at the expression. This is the single load-bearing nuance of the whole plan and the specific corruption 13-RESEARCH.md Pitfall 1 names.
- **`WFItemType` is encoded only as `0`, and said so twice.** Both new docstrings state explicitly that other values are deliberately unaudited because no donor exercises a non-text row. The guard goes one step further and asserts only that the **key is present**, never which value it holds — asserting `== 0` would have silently encoded the same unaudited claim one level down. (Prohibition P-01.)
- **`WFValue` nests the existing envelope verbatim.** No deep copy, no rebuild, no re-serialization. That is what keeps every `attachmentsByRange` offset valid, and it is why no new `uid()` call was introduced and byte-idempotency survives.
- **Guard placement introduces no ordering mask.** Registered after `verify_conditional_action_string()` and before `verify_numeric_operands()`, strictly above the single write. No other guard fires on an unwrapped row — asserted in the plan, and then *confirmed empirically*: in both full-build reverts `verify_list_item_wrappers()` was the guard that raised, so no fallback to the direct-call result was needed and the chain order was never touched.
- **`docs/manifest_check.py` left red, deliberately.** Its failure is the expected D-04 consequence of regenerating the sources. Editing MANIFEST rows without re-signing, or weakening the checker, is exactly the silencing prohibition P-02 forbids. Plan 13-04 owns the re-sign.
- **Task 2 committed `--allow-empty`.** Every mutation it makes is temporary and restored, so its only durable output is the recorded evidence and the commit body *is* the deliverable. Recording it as an empty commit is more honest than manufacturing a file change to carry it.
- **The demonstration subject was a pinned absolute SHA (`698ab99`), never a relative ref**, and its defectiveness (exactly 660 unwrapped rows) was asserted before it was used — so the demonstration cannot silently succeed against the wrong artifact.

## Deviations from Plan

None — plan executed exactly as written. No deviation rule was invoked; no auto-fix was required; no fix-attempt limit was approached.

One observation worth recording precisely rather than smoothing over, because it *looks* like a discrepancy and is not:

- **The Aware full-build revert's offender indices are `1209`, not Core's `1141`.** The plan's step 3 asks for "the same guard message." The prose and the `660 total` are identical across all three demonstrations; only the action indices differ. That difference is the point, not noise: Aware inserts its own actions ahead of the Mirror block, so `1209` is the Aware fork's **own** index for the same first offending List action. An inherited-from-Dumb failure would have carried Dumb's `1141`. The differing index is therefore positive evidence that `build_sentient.py`'s own traversal raised — exactly what a per-fork assertion has to prove. Recorded in the Task 2 commit body in these terms.

## Issues Encountered

None. Every build behaved as predicted, every guard fired only where intended, and every temporary mutation was restored via `git checkout --` to a byte-identical digest. `git status --short` is empty and `git diff --quiet` exits 0 over all four plan files.

## Verification Results

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebbf… HEAD` (D-01 provenance) | exit 0, re-checked before every generator invocation |
| Baseline before any edit — 12 × `docs/*.py` | **all PASS** (so any red during execution is caused by this plan) |
| Baseline before any edit — gate A, both forks | `Validation passed.` on both |
| `python3 tools/build_state_engine.py` | exit 0 |
| `python3 tools/build_sentient.py` | exit 0, digest `d01154b3e1b5990e5d3bc6d92e8dd895b92d0448217356772d077022e5215666` |
| `is.workflow.actions.list` actions, per fork | **67** (unchanged) |
| Wrapped rows, per fork | **660** |
| Bare-string literal rows, per fork | **6** |
| Dict rows lacking `WFItemType`, per fork | **0** |
| Per-action row counts, per fork | `[6] + [10]*66` — identical to the pre-fix distribution |
| Every wrapped row's `WFValue.WFSerializationType` | `WFTextTokenString` — envelope preserved, all 660 rows, both forks |
| Row strings BMP-only (no code point > U+FFFF) | confirmed, all 660 rows, both forks |
| Every `attachmentsByRange` key `{p, 1}` indexes `U+FFFC` at `p` | confirmed, all 660 rows, both forks |
| `git diff` inside `list_items()` (`:416-419`) | **no hunk** — the must-not-touch sibling is byte-identical |
| AST: `_list_row` and `verify_list_item_wrappers` module-level in the Dumb generator | both FOUND |
| AST: `ast.Assert` nodes inside the guard body | **0** — SystemExit convention held |
| AST: `ast.Raise` nodes inside the guard body | ≥1 |
| AST: guard registered above the single write, inside `main()` | call line **4248** < `write_bytes` line **4272** |
| AST: Aware touch point A (`ImportFrom` names for `build_state_engine`) | `verify_list_item_wrappers` present |
| AST: Aware touch point B (bare `Expr(Call(Name(...)))`) | `verify_list_item_wrappers` present |
| `python3 docs/phase6_self_check.py` (double-build byte-idempotency) | exit 0 — no new `uid()` call |
| `python3 docs/phase5_self_check.py` (CIRC-04 regression) | exit 0 |
| `python3 docs/note_identity_check.py` (ROOM-03 regression) | exit 0 |
| `python3 docs/sequence_dispatch_check.py` (Mirror dispatch) | exit 0 |
| Other checkers — `environmental_restore`, `phase7`, `phase9`, `router_ui_census`, `sentient_audit`, `sentient_core`, `state_engine_self_check` | exit 0 (**eleven green in total**) |
| `python3 docs/manifest_check.py` | **EXPECTED RED (D-04)** — `AssertionError: row 'Core source': MANIFEST declares 2831992 bytes, src/PROSOCHE-Dumb.xml is 2916560 bytes`. Owned by plan 13-04. Not silenced, not "fixed" by editing rows without re-signing |
| Gate A, Core fork (`--target-macos 26 --target-platform all`) | `Validation passed.`, exit 0 |
| Gate A, Aware fork (`--target-macos 26 --target-platform all`) | `Validation passed.`, exit 0 |
| Gate B | **not run, not chained** — advisory only, permanent waiver, structurally incapable of exiting 0 |
| Demonstration subject provenance | pinned absolute SHA `698ab99`, confirmed ancestor of HEAD, confirmed to carry exactly **660** unwrapped rows before use |
| Guard sensitivity (direct call) | `verify_list_item_wrappers()` raised `SystemExit` against `698ab99:src/PROSOCHE-Dumb.xml`: `List rows carry a raw WFTextTokenString instead of the iOS {WFItemType, WFValue} wrapper (renders blank on device): action 1141 row 0, action 1141 row 1, action 1141 row 2, action 1141 row 3, action 1141 row 4 (660 total)` |
| Guard sensitivity (non-vacuity) | the same guard, same process, returned **without raising** on both post-fix forks |
| Guard sensitivity (full build, Core) | `mirror_text()`'s `WFItems` argument reverted to `list(items)` → `python3 tools/build_state_engine.py` exited **1** with the **byte-identical** message; `src/PROSOCHE-Dumb.xml` sha256 **unchanged** across the failed build (`99388cad…` before and after) — the raise preceded `SOURCE.write_bytes()`. Restored via `git checkout --`, rebuilt, digest byte-identical |
| Guard sensitivity (full build, Aware) | `src/PROSOCHE-Dumb.xml` overwritten with the pre-fix blob from `698ab99` (2831992 bytes, `589ee121…`; working tree only, index untouched) → `python3 tools/build_sentient.py` alone exited **1** with the same prose and same `660 total`, at the Aware fork's own indices `action 1209 row 0…4`; `src/PROSOCHE-Sentient.xml` sha256 **unchanged** (`d01154b3…` before and after). Restored via `git checkout --`, both forks rebuilt, both digests byte-identical |
| Ordering mask | **none** — `verify_list_item_wrappers()` was the guard that raised in both full-build reverts; no fallback needed; the verify chain order was not changed |
| Working tree after both task commits | `git status --short` empty; `git diff --quiet` over all four plan files exits 0 |
| Scratch artifacts committed | **none** — all scratch scripts live in the session scratchpad, outside the repository |
| No file deletions in either commit | `git diff --diff-filter=D --name-only HEAD~1 HEAD` empty for `fe2cbb6`; `cc93b3e` is an empty commit |

## Known Stubs

None. No hardcoded empty value, placeholder string, TODO, FIXME or unwired component was introduced. The one knowingly-deferred item (D11, `Item At Index` extraction semantics over a wrapped List) is a **plan-declared `backstop`**, not a stub: the file-level half of it is fully verified here (row count, row ordering, `WFItemSpecifier`/`WFItemIndex` untouched, no new arithmetic, no new `uid()`), and only the device-observable half is deferred to Phase 19 UAT, which 13-RESEARCH.md Open Question 1 and assumption A4 already own.

## Threat Flags

None. No new network endpoint, auth path, file-access pattern or trust-boundary schema change was introduced. The register's `mitigate` dispositions are discharged as planned:

- **T-13-01 (Tampering, `_list_row()`/`mirror_text()`)** — branched on `isinstance(item, str)`; measured 660 wrapped **and** 6 bare per fork. A blanket sweep would have shown 666 wrapped / 0 bare and failed the assertion.
- **T-13-02 (Repudiation, the guard)** — three-way sensitivity demonstration against a known-defective artifact recovered from git, plus a non-vacuous pass on both post-fix forks in the same process.
- **T-13-03 (DoS, Aware arming)** — AST assertion of both touch points, immune to the comment noise that makes a raw `grep -c verify_` a lower bound.
- **T-13-04 (Tampering, rebuild provenance)** — `git merge-base --is-ancestor 7ca8ebbf… HEAD` exited 0 before every generator invocation in both tasks.
- **T-13-06 (Tampering, the single write)** — guard registered strictly above `SOURCE.write_bytes()` (AST line 4248 < 4272), and **both** full-build reverts confirmed the digest unchanged across a failing build.
- **T-13-07 (Spoofing, donor provenance)** — the wrapper shape was taken only from the verbatim decrypted XML in 13-RESEARCH.md; no shape was extended, and `WFItemType` values beyond `0` stay unaudited by explicit docstring statement.
- **T-13-05 / T-13-SC (accept)** — unchanged: rows carry generator-authored constants only, and this plan ran no package-manager install.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

**Ready.** The remaining plans in this phase start from the baseline they were written against:

- **13-02** (pin the Donor-5-confirmed conditional shape) — untouched by this plan. No `WFConditionalActionString` site was modified; `verify_conditional_action_string()` was extended by exactly zero lines, only appended *after*. Its 20 variable-bearing sites per fork are exactly as this plan found them.
- **13-03** (docs) — the three verbatim `SystemExit` transcripts, the pre/post digests for both forks, and the pinned subject SHA are all recorded in the `cc93b3e` commit body, ready to transcribe into `docs/BUILD-NOTES.md` §28. Note for the doc pass: the List row wrapper is a **new, eighth parameter-defect axis** (a *container* defect), distinct from axis 2's string-envelope defect — and the `WFItemType`-beyond-`0` gap must be written up as unsettled, never inferred.
- **13-04** (re-sign, MANIFEST, UAT) — `docs/manifest_check.py` is red for exactly one known reason and both source XMLs are final and gate-A clean, so the re-archive/re-sign can proceed directly. All six MANIFEST size/SHA-256 rows are stale; the new source digests are `99388cad…` (Core) and `d01154b3…` (Aware).

**Carried forward, not blockers** — the three probe rows the plan declined to resolve are restated here rather than dropped: `CIRC-07 / unclassified` (the probe could not classify the Mirror requirement into a shape category, notwithstanding the direct 660/0 criterion this plan does carry), `ROOM-03 / unclassified` (hand-authored Note template, no derivable shape predicate, regression-protected only), and `DIST-01 / unclassified` (gate A is binary with no derivable shape edge; surfaces in 13-04). Assumption **A4** — that wrapping does not change `getitemfromlist` extraction semantics — remains device-only and is owned by Phase 19 UAT, which must assert "Mirror renders non-empty text" against a **re-imported** build; a user still running the previously signed artifact keeps the blank-row Mirror until they re-import, which is inherent to Shortcuts distribution and needs no migration.

## Self-Check: PASSED

- `tools/build_state_engine.py` — FOUND
- `tools/build_sentient.py` — FOUND
- `src/PROSOCHE-Dumb.xml` — FOUND
- `src/PROSOCHE-Sentient.xml` — FOUND
- `.planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-01-SUMMARY.md` — FOUND
- Commit `fe2cbb6` — FOUND in `git log`
- Commit `cc93b3e` — FOUND in `git log`
- Working tree clean after both task commits (`git status --short` empty)
- No file deletions in either commit (`git diff --diff-filter=D` empty)

---
*Phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper*
*Completed: 2026-08-17*
