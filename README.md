# PROSOCHĒ — Nine Circles

An iPhone Shortcut that restores the missing interval between the impulse to open a habit-forming app and the act of consuming it. The design (canonical strategy v2, 2026-08-19) is the **covenant model**: behavioural Pressure maps to nine Circles in four bands — Silent, Ambient, Ask, Rescue — and a declared intention with a boundary *covers* opens inside its window so they fire nothing at all. Silence is the reward for deliberate, bounded use. The full spec is `PROSOCHE_Nine_Circles_Canonical_Strategy.md`.

Two native iOS Shortcuts are distributed here:

- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` is fully deterministic.
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` adds one optional Apple Intelligence contract audit.

**Build state:** the currently signed artifacts implement the v1 interaction model; the covenant conversion (roadmap Phases 17–20) is in progress. Their editable unsigned sources are `src/PROSOCHE-Dumb.xml` and `src/PROSOCHE-Sentient.xml`; the source filenames deliberately keep the older fork words. Dated pre-sign archives and SHA-256 values are in `artifacts/shortcuts/MANIFEST.md`.

The two forks were previously named `Dumb` and `Sentient`. **The rename is a breaking change for an existing install:** a signed `.shortcut` carries no display name inside it, so the filename is the library entry's name, and the two Personal Automations that drive PROSOCHĒ keep pointing at the old entry. Nothing can re-point them — open each automation and select the new shortcut by hand.

## Privacy and limits

Core behaviour is local and has no external analytics or network dependency. Aware sends only the current voluntary intention/boundary, Circle, Heat, open count, and the recorded prior-contract result to Apple's selected model; it never reads the `PROSOCHĒ` Note or app contents, and a covered open makes no model call at all. Empty, malformed, or completed-slow model output continues the deterministic Core path. The model cannot control state arithmetic, thresholds, timers, coverage, exits, or Frozen.

This is self-directed and bypassable: users can decline AI, choose not to use the Shortcut, or disable an automation. The source pins the device-evidenced `Apple Intelligence on Device` model literal, but final real-device import/run evidence remains required before claiming device behaviour.

## License

**PolyForm Noncommercial 1.0.0**, copyright (c) 2026 Dougal Hanson (see `LICENSE`): free for any noncommercial purpose — personal use, forking, sharing, study. Commercial use is not licensed. This licence applies going forward from 2026-08-19; versions published before that date (through git tag `pre-covenant-overhaul`) were released under MIT and remain so. PROSOCHĒ is free for personal use, permanently — no feature gate, no ads, no data sale, no telemetry leaving the device.
