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
  .planning/todos/pending/2026-08-17-note-entity-chooser-on-clean-install.md"

### 3. Sync My Profile extracts correctly and stays scoped
expected: extracts the `MY PHONE, ON PURPOSE` section and mirrors it into state.json
(§7.3); confirm it does not parse the whole Note on this path.
result: pending

### 4. Change Profile persists and changes Circle mapping
expected: persists, and demonstrably changes subsequent Circle mapping (cross-check
against Phase 5's UAT).
result: pending

### 5. Change Sequence persists and changes Circle mapping
expected: persists, and demonstrably changes which primitives fire per Circle
(cross-check against Phase 5's UAT).
result: pending

### 6. Toggle Voice persists and gates The Voice
expected: setting persists and actually gates whether The Voice primitive speaks.
result: pending

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

### 7b. NOT covered by this run
note: "Circles 1-6, 8 and 9 were never exercised. Test 7 above is recorded fail on the strength
  of Circle 7 alone; it is not evidence about the other eight."

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
passed: 0
issues: 0
