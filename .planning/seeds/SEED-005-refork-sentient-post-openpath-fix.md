---
id: SEED-005
status: dormant
planted: 2026-08-16
planted_during: PROSOCHĒ Nine Circles — post OPEN-path device confirmation
trigger_when: whenever Sentient work resumes — hard prerequisite for SEED-006 (merge Dumb/Sentient)
scope: small — re-run an existing generator script, then a first Sentient device pass
---

> **COVENANT OVERHAUL (2026-08-19):** Owned by Phase 20 (Aware verdict alignment), which rebuilds Aware from the post-conversion Core rather than patching it.


# SEED-005: Re-fork Sentient now that Dumb's OPEN path is device-confirmed

## Why This Matters

`tools/build_sentient.py` forks `src/PROSOCHE-Dumb.xml` additively and has not been re-run
since build `2026-08-14k` — it does not yet carry any of the fixes from cycles 14, 15, or
16 of the `open-routing-sequence-error` debug session (date-coercion, compound-value/
`get_value()`, the `pending_exit` container/leaf restructure, the `filter.notes`
result-bound fix), all of which are now device-confirmed on the Dumb fork
(build `2026-08-15o`).

Separately, the Sentient-only `If [Audit Token] contains` condition is known to render red
in Shortcuts.app's UI — very likely the same `WFConditionalActionString`/operand-coercion
family as the Dumb-fork red-operator todo, and should be checked against whatever donor
evidence that todo settles before assuming it needs a separate fix.

## When to Surface

**Trigger:** whenever Sentient work resumes. This is a **hard prerequisite** for SEED-006
(merging Dumb and Sentient into one fork) — merging a three-cycles-stale Sentient would
fold known-broken code into the one artifact everyone gets.

This seed will surface during `/gsd-new-milestone` when the milestone scope touches the
Sentient fork, `tools/build_sentient.py`, or Apple On-Device Intelligence.

## Scope Estimate

**Small.** Confirm provenance guard, re-run the generator (forks additively, no manual
merge expected), confirm all shared build guards run against the Sentient build too
(they've bypassed a Dumb-only guard pass twice before), validate/sign/decrypt-verify, then
treat the first Sentient device pass with full debug-session rigor since Sentient has never
been device-tested in this project at all.

## Breadcrumbs

- `.planning/debug/resolved/open-routing-sequence-error.md` — the closed session whose
  fixes this propagates to the second fork.
- `.planning/debug/HANDOFF.md` §6 item 12 — this seed's origin.
- SEED-006 (Merge Dumb and Sentient) — depends on this landing first.
- The red-operator/`WFItems` todo (Dumb fork) — check for shared root cause before treating
  Sentient's red-render as a separate investigation.

## Notes

Originally captured as a standalone todo
(`2026-08-15-fork-sentient-post-openpath-fix.md`); full original text preserved in git
history — `git log -p -- .planning/todos/pending/2026-08-15-fork-sentient-post-openpath-fix.md`.
