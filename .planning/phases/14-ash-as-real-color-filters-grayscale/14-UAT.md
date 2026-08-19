---
status: blocked
phase: 14-ash-as-real-color-filters-grayscale
source: [14-01-SUMMARY.md, 14-02-SUMMARY.md, 14-03-PLAN.md]
blocked_on: DIST-03
started: 2026-08-19
updated: 2026-08-19
---

# Phase 14 — Device UAT: does the phone actually go black and white, and does colour actually come back?

## ⚠ SAFETY PREAMBLE — read this before anything else on this page

**This instrument deliberately changes an accessibility setting on the phone it runs on.** It
turns iOS **Color Filters** on, which renders the whole screen in greyscale, and then asks
whether the product turns them off again.

1. **The screen will actually go black and white.** Circle `Black and White` emits
   `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` with
   `state = 1`. This is the real system toggle, not an in-app effect, and it persists across
   apps and across a reboot until something turns it off.
2. **If the phone is left in greyscale, iOS Settings is the only recovery.** Settings →
   Accessibility → Display & Text Size → **Color Filters** → off. **Learn that path before you
   start**, and know that Settings itself will also be in greyscale while you navigate it. The
   Accessibility Shortcut (triple-click the side button) can also be bound to Color Filters as
   a faster escape — bind it in Settings → Accessibility → Accessibility Shortcut **before**
   Test 1, not after.
3. **If you already use Color Filters yourself**, stop and read the next block. This build will
   switch your own setting off and cannot put it back.
4. **Test 1 force-quits the shortcut mid-intervention.** Do not begin if you need this phone for
   anything else in the next ~45 minutes.

### The accepted, undisclosed-to-nobody hazard — read this even if you are not testing today

**PROSOCHĒ cannot detect a pre-existing Color Filters setting, and does not try.** iOS exposes
**no** `Get*`/`Query*` intent for any accessibility setting across all 35 intents in
`AccessibilityUtilities.framework` — spike 005, tier-1 evidence. So the restore leg is
**unconditional**: it sets Color Filters *off*, whatever they were before. A user who runs Color
Filters deliberately for colour-blindness, migraine or low vision has their own accommodation
switched off every time they close a tracked app.

**This is accepted and backlogged, not mitigated.** What ships is the kill switch
`safety.ash_managed_color_filters` (Test 5) and a plain-language disclosure in the Control Room
Note. The undone half is
`.planning/todos/pending/2026-08-19-ash-void-circle-when-user-already-uses-grayscale.md`.

**If the tester is such a user**, record their pre-test Color Filters configuration by hand
before Test 1 and restore it by hand afterwards. The product will not do it for them.

---

## Header — what is under test

| Field | Value |
|---|---|
| Phase | `14-ash-as-real-color-filters-grayscale` |
| Written | 2026-08-19 |
| Commit artifacts were signed at | The **phase 14 plan 14-03** re-sign, 2026-08-19. Both forks were rebuilt after the Control Room Note disclosure landed and re-signed under their exact display names with no suffix. |
| Fork 1 | **Core** — `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — 235369 bytes — SHA-256 `c359bbe2f801f899ac21237000d589df5be9e7e575a825306c5333055a76658e` |
| Fork 2 | **Aware** — `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — 241805 bytes — SHA-256 `bd269b0cd3ae496811ec4482ab965cdb0288f2ec127d9d7350c344d36ec575d2` |
| Sources the signed files were produced from | Core `src/PROSOCHE-Dumb.xml` 2915855 bytes SHA-256 `e15ae8bc5a4da5a93141be620ac70000bf4aa1a896a9980939b8b4002c198d28`; Aware `src/PROSOCHE-Sentient.xml` 2987938 bytes SHA-256 `bcb2b37e97d563d3e3a407a1a4c6a75777101606000cff8990b2049aa7fe93cb`. Both signed containers were **decrypt-verified** against these sources — identifier sequence identical action-for-action, 15 AX sites each. |
| Manifest rows | `artifacts/shortcuts/MANIFEST.md`, the `Core signed` and `Aware signed` rows. All values above are copied from that table, and `python3 docs/manifest_check.py` proves every row against disk. |
| Device requirement | An iPhone running **iOS 26.x**. The paired device on record is an **iPhone 15 Pro (`iPhone16,1`) on iOS 26.6** — inside the declared target, so an observation on it is same-major-version evidence, not an extrapolation. |
| Personal Automations | **Required for Tests 1, 2, 3 and 4.** Tests 5 and 6 are reachable from the shortcut's own manual menu. |
| Apple Intelligence | **Not required.** Every test here exercises the deterministic Color Filters path, which is byte-identical on both forks (15 AX sites each). Run everything on **Core**. |

