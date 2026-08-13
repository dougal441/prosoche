---
phase: 06-exits-exit-learning-contracts
verified: 2026-08-13T08:22:28Z
status: passed
score: 5/5 must-haves verified
behavior_unverified: 0
overrides_applied: 0
---

# Phase 6: Exits, Exit Learning & Contracts Verification Report

**Phase Goal:** Every exit is reachable and honestly recorded, the system learns over time which exits actually get the user away from the phone, and every contract the user makes is honoured, recorded, and feeds back into Heat.
**Verified:** 2026-08-13T08:22:28Z
**Status:** passed
**Re-verification:** Gap-fix audit after `e6ea081` (no earlier canonical Phase 6 verification report existed).

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Six exits route to the specified targets, including an honest Consult query menu and first-class Close. | ✓ VERIFIED | `route_exit()` generates Capture, Coordinate, Create, Connect, Consult, and Close. Generated Consult asks once, then offers Search Web/Maps, Notes, Reminders, Calendar, and Back; both searches consume `Consult Query`. Connect only opens Contacts. |
| 2 | Leaving is available before every primitive, disabled exits are excluded, and committed exits record complete metadata. | ✓ VERIFIED | `open_pipeline()` saves before `universal_leaving()`; the wrapper precedes primitive dispatch. `enabled_exits()` intersects profile exits in canonical order. `record_exit_and_route()` reloads, owns, writes a 20-item-bounded event with type/timestamp/app/circle/heat, saves, then routes. |
| 3 | The next genuine OPEN learns one pending-exit outcome and selection is deterministic, rotates while sparse, exploits the best average, and explores at a Config-driven rate. | ✓ VERIFIED | `complete_pending_exit()` is inside the genuine-OPEN path after debounce/cooldown guards and clears `pending_exit`. `select_exit()` reads `exits.exploit_min_observations` and `exits.exploration_rate`, performs canonical sparse rotation and tie-breaking, and routes `Selected Exit`; no model/network/random selection action exists. |
| 4 | Any intention is accepted with preset/custom boundaries. | ✓ VERIFIED | Confession's optional text Ask has no keyword/sincerity gate; the menu provides 2/5/10/15/custom positive-minute boundaries and `persist_contract()` reloads and proves ownership before one full-state save. |
| 5 | CLOSE records nullable/no-contract or respected/overrun outcomes correctly, only displays contract feedback when applicable, and next OPEN applies feedback only for a declared contract. | ✓ VERIFIED | The matching-owner CLOSE branch serializes `respected` as JSON boolean/null and no-contract `overrun_seconds`/`respected` as null; display is guarded by declared duration. OPEN first guards `Previous Declared Duration` before Heat relief/penalty. |

