---
phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
verified: 2026-08-17T06:52:44Z
status: human_needed
score: 27/29 must-haves verified
behavior_unverified: 2 # A1 (repeat.each over an empty array) and the JSON-null-leaf coercion assumption — both explicitly marked verification:backstop by the plans and unsettled only at evidence rung 2 (device/simulator), not code presence
overrides_applied: 0
human_verification:
  - test: "First OPEN against clean state (12-UAT.md Test 1)"
    expected: "No 'could not evaluate the key path' or 'no value was found' alert; state.json shows active_session as a live object, schema_version 4, exit_events [], exit_selection_counter 0"
    why_human: "Personal Automation triggers and on-device state.json inspection are device-gated per .claude/CLAUDE.md §9 — no simulator or file-level substitute exists"
  - test: "A genuine leave and confirm exit — all six routes plus Create clean/reuse (12-UAT.md Test 2)"
    expected: "Every route opens the correct app/menu with no key-path error; Create asks for a URL on a clean install and reuses the saved URL on a second exit"
    why_human: "record_exit_and_route() and route_exit() have zero device evidence at any rung prior to this phase; this is explicitly named the phase's highest-priority open risk in 12-UAT.md"
  - test: "CLOSE after a session that changed brightness or volume (12-UAT.md Test 3)"
    expected: "restore_managed_settings('Reloaded State') actually returns brightness/volume to the pre-primitive value after the container/leaf conversion"
    why_human: "This is the SESS-07 / SAFE-01 state-transition invariant this phase exists to protect. Source-order proves restore_managed_settings() is emitted before notification()/save_state(), and the leaf seed makes the dotted reads on that path structurally unable to hard-error — but whether the physical restore actually completes on a real device is a runtime behavior no file-level check can see."
  - test: "A superseded CLOSE (12-UAT.md Test 4)"
    expected: "The condition-4 ownership compare still routes a superseded CLOSE to a Nothing-only path — no write, no restore, no notification"
    why_human: "Cancellation/ownership invariant; code inspection confirms the compare is unchanged and reachable, but the actual race-safe behavior needs a real interleaved-OPEN device trial"
  - test: "Second OPEN after an exit — exit_stats composite reads (12-UAT.md Test 5)"
    expected: "No key-path error on exit_stats.<type>.count/.sum_return_seconds/.samples; pending_exit clears back to sentinel"
    why_human: "Composite dotted reads against runtime-resolved keys; device-gated per 12-UAT.md"
  - test: "exit_events after several exits — ordering and cap (12-UAT.md Test 7)"
    expected: "Array is newest-first; the twenty-entry cap is exercisable but not observable with only a few exits"
    why_human: "Source-order proves the append-then-filter mechanics (new event pushed before older entries are copied in stored order), but the actual on-device array contents are unobserved — 12-UAT.md is honestly BLOCKED (xcrun devicectl: 'No devices found.')"
  - test: "A1 — is.workflow.actions.repeat.each over an EMPTY array (12-01 must_haves, verification: backstop)"
    expected: "Zero-iteration no-op, not a runtime type error, when exit_events is seeded []"
    why_human: "Explicitly marked [ASSUMED] by the plan and deferred to evidence rung 2 (simulator probe); the planner deliberately did not spend a probe on it (PD-1, docs/BUILD-NOTES.md §27) because the fix is byte-identical either way — but the runtime behavior itself remains unconfirmed"
  - test: "read_value() of a JSON-null leaf under the create_target_url option-a choice (12-04 must_haves, verification: backstop)"
    expected: "No untested Shortcuts coercion path is exercised, since create_target_url is seeded as the string sentinel 'null', never a bare JSON null"
    why_human: "Explicitly marked verification:backstop by the plan; while code inspection confirms option-a was the path taken (docs/BUILD-NOTES.md §27 PD-2) which structurally avoids the risk, the plan itself calls for confirmation beyond presence"
---

# Phase 12: State-Shape Sentinel Gaps — exit_events and active_session Verification Report