**One-line re-verification recipe** — run this before trusting any outcome recorded below, to
prove you are testing the build this file was written against:

```bash
shasum -a 256 "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut" \
              "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut"
```

Both digests must match the header exactly. If they do not, either the artifacts were re-signed
after this file was written — in which case update the header from `MANIFEST.md` first and say
so — or you are looking at the wrong files. **A digest mismatch invalidates every test below.**

### ⚠ Batching note — run this in the same sitting as `16-UAT.md`

A connected iPhone session is the scarcest input this project has, and **this instrument is not
worth a session of its own.** It shares its entire setup with the phase-16 device instrument:
the same clean install, the same deleted `state.json`, the same two Personal Automations, the
same `Test a Circle` entry point, and the same force-quit and Emergency Restore mechanics.

| Also run | Why it batches here |
|---|---|
| **`16-UAT.md` — all twelve tests, still outstanding** | **The primary partner.** Its Tests 6–11 are the same interruption trials as Test 1 below, run against brightness and volume instead of colour. Its Test 11 taps Emergency Restore, which Test 1 also taps — one tap can be observed for all three primitives at once if Dimming, Silence and Black and White have all fired in the same session. |
| `13-UAT.md`, `12-UAT.md`, `10-UAT.md` | Blocked on the same `DIST-03`; each costs minutes once a device is in hand. |
| **Phase 19** — nine-Circle device UAT | Needs the same clean install and the same automations. Black and White is one of the nine it sweeps. |

**Sequencing within the session:** run `16-UAT.md`'s Setup once, then let Dimming, Silence
**and** Black and White all fire before any restore test. A single Emergency Restore tap then
answers `16-UAT.md` Test 11 and this file's Test 1 together.

---

## Why every test here is device-gated, and why no simulator result can settle any of them

Per `.claude/CLAUDE.md` §9's evidence-escalation ladder and its **"Rung 2's ceiling"** list. The
ceiling names **real-hardware environmental behaviour** explicitly, and this primitive is inside
it for a measured reason, not a cautious one:

- The sibling environmental action **fails outright on a simulator**. `Set Brightness` returns
  *"There was a problem setting the brightness"*, and `Get Device Details → Current Brightness`
  reads `0` there — measured by spike `010-coercion-at-a-direct-set-parameter`, 2026-08-18. A
  simulator cannot execute this class of action at all.
- A simulator observation is **never promotable above `UNVERIFIED`** for anything inside that
  ceiling, however good the import channel is. Spike 007's import claim was retired and the
  simulator *can* import a signed `.shortcut` — that changes nothing here, because the ceiling
  is about what the action does, not about how the file gets there.
- **Personal Automations are user-created on the device** and cannot be exercised anywhere else
  at any effort. That is `DIST-03`'s irreducible core, and Tests 1–4 depend on it.

**Stated plainly: nothing in Phase 14 is device-proven, by construction.** Everything the phase
shipped is rung-1 structural — a `plistlib` census of the built artifact, a decrypt of the
signed container, and fourteen static checkers. **A guard proven to fire on a synthesised defect
is proof about the guard, not about the device.** Every test below starts blank, and **a test
you did not run is BLOCKED, not passed.** No device outcome may be inferred from a structural
check, a decrypted artifact or a simulator run.

### What is already settled below rung 3 — do NOT re-run these on hardware

