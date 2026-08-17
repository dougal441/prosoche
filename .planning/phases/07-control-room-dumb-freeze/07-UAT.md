---
status: testing
phase: 07-control-room-dumb-freeze
source: [07-LIGHT-SUMMARY.md]
started: 2026-08-16T00:15:00.000Z
updated: 2026-08-16T00:15:00.000Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: 1
name: Status shows real numbers
expected: |
  The Status menu item shows real numbers, not blanks — the axis-2 empty-field defect
  presented exactly as plausible-looking blank text.
awaiting: user response

## Context

Exactly one manual-menu item has any device evidence — `Open Control Room` — and even that
is **partial**: the closing device report of the `open-routing-sequence-error` session did
not explicitly confirm the `filter.notes` fix (Finding 2), so "does a note picker still
appear?" remains locally verified only. Every other menu item is untested on iPhone.

The menu is the product's entire administrative surface (§18): Status, Open Control Room,
Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today,
Emergency Restore (plus Toggle On-Device AI / Test Model, out of scope here — Sentient
only).

Two items carry outsized risk. **Emergency Restore** is the designed escape hatch (§21) —
if it doesn't work, every other safety argument in the product is void, since it's what
makes stateful friction defensible at all. **Test a Circle** is the harness Phase 5's UAT
depends on, and it was itself broken on device once (the `sequence` Set Dictionary Value
error) — confirm it here before trusting it there.

This UAT also owns §32's **Safety** acceptance criteria that are recovery-shaped rather
than menu-shaped: corrupt/missing `state.json` and a deleted Control Room Note must each
self-heal rather than fail, from all three invocation modes (manual, OPEN, CLOSE).

Do this before stripping debug scaffolding, so failures stay localisable.

Canonical strategy §18 (manual run/menu), §21 (Emergency Restore), §17 (Note structure),
§7.3 (profile sync), §32 (Bootstrap and Safety acceptance criteria).

## Tests

### 1. Status shows real numbers
expected: real numbers, not blanks (watch for the axis-2 empty-field defect).
result: pass
note: "Device, 2026-08-17 11:15, Core b07497ba, clean install. Status rendered:
  Fork: Core / Profile: Purgatory / Sequence: Classic / Voice: Yes /
  Circle (0 means the silent band: recorded, nothing shown): 1 / Pressure: 0 /
  Cool-down until: <blank>. Every field but the last holds a real value, so the axis-2
  empty-field defect is NOT present on this path. Independently cross-checked against
  state.json written by the same run: circle=1, pressure=0 — the UI and the file agree.
  ONE RESIDUAL AMBIGUITY, deliberately not resolved: `Cool-down until:` is blank. On clean
  state no cooldown exists (state.json confirms `cooldown_until: null`), so blank is
  legitimate — but a legitimately-empty field and an axis-2 empty envelope are
  indistinguishable here. Re-read Status while a cooldown is actually live (i.e. after
  reaching Ice) to disambiguate. Recorded as pass because the six populated fields are the
  test's actual assertion."