**Phase Goal:** Close the two remaining STATE-SHAPE + GATE-SEMANTICS gaps — `exit_events` and `active_session` — using the container/leaf pattern already verified twice on `settings_snapshot` and `pending_exit`. Seed a permanent container for each in the bootstrap template mirroring `seed_pending_exit()`. Add a `verify_*_seed()` build guard per key following `verify_pending_exit_seed()`. Audit every read/write/clear site for both keys by full-codebase sweep — `record_exit_and_route()`, `universal_leaving()`, and anything else grep finds — and ensure clearing gates test leaf value (condition 5 against `CLEARED_SENTINEL`) rather than container existence (condition 100). Remove both keys from `KNOWN_SENTINEL_EXISTENCE_GATES` so the registry honestly reads zero remaining gaps. Fix whole classes, never site-by-site. Hard prerequisite for Phase 17.

**Verified:** 2026-08-17T06:52:44Z
**Status:** human_needed
**Re-verification:** No — initial verification

## Goal Achievement

This verification re-ran the whole build/checker chain independently rather than trusting SUMMARY claims, and additionally re-verified two follow-on fixes (WR-01 indentation bug, WR-02 MANIFEST staleness) and the re-archive/re-sign step directly against the live tree and the decrypted signed artifact.

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | Bootstrap template declares `exit_events: []` and `exit_selection_counter: 0` | ✓ VERIFIED | `EXIT_EVENTS_SEED`, `seed_exit_events()` at `tools/build_state_engine.py:2870-2903`; confirmed in decrypted signed `.shortcut` payload: `"exit_events": [], "exit_selection_counter": 0` |
| 2 | `exit_events` rolling window bounded at 20 via condition-0 (`Repeat Index < 20`) | ✓ VERIFIED | `record_exit_and_route()` lines 955-959: `if_block("Repeat Index", 0, number=20)` |
| 3 | `exit_events` ordering is newest-first and stable | ✓ VERIFIED | Line 954 appends the new event to `Exit Events Next` *before* the `Repeat With Each` loop (line 956) replays prior entries in stored order into the same variable |
| 4 | `exit_selection_counter` seeded 0 lets condition-101 guards take their Otherwise arm cleanly | ✓ VERIFIED | `select_exit()` line 782 and `record_exit_and_route()` line 975 both gate on condition 101 (`does not have any value`), unreachable once the counter is seeded a real number |
| 5 | `schema_version` is 4 across all three coupled literals | ✓ VERIFIED | `SCHEMA_VERSION="4"`, `SCHEMA_VERSION_PREVIOUS="3"`, `SCHEMA_VERSION_ACCEPTED` includes `"4"` at lines 3994-4008; confirmed `"schema_version": 4` in decrypted signed artifact |
| 6 | Both forks rebuild byte-idempotently and pass Gate A clean | ✓ VERIFIED | Independently rebuilt both forks (`python3 tools/build_state_engine.py && python3 tools/build_sentient.py`) — byte-identical to committed tree; `validate-shortcut --target-macos 26 --target-platform all` returned `Validation passed.` on both forks |
| 7 | `active_session` seeded as a permanent 4-leaf sentinel container (`id`, `started_at`, `declared_duration_seconds`, `intention`) | ✓ VERIFIED | `ACTIVE_SESSION_SEED` + `seed_active_session()` at lines 2971-3028; confirmed in decrypted signed artifact with correct **2-space** indentation (WR-01 fix verified live, not just claimed — see below) |
| 8 | Every seeded leaf carries `CLEARED_SENTINEL`, never the empty string | ✓ VERIFIED | `ACTIVE_SESSION_SEED` values are all `CLEARED_SENTINEL = "null"`; `verify_active_session_seed()` assertion 2 (lines 3074-3079) independently raises on any empty-string leaf |
| 9 | `PENDING_EXIT_ANCHOR` no longer collides with `seed_active_session()`'s rewrite target | ✓ VERIFIED | `PENDING_EXIT_ANCHOR = '"last_app": null,'` (line 2683) vs. `ACTIVE_SESSION_ANCHOR = '"active_session": null,'` (line 2980) — distinct lines; from-scratch rebuild completed with exit 0, no `StopIteration` |
| 10 | `verify_active_session_seed()` asserts container shape on both forks, fires `SystemExit` on defect | ✓ VERIFIED | Independently constructed a synthetic corruption (rewrote 4 `active_session.id` clear-sites to bare `active_session`) and confirmed `verify_sentinel_gates()` fires with the exact SESS-07/SAFE-01-referencing message; both forks arm the guard (`tools/build_sentient.py:317`) |
| 11 | No condition-100 existence gate stands over any `active_session` read in either fork | ✓ VERIFIED | Read every one of the 6 converted call sites directly (`persist_contract`, `record_exit_and_route`, `close_pipeline` ×2, `route_exit`'s Create branch, `live_ice_redirect`, `manual_emergency_restore`) — all use condition-4 ownership compares or condition-5 leaf gates, zero condition-100 |
| 12 | `active_session` never written/cleared as a whole container; `open_pipeline()` writes 4 leaves; 3 clears write `.id` only | ✓ VERIFIED | `grep 'set_value("active_session'` shows exactly: 4 leaf writes in `open_pipeline()` (lines 1229-1232), 2 leaf updates in `persist_contract()` (lines 590-591), and exactly 3 `.id`-only clears at `close_pipeline()` (1358), `live_ice_redirect()` (1872), `manual_emergency_restore()` (1956) |
| 13 | Session-ownership compare (condition-4) survives untouched at all 4 owner sites | ✓ VERIFIED | Confirmed present and unchanged in `persist_contract()`, `record_exit_and_route()`, `close_pipeline()` (both entry and reload arms) |
| 14 | `KNOWN_SENTINEL_EXISTENCE_GATES` is the empty tuple; `verify_sentinel_gates()` runs unexempted with zero offenders | ✓ VERIFIED | `KNOWN_SENTINEL_EXISTENCE_GATES = ()` at line 232; full build passed (exit 0) with this guard active and unexempted |
| 15 | `restore_managed_settings()` still emitted in `close_pipeline()` before `notification()` and `save_state('Reloaded State')` | ✓ VERIFIED | Source order confirmed at lines ~1354-1360: restore call, then contract-result display, then notification, then `save_state`; `docs/environmental_restore_check.py` passed (exit 0) |
| 16 | Exit routing still matches exact route names via condition-4 | ✓ VERIFIED | `route_exit()` line 869: `if_block(choice_name, 4, string=name)` for all six routes |
| 17 | Six exit routes' order and state keys unchanged | ✓ VERIFIED | `docs/phase6_self_check.py` passed (exit 0), which asserts exact route presence and ordering |
| 18 | `docs/state_engine_self_check.py`'s required setter-key tuple names `active_session.id` | ✓ VERIFIED | Line 95: `for required in (..., "active_session.id", ...)`, with an explanatory comment naming the Phase 12 move; checker passed (exit 0) |
| 19 | `profile_snapshot.create_target_url` resolves in the bootstrap seed | ✓ VERIFIED | `seed_create_target_url()` at line 3127; confirmed in decrypted signed artifact: `"create_target_url": "null"` |
| 20 | Create branch's set/unset gate reads FALSE on clean install (condition-5, not condition-100) | ✓ VERIFIED | `route_exit()` line 887: `if_block("Create Target URL", 5, string=CLEARED_SENTINEL)`, with an inline comment explicitly distinguishing this state-read gate from the transient-input gate below it (condition 100, correctly kept) |
| 21 | `verify_state_seed()`'s read-side scan covers every literal State/Reloaded State read, not just `settings_snapshot` | ✓ VERIFIED | `STATE_READ_SOURCE_VARIABLES = ("State", "Reloaded State")` filters by `WFInput.Value.VariableName` identity (lines 2571, 2620); full build passed with this generalised guard active |
| 22 | Generalised scan excludes Config/Previous Session reads | ✓ VERIFIED | Same source-variable filter at line 2620 structurally excludes any variable not named `State`/`Reloaded State`; `docs/BUILD-NOTES.md` §27 records the measured counts (30 literal + 23 composite Config reads, 3 Previous Session reads) that would have false-failed without this filter |
| 23 | `exit_stats.*` composite reads tolerated by named prefix, not deleted wholesale | ✓ VERIFIED | `STATE_SEED_COMPOSITE_PREFIXES = ("exit_stats.",)` at line 2579, checked at line 2630 |
| 24 | Generalised guard reports zero missing keys on both forks | ✓ VERIFIED | Both `python3 tools/build_state_engine.py` and `python3 tools/build_sentient.py` exited 0 with `verify_state_seed()` active in the verify chain |
| 25 | Both forks signed under exact live display names, no `_signed` suffix | ✓ VERIFIED | `ls artifacts/shortcuts/` shows exactly `PROSOCHĒ — Nine Circles — Core.shortcut` and `— Aware.shortcut` |
| 26 | Every MANIFEST.md row matches disk; `manifest_check.py` exits 0 | ✓ VERIFIED | Independently recomputed size + SHA-256 for all 4 disk artifacts (2 sources, 2 signed) — byte-for-byte and hash-for-hash identical to the current MANIFEST.md table; `python3 docs/manifest_check.py` → `manifest check: passed (6 rows verified against disk)` |
| 27 | Gate B reports exactly one waived line per fork (`WFCreateNoteInput`) | ✓ VERIFIED | Independently ran `validate-shortcut --target-macos 27 --target-platform all` on both forks — each returned exactly one error line, matching the documented waiver text verbatim |
| 28 | `12-UAT.md` exists, cold-runnable, explicit BLOCKED branch, no fabricated device evidence | ✓ VERIFIED | File reviewed in full: 7 named tests, all outcome fields genuinely blank, `xcrun devicectl list devices` → "No devices found." recorded verbatim, verdict section explicitly blank pending a real device |
| 29 | Every deviation/assumption recorded in `docs/BUILD-NOTES.md` under a Phase 12 heading | ✓ VERIFIED | `docs/BUILD-NOTES.md` §26-27 present: A1, A2, A3, A5 assumptions; PD-1/PD-2/PD-3 decisions; 4 measured research corrections; verbatim Gate B baselines |
| — | **A1**: `repeat.each` over an empty array is a zero-iteration no-op | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | Marked `verification: backstop` by the plan itself. `exit_events` is now always present, so the absent-key hard-error case is closed, but the empty-array runtime semantic remains `[ASSUMED]`, unsettled at evidence rung 2 per `docs/BUILD-NOTES.md` §27 |
| — | **JSON-null-leaf coercion**: `read_value()` of a JSON-null leaf is never exercised under option-a | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | Marked `verification: backstop`. Code inspection confirms option-a (sentinel string, not bare JSON null) was the path actually taken, which structurally avoids the risk — but the plan calls for confirmation beyond presence |

**Score:** 27/29 truths verified (2 present, behavior-unverified — both explicitly `verification: backstop` per the plans, not code gaps)

### Follow-on fixes verified directly against the live tree (not from stale SUMMARY claims)

| Item | Claim | Verified |
|---|---|---|
| WR-01 (commits `5f55edc`, `58b3b87`) | `seed_active_session()`'s double-indent bug fixed; emitted line now matches sibling indentation | ✓ Confirmed 2-space indent in both `src/PROSOCHE-Dumb.xml:1476` and `src/PROSOCHE-Sentient.xml`, and in the **decrypted signed artifact** (not just source) |
| WR-02 (commit `58b3b87`) | `MANIFEST.md` refreshed to describe the Phase 12 rebuild accurately | ✓ Confirmed Phase 12 paragraph present, schema_version 3→4 correction present, `⚠` bullet present |
| Re-archive/re-sign (commit `a21ad8f`) | Both forks re-signed against WR-01-corrected source; `MANIFEST.md` refreshed; signed artifacts byte-consistent | ✓ Confirmed all 6 MANIFEST rows match disk exactly (independently recomputed hashes); `docs/manifest_check.py` passes; decrypted signed `.shortcut` confirmed to carry the corrected 2-space indentation |

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `tools/build_state_engine.py` | `EXIT_EVENTS_SEED`, `seed_exit_events()`, `verify_exit_events_seed()`, `ACTIVE_SESSION_SEED`, `seed_active_session()`, `verify_active_session_seed()`, `KNOWN_SENTINEL_EXISTENCE_GATES = ()`, `STATE_READ_SOURCE_VARIABLES`, `seed_create_target_url()` | ✓ VERIFIED | All present, all wired into `main()`'s generation and verify chain |
| `tools/build_sentient.py` | All new guards armed per fork | ✓ VERIFIED | `verify_active_session_seed`, `verify_exit_events_seed`, `verify_state_seed` imported and called |
| `docs/state_engine_self_check.py` | Required setter-key tuple names `active_session.id` | ✓ VERIFIED | Line 95, with explanatory Phase 12 comment |
| `src/PROSOCHE-Dumb.xml` | Regenerated Core fork carrying all seeded fields | ✓ VERIFIED | Decrypted and inspected directly from the signed `.shortcut` |
| `src/PROSOCHE-Sentient.xml` | Regenerated Aware fork inheriting the same shape | ✓ VERIFIED | Byte-idempotent rebuild confirmed |
| `artifacts/shortcuts/MANIFEST.md` | Refreshed rows + accurate prose | ✓ VERIFIED | `manifest_check.py` passes; independently recomputed hashes match |
| `.planning/phases/.../12-UAT.md` | Cold-runnable device UAT, explicit BLOCKED | ✓ VERIFIED | Reviewed in full |
| `docs/BUILD-NOTES.md` | Phase 12 deviation record | ✓ VERIFIED | §26-27 present and complete |

### Key Link Verification

| From | To | Via | Status |
|---|---|---|---|
| `seed_exit_events()` | `verify_exit_events_seed()` | Both read `EXIT_EVENTS_SEED` | ✓ WIRED |
| `main()` | `seed_exit_events(actions)` before `fix_state_rebind(actions)` | Ordering confirmed at lines 4133-4135 | ✓ WIRED |
| `seed_active_session()` | `verify_active_session_seed()` | Both read `ACTIVE_SESSION_SEED` | ✓ WIRED |
| `open_pipeline()` | 4 `active_session.*` leaf writes | `set_value()` calls confirmed | ✓ WIRED |
| `verify_sentinel_gates()` | `KNOWN_SENTINEL_EXISTENCE_GATES` | Empty tuple, both rules unexempted; independently confirmed sensitivity via synthetic corruption | ✓ WIRED |
| `close_pipeline()` | `restore_managed_settings("Reloaded State")` | Emitted before `notification()`/`save_state()`; source order confirmed | ✓ WIRED |
| `route_exit()` Create branch | `profile_snapshot.create_target_url` seed | Condition-5 gate against `CLEARED_SENTINEL` | ✓ WIRED |
| `verify_state_seed()` | Bootstrap template | Every literal `State`/`Reloaded State` `getvalueforkey` resolved against the seed at full depth | ✓ WIRED |
| `artifacts/shortcuts/*.shortcut` | `artifacts/shortcuts/MANIFEST.md` | Independently recomputed size + SHA-256 | ✓ WIRED |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Full 12-checker chain exits 0 | `state_engine_self_check.py`, `phase5/6/7/9_self_check.py`, `sentient_audit_check.py`, `sentient_core_check.py`, `environmental_restore_check.py`, `router_ui_census.py`, `sequence_dispatch_check.py`, `note_identity_check.py`, `manifest_check.py` | All 12 exit 0 | ✓ PASS |
| Both forks rebuild byte-idempotently | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py` | Output byte-identical to committed source | ✓ PASS |
| Gate A (mandatory) | `validate-shortcut --target-macos 26 --target-platform all` × 2 forks | `Validation passed.` on both | ✓ PASS |
| Gate B (advisory) | `validate-shortcut --target-macos 27 --target-platform all` × 2 forks | Exactly one waived line per fork (`WFCreateNoteInput`), matching the documented waiver | ✓ PASS |
| Signed-artifact decrypt round-trip | `aea decrypt` + `aa extract` + `plutil -convert xml1` on Core `.shortcut` | Confirmed `schema_version: 4`, 2-space-indented 4-leaf `active_session`, `exit_events: []`, `exit_selection_counter: 0`, `create_target_url: "null"` present in the actually-shipped binary | ✓ PASS |
| `verify_sentinel_gates()` sensitivity | Synthetic corruption of the 3 `active_session.id` clear-sites to bare `active_session` | Guard fired with the SESS-07/SAFE-01-referencing SystemExit message | ✓ PASS |
| Build provenance gate | `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` | Exit 0 | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan(s) | Description | Status | Evidence |
|---|---|---|---|---|
| SESS-07 | 12-02, 12-03, 12-05 | CLOSE restores any environmental setting changed during the session | ✓ SATISFIED (hardened) | `active_session` container/leaf conversion removes the hard-error risk on `restore_managed_settings()`'s path; `environmental_restore_check.py` passes; originally satisfied at Phase 4, this phase closes a fresh-install crash risk on that same guarantee |
| STATE-12 | 12-01, 12-04 | Bounded, versioned JSON with rolling windows, no unbounded arrays | ✓ SATISFIED (hardened) | `exit_events` now seeded `[]` and bounded at 20 via condition-0; originally satisfied at Phase 2, this phase closes the one remaining unseeded rolling-window key |
| EXIT-01 | 12-03, 12-04 | Capture routes to idea-externalising target | ✓ SATISFIED (unaffected functionally, gate-safety improved) | `route_exit()`'s Capture menu unchanged; ownership-compare gates around it hardened |
| EXIT-02 | 12-03, 12-04 | Coordinate routes to a planning target | ✓ SATISFIED (unaffected functionally, gate-safety improved) | Same as EXIT-01 |
| SAFE-01 | 12-02, 12-03 | Brightness never set to zero | ✓ SATISFIED (hardened) | Unrelated to this phase's numeric floor logic (unchanged), but the `active_session` leaf-seed removes the crash path that could previously abort `close_pipeline()` before the restore ever ran |

None of the 5 requirement IDs are newly introduced by Phase 12 in `.planning/REQUIREMENTS.md` — all 5 are mapped to their originating phases (2, 4, 5, 6) as already `Complete`. This is expected: Phase 12 is a retroactive gap-closure phase that hardens the state-shape/gate-semantics guarantees those earlier phases established, rather than introducing new requirement coverage. No orphaned requirements found — every ID declared in the plan frontmatter is accounted for in REQUIREMENTS.md.

### Anti-Patterns Found

None. Searched all phase-12-modified files (`tools/build_state_engine.py`, `tools/build_sentient.py`, `docs/state_engine_self_check.py`, `docs/BUILD-NOTES.md`, `artifacts/shortcuts/MANIFEST.md`) for `TBD`/`FIXME`/`XXX`/`TODO`/`HACK`/`PLACEHOLDER` and stub-shaped patterns. Zero unreferenced debt markers found. The one `<placeholder text>` string that appeared in a grep match is inside a docstring describing a code pattern (`if_block(..., string=<placeholder text>)`), not an actual stub.

### Human Verification Required

See frontmatter `human_verification` list. Summary: `12-UAT.md` (7 device-only tests covering the exit-recording path, the CLOSE restore path, and the superseded-CLOSE ownership invariant) is honestly recorded as **BLOCKED** — `xcrun devicectl list devices` reported "No devices found." This is not treated as a verification failure per this phase's own success criteria and `12-CONTEXT.md`: no automated substitute exists for Personal Automation triggers, the Notes app path, or real brightness/volume restore behavior (`.claude/CLAUDE.md` §9, "Rung 2's ceiling"). Two additional items are explicitly `verification: backstop` in the plans themselves (A1 — `repeat.each` over an empty array; the JSON-null-leaf coercion assumption) and remain unsettled at evidence rung 2.

### Gaps Summary

No gaps found. Every must-have truth from all 5 plans, plus the roadmap's own goal/deliverables language, is verified directly against the live codebase — not inferred from SUMMARY.md claims. The two follow-on fixes (WR-01 double-indent, WR-02 stale MANIFEST prose) and the re-archive/re-sign step, none of which are reflected in any plan SUMMARY, were independently confirmed against the live tree and the decrypted signed artifact. All 12 project checkers, both validator gates, and the byte-idempotency rebuild pass cleanly at HEAD. The phase's only open item is genuinely device-gated (the exit-recording path has zero device evidence at any rung, honestly recorded as BLOCKED) plus two explicitly-backstop assumptions the plans themselves flagged as unsettled — none of these are code defects, and per this phase's own stated scope they do not block phase completion, but they are real open items that deserve a human decision on when to close them (i.e., when a device becomes reachable).

---

_Verified: 2026-08-17T06:52:44Z_
_Verifier: Claude (gsd-verifier)_
