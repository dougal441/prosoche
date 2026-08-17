---
created: 2026-08-17T16:20:00.000Z
title: Phase 12 device UAT — exit-recording path (12-UAT.md), blocked on DIST-03
area: general
severity: blocker
files:
  - .planning/phases/12-state-shape-sentinel-gaps-exit-events-and-active-session/12-UAT.md
  - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut
  - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut
---

## Problem

`12-UAT.md` — the seven-test device UAT for the exit-recording path
(`record_exit_and_route()`, `route_exit()`'s six routes including the `create_target_url`
gate, and `restore_managed_settings()` reached from `close_pipeline()`'s owner arm) — is
authored and cold-runnable but **blocked** on DIST-03. `xcrun devicectl list devices`
reported `No devices found.` on 2026-08-17, the same underlying connectivity gap that has
held DIST-03 open since Phase 8 and blocked `09-UAT.md` and `10-UAT.md`.

This is this phase's **highest-risk untested surface**: the exit-recording path has zero
device evidence at any rung, at any point in this project's history. The closed
2026-08-13/14 OPEN-path debug session reached breadcrumb J on the OPEN path only.

## Artifacts under test

Confirm, when resuming this todo, that the build has not drifted before trusting any test
result recorded against it — recompute both hashes and compare:

| Fork | Path | SHA-256 |
|---|---|---|
| Core | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` | `d1377102f6ad45a084a4467ae72d82d5dc27fbb1e1d31bda30d47bb124750a59` |
| Aware | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` | `e2a56bf2b6bc76ef57aa7013d267b77e33172a65dae1d9eca2d20540b6618719` |

Both signed at commit `ea7a0f409aa5707e25111ac8227a761689839d1e`.

If the hashes no longer match `artifacts/shortcuts/MANIFEST.md`, re-sign fresh artifacts and
update `12-UAT.md`'s header (and this todo's table) with the new values before running the
tests — do not run an outdated UAT document against a newer build, or a newer UAT document
against these older artifacts.

## Solution

1. Confirm a device is reachable: `xcrun devicectl list devices` reports at least one
   device, or iPhone Mirroring is live.
2. Follow `12-UAT.md`'s Setup section exactly (fresh install both forks, delete
   `state.json`, (re)point both Personal Automations).
3. Run all seven tests, including Test 2's seven sub-observations (all six exit routes plus
   the Create clean-install / Create-reuse pair) — this is the test that exercises
   `route_exit()`'s Create branch gate for the first time on real hardware.
4. Record every outcome in `12-UAT.md` directly — never infer a result from a simulator run
   or from the decrypted-artifact structural evidence Task 1 already produced.
5. Update this phase's `## Verdict` section once all seven outcomes are recorded.
6. Close this todo and check DIST-03 in `.planning/REQUIREMENTS.md` only once every test in
   `12-UAT.md` carries a real outcome.

## Related

- `.planning/phases/12-state-shape-sentinel-gaps-exit-events-and-active-session/12-UAT.md` —
  the seven tests this todo tracks.
- `.planning/todos/pending/2026-08-16-device-uat-nine-circles-and-sequence-switching.md` —
  the running meta todo this UAT's Circle-firing observations should also feed.
- `.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md` — the
  no-fabrication precedent this UAT follows (ten tests, zero passed, all blocked).
- Run via `/gsd-verify-work 12` once a device is reachable.