### 2. Open Control Room — no stray note picker
expected: opens the Note directly; explicitly confirm no note picker / list of every note
appears (the outstanding Finding-2 check).
result: fail
severity: blocker
note: "Device, 2026-08-17 11:16-11:28, Core b07497ba, clean install (iCloud Shortcuts folder
  observed EMPTY beforehand; no Apple Note titled PROSOCHĒ). TWO failures, both worse than
  the test as written anticipated.
  (a) The stray picker fires on the *Status* path, not just Open Control Room — a full iOS
  Note chooser over every note in the library. `tools/build_state_engine.py:2073` states
  'Status never writes to the Note', so this path should not touch Notes at all.
  (b) Open Control Room opened the WRONG note — an unrelated personal note
  (`/gsd-phase \"Build v2 stakeholder addendum\"`), which was the first row of that same
  chooser. Searching all of Notes for `PROSOCH` returned `Notes — None Found`: no Control
  Room Note was created at all.
  The cycle-16 fix is NOT at fault and DID ship — the signed container was decrypted and its
  single filter.notes (action 4175) carries AppIntentDescriptor(NoteEntity) +
  WFContentItemLimitEnabled=True + WFContentItemLimitNumber=1.0, and the predicate is
  well-formed (Operator 99, Property Name, WFTextTokenString 'PROSOCHĒ' with correct U+0112).
  Distinguishing experiment run on device: a note titled exactly PROSOCHĒ was created BY HAND,
  Open Control Room was re-run, and it then found and opened the correct note. So the filter
  works; the defect is confined to the ZERO-MATCH path, where the create-note branch
  (action 4192, name='PROSOCHĒ') never fires and the empty result is dereferenced anyway.
  This is the axis-7 'shape must exist before it is read' class applied to the Note.
  Blocker rather than major because all four appendnote sites write to the same
  `Control Room Note` variable, so a clean install is positioned to append PROSOCHĒ state
  into an arbitrary personal note — silent user-data corruption.
  CORRECTION, same session ~11:39, user-run: after deleting the hand-made note AND emptying it
  from Recently Deleted, `Open Control Room` CREATED the Control Room Note correctly and fully
  populated. So the create branch DOES work, and the 'create never fires' reading recorded
  earlier is refuted. The two failing observations above stand exactly as written, but the
  cause is now believed to be that the slate was not as clean as it appeared: Notes search does
  NOT cover Recently Deleted, this device has many prior test cycles behind it, and a PROSOCHĒ
  note sitting in Recently Deleted would explain a found-branch over an unresolvable entity.
  OPEN QUESTION, and the thing to test next: does is.workflow.actions.filter.notes match notes
  in Recently Deleted? If yes, any user who deletes the Note without purging lands in the broken
  state. Full analysis and the experiment that settles it:
  .planning/todos/pending/2026-08-17-note-entity-chooser-on-clean-install.md
  SECOND CORRECTION (2026-08-18, fresh install, everything wiped, Recently Deleted purged):
  `Open Control Room` was chosen as the VERY FIRST action, before Status or anything else. The
  PROSOCHĒ Note WAS created and fully populated (READ THIS FIRST + setup instructions) — AND the
  stray Note chooser appeared ANYWAY, this time with PROSOCHĒ itself as the first row. So BOTH
  standing hypotheses are refuted: it is not caused by choosing Status first (the user's
  hypothesis), and it is not caused by the Note being absent (mine). Selecting PROSOCHĒ from the
  chooser let the run finish and the Note opened correctly.
  On the NEXT run of the same build, no chooser appeared at all. Intermittent, and the ordering
  (create -> chooser) points at a RACE: a freshly created Note is not yet returned by
  filter.notes, so a same-run re-resolve finds nothing and iOS falls back to asking. That is the
  hypothesis to test next, and it is testable without a device by inspecting whether the created
  note's output is reused or re-queried.
  Test 2 therefore remains FAIL — a stray picker over every user note does appear — but the
  trigger is narrower and more intermittent than first recorded."

### 2b. NEW FINDING — an Ask for Input with no prompt text
expected: not covered by any existing test; recorded here because it was observed on the
  Open Control Room path.
