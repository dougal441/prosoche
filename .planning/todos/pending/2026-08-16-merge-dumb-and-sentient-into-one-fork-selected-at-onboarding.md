---
created: 2026-08-16T00:19:00.000Z
title: Merge Dumb and Sentient into one fork, selected at onboarding
area: general
severity: major
files:
  - tools/build_state_engine.py
  - tools/build_sentient.py
  - PROSOCHE_Nine_Circles_Canonical_Strategy.md
---

## Problem

Ship **one** shortcut instead of two, with the user choosing at onboarding whether the
on-device model is used. Today the product is two separately-generated, separately-signed
artifacts (`Dumb` / `Sentient`, becoming `Core` / `Aware` under Build Addendum 01), and the
user must know before downloading which one their phone supports.

The case for merging is strong from a UX standpoint: it removes a decision the user is
badly placed to make (few people know whether their iPhone is Apple-Intelligence-capable),
removes a support burden, removes the "I installed the wrong one" failure, and removes an
entire duplicated build/sign/verify pipeline that has already caused real problems —
Sentient is currently **three debug cycles stale** precisely because it is a second artifact
that has to be remembered separately.

**This requires a canonical-strategy amendment.** §35's decision table says `AI | Two
product forks`, §5.7 justifies the split on hardware capability, and §13 explicitly warns
"do not build Dumb as a degraded afterthought." §31 makes two signed `.shortcut` files the
stated deliverable, and the ROADMAP calls dual distribution "this project's definition of
done." Per §38, the document wins over conversation unless it is amended — so the first
deliverable is a recorded decision, not code.

**Three technical risks that decide whether this is even buildable:**

1. **Capability detection is UNVERIFIED.** A merged artifact must behave correctly when
   installed on a non-Apple-Intelligence iPhone. There is no verified way in this project's
   evidence base to *ask* iOS whether the on-device model is available. Whether an `askllm`
   action on an incapable device errors, hangs, or degrades silently is unknown — and a
   hard error would break the deterministic engine for the exact users who most need the
   Dumb path. This must be settled by donor/device evidence before the merge is designed.
2. **The On-Device literal is still unrecovered** (CAP-26 / UA-02). In a two-fork world
   that blocks Sentient only. In a merged world it blocks *everyone*, because the AI path
   ships to every user even if most keep it off. See
   `2026-08-16-recover-the-use-model-on-device-literal.md`.
3. **Determinism must be provably untouched.** §31 and §38: Sentient is an additive wrap
   that must never alter the deterministic engine. A merged artifact makes that harder to
   assert, since both paths now live in one graph. The build guards must be able to prove
   the AI path cannot reach arithmetic, thresholds, timers, Circle IX, or any safety
   decision.

Note also that the scientific argument for two forks survives the merge: §13 and §33
Question 4 want Dumb as a **control baseline** for comparing against Sentient. A runtime
toggle preserves that comparison as long as the setting is recorded and stable.

## Solution

1. **Amend the strategy first.** Update §35's decision table, §5.7, §31's deliverables and
   the ROADMAP's definition of done together, so the document stays internally consistent.
   Record the reasoning — this is a deliberate reversal, not a drift.
2. **Settle capability detection before designing anything.** Build a donor shortcut with a
   single `Use Model` action, run it on a **non-capable** iOS 26 device if one is
   available, and observe what actually happens. If no incapable device is reachable, that
   is itself a finding: the merge cannot be safely shipped without it, and the two-fork
   design should stand until it can be tested. Do not design around an assumption here.
3. **Design the gate as deterministic-first.** The AI path must be entered only when
   `ai_enabled` is true **and** a capability check passes, with every failure — unavailable,
   slow, malformed, errored — falling through to the Dumb path (§14.3, §32). The existing
   fallback architecture already requires this; the merge just makes it load-bearing for
   everyone.
4. **Add the selection to onboarding**, per §7.1's rule that import questions stay simple
   and robust. Note the existing constraint that `WFWorkflowImportQuestions` is a
   literal-text-prefill mechanism, not a form builder — a "use on-device intelligence?
   yes/no" question already exists for the Sentient fork and is the natural model. Make the
   choice changeable afterwards from the manual menu (`Toggle On-Device AI`), since users
   will not know what they want at import time.
5. **Keep the build guards fork-aware.** The Sentient-only insertions have twice bypassed a
   Dumb-only guard pass; in a merged generator every guard must run over the whole graph.
6. **Re-run the full device UAT set against the merged artifact** in both modes (AI on, AI
   off). A merged build is a new artifact, not a repackaging — it inherits none of the
   Dumb fork's device confirmation for free.
7. **Sequencing.** Do not start this before the Sentient re-fork
   (`2026-08-15-fork-sentient-post-openpath-fix.md`) lands. Merging a three-cycles-stale
   Sentient into a device-confirmed Dumb would fold known-broken code into the one artifact
   everyone gets.

## Related

- Canonical strategy §5.7 (device split), §13 (Dumb is the baseline, not a degraded
  afterthought), §14.3 (fallbacks), §31 (deliverables — two signed files), §33 Question 4
  (Dumb as control), §35 (`AI | Two product forks`), §38 (the document wins).
- `PROSOCHE_Build_Addendum_01.md` §2 — Core/Aware naming, which a merge makes moot or
  changes into a mode name rather than a product name.
- `2026-08-15-fork-sentient-post-openpath-fix.md` — hard prerequisite.
- `2026-08-16-recover-the-use-model-on-device-literal.md` — becomes blocking for all users.
- `2026-08-16-optimise-ux-onboarding-and-functionality.md` — the onboarding flow this selection lands in.
