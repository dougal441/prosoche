# PROSOCHĒ — Capability Decisions

Decisions in this document are numbered `BD-NN` ("blocker decision"). They are **binding on later phases** — once recorded, a later plan does not silently re-litigate a BD entry; it either builds against it or raises a new, explicitly-flagged architectural question through the normal deviation process. `BD-01`..`BD-05` correspond to the five blockers named in `.planning/phases/01-capability-audit-config-foundation/01-CONTEXT.md`.

## Table of contents

| Decision | Title | Owning plan |
|---|---|---|
| BD-01 | Ash / Color Filters | 01-01 (this plan) |
| BD-02 | Dimming / brightness read-back | 01-04 |
| BD-03 | Silence / volume read-back | 01-04 |
| BD-04 | Use Model On-Device literal | 01-05 |
| BD-05 | Notes actions on the iOS target | 01-04 |

---

## BD-01 — Ash / Color Filters

**Question:** The Ash primitive (canonical strategy §11 Primitive B: "Grayscale where iOS can apply and restore it safely. Passive reduction of visual salience.") requires a system-level grayscale/Color Filters toggle. The capability audit (CAP-20 in `docs/BUILD-NOTES.md`) found no such action verified available to Shortcuts.app on iPhone. D-08 requires deciding Ash's fate among three named options. What should Ash do on the iOS build?

**Evidence:** CAP-20 in `docs/BUILD-NOTES.md` §4, and its supporting `DEV-01` entry in §5. Summary: `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` is the only Color-Filters-adjacent action found anywhere in the bundled ToolKit snapshots; it is present in the generic `toolkit-v63-tool-ids.json`/`toolkit-v78-tool-ids.json` snapshots but every parameter and its top-level platform tag in `toolkit-v78-first-party-parameter-keys.json` reads `platforms: ["macOS 27"]` only, and it is entirely absent from the iOS-27-Simulator-specific `toolkit-v78-ios27-tool-ids.json` snapshot. No grayscale read-back mechanism exists in any bundled snapshot. This is corroborated independently by `.planning/research/STACK.md` §3 row 10 and `.planning/research/PITFALLS.md` C3/C4.

**Options considered** (verbatim from D-08):

1. **Substitute a different visual-salience reduction.** Replace the system grayscale toggle with a different, verifiably-available mechanism that still reduces visual salience — e.g. Set Brightness (CAP-08, `is.workflow.actions.setbrightness`, confirmed present on both iOS 27 Simulator and macOS 27) dimmed toward the prototype's Dimming value, or a Shortcuts-native full-screen overlay if a verified action for one exists. *Not chosen as the primary path*, because Dimming is already a separate, distinct primitive (Primitive E) in the same sequence — collapsing Ash into a second Dimming call would remove a primitive from the tested sequence rather than substitute one, contradicting D-13's instruction to keep the sequence table intact, and canonical strategy §12 already places Ash and Dimming as separately testable slots specifically to compare passive-friction primitives independently.
2. **Require user opt-in to a PROSOCHĒ-managed configuration.** Ask the user, at import time or via a one-time Control Room setup step, to manually enable Color Filters/grayscale in iOS Settings → Accessibility once, and have PROSOCHĒ never touch the toggle programmatically — Ash then becomes "confirm the user is in their own pre-configured grayscale mode" rather than "toggle grayscale." *Not chosen*, because there is no verified read-back action for Color Filters state either (same CAP-20 evidence), so PROSOCHĒ cannot even confirm the opt-in configuration is currently active — the primitive would degrade to firing blind, which is materially worse than an honestly-skipped intervention, and it introduces a manual per-user Settings dependency this phase's D-01 constraint (native Shortcuts only, no companion app) is meant to avoid multiplying.
3. **Degrade Ash to a non-environmental variant.** Keep Ash as a distinct sequence entry but redefine what it *does*: instead of a system-level display change, it becomes a verified, self-contained Shortcuts behaviour that produces the same passive-friction *effect* (a still, low-salience moment) without touching any system accessibility setting — e.g. a brief full-screen text/Show Result pause with intentionally desaturated, low-contrast static copy (no colour, no imagery, no urgency), using only verified actions (`is.workflow.actions.showresult`/`is.workflow.actions.alert`-class primitives already required elsewhere in the build). *Chosen* — see Decision below.

**Decision:** Option 3 — degrade Ash to a non-environmental variant. Ash keeps its position in all three sequence orderings and keeps producing a passive, low-salience moment, but it is implemented as a verified, self-contained in-Shortcut visual pause (deliberately colourless/low-contrast static content shown via a verified display action) rather than a system Color Filters toggle. The exact display action and copy are a Phase 2/5 authoring decision, not decided here; what is binding here is that Ash is *not* implemented as `UAToggleColorFiltersIntent` or any invented grayscale-toggle identifier, and it never reads or writes the device's actual accessibility state.

**Rationale:** Canonical strategy §21's absolute rule for Grayscale/Color Filters states: "Accessibility settings may already be intentionally configured by the user. Do not blindly disable a pre-existing state. If Shortcuts cannot detect and restore the original condition safely, either: skip dynamic grayscale; or require the user to opt into a known PROSOCHĒ-managed configuration." CAP-20's evidence establishes Shortcuts cannot detect *or* restore the original Color Filters state on iOS at all (no read-back action found), which rules out any design that touches the real accessibility toggle — both the literal "toggle it live" reading of Primitive B and Option 2's opt-in-and-trust variant fail this test, because Option 2 still requires trusting an unconfirmable state. PITFALLS.md C4 independently names the same hazard: "a pre-existing accessibility configuration must never be blindly overridden," and notes there is no verified way to even detect whether a user already has grayscale on for a genuine vision-related need. Option 3 satisfies §21's "skip dynamic grayscale" branch precisely — it does not touch the system accessibility surface at all, so there is nothing to clobber and nothing that needs restoring — while still preserving Ash as a distinct, testable sequence entry rather than silently collapsing it into Dimming (which the sequence table treats as separately significant, per D-13's requirement to keep the sequences intact).

**Consequence for later phases:** Phase 5 (Circle primitive implementation) is explicitly gated on this decision. Phase 5 must build the primitive referenced here as **CIRC-02** to do exactly this: render a self-contained, low-salience visual pause using only actions verified elsewhere in this audit (e.g. `is.workflow.actions.showresult` / `is.workflow.actions.alert`-class display, deliberately colourless/low-contrast static copy, no imagery, no urgency framing) — CIRC-02 must **never** call `UAToggleColorFiltersIntent` or any other UniversalAccess accessibility-toggle identifier, and must never attempt to read the device's live accessibility configuration. If a future ToolKit snapshot or on-device test reveals a genuinely iOS-available, read-and-restore-capable grayscale action, that would be a new capability finding requiring a new deviation entry and a possible BD-01 revision — it is not assumed here.

**Requirement:** AUDIT-02

---

## BD-02 — Dimming / brightness read-back

_Owner: plan 01-04._

## BD-03 — Silence / volume read-back

_Owner: plan 01-04._

## BD-04 — Use Model On-Device literal

_Owner: plan 01-05._

## BD-05 — Notes actions on the iOS target

_Owner: plan 01-04._
