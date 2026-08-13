---
phase: 06-exits-exit-learning-contracts
verified: 2026-08-13T08:13:08Z
status: gaps_found
score: 1/5 must-haves verified
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "All six exits route correctly, including Consult's direct query-shaped menu."
    status: failed
    reason: "Consult exposes only Search web and Search maps, with hard-coded query text; it lacks Notes, Reminders, Calendar, and a user-provided query."
    artifacts:
      - path: "tools/build_state_engine.py"
        issue: "route_exit() defines Consult with two menu choices and static search inputs."
      - path: "src/PROSOCHE-Dumb.xml"
        issue: "Both generated Consult menus contain only Search web and Search maps."
    missing:
      - "Ask what the user is trying to find and route that value through search."
      - "Add Notes, Reminders, Calendar, and Back to the Consult menu."
  - truth: "Leaving is safely reachable and exit routing cannot revive a stale session."
    status: failed
    reason: "Create persists its URL after an interactive Ask using the earlier Reloaded State, without reloading state or proving session ownership again. A CLOSE or newer OPEN during that interaction can be overwritten. The enabled-exit list is also unguarded when every exit is disabled."
    artifacts:
      - path: "tools/build_state_engine.py"
        issue: "Create writes profile_snapshot.create_target_url directly after Ask; select_exit() performs modulo/list selection without a zero-enabled-exits guard."
    missing:
      - "Reload state and confirm active_session.id after Create input before saving or opening the URL."
      - "Provide a safe Leaving outcome when the enabled-exit list is empty."
  - truth: "Deterministic Config-driven epsilon-greedy learning changes real exit routing."
    status: failed
    reason: "The exploration loop repeatedly overwrites Selected Exit for each non-best candidate. It therefore ends at the last canonical candidate (and can select the best when it is Close), not the canonical next non-best exit."
    artifacts:
      - path: "tools/build_state_engine.py"
        issue: "select_exit() does not stop after the first non-best candidate and compares against its mutable Selected Exit value."
    missing:
      - "Select exactly one canonical next enabled non-best candidate before the shared recorder/router."
  - truth: "Only a real contract affects the next OPEN's Heat calculation."
    status: failed
    reason: "CLOSE assigns Contract Respected=true whenever overrun is non-positive; no-contract sessions use declared duration 0, so they are recorded as respected and the next OPEN applies contract_respected_relief."
    artifacts:
      - path: "tools/build_state_engine.py"
        issue: "close_pipeline() sets respected after the zero-duration fallback; open_pipeline() applies relief based on respected without a declared-duration guard."
    missing:
      - "Represent no-contract outcomes distinctly and guard next-OPEN contract feedback on a positive declared duration."
---

# Phase 6: Exits, Exit Learning & Contracts Verification Report

**Phase Goal:** Every exit is reachable and honestly recorded, the system learns over time which exits actually get the user away from the phone, and every contract the user makes is honoured, recorded, and feeds back into Heat.

**Verified:** 2026-08-13T08:13:08Z
**Status:** gaps_found
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | All six exits route correctly. | ✗ FAILED | Capture, Coordinate, Create, Connect, and Close have routes, but generated Consult menus at actions 749 and 887 contain only `Search web` and `Search maps`; their inputs are static. |
| 2 | Leaving is always safe; disabled exits are not selected; an exit is honestly recorded. | ✗ FAILED | The pre-dispatch Leaving wrapper and owned bounded event writer exist, but Create saves a stale `Reloaded State` after user input, and no zero-enabled-exits branch prevents empty-list selection. |
| 3 | The next genuine OPEN records an outcome and learning selects real routes deterministically. | ✗ FAILED | Pending-exit recording is inside the genuine OPEN branch and route menus share the writer/router, but exploration does not select exactly one non-best exit. |
| 4 | Any intention is accepted and paired with a preset or valid custom boundary. | ✓ VERIFIED | `confession()` accepts text input without a content gate, offers 2/5/10/15/custom, and persists only positive durations after a reload/ownership check. |
| 5 | Contract outcomes affect Heat only when a contract exists, and no-contract sessions show no overrun. | ✗ FAILED | UI correctly suppresses the overrun alert for declared duration 0, but those sessions are still recorded as respected and receive next-OPEN Heat relief. |

**Score:** 1/5 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
| --- | --- | --- | --- |
| `tools/build_state_engine.py` | Generates phase-six exits, ownership, contracts, and deterministic learning. | ⚠️ PARTIAL | Substantive and wired into the build; contains the four blockers above. |
| `src/PROSOCHE-Dumb.xml` | Executable generated shortcut graph. | ⚠️ PARTIAL | Parses and validates structurally, but faithfully contains the incomplete Consult and stale Create paths. |
| `docs/phase6_self_check.py` | Regression evidence for Phase 6 requirements. | ⚠️ PARTIAL | Passes, but only checks marker/key/action presence; it does not exercise Consult completeness, Create's second ownership check, exploration reference cases, or no-contract Heat feedback. |