result: fail
severity: minor
note: "Device, 2026-08-18, fresh install. Immediately after selecting the Note from the stray
  chooser, a text-entry sheet appeared with Cancel/Done and a bare placeholder reading `Text`,
  and NO prompt text above it. A user has no way to know what is being asked for. Zoomed and
  confirmed the prompt area is genuinely empty rather than merely truncated. Cancelled rather
  than submitting arbitrary text; the run still completed and the Note opened correctly.
  NOT an axis-2 Ask defect — that first reading was checked and REFUTED. All 26
  is.workflow.actions.ask sites in the decrypted artifact carry a non-empty WFAskActionPrompt
  ('Where should Create open?', 'What are you trying to find?', 'What are you reaching for?
  (optional)', 'How many minutes?'). None is blank, so this sheet is not an Ask action.
  BETTER EXPLANATION, and it unifies this with Test 2's chooser: both are iOS AppIntent
  PARAMETER-RESOLUTION prompts against the same unresolved `appendnote`. iOS asks the user to
  supply whatever an AppIntent parameter could not resolve — first the `entity` (presented as the
  'Note' chooser), then the `text` (presented as a bare box whose placeholder is literally the
  parameter's name, 'Text'). One root cause, two prompts, in parameter order.
  That reading also explains why the sheet was tinted like Notes and why it appeared immediately
  after the chooser was answered. Records this as ONE defect with two surfaces rather than two
  independent ones — which matters, because fixing the note resolution should remove both."

### 3. Sync My Profile extracts correctly and stays scoped
expected: extracts the `MY PHONE, ON PURPOSE` section and mirrors it into state.json
(§7.3); confirm it does not parse the whole Note on this path.
result: pending

### 4. Change Profile persists and changes Circle mapping
expected: persists, and demonstrably changes subsequent Circle mapping (cross-check
against Phase 5's UAT).
result: partial
note: "Device, 2026-08-18 07:59-08:01. PERSISTENCE PASSES. The `Choose profile` menu offers all
  three — Paradise / Purgatory / Inferno. Selected Inferno (from Purgatory); a follow-up Status
  reads `Profile: Inferno`, and the same Status independently confirms `Sequence: BlackMirror`
  from Test 5, so both settings persist together without clobbering each other.
  MAPPING HALF NOT DEMONSTRATED: profile governs the pressure->Circle THRESHOLDS, and pressure is
  0 on this clean state, so no threshold crossing was exercised. Proving it needs accumulated
  Pressure via real OPENs, which needs the automations. Not claimed here.
  FALSE ALARM, recorded so it is not re-raised: the save-permission dialog's JSON preview still
  read `\"profile\":\"Purgatory\"` immediately AFTER Inferno was chosen. That looked like the
  selection failing to apply, but Status then showed Inferno — the preview is of an earlier
  save within the same run, not of the final state. Do not read that dialog as the post-change
  state."

### 5. Change Sequence persists and changes Circle mapping
expected: persists, and demonstrably changes which primitives fire per Circle
(cross-check against Phase 5's UAT).
result: pass
note: "Device, 2026-08-18 07:54. The `Choose sequence` menu offers all three — Classic,
  BlackMirror, Ambient. Selected BlackMirror; the change persisted through the run.
  DEMONSTRABLY changed the mapping, and the proof is unusually clean because the Mirror defect
  acted as the probe: under `Classic`, Circle 7 (Mirror) fails the axis-4 error and Circles 1
  and 9 fire; after switching to `BlackMirror`, Circle 4 — the position BlackMirror maps to
  Mirror — fails with the IDENTICAL error. The failure moved with the primitive when the
  sequence changed, which is exactly the 'demonstrably changes which primitives fire per Circle'
  assertion this test makes. Recorded as pass on that evidence."

### 6. Toggle Voice persists and gates The Voice
expected: setting persists and actually gates whether The Voice primitive speaks.
result: partial
note: "Device, 2026-08-18 07:51-07:53. PERSISTENCE HALF PASSES: Toggle Voice was run twice; the
  save-permission dialog rendered the outgoing state.json both times, showing `voice_enabled:0`
  on the first and `voice_enabled:1` on the second, and a subsequent Status confirmed the value
  had stuck. So the toggle writes and persists.
  GATING HALF UNTESTED: whether it actually gates The Voice primitive speaking was not exercised
  — the primitive that would speak was not reached.
  DEFECT FOUND ON THIS PATH, recorded rather than deferred: Status now reads `Voice: 1` where the
  clean bootstrap read `Voice: Yes`. Bootstrap writes `voice_enabled` as the JSON boolean `true`;
  Toggle Voice rewrites the same key as the NUMBER 0/1. The Status renderer maps booleans to
  Yes/No and passes numbers through raw, so the display silently degrades after the first toggle.
  This is the axis-6 boolean-vs-number coercion hazard with a visible symptom, and `state.json`
  shows the same inconsistency at bootstrap for `panic_escape_enabled` (number 1) alongside
  `voice_enabled` (boolean true). Any downstream condition comparing these as booleans or strings
  is a latent runtime failure."

### 7. Test a Circle — all nine selectable and firing
expected: all nine fire on demand without altering real Pressure.
result: fail
severity: blocker
note: "Device, 2026-08-17 11:30 and again 11:33, Core b07497ba. SELECTABLE: yes — all nine
  render in one menu with the Build-Addendum-01 Dante names (Circle 1 · Limbo, 2 · Lust,
  3 · Gluttony, 4 · Greed, 5 · Wrath, 6 · Heresy, 7 · Violence, 8 · Fraud, 9 · Treachery) and
  all nine fit on screen without scrolling. FIRING: no. Choosing `Circle 7 · Violence` — the
  position the `Classic` sequence maps to Mirror — produced the runtime error
  'Please choose a value for each parameter in this action.' and the primitive never ran.
  Reproduced deterministically twice. This is the axis-4 signature (`.claude/CLAUDE.md`
  Conventions rule 4: an unfilled required picker reports exactly this string).
  NOT the two known axis-4 instances: the decrypted artifact was checked and all 69
  getitemfromlist sites carry WFItemSpecifier and the single count site carries WFCountType,
  so the unfilled parameter is a THIRD, previously unrecorded instance.
  Not yet localised. Tapping the error's `Show` scrolls the editor toward the offending
  action, but across a 4346-action list the animation drifts and the highlight could not be
  pinned in this session. Leading suspect, unproven: the 22
  `is.workflow.actions.getdevicedetails` sites, which carry key `WFDeviceDetail` with literals
  'Current Brightness' / 'Current Volume' — a key/literal pair `.claude/CLAUDE.md` capability
  audit item 8 records as UNVERIFIED ('the exact WFDeviceDetailsProperty string is not
  documented ... do not guess'). The editor settled on 'Get the Current Brightness' /
  'Set variable Captured Brightness' on the first Show. A breadcrumb build is the way to settle
  it — do not fix on this suspicion alone.
  Scope UNKNOWN: only Circle 7 was exercised before the session ended. Whether the other eight
  Circles fail identically is untested and is the first thing to establish on the next run,
  because it separates 'one primitive is broken' from 'the shared dispatch preamble is broken'."

### 7b. SCOPE — established on a second, fresh install (2026-08-18)
note: "The device was wiped, the Core artifact re-airdropped and reinstalled, and both
  automations rebuilt. Circle 7 FAILED AGAIN, identically — third reproduction, and the first
  two were on a different install. That settles it: the defect is in the SHIPPED ARTIFACT, not
  an artefact of any editor interaction.
  Then the other Circles were probed, which is the discriminator Test 7 needed:
    - Circle 1 · Limbo  -> WORKS. Alert titled `PROSOCHĒ`, body `Circle 1 · pressure 0 · heat 0`
      — non-empty, with both numeric facts correctly substituted and matching clean state.
    - Circle 3 · Gluttony -> ran to completion with NO visible alert and no error. Unclassified:
      consistent with a deliberately silent primitive (Dimming/Silence change no UI) but equally
      consistent with a silent no-op. Not called either way here.
    - Circle 7 · Violence -> FAILS, 'Please choose a value for each parameter in this action.'
    - Circle 9 · Treachery -> WORKS. The device was ejected to the Home Screen, which is the
      expected Exile/Ice-shaped behaviour (note `is.workflow.actions.lockscreen` appears 0 times
      in the decrypted artifact, so Home-Screen ejection rather than Lock Screen is what this
      build actually implements).
  CONCLUSION, and it is the useful one: the shared dispatch preamble is NOT broken — if it were,
  Circle 1 and Circle 9 could not fire. The unfilled picker is on the MIRROR primitive
  specifically, which on the `Classic` sequence is Circle 7. That is a much tighter search area
  than 'somewhere in 4346 actions'.
  Still not covered: Circles 2, 4, 5, 6, 8."

### 7c. Consequence for Phase 13
note: "Because Mirror is precisely the primitive that fails, 13-UAT.md Tests 1 and 2 cannot be
  answered at all on this build — the alert never renders, so there is no body to judge empty or
  populated. The WFItems wrapper question is gated behind this axis-4 fix, not refuted by it."

### 8. Reset Today resets counters without destroying history
expected: behavioural day's counters reset; historical data (contracts, sessions, etc.) is
not destroyed.
result: pending

### 9. Emergency Restore — while in Ice
expected: clears cooldown, clears active session, restores any managed setting — tested
*while actually in Ice*, not from a clean state (a clean state proves nothing).
result: pending

### 10. Emergency Restore — while a session is active
expected: same guarantees hold when triggered mid-session.
result: pending

### 11. Idempotence across repeated manual runs
expected: running the menu repeatedly never overwrites existing state or creates a second
Control Room Note — exactly one Note exists afterward.
result: pending

### 12. Recovery — deleted Control Room Note
expected: next run recreates it, populated, without crashing.
result: pending

### 13. Recovery — malformed JSON state.json
expected: safe recovery, not a hard error.
result: pending

### 14. Recovery — valid-JSON-but-wrong-schema state.json
expected: safe recovery, not a hard error.
result: pending

### 15. Recovery — state.json deleted entirely
expected: bootstrap re-runs cleanly.
result: pass
note: "Device, 2026-08-17 11:10-11:15, Core b07497ba. Precondition was genuinely clean and was
  verified before the run, not assumed: Files → iCloud Drive → Shortcuts was observed EMPTY —
  no PROSOCHE folder, no state.json at all. A manual run then completed bootstrap with no
  error dialog and reached the manual control menu, whose prompt text rendered in full.
  Afterwards Files showed Shortcuts → PROSOCHE → state.json (2 KB), and its contents parse as
  well-formed JSON at schema_version 4 with every container seeded. So bootstrap-from-nothing
  both runs cleanly AND writes correct state — the stronger of the two readings.
  Caveat, recorded so it is not over-claimed: this exercised the MANUAL invocation mode only.
  Test 16 (the same recovery from OPEN and CLOSE) remains untested."

### 16. Recovery cases hold across all three invocation modes
expected: tests 12–15 each re-verified from manual, OPEN, and CLOSE invocation — the
self-healing chain was deliberately hoisted above the router for exactly this reason.
result: pending

## Summary

total: 16
passed: 3        # T1, T5, T15
partial: 2       # T4 (persists; mapping half unproven), T6 (persists; gating half unproven)
failed: 3        # T2 (stray Note prompts), T2b (unprompted text box, same root cause), T7 (Mirror axis-4)
pending: 9       # T3, T8, T9, T10, T11, T12, T13, T14, T16
issues: 3

## Session log

- 2026-08-17 — first device session, Core b07497ba, first install.
- 2026-08-18 — device wiped, artifact re-airdropped, automations rebuilt; all
  2026-08-17 results that were re-tested reproduced identically.
