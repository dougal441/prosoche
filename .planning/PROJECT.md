# PROSOCHĒ — Nine Circles

## What This Is

PROSOCHĒ is a free, open-source iPhone Shortcut that restores the missing interval between the impulse to open a habit-forming app and the act of consuming it. It watches user-selected apps through native iOS Personal Automations (App Is Opened / Is Closed), accumulates behavioural **Pressure** from clustered and repeated openings, and escalates the user through nine progressively stronger friction "Circles." It ships as two forks from one engine: **Dumb** (fully deterministic, broad iOS 26 support) and **Sentient** (same deterministic engine plus Apple's **On-Device** Intelligence model as an attention mirror).

It is not a screen-time blocker and not a parental-control system. It is an adaptive friction system for self-directed behaviour change.

## Core Value

**When a user automatically reaches for a target app, PROSOCHĒ interrupts strongly enough that the user makes an actual choice — and the strength of that interruption adapts to their own recent behaviour.**

If everything else fails, the OPEN → Heat/Gravity/Pressure → Circle → intervention loop must work reliably on a real iPhone without corrupting state.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Two signed, importable `.shortcut` files: `PROSOCHĒ — Nine Circles — Dumb` and `PROSOCHĒ — Nine Circles — Sentient`
- [ ] Unsigned XML source retained for both forks (open-source, inspectable, forkable)
- [ ] Single-shortcut invocation routing: manual run vs `OPEN` input vs `CLOSE` input
- [ ] First-run bootstrap creates `state.json` and the `PROSOCHĒ — Control Room` Apple Note; later manual runs never overwrite existing state
- [ ] Control Room Note contains READ THIS FIRST setup instructions for both Personal Automations, the safety warning about essential apps, and the editable `MY PHONE, ON PURPOSE` proforma
- [ ] Deterministic behavioural state engine: behavioural day (date − 4h), Heat (decay/increment/rapid-return/contract-fidelity, floor 0, cap 30), Gravity (`floor(opens_today/6)`, cap 5), Pressure (`heat + gravity`)
- [ ] Three descent profiles with distinct Pressure→Circle thresholds: Paradise / Limbo (default) / Inferno
- [ ] Nine intervention primitives: Knock, Ash, Silence, Confession, Dimming, Exile, Mirror, Voice, Ice
- [ ] Three switchable Circle sequences: Classic (default), Black Mirror, Ambient
- [ ] Intention contracts: free-text purpose + time boundary (2/5/10/15/custom); deliberate leisure is a valid contract
- [ ] Six exits: Capture, Coordinate, Create, Connect, Consult, Close — all invokable, all outcomes recorded
- [ ] Consult provides at least a direct query-shaped search route (web/maps/notes/reminders/calendar menu in Dumb)
- [ ] Local epsilon-greedy explore/exploit exit learning keyed on time-until-next-tracked-OPEN
- [ ] CLOSE handler measures real session duration, is race-proof via session IDs and state reload, computes contract overrun, restores any settings PROSOCHĒ changed
- [ ] Circle IX (Ice): deterministic cooldown (~60s Paradise / ~3m Limbo / ~5m Inferno), never model-decided, blocked attempts don't inflate Heat, always a route out
- [ ] Environmental safety: never zero brightness, never raise volume, never blindly override accessibility settings, skip any stateful change that cannot be restored
- [ ] Control Room manual menu: Status, Open Control Room, Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today, Emergency Restore (+ Toggle On-Device AI, Test Model in Sentient)
- [ ] Emergency Restore clears cooldown, active session, and recoverable brightness/volume/colour state
- [ ] Dumb Mirror engine: ≥30 telemetry templates that never invent facts and are gated on available facts
- [ ] Native import questions (Layer A): descent profile; voice yes/no; (Sentient only) on-device intelligence yes/no
- [ ] `Sync My Profile` extracts the human proforma from the Note into `state.json` — the fast OPEN path never parses the whole Note
- [ ] Sentient uses the On-Device model only, at Circles II–VIII, with structured `ALLOW`/`CHALLENGE`/`DENY` output, parse validation, deterministic fallback, and at most one challenge round
- [ ] Sentient is a contract auditor (specificity / boundedness / consistency), never a lie detector, never claims to know in-app content
- [ ] Rolling-window JSON state (last ~20 sessions, ~10 contracts, per-exit aggregates) — no unbounded arrays, no CSV
- [ ] Corrupt or missing JSON, and a deleted Control Room Note, both trigger safe recovery rather than failure
- [ ] Build notes documenting every unverified iOS action, deviation, and fallback taken
- [ ] Both forks pass the Shortcuts Playground validator, sign, and import

### Out of Scope

- Focus modes — explored and deliberately removed from v1; possible later environmental layer
- NFC / physical commitment tokens — deliberately removed from v1; possible Phase D extension
- Screen Time blocking APIs (FamilyControls / ManagedSettings / DeviceActivity) and any companion iOS app — PROSOCHĒ is a behavioural intervention, not secure access control
- CSV or any second machine store — one JSON for machine state, one Note for human history
- ChatGPT / third-party extension models, arbitrary web APIs, analytics services — a different trust boundary. (Private Cloud Compute was originally excluded too; the owner relaxed this on 2026-08-13 — see BD-04-R. On-Device is preferred, PCC is acceptable.)
- Remote A/B testing infrastructure — sequences are switchable locally for manual comparison only
- `Get App & Website Data` / Screen Time telemetry as a core dependency — research/measurement only, later phase
- "Life Returned" value quantification and pay-after-value support prompts — recorded as concepts, designed rigorously later
- Any claim of tamper-proofing — the user can always disable the Personal Automation, and the product must never claim otherwise

## Context

- **Canonical source:** `PROSOCHE_Nine_Circles_Canonical_Strategy.md` in this repo. Where any earlier idea conflicts with that document, that document wins.
- **Build tool:** Shortcuts Playground (`shortcut-builder` / `shortcut-remixer` agents, `shortcuts-playground` skill). Playground itself warns generated shortcuts get ~90% of the way and that variable wiring and repeat loops must be inspected — plist validation is necessary but not sufficient.
- **Hard iOS constraint:** a distributed Shortcut cannot install Personal Automations on the user's behalf. The user must create the OPEN and CLOSE automations manually; the Control Room Note must instruct them clearly. This is a deliberate product constraint, not a defect.
- **Hard iOS constraint:** the Shortcut reacts to an app-open trigger; it does not intercept it. The target app may briefly become active before Circle IX ejects.
- **Evidence base:** one sec field study (friction + an easy dismissal option had the strongest effect — the choice architecture is the product, not the clever sentence); Lukoff et al. 2018 (deliberate leisure can be meaningful — do not treat all leisure as failure); Keller et al. RCT (planning and self-efficacy are the active mechanisms); Wellspent RCT (self-defined targets and just-in-time nudges); grayscale field experiments (design friction works, though dynamic per-session toggling remains an untested hypothesis).
- **Primary prototype metric:** rapid-return rate. Secondary: contract fidelity (actual/intended duration, medians not means).
- **Dominant failure mode:** the intervention becomes annoying enough that the user disables PROSOCHĒ. That is a product failure even if it blocks more openings.
- **Distribution:** free and open source, forkable, no feature gate, no ads, no data sale, no telemetry leaving the device.

## Constraints

- **Platform**: iOS 26.x, native Shortcuts only — no companion app, no private APIs
- **Tech stack**: Shortcuts plist XML built and signed via Shortcuts Playground; one `state.json`; one Apple Note
- **AI**: Apple Intelligence via the iOS 26 `Use Model` action, Sentient fork only. On-Device preferred; Private Cloud Compute acceptable (relaxed 2026-08-13, BD-04-R). ChatGPT / extension models excluded. Never write a guessed `WFLLMModel` value — omitting the key is safe, guessing it is not.
- **Privacy**: no behavioural data leaves the device; Sentient receives only a compact local context window, never the whole Note
- **Capability**: every iOS action identifier and parameter shape must be verified before use — if it cannot be verified, use the safest fallback, record the deviation, and keep the Shortcut runnable. Never fabricate an action because the strategy asks for it.
- **Safety**: no zero brightness, no unsafe or startling volume, no accessibility-stranding state, Emergency Restore always available
- **Determinism**: the model never controls arithmetic, thresholds, timers, Circle IX, or any safety decision
- **Device split**: Dumb targets all iOS 26 iPhones; Sentient requires Apple Intelligence-capable hardware (iPhone 15 Pro and later)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| One JSON for machine state, one Apple Note for human history; no CSV | A growing rich-text Note is not a transactional store; parsing it on every OPEN is slow and race-prone. One machine store, not two. | — Pending |
| Build Dumb to stability first, then fork Sentient onto the identical deterministic engine | Dumb is the baseline product and the control condition, not a degraded afterthought. Sentient must not alter the state engine. | — Pending |
| Pressure = Heat + Gravity, mapped to nine Circles via a per-profile threshold table | Separates short-term compulsive clustering from slow whole-day accumulation; keeps all coefficients tunable prototype parameters. | — Pending |
| Behavioural day = current date − 4 hours | Avoids the obvious midnight reset loophole. | — Pending |
| Exits chosen by local epsilon-greedy learning on time-until-next-tracked-OPEN, never by the model | Which exit breaks the loop is an empirical per-user question, and an LLM must not do arithmetic. | — Pending |
| Sentient is a contract auditor (specific / bounded / consistent), never a lie detector | It cannot know in-app content or mental state; challengeable behavioural facts are stronger and more honest than accusation. | — Pending |
| Deliberate leisure is an explicitly valid contract | Evidence shows apparently "meaningless" use can be meaningful; punishing all leisure drives disablement. | — Pending |
| Personal Automations are user-created, documented in the Control Room Note | Apple does not permit a shared Shortcut to install them. Honesty about this is part of the product. | — Pending |
| Three switchable Circle sequences, changed locally from the Control Room menu | Sequence order is a genuinely open question; local switching enables manual comparison without remote A/B infrastructure. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-08-13 after initialization*
