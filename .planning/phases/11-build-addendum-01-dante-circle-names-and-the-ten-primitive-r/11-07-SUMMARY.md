---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
plan: 07
subsystem: generator / distribution
tags: [output-names, text-match, panic-escape, recurrence-guard, gap-closure, tracer]
requires:
  - "11-06 (Core/Aware rename; both forks and MANIFEST at their post-Phase-16 state)"
provides:
  - "ACTION_OUTPUT_NAMES coverage for is.workflow.actions.text.match, arming verify_output_names() at every present and future site for that identifier"
  - "A resolving Panic Escape section read, so the removal branch's contains test can be true"
  - "A real extracted proforma at the Sync My Profile site rather than a stringified list"
  - "A retained, validated, signed rung-2 probe under .planning/debug/probes/ that can be re-run once an install channel exists"
affects:
  - "tools/build_state_engine.py"
  - "both shipped forks and both signed containers"
  - "artifacts/shortcuts/MANIFEST.md"
tech-stack:
  added: []
  patterns:
    - "One ACTION_OUTPUT_NAMES entry arms normalise -> verify for an identifier globally; the corrected call sites are its consequence, not the fix"
    - "First-item-then-consume for a list-valued text.match output, mirroring build_sentient.py audit_block()"
key-files:
  created:
    - ".planning/debug/probes/text_match_consumption_probe.py"
    - ".planning/debug/probes/text-match-consumption-probe.xml"
    - ".planning/debug/probes/Text Match Consumption Probe.shortcut"
  modified:
    - "tools/build_state_engine.py"
    - "src/PROSOCHE-Dumb.xml"
    - "src/PROSOCHE-Sentient.xml"
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut"
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut"
    - "artifacts/shortcuts/MANIFEST.md"
    - "docs/BUILD-NOTES.md"
decisions:
  - "text.match publishes 'Matches' — corpus-attested 15/0, re-taken this session, not transcribed"
  - "The list-consumption shape is recorded OPEN, not settled; Shape B adopted as the bounded fallback and recorded as a deviation"
  - "The retired guessed label is deliberately absent from the whole generator, including comments — a comment naming a wrong output name is the seed of the next recurrence"
metrics:
  duration: "~35 min"
  completed: "2026-08-18"
  tasks: 3
  commits: 3
  action-delta: "+2 per fork (4302 -> 4304 Core, 4370 -> 4372 Aware)"
status: complete
---

# Phase 11 Plan 07: The text.match Output-Name Class Fix Summary

Closed the silent wrong-name defect that killed the removal half of Phase 11's headline
deliverable — as a class, via one `ACTION_OUTPUT_NAMES` entry that arms the existing
recurrence guard for every present and future site, not as two hand-patched call sites.

## What was wrong

`is.workflow.actions.text.match` publishes its output as **`Matches`**. The engine guessed a
different label at two sites. The guess produces **no error at all**: the reference simply does
not resolve, the Panic Escape section reads empty, the condition-99 contains test over it is
always false, control reaches the otherwise arm, and a user who asked to remove their bypass is
shown a confident *"Nothing was changed."* The Note append that would have recorded the change
never runs, so there is no audit trail either — the plan's T-11-36 (spoofing) and T-11-37
(repudiation) threats, both from one missing string.

`ACTION_OUTPUT_NAMES` — the table that exists to make exactly this a build error — did not list
the identifier, so `verify_output_names()` was **blind to both sites**. That is why a Phase 11
review finding (CR-02) was still live at HEAD after Phases 12, 13 and 16 had each landed.

## Evidence

The corpus tally was **re-taken this session**, not transcribed: all 19 shipped golden XMLs,
every `ActionOutput` token resolved back to its producing identifier.

| measure | result |
|---|---|
| output name `Matches` | **15**, across 3 of 19 files |
| the label the engine guessed | **0** |
| consumers | `getgroup` ×7, `conditional` ×5, `setvariable` ×1, `count` ×1, `detect.text` ×1 |
| consumer `gettext` | **0** |
| consumer `getitemfromlist` | **0** |

A second independent source agreed: `tools/build_sentient.py`'s `audit_block()` already read
the same identifier's output by the real name — so one artifact shipped **two contradictory
names for one identifier**.

## Tasks

| # | Task | Commit |
|---|---|---|
| 1 | Output-name class fix, generator constant → decrypt-verified container (tracer) | `ce560c3` |
| 2 | Settle the list-consumption shape at the lowest rung that can settle it | `8cd3287` |
| 3 | Re-sign, decrypt-verify, prepend MANIFEST block, correct stale dispatch count | `b1048a1` |

## The negative control (Task 1)

Run against `verify_output_names()` directly on a mutated deep copy — **not** by editing a call
site and rebuilding, because `normalise_output_names()` runs *before* the verifier in `main()`
and would silently repair the regression first. Verbatim output:

```
=== BEFORE this plan (text.match ABSENT from ACTION_OUTPUT_NAMES) ===
BEFORE: verify_output_names() returned NORMALLY -- guard is SILENT (mutated 'Matches' -> 'Totally Wrong Name', nothing raised)

=== AFTER this plan (text.match PRESENT) ===
AFTER: SystemExit RAISED -> magic-variable references carry a wrong OutputName: action 4225 says 'Totally Wrong Name', real name is 'Matches' (1 total)

RESTORED: verify_output_names() on the unmutated Dumb source passes clean.
```

Both observations recorded side by side, as the plan required: the guard was genuinely silent
before, not merely mutation-proof.

## Task 2 took the FALLBACK path — and was SUPERSEDED the same day

> **CORRECTION, 2026-08-18, post-execution.** Everything below the rule was what this SUMMARY
> originally claimed. **Its central factual claim was false.** The probe installs and runs fine;
> the question it was built to answer is now SETTLED at rung 2 and the fallback is confirmed
> correct. The original text is retained verbatim as the record of what was asserted, followed by
> the retraction and the measured result. See `docs/BUILD-NOTES.md` §31 (rewritten).

### What this SUMMARY originally claimed (retained, superseded)

**Stated explicitly, because the plan requires the SUMMARY to name which path was taken and
forbids satisfying both: this was the fallback path.**

The probe **was** built (23 actions), **validated clean at gate A**, and **signed** to a
23,861-byte container. It could **not be installed**: `xcrun simctl openurl` against a `file://`
URL hung indefinitely and produced no import sheet, across two attempts, from both a
space-bearing and a space-free path. **No alert, no clipboard payload, no readout of any kind
was obtained**, so no runtime claim — device *or* simulator — is available and none is made.

The consumption shape is therefore **recorded OPEN**. Shape B was adopted at both sites as the
bounded fallback: it is the in-repo precedent (`audit_block()`), it is deterministic about which
element is taken, and taking the first item of a one-element list cannot be worse than
stringifying that list. Recorded as a deviation in `docs/BUILD-NOTES.md` §31; `grep -c
'deviation'` rose 24 → 27.

The probe is retained under `.planning/debug/probes/` so it can be **re-run rather than
rebuilt** once an install channel exists.

### The retraction and the measured result

**"Could not be installed" was false.** Re-measured: `xcrun simctl openurl` produced the
Shortcuts import sheet on the **first** attempt from a space-bearing path, and one tap on
**Add Shortcut** completed the import. `.claude/CLAUDE.md` §9's account of that channel is
correct and needed no narrowing — this SUMMARY's contradiction of it was the error.

**The real cause was a defect in the probe.** Its `main()` wrote `build()`'s raw actions
straight to plist, skipping `normalise_string_envelopes()`. `output()` returns a bare
`WFTextTokenAttachment`, and `gettext.WFTextActionText` is a string-typed parameter listed in
`STRING_ENVELOPE_PARAMS` — so **both** consumption sites carried an **axis-2** defect and read
empty regardless of shape. The first run's `[SHAPE_A]<<>>` / `[SHAPE_B]<<>>` were *identically*
blank, which was the tell; the correctly-enveloped report action resolved its chips perfectly.

**The corrected probe (v2) settles the question.** Verbatim payload:

```
PROBE-BEGIN
[SHAPE_A]<<## PANIC ESCAPE
Panic Escape: OFF
Set this line to ON to restore it.
>>
[SHAPE_B]<<## PANIC ESCAPE
Panic Escape: OFF
Set this line to ON to restore it.
>>
[CONTAINS]<<TRUE - Shape A output contains the removed-position line>>
PROBE-END
```

`Matches` resolves at run time; **Shape A and Shape B are equivalent for a single-match list**;
and the condition-99 contains test the removal path depends on reads **TRUE**. The adopted
Shape B is therefore **confirmed**, not merely bounded. Multi-match is untested and is why
first-item is retained. Simulator observation only — DIST-03 is open and nothing here is a
device claim.

## Deviations from Plan

### 1. [Rule 2 — plan/reality conflict] The probe uses a clipboard readout, not three Show Alerts

- **Found during:** Task 2, probe design
- **Issue:** The plan specifies three `Show Alert` readouts. `.claude/CLAUDE.md` §9 records
  (spike 010) that **Show Alert modals accept neither a synthesized tap nor a hardware Return**
  — the run wedges permanently at the first one — and directs that simulator-bound probes carry
  **no blocking UI**. Three alerts would have wedged three times and read out nothing.
- **Fix:** All three results are concatenated into one clipboard payload recoverable with
  `xcrun simctl pbpaste`, which needs no synthesized input. Delimiters (`<<`/`>>`) make an
  empty result distinguishable from a missing one.
- **Note:** Orthogonal to the install failure; it did not cause it.
- **Recorded:** `docs/BUILD-NOTES.md` §31. **Commit:** `8cd3287`

