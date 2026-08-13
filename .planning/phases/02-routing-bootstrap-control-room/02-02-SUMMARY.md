---
phase: 02-routing-bootstrap-control-room
plan: 02
subsystem: automation
tags: [ios-shortcuts, plist-xml, apple-notes, markdown, onboarding-copy]

# Dependency graph
requires:
  - phase: 02-routing-bootstrap-control-room (plan 02-01)
    provides: "The Control Room Body Text action (minimal opening section) and the markdownContents-wired Note-creation action it feeds"
provides:
  - "The complete Control Room Note body: READ THIS FIRST, Automation A (OPEN) and Automation B (CLOSE) exact build steps, the essential-apps safety warning, the six-prompt MY PHONE, ON PURPOSE proforma, CURRENT SETTINGS (interpolated), CURRENT STATE, ATTENTION LEDGER, and the two reserved sections"
  - "An in-file assertion that the Note-creation action's content key is the camelCase markdownContents (not markdown/contents/Contents/markdown_contents), non-empty, and wired to an earlier-assigned Control Room Body variable"
  - "UA-01 in docs/BUILD-NOTES.md extended with the four Phase 2 on-device observations that stand as acceptance evidence for BOOT-04, plus a recorded BD-05 fallback trigger"
  - "docs/BUILD-NOTES.md §9: the canonical Dumb-fork signing name cross-reference for Phase 7"
affects: [02-03, 02-04, phase-7, phase-8]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Note/document body text authored as a Python triple-quoted string with marker tokens, converted to the Unicode object-replacement placeholder and byte offsets programmatically, then hand-inserted into the plist XML at the exact WFTextTokenString/attachmentsByRange indentation depth an existing sibling literal (Default State JSON) already established — never hand-counted"
    - "Where an acceptance criterion requires an identical literal string to appear in two parallel instructional sections (here: the shortcut name in both Automation A and Automation B), write both sections out in full rather than one full section plus a delta reference, so the identity is a verifiable fact in the text rather than an inference the reader has to make"

key-files:
  created: []
  modified:
    - src/PROSOCHE-Dumb.xml
    - docs/BUILD-NOTES.md

key-decisions:
  - "Automation B is written as its own full ten-step numbered list (mirroring Automation A) rather than a single delta paragraph, so the shortcut name PROSOCHĒ — Nine Circles — Dumb appears twice, identically, satisfying the acceptance criterion literally instead of by inference from 'the same way as A'"
  - "Added a new top-level docs/BUILD-NOTES.md §9 for the canonical signing-name cross-reference rather than folding it into an existing section, since no existing section was a content fit without rewording prior append-only text"
  - "The BD-05 fallback trigger is recorded as a new labelled field inside the existing UA-01 entry (not a separate paragraph elsewhere), so the trigger condition sits next to the exact observation that would raise it"
  - "CURRENT STATE / ATTENTION LEDGER / VALUE-LIFE-RETURNED / SUPPORT-PROSOCHĒ are written as the plan specifies — honest first-run placeholders, not fabricated content — since canonical strategy §17 marks the last two permanently reserved and Phase 7 (ROOM-08) is what makes CURRENT STATE and ATTENTION LEDGER dynamic"

requirements-completed: [ROOM-01, ROOM-02, ROOM-03, ROOM-04, ROOM-05, ROOM-06, BOOT-04]

