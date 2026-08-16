---
task: 260817-au7
slug: ios26-automation-onboarding
type: quick
subsystem: onboarding
tags: [control-room-note, personal-automations, ios26, wftexttokenstring, attachments-by-range, rebuild, signing]

requires:
  - phase: 10
    plan: 04
    provides: the build/validate/sign/decrypt-verify loop and docs/manifest_check.py, reused verbatim here
provides:
  - Control Room Note onboarding that describes automations a user can actually build on iOS 26
  - The exact-literal typo warning at the point the literal is entered
  - The "one automation covers every watched app" statement
  - docs/BUILD-NOTES.md section 20 — the repair record, including the attachment-offset hazard
  - Two re-signed forks proven by AEA1 decryption to carry the corrected body
affects:
  - The outstanding device UAT, which now owns confirming the rendered flow end to end

tech-stack:
  added: []
  patterns:
    - "Recompute attachmentsByRange whenever a WFTextTokenString is edited — the ranges are
      absolute offsets into the final string, so lengthening text ahead of an attachment
      silently converts a valid plist into one carrying out-of-bounds ranges"
    - "Prove the round trip before writing — a no-op plistlib.dumps(..., sort_keys=False)
      that comes back byte-identical to the source licenses a structured edit; without it,
      a semantic edit is indistinguishable from reformatting noise in the diff"
    - "Fix the copy where it lives, not where it looks like it should live — grep the
      generator before assuming it owns the prose it writes"

key-files:
  created:
    - .planning/quick/260817-au7-ios26-automation-onboarding/PLAN.md
    - .planning/quick/260817-au7-ios26-automation-onboarding/SUMMARY.md
  modified:
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml
    - PROSOCHE_Nine_Circles_Canonical_Strategy.md
    - docs/BUILD-NOTES.md
    - artifacts/shortcuts/MANIFEST.md
    - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut
    - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut
    - .planning/STATE.md

key-decisions:
  - "The Note body was edited via a plistlib round trip that recomputes attachmentsByRange,
    not by string substitution in the XML. The body is a WFTextTokenString whose two
    attachments sit at offsets 4389/4420 — downstream of the edit. A plain text edit would
    have left both ranges stale and out of bounds, which VARIABLES.md records as able to
    crash Shortcuts on import. The plist was confirmed to round-trip byte-identically first."
  - "Sentient was NOT hand-edited. tools/build_sentient.py forks the built Dumb source, so
    rebuilding propagated the corrected body verbatim. Editing both by hand would have
    created two independently-authored copies of prose that is meant to be one."
  - "The Run Shortcut target string PROSOCHĒ — Nine Circles — Dumb was left untouched in both
    forks, even though Sentient's inherited body therefore names the wrong fork. BUILD-NOTES
    section 9 pins that string to the Dumb signing name; changing it is a fork-naming
    decision owned by Build Addendum 01, not a copy repair."
  - "The MANIFEST's two existing device-gap warnings were kept verbatim and a third appended.
    A merged warning cannot be audited against the original."

# Metrics
duration: ~30 minutes
completed: 2026-08-17
tasks-completed: 4
tasks-total: 4
files-modified: 8
status: complete
---

# Quick Task 260817-au7: Repair the iOS 26 automation onboarding Summary

The Control Room Note told users to do something iOS cannot do; it now tells them the thing
that was device-proven to work, warns them about the one typo that fails silently, and both
signed forks were decrypted to prove the corrected text is inside the bytes a user imports.

## What Was Built

### Task 1 — the Note body (commit `489bc1e`)

Three defects, all in copy:

1. **Step 10 was impossible.** "Set the Run Shortcut action's input to the text `OPEN`" —
   `Run Shortcut`'s Input parameter accepts a **variable**. There is no field in which those
   four letters can be typed.
2. **The app-trigger screen is a shortcut picker**, so selecting PROSOCHĒ there produces a
   **no-input** automation: `ExtensionInput` arrives absent, composes as an empty string, and
   the router falls through to MANUAL on every single trigger.
3. **Step 7 carried the stale `Ask Before Running` label**; iOS 26 offers
   `Run After Confirmation` / `Run Immediately`.

