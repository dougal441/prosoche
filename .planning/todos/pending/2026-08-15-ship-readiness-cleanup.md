---
created: 2026-08-15T21:05:00.000Z
title: Ship-readiness cleanup for PROSOCHĒ Dumb (post OPEN-path closure)
area: general
severity: major
files:
  - tools/build_state_engine.py
  - artifacts/shortcuts/MANIFEST.md
  - .gitignore
---

## Problem

With the `open-routing-sequence-error` debug session closed and symptom 1 device-verified,
several small-but-real items remain before Dumb is ship-ready. None of these block or
were touched by the closed session, but none should be left living only as prose in a
now-archived debug file either.

1. **Debug scaffolding still ships.** `BUILD_STAMP`, `ROUTER_TRACE`, `OPEN_BISECT`, and
   the ten breadcrumb alerts are all single-constant toggles (search
   `tools/build_state_engine.py` for `OPEN_BISECT =`) that were deliberately kept ON
   throughout the debug session for on-device localisation. They must be stripped before
   any real ship.
2. **No `.gitignore`.** `.DS_Store` and `__pycache__` keep reappearing in `git status`
   (visible in this repo's own current status).
3. **`artifacts/shortcuts/MANIFEST.md` is stale** — still dated `2026-08-13` only, not
   updated across the 2026-08-14/15 cycles (deliberately left alone mid-session as
   out-of-scope; recorded in the resolved debug file's Process Note).
4. **Finding 2 (Control Room note-picker fix) is locally verified but NOT explicitly
   device-confirmed.** The final device report that closed symptom 1 covered the OPEN
   path only ("we got every single letter... Circle 1"); it did not report tapping
   "Open Control Room" to confirm the `filter.notes` result-bound fix
   (`WFContentItemLimitEnabled`/`Number` + `AppIntentDescriptor`, Donor-8-matched, cycle
   16). This is a one-tap manual check, not further code work — but it was never
   silently claimed closed and should be confirmed before ship.
5. **Brightness/volume MVP-cut decision, reaffirmed 2026-08-15, still not applied in
   code.** `restore_managed_settings`, `dim()`, `silence()`, and `settings_snapshot`
   still ship; the 18 uncoerced `setbrightness`/`setvolume` operand sites (same
   coercion-aggrandizement class as the fixed math/getitemfromlist sites) remain
   deliberately deferred. The scope decision itself needs to be actually executed —
   either cut the primitives per the user's decision, or finish the coercion fix if the
   decision changes.

## Solution

1. Strip `BUILD_STAMP`, `ROUTER_TRACE`, `OPEN_BISECT`, and the breadcrumb alerts from
   `tools/build_state_engine.py` (search for `OPEN_BISECT =` for the toggle location).
   Regenerate, validate, sign, decrypt-verify, and confirm the artifact still runs the
   OPEN path correctly on device (a real regression test against this session's own
   closed defect, since the scaffolding removal touches the same control-flow region).

   **Precondition now satisfied (2026-08-16, `.planning/phases/04-close-pipeline-session-race/04-03-PLAN.md`).**
   This step's own implicit assumption — that removing breadcrumb J and the rest of the
   `OPEN_BISECT` scaffolding leaves no on-device confirmation signal at all — no longer
   holds. OPEN and CLOSE each now carry a permanent, unconditional Notification
   confirmation, independent of `OPEN_BISECT`, any primitive, or a declared contract:
   `tools/build_state_engine.py`'s new `notification()` helper, called once from
   `open_pipeline()` (Circle/Pressure/Heat, right after the position breadcrumb J
   occupied) and once from `close_pipeline()`'s `owns_if` TRUE branch (session
   duration). Stripping the breadcrumb scaffolding is therefore safe to execute; it is
   still not executed by this note, and this todo's other four items remain open.

   **DONE 2026-08-16** — BUILD_STAMP/ROUTER_TRACE/OPEN_BISECT and all ten breadcrumb
   sites stripped from `tools/build_state_engine.py`; rebuilt, self-checked, validated,
   signed; MANIFEST.md Dumb rows refreshed. On-device OPEN-path regression confirmation
   remains blocked on DIST-03 (no connected iPhone via `xcrun devicectl`) — re-run once a
   device is available.
2. Add a `.gitignore` covering `.DS_Store`, `__pycache__/`, `*.pyc`, and any other
   build-local noise currently tracked by accident.
3. Refresh `artifacts/shortcuts/MANIFEST.md` to include the 2026-08-14/15 archive
   entries.
4. Tap "Open Control Room" on the shipped build and confirm the resolved note opens with
   NO picker/list of every note also appearing. If it still appears, re-open
   `.planning/debug/resolved/open-routing-sequence-error.md`'s cycle-16 Finding 2 account
   and check whether the device actually installed build `2026-08-15o` (menu prompt
   should read that stamp) before assuming the fix itself is wrong.
5. Execute the brightness/volume cut on the main line: remove
   `restore_managed_settings`/`dim()`/`silence()`/`settings_snapshot` and the 18 deferred
   sites entirely (making `DEV-06`'s restore-ownership read-side moot, per
   `HANDOFF.md` §6 item 7).

   **⚠️ CONFLICT — deliberate, user decision 2026-08-16.** A sibling todo,
   `2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md`, does the
   *opposite*: it finishes the coercion-aggrandizement fix for the same 18 sites and tests
   stateful capture-and-restore properly. This is intentional and the two run in parallel —
   **the cut proceeds here on main regardless**, while the reintroduction is validated on a
   separate experimental fork and may be brought back into main later only if it proves
   safe. Do not resolve this conflict by skipping either side, and do not treat the sibling
   todo's existence as a reason to leave the code in place here.

## Related

- `.planning/debug/resolved/open-routing-sequence-error.md` — Process Note (MANIFEST.md
  staleness), cycle 14 (brightness/volume audit), cycle 16 (filter.notes fix, closure).
- `.planning/debug/HANDOFF.md` §6 items 2, 3, 10, 11 — this todo's origin.
