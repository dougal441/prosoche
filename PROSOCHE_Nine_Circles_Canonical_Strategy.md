# PROSOCHĒ — Nine Circles
## Canonical Product Strategy v2 — The Covenant Model

**Status:** Canonical strategy, version 2.0 — supersedes v1.0 **in full**
**Date:** 19 August 2026 (v1.0: 13 August 2026)
**Provenance:** v1.0 is preserved verbatim at git tag `pre-covenant-overhaul` (commit `10305e6`). Appendix A maps v1 section numbers to their v2 home, so historical citations of "canonical strategy §N" remain resolvable.
**Target:** iOS 26.x
**Build tool:** Shortcuts Playground
**Distribution intent:** Free and open source
**Product forks:** PROSOCHĒ Core (deterministic) + PROSOCHĒ Aware (adds Apple On-Device Intelligence)

**Authority.** This document is the live product spec. Where any earlier document, plan, or conversation conflicts with it, this document wins. Dated capability and design decisions live in `docs/CAPABILITY-DECISIONS.md`; a decision recorded there after this document's date wins until folded in here. The v1 interaction model — one primitive fired on every OPEN at Circle ≥ 1, a universal `Leaving / Continue` pre-menu, Intention as a rung with no routing consequence — is retired. The shipped artifacts still implement it until the conversion phases in `.planning/ROADMAP.md` (Phases 17–20) land; that gap is a recorded build state, not a contradiction.

---

# 0. Executive design brief

PROSOCHĒ is a free, open-source iPhone Shortcut that restores the missing interval between the impulse to open a habit-forming app and the act of consuming it.

The central hypothesis is unchanged from v1:

> The problem is not that people use phones. The problem is that intention disappears between the impulse to open an app and the act of consuming it.

Modern social apps compress **cue → action → consumption**. PROSOCHĒ restores the missing middle: **cue → awareness → intention → deliberate action**.

What v2 changes is *how the product decides when to act*. Version 1 had one axis: behavioural Pressure mapped to a Circle, and the Circle's primitive fired on every open. That model punished conscious use and unconscious use alike — a person deliberately enjoying ten minutes of videos got the same grey screen as a person thrashing through their sixth automatic reopen. Version 2 has **two axes**:

1. **The ladder** — Pressure (Heat + Gravity) mapped to nine Circles. This is the system's *behavioural evidence of automaticity*, computed deterministically from opens, reopens, and contract outcomes. It is unchanged from v1 and is already built.
2. **The covenant** — a declared intention with a time boundary (an **intention contract**). This is the user's *declared evidence of consciousness*. In v2 it is not a rung on the ladder; it is a **gate above it**: an open covered by a valid contract fires **nothing**. Not a gentler primitive — nothing. State still accumulates silently.

The product's stance follows from the two axes:

**Silence is the reward.** When use is intentional, PROSOCHĒ is invisible. When behavioural evidence says intention has disappeared, it escalates — first ambient friction that demands nothing, then a direct ask, then rescue. An honest declaration at the ask buys back the silence. The mechanism is benevolent: it hums in the background, capturing what it needs, and speaks only when it must — and every escalation is an escalation in *salience*, never in *frequency*.

The architecture is unchanged: **one signed `.shortcut`** per fork containing the logic, **one Apple Note (`PROSOCHĒ`)** as the human setup guide, manifesto, and readable ledger, **one small JSON state file** as the machine store. No CSV, no companion app, no cloud, no telemetry leaving the device.

The self-saucing flow is unchanged: import, answer a few native questions, tap once, PROSOCHĒ creates its Note and state, the Note teaches the user to create the two Personal Automations Apple will not let a shared Shortcut install, and from then on PROSOCHĒ runs itself.

---

# 1. The problem

There is a large category of commercial products — blockers, timers, focus apps, physical tokens — that monetize a problem created partly by the attention economy itself. The user should not need another subscription to regain control of their own device.

Apple's Screen Time measures and sets simple limits, but its friction is easy to dismiss and does not adapt to behaviour. My friends dismiss its prompt without reading it — the dismissal itself has become the habit. Commercial blockers add stronger enforcement, but the core behavioural mechanisms can be explored with native Shortcuts.

The opportunity is: **how far can native iOS go when friction is adaptive, personal, contextual, and — crucially — absent whenever it is not needed?**

A phone is a map, a camera, a notebook, a communications device, an instrument, a library. The design must not confuse "less phone" with "better life." The distinction that matters is **deliberate use versus automatic use**. A ten-minute deliberately chosen session of ridiculous videos is fully compatible with PROSOCHĒ. Opening the same app six times in fifteen minutes without knowing why is what PROSOCHĒ exists to interrupt.

---

# 2. Philosophy

## 2.1 Prosochē — Epictetus and the practice of attention

The product is named for the Stoic discipline of **prosochē** (προσοχή): sustained attention to one's own assent, treated not as a mood but as a *practice*.

Epictetus opens the *Enchiridion* by dividing what is up to us from what is not. The phone constantly presents impressions the user does not control — what appears, what others post, what the algorithm rewards. What is up to the user is the moment **before assent**: whether an impression becomes an action. The concise model PROSOCHĒ operationalizes is:

**impression → attention → assent → action → habit**

Persuasive interfaces compress this into **impression → action**. PROSOCHĒ's whole purpose is to reinsert the attention-and-assent interval — and the intention contract is *the act of assent made explicit*. When the user has assented deliberately, the mechanism withdraws; that is the covenant.

In *Discourses* 4.12, "On Attention," Epictetus makes two observations that map directly onto v2's design:

1. **Attention practiced becomes habitual, and so does inattention.** "When you have relaxed your attention for a while, do not fancy you will recover it whenever you please" — the deferral of attention ("I will attend tomorrow") is itself a habit under formation. This is precisely the **ritualisation failure mode** (§13): a user who dismisses an attention prompt mechanically is practicing inattention *through the intervention itself*. The anti-ritualisation variability in §13 exists because Epictetus was right about deferral.
2. **The goal of the practice is that it becomes second nature and the scaffold withdraws.** PROSOCHĒ's definition of success (§21) is that it gradually has less work to do. The mechanism fading into silence is the practice being internalized.

Do not falsely attribute modern slogans as ancient quotations. The honest framing: PROSOCHĒ is a modern application of Epictetus' dichotomy of control and discipline of attention to interface design. Product language that carries this accurately:

> Your phone should wait for an intention.

> You cannot control everything that asks for your attention. You can practice deciding what receives it.

> Attention becomes a life by being spent.

## 2.2 Thaler and choice architecture — nudge, ask, shove

Richard Thaler's nudge theory is the second load-bearing philosophy, and in v2 it structures the bands themselves:

- **Band B is a nudge.** Salience changes (grayscale, silence, reduced brightness) alter the choice environment without removing choice and without demanding anything. Thaler's core claim — small changes to choice architecture meaningfully alter behaviour while preserving freedom — is Band B's entire design.
- **The intention contract is a commitment device.** Thaler's work on self-control (the planner–doer model; Save More Tomorrow) shows people willingly bind their future selves when asked at the right moment. The contract is exactly that: a self-authored commitment ("ten minutes of reels"), made binding not by enforcement but by the system remembering it and reflecting the outcome back.
- **The bands are a libertarian-paternalism gradient the user opted into.** Band B nudges, Band C asks, Band D shoves — and the shove exists only because the user installed a tool whose stated job is to shove them when their own declared standard has been abandoned. Escalation is proportionate to evidence, which is what keeps the paternalism honest.
- **Defaults do the work.** The default is silence (Band A / coverage). Friction is the exception that behaviour must earn, never the ambient condition.

