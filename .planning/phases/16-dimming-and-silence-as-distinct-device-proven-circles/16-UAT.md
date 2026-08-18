---
status: blocked
phase: 16-dimming-and-silence-as-distinct-device-proven-circles
source: [16-01-SUMMARY.md, 16-02-SUMMARY.md, 16-03-SUMMARY.md, 16-04-SUMMARY.md, 16-05-SUMMARY.md, 16-06-PLAN.md]
blocked_on: DIST-03
started: 2026-08-18
updated: 2026-08-18
---

# Phase 16 — Device UAT: does the capture-and-restore loop actually close?

## ⚠ SAFETY PREAMBLE — read this before anything else on this page

**This file is the first instrument in this project that deliberately changes the physical
state of the phone it runs on.** Every other UAT observed rendering. This one dims the screen
and drops the media volume, on purpose, and then asks whether the product puts them back.

1. **Brightness and volume will actually change.** Since the Phase 9 coercion fix merged, Set
   Brightness and Set Volume execute where they previously no-opped. The dim target in this
   build is **`0`** — the device's true minimum. Expect the screen to become **very dark**.
2. **If the phone is left dim or quiet, iOS Settings is the only recovery.** Settings →
   Display & Brightness for the slider; the hardware volume buttons or Settings → Sounds &
   Haptics for media volume. Control Centre works too. **Learn where these are before you
   start**, because you may have to find them on a screen you can barely read.
3. **Do not begin if you need this phone for anything else in the next ~90 minutes.** Tests 6
   and 7 involve force-quitting an app and restarting the device mid-session.

### The live hazard — read this even if you are not testing today

**Any device that has already run a post-coercion-fix build and reached Dimming or Silence is
dim and quiet RIGHT NOW, with no capture on disk, and Emergency Restore cannot help it.**

That is not a hypothetical. Until the build named in the header below, the captured original
brightness was written into the `State` dictionary, which is never saved again after the OPEN
arm's last save — so it never reached `state.json`. CLOSE and Emergency Restore both reload
the file, find the cleared sentinel, fail the numeric `> 0` gate and skip. Emergency Restore
reads the same file as CLOSE, so tapping it on such a device does nothing at all: there is
nothing on disk for it to restore *to*.

**Such a device must be restored by hand, through iOS Settings, before testing begins.** This
is also the single clearest statement of the defect this phase fixed — if you find the phone
dim with a `settings_snapshot` full of `"null"`, you have just reproduced the P0 by accident.

---

## Header — what is under test

| Field | Value |
|---|---|
| Phase | `16-dimming-and-silence-as-distinct-device-proven-circles` |
| Written | 2026-08-18 |
| Commit artifacts were signed at | `9e1e540` — the **phase 11** wave-9 re-sign. **Re-pinned from `04f3612` (phase 16) on 2026-08-18**: phase 11 waves 7-9 each rebuilt and re-signed both forks, so the phase-16 digests below no longer existed on disk. The phase-16 values are retained in git history, not restated here. |
| Fork 1 | **Core** — `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — 231148 bytes — SHA-256 `873fa3dbda7b1f3440bfc76997c2962198ddec2052096833787547b52f129f10` |
| Fork 2 | **Aware** — `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — 238095 bytes — SHA-256 `4b7c2cfbddf0dccf47ef8e34209378faf14ca2d760dc089013d3b033ebd2ada0` |
| Manifest rows | `artifacts/shortcuts/MANIFEST.md`, the `Core signed` and `Aware signed` rows. All four values above are copied from that table, and `python3 docs/manifest_check.py` proves every row against disk. |
| Device requirement | An iPhone running **iOS 26.x**. The paired device on record is an **iPhone 15 Pro (`iPhone16,1`) on iOS 26.6** — inside the declared target, so an observation on it is same-major-version evidence, not an extrapolation. |
| Personal Automations | **Required for Tests 4 and 6–11.** Tests 1, 2, 3, 5 and 12 are reachable from the shortcut's own manual menu. |
| Apple Intelligence | **Not required.** Every test here exercises the deterministic capture/apply/restore path, which is identical on both forks. Run everything on **Core**; the Aware fork is exercised only by the note under Test 12. |

**One-line re-verification recipe** — run this before trusting any outcome recorded below, to
prove you are testing the build this file was written against:

```bash
shasum -a 256 "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut" \
              "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut"
```

Both digests must match the header exactly. If they do not, either the artifacts were re-signed
after this file was written — in which case update the header from `MANIFEST.md` first and say
so — or you are looking at the wrong files. **A digest mismatch invalidates every test below**,
because the whole point of this phase is that the previous build could not restore.

### ⚠ Batching note — do not schedule this session alone

A connected iPhone session is the scarcest input this project has. **This session should
discharge several standing debts at once.** Schedule it together with:

| Also run | What it is | Why it batches here |
|---|---|---|
| `12-UAT.md` **Test 3** | CLOSE after a session that changed brightness or volume | It is *the same observation* as Test 4 below, written from the SESS-07 side. Running it separately would dim the phone twice for one fact. |
| **Phase 18** — locked-screen CLOSE | Whether a CLOSE firing against a locked screen persists at all | The locked-screen case is **handed to Phase 18 and is deliberately NOT a test in this file** — see the section below. Phase 18's own ROADMAP text says the two should be investigated together rather than twice. |
| **Phase 19** — nine-Circle device UAT | The full sweep of all nine Circles and sequence switching | It needs the same clean install, the same deleted `state.json` and the same Personal Automations this file's Setup builds. |
| `13-UAT.md` | Wrapped `WFItems` row rendering | BLOCKED on the same DIST-03; its Tests 1–4 need no automations and cost minutes once a device is in hand. |
| `10-UAT.md` | Circle 0, the quieted Control Room, `Setup Check` | Same. |
| Spike **010** Breadcrumbs probe | `.planning/spikes/010-coercion-at-a-direct-set-parameter/PROSOCHE Coercion Probe Breadcrumbs.shortcut` | Test 1 below **is** this probe. It is already built, signed and simulator-tested. |

---

