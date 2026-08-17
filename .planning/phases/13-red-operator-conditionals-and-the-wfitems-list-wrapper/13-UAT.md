---
status: blocked
phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
source: [13-01-SUMMARY.md, 13-02-SUMMARY.md, 13-03-SUMMARY.md, 13-04-PLAN.md]
blocked_on: DIST-03
started: 2026-08-17
updated: 2026-08-17
---

# Phase 13 — Device UAT: does a wrapped `WFItems` row actually render?

## Header — what is under test

| Field | Value |
|---|---|
| Phase | `13-red-operator-conditionals-and-the-wfitems-list-wrapper` |
| Written | 2026-08-17 |
| Commit artifacts were signed at | `365937e` — **the CR-01 re-ship**, which supersedes plan 13-04 task 1's `737ce07` |
| Fork 1 | **Core** — `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — 233802 bytes — SHA-256 `b07497ba1a66506aaaa9c48134f463ceefeac7f4a656e86dad48b0a76414ac5b` |
| Fork 2 | **Aware** — `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — 237842 bytes — SHA-256 `212598cff4dd349316aee93c872fb2fd2862eee11f0278d8d02f69a89f447533` |
| Manifest row | `artifacts/shortcuts/MANIFEST.md`, the six "Core"/"Aware" rows — all six values above are copied from it, and `python3 docs/manifest_check.py` proves every row against disk |
| Device requirement | An iPhone running **iOS 26.x** |
| Personal Automations | **Not required for Tests 1–4.** Every test below is reachable from the shortcut's own manual menu, which is why this file can be run without first hand-building the two automations. Test 5 is the only one that needs them. |
| Apple Intelligence | **Not required.** Every test exercises the deterministic Mirror and exit paths, identical on both forks. Run Tests 1–4 on **Core**; Test 6 repeats Test 2 on **Aware** only to confirm the fork divergence did not disturb the wrapper. |

A later run of this file may confirm it is testing the same build it was written against by
recomputing both forks' SHA-256 and comparing against the two values above.

## ⚠ Re-import precondition — read this before anything else

**You must import the artifact signed at commit `365937e` and named in the header, and you must
not test an install that predates it.** This supersedes an earlier revision of this file that
named `737ce07`. That build shipped a second, unevidenced row framing — 44 attachment-free
(literal-by-content) rows encoded as variable rows, all at row 8, the row selected at **Circle
VIII** — found by this phase's own code-review pass as CR-01 and corrected in `365937e`. Importing
the `737ce07` build would test the defect, not the fix. The defect this phase fixed lives in the *shipped
artifact*, not in any on-device state: every `is.workflow.actions.list` row that carried a
variable was emitted without its `{WFItemType: 0, WFValue: …}` row framing, which is predicted to
render as an **empty Mirror body**. A device still holding any earlier build keeps that blank row
until it re-imports. Testing a stale install would observe the old defect and attribute it to a
fix that did land — the single most likely way this file produces a false negative.

Delete any previously installed `PROSOCHĒ — Nine Circles — Core` and
`PROSOCHĒ — Nine Circles — Aware` from the Shortcuts app **before** importing, then confirm the
imported entry is the new one. Because a signed `.shortcut` carries no display name inside it —
the signer strips `WFWorkflowName`, measured on this build — the filename is the only carrier,
so two builds of the same name cannot be told apart in the library once both are installed.

## What this phase changed, in one paragraph

Every List row that **carries an attachment** is now framed as `{WFItemType: 0, WFValue: <the
token string>}`; **616** rows across 66 call sites. **50** rows stay **bare string literals** —
the six exit-name rows plus 44 attachment-free template rows — because Donors 4 and 4.1 show
device-authored `WFItems` arrays using exactly that two-kind mix, and a row with no attachment is
a literal row whatever its Python type. The conditional-operand family — the other half of this
phase's original hypothesis — was **refuted** by Donor 5 and deliberately left **unchanged**.
Nothing else moved.

*(Superseded figure: an earlier revision of this file said 660 wrapped / 6 bare. That was the
`737ce07` build, which discriminated on Python type and so wrapped 44 attachment-free rows as
variable rows. Corrected in `365937e` — see the re-import precondition above.)*

## Why device-only — no automated substitute exists

No file-level check, simulator run, or decrypted-artifact inspection can settle any test in this
file. Per `.claude/CLAUDE.md` §9 ("Rung 2's ceiling") and the evidence hierarchy it extends:

- **Row rendering is a device-visible property.** Whether iOS materialises a wrapped row's
  `WFValue` into visible alert text is runtime behaviour. The plist is already proven correct at
  file level — that is exactly what a device observation neither adds to nor subtracts from.
