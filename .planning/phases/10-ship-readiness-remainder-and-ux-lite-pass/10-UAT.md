---
status: blocked
phase: 10-ship-readiness-remainder-and-ux-lite-pass
source: [10-01-SUMMARY.md, 10-02-SUMMARY.md, 10-03-SUMMARY.md, 10-04-SUMMARY.md]
blocked_on: DIST-03
started: 2026-08-17
updated: 2026-08-17
---

# Phase 10 — Device UAT

## Header — what is under test

| Field | Value |
|---|---|
| Phase | `10-ship-readiness-remainder-and-ux-lite-pass` |
| Written | 2026-08-17 |
| Fork under test | **Dumb only.** Sentient is not exercised by this file. |
| Artifact | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` |
| Bytes | 193,498 |
| SHA-256 | `47957dbf429bd2d5671b69d87d8510b08abf70bbe1cfca8975a192c96bcb6324` |
| Manifest row | `artifacts/shortcuts/MANIFEST.md`, row **Dumb signed** — both values above are copied from it and `python3 docs/manifest_check.py` proves that row against disk |
| Device requirement | An iPhone running **iOS 26.x**, with both Personal Automations already built by hand and both pointing at the Dumb fork **by its display name** `PROSOCHĒ — Nine Circles — Dumb` |
| Apple Intelligence | **Not required.** No test in this file uses `Use Model`; the Dumb fork contains no model call. No test here needs an iPhone 15 Pro or later. |

**Every test in this file is blocked on DIST-03 while no device is connected.**
`xcrun devicectl list devices` reports `No devices found.` as of 2026-08-17. That is the same
blocker that has held DIST-03 open since Phase 8 and that stalled
`.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md`
at one of twelve. Until a device is in hand, every `outcome:` field below stays blank.

### The two Personal Automations, by name

These are user-built on the device and are **not** in the repository. Both run the same single
Shortcut and are distinguished only by the literal text they pass as Shortcut Input.

| Name used in this file | iOS trigger | Shortcut Input it must pass | Run After Confirmation |
|---|---|---|---|
| **Automation A** | App Is Opened, on the tracked app(s) | `OPEN` | Off (run immediately) |
| **Automation B** | App Is Closed, on the same app(s) | `CLOSE` | Off (run immediately) |

Anything other than those two exact literals falls through the router to the manual control
menu **by design** (DEV-02). Test 8 exists to diagnose exactly that.

### Where to read state

`state.json` lives at **Files → iCloud Drive → Shortcuts → PROSOCHE → state.json**
(the Shortcut writes it with `WFFileDestinationPath = "PROSOCHE/state.json"`). Open it in Files
with a long-press → Quick Look, or share it to any text viewer. Several tests below name exact
fields in it, because the `Status` alert does **not** show `heat`, `opens_today` or
`active_session` — it shows Fork, Profile, Sequence, Voice, Circle, Pressure and Cool-down only.

The Control Room Note is an Apple Note named **`PROSOCHĒ — Control Room`**.

### The manual control menu, in shipped order

Running the Shortcut by hand (Shortcuts app → tap the tile) reaches the manual arm. Its ten
items, in the order they appear:

`Status` · `Open Control Room` · `Sync My Profile` · `Change Profile` · `Change Sequence` ·
`Toggle Voice` · `Test a Circle` · `Reset Today` · `Emergency Restore` · `Setup Check`

### The arithmetic these tests predict against

Read from the built artifact's Config literal at this exact build, so a tester can predict a
number before they observe it rather than after:

- `pressure = heat + gravity`
- `gravity = floor(opens_today / 6)`, capped at 5
- `heat` per genuine open: `−1 per full 600 s elapsed since last_close_at` (decay), then
  `+1` (`heat.open_base`), then **exclusively** `+2` if the reopen came under 120 s since the
  last close, else `+1` if under 600 s, else nothing. Floor 0, cap 30.
- Circle = the highest 1-based index in the active profile's threshold array that `pressure`
  reaches. Nothing reached ⇒ **Circle 0, the silent band**.

| Profile | Thresholds (Circle 1 … 9) | Circle 1 entry |
|---|---|---|
| Paradise | 4, 7, 10, 13, 16, 19, 22, 25, 28 | pressure ≥ 4 |
| **Limbo (default)** | **3, 5, 7, 9, 11, 13, 16, 19, 22** | **pressure ≥ 3** |
| Inferno | 2, 3, 5, 7, 9, 11, 13, 15, 17 | pressure ≥ 2 |

Default sequence is **Classic**: Circle 1 `Knock`, 2 `Ash`, 3 `Silence`, 4 `Confession`,
5 `Dimming`, 6 `Exile`, 7 `Mirror`, 8 `Voice`, 9 `Ice`.

> **Known open defect, so it is not reported as a UAT failure:** Circle 8 (`Voice` under
> Classic) dispatches nothing. `docs/sequence_dispatch_check.py` reports it as an orphan on
> every run. It is owned by
> `.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md`. No test below fires
> Circle 8.

### Shipped-surface inventory (from `docs/router_ui_census.py` at this build)

A device observation that contradicts a row here is a **real finding**, not a measurement error.

| Surface | OPEN | CLOSE | MANUAL |
|---|---:|---:|---:|
| `choosefrommenu` | 10 | **0** | 13 |
| `ask` | 6 | **0** | 18 |
| `alert` | 8 | 1 | 56 |
| `notification` | **0** | 1 | 0 |
| `shownote` | 0 | 0 | 1 (gated) |

---

## Step 0 — Re-import the artifact (setup, not a test)

**This is not numbered as a test and has no outcome field.** It must happen before Test 1,
otherwise every observation below describes the *previous* build rather than this one.

**Setup.** Get `PROSOCHĒ — Nine Circles — Dumb.shortcut` (193,498 bytes,
`47957dbf…6324`) onto the iPhone — AirDrop from the build Mac, or iCloud Drive.

**Sequence.**
1. Tap the file on the iPhone. Shortcuts offers to add it.
2. Confirm the incoming shortcut's name reads exactly `PROSOCHĒ — Nine Circles — Dumb` and
   that it **replaces** the existing library entry rather than creating a second one.
3. Open **Settings → Shortcuts → Automations** (or the Shortcuts app's Automation tab) and
   confirm both Automation A and Automation B still point at that entry.

**Expected observation.** Exactly **one** library entry named `PROSOCHĒ — Nine Circles — Dumb`,
and both automations still bound to it.

**If a second entry appears**, the cause is the filename, not the build: a signed `.shortcut`
carries **no display name inside it** (measured in 10-04 — the signer strips `WFWorkflowName`,
and the AEA1 auth-data plist holds only `SigningCertificateChain`). Delete the duplicate,
rename the file to the exact display name with no suffix, and re-import before continuing.

**`state.json` and the Control Room Note survive a re-import.** Neither lives inside the
shortcut — `state.json` is a file in the Shortcuts iCloud folder and the Note is an Apple Note.
No test below needs a fresh install, and no accumulated behavioural state is lost by this step.

---

## Tests

Ten tests. Every `outcome:` starts blank and stays blank unless a human observed it on a real
iPhone.

---

### 1. Silent band — first open of a behavioural day

The phase's headline claim, and the single most important test in this file.

**Setup.**
1. Run the Shortcut by hand → `Reset Today`. This zeroes `opens_today` and `gravity`.
2. Run it by hand again → `Status`. Note the **Profile** and the **Pressure** it reports.
3. **`Reset Today` does not zero `heat`.** Heat only decays, at −1 per full 10 minutes since
   the last close. Open `state.json` and read `heat`. Under the default **Limbo** profile this
   test is only meaningful when `heat ≤ 1` at this point, so that the open below lands at
   `pressure ≤ 2`, under Limbo's Circle-1 entry of 3. If `heat` is higher, leave the device
   alone for `10 × (heat − 1)` minutes and re-read, or record the actual starting `heat` and
   adjust the predicted pressure accordingly rather than skipping the test.
4. Confirm `cooldown_until` in `state.json` is `null`. A live cool-down short-circuits the OPEN
   pipeline before any Heat arithmetic and would make this test measure nothing.

**Sequence.** Open one tracked app, once, from the Home Screen. Do not touch anything else.
Wait five seconds. Close it. Then run the Shortcut by hand → `Status`.

**Expected observation.** Two halves, both required:

- **On screen, at the moment of opening: nothing at all.** No notification banner, no
  `Leaving / Continue` menu, no alert, no dimming, no sound, no spoken line. The app opens as
  if PROSOCHĒ were not installed. The census above says the OPEN arm carries zero
  notifications, and the `Leaving / Continue` menu is enclosed by a `Circle Next > 0`
  conditional, so at Circle 0 no surface should fire.
- **In the record, everything moved.** `Status` reports
  `Circle (0 means the silent band: recorded, nothing shown): 0` and a Pressure of `1`
  (assuming `heat` was 0 at step 3). `state.json` shows `heat` **1**, `gravity` **0**,
  `pressure` **1**, `circle` **0**, `opens_today` incremented by 1, `last_open_at` a fresh
  epoch, and `active_session` a **live object** with an `id`, a `started_at` and
  `declared_duration_seconds` — not `null`.

**Failure evidence to capture.**
- If *anything* appeared on screen: a screenshot or screen recording of it, plus the
  `state.json` contents immediately after.
- If nothing appeared but the record did not move: the full `state.json` before and after,
  plus the `Status` alert screenshot. A silent screen with an unmoved record is the opposite
  failure — the band suppressing accumulation as well as display — and is more serious than a
  visible surface.

outcome:

---

### 2. Band exit — how many opens does it take?

**Setup.** Continue directly from Test 1 without resetting. Note the current `Status` Pressure.

**Sequence.** Repeatedly open the tracked app, close it, and open it again. Keep the gaps
short — **under 120 seconds between close and next open**, which is where the `+2` exclusive
reopen bonus applies — and leave more than 2 seconds between events so the duplicate-OPEN
debounce does not swallow one. **Count every open.** Stop at the first open that produces a
visible surface.

**Expected observation.** For the first time, at the open where `pressure` reaches the active
profile's Circle-1 entry (**3** under Limbo), the run produces:

1. the `Leaving / Continue` menu, carrying the reworded prompt:

   > You just opened a tracked app. PROSOCHĒ is at Circle 1.
   >
   > Leaving: PROSOCHĒ suggests somewhere better to go and takes you there.
   > Continue: you go into the app, after this Circle's intervention.

2. and, after choosing `Continue`, the Circle-1 primitive — `Knock` under the Classic sequence.

Predicted from the arithmetic above, with `heat` 1 after Test 1 and each reopen under 120 s:
the **second** counted open should reach `heat` 4 and therefore `pressure` 4, crossing Limbo's
threshold of 3. If closes are slower than 600 s the rise is far shallower and it may take many
more.

**Record the actual number of opens.** That number is the on-device tuning signal the raised
thresholds exist to produce, and it is the point of this test — not the pass/fail.

**Failure evidence to capture.** If a surface appears *earlier* than the profile's threshold
predicts, screenshot the surface and capture `state.json` at that moment — that is the silent
band leaking. If no surface ever appears after fifteen counted opens, capture `state.json`
plus a `Status` screenshot; a `pressure` that is climbing with no surface is a broken gate, and
a `pressure` that is not climbing is a broken pipeline, and the `state.json` distinguishes them.

outcome:

---

### 3. No notification on OPEN

**Setup.** None beyond Tests 1 and 2 — this test is an observation made *across* them.

**Sequence.** Across every single open performed in Tests 1 and 2, watch the top of the screen
at the moment the app launches.

**Expected observation.** **No** Circle-and-pressure-and-heat notification banner at any point,
at any Circle, including the opens in Test 2 that do produce the `Leaving / Continue` menu. The
OPEN arm contains zero `notification` actions at this build. The CLOSE confirmation
notification is a **different** surface and still fires — see Test 8's setup, where it is the
expected behaviour.

**Failure evidence to capture.** A screenshot of the banner, with its full text legible, plus
which open number of Test 2 it appeared on.

outcome:

---

### 4. Control Room note-show — positive leg

The behavioural confirmation the cycle-16 `filter.notes` fix has never had. Its plist-level fix
is applied and Donor-8-matched; only the *effect* is unverified.

**Setup.** Ensure the Note `PROSOCHĒ — Control Room` exists — if Test 1's manual runs completed,
it does. Close the Notes app entirely (swipe it away in the app switcher) so its foreground
appearance is unambiguous.

**Sequence.** Shortcuts app → tap `PROSOCHĒ — Nine Circles — Dumb` → in the manual menu choose
**`Open Control Room`**.

**Expected observation.** The Notes app comes to the foreground showing **the Control Room Note
itself**, directly. **No note-list picker, no "Choose a Note" sheet, and no list of every note
in the account appears at any point** — not before the note, not after it.

**Failure evidence to capture.** A screenshot of the picker or list, showing enough of it to
tell a filtered list from an unfiltered one, plus a note of whether the correct note was
reachable from it.

outcome:

---

### 5. Control Room note-show — negative leg

The regression check for the new gate, and at least as important as Test 4.

**Setup.** Close the Notes app entirely before **each** of the three runs below, so that "the
Notes app opened" is unambiguous every time.

**Sequence.** Three separate runs of the Shortcut by hand, one menu item each:
1. → `Status`
2. → `Toggle Voice`
3. → `Reset Today`

**Expected observation.** On **none** of the three does the Notes app come to the foreground.
`Status` shows its alert and ends. `Toggle Voice` and `Reset Today` do their work and end —
both of these *do* append to the Control Room Note, and appending must happen **without**
opening Notes. The single `shownote` action in the artifact is gated on
`Manual Show Note Requested > 0`, which only `Open Control Room` sets.

**Failure evidence to capture.** Which of the three items launched Notes, a screenshot of what
Notes displayed, and whether it showed the note directly or a picker. Record all three
individually — one leaking item and three leaking items are different findings.

outcome:

---

### 6. Setup Check reports automation status truthfully

**Setup.** Note, before running, which of the two automations has actually fired on this device
since `state.json` was last created: `last_open_at` and `last_close_at` in `state.json` are the
ground truth this feature derives from.

**Sequence.** Run the Shortcut by hand → `Setup Check`.

**Expected observation.** One alert titled `Setup Check` reading:

> Automation A — App Is Opened, passing OPEN: {seen | not seen yet}
> Automation B — App Is Closed, passing CLOSE: {seen | not seen yet}
>
> This reports whether PROSOCHĒ has ever recorded a genuine open or an owning close. A close
> that a newer open superseded, or an open during a cool-down, records nothing — so a "not seen
> yet" verdict can be wrong, but a "seen" verdict never is.

Each verdict must match `state.json`: `seen` exactly when the corresponding epoch key is a
positive number, `not seen yet` when it is `null` or absent.

**Record which situation the device is actually in — do not force both.** If Automation B has
fired, the pair reads `seen` / `seen`; if only A has, it reads `seen` / `not seen yet`. Both are
valid results. Only report a failure if a verdict **contradicts** `state.json`.

**Failure evidence to capture.** A screenshot of the alert alongside the `last_open_at` and
`last_close_at` values from `state.json` read within the same minute.

outcome: **FAIL — the feature under test is not present on this build.** Device, 2026-08-18 08:07,
Core `b07497ba`, fresh install. `Setup Check` is present as the tenth and last item of the manual
menu and it does run. But the alert it produces is titled **`Panic Escape`**, not `Setup Check`,
and its entire body reads:

> *Panic Escape — The Note says ON and Panic Escape is already available. Nothing was changed.*

The run then ended; no second alert followed. **No automation status is reported at all** — neither
`Automation A — App Is Opened` nor `Automation B — App Is Closed`, and no `seen` / `not seen yet`
verdict for either.

This is not a wrong verdict that could be excused by the test's "only report a failure if a verdict
contradicts `state.json`" clause — there are **no verdicts to contradict anything**. The menu item
appears to be wired to a Panic-Escape availability check rather than to the automation-status
reporter this test specifies.

Worth noting the state context, since it makes the gap concrete: `state.json` on this device has
`last_open_at: null` and `last_close_at: null`, so the correct output would have been
`not seen yet` / `not seen yet` — a verdict the feature is currently incapable of producing.

---

### 7. The manual menu prompt explains itself

A judgement test. There is no non-device substitute for a human comprehension claim.

outcome: **PASS.** Device, 2026-08-18, observed on every manual run this session. The menu renders
with a full explanatory prompt above the items, in complete non-empty text:

> *This is PROSOCHĒ's manual control menu. You are here because the Shortcut was run by hand, or
> because an automation passed it something other than OPEN or CLOSE. If you did not mean to be
> here, choose Open Control Room — that Note has the setup instructions.*

It states what the screen is, both reasons the user might be seeing it, and gives an explicit
recovery route for the "I didn't mean to be here" case — which is the exact confusion recorded as
gap G-04-4b (the user encountering a bare `PROSOCHĒ` prompt and being unable to tell what it
signified). The shipped copy resolves that. Rendering is also evidence against the axis-2
empty-display-parameter defect on this action.

The full menu, in shipped order, was confirmed to be ten items: Status, Open Control Room, Sync My
Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today, Emergency
Restore, Setup Check.

**Setup.** None.

**Sequence.** Run the Shortcut by hand and **read the menu prompt before choosing anything.**

**Expected observation.** The prompt reads:

> This is PROSOCHĒ's manual control menu. You are here because the Shortcut was run by hand, or
> because an automation passed it something other than OPEN or CLOSE. If you did not mean to be
> here, choose Open Control Room — that Note has the setup instructions.

and it states all three things: that this is **manual control**; that it **also** opens when an
automation passed an unrecognised input; and that **`Open Control Room`** is where to go.

**Record the judgement, not just the string match:** would a person who did not expect to land
here understand from this prompt why they did? Write the answer in the outcome field in words.

**Failure evidence to capture.** A screenshot of the prompt as rendered (iOS may truncate a long
`WFMenuPrompt` — if it is cut off on the device, that is itself the finding), plus the reader's
own account of what they understood it to mean.

outcome:

---

### 8. No menu on CLOSE — and the diagnostic if there is one

**Setup.** Make sure a genuine session is open: open a tracked app so `active_session` in
`state.json` is non-null.

**Sequence.** Close the tracked app (swipe up to the Home Screen, or switch away) so Automation
B fires.

**Expected observation.** **No menu appears.** The CLOSE arm carries 0 `choosefrommenu` and 0
`ask` actions at this build. What *should* appear is one CLOSE notification and/or one alert —
that is the CLOSE confirmation and it is expected, not a failure.

**Failure evidence to capture — this is the whole point of the test.** If a menu *does* appear:

1. Screenshot the menu itself.
2. Then open **Automation B** in the Shortcuts app, tap into its `Run Shortcut` action, and
   **screenshot the input field verbatim** — including any trailing whitespace, any autocorrect
   substitution (a curly quote, a capitalised `Close`, an added period), and whether the field
   is empty.

**The CLOSE arm provably contains no menu.** A menu here therefore means the input did not match
the expected literal `CLOSE`, and the run fell through to manual control **by design**
(DEV-02 records that fall-through as a deliberate router tradeoff). The screenshot of the input
field is what settles it; nothing in the repository can.

outcome:

---

### 9. Dimming and Silence — capture and apply

**This is not a substitute for the Phase 9 UAT.**
`.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md`
holds twelve tests, of which only test 1 has ever passed. Those twelve own the failure-mode
trials — force-quit mid-session, device restart mid-session, CLOSE never firing, overlapping
sessions, the compound overlap-plus-force-quit trial, and the DEV-06 prediction cross-check —
and **they remain outstanding**. This test is here only because this phase re-signed the
artifact those tests were written against, so a smoke check that the path still behaves belongs
with this build. Passing this test says nothing about any of those twelve.

**Setup.**
1. Run `Emergency Restore` once first, to clear any stale `settings_snapshot` from an earlier
   run.
2. **Write down, by hand, the device's current brightness and current media volume** before
   firing anything. Do not infer them afterwards.
3. Confirm the active sequence is `Classic` via `Status`. Under Classic, Circle 3 is `Silence`
   and Circle 5 is `Dimming`.

**Sequence.** Run the Shortcut by hand → `Test a Circle` → `Circle 5` (Dimming). Observe.
Then run it by hand again → `Test a Circle` → `Circle 3` (Silence). Observe.

**Expected observation.**
- Dimming visibly lowers the screen brightness. The screen is **dim, not black** — it remains
  usable, per the BD-02 addendum. If the screen becomes genuinely unusable, that is a finding
  and the run stops here; go straight to Test 10 or restore through iOS Settings.
- Silence lowers **media** volume only. The ringer must be untouched — every volume write in
  the artifact targets `Media` (SAFE-02 / BD-03).
- `state.json`'s `settings_snapshot` now holds a **real, non-empty, numeric**
  `brightness.original_value` and `volume.original_value` matching the values written down at
  setup. An empty string, a `null`, or a wrongly typed value is a capture failure and is exactly
  what Phase 9's test 3 was written to catch.

**A manual `Test a Circle` creates no session, so no CLOSE will restore it.** The change is
deliberately left outstanding at the end of this test — Test 10 is the recovery, and the
session-driven capture→apply→restore round trip belongs to Phase 9 UAT test 5.

**Failure evidence to capture.** The hand-written before values; a photo or screenshot showing
the after state; and the `settings_snapshot` subtree from `state.json` copied verbatim.

outcome:

---

### 10. Emergency Restore — SAFE-05's behavioural confirmation

**Setup.** Come to this test **directly from Test 9**, with a Dimming or Silence change still
outstanding and `settings_snapshot` populated.

**Sequence.** Run the Shortcut by hand → `Emergency Restore`.

**Expected observation.**
- Brightness returns to the value written down at Test 9's setup.
- Media volume returns to the value written down at Test 9's setup.
- Any cool-down clears: `cooldown_until` in `state.json` reads `null` afterwards.

**If brightness or volume does NOT return:** restore it by hand through **iOS Settings →
Display & Brightness** and **Settings → Sounds & Haptics** (or the Control Centre sliders),
record the failure with its evidence, and **abandon the remaining tests** rather than
continuing. Do not push through a failed restore.

**Failure evidence to capture.** The hand-written before values, the observed after values, the
`settings_snapshot` and `cooldown_until` values from `state.json` after the run, and a plain
statement of whether the tester had to restore anything manually.

outcome:

---

## Results

| # | Test | Outcome |
|---|---|---|
| 1 | Silent band — first open of a behavioural day | |
| 2 | Band exit — how many opens does it take? | |
| 3 | No notification on OPEN | |
| 4 | Control Room note-show — positive leg | |
| 5 | Control Room note-show — negative leg | |
| 6 | Setup Check reports automation status truthfully | |
| 7 | The manual menu prompt explains itself | |
| 8 | No menu on CLOSE — and the diagnostic if there is one | |
| 9 | Dimming and Silence — capture and apply | |
| 10 | Emergency Restore — SAFE-05's behavioural confirmation | |

**Opens required to leave the silent band (Test 2):** _not measured_

## Summary

total: 10
passed: 0
issues: 0
skipped: 0
blocked: 10

## Standing note — what may not be substituted for a device observation

If no device is available, **record the blocker, leave every outcome blank, and stop.** That is
a legitimate, recorded outcome and is the precedent set by the 2026-08-16 breadcrumb-strip quick
task (`.planning/quick/260816-ukb-strip-the-open-bisect-debug-breadcrumb-s/`) and by Phase 9
Plan 02. It is not a failure.

**Do not substitute a Mac import, a simulator run, or any inference from the decrypted artifact
for a device observation.** The decrypted-artifact evidence produced by 10-04 — nine of nine
structural assertions re-asserted against both recovered plists — proves **structure, never
behaviour**, and the difference is the entire reason this file exists. The project's own record
is explicit that operator and operand type validity, and iOS's interactive-fallback behaviour
(the note picker in Test 4 is precisely such a case), are invisible to every file-level evidence
channel available: not the validator, not the ToolKit catalog, not AEA1 decryption.

DIST-03 stays **unchecked** in `.planning/REQUIREMENTS.md` until every test above has a recorded
outcome from a real iPhone.

## Verdict

_Blank. Filled in only after the ten tests above resolve on a real device._