## ⚠ Re-import precondition — a stale install produces a false negative on almost every test

**You must import the artifacts signed at commit `04f3612` and named in the header, and you must
not test an install that predates them.**

The defect this phase fixed lives in the **shipped artifact**, not in on-device state. A device
still holding any earlier build carries an *unpersisted capture*: it will dim, it will write the
original into a dictionary that is never saved, and then CLOSE will find nothing to restore. On
that build, Tests 2, 3, 4, 6, 7, 8, 9, 10 and 11 all fail — and they fail for a reason that has
already been fixed. **Testing a stale install would observe the old defect and attribute it to a
fix that did land**, which is the single most likely way this file produces a false negative.

**How to confirm which build is installed.** A signed `.shortcut` carries no display name inside
it — the signer strips `WFWorkflowName`, measured on this build — so the filename is the only
carrier, and two builds of the same name are indistinguishable in the library once both are
installed. There is no version string to read on device. **The only reliable procedure is to
replace, not to inspect:**

1. In the Shortcuts app, long-press `PROSOCHĒ — Nine Circles — Core` → **Delete**. Do the same
   for `PROSOCHĒ — Nine Circles — Aware` if present.
2. Confirm the library no longer lists either name.
3. Import the two files named in the header, freshly transferred from this repository at commit
   `04f3612`.
4. Confirm each library entry reads **exactly** `PROSOCHĒ — Nine Circles — Core` /
   `— Aware`, with **no suffix**. A suffixed entry is a different library item that your
   Personal Automations do not reference.

**Then re-point both Personal Automations** (Setup step 5). Deleting a shortcut leaves the
automations pointing at nothing; they do not follow the replacement.

---

## What this phase changed, in one paragraph

The captured original brightness and volume are now written to `state.json` **before** Set
Brightness / Set Volume runs, on every path that applies a change (plan 16-01, +44 actions per
fork). `safety.brightness_floor` and `safety.dim_target` both moved to **`0`**, so Dimming
reaches the device's true minimum, and the eleven-per-fork shipped comment actions asserting a
lower bound on the brightness write were replaced by a statement of the capture-and-restore
property (plan 16-03, decision D-01). The two dead snapshot leaves `changed_at` and
`changed_by_session_id` — 44 writes per fork, zero readers — were removed from the writes, the
bootstrap seed and the phase5 assertion, with a build guard that fails any future build which
reads one (plan 16-04, decision D-02, −88 actions per fork). Nothing else in the
capture/apply/restore path moved: **the has-any-value container gate and the numeric `> 0`
capture gate are byte-identical to their pre-phase form** in both primitives, and both restore
gates are untouched.

**A consequence of D-01 worth knowing before you test.** `dim_target` is now `0`, and the
already-dim short-circuit fires when the captured brightness is **≤** the dim target, inside an
arm that already requires the captured brightness to be **> 0**. Those two conditions are now
mutually exclusive, so **the already-dim arm is effectively unreachable for brightness on this
build**: any positive captured brightness is dimmed to `0`. That is the decision working as
specified, not a defect — but it means Test 5's zero-brightness observation happens on *every*
dimming run rather than occasionally.

---

## Why device-only, per test — and what NOT to re-run on hardware

Per `.claude/CLAUDE.md` §9's evidence-escalation ladder and its "Rung 2's ceiling" list. The
governing rule is **never climb higher than the open question requires** — a device session
spent re-deriving something a free rung already settled is a session wasted.

### Already settled below rung 3 — do NOT re-run these on hardware

| Question | Where it was settled | Verdict |
|---|---|---|
| **Does the coercion chip render red at a `Set Brightness` parameter?** | Rung 2, plan 16-02, spike 010 | **The question is void.** The coerced and uncoerced legs render **identically**. A conditional's operator picker is populated from the operand's static type, so a mismatch renders red; **`Set Brightness` has no operator picker**, so there is nothing for a type mismatch to break. `09-UAT.md` Test 1 — this project's one recorded device pass on this subject — **was never evidence about `WFBrightness`/`WFVolume` at all.** A green chip there is not weak evidence; it is *no* evidence. Do not re-run a chip inspection and do not record one as a result. What replaces it is Test 1 below, which observes the **value applied**. |
| **Are the 11 uncoerced `setvolume` sites a defect?** | Rung 1, plan 16-02, name-scoped provenance audit | **No — correctly uncoerced.** All 11 `Set Variable "Silence Target"` assignments are `is.workflow.actions.number`-sourced and therefore already Number-typed; the 4 coerced sites are the *restore* operands, which come back out of state as Text. 11 + 4 = 15 exactly, on both forks. **Do not "fix" the asymmetry by pattern-matching brightness.** Nothing about this needs a device. |
| **Can a simulator import a signed `.shortcut`?** | Rung 2, plan 16-02 | **Yes** — `xcrun simctl openurl <udid> "file:///…"` plus one synthesized tap. This retires spike 007's contrary claim. Relevant here only because it means the probe in Test 1 has *already been import-tested*, so a failure on device is about the device. |
| **Is the persist-before-apply ordering structurally real?** | Rung 1, plan 16-01 | **Yes, on both forks**, pinned by `verify_capture_persistence` with a negative control proving the guard fires. **This is exactly what a device observation neither adds to nor subtracts from** — it says the right bytes shipped, and nothing about whether the loop closes. |

### Genuinely device-gated — nothing cheaper settles these

- **`Get Device Details → Current Brightness` returning a real, usable, correctly-typed value.**
  Inside §9's rung-2 ceiling: real-hardware environmental behaviour. The simulator reads
  brightness as `0` and cannot execute `Set Brightness` at all — measured, plan 16-02. **Tests
  1, 2, 3.**
- **Whether `Set Brightness` CONSUMES a Number-coerced operand at run time.** Rung 2 was tried
  and is now known to be *unable* to answer it: the run-time channel produced a **capability**
  error on both the coerced leg and a one-action negative control with no operand at all, so it
  cannot distinguish a resolved operand from an absent one. **No further simulator effort will
  help.** **Test 1.**
