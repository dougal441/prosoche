# PROSOCHĒ — Nine Circles
## Canonical Product Strategy, Research Brief, Architecture and Agent Build Specification

**Status:** Canonical strategy for prototype build  
**Date:** 13 August 2026  
**Target:** iOS 26.x  
**Build tool:** Shortcuts Playground  
**Distribution intent:** Free and open source  
**Product forks:** PROSOCHĒ Dumb + PROSOCHĒ Sentient

---

# 0. Executive design brief

PROSOCHĒ is a free, open-source iPhone Shortcut designed to return agency to the user at the exact moment habitual phone use begins.

It is not primarily a screen-time blocker. It is an **adaptive friction system**.

The central product hypothesis is:

> The problem is not that people use phones. The problem is that intention disappears between the impulse to open an app and the act of consuming it.

Modern social apps compress:

**cue → action → consumption**

PROSOCHĒ restores the missing middle:

**cue → awareness → intention → deliberate action**

The Shortcut watches user-selected distracting apps through native iOS Personal Automations. Repeated and clustered app openings increase behavioural **Pressure**, which causes the user to descend through nine progressively stronger “Circles.” Early Circles are almost invisible speed bumps. Later Circles make the phone increasingly uncooperative with automatic behaviour.

The user chooses how aggressively this happens:

- **Paradise** — gentle descent
- **Limbo** — balanced/default
- **Inferno** — rapid descent

The system has two behavioural signals:

- **Heat** — short-term compulsive clustering: rapid reopenings, repeated returns, contract overruns.
- **Gravity** — slower accumulation across the behavioural day.

Together:

**Pressure = Heat + Gravity**

Pressure maps to the current Circle.

The architecture is deliberately self-contained:

1. **One signed `.shortcut`** contains the application logic.
2. **One Apple Note — `PROSOCHĒ — Control Room`** is the human-readable setup guide, personal phone-use manifesto, configuration surface and readable behavioural history.
3. **One small JSON state file** is the fast machine-state store.

There is no CSV. The Note is the human log. JSON is the machine state.

The user experience must remain “self-saucing”:

1. Import shortcut.
2. Answer the few native import questions that Shortcuts can reliably support.
3. Tap PROSOCHĒ once.
4. PROSOCHĒ creates its Control Room Note and JSON state automatically.
5. The Note tells the user exactly how to create the two Personal Automations that Apple does not permit a shared Shortcut to install on their behalf.
6. Once those automations exist, PROSOCHĒ runs itself.

Two forks will be built from the same core:

### PROSOCHĒ Dumb

For iOS 26-compatible iPhones that do not support Apple Intelligence, or for users who choose not to use a model.

It uses deterministic rules, telemetry, scripts, message banks, intention prompts and learned exit routing.

It must be fully useful on its own.

### PROSOCHĒ Sentient

For Apple Intelligence-capable devices, beginning with iPhone 15 Pro / 15 Pro Max and later supported models.

It uses the **On-Device** Apple Intelligence model only. No ChatGPT. No Private Cloud Compute. No external API.

The model acts as an increasingly context-aware “attention mirror”: it sees only locally derived PROSOCHĒ telemetry and the user's own declared values, intentions and recent behavioural contracts.

It does **not** claim to read the user's mind or know what happened inside an app.

The desired feeling is not:

> My phone is policing me.

It is:

> My phone has noticed exactly what I am doing.

---

# 1. The problem

There is a large category of commercial products — blockers, timers, focus apps and physical tokens — that monetize a problem created partly by the attention economy itself.

PROSOCHĒ begins from a different premise.

The user should not need another subscription merely to regain control of their own device.

Apple's native Screen Time is useful for measurement and simple limits, but its friction is easy to dismiss and its design is not adaptive to behaviour. Commercial products such as Opal, Brick and similar tools add stronger enforcement, but the core behavioural mechanisms can be explored using native Shortcuts.

The opportunity is not to reproduce every paid blocker feature.

The opportunity is to ask:

**How far can native iOS go when friction is adaptive, personal, contextual and increasingly difficult to ignore?**

The product should preserve useful smartphone capabilities.

A phone can be:

- a map;
- a camera;
- a notebook;
- a communications device;
- a music player;
- a library;
- a research tool;
- a calendar;
- a creative instrument;
- an accessibility device;
- a way to connect with people.

The design should not confuse “less phone” with “better life.”

The better distinction is:

**deliberate use versus automatic use.**

A ten-minute deliberately chosen session watching ridiculous videos may be entirely compatible with PROSOCHĒ.

Opening the same app six times in fifteen minutes without knowing why is the behaviour PROSOCHĒ is designed to interrupt.

---

# 2. Philosophy

## 2.1 Attention is the scarce resource

The product is fundamentally about attention rather than screen time.

Time is useful as a measurement, but attention determines what a period of time becomes.

The central product language should therefore revolve around:

- attention;
- intention;
- agency;
- choice;
- habit;
- finite time;
- deliberate leisure;
- returning to what matters;
- using the phone as a tool.

Avoid pseudo-neuroscientific marketing about “dopamine detox” or claims that the brain is being chemically depleted by individual app openings.

The mechanism can be described more accurately:

- repeated cues can become habitual;
- low-friction interfaces make automatic behaviour easy;
- small amounts of friction can interrupt a habitual action sequence;
- explicit intention can restore a deliberate choice point;
- repeated successful choices may reshape future behaviour.

## 2.2 Epictetus and prosochē

The philosophical lineage should become part of the future marketing strategy.

Epictetus opens the *Enchiridion* by distinguishing what is “up to us” from what is not. In *Discourses* 4.12, “On Attention,” he treats sustained attention — **prosochē** — as a practice that itself becomes habitual, and warns that inattention can become a habit when repeatedly deferred.

PROSOCHĒ can translate that ancient practice into interface design.

The phone constantly presents impressions.

The user cannot always control what appears, what others post, what notifications exist, what the algorithm rewards, or what external events occur.

The intervention point is the moment before assent and action.

A concise philosophical model for PROSOCHĒ is:

**impression → attention → assent → action → habit**

Modern persuasive interfaces often try to compress this into:

**impression → action**

PROSOCHĒ's purpose is to restore the missing interval.

Potential future product language:

> Your phone should wait for an intention.

> Attention becomes a life by being spent.

> You cannot control everything that asks for your attention. You can practice deciding what receives it.

Do not falsely attribute a modern slogan such as “attention is the only thing you can control” as a direct ancient quotation. The relationship should be described accurately as a modern application of Epictetus' dichotomy of control and practice of attention.

---

# 3. Design influences

PROSOCHĒ deliberately combines several traditions.

## Richard Thaler / behavioural nudges

Small changes to choice architecture can meaningfully alter behaviour without removing choice.

PROSOCHĒ should generally prefer:

- friction;
- defaults;
- changed salience;
- interruption;
- visible consequences;
- deliberate re-entry;

before hard restriction.

## Cal Newport / digital minimalism

Technology should be deliberately selected because it supports a valued life, not passively accepted because it is available.

PROSOCHĒ should therefore ask not only:

> What do you want to use less?

but:

> What is your phone actually for?

and:

> What do you want your reclaimed attention for?

## Atomic Habits / environment and friction

Make unwanted automatic behaviours harder.

Make desired alternatives easier.

The redirect is therefore not merely punishment. It should place a better action one tap away.

## Steve Jobs / computer as tool

The aspirational frame is the smartphone as an instrument that extends human capacity, rather than an environment that continuously captures attention.

## Black Mirror

The “Black Mirror” quality is a deliberate aesthetic principle.

It must not come from hostility, surveillance theatre or fake mind-reading.

It should come from accurate memory.

For example:

> This is your fourth return in seventeen minutes.

is stronger than:

> Stop wasting time.

Likewise:

> The last three sessions you called “quick replies” lasted 8, 11 and 13 minutes.

is stronger than:

> You're lying to yourself.

The system should become uncanny because it notices patterns the user normally fails to notice.

---

# 4. Current product boundaries

This section supersedes earlier ideas.

## In scope now

- One master Shortcut.
- User-selected app-open automation.
- User-selected app-close automation.
- Nine escalating Circles.
- Paradise / Limbo / Inferno profiles.
- Heat, Gravity and Pressure.
- Apple Note Control Room.
- One JSON machine-state file.
- Readable event logging in the Note.
- Intent contracts.
- Replacement / exit pathways.
- Explore/exploit learning to discover which exits work for the user.
- Safe reversible environmental friction where iOS actions allow it.
- On-device Apple Intelligence in the Sentient fork.
- Fully deterministic fallback in the Dumb fork.
- Free/open-source distribution.
- Future-value telemetry stored locally.

## Explicitly out of scope for the current build

### Focus

Focus-based design was explored and deliberately removed from v1.

Focus may be revisited later as an environmental layer, but it is not required for the Nine Circles engine.