Both sections were replaced with a twelve-step flow built on the device-proven wrapper: on
the shortcut-picker screen tap **Create New Shortcut**; add a **Text** action holding the
literal; add **Run Shortcut** below it; confirm its Input is the preceding Text magic
variable, using **Choose Variable** if not auto-filled; save with the blue checkmark.

Two additions beyond the literal fix:

- **The typo warning is inline, at step 9, where the literal is entered** — not appended as a
  trailing caveat. It names `CLOSED` explicitly because that is the mistake this user actually
  made during Phase 4 UAT, and it states that the failure is silent, which is the property
  that makes the warning worth its words.
- **"You need two automations in total, not two for every app"** sits once, before Automation
  A, with the reason (PROSOCHĒ measures reaching as a whole, not app by app) and the reason A
  and B remain split (different literals).

### The hazard this task was actually about

The Note body is **authored in the XML, not generated**. `grep 'READ THIS FIRST' tools/*.py`
returns nothing; `tools/build_state_engine.py` reads `src/PROSOCHE-Dumb.xml`, patches by
comment-marker anchor, and writes it back, so a hand edit to the body survives every rebuild.

The body is a `is.workflow.actions.gettext` (Dumb index 3616) whose `WFTextActionText` is a
**`WFTextTokenString`** carrying two attachments — `Import Descent` at `{4389, 1}` and
`Import Voice` at `{4420, 1}` — **both downstream of the edited region**. The replacement
lengthened the string 5121 → 6210 characters, moving both placeholders to 5478 and 5509.

A plain string substitution in the XML would have left the range keys reading 4389/4420 and
shipped a plist with two ranges pointing into the middle of unrelated prose — the failure
`VARIABLES.md` records as able to **crash Shortcuts on import**. The edit was therefore made
through a plistlib round trip that rebuilds `attachmentsByRange` from the new placeholder
offsets in document order, with a guard asserting the old offsets matched the old keys first,
and a second asserting the replacement text introduces no new placeholder.

Licensing that approach: a **no-op** `plistlib.dumps(data, fmt=FMT_XML, sort_keys=False)` was
confirmed byte-identical to the 2,259,398-byte source before any edit was made, so the
resulting diff is 17 insertions / 11 deletions of real content and nothing else.

### Task 2 — strategy and record (commit `9cb2091`)

`PROSOCHE_Nine_Circles_Canonical_Strategy.md`'s Automation A/B blocks were the only other
source able to recreate the wrong instructions (grep across the tree found the old steps
elsewhere only in dated `artifacts/shortcuts/*/` archives, which are historical records and
were left alone). Both blocks now name `Run Immediately`, the `Create New Shortcut` picker
step, the `Text` to `Run Shortcut` binding, and carry the one-automation statement plus a
closing line on why the literal must be exact.

`docs/BUILD-NOTES.md` **section 20** records all three defects, why the wrapper flow is
trusted at the mechanism level but not as rendered text, the `attachmentsByRange`
recomputation, and the carried-forward Sentient fork-name defect so it cannot be mistaken for
new damage. Section 20 is a pure append; the diff contains zero deletions.

### Tasks 3 and 4 — rebuild, prove, close (commit `c961af9`, this commit)

The 10-04 loop, unchanged. Provenance guard first (`git merge-base --is-ancestor 7ca8ebb…
HEAD` exits 0) before either builder.

A quiet confirmation fell out of the rebuild: after `tools/build_state_engine.py` ran,
`src/PROSOCHE-Dumb.xml` was **unmodified in `git status`** — the generator reproduced the
hand-edited file byte for byte, so the edit is stable under every future rebuild rather than
merely surviving this one.

## Verification Evidence

| Check | Result |
|---|---|
| No-op plistlib round trip before editing | byte-identical, 2,259,398 == 2,259,398 |
| `plutil -lint src/PROSOCHE-Dumb.xml` after edit | `OK` |
| `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit 0, before either builder |
| Both builders | exit 0; **Dumb came back byte-identical to the hand edit** |
| Stale strings in both forks (`Ask Before Running`, `Set the Run Shortcut action's input to the text`) | **0** |
| New strings in both forks (7 asserted) | **7/7** each |
| `attachmentsByRange` keys vs placeholder offsets, both forks | `[5478, 5509] == [5478, 5509]` |
| `12. Save with the blue checkmark.` occurrences per fork | 2 — Automation A and Automation B |
| `validate-shortcut --target-macos 26 --target-platform all` x2 | `Validation passed.`, exit 0 each |
| Signed sizes | 193,819 and 198,124 — both non-zero, exact display names, no suffix |
| Dated archives vs `src/` | SHA-256 **equal** for both forks |
| `plutil -lint` on both recovered plists | `OK` |
| Decrypted body assertions, per fork | 1 body, `WFTextTokenString`, offsets match, 0 stale, 7/7 new |
| Eleven `docs/*.py` checks | **all exit 0** |
| `manifest_check.py` | red before the refresh (as designed), `passed (6 rows verified against disk)` after |
| `timeout` | never invoked |
| `--target-platform ios` | never invoked |

