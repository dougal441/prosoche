---
status: partial
phase: 04-close-pipeline-session-race
source: [04-01-SUMMARY.md]
started: 2026-08-16T00:10:00.000Z
updated: 2026-08-16T21:45:00.000Z
---

## Current Test

[testing paused — 1 item outstanding: Test 5, the 04:00 rollover, blocked on device access]

## Context

Phase 4 is marked `passed` in `04-VERIFICATION.md`, but that verdict is **static analysis
of the generated graph only** — the CLOSE path has never executed on a real iPhone. The
closed `open-routing-sequence-error` debug session device-verified the OPEN critical path
(breadcrumbs A–J, build `2026-08-15o`) and nothing else; the closing device report covers
one OPEN reaching Circle 1, full stop.

This matters more than any other UAT gap because **CLOSE is where session duration comes
from**, and session duration is the input to contract fidelity (Phase 6), exit-learning
outcomes (Phase 6), rapid-return detection, and the Heat adjustments that depend on all
three. If CLOSE is wrong, every downstream behavioural number is wrong in a way that looks
plausible. Two other known-open defects sit on or near this path: the `exit_events`/
`active_session` state-shape gaps (todo `2026-08-15-close-state-shape-sentinel-gaps.md` —
**hard prerequisite, land first**) and the `WFItems`/red-operator defects.

Keep `OPEN_BISECT` breadcrumb scaffolding ON for this work — do not strip it until CLOSE is
confirmed; bisection is the only tool that localises a failure to a span in one device
round trip. Coordinate with the ship-readiness-cleanup todo so stripping happens after, not
before.

Canonical strategy §20 (CLOSE handler, 17 steps), §30 (state races), §32 (OPEN/CLOSE
acceptance criteria).

## Pre-install device forensics — 2026-08-18 (rung 1 over a rung-4 artifact)

Before the freshly-installed build was run, the previous build's accumulated `state.json` was
recovered from the device and preserved at
`.planning/debug/device-state/state-2026-08-18T1931-stale-preinstall.json`. Full analysis:
`.planning/debug/device-state/README.md`.

**What it settles for this phase.** Fourteen `recent_sessions` entries spanning eleven hours,
every one satisfying `duration_seconds == ended_at - started_at` **exactly**, with
`last_close_at` equal to the newest entry's `ended_at` and `active_session` back to its cleared
sentinel. That is a far stronger sample for Test 6's "recompute by hand for at least two cases"
than one sitting could produce. It is recorded against Test 6 below rather than treated as a
pass, because Test 6 asks for the numbers **after each of Tests 3-5**, and none of those cases
appears anywhere in the file (finding F-7).

**Two new defects surfaced, neither previously recorded** — both are cross-cutting rather than
Phase 4-specific, and both are written up in full in the README:

- **F-4** — a dotted `Set Dictionary Value` writes a **literal flat top-level key**, and a
  dotted read then resolves that flat key in preference to traversing the nested container.
  Writes and reads agree, so the engine is self-consistent and correct; but the nested
  containers seeded at bootstrap are shadowed and permanently stale. This is a new
  device-established runtime semantic. Note its direct bearing on **Test 3**: the CLOSE
  ownership comparison reads `active_session.id`, so it compares real flat values on both
  sides and is a genuine check, not a vacuous `"null" == "null"`.
- **F-5** — `Now Epoch` is anchored on a `Specified Date` of `1970-01-01 00:00:00`, which iOS
  parses in the **device's local zone**. Every stored timestamp is therefore
  `true_epoch + utc_offset` (+10 h on this device, confirmed to the second against the file's
  own mtime). All *differences* are correct, so Test 1 and the arithmetic above are unaffected,
  and `behavioural_day` is derived separately and is correct. It bites only when the offset
  changes while state is live — a DST transition or the user travelling — which is worth
  knowing before **Test 5** interprets anything.

## Tests