## 2.3 The other design influences, carried forward

- **Cal Newport / digital minimalism:** ask not just "what do you want to use less?" but "what is your phone for, and what do you want the reclaimed attention for?" — this is the `MY PHONE, ON PURPOSE` proforma (§15).
- **Atomic Habits / environment design:** make the unwanted automatic behaviour harder and the desired alternative easier. The six exits (§14) place a better action one tap away; the redirect is never mere punishment.
- **Steve Jobs / the computer as tool:** the aspirational frame is the smartphone as an instrument that extends capacity, not an environment that captures attention.
- **Black Mirror as aesthetic:** the uncanny quality must come from **accurate memory**, never surveillance theatre or fake mind-reading. "This is your fourth return in seventeen minutes" is stronger than "Stop wasting time." The Mirror only ever states recorded facts.

## 2.4 The covenant, stated once

The covenant is the product's moral core and its routing rule in one sentence:

**If you tell PROSOCHĒ what you are doing and stay inside your own boundary, it does nothing at all; the more your behaviour departs from any declared intention, the more visible it becomes.**

Punishment is never the point. Every intervention is an attempt to restore the interval where a choice can happen — and the strongest interventions exist for the moments when the user's own declared standard, not the system's, has been abandoned.

---

# 3. Evidence

The research does not prove the Nine Circles design. It supports its mechanisms — and v2 aligns the product *more* tightly to this evidence than v1 did. Each source, with the v2 mechanism it grounds:

## 3.1 Lukoff et al. 2018 — meaningful vs meaningless use → deliberate leisure is valid

86,402 logged sessions. Habitual use to pass time correlated with lower perceived meaningfulness and a felt loss of autonomy; yet apparently "meaningless" use could serve a real function (micro-escape). The correct distinction is purposeful/unpurposeful, autonomous/automatic, bounded/unbounded — not productive/unproductive. **v2 mechanism:** a bounded deliberate-leisure contract ("ten minutes of stupid videos") is approved and earns full silence. The product never treats leisure as failure.

## 3.2 The regret preprint (2026) — the intention–actual gap → the contract is the metric

In-the-wild data suggesting the **gap between intended and actual use** predicts regret more strongly than duration. Exploratory, not established — but it names v2's central measurement: **contract fidelity** (intended vs observed), which the covenant model makes the co-primary metric (§21). The contract is the intention–actual gap made operational.

## 3.3 Keller et al. RCT — planning and self-efficacy → the ask is a planning act

The goal-directed intervention was not superior to active control on main outcomes, but the mechanism findings were: self-efficacy mediated improvement, and each unit of planning associated with roughly six fewer unlocks/day. **v2 mechanism:** the Band C ask is a planning act, not a lecture — state a purpose, set a boundary. Repeated successful planning is the active ingredient, which is why the ask must never degrade into a ritual (§13).

## 3.4 one sec field study — choice architecture beats the clever sentence

280 participants, six weeks: friction plus an easy option to abandon the opening dismissed ~36% of attempts; openings fell ~57% first-to-sixth week. The decomposition experiment (n=500) found **the dismissal option was the strongest single mechanism** — stronger than the deliberation message. **v2 mechanism:** every interactive surface carries a one-tap leave route (§12), and Band D's forceful moves *are* the dismissal, performed for the user. The design never over-invests in message text at the expense of the choice architecture.

## 3.5 Grayscale field experiments — ambient friction works

A preregistered field experiment (n=112) found grayscale produced an immediate, significant, objectively measured reduction in screen time, larger and faster than goal-setting; two further studies concur. **v2 mechanism:** Band B. Note honestly: the evidence is for sustained grayscale; per-session toggling remains a product hypothesis under test.

## 3.6 Wellspent RCT — self-defined boundaries, just-in-time

Personalized full-screen reminders at a **self-defined limit** reduced time on the most problematic app (~29 min/day) without reducing the study's problematic-use score. **v2 mechanism:** boundaries are always the user's own (the contract boundary, the severity elicitation in §11), and interventions are just-in-time, never scheduled.

## 3.7 Almoallim & Sas 2022 — beyond screen time

Digital-wellbeing tools should support meaningful use rather than only suppress use, employ navigation/friction, and design ethically. Aligned throughout.

## 3.8 MindShift — LLM interventions are promising, exploratory

Context-aware LLM persuasion showed higher acceptance in a small field trial. **v2 mechanism:** Aware's model role stays modest and bounded (§20): an attention mirror and contract auditor inside a deterministic envelope, positioned as experimental.

## 3.9 Habituation — why variability exists

The general habituation literature (response decrement under repeated identical stimulation; recovery under stimulus variation) plus the observed real-world failure of Screen Time prompts — dismissed by reflex, contents unread — ground §13: an intervention surface repeated identically trains its own dismissal. This is stated as design rationale, not as a clinical claim.

---

# 4. Product boundaries

## In scope

- One master Shortcut per fork; user-created OPEN/CLOSE Personal Automations over user-selected apps.
- The two-axis covenant model: nine Circles + Circle 0, four bands, intention contracts with coverage.
- Heat, Gravity, Pressure; Paradise / Purgatory / Inferno profiles; severity-based onboarding.
- The `PROSOCHĒ` Apple Note; one JSON state file; readable ledger.
- ALLOW / CHALLENGE / DENY verdicts in **both** forks (deterministic in Core; model-shaped within a deterministic envelope in Aware).
- Six exits with local explore/exploit learning; safe reversible environmental friction; Emergency Restore.
- Deterministic anti-ritualisation variability (counter-based; ships off until researched — §13).
- Free, open-source distribution; future-value telemetry stored locally.

## Explicitly out of scope

- **Focus modes** — explored, removed from v1, unchanged in v2.
- **NFC / physical commitment tokens** — future extension (SEED-001 holds the Circle IX physical-unlock concept).
- **Screen Time blocking APIs / any companion app** — PROSOCHĒ is a behavioural intervention, not secure access control.
- **CSV or any second machine store** — one JSON, one Note.
- **Cloud AI as a requirement** — Aware uses the On-Device model; Private Cloud Compute is an authorised fallback only (BD-04-R); ChatGPT/extension models are excluded; no external analytics ever.
- **Remote A/B infrastructure** — sequences and knobs are switchable locally.
- **Tamper-proofing claims** — the user can always disable the automation; the product must say so plainly.
- **Mid-session timers.** Shortcuts has no timer trigger a distributed Shortcut can install. Boundary enforcement happens at the *next event*: CLOSE records the overrun; the next OPEN re-engages. No design may assume an intervention can fire while a session is in progress, and none may fabricate a timer mechanism.
- **True randomness in strong interventions.** Variability (§13) is deterministic (counter-based). Nothing nondeterministic ever touches Frozen, cooldown durations, safety paths, or environmental changes; downward "punishment lottery" Circle jumps are explicitly rejected (§13).
- **Lie detection, addiction diagnosis, therapy intake** — unchanged from v1.

---

# 5. The two axes

## 5.1 Axis one — the ladder (behavioural evidence)

Unchanged from v1 and already built:

- **Heat** — short-term compulsive clustering: base per open, bonuses for rapid reopening, penalty for contract overrun, relief for a kept contract, decay with time away, floor 0, cap 30.
- **Gravity** — slow accumulation: `floor(opens_today / 6)`, cap 5, over the behavioural day (date − 4h).
- **Pressure = Heat + Gravity**, mapped to Circle 0–9 through the active profile's ascending threshold table (ordered ≥ scan, never equality).

The ladder answers one question: *how much does recent behaviour look like automaticity?* It is fully deterministic and the model never touches it.

