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

### Locked Decisions (user, 2026-08-18, post-research)

**D-14-01 — Validator gate A: expect exactly the enumerated residue, fail on anything else.**
Once `AXToggleColorFiltersIntent` ships, gate A (`--target-macos 26 --target-platform all`)
emits `Unknown AppIntent identifier` once per AX site (~15/fork) and can never exit 0 again.
Measured this session: the validator has no allowlist, flag, env var, or repo-controllable
data path — its id set is built from `skill_dir/data/toolkit-v*-tool-ids.json` where
`skill_dir` is fixed relative to the validator script inside the plugin cache. Signing is
unaffected (a 21,698-byte signed `.shortcut` was produced from a plist carrying the unknown
identifier).

The disposition is option (a) from `14-RESEARCH.md` Open Question 2:
1. Amend `.claude/CLAUDE.md`'s gate-A clause from "must pass clean, exit 0" to "residue must
   equal exactly the enumerated waiver" — mirroring the treatment gate B already has. This is
   a **constitutional edit and must be its own named task**, not a side effect of another task.
2. Add a repo-local `docs/` checker that runs gate A on both forks, subtracts exactly the
   enumerated `Unknown AppIntent identifier` lines for the AX identifier, and **exits non-zero
   on anything else**. The waiver must be mechanical, not remembered.
3. Record the deviation in `docs/BUILD-NOTES.md`'s deviation log with the reproduction
   command, so a future reader hitting a red gate A finds the reason **before** reaching for
   the `UA*` macOS identifier.

Explicitly rejected: synthesising an `AppIntentDescriptor` (does not make gate A clean, and
fabricates three field values no donor supplies); vendoring a patched ToolKit snapshot (no
override path exists, and the plugin cache is outside the repo and lost on update).

**D-14-02 — Probe the `state` response parameter for read-back within this phase.**
Spike 005 recorded an untested lead: every `Toggle*` intent in
`AccessibilityUtilities.framework` declares a `state` **response** parameter. If it is
consumable as a magic variable, Ash can detect a pre-existing user filter and leave it alone,
instead of relying on default-ON plus an onboarding disclosure the user must read to opt out.
Add a scoped investigation task. If the probe succeeds, prefer preservation. If it fails or is
inconclusive, fall back to the planned `safety.ash_managed_color_filters` opt-out flag plus
disclosure — do **not** let the probe block the phase. Record the result either way; this is
the difference between an accessibility risk that is mitigated and one that is merely
disclosed.

**D-14-03 — Retire backlog phase 999.3 when this phase lands.**
`.planning/phases/999.3-grayscale-ash-capability-donor-test/2026-08-16-grayscale-ash-capability-donor-test.md`
records its own steps 1, 2, 4 and 6 as complete, step 3 as n/a, and step 5 — *"rebuild Ash"* —
as the single open item. Step 5 **is** this phase. Close 999.3 rather than leaving it in the
ROADMAP as separate future work.

### Donor evidence — read directly, three donors not one

All three are decrypted in `.planning/spikes/005-ios-color-filters-identifier/`. Identifier is
`com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` in every case.

| Donor file | `WFWorkflowActionParameters` (beyond `UUID`) | What it establishes |
|---|---|---|
| `SetColourFilters-Shortcut.xml` | `state: <integer>1` | Turn **On** — `operation` absent |
| `Donor9.1-Shortcut.xml` | `state: <integer>0` | Turn **Off** — `operation` absent |
| `Donor9-Shortcut.xml` action 1 | `operation: <string>toggle`, `state: <integer>1` | **Toggle** form; `operation` is a **string**, not an integer |
| `Donor9-Shortcut.xml` action 2 | *(none — bare UUID only)* | The default/unconfigured form |

The `operation` row is why Donor 9 was built: Apple's own `.intentdefinition` declares
`operation` as an Integer, and the device writes the string `"toggle"`. Same class of error as
the `state = 2`-for-Off trap, which would have shipped a restore leg that leaves users stuck in
grayscale. **An `.intentdefinition` describes the intent's type system, not the plist encoding,
and never outranks a donor.**

PROSOCHĒ uses the **Turn** forms (`state: 1` apply, `state: 0` restore, `operation` omitted) —
deterministic set, never toggle. A toggle would desynchronise from `settings_snapshot`
ownership the first time a run was interrupted.

### Claude's Discretion
Everything not locked above. In particular, `14-RESEARCH.md`'s recommendations on Open
Questions 1 (reuse the `original_value` leaf name and pay for it in the docstring), 3 (build a
no-blocking-UI simulator probe — no `Show Alert`, or the run wedges permanently) and 5 (state
the property the build guarantees rather than a per-arm outcome, and keep the emitted comment's
first line stable because `comment_index()` anchors on the prefix) are accepted as written
unless the planner finds evidence against them.

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
