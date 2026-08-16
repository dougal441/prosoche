---
task: 260817-2ng
slug: use-model-literal-reconciliation
type: quick
created: 2026-08-17
---

# Quick Task: Reconcile the stale Use Model On-Device literal audit trail

## Objective

Close todo #12 / UA-02 / CAP-26 as **bookkeeping**. The `WFLLMModel` On-Device literal was
already recovered by device export on 2026-08-13 (`docs/device-evidence/UseModel-OnDevice.xml`,
commit `013a217`) and is already hardcoded in `tools/build_sentient.py:29`. Only the audit
trail is stale. Documentation only — no rebuild, no re-sign, no code change.

## Established facts (verified before editing)

- `docs/device-evidence/UseModel-OnDevice.xml` line 17: `WFLLMModel` = `Apple Intelligence on Device`
- `tools/build_sentient.py:29`: `MODEL = "Apple Intelligence on Device"  # direct device-export evidence`
- `013a217` — "feat(01): device evidence — On-Device literal recovered, iOS Color Filters identifier corrected"
- `docs/BUILD-NOTES.md` §11 already records the recovery; §4/§5/§6/§7 never caught up.

## Tasks

1. **CAP-26** (`docs/BUILD-NOTES.md` §4) — literal status token `UNRECOVERED-LOCALLY` →
   `ROUND-TRIP-CONFIRMED`, recording the literal verbatim and citing the device-evidence file,
   §11, and `013a217`. Keep the three-attempt local-recovery narrative (still accurate about the
   *bundle*, and it explains why a device export was needed). Append, do not delete.
2. **DEV-03** (§5) — close, citing the same evidence. Update the §7.B deviation index row.
3. **UA-02** (§6) — close, recording what was actually recovered. Update §7.A summary row.
4. **BD-04** (`docs/CAPABILITY-DECISIONS.md`) — append a `BD-04-R2` record noting Branch A was
   subsequently reached, in the style of BD-01-R / BD-04-R / BD-01-R2. Do not rewrite BD-04's
   original reasoning.
5. **`.planning/STATE.md`** — the "device-evidenced Apple Intelligence on Device model literal"
   line is the accurate one; reconcile in that direction and note the reconciliation. Add the
   Quick Tasks Completed row.
6. **Todo** — move `.planning/todos/pending/2026-08-16-recover-the-use-model-on-device-literal.md`
   to `completed/` with a dated closing note.

## The one thing that must NOT be claimed done

Step 5 of the source todo — confirming **on device, with no network available**, that
`Use Model` actually runs on-device and cannot silently fall back to Private Cloud Compute —
remains **open** and needs an Apple-Intelligence-capable iPhone (15 Pro+). It must be recorded
explicitly as the single remaining open item. **User-facing on-device guarantee copy (README,
the Control Room Note, release text) stays unchanged** until that check passes. Do not soften
this to "verified".

## Constraints

- Do not touch `tools/build_sentient.py` — already correct.
- No rebuild, no re-sign, no renames.
- Append rather than delete in the audit documents.
- ROADMAP.md untouched.

## Success criteria

- [ ] CAP-26 reads `ROUND-TRIP-CONFIRMED` with the literal and its evidence
- [ ] DEV-03 and UA-02 closed
- [ ] BD-04 notes Branch A reached, by appended record
- [ ] Runtime no-network check recorded as the one remaining open item; no guarantee copy changed
- [ ] `tools/build_sentient.py` absent from `git diff --stat`
- [ ] Todo moved to `completed/` with closing note
- [ ] STATE.md Quick Tasks table updated; ROADMAP.md untouched
- [ ] Committed atomically
