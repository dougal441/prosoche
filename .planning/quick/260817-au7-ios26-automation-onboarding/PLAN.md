---
task: 260817-au7
slug: ios26-automation-onboarding
type: quick
todo: .planning/todos/pending/2026-08-14-repair-ios-26-automation-onboarding.md
autonomous: true
---

# Quick Task 260817-au7 — Repair the iOS 26 Personal Automation onboarding

## Objective

The Control Room Note's Automation A and Automation B build steps cannot produce the
required OPEN and CLOSE automations as written. Replace them with the device-proven
`Create New Shortcut` wrapper flow, propagate to both forks and to the strategy document,
and rebuild/validate/sign/verify.

## What is actually wrong

1. **Step 10 is impossible.** "Set the Run Shortcut action's input to the text OPEN" —
   Run Shortcut's Input parameter accepts a variable, not typed literal text.
2. **The app-trigger screen is a shortcut picker.** Selecting PROSOCHĒ there yields a
   **no-input** automation, so the router falls to MANUAL on every trigger.
3. **Step 7 uses the stale `Ask Before Running` label.** iOS 26 presents
   `Run After Confirmation` / `Run Immediately`.

## Where the text lives (established by inspection, not assumption)

- The Note body is **authored in the XML**, not generated. `tools/build_state_engine.py`
  reads `src/PROSOCHE-Dumb.xml`, patches by comment-marker anchors, and writes it back;
  it contains no copy of this prose (`grep 'READ THIS FIRST' tools/*.py` → no match).
- The body is action index **3616** in Dumb / **3684** in Sentient, a
  `is.workflow.actions.gettext` whose `WFTextActionText` is a **`WFTextTokenString`**
  carrying two attachments at `{4389, 1}` (`Import Descent`) and `{4420, 1}`
  (`Import Voice`) — **both downstream of the edit region**, so
  `attachmentsByRange` MUST be recomputed or the plist ships out-of-bounds ranges.
- `tools/build_sentient.py` forks the **built** Dumb source, so Sentient inherits the
  corrected body automatically; it is not edited by hand.
- `PROSOCHE_Nine_Circles_Canonical_Strategy.md` §"Automation A/B" also prints the old
  shape and can recreate it.

## Tasks

1. **Rewrite the Note body's automation sections** in `src/PROSOCHE-Dumb.xml` via a
   plistlib round-trip that recomputes `attachmentsByRange` from the `￼` offsets.
   Content: the five-step Create New Shortcut wrapper for both A and B, `Run Immediately`
   in place of `Ask Before Running`, the exact-literal typo warning at the point the
   literal is entered, and the "one automation covers all target apps" statement.
2. **Correct `PROSOCHE_Nine_Circles_Canonical_Strategy.md`** minimally, and record the
   change in `docs/BUILD-NOTES.md`.
3. **Rebuild, check, validate, sign, decrypt-verify, refresh MANIFEST** — the 10-04 loop.
4. **Close the todo** into `.planning/todos/completed/` with a dated honest note, and
   update `STATE.md`'s Quick Tasks table.

## Hard constraints

- Provenance guard `git merge-base --is-ancestor 7ca8ebb… HEAD` before either builder.
- `--target-platform all`, never `ios` (DEV-01). No `timeout`. No renames.
- Signed filenames exactly equal the display names, no suffix.
- No Phase 10 guard weakened; all eleven `docs/*.py` checks exit 0 at the end.

## Verification

- Old strings absent from both forks: `Ask Before Running`, `Set the Run Shortcut
  action's input to the text`.
- New strings present in both forks: `Create New Shortcut`, `Run Immediately`,
  `Choose Variable`, the typo warning, the one-automation statement.
- `attachmentsByRange` keys equal the recomputed `￼` offsets in both forks.
- Eleven checks exit 0; both validators pass; both signed files decrypt and carry the
  corrected body.
