---
status: testing
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
source: [11-VERIFICATION.md]
started: 2026-08-18T16:40:00Z
updated: 2026-08-18T16:40:00Z
blocker: DIST-03
build_identity:
  commit: 7352886
  core: "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut — 231148 bytes — SHA-256 873fa3dbda7b1f3440bfc76997c2962198ddec2052096833787547b52f129f10"
  aware: "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut — 238095 bytes — SHA-256 4b7c2cfbddf0dccf47ef8e34209378faf14ca2d760dc089013d3b033ebd2ada0"
  note: >-
    Copied from artifacts/shortcuts/MANIFEST.md's live rows, which `python3 docs/manifest_check.py`
    proves against disk. Re-verify before trusting any outcome recorded here — if these do not
    match, the artifact moved and every result below is void.
---

## Current Test

number: 1
name: Drive Dim and Silence on a real iPhone and observe capture-and-restore
expected: |
  The device visibly changes (brightness and volume), the original value is on disk in
  `settings_snapshot.<group>.original_value` BEFORE the change is applied, and the original is
  restored on CLOSE.
awaiting: a connected iPhone (DIST-03)

## Device availability — measured, not assumed

Re-measured 2026-08-18 at the close of phase 11 via `xcrun devicectl list devices --json-output`:

| field | value |
|---|---|
| name | `dougal` |
| model | `iPhone16,1` (iPhone 15 Pro) |
| `pairingState` | `paired` |
| `tunnelState` | **`unavailable`** |
| `transportType` | **`none`** |

**The blocker is real and its reason is specific: the known device has no live tunnel and no
active transport — there is no session to drive.** It is not that no device exists. Per
`.claude/CLAUDE.md`'s standing instruction, branch on `tunnelState` read from the JSON output,
never on the `State` column, which has read `available (paired)` while the tunnel was down.

## Relationship to 16-UAT.md

**Tests 1 and 2 below overlap `16-UAT.md`'s twelve tests and should be run in the same session.**
`16-UAT.md` is the fuller instrument for the capture-and-restore loop; it was re-pinned to this
phase's artifacts in commit `7352886`. Run `16-UAT.md` first, then use this file for the items it
does not cover (tests 3–5).

**Why this matters more after phase 11 than before it.** Plan 11-08 made 44 environmental actions
per fork reachable for the first time since either function was written. Before it, running these
tests would have observed *nothing happening* — and that could have been read as passing. Phase 11
changes what the UAT is testing, and nothing about its outcome.

## Tests

### 1. Dim and Silence capture-and-restore on hardware
expected: The device changes; the original is persisted before the change is applied; the original
is restored on CLOSE. Verify **the value applied**, never merely the absence of an error —
`setbrightness.WFBrightness` is OPTIONAL and an unresolved operand silently applies 50%.
why_human: `Set Brightness` cannot execute on a simulator at all (returns "There was a problem
setting the brightness"), and `Get Device Details → Current Brightness` reads `0` there.
`.claude/CLAUDE.md` §9, rung 2's ceiling.
result: [pending — BLOCKED on DIST-03]

### 2. Panic Escape removal and restoration via a real Apple Note edit
expected: Both directions work. Specifically, no false "Nothing was changed." on the removal path —
that message on a successful-looking run is the exact defect plan 11-07 closed structurally.
why_human: `com.apple.mobilenotes` is absent from the booted simulator's 25 apps, so the entire
Note path is rung 3+. The `text.match` consumption shape was settled at rung 2 (both shapes
equivalent, contains-test TRUE) but that is a simulator result about list consumption, not a device
result about reading the real Note.
result: [pending — BLOCKED on DIST-03]

### 3. Reach Intention on the Aware fork via BOTH OPEN-arm renderings
expected: A contract audit fires on each rendering, and the on-device model source is honoured.
why_human: Apple Intelligence is inside rung 2's ceiling — the simulator is not AI-capable
hardware. Plan 11-09 made the audit count 2 per fork structurally; whether both actually fire is
device-gated.
result: [pending — BLOCKED on DIST-03]

### 4. Note binding and re-creation (BOOT-08)
expected: No duplicate Note after run 2; the full body is recreated after deletion.
why_human: Runtime re-binding is not derivable from the plist.
result: [pending — BLOCKED on DIST-03]

### 5. Note append atomicity under interruption
expected: At-most-one-note-bound-per-run, and nothing stronger. Do not record a stronger property
than was observed.
why_human: A negative runtime property; declared `verification: backstop`.
result: [pending — BLOCKED on DIST-03]

### 6. Disposition of 16-UAT.md's stale build-identity pin
expected: Re-pinned to the current digests, or explicitly recorded as superseded with a pointer to
where the current identity lives.
why_human: A maintenance decision about the phase's own device instrument, not a code fact.
result: **RESOLVED 2026-08-18, commit `7352886`** — re-pinned. `16-UAT.md` now carries Core
231148 / `873fa3db…` and Aware 238095 / `4b7c2cfb…`, copied from MANIFEST's live rows and proved
against disk by `docs/manifest_check.py`. The phase-16 values are left in git history rather than
restated. No device session needed.

## Summary

total: 6
passed: 0
issues: 0
pending: 0
skipped: 0
blocked: 5
resolved_without_device: 1

## Gaps

None recorded. All five outstanding items are blocked on DIST-03 rather than failed — nothing here
has been observed and found wanting, and nothing may be recorded as passing on structural evidence.
