# PROSOCHĒ — Nine Circles

Two native iOS Shortcuts are distributed here:

- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` is fully deterministic.
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` adds one optional Apple Intelligence contract audit in Circles II–VIII.

Their editable unsigned sources are `src/PROSOCHE-Dumb.xml` and `src/PROSOCHE-Sentient.xml`; the source filenames deliberately keep the older fork words. Dated pre-sign archives and SHA-256 values are in `artifacts/shortcuts/MANIFEST.md`.

The two forks were previously named `Dumb` and `Sentient`. **The rename is a breaking change for an existing install:** a signed `.shortcut` carries no display name inside it, so the filename is the library entry's name, and the two Personal Automations that drive PROSOCHĒ keep pointing at the old entry. Nothing can re-point them — open each automation and select the new shortcut by hand.

## Privacy and limits

Core behaviour is local and has no external analytics or network dependency. Sentient sends only the current voluntary intention/boundary, Circle, Heat, open count, and—at Circles VII–VIII only—the recorded prior-contract result to Apple's selected model; it never reads the Control Room Note or app contents. Empty, malformed, or completed-slow model output continues the deterministic Dumb path. It cannot control state arithmetic, thresholds, timers, exits, or Ice.

This is self-directed and bypassable: users can decline AI, choose not to use the Shortcut, or disable an automation. The source pins the device-evidenced `Apple Intelligence on Device` model literal, but final real-device import/run evidence remains required before claiming device behaviour.