coverage:
  - id: D1
    description: "READ THIS FIRST explains what PROSOCHĒ is before asking anything of the reader, then states plainly that the Shortcut cannot install its own automations and that PROSOCHĒ is bypassable"
    requirement: "ROOM-01"
    verification:
      - kind: other
        ref: "python3 Note-body content check (Task 1 <verify>) — headings/statements/regex assertions"
        status: pass
      - kind: other
        ref: "bin/validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all"
        status: pass
    human_judgment: true
    rationale: "No iPhone or Notes-capable simulator is available in this environment; whether the Note actually renders non-empty, with real markdown headings, on-device is exactly the class of runtime-only fact this plan escalates to UA-01 (docs/BUILD-NOTES.md §6), gated on Phase 2's on-device pass, rather than assumed from a validator-clean file."
  - id: D2
    description: "Automation A (OPEN) gives exact, followable build steps ending in Run Shortcut with input text OPEN, naming the shortcut PROSOCHĒ — Nine Circles — Dumb"
    requirement: "ROOM-02"
    verification:
      - kind: other
        ref: "python3 Note-body content check (Task 1 <verify>) — 'Automation A', 'Is Opened', 'Run Shortcut', 'OPEN' substrings"
        status: pass
    human_judgment: true
    rationale: "Same on-device rendering gap as D1 — UA-01 is the closing verification, not available in this build environment."
  - id: D3
    description: "Automation B (CLOSE) gives exact, followable build steps ending in Run Shortcut with input text CLOSE, same apps and shortcut name as Automation A"
    requirement: "ROOM-03"
    verification:
      - kind: other
        ref: "python3 Note-body content check (Task 1 <verify>) — 'Automation B', 'Is Closed', 'CLOSE' substrings; manual shortcut-name-occurs-twice check"
        status: pass
    human_judgment: true
    rationale: "Same on-device rendering gap as D1."
  - id: D4
    description: "Safety warning names Phone, Wallet, an authenticator, and a password manager as apps not to target, placed immediately after the automation build steps"
    requirement: "ROOM-05"
    verification:
      - kind: other
        ref: "python3 Note-body content check (Task 1 <verify>) — 'Wallet', 'authenticator', 'password manager' substrings"
        status: pass
    human_judgment: false
  - id: D5
    description: "MY PHONE, ON PURPOSE proforma carries all six §7.2 prompts as sub-headings and names all six exits (Capture, Coordinate, Create, Connect, Consult, Close)"
    requirement: "ROOM-06"
    verification:
      - kind: other
        ref: "python3 Note-body content check (Task 1 <verify>) — six prompt-phrase and six exit-name substrings"
        status: pass
    human_judgment: false
  - id: D6
    description: "The empty-body trap is asserted in the file: exactly one Note-creation action, markdownContents present and non-empty, no alternative content-key spelling, wired to a Control Room Body variable assigned earlier in the same branch"
    requirement: "BOOT-04"
    verification:
      - kind: other
        ref: "python3 empty-body gate script (Task 2 <verify>)"
        status: pass
      - kind: other
        ref: "bin/validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all"
        status: pass
    human_judgment: true
    rationale: "The validator and this file-level assertion both pass, but CAP-08's documented failure mode (the wrong key passes validation and yields an empty body at runtime) is by definition invisible to any build-machine check — closing this requires the on-device UA-01 confirmation this plan extended, which cannot run in this environment."

# Metrics
duration: 10min
completed: 2026-08-13
status: complete
---

# Phase 2 Plan 2: Control Room Note Body & the Empty-Body Trap Gate Summary

**The complete `PROSOCHĒ — Control Room` Note body (READ THIS FIRST, Automation A/B build steps, safety warning, six-prompt proforma, settings/state/ledger/reserved sections) plus an in-file gate asserting the camelCase `markdownContents` key that is the one failure mode a green validator cannot catch.**

## Performance

- **Duration:** ~10 min
- **Completed:** 2026-08-13T03:01:49Z
- **Tasks:** 2 completed
- **Files modified:** 2 (0 created, 2 modified)

## Accomplishments

- `src/PROSOCHE-Dumb.xml`'s `Control Room Body` `Text` action literal grew from 02-01's 534-character opening section to a 5,121-character complete Note: READ THIS FIRST (what PROSOCHĒ is, plus the unhedged cannot-self-install and bypassable statements), Automation A — OPEN and Automation B — CLOSE as two full, parallel ten-step numbered lists (the shortcut name `PROSOCHĒ — Nine Circles — Dumb` appears identically in both), an unmissable "Do not target these apps" safety warning immediately after, the six-prompt `MY PHONE, ON PURPOSE` proforma naming all six exits, `CURRENT SETTINGS` (interpolating `Import Descent`/`Import Voice` through two new `￼` placeholders and matching `attachmentsByRange` entries), and the `CURRENT STATE` / `ATTENTION LEDGER` / `VALUE / LIFE RETURNED` / `SUPPORT PROSOCHĒ` sections exactly as canonical strategy §17 and the plan specify
- Zero exclamation marks, zero emoji, no claim about an in-app feeling or an AI capability the Dumb fork does not have — verified programmatically, not just by eye
- The one structural change to the action graph was converting the `Control Room Body` literal from a plain `<string>` to a `WFTextTokenString` dict (`Value.string` + `attachmentsByRange`) — no action added, removed, or reordered; `WFWorkflowImportQuestions` still resolves to indices 2 and 4 with `WFTextActionText` present at both, confirmed by direct re-check after both tasks
- Task 2's empty-body gate confirmed in the file (not just by inspection) that the Note-creation action carries exactly one `markdownContents` key, non-empty, with no `markdown`/`contents`/`Contents`/`markdown_contents` alternative anywhere in the file, wired to `Control Room Body`, which is set by an earlier `Set Variable` action — 02-01 had already wired this correctly, so this task added the assertion and the documentation escalation rather than an XML fix
- `docs/BUILD-NOTES.md` UA-01 extended (not duplicated) with the four Phase 2 on-device observations that are the acceptance evidence for BOOT-04 (Note exists, title matches what `Find Notes` will search for, body populated, markdown headings render as headings), plus a new "Fallback trigger (BD-05)" field naming exactly which observation would trigger the file-based fallback and what that fallback changes; a new §9 records the canonical Dumb-fork signing name for Phase 7. Both edits are strictly additive — confirmed by diffing against the pre-task commit and finding no removed lines

