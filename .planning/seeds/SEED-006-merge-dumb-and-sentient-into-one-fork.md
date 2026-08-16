---
id: SEED-006
status: dormant
planted: 2026-08-16
planted_during: PROSOCHĒ Nine Circles — post OPEN-path device confirmation
trigger_when: after SEED-005 (Sentient re-fork) lands, and only after capability detection is settled by donor/device evidence
scope: large — requires a canonical-strategy amendment plus new device evidence before design can start
---

# SEED-006: Merge Dumb and Sentient into one fork, selected at onboarding

## Why This Matters

Ship **one** shortcut instead of two, with the user choosing at onboarding whether the
on-device model is used, rather than two separately-generated, separately-signed
artifacts the user must pick between before downloading. The UX case is strong: removes a
decision the user is badly placed to make (few know if their iPhone is
Apple-Intelligence-capable), removes support burden, removes "installed the wrong one,"
and removes a duplicated build/sign/verify pipeline that has already caused real
problems — Sentient is currently three debug cycles stale precisely because it's a second
artifact that has to be remembered separately.

**This requires a canonical-strategy amendment.** §35 says `AI | Two product forks`, §5.7
justifies the split on hardware capability, §13 warns against building Dumb as a "degraded
afterthought," §31 makes two signed `.shortcut` files the stated deliverable. Per §38, the
document wins over conversation unless amended — the first deliverable is a recorded
decision, not code.

Three technical risks decide whether this is even buildable:

1. **Capability detection is UNVERIFIED.** No verified way in this project's evidence base
   to *ask* iOS whether the on-device model is available. Whether `askllm` on an incapable
   device errors, hangs, or degrades silently is unknown — a hard error would break the
   deterministic engine for exactly the users who most need the Dumb path.
2. **The On-Device literal is still unrecovered** (CAP-26/UA-02) — in a merged world this
   blocks *everyone*, since the AI path ships to every user even if most keep it off.
3. **Determinism must be provably untouched** — §31/§38 require Sentient stay a
   non-mutating additive wrap; a merged artifact makes that harder to assert since both
   paths live in one graph.

Note the scientific case for two forks survives the merge (§13, §33 Q4 want Dumb as a
control baseline) — a runtime toggle preserves that comparison as long as the setting is
recorded and stable.

## When to Surface

**Trigger:** after `2026-08-15-fork-sentient-post-openpath-fix` (SEED-005) lands, and only
after capability detection is settled by donor/device evidence on a non-Apple-Intelligence
device. Do not design around an assumption here — if no incapable device is reachable to
test on, that is itself a finding that the two-fork design should stand.

This seed will surface during `/gsd-new-milestone` when the milestone scope touches
onboarding, distribution, or the Dumb/Sentient fork split.

## Scope Estimate

**Large.** Strategy amendment across §35/§5.7/§31/ROADMAP, a capability-detection donor
test, a deterministic-first gate design (`ai_enabled` + capability check, every failure
falls through to Dumb), onboarding import-question changes, fork-aware build guards, and a
full re-run of the device-UAT set against the merged artifact in both AI-on and AI-off
modes — a merged build inherits none of the Dumb fork's device confirmation for free.

## Breadcrumbs

- Canonical strategy §5.7 (device split), §13 (Dumb as baseline, not afterthought), §14.3
  (fallbacks), §31 (deliverables), §33 Q4 (Dumb as control), §35 (`AI | Two product
  forks`), §38 (document wins).
- `PROSOCHE_Build_Addendum_01.md` §2 (Core/Aware naming — a merge makes this a mode name
  rather than a product name).
- SEED-005 (Re-fork Sentient) — hard prerequisite.
- The "Recover the Use Model On-Device literal" todo — becomes blocking for all users once
  merged.
- The "Optimise UX — onboarding" todo — the onboarding flow this selection lands in.

## Notes

Originally captured as a standalone todo
(`2026-08-16-merge-dumb-and-sentient-into-one-fork-selected-at-onboarding.md`); full
original text (including the capability-detection risk table) preserved in git history —
`git log -p -- .planning/todos/pending/2026-08-16-merge-dumb-and-sentient-into-one-fork-selected-at-onboarding.md`.
