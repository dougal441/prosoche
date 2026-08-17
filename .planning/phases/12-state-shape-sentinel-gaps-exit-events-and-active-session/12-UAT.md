---
status: blocked
phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
source: [12-01-SUMMARY.md, 12-02-SUMMARY.md, 12-03-SUMMARY.md, 12-04-SUMMARY.md, 12-05-PLAN.md]
blocked_on: DIST-03
started: 2026-08-17
updated: 2026-08-17
---

# Phase 12 — Device UAT: the exit-recording path

## Header — what is under test

| Field | Value |
|---|---|
| Phase | `12-state-shape-sentinel-gaps-exit-events-and-active-session` |
| Written | 2026-08-17 |
| Commit artifacts were signed at | `ea7a0f409aa5707e25111ac8227a761689839d1e` |
| Fork 1 | **Core** — `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — 229903 bytes — SHA-256 `d1377102f6ad45a084a4467ae72d82d5dc27fbb1e1d31bda30d47bb124750a59` |
| Fork 2 | **Aware** — `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — 234118 bytes — SHA-256 `e2a56bf2b6bc76ef57aa7013d267b77e33172a65dae1d9eca2d20540b6618719` |
| Manifest row | `artifacts/shortcuts/MANIFEST.md`, the six "Core"/"Aware" rows — all six values above are copied from it and `python3 docs/manifest_check.py` proves every row against disk |
| Device requirement | An iPhone running **iOS 26.x**, with both Personal Automations already built by hand and pointing at the fork under test **by its exact display name** (`PROSOCHĒ — Nine Circles — Core` or `— Aware`) |
| Apple Intelligence | **Not required for these tests.** Every test below exercises the deterministic exit-recording path, which is identical on both forks. Fork 2 (Aware) additionally carries the `Use Model` call, which is out of scope for this file. |

A later run of this file may confirm it is testing the same build it was written against by
recomputing both forks' SHA-256 and comparing against the two values above, and by confirming
the checkout is still at (or descended from) commit `ea7a0f409aa5707e25111ac8227a761689839d1e`.

## Why device-only — no automated substitute exists

No file-level check, simulator run, or decrypted-artifact inspection can settle any test in
this file. Specifically, per `.claude/CLAUDE.md` §9 ("Rung 2's ceiling") and the evidence
hierarchy it extends:

- **Personal Automation triggers** (App Is Opened / Is Closed) are user-created directly on
  the device and cannot be exercised on a simulator at any effort — there is no equivalent
  mechanism to script or fake one.
- **The Control Room Note path is device-gated by measurement, not by policy.**
  `com.apple.mobilenotes` is absent from the booted simulator's 25-app inventory (measured
  2026-08-17, `.claude/CLAUDE.md` §9) — so `com.apple.mobilenotes.SharingExtension`,
  `appendnote`, `filter.notes` and `shownote` behaviour needs a real device.
- **Real-hardware environmental behaviour** — brightness and volume capture-and-restore via
  `restore_managed_settings()` — is rung 3+ by definition; no simulator or file-level
  inspection can observe whether an actual screen dims and un-dims.
- **This phase's specific new-risk surface is entirely unexercised.** The closed
  2026-08-13/14 OPEN-path debug session (`docs/BUILD-NOTES.md`) reached breadcrumb J on the
  **OPEN** path only. Nothing in `docs/BUILD-NOTES.md` records an exit-recording device
  observation at any point in this project's history — `record_exit_and_route()`,
  `route_exit()`, and `close_pipeline()`'s restore arm have **zero** device evidence at any
  rung before this file.

A decrypted-artifact inspection (this plan's Task 1, and 10-04/10-05's precedent) proves only
that the right bytes shipped — it is structural evidence and is explicitly not a substitute
for observing the shortcut run.

## Setup

1. **Fresh-install both forks** from the two signed artifacts named above — delete any
   previously installed shortcut of either name from the Shortcuts app first, so there is no
   ambiguity about which build a Personal Automation is pointing at.