### NFC

Physical NFC gating was explored and deliberately removed from v1.

It remains a possible future “physical commitment device” extension.

### Screen Time blocking APIs

The current project does not require a companion iOS application using FamilyControls / ManagedSettings / DeviceActivity.

PROSOCHĒ is a behavioural intervention Shortcut, not a secure parental-control system.

### CSV

Do not create a CSV in addition to JSON.

Human-readable history belongs in the Note.

Machine state belongs in JSON.

### External/cloud AI

Sentient must use Apple's On-Device model.

Do not use:

- ChatGPT;
- Private Cloud Compute;
- arbitrary web APIs;
- analytics services.

### Hard A/B testing infrastructure

The initial product will support multiple intervention sequences so the creator and friends can manually test them.

Do not build a remote experimentation platform.

---

# 5. Technical viability

## 5.1 App-open and app-close events are viable

Apple's Shortcuts App trigger supports:

- **Is Opened** — fires when the user opens or switches to a selected app.
- **Is Closed** — fires when the user closes or switches away from a selected app.

Apple also lists App automations among the Personal Automations that can run automatically rather than requiring confirmation.

This gives PROSOCHĒ the basic event stream:

**OPEN → intervention → CLOSE → session duration**

Important limitation:

A Shortcut is reacting to the app-open trigger.

It is not a kernel-level interception mechanism.

Therefore Circle IX can immediately eject, redirect or lock the phone using available actions, but the target app may briefly become active first.

The user can also disable the Personal Automation.

PROSOCHĒ must never claim to be tamper-proof.

That is acceptable because the product goal is self-directed behaviour change, not coercive access control.

## 5.2 A shared shortcut cannot fully install the Personal Automations

Personal Automations are device-specific.

The distributed Shortcut can contain all behaviour, but the user must create the OPEN and CLOSE automation wrappers on their own iPhone.

Therefore the first-run Control Room Note must contain clear setup instructions.

This is a deliberate product constraint.

## 5.3 Native Shortcuts can be large

Apple's documentation tells users to add as many actions as needed when building Shortcuts/automations. No useful documented hard maximum number of ordinary Shortcut actions has been identified.

Therefore the main engineering risk is not a nominal “number of steps” ceiling.

The relevant risks are:

- runtime complexity;
- variable wiring;
- control-flow errors;
- data volume;
- model latency;
- Notes parsing;
- overlapping automation runs;
- state restoration failures.

The Shortcuts Playground project itself says generated shortcuts can get roughly 90% of the way to a complete solution and specifically warns that variables and repeat-loop wiring should be inspected.

The agent must therefore validate the generated plist and manually reason through the state graph rather than assuming generation equals correctness.

## 5.4 The Note can log, but should not be the hot-path database

Native Shortcuts supports Note creation and `Append to Note`.

A pure Notes database is technically possible.

However, using an indefinitely growing rich-text Note as the authoritative machine state creates avoidable problems:

- every OPEN may require finding the Note;
- its body grows over time;
- extracting the latest state requires parsing;
- Notes may sync through iCloud;
- concurrent OPEN/CLOSE runs create race concerns;
- a document store is not a transactional key-value store.

The current architecture is therefore:

### JSON = current machine state

Small.

Fast.

Rewritten transactionally where possible.

Contains the data required for the next decision.

### Note = human Control Room and readable ledger

Append meaningful behavioural events.

Contain the user's manifesto/profile.

Show trends and value.

Provide setup instructions.

This retains the self-saucing experience without forcing the blocker to parse its complete autobiography before each intervention.

## 5.5 No CSV

CSV was previously considered for structured events.

It is now rejected.

There should be one machine store, not two.

If deeper event history is needed for learning, JSON can contain:

- a compact rolling event history;
- counters;
- recent contracts;
- per-exit reward summaries;
- daily aggregate snapshots.

The Note remains the long-lived human-readable record.

## 5.6 Apple Intelligence is technically viable

iOS 26 includes a `Use Model` Shortcut action.

Apple allows the action to select:

- On-Device;
- Private Cloud Compute;
- Extension Model / ChatGPT.

PROSOCHĒ Sentient must select **On-Device**.

Apple states that this model can handle simple requests without a network connection and that model inputs may include variables and outputs from previous actions.

That makes the following viable:

- classify an intention;
- produce a concise behavioural mirror;
- inspect consistency between a declared intention and recent behavioural telemetry;
- select among a small set of intervention styles;
- formulate one clarification question;
- summarize a recent pattern;
- generate a spoken intervention.

It should not be used for:

- arithmetic;
- Heat/Gravity calculation;
- timers;
- threshold decisions;
- authoritative safety decisions;
- claims of deception;
- Circle IX lockout logic.

Apple also warns generative outputs may vary. Therefore deterministic fallbacks are mandatory.

## 5.7 Device split

Apple Intelligence support begins on the iPhone 15 Pro and iPhone 15 Pro Max generation and later compatible Apple Intelligence iPhones.

Many older iPhones can run iOS 26 without Apple Intelligence.

Therefore the two-fork strategy is technically sensible:

- **Dumb:** broad iOS 26 support.
- **Sentient:** Apple Intelligence-capable devices.

Do not build Dumb as a degraded afterthought.

It should be a coherent product with the same behavioural architecture.

---

# 6. Why the evidence supports PROSOCHĒ's direction

The research does not prove that this exact Nine Circles design will work.

It does, however, support several of its core mechanisms.

## 6.1 Meaningful versus meaningless smartphone use

Lukoff, Yu, Kientz and Hiniker's 2018 study, *What Makes Smartphone Use Meaningful or Meaningless?*, combined interviews, experience sampling and logging of **86,402 app-use sessions**.

Key findings relevant to PROSOCHĒ:

- habitual use to pass time was associated with lower perceived meaningfulness;
- entertainment and passive social media were associated with lower meaningfulness;
- participants described a loss of autonomy during these forms of use;
- motivation to achieve a specific purpose tended to decline during app use, especially passive social media and entertainment;
- apparently “meaningless” use could still serve a broader meaningful function, such as a micro-escape from an unpleasant situation.

This matters.

PROSOCHĒ should not assume all leisure is bad.

The correct distinction is closer to:

- purposeful versus unpurposeful;
- autonomous versus automatic;
- bounded versus unbounded;
- aligned versus displaced.

That directly supports the product decision to accept:

> I deliberately want ten minutes of stupid videos.

as a legitimate intention.

## 6.2 Goal-directed smartphone use RCT — “Not Less But Better”

Keller et al. evaluated a theory-based intervention called **Not Less But Better** in a 20-day randomized controlled trial.

The intervention consisted of five four-day modules:

1. **Observe** — notice impulses, physical reactions and checking behaviour.
2. **Reflect** — understand habitual/problematic use.
3. **Vision** — mindfulness, values and goal setting.
4. **Plan** — action planning and alternative responses.
5. **Support** — sustainable behaviour-change support.

The active control was a conventional digital-detox approach where participants planned at least one hour of phone timeout per day.

Important numbers:

- 232 people enrolled.
- 110, about 47%, provided post-intervention data.
- 88, about 38%, remained at three-week follow-up.

This attrition is important and prevents overclaiming.

Both conditions reduced problematic smartphone use and phone time.

The goal-directed intervention was **not clearly superior to the active digital-detox control on the main outcomes**.

However, the mechanism findings are highly relevant:

- increased self-efficacy statistically mediated improvement in problematic smartphone use;
- higher planning was associated with fewer daily unlocks;
- each one-unit increase in planning was associated with roughly six fewer unlocks/day in the reported model;
- planning had an indirect association with problematic smartphone use through unlock frequency.

Design implication for PROSOCHĒ:

The product should not merely restrict.

It should help the user develop:

- awareness;
- a vision of good phone use;
- plans;
- alternative behaviours;
- self-efficacy.

This is the evidence basis for the Control Room manifesto, intention contracts and replacement exits.

## 6.3 Wellspent RCT — personalized nudges and self-defined limits

A 2026 randomized controlled trial evaluated the **Wellspent** app.

Design:

- 70 iPhone users.
- 35 intervention / 35 control.
- Three-week trial.
- Participants nominated at least one problematic social-media app.
- The intervention used personalized full-screen reminders when a session exceeded a **self-defined time limit**, giving the user a choice to quit or continue.

Results:

- no statistically significant reduction in the study's problematic-social-media-use outcome;
- no significant increase in self-efficacy;
- approximately **29.35 minutes/day lower screen time** on the most problematic app in the intervention group;
- a significant reduction in perceived problematic smartphone use.

The study is small and short-term.

It should not be marketed as definitive proof.

But it supports two PROSOCHĒ choices:

1. let people define their own target apps and boundaries;
2. use just-in-time interventions rather than a single daily limit.

## 6.4 one sec — friction plus an exit choice

