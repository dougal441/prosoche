---
status: blocked
phase: 15-circle-8-the-voice-primitive
source: [15-01-SUMMARY.md, 15-02-SUMMARY.md, 15-03-SUMMARY.md, 15-04-SUMMARY.md, 15-05-PLAN.md]
blocked_on: DIST-03
started: 2026-08-18
updated: 2026-08-18
---

# Phase 15 — Device UAT: does Circle 8 actually speak?

## ⚠ HEAD-OF-FILE WARNING — read this before running anything

**Unless a later rung-3 device session or a fresh rung-2 probe has closed the axis-4
unfilled-picker blocker since this file was written, Tests 1, 2 and 3 below are EXPECTED TO
FAIL** with the alert *"Please choose a value for each parameter in this action."* This is not
a guess: the Mirror primitive both `mirror()` (Circle 7) and `voice()` (Circle 8) are built on
carries a **device-reproduced** failure, reproduced three times across two independent installs,
proven to follow the primitive rather than the Circle index
(`.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md`). Plan 15-02's own
rung-2 simulator probe (spike 011) did **not** discriminate which of the three candidate action
identifiers carries it — verdict `not discriminated at rung 2`, routed to Branch B, no generator
fix attempted. Nothing in Phase 15 closed this defect; the phase's own scope was the Mirror/Voice
split, the `voice_enabled` type fix, and the build guards that hold both structurally — none of
which touches the axis-4 question.

**If you hit that exact error at Circle 8 or Circle 7, this is the KNOWN inherited defect, not a
new regression.** Record it as such, cross-reference
`.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md`, and do **not** file a
new todo for it. **If you hit a *different* error, or Circle 8/7 behave in some other unexpected
way, that IS a new finding** — record it in full, with a screenshot and the exact alert text,
because the axis-4 error has one specific known wording and anything else is unexplained by this
project's current record.

**Do not infer a PASS from a green build.** Every checker, gate A on both forks, and this phase's
six build guards are green — none of that is evidence Circle 8 fires audibly on a phone.
`artifacts/shortcuts/MANIFEST.md`'s plan-15-05 block and `docs/BUILD-NOTES.md` §36 both say so in
the same words used here.

---

## Header — what is under test

| Field | Value |
|---|---|
| Phase | `15-circle-8-the-voice-primitive` |
| Written | 2026-08-18 |
| Commit artifacts were signed at | `0870817` — plan 15-05 Task 1's rebuild-and-sign commit |
| Fork 1 | **Core** — `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — 225345 bytes — SHA-256 `a5b2976adb88f9ac9db8d4ded298634cf6afd04e84a4a65cd0218b028db8af34` |
| Fork 2 | **Aware** — `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — 231675 bytes — SHA-256 `8a20813efe9c3211a21425d77bfb723e15a686e97557c877196b266b150834c8` |
| Manifest rows | `artifacts/shortcuts/MANIFEST.md`, the plan-15-05 block's `Core signed` and `Aware signed` rows. All four values above are copied from that block, and `python3 docs/manifest_check.py` proves every row against disk. |
| Device requirement | An iPhone running **iOS 26.x**. The paired device on record is an **iPhone 15 Pro (`iPhone16,1`) on iOS 26.6** — inside the declared target, so an observation on it is same-major-version evidence, not an extrapolation. |
| Personal Automations | **Not required.** Every test below is reachable from the shortcut's own manual menu (`Test a Circle`, `Toggle Voice`). |
| Apple Intelligence | **Not required.** Every test here exercises the deterministic Mirror/Voice path, which is identical on both forks. Run on **Core** unless otherwise noted. |
| Currently installed on the developer's iPhone | **NOT this build.** The last device session (2026-08-17/18) ran against Core `b07497ba1a66506aaaa9c48134f463ceefeac7f4a656e86dad48b0a76414ac5b` (233802 bytes, the phase-13 CR-01 signing) — several rebuilds behind this one. No install has happened since. |

**One-line re-verification recipe** — run this before trusting any outcome recorded below, to
prove you are testing the build this file was written against:

```bash
shasum -a 256 "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut" \
              "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut"
```

Both digests must match the header exactly. If they do not, either the artifacts were re-signed
after this file was written — in which case update the header from `MANIFEST.md` first and say
so — or you are looking at the wrong files. **A digest mismatch invalidates every test below.**

### ⚠ Batching note — do not schedule this session alone, and mind the schema-bump ordering

A connected iPhone session is the scarcest input this project has. **This session should
discharge several standing debts at once.** Schedule it together with:

| Also run | What it is | Why it batches here |
|---|---|---|
| `16-UAT.md` | Dimming/Silence capture-and-restore, the highest-risk untested path in the product | Same clean-install setup; needs the same device session |
| `12-UAT.md` **Test 3** | CLOSE after a session that changed brightness or volume | Same observation, written from the SESS-07 side |
| `13-UAT.md` | Wrapped `WFItems` row rendering | Same DIST-03 blocker; costs minutes once a device is in hand |
| `10-UAT.md` | Circle 0, the quieted Control Room, `Setup Check` | Same |
| Phase 19's full nine-Circle device sweep | Every Circle fires at least once on hardware | This file's Tests 1–2 **are** two of that sweep's nine observations; do not repeat them there |

**⚠ Schema-bump ordering — read this before you do anything else with this device.** Per plan
15-03's recorded sequencing constraint (`15-03-SUMMARY.md` § "Schema bump — sequencing
constraint"): **build and install this Phase-15 signed build BEFORE any Pressure-accumulation UAT
session, never after.** The `schema_version` 4→5 bump this build carries wipes `heat`, `gravity`,
`pressure`, every rolling window, the session record, `exit_events` and every
`exit_stats[*].samples` on the developer's iPhone at the first run of the new build. That
accumulation is the prerequisite for roughly thirty queued tests across phases 06, 12 and 13 — if
that session happens first and this build is installed after, it is thrown away and must be
repeated. **Also note:** re-installing a `.shortcut` alone does **not** wipe `state.json` — the
two are separate files, and a shortcut re-install alone leaves accumulated state intact. Only the
`schema_version` bump forces the rebuild.

---

## Setup

Complete every step in order before Test 1.

1. **Delete both existing installs and re-import.** A signed `.shortcut` carries no display name
   inside it (the signer strips `WFWorkflowName`), so the filename is the only carrier and the
   only reliable way to confirm which build is installed is to replace, not inspect. In the
   Shortcuts app, long-press `PROSOCHĒ — Nine Circles — Core` → **Delete** (and `— Aware` if
   present). Confirm the library no longer lists either name. Import the two files named in the
   header, freshly transferred from this repository at commit `0870817`. Confirm each library
   entry reads **exactly** the display name, with **no suffix**.
2. **Note the active sequence.** Run the shortcut → `Status`, or read `state.json`'s `sequence`.
   Which Circle is Mirror (Circle 7) and which is Loud Mirror/Voice (Circle 8) does not change by
   sequence — all three sequences place Mirror at Circle 7 and Loud Mirror at Circle 8 — but
   record which sequence is active anyway, since other batched instruments need it.
3. **Confirm `voice_enabled`'s current setting.** Run the shortcut → `Status`; the Voice line now
   reads `Voice: 1` or `Voice: 0` (D-05's numeric normalisation — it no longer reads `Voice: Yes`
   on a fresh install). Record which.
4. **Read state at** Files → iCloud Drive → Shortcuts → PROSOCHE → `state.json` (long-press →
   Quick Look), if you need to confirm `schema_version` reads `5` after the first run on this
   build.

---

## Tests

Four tests. Each names an explicit expected observation and an explicit failure signature. A test
you did not run is BLOCKED, not passed. Given the head-of-file warning, Tests 1–3 are expected to
fail with the axis-4 error unless that defect has been independently closed since this file was
written — record the ACTUAL observation regardless of expectation; an unexpected pass is exactly
as reportable as an unexpected failure.

---

### 1. Circle 8 speaks

**Why this is first.** It is the phase's headline claim (CIRC-08) and the one most likely to be
blocked by the inherited axis-4 defect — see the head-of-file warning.

**Setup.** Voice enabled (`Status` reads `Voice: 1`; if not, `Toggle Voice` first). Use the
`Test a Circle` harness rather than accumulating real Pressure to Circle 8 — the harness never
writes Pressure, and accumulating to Circle 8 is roughly thirty tests' worth of prerequisite work
this phase does not require.

**Sequence.** Run the shortcut manually → `Test a Circle` → **Circle 8 · Fraud**.

**Expected observation (if the axis-4 defect is closed).** The alert renders **and** the same
text is spoken **exactly once** — not zero times, not twice. The spoken text matches the alert's
body verbatim.

**Expected observation (if the axis-4 defect is still open, per the head-of-file warning).** The
alert *"Please choose a value for each parameter in this action."* appears instead, and nothing
renders or speaks. This is the KNOWN inherited defect — cross-reference the blocker todo, do not
file a new one.

**Failure signature for a genuinely NEW defect (neither of the above).** Any other error text, an
alert that renders with no speech and no axis-4 error, speech without a visible alert, or speech
occurring more than once. Capture the exact alert text and a screenshot.