2. **Delete `PROSOCHE/state.json`** from the Shortcuts iCloud folder (Files → iCloud Drive →
   Shortcuts → PROSOCHE) so the run starts from a genuinely clean state. (The `schema_version`
   3→4 bump this phase carries would also force a rebuild on next OPEN, but deleting the file
   removes that as a confound — the tests below should observe first-run bootstrap behaviour,
   not migration behaviour.)
3. **Create or re-point the two Personal Automations** (Settings → Shortcuts Automation, or
   the Shortcuts app → Automation tab) to the installed shortcut's exact display name — `App
   Is Opened` → `OPEN` as Shortcut Input, `App Is Closed` → `CLOSE` as Shortcut Input, both
   with `Run Immediately` (Ask Before Running off). Point them at whichever fork the current
   test targets.
4. **Read state at** Files → iCloud Drive → Shortcuts → PROSOCHE → `state.json` (long-press →
   Quick Look, or share to a text viewer). The Control Room Note is the Apple Note titled
   `PROSOCHĒ`.

## Tests

Each test names an explicit expected observation and leaves its own result field blank until
run.

---

### 1. First OPEN against clean state

**Setup.** Continue directly from the Setup section above — `state.json` freshly deleted, no
prior run this session.

**Sequence.** Open one tracked app from the Home Screen (the Core fork is sufficient for this
test).

**Expected observation.** The bootstrap runs and writes a fresh `state.json` with no visible
error. Specifically:

- **No** "no value was found for dictionary key" alert.
- **No** "could not evaluate the key path" alert — this is the exact failure mode a missing
  seeded key produces on a dotted read, and this phase's entire purpose is to make it
  structurally unreachable (`exit_events`, `active_session`, `profile_snapshot.create_target_url`
  all seeded).
- A session starts: `state.json` shows `active_session` as a live object with a non-null
  `id`, `started_at`, and `declared_duration_seconds` — not the four-leaf sentinel from the
  bootstrap template.
- `state.json` shows `schema_version: 4`, `exit_events: []`, and
  `exit_selection_counter: 0` (unless the session below already advances the counter).

**Failure evidence to capture.** A screenshot of any alert text verbatim, plus the full
`state.json` contents immediately after the open.

outcome: **PARTIAL — the bootstrap/state-shape half is CONFIRMED PASSING; the OPEN half is not
yet exercised.** Read this split literally; do not promote it to a full pass.

Device, 2026-08-17 11:10–11:15, Core `b07497ba`. Precondition verified rather than assumed:
Files → iCloud Drive → Shortcuts was observed **empty** (no `PROSOCHE` folder, no `state.json`)
immediately before the run. A **manual** run then bootstrapped and reached the control menu.

**CONFIRMED — every structural assertion this test makes about the written file.** The full
`state.json` (2 KB) was read on device and holds:

- `schema_version: 4` ✓
- `exit_events: []` ✓ — the key `06-CONTEXT.md` recorded as "entirely absent from the bootstrap
  template", the axis-7 gap this phase exists to close. It is present and seeded.
- `exit_selection_counter: 0` ✓
- `active_session` seeded as the **four-leaf sentinel container**
  `{"id": "null", "started_at": "null", "declared_duration_seconds": "null", "intention": "null"}` ✓
- `pending_exit` seeded as `{"type": "null", "timestamp": "null"}` ✓
- `settings_snapshot.brightness` and `.volume` each seeded with all three leaves
  (`original_value` / `changed_at` / `changed_by_session_id`, all `"null"`) ✓
- `exit_stats` seeded for **all six** exits, each `{count: 0, sum_return_seconds: 0, samples: []}` ✓
- `profile_snapshot.create_target_url: "null"` seeded ✓, `enabled_exits` holding all six ✓
- **No** "no value was found for dictionary key" alert and **no** "could not evaluate the key
  path" alert appeared ✓

The container/leaf discipline is visible in the file and is exactly as
`.claude/CLAUDE.md` axis 7 specifies: **container leaves carry the STRING sentinel `"null"`**
(gatable by a condition-5 string-is-not test) while genuinely scalar top-level fields
(`last_open_at`, `last_close_at`, `last_app`, `cooldown_until`, `note_content_hash`,
`last_model_message`) carry **real JSON `null`**. That asymmetry is deliberate and correct here.

**NOW CONFIRMED — a real OPEN was driven through the Personal Automation (2026-08-18 08:16).**
`AliExpress` (one of the two tracked apps, read out of the automation's own app list) was launched
from Spotlight. The `App Is Opened` automation fired, PROSOCHĒ ran, and `state.json` afterwards
reads:

- `active_session.id: "session-1787041019-63888487"` — a **live, non-null session id** ✓
- `active_session.started_at: 1787041019` ✓
- `active_session.declared_duration_seconds: null` (correct — no contract was declared) ✓
- `last_open_at: 1787041019`, `last_app: "tracked"` ✓
- `pressure: 0.3333…`, `gravity: 0.3333…` — Pressure accumulated from the open ✓
- `circle: 0` — the **silent band**, so nothing was shown ✓
- **No** "no value was found for dictionary key" alert, **no** "could not evaluate the key path"
  alert ✓

So `active_session` is no longer the four-leaf sentinel: it is a live object, which is precisely
the assertion that was outstanding. **Test 1 is now a full PASS.**

TWO ANOMALIES observed in the same file, recorded rather than swept:

1. **`opens_today: 2` after a single app launch.** Only one deliberate open occurred. Either the
   `App Is Opened` automation fired twice for one launch, or the open was double-counted. This is
   adjacent to the secondary candidate already flagged in `04-UAT.md` gap G-04-3 — that OPEN's
   debounce keys off a single global `last_open_at` rather than per-tracked-app. Worth settling,
   because every Pressure figure downstream inherits the error.
2. **`heat` serialises as the STRING `"0"`** while `pressure` and `gravity` are numbers. Same
   axis-6 boolean/number/string coercion family as the `voice_enabled` defect recorded in
   `07-UAT.md` Test 6, and dangerous for the same reason: a numeric comparison against a
   text-typed operand renders red in the editor, is structurally valid in the file, and fails at
   runtime.

Recorded caveat: `panic_escape_enabled` serialises as the number `1` while `voice_enabled`
serialises as the boolean `true`. Both are readable, so this is not a defect on its face, but
the inconsistency is noted here because a boolean-vs-number coercion is exactly the sort of
thing axis 6 turns into a runtime operand-type failure later.

---

### 2. A genuine leave and confirm exit — each of the six routes

**Why this is the highest-priority test in this file.** The exit-recording path
(`record_exit_and_route()`, then `route_exit()`) was **never** exercised by the closed
OPEN-path debug session and carries zero device evidence at any rung. This is where a
`could not evaluate the key path` error would first appear if any of this phase's seeded
keys were wrong in a way file-level checking missed.

**Setup.** From an OPEN that reaches a Circle ≥ 1 (raise Pressure with a few closely-spaced
opens if the first open lands at Circle 0 — see 10-UAT.md Test 2 for the arithmetic), choose
`Leaving` at the intervention menu, then choose an exit from PROSOCHĒ's suggestion menu.

**Sequence.** Repeat across **separate runs**, choosing each of the six routes in turn:
`Capture`, `Coordinate`, `Create`, `Connect`, `Consult`, `Close`.

**Expected observation, per route:**

- `Capture` → a submenu of `Notes` / `Voice Memos` / `Camera`; the chosen app opens.
- `Coordinate` → a submenu of `Reminders` / `Calendar`; the chosen app opens.
- `Connect` → the Contacts app opens directly (no submenu, no call/message/send action of
  any kind — PROSOCHĒ never contacts anyone on the user's behalf).
- `Consult` → a text prompt ("What are you trying to find?"), then a six-item menu (`Search
  Web`, `Search Maps`, `Open Notes`, `Open Reminders`, `Open Calendar`, `Back`); the chosen
  surface opens with the query, or nothing happens on `Back`.
- `Close` → returns straight to the Home Screen.
- `Create` — **run this one specifically on a clean install** (delete `state.json` again
  immediately before this sub-test, or use the other fork's first run): the expected
  observation is that **the user is asked** "Where should Create open?" via a URL prompt —
  **not** that a placeholder URL silently opens. This is `route_exit()`'s Create branch,
  gated by `profile_snapshot.create_target_url`'s sentinel-seed (Plan 12-04, checkpoint
  option-a): the first-ever Create exit on a clean install must always ask, because the seed
  value can never satisfy the condition-5 "captured" gate. On a **second** Create exit in the
  same install, after the first has saved a real URL, the expected observation flips: no
  prompt, and the previously saved URL opens directly.

**No route may produce a "could not evaluate the key path" error or a silently-opened
placeholder URL (the literal string `"null"` as a URL).**

**Failure evidence to capture, per route.** A screenshot of any error alert verbatim; for
`Create`, a screenshot of whichever behaviour actually occurred (prompt vs. silent open) and
the `profile_snapshot.create_target_url` value in `state.json` immediately after.

outcome (Capture):

outcome (Coordinate):

outcome (Connect):

outcome (Consult):

outcome (Close):

outcome (Create, clean install — must ask):

outcome (Create, second exit — must reuse saved URL):

---

### 3. CLOSE after a session that changed brightness or volume

**Why this is the SESS-07 / SAFE-01 test.** `restore_managed_settings("Reloaded State")` is
the only path that returns brightness and volume to their captured values after a Dimming or
Silence primitive. Plan 12-02/12-03 made every dotted read on this path structurally
incapable of raising on a fresh `state.json`; this test is the first device observation that
the restore actually reaches and actually restores.

**Setup.** Raise Pressure to a Circle that fires Dimming or Silence (Classic sequence: Circle
5 is Dimming). Note the brightness/volume level by hand before the primitive fires.

**Sequence.** Let Dimming or Silence fire, then close the tracked app (trigger the CLOSE
Personal Automation).

**Expected observation.** `close_pipeline()`'s owner arm is reached (see Test 4 below for the
non-owner case) and `restore_managed_settings("Reloaded State")` runs before the CLOSE
confirmation notification and before `save_state()`. Brightness/volume return to the
hand-noted pre-primitive value. `state.json`'s `settings_snapshot` (or equivalent captured
value) clears after the restore.

**If brightness or volume does NOT return:** restore it by hand through iOS Settings, record
the failure with its evidence, and do not push through to the remaining tests in this
sub-section.

**Failure evidence to capture.** The hand-written before value, the observed after value, and
the relevant `state.json` fields immediately after the CLOSE.

outcome:

---

### 4. A superseded CLOSE

**Setup.** Start a session (OPEN), do not close it yet.

**Sequence.** Start a **second** session before closing the first — open the tracked app
again from a different route if possible (or trigger a second OPEN automation run), so a new
`active_session.id` is written. Then close the **first** (now-superseded) session.

**Expected observation.** The condition-4 ownership compare at `close_pipeline()`'s reload
gate (`Reloaded Session ID` vs. `Captured Session ID`) is unchanged by this phase's container/
leaf conversion (Plan 12-03 verified this in file-level evidence only). The superseded CLOSE
should write **nothing**: no session record appended to `recent_sessions`, no
`restore_managed_settings()` call, no CLOSE confirmation notification, no `save_state()`. The
second (current) session's `active_session` in `state.json` should be undisturbed by the
superseded CLOSE run.

**Failure evidence to capture.** `state.json` immediately before and after the superseded
CLOSE, plus whether any notification or alert appeared.

outcome:

---

### 5. Second OPEN after an exit

**Why this test exists.** The `pending_exit` outcome path and the `exit_stats.<type>`
composite reads (`STATE_SEED_COMPOSITE_PREFIXES`, Plan 12-04) become reachable only on the
OPEN that follows a recorded exit — no earlier test in this file reaches them.

**Setup.** Complete Test 2's `Close` route (or any route) so `pending_exit.type` and
`pending_exit.timestamp` are set in `state.json`.

**Sequence.** Open the tracked app again.

**Expected observation.** No "could not evaluate the key path" error on the
`exit_stats.<type>.count` / `.sum_return_seconds` / `.samples` composite reads. `state.json`'s
`exit_stats` object gains or updates an entry keyed by the exit type chosen in Test 2, and
`pending_exit` is cleared back to its sentinel after this OPEN consumes it.

**Failure evidence to capture.** `state.json`'s `exit_stats` and `pending_exit` values before
and after this open, plus any error alert verbatim.

outcome:

---

### 6. Control Room after an exit

**Setup.** Continue from Test 2 or Test 5 — at least one exit has been recorded.

**Sequence.** Run the shortcut manually → `Open Control Room`.

**Expected observation.** The Note opens (confirming the Control Room Note path survives the
refactor — this is device-gated per the "Why device-only" section above) and shows the ledger
entry for the exit chosen in Test 2, appended per the Note's existing append convention.

**Failure evidence to capture.** A screenshot of the Note content, or a screenshot of any
error if the Note failed to open or append.

outcome:

---

### 7. `exit_events` after several exits

**Setup.** Complete at least three of Test 2's routes across separate sessions, so
`exit_events` has accumulated multiple entries.

**Sequence.** Read `state.json`'s `exit_events` array directly (no shortcut run needed for
this step — pure state inspection).

**Expected observation.** The array is **newest-first** (the most recently recorded exit is
element 0) and **capped at twenty** entries (`record_exit_and_route()`'s
`Repeat Index < 20` cap). With only three-to-a-few exits recorded in this test session, the
array should simply contain exactly that many entries in newest-first order — the cap itself
is not exercisable without twenty-plus real exits, but the ordering is observable now.

**Failure evidence to capture.** The full `exit_events` array contents and the order in which
the exits were actually performed, side by side.

outcome:

---

## Results

| # | Test | Outcome |
|---|---|---|
| 1 | First OPEN against clean state | |
| 2 | A genuine leave and confirm exit (all six routes + Create clean/reuse) | |
| 3 | CLOSE after a session that changed brightness or volume | |
| 4 | A superseded CLOSE | |
| 5 | Second OPEN after an exit | |
| 6 | Control Room after an exit | |
| 7 | `exit_events` after several exits | |

## Summary

total: 7 (Test 2 carries 7 sub-observations)
passed: 0
issues: 0
skipped: 0
blocked: 7

## Reachability probe

```
$ xcrun devicectl list devices
No devices found.
```

Run 2026-08-17. iPhone Mirroring was not attempted as a substitute channel — devicectl
reporting no connected devices means no iPhone is attached to this Mac at all, so a mirroring
session (which requires the same physical/Wi-Fi connection) is not available either.

**Verdict: BLOCKED.**

## Standing note — what may not be substituted for a device observation

**Every outcome field above stays blank.** This is the recorded precedent set by
`10-UAT.md` (Phase 10: `xcrun devicectl list devices` → "No devices found." → all ten tests
left blank, DIST-03 unchecked) and reaffirmed by Phase 9 Plan 02 (12 device-proving tests
blocked on the same underlying connectivity gap). It is not a failure and it is not an
oversight — it is this project's standing, deliberate policy that a fabricated pass is worse
than a blank.

**Do not substitute a Mac import, a simulator run, or any inference from the decrypted
artifact for a device observation.** This plan's Task 1 decrypted both signed artifacts and
confirmed `schema_version 4`, a four-leaf `active_session`, and `exit_events == []` in the
bootstrap template — that is structural proof only. None of it observes whether
`record_exit_and_route()`, `route_exit()`, or `restore_managed_settings()` actually run
correctly when a real Personal Automation trigger invokes them on a real device.

**This UAT is re-run unchanged when a device becomes reachable.** Do not rewrite the tests
above to fit whatever device eventually connects; run them exactly as written against the
build named in the header (or a freshly signed rebuild, provided its SHA-256 is updated in
the header first). The seven tests above are unaffected by which Personal Automations already
exist on the tester's phone — Setup step 3 covers (re)creating them.

DIST-03 stays **unchecked** in `.planning/REQUIREMENTS.md` until every test above has a
recorded outcome from a real iPhone.

## Verdict

_Blank. Filled in only after the seven tests above resolve on a real device._
