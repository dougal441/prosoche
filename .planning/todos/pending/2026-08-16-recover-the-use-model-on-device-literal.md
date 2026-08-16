---
created: 2026-08-16T00:18:00.000Z
title: Recover the Use Model On-Device literal (UA-02)
area: general
severity: major
files:
  - docs/CAPABILITY-DECISIONS.md
  - docs/BUILD-NOTES.md
  - tools/build_sentient.py
---

## Problem

This is the **last unresolved capability blocker from Phase 1**, and the only one that
directly contradicts a headline product claim.

The strategy is unambiguous (§5.6, §27, §35): Sentient uses Apple's **On-Device** model
only — never Private Cloud Compute, never ChatGPT, never a network. That guarantee is the
entire basis of the privacy model, and it is what makes "your phone has noticed exactly
what you are doing" acceptable rather than alarming.

But the exact plist literal for the On-Device case of `WFLLMModel` was never recovered.
CAP-26 is recorded as `UNRECOVERED-LOCALLY`, confirmed independently:
`com_apple_shortcuts_wfask_llmmodel_parameter` has no entry in the bundled enum-cases
catalog, there are zero `askllm`/`WFLLMModel` matches across all 19 golden shortcuts, and
the only literal appearing anywhere in the bundle is `"Apple Intelligence"` — a string that
predates the iOS 26 three-way model picker (On-Device / Private Cloud Compute / Extension
Model).

BD-04 took AUDIT-06's Branch B: rather than guess, the guarantee was **explicitly
re-planned**, and Phase 8 was gated — it may build `Use Model` with evidenced parameters
and a deterministic fallback, but **may not write a `WFLLMModel` value or claim On-Device
is enforced** until UA-02 closes. That gate is still closed today.

Two consequences, both live:

1. **The product cannot honestly advertise its central privacy claim** until this is
   settled. Shipping Sentient while telling users it is on-device only, when the file does
   not pin the model source, would be a false claim — not a technical shortcut.
2. `.planning/STATE.md` records that Sentient "uses the device-evidenced Apple
   Intelligence on Device model literal", which reads as though this were resolved. That
   line and CAP-26's `UNRECOVERED-LOCALLY` status cannot both be right. **Reconciling them
   is part of this todo** — determine which is accurate before doing anything else.

A `Use Model.shortcut` donor already sits unanalysed in `.planning/debug/`.

## Solution

1. **Reconcile the contradiction first.** Read `.planning/debug/Use Model.shortcut` and
   `docs/BUILD-NOTES.md` CAP-26 together and establish what is actually known. It is
   possible the literal was already recovered and the audit trail was not updated — in
   which case this todo is mostly bookkeeping, and that is a good outcome worth five
   minutes of checking before starting a device round trip.
2. **If genuinely unrecovered, run the round trip** exactly as §3 item 15 of
   `.claude/CLAUDE.md` specifies, on an Apple-Intelligence-capable iPhone (15 Pro or
   later):
   - build a minimal shortcut in Shortcuts.app containing one `Use Model` action;
   - **manually select On-Device in the Model picker**, save;
   - export and recover the plist (`aea decrypt` + `aa extract`, or Share → Copy for
     unsigned XML);
   - read the resulting `WFLLMModel` literal back verbatim.
3. **Record it as a device-evidenced fact**, not a bundle fact, and hardcode that exact
   literal into `tools/build_sentient.py`. Close CAP-26 and UA-02 in the audit trail.
4. **Keep the deterministic fallback regardless** (§5.6, §14.3, §32): the model may fail,
   be slow, or return malformed output, and Sentient must degrade to Dumb without breaking.
   Recovering the literal does not remove that requirement.
5. **Verify the guarantee holds at runtime, not just in the file** — confirm on device
   that the action runs with no network available. A literal that validates but silently
   falls back to PCC would be worse than no claim at all.
6. **Then update the user-facing copy** (README §26, the Note, any release text) to state
   the on-device guarantee plainly. Until step 5 passes, the product must keep saying what
   D-06/DIST-07 required it to say instead.

## Related

- Canonical strategy §5.6 (Use Model viability), §14 (Sentient), §27 (privacy model — the
  On-Device requirement), §32 (Sentient acceptance criteria), §35 (Cloud LLM: No).
- `.claude/CLAUDE.md` §3 item 15 — the round-trip procedure, and the do-not-guess rule.
- `docs/CAPABILITY-DECISIONS.md` BD-04, `docs/BUILD-NOTES.md` CAP-26.
- `.planning/debug/Use Model.shortcut` — unanalysed donor.
- `2026-08-15-fork-sentient-post-openpath-fix.md` — the Sentient rebuild this unblocks.
- `2026-08-16-merge-dumb-and-sentient-into-one-fork-selected-at-onboarding.md` — a merged
  fork makes this blocking for *all* users, not just Sentient users.
