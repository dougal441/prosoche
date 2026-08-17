---
phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
plan: 02
subsystem: infra
tags: [shortcuts, plist, conditional, wfconditionalactionstring, build-guards, generator, donor-evidence, circ-07, refutation]

# Dependency graph
requires:
  - phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
    plan: "13-01"
    provides: "both forks building clean with the wrapped Mirror rows, eleven of twelve docs/*.py checkers green, and the --allow-empty evidence-commit convention this plan reuses"
  - phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
    plan: "12-03"
    provides: "the direct-call isolation technique for a masked second assertion, applied here in advance rather than discovered mid-execution"
provides:
  - "verify_conditional_action_string() extended with a POSITIVE assertion pinning the Donor-5 WFTextTokenString envelope on every variable-bearing comparison target"
  - "the refutation of the ROADMAP's '14 defective sites' claim, recorded in the guard's own docstring so it travels with the code rather than only with planning prose"
  - "an explicit in-code statement that the 172/175 raw-literal comparison targets are deliberately unasserted, and why"
  - "four verbatim SystemExit transcripts plus the full-build revert transcript, recorded in the Task 2 commit body for 13-03 to transcribe into docs/BUILD-NOTES.md section 28"
  - "the ordering mask between the guard's two raises, demonstrated and recorded rather than engineered around"
affects: [13-03, 13-04, mirror_and_voice, Phase-19-device-UAT]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A guard that PINS a device-confirmed shape rather than repairing a broken one -- the failure message says the change that tripped it is the defect, inverting the usual guard semantics"
    - "Two disjoint-by-Python-type checks sharing one loop and one pair of continue guards: a str comparison against the raw placeholder, and a dict-only positive envelope check"
    - "Whole-function byte-comparison via ast.get_source_segment across two git revisions, as the must-not-touch proof for emitters -- strictly stronger than a def-line diff grep, which matches only the signature"
    - "Recording an ABSENT touch point as a decision: when a guard is already armed on both forks, the two-touch-point rule has a genuine exception that must be stated, not inferred"
    - "Demonstrating an ordering mask by tripping both assertions in one action list and showing only the first message, instead of reordering the chain to avoid it"

key-files:
  created: []
  modified:
    - "tools/build_state_engine.py"
    - "tools/build_sentient.py"

key-decisions:
  - "PIN, DO NOT FIX. Donor 5 shows iOS itself authoring the exact construct the ROADMAP suspected of being defective, so sweeping the 20 variable-bearing sites would have replaced a device-confirmed shape with a guess -- what the do-not-fabricate rule forbids outright. The deliverable inverted from a repair into a positive assertion."
  - "The refutation lives in the guard's docstring, not only in planning prose. The standing risk was never that the shape is wrong; it is that the ROADMAP, HANDOFF.md and the pending todo all still assert it is, inviting a future pass to 'repair' 20 correct sites. Prose scrolls out of context; a docstring beside the code does not."
  - "The 172/175 raw-literal comparison targets were left untouched AND unasserted, stated explicitly in the docstring. Donor 5 covers only the variable-bearing case; no donor covers the pure literal. Inventing an assertion for them would encode a guess as a build gate (T-13-11, D-03)."
  - "The pin asserts only the three properties Donor 5 actually exhibits -- serialization type, a U+FFFC in the string, a non-empty attachmentsByRange. It says nothing about WFCondition, coercion aggrandizements or literal values, so it cannot block a legitimate future shape the donor does not speak to (T-13-13)."
  - "NO new tools/build_sentient.py touch point was added, and the absence was recorded as a decision. verify_conditional_action_string was already imported and already invoked, armed by Phase 12 (12-01, PD-3). Only the per-fork justification comment changed. An unstated absence would read as the two-touch-point regression Phase 12 actually committed."
  - "The ordering mask was demonstrated, never worked around. main()'s verify chain order and the order of the two raises inside the function are both byte-identical to Task 1's committed version. Reordering either to make a demonstration convenient is the weakening the plan's prohibitions forbid."
  - "The Aware-side re-demonstration was deliberately omitted, with the reason recorded. The same function object is reached through the same already-armed call; Phase 12 already demonstrated it there. This is the opposite of 13-01's situation, where the guard was NEWLY armed on Aware and the arming itself was the thing under test."
  - "docs/manifest_check.py left RED, unchanged from 13-01. Its failure is the expected D-04 consequence of the wave-1 rebuild. Plan 13-04 owns the re-sign."
  - "Task 2 committed --allow-empty, following 13-01. Every mutation is temporary and restored, so the commit body IS the deliverable; manufacturing a file change to carry it would be less honest."