- **What `WFBrightness = 0` actually looks like on a real screen.** The "dim, not black" claim
  rests on **one unrepeated user report**, and decision D-01 accepts it on that basis. This is
  the device input to a decision already taken. **Test 5.**
- **That `state.json` round-trips a captured brightness without precision loss.** Rung 1 proves
  the save is emitted; only hardware proves the value survives. **Tests 2, 4.**
- **Every interruption trial.** Force-quit, restart, missed CLOSE, overlapping sessions and the
  compound case all require interrupting a live run on real hardware. **Tests 6–10.**
- **Emergency Restore.** It has **never been tapped on a device**. **Test 11.**
- **Personal Automations.** User-created on the device; they cannot be exercised anywhere else,
  at any effort. This is DIST-03's irreducible core.

### ⚠ The one hazard CAP-08 puts on every brightness test in this file

**`setbrightness.WFBrightness` is OPTIONAL and defaults to 50%** — measured at rung 2, plan
16-02, recorded as CAP-08. An absent or unresolved operand renders as "Set brightness to 50%"
and does **not** raise the unfilled-parameter error. So an operand that fails to resolve fails
**silently**, applying an unrequested 50% with no capture behind it, rather than halting.

**Therefore: every brightness test below is written to verify the value that was actually
applied, never the absence of an error message.** "No error appeared" is fully consistent with
a silently defaulted 50%. A test that checks only for the absence of an error is a false-pass
generator, and any outcome recorded in those terms must be treated as unrecorded.

---

## The screen-locked case is Phase 18's, and is deliberately NOT tested here

`09-UAT.md`'s ugly-cases block listed "screen locked mid-session" alongside force-quit, restart
and missed CLOSE. **It is not a test in this file, on purpose.**

**Phase 18 — "Persist state when CLOSE fires from a locked screen" — owns it.** Its ROADMAP
entry names this exact overlap and says the two "should be investigated together rather than
twice"; its source todo is the authority on the observed symptom; and
`.planning/spikes/001-device-is-locked-literal` and
`.planning/spikes/002-close-automation-vs-screen-lock` already hold adjacent spike work.
Phase 18 must establish *first* whether the automation fires at all, fires and cannot write, or
fires and writes late — because the fix differs entirely per case, and an unrestored
environmental change is one of the consequences it is chartered to fix.

Duplicating it here would produce a second, shallower investigation of the same device
behaviour from a worse angle. **When Phase 18 runs, its instrument should include a brightness
or volume change in the locked session**, so the environmental restore is observed on that path
in the same session. That is the whole handoff.

---

## ⚠ Known outstanding artifacts — so a blank alert is attributed correctly

Phase 13 is merged, so the blank-Mirror defect it fixed is **no longer expected**. But three
interim states still ship in the build under test, and each can look like a Dimming failure if
you do not know about it. **None of these is a finding. Do not report them as one.**

| What you may see | Why | Owner |
|---|---|---|
| **Circle 6 shows `Eject`, not `Redirect`** | BD-06 gives Circle 6 to `Redirect` in `Classic` and `Ambient`, but `Redirect` has no implementation yet, and the build guard fails on any dispatch branch no sequence names. All three sequences hold `Eject` at Circle 6 as an interim. | **Phase 17** |
| **Circle 8 (`Loud Mirror`) behaves exactly like Circle 7 (`Mirror`)** | Circle 8 dispatches the same `mirror_and_voice()` implementation so the entry reaches a real branch at all. It is a stand-in, not the designed Voice primitive. | **Phase 15** |
| **`Black and White` shows an alert instead of turning the screen grayscale** | Color Filters is not togglable from Shortcuts on iOS; the primitive ships as its alert-only fallback. | **Phase 14** |

If a Circle produces a blank or unexpected alert **that is not one of the three above**, it is a
real finding — capture it, and note which Circle and which sequence were active.

---

## Setup

Complete every step in order before Test 1. Steps 6 and 7 are the ones the whole file depends
on; do not skip them because they feel like bookkeeping.

1. **Restore the phone by hand if it is already dim or quiet.** Read the safety preamble's live
   hazard first. If `state.json` shows a `settings_snapshot` full of `"null"` on a dim phone,
   fix the brightness in iOS Settings before doing anything else, and record that you had to.
2. **Delete both existing installs and re-import**, per the re-import precondition above.
   Confirm both library names are exact and unsuffixed.
3. **Delete `state.json`.** Files → iCloud Drive → Shortcuts → **PROSOCHE** → `state.json` →
   long-press → Delete. This forces a genuinely clean bootstrap and is what makes Test 12's
   seed-shape assertion meaningful.
4. **Run the shortcut once manually** and let bootstrap complete. Confirm `state.json` is
   recreated.
5. **Re-point both Personal Automations** to the **exact display name**
   `PROSOCHĒ — Nine Circles — Core`: Shortcuts → Automation → `App Is Opened` → Shortcut Input
   `OPEN`; `App Is Closed` → Shortcut Input `CLOSE`. Both with **Run Immediately** (Ask Before
   Running **off**). Deleting the shortcut in step 2 left these pointing at nothing.
6. **Record the pre-session brightness and volume BY HAND, IN WRITING, right now.** Not from
   memory, not from a screenshot you intend to take later, and not from the shortcut's own
   reading — the entire proof in Tests 4 and 11 is a comparison against these two numbers, and
   if they come from the same mechanism under test the comparison is circular.

   | Quantity | Where to read it | Value recorded by hand |
   |---|---|---|
   | Brightness | Settings → Display & Brightness, slider position (or Control Centre) | |
   | Media volume | Play any audio, then Settings → Sounds & Haptics, or the on-screen slider | |
   | Time recorded | | |

7. **Note the active sequence.** Run the shortcut → `Status`, or read `state.json`'s `sequence`.
   Which Circle fires Dimming and Silence depends on it:

   | Sequence | Silence at | Dimming at |
   |---|---|---|
   | `Classic` | Circle 3 · Gluttony | Circle 5 · Wrath |
   | `BlackMirror` | Circle 5 · Wrath | Circle 7 · Violence |
   | `Ambient` | Circle 2 · Lust | Circle 3 · Gluttony |

   **Record which sequence was active for every test below.** A result with no sequence recorded
   cannot be interpreted.

