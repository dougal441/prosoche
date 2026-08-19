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

> **SCOPE RESET — user, 2026-08-19.** The first planning pass built Ash as a fourth member of the
> capture-and-restore machine, alongside brightness and volume. That was over-built. Grayscale has
> exactly **two** values, so there is no original to remember: "restore" is unconditionally
> "set it off". The snapshot, the ownership marker, the persist-before-apply ordering and the
> read-back probe were all solving a problem brightness has and colour does not. **Six plans and
> sixteen tasks are superseded by the decisions below.**

### D-14-A — Ash is an unconditional toggle. No state, no snapshot, no capture.

`ash()` emits the AX Color Filters action with `state = 1`. Nothing else. It does **not** read
`settings_snapshot`, does **not** write an ownership marker, does **not** call `save_state()`, and
is **not** gated on a captured original. Grayscale is not restored to a remembered value; it is
turned off. There is nothing to capture, so the entire persist-then-apply ordering rule (axis 7,
the phase-16 precedent) **does not apply to this primitive** and must not be imported into it.

Consequence, stated so it is not rediscovered later: `settings_snapshot` stays at **two** groups,
not three. `SNAPSHOT_SEED` is untouched, `seed_settings_snapshot()` needs no third recogniser pass,
`clear_snapshot()` is untouched, and the two→three abstraction question the assumption-delta
detector raised is **moot** — there is no third group.

### D-14-B — The off leg goes inside `restore_managed_settings()`, unconditionally.

One insertion, four call sites for free: the CLOSE pipeline, Emergency Restore, Ice expiry, and the
live-Ice redirect all already call it (measured — `tools/build_state_engine.py`, four call sites).
The line is unconditional `state = 0`: no snapshot read, no numeric gate, no ownership test.

**Emergency Restore is included deliberately and is not scope creep.** The user's instruction was
"turn it off upon close". If CLOSE never fires — force-quit, battery death, a locked-screen close —
the user is left in grayscale with no way back, which is the single worst outcome this phase can
produce. Emergency Restore is the existing panic button and `SAFE-05` already requires it to restore
"colour settings". Because the off leg is unconditional, reaching all four sites costs exactly the
same as reaching one.

The function's name and docstring speak of restoring *captured* values. The colour line is not that
and must be commented in place as unconditional, so a later reader does not "fix" it by adding the
gate its neighbours have.

### D-14-C — No alert, no notification, no menu at this Circle. Silence is the design.

`ash()` today is a comment plus one `alert(...)` — that alert **is** the current Circle 2, and it is
why Circle 2 is indistinguishable from Circle 1 on device. It is **deleted**, not supplemented.

The shipped user experience is exactly: open the tracked app → the Circle fires → the phone goes
black and white. Leave the app → colour returns. No text, no tap, no acknowledgement. The escalation
from Circle 1 to Circle 2 is the escalation from *interrupting with words* to *changing the
environment without them*.

### D-14-D — Assume the user does not already run grayscale. Backlogged, not solved.

No detection is built. Spike 005 established there is no read-back for any accessibility setting,
and the `state`-response-parameter lead is **cut from this phase**. The pre-existing-user case —
where this Circle must fire a blank — is captured as
`.planning/todos/pending/2026-08-19-ash-void-circle-when-user-already-uses-grayscale.md`.

**This supersedes D-14-02 entirely: spike 011 is not built in this phase.**

**One thing is kept rather than deferred:** `safety.ash_managed_color_filters` already exists in
Config as dead code. Make it live as a plain kill switch — true → the toggle, false → the Circle
fires a blank (a bare Nothing, no alert). It costs a handful of lines, it is the mechanism the
backlog item will need anyway, and without it a colour-blind user has **no recourse at all** until
that item ships. Onboarding must still state plainly that PROSOCHĒ turns Color Filters on and off.

### D-14-01 — Validator gate A: expect exactly the enumerated residue, fail on anything else. **UNCHANGED.**

Still applies in full — the identifier is unknown to the validator regardless of how simply it is
wired, so gate A can never exit 0 again once it ships. Measured: no allowlist, flag, env var, or
repo-controllable data path; signing is unaffected (a 21,698-byte signed `.shortcut` was produced
from a plist carrying it). Disposition, per user decision 2026-08-18:

1. Amend `.claude/CLAUDE.md`'s gate-A clause from "must pass clean, exit 0" to "residue must equal
   exactly the enumerated waiver", mirroring gate B's existing treatment. **Its own named task.**
2. Add a repo-local `docs/` checker that runs gate A on both forks, subtracts exactly the enumerated
   lines for the AX identifier, and exits non-zero on anything else.
3. Record the deviation in `docs/BUILD-NOTES.md` with the reproduction command, so a future reader
   hitting a red gate A finds the reason **before** reaching for the `UA*` macOS identifier.

The waiver enumerates **both** line families — `Unknown AppIntent identifier` and the
missing-`AppIntentDescriptor` line — because a descriptor-less action emits both per instance and
item 1 of this decision forbids synthesising a descriptor. A one-family waiver would be permanently
unsatisfiable. Rejected: synthesising a descriptor; vendoring a patched ToolKit snapshot.

**Site count changes with the simplification.** The apply leg renders once per `primitive_dispatch()`
rendering; the off leg renders once per `restore_managed_settings()` call site. Derive the real
number from the built artifact with `plistlib` — do **not** carry forward the superseded 15/fork
figure, which assumed the snapshot design.

### D-14-03 — Retire backlog phase 999.3 when this phase lands. **UNCHANGED.**

Its steps 1/2/4/6 are complete, 3 is n/a, and step 5 — "rebuild Ash" — is this phase.

### Donor evidence — read directly, three donors not one

All decrypted in `.planning/spikes/005-ios-color-filters-identifier/`. Identifier is
`com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` in every case.

| Donor file | Parameters beyond `UUID` | Establishes |
|---|---|---|
| `SetColourFilters-Shortcut.xml` | `state: <integer>1` | Turn **On** — `operation` absent |
| `Donor9.1-Shortcut.xml` | `state: <integer>0` | Turn **Off** — `operation` absent |
| `Donor9-Shortcut.xml` action 1 | `operation: <string>toggle`, `state: <integer>1` | **Toggle** form; `operation` is a **string** |
| `Donor9-Shortcut.xml` action 2 | *(none — bare UUID only)* | The default/unconfigured form |

Apple's `.intentdefinition` declares `operation` as Integer and `off` as case index **2**. Both are
wrong as plist encodings, and **`state = 2` for Off would leave users stuck in grayscale**. An
`.intentdefinition` describes the intent's type system, not the plist encoding, and never outranks a
donor.

PROSOCHĒ uses the **Turn** forms — `state: 1` on, `state: 0` off, `operation` omitted. Never Toggle:
a toggle desynchronises the moment a run is interrupted.

### Claude's Discretion

Everything not fixed above. `14-RESEARCH.md`'s recommendation 5 still stands — state the property
the build guarantees rather than a per-arm outcome, and keep the emitted comment's **first line
stable**, because `comment_index()` anchors on the prefix.

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