- **`getitemfromlist` over a wrapped List has no donor.** Donors 4 and 4.1 show iOS *producing*
  wrapped rows, but no donor chains a wrapped List into `getitemfromlist`. Whether Item At Index
  returns the **intended** row over a wrapped array is unmeasured at every rung below 3.
- **Operator/operand type validity is invisible in the plist.** A numeric condition on a
  text-typed operand renders **red** in the editor, is structurally valid in the file, and fails
  at runtime. `.claude/CLAUDE.md` § "Operator/operand type validity is invisible in the plist"
  states plainly that **no** file-level analysis can detect this — not the validator, not the
  catalog, not decrypting the signed artifact.
- **The simulator cannot stand in.** It lacks `com.apple.mobilenotes` (measured 2026-08-17, 25
  installed apps) and cannot import a signed `.shortcut` at all.

The shipped containers were decrypted and measured at **67 List actions, 616 wrapped rows, 50
bare rows, 0 attachment-free wrapped rows and 0 unwrapped rows per fork** (re-measured at
`365937e` after the CR-01 correction; plan 13-04 Task 1's original 660/6 reading describes the
superseded `737ce07` build). **That is structural proof that the right bytes shipped and nothing
more.** It does not observe whether a Mirror renders.

## Setup

1. **Delete** any existing `PROSOCHĒ — Nine Circles — Core` and `— Aware` from the Shortcuts
   app (long-press → Delete), so there is no ambiguity about which build is under test.
2. **Import** `PROSOCHĒ — Nine Circles — Core.shortcut` from the header. Confirm the library
   entry reads exactly `PROSOCHĒ — Nine Circles — Core` with no suffix.
3. **Delete `PROSOCHE/state.json`** (Files → iCloud Drive → Shortcuts → PROSOCHE) so the run
   starts from a genuinely clean state, then run the shortcut once manually and let bootstrap
   complete. A clean state also means no previous contract is recorded, which is what makes
   Test 2's expected-row table valid — see that test's precondition.
4. **Read state at** Files → iCloud Drive → Shortcuts → PROSOCHE → `state.json` (long-press →
   Quick Look). The Control Room Note is the Apple Note titled `PROSOCHĒ`.
5. **Note the active sequence.** Run the shortcut → `Status`, or read `state.json`'s `sequence`.
   Tests 1 and 2 use the `Test a Circle` menu item, which is sequence-independent for row
   selection but not for *which primitive* fires — on `Classic` and `Ambient`, Circle 7 is
   `Mirror`; on `BlackMirror` it is Circle 4. Use whichever Circle your sequence maps to
   `Mirror`, and record which one you used.

## Tests

Each test names an explicit expected observation and leaves its own result field blank until run.

---

### 1. A Mirror renders non-empty text

**Why this is the highest-priority test in this file.** It is the direct CIRC-07 assertion and
the entire reason the phase exists. Every one of the 616 wrapped rows is a template row of this
kind; if a wrapped row does not materialise, this is where it shows. Note that **row 8 is now a
bare literal row** on both the success and lapse families (the 44 rows CR-01 moved), so a blank
at Circle VIII would indict the *bare* path rather than the wrapper — record which row was
showing, not just that it was blank.

**Setup.** Complete the Setup section. No Pressure accumulation is needed — the `Test a Circle`
menu item drives the primitive directly.

**Sequence.** Run the shortcut manually → `Test a Circle` → `Circle 7 · Violence` (on `Classic`
or `Ambient`; on `BlackMirror` choose `Circle 4 · Greed`, the position that sequence gives
`Mirror`).

**Expected observation.** An alert titled **`Mirror`** appears, and its **body contains real
sentence text** — a sentence naming a Circle, a pressure value and a heat value. Specifically
**not**: an empty body, a body showing only whitespace, a body showing a lone `￼` object
placeholder character, or an alert with a title and no message at all.

**This is the observation that would have been blank before this phase.** An empty or
whitespace-only body means the wrapper did not take effect on device and is a **failing** result,
not an inconclusive one — record it as such.

**Failure evidence to capture.** A screenshot of the alert exactly as it appears, including the
title bar, plus the `circle`, `pressure` and `heat` values from `state.json` at that moment.

outcome:

---

### 2. The selected row is the intended one, not merely a non-empty one

**Why this test exists and Test 1 is not enough.** This is the only test that settles Open
Question 1 — whether `getitemfromlist`'s `Item At Index` extraction behaves the same over a
**wrapped** List as over a bare one — and assumption **A4**. No donor chains a wrapped List into
`getitemfromlist`. A row that renders non-empty but is the **wrong** row would pass Test 1
cleanly and hide the regression completely, which is precisely why the assertion must be
"the intended row" rather than "some text".

**Precondition — clean state, no previous contract.** The Mirror overrides its baseline wording
when the recorded previous contract says a boundary was kept (`Previous Respected` = `true`) or
broken (`false`). On a clean install neither applies, so the **baseline** table below is the one
in force. If `state.json` shows a previous contract, delete `state.json` and re-bootstrap before
running this test, or the expected row will legitimately differ.