A peer-reviewed field study of the one sec self-nudge app is especially relevant.

Field component:

- 280 participants;
- six weeks.

one sec interrupted target-app opening with friction and an opportunity to cancel.

Observed:

- users dismissed approximately **36%** of target-app opening attempts after intervention;
- target-app opening attempts decreased by approximately **37%** over the six weeks;
- the combined reduction in actual target-app openings reached approximately **57%** from first to sixth week.

A separate preregistered experiment with **500 participants** decomposed the intervention.

The most useful finding for PROSOCHĒ:

**Giving the user the option to dismiss the consumption attempt had the strongest effect.**

Time-delay friction also had an effect.

The deliberation message by itself was not the strongest mechanism.

This is an important challenge to an overly verbal “Black Mirror” design.

The model's clever sentence should not become the product.

The behavioural choice architecture is the product.

PROSOCHĒ should always make leaving easy.

## 6.5 Grayscale as design friction

A preregistered randomized field experiment with 112 participants compared:

- grayscale/design friction;
- goal-setting/self-commitment;
- self-monitoring control.

Grayscale produced an immediate significant reduction in objectively measured screen time compared with control.

Goal-setting produced a smaller, more gradual reduction.

A separate 2023 experimental study also reported reductions associated with grayscale, and a small 2026 cross-over feasibility study in medical students reported about 28 fewer minutes/day in grayscale versus colour.

This supports grayscale as a low-level passive intervention.

It does **not** prove that dynamically toggling grayscale only during target-app sessions will have the same effect.

That remains a product hypothesis.

## 6.6 Research-informed digital wellbeing design

A 2022 functionality review of digital-wellbeing tools argued that interventions should go beyond raw screen time.

Its design implications included:

- broader digital wellbeing rather than only time reduction;
- supporting meaningful use rather than merely suppressing meaningless use;
- using digital navigation/friction;
- explicit time-based visualisation;
- ethical design.

This aligns closely with PROSOCHĒ.

## 6.7 Recent research strengthens the intention gap hypothesis

A 2026 in-the-wild research preprint on regretful social-media sessions reported that the **gap between intended and actual use** predicted regret more strongly than duration alone in its sample.

This is not yet evidence equivalent to a large peer-reviewed trial and should be treated as exploratory.

However, it supports a particularly important PROSOCHĒ metric:

**contract fidelity = intended use versus observed duration/return behaviour**

That may ultimately be more informative than total screen time.

## 6.8 LLM interventions are promising but still exploratory

Research prototypes such as MindShift have explored LLM-generated, context-aware smartphone interventions.

A small five-week field experiment reported higher intervention acceptance and lower usage duration for context-aware LLM persuasion compared with simpler baselines.

The evidence base is still small.

PROSOCHĒ Sentient should therefore be positioned as an experimental adaptive interface, not as a scientifically proven AI treatment.

---

# 7. Onboarding: what PROSOCHĒ needs to learn

Earlier onboarding concepts became too complex for the constraints of a Shortcut.

The current principle is:

**Ask only what can materially change the intervention.**

Do not build a therapy intake.

Do not build a 20-question survey.

Use two layers.

## 7.1 Layer A — native import questions

Use `WFWorkflowImportQuestions` only for simple, robust parameters.

Recommended:

### 1. Choose your descent

`Paradise / Limbo / Inferno`

Default: Limbo.

### 2. Sentient capability / preference

For the Sentient fork:

`Use on-device intelligence? yes/no`

For the Dumb fork this does not exist.

### 3. Voice

`May PROSOCHĒ speak to you at the highest circles? yes/no`

This is enough import-time configuration.

Do not try to collect a detailed behavioural profile through import questions.

## 7.2 Layer B — pre-filled Control Room proforma

The first manual run creates:

**PROSOCHĒ — Control Room**

Near the top is a human-editable section:

## MY PHONE, ON PURPOSE

The user fills this directly in Notes.

Suggested proforma:

### What is my phone genuinely for?

Write a few things your phone does that improve your life.

Examples:
- communicate with the people I love;
- navigate;
- capture ideas;
- take photographs;
- make/listen to music;
- learn;
- organise my life;
- deliberately relax.

### Which apps take more attention than I intend to give them?

List the apps you are configuring the OPEN/CLOSE automations for.

Example:
- Instagram
- Facebook
- Reddit
- TikTok

### What do I actually want the reclaimed attention for?

Examples:
- books;
- making music;
- training;
- cooking;
- friends;
- my partner;
- my children;
- being outside;
- thinking;
- sleeping;
- doing nothing.

### When PROSOCHĒ stops an automatic open, what would I rather do?

Choose several from the six exits below and name preferred apps/actions.

### What does deliberate leisure look like for me?

Example:
- ten minutes of Reels after dinner is fine;
- I do not want to turn five minutes into forty;
- I do not want to repeatedly check the same feed.

### Optional sentence to my future self

Example:
- “I installed this because I was tired of checking without deciding.”

The Note should make clear that the user can write naturally.

## 7.3 How the Shortcut uses the proforma

The fast OPEN path should **not parse the entire Note every time**.

Instead:

- first run creates the Note;
- the manual Control Room menu includes `Sync My Profile`;
- that action extracts the human-profile section;
- the profile is mirrored into `state.json`;
- Sentient receives the compact JSON profile when it needs personal context.

Manual runs can also check whether the Note has changed and offer to resync.

This keeps the user-facing setup natural without making every app opening depend on Notes parsing.

---

# 8. The six exits

When PROSOCHĒ successfully interrupts an automatic app opening, the next design question is:

> Where should attention go?

Do not assume “productive app” is always the answer.

The system should support six directions.

All start with C for coherence.

## 8.1 Capture

Purpose:

**Get something out of your head.**

Possible targets:

- Notes;
- Voice Memos;
- Camera;
- a configured journaling app.

Examples:

- capture an idea;
- write a thought;
- record a voice note;
- photograph something deliberately.

This is ideal when the original impulse was partly driven by internal restlessness or a thought the user did not want to lose.

## 8.2 Coordinate

This replaces the earlier name “Orient.”

Purpose:

**Turn vague mental load into a plan.**

Possible targets:

- Reminders;
- Calendar;
- Notes task list.

Examples:

- look at what is actually next;
- schedule something;
- capture a task;
- check the day's commitments.

Coordinate should not be framed as “be productive.”

It is about reducing ambiguity.

## 8.3 Create

Purpose:

**Make rather than consume.**

Targets are user-defined and may include:

- music apps;
- GarageBand;
- creative writing;
- drawing;
- camera;
- editing;
- a musical instrument app;
- Notes.

The user should choose what “create” means.

## 8.4 Connect

Purpose:

**Move from passive social consumption to actual human contact.**

Possible targets:

- Messages;
- Phone;
- FaceTime;
- a selected messaging app;
- Contacts.

Do not randomly call people.

The Shortcut may simply open the communication tool or show a short prompt:

> Is there someone you actually wanted to speak to?

Connection should be optional because not every user wants social pressure as a behavioural intervention.

## 8.5 Consult

This is the new information-seeking route.

Purpose:

**Find the thing without entering a feed.**

A significant amount of apparently problematic social-app use begins with a legitimate information need:

- find a restaurant someone mentioned;
- look up an event;
- research a product;
- find a place;
- answer a factual question;
- find a reference;
- locate a post or creator.

The problem is that the user enters an environment optimized for unrelated discovery and loses the original information need.

Consult should create a direct search route.

Examples:

- Ask: `What are you trying to find?`
- Open a web search for that query.
- If the query sounds like a place, route to Maps search.
- If it is a reminder or known personal item, route to Notes/Reminders search where supported.
- Sentient may classify the information need into:
  - web;
  - maps/place;
  - personal notes;
  - calendar/reminders;
  - direct communication.

The Dumb fork can present a small menu instead.

Research rationale:

Meaningful smartphone-use research consistently distinguishes specific-purpose use from habitual/passive consumption. Recent qualitative work also classifies accessing information and coordinating activities as examples of effectual, goal-directed smartphone use.

The design goal is not “never search.”

It is:

**replace feed-shaped information seeking with query-shaped information seeking.**

## 8.6 Close

This replaces the earlier label “Leave.”

Purpose:

**The phone is not the next action.**

Close means:

- return Home;
- Lock Screen where appropriate;
- optionally start already-selected audio;
- put the device down.

Its paired message may use the user's values:

> You said you wanted this time for making music.

or:

> Nothing on the phone is the next step.

This is a critical product principle:

**The best alternative app may be no app.**

---

# 9. Learning which exits work: explore/exploit

Do not permanently choose one default redirect.

PROSOCHĒ should learn which exit actually breaks the loop for this user.

This can be entirely local and deterministic.

## 9.1 Observation

When an exit is used, record:

- exit type;
- timestamp;
- target app that triggered it;
- current Circle;
- current Heat/Pressure;
- time of day;
- time until the next target-app OPEN.

The simplest outcome signal is:

**How long did it take before the user returned to a tracked app?**

Useful derived outcomes:

- returned within 2 minutes;
- returned within 10 minutes;
- returned within 30 minutes;
- no return within 30 minutes.

## 9.2 Exploration phase

Initially, rotate reasonably evenly across the user's enabled exits.

Do not randomize to an exit they explicitly disabled.

The purpose is to learn.

## 9.3 Exploitation phase

After enough observations exist, prefer exits associated with longer periods away from target apps.

A simple epsilon-greedy policy is sufficient.

Conceptually:

- most of the time choose the historically stronger exit;
- occasionally test another enabled exit so the system continues learning.

The exact exploration percentage must be configuration, not marketing doctrine.

Do not use the LLM to calculate the winning exit.

## 9.4 Contextual learning later

Once basic learning works, success can be conditioned on:

- morning/day/evening;
- weekday/weekend;
- target app;
- current intention category;
- current Circle.

Example:

- Coordinate may work well during work hours.
- Create may work well in evenings.
- Close may work best during late-night rapid-return clusters.
- Consult may work best when the stated intention is information-seeking.

This is a future refinement after basic exit learning is proven stable.

---

# 10. Behavioural state model

## 10.1 Behavioural day

Do not reset at midnight.

Define:

**Behavioural Day = Current Date minus 4 hours**

Format as date key.

This creates an approximate 04:00–03:59 day.

It avoids an obvious midnight loophole.

## 10.2 Heat

Heat measures local compulsive clustering.

Candidate baseline logic:

1. Decay Heat according to time since the last genuine target-app interaction.
2. Add Heat for the new OPEN.
3. Add extra Heat for rapid reopening.
4. Add Heat when the previous declared time boundary was substantially exceeded.
5. Reduce Heat when the user respected a declared boundary.
6. Cap Heat.

The exact coefficients are initial defaults and must remain easy to change during testing.

Suggested initial rule:

- base genuine OPEN: `+1`
- reopen <2 minutes: additional `+2`
- reopen <10 minutes: additional `+1`
- previous session exceeded declared duration by >50% and >2 minutes: `+2`
- previous contract respected: `-1`
- decay: `-1` per ~10 minutes away
- floor: `0`
- cap: `30`

Heat is not “addiction severity.”

It is an operational intervention signal.

## 10.3 Gravity

Gravity measures slower accumulation across the day.

Suggested initial rule:

`gravity = floor(opens_today / 6)`

cap at `5`.

Gravity means that repeated use across an entire day still gradually increases intervention even without rapid bursts.

## 10.4 Pressure

`pressure = heat + gravity`

Pressure maps to the Nine Circles.

## 10.5 Profiles

### Paradise

Slow descent:

`1, 4, 7, 10, 13, 16, 19, 22, 25`

### Limbo

Balanced:

`1, 3, 5, 7, 9, 11, 14, 17, 20`

### Inferno

Fast descent:

`1, 2, 4, 6, 8, 10, 12, 14, 16`

These are prototype parameters.

The product should make them easy to tune.

The names are part of the experience, not clinical classifications.

---

## 10.6 Circle 0 — the silent band

Pressure below the active profile's first threshold resolves to **Circle 0**.

In Circle 0 the behavioural state engine runs and persists in full — behavioural day, Heat, Gravity, Pressure, open count, and the active session are all computed and written to `state.json` exactly as they are at any other Circle.

Nothing is shown. No notification, no menu, no primitive. Circle 0 is a band the person never sees.

The Leaving/Continue offer and every intervention primitive begin at Circle 1.

The band exists because a user buried in pop-ups from the very first open of the day deletes the Shortcut — which section 12's testing philosophy already names as the key failure. A system that interrupts an open the person has not yet repeated has spent its credibility before it has earned any.

The entry thresholds are prototype values for on-device tuning. The currently shipped entry values — the Pressure at which Circle 1 is first reached — are **Paradise 4, Limbo 3, Inferno 2**.

BD-06's Dante naming covers Circles 1 through 9 only. Circle 0 needs no name, because it is never surfaced; the later Build Addendum 01 rename phase therefore has nothing to assign here.

---

# 11. Nine intervention primitives

The exact order is intentionally testable.

The nine primitives occupy Circles 1 through 9; Circle 0 has no primitive by design (see section 10.6).

The system needs nine behavioural primitives.

## Primitive A — The Knock

A small interruption.

Example:

> Open #4 today · Heat 3  
> One breath. What did you come here for?

No lecture.

The Knock is Circle 1's intervention in the Classic and Black Mirror orderings, but it is not the first thing a user encounters — Circle 0 precedes it silently.

## Primitive B — Ash

Grayscale where iOS can apply and restore it safely.

Passive reduction of visual salience.

## Primitive C — Silence

Mute/reduce media audio only if PROSOCHĒ can safely capture and restore state.

Never blast sound as punishment.

## Primitive D — Confession / Intention Contract

Ask:

> What exactly did you come here to do?

Accept free text.

Then require a boundary:

- 2 min
- 5 min
- 10 min
- 15 min
- Custom

“Watch stupid videos for ten minutes” is a valid answer.

## Primitive E — Dimming

Reduce display salience with safe brightness adjustment if reversible.

Never set zero brightness.

Never interfere with accessibility settings in a way that can strand the user.

## Primitive F — Exile

Immediately remove the target app from the path of least resistance.

Use an exit.

No permission prompt.

Conceptually:

> Come back if you still mean to.

The user remains free to return.

Returning is now an affirmative act and creates another OPEN.

## Primitive G — The Mirror

Show a precise behavioural reflection.

Dumb:

deterministic telemetry-based message.

Sentient:

on-device model-generated reflection.

## Primitive H — The Voice

The Mirror becomes spoken once.

Never shout.

Never manipulate sound to unsafe levels.

## Primitive I — Ice

Deterministic cooldown / strongest available safe ejection.

The model does not decide Ice.

This is a behavioural threshold.

If native Lock Screen is available and verified, it may be used.

Otherwise route to Close / Control Room / another strongest safe exit.

The user must eventually cool out of Ice.

---

# 12. Candidate Circle sequences

Do not assume one order is correct.

Include several arrangements for manual testing.

All three candidate sequences are nine-slot orderings over Circles 1 through 9; none of them assigns anything to Circle 0.

## 12.1 Classic

Designed to introduce passive friction before cognitive demands.

1. The Knock
2. Ash
3. Silence
4. Confession
5. Dimming
6. Exile
7. The Mirror
8. The Voice
9. Ice

## 12.2 Black Mirror

Designed to introduce behavioural self-awareness earlier.

1. The Knock
2. Confession
3. Ash + Confession
4. The Mirror
5. Silence + Mirror
6. Dimming + Mirror
7. Exile
8. The Voice
9. Ice

## 12.3 Ambient

Designed to minimize interruption burden.

1. Ash
2. Silence
3. Dimming
4. The Knock
5. Confession
6. Exile
7. The Mirror
8. The Voice
9. Ice

## Testing philosophy

Do not build a remote A/B infrastructure.

Allow the sequence to be changed from the manual Control Room menu.

The creator and test group can compare:

- subjective annoyance;
- disable rate;
- rapid-return rate;
- target-app openings;
- contract fidelity;
- time until return following an exit.

The key failure mode is:

**The intervention is so annoying that the user disables PROSOCHĒ.**

That is a product failure even if it theoretically blocks more openings.

---

# 13. PROSOCHĒ Dumb

Dumb is not “Sentient without the good bits.”

It is the baseline product.

Everything structural is deterministic:

- Heat;
- Gravity;
- Pressure;
- thresholds;
- contracts;
- exit learning;
- cooldown;
- restoration;
- telemetry;
- profile;
- sequence.

## 13.1 Dumb Mirror engine

Use telemetry templates that never invent facts.

Examples:

> This is open #12 today.

> You were here three minutes ago.

> The last five-minute session lasted thirteen minutes.

> You have returned four times in twenty minutes.

> You said you wanted five minutes. You left after four.

> The next ten minutes are still unspent.

> You said you came here to reply to someone.

> The feed has no natural stopping point. Your task does.

Maintain at least 30 templates.

Select templates according to available facts.

Do not show a time-overrun message if there was no contract.

## 13.2 Dumb intent gate

Ask:

1. What exactly did you come here to do?
2. For how long?

A blank/vague response can trigger a redirect at higher Circles.

Do not try to parse philosophical sincerity.

## 13.3 Dumb Consult

Ask what information the user needs.

Offer:

- Search Web
- Search Maps
- Open Notes
- Open Reminders
- Open Calendar
- Back

This preserves the information need without a model.

---

# 14. PROSOCHĒ Sentient