### Key Link Verification

| From | To | Via | Status | Details |
| --- | --- | --- | --- |
| New OPEN session | Universal Leaving | initial Save File before wrapper | ✓ WIRED | The generated session/state writer precedes the universal menu; wrapper precedes primitive dispatch. |
| Exit choice | bounded event then route | reload → owner comparison → one save → route | ⚠️ PARTIAL | Correct for normal routes; Create adds a second post-input writer without a fresh reload/owner check. |
| `pending_exit` | next genuine OPEN | guarded outcome updater | ✓ WIRED | The updater is after cooldown/debounce guards and clears `pending_exit` after one sample. |
| Selector | real route | suggested/manual choices share recorder/router | ⚠️ PARTIAL | Both paths are connected, but exploration's computed selected value is incorrect. |
| CLOSE record | next OPEN Heat | `recent_sessions` outcome fields | ✗ NOT_WIRED CORRECTLY | No-contract records are indistinguishable from respected contracts for Heat relief. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| Phase 5 structural regression | `python3 docs/phase5_self_check.py` | `phase5 self-check: passed` | ✓ PASS |
| Phase 6 supplied structural regression | `python3 docs/phase6_self_check.py` | `phase6 self-check: passed` | ✓ PASS — insufficient coverage noted above |
| Plist syntax | `plutil -lint src/PROSOCHE-Dumb.xml` | `OK` | ✓ PASS |
| Target-26 structural validation | `python3 .../validate_shortcut.py src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` | `Validation passed.` | ✓ PASS |

### Requirements Coverage

| Requirement | Status | Evidence |
| --- | --- | --- |
| EXIT-01 | ✓ SATISFIED | Capture menu opens Notes, Voice Memos, or Camera. |
| EXIT-02 | ✓ SATISFIED | Coordinate menu opens Reminders or Calendar. |
| EXIT-03 | ✗ BLOCKED | Create has a target route but violates the required post-interaction ownership safety. |
| EXIT-04 | ✓ SATISFIED | Connect opens Contacts only; no send/call/message action is present. |
| EXIT-05 | ✗ BLOCKED | Consult lacks three required destinations and a query-shaped search path. |
| EXIT-06 | ✓ SATISFIED | Close uses Return to Home Screen as a selectable route. |
| EXIT-07 | ✗ BLOCKED | Empty enabled exits reaches unguarded modulo/list selection, so Leaving is not guaranteed. |
| EXIT-08 | ✓ SATISFIED | Canonical filtering intersects the enabled list before selection. |
| EXIT-09 | ✓ SATISFIED | Owned exit event includes type, timestamp, app, circle, and heat; rolling list is capped. |
| LEARN-01 | ✓ SATISFIED | Pending outcome runs only after genuine OPEN guards and clears after recording. |
| LEARN-02 | ✓ SATISFIED | Sparse selection uses persisted counter modulo enabled count. |
| LEARN-03 | ✗ BLOCKED | Exploration can choose the wrong exit and can choose the best exit. |
| LEARN-04 | ✓ SATISFIED | Reads `Config.exits.exploration_rate`. |
| LEARN-05 | ✓ SATISFIED | No model invocation or network action participates in selection. |
| CONT-01 | ✓ SATISFIED | Blank/free-form intention is accepted without judgment. |
| CONT-02 | ✓ SATISFIED | Preset and positive custom boundaries are present. |
| CONT-03 | ✓ SATISFIED | Positive-duration, non-positive-overrun contracts record respected. |
| CONT-04 | ✓ SATISFIED | Positive overrun is stored in completed session record. |
| CONT-05 | ✗ BLOCKED | No-contract sessions incorrectly get contract-respected Heat relief. |
| CONT-06 | ✓ SATISFIED | Contract alert is guarded on positive declared duration. |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| --- | --- | --- | --- | --- |
| `docs/phase6_self_check.py` | 30–61 | Presence-only assertions | ⚠️ Warning | Passing self-check does not prove the advertised ownership, selector, or no-contract behavior. |

## Gaps Summary

Four structural defects block Phase 6: incomplete Consult routing, a stale Create writer, an incorrect epsilon-exploration loop, and false no-contract Heat relief. The local structural validator and supplied self-checks pass, but neither exercises these contracts. On-device iPhone route observation remains useful after the structural gaps are repaired; it cannot waive them.

_Verified: 2026-08-13T08:13:08Z_
_Verifier: the agent (gsd-verifier)_