outcome (alert rendered — Y/N):

outcome (spoken — Y/N, and how many times):

outcome (exact text of any error, verbatim):

---

### 2. Circle 7 no longer speaks

**Why this test exists.** D-02's visible behaviour change (`docs/BUILD-NOTES.md` §36.1) — Circle
7 goes quiet for existing `voice_enabled = 1` users. **The tester must be told this is intended,
or it will be filed as a regression.** It is not: Circle 7 dispatches `mirror()`, which has no
`speaktext` action at all — `verify_speaktext_placement()` fails the build if it ever regains one.

**Setup.** Voice enabled (`Status` reads `Voice: 1`).

**Sequence.** Run the shortcut manually → `Test a Circle` → **Circle 7 · Violence**.

**Expected observation.** The alert renders and **nothing is spoken** — this is correct, expected
behaviour, not a defect. If Circle 7 *is* reachable at all (see the head-of-file warning — Circle
7 shares the same Mirror primitive and may hit the same axis-4 defect), record that instead.

**Failure signature.** Circle 7 speaks (a genuine regression — `verify_speaktext_placement()`
should have caught this at build time, so also check which build is actually installed), or
Circle 7 raises an error other than the known axis-4 one.

outcome (alert rendered — Y/N):

outcome (spoken — Y/N — expected N):

---

### 3. Circle 8 degrades rather than skips, with voice off

**Why this test exists.** D-01's accepted cost, made observable: with voice off, Circle 7 and
Circle 8 are expected to look **identical** to the user — both show an alert, neither speaks.
This is the tradeoff §36.1 records, not a defect. It is also the direct test that Circle 8 does
not go silently empty the way the pre-Phase-15 build did (the original defect this whole phase
exists to close).

**Setup.** Toggle Voice off in the Control Room (`Status` should then read `Voice: 0`).

**Sequence.** Run the shortcut manually → `Test a Circle` → **Circle 8 · Fraud**.

**Expected observation.** An alert renders and **nothing is spoken** — indistinguishable from
Circle 7 at this setting, and that indistinguishability is D-01's recorded, accepted cost, not a
bug to fix. If the axis-4 defect is still open, no alert renders at all — see the head-of-file
warning.

**Failure signature.** Nothing renders at all with **no** axis-4 error present (this would be a
NEW empty-Circle defect, exactly the class this phase exists to prevent), or speech occurs despite
voice being off (a consent-gate failure — check `verify_voice_gates()` is actually armed in the
installed build).

outcome (alert rendered — Y/N):

outcome (spoken — Y/N — expected N):

---

### 4. The consent flag round-trips as a number

**Why this test exists.** D-05's normalisation — before this phase, a fresh install's Status line
read `Voice: Yes` (boolean rendering) and degraded to `Voice: 1` (numeric rendering) after the
first `Toggle Voice` call, because the two writers disagreed on JSON type. After D-05, both
writers agree and the Status line should never show `Yes`/`No` at all.

**Setup.** A fresh bootstrap on this build (Setup step 1's re-import, or a deleted `state.json`
if you want a fully clean seed — not required for this test, since D-05 changed the writer, not
just the toggle path).

**Sequence.** Run the shortcut manually → `Status`, before touching `Toggle Voice`. Then
`Toggle Voice` once, and read `Status` again.

**Expected observation.** Both readings show the **numeric** form (`Voice: 1` or `Voice: 0`) —
consistently, with no `Yes`/`No` wording at either point. `state.json`'s `voice_enabled` key is a
JSON number, not a boolean, at both readings (Quick Look → note whether the value is quoted or
bare `true`/`false` vs. a bare digit).

**Failure signature.** Any occurrence of `Voice: Yes` or `Voice: No` in the Status line (would
mean an un-rebuilt or stale artifact — re-check the header digest), or `state.json`'s
`voice_enabled` holding `true`/`false` rather than `1`/`0` after a fresh bootstrap on this build.

outcome (Status line reading, before Toggle Voice):

outcome (Status line reading, after Toggle Voice):

outcome (`state.json` `voice_enabled` value and JSON type, Quick Look):

---

## Closing note

This file's four tests are the phase's own Manual-Only Verifications
(`15-VALIDATION.md` § "Manual-Only Verifications") turned into a cold-runnable instrument. Do not
mark this file's `status:` frontmatter field `passed` unless every test above ran with recorded
outcomes and no test reports a genuinely new defect. If Tests 1–3 report the known axis-4 error as
expected, that is a `blocked` outcome for CIRC-08, not a `passed` one — record it as such and
leave `status: blocked` until the axis-4 defect itself closes.
