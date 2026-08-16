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

   **❌ SUPERSEDED — DO NOT EXECUTE. User decision, 2026-08-16: "They're both back now,
   and working on main."** The cut is cancelled. Dimming and Silence stay, each as its own
   distinct Circle, and the work moves to
   `.planning/todos/pending/2026-08-16-dimming-and-silence-as-distinct-circles.md`.

   The parallel experiment resolved in favour of keeping them: Phase 9 landed the
   numeric-coercion fix for all 28 `setbrightness`/`setvolume` sites and merged to main
   (`2e2261e`, artifacts regenerated in `c6d8737`). Consequence to carry forward — the
   merge made these writes **live** where they previously no-opped, so
   `restore_managed_settings()` is now load-bearing on a path with zero device evidence
   (`docs/BUILD-NOTES.md` §18). DEV-06 (restore-ownership read side) is live again rather
   than moot, since it was only ever moot conditional on this cut proceeding.

   *Historical note — the original conflict framing:* a sibling todo,
   `2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md`, ran the
   opposite experiment on a separate fork. That fork won and merged; both todos are now
   absorbed by the successor named above.

## Related

- `.planning/debug/resolved/open-routing-sequence-error.md` — Process Note (MANIFEST.md
  staleness), cycle 14 (brightness/volume audit), cycle 16 (filter.notes fix, closure).
- `.planning/debug/HANDOFF.md` §6 items 2, 3, 10, 11 — this todo's origin.

---

## CLOSED 2026-08-17 — fully absorbed by Phase 10

Every item is now resolved or dead. Moved to `completed/`.

| Item | Disposition |
|---|---|
| 1. Strip debug scaffolding | **DONE 2026-08-16** (quick task `260816-ukb`), recorded in-place above. |
| 2. Add `.gitignore` | **No work needed.** Phase 10 measured it: `.DS_Store`, `__pycache__/` and `*.pyc` were already covered and `git status --ignored` confirmed them ignored. Recorded in `10-04-SUMMARY.md` so it is not re-litigated. |
| 3. Refresh `MANIFEST.md` | **DONE** — Phase 10 plan 10-04 (`ad0a9ad`) refreshed it and added `docs/manifest_check.py`, which now fails the build if a row drifts from its artifact. |
| 4. Device-confirm the Control Room note-picker fix | **Carried, not dropped.** It is Test 4 of `.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md`, blocked only on DIST-03 (no connected iPhone). Phase 10 additionally *gated* the previously-ungated `shownote`, so Test 5 now also checks the other eight menu items no longer end in the Notes app. |
| 5. Execute the brightness/volume cut | **DEAD.** Cancelled by user decision 2026-08-16, reaffirmed 2026-08-17. Phase 10 was re-planned specifically to exclude it, and `docs/environmental_restore_check.py` (`b18d415`) now pins `dimming()`, `silence()`, `restore_managed_settings()`, the `settings_snapshot` seed and both `NUMERIC_OPERAND_FIELDS` entries — the build fails if any is removed, so the cut cannot return by accident. |

Phase 10 also delivered work this todo never asked for: the Circle 0 silent band, the
`Setup Check` menu item, the `shownote` gate, and five new structural checks. See
`.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/`.
