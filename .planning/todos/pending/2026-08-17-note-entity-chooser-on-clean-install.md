---
created: 2026-08-17T13:25:00.000Z
title: Manual state-changing runs leave Control Room Note unresolved — iOS raises entity+text AppIntent prompts
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

## SEVERITY UPGRADED TO BLOCKER — second observation, same run

Continuing the same clean-install session, **`Open Control Room` was chosen**. Three facts,
all device-observed:

1. **It opened the WRONG note.** The Notes app opened the user's own note titled
   `/gsd-phase "Build v2 stakeholder addendum"` — an unrelated personal note. This was the
   **first row** of the chooser seen minutes earlier on the `Status` path.
2. **No Control Room Note was created.** Searching all of Notes for `PROSOCH` returns
   `Notes — None Found` (the single "Top Hit" is that same `/gsd-phase` note, matching on its
   *body* text `@PROSOCHE_Build_Addendum_01.md`, not on its title). So after explicitly choosing
   `Open Control Room` — the one menu item the user confirms is responsible for creating it —
   **no note titled `PROSOCHĒ` exists.**
3. **The predicate itself is well-formed.** Dumped from the decrypted artifact, the
   `WFContentItemFilter` is `Operator: 99` (contains), `Property: Name`,
   `WFActionParameterFilterPrefix: 1` (All), value `WFTextTokenString` `"PROSOCHĒ"` with the
   correct U+0112 `Ē` and an empty `attachmentsByRange`. Nothing about the filter is malformed.

**Why this is a blocker, not a major.** `filter.notes` returns a note that does not match its
own predicate, the found-branch is therefore taken, the create-note branch
(action 4192, `name = 'PROSOCHĒ'`) is **skipped**, and an arbitrary personal note is bound to the
variable `Control Room Note`. The four `appendnote` sites write to exactly that variable — so any
state-changing manual run is positioned to **append PROSOCHĒ's state block into a personal
note**. That is silent user-data corruption, and the user cannot tell it happened.

It also means the entire Control Room surface (§17, §18) does not function on a clean install.

### Revised root-cause candidates, best-supported first

1. **The `AppIntentDescriptor` added by `fix_notes_filter_limit()` re-routes the action through
   the AppIntent `NoteEntity` query, which ignores the legacy `WFContentItemFilter`.**
   `WFContentItemLimitNumber = 1.0` then truncates an unfiltered result set to its first row.
   This predicts precisely what was seen: one note, wrong note, no chooser on that path. It also
   means **cycle 16 traded a visible chooser for a silently wrong answer** — strictly worse,
   and exactly the kind of regression a file-level check cannot see.
2. **Diacritic-insensitive matching.** iOS string comparison is commonly diacritic- and
   case-insensitive, so `contains "PROSOCHĒ"` may match `PROSOCHE`. Does **not** explain this
   observation on its own — the matched note's *title* contains neither spelling; only its body
   does — but it is a real hazard for the `Name` predicate once a `PROSOCHĒ` note does exist,
   and would make the note identity ambiguous against any note mentioning the project.

Distinguishing 1 from 2 is one device run: create a note titled exactly `PROSOCHĒ` by hand, re-run
`Open Control Room`, and see whether it is found. If an unrelated note is still returned,
candidate 1 stands and `docs/note_identity_check.py`'s Operator-99 pin is verifying a predicate
that is not being consulted.

## THE EXPERIMENT WAS RUN — candidate 1 is REFUTED

**Device, same session, 2026-08-17 11:27.** A note titled exactly `PROSOCHĒ` (U+0112 verified by
zoom on the rendered title) was **created by hand** in Notes → iCloud. `Open Control Room` was
then re-run.

**Result: it found and opened the correct `PROSOCHĒ` note.**

So `WFContentItemFilter` **is** consulted, the `Operator 99` / `Property Name` predicate **does**
match correctly, and `fix_notes_filter_limit()` is **not** at fault. Candidate 1 is dead, and
candidate 2 (diacritic-insensitivity) is untested but no longer needed to explain anything.

⚠ **The `PROSOCHĒ` note now on the device is HAND-MADE, not product-created.** Nothing downstream
may treat its existence as evidence that the create path works — it does not. Delete it before
any future clean-install run.

### Corrected root cause — narrower and still a blocker

The defect is confined to the **zero-match / clean-install path**. When no `PROSOCHĒ` note
exists, `filter.notes` correctly matches nothing, and then:

- the **create-note branch does not run** (action 4192,
  `com.apple.mobilenotes.SharingExtension`, `name = 'PROSOCHĒ'` — never fired across two clean
  runs; `Notes — None Found` confirms no note was ever created), and
- the empty result is **dereferenced anyway** — producing the iOS entity chooser on the `Status`
  path and an arbitrary first-note binding on the `Open Control Room` path.

This is the **axis-7 class** (`.claude/CLAUDE.md`, "State shape must exist before it is read")
applied to the Note rather than to `state.json`, and it carries that axis's known trap: the
found/not-found gate is an **existence test over a possibly-empty read**, which that same
document records as unimplementable — the gate is either unreachable or trivially true. The fix
therefore belongs with the container/leaf treatment used for `pending_exit`, not with the filter.

**Still a blocker** for the reason already given: on a clean install an arbitrary personal note
gets bound to `Control Room Note`, which all four `appendnote` sites write to.

## ⚠ CORRECTION — the "create branch never fires" root cause is REFUTED