**Sequence.** Repeat Test 1's `Test a Circle` path for **at least three different Circles** —
suggested: **3**, **7** and **9** — recording the Circle chosen and the exact Mirror body each
time. `Test a Circle` copies the chosen Circle into the value the Mirror indexes with, so the
mapping below is exact and requires no arithmetic.

**Expected observation.** For a chosen Circle *N*, the Mirror body is the *N*-th baseline
template, with the Circle, pressure and heat values substituted in:

| Circle | Expected baseline template (values substituted where marked ◻) |
|---:|---|
| 1 | `Circle ◻ follows recorded pressure ◻ and heat ◻.` |
| 2 | `Recorded now: Circle ◻, pressure ◻, heat ◻.` |
| 3 | `This open reaches Circle ◻ from pressure ◻ and heat ◻.` |
| 4 | `The current record places this at Circle ◻, pressure ◻, heat ◻.` |
| 5 | `Facts for this interruption: Circle ◻; pressure ◻; heat ◻.` |
| 6 | `The saved calculation is Circle ◻ with pressure ◻ and heat ◻.` |
| 7 | `This is Circle ◻ on recorded pressure ◻ and heat ◻.` |
| 8 | `The deterministic reading is Circle ◻, pressure ◻, heat ◻.` |
| 9 | `Recorded signals: Circle ◻, pressure ◻, heat ◻.` |

**Three distinguishable failure shapes, and they mean different things — record which one you
see, not merely "failed":**

- **Right wording, wrong Circle number inside it** → the row selection is correct and the
  substitution is not.