patterns-established:
  - "When measurement refutes the project record, the refutation belongs in the code the record is wrong about -- a docstring paragraph carrying the measured counts and the superseded claim, so the next reader cannot re-litigate it from the guard alone"
  - "A guard extension must prove the PRE-EXISTING assertion still has teeth, not only that the new one fires -- otherwise the extension can silently disarm what it was added beside"

requirements-completed: [CIRC-07, DIST-01]
requirements-regression-protected: [CIRC-04, ROOM-03, EXIT-08]

coverage:
  - id: D1
    description: "verify_conditional_action_string() carries a POSITIVE assertion that a variable-bearing WFConditionalActionString is a WFTextTokenString whose Value.string contains U+FFFC and whose Value.attachmentsByRange is non-empty -- the shape Donor 5 shows iOS itself authoring"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "AST over tools/build_state_engine.py: exactly 2 ast.Raise nodes and 0 ast.Assert nodes inside the guard; the second raise is reached only from the isinstance(value, dict) branch"
        status: pass
    human_judgment: false
  - id: D2
    description: "The pin passes non-vacuously: exactly 20 variable-bearing sites per fork, all conforming, 0 offenders -- the sites were already correct at HEAD and this plan changed none of them"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "plistlib walk over both rebuilt artifacts: 192 (Core) / 195 (Aware) mode-0 conditionals carrying the slot; 20 variable-bearing each with codes [4]*19 + [99]; every one carries WFSerializationType == WFTextTokenString, a U+FFFC in Value.string and a non-empty Value.attachmentsByRange; 0 pin offenders"
        status: pass
    human_judgment: false
  - id: D3
    description: "No emission site was swept: token(), if_block() and list_items() are byte-identical to the pinned absolute SHA 698ab99, and the raw-literal count is unchanged at 172 Core / 175 Aware"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "ast.get_source_segment on BOTH revisions, whole-function byte comparison (not a def-line grep, which would match only the signature and let a body edit pass silently -- T-13-08). Independently: git status showed only the two .py files modified, and both source XML digests were unchanged through the whole plan"
        status: pass
    human_judgment: false
  - id: D4
    description: "The two raise statements are demonstrably distinguishable, each fired against its own synthetic mutation, and the ordering mask between them is recorded verbatim rather than removed by reordering"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "Four direct-call variants in one process: pin isolated (pin message, '1 total'), bare-placeholder (legacy message, textually different), both-in-one-list (ONLY the legacy message, mask confirmed), and both shipped forks (no raise). Plus the full-build revert of token(), which exited 1 naming 20 offenders"
        status: pass
    human_judgment: false
  - id: D5
    description: "The Aware fork needs no new touch point because verify_conditional_action_string is already in build_sentient.py's import list and already called; both remain present, and the reason no third touch point exists is recorded in code and in the commit body"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "AST over tools/build_sentient.py: the name is in the ImportFrom names for build_state_engine AND present as an Expr(Call(Name(...))) statement -- asserted for verify_conditional_action_string AND verify_list_item_wrappers. A raw grep -c verify_ was deliberately NOT used: the justification comments also match it, making the count a lower bound rather than an equality"
        status: pass
    human_judgment: false
  - id: D6
    description: "The 172/175 raw-literal WFConditionalActionString values are left untouched and unasserted, with the reason recorded in code"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "Raw-literal counts asserted unchanged at 172 / 175 (an accidental sweep would fail the assertion); the guard's docstring carries the paragraph naming Donor 5's silence on the pure-literal case and the device-proven OPEN/CLOSE router evidence"
        status: pass
    human_judgment: false
  - id: D7
    description: "Both forks rebuild clean, byte-idempotently, and pass the Shortcuts Playground validator at the iOS 26 target"
    requirement: "DIST-01"
    verification:
      - kind: integration
        ref: "Both generators exit 0; docs/phase6_self_check.py (double-build byte-idempotency) exits 0; gate A prints 'Validation passed.' exit 0 on both source XMLs. Gate B not run and in no chain"
        status: pass
    human_judgment: false
  - id: D8
    description: "The raise precedes the single SOURCE.write_bytes() -- a failing build cannot ship a lost envelope"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "Full-build revert of token(): python3 tools/build_state_engine.py exited 1 and src/PROSOCHE-Dumb.xml's sha256 was UNCHANGED across the failed build (99388cad... before and after)"
        status: pass
    human_judgment: false
  - id: D9
    description: "The variable-bearing conditionals render and compare correctly on a real iPhone -- the fact gates select the intended Mirror template family"
    requirement: "CIRC-07"
    verification:
      - kind: backstop
        ref: "Device-only (13-RESEARCH.md assumption A1 / Open Question 2). The file-level half IS verified here: all 20 sites match the device-authored Donor 5 key for key, the left operands carry the WFInput attachment envelope verify_conditional_inputs() already asserts, and no site was changed by this plan. Runtime render is owned by Phase 19 device UAT"
        status: deferred
    human_judgment: true

