# PROSOCHĒ — Nine Circles

## What This Is

PROSOCHĒ is a free iPhone Shortcut — source-available, free for any noncommercial purpose (PolyForm Noncommercial 1.0.0, BD-12) — that restores the missing interval between the impulse to open a habit-forming app and the act of consuming it. It watches user-selected apps through native iOS Personal Automations (App Is Opened / Is Closed) and runs the **covenant model** on two axes: behavioural **Pressure** (Heat + Gravity) maps to nine Circles grouped into four bands — Silent (0), Ambient (1–3), Ask (4–6), Rescue (7–9) — while a valid **intention contract** covers opens inside its window so that they fire nothing at all. Consciousness is rewarded with silence; escalation is proportionate to behavioural evidence and is always an escalation in salience, never frequency. It ships as two forks from one engine: **Core** (fully deterministic, broad iOS 26 support) and **Aware** (the same deterministic engine plus Apple's On-Device Intelligence as an attention mirror and contract auditor inside a deterministic envelope).

It is not a screen-time blocker and not a parental-control system. It is an adaptive friction system for self-directed behaviour change, built on Epictetus' discipline of attention (prosochē) and Thaler's choice architecture.

## Core Value

**When use is intentional, PROSOCHĒ is invisible. When intention disappears, it interrupts exactly strongly enough to restore it — and an honest declaration buys back the silence.**

If everything else fails, the OPEN → Heat/Gravity/Pressure → Circle → coverage-check → intervention loop must work reliably on a real iPhone without corrupting state.

## Requirements

### Validated

(None yet — ship to validate)

### Active

**Delivered foundation (built and carried forward; device proof tracked by Phase 22):**

- [x] Deterministic behavioural state engine: behavioural day (date − 4h), Heat (decay/increment/rapid-return/contract-fidelity, floor 0, cap 30), Gravity (`floor(opens_today/6)`, cap 5), Pressure (heat + gravity), Circle 0 silent band
- [x] Single-shortcut invocation routing (manual / `OPEN` / `CLOSE`), first-run bootstrap, self-healing state and Note recovery
- [x] `PROSOCHĒ` Note with READ THIS FIRST, both automation walkthroughs, safety warnings, Color Filters disclosure + kill switch, and the editable `MY PHONE, ON PURPOSE` proforma
- [x] Race-proof CLOSE pipeline with session ownership, duration measurement, and environmental restore
- [x] Nine of the eleven-primitive roster built (all but Redirect — Phase 18 — and the parked Blackout), including real Color Filters grayscale, the Voice primitive, and capture-persist-restore for brightness/volume
- [x] Six exits (Capture, Coordinate, Create, Connect, Consult, Close) with deterministic epsilon-greedy exit learning
- [x] Aware fork as one additive gated insertion with the device-evidenced `Apple Intelligence on Device` literal
- [x] Build discipline: two-gate validation via `gate_a_residue_check.py`, 14 structural checkers, nine parameter-defect axes, AEA1 decrypt verification

**The covenant conversion (canonical strategy v2; Phases 17–20):**

- [ ] Covenant substrate: `active_contract` window state, coverage gate on the OPEN path, invalidation rules (expiry / open-count / rapid-return), coverage ceiling at Circle 7, `recent_contracts` actually written
- [ ] Verdicts in both forks: ALLOW/CHALLENGE/DENY inside a deterministic per-Circle envelope; Core's verdict is recorded-fact arithmetic; DENY only at Circle 6 and only ever a redirect
- [ ] Bands and surfaces: the universal pre-menu retired; Band B fires silently; one interactive surface per OPEN maximum; every interactive surface carries a one-tap leave route; Panic Escape re-expressed as that in-surface affordance
- [ ] Slot table v2: Mirror at Circle 5, Redirect built at Circle 6, Eject at 7, band-invariant sequences with Frozen pinned at 9; Dim split (soft Dim in Ambient; Blackout parked)
- [ ] Personalized descent: plain-language severity question → profile, modality question → sequence; band-entry keys reserved in Config
- [ ] Anti-ritualisation variability: deterministic counter-based spot check (ships off; Phase 23 researches and tunes it); never in Frozen, safety, environmental, or coverage paths
- [ ] Covenant metrics: contract fidelity co-primary with rapid-return rate; covered-open share; surfaces per day

**Distribution (standing):**

- [ ] Two signed, importable `.shortcut` files (`PROSOCHĒ — Nine Circles — Core` / `— Aware`) implementing canon v2, with unsigned XML retained
- [ ] Both forks import onto a real iPhone and complete a first manual run (DIST-03, still the standing device blocker)
- [ ] Build notes documenting every unverified iOS action, deviation, and fallback

### Out of Scope

- Focus modes — explored and deliberately removed; possible later environmental layer
- NFC / physical commitment tokens — future extension (SEED-001 holds the Frozen physical-unlock concept)
- Screen Time blocking APIs (FamilyControls / ManagedSettings / DeviceActivity) and any companion app — behavioural intervention, not secure access control
- CSV or any second machine store — one JSON, one Note
- ChatGPT / third-party extension models, arbitrary web APIs, analytics — different trust boundary (PCC is an authorised fallback only, BD-04-R)
- Remote A/B infrastructure — sequences and knobs switch locally
- **Mid-session timers** — Shortcuts offers no installable timer trigger; boundary enforcement happens at the next OPEN/CLOSE event, and no design may pretend otherwise
- **True randomness in strong interventions** — variability is deterministic (counter-modulo); nothing nondeterministic touches Frozen, cooldowns, safety, environmental changes, or coverage arithmetic; downward "punishment lottery" Circle jumps are rejected by design
- Tamper-proofing claims — the user can always disable the automation, and the product says so
- Lie detection, addiction diagnosis, therapy-intake onboarding

## Context

- **Canonical source:** `PROSOCHE_Nine_Circles_Canonical_Strategy.md` **v2.0 (2026-08-19, the covenant model)** — a ground-up rewrite that supersedes v1.0 in full. v1.0 is preserved at git tag `pre-covenant-overhaul`; canon Appendix A maps every v1 §N to its v2 home, so historical citations remain resolvable. Where any earlier idea conflicts with v2, v2 wins; dated decisions in `docs/CAPABILITY-DECISIONS.md` (through BD-12) win until folded in.
- **Build tool:** Shortcuts Playground (`shortcut-builder` / `shortcut-remixer`, `shortcuts-playground` skill). Plist validation is necessary but never sufficient; the nine parameter-defect axes and the evidence-escalation ladder in `.claude/CLAUDE.md` govern.
- **Hard iOS constraints:** a distributed Shortcut cannot install Personal Automations (the Note teaches the user); the Shortcut reacts to an app-open trigger rather than intercepting it; there is no mid-session timer.
- **Evidence base:** Epictetus (*Enchiridion* 1; *Discourses* 4.12 — attention as practice; deferred attention as a forming habit, which is the ritualisation failure mode); Thaler (choice architecture, commitment devices — the bands are a nudge→ask→shove gradient the user opts into); one sec field study (the easy dismissal option is the strongest lever — the choice architecture is the product); Lukoff et al. 2018 (deliberate leisure is valid); Keller et al. RCT (planning and self-efficacy are the active mechanisms); Wellspent RCT (self-defined boundaries, just-in-time); grayscale field experiments (ambient friction works); the 2026 regret preprint (the intention–actual gap is the metric — contract fidelity operationalizes it).
- **Primary metrics:** rapid-return rate and contract fidelity (co-primary); covered-open share and surfaces-per-day as the covenant's own success curve; disable rate as the fatal signal.
- **Dominant failure modes:** disablement (an intervention annoying enough to switch off is a failure whatever it blocked) and ritualisation (a surface dismissed by reflex is practicing inattention through the product itself).
- **Current build state:** the shipped artifacts implement the v1 interaction model until Phases 17–20 land. Five device-session blockers from the 2026-08-18/19 UAT are open (see STATE.md); DIST-03 remains the standing device gate.
- **Distribution:** free for noncommercial use, source-available, forkable, no feature gate, no ads, no data sale, no telemetry leaving the device (PolyForm Noncommercial 1.0.0 going forward; MIT through tag `pre-covenant-overhaul`, not retroactive — BD-12).

## Constraints

- **Platform**: iOS 26.x, native Shortcuts only — no companion app, no private APIs
- **Tech stack**: Shortcuts plist XML built and signed via Shortcuts Playground; one `state.json`; one Apple Note
- **AI**: Apple Intelligence via the iOS 26 `Use Model` action, Aware fork only. On-Device preferred and pinned with the device-evidenced literal (BD-04-R2); PCC acceptable as fallback; ChatGPT excluded. Never write a guessed `WFLLMModel` value.
- **Privacy**: no behavioural data leaves the device; Aware receives only a compact local context window, never the whole Note; covered opens make no model call
- **Capability**: every iOS action identifier and parameter shape must be verified before use — if it cannot be verified, use the safest fallback, record the deviation, keep the Shortcut runnable. Never fabricate an action because the strategy asks for it.
- **Build provenance**: before running `tools/build_state_engine.py` or `tools/build_sentient.py`, require `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD`; abort the rebuild if it fails.
- **Safety**: no unsafe or startling volume, no accessibility-stranding state, Emergency Restore always available and never gated. Every environmental change is captured **and durably persisted** before it is applied and reliably restored; any setting whose original cannot be captured is left unchanged — capture-and-restore reliability is the safety mechanism (D-01; `safety.brightness_floor` and `safety.dim_target` ship at `0`; authority `docs/CAPABILITY-DECISIONS.md` BD-02). The loop is device-unproven and owned by Phase 22.
- **Determinism**: the model never controls arithmetic, thresholds, timers, coverage, verdict envelopes, Circle IX/Frozen, or any safety decision; all variability is counter-based and deterministic
- **Device split**: Core targets all iOS 26 iPhones; Aware requires Apple Intelligence-capable hardware (iPhone 15 Pro and later); the one-product question is owned by Phase 25

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| **The covenant model (BD-09, 2026-08-19):** contract coverage is a routing axis above the Circle ladder; covered opens fire nothing; four fixed bands; verdicts in both forks | The v1 ladder punished conscious and unconscious use alike, contradicting the product's own stated purpose ("makes your phone wait for an intention"). Silence must be the reward for declared, bounded use | Canon v2; conversion = Phases 17–20 |
| Ground-up doc re-foundation rather than an addendum (user decision 2026-08-19) | Stale v1 fragments in live docs would corrupt future planning; git tag `pre-covenant-overhaul` preserves provenance | This overhaul |
| Boundary is mandatory at the ask | Without an end time there is no window, no expiry, no fidelity — the system could neither go silent nor come back | Canon §7.1 |
| Coverage ceiling at Circle 7; Frozen never covered | A declaration must never outrun the behavioural record; Band D is reached only through behaviour that already invalidated coverage | Canon §7.2 |
| Personalization = severity → profile, modality → sequence (BD-10) | Two people with identical usage deserve different products when they judge it differently; self-defined targets are the evidenced mechanism | Canon §11; Phase 19 |
| Anti-ritualisation variability is deterministic and ships off (BD-11) | Ritualised dismissal is the observed real-world failure of Screen Time prompts; variability resists habituation, but a punishment lottery would break proportionality — so counter-based, Band C jumps only, researched before armed | Canon §13; Phase 23 |
| One JSON for machine state, one Apple Note for human history; no CSV | One machine store, not two | Carried from v1 |
| Core built first and complete; Aware is an additive non-mutating wrap | Core is the baseline product and control condition | Carried; refork tracked by SEED-005 |
| Exits chosen by local epsilon-greedy learning, never by the model | Which exit breaks the loop is an empirical per-user question; the model must not do arithmetic | Carried |
| Deliberate leisure is an explicitly valid contract | Evidence: apparently "meaningless" use can be meaningful; punishing leisure drives disablement | Carried; coverage makes it mechanical |
| Personal Automations are user-created, documented in the Note | Apple does not permit a shared Shortcut to install them; honesty about this is part of the product | Carried |
| Dante names positional; Paradise/Purgatory/Inferno; Core/Aware | BD-06 Decisions 1–3, 5, 6 and BD-06-A1/A4 stand (6 reaffirmed by BD-09); only the slot table (Decision 4) is superseded | Carried |

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
*Last updated: 2026-08-19 — re-founded on canonical strategy v2 (the covenant model); v1 planning state preserved at git tag `pre-covenant-overhaul`*