Sentient uses the same state engine but adds the on-device model at multiple Circles.

It should feel increasingly aware as Pressure increases.

The key rule:

**Sentient observes behaviour; it does not claim access to hidden mental states.**

## 14.1 What Sentient can know

It can know:

- target app;
- current time;
- open count;
- Heat;
- Gravity;
- Pressure;
- recent return intervals;
- user's reclaim goal;
- phone-purpose profile;
- enabled exits;
- declared current intention;
- declared duration;
- previous intentions;
- previous session durations;
- whether previous time contracts were respected;
- which exits tended to prevent rapid returns;
- recent model messages.

It cannot know:

- what content was viewed inside Instagram;
- whether a message was actually sent;
- whether the user felt bored/anxious;
- whether the user is “lying.”

## 14.2 From lie detector to contract auditor

Do not ask:

> Is the user lying?

Ask:

> Is the current contract specific, bounded and behaviourally consistent with recent observed contracts?

Three dimensions:

### Specificity

Is there a recognizable purpose?

### Boundedness

Is there a stopping condition or time limit?

### Consistency

Have similar stated intentions repeatedly resulted in substantial overruns or immediate returns?

Sentient may become sceptical.

Example:

> You have called the last four sessions “quick replies.” They averaged eleven minutes. What exactly are you replying to?

This is factual and challengeable.

## 14.3 Sentient verdicts

Structured output:

- `ALLOW`
- `CHALLENGE`
- `DENY`

DENY only at sufficiently high Circles.

A denial means redirect, not system-level punishment.

At most one challenge round.

Never create an interrogation loop.

Circle IX remains deterministic.

## 14.4 Sentient should appear at multiple Circles

A possible design:

### Circle I

Deterministic.

Speed matters more than intelligence.

### Circle II

Optional lightweight model mirror only when cached/fast enough; otherwise deterministic.

### Circle III

Model may choose between a small set of message tones based on recent pattern, but may not alter Pressure.

### Circle IV

Sentient classifies the intention and can ask one precision question.

### Circle V

Sentient adds a short observation using current contract and recent history.

### Circle VI

Sentient can classify which of the six exits best matches the user's stated intent, but the explore/exploit engine still governs long-term routing.

### Circle VII

Full Contract Auditor / Mirror.

### Circle VIII

Full Mirror + Voice.

### Circle IX

No model.

Deterministic Ice.

## 14.5 Model latency and caching concept

Do not force model inference onto every early OPEN if it makes the intervention visibly slow.

A useful future optimization:

**precompute the next likely Mirror on CLOSE.**

CLOSE already has:

- completed session duration;
- contract outcome;
- return history;
- user profile.

Sentient could generate a short “next reflection” and cache it in JSON.

The next OPEN can display this immediately and update with deterministic facts.

This should only be implemented if Shortcuts Playground testing shows it is reliable.

## 14.6 Sentient system prompt principles

The system instruction should say, in substance:

You are PROSOCHĒ, an attention mirror running privately on this device.

You are not a therapist, parent, moral authority or lie detector.

Distinguish deliberate use from automatic use using only supplied behavioural telemetry.

Deliberate leisure is valid.

Never invent what happened inside an app.

Never diagnose addiction.

Use concrete behavioural facts.

Be calm, concise, lucid, slightly uncanny and unsentimental.

Prefer one specific observation over a motivational slogan.

Return structured output suitable for Shortcut parsing.

Avoid:
- addiction
- dopamine
- weakness
- lazy
- failure
- shame
- exclamation marks
- emoji

---

# 15. Longitudinal memory: where Sentient becomes interesting

The most powerful model context is not the present open.

It is the pattern across time.

Example state:

- rapid returns today: 7
- “quick reply” contracts this week: 9
- median planned duration: 3 min
- median actual duration: 11 min
- deliberate-leisure contracts: 6
- median deliberate-leisure overrun: 4%
- best-performing exit at night: Close
- weakest exit at night: Coordinate

Then Sentient can produce useful observations such as:

> Your deliberate scrolling is usually bounded. The sessions you call “quick replies” are the ones that expand.

or:

> You don't stay here longest at night. You come back most often within six minutes of leaving.

or:

> Three Tuesdays ago this was your hottest evening. Rapid returns have been falling since.

This is the core “Black Mirror” opportunity.

The user gets a behavioural mirror they could not easily create unaided.

## Rules

- Do not invent trends.
- Only make comparative claims when enough data exists.
- Prefer medians to means for session duration.
- Label estimated metrics as estimates.
- Never infer mental-state labels from telemetry alone.

---

# 16. JSON state design

The exact schema may change during implementation, but it should include:

```json
{
  "schema_version": 1,
  "profile": "Limbo",
  "sequence": "Classic",
  "fork": "Dumb|Sentient",
  "voice_enabled": true,
  "ai_enabled": true,
  "behavioural_day": "2026-08-13",
  "opens_today": 0,
  "heat": 0,
  "gravity": 0,
  "pressure": 0,
  "circle": 1,
  "last_open_at": null,
  "last_close_at": null,
  "last_app": null,
  "active_session": null,
  "recent_sessions": [],
  "recent_contracts": [],
  "exit_stats": {},
  "cooldown_until": null,
  "settings_snapshot": {},
  "profile_snapshot": {},
  "last_model_message": null
}
```

Do not blindly preserve unbounded arrays.

Use rolling windows plus aggregates.

Examples:

- last 20 sessions;
- last 10 contracts;
- per-exit counts/reward aggregates;
- daily aggregate records for a limited period.

The Note contains the readable longer history.

---

# 17. Control Room Note

The Note is part of the product, not just debug output.

Its tone should be calm and clean.

Suggested structure:

# PROSOCHĒ — CONTROL ROOM

## READ THIS FIRST

What PROSOCHĒ is.

How to create OPEN automation.

How to create CLOSE automation.

Safety warning: do not target Phone, Maps, Wallet, authenticators, password managers or other essential apps.

## MY PHONE, ON PURPOSE

The editable proforma.

## CURRENT SETTINGS

- Fork
- Profile
- Sequence
- Voice
- AI
- Enabled exits

## CURRENT STATE

A human-readable state snapshot updated periodically/manual run.

## ATTENTION LEDGER

Readable events.

Do not append every tiny implementation detail.

Prefer meaningful entries:

- Circle changes;
- contracts;
- redirects;
- rapid-return clusters;
- successful cool-downs;
- daily summaries;
- profile changes.

Example:

`08:17 — Instagram opened. Heat 6 → Circle IV. Intention: reply to Maya. Contract: 5m.`

`08:22 — Session closed at 4m 36s. Contract kept.`

`08:25 — Instagram reopened after 3m. Heat 7.`

`08:26 — Exit: Consult → web search.`

## VALUE / LIFE RETURNED

Reserved for later measurement design.

## SUPPORT PROSOCHĒ

Reserved for later pay-after-value design.

---

# 18. First-run self-saucing flow

## Import

User installs either Dumb or Sentient.

Native import questions capture simple static configuration.

## First tap

PROSOCHĒ checks for state.

If absent:

1. create PROSOCHĒ directory in the Shortcuts-accessible file location;
2. create `state.json`;
3. create Control Room Note;
4. populate Note with the setup instructions and human profile proforma;
5. populate JSON with initial profile/fork/config;
6. open/show the Control Room Note.

The Note explicitly tells the user to create:

### Automation A — OPEN

- Trigger: App
- select target apps
- `Is Opened`
- run automatically
- Run Shortcut: `PROSOCHĒ — Nine Circles`
- pass input: `OPEN`

### Automation B — CLOSE

- same target apps
- `Is Closed`
- run automatically
- Run Shortcut: `PROSOCHĒ — Nine Circles`
- pass input: `CLOSE`

The Shortcut cannot truthfully claim to install these automatically.

## Second manual run

Show Control Room menu:

- Status
- Open Control Room
- Sync My Profile
- Change Profile
- Change Sequence
- Toggle Voice
- Test a Circle
- Reset Today
- Emergency Restore

Sentient only:

- Toggle On-Device AI
- Test Model

---

# 19. OPEN handler

When input = `OPEN`:

1. load JSON state;
2. if missing, self-heal/bootstrap;
3. calculate behavioural-day rollover;
4. obtain Current App if available/verified;
5. debounce duplicate OPEN events;
6. check cooldown;
7. calculate time since prior real interaction;
8. decay Heat;
9. increment open count;
10. add rapid-return Heat;
11. incorporate previous contract fidelity;
12. calculate Gravity;
13. calculate Pressure;
14. map Pressure to Circle;
15. create session ID;
16. persist state;
17. log meaningful OPEN if appropriate;
18. execute current Circle behaviour.

Where possible, show the behavioural intervention before non-essential Note logging.

No Screen Time API blocking.

---

# 20. CLOSE handler

CLOSE gives PROSOCHĒ observed session duration.