## 5.2 Axis two — the covenant (declared intention)

An **intention contract** is free text plus a time boundary, exactly as v1 defined it — "watch stupid videos, 10 minutes" is valid. What v2 adds is consequence:

- A valid contract **covers** opens inside its window: covered opens fire nothing (§7).
- Contract outcomes feed the verdict history (§8) as well as Heat.
- Contracts can be **invalidated** by behaviour before their window ends (§7.3), which is what re-engages the system.

The covenant answers the other question: *has the user told the truth about what they are doing, and are they inside their own boundary?*

## 5.3 The routing rule

On every genuine OPEN, after the state engine runs and persists:

1. **Circle 0** → silent. (Band A.)
2. **Valid contract covering this open, and Circle ≤ coverage ceiling** → silent. (Coverage.)
3. **Otherwise** → the current Circle's primitive fires, per the active sequence. (Bands B–D.)

That is the whole model. Everything else in this document is the content of those three lines.

---

# 6. The four bands

Circles group into four bands with fixed boundaries. Dante's names stay **positional** (BD-06 Decisions 1–2): the name labels the depth, the sequence table decides the intervention.

| Band | Circles | Dante names | Character | Thaler reading | Uncovered open shows |
|---|---|---|---|---|---|
| **A — Silent** | 0 | The Indifferent | Trust by default. State accumulates; nothing is shown, ever. | The default | Nothing |
| **B — Ambient** | 1–3 | Limbo, Lust, Gluttony | Passive friction. The phone becomes slightly less rewarding. **No dialogs** except Circle 1's single-tap pause. Nothing is demanded. | Nudge | Pause (1) · Black and White (2) · Silence (3) |
| **C — Ask** | 4–6 | Greed, Wrath, Heresy | Declared-intent engagement. The ask *is* the intervention; the verdict routes it. An honest answer ends the encounter and buys silence. | Ask / commitment device | Intention (4) · Mirror (5) · Redirect (6) |
| **D — Rescue** | 7–9 | Violence, Fraud, Treachery | Behaviour has overridden declaration. No questions. Forceful rescue with guaranteed routes out. | Shove (opted into) | Eject (7) · Loud Mirror (8) · Frozen (9) |

Band rules:

