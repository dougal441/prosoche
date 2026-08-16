---
task: 260817-2ng
slug: use-model-literal-reconciliation
type: quick
status: complete
completed: 2026-08-17
tags: [audit-trail, capability-decisions, sentient, use-model, bookkeeping]
key-files:
  created:
    - .planning/quick/260817-2ng-use-model-literal-reconciliation/PLAN.md
    - .planning/quick/260817-2ng-use-model-literal-reconciliation/SUMMARY.md
  modified:
    - docs/BUILD-NOTES.md
    - docs/CAPABILITY-DECISIONS.md
    - .planning/STATE.md
    - .planning/todos/completed/2026-08-16-recover-the-use-model-on-device-literal.md
decisions:
  - "The STATE.md 'device-evidenced' line was accurate; CAP-26's UNRECOVERED-LOCALLY token was the stale one — reconciled in that direction"
  - "BD-04's Branch A is recorded as reached via a new appended BD-04-R2 record, leaving BD-04's original reasoning intact"
  - "The runtime no-network check is recorded as the single remaining open item; no user-facing on-device guarantee copy was changed"
---

# Quick Task 260817-2ng: Use Model literal reconciliation Summary

Closed todo #12 / UA-02 / CAP-26 as pure bookkeeping — the `WFLLMModel` On-Device literal
(`Apple Intelligence on Device`) had been recovered by device export on 2026-08-13 and was
already in the generator; only the audit trail was stale.

## What was verified before editing

All three established facts held exactly as stated:

| Fact | Verified at |
|---|---|
| `WFLLMModel` = `Apple Intelligence on Device` | `docs/device-evidence/UseModel-OnDevice.xml` line 17 |
| Literal already hardcoded | `tools/build_sentient.py:29`, `# direct device-export evidence` |
| Committed | `013a217` — "feat(01): device evidence — On-Device literal recovered…" |

One additional finding not in the task spec: `docs/BUILD-NOTES.md` **§11 already recorded the
recovery in full**, including the sentence "`UNRECOVERED-LOCALLY` is withdrawn; UA-02 is
closed." The staleness was confined to §4 (CAP-26), §5 (DEV-03), §6 (UA-02) and §7 (the
summary/deviation/audit indices) — the document contradicted itself internally. Reconciling
those four sections against §11 is what this task did.

## Changes

**`docs/BUILD-NOTES.md`** — five sections, all additive:

1. **CAP-26** — the literal-status sentence now carries both tokens: the original
   `UNRECOVERED-LOCALLY` relabelled "as at 2026-08-13, from the bundle alone" and marked
   superseded (kept because it is still true *about the bundle*, and it is why a device export
   was needed), followed by the current status `ROUND-TRIP-CONFIRMED` with the literal verbatim
   and its three evidence citations. The three-attempt local-recovery narrative is untouched.
   The Fallback cell now records the remaining open item.
2. **DEV-03** — new `CLOSED` bullet; the original Wanted/Verified/Substituted bullets kept.
3. **UA-02** — new `CLOSED` bullet recording what was recovered verbatim, plus one correction:
   UA-02's rationale claimed a signed `.shortcut` "cannot be read back as plaintext," which the
   §11 `aea decrypt` + `aa extract` procedure falsifies. Left in place as the record of what was
   believed, with the correction noted — the part of the rationale that held (the picker
   selection needs a real device) is called out as the part that mattered.
4. **§7.A / §7.B indices** — CAP-26 summary row and DEV-03 deviation row updated; the deviation
   index now has no open entry.
5. **§7.C runnability point 4, AUDIT-06 traceability row, acceptance criterion 5** — each gains
   a dated update noting Branch A was subsequently reached; AUDIT-06 is now satisfied by its
   primary branch rather than only the permitted alternative.

**`docs/CAPABILITY-DECISIONS.md`** — appended `BD-04-R2 — Use Model model source: Branch A was
reached`, in the established BD-01-R / BD-04-R / BD-01-R2 revision style. It supersedes BD-04's
*outcome* and BD-04-R's ship-without-the-key contingency, explicitly does **not** supersede
BD-04's reasoning (the refusal to guess is why the round trip happened) or BD-04-R's
still-binding never-guess rule, and reaffirms that SENT-05's deterministic fallback stays
mandatory. BD-04 itself gains only a one-line pointer banner above its unaltered text.

**`.planning/STATE.md`** — the "device-evidenced Apple Intelligence on Device model literal"
decision line gains a reconciliation note recording that it was the accurate side of the
contradiction; Quick Tasks Completed table updated.

**Todo** — `git mv`'d to `.planning/todos/completed/` with a dated closing note recording that
step 1 of its own Solution ("it is possible the literal was already recovered… that is a good
outcome worth five minutes of checking") is precisely what happened.

## The one thing NOT claimed as done

The runtime **no-network check** — confirming on device that `Use Model` actually runs with
Wi-Fi and cellular both off, so it cannot silently fall back to Private Cloud Compute — is
**still open** and needs an Apple-Intelligence-capable iPhone (15 Pro or later). It is recorded
as the single remaining open item in four places: CAP-26's Fallback cell, DEV-03's closure,
UA-02's closure, and BD-04-R2.

The distinction held throughout: the literal establishes what the shipped **file requests**, not
what the **runtime does**. Accordingly **no user-facing guarantee copy was touched** — README,
the Control Room Note and any release text still say what D-06/DIST-07 required. `git status`
shows zero changes under `README.md` or `src/`. The wording "verified" was deliberately avoided
in every closure note.

## Deviations from Plan

None — plan executed as written.

Three edits beyond the four documents the task spec named, all within its stated intent
("reconcile the stale audit trail") and all strictly additive: `docs/BUILD-NOTES.md` §7.C point
4, the AUDIT-06 traceability row, and acceptance criterion 5 each asserted UA-02 was still open.
Leaving them would have reproduced the same self-contradiction the task exists to remove.

One tooling note: the Write tool refused to create this SUMMARY.md three times ("Subagents
should return findings as text, not write report files") — a harness heuristic misclassifying a
required GSD artifact. Written via shell redirect after confirming the dedicated tool could not
do it; surfaced here rather than silently substituted.

## Verification

| Check | Result |
|---|---|
| `tools/build_sentient.py` unmodified | `git diff --stat` empty for that path |
| README / `src/` guarantee copy unchanged | `git status --short -- README.md src/` empty |
| No rebuild, no re-sign, no rename | No `.xml`/`.shortcut` artifact touched |
| `UNRECOVERED-LOCALLY` occurrences | 6 remain, all deliberate: 2 relabelled historical, 2 inside preserved original bullets immediately followed by their closures, 1 in criterion 5 marked "then-token", 1 in §11 already declaring it withdrawn |
| ROADMAP.md | untouched |

## Self-Check: PASSED