Race-proof it.

1. load JSON;
2. capture active session ID;
3. capture start timestamp;
4. brief wait if needed for app-switch race handling;
5. reload state;
6. if active session ID changed, a newer OPEN owns state — stop;
7. calculate actual session duration;
8. compare against declared contract;
9. calculate overrun;
10. update contract fidelity;
11. update recent sessions;
12. restore any settings PROSOCHĒ itself changed;
13. update exit-learning outcome if relevant;
14. clear active session;
15. persist JSON;
16. append readable CLOSE/contract outcome to Note when useful;
17. Sentient may optionally precompute future mirror context.

---

# 21. Environmental state safety

Any system-setting friction is subordinate to safety.

## Brightness

- Never zero.
- Only change if PROSOCHĒ can reliably restore.
- Prefer ~10–15% as a prototype dim value.
- If original state cannot be read, do not make a stateful brightness intervention.

## Volume

- Never increase volume as punishment.
- Never produce startling output.
- If changing volume for Silence, restore original value.
- If original value cannot be captured reliably, skip the intervention.

## Grayscale / Color Filters

Accessibility settings may already be intentionally configured by the user.

Do not blindly disable a pre-existing state.

If Shortcuts cannot detect and restore the original condition safely, either:

- skip dynamic grayscale; or
- require the user to opt into a known PROSOCHĒ-managed configuration.

## Emergency Restore

Manual menu must provide an Emergency Restore action.

It clears:

- PROSOCHĒ cooldown;
- active session;
- any recoverable temporary brightness;
- recoverable volume;
- recoverable colour settings.

---

# 22. Circle IX — Ice

No NFC in this version.

No model judgement.

Ice is reached deterministically through Pressure.

Initial concept:

- Paradise: ~60 sec
- Limbo: ~3 min
- Inferno: ~5 min

Exact values are prototype parameters.

During Ice:

- target-app OPEN immediately ejects/locks/redirects;
- blocked attempts should not endlessly inflate Heat;
- show remaining cooldown if practical.

When Ice expires:

- provide Heat relief;
- clear cooldown.

There must be a route out.

The product should not trap the user in permanent escalating punishment.

---

# 23. Measurement

Measurement is local.

The first objective metrics:

- target-app OPEN count;
- rapid-return count;
- session duration;
- declared duration;
- contract overrun;
- Circle distribution;
- redirects;
- exit selected;
- time to next target-app return;
- daily Heat maxima;
- user resets;
- profile changes.

## Primary prototype metric

**Rapid-return rate**

This may be more diagnostic of habitual looping than raw screen time.

Examples:

- percentage of sessions followed by another tracked OPEN within 2 minutes;
- percentage followed within 10 minutes.

## Second metric

**Contract fidelity**

For time-bound sessions:

`actual duration / intended duration`

Use medians and distributions.

Do not turn this into moral scoring.

## Disable rate

In friend testing, ask whether the system was disabled and why.

That is a critical product-quality signal.

A blocker that users turn off is not effective.

---

# 24. “Life Returned” — record now, design later

This idea is intentionally parked for a later product phase.

PROSOCHĒ should eventually quantify value created.

But it must be mathematically honest.

Do not claim:

`100 blocked opens = X hours saved`

without evidence.

## Observed metrics can be stated directly

Examples:

- 1,284 automatic opens interrupted;
- 412 rapid returns broken;
- 73 exits accepted;
- median target-app session fell from X to Y;
- observed target-app Screen Time fell from X to Y if Screen Time telemetry is available.

## Estimated attention reclaimed

A future conservative estimate can use a personal counterfactual baseline.

Concept:

`expected comparable session duration - observed session duration`

with lower bound zero.

Use rolling personal medians rather than a global assumption.

Potential baseline dimensions:

- app;
- time of day;
- Circle;
- deliberate versus automatic contract type.

Label this:

**Estimated Attention Reclaimed**

or:

**Estimated Life Returned**

Never present it as exact.

## Screen Time telemetry

iOS 26 added `Get App & Website Data` to Shortcuts.

This may become a useful measurement source.

It is not required for blocking.

Before implementing value metrics, the build agent must inspect the action's actual schema and runtime granularity on iPhone.

Do not assume it provides arbitrary historical querying until tested.

---

# 25. Pay after value — record now, implement later

The product will remain free and open source.

No feature gate.

No subscription required.

No ads.

No sale of behavioural data.

The monetization philosophy is:

**Pay after value.**

PROSOCHĒ should first create measurable value.

Only later should it gently offer the user a way to support the project.

Possible triggers:

- 100 automatic openings interrupted;
- a threshold of estimated attention reclaimed;
- 30 active days;
- another conservative milestone.

Example future copy:

> PROSOCHĒ has interrupted 184 automatic opens.  
> Estimated attention returned: 3h 17m.  
>  
> PROSOCHĒ is free and open source, permanently.  
> If that time has been worth something to you, you can pay what you think it was worth.

Options:

- Support PROSOCHĒ
- Not now
- Never ask again

Important:

- payment is not a behavioural intervention;
- never display the payment ask while the user is being blocked;
- never use guilt;
- never threaten loss of functionality;
- never transmit the user's attention history to the creator merely to calculate payment.

Potential infrastructure later:

- GitHub Sponsors;
- a pay-what-you-want payment link.

This is a future product/marketing workstream, not MVP build scope.

---

# 26. Open-source principles

PROSOCHĒ should be understandable by its users.

Repository should eventually contain:

- signed release `.shortcut`;
- unsigned XML source;
- human-readable architecture docs;
- model prompts;
- Heat/Gravity logic;
- known iOS limitations;
- privacy explanation;
- contribution guide;
- changelog.

The README should make clear:

- all behavioural data stays on the user's device in the default design;
- no external analytics;
- Sentient uses Apple's On-Device model;
- model output can be wrong;
- the system is self-directed and bypassable;
- the user owns the Shortcut and can inspect/edit it.

The product should be forkable.

---

# 27. Privacy model

Default:

**No behavioural data leaves the phone.**

The Note and JSON may sync through the user's own iCloud depending on their device configuration, but PROSOCHĒ itself does not transmit telemetry to its creator.

Sentient:

- use On-Device model only;
- never send PROSOCHĒ profile/history to ChatGPT;
- never select Private Cloud Compute;
- pass only a compact recent context window;
- do not pass the whole Note;
- store only final model outputs required for continuity;
- do not store hidden reasoning.

---

# 28. Model-context design

Sentient input should be compact.

Example:

```text
GOAL:
Make music, read more, train, spend time with people.

PHONE PURPOSE:
Communication, navigation, music, capture ideas, research.

CURRENT:
App: Instagram
Time: 22:41
Open today: 12
Heat: 11
Gravity: 2
Pressure: 13
Circle: 7
Time since last close: 2m 14s

CURRENT CONTRACT:
"Reply to Hannah about Saturday"
5 minutes

RECENT CONTRACTS:
1. "Reply to Tom" planned 3m / actual 10m / return 4m
2. "Watch reels" planned 10m / actual 9m / return 48m
3. "Reply to Alex" planned 5m / actual 12m / return 3m

EXIT HISTORY:
Close: 6 samples / median return 31m
Coordinate: 5 samples / median return 4m
Create: 4 samples / median return 18m
```

This gives the model enough context to be useful without needing the complete Note.

---

# 29. What “Sentient” should sound like

The model is not a motivational quote generator.

Bad:

> Believe in yourself! Put the phone down and chase your dreams!

Bad:

> Your dopamine system is hijacked.

Bad:

> You're lying again.

Good:

> The last three “quick reply” sessions ran past ten minutes.

Good:

> Your deliberate ten-minute leisure sessions usually stop on time. This one has no stopping condition yet.

Good:

> You returned two minutes after leaving. What is different about this opening?

Good:

> Close has kept you away longer than any app redirect tonight.

Good:

> You said this time was for making music. The phone is still available later.

The model should occasionally acknowledge success.

The product must not create a learned association that opening a target app always produces criticism.

Examples:

> You said five minutes and left after four. Deliberate use appears to be working.

> This is your first return in two hours. Heat has cooled.

> Your recent leisure contracts have mostly stayed within their boundaries.

Positive reinforcement is part of the nudge architecture.

---

# 30. Failure modes

## Intervention fatigue

Symptom:

User dismisses prompts mechanically.

Mitigation:

- passive early Circles;
- sequence variation;
- concise copy;
- no repetitive lecture;
- Sentient avoids repeating the same Mirror.

## Disablement

Symptom:

User turns off automation.

Mitigation:

- respect deliberate leisure;
- avoid excessive prompts;
- allow Paradise;
- make strong interventions conditional on actual Pressure;
- learn effective exits rather than always punishing.

## State races

Symptom:

OPEN/CLOSE overlap during rapid app switching.

Mitigation:

- session IDs;
- JSON as authoritative state;
- reload state before CLOSE commit;
- idempotent restoration.

## Notes growth

Symptom:

Control Room becomes huge.

Mitigation:

- JSON carries live state;
- Note logs meaningful events, not every internal calculation;
- later add archival/daily summaries if needed.

## Generative inconsistency

Symptom:

Sentient output is malformed or inappropriate.

Mitigation:

- structured output;
- parse validation;
- deterministic fallback;
- model never controls arithmetic or Ice;
- one challenge maximum.

## Accessibility interference

Symptom:

Grayscale/brightness manipulation conflicts with user needs.

Mitigation:

- capability/state audit;
- opt out;
- never blindly override accessibility configuration.

## False psychological inference

Symptom:

Model states the user is bored, anxious, addicted or dishonest without evidence.

Mitigation:

- strict prompt;
- behavioural facts only;
- deterministic safety checks;
- product copy avoids diagnosis.

## Over-optimization for phone-based alternatives

Symptom:

PROSOCHĒ merely changes which app consumes time.

Mitigation:

- Close is a first-class exit;
- user profile includes offline life;
- exit-learning rewards time away from tracked apps.

---

# 31. Build strategy for the Shortcuts Playground agent

The agent's job is not to write another strategy.

It must build working shortcuts from this strategy.

## Deliverables

Produce:

- `PROSOCHĒ — Nine Circles — Dumb.shortcut`
- `PROSOCHĒ — Nine Circles — Sentient.shortcut`
- unsigned XML draft for each
- build notes documenting unsupported/deviated actions

Prefer a shared source architecture where practical.

## Before authoring

Read Shortcuts Playground:

- `SKILL.md`
- `BEST_PRACTICES.md`
- `ACTIONS.md`
- `APPINTENTS.md`
- `PLIST_FORMAT.md`
- `VARIABLES.md`
- `CONTROL_FLOW.md`
- `DATE_TIME.md`
- relevant golden shortcut XML
- validator documentation

Run self-test.

Target iOS.

## Capability audit

Verify the exact iOS action identifier and parameter shape for:

- Get Current App
- Get File
- Save File / overwrite
- Dictionary / JSON parsing
- Get Dictionary Value
- date arithmetic
- Notes search/find
- Create Note
- Append to Note
- show/open note if available
- Ask for Input
- Choose from Menu/List
- Open App
- Open URLs / web search
- Maps search/deep link capability
- Set Brightness
- get current brightness
- Set Volume
- get current volume
- Color Filters / grayscale
- Speak Text
- Lock Screen
- Base64 encoding if needed
- Use Model / On-Device model
- model structured output capability
- Get App & Website Data (research/measurement only, not core v1)

Do not fabricate an action because the strategy requests it.

If an action cannot be verified:

- use the safest fallback;
- record the deviation;
- keep the Shortcut runnable.

## Import questions

Implement only simple robust setup values.

Do not over-engineer import-time UX.

## Build Dumb first

Dumb establishes:

- invocation routing;
- bootstrap;
- JSON;
- Control Room;
- OPEN;
- CLOSE;
- Heat;
- Gravity;
- Pressure;
- profiles;
- sequences;
- all non-AI Circle primitives;
- contracts;
- exits;
- explore/exploit;
- restoration;
- cooldown;
- fallback mirrors.

Only after Dumb is stable, fork Sentient.

## Build Sentient second

Add:

- model capability checks;
- On-Device Use Model;
- intent classification;
- contract auditing;
- Mirror generation;
- voice;
- exit classification assistance;
- malformed-output fallback.

Do not alter the deterministic state engine.

---

# 32. Agent acceptance criteria

The build is not done because the plist validates.

It must also satisfy behavioural/state cases.

## Bootstrap

- Fresh import works.
- First manual run creates JSON.
- First manual run creates one Control Room.
- Control Room contains OPEN/CLOSE automation instructions.
- Human profile proforma is present.
- Existing state is not overwritten on later manual runs.

## OPEN/CLOSE

- OPEN increments once.
- Duplicate trigger debounce works.
- CLOSE measures session duration.
- Rapid switching between two tracked apps does not corrupt state.
- Behavioural day rolls at 04:00.
- Heat decays.
- Rapid return increases Heat.
- Gravity accumulates.
- Pressure maps correctly.
- all three profiles differ.

## Contracts

- Free-text intention works.
- Duration selection works.
- deliberate leisure is accepted.
- contract overrun recorded.
- contract success recorded.
- future Heat can use contract outcome.

## Exits

All enabled exits can be invoked:

- Capture
- Coordinate
- Create
- Connect
- Consult
- Close

Consult supports at least a direct search route.

Exit outcomes are recorded.

Basic explore/exploit selection functions.

## Circles

- candidate sequence can be changed.
- Circle mapping changes accordingly.
- stronger Circle does not necessarily show every earlier prompt.
- ambient effects are restored.
- Circle IX cooldown is deterministic.
- cooldown attempts do not endlessly inflate Heat.
- user exits Ice.

## Dumb

- no Apple Intelligence dependency.
- fallback Mirrors use only real facts.
- no malformed telemetry messages.

## Sentient

- uses On-Device model only.
- no cloud/ChatGPT.
- model can fail without breaking shortcut.
- output is parsed/validated.
- one CHALLENGE maximum.
- model never claims to know app contents.
- model never decides Circle IX.
- deliberate leisure can be ALLOW.
- prior contract consistency can inform challenge.
- spoken intervention occurs at most once per run.

## Safety

- no zero brightness.
- no unsafe volume.
- no accessibility-stranding behaviour.
- Emergency Restore works.
- deleting Control Room does not crash app; safe recovery occurs.
- corrupt/missing JSON triggers safe recovery.

## Privacy

- no external network dependency for core functionality.
- no behavioural telemetry sent away.
- no cloud model.

## Distribution

- validator passes.
- shortcut signs.
- shortcut imports.
- both forks are named clearly.
- source XML retained.

---

# 33. Research questions for prototype testing

These are product questions, not requirements to implement formal experimentation.

## Question 1

Which sequence produces the best balance between:

- reduced rapid-return behaviour;
- low annoyance;
- low disablement?

Compare Classic / Black Mirror / Ambient.

## Question 2

Is Heat more useful than raw open count?

Look for users who have the same daily opens but different clustering.

## Question 3

Which exit classes actually interrupt the loop?

Measure time to next tracked OPEN.

## Question 4

Does Sentient add meaningful value over Dumb?

Not:

> Which one sounds cooler?

But:

- Does it lead to fewer rapid returns?
- Does it make intention contracts more specific?
- Is it less repetitive?
- Does it annoy users more?
- Do users report learning something about their behaviour?

## Question 5

What messages become stale?

The system should not repeatedly show the same philosophical line.

## Question 6

At what Circle does friction become counterproductive?

This is why Paradise/Limbo/Inferno exist.

---

# 34. Future roadmap — intentionally not in current build

## Phase A — prove the Shortcut

- Dumb and Sentient
- Notes + JSON
- Nine Circles
- Heat/Gravity
- exits
- learning

## Phase B — value

- Screen Time telemetry audit
- honest personal baselines
- Estimated Attention Reclaimed / Life Returned
- daily/weekly summaries

## Phase C — pay after value

- support link
- local milestone prompt
- never-pay option
- no functionality gate

## Phase D — physical commitment

Revisit NFC.

Potential use:

- deliberately located physical tag;
- optional Circle IX unlock;
- commitment through movement/physical separation.

## Phase E — stronger native enforcement

Only if needed:

- open-source companion iOS app;
- Screen Time / ManagedSettings APIs;
- tighter blocking.

The core Nine Circles philosophy should remain independent from stronger enforcement.

## Phase F — community science

If there is interest:

- optional export of anonymized local metrics initiated by the user;
- open analysis;
- publish protocol;
- transparent intervention comparisons.

No hidden analytics.

---

# 35. Canonical product decisions

These decisions supersede earlier exploration.

| Decision | Current answer |
|---|---|
| Core product | Adaptive friction / attention intervention |
| Target | iOS 26 |
| Focus | No |
| NFC | No |
| Screen Time blocking | No |
| Screen Time telemetry | Later / optional measurement |
| Machine persistence | One JSON |
| Human persistence | One Control Room Note |
| CSV | No |
| Target-app trigger | App OPEN Personal Automation |
| Session measurement | App CLOSE Personal Automation |
| Profiles | Paradise / Limbo / Inferno |
| Escalation | Heat + Gravity = Pressure |
| Circles | Nine |
| Sequence | Configurable; Classic default |
| User intention | Free text + time boundary |
| Leisure | Explicitly valid |
| Exit system | Capture / Coordinate / Create / Connect / Consult / Close |
| Exit selection | Explore/exploit learning |
| AI | Two product forks |
| Dumb | Deterministic |
| Sentient | Apple On-Device model |
| Cloud LLM | No |
| “Lie detection” | No |
| AI role | Contract auditor / attention mirror |
| AI control of hard lock | No |
| Open source | Yes |
| Payment | Free forever; pay after value later |
| “Life Returned” | Record concept now; design rigorously later |
| Marketing philosophy | Attention / agency / Epictetus / prosochē |

