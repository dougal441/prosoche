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

## Closed — 2026-08-17 (quick task `260817-2ng`)

**Closed as bookkeeping.** Step 1 of the Solution above ("it is possible the literal was
already recovered and the audit trail was not updated — in which case this todo is mostly
bookkeeping, and that is a good outcome worth five minutes of checking") is exactly what
happened. No device round trip was needed or performed.

The recovery had already taken place on **2026-08-13**: `WFLLMModel` = `Apple Intelligence on
Device`, recovered from a device export at `docs/device-evidence/UseModel-OnDevice.xml` line 17,
written up in `docs/BUILD-NOTES.md` §11, committed in `013a217`, and already hardcoded at
`tools/build_sentient.py:29` (`# direct device-export evidence`). Only §4/§5/§6/§7 of
BUILD-NOTES and BD-04 had not caught up. The contradiction named in Problem point 2 resolved in
favour of `.planning/STATE.md` — its "device-evidenced" line was right and CAP-26's
`UNRECOVERED-LOCALLY` token was the stale one.

Reconciled: CAP-26 now reads `ROUND-TRIP-CONFIRMED` with the literal and its evidence; DEV-03
and UA-02 are closed (and their §7 index rows updated); `docs/CAPABILITY-DECISIONS.md` gains
BD-04-R2 recording that BD-04's **Branch A** was reached. Steps 2 and 3 of the Solution are
satisfied by the prior work; step 4 (deterministic fallback, SENT-05) is untouched and remains
mandatory. `tools/build_sentient.py` was not modified — it was already correct.

**Still open — needs a device.** Step 5 of the Solution is **not** done: nobody has confirmed on
device that `Use Model` actually runs with **no network available**, i.e. that it cannot
silently fall back to Private Cloud Compute despite the On-Device literal. That needs an
Apple-Intelligence-capable iPhone (15 Pro or later) with Wi-Fi and cellular both off. The
literal proves what the *file requests*, not what the *runtime does*.

Consequently **step 6 is also not done and must not be done yet**: the user-facing on-device
guarantee copy (README §26, the Control Room Note, any release text) is deliberately
**unchanged** and still says what D-06/DIST-07 required. A literal that validates but silently
falls back to PCC would be worse than no claim at all. This is not to be described as verified.

Tracked going forward in `docs/BUILD-NOTES.md` §6 (UA-02 closure note) and
`docs/CAPABILITY-DECISIONS.md` BD-04-R2 as the single remaining open item on this capability.