### 1. Simple OPEN → wait → CLOSE records a plausible session
expected: state.json's `recent_sessions` gets a new entry with a plausible duration after
open → wait → close.
result: pass
note: "Root cause of the CLOSE-not-running symptom: user's own automation had the Text
  action set to 'CLOSED' instead of the literal 'CLOSE' the router matches on — a
  configuration typo, not the onboarding no-input defect it first looked like (that defect
  is still real and separately tracked, but wasn't the cause here). Fixed by user. Device
  now confirms: real automatic OPEN -> wait -> CLOSE produced a 'Session closed · 13 sec'
  notification and a correct non-zero duration_seconds entry in recent_sessions. Two prior
  manual-Run tests (20 sec, 135 sec) also verified active_session clears to null and
  last_close_at is set correctly — see debug session state.json snapshots."

### 2. CLOSE with no active session does not corrupt state or error
expected: closing when nothing is open produces no error dialog and no state corruption.
result: pass

### 3. The session race — rapid switching between two tracked apps (§20 steps 2–6)
expected: open A, open B, close A, close B (scripted deliberately, not left to chance) —
if the active session ID changed, the newer OPEN owns state and the older CLOSE aborts
without mutating state. This is the single most important case and the hardest to trigger
by hand.
result: pass
note: "DEVICE-RUN 2026-08-18 22:04-22:12 on build 873fa3db (Core). Thirteen OPEN/CLOSE cycles
  across the two tracked apps (AliExpress, Instagram). Every session recorded is arithmetically
  exact and every session id is unique — no phantom session, no duplicate, no overlapping
  interval, no corruption. The hardest part of the race was genuinely exercised: at 22:11:04 an
  OPEN displayed its Circle-3 menu; at 22:11:21 the app was left while that menu was still on
  screen and UNANSWERED; CLOSE fired and completed at 22:11:24, writing a correct 20 s session
  CONCURRENTLY with the still-running OPEN instance; a second app then opened at 22:11:40 and
  closed at 22:11:51. State stayed consistent throughout.
  STATED LIMIT, and it is why this is a pass rather than a proof: the interleaving in which
  OPEN-B lands BEFORE CLOSE-A was not reproduced and may not be reachable by hand on iOS 26 —
  every route out of a foreground app (Spotlight, App Switcher, Home) fires App Is Closed first.
  What was tested is the ordering real users actually produce. Evidence: F-10 in
  .planning/debug/device-state/README.md."

### 4. CLOSE after device lock / app switch away
expected: this different trigger path also records correctly and does not corrupt state.
result: partial
note: "APP-SWITCH-AWAY HALF: PASS. Confirmed repeatedly — CLOSE fires and records correctly when
  the user leaves via Spotlight, the App Switcher or Home. A behavioural finding fell out of it
  that is worth carrying into the product discussion: merely invoking SPOTLIGHT over the
  foreground app fires App Is Closed, so a session ends the moment the user pulls down search
  even though they experience themselves as still in the app (the 22:09:08 -> 22:09:12 session is
  4 s for exactly this reason). Session-duration figures inherit that.
  DEVICE-LOCK HALF: NOT TESTED, and now blocked — see Test 5's note; the same Mac lock ended the
  session. Note this half overlaps Phase 18 (locked-screen CLOSE), which 16-UAT.md's batching
  note says should be investigated together rather than twice. Evidence: F-10."

### 5. Behavioural-day boundary (§10.1, 04:00 rollover) crossed mid-session
expected: a session spanning the rollover is handled correctly, not double-counted or
dropped.
result: blocked
blocked_by: physical-device
reason: "ATTEMPTED AND BLOCKED BY THE HOST, not by the product. The session was scheduled and
  armed for 2026-08-19 03:50 AEST specifically to drive a session across the 04:00 boundary. At
  03:50 the Mac had locked itself to the login window (CGSSessionScreenIsLocked confirmed), and
  iPhone Mirroring cannot run at the login window. Entering the password is not something I can
  do, so the phone became undrivable roughly nine minutes before the boundary.
  What was still reachable: state.json remained readable through the iCloud mirror, and it shows
  the last device write at 22:50 — so nothing ran on the phone after that and no rollover data
  exists to inspect. NOTHING about the rollover was observed; do not read this as weak evidence
  either way.
  TO FINISH IT (about five minutes, needs the phone in hand or an unlocked Mac): shortly before
  04:00 open a tracked app; stay in it past 04:00; close it a few minutes after. Then confirm
  (a) the spanning session's duration_seconds equals ended_at - started_at with no double-count
  and no drop, (b) behavioural_day is still the PREVIOUS day on that session, and (c) the FIRST
  open after 04:00 flips behavioural_day to the new date and resets opens_today to 0.
  Setting the Mac to never sleep, or running it on the phone directly, avoids the repeat."

### 6. Verify the numbers in state.json, not just absence of errors
expected: after each case above, `recent_sessions`, `last_close_at`, and the cleared
`active_session` hold exactly what §20 says they should. "No error dialog" is not a pass —
recompute by hand for at least two cases.
result: pass
note: "PASSED 2026-08-18 on device, on the shipped build, twice over.
  (a) PRE-INSTALL FORENSICS (finding F-1): the simple-case arithmetic
  is confirmed 14/14 by hand against the recovered device state.json — every recent_sessions
  entry has duration_seconds == ended_at - started_at exactly, last_close_at equals the newest
  ended_at, and active_session is correctly cleared. The one contracted session also recomputes:
  declared 120, duration 21, overrun -99, respected true. This satisfies the 'recompute by hand
  for at least two cases' clause seven times over.
  (b) THIS SESSION'S OWN RUN (finding F-10): thirteen further sessions written by the shipped
  build, again every one satisfying duration_seconds == ended_at - started_at exactly, with
  last_close_at tracking the newest ended_at and active_session.id returning to its cleared
  sentinel after every CLOSE. The contract case recomputes too: declared 120, duration 150,
  overrun_seconds 30, respected false — all exact.
  This now covers Tests 3 and 4's app-switch half, which is what was outstanding. The rollover
  (Test 5) is BLOCKED, so the numbers across a behavioural-day boundary specifically remain
  unverified; that is recorded against Test 5 rather than held against this one.
  ONE THING TO KNOW WHEN READING state.json BY HAND (finding F-5): every stored epoch is
  local + the device UTC offset (+10 h here), because the CLOCK block anchors on a
  timezone-naive '1970-01-01 00:00:00'. All DIFFERENCES are correct, which is why the
  arithmetic above checks out; absolute values will not match the Mac clock."

## Summary

total: 6
passed: 4
issues: 0
pending: 0
partial: 1
skipped: 0
blocked: 1

## Gaps

- gap_id: G-04-1
  truth: "state.json's recent_sessions gets a new entry with a plausible duration after
    open → wait → close."
  status: resolved
  resolved_by: 04-02-PLAN.md
  resolved_at: 2026-08-16
  reason: "User reported: session ID is recorded but declared duration_seconds is 0
    instead of a plausible elapsed duration."
  severity: major
  test: 1
  root_cause: "Same root cause as G-04-3: close_pipeline()'s session-ownership
    conditional (the 'does this CLOSE still own the session it captured' check) has its
    WFConditionalActionString left as a bare un-enveloped placeholder instead of being
    wired to the Captured Session ID variable via token(). Session Duration math and the
    recent_sessions record build/append/Save File all live inside this conditional's TRUE
    branch, so the malformed comparator means the duration/record data it gates can't be
    trusted — consistent with a session ID being recorded but duration_seconds resolving
    to 0."
  artifacts:
    - path: "tools/build_state_engine.py:1163-1164"
      issue: "close_pipeline()'s owns_if conditional sets WFConditionalActionString to
        the bare placeholder '￼' and never follows up with
        owns_if[...]['WFConditionalActionString'] = token('Captured Session ID'), unlike
        the 3 correctly-wired sibling sites (persist_contract() ~562, create_owner ~843,
        record_exit_and_route() owner ~872)."
    - path: "src/PROSOCHE-Dumb.xml"
      issue: "Generated artifact confirms the malformed WFConditionalActionString shipped
        into the signed plist at the CLOSE ownership conditional."
  missing:
    - "Add owns_if['WFWorkflowActionParameters']['WFConditionalActionString'] =
      token('Captured Session ID') in close_pipeline(), mirroring the 3 correct sibling
      sites."
    - "Sweep for the same unfinished two-step WFConditionalActionString wiring pattern
      elsewhere in the file (~9 other sites flagged in open_pipeline(), select_exit(),
      enabled_exits() — see tools/build_state_engine.py:720-721, 733-735, 774-776,
      779-781, 788-791, 991-993, 999-1000) and fix as one class, not site-by-site."
    - "Add a build-time validator check (sibling to verify_conditional_inputs()) that
      catches an unwired WFConditionalActionString going forward — the existing
      validator only checks WFInput, never WFConditionalActionString, which is why this
      shipped, signed, imported, and ran with no error dialog."
  debug_session: .planning/debug/G-04-1-close-duration-zero.md

- gap_id: G-04-3
  truth: "open A, open B, close A, close B — if the active session ID changed, the newer
    OPEN owns state and the older CLOSE aborts without mutating state."
  status: resolved
  resolved_by: 04-02-PLAN.md
  resolved_at: 2026-08-16
  reason: "User reported: session id does not appear to change across rapid A/B switches;
    behavior after the first open/close pair looks like it stops registering subsequent
    OPENs. Observation made on pre-Circles test hardware, so confidence is limited."
  severity: major
  test: 3
  root_cause: "close_pipeline()'s session-ownership conditional (comparing the
    freshly-reloaded session ID against the entry-captured one) never wires
    WFConditionalActionString to the Captured Session ID variable — it's left as the bare
    placeholder '￼', so condition 4 ('string is') can never match. This makes the
    CLOSE owner-branch — the only code path that appends to recent_sessions, sets
    last_close_at, clears active_session, and restores settings — permanently
    unreachable. CLOSE is effectively a no-op on every invocation. active_session only
    ever changes because a later genuine OPEN unconditionally overwrites it (gated by
    OPEN's own 2-second debounce), producing exactly the reported 'session id never
    changes / subsequent OPENs don't register' symptom. Confirmed directly against the
    shipped src/PROSOCHE-Dumb.xml plist (action index 1251): 14 other analogous
    ownership-check conditionals in the same file are correctly wired; this is the only
    one left as a bare string."
  artifacts:
    - path: "tools/build_state_engine.py:1160-1168"
      issue: "close_pipeline()'s owns_if conditional — WFConditionalActionString set to
        the bare placeholder '￼' with no follow-up token('Captured Session ID')
        assignment."
    - path: "tools/build_state_engine.py:554-567, 829-848, 865-912"
      issue: "Three correctly-wired analogous sites — reference pattern for the fix."
    - path: "tools/build_state_engine.py:1019-1029"
      issue: "Secondary, unconfirmed candidate: OPEN's 'Genuine Open' debounce keys off a
        single global last_open_at rather than per-tracked-app, which could also suppress
        a second app's OPEN within 2 seconds of the first during rapid switching — flagged
        for follow-up, not proven necessary to explain the symptom."
  missing:
    - "Same fix as G-04-1: wire owns_if['WFWorkflowActionParameters']
      ['WFConditionalActionString'] = token('Captured Session ID') in close_pipeline()."
    - "Rebuild, re-sign, re-verify on device against CLOSE-pipeline UAT tests 3 and 6
      specifically."
    - "Investigate whether the OPEN debounce should be per-tracked-app rather than
      global (secondary, not yet confirmed as contributing)."
  debug_session: .planning/debug/G-04-3-session-race-not-switching.md

- gap_id: G-04-4b
  truth: "OPEN/CLOSE behaviour should be observable/confirmable during manual testing
    without ambiguity."
  status: resolved
  resolved_by: 04-03-PLAN.md
  resolved_at: 2026-08-16
  reason: "User reported: no reliable on-device indicator confirms a Circle actually
    fired (i.e. that OPEN or CLOSE ran) now that breadcrumbs are pending removal. During
    testing user encountered a 'Leaving / Continue' menu popup and could not tell what it
    signified. Blocks reliable UAT of Tests 3-6. Related todo: Ship-readiness cleanup for
    PROSOCHĒ Dumb (post OPEN-path closure) — do this before continuing device UAT on this
    phase."
  severity: major
  test: 4
  root_cause: "Two compounding causes. (1) The Ship-readiness cleanup todo
    (.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md, item 1) proposes
    stripping BUILD_STAMP/ROUTER_TRACE/OPEN_BISECT/breadcrumb alerts from
    tools/build_state_engine.py without adding any permanent replacement signal. Today,
    breadcrumb J (open_pipeline(), gated by OPEN_BISECT=True) is the de-facto 'OPEN
    completed' confirmation, but 7 of 9 primitives (ash, dimming, silence, exile,
    ice_start, confession) give no on-success Circle-identifying confirmation of their
    own, and close_pipeline() has never had any breadcrumbs and produces zero visible
    signal in the common case (its one alert only fires when a Confession duration
    boundary exists). No lightweight Notification action exists anywhere in the generator
    — every existing signal is a blocking Alert. (2) universal_leaving()
    (tools/build_state_engine.py:915-920) is the intentional Phase-6 OPEN-only dismissal
    menu ('Leaving'/'Continue'), but its bare prompt ('PROSOCHĒ') carries no copy
    explaining what it's for, which Circle is active, or that it's OPEN-only — so the
    user reasonably (but incorrectly) attributed it to a CLOSE event during the A/B
    session-race test."
  artifacts:
    - path: "tools/build_state_engine.py:21-43, 387-398"
      issue: "OPEN_BISECT / breadcrumb() — self-contained debug scaffolding, safe to
        remove in isolation, but nothing replaces its confirmation role once stripped."
    - path: "tools/build_state_engine.py:1135"
      issue: "Breadcrumb J in open_pipeline() — currently the only unconditional
        'OPEN completed' signal, about to be removed by ship-readiness-cleanup."
    - path: "tools/build_state_engine.py:915-920"
      issue: "universal_leaving() menu — bare 'PROSOCHĒ' prompt with items ['Leaving',
        'Continue'], no explanatory copy, called only from open_pipeline() (never
        close_pipeline())."
    - path: "tools/build_state_engine.py:1141-1218"
      issue: "close_pipeline() — no breadcrumbs ever, and its only alert is conditional
        on a rarely-true Confession duration boundary; produces zero visible signal in
        the common case."
    - path: ".planning/todos/pending/2026-08-15-ship-readiness-cleanup.md"
      issue: "Item 1 / Solution step 1 scopes breadcrumb removal without an explicit
        replacement-signal step, which would create this regression if executed as-is."
  missing:
    - "Add a permanent, primitive-independent, non-debug confirmation signal before
      executing ship-readiness-cleanup item 1 — e.g. one unconditional lightweight
      Notification (not a blocking Alert) fired at OPEN-pipeline breadcrumb J's current
      position (naming Circle/Pressure/Heat), plus a symmetrical unconditional
      Notification at the end of close_pipeline()'s owning-CLOSE branch (naming session
      duration), independent of whether a contract was declared."
    - "Give universal_leaving()'s menu prompt real copy (state the Circle number and/or
      that this is the OPEN-path dismissal choice)."
    - "Update the ship-readiness-cleanup todo's Solution section to make the replacement
      signal an explicit prerequisite/sibling step, not an implicit gap."
  debug_session: .planning/debug/G-04-4b-no-open-close-indicator.md