# Metrics
duration: 25 min
completed: 2026-08-17
status: complete
---

# Phase 13 Plan 02: Pinning the Donor-5 conditional envelope Summary

**The ROADMAP's "14 defective conditional sites" is refuted by measurement — there are zero — so this plan swept nothing and instead pinned the device-confirmed `WFTextTokenString` envelope with a positive build-time assertion that passes non-vacuously over 20 sites per fork, carries the refutation in its own docstring, and fires against a synthetic loss of the shape while leaving both emitters byte-identical to the phase-start SHA.**

## Performance

- **Duration:** ~25 min
- **Tasks:** 2
- **Files modified:** 2 (both generators; neither source XML changed)

## Accomplishments

- **Inverted the deliverable from "fix" to "pin", on evidence.** `.planning/debug/Donor 5.shortcut` — decrypted for the first time during this phase's research — shows iOS **itself** authoring the exact construct the ROADMAP suspected of being a defect: a variable in a conditional's TEXT slot as a `WFTextTokenString` (single `U+FFFC` string, `attachmentsByRange` keyed `{0, 1}` holding a **bare** `{Type, VariableName}` dict), alongside a `WFInput` taking the **opposite** `WFTextTokenAttachment` envelope, with no coercion aggrandizement on either side. `token()` at `:145-148` emits a key-for-key identical shape. Sweeping would have replaced a device-confirmed shape with a guess.
- **Re-derived the refutation independently rather than trusting the research document.** Measured directly from the phase-start artifacts before any edit, per fork: **192 (Core) / 195 (Aware)** mode-0 conditionals carry the slot; **20 each** are variable-bearing, split **19 at code 4 and 1 at code 99**; **172 / 175** are raw literals; **0** bare abandoned placeholders; **0** pin offenders. Zero defective sites, not fourteen.
- **Put the refutation in the code, not only in prose.** The guard's docstring now records the donor by path, the shape it exhibits, the measured counts, the superseded "14" claim, and — explicitly — that this assertion **pins a correct shape rather than repairing a broken one**, so if it fires, the change that tripped it is the defect. Planning prose scrolls out of context; a docstring beside the code does not. This is the countermeasure to T-13-08, whose real attack surface is the stale record itself.
- **Proved the pre-existing assertion survived the extension.** A guard extension can silently disarm what it was added beside. Variant (b) of the demonstration mutates a site to the bare `U+FFFC` string and confirms the **original** raise still fires, with a message textually different from the pin's.
- **Demonstrated the ordering mask instead of engineering around it.** Tripping both assertions in one action list yields **only** the first raise's message — and the pin's offender is entirely invisible, with the `(1 total)` being the *legacy* count rather than a combined one. `main()`'s verify chain order and the order of the two raises are both byte-identical to Task 1's committed version.
- **The full-build revert fired the pin itself, not an earlier guard.** The plan anticipated masking by an earlier guard in the chain, since `token()` feeds slots beyond `WFConditionalActionString`, and asked for that to be recorded as a finding. It did not occur: reverting `token()` to the attachment envelope exited **1** naming **20 offenders** — the whole variable-bearing family in the Core fork, independently corroborating Task 1's inventory.
- **Recorded an ABSENT touch point as a decision.** `verify_conditional_action_string` was already imported and already invoked in `build_sentient.py`, armed by Phase 12. This plan therefore adds **no third touch point** — a genuine exception to the two-touch-point rule. Left unstated, that absence would read exactly like the regression Phase 12 actually committed.

