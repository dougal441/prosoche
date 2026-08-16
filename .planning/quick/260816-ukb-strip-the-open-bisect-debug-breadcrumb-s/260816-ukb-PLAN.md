---
quick_id: 260816-ukb
status: ready
---

# Strip the OPEN_BISECT debug breadcrumb scaffolding

1. In `tools/build_state_engine.py`, remove all three debug-scaffolding toggles and every
   piece of code they gate (the todo's blocking precondition — a permanent, unconditional
   `notification()` OPEN/CLOSE confirmation added by `04-03-PLAN.md`, independent of any of
   this — is already satisfied, so this is safe to do in full):
   - `OPEN_BISECT`: delete the constant, its preceding "CYCLE 7 MEASUREMENT INSTRUMENT"
     comment block, `BISECT_TITLE`, the `breadcrumb()` helper function and its docstring,
     and every one of its ten `a += breadcrumb("X")` call sites (letters A through J, all
     inside `open_pipeline()`) together with each site's own explanatory
     `# BREADCRUMB X - ...` comment immediately above it.
   - `ROUTER_TRACE`: delete the constant, its preceding comment block, `TRACE_MARKER` and
     `TRACE_END_MARKER`, the `router_trace()` function, its `if ROUTER_TRACE: ...
     router_trace()` call inside `main()`, and the now-orphaned
     `remove_marker_block(actions, TRACE_MARKER, TRACE_END_MARKER)` call in `main()` (its
     two arguments no longer exist once the constants above are removed).
   - `BUILD_STAMP`: delete the constant and its preceding comment block. In
     `manual_emergency_restore()`, change the menu prompt from
     `f"PROSOCHĒ · {BUILD_STAMP}"` to the plain literal `"PROSOCHĒ"` — this is the
     documented fix (`docs/BUILD-NOTES.md` §13 "Scaffolding debt" and §"SHIP CHECKLIST":
     "remove the stamp from the prompt"), not an invented change.
   - Reword the comment beside the permanent `notification()` call at the end of
     `open_pipeline()` (currently "fires on every genuine open regardless of OPEN_BISECT,
     replacing breadcrumb J's de facto confirmation role") so it no longer references the
     removed `OPEN_BISECT`/breadcrumb-J machinery, while keeping the `(G-04-4b)` reference
     and the notification call itself untouched.
   - Do NOT touch the `notification()` calls, the `alert()` helper (still used by
     production Circle primitives like Ash/Dimming/Silence/Mirror/Contract/Status), or any
     other marker constant (`DISPATCH_MARKER`, `ROUTE_FALLBACK_MARKER`,
     `ROUTE_FALLBACK_COMMENT`, etc.).
   - Confirm completeness with
     `grep -n 'OPEN_BISECT\|ROUTER_TRACE\|BUILD_STAMP\|breadcrumb(' tools/build_state_engine.py`
     — it must return no matches.

2. Rebuild and verify the Dumb artifact. First confirm the build-provenance guard passes:
   `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` (abort if it
   fails — do not proceed). Then run, in order: `python3 tools/build_state_engine.py` to
   regenerate `src/PROSOCHE-Dumb.xml`; `python3 docs/state_engine_self_check.py` (must exit
   0); `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all`
   (must report zero errors); `sign-shortcut src/PROSOCHE-Dumb.xml --name "PROSOCHĒ — Nine
   Circles — Dumb" --output-dir artifacts/shortcuts` (must produce a non-empty
   `PROSOCHĒ — Nine Circles — Dumb.shortcut`, no `_signed` suffix). Confirm the regenerated
   XML carries no leftover scaffolding: `grep -c "Report the LAST letter you see"
   src/PROSOCHE-Dumb.xml` and `grep -c "ROUTER TRACE" src/PROSOCHE-Dumb.xml` must both be
   `0`. Archive a dated copy matching the existing convention:
   `mkdir -p "artifacts/shortcuts/$(date +%Y-%m-%d)" && cp src/PROSOCHE-Dumb.xml
   "artifacts/shortcuts/$(date +%Y-%m-%d)/PROSOCHĒ — Nine Circles — Dumb-$(date
   +%H%M%S).xml"`. On-device regression confirmation of the OPEN path stays blocked per
   STATE.md's existing DIST-03 note (`xcrun devicectl` reports no connected iPhone) — do
   not attempt it or treat its absence as a failure; record it as a caveat in the
   completion note instead (step 3).

3. Update only the three Dumb-fork rows (source, archive, signed) in
   `artifacts/shortcuts/MANIFEST.md` with the freshly rebuilt file's byte count and
   `shasum -a 256` hash, pointing the archive row at the new dated copy from step 2; leave
   the Sentient rows and the file's header line untouched. Then, in
   `.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md`, mark Solution item 1
   done by appending a dated completion note directly beneath it (e.g. "**DONE
   2026-08-16** — BUILD_STAMP/ROUTER_TRACE/OPEN_BISECT and all ten breadcrumb sites
   stripped from `tools/build_state_engine.py`; rebuilt, self-checked, validated, signed;
   MANIFEST.md Dumb rows refreshed. On-device OPEN-path regression confirmation remains
   blocked on DIST-03 (no connected iPhone via `xcrun devicectl`) — re-run once a device is
   available."), without altering the wording, order, or status of items 2 through 5.