## Task Commits

Each task was committed atomically:

1. **Task 1: Author the complete Control Room Note body** - `6d8cd89` (feat)
2. **Task 2: The empty-body trap — prove the content key and the payload, and escalate what only a device can settle** - `e717c49` (docs)

## Files Created/Modified

- `src/PROSOCHE-Dumb.xml` - The `Control Room Body` `Text` action literal rewritten in place from opening section to complete Note (56 actions, unchanged from 02-01; import-question binding at indices 2/4 re-verified intact)
- `docs/BUILD-NOTES.md` - UA-01 (§6) extended with four Phase 2 observations and a BD-05 fallback-trigger field; new §9 records the canonical Dumb-fork signing name — both edits append-only, verified by diff

## Decisions Made

See `key-decisions` in the frontmatter above for the four decisions requiring justification. In brief: two are authoring-precision choices made to satisfy an acceptance criterion literally rather than by inference (spelling out Automation B in full rather than as a delta, and adding a new BUILD-NOTES.md section rather than reworking an existing one), and two are direct applications of what the plan and canonical strategy already specify (the BD-05 fallback field placed next to UA-01 rather than elsewhere, and the reserved/placeholder sections left exactly as specified rather than embellished).

## Deviations from Plan

None - plan executed exactly as written. No bug fixes, no missing-critical additions, no blocking issues, and no architectural questions arose; both tasks' acceptance criteria were met without weakening any of them.

## Known Stubs

Four sections of the Note body are intentionally static placeholders, exactly as specified by the plan and canonical strategy §17 (not undocumented stubs):

- `## CURRENT STATE` (`src/PROSOCHE-Dumb.xml`, `Control Room Body` literal) — reads "Nothing has been recorded yet. This is the first run." Making this section dynamically refresh on manual run is `ROOM-08`, owned by Phase 7.
- `## ATTENTION LEDGER` (same literal) — reads "Entries begin in later phases of this build." Real entries begin once OPEN/CLOSE handling exists (Phase 3 onward) and the writer itself is Phase 7's (`ROOM-08` family).
- `## VALUE / LIFE RETURNED` and `## SUPPORT PROSOCHĒ` (same literal) — each reads "Reserved. Nothing is \[measured/asked for\] here yet." Canonical strategy §17 marks both permanently reserved for a later design that is not yet scheduled anywhere in `.planning/ROADMAP.md` or `.planning/REQUIREMENTS.md`; the plan's own instruction is explicit not to invent content here or imply a future paid gate.

None of these prevent this plan's own goal — a reader with only this Note can finish installing PROSOCHĒ and start filling in the proforma — since none of the four are load-bearing for onboarding.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required. This plan's work is fully covered by the existing UA-01 item (now extended) in `docs/BUILD-NOTES.md` §6, gated on Phase 2's on-device confirmation pass; no new user action item was created, per the plan's explicit instruction not to compete with UA-01.

## Next Phase Readiness

`src/PROSOCHE-Dumb.xml` still validates at `--target-macos 26 --target-platform all` and its Control Room Note is now complete and content-correct by every check this build machine can run. Ready for 02-03 (OPEN/CLOSE/fail-safe routing bodies) and 02-04 (state-load-and-do-not-overwrite, Note-existence guard, import-answer normalisation) to extend in place, strictly below action index 5. The remaining open item is unchanged from 02-01: UA-01 (now covering all four Phase 2 on-device observations, including the two this plan added) should be confirmed at the earliest real on-device import: whether `markdownContents` produces a genuinely non-empty, correctly-headed Note is the one fact nothing in this repository can settle without a device.

---
*Phase: 02-routing-bootstrap-control-room*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: `src/PROSOCHE-Dumb.xml`
- FOUND: `docs/BUILD-NOTES.md`
- FOUND: `.planning/phases/02-routing-bootstrap-control-room/02-02-SUMMARY.md`
- FOUND: commit `6d8cd89`
- FOUND: commit `e717c49`