## Task Commits

Each task was committed atomically:

1. **Task 1: pin the Donor-5 conditional envelope with a positive build-time assertion** — `9578c17` (feat)
2. **Task 2: prove both raises are sensitive and distinguishable, and record the ordering mask** — `e4abc2c` (test, `--allow-empty`)

## Files Created/Modified

- `tools/build_state_engine.py` — extended `verify_conditional_action_string()`: a `unpinned` offender list beside the existing `offenders`, a dict-only positive check inside the **existing** loop reusing both `continue` guards, a second `raise SystemExit` after the existing one, and a Donor-5 provenance paragraph appended to the docstring.
- `tools/build_sentient.py` — extended the Phase 12 justification bullet that already names this guard, to record what the already-armed call now **also** asserts on the Aware fork, and to state that no new touch point was added and why.
- `src/PROSOCHE-Dumb.xml` — **unchanged**, `99388cad597417685eb8624a0b4b34e18a6bd30805ac38beb2f3188026c3e679`.
- `src/PROSOCHE-Sentient.xml` — **unchanged**, `d01154b3e1b5990e5d3bc6d92e8dd895b92d0448217356772d077022e5215666`.

The two XMLs are listed in the plan's `files_modified` but are correctly **byte-identical** through the whole plan: this change is a pure assertion over an already-emitted artifact and cannot alter what ships, only what the build refuses to ship. `git status --short` showed only the two `.py` files at every commit point.

## Decisions Made

- **Pin, do not fix.** Donor 5 is device-authored and tops this project's evidence hierarchy. Sweeping 20 conforming sites on the strength of a stale ROADMAP figure is exactly the fabrication the project's do-not-fabricate rule forbids.
- **The 172/175 raw literals stay untouched *and* unasserted, said so in the docstring.** Donor 5 covers only the variable-bearing case; whether iOS writes a pure literal as a bare string or an attachment-free `WFTextTokenString` is **UNVERIFIED**. Those literals are device-proven working — the OPEN/CLOSE router compares `Input Key` against raw `"OPEN"`/`"CLOSE"` and `HANDOFF.md:126` records every breadcrumb A–J firing on device. Settling it needs a one-action donor with a literal comparison: a rung-4 request, not a rung-1 inference.
- **The pin asserts only what the donor exhibits.** Serialization type, a `U+FFFC` in the string, a non-empty `attachmentsByRange` — and nothing about `WFCondition`, coercion aggrandizements or literal values. A stricter pin would be a denial-of-service against a legitimate future shape the donor does not speak to (T-13-13).
- **Whole-function AST byte-comparison, never a `def`-line grep.** The must-not-touch proof for `token()`, `if_block()` and `list_items()` extracts each function's full source segment from **both** revisions and compares bytes. A signature-level grep would be blind to a body edit — precisely the failure this plan exists to prevent.
- **The demonstration subject is a pinned absolute SHA (`698ab99`), never a relative ref**, so the emitter comparison cannot drift with however many commits the phase lands.
- **Aware-side re-demonstration deliberately omitted.** Same function object, same already-armed call, already demonstrated in Phase 12. This is the mirror image of 13-01, which correctly *did* re-demonstrate on Aware because its guard was newly armed there and the arming itself was under test.
- **`docs/manifest_check.py` left red.** Unchanged from 13-01: the expected D-04 consequence of the wave-1 rebuild. Editing MANIFEST rows without re-signing, or weakening the checker, is the silencing the plan's prohibitions forbid. Plan 13-04 owns the re-sign.