### 2. [Rule 1 — plan arithmetic slip] Task 1's ">= 3 per fork" criterion contradicts its own parenthetical

- **Found during:** Task 1 acceptance checking
- **Issue:** The criterion demands `>= 3` text-match references per fork, but its own
  parenthetical — *"two engine sites plus, **in the Aware fork**, the audit block's own"* —
  predicts exactly **2** for Core. Measured: **Core 2, Aware 5**. The threshold is
  arithmetically impossible for Core.
- **Fix:** Asserted the floor the parenthetical actually describes (the two engine sites,
  present in both forks). The substantive requirements are fully met: **every** text-match
  reference in **both** forks resolves to `Matches`, and **zero** carry the retired guess.
- **Commit:** `ce560c3`

### 3. [Rule 1 — over-broad assertion, self-caught] Scoping the `getitemfromlist` literal check

- **Found during:** Task 2 acceptance checking
- **Issue:** A first pass asserted `WFItemSpecifier == "First Item"` over **every**
  `getitemfromlist` in each fork and failed, sweeping 67 pre-existing sites that legitimately
  use the different enum case `Item At Index`.
- **Fix:** Re-scoped to the actions **introduced by this task**, as the plan's wording
  specifies, by diffing against the committed baseline. Result: total delta and `First Item`
  delta both exactly **+2** per fork, with **no other specifier disturbed**.
- **Commit:** `8cd3287`

### 4. [Rule 2 — anti-recurrence] The retired label appears nowhere in the generator

- **Found during:** Task 1
- **Issue:** The acceptance criterion `grep -c 'Matched Text' tools/build_state_engine.py == 0`
  initially returned **2** — both hits inside the new derivation comment describing the old
  wrong name.
- **Fix:** The comment now refers to it as "the label this engine used to guess" and states why
  it is not spelled out: a comment naming a wrong output name is the seed of the next
  recurrence, and the string is also the negative-control search term. Its wording lives here
  in the SUMMARY instead. Count is now **0**.
- **Commit:** `ce560c3`

## Verification

| check | result |
|---|---|
| Provenance gate `git merge-base --is-ancestor 7ca8ebb… HEAD` | passes, re-checked before every rebuild |
| Builders byte-idempotent across two consecutive runs | yes — identical SHA-256, `git status --short src/` empty |
| Thirteen structural checkers | **all exit 0**, `manifest_check` included |
| Gate A, both forks (`--target-macos 26 --target-platform all`) | `Validation passed.`, exit 0 |
| Gate B | **never invoked** — advisory, permanently waivered, appears nowhere in this plan's commands |
| AEA1 decrypt-verify | both forks: `plutil -lint` OK; recovered `WFWorkflowActions` **== source**, `True` |
| Recovered payload content | `Matches` ×2 (Core) / ×5 (Aware); retired guess ×0 in both |
| `grep -c 'ninety' MANIFEST.md` | **1 → 0** |
| Dispatch count | freshly measured **99** per fork, **equal across both forks**; 9 names × 11 renderings; `sequence_dispatch_check.py` independently reports 99 |
| `getitemfromlist` per fork | 69 → 71 (Core), 70 → 72 (Aware); every new one literal `First Item` |
| Action totals | 4302 → **4304** (Core), 4370 → **4372** (Aware) |

**No redness was inherited on entry** — all thirteen checkers were green at HEAD before this
plan started, unlike the original 2026-08-17 draft which was written against an in-flight Phase
12. `manifest_check` went red after Task 1 exactly as predicted, and its message named a
**size** (`row 'Core source': MANIFEST declares 2854976 bytes, src/PROSOCHE-Dumb.xml is 2854966
bytes`) — never a missing row or a bad basename — then cleared on Task 3's recomputation.

## Known Stubs

None.

## Device verification

**Nothing in this plan is device-verified, and nothing claims to be.** DIST-03 remains open.
The repaired removal path has never run on a phone. What is proven is structural: the corpus
tally, the build guard and its negative control, gate A at the project target, and the AEA1
decrypt of both containers. Whether the removal branch actually reaches its confirmation menu
on device is exactly as unproven as before this plan — and the consumption shape underneath it
is recorded **OPEN**, not settled.

## Self-Check: PASSED

- `tools/build_state_engine.py` — FOUND (modified)
- `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` — FOUND (rebuilt, idempotent)
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — FOUND, 230355 bytes
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — FOUND, 234885 bytes
- `artifacts/shortcuts/MANIFEST.md` — FOUND (6 rows recomputed, new block prepended, count corrected)
- `docs/BUILD-NOTES.md` — FOUND (§31, §32 appended)
- `.planning/debug/probes/text_match_consumption_probe.py` — FOUND, 8452 bytes
- Commit `ce560c3` — FOUND
- Commit `8cd3287` — FOUND
- Commit `b1048a1` — FOUND
