---
created: 2026-08-15T21:05:00.000Z
title: Re-fork Sentient now that Dumb's OPEN path is device-confirmed
area: general
severity: major
files:
  - tools/build_sentient.py
  - src/PROSOCHE-Sentient.xml
---

## Problem

`tools/build_sentient.py` forks `src/PROSOCHE-Dumb.xml` additively and has not been
re-run since build `2026-08-14k`. It therefore does NOT yet carry any of the fixes from
cycles 14, 15, or 16 of the `open-routing-sequence-error` debug session (the date-
coercion fixes, the compound-value/`get_value()` fixes, the `pending_exit`
container/leaf restructure, or the `filter.notes` result-bound fix) — all of which are
now device-confirmed correct on the Dumb fork (build `2026-08-15o`).

Separately, the Sentient-only `If [Audit Token] contains` condition is known to render
red in Shortcuts.app's UI (recorded in `HANDOFF.md` §6 item 6, out of scope while
Sentient was parked). This is very likely the same `WFConditionalActionString` /
operand-coercion family as the Dumb-fork sites tracked in the sibling todo
`2026-08-15-fix-red-operator-and-list-wrapper-defects.md`, and should be checked against
whatever donor evidence that todo settles before assuming it needs a separate fix.

## Solution

1. Confirm branch is `codex/automation-parameter-diagnosis` and the provenance guard
   (`git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD`) passes,
   per `.claude/CLAUDE.md`'s Constraints.
2. Re-run `python3 tools/build_sentient.py` so it picks up every cycle-14/15/16 fix from
   `src/PROSOCHE-Dumb.xml` (the script forks additively; no manual merge should be
   needed, but confirm the shared guards — `verify_string_envelopes`,
   `verify_output_names`, `verify_required_pickers`, `verify_router_shape`,
   `verify_compound_value_reads`, `verify_pending_exit_seed`, `verify_sentinel_gates` —
   all run against the Sentient build too, per this session's own recurring finding that
   Sentient-only insertions have twice bypassed a Dumb-only guard pass).
3. Validate (`bin/validate-shortcut --target-macos 26 --target-platform ios`), sign, and
   decrypt-verify the shipped `.shortcut` directly (per `.claude/CLAUDE.md` §8), the same
   discipline used for every Dumb cycle in the closed debug session.
4. Re-check the `If [Audit Token] contains` red-render against whatever fix pattern the
   `WFConditionalActionString`/`WFItems` todo establishes for the Dumb fork; do not
   assume it needs an independent investigation without first checking for shared root
   cause.
5. This is genuinely new-build risk (Sentient has never been device-tested in this
   session at all) — treat the first Sentient device pass with the same rigor as the
   Dumb session: breadcrumb bisection is already wired in from the shared generator,
   predict breadcrumb positions before the device run, and record results the same way
   `.planning/debug/resolved/open-routing-sequence-error.md` does, opening a fresh debug
   session if a new defect surfaces (Sentient has additional On-Device `Use Model`
   actions with their own unverified model-source literal — see CLAUDE.md §3 item 15 —
   that the Dumb session never exercised).

## Related

- `.planning/debug/resolved/open-routing-sequence-error.md` — the closed session whose
  fixes this todo propagates to the second fork.
- `.planning/debug/HANDOFF.md` §6 item 12 (resume checklist item 5) — this todo's origin.
