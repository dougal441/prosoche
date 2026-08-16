---
phase: 09-reintroduce-and-validate-dimming-silence-stateful-restore-on
plan: 02
subsystem: distribution
tags: [shortcuts, ios, signing, device-uat, capture-restore, checkpoint]

# Dependency graph
requires:
  - phase: 09-01
    provides: coercion-fixed src/PROSOCHE-Dumb.xml and src/PROSOCHE-Sentient.xml (NUMERIC_OPERAND_FIELDS fix, all 28 sites audited)
provides:
  - Both forks re-signed in place with the coercion fix baked in, SHA-256-confirmed different from artifacts/shortcuts/MANIFEST.md's recorded values
  - 09-UAT.md authored: 12 numbered device-proving tests (ROADMAP.md Phase 9 criteria 2-7) plus a first-principles DEV-06 restore-ownership design write-up
  - A blocked device-proving checkpoint (Tasks 2-3) — zero iPhones connected this session, matching the open DIST-03 blocker
affects: [09-verdict, ship-readiness-cleanup]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Device-checkpoint-blocked SUMMARY pattern (reused from 08-03-SUMMARY.md): status: blocked,
      requirements-completed left empty until device evidence actually lands, a dedicated
      Checkpoint section naming the exact blocker"

key-files:
  created:
    - .planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md
  modified:
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut"
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut"

key-decisions:
  - "Did not auto-approve Task 2/3's checkpoint:human-verify gates despite workflow.auto_advance
    being true in .planning/config.json — both require physical iPhone interaction that cannot be
    simulated or fabricated; auto-approving would mean guessing a device result, which this
    project's own CLAUDE.md do-not-fabricate rule and this plan's own <important_context> both
    explicitly forbid."
  - "requirements-completed left empty: RESTORE-02 through RESTORE-07 all require device evidence
    (09-UAT.md Tests 1-12), none of which exist yet — marking any of them complete from Task 1's
    static work alone would misrepresent unverified claims as proven."

requirements-completed: []

coverage:
  - id: D1
    description: "Both forks re-signed in place carrying the 09-01-PLAN.md coercion fix; SHA-256 confirmed different from MANIFEST.md's recorded pre-Phase-9 values"
    verification:
      - kind: other
        ref: "shasum -a 256 on both signed .shortcut files vs artifacts/shortcuts/MANIFEST.md — both differ"
        status: pass
      - kind: other
        ref: "test -s on both signed .shortcut files — both non-empty"
        status: pass
    human_judgment: false
  - id: D2
    description: "09-UAT.md authored with exactly 12 numbered device-proving tests and a first-principles DEV-06 write-up (points a-d), before any device work begins"
    verification:
      - kind: other
        ref: "grep -c '^### ' 09-UAT.md == 12"
        status: pass
    human_judgment: false
  - id: D3
    description: "Device evidence for ROADMAP.md Phase 9 criteria 2-7 (RESTORE-02 through RESTORE-07): coercion-chip gate, capture/restore round trip, four failure-mode trials plus one compound trial, Emergency Restore recovery, DEV-06 live re-evaluation, and a written safe/retired verdict"
    verification: []
    human_judgment: true
    rationale: "Requires a physical, Apple-Intelligence-capable iPhone running iOS 26.x with Shortcuts.app — no simulator or headless runtime exists for this platform, and xcrun devicectl reports zero connected devices this session. Cannot be automated or fabricated; blocked at Task 2's checkpoint per this plan's own <important_context>."

# Metrics
duration: ~7min (Task 1 only; Tasks 2-3 blocked on device access)
completed: 2026-08-16
status: blocked
---

# Phase 09 Plan 02: Dimming/Silence Device-Proving (Task 1 complete, Tasks 2-3 blocked) Summary

**Both forks re-signed with the setbrightness/setvolume coercion fix baked in and a 12-test 09-UAT.md authored — device-proving trials themselves remain blocked because zero iPhones are connected to this build machine.**

## Performance

- **Duration:** ~7 min (Task 1 only)
- **Started:** 2026-08-16T10:05:40Z
- **Completed (Task 1):** 2026-08-16T10:07:50Z
- **Tasks:** 1 of 3 completed; 2 blocked at a `checkpoint:human-verify` gate
- **Files modified:** 3 (2 re-signed `.shortcut` artifacts, 1 new `09-UAT.md`) plus 2 tracked dated-archive XMLs

## Accomplishments
- Re-signed `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` and `— Sentient.shortcut` from the `09-01-PLAN.md`-fixed `src/PROSOCHE-Dumb.xml`/`src/PROSOCHE-Sentient.xml`, confirming both signed SHA-256 values differ from `artifacts/shortcuts/MANIFEST.md`'s recorded pre-Phase-9 values — proof the coercion fix is actually baked into the artifact a human will import next.
- Authored `.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md` with the exact structure `05-UAT.md`/`04-UAT.md`/`07-UAT.md` established: frontmatter, `## Current Test` pointing at Test 1, a `## Context` section explaining why the coercion-chip check is a hard gate (not a formality), and 12 numbered `### N.` test entries covering ROADMAP.md Phase 9 criteria 2-7, closed with `## Summary` (`total: 12, passed: 0, issues: 0, skipped: 0`) and a placeholder `## Verdict`.
- Wrote the DEV-06 restore-ownership first-principles design write-up as its own `#### ` subsection inside `## Context`, covering all four required points: (a) why the current no-ownership-check design is already correct for the two-session overlap case (traced through `active_session`'s single-slot design and SESS-03's race protocol), (b) the specific stuck-dim/stuck-quiet regression a naive `changed_by_session_id` equality check would introduce, (c) the explicit decision this plan tests (do not implement a naive check; let Tests 9-10 look for a real gap), and (d) why the Session ID scope defect becomes a hard prerequisite if a check is ever implemented later.
- Confirmed via `xcrun devicectl list devices` that zero iPhones are connected this session (matches the open `DIST-03` blocker already on record in `STATE.md`), so Task 2's coercion-chip gate and Task 3's device trials cannot proceed — per this plan's own explicit instructions, did not fabricate or guess a device-test result to force completion.

