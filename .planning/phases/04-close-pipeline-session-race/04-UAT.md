---
status: diagnosed
phase: 04-close-pipeline-session-race
source: [04-01-SUMMARY.md]
started: 2026-08-16T00:10:00.000Z
updated: 2026-08-16T09:45:00.000Z
---

## Current Test

[testing complete]

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

## Tests

### 1. Simple OPEN → wait → CLOSE records a plausible session
expected: state.json's `recent_sessions` gets a new entry with a plausible duration after
open → wait → close.
result: issue
reported: "i can now see a session id in the state.json but declared duration seconds is
  :0 so maybe that didn't work, so valid session yes, but is going to have to be fixed
  later down the line"
severity: major

### 2. CLOSE with no active session does not corrupt state or error
expected: closing when nothing is open produces no error dialog and no state corruption.
result: pass

### 3. The session race — rapid switching between two tracked apps (§20 steps 2–6)
expected: open A, open B, close A, close B (scripted deliberately, not left to chance) —
if the active session ID changed, the newer OPEN owns state and the older CLOSE aborts
without mutating state. This is the single most important case and the hardest to trigger
by hand.
result: issue
reported: "doesnt look like the session id has changed once. i switched a to b to a close.
  open b to a to b. it kind of looks like it gets open, and gets close (because i get a
  menu popup) and then it's not doing next open? but, it's also hard to tell because we
  still have the test hardware pre-circles."
severity: major

### 4. CLOSE after device lock / app switch away
expected: this different trigger path also records correctly and does not corrupt state.
result: skipped
reason: "User: couldn't test — no reliable indicator of experiencing a Circle (which would
  confirm OPEN or CLOSE ran). Blocked on Ship-readiness cleanup for PROSOCHĒ Dumb
  (post-OPEN-path-closure, todo backlog item) to remove trace breadcrumbs first. While
  investigating, user also hit a confusing 'Leaving / Continue' menu popup and was unsure
  what it indicated — see Gaps G-04-4b."

### 5. Behavioural-day boundary (§10.1, 04:00 rollover) crossed mid-session
expected: a session spanning the rollover is handled correctly, not double-counted or
dropped.
result: skipped
reason: "Session paused (user + Claude decision): no reliable on-device indicator that a
  Circle/OPEN/CLOSE actually fired (see G-04-4b). Deferred until Ship-readiness cleanup
  restores observability."

### 6. Verify the numbers in state.json, not just absence of errors
expected: after each case above, `recent_sessions`, `last_close_at`, and the cleared
`active_session` hold exactly what §20 says they should. "No error dialog" is not a pass —
recompute by hand for at least two cases.
result: skipped
reason: "Session paused (user + Claude decision): same observability gap as Test 5 (see
  G-04-4b) — cannot reliably verify individual case numbers without confirming OPEN/CLOSE
  fired."

## Summary

total: 6
passed: 1
issues: 2
pending: 0
skipped: 3

## Gaps

- gap_id: G-04-1
  truth: "state.json's recent_sessions gets a new entry with a plausible duration after
    open → wait → close."
  status: failed
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
  status: failed
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
  status: failed
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
