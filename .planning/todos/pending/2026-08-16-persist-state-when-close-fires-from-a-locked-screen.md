---
created: 2026-08-16T20:35:00.000Z
title: Persist state when CLOSE fires from a locked screen
area: general
severity: major
files:
  - src/PROSOCHE-Dumb.xml
  - src/PROSOCHE-Sentient.xml
  - tools/build_state_engine.py
  - docs/BUILD-NOTES.md
---

## Problem

Spike 002 (`.planning/spikes/002-close-automation-vs-screen-lock/`) established on device
that **locking the screen does fire the CLOSE Personal Automation**, same as switching
apps. That question is closed — see the spike for evidence.

It surfaced a second, separate problem in the process, which this todo owns:

**When the shortcut runs from an automation and tries to touch iCloud storage, iOS raises
a privacy-permission prompt on every single run — "Always Allow" does not stick.** When the
trigger was a screen lock, the prompt came back as *"this shortcut requires privacy
permissions that cannot be granted while your device is locked."*

Observed during spike 002 across four probe builds:

- Reproduces with plain app open/close, **no locking involved** — so it is not purely a
  locked-screen artifact, though the locked case additionally cannot be granted at all.
- Reproduces after removing an unconditional `is.workflow.actions.file.createfolder` from
  the hot path (that was a hypothesis; removing it did not fix it).
- The probe's log file was rewritten rather than appended each run, consistent with the
  `Get File` read silently failing every time and the shortcut falling through to its
  "no existing content" branch.

## Why this matters

Production PROSOCHĒ reads and writes `state.json` through the same
`is.workflow.actions.documentpicker.open` / `.save` pattern the probe used, on **every**
OPEN and CLOSE (`.planning/research/ARCHITECTURE.md` §4–5). If that pattern cannot complete
silently from an automation, then:

1. a permission prompt can appear on top of the lock screen during an ordinary CLOSE,
   violating the "automations must be silent / never prompt unseen" requirement
   (`.claude/CLAUDE.md` Safety; `.planning/research/PITFALLS.md` C10); and
2. session finalisation on CLOSE — nulling `active_session`, appending to
   `recent_sessions`/`recent_contracts`, restoring `settings_snapshot` — may silently fail
   to persist at exactly the moment it is needed.

Both are correctness problems for the CLOSE pipeline, not cosmetic ones.

## Open questions

- Does production PROSOCHĒ actually exhibit this, or did the probe differ in some material
  way? Prior debug cycles 16–18 verified the OPEN path end to end on device without this
  being reported — establish whether it was present and unnoticed, absent, or masked.
- Is the grant per-shortcut and reset by delete/re-import (the probe was re-imported many
  times), or genuinely non-persistent across automation runs?
- Does the prompt originate from `documentpicker.open`, `documentpicker.save`, or both?
  Bisect them.
- Is there a storage path that avoids the prompt entirely from an automation context?

## Notes

Ruled out during the spike, do not re-try as fixes:

- **Notes actions** — `Create Note` imported as "unknown action"; `Filter Notes` /
  `Append to Note` popped an interactive picker on device and wrote nothing.
- **Notification Center as the store** — read-only to the user, cannot be read back by the
  shortcut, so it cannot back `state.json`. Usable as a diagnostic display only.
- **Removing the unconditional Create Folder** — tried, did not resolve the prompt.
