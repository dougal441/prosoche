# Feature Research

> **v1-ERA RESEARCH (2026-08-13) — read with the re-foundation in mind.** The project was
> re-founded 2026-08-19 on canonical strategy **v2.0** (the covenant model; decisions
> BD-09..BD-12 in `docs/CAPABILITY-DECISIONS.md`): contract coverage above the Circle ladder,
> four fixed bands, verdicts in both forks, the BD-09 slot table. `§N` citations below refer
> to canon **v1** (preserved at git tag `pre-covenant-overhaul`) and resolve via canon v2
> Appendix A. Toolchain, plist, and capability findings here remain valid; claims about the
> interaction model (combined sequence entries, Confession as a Circle-4 rung with no routing
> consequence, the `Limbo` profile name — now `Purgatory` — and the universal Leaving menu)
> are historical.


**Domain:** Adaptive-friction attention/digital-wellbeing intervention, delivered as a native iOS Shortcut (no companion app, no blocking APIs)
**Researched:** 2026-08-13
**Confidence:** HIGH (all features traced to the canonical strategy document; competitor benchmarking MEDIUM — based on current marketing/review pages, not internal telemetry)

**Scope note:** Every feature listed below already exists in `PROSOCHE_Nine_Circles_Canonical_Strategy.md`. This document does not invent scope — it classifies, sequences, and benchmarks what is already specified. Section references (`§N`) point to that file.

---

## Consolidated Classification

### Table Stakes (product is broken or dishonest without these)

The deterministic core. Without these, PROSOCHĒ is not a working behavioural-friction Shortcut — it's a toy or a lie (e.g. claiming adaptive Pressure while doing nothing behavioural, or claiming "safe" while it can't restore brightness).