## Task Commits

1. **Task 1: Sign both post-fix forks and author 09-UAT.md (including the DEV-06 design write-up)** - `0f923f4` (feat)

**Plan metadata:** (this commit, `docs(09-02): complete Dimming/Silence device-proving plan` — see below)

## Checkpoint

Tasks 2 and 3 (`type="checkpoint:human-verify"`, `gate="blocking"`) require a real, Apple-Intelligence-capable iPhone running iOS 26.x with Shortcuts.app installed. This session's `xcrun devicectl list devices` reports "No devices found" — consistent with the pre-existing `DIST-03` blocker in `STATE.md`. There is no simulator or headless Shortcuts runtime on any platform (`TOOLKIT_SNAPSHOT.md`), so this cannot be worked around automatically.

`.planning/config.json` has `workflow.auto_advance: true`, which would normally auto-approve a `checkpoint:human-verify`. This plan's own `<important_context>` explicitly instructs against that here: auto-approving would mean fabricating a device-test result, which this project's `.claude/CLAUDE.md` do-not-fabricate rule forbids outright. Task 2 is therefore genuinely blocked, not skipped — `09-UAT.md`'s Test 1 remains `result: pending`, and Task 3 cannot begin until Test 1 resolves to `pass` (per Task 3's own `<precondition>`).

**What a human needs to do to unblock:** connect a real, Apple-Intelligence-capable iPhone (15 Pro or later) running iOS 26.x, transfer the freshly re-signed `.shortcut` files from `artifacts/shortcuts/`, and work through `09-UAT.md` Tests 1-12 in order (via `/gsd-verify-work 9` or directly), following the exact `<how-to-verify>` steps recorded in `09-02-PLAN.md`'s Task 2 and Task 3.

## Files Created/Modified
- `.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md` (new) - 12-test device-proving checklist plus the DEV-06 design write-up; all tests `result: pending`
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` - re-signed from `src/PROSOCHE-Dumb.xml` (carries the 09-01-PLAN.md coercion fix)
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` - re-signed from `src/PROSOCHE-Sentient.xml` (same fix)
- `artifacts/shortcuts/2026-08-16/PROSOCHĒ — Nine Circles — Dumb-200504.xml`, `— Sentient-200516.xml` (new, tracked) - dated unsigned archives produced by the signer, following the existing `2026-08-13/` precedent already tracked in this repo

## Decisions Made
- Did not touch `MANIFEST.md` in this task, per the plan's explicit instruction that rewriting it is a separate, already-tracked backlog item.
- Tracked the new `artifacts/shortcuts/2026-08-16/` dated archive directory (matching the existing `2026-08-13/` precedent already committed to this repo), rather than leaving it untracked or gitignoring it.
- Gave the DEV-06 write-up its own `#### ` (H4) heading rather than `### ` (H3), so it does not inflate the plan's own `grep -c "^### "` verify command past the required count of exactly 12.
- Left `requirements-completed: []` — RESTORE-02 through RESTORE-07 all require device evidence this plan has not yet obtained; marking them complete from Task 1's static work alone would misrepresent the plan's actual state.

## Deviations from Plan

None - Task 1 executed exactly as written. Tasks 2-3 are not deviations; they are the plan's own anticipated `checkpoint:human-verify` outcome given zero connected devices, explicitly called out in this plan's `<important_context>` as the expected result of this session.

## Issues Encountered
None beyond the pre-existing, already-documented device-access blocker (`DIST-03`).

## User Setup Required

**Physical device access required to proceed.** See the Checkpoint section above:
- Connect a real, Apple-Intelligence-capable iPhone (15 Pro+) running iOS 26.x
- Import both freshly re-signed `.shortcut` files from `artifacts/shortcuts/`
- Work through `09-UAT.md` Tests 1-12 (via `/gsd-verify-work 9`), starting with the Test 1 coercion-chip gate

## Next Phase Readiness
- Task 1's artifacts (signed forks + fully-authored `09-UAT.md`) are ready for a human to pick up the moment a device is available — no further build-machine work is needed to unblock Tasks 2-3.
- Phase 9's written verdict (ROADMAP criterion 7 / RESTORE-07) cannot be produced until `09-UAT.md`'s 12 tests resolve; this plan is not complete until that happens.
- The main-line ship-readiness cut (`.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md`) proceeds independently of this plan's outcome, per this phase's own objective.

---
*Phase: 09-reintroduce-and-validate-dimming-silence-stateful-restore-on*
*Completed: 2026-08-16 (Task 1 only; Tasks 2-3 blocked)*