| Question | Where it was settled | Verdict |
|---|---|---|
| Which identifier does iOS use? | Rung 4 — three decrypted device donors, spike 005 | `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`. **Not** the `UA*` macOS twin. Settled; do not re-derive. |
| What does `state` hold? | Rung 4 — the same three donors | Bool-as-integer: `1` = On, `0` = Off. **Not** `2` for Off — Apple's own `.intentdefinition` says `2` and is wrong as a plist encoding; shipping it would strand users in greyscale. |
| Is `operation` needed? | Rung 4 — both Turn donors elide it | Omitted in both legs. `"turn"` is the one literal no donor has ever emitted. |
| Are 15 AX sites emitted per fork? | Rung 1 — `plistlib` census of both built artifacts, re-measured on the **decrypted** signed containers | Yes: 11 apply + 4 restore, identical in Core and Aware. Structural, and it settles nothing about behaviour. |
| Does gate A pass? | Rung 1 — `docs/gate_a_residue_check.py` | **No, and it never will again.** The identifier is absent from all three bundled ToolKit snapshots, so gate A exits 1 by construction with a 30-line residue per fork. That is expected. **It is not a reason to reach for the macOS twin** — `docs/BUILD-NOTES.md` `DEV-08`. |

---

## Setup

Complete `16-UAT.md`'s Setup first — it is the same setup and it is more thorough. Then:

1. **Bind the Accessibility Shortcut to Color Filters** before anything else: Settings →
   Accessibility → Accessibility Shortcut → **Color Filters**. Triple-clicking the side button
   is then your escape hatch from a screen you cannot read comfortably.
2. **Record the tester's own pre-test Color Filters state by hand** — on or off, and if on,
   which filter and intensity. The product cannot read this and cannot restore it.
3. **Confirm which Circle fires `Black and White` under the sequence you selected.** It is
   **not** always Circle 2: `Classic` places it at Circle 2, `BlackMirror` at Circle 3, and
   `Ambient` at Circle 1. Read the `sequences` array in `src/CONFIG-BLOCK.md`, or the Control
   Room Note's Circle list plus your chosen sequence. **Recording an outcome against the wrong
   Circle is a recording error, not a product failure.**
4. **Reach the Circle via `Test a Circle` from the manual menu**, which drives the primitive
   directly and writes no Pressure — except in Tests 2–4, which need a real tracked-app
   open/close cycle and therefore need the Personal Automations.

---

## Tests

Six tests, numbered 1–6, **ordered by value rather than by code order**. Each names an explicit
expected observation and leaves its own `outcome:` field blank until run.

---

### 1. Force-quit mid-intervention, then Emergency Restore — does colour come back?

**This is the single highest-value observation in the phase, and it is first for that reason.**
There is **no snapshot** behind this primitive: the restore leg is one unconditional
`state = 0` at the top of `restore_managed_settings()`, and Emergency Restore is the only path
to it that does not require a CLOSE. **If CLOSE never fires — force-quit, battery death, a
locked-screen close — the unconditional off leg reached through the panic button is the only
thing between a user and being permanently stuck in greyscale.** Everything else in this file
is secondary to whether that one path works.

It is also the test that answers a debt older than this phase: **Emergency Restore has never
been tapped on a device**, in any phase, ever.

**Sequence.**

1. Open the tracked app so PROSOCHĒ fires and reaches the `Black and White` Circle. Confirm the
   screen goes black and white.
2. **Force-quit** — swipe up from the app switcher and kill both the tracked app **and** the
   Shortcuts app, so no CLOSE can fire. Confirm the screen is **still** black and white.
3. Open the Shortcuts app fresh and run `PROSOCHĒ — Nine Circles — Core` **by hand**.
4. Choose **Emergency Restore** from its menu.

**Expected observation.** Colour returns — the screen is in full colour immediately after
Emergency Restore completes, without opening Settings.

**What a failure looks like.** The screen stays greyscale after Emergency Restore. If it does,
capture *why* before recovering by hand: does Emergency Restore run at all, does it show its
completion confirmation, and does any error dialog appear? The off leg is emitted **first**
inside `restore_managed_settings()` precisely so that a dotted-read hard error further down
cannot abort the run before colour is restored — a failure here means either that ordering did
not hold or the action did not execute.

**Recover by hand afterwards if it failed:** triple-click the side button, or Settings →
Accessibility → Display & Text Size → Color Filters → off.

**Do not record "no error appeared" as a pass.** The observation is the screen's colour, nothing
else.