| Feature | Why non-negotiable | Complexity | Section |
|---|---|---|---|
| Bootstrap creates `state.json` + Control Room Note, idempotent on later runs | Without this the product has no memory and re-onboards destructively every run | HIGH | §7, §18, §32 |
| Native import questions (profile, voice; AI toggle Sentient-only) | Zero-config first run is part of the "self-saucing" promise | LOW | §7.1 |
| Behavioural day = date − 4h | Midnight-reset loophole would make Pressure trivially gameable | LOW–MEDIUM | §10.1 |
| Heat calc (decay/increment/rapid-return/contract-fidelity, floor 0, cap 30) | This *is* the compulsive-clustering signal — the product's core claim | HIGH | §10.2 |
| Gravity calc (`floor(opens_today/6)`, cap 5) | Whole-day accumulation signal; without it Pressure only reacts to bursts | LOW | §10.3 |
| Pressure = Heat + Gravity, mapped to Circle via profile table | The entire escalation mechanic depends on this single line of arithmetic | MEDIUM | §10.4–10.5 |
| Three profiles (Paradise/Limbo/Inferno) | "You choose how aggressively this happens" is a stated product promise | LOW–MEDIUM | §10.5 |
| Session-ID race-proof OPEN/CLOSE reconciliation | Overlapping automations on rapid app-switching will silently corrupt state without this | **HIGH** | §19, §20, §32 |
| CLOSE handler measures real session duration, computes overrun, restores settings | Contract fidelity, Heat's contract term, and exit-learning outcomes all depend on an honest CLOSE | HIGH | §20 |
| Nine primitives implemented (at minimum Knock, Confession, Exile, Ice) | These are the actual intervention — without them Pressure calculates but nothing happens | see Circles table below | §11 |
| Circle IX (Ice): deterministic cooldown, never model-decided, blocked attempts don't inflate Heat, always a route out | The one hard safety/product-integrity boundary — a trap with no exit is the single worst possible failure mode | HIGH | §11, §22, §32 |
| Intention contracts: free text + duration incl. custom; deliberate leisure valid | Table-stakes because Confession is one of the nine primitives and contract fidelity is the secondary success metric | LOW–MEDIUM | §8.4 (D), §13.2 |
| Six exits, all invokable, all outcomes recorded | "Where should attention go?" is answered nowhere else in the product | LOW–MEDIUM per exit | §8 |
| Exit outcome recording (time-to-next-tracked-OPEN) | Without this, exit learning has no signal to learn from | MEDIUM–HIGH | §9.1 |
| Basic exit rotation (explore phase) | Needed before any exploitation is possible; also table stakes because the spec requires "basic explore/exploit selection functions" (§32) | MEDIUM | §9.2 |
| Environmental safety floors (no zero brightness, no loud volume, no accessibility-stranding, skip if can't restore) | This is the line between "friction" and "harm" — a hard constraint, not a feature to trade off | HIGH | §21, §32 |
| Emergency Restore | The single required escape hatch from any stuck/ambient state | MEDIUM–HIGH | §17, §21 |
| Corrupt/missing JSON and deleted Note both trigger safe recovery | A behavioural tool that crashes on its own missing state file is not shippable | MEDIUM–HIGH | §32 |
| Control Room manual menu (Status, Open Control Room, Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today, Emergency Restore) | This is the entire configuration surface — there is no other UI | MEDIUM | §18 |
| Control Room Note structure (READ THIS FIRST, proforma, settings, state, ledger) | The Note *is* onboarding — Apple forbids the Shortcut from installing automations itself, so the Note's instructions are the only path to a working install | MEDIUM–HIGH | §17 |
| Rolling-window JSON (last ~20 sessions, ~10 contracts, per-exit aggregates) | Required by spec to avoid unbounded arrays; also the substrate every metric and the Sentient context window reads from | MEDIUM | §16, PROJECT.md |
| Two signed `.shortcut` files + unsigned XML + build notes, validator pass | Without this nothing ships at all | MEDIUM | §26, §31–32 |
| No telemetry leaves device / no feature gate / no ads | Core to the honesty claim ("free and open source, permanently") — a business-model table stake, not a code table stake | N/A (policy) | §25, §27 |
| Never claim tamper-proof | A single sentence of copy, but the most important honesty constraint in the whole document — the user can always disable the Personal Automation | LOW | §5.1, PROJECT.md |

### Differentiators (the reason this product is interesting)

None of these exist in competing native-Shortcut or commercial blocker products in this combination. See Benchmark section for detail.

| Feature | Value proposition | Complexity | Section |
|---|---|---|---|
| Heat + Gravity dual-signal adaptive Pressure across nine discrete Circles | No competitor escalates through graduated stages driven by *live behavioural clustering* — Opal/ScreenZen are single-stage friction, Brick is binary blocked/unblocked | HIGH | §10, §11 |
| Three switchable Circle sequences (Classic/Black Mirror/Ambient) for local A/B comparison | Turns "which intervention order actually works" from marketing doctrine into a testable local variable, without remote infrastructure | MEDIUM | §12 |
| Six-exit taxonomy (Capture/Coordinate/Create/Connect/Consult/Close) with local epsilon-greedy learning of which redirect actually breaks the loop, per user | ScreenZen has static "replacement apps"; nothing in the category *learns* per-user which redirect works | HIGH | §8, §9 |
| Consult as query-shaped information retrieval (vs feed-shaped) | Directly answers "I had a real reason to open the app" without re-entering the addictive surface — no competitor separates information-seeking from consumption this way | MEDIUM | §8.5 |
| Deliberate leisure as an explicitly valid, protected contract outcome | Every competitor's mental model treats all target-app time as the enemy; PROSOCHĒ's is evidence-led (Lukoff et al.) and materially changes what "success" means | LOW (mostly a philosophy/copy decision, not new plist logic) | §6.1, §8.4 |
| Contract fidelity (intended vs actual duration, medians) as a first-class metric alongside/above raw screen time | Recent evidence (intention-actual gap) suggests this predicts regret better than duration alone — no mainstream competitor surfaces this | LOW–MEDIUM (derived from data already tracked) | §6.7, §23 |
| Sentient: On-Device model as "contract auditor" (specificity/boundedness/consistency), never a lie detector, structured ALLOW/CHALLENGE/DENY, max one challenge | No competitor product has an LLM behavioural-consistency auditor; the "not a lie detector" framing is itself a differentiator vs generic AI nagging | HIGH | §14 |
| Sentient longitudinal memory (median durations, exit performance by time of day, deliberate-leisure overrun trend) fed as compact context | This is "the Black Mirror opportunity" — a personal behavioural mirror the user could not easily construct themselves | HIGH | §15, §28 |
| Sentient per-circle AI involvement tiering (deterministic at I/IX, escalating model role II–VIII) | Balances latency/reliability against personalization — a genuinely novel graduated-AI-involvement pattern, not "AI everywhere" or "AI nowhere" | HIGH | §14.4 |
| Dumb Mirror engine: ≥30 fact-gated telemetry templates that never invent facts | A meaningful non-AI "Black Mirror" experience — most blockers either have no reflective copy or use generic motivational strings | MEDIUM | §13.1 |
| JSON + Note dual-store architecture (fast machine state + human-editable manifesto/ledger co-located in Notes) | No competitor gives users an inspectable, forkable, editable personal manifesto sitting next to their behavioural history | MEDIUM–HIGH | §5.4, §17 |
| Free, open-source, zero blocking-API, native-Shortcuts-only implementation | Positioning differentiator: no subscription, no hardware purchase, no FamilyControls entitlement, fully inspectable | N/A (architecture) | §26 |
| "Pay after value" model (parked, not v1) | Differentiates the eventual business model from every subscription competitor — recorded now, not built now | — | §25 |

### Anti-Features (deliberately NOT built — with reason)

Sourced from the canonical strategy's explicit Out of Scope list (§4) **and** from the evidence that disablement/intervention fatigue is the dominant failure mode (§30, §12 testing philosophy).

| Anti-feature | Surface appeal | Why rejected | What to do instead |
|---|---|---|---|
| Focus modes | Native iOS primitive, seems free to integrate | Explored and deliberately removed from v1; conflates "do not disturb" with adaptive per-app friction — different mental model | Possible future environmental layer, not required for the Nine Circles engine (§4) |
| NFC / physical commitment tokens (Brick-style) | Real-world friction has genuine evidence behind it (see Brick) | Adds a hardware dependency and a purchase requirement that contradicts "free, native, no companion app" | Revisit as Phase D extension only, as optional Circle IX unlock (§34) |
| Screen Time blocking APIs (FamilyControls/ManagedSettings/DeviceActivity) + companion app | Would make interventions "real" (unbypassable) | PROSOCHĒ is a behavioural intervention, not access control — building this would let the product claim tamper-proofing it cannot honestly make; also requires Xcode/entitlements, not just Shortcuts | Circle IX remains a strong-but-bypassable deterministic cooldown; the honesty about bypassability is explicitly part of the product (§5.1, §21) |
| CSV / any second machine store | Feels like "proper data export" | Two machine stores creates two sources of truth and race conditions; a growing rich-text Note is not a transactional store either | One JSON (machine), one Note (human) — nothing else (§5.5) |
| Cloud AI (ChatGPT, Private Cloud Compute, arbitrary web APIs, analytics services) | Better model quality, more capability | Breaks the on-device privacy claim, adds network dependency and latency, undermines "no behavioural data leaves the phone" | Apple On-Device model only, in Sentient fork only (§5.6, §27) |
| Remote A/B testing infrastructure | "Real" experimentation with server-side assignment | Out of proportion to a Shortcut-only prototype; the creator/friends comparison need is small | Three sequences switchable locally from Control Room menu (§12) |
| Screen Time telemetry (`Get App & Website Data`) as a core dependency | Would make "Life Returned" numbers objective | Action's real schema/granularity is unverified on-device; making it load-bearing risks building on an unverified capability | Research/measurement-only, later phase, and only after inspecting actual runtime behaviour (§24) |
| "Life Returned" quantification + pay-after-value prompts | Obvious monetization/motivation hook | Cannot yet be made mathematically honest (`100 blocked opens = X hours saved` is not evidenced); asking for money mid-intervention would be manipulative | Record the concept; observed counts (opens interrupted, rapid returns broken) can ship now, estimated-value math is designed rigorously later (§24–25) |
| Any tamper-proofing claim | Sounds more effective/trustworthy | The user can always disable the Personal Automation — claiming otherwise is dishonest and would be discovered instantly | State this limitation explicitly in the Control Room Note and README (§5.1, §26) |
| Repetitive/moralizing lecture copy at every Circle, or the same Mirror message reused | Feels like "reinforcing the message" | This is precisely the intervention-fatigue mechanism that leads to disablement — the dominant product failure mode | Passive early Circles, sequence variation, ≥30 templates, Sentient avoids repeating the same Mirror (§13.1, §29, §30) |
| Treating all target-app time / all leisure as failure | Simpler mental model, "less time = win" | Contradicted directly by Lukoff et al. (habitual/passive use less meaningful, but apparently "meaningless" use can serve a real function); punishing all leisure is a known driver of disablement | Deliberate leisure is an explicitly valid, protected contract outcome (§6.1, §8.4) |
| AI as lie detector / addiction diagnostician / mental-state inference | "Catch the user in the act" feels powerful | Sentient cannot know in-app content or mental state; false psychological inference is a named failure mode; also erodes trust and increases disablement | Contract auditor framing only — specificity/boundedness/consistency, behavioural facts only, max one challenge (§14.2, §30) |
| Guilt-based or functionality-gated monetization | Faster path to revenue | Explicitly rejected — never display a payment ask while the user is being blocked, never threaten loss of functionality | Pay-after-value, opt-in, "never ask again" option, no feature gate (§25) |

---

## Feature Landscape by Category

Each table below classifies features within the requested category, with Shortcuts-authoring-specific complexity notes.

### 1. Bootstrap & Setup

| Feature | Classification | Complexity (Shortcuts-specific) | Notes |
|---|---|---|---|
| First-run existence check → create `state.json` + Control Room Note | TABLE STAKES | HIGH | Requires reliable file-existence check in the Shortcuts-accessible location, then atomic-ish create of both artifacts before any Circle logic can run; must not race with a simultaneous OPEN |
| Later manual runs never overwrite existing state | TABLE STAKES | MEDIUM | One conditional branch, but easy to get wrong (must distinguish "manual configuration run" from "first bootstrap run" reliably) |
| Native import questions (`WFWorkflowImportQuestions`): descent profile, voice, AI toggle (Sentient) | TABLE STAKES | LOW | Native Shortcuts import-question mechanism; free-text/menu, no custom UI needed |
| Control Room proforma pre-fill ("MY PHONE, ON PURPOSE") | TABLE STAKES | MEDIUM | Create Note with structured Markdown-like headings via `Create Note`; must be legible and editable afterward |
| `Sync My Profile` — extract proforma section from Note into JSON | TABLE STAKES | MEDIUM–HIGH | Requires finding/parsing a bounded section of Note text without parsing the whole Note; text-extraction robustness against user edits is the real risk |

### 2. State Engine

| Feature | Classification | Complexity | Notes |
|---|---|---|---|
| Behavioural day = date − 4h | TABLE STAKES | LOW–MEDIUM | Standard date-arithmetic action, formatted to a date-key string; low risk once verified |
| Heat (decay + increment + rapid-return + contract-fidelity terms, floor 0, cap 30) | TABLE STAKES | HIGH | Five distinct arithmetic branches feeding one number, each needing its own conditional in the plist; getting cap/floor wrong silently breaks every downstream Circle mapping |
| Gravity (`floor(opens_today/6)`, cap 5) | TABLE STAKES | LOW | Single formula; the easiest state-engine primitive |
| Pressure = Heat + Gravity | TABLE STAKES | LOW | Trivial once Heat/Gravity exist |
| Pressure → Circle mapping via per-profile threshold table | TABLE STAKES | MEDIUM | Three profile tables × nine thresholds; a dictionary/lookup pattern, must be re-evaluated on every OPEN |
| **Session-ID race-proof reconciliation (OPEN debounce, CLOSE reload-and-compare-then-commit)** | TABLE STAKES | **HIGH** | The single hardest piece of the whole build. Requires: generate session ID on OPEN → persist → on CLOSE, reload state and compare session ID before committing → if a newer OPEN owns state, abandon commit. Getting this wrong is the primary corruption vector (§20, §30 "state races") |
| Rolling-window JSON persistence (bounded arrays + aggregates) | TABLE STAKES | MEDIUM | Requires trimming logic on every append (drop oldest of ~20 sessions/~10 contracts), not just append |
| Corrupt/missing JSON self-heal | TABLE STAKES | MEDIUM–HIGH | Needs a parse-validate-else-rebuild branch on every load, not just at bootstrap |

### 3. Circles & Primitives

| Feature | Classification | Complexity | Notes |
|---|---|---|---|
| A — The Knock (small interruption/notice) | TABLE STAKES | LOW | Alert/notification with 1–2 facts |
| B — Ash (grayscale) | DIFFERENTIATOR | MEDIUM–HIGH | Depends on verified Color Filters capture/restore; must be skippable if restore can't be guaranteed (§21) |
| C — Silence (mute media audio) | DIFFERENTIATOR | MEDIUM–HIGH | Same capture/restore risk as Ash, for volume; must never raise volume |
| D — Confession (intention contract) | TABLE STAKES | MEDIUM | Ask for Input (free text) + Choose from Menu (duration incl. custom) — see Contracts category for the fidelity math this feeds |
| E — Dimming (brightness) | DIFFERENTIATOR | MEDIUM–HIGH | Safety-critical: must capture current brightness, never set to zero, skip if unreadable |
| F — Exile (redirect via an Exit, no permission prompt) | TABLE STAKES | MEDIUM | Invokes one of the six Exits; complexity lives in the Exit itself |
| G — The Mirror (behavioural reflection) | Dumb: DIFFERENTIATOR; Sentient: DIFFERENTIATOR | Dumb MEDIUM (template selection gated on available facts) / Sentient HIGH (model call, parse, fallback) | Dumb version is table-stakes-adjacent (≥30 templates required by spec) but classified as differentiator because it's the product's distinguishing "notices patterns" feature |
| H — The Voice (Mirror spoken once) | DIFFERENTIATOR | MEDIUM | `Speak Text` action gated on voice-enabled setting; must never repeat within one run |
| I — Ice (deterministic cooldown, hard stop) | TABLE STAKES | HIGH | Safety-critical: fixed per-profile duration, blocked attempts must not inflate Heat, must always resolve to a route out — no model involvement permitted at any point |
| Three switchable sequences (Classic/Black Mirror/Ambient) | DIFFERENTIATOR | MEDIUM | Reorders which primitive fires at which Circle; needs a per-sequence lookup table, not new primitive logic |

### 4. Contracts

| Feature | Classification | Complexity | Notes |
|---|---|---|---|
| Free-text intention capture | TABLE STAKES | LOW | `Ask for Input` — trivial |
| Duration selection (2/5/10/15/custom) | TABLE STAKES | LOW | `Choose from Menu` + custom-number fallback |
| Deliberate leisure accepted as a valid contract (no filtering/judgment logic) | TABLE STAKES (philosophy encoded as an *absence* of gatekeeping logic) | LOW | The differentiator is the policy decision, not new code — simplest possible implementation is "don't validate content" |
| Contract fidelity computation (actual/intended, overrun flag) | TABLE STAKES | MEDIUM | Requires CLOSE handler's duration measurement (dependency) plus simple division/threshold |
| Contract history rolling window (last ~10) | TABLE STAKES | MEDIUM | Same trim-on-append pattern as session history |
| Contract outcome feeds future Heat | TABLE STAKES | MEDIUM | Cross-cutting: Heat's "previous contract respected/overrun" term reads this on the next OPEN |

### 5. Exits

| Feature | Classification | Complexity | Notes |
|---|---|---|---|
| Capture (Notes/Voice Memos/Camera) | TABLE STAKES | LOW | Open one of a small set of user-preferred apps |
| Coordinate (Reminders/Calendar/Notes tasks) | TABLE STAKES | LOW | Same pattern as Capture |
| Create (user-defined target app) | TABLE STAKES | LOW | Open App by user-configured identifier |
| Connect (Messages/Phone/FaceTime/Contacts, optional prompt) | TABLE STAKES | LOW–MEDIUM | Slightly higher because it should stay optional and never auto-call anyone |
| Consult (Dumb: menu of Web/Maps/Notes/Reminders/Calendar; Sentient: intent classification) | TABLE STAKES | MEDIUM (Dumb) / HIGH (Sentient classification layer) | Dumb version is a `Choose from Menu` + URL-encoded search per branch; this is the most structurally complex of the six exits even in Dumb form |
| Close (Home/Lock, optional pre-selected audio) | TABLE STAKES | LOW | Simplest exit; the philosophically important one ("no phone is the next action") |
| Exit outcome recording (all six invokable, all outcomes recorded) | TABLE STAKES | MEDIUM | Every exit must write the same outcome shape to JSON regardless of which was chosen |

### 6. Exit Learning

| Feature | Classification | Complexity | Notes |
|---|---|---|---|
| Observation capture (exit, timestamp, app, Circle, Heat/Pressure, time-of-day, time-to-next-OPEN) | TABLE STAKES | HIGH | Time-to-next-OPEN can only be computed retroactively on the *next* OPEN of a tracked app, requiring the previous exit event to still be addressable in state |
| Explore phase (uniform rotation across enabled, non-disabled exits) | TABLE STAKES | MEDIUM | Simple rotation/random-pick logic, gated on the user's enabled-exits config |
| **Exploit phase (epsilon-greedy on per-exit reward aggregates)** | DIFFERENTIATOR | **HIGH** | A genuine local bandit algorithm authored entirely in plist arithmetic: maintain per-exit aggregate reward, weighted/probabilistic selection with an epsilon parameter — this is the most novel piece of logic in the entire product and the least like "normal Shortcuts building" |
| Contextual learning (time-of-day/weekday/app/Circle conditioning) | DEFERRED (explicit future refinement) | — | Spec explicitly states this comes only "after basic exit learning is proven stable" (§9.4) — not v1 scope |

### 7. Control Room / Configuration

| Feature | Classification | Complexity | Notes |
|---|---|---|---|
| Control Room Note structure (READ THIS FIRST / proforma / current settings / current state / ledger / value+support placeholders) | TABLE STAKES | MEDIUM–HIGH | Multi-section Note authored at bootstrap; "current state"/"ledger" sections must be updatable without destroying the human-edited proforma section |
| Manual menu: Status, Open Control Room, Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today, Emergency Restore | TABLE STAKES | MEDIUM | `Choose from Menu` with 9 branches, each a small independent action against the same JSON |
| Sentient-only additions: Toggle On-Device AI, Test Model | TABLE STAKES (Sentient fork only) | LOW–MEDIUM | Two more menu branches; "Test Model" needs a minimal round-trip call to `Use Model` |
| Readable event ledger (meaningful entries only, not every calculation) | TABLE STAKES | MEDIUM | Requires a curation rule (what counts as "meaningful") to avoid the Notes-growth failure mode (§30) |

### 8. Safety & Restoration

| Feature | Classification | Complexity | Notes |
|---|---|---|---|
| Brightness safety (never zero, only change if restorable, skip otherwise) | TABLE STAKES | HIGH | Must capture-before-change and verify restore capability at runtime, not assume it |
| Volume safety (never raise, restore or skip) | TABLE STAKES | HIGH | Same capture/restore risk profile as brightness |
| Grayscale/Color Filters safety (don't override a pre-existing user configuration) | TABLE STAKES | HIGH | Requires detecting whether the user already has Color Filters configured for accessibility reasons before touching it |
| Emergency Restore (clears cooldown, active session, recoverable brightness/volume/colour) | TABLE STAKES | MEDIUM–HIGH | One consolidated action that must know how to undo everything the environmental primitives might have changed |
| CLOSE-time restoration of any PROSOCHĒ-changed settings | TABLE STAKES | HIGH | Tied directly to the race-proof CLOSE handler — restoration must happen on the CLOSE that actually owns the session |
| Circle IX Ice safe route out (blocked attempts don't inflate Heat, remaining cooldown shown, Heat relief on expiry) | TABLE STAKES | HIGH | The one place where a bug becomes a genuine harm (a user "trapped" by their own tool), so this gets the most scrutiny of any single feature |
| Corrupt/missing JSON + deleted Note recovery | TABLE STAKES | MEDIUM–HIGH | Must not crash the Shortcut; must rebuild a minimal safe state rather than fail silently mid-Circle |

### 9. Sentient AI Layer (Sentient fork only)

| Feature | Classification | Complexity | Notes |
|---|---|---|---|
| On-Device `Use Model` integration + capability check | DIFFERENTIATOR | HIGH | Must verify the action's actual identifier/parameter shape on-device before relying on it (§31 capability audit); hardware-gated to iPhone 15 Pro+ |
| Structured `ALLOW`/`CHALLENGE`/`DENY` output, parse validation, deterministic fallback | DIFFERENTIATOR | HIGH | Generative output can be malformed; every call site needs a parse-then-validate-then-fallback pattern, not a happy-path assumption |
| Contract auditor prompt (specificity/boundedness/consistency), max one challenge round | DIFFERENTIATOR | MEDIUM–HIGH | Prompt engineering plus a hard cap enforced in plist logic (never let the model loop into repeated interrogation) |
| Per-circle AI involvement tiering (deterministic I, optional-lightweight II, tone-only III, classify+question IV, observation V, exit-classify-advisory VI, full auditor VII, full+voice VIII, deterministic IX) | DIFFERENTIATOR | HIGH | Nine distinct conditional branches of "how much does the model do here," each needing its own fallback |
| Longitudinal memory reflections (median durations, best/weakest exit by time of day, deliberate-leisure overrun trend) | DIFFERENTIATOR | HIGH | Requires computing rolling-window aggregates and packing them into a compact context block, not raw history |
| Exit classification assist (Circle VI) — advisory only, bandit still governs routing | DIFFERENTIATOR | MEDIUM | Model output is *read*, not authoritative — the epsilon-greedy engine remains in control |
| CLOSE-time precompute/cache of next Mirror | DEFERRED (explicitly conditional: "only if Shortcuts Playground testing shows it is reliable," §14.5) | HIGH | Named optimization, not a required v1 feature |
| System prompt guardrails (no addiction/dopamine/shame language, no diagnosis, behavioural facts only) | TABLE STAKES (for Sentient's honesty claim) | LOW–MEDIUM | Prompt text and copy discipline, not plist complexity — but load-bearing for the "not a lie detector" promise |

### 10. Logging & Telemetry

| Feature | Classification | Complexity | Notes |
|---|---|---|---|
| Core local metrics (opens, rapid returns, session duration, contract overrun, Circle distribution, redirects, exit selected, time-to-return, daily Heat maxima, resets, profile changes) | TABLE STAKES | MEDIUM | Mostly a byproduct of state-engine and exit-learning writes; the work is in *aggregating* consistently, not new capture |
| Primary metric: rapid-return rate | TABLE STAKES | LOW | Derived percentage from already-tracked data |
| Secondary metric: contract fidelity (medians, not means) | TABLE STAKES | LOW–MEDIUM | Derived from contract history; must compute medians, which is slightly more work than a running mean in plist logic |
| Disable-rate signal (friend-testing protocol) | TABLE STAKES conceptually, but a **testing protocol**, not a shippable feature | — | Ask directly in manual testing; no code artifact required for v1 |
| "Life Returned" / Estimated Attention Reclaimed quantification | ANTI-FEATURE (deferred) | — | Explicitly parked pending honest baseline design (§24) |
| Pay-after-value support prompts | ANTI-FEATURE (deferred) | — | Explicitly parked (§25) |
| Screen Time telemetry (`Get App & Website Data`) as core dependency | ANTI-FEATURE (deferred) | — | Research/measurement-only, later phase, action schema unverified (§24) |

### 11. Distribution

| Feature | Classification | Complexity | Notes |
|---|---|---|---|
| Two signed `.shortcut` files (Dumb + Sentient) | TABLE STAKES | MEDIUM | Shortcuts Playground build/sign pipeline; Sentient is a fork of the identical Dumb engine, not a rewrite |
| Unsigned XML source retained for both | TABLE STAKES | LOW | Byproduct of the build pipeline, kept for open-source inspectability |
| Build notes documenting every unverified action/deviation/fallback | TABLE STAKES | LOW | Documentation discipline, not plist logic |
| Validator pass for both forks | TABLE STAKES | MEDIUM | Shortcuts Playground validator is necessary but explicitly stated as *not sufficient* — manual state-graph reasoning still required |
| Open-source repo docs (README, privacy explanation, architecture notes, prompts, contribution guide, changelog) | TABLE STAKES (for the "honest open source" claim) | LOW | Docs, not code — but load-bearing for the forkability promise |

---

## Feature Dependencies

```
Bootstrap (state.json + Control Room Note exist, idempotent)
    └──requires──> nothing (first thing built)

State Engine core (behavioural day, Heat/Gravity/Pressure, JSON schema, session IDs)
    └──requires──> Bootstrap

Profile threshold tables (Paradise/Limbo/Inferno)
    └──requires──> State Engine core

Circle selection (Pressure → Circle via active sequence)
    └──requires──> Profile threshold tables

Nine Primitives (Knock, Ash, Silence, Confession, Dimming, Exile, Mirror, Voice, Ice)
    └──requires──> Circle selection
    Confession
        └──requires──> nothing extra (just Ask for Input + duration menu)
        └──feeds──> Contracts
    Exile
        └──requires──> Exits (at least one implemented)
    Ash / Silence / Dimming
        └──requires──> Safety & Restoration groundwork (capture-before-change pattern)
    Ice (Circle IX)
        └──requires──> Circle selection + Safety & Restoration (must guarantee a route out)

CLOSE handler (race-proof session duration measurement)
    └──requires──> State Engine core (session IDs)

Contract fidelity (actual vs intended duration)
    └──requires──> Confession primitive (intended duration exists)
    └──requires──> CLOSE handler (actual duration exists)
    └──feeds──> Heat's contract-fidelity term (next OPEN)
    └──feeds──> Logging & Telemetry (contract fidelity metric)

Six Exits (Capture/Coordinate/Create/Connect/Consult/Close)
    └──requires──> nothing beyond basic action wiring
    └──feeds──> Exit Learning (needs exits to exist before it can record outcomes)

Exit outcome recording (time-to-next-tracked-OPEN)
    └──requires──> Six Exits + OPEN handler (to detect "next tracked OPEN")

Exit Learning — explore phase
    └──requires──> Exit outcome recording (a few samples) + Control Room enabled-exits config

Exit Learning — exploit phase (epsilon-greedy)
    └──requires──> Exit Learning — explore phase (needs accumulated per-exit aggregates)

Control Room manual menu (Change Profile/Sequence, Sync Profile, Toggle Voice, etc.)
    └──requires──> Bootstrap + State Engine core (has state to mutate)

Safety & Restoration (Emergency Restore, per-primitive capture/restore, CLOSE-time restore)
    └──requires──> whichever environmental Primitives (Ash/Silence/Dimming) are implemented
    └──requires──> CLOSE handler (restoration commits on the CLOSE that owns the session)

Logging & Telemetry (ledger, rolling-window aggregates, rapid-return rate, contract fidelity)
    └──requires──> State Engine core + Contract fidelity + Exit outcome recording all writing to JSON

Sentient AI layer (Use Model, ALLOW/CHALLENGE/DENY, contract auditor, longitudinal memory, exit-classify assist)
    └──requires──> the ENTIRE Dumb deterministic engine stable and unmodified (explicit build-order rule, §31)
    └──requires──> Contract fidelity + Exit-learning aggregates + Logging (Sentient reads these as context — it does not compute them)
    └──must NOT alter──> State Engine core, Circle selection, Circle IX/Ice

Distribution (signing, validator, both forks)
    └──requires──> Dumb fork fully working
    └──requires──> Sentient fork fully working (built as a layer on top, never altering the shared engine)
```

### Dependency Notes

- **State Engine is the single load-bearing dependency for almost everything.** No Circle can be selected, no primitive can fire, no contract can be evaluated, and no exit can be learned from until Heat/Gravity/Pressure and race-proof session IDs exist and are trustworthy. This is why it must be built and stabilized before anything else — including before Dumb's own Mirror engine or exits are polished.
- **CLOSE (real session duration) must exist before Contract fidelity, which must exist before Heat can use contract outcomes, which must exist before Exit Learning has a meaningful reward signal that reflects actual behaviour** (this is the chain given in the task brief, and it holds precisely: Confession → CLOSE → Contract fidelity → Heat's contract term / Exit Learning's outcome signal).
- **Exit outcomes must be recorded before explore/exploit can learn**, and explore must run long enough to populate per-exit aggregates before exploit is meaningful — exploit is not a separate build task from explore, it's explore's data becoming useful after volume.
- **Safety & Restoration is not a late "polish" phase** — it is a prerequisite for shipping any environmental primitive (Ash/Silence/Dimming) at all. The canonical strategy makes this explicit: skip the primitive entirely if its restore path cannot be verified (§21). Treat Safety as gating, not as cleanup.
- **Sentient must not be built until Dumb is stable**, and building it must never require touching the deterministic engine — this is a hard architectural rule (§13, §31), not just a sequencing preference. It exists specifically so Dumb remains the scientific control condition for A/B comparison against Sentient.
- **Circle IX (Ice) sits at the intersection of State Engine, Circle selection, and Safety** — it cannot be built as "just another primitive." It requires the Pressure/Circle mapping to be trustworthy, the safety-restoration pattern to already exist (to guarantee the eventual exit), and it is the one place with zero tolerance for the "90% correct" risk the Shortcuts Playground itself warns about (§5.3).

---

## Benchmark: Comparable Products' Core Loops

| Product | Core loop | Mechanism strength (per available evidence) | PROSOCHĒ analogue | Genuinely novel vs this competitor? |
|---|---|---|---|---|
| **one sec** | Friction screen + explicit dismiss option before opening a target app | Field study (280 participants, 6 weeks): ~36% of attempts dismissed after intervention; ~37% reduction in attempts over 6 weeks; ~57% combined reduction in actual openings by week 6. Preregistered 500-participant decomposition found **the option to dismiss the consumption attempt was the single strongest component — stronger than the time-delay friction, and stronger than the deliberation message itself** | Direct analogue to Exile (redirect via Exit, no permission prompt) and to Ice's mandatory "always a route out" rule; also the core justification for why all six Exits exist at all | Yes, on the escalation dimension: one sec has one friction stage. PROSOCHĒ has nine, driven by adaptive Pressure. But PROSOCHĒ's single most important validated design principle *is* one sec's finding — easy exit beats clever copy. This should discipline the Mirror/Voice primitives: they must never become the mechanism the product relies on. |
| **Wellspent** | Full-screen reminder at a user's self-defined session time limit, offering quit-or-continue | RCT (70 users, 3 weeks): no significant reduction on the primary problematic-use outcome or self-efficacy, but ~29.35 min/day lower screen time on the target app and a significant reduction in *perceived* problematic use | Direct analogue to Confession's duration boundary + the Heat term for contract overrun | Partially. Wellspent is single-instrument (one reminder at one self-set limit). PROSOCHĒ layers self-defined boundaries inside a multi-stage escalating system with a persistent behavioural memory (Heat/Gravity) that Wellspent does not have. |
| **ScreenZen** | Countdown delay before opening a blocked app, optional intention prompt ("what are you seeking?"), replacement-app suggestions, daily limits/cooldowns/scheduled blocks | Marketing/reviews report ~40% turn-back rate at a 15-second delay — directionally consistent with one sec's friction findings, though not from a peer-reviewed source | The closest existing commercial analogue to PROSOCHĒ's Confession + Exit pattern; "replacement apps" maps to the exit taxonomy | Partially. ScreenZen has a static replacement-app list; it does not learn per-user which replacement actually works (no bandit/exploit phase), has no Pressure/Heat/Gravity escalation, and treats leisure use uniformly as something to delay rather than distinguishing deliberate from automatic. |
| **Opal** | Scheduled/timed Focus Sessions (Screen Time API), Deep Focus mode that prevents cancellation, App Limits, Smart Schedules, analytics dashboard | Marketing-stated; relies on Apple's actual Screen Time blocking APIs, subscription-based | Opal is the clearest example of the category PROSOCHĒ explicitly rejects: it uses real blocking APIs and a companion-app architecture, and its friction is schedule/session-based rather than behaviourally adaptive | Yes, structurally. Opal's friction level does not change based on how the user is actually behaving in the moment — a scheduled Focus Session is identical on a calm day and a compulsive-clustering day. PROSOCHĒ's entire premise (Heat/Gravity-driven Pressure) has no equivalent in Opal. |
| **Brick** | NFC hardware puck; tap to lock apps, tap again to unlock; "Strict Mode" prevents deletion/disabling during a session | Physical friction is a genuinely different mechanism class — real-world friction most digital tools cannot replicate; $59 hardware, no subscription | The analogue PROSOCHĒ explicitly ruled out for v1 (§4 "NFC") | Yes, by design choice rather than technical inability. Brick's "Strict Mode" (can't be disabled mid-session) is the direct opposite of PROSOCHĒ's non-negotiable honesty constraint (never claim tamper-proof, user can always disable the Personal Automation). This is a deliberate positioning difference, not a missing feature. |
| **Apple Screen Time (native)** | App Limits + Downtime, with a one-tap "Ignore Limit for 15 minutes" bypass | Apple's own baseline: useful for measurement and simple limits; friction is a single dialog, trivially and repeatedly dismissible; no adaptivity, no behavioural memory | The explicit "why this product exists" baseline (§1) — PROSOCHĒ starts from the premise that Screen Time's friction is too easy to dismiss and not adaptive to behaviour | Yes, comprehensively. No adaptive Pressure, no exit taxonomy, no contract fidelity, no learning, no reflective Mirror. Screen Time is the un-adaptive control condition PROSOCHĒ is positioned against. |
| **Forest** | Gamified commitment device: plant a virtual tree that "dies" if you leave the app during a session; streaks, rewards, tree collection | Popular but evidence is mostly anecdotal/engagement-metric based, not RCT-grade in the sources reviewed here | No direct PROSOCHĒ analogue — and deliberately so | Yes, by explicit design rejection. PROSOCHĒ's own "bad" example copy list rejects motivational/gamified framing ("Believe in yourself!"); there are no points, streaks, or virtual rewards anywhere in the canonical spec. The Mirror primitive's whole design principle — "accurate memory, not hostility or cheerleading" — is a direct alternative to Forest's gamification mechanic. |

### What is genuinely novel about PROSOCHĒ (not just recombination)

1. **Dual-signal (Heat + Gravity) adaptive Pressure driving nine graduated Circles.** No competitor reviewed has multi-stage escalation keyed to live behavioural clustering rather than a fixed schedule or single threshold.
2. **A local epsilon-greedy bandit learning which of six named exits actually breaks the loop, per user.** ScreenZen's replacement-app list is the closest analogue and is static, not adaptive.
3. **Contract fidelity (intention vs actual, medians) as a first-class metric**, aligned with emerging evidence that the intention-actual gap predicts regret better than duration alone (§6.7) — not surfaced by any competitor reviewed.
4. **Deliberate leisure as a protected, valid contract outcome**, encoded as an absence of judgment logic rather than a moral filter — directly contradicts the implicit design of every competitor reviewed, which treats target-app time uniformly as the thing to reduce.
5. **On-device LLM as a contract auditor, never a lie detector**, with a hard one-challenge cap and a system prompt that explicitly forbids diagnosis/psychological inference — no competitor product has this framing; most AI-assisted digital-wellbeing prototypes (e.g. MindShift, §6.8) are still exploratory and none constrain themselves this way.
6. **A dual JSON+Note architecture that gives the user an inspectable, editable personal manifesto co-located with their behavioural ledger** — no competitor exposes a human-readable, user-owned log of this kind.
7. **A hard, explicit non-tamper-proof honesty constraint** — the positioning opposite of Brick's Strict Mode and the underlying premise of every Screen Time API-based competitor.

---

## Anti-Features (Evidence-Reinforced)

Beyond the strategy's explicit Out of Scope list, the evidence base independently reinforces two behaviours PROSOCHĒ must avoid, because **intervention fatigue and disablement are the dominant failure mode** (§30, §12):

- **Do not let the model's clever sentence become the mechanism.** one sec's decomposition study found the dismiss option, not the deliberation message, drove the strongest effect. If Sentient's Mirror/Voice primitives are treated as the product's core value, the product is optimizing the wrong lever — the choice architecture (Exile/Exits/Ice's guaranteed route out) is the mechanism; the reflective copy is secondary.
- **Do not repeat the same message or treat every target-app open as a violation.** Repetition and blanket judgment are named failure modes that produce either mechanical prompt-dismissal (fatigue) or outright disabling of the automation (the worst possible outcome, since it is a product failure "even if it theoretically blocks more openings," §12).

---

## MVP Definition

### Minimum Honest v1 — PROSOCHĒ Dumb (fully coherent, independently shippable)

Everything below is deterministic and does not depend on Apple Intelligence hardware. This is not "Sentient without the AI" — it is the baseline product and control condition (§13).

- [ ] Bootstrap: idempotent `state.json` + Control Room Note creation
- [ ] Native import questions (profile, voice — no AI toggle)
- [ ] State Engine: behavioural day, Heat, Gravity, Pressure, three profiles, race-proof session IDs
- [ ] OPEN handler (full 18-step sequence, §19) and CLOSE handler (full 17-step sequence, §20)
- [ ] Nine primitives in Dumb form (Mirror = ≥30 fact-gated templates; Voice = Dumb Mirror spoken)
- [ ] Three switchable sequences (Classic/Black Mirror/Ambient)
- [ ] Intention contracts: free text + duration incl. custom; deliberate leisure accepted without judgment
- [ ] Six exits including Dumb's menu-based Consult
- [ ] Exit outcome recording + explore/exploit epsilon-greedy (this is arithmetic, not AI — fully in-scope for Dumb)
- [ ] Circle IX Ice: deterministic cooldown, no Heat inflation on blocked attempts, always a route out
- [ ] Environmental safety floors + Emergency Restore
- [ ] Control Room manual menu (all items except Toggle On-Device AI / Test Model)
- [ ] Corrupt-state and deleted-Note recovery
- [ ] Rolling-window logging + readable ledger + rapid-return rate + contract fidelity
- [ ] Signed `.shortcut` + unsigned XML + build notes, validator pass

### Sentient-only additions (layered on top of a stable Dumb engine — never altering it)

- [ ] On-Device `Use Model` integration with verified capability check
- [ ] Structured `ALLOW`/`CHALLENGE`/`DENY` verdicts, parse validation, deterministic fallback, max one challenge
- [ ] Contract auditor prompt (specificity/boundedness/consistency) — never a lie detector
- [ ] Per-circle AI involvement tiering (deterministic I → escalating II–VIII → deterministic IX)
- [ ] Longitudinal memory reflections fed as compact context (medians, per-exit performance, deliberate-leisure trend)
- [ ] Exit classification assist at Circle VI (advisory only — the bandit still routes)
- [ ] Sentient system prompt guardrails (no addiction/dopamine/shame/diagnosis language)
- [ ] Toggle On-Device AI / Test Model Control Room menu items

### Explicitly deferred (v1.x or later, regardless of fork)

- [ ] Contextual exit learning (time-of-day/weekday/app/Circle conditioning) — spec-stated future refinement (§9.4)
- [ ] CLOSE-time precompute/cache of next Sentient Mirror — conditional on Playground reliability testing (§14.5)
- [ ] Screen Time telemetry (`Get App & Website Data`) as a measurement layer — schema/granularity unverified
- [ ] "Life Returned" / Estimated Attention Reclaimed value quantification — needs rigorous honest baseline design
- [ ] Pay-after-value support prompts — needs the above first, and must never appear mid-intervention
- [ ] Community science / anonymized opt-in export — Phase F, only if there is interest
- [ ] NFC/physical commitment device, Focus modes, stronger Screen Time enforcement, companion app — Phases D/E, explicitly out of scope for the current build (§4, §34)

---

## Feature Prioritization Matrix

| Feature area | User Value | Implementation Cost | Priority |
|---|---|---|---|
| State Engine (Heat/Gravity/Pressure, session-ID race-proofing) | HIGH | HIGH | P1 |
| CLOSE handler + Contract fidelity | HIGH | HIGH | P1 |
| Circle IX Ice + Safety/Restoration | HIGH | HIGH | P1 |
| Nine primitives (Dumb) | HIGH | MEDIUM–HIGH | P1 |
| Six exits + outcome recording | HIGH | MEDIUM | P1 |
| Control Room bootstrap + manual menu | HIGH | MEDIUM | P1 |
| Explore/exploit exit learning | MEDIUM–HIGH | HIGH | P1 (spec-required for v1) |
| Three sequences (Classic/Black Mirror/Ambient) | MEDIUM | MEDIUM | P2 |
| Dumb Mirror engine (≥30 templates) | MEDIUM–HIGH | MEDIUM | P1 (spec-required) |
| Sentient: Use Model + ALLOW/CHALLENGE/DENY + contract auditor | HIGH (defines the fork) | HIGH | P1 for Sentient fork, built only after Dumb is stable |
| Sentient longitudinal memory | HIGH | HIGH | P2 (can ship after basic Sentient auditor works) |
| Contextual exit learning | MEDIUM | MEDIUM–HIGH | P3 (explicitly deferred) |
| Screen Time telemetry measurement | LOW–MEDIUM | HIGH (unverified action) | P3 |
| Life Returned / pay-after-value | MEDIUM (future) | MEDIUM | P3 |
| NFC / Focus / companion app / stronger enforcement | LOW (v1) | HIGH | Out of scope |

---

## Sources

- `PROSOCHE_Nine_Circles_Canonical_Strategy.md` (canonical, this repo) — all feature specification, all classification traces, all evidence citations (Lukoff et al. 2018; Keller et al. RCT; Wellspent RCT 2026; one sec field study + preregistered decomposition; grayscale field experiments; regretful-sessions preprint 2026; MindShift)
- `.planning/PROJECT.md` (this repo) — Active/Out-of-Scope requirement framing, constraints, key decisions
- [Opal: Screen Time Control — App Store](https://apps.apple.com/us/app/opal-screen-time-control/id1497465230)
- [Opal — The #1 Screen Time App](https://www.opal.so/)
- [Opal FAQ — What is Opal and how does it work?](https://opalapp.com/help/what-is-opal)
- [Brick — Take Back Control of Your Screen Time](https://getbrick.com/)
- [Brick Phone Blocker Review 2026 — CyberNews](https://cybernews.com/reviews/brick-phone-blocker-review/)
- [I Used the Brick Phone Blocker for a Year](https://whatifididnt.com/blog/brick-phone-app/)
- [ScreenZen — App Store](https://apps.apple.com/us/app/screenzen-screen-time-control/id1541027222)
- [ScreenZen App: How It Blocks Apps, Sites, and Scrolls — Nibble Blog](https://nibble-app.com/blog/screenzen)
- [ScreenZen Review 2026 — unhookd](https://unhookd.app/blog/screenzen-worth-it-review)

---
*Feature research for: PROSOCHĒ — Nine Circles (adaptive-friction attention intervention, native iOS Shortcut)*
*Researched: 2026-08-13*