8. **Read state at** Files → iCloud Drive → Shortcuts → PROSOCHE → `state.json` (long-press →
   Quick Look). The Control Room Note is the Apple Note titled `PROSOCHĒ`.

---

## Tests

Twelve tests, numbered 1–12. Each names an explicit expected observation and leaves its own
`outcome:` field blank until run. **A test you did not run is BLOCKED, not passed**, and a
result settled at rung 2 is recorded as settled at rung 2 with its channel named — never
promoted to a device result.

---

### 1. The coerced operand's applied VALUE, via the spike-010 Breadcrumbs probe

**Why this replaces the old chip gate, and why it is first.** `09-UAT.md`'s Test 1 — the one
recorded pass this project has on the subject — asked whether the coercion chip renders red.
Plan 16-02 established at rung 2 that **the chip gate cannot discriminate here at all**: the
coerced and uncoerced legs render identically, because `Set Brightness` has no operator picker
for a type mismatch to break. So the question was **sharpened, not answered**: from "does the
chip go red" to "**what value was actually applied**". That is the only form of it a device can
settle, and per CAP-08 it is the only form worth asking — an unresolved operand applies a
silent, unrequested 50%.

**Setup.** Import
`.planning/spikes/010-coercion-at-a-direct-set-parameter/PROSOCHE Coercion Probe Breadcrumbs.shortcut`.
This is the **Breadcrumbs** variant, built for a device session where a human can tap; the
silent variant exists for simulators and is not what you want here. Its legs run **C → A → B →
D** so the device read happens before either write and the restore leg puts back the true
original rather than the probe's own test value. `assert_probe_shape.py` asserts the two
variants are identical on all three Set Brightness sites.

**Sequence.** Run the probe and step through its breadcrumb alerts. Leg **A** is the coerced
chain — a `gettext`-fed named variable feeding `WFBrightness` with the coercion first in
`Aggrandizements`, the exact shape `restore_managed_settings()` emits. Leg **B** is the
identical chain **deliberately bare**, with no coercion.

**Expected observation.** Read the *brightness slider*, not the alert text:

- Leg **A** (coerced) drives brightness to **0.42** — visibly a little under half.
- Leg **B** (uncoerced control) drives brightness to **0.66** — visibly about two-thirds.

**A result of ~50% on either leg is the CAP-08 silent default and means the operand did not
resolve.** That is a failing observation, not a passing one, and it is invisible in the alert
text. **Record the observed slider position for each leg**, not "no error".

**If leg A does not apply 0.42:** that is the fresh-donor trigger from `09-RESEARCH.md`
("Recommended verification path"). **Do not guess a second `CoercionItemClass`** — build a
donor on device with a variable-fed Set Brightness and decrypt it. No replacement class appears
anywhere in this project and `assert_probe_shape.py` fails the build if one ever does.

**Failure evidence to capture.** A screenshot of the brightness slider immediately after each
leg, the breadcrumb letter showing at that moment, and the full text of any error dialog.

outcome (leg A, coerced — observed brightness):

outcome (leg B, uncoerced control — observed brightness):

---

### 2. A real capture is VISIBLE in `state.json`

**This is the single most valuable test in this instrument.** It is the direct test for the
persistence defect and **the one that would have caught it**. Everything from Test 4 onward is
meaningless if this fails, because every restore path reads the value this test looks for.

**Setup.** Complete the Setup section. No Pressure accumulation needed — `Test a Circle` drives
the primitive directly and never writes Pressure. Have the Files app ready to inspect
`state.json` **without leaving PROSOCHĒ running**.

**Sequence.** Run the shortcut manually → `Test a Circle` → the Circle your sequence maps to
**Dimming** (Setup step 7). Let it fire. **Then, before doing anything else**, open Files →
iCloud Drive → Shortcuts → PROSOCHE → `state.json` and read
`settings_snapshot.brightness.original_value`. Repeat for **Silence** and read
`settings_snapshot.volume.original_value`.

**Expected observation.**

- The screen visibly dims (and media volume visibly drops, on the Silence run).
- `settings_snapshot.brightness.original_value` holds a **real number** — a positive value
  matching the brightness you recorded by hand in Setup step 6, expressed as a fraction (a
  60% slider reads roughly `0.6`).
- Specifically **not** `"null"`, not `""`, not `0`, and not a value that looks like the *new*
  dim target rather than the *old* original.
- The same for `settings_snapshot.volume.original_value` after the Silence run.

**Reading `"null"` here is the pre-fix defect reproduced**, and means either the wrong build is
installed (go back to the re-import precondition) or the fix did not take. It is a **failing**
result, not an inconclusive one.

**Note on precision.** Record the value **exactly as written in the file**, digits and all. That
a captured brightness round-trips through `state.json` without precision loss is a `backstop`
truth from plan 16-01 that only hardware can settle, and it is settled by reading this number
carefully rather than by glancing at it.

**Failure evidence to capture.** A screenshot of the `settings_snapshot` block in Quick Look,
the hand-recorded original from Setup step 6 beside it, and the Circle and sequence used.

outcome (brightness capture value read from `state.json`):

outcome (volume capture value read from `state.json`):

---

### 3. The has-any-value guard correctly SKIPS the change when the read returns nothing

**Why this test exists.** The guard is this project's input validation over an absent or
untrusted `Get Device Details` reading, and it is the reason a failed read cannot become a
dark screen. Both gates are byte-identical to their pre-phase form — the container gate on the
whole snapshot dictionary (condition 100, has-any-value) and the numeric `> 0` gate on the
captured reading. **The property under test is a NON-event**: nothing happens, and that is the
pass.

**Setup.** Two reachable ways to exercise it; do whichever your device allows, and say which.

- **(a) The unrestored-snapshot path.** Run Dimming once so a snapshot exists in `state.json`
  and is **not** cleared (do not close the app). Then run `Test a Circle` → the Dimming Circle
  **again**. The container gate should see an existing snapshot and short-circuit.