---

# 36. Product-manager summary

## Problem

People frequently open social apps without a deliberate decision, then remain inside environments designed to remove natural stopping cues.

Existing products often respond with static limits or hard blocks.

PROSOCHĒ will instead target the **moment intention disappears**.

## User

Someone who wants to keep an iPhone and its useful functions while reducing automatic, repetitive use of selected apps.

They are opting into friction.

They do not want another subscription or a moralizing productivity coach.

## Job to be done

> When I automatically reach for an app that repeatedly takes more attention than I intend, interrupt the habit strongly enough that I make an actual choice, and help me move toward what I meant to do instead.

## Value proposition

**PROSOCHĒ makes your phone wait for an intention.**

It is:

- free;
- open source;
- local;
- adaptive;
- self-configuring;
- user-owned;
- increasingly difficult to ignore only when behaviour warrants it.

## Product mechanism

1. User opens target app.
2. Shortcut receives OPEN.
3. Local JSON state is loaded.
4. Heat decays/increases according to recent behaviour.
5. Gravity reflects accumulated use.
6. Pressure determines Circle.
7. Circle applies appropriate friction.
8. At stronger Circles, user states an intention and boundary.
9. PROSOCHĒ may redirect to one of six exits.
10. CLOSE records actual session duration.
11. Behavioural outcomes affect future Heat and exit learning.
12. Sentient can reflect patterns back to the user using only local telemetry.

## Why this is different

It does not optimize solely for “less screen time.”

It optimizes for:

**more deliberate use, fewer automatic returns, better contract fidelity and more attention available for the life the user says they want.**

## Product forks

### Dumb

Deterministic.

Broad compatibility.

The scientific/control baseline.

### Sentient

Same engine plus on-device behavioural interpretation.

Increasingly personalized and context-aware.

The model is a mirror, not the enforcement authority.

## Data architecture

### JSON

Fast state.

### Note

Human memory, manifesto, setup and readable history.

No CSV.

## Onboarding

Keep native import questions simple.

Use a pre-filled Note proforma for the richer questions:

- What is your phone for?
- Which apps take more attention than intended?
- What do you want the reclaimed attention for?
- What exits would genuinely be better?
- What does deliberate leisure mean to you?

Sync this profile into JSON.

## Six exits

- **Capture** — externalize an idea.
- **Coordinate** — turn mental load into a plan.
- **Create** — make something.
- **Connect** — contact a person rather than consume a social feed.
- **Consult** — satisfy a specific information need directly.
- **Close** — no phone is the next action.

Learn locally which exit actually prevents rapid return.

## Core metric

Rapid-return rate.

Secondary:

- contract fidelity;
- target-app session duration;
- intervention/exit success;
- disablement.

## Research basis

The design is consistent with evidence showing:

- purpose and autonomy matter more than raw screen time alone;
- planning and self-efficacy are relevant mechanisms;
- personalized just-in-time nudges can reduce targeted use;
- friction and an explicit opportunity to exit can substantially reduce app openings;
- grayscale can act as useful design friction;
- the intention/actual-use gap may be a particularly useful behavioural signal.

The evidence does **not** prove Nine Circles.

The prototype exists to test the combined architecture.

## Commercial model

Not freemium.

Not subscription-gated.

Not advertising.

Not data monetization.

Future:

**free forever, pay after value.**

Only ask for support after the user's own local metrics show meaningful value.

## Philosophy

PROSOCHĒ is ultimately not about Instagram.

It is about the practice of attention.

The ancient Stoic concept of *prosochē* treated attention as something cultivated through repeated practice.

Modern devices have become extraordinarily good at removing the interval between impulse and action.

PROSOCHĒ puts that interval back.

## Definition of success

The best outcome is not that the user reaches Circle IX every day.

It is the opposite.

Over time:

- fewer automatic opens;
- fewer rapid returns;
- more bounded deliberate sessions;
- lower Heat;
- fewer high-Circle interventions;
- the phone returns to being a tool.

The endpoint is that PROSOCHĒ gradually has less work to do.

---

# 37. Primary sources and research references

## Apple / technical

Apple Support — What's new in Shortcuts for iOS, iPadOS, macOS, watchOS and visionOS 26  
https://support.apple.com/en-au/125148

Apple Support — Setting triggers in Shortcuts on iPhone or iPad  
https://support.apple.com/en-ca/guide/shortcuts/apde31e9638b/ios

Apple Support — Enable or disable a personal automation in Shortcuts  
https://support.apple.com/en-au/guide/shortcuts/apd602971e63/ios

Apple Support — Intro to personal automation  
https://support.apple.com/en-gb/guide/shortcuts/apd690170742/9.0/ios/26

Apple Support — Use Apple Intelligence in Shortcuts on iPhone  
https://support.apple.com/guide/iphone/use-apple-intelligence-in-shortcuts-iph78c41eaf8/ios

Apple Support — Share actions / Append to Note  
https://support.apple.com/en-au/guide/shortcuts/apdaf74d75a5/ios

Apple Support — Create a new personal automation  
https://support.apple.com/en-gb/guide/shortcuts/apdfbdbd7123/9.0/ios/26

Shortcuts Playground  
https://github.com/viticci/shortcuts-playground-plugin

## Behavioural / digital wellbeing

Lukoff K, Yu C, Kientz J, Hiniker A. *What Makes Smartphone Use Meaningful or Meaningless?* Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies. 2018.  
https://doi.org/10.1145/3191754

Keller J, Roitzheim C, Radtke T, Schenkel K, Schwarzer R. *A Mobile Intervention for Self-Efficacious and Goal-Directed Smartphone Use in the General Population: Randomized Controlled Trial.* JMIR mHealth and uHealth. 2021.  
https://pubmed.ncbi.nlm.nih.gov/34817388/

*Promoting Self-Regulated Social Media Use on Smartphones With a Mobile Intervention App (Wellspent): Randomized Controlled Trial.* JMIR mHealth and uHealth. 2026.  
https://pubmed.ncbi.nlm.nih.gov/41950504/

Grüning DJ, Riedel F, Lorenz-Spreen P. *Directing smartphone use through the self-nudge app one sec.*  
https://pmc.ncbi.nlm.nih.gov/articles/PMC9974409/

Zimmermann L, Sobolev M. *Digital Strategies for Screen Time Reduction: A Randomized Field Experiment.* Cyberpsychology, Behavior, and Social Networking. 2023.  
https://pubmed.ncbi.nlm.nih.gov/36577008/

Almoallim S, Sas C. *Toward Research-Informed Design Implications for Interventions Limiting Smartphone Use: Functionalities Review of Digital Well-being Apps.* JMIR Formative Research. 2022.  
https://pubmed.ncbi.nlm.nih.gov/35188897/

*Suffering from problematic smartphone use? Why not use grayscale setting as an intervention! — An experimental study.* Computers in Human Behavior Reports. 2023.  
https://doi.org/10.1016/j.chbr.2023.100294

*Before You Scroll Again: Predicting Regretful Social Media Sessions from In-the-Wild Contextual and Wearable Sensing.* 2026 preprint. Treat as emerging evidence, not established clinical fact.  
https://arxiv.org/abs/2606.08965

Wu R et al. *MindShift: Leveraging Large Language Models for Mental-States-Based Problematic Smartphone Use Intervention.* 2023 research preprint.  
https://arxiv.org/abs/2309.16639

## Philosophy

Epictetus, *Enchiridion*, Chapter 1 — distinction between what is and is not in our control.  
https://classics.mit.edu/Epictetus/epicench.html

Epictetus, *Discourses*, Book IV, Chapter 12 — On Attention.  
https://en.wikisource.org/wiki/The_Discourses_of_Epictetus%3B_with_the_Encheiridion_and_Fragments/Book_4/Chapter_12

---

# 38. Final instruction to the build agent

Treat this file as the canonical product strategy.

Where earlier conversation ideas conflict with this document, this document wins.

Do not expand scope with Focus, NFC, CSV, cloud AI or Screen Time blocking.

Do not simplify the product into a timer.

Build the deterministic behavioural engine first.

Build the Dumb fork until it is reliable.

Fork it into Sentient and layer the On-Device model onto the same deterministic state machine.

Preserve the core idea throughout implementation:

**PROSOCHĒ is not trying to make the phone unusable.**

It is trying to make unconscious use progressively harder than conscious choice.

The strongest version of the product is one that, over time, intervenes less because the user has learned to arrive at the phone with an intention.