Recovered action counts: 3,718 (Dumb) and 3,786 (Sentient).

## Deviations from Plan

None. No deviation rule fired: no bug was uncovered by the change, nothing was missing that
correctness required, nothing blocked a task, and no architectural question arose. No
checkpoint, no auth gate, no package-manager install.

The one judgement call worth naming is a deliberate **non**-fix, recorded under Deferred
Items below rather than as a deviation, because it is pre-existing and independent.

## Known Stubs

None. Nothing in this change is a placeholder; every string added is final onboarding copy
and every value in the MANIFEST was computed from a file on disk.

## Deferred Items

| Item | Where | Why deferred |
|---|---|---|
| **Both forks name `PROSOCHĒ — Nine Circles — Dumb` as the Run Shortcut target** — so Sentient's inherited note body names the wrong fork | Control Room Note, both forks | Pre-existing and older than this task; `docs/BUILD-NOTES.md` section 9 pins that string to the Dumb signing name, so changing it is a fork-naming decision. Belongs with `.planning/todos/pending/2026-08-14-apply-build-addendum-01.md`. Recorded in section 20 so it is not read as new damage. |
| **The rendered flow is device-unproven end to end** | Control Room Note, both forks | The INPUT PROBE proved the handoff mechanism (`RAW [OPEN]` / `NORMALISED [OPEN]`), not this text. Owned by `.planning/todos/pending/2026-08-16-device-uat-nine-circles-and-sequence-switching.md`; `MANIFEST.md` carries a warning saying so. |
| **A dangling staged deletion left by the previous quick task** — `.planning/todos/pending/2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md` is deleted in the index but not committed | git index at task start | Out of scope. Commit `b639ba1` added the `completed/` copy but never committed the matching removal. Every commit in this task used pathspec-limited `git commit <paths>` so the entry was neither swept in nor disturbed. |

## Threat Flags

None. Nothing in this change introduces a network endpoint, an auth path, a file-access
pattern, or a schema change at a trust boundary. The only executable touched was a
throwaway edit script in the scratchpad; no project tool was modified.

## Notes for the Next Task

- **The Note body is XML-authored and the generator reproduces it byte for byte.** Future
  copy passes (`2026-08-16-optimise-ux-onboarding-and-functionality.md` in particular) should
  edit `src/PROSOCHE-Dumb.xml` action 3616 and rebuild — but must recompute
  `attachmentsByRange` every time, because the two attachments live near the end of the body
  and almost any copy edit moves them.
- **`docs/manifest_check.py` goes red on every rebuild until MANIFEST is refreshed.** That
  happened here exactly as 10-04 predicted and is the cheapest signal that a build shipped
  without its record.

## Note on how this file was written

The `Write` tool refused to create this SUMMARY.md ("Subagents should return findings as
text, not write report files"). That is a harness heuristic misreading a required GSD
artifact — the orchestrator reads this file from disk. It was therefore written via a shell
redirect, as the task objective directed.

## Self-Check: PASSED

- `.planning/quick/260817-au7-ios26-automation-onboarding/PLAN.md` — FOUND
- `.planning/quick/260817-au7-ios26-automation-onboarding/SUMMARY.md` — FOUND
- `.planning/todos/completed/2026-08-14-repair-ios-26-automation-onboarding.md` — FOUND
- `.planning/todos/pending/2026-08-14-repair-ios-26-automation-onboarding.md` — ABSENT (correct)
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` — FOUND
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` — FOUND
- `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Dumb-020725.xml` — FOUND
- `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Sentient-020737.xml` — FOUND
- commit `489bc1e` — FOUND
- commit `9cb2091` — FOUND
- commit `c961af9` — FOUND