- **(b) The failed-read path.** Only reachable if `Get Device Details → Current Brightness`
  returns nothing or a non-positive value on this hardware. If Test 2 showed a healthy read,
  path (b) may be unreachable — **say so and record it as not-exercised rather than as passed.**

**Expected observation.**

- **Path (a):** the second run changes **nothing**. Brightness stays where the first run left
  it — it is neither re-dimmed nor raised — and `settings_snapshot.brightness.original_value`
  is **unchanged**, still holding the *first* run's original. The second run must not overwrite
  it; overwriting is how the true original is lost forever.
- **Path (b):** an alert titled **`Dim`** reading *"Brightness could not be captured, so nothing
  was changed."* appears, and the brightness **does not move**. The parallel Silence alert says
  volume.

**Per CAP-08, verify the brightness DID NOT MOVE.** A silent 50% default would satisfy any
check phrased as "no error appeared" while doing exactly the thing this gate exists to prevent.

**Failure evidence to capture.** The `settings_snapshot` value before and after the second run,
side by side; a screenshot of any alert; the brightness slider position before and after.

outcome (path used — a / b / not exercised):

outcome (observation):

---

### 4. Full capture → apply → restore round trip, against the hand-recorded originals

**Why this is the phase's central claim.** CIRC-03, CIRC-05, SAFE-03. This is also `12-UAT.md`
Test 3 written from the other side — run it once and record the outcome in both files.

**Setup.** Complete the Setup section, **including step 6's hand-recorded numbers** — they are
the comparison and they must not come from the shortcut. Ensure `settings_snapshot` is clear
before starting (both leaves at the sentinel); if not, tap Emergency Restore first and note
that you did.

**Sequence.** Open a tracked app and let Pressure carry the run to the Circle your sequence maps
to Dimming, then **close the tracked app** so the CLOSE Personal Automation fires. Repeat for
Silence. Use the real automation path, not `Test a Circle` — a restore that works only from the
manual menu has not been proven where it matters.

**Expected observation.**

1. The primitive fires; the screen dims (or volume drops).
2. On CLOSE, brightness returns to **exactly** the value recorded by hand in Setup step 6 —
   compared against your written note, not against your memory of how the screen looked.
3. `settings_snapshot.brightness.original_value` is **cleared back to the sentinel** after the
   restore, while the `settings_snapshot` container and both group sub-dictionaries **survive**.
   A missing container is a different and worse defect: a later dotted read against a string
   parent is a hard error in this runtime.
4. The CLOSE confirmation notification appears **after** the restore.
5. The same for Media volume, which must never be restored to *above* its saved original.

**If brightness or volume does NOT return:** restore it by hand through iOS Settings, record the
failure with its evidence, and **stop** — do not push through to Tests 6–10, which all assume
the happy path works.

**Failure evidence to capture.** The hand-recorded original, the post-restore reading, the
`settings_snapshot` block before and after CLOSE, and the sequence and Circle used.

outcome (brightness — hand-recorded original vs. post-restore reading):

outcome (volume — hand-recorded original vs. post-restore reading):

outcome (snapshot cleared, container intact — yes / no):

---

### 5. What `WFBrightness = 0` actually looks like on this screen

**Why this is an OBSERVATION, not a pass/fail.** Decision **D-01** moved
`safety.brightness_floor` and `safety.dim_target` from `0.10`/`0.12` to **`0`/`0`**, on the
basis of a user's on-device report that iOS renders its practical minimum as *dim, not black*.
**That report is unrepeated, and this phase could not itself produce the evidence.** This test
is the device input to a decision already taken — record what you see, not what the decision
predicts.

Note the D-01 consequence recorded above: with `dim_target = 0` the already-dim short-circuit
is unreachable, so **every** dimming run on this build drives brightness to `0`. You will not
have to contrive this observation; Test 2 will already have produced it.

**Setup.** Complete the Setup section. Do this in a **normally lit room, not in the dark** — a
screen that is readable in darkness may be unusable in daylight, and the safety property is
about a phone someone is actually holding.

**Sequence.** Run `Test a Circle` → the Dimming Circle. Look at the screen. Then attempt an
ordinary task on it: read a notification, find the Settings app, tap a button.

**What to record — all four, separately:**

- Is the screen **dim but legible**, or effectively **black**?
- Could you **navigate to iOS Settings** on it unaided?
- Does it differ in a **lit room versus a dark one**?
- Does Control Centre's slider show `0`, or does iOS clamp it to some minimum above zero?

**How this feeds back.** If the screen is legible, D-01 is corroborated and the safety property
stands where the phase put it — on capture-and-restore, not on floor avoidance. **If it is
effectively black and unusable, that is a real finding against a LOCKED decision**: record it in
full and surface it to the user rather than adjusting anything yourself. D-01 is the user's
decision to revisit, and the correct response is evidence, not a unilateral floor.

**Failure evidence to capture.** A photograph of the screen taken with another device — a
screenshot cannot show brightness. Note the ambient lighting.

outcome (legible or black; navigable; lighting; slider reading):

---

### 6. App force-quit mid-session, before CLOSE fires

**Why.** SAFE-03. Force-quitting the tracked app may prevent the CLOSE automation from firing at
all, leaving a populated `settings_snapshot` with no CLOSE to consume it. Before this phase the
snapshot was never on disk, so this trial was unreachable in any meaningful sense; now the
snapshot persists, which is exactly what makes recovery possible **and** what makes this trial
worth running.

**Setup.** Clean `settings_snapshot`. Hand-recorded originals to hand.

**Sequence.** Open the tracked app, let Pressure reach the Dimming Circle, let the screen dim,
then **force-quit the app** (swipe up from the app switcher) **before** closing it normally.

**Expected observation.** State the honest expectation: **the device is likely to stay dim**,
because CLOSE is what restores and force-quitting may prevent it firing. What must be true is
that the state is **recoverable**, not that it self-heals:

