---
created: 2026-08-17T13:25:00.000Z
title: Manual run on a clean install summons the iOS Note chooser — cycle-16 filter fix shipped but does not hold
area: general
severity: major
files:
  - tools/build_state_engine.py:2073
  - tools/build_state_engine.py:4144
  - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut
---

## Problem

**Device-observed, 2026-08-17, iPhone Mirroring, Core build `b07497ba…` (SHA-256 matched to
`13-UAT.md`'s header before the run).**

On a **clean install** — iCloud `Shortcuts/` folder empty, no `state.json`, and **no Apple Note
titled `PROSOCHĒ`** — running the shortcut manually and choosing **`Status`** presents the
**system "Note" chooser listing every note in the user's Notes library**.

Two things make this more than a restatement of the known cycle-16 symptom:

1. **It fires on the `Status` path.** `tools/build_state_engine.py:2073` states plainly:
   `# appendnote -- Status never writes to the Note.` Whatever is dereferencing the Note on this
   path is not supposed to be on this path.
2. **The cycle-16 fix shipped and is present in the running artifact.** The signed container was
   decrypted (`aea decrypt` → `aa extract`) and the single `is.workflow.actions.filter.notes`
   at action index **4175** carries all three of `fix_notes_filter_limit()`'s fields:
   `AppIntentDescriptor` (`NoteEntity` / `com.apple.mobilenotes`),
   `WFContentItemLimitEnabled = True`, `WFContentItemLimitNumber = 1.0`.
   So this is **a fix that does not hold at runtime, not a missing fix** — which is why it
   presents as a regression of something already closed.

### User-data risk — why this is not merely cosmetic

The chooser is live and destructive if answered wrongly. Selecting any note binds it as the
Control Room Note, and the four `appendnote` sites then **append PROSOCHĒ's settings/state block
into that note**. On a clean install the correct target does not exist yet, so *every* option
in the chooser is a personal note. The UAT run deliberately declined to select one.

### Ranked hypothesis — NOT yet localised

All four `appendnote` sites and the one `shownote` bind their note reference to the **variable
`Control Room Note`**, measured in the decrypted artifact:

| action index | identifier | note reference |
|---:|---|---|
| 4230 | `is.workflow.actions.appendnote` | `entity` → Variable `Control Room Note` |
| 4303 | `is.workflow.actions.appendnote` | `entity` → Variable `Control Room Note` |
| 4325 | `is.workflow.actions.appendnote` | `entity` → Variable `Control Room Note` |
| 4335 | `is.workflow.actions.appendnote` | `entity` → Variable `Control Room Note` |
| 4340 | `is.workflow.actions.shownote`   | `WFInput` → Variable `Control Room Note` |

With no `PROSOCHĒ` note present, `filter.notes` returns **zero rows**, the
`Get Item From List → First Item` consumer yields **empty**, and `Control Room Note` is empty.
An **empty entity reference is the classic trigger for iOS's entity chooser** — iOS asks the user
to supply the entity the action could not resolve. That is consistent with the limit fix being
irrelevant here: bounding a search to one result does nothing when the search matches nothing.

This is a hypothesis with file-level support, **not a localisation**. It is not yet known which
of the five sites raises the prompt, and the create-note branch
(`com.apple.mobilenotes.SharingExtension`, action 4192, `name = 'PROSOCHĒ'`) exists but its
ordering/gating relative to the dereference has not been traced.

### Confirmed precondition (user, 2026-08-17)

The `PROSOCHĒ` note is created only when the user chooses **`Open Control Room`**. So on a clean
install every other menu item runs against a Note that does not exist yet.

## Solution

TBD — needs a breadcrumb run to localise before any fix is written. Candidate directions, in the
order the evidence supports:

1. **Localise first.** Flag-gated breadcrumbs at each of the five sites, one device run, to
   identify which action raises the chooser. Do not fix site-by-site — `.claude/CLAUDE.md`
   ("Fix whole classes, never site-by-site") applies; every defect found in this project so far
   was systematic.
2. **Guarantee the Note exists before anything dereferences it.** The container/leaf refinement
   of axis 7 is the closest existing precedent: seed the Note as a bootstrap invariant rather
   than creating it lazily on one menu branch.
3. **Gate every Note consumer** on a non-empty `Control Room Note`, the same way
   `gate_control_room_shownote()` already gates the `shownote`. Note that gating on a dotted
   existence test is unimplementable per axis 7 — gate on a string is-not-empty test.

## Impact on outstanding UAT

Predicts the same failure, for the same reason, in:

- `07-UAT.md` Test 2 — "Open Control Room — no stray note picker" (the outstanding Finding-2
  check). **Observed failing on the `Status` path, which is stricter than the test as written.**
- `07-UAT.md` Test 12 — "Recovery — deleted Control Room Note". Deleting the note reproduces
  exactly the clean-install precondition.
- `07-UAT.md` Test 16 — recovery cases across manual / OPEN / CLOSE invocation modes.

## Evidence

- Device: iPhone Mirroring session, 2026-08-17 11:15–11:22, screenshots captured in-session.
- Artifact: `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut`,
  SHA-256 `b07497ba1a66506aaaa9c48134f463ceefeac7f4a656e86dad48b0a76414ac5b`, decrypted and
  parameter-dumped.
- Precondition: iCloud Drive → Shortcuts folder observed **empty** immediately before the run.
