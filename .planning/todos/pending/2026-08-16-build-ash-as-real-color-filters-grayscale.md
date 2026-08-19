---
created: 2026-08-16T23:22:00.000Z
title: Build Ash as real Color Filters grayscale
area: general
severity: major
files:
  - tools/build_state_engine.py:486
  - src/CONFIG-BLOCK.md:80
  - docs/CAPABILITY-DECISIONS.md
---

## Problem

**Ash ships as an alert box.** The entire primitive is:

```python
def ash():
    return [comment("""Ash is the validator-clean visual-pause fallback:
- It changes no accessibility setting.
- Color Filters is deliberately excluded because the iOS action is not validator-supported."""),
            alert("Ash", "Pause. Put the phone down for one breath.")]
```

`UAToggleColorFilters` appears **zero times** in `src/PROSOCHE-Dumb.xml`, and so does the
real iOS identifier. On device, Circle 2 (Classic) is indistinguishable from Circle 1 — two
alert boxes with different words.

Canonical strategy §6.5 gives grayscale **the strongest single piece of research support in
the whole document**: a preregistered randomized field experiment (112 participants) found
grayscale produced an immediate, significant, objectively-measured reduction in screen time
— larger and faster than goal-setting. Ash is plausibly the highest-evidence primitive in
the product and it is the only one still not implemented as designed.

**The blocker that justified the cut is gone.** Spike 005
(`.planning/spikes/005-ios-color-filters-identifier/`, verdict VALIDATED, merged
`4d80176`) settled it from decrypted device donors — tier-1 evidence under this project's
own hierarchy:

- **Identifier (iOS 26):**
  `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`
  — an `AX*` intent, **not** the `UA*` macOS twin that BD-01 and BD-01-R both argued
  against. It is absent from all three bundled ToolKit snapshots (v63, v78, v78-ios27), so
  no amount of catalog work could ever have found it. Expect the validator to be blind to
  it; that is a known catalog gap, not a reason to skip.
- **Serialization:** `state` is a **bool-as-integer** — `1` = On, `0` = Off. `operation` is
  a string case id that is **elided when Turn**, so authoring omits it. No `ShowWhenRun`.
- **Both legs are donor-confirmed** — apply (`state = 1`) and restore (`state = 0`). There
  is no remaining gate on the write path.

Two corrections that spike paid for and this build must not re-pay: Apple's own
`.intentdefinition` declares `operation` as an Integer and `off` as case index `2`. Both
are wrong as plist encodings. Shipping `state = 2` for Off would have **left users stuck in
grayscale**. An `.intentdefinition` describes the intent's type system, not the plist
encoding, and does not outrank a donor.

**The one real constraint that remains: there is no read-back.** No `Get*`/`Query*` intent
exists for any accessibility setting across all 35 intents in
`AccessibilityUtilities.framework`. So §21's "do not blindly override a pre-existing
accessibility state" rule cannot be satisfied by detection. PROSOCHĒ must not clobber
someone who runs Color Filters deliberately for colour-blindness, migraine, or low vision.

The opt-in remedy already exists in Config and is currently dead code:
`safety.ash_managed_color_filters` (default `true`, `src/CONFIG-BLOCK.md`). Nothing reads
it. `CONFIG-BLOCK.md`'s BD-01-R note already claims Ash *is* a real Color Filters change —
that claim is currently false in the artifact, which is its own documentation defect to
close.

## Solution

1. **Author the apply leg** in `ash()` using the donor-confirmed shape exactly:
   identifier `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`,
   parameter `state` = integer `1`, `operation` omitted. Do not add `ShowWhenRun`. Do not
   substitute the `UA*` identifier.
2. **Author the restore leg** — `state` = integer `0` — and wire it everywhere the other
   environmental primitives already restore: CLOSE, Emergency Restore, Ice expiry, and the
   live-Ice redirect. Reuse `restore_managed_settings()`'s ownership pattern rather than
   inventing a parallel one. **A grayscale that does not restore is strictly worse than no
   grayscale**; treat the restore leg as the deliverable, not the apply leg.
3. **Branch on `safety.ash_managed_color_filters`.** True → real filter toggle. False →
   BD-01's non-environmental pause (the current alert). This is §21's opt-in remedy and the
   only defensible answer given no read-back. Onboarding must state plainly that PROSOCHĒ
   will turn Color Filters on and off, so a user who needs their own filter setting can
   turn the flag off.
4. **Track state in `settings_snapshot`** alongside brightness and volume, so Emergency
   Restore has one uniform recovery surface and the "was it PROSOCHĒ that changed this?"
   question has one answer.
5. **Expect the validator not to know the identifier.** It is in none of the bundled
   snapshots. Record the deviation explicitly rather than letting a validator complaint
   trigger a substitution back to the `UA*` identifier — that would ship a macOS action to
   an iPhone.
6. **Treat this as new authoring against all seven parameter axes** (`.claude/CLAUDE.md`
   "Generator authoring rules"), then rebuild under the provenance guard, self-check,
   validate, sign, refresh `artifacts/shortcuts/MANIFEST.md`.
7. **Correct the docs that currently overstate reality** — `src/CONFIG-BLOCK.md`'s BD-01-R
   note asserts Ash is already a real Color Filters change. Make that true, or make the
   note honest, but do not leave both.
8. **Close spike 005 step 5** in
   `.planning/phases/999.3-grayscale-ash-capability-donor-test/` — it is the one remaining
   open item there and this todo is its execution.

## Related

- `.planning/spikes/005-ios-color-filters-identifier/README.md` — identifier,
  serialization, and the two refuted `.intentdefinition` values. Read before authoring.
- `.planning/phases/999.3-grayscale-ash-capability-donor-test/` — step 5 ("rebuild Ash")
  is exactly this todo.
- `docs/CAPABILITY-DECISIONS.md` BD-01 / BD-01-R / BD-01-R2, `docs/BUILD-NOTES.md` CAP-20.
- Canonical strategy §6.5 (the grayscale evidence), §11 Primitive B, §21 (accessibility
  safety and the capture-or-skip rule).
- Optional follow-on recorded in the spike's Open Questions: every `Toggle*` intent
  declares a `state` **response** parameter. If it is consumable as a magic variable, Ash
  could detect and preserve a pre-existing filter instead of requiring opt-out — an
  enhancement to §21 compliance, not a gate on this work.

## Device observation, 2026-08-18 — Circle 2 fires but the screen does not grey

First time Ash has run on hardware in this project. On the shipped Core build `873fa3db…`,
sequence `Classic` (Ash = Circle 2), a real OPEN reaching Circle 2 displayed the alert
**"Black and White — One breath away from the screen before you go on."** and the screen
**stayed in full colour** — the tracked app's red chrome was unchanged behind the alert.

So the Circle **dispatches** correctly and its copy renders; what does not happen is any actual
colour change. That is consistent with this todo's whole premise (`CAP-10`: no grayscale toggle
is exposed to Shortcuts on iOS) and with the primitive currently being alert-only.

Recorded in passing during phase 4/6/9 UAT and **not investigated** — no attempt was made to
determine whether a Color Filters action was reached, skipped or absent on that path. Treat it as
a starting observation for this todo, not as a diagnosis. Evidence:
`.planning/debug/device-state/README.md`, finding F-22.