- `settings_snapshot.brightness.original_value` still holds the real original in `state.json` —
  **this is the property the phase delivered**, and it is what makes Test 11's recovery possible.
- No error dialog is stranded on screen.
- Nothing in `state.json` is corrupted; the container and both sub-dictionaries survive.

**Then go to Test 11 and tap Emergency Restore for this failure mode before continuing.** Do not
run Test 7 on a phone still dim from Test 6 — you would be unable to tell which trial left it
that way.

**Failure evidence to capture.** The `settings_snapshot` block immediately after the force-quit,
the brightness reading, and whether the CLOSE confirmation notification appeared at all.

outcome:

---

### 7. Device restart mid-session, before CLOSE fires

**Why.** SAFE-03, and the harshest persistence test in the file: a restart destroys every
in-memory dictionary, so **only what reached disk survives**. This is the trial that most
directly distinguishes this build from its predecessor.

**Setup.** Clean `settings_snapshot` (tap Emergency Restore if Test 6 left one). Hand-recorded
originals to hand. **Know how to reach Settings on a dark screen before you begin** — you may
have to do it after the restart.

**Sequence.** Open the tracked app, let Pressure reach the Dimming Circle, let the screen dim,
then **restart the device** (power off and on) before closing the app.

**Expected observation.**

- After the restart, `settings_snapshot.brightness.original_value` **still holds the real
  original**. It was written to disk before the device was changed, so a restart cannot lose it.
  **Reading `"null"` here means the persistence fix did not survive a restart** — a major
  finding, and precisely what this test is for.
- Brightness after restart: record it. iOS may or may not restore brightness itself across a
  restart; that is a device behaviour, not a product behaviour, and it must not be credited to
  PROSOCHĒ. Record what iOS did and what the file said, separately.
- The stale `active_session` from the interrupted run does not prevent a later run from
  operating.

**Then go to Test 11.**

**Failure evidence to capture.** The `settings_snapshot` block after restart, the brightness
reading after restart, and the hand-recorded original.

outcome (snapshot survived restart — value read):

outcome (brightness after restart):

---

### 8. CLOSE never fires at all

**Why.** SAFE-03. Distinct from Test 6: there the app was killed, here CLOSE simply never
arrives — the automation is disabled, mis-pointed, or the app was never "closed" in the sense
iOS recognises. This is the most likely *silent* failure in ordinary use, because nothing
visibly goes wrong at the moment it happens.

**Setup.** Clean `settings_snapshot`. Then **disable the `App Is Closed` Personal Automation**
(Shortcuts → Automation → toggle it off). Record that you did, and **remember to re-enable it
afterwards** — every later test needs it.

**Sequence.** Open the tracked app, reach the Dimming Circle, let the screen dim, then leave the
app normally. Wait a few minutes.

**Expected observation.**

- The screen **stays dim** — there is no other restore trigger on this path, and the honest
  expectation is that nothing recovers it automatically.
- `settings_snapshot.brightness.original_value` still holds the real original, so **Emergency
  Restore can recover it** (Test 11). That recoverability is the whole safety argument for this
  failure mode.
- `active_session` remains populated with no owner to close it. Record whether a subsequent OPEN
  is disturbed by it.

**Re-enable the `App Is Closed` automation before continuing. Then go to Test 11.**

**Failure evidence to capture.** The `settings_snapshot` and `active_session` blocks, and the
brightness reading.

outcome:

---

### 9. Two overlapping sessions

**Why, and what the code predicts.** `09-UAT.md`'s first-principles write-up (a) — carried
forward as *reasoning*, never as a result — traces it: `active_session` is a single slot, not a
stack; SESS-03's race protocol means only the winning (last) OPEN's CLOSE ever reaches the
restore, since a superseded CLOSE reloads state, finds it no longer owns `active_session`, and
takes a Nothing-only branch; and `dimming()`/`silence()` no-op when an unrestored snapshot
already exists. So session B's Dimming call should be a **complete no-op**, and B's CLOSE
should restore **session A's** captured original — the one true original that exists. **No
ownership check of any kind is involved**, which is exactly why decision D-02 could remove
`changed_at` and `changed_by_session_id` outright.

**This test is where that reasoning meets hardware for the first time.** It is a prediction to
test, not a conclusion to confirm — and it is also the DEV-06 cross-check `09-UAT.md` carried as
its Test 12, folded in here rather than kept as a separate numbered test, because it is the same
observation read for a different purpose.

**Setup.** Clean `settings_snapshot`. Hand-recorded originals to hand. Two tracked apps, or one
tracked app opened twice in quick succession.

**Sequence.** Open tracked app **A**, let it reach the Dimming Circle and dim. **Before closing
A**, open tracked app **B** (or re-open A) so a second session starts. Then close **B**.

**Expected observation.**

- B's Dimming call is a **no-op**: it neither re-captures nor re-dims, and
  `settings_snapshot.brightness.original_value` **still holds A's original, unchanged**.
  Overwriting it with the already-dimmed value would destroy the true original permanently —
  this is the most consequential thing to check in the whole test.
- B's CLOSE restores brightness to **A's** hand-recorded original.
- The snapshot clears afterwards; the container survives.

**Record explicitly whether the no-ownership-check design HELD or a gap was found.** That
sentence is the DEV-06 cross-check, and D-02's removal of the two identity leaves rests on it.

**Failure evidence to capture.** The `settings_snapshot` value at three moments — after A dims,
after B opens, after B closes — plus `active_session` at each, and the brightness at each.

outcome (did B's dimming no-op, leaving A's original intact — yes / no):

outcome (did B's CLOSE restore A's original):

outcome (DEV-06 prediction — held / gap found, stated plainly):

---

### 10. The compound trial — two overlapping sessions PLUS a force-quit of the winner

**This is its own numbered test and not an appendix to Test 9, deliberately.** Testing the four
failure modes separately never reaches this state, and **this is the state Emergency Restore
exists for**: a populated `settings_snapshot` whose only possible restorer has been destroyed.
Test 9 leaves a valid owner; Test 6 leaves a single unowned session. Only the compound of the
two produces a snapshot that *no* CLOSE can ever reach — and a compound failure mode demoted to
a footnote under a simpler test is exactly how that state goes untested forever.

