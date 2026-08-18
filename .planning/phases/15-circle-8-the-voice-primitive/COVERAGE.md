# Phase 15 — API Coverage Declaration

**Declared:** 2026-08-18
**Verdict:** No external API integration.

No external API integration: this phase edits local Python plist generators and structural checkers; the only "surface" is Apple's own Shortcuts action catalog, which is consumed via the bundled ToolKit snapshots, not called over a network.

## Reasoning

- **No network.** DIST-08 records that core functionality has no external network dependency. Nothing in `tools/build_state_engine.py`, `tools/build_sentient.py`, or any `docs/*_check.py` opens a socket.
- **No SDK, no package install.** `15-RESEARCH.md` § Package Legitimacy Audit records "not applicable — this phase installs no external packages." There is no npm, PyPI, or crates surface to audit.
- **No credentials, no secrets, no env vars.** Confirmed by `15-RESEARCH.md` § Runtime State Inventory ("Secrets / env vars: None").
- **The one "external" surface is a local data file.** `is.workflow.actions.speaktext`'s parameter set is read from
  `toolkit-v78-first-party-parameter-keys.json` and `toolkit-v63-tool-ids.json`, both shipped inside the installed Shortcuts Playground plugin. That is a file read, not an API call.
- **Signing uses macOS built-ins.** `shortcuts sign` (via `sign-shortcut`), `aea`, and `aa` are local binaries invoked as subprocesses.

## Consequence for planning

No API-integration task, no client-generation task, no auth/rate-limit/retry design work, and no
`user_setup` block appears in any Phase 15 plan.