**User-run observation, 2026-08-17 ~11:39, same session.** The user deleted the hand-made
`PROSOCHĒ` note **and then emptied it from Recently Deleted** — explicitly flagging that second
step as important — and re-ran `Open Control Room`. **It created the Control Room Note correctly**,
titled `PROSOCHĒ` and fully populated (`READ THIS FIRST`, the automation-setup instructions, the
Core/Aware rename paragraph). Verified on device: a single `PROSOCHĒ` note, modified 11:39.

So **the create branch does fire and does work** when nothing matches. The root cause recorded
above — "the create-note branch never runs" — is **wrong and must not be carried forward.**

### What survives, and what is now open

**Still true (device-observed, unchanged):**

- On the first clean run, choosing `Status` raised a full iOS Note chooser over every user note.
- On the second run, `Open Control Room` opened an **unrelated personal note**
  (`/gsd-phase "Build v2 stakeholder addendum"`) and did not create a Control Room Note.
- The `filter.notes` predicate is well-formed, and the cycle-16 limit fix did ship.

**Now the leading candidate — Recently Deleted.** The state I tested was NOT as clean as it
looked. A Notes *search* for `PROSOCH` returned `Notes — None Found`, but **Notes search does not
cover the Recently Deleted folder**, and this device has been through many prior test cycles in
which a `PROSOCHĒ` note would have been created and deleted. If `is.workflow.actions.filter.notes`
matches notes sitting in **Recently Deleted**, then on my run it found a *deleted* note, took the
found-branch, skipped creation, and produced an unresolvable entity — which is precisely the
chooser and the wrong-note binding that were seen. The user's emphasis on purging Recently
Deleted is independent support for this reading.

**This is now the question to settle, and it is a genuinely new one:** does `filter.notes` match
notes in Recently Deleted? If it does, every user who has ever deleted their Control Room Note
without purging is in the broken state, and the fix is a predicate or branch that excludes
deleted notes — not anything to do with creation.

**Experiment.** Create a `PROSOCHĒ` note, delete it but leave it in Recently Deleted, then run
`Open Control Room` and observe whether it is found, a chooser appears, or a fresh note is made.

### Severity

Downgraded in confidence, not yet re-tagged. The `blocker` tag is retained for now because the
observed consequence — an arbitrary personal note bound to `Control Room Note`, which all four
`appendnote` sites write to — is unchanged and is silent user-data corruption if it recurs. If the
Recently Deleted hypothesis is confirmed and the trigger is that narrow, `major` is the fairer tag.

## FINAL CHARACTERISATION (2026-08-18, fresh install) — supersedes everything above

Both earlier hypotheses are dead. The behaviour is now pinned by four observations on a wiped
device with the Note **present**:

| path chosen | Note existed? | chooser? | then? |
|---|---|---|---|
| `Open Control Room` (first action, purged slate) | no → created during the run | **yes**, PROSOCHĒ first row | bare `Text` prompt |
| next run, `Test a Circle` | yes | **no** | — |
| `Toggle Voice` | yes | **yes**, PROSOCHĒ first row | bare `Text` prompt |
| `Status` (previous session, no Note) | no | **yes** | — |

**What this rules out.** Not "Status first" (fires on Open Control Room and Toggle Voice too).
Not "the Note is missing" (fires with the Note present and offered as row 1). Not the
`filter.notes` predicate (well-formed, and `Open Control Room` resolves the right note).

**What it points at.** The chooser appears on **state-changing manual runs** — exactly the runs
where `manual_note_refresh()` appends the settings block — and does **not** appear on a run that
changes no state. The prompt pair is always the same and always in this order:

1. a **`Note` entity chooser** → `appendnote`'s `entity` could not resolve;
2. a **bare text box whose placeholder is the parameter's own name, `Text`** → `appendnote`'s
   `text` could not resolve.

These are iOS **AppIntent parameter-resolution prompts**, not project UI. iOS asks the user to
supply whatever an AppIntent parameter could not resolve, in parameter order. That is why the
second box has no prompt copy — there is none to have. **Both surfaces are one defect.**

Confirmed NOT an axis-2 Ask defect: all **26** `is.workflow.actions.ask` sites in the decrypted
artifact carry real prompts (`'What are you reaching for? (optional)'`, `'How many minutes?'`,
`'Where should Create open?'`, `'What are you trying to find?'`). None is blank.

**So the defect is: on the manual state-changing path, the variable `Control Room Note` is empty
when `manual_note_refresh()`'s `appendnote` runs.** It is populated on the `Open Control Room`
branch (which is why that one opens the right note) but not on the shared manual path. Localise
by tracing where `Control Room Note` is set relative to `manual_note_refresh()` — a source-level
question needing no device.

**Severity settles at `major`, not `blocker`.** The user-data-corruption risk that justified
`blocker` assumed an arbitrary note would be bound silently. In practice iOS *asks*, the correct
note is offered as the first row, and cancelling aborts cleanly without writing. It is intrusive
and confusing, not silently destructive.

## Second, unrelated finding from the same session — the file-save permission prompt

Every state-changing run raises the iOS prompt **"Allow 'PROSOCHĒ — Nine Circles — Core' to save
1 dictionary to a file?"** with `Don't Allow` / `Allow Once` / `Always Allow`, and the prompt body
renders the raw `state.json` to the user. Until `Always Allow` is chosen this recurs on **every**
save, which on the OPEN path would mean a permission dialog in front of the very interruption the
product exists to deliver. Worth an explicit onboarding step in the Control Room Note telling the
user to choose `Always Allow` on first run — otherwise the automation path is unusable and the
failure looks like PROSOCHĒ not firing.

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