**Setup.** Clean `settings_snapshot`. Hand-recorded originals to hand. Both automations enabled.

**Sequence.**

1. Open tracked app **A**; let it reach the Dimming Circle and dim.
2. **Before closing A**, open tracked app **B** so B becomes the winning session — reproducing
   Test 9's overlap exactly.
3. **Force-quit B** (app switcher, swipe up) before B's CLOSE fires.

Now: A's CLOSE is superseded and will take the Nothing-only branch even if it fires; B's CLOSE
never fires at all. **No CLOSE can reach the snapshot.**

**Expected observation.**

- The device **stays dim**. Expected, and not a failure of this test.
- `settings_snapshot.brightness.original_value` still holds **A's real original** on disk —
  intact, un-overwritten, and reachable by Emergency Restore.
- `active_session` holds B's stranded session; `state.json` is otherwise uncorrupted.
- No error dialog is stranded on screen.

**The pass condition is not that the device recovers on its own — it is that the information
needed to recover it survived.** Then run Test 11 against **this** state specifically; it is the
hardest recovery in the file and the one Emergency Restore was built for.

**Failure evidence to capture.** The full `settings_snapshot` and `active_session` blocks, the
brightness reading, the order and timing of every step, and which app was A and which was B.

outcome (snapshot intact and holding A's original — value read):

outcome (Emergency Restore recovered from this compound state — see Test 11):

---

### 11. Emergency Restore after EVERY failure mode above

**⚠ Emergency Restore has never been tapped on a device. Not once, in this project's history.**
It is a safety mechanism carrying zero behavioural evidence, and until the build under test it
was **structurally incapable** of working — it reads the same `state.json` as CLOSE, found the
same cleared sentinel, failed the same numeric `> 0` gate, and skipped. **This test is the first
evidence that SAFE-05 is real.**

**Setup.** Run this test **once after each of Tests 6, 7, 8 and 10**, before starting the next
one. Do not batch them to the end: recovering from four accumulated failure modes at once proves
only that the last one recovered, and leaves you unable to say which mode Emergency Restore
handles.

**Sequence.** Run the shortcut manually → **`Emergency Restore`** (the ninth item on the manual
menu). It is also reachable from the `Frozen is active` cool-down redirect, which is deliberate —
a user inside Ice must still be able to reach it.

**Expected observation, per trial.**

- Brightness returns to the value recorded by hand in Setup step 6 — and, per CAP-08, **verify
  the slider actually moved to that value**, never merely that no error appeared.
- Media volume likewise, never restored above its saved original.
- `settings_snapshot` clears to the sentinel; the container and both sub-dictionaries survive.
- If nothing was captured for that trial, Emergency Restore completes with **no error and no
  state corruption** — a clean no-op is a pass.

**Record a separate outcome per failure mode.** "Emergency Restore works" is not a usable
result; which state it recovered from is the entire content of the finding. **Test 10's row is
the important one** — that is the state no CLOSE can reach.

**Failure evidence to capture.** Per trial: the `settings_snapshot` before and after, the
brightness and volume before and after, and the hand-recorded originals.

outcome (after Test 6 — force-quit):

outcome (after Test 7 — restart):

outcome (after Test 8 — CLOSE never fires):

outcome (after Test 10 — the compound overlap + force-quit state):

outcome (Emergency Restore on a device with nothing captured — clean no-op — yes / no):

---

### 12. The removed snapshot leaves are absent from a fresh bootstrap, and nothing broke

**Why.** Decision **D-02** removed `settings_snapshot.<group>.changed_at` and
`.changed_by_session_id` — 44 writes per fork, **zero** readers. Removal is safe *only* because
nothing reads them: a dotted read of a missing segment is a **hard error** in this runtime, not
a soft miss, so a surviving reader would be a crash rather than a degradation. Static proof is
complete and permanent (`verify_no_removed_snapshot_leaf_reads`, both surfaces, demonstrated to
fire on injected reads). **What only a device settles is the file on the phone.**

**Setup.** This test needs the genuinely fresh `state.json` created in Setup step 3–4. If you
have overwritten it, delete and re-bootstrap before running this.

**Sequence.** Open `state.json` and read the whole `settings_snapshot` block. Then run one full
Dimming cycle (Test 4's path) and read it again.

**Expected observation.**

- The bootstrap seed reads exactly:

  ```
  "settings_snapshot": {
    "brightness": {"original_value": "null"},
    "volume": {"original_value": "null"}
  }
  ```

  **One leaf per group.** No `changed_at`, no `changed_by_session_id`. The container and both
  group sub-dictionaries **must** be present — their removal, unlike the leaves', would
  reintroduce a hard-error class.
- A full capture/restore cycle completes normally with the smaller shape. Nothing errors, and
  the restore in Test 4 worked — which it did, or you did not get here.

**The upgrade case, which is the device half of D-02's `backstop` truth.** If this phone holds
a `state.json` seeded by an **older** build, it will still carry the two removed leaves. The
structural reasoning is that they persist harmlessly and no run reads them, because the removal
deletes writes and shrinks the seed while adding no read and changing no gate — so an older,
larger file is a strict superset of what the new build touches, and **no migration is needed**.
**That reasoning is a claim about a real file on a real phone and only this session can confirm
it.** If you have such a device, run one Dimming cycle against the *old* file before deleting
it, and record what happened. If you do not, record that the upgrade case was **not exercised**
— do not infer it.

**The Aware fork, in the same breath.** Import
`PROSOCHĒ — Nine Circles — Aware.shortcut` at the header's digest and run one Dimming cycle.
Both forks are generated from one pass and measure identically, so this is a low-expectation
regression check — but `tools/build_sentient.py`'s fork step is the only place a correct Core
artifact could become an incorrect Aware one. Apple Intelligence is not required.

**Failure evidence to capture.** The `settings_snapshot` block from the fresh bootstrap, the
same block after one cycle, and the Aware fork's reading.

outcome (fresh-bootstrap seed shape — one leaf per group — yes / no):

outcome (upgrade case — old file with the removed leaves — exercised / not exercised):

outcome (Aware fork, one Dimming cycle):

---

## Results

| # | Test | Outcome |
|---|---|---|
| 1 | Coerced operand's applied value, via the spike-010 Breadcrumbs probe | |
| 2 | A real capture is visible in `state.json` | |
| 3 | The has-any-value guard correctly skips the change | |
| 4 | Full capture → apply → restore round trip | |
| 5 | What `WFBrightness = 0` looks like on this screen | |
| 6 | App force-quit mid-session | |
| 7 | Device restart mid-session | |
| 8 | CLOSE never fires at all | |
| 9 | Two overlapping sessions | |
| 10 | Compound — overlap plus force-quit of the winner | |
| 11 | Emergency Restore after every failure mode | |
| 12 | Removed snapshot leaves absent from a fresh bootstrap | |

## Summary

total: 12 (Tests 1, 2, 4, 7, 9, 10, 11 and 12 carry multiple sub-observations)
passed: 0
issues: 0
skipped: 0
blocked: 12

## Reachability probe — MEASURED at execution time, 2026-08-18

```
$ xcrun devicectl list devices
Name     Hostname                  Identifier                             State         Model
------   -----------------------   ------------------------------------   -----------   --------------------------
dougal   dougal.coredevice.local   8E45671C-9E4D-54C9-AC19-2EB65747337E   unavailable   iPhone 15 Pro (iPhone16,1)

$ xcrun devicectl list devices --json-output <path>    # read from the JSON, not the table
tunnelState:   unavailable
pairingState:  paired
transportType: none
osVersionNumber: 26.6
productType:   iPhone16,1
udid:          00008130-00094480229A001C
```

**Read `tunnelState` from the JSON, never the `State` column from the table.** On 2026-08-17 the
table read `available (paired)` while `tunnelState` was `disconnected` — the column is not the
tunnel. Today both agree, but the rule stands because the column has already been misleading
once in this phase.

**Verdict: BLOCKED — a paired device exists, but there is no live tunnel and no active
transport.**

The blocked reason is **"paired device present, `tunnelState: unavailable`, `transportType:
none`; no live session to drive"** — *not* "no devices found". That older wording appears in
`16-RESEARCH.md` and in a superseded block of `16-CONTEXT.md`; it was true at the start of the
2026-08-17 session and is false now. Recording it would be recording something false, which this
project forbids exactly as firmly as it forbids a false pass. The reason has also moved *again*
since planning: 2026-08-17 measured `tunnelState: disconnected` with `transport: wired`; today
the transport is gone entirely.

Two facts worth carrying forward:

- **`iPhone16,1` is Apple-Intelligence-capable**, so this hardware can exercise the **Aware**
  fork when a session is arranged. The device split in `## Constraints` is satisfied.
- **iOS 26.6 is inside the declared `iOS 26.x` target**, so an observation on it is
  same-major-version evidence rather than an extrapolation.

Substantively DIST-03 would block an autonomous run even with a live tunnel: Personal
Automations are user-created on the device and cannot be exercised anywhere else, at any effort.

## Standing note — what may not be substituted for a device observation

**Every `outcome:` field above stays blank.** This is the recorded precedent of `10-UAT.md`
(Phase 10), `12-UAT.md` (Phase 12) and `13-UAT.md` (Phase 13), all blocked on DIST-03 with every
outcome left blank. It is not a failure and not an oversight — it is this project's standing,
deliberate policy that **a fabricated pass is worse than a blank**.

**Do not substitute a simulator run, a Mac import, a static checker, or any inference from the
decrypted artifact for a device observation.** Both signed containers were decrypted at commit
`04f3612` and their recovered action lists are byte-identical to the built sources (Core 4302
actions, Aware 4370). **That is structural proof that the right bytes shipped and nothing more.**
It does not observe whether a screen un-dims. The simulator cannot close the gap either: it
cannot execute `Set Brightness` at all, it reads brightness as `0`, and it lacks
`com.apple.mobilenotes` — measured, plan 16-02.

**`09-UAT.md`'s single recorded pass does NOT carry forward.** It is superseded by this file.
Its Test 1 passed a chip inspection that plan 16-02 has since shown carries **no information**
at a direct Set-action parameter, it has no build-identity header, and it names the pre-rename
forks. See the superseded banner on that file.

**This UAT is re-run unchanged when a device becomes reachable.** Do not rewrite the tests to
fit whatever device eventually connects. Run them exactly as written against the build named in
the header, or against a freshly signed rebuild — provided both SHA-256 values in the header are
updated from `MANIFEST.md` first, and the re-import precondition is applied to it too.

**If this file is still blocked when Phase 19 runs, fold it into Phase 19's device UAT rather
than dropping it.** Tests 2, 4 and 11 are the assertions that convert this phase from
structurally-proven to actually-working, and Test 10 is the one that must not be demoted back
into a footnote.

DIST-03 stays **unchecked** in `.planning/REQUIREMENTS.md` until every test above has a recorded
outcome from a real iPhone.

## Verdict

_Blank. Filled in only after the twelve tests above resolve on a real device._

**Required shape when it is filled in** — one of exactly two judgements, each citing the test
numbers that support it:

- **DEMONSTRATED SAFE** — capture, apply and restore close as a loop (Tests 2, 4), the guard
  correctly skips rather than guessing (Test 3), every failure mode leaves a recoverable state
  (Tests 6, 7, 8, 9, 10), and Emergency Restore recovers from each one including the compound
  case (Test 11). State per claim which test number carries it.
- **RETIRED** — the loop does not close on hardware, and Dimming and/or Silence degrade to a
  non-stateful variant rather than making an unrestorable change. Canonical strategy §21's rule
  is unambiguous here: *do not perform a stateful change unless the original can be reliably
  captured and restored.* Name the test number that forced the retirement, and what the
  replacement primitive is.

A verdict that cites no test numbers is not a verdict. A verdict recorded without a device
session is a fabrication and this file exists partly to make that hard to do by accident.
