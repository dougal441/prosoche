# Phase 14: Ash as real Color Filters grayscale - Context

**Gathered:** 2026-08-18
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss)

<domain>
## Phase Boundary

Build Ash as a **real Color Filters grayscale toggle**. It currently ships as an alert box
— on device, Circle 2 is indistinguishable from Circle 1: two alerts with different words.

**This is plausibly the highest-evidence primitive in the product.** Canonical strategy §6.5
cites a preregistered randomised field experiment (112 participants) finding grayscale
produced an immediate, significant, objectively-measured reduction in screen time — larger
and faster than goal-setting. It is the only primitive still not implemented as designed.

**The blocker that justified the cut is gone.** Spike 005
(`.planning/spikes/005-ios-color-filters-identifier/`, VALIDATED, merged `4d80176`) settled
it from decrypted device donors — tier-1 evidence. Identifier:
`com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` — an `AX*`
intent, **not** the `UA*` macOS twin. `state` is a **bool-as-integer**: `1` = On, `0` = Off.
`operation` is elided when Turn, so omit it. No `ShowWhenRun`. Both legs are donor-confirmed.
Two corrections the spike paid for and this phase must not re-pay: Apple's own
`.intentdefinition` declares `state` as Integer with `off` = case index **2**, and both are
wrong as plist encodings — **shipping `state = 2` for Off would leave users stuck in
grayscale**. An `.intentdefinition` describes the intent's type system, not the plist
encoding, and never outranks a donor.

**Expect the validator not to know the identifier** — it is absent from all three bundled
ToolKit snapshots. Record the deviation rather than letting a validator complaint trigger a
substitution back to `UA*`, which would ship a macOS action to an iPhone.

**The restore leg is the deliverable, not the apply leg.** A grayscale that does not restore
is strictly worse than no grayscale. Wire `state = 0` everywhere the other environmental
primitives restore — CLOSE, Emergency Restore, Ice expiry, the live-Ice redirect — reusing
`restore_managed_settings()`'s ownership pattern, and track it in `settings_snapshot`
alongside brightness and volume so Emergency Restore has one uniform recovery surface.
Routing it through the same path means one device pass can prove all three environmental
primitives.

**There is no read-back** — no `Get*`/`Query*` intent exists for any accessibility setting
across all 35 intents in the framework — so §21's "do not clobber a pre-existing
accessibility state" cannot be satisfied by detection. **User decision 2026-08-17: default
ON, disclosed in onboarding.** Branch on `safety.ash_managed_color_filters` (already in
Config, currently dead code): true → real toggle, false → BD-01's non-environmental pause.
Onboarding must state plainly that PROSOCHĒ turns Color Filters on and off, so a user who
needs their own filter setting for colour-blindness, migraine or low vision can turn the flag
off.

Also correct `src/CONFIG-BLOCK.md`'s BD-01-R note, which currently asserts Ash *is* already a
real Color Filters change — make it true or make it honest, but do not leave both. Closes
spike 005 step 5.

**Severity:** major
**Requirements:** CIRC-02, SAFE-01, SAFE-02, SAFE-05, AUDIT-02
**Depends on:** Phase 11

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — discuss phase was skipped per user setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide decisions.

</decisions>

<code_context>
## Existing Code Insights

Codebase context will be gathered during plan-phase research.

</code_context>

<specifics>
## Specific Ideas

No specific requirements — discuss phase skipped. Refer to ROADMAP phase description and success criteria.

</specifics>

<deferred>
## Deferred Ideas

None — discuss phase skipped.

</deferred>