**Score:** 5/5 truths verified (0 present, behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
| --- | --- | --- | --- |
| `tools/build_state_engine.py` | Source graph generator | ✓ VERIFIED | Substantive generator emits the ownership, selector, routing, contract, and outcome graph; rebuilding twice leaves identical XML. |
| `src/PROSOCHE-Dumb.xml` | Runnable Dumb shortcut graph | ✓ VERIFIED | Generated plist parses and validates at target macOS 26/platform all; actions carry the actual route/state wiring, not a placeholder tracer. |
| `docs/phase6_self_check.py` | Independent structural regression guard | ✓ VERIFIED | Executes successfully; it rebuilds twice, parses the plist, and checks routes, ownership, contracts, selector, and forbidden actions. |

### Key Link Verification

| From | To | Via | Status | Details |
| --- | --- | --- | --- |
| OPEN session | universal Leaving | persisted state then menu | ✓ WIRED | `save_state()` appears before `universal_leaving()`, whose Continue arm alone reaches primitive dispatch. |
| exit choice | bounded event and route | reload → ownership equality → save → `route_exit()` | ✓ WIRED | Both suggested and manual choices call the same recorder/router; stale owner arms contain only `Nothing`. |
| pending exit | next OPEN outcome → stats → selected route | guarded genuine OPEN and `Selected Exit` | ✓ WIRED | Outcome updates count/sum/samples then clears pending; selector consumes stats and feeds both route paths. |
| Confession | CLOSE outcome | next OPEN Heat | ✓ WIRED | Contract writes to active session, CLOSE serializes the outcome, and OPEN's declared-duration guard controls feedback. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| --- | --- | --- | --- | --- |
| Exit router | `Selected Exit` | persisted exit stats, Config, enabled profile exits, or manual chooser | Yes | ✓ FLOWING |
| Consult | `Consult Query` | user Ask for Input | Yes | ✓ FLOWING |
| Create | `Create Target URL` | persisted profile target or user URL Ask after re-ownership | Yes | ✓ FLOWING |
| Contract feedback | previous session outcome | matching-owner CLOSE record | Yes | ✓ FLOWING |

### Repaired-Gap Regression Checks

| Former gap | Evidence in the generated graph | Status |
| --- | --- | --- |
| Consult used static routes rather than a full user-query menu | The post-Ask menu has all six items; Search Web and Maps receive the `Consult Query` variable, with no `helpful next step`/`nearby` fallback. | ✓ VERIFIED |
| Create could write/route after stale ownership | After the URL Ask the graph reloads State, compares `Create Owner ID` to `Session ID`, and only then saves the target and opens it; the stale arm is `Nothing`. | ✓ VERIFIED |
| Exploration could choose a non-canonical/non-deterministic exit | The selector stores `Best Exit`, selects only the first canonical candidate after it, wraps to the first canonical non-best candidate exactly once, and retains the sole enabled exit when no non-best exists. | ✓ VERIFIED |
| No-contract CLOSE could create feedback or Heat relief | No-contract branches write JSON `null`, suppress the result UI, and next OPEN requires a positive prior declared duration before applying relief/penalty. | ✓ VERIFIED |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| Phase 5 regression | `python3 docs/phase5_self_check.py` | `phase5 self-check: passed` | ✓ PASS |
| Phase 6 routing/learning/contracts | `python3 docs/phase6_self_check.py` | `phase6 self-check: passed` | ✓ PASS |
| Plist syntax | `plutil -lint src/PROSOCHE-Dumb.xml` | `OK` | ✓ PASS |
| Target validator | `validate-shortcut … --target-macos 26 --target-platform all` | `Validation passed.` | ✓ PASS |
| Whitespace/idempotence | two builds in both self-checks; `git diff --check` | identical output; clean | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan | Status | Evidence |
| --- | --- | --- | --- |
| EXIT-01–EXIT-06 | 06-01 | ✓ SATISFIED | Six first-party routes, including full Consult and non-initiating Contacts. |
| EXIT-07–EXIT-09 | 06-01 | ✓ SATISFIED | Universal Leaving, canonical enabled filter, owned complete event record. |
| LEARN-01–LEARN-05 | 06-03 | ✓ SATISFIED | Guarded one-time outcome recording; deterministic Config-driven sparse/exploit/explore selector. |
| CONT-01–CONT-06 | 06-02 | ✓ SATISFIED | Unjudged intention, boundaries, owner-only nullable outcomes, UI and Heat guards. |

### Anti-Patterns Found

None. The generator contains temporary `*-placeholder` values while constructing condition dictionaries, but each is replaced before plist emission; generated XML contains the live variable comparisons. No untracked `TBD`, `FIXME`, or `XXX` markers exist in Phase 6-modified implementation files.

### Runtime UAT Note

This is a structural verification: the validator and plist parser cannot execute iOS actions. Real-device route behavior remains final UAT, but is non-blocking for this phase's structural gate and is not represented as a gap or a human-verification item.

---

_Verified: 2026-08-13T08:22:28Z_
_Verifier: gsd-verifier_
