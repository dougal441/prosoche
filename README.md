# PROSOCHĒ — Nine Circles

Two native iOS Shortcuts are distributed here:

- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` is fully deterministic.
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` adds one optional Apple Intelligence contract audit in Circles II–VIII.

Their editable unsigned sources are `src/PROSOCHE-Dumb.xml` and `src/PROSOCHE-Sentient.xml`; dated pre-sign archives and SHA-256 values are in `artifacts/shortcuts/MANIFEST.md`.

## Privacy and limits

Core behaviour is local and has no external analytics or network dependency. Sentient sends only the current voluntary intention/boundary, Circle, Heat, and open count to Apple's selected model; it never reads the Control Room Note or app contents. Model output can be wrong, empty, unavailable, or slow, so each of those cases continues the deterministic Dumb path. It cannot control state arithmetic, thresholds, timers, exits, or Ice.

This is self-directed and bypassable: users can decline AI, choose not to use the Shortcut, or disable an automation. The source pins the device-evidenced `Apple Intelligence on Device` model literal, but final real-device import/run evidence remains required before claiming device behaviour.