- **Band boundaries are fixed at 0 / 1–3 / 4–6 / 7–9 across all sequences and profiles.** Sequences vary the order *within* a band only (§9.2). Config reserves per-profile band-entry keys (`bands.ask_entry`, `bands.rescue_entry`, both defaulting to 4 and 7) as tuning capability for device evidence — a reserved knob, not a v2 behaviour.
- **Band A is inviolable.** No surface, no notification, no model call, no variability event is ever reachable from a Circle 0 open. (Built — Phase 10's silent band; guarded by `verify_circle_zero_silence()`.)
- **Band B is silent friction.** Black and White, Silence, and (in the Ambient sequence) Dim apply with no announcement and no menu — the environmental change *is* the touchpoint. Circle 1's Pause is the single exception: one alert, one tap, no question. There is deliberately no "declare your intention" affordance inside Band B surfaces; a user who wants standing coverage can declare voluntarily from the manual menu (§7.1), and pressure that stays in Band B rarely warrants the ask.
- **Band C engages.** Circle 4 asks directly (Intention). Circle 5 reflects — the Mirror shows the recorded gap ("You said reply to Maya, 5 minutes. This is your fourth open in nine minutes.") and offers three routes: continue, leave, or declare. Circle 6 stops asking: Redirect lands the user in a deterministically selected exit, no menu (BD-06 Decision 6, reaffirmed).
- **Band D rescues.** Eject (7) sends the user straight to the Home Screen. Loud Mirror (8) speaks the reflection once — Fraud is the right name for the depth at which the system says aloud what the gap between word and deed has been. Frozen (9) is the deterministic cooldown, untouched from v1.
- **Descending never replays the shallower bands' prompts.** One primitive per open, always (built: exact-match dispatch, BD-06 Decision 5).

---

# 7. The covenant lifecycle

## 7.1 Creation

A contract is created at:

- **The Band C ask** (Circle 4's Intention primitive, or Circle 5's "declare" route): free-text purpose + boundary (2/5/10/15/custom minutes). Blank or vague text is accepted without sincerity judgment (Core never polices wording); the **boundary is mandatory** — it is what makes coverage computable, expiry detectable, and fidelity measurable. Without an end there is no window, and the system could neither go silent nor come back. If the user declines the boundary picker, a config default (`contract.default_boundary_minutes`) is applied and said aloud in the confirmation line.
- **Voluntarily**, from the manual menu ("Set an intention") — a user who knows they want twenty minutes tonight can declare before any descent, and the coverage rules are identical.

To reduce the cost of honesty, the ask prefills from history where facts exist: the previous intention is offered as a one-tap option ("Same as last time: reply to Maya · 5 min").

## 7.2 Coverage

A contract covers a **time window**, not a single session: from `made_at` to `made_at + boundary`. Closing at minute 3 and reopening at minute 6 of a 10-minute contract is covered — that is a person using their granted time, and check-close-recheck within a declared window is not the behaviour this product interrupts.

A covered open: runs the full state engine, records everything, applies **no primitive, no surface, no model call**. Coverage is checked deterministically (epoch comparisons and flat reads) after the state save and before any dispatch.

**The coverage ceiling.** A contract cannot cover an open at Circle ≥ `contract.coverage_ceiling_circle` (ships at 7, the Band D boundary). By construction a user only reaches Band D through behaviour that has already invalidated coverage; the ceiling is the deterministic backstop that guarantees a declaration can never outrun the record, and it keeps Frozen absolutely independent of anything declared.

## 7.3 Invalidation

Coverage ends early — and the *next* open re-engages at whatever Circle Pressure says — when any of these deterministic conditions is met:

1. **Expiry:** the window has ended.
2. **Open-count breach:** opens within the window exceed `contract.max_opens_per_window` (ships at 3).
3. **Rapid-return breach:** the rapid-reopen Heat bonus fires more than `contract.max_rapid_returns_per_window` times within the window (ships at 1 — the second rapid return invalidates).

Invalidation is silent at the moment it happens (PROSOCHĒ cannot act mid-session and does not pretend to); its consequence is that the next open is uncovered. When that open lands in Band C, the Mirror or the ask does exactly what re-engagement should: reflect the recorded gap, then invite a new declaration.

## 7.4 Fidelity

Contract fidelity is measured per window: `consumed_seconds` (the sum of tracked session time inside the window, accumulated at each CLOSE) against the declared boundary.

- **Kept** (window ends with consumed ≤ boundary, no invalidation): recorded as respected; Heat relief applies (`heat.contract_respected_relief`). Silence continues to be the reward — no congratulation surface is shown; success may be acknowledged later through the Mirror's positive templates (§19), never through a new touchpoint.
- **Overrun:** recorded with magnitude; the existing Heat penalty applies (`heat.overrun_penalty` under the ratio + absolute-seconds AND-rule).
- Outcomes append to `recent_contracts` (rolling window, last ~10) — which the verdict history (§8) and the Aware auditor both read. This makes `recent_contracts` load-bearing for the first time; v1 defined it and never wrote it.

## 7.5 Covered reopens and Heat

A reopen inside a covered window adds `heat.open_base` and counts toward Gravity, but earns **no rapid-return bonus** (`heat.covered_reopen_bonus` ships as `none`; PROTOTYPE INTERPRETATION, tunable). Reopening within one's own declared window is granted time, not compulsive clustering — but the open still exists, so a day of wall-to-wall covered windows still accumulates Gravity and still descends. Coverage silences surfaces; it never silences the ledger.

## 7.6 Why gaming fails

"Declare the maximum every time" does not defeat the system: every open still counts toward Gravity; overruns still burn Heat; invalidation still ends coverage mid-window; and a **verdict history** of blown contracts pulls CHALLENGE earlier (§8). Honest declarers live shallow with a clean phone. Dishonest declarers descend anyway — just with their own words on the record, which is what the Mirror is for.

---

# 8. Verdicts — ALLOW / CHALLENGE / DENY in both forks

The ask returns a verdict. In v1 this existed only in the Aware fork and changed almost nothing; in v2 it exists in both forks and routes the encounter.

## 8.1 The deterministic envelope

The set of verdicts *available* at each Circle is deterministic and identical in both forks:

| Circle | Available verdicts |
|---|---|
| 4 (Greed) | ALLOW, CHALLENGE |
| 5 (Wrath) | ALLOW, CHALLENGE |
| 6 (Heresy) | ALLOW, CHALLENGE, DENY |

- **ALLOW** → the contract is created, coverage begins, the run ends. Clean phone.
- **CHALLENGE** → exactly one revision round (never an interrogation loop): tighten the wording or accept a shorter boundary, then ALLOW. A challenge that the user answers still ends in coverage.
- **DENY** → Redirect: the user lands in the deterministically selected exit. DENY exists only at Circle 6 and means redirect, never punishment — no settings change, no Heat surcharge, no cooldown.

## 8.2 Core's verdict — behavioural, never textual

Core cannot and does not judge wording (no sincerity policing — carried from v1's intent-gate rule). Its verdict is computed from recorded behaviour only:

- Default **ALLOW**.
- **CHALLENGE** when the recent record argues for it: `recent_contracts` shows ≥ `verdict.challenge_overrun_count` substantial overruns in the rolling window, or the previous contract was invalidated by breach rather than kept.
- **DENY** at Circle 6 when the same conditions hold there.

All thresholds are Config values. The whole function is arithmetic over recorded facts.

## 8.3 Aware's verdict — judgment inside the same envelope

Aware submits the stated intention plus the compact context window (§20) to the On-Device model, which audits **specificity, boundedness, consistency** — never sincerity, never mental states, never app contents — and returns a structured verdict. The rules that keep it safe are unchanged from v1 and now have sharper teeth:

- The model chooses **only within the deterministic envelope** for the current Circle; a verdict outside it is discarded.
- Malformed, empty, or slow output falls back to Core's deterministic verdict, silently.
- At most one CHALLENGE round, ever.
- The model never touches Heat, Gravity, Pressure, thresholds, timers, exit selection, coverage arithmetic, or Frozen.
- **Covered opens make no model call at all.** Silence includes the model.

A clearly bounded deliberate-leisure contract can receive ALLOW in both forks. Consistency challenges use only recorded facts: "You have called the last four sessions 'quick replies.' They averaged eleven minutes. What exactly are you replying to?" is factual and challengeable; "you're lying" is forbidden.

---

# 9. Primitives and sequences

## 9.1 The roster — eleven primitives

BD-06's structure stands: names are Addendum-01 shipped names, internal Python identifiers keep their original names, each sequence selects nine.

| # | Internal | Shipped name | Band | Status |
|---|---|---|---|---|
| 1 | knock | **Pause** | B | Built. One alert, one tap, real telemetry, no lecture. |
| 2 | ash | **Black and White** | B | Built as a real Color Filters toggle (BD-01-R2); restore leg wired at all four recovery paths; device proof pending. |
| 3 | silence | **Silence** | B | Built with capture-persist-restore; device proof pending (Phase 22). |
| 4 | dimming | **Dim** | B | Built (soft dim). Ambient sequence only until the capture-and-restore loop is device-proven. |
| 5 | confession | **Intention** | C | Built; v2 gives its verdict routing consequence (§8). |
| 6 | mirror | **Mirror** | C | Built (30 fact-gated templates); v2 moves it to Circle 5 and adds the three-route surface (§6). |
| 7 | — | **Redirect** | C | To build (Phase 18): lands the user in the deterministically selected exit, no menu; records through the same learning loop as voluntary exits. |
| 8 | exile | **Eject** | D | Built (straight to Home Screen). |
| 9 | voice | **Loud Mirror** | D | Built (Phase 15); speaks the reflection once, gated on consent, safe volume. |
| 10 | ice_start | **Frozen** | D | Built. Deterministic cooldown; never model-touched; route out guaranteed. |
| 11 | — | **Blackout** | D | **Parked.** Hard dim to the device minimum as a Band D primitive — not in any sequence until the capture-and-restore loop is device-proven *and* a sequence slot is deliberately re-cut for it. Recorded so the idea is kept without a stale slot claim. |

The v1 single "Dim at Circle 5" is retired: the user's design splits dimming into soft ambient friction (Dim, Band B) and a forceful variant (Blackout, parked). D-01 is untouched — `safety.brightness_floor` and `safety.dim_target` ship at `0`, and the safety property is the capture-and-restore loop (§18), not any particular target value.

## 9.2 Sequences — band-invariant orderings

Three sequences remain, re-derived under one invariant: **band composition is fixed; only order within a band varies.** Band B draws from {Pause, Black and White, Silence, Dim}, Band C is {Intention, Mirror, Redirect}, Band D is {Eject, Loud Mirror, Frozen} with **Frozen pinned at Circle 9** always. This is what keeps the coverage gate, the verdict envelope, and the band rules identical whichever sequence is active.

| Circle | Classic (default) | BlackMirror | Ambient |
|---|---|---|---|
| 1 | Pause | Pause | Black and White |
| 2 | Black and White | Silence | Silence |
| 3 | Silence | Black and White | Dim |
| 4 | Intention | Mirror | Intention |
| 5 | Mirror | Intention | Mirror |
| 6 | Redirect | Redirect | Redirect |
| 7 | Eject | Loud Mirror | Eject |
| 8 | Loud Mirror | Eject | Loud Mirror |
| 9 | Frozen | Frozen | Frozen |

- **Classic** is the covenant ladder as designed: the reference escalation.
- **BlackMirror** surfaces reflection before the ask (Mirror at 4) and speaks before it ejects — the uncanny sequence.
- **Ambient** is environmental-first (no Pause; Dim replaces it in Band B) — for the user who prefers quiet changes over dialogs (§11).
- Classic and BlackMirror drop Dim; Ambient drops Pause; all three drop Blackout (parked). Redirect at 6 in all three: with verdicts routing Band C, the colder Eject-at-6 variant BD-06 gave BlackMirror is retired — Eject is Band D's business.

This table supersedes BD-06 Decision 4's slot allocation (recorded as BD-09). Sequence switching from the manual menu, the exact-match dispatch, and the dispatch-coverage build guard all carry forward unchanged.

---

# 10. Behavioural state model

## 10.1 Unchanged core

Behavioural day (date − 4h, 04:00 rollover), Heat pipeline (decay → base → reopen bonus per `reopen_bonus_mode` → overrun penalty → respected relief → clamp), Gravity, Pressure, ordered-scan Circle resolution, duplicate-OPEN debounce, race-proof CLOSE with session ownership, rolling windows, flat-key discipline, the nine parameter-defect axes, and every build guard: all carried forward exactly as built. The v2 conversion adds to this engine; it does not alter it.

## 10.2 Covenant state (new keys, same discipline)

A permanent seeded container (axis-7 discipline: seed at bootstrap, write and clear leaves flat, numeric or sentinel gates, never condition-100 over a container; mind the single-item list collapse):

```json
"active_contract": {
  "made_at": 0,
  "expires_at": 0,
  "intention": "none",
  "boundary_seconds": 0,
  "opens_within": 0,
  "rapid_returns_within": 0,
  "consumed_seconds": 0,
  "status": "none"
}
```

plus `recent_contracts` (rolling ~10, now actually written — outcome, declared vs consumed, invalidation reason), and a persisted `variability_counter` (§13). Schema version bumps with the usual migration honesty; every new key gets a seed and a `verify_*_seed()` guard.

## 10.3 Config additions

All PROTOTYPE DEFAULTs, tunable in the single Config block, never hardcoded inline:

```json
"contract": {
  "default_boundary_minutes": 10,
  "max_opens_per_window": 3,
  "max_rapid_returns_per_window": 1,
  "coverage_ceiling_circle": 7
},
"verdict": {
  "challenge_overrun_count": 2,
  "deny_min_circle": 6
},
"bands": {
  "ask_entry": 4,
  "rescue_entry": 7
},
"variability": {
  "spot_check_interval": 0
},
"heat": { "covered_reopen_bonus": "none" }
```

(`heat.covered_reopen_bonus` shown here in its family; it joins the existing `heat` object.)

---

# 11. Profiles and personalized descent

Two people with identical usage can deserve different products: one is content with their use and wants a light touch; the other uses the same amount, is unhappy about it, and wants strictness. v2 personalizes on **how much of a problem the person says it is**, not on how much they use.

## 11.1 Severity → profile

The existing three-profile machinery (Paradise / Purgatory / Inferno threshold tables, Circle 0 entry points, Ice durations) is the substrate. What changes is the elicitation: the import question stops asking users to choose between three mythological words cold and asks the severity question in plain language:

> **How do you feel about your use of the apps you'll track?**
> - "Mostly fine — keep a light touch" → **Paradise** (slow descent; Band C is rare)
> - "Somewhat concerned — balance it" → **Purgatory** (default)
> - "It's a real problem — be strict with me" → **Inferno** (fast descent; the ask arrives early)

The mythological names remain the profiles' names everywhere else (Note, Status, Change Profile); the elicitation maps a feeling to a pace. Mechanically this is the existing import question with new option text and the same If-chain mapping — `WFWorkflowImportQuestions` remains a literal-prefill mechanism and is used within its limits.

## 11.2 Modality → sequence

A second plain-language question selects the default sequence:

> **When PROSOCHĒ does step in, what should it prefer?**
> - "Questions and reflections" → **Classic**
> - "Quiet changes to the screen and sound" → **Ambient**

BlackMirror remains a connoisseur's choice, switchable from the manual menu as all sequences are.

## 11.3 Descent pace is the personalization mechanism

Fixed bands plus per-profile thresholds already produce the requested behaviour: the content user's Pressure climbs slowly, so they live in Bands A–B and may never meet the ask; the unhappy user's Pressure climbs fast, so the ask arrives quickly. The reserved `bands.ask_entry` / `bands.rescue_entry` keys (§6) allow future per-profile band-boundary tuning if device evidence shows pace alone is not enough — a deliberate second knob, unused in v2.0.

## 11.4 Re-elicitation

Severity drifts. `Change Profile` and `Change Sequence` exist in the manual menu; the Attention Receipt moment (Phase 27) is the natural future point to gently re-ask the severity question. Recorded as a v2-later idea, not a v2.0 surface.

---

# 12. Touchpoint invariants

These are product law, testable, and the acceptance criteria in §24 assert them:

1. **A conscious user's day produces zero surfaces.** All opens land in Band A or under coverage.
2. **At most one interactive surface per OPEN, ever.** The ask-plus-one-challenge counts as one surface flow. There is no announcement before a primitive and no second dialog after it. The v1 universal `Leaving / Continue` pre-menu is retired; its two jobs move into the primitives themselves.
3. **Every interactive surface carries a one-tap leave route** (§3.4's strongest lever): Pause offers leave/continue; the ask offers "take me somewhere better" alongside declaration; the Mirror offers continue/leave/declare. Band B's non-interactive surfaces have nothing to dismiss — the friction itself is the whole encounter. Band D's forceful moves *are* the leave, performed for the user.
4. **Escalate salience, never frequency.** Depth changes what a touchpoint is, not how many there are.
5. **Silence is never interrupted to praise.** Success is reflected only inside surfaces that were already firing (§19's positive templates).
6. **Panic Escape** is re-expressed: it is no longer a pre-menu but the **leave affordance inside interactive surfaces**. Its deliberate removability (Addendum 01 §3) survives with the same Note-edit-plus-confirmation path; removing it strips the leave option from Band B–C surfaces. **Emergency Restore is not Panic Escape** and remains unconditionally reachable — that separation is safety-critical and carries forward verbatim from Phase 11.

---

# 13. Variability against ritualisation

## 13.1 The failure mode

An intervention repeated identically trains its own dismissal: the user's finger learns the geometry, and the prompt is gone before the words are read — attention deferred by reflex, which is Epictetus' warning in *Discourses* 4.12 made literal, and exactly what has happened to Screen Time's daily-limit prompt in the wild. For PROSOCHĒ this failure is fatal rather than incidental, because the product's entire value lives in the moment of genuine consideration.

## 13.2 The design answer — deterministic variability

The stimulus varies so the response cannot become motor. All variability is **counter-based and deterministic** (persisted counters and modulo tests, the same idiom as the exit epsilon step): reproducible under test, auditable in state, no `number.random` anywhere. The standing decision that nothing nondeterministic enters the exit path extends product-wide: **nothing nondeterministic, and no variability of any kind, ever touches Frozen, cooldown durations, coverage arithmetic, verdict envelopes, safety paths, or environmental changes.**

Three sanctioned mechanisms:

1. **Surface rotation** (exists, extend): the Mirror already selects among 30 fact-gated templates; Pause gains a small copy bank so its words are not constant. Rotation is keyed off persisted counters, not chance.
2. **The spot check** (new, ships off): when `variability.spot_check_interval = N > 0`, every Nth *uncovered Band B* open runs the Intention ask in place of the slotted passive primitive. A jump **into the ask band only** — never into Band D, never out of Band A, never during cooldown, never altering Pressure or thresholds. The rationale: an occasional unpredicted ask at a shallow depth keeps the ask an event rather than a station on a memorized route, and gives an honest user an unprompted chance to buy standing silence cheaply. Downward jumps into Band D are rejected by design: a punishment lottery breaks proportionality, violates the benevolence stance, and would make the strongest interventions arbitrary precisely where trust matters most.
3. **Exit exploration** (exists): the epsilon-greedy exit rotation already makes the *destination* of redirects usefully non-monotonous.

## 13.3 Research posture

`spot_check_interval` ships at `0` (off). Phase 23 owns the research: turn it on after the covenant model has device evidence, and evaluate against contract specificity over time, fidelity trends, and observed dismissal cost (SEED-009 item 2's dismissibility observations), plus self-report. Honesty note: on-device measurement of "was this dismissal mechanical?" is weak; the phase must define its proxies before tuning and record what they cannot see.

---

# 14. The six exits

Carried forward from v1 without structural change, with Redirect now a Band C primitive feeding the same machinery:

- **Capture** — get something out of your head (note, voice memo, camera).
- **Coordinate** — turn vague load into a plan (reminders, calendar).
- **Create** — make rather than consume (user-defined target).
- **Connect** — an actual human instead of a feed (never initiates contact on the user's behalf).
- **Consult** — satisfy the information need without entering a feed: query-shaped search (web/maps/notes/reminders/calendar menu in Core; classification assist in Aware).
- **Close** — the phone is not the next action: home or lock, a first-class outcome, never decorated.

Exit learning is unchanged: outcomes are time-until-next-tracked-OPEN; epsilon-greedy with even rotation below `exits.exploit_min_observations`; exploration rate is Config; selection is deterministic and never the model's. Voluntary leaves, DENY redirects, and Circle 6 Redirects all record through `record_exit_and_route()` so the involuntary path feeds the same learning loop. Route deepening (each exit landing somewhere real, seeded with the current intention where one exists) is Phase 18 scope.

---

# 15. Onboarding and the Note

## 15.1 Import questions (Layer A)

Simple, robust, literal-prefill only:

1. **Severity** → profile (§11.1). Default Purgatory.
2. **Modality** → sequence (§11.2). Default Classic.
3. **Voice** — "May PROSOCHĒ speak to you at the deepest circles? yes/no."
4. **On-device intelligence** (Aware only) — yes/no.

## 15.2 The Note (Layer B)

`PROSOCHĒ` (renamed from `PROSOCHĒ — Control Room` by Addendum 01; internal name unchanged) carries, as built: READ THIS FIRST with the exact steps for both Personal Automations and the plain statement that PROSOCHĒ cannot install them and is bypassable; the essential-apps safety warning; the **Color Filters disclosure and its kill switch** (`safety.ash_managed_color_filters`); the editable `MY PHONE, ON PURPOSE` proforma; CURRENT SETTINGS; CURRENT STATE; the ATTENTION LEDGER (meaningful events only); the optional-hardening note (adding Shortcuts itself to the target list); and the Panic Escape removal path. `Sync My Profile` remains the only path that parses the proforma into state; the OPEN path never reads the Note.

The v2 addition to the Note's teaching voice: one short paragraph explaining the covenant — *tell it what you're doing and stay inside your boundary, and it stays out of your way.* The manual menu carries forward (Status, Open Control Room, Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today, Emergency Restore, Setup Check; plus Toggle On-Device AI and Test Model in Aware) and gains **Set an intention** (§7.1).

---

# 16. OPEN handler

When input = `OPEN`:

1. load state; self-heal if missing/corrupt;
2. behavioural-day rollover;
3. duplicate-OPEN debounce;
4. cooldown check (a live Frozen short-circuits to the redirect, unchanged);
5. pending-exit outcome recording;
6. Heat decay → open count → covered-reopen-aware rapid-return bonus (§7.5) → contract-fidelity adjustment → Gravity → Pressure → Circle;
7. contract bookkeeping: increment `opens_within` / `rapid_returns_within` if a window is live; apply invalidation rules (§7.3);
8. create session; persist state;
9. **route (§5.3):** Circle 0 → end. Covered and Circle < ceiling → end. Otherwise → variability spot check if armed and eligible (§13.2), else the current Circle's primitive per the active sequence;
10. log meaningful events to the ledger where appropriate — never ahead of the intervention.

# 17. CLOSE handler

Unchanged race-proof structure (reload, ownership check, abort if superseded), plus covenant accounting:

1. measure session duration from the recorded start;
2. add it to `active_contract.consumed_seconds` when a window is live; settle the contract outcome on expiry (§7.4) into `recent_contracts` and the Heat inputs;
3. update recent sessions; record exit outcomes where relevant;
4. **restore every environmental setting PROSOCHĒ changed** — brightness, volume, Color Filters off — through `restore_managed_settings()`;
5. clear the session; persist; append a readable CLOSE line when useful;
6. Aware may precompute the next Mirror (v2-later, OPT-01/02).

---

# 18. Environmental safety

Current truth, stated directly (the dated decision trail is BD-02, D-01, D-02, BD-01-R2 in `docs/CAPABILITY-DECISIONS.md`):

- **The safety property is capture → durable persist → apply → restore.** Every environmental change captures its original value and persists it to disk *before* the device is changed, and every recovery path restores it: CLOSE, Emergency Restore, Ice expiry, the live-Ice redirect. A setting whose original cannot be captured is left unchanged.
- **Brightness:** `safety.brightness_floor` and `safety.dim_target` both ship at `0` (D-01) — iOS's practical minimum renders dim, not black, per the owner's on-device report. The bound is a tuning value; the loop above is the safety mechanism. The loop is structurally proven and **device-unproven** — Phase 22 owns the proof, including force-quit, restart, CLOSE-never-fires, overlapping sessions, and locked-screen cases. `setbrightness.WFBrightness` is OPTIONAL and defaults to 50%, so device tests must verify the *value applied*, never the absence of an error.
- **Volume:** capture-and-restore proven end-to-end at rung 3 for volume; never raised, never startling, `Media` channel pinned at all sites.
- **Color Filters (Black and White):** a two-valued setting with no read-back anywhere in iOS — so "restore" is unconditionally "set it off," wired first in `restore_managed_settings()` so no dotted read can abort ahead of it. Default ON, disclosed in the Note with the `safety.ash_managed_color_filters` kill switch; the pre-existing-grayscale user is accepted and backlogged, not silently harmed twice.
- **Emergency Restore** clears cooldown and the active session and restores recoverable brightness, volume, and colour state; it is reachable from the manual menu and from inside Frozen, and is never gated on any Note-editable setting.
- **Accessibility:** pre-existing accessibility configuration is never blindly overridden; the kill switch and disclosure are the §21-lineage opt-in mechanism.

---

# 19. What PROSOCHĒ sounds like

Carried from v1 in full. Concrete behavioural facts; no slogans, no exclamation marks, no emoji; never "addiction," "dopamine," "weakness," "lazy," "failure," "shame." One specific observation beats a motivational sentence. The Mirror's 30+ templates are fact-gated (no overrun line without a contract; no trend without data; medians over means) and include success acknowledgment — "You said five minutes and left after four. Deliberate use appears to be working." — so opening a tracked app never reliably predicts criticism. The system's memory is its uncanniness; accuracy is its licence.

---

# 20. PROSOCHĒ Aware

Core is the baseline product and the control condition, not a degraded afterthought; Aware adds judgment, never authority.

- **Model:** Apple On-Device via `Use Model`, pinned with the device-evidenced literal `Apple Intelligence on Device` (BD-04-R2). PCC remains an authorised fallback only; ChatGPT/extension models excluded. The no-network runtime guarantee stays unclaimed until device-verified.
- **Where the model appears:** the Band C ask (verdict within the envelope, §8.3) and reflection generation for Mirror/Loud Mirror. Nowhere else. Covered opens and Bands A/B/D make no model call. Frozen never involves the model.
- **Context:** the compact window only — profile goals, current telemetry, current and recent contracts, exit history. Never the Note, never app contents, never invented mental states.
- **Failure:** malformed, empty, or slow output falls through to Core behaviour without breaking the run. Deterministic fallbacks are mandatory everywhere.
- **The longitudinal opportunity** (v1 §15, carried): patterns across time — "Your deliberate scrolling is usually bounded. The sessions you call 'quick replies' are the ones that expand." — remain the strongest Aware material, built strictly from recorded aggregates.

---

# 21. Measurement

Local only. The v2 metric set:

- **Co-primary: rapid-return rate** (sessions followed by another tracked OPEN within 2/10 minutes) **and contract fidelity** (consumed vs declared, medians and distributions, never moral scoring).
- **Covered-open share:** the fraction of opens under coverage — rising is the covenant working.
- **Surfaces per day:** the touchpoint budget made measurable — falling while covered share rises is the product succeeding.
- **Circle distribution, exit outcomes, time-to-return** — unchanged.
- **Disable rate** — still the critical product-quality signal: an intervention annoying enough to be switched off is a failure whatever it blocked.

Definition of success, unchanged in spirit and now mechanically visible: fewer automatic opens, fewer rapid returns, more bounded deliberate sessions, lower Heat, **more silence** — PROSOCHĒ gradually has less work to do.

---

# 22. Failure modes

- **Intervention fatigue** → Band A/B silence, coverage, concise copy, template rotation.
- **Ritualisation** (new, first-class) → §13's variability; the ask prefills to stay cheap for honest users; fidelity trends watched as the proxy.
- **Coverage gaming** (new) → §7.6: Gravity still counts, invalidation still bites, verdict history pulls CHALLENGE earlier.
- **Disablement** → deliberate leisure respected, silence as default, Paradise available, strong moves only on strong evidence.
- **State races** → session IDs, reload-before-commit, idempotent restore (built).
- **Notes growth** → JSON is live state; the Note logs meaningful events only.
- **Generative inconsistency** → structured output, parse validation, deterministic fallback, envelope discipline (built).
- **Accessibility interference** → disclosure + kill switch + unconditional off-leg (built).
- **False psychological inference** → banned vocabulary, facts only (built).
- **Phone-shaped substitution** → Close is first-class; exit learning rewards time away, not app-swapping.

---

# 23. What is already built and stands

The v2 conversion is a routing and surface change on top of a proven foundation. Delivered and carried forward without redesign:

- **The deterministic state engine** — behavioural day, Heat/Gravity/Pressure, profile threshold tables, Circle 0 silent band, duplicate debounce (Phases 3, 10).
- **The race-proof CLOSE pipeline** and session-ownership protocol (Phase 4).
- **Bootstrap, routing, self-healing** — corrupt/missing state recovery, Note recreation, import questions (Phase 2).
- **The Control Room Note** and manual menu, Sync My Profile, Test a Circle, Setup Check (Phases 2, 7, 10).
- **Ten primitives** including the real Color Filters toggle (Phase 14), the Voice primitive (Phase 15), and capture-persist-restore environmental machinery (Phases 9, 16) — device proof pending, owned by Phase 22.
- **Six exits with epsilon-greedy learning** and the pending-exit outcome loop (Phase 6).
- **The Aware fork** as one additive gated insertion with the device-evidenced model literal (Phase 8; SEED-005 tracks the refork).
- **The whole build discipline:** the nine parameter-defect axes, the two-gate validator rule with `gate_a_residue_check.py`, 14 structural checkers, dispatch-coverage and seed guards, AEA1 decrypt verification, donor evidence, the evidence-escalation ladder. None of this is model-dependent; all of it is what makes the conversion safe to attempt.
- **Dante naming and fork naming** (Addendum 01 / BD-06 Decisions 1–3, 5 / BD-06-A1): positional Circle names, Paradise/Purgatory/Inferno, Core/Aware, the `PROSOCHĒ` Note title.

---

# 24. Build strategy and acceptance criteria

## 24.1 Conversion strategy

The roadmap (Phases 17–20) converts the artifacts in dependency order: covenant substrate (state, coverage gate, Core verdict) → bands and surfaces (pre-menu retirement, slot table v2, Redirect, Mirror surface) → personalized onboarding → Aware envelope alignment. Device debugging and the full UAT follow (Phases 21–22); variability research after evidence (Phase 23). One generator, both forks, every change through the existing guard suite; no phase re-litigates settled capability decisions.

## 24.2 Acceptance criteria (delta over the v1 criteria, which remain in force for everything carried)

**Coverage**
- A covered open shows no surface, sends no notification, calls no model, and still updates state fully.
- Coverage never applies at Circle ≥ the ceiling; a live cooldown always short-circuits first.
- Each invalidation rule (expiry, open-count, rapid-return) ends coverage and the next uncovered open routes normally.
- Contract outcomes land in `recent_contracts` losslessly and feed both Heat and the verdict history.

**Bands and surfaces**
- A Circle 0 open shows nothing; an uncovered Band B open shows only its primitive (single alert at Circle 1; no dialog at 2–3); an uncovered Band C open shows exactly one interactive surface; Band D fires forcefully with no question.
- No open ever shows two surfaces. The pre-menu is gone; every interactive surface carries its leave route; Panic Escape removal strips exactly those leave routes and nothing else; Emergency Restore is untouched by all of it.
- The three sequences differ only within bands; Frozen is Circle 9 in all three; dispatch coverage remains a hard build gate.

**Verdicts**
- Core's verdict is pure recorded-fact arithmetic; Aware's is envelope-bounded with silent deterministic fallback; one challenge round maximum; DENY only at Circle 6 and only ever a redirect.

**Personalization**
- The severity and modality questions map to profile and sequence; all three profiles produce demonstrably different descent for identical open patterns; band-entry keys exist in Config and default to 4/7.

**Variability**
- Ships off. When armed in test: spot checks fire only on eligible uncovered Band B opens at the counter interval, deterministically reproducible from state; nothing nondeterministic anywhere in Frozen, safety, environmental, or coverage paths.

**Safety (unchanged and re-asserted)**
- Environmental capture-persist-restore on every path; Emergency Restore recovers every failure mode found; no unsafe volume; no accessibility stranding; Frozen always expires with a route out.

---

# 25. Canonical product decisions

| Decision | Current answer |
|---|---|
| Core product | Adaptive-friction attention system on the covenant model |
| Interaction model | Two axes: Pressure ladder + contract coverage; four fixed bands |
| Coverage | Valid contract → silence; ceiling at Circle 7; deterministic invalidation |
| Target | iOS 26.x, native Shortcuts only |
| Forks | Core (deterministic) + Aware (On-Device model); one-product question owned by Phase 25 |
| Verdicts | ALLOW/CHALLENGE/DENY in both forks; deterministic envelope; DENY = redirect at Circle 6 only |
| Circles | Nine + silent Circle 0; Dante names positional; Frozen pinned at 9 |
| Sequences | Three, band-invariant; Classic default; switchable locally |
| Profiles | Paradise / Purgatory / Inferno, selected by plain-language severity question |
| Personalization | Severity → profile; modality → sequence; band-entry keys reserved |
| Intention | Free text + mandatory boundary; deliberate leisure explicitly valid; blank text never judged |
| Variability | Deterministic, counter-based; spot check into Band C only; ships off; never in Frozen/safety/environmental |
| Exits | Six; epsilon-greedy learning; deterministic selection; Redirect feeds the same loop |
| AI role | Attention mirror and contract auditor inside a deterministic envelope; no model on covered opens |
| Model control of state, thresholds, timers, Frozen | Never |
| Machine store / human store | One JSON / one Note; no CSV |
| Privacy | Nothing leaves the device; compact model context only |
| Environmental safety | Capture → persist → apply → restore; kill switch + disclosure for Color Filters |
| Distribution | Free, open source, forkable; pay-after-value later; never during a block |
| Marketing spine | Attention / agency / Epictetus / prosochē / Thaler's choice architecture |

---

# 26. Open source and privacy

Unchanged from v1: the repository ships signed artifacts, unsigned XML source, architecture docs, prompts, and honest limitation notes. The README states plainly that behavioural data stays on the device, there is no analytics, model output can be wrong, and the system is self-directed and bypassable. The Note and JSON may sync through the user's own iCloud; PROSOCHĒ itself transmits nothing. Aware stores only final model outputs needed for continuity, never hidden reasoning. "Life Returned" estimation (personal counterfactual baselines, always labelled estimates) and pay-after-value support (never during a block, never guilt, never a functionality gate, `Never ask again` honoured permanently) remain recorded-now-designed-later, owned by Phases 26–28.

---

# 27. Sources

## Philosophy

Epictetus, *Enchiridion*, ch. 1 — the dichotomy of control.
https://classics.mit.edu/Epictetus/epicench.html

Epictetus, *Discourses*, Book IV, ch. 12 — "On Attention" (prosochē; the habit-forming cost of deferred attention).
https://en.wikisource.org/wiki/The_Discourses_of_Epictetus%3B_with_the_Encheiridion_and_Fragments/Book_4/Chapter_12

Thaler R, Sunstein C. *Nudge: Improving Decisions About Health, Wealth, and Happiness.* 2008 — choice architecture, defaults, libertarian paternalism.

Thaler R, Benartzi S. *Save More Tomorrow: Using Behavioral Economics to Increase Employee Saving.* Journal of Political Economy, 2004 — commitment devices.

Thaler R, Shefrin H. *An Economic Theory of Self-Control.* Journal of Political Economy, 1981 — the planner–doer model.

## Behavioural / digital wellbeing

Lukoff K, Yu C, Kientz J, Hiniker A. *What Makes Smartphone Use Meaningful or Meaningless?* IMWUT, 2018. https://doi.org/10.1145/3191754

Keller J, Roitzheim C, Radtke T, Schenkel K, Schwarzer R. *A Mobile Intervention for Self-Efficacious and Goal-Directed Smartphone Use…* JMIR mHealth and uHealth, 2021. https://pubmed.ncbi.nlm.nih.gov/34817388/

*Promoting Self-Regulated Social Media Use… (Wellspent): RCT.* JMIR mHealth and uHealth, 2026. https://pubmed.ncbi.nlm.nih.gov/41950504/

Grüning DJ, Riedel F, Lorenz-Spreen P. *Directing smartphone use through the self-nudge app one sec.* https://pmc.ncbi.nlm.nih.gov/articles/PMC9974409/

Zimmermann L, Sobolev M. *Digital Strategies for Screen Time Reduction: A Randomized Field Experiment.* 2023. https://pubmed.ncbi.nlm.nih.gov/36577008/

Almoallim S, Sas C. *Toward Research-Informed Design Implications for Interventions Limiting Smartphone Use…* JMIR Formative Research, 2022. https://pubmed.ncbi.nlm.nih.gov/35188897/

*Suffering from problematic smartphone use? Why not use grayscale setting…* Computers in Human Behavior Reports, 2023. https://doi.org/10.1016/j.chbr.2023.100294

*Before You Scroll Again: Predicting Regretful Social Media Sessions…* 2026 preprint — treat as emerging evidence. https://arxiv.org/abs/2606.08965

Wu R et al. *MindShift: LLMs for Mental-States-Based Problematic Smartphone Use Intervention.* 2023 preprint. https://arxiv.org/abs/2309.16639

## Apple / technical

Apple Support — What's new in Shortcuts (iOS 26): https://support.apple.com/en-au/125148
Apple Support — Setting triggers in Shortcuts: https://support.apple.com/en-ca/guide/shortcuts/apde31e9638b/ios
Apple Support — Personal automation intro / creation / enable-disable: https://support.apple.com/en-gb/guide/shortcuts/apd690170742/9.0/ios/26 · https://support.apple.com/en-gb/guide/shortcuts/apdfbdbd7123/9.0/ios/26 · https://support.apple.com/en-au/guide/shortcuts/apd602971e63/ios
Apple Support — Apple Intelligence in Shortcuts: https://support.apple.com/guide/iphone/use-apple-intelligence-in-shortcuts-iph78c41eaf8/ios
Shortcuts Playground: https://github.com/viticci/shortcuts-playground-plugin

---

# Appendix A — v1 → v2 section map

Historical documents cite "canonical strategy §N" against v1 (git tag `pre-covenant-overhaul`). Resolution table:

| v1 § | Subject | v2 home |
|---|---|---|
| 0 | Executive brief | §0 |
| 1 | The problem | §1 |
| 2 | Philosophy / Epictetus | §2 (expanded: §2.1–2.4) |
| 3 | Design influences (Thaler, Newport, Clear, Jobs, Black Mirror) | §2.2–2.3 |
| 4 | Product boundaries | §4 |
| 5 | Technical viability (triggers, no self-install, size, Note-vs-JSON, no CSV, Use Model, device split) | Facts carried into §0, §4, §15, §20; the full v1 analysis is historical and stands at the tag |
| 6 | Evidence | §3 |
| 7 | Onboarding | §15 (severity/modality: §11) |
| 8 | The six exits | §14 |
| 9 | Explore/exploit | §14 |
| 10 | Behavioural state model; 10.5 profiles; 10.6 Circle 0 | §5.1, §10, §11; Circle 0: §6 (Band A) |
| 11 | Nine primitives | §9.1 (roster now eleven; Dim split; Blackout parked) |
| 12 | Candidate sequences + testing philosophy | §9.2, §21–22 |
| 13 | Dumb fork | Core throughout; templates/voice: §19; verdict: §8.2 |
| 14 | Sentient fork; 14.3 verdicts | §20; verdicts: §8 (**changed:** both forks, routing consequence) |
| 15 | Longitudinal memory | §20 |
| 16 | JSON state design | §10 |
| 17 | Control Room Note | §15.2 |
| 18 | First-run flow / automations | §15; the exact automation steps live in the Note literal (quick task 260817-au7) |
| 19 | OPEN handler | §16 (**changed:** coverage gate at step 9) |
| 20 | CLOSE handler | §17 (**changed:** consumed-seconds accounting) |
| 21 | Environmental safety | §18 (**changed:** states D-01-era truth directly; the v1 floor clause is retired and not restated) |
| 22 | Circle IX / Ice | §6 Band D, §9.1, §18; unchanged mechanics |
| 23 | Measurement | §21 (**changed:** fidelity co-primary; covered share; surfaces/day) |
| 24 | Life Returned | §26; Phases 26–27 |
| 25 | Pay after value | §26; Phase 28 |
| 26 | Open-source principles | §26 |
| 27 | Privacy model | §26 |
| 28 | Model-context design | §20 |
| 29 | What Sentient sounds like | §19 |
| 30 | Failure modes | §22 (**expanded:** ritualisation, coverage gaming) |
| 31 | Build strategy | §24 |
| 32 | Acceptance criteria | §24.2 (v1 criteria remain in force for carried behaviour) |
| 33 | Research questions | §13.3, §21, Phase 22–23 goals |
| 34 | Future roadmap | `.planning/ROADMAP.md` |
| 35 | Canonical decisions | §25 |
| 36 | PM summary | §0, §2.4, §21 |
| 37 | Sources | §27 |
| 38 | Final instruction | Authority note in the header |

# Appendix B — Vocabulary

- **The covenant model** — the v2 design: silence for declared, bounded use; proportionate escalation otherwise.
- **Intention contract / contract** — the mechanism term (state keys, code, metrics): free text + boundary + window.
- **Coverage / covered open** — an open inside a valid contract window at a Circle below the ceiling; fires nothing.
- **Bands** — Silent (0) · Ambient (1–3) · Ask (4–6) · Rescue (7–9); fixed boundaries, sequence-invariant.
- **Verdict envelope** — the deterministic per-Circle set of available verdicts the model may choose within.
- **Spot check** — a counter-scheduled ask fired in place of an Ambient primitive; the anti-ritualisation jump, Band C only.
- **Panic Escape** — the removable one-tap leave affordance inside interactive surfaces. Never Emergency Restore.
- **Ritualisation** — mechanical dismissal of a repeated identical surface; the failure mode §13 exists to interrupt.