outcome (screen greyscale after the Circle fired):

outcome (screen still greyscale after force-quit):

outcome (colour returned after Emergency Restore):

---

### 2. The screen goes black and white when the Circle fires

The apply leg, observed on hardware for the first time. Rung 1 proves 11 apply sites shipped; it
proves nothing about whether iOS honours the intent.

**Sequence.** Open the tracked app so PROSOCHĒ fires and resolves to the `Black and White`
Circle (Setup step 3).

**Expected observation.** The whole screen — not just the shortcut's UI — renders in greyscale,
and it does so with **no alert, no notification and no menu**. Per decision **D-14-C** the alert
that used to *be* this Circle is deleted, not supplemented: the shipped experience is that the
phone simply goes black and white.

**A visible alert at this Circle is a failure**, and specifically a failure of D-14-C, not of the
toggle.

**If the action raises "Please choose a value for each parameter in this action"** — that is the
axis-4 unfilled-picker class, and it would mean the emitted `state` parameter did not resolve.
Capture the full dialog text.

outcome (screen renders greyscale):

outcome (no alert, notification or menu appeared at this Circle):

---

### 3. Colour returns on leaving the app

The ordinary path — the one that runs on every session, via the CLOSE pipeline.

**Sequence.** With the screen greyscale from Test 2, leave the tracked app normally (home
gesture or app switcher) so Automation B fires CLOSE.

**Expected observation.** Colour returns within a few seconds of leaving the app, without any
manual action.

**If colour does not return**, check whether CLOSE fired at all before attributing the failure to
the restore leg — the same distinction `16-UAT.md`'s Tests 6–10 draw for brightness and volume.
A missed CLOSE is a different defect from a restore leg that ran and did nothing.

outcome:

---

### 4. Colour returns through Ice expiry and through the live-Ice redirect

The two remaining `restore_managed_settings()` call sites. One insertion reaches all four; Tests
1 and 3 cover two of them, and these are the other two. **They are separate observations, not one
— a shared code path can still be reached by only one of two callers.**

**Sequence — Ice expiry.** Accumulate enough Pressure to reach Circle 9 (`Frozen`/Ice), let the
cooldown run its natural course to expiry, and observe the screen at the moment of expiry.

**Sequence — live-Ice redirect.** While a cooldown is live, open the tracked app so the run takes
the live-Ice redirect branch, and observe the screen.

**Expected observation.** In both cases Color Filters are off after the path completes. Note that
these paths turn colour **off** whether or not the `Black and White` Circle fired this session —
the leg is unconditional by design (**D-14-B**), so "it was already off and stayed off" is a
valid pass here, not an inconclusive result. **To make the observation meaningful, reach the
`Black and White` Circle first in the same session** so there is something to restore.

outcome (Ice expiry):

outcome (live-Ice redirect):

---

### 5. The kill switch set off leaves Color Filters untouched and the Circle fires a blank

`safety.ash_managed_color_filters` is the **only** recourse a user who runs Color Filters
themselves currently has. If it does not work, the disclosure in the Control Room Note is a
promise the product cannot keep.

**Sequence.**

1. Open `PROSOCHĒ — Nine Circles — Core` in the Shortcuts app for editing.
2. Find the `Text` action near the top holding the Config literal, and change
   `"ash_managed_color_filters": true` to `false`. Save.
3. Turn Color Filters **on by hand** in Settings first, so there is a user setting present for
   the product to fail to respect.
4. Run the shortcut → `Test a Circle` → the `Black and White` Circle.

**Expected observation.**

- The screen's Color Filters state is **unchanged** — still on, exactly as the tester set it.
- The Circle produces **nothing at all**: no toggle, no alert, no notification, no menu. A bare
  Nothing. This is what **D-14-D** specifies, and it is deliberately *not* BD-01's
  non-environmental visual pause, which was deleted.
- **Then leave the app so CLOSE fires.** The restore leg is **unconditional and is NOT gated on
  this flag**, so the tester's hand-set Color Filters **will be switched off**. That is the
  expected, documented behaviour, and it is exactly the accepted hazard in this file's safety
  preamble — record it, do not record it as a defect against this test.