## Deviations from Plan

None — plan executed exactly as written. No deviation rule was invoked; no auto-fix was required; no fix-attempt limit was approached.

Two observations worth recording precisely rather than smoothing over, because each *looks* like a discrepancy and is not:

- **The full-build revert did not hit an ordering mask, though the plan budgeted for one.** Task 2's action text said an earlier guard in `main()`'s chain might claim the failure first and that this would be "a finding to record, not a problem to solve." The pin was in fact the guard that raised, so no fallback to the direct-call result was needed. The mask that *does* exist is internal to the function — between its own two raises — and was demonstrated separately in variant (c). Both outcomes were pre-specified; recording which one occurred is the point.
- **The plan's `files_modified` lists both source XMLs, and neither changed.** This is correct, not an omission. The plan's own `<action>` step 4 requires that no emission site move, and the acceptance criteria assert the artifact counts are *unchanged*. A diff in either XML would have been a failure of this plan, not evidence of its success.

## Issues Encountered

None. Every build behaved as predicted, both assertions fired only where intended, and the temporary `token()` mutation was restored via `git checkout --` to byte-identical digests. `git status --short` is empty and `git diff --quiet` exits 0 over all four plan files.

## Verification Results

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebbf… HEAD` (D-01 provenance) | exit 0, re-checked before every generator invocation in both tasks |
| Baseline before any edit — 11 × `docs/*.py` | **all PASS** (so any red during execution is caused by this plan) |
| Baseline before any edit — `docs/manifest_check.py` | already red for the D-04 reason inherited from 13-01 |
| Baseline before any edit — measured inventory | 192/195 slots, 20/20 variable-bearing, 172/175 literals, 0 bare, 0 pin offenders — matching 13-RESEARCH.md exactly, re-derived independently |
| `python3 tools/build_state_engine.py` | exit 0 |
| `python3 tools/build_sentient.py` | exit 0, digest `d01154b3e1b5990e5d3bc6d92e8dd895b92d0448217356772d077022e5215666` — unchanged |
| Mode-0 conditionals carrying `WFConditionalActionString`, per fork | **192 Core / 195 Aware** |
| …variable-bearing, per fork | **20 / 20**, codes `[4]*19 + [99]` in both |
| …raw literal strings, per fork | **172 / 175** — unchanged, no sweep happened |
| Bare abandoned `"￼"` placeholders, per fork | **0 / 0** |
| **Pin offenders, per fork** | **0 / 0** — every one of the 20 carries `WFTextTokenString`, a `U+FFFC` in `Value.string`, and a non-empty `Value.attachmentsByRange` |
| AST: `ast.Raise` nodes inside the guard | **exactly 2** |
| AST: `ast.Assert` nodes inside the guard | **0** — SystemExit convention held |
| AST: docstring contains `Donor 5` and `WFTextTokenString` | both FOUND |
| AST: `token()` vs `698ab99` (whole-function `get_source_segment` byte compare) | **byte-identical** |
| AST: `if_block()` vs `698ab99` | **byte-identical** |
| AST: `list_items()` vs `698ab99` | **byte-identical** |
| AST: Aware touch point A (`ImportFrom` names for `build_state_engine`) | `verify_conditional_action_string` **and** `verify_list_item_wrappers` both present |
| AST: Aware touch point B (bare `Expr(Call(Name(...)))`) | both present — neither guard lost a touch point |
| New Aware touch points added by this plan | **zero, deliberately** — the guard was already armed by Phase 12; recorded in code and in the commit body |
| `python3 docs/phase6_self_check.py` (double-build byte-idempotency) | exit 0 |
| Eleven `docs/*.py` checkers after the change | **all PASS** (`state_engine_self_check`, `phase5`, `phase6`, `phase7`, `phase9`, `sentient_audit`, `sentient_core`, `environmental_restore`, `router_ui_census`, `sequence_dispatch`, `note_identity`) |
| `python3 docs/manifest_check.py` | **EXPECTED RED (D-04)** — `AssertionError: row 'Core source': MANIFEST declares 2831992 bytes, src/PROSOCHE-Dumb.xml is 2916560 bytes`. Owned by plan 13-04. Not silenced, not "fixed" by editing rows without re-signing |
| Gate A, Core fork (`--target-macos 26 --target-platform all`) | `Validation passed.`, exit 0 |
| Gate A, Aware fork (`--target-macos 26 --target-platform all`) | `Validation passed.`, exit 0 |
| Gate B | **not run, not chained** — advisory only, permanent waiver, structurally incapable of exiting 0 |
| Guard sensitivity (direct call — **pin isolated**) | one variable-bearing target replaced with the opposite `WFTextTokenAttachment` envelope → `SystemExit`: `variable-bearing conditional comparison targets have LOST the device-confirmed Donor 5 WFTextTokenString envelope (a single ￼ string plus a non-empty attachmentsByRange); this assertion PINS a shape iOS itself authors, so the change that tripped it is the defect, not the shape: actions 158 (1 total)` |
| Guard sensitivity (direct call — **legacy assertion still has teeth**) | one target replaced with the bare `U+FFFC` string → `SystemExit`: `conditional comparison targets hold the abandoned bare placeholder character instead of a wired token() reference: actions 158 (1 total)` — **textually different** from the pin's |
| **Ordering mask** (direct call — both tripped in one action list) | action 158 → bare placeholder, action 159 → lost envelope; **only the FIRST raise's message appears**, byte-identical to the legacy one above. The pin's offender is entirely invisible and the `(1 total)` is the *legacy* count. **Recorded, not worked around** — neither `main()`'s chain nor the two raises were reordered |
| Guard sensitivity (non-vacuity) | in the **same process** that captured all three failures, the guard returned **without raising** on both shipped forks |
| Guard sensitivity (full build, Core) | `token()` temporarily returned the `WFTextTokenAttachment` envelope → `python3 tools/build_state_engine.py` exited **1**: `…actions 158, 546, 635, 660, 691 (20 total)` — the whole variable-bearing family |
| Which guard fired in the full build | **the pin itself** — no earlier guard in `main()`'s chain claimed the failure, so no fallback to the direct-call result was needed and the chain order was never touched |
| Write-ordering proof | `src/PROSOCHE-Dumb.xml` sha256 **unchanged** across the failed build (`99388cad…` before and after) — the raise preceded `SOURCE.write_bytes()` |
| Restoration | `git checkout -- tools/build_state_engine.py`; provenance re-checked exit 0; both forks rebuilt; **both digests byte-identical** to the pre-demonstration values |
| `main()` verify chain order vs Task 1's commit | **byte-identical** (`git diff --quiet` exits 0 over the whole generator) |
| Working tree after both task commits | `git status --short` empty; `git diff --quiet` exits 0 over all four plan files |
| Scratch artifacts committed | **none** — all scratch scripts live in the session scratchpad, outside the repository |
| File deletions in either commit | `git diff --diff-filter=D --name-only HEAD~1 HEAD` empty for `9578c17`; `e4abc2c` is an empty commit |

## Known Stubs

None. No hardcoded empty value, placeholder string, TODO, FIXME or unwired component was introduced. The one knowingly-deferred item (D9, device render of the variable-bearing conditionals) is a **plan-declared `backstop`**, not a stub: the file-level half is fully verified here — all 20 sites match Donor 5 key for key and none was changed — and only the device-observable half is deferred to Phase 19 UAT, which `13-RESEARCH.md` assumption A1 and Open Question 2 already own.

## Threat Flags

None. No new network endpoint, auth path, file-access pattern or trust-boundary schema change was introduced. The register's `mitigate` dispositions are discharged as planned:

- **T-13-08 (Tampering, the 20 variable-bearing sites)** — pinned by a positive build-time assertion, proven to fire; and this plan itself provably swept nothing, by whole-function AST byte-comparison of `token()`, `if_block()` and `list_items()` against the pinned absolute SHA `698ab99`.
- **T-13-09 (Repudiation, the pin assertion)** — fires against a synthetic loss of the envelope in two independent ways (direct call and full build) and passes non-vacuously on both shipped forks in the same process.
- **T-13-10 (Repudiation, the ordering mask)** — demonstrated by tripping both assertions in one action list and recorded verbatim; neither the chain nor the raises were reordered.
- **T-13-11 (Tampering, the 172/175 raw literals)** — left untouched and unasserted by explicit decision, with the reason in the guard's docstring; their counts are asserted unchanged, so an accidental sweep fails the build's verification.
- **T-13-12 (Tampering, rebuild provenance)** — `git merge-base --is-ancestor 7ca8ebbf… HEAD` exited 0 before every generator invocation in both tasks.
- **T-13-13 (DoS, an over-strict pin)** — the pin asserts only the three properties Donor 5 exhibits, and nothing about `WFCondition`, coercion or literal values.
- **T-13-14 / T-13-SC (accept)** — unchanged: comparison targets carry generator-authored variable names and fixed literals only, and this plan ran no package-manager install.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

**Ready.** The remaining plans start from the baseline they were written against:

- **13-03** (docs) — this plan's durable evidence is in the `e4abc2c` commit body: four verbatim direct-call `SystemExit` transcripts, the full-build revert transcript naming 20 offenders, the pre/post digests, and the mask observation. Three specific things the doc pass must carry, because they are corrections to the project record rather than additions to it: (1) the ROADMAP's "14 defective conditional sites" is **zero** — the measured figures are 192/195 slots, 20/20 variable-bearing, 172/175 literals; (2) `if_block("Previous Respected", 4, …)` is **not a member of the family** — it passes a raw literal and never a `token()`, so the ROADMAP's "concrete starting site" was a false lead; and (3) the raw-literal comparison-target question is **unsettled by decision**, needing a rung-4 one-action donor, and must never be written up as resolved.
- **13-04** (re-sign, MANIFEST, UAT) — unaffected by this plan. Both source XMLs are byte-identical to what 13-01 produced (`99388cad…` Core, `d01154b3…` Aware) and remain gate-A clean, so the re-archive/re-sign proceeds from the same digests 13-01 handed over. `docs/manifest_check.py` is red for exactly the one known reason.
- **Phase 19 device UAT** — inherits one additional assertion beyond 13-01's "Mirror renders non-empty text": that the variable-bearing conditional operands render as **valid (non-red) chips** on device. `13-RESEARCH.md` assumption **A1** stands unresolved and unresolvable — the 2026-08-14 build is not retained and the cited screenshot does not exist in the worktree, the main checkout, or git history. No task depended on it. A red chip at Phase 19 is therefore a **new finding with a live artifact to inspect**, which is precisely the outcome this phase's goal asks for.

## Self-Check: PASSED

- `tools/build_state_engine.py` — FOUND
- `tools/build_sentient.py` — FOUND
- `src/PROSOCHE-Dumb.xml` — FOUND (unchanged, `99388cad…`)
- `src/PROSOCHE-Sentient.xml` — FOUND (unchanged, `d01154b3…`)
- `.planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-02-SUMMARY.md` — FOUND
- Commit `9578c17` — FOUND in `git log`
- Commit `e4abc2c` — FOUND in `git log`
- Working tree clean after both task commits (`git status --short` empty)
- No file deletions in either commit (`git diff --diff-filter=D` empty)

---
*Phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper*
*Completed: 2026-08-17*