- **Wrong wording for the Circle chosen** (e.g. Circle 7 renders row 3's sentence) → wrapping
  changed what `getitemfromlist` returns. **This is the A4 regression** and the finding this
  test exists to catch.
- **Consistently off by one** (Circle 7 renders row 6 or row 8) → an index-base change, not a
  wrapper problem.

**Failure evidence to capture.** A screenshot per Circle tested, the Circle chosen, and the exact
body text transcribed, side by side.

outcome (Circle 3):

outcome (Circle 7):

outcome (Circle 9):

---

### 3. The six exit names still render as literal text

**Why this test exists — it is the counter-test for the blanket-sweep failure mode.** The six
exit-name rows are the rows this phase deliberately did **not** wrap, because Donors 4 and 4.1
show plain literals as bare strings in a device-authored array. A sweep that wrapped every row
would have corrupted exactly these six. They also round-trip through a `Repeat With Each` that
compares each row against the enabled-exit list, so a wrong row shape shows up here as a
*missing* exit rather than a blank one.

**Sequence.** Reach the Leaving flow: run the shortcut → `Test a Circle` → any Circle → choose
**`Leaving`** at the intervention menu, then look at PROSOCHĒ's exit suggestion list.

**Expected observation.** The exit names render as their **literal text** — `Capture`,
`Coordinate`, `Create`, `Connect`, `Consult`, `Close` — with every exit enabled in
`profile_snapshot.enabled_exits` present and readable. Specifically **not**: a blank row, a row
showing `￼`, a shorter list than `enabled_exits` implies, or an empty suggestion list.

**Failure evidence to capture.** A screenshot of the suggestion list, alongside
`state.json`'s `profile_snapshot.enabled_exits` array, so a missing entry can be told apart from
a deliberately disabled one.

outcome:

---

### 4. Conditional operator chips — an **observation**, not a pass/fail expectation

**Read this framing before recording anything.** This phase changed **nothing** in the
conditional family. The 2026-08-14 red-operator report is **not reproducible at HEAD**, the
screenshot that recorded it does not exist anywhere in the repository or in git history, and
Donor 5 shows the `TEXT`-slot comparison target is **already correct** at all 20 variable-bearing
sites (19 at condition 4, 1 at condition 99). This phase pinned that correct shape with a
positive build assertion rather than altering it.

So there is **no expected result here**. Record what you see.

- **No red chip** → consistent with the refutation. Not a pass of anything; simply the expected
  absence.
- **A red chip** → a **new finding with a live artifact to inspect**, which is exactly the
  outcome the phase goal asks for. Capture it thoroughly; it is worth more than a clean run.

**Sequence.** Open the imported shortcut in the Shortcuts **editor** (long-press → Edit). Scroll
through the action list and inspect the `If` actions — particularly any comparing one variable
against another variable rather than against a typed literal. Note that operator/operand type
validity is invisible in the file and the editor's red rendering is the **only** channel that
surfaces it.

**What to record.** Whether any operator or operand chip renders red; if so, a screenshot showing
the action, its operator, both operands, and enough surrounding actions to locate it in the list;
and the approximate action position.

outcome (any red chip seen — yes / no):

outcome (details if yes):

---

### 5. A real OPEN through a Personal Automation reaches a Mirror

**Why this is separate from Test 1.** Tests 1–4 drive the primitives through the manual menu,
which is the right instrument for row rendering because it removes Pressure arithmetic as a
confound. It does **not** confirm the Mirror renders on the path a user actually takes. This test
does, and it is the only one here that requires the two Personal Automations.

**Setup.** Create or re-point both Personal Automations (Shortcuts app → Automation) to the
**exact display name** `PROSOCHĒ — Nine Circles — Core`: `App Is Opened` → `OPEN` as Shortcut
Input, `App Is Closed` → `CLOSE` as Shortcut Input, both with `Run Immediately` (Ask Before
Running off).

**Sequence.** Open a tracked app repeatedly in close succession until Pressure carries the run to
the Circle your sequence maps to `Mirror` (`Status` reports the current Circle between opens).

**Expected observation.** The Mirror alert fires with non-empty body text, matching the same
baseline table as Test 2 for whatever Circle the run reports.

**Failure evidence to capture.** A screenshot of the alert and of `Status` immediately before it,
so the reported Circle and the rendered row can be compared.

outcome:

---

### 6. Repeat Test 2 on the Aware fork

**Why.** `tools/build_sentient.py` forks the built Core source and applies a deliberate string
divergence through an offset-recomputing round trip. Both forks measure 616 wrapped rows in their
decrypted payloads, so this is a low-expectation regression check rather than a new question —
but the fork step is the only place a correct Core artifact could become an incorrect Aware one.

**Setup.** Import `PROSOCHĒ — Nine Circles — Aware.shortcut` from the header, deleting any
earlier Aware install first. Apple Intelligence is not required for this test.

**Sequence.** Run Test 2 against Aware for a single Circle (7 is sufficient).

**Expected observation.** Identical to Test 2 — the *N*-th baseline template, non-empty.

**Failure evidence to capture.** A screenshot, plus confirmation that the installed entry is the
Aware build at the header's SHA-256.

outcome:

---

## Results

| # | Test | Outcome |
|---|---|---|
| 1 | A Mirror renders non-empty text | |
| 2 | The selected row is the intended one (Circles 3, 7, 9) | |
| 3 | The six exit names still render as literal text | |
| 4 | Conditional operator chips — observation only | |
| 5 | A real OPEN through a Personal Automation reaches a Mirror | |
| 6 | Repeat Test 2 on the Aware fork | |

## Summary

total: 6 (Test 2 carries 3 sub-observations, Test 4 carries 2)
passed: 0
issues: 0
skipped: 0
blocked: 6

## Reachability probe

```
$ xcrun devicectl list devices
No devices found.
```

Run 2026-08-17. iPhone Mirroring was not attempted as a substitute channel — `devicectl`
reporting no connected devices means no iPhone is attached to this Mac at all, so a mirroring
session (which requires the same physical/Wi-Fi connection) is not available either.

**Verdict: BLOCKED.**

## Standing note — what may not be substituted for a device observation

**Every outcome field above stays blank.** This is the recorded precedent set by `10-UAT.md`
(Phase 10: `xcrun devicectl list devices` → "No devices found." → all ten tests left blank,
DIST-03 unchecked) and reaffirmed by `12-UAT.md` on the same probe result. It is not a failure and
it is not an oversight — it is this project's standing, deliberate policy that a fabricated pass
is worse than a blank.

**Do not substitute a simulator run, a Mac import, or any inference from the decrypted artifact
for a device observation.** Both signed containers were decrypted and confirmed at 67 List
actions, 616 wrapped rows, 50 bare rows, 0 attachment-free wrapped rows and 0 unwrapped rows per
fork (at `365937e`). That is structural proof only. None of it observes whether a wrapped row renders, or which row `getitemfromlist`
returns, and the simulator cannot close the gap either — it lacks `com.apple.mobilenotes` and
cannot import a signed `.shortcut` at all.

**This UAT is re-run unchanged when a device becomes reachable.** Do not rewrite the tests above
to fit whatever device eventually connects; run them exactly as written against the build named
in the header, or against a freshly signed rebuild provided its SHA-256 is updated in the header
first. If a rebuild is used, the re-import precondition applies to it too.

**If this file is still blocked when Phase 19 runs, fold it into Phase 19's device UAT rather
than dropping it** — Tests 1 and 2 are the assertions `13-RESEARCH.md` assigns to Phase 19 by
name (assumptions A1 and A4), and Test 2's expected-row table is the part that must not be
weakened into a non-emptiness check.

DIST-03 stays **unchecked** in `.planning/REQUIREMENTS.md` until every test above has a recorded
outcome from a real iPhone.

## Verdict

_Blank. Filled in only after the six tests above resolve on a real device._