**A failure here is:** the Circle toggling Color Filters despite the flag being `false`, or the
Circle producing a visible alert.

**Restore the flag to `true` afterwards** if the same install is used for any later test.

outcome (Color Filters unchanged at the Circle):

outcome (Circle produced no visible output):

outcome (CLOSE switched the tester's own setting off, as documented):

---

### 6. The action imports and runs without an unfilled-parameter error

The cheapest test in the file, and the one that would explain a failure in every test above.
Gate A does not know this identifier — by construction — so no structural check anywhere can
tell whether iOS accepts the emitted action.

**Sequence.** Complete the import in Setup. Then run `Test a Circle` → `Black and White` once,
from the manual menu, with no automations involved.

**Expected observation.**

- The shortcut **imports** without warning about an unknown or unavailable action.
- The `Black and White` step runs and completes.
- **No** "Please choose a value for each parameter in this action" dialog.

**If the import itself warns about an unavailable action**, that is the most important negative
result in the file and it invalidates Tests 1–5. Capture the exact warning text. It would mean
the donor-confirmed identifier is not accepted on this OS version, which is the one outcome the
three-donor evidence base does not cover — the donors prove the identifier was *written* by
Shortcuts on the owner's device, which is strong but is not the same as this build's emission
being accepted.

**Do not "fix" any such failure by substituting the macOS `UA*` twin.** See
`docs/BUILD-NOTES.md` `DEV-08`.

outcome (import produced no unavailable-action warning):

outcome (Black and White ran with no unfilled-parameter dialog):

---

## Results

| # | Test | Outcome |
|---|---|---|
| 1 | Force-quit mid-intervention → Emergency Restore returns colour | |
| 2 | Screen goes black and white when the Circle fires, silently | |
| 3 | Colour returns on leaving the app | |
| 4 | Colour returns through Ice expiry and the live-Ice redirect | |
| 5 | Kill switch off → Color Filters untouched, Circle fires a blank | |
| 6 | Imports and runs with no unfilled-parameter error | |

**Every cell above is blank because no device test has been run.** Nothing in this phase is
device-proven.

---

## Device availability, measured at authoring time

Measured 2026-08-19 at plan 14-03 execution, branching on `tunnelState` read from
`--json-output` and **never** on the `State` column — the column read `available (paired)` on
2026-08-17 while the tunnel was down, so the column is not the signal.

```bash
xcrun devicectl list devices --json-output <path>   # read from the JSON, not the table
```

| Field | Measured value |
|---|---|
| `deviceProperties.name` | `dougal` |
| `hardwareProperties.marketingName` / `productType` | iPhone 15 Pro / `iPhone16,1` |
| `deviceProperties.osVersionNumber` | `26.6` |
| `connectionProperties.pairingState` | `paired` |
| **`connectionProperties.tunnelState`** | **`unavailable`** |
| `connectionProperties.transportType` | `null` (none) |
| `connectionProperties.lastConnectionDate` | `2026-08-18T21:18:00.000Z` |
| `State` column in the printed table | `unavailable` — **not the signal, recorded only to show it agrees today** |

**Resolved to the blocked branch.** The blocker is real and its reason is unchanged from plan
16-06's measurement: **a known, paired device with no live tunnel and no active transport — no
session to drive.** It is *not* "no devices found"; recording that would be recording something
false, which this project forbids exactly as firmly as a false pass.

`DIST-03` stays open. All six tests above stay blank.

---

## What this file does NOT establish, stated plainly

- **That the screen turns black and white at all.** Structural coverage only — `14-01-SUMMARY.md`.
- **That colour ever comes back**, on any of the four recovery paths.
- **That Emergency Restore works.** It has still never been tapped on a device, in any phase.
- **That the kill switch does anything on hardware.** Its gate is structurally present and its
  numeric `> 0` form is correct for a JSON boolean; whether it resolves correctly at run time is
  device-gated.
- **That the emitted action is accepted by iOS 26 at all.** Gate A cannot know, by construction,
  and signing is measured unaffected by the unknown identifier — which proves the artifact is
  *shippable*, not that it *runs*.
- **Anything about the pre-existing-grayscale user.** No detection is built; the case is
  accepted, disclosed and backlogged.
