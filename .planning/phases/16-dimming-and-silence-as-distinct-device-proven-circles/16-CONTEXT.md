# Phase 16: Dimming and Silence as distinct device-proven Circles - Context

**Gathered:** 2026-08-17
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss)

<domain>
## Phase Boundary

Prove Dimming and Silence work as **distinct, device-verified Circles with reliable
capture-and-restore** — the outstanding half of Phase 9, which merged its code untested.

**Two things are true and the second is the risk.** They are built and merged: Phase 9
landed the numeric-coercion fix for all 28 `setbrightness` (14) / `setvolume` (14) operand
sites (`2e2261e`, artifacts in `c6d8737`), and Phase 10 pinned the whole surface with
`docs/environmental_restore_check.py` so it cannot be removed by accident. **But they have
never run on a phone, and the merge made them live** — before the coercion fix these actions
silently no-opped; now they actually change brightness and volume, and the code that puts
them back has never once executed on hardware. `09-UAT.md` has 12 tests; exactly one has
passed — test 1, the static "coercion chip does not render red" gate.

**The coercion shape itself is analogy-based, not donor-confirmed.**
`WFCoercionVariableAggrandizement` / `CoercionItemClass: WFNumberContentItem` is confirmed
for the Donor-4.1 *conditional operand* position; whether it is correct at a **direct
Set-action parameter** position is genuinely unknown. `Donor 10.shortcut` contains no
variable-fed `WFBrightness`/`WFVolume` example. If it proves wrong, follow `09-RESEARCH.md`'s
fresh-donor protocol — build a donor on device with a variable-fed Set Brightness and decrypt
it. **Do not guess a second `CoercionItemClass`.**

**Deliverables.** Run `09-UAT.md` tests 2–12 on a real iPhone. The closed-loop proof is what
matters: `Get Device Details` returns a real, correctly-typed value; the has-any-value guard
correctly *skips* the change when the read returns nothing; CLOSE restores the original
exactly. **Then the ugly cases** — app force-quit mid-session, device restart mid-session,
CLOSE never firing, two overlapping sessions, screen locked mid-session. Each must restore or
leave the user at a safe value. Never dark. Never silent forever. Never loud. Emergency
Restore must recover from every failure mode found, and it has itself never been tapped on a
device.

**DEV-06 is live again** — `changed_at` / `changed_by_session_id` are written at 20 sites and
read nowhere. That was recorded MOOT conditional on the cut proceeding; the cut is cancelled,
so DEV-06 and the `Session ID` scope defect both return. `docs/BUILD-NOTES.md` §17 reserves
the DEV-06 decision to the user — surface it, do not decide it unilaterally.

**The brightness floor was corrected and needs a decision on main.** Phase 9 revised BD-02's
"never zero, 10–15% band": the user's on-device observation is that iOS's practical minimum
is dim, not black, so avoiding zero was never itself the safety property — capture-and-restore
reliability is. That revision was scoped to the experimental fork; decide it for main here.

Distinct-Circle allocation is already settled by **BD-06 Decision 4** — do not re-cut it.

**Severity:** major
**Requirements:** CIRC-03, CIRC-05, SAFE-01, SAFE-02, SAFE-03, SAFE-05, DIST-03
**Depends on:** Phase 12

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — discuss phase was skipped per user
setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide
decisions.

### LOCKED — decided by the user 2026-08-17, after research, before planning

- **D-01 — BD-02 brightness floor on main: the floor is 0, and the dim target follows it down.**
`safety.brightness_floor` `0.10 → 0` and `safety.dim_target` `0.12 → 0`. Dimming reaches the
device's true minimum (which iOS renders dim, not black — the on-device observation that
prompted the Phase 9 addendum). This makes the correction observable rather than inert: a
floor of 0 under an unchanged target of 0.12 would never bind.

Consequence, and it is not optional: `docs/environmental_restore_check.py:257` currently
asserts `dim_target > 0` **strictly**. That assertion encodes the very "never zero" clause the
Phase 9 addendum removed, so it must be relaxed to `>= 0`. The `dim_target >= floor` assertion
at `:259` stays exactly as it is. Do **not** weaken any other assertion in that checker while
in there. `docs/CAPABILITY-DECISIONS.md` BD-02 must be updated on the main line to record this
as decided, superseding the "10–15% band, never zero" text and promoting the Phase 9 addendum
from provisional to settled. The project CLAUDE.md `## Constraints` Safety bullet still
describes the relaxed floor as "provisional, not confirmed" and scoped to the experimental
fork — that is now stale and must be corrected too.

The safety property is unchanged and is the whole point: **capture-and-restore reliability**,
not floor avoidance. Which makes D-02 and the persistence defect the real safety work here.

#### D-01 site list — SUPERSEDED IN PLACE by the 2026-08-18 revision below

An earlier revision of this file asserted **"the measured count is NINE, not six"** and carried a
nine-row table. **That claim is retired.** It was the third of four successive counts, each of
which claimed completeness and each of which was wrong: six, then eight, then nine, then thirteen
or more. The table is not reproduced here, because reproducing a list that was presented as
complete and was not is exactly how the next reader repeats the mistake. Read the block below
instead; it is the current record.

Two findings from that earlier pass survive because they were measured and are still true, and
they are restated in the plans that own them:

- **`dimming()`'s emitted Shortcuts `comment()` ships.** `dimming()` has **no Python docstring**,
  so any instruction phrased as "update the function docstrings" does not reach it. Its first
  emitted action is a `comment()` whose middle bullet asserts a lower bound on the brightness
  write, and `primitive_dispatch()` renders that comment **eleven times per fork**. Measured
  2026-08-17: 11 occurrences in `src/PROSOCHE-Dumb.xml` and 11 in `src/PROSOCHE-Sentient.xml`.
  Without the fix both signed forks ship 22 user-visible comment actions asserting a bound the
  same build sets to zero — a false safety claim inside the product, not merely in its records.
  Plan 16-03 asserts a count of zero against the **rebuilt** artifact, and additionally asserts
  that the replacement states the property rather than a softer bound.
- **`silence()`'s parallel comment must NOT be edited.** Measured and confirmed:
  `tools/build_state_engine.py:618-621` states Media-only volume scoping and never-increase, which
  is SAFE-02 and remains true under D-01. The structural symmetry of `dimming()` and `silence()`
  is not a reason to change both; editing it would weaken a live safety statement that D-01 does
  not touch.

#### D-01 — the 2026-08-18 revision. This block is the current record.

The decision itself is **unchanged and remains LOCKED.** Only its blast radius, and how the work
is organised, changed. Four things were decided:

**1. The canonical strategy is FROZEN. It is out of scope and no task may edit it.**
`PROSOCHE_Nine_Circles_Canonical_Strategy.md` is a **historical design input, not a living spec.**
Its §21 floor clause stays exactly as written. Instead, `docs/CAPABILITY-DECISIONS.md` BD-02
records the supersession **explicitly**: that §21's floor clause is superseded on the main line by
D-01, that the canon is retained unmodified as the original design input, and that **BD-02 is the
authority where the two disagree.** This note is load-bearing rather than decorative — three of
the amended sites cite §21 as their authority, so without it the amended record does not cohere.
It is a named acceptance criterion of plan 16-05.

The same freeze applies to every other historical record. They are records of what was true then,
and rewriting them destroys the audit trail this project depends on. **Out of scope, do not edit:**
all closed prior-phase directories (`.planning/phases/01|05|09|10|11|12-*/`),
`.planning/debug/resolved/`, `.planning/todos/completed/`, `.planning/research/`, and `artifacts/`
(archived and signed; rewriting it would additionally invalidate the manifest digests).

**2. The work is SPLIT into a code plan and a record plan.**

- **`16-03` keeps the CODE change** (wave 2, unchanged): the two Config literal values, the two
  `docs/environmental_restore_check.py` assertion-side edits plus its narrative comment and its
  module docstring, `docs/phase5_self_check.py`'s per-action brightness assertion, and
  `dimming()`'s emitted `comment()` in `tools/build_state_engine.py`. Six CODE sites.
- **`16-05` is a NEW plan carrying the RECORD change** (wave 4): every documentation, requirement,
  roadmap and decision carrier, plus the repo-scoped gate. Twenty-one measured sites across nine
  files.
- The rebuild / re-sign / manifest / UAT / device-checkpoint plan was renumbered `16-05 → 16-06`
  and **remains the last wave**, because it closes D-MANIFEST and pins build identity.

The rationale the user endorsed: **the safety-critical code fix must not be held hostage to a
documentation sweep that has already failed four times.**

**3. Why enumeration kept failing, and what ends it. The class is not purely lexical.**

Proved directly:

```
grep -niE "never zero|strictly positive|10-15%|brightness_floor|dim_target" docs/phase5_self_check.py
  → ZERO matches
```

…yet `docs/phase5_self_check.py:117` is a confirmed site — it encodes the retired rule as a
**value check with none of the vocabulary**. So **no grep gate, however well written, can be the
complete answer, and no single enumeration pass has proven trustworthy.**

The plans therefore combine two instruments and present **neither alone as complete**:

- a **mechanical gate** for the lexical majority — a new standalone `docs/*.py` checker (plan
  16-05, task 3) that greps live files, fails listing every survivor with file and line, carries
  its exclusions as an **explicit commented allowlist** so a reader can see what was deliberately
  spared and why, and carries a comment stating plainly that it **cannot catch non-lexical
  encodings**, citing `docs/phase5_self_check.py:117` as the known instance so nobody later
  mistakes a green gate for proof the class is empty. It also carries the positive cross-check
  that `src/CONFIG-BLOCK.md`'s fenced JSON and the built forks' Config literal agree on both keys
  — the assertion that would have caught the `CONFIG-BLOCK.md` miss mechanically. It is registered
  in `16-VALIDATION.md`'s full-suite command and in plan 16-06's verify chain.
- an **explicit human-reasoned list** for the non-lexical residue, carried in plan 16-05's
  `<measured_site_list>` section.

**4. The site list is MEASURED, not proven exhaustive — and the plans say so in their own text.**
Re-measuring during this revision found **four sites appearing in no prior enumeration**: a
*second* site in `.planning/PROJECT.md` (a file whose first site was already listed), two more in
`.planning/ROADMAP.md`, and one in `.planning/STATE.md`. That is the fifth undercount, caught
before execution rather than after. The gate is what makes a sixth **visible** rather than silent.

- **D-02 — DEV-06: remove `changed_at` and `changed_by_session_id` entirely.** Decided by the
user via `ponytail`, on the standard "if the functionality doesn't need it, get rid of it".

The trace behind the decision, so it is not re-litigated: there are **zero** consumers. No
`read_value` targets either field anywhere in either fork. The only non-write references are
the explanatory comment at `tools/build_state_engine.py:472`, the bootstrap seed shape at
`:2759-2760`/`:2778`, and the seed-shape assertion at `docs/phase5_self_check.py:108`. The
failure modes this phase exists to prove do not need them either — overlapping sessions is
already guarded by `if_block("<group> Snapshot", 100)` (has-any-value on the whole snapshot
dict, so a second session short-circuits to `nothing` and never overwrites a live original),
and every restore path gates on `original_value > 0`. Neither guard consults identity or time.

Removal is therefore a **three-site coordinated generator change**, not a delete of the writes
alone: (a) the `set_value` writes in the capture arms, (b) the seed shape and
`SNAPSHOT_SEEDED_EMPTY`, (c) the `phase5_self_check.py` assertion. Per the project convention
"fix whole classes, never site-by-site", do it once at the generator level and let both forks
regenerate. Removing a seeded leaf is safe **only because there is no reader** — CLAUDE.md's
verified runtime semantics make a dotted read of a missing segment a hard error, so the
regression check to keep is "no `read_value` targets a removed leaf".

### Explicitly NOT at Claude's discretion (carried from the ROADMAP goal)

- **A second `CoercionItemClass`** must never be guessed. If `WFNumberContentItem` proves
  wrong at the direct Set-action parameter position, follow `09-RESEARCH.md`'s fresh-donor
  protocol instead.
- **Distinct-Circle allocation** is settled by BD-06 Decision 4 — do not re-cut it.
- **No device result may be fabricated.** Anything untested on hardware is recorded as BLOCKED
  with its real reason — and the reason must be the true one. See the corrected DIST-03 status
  immediately below.

### CORRECTION — the DIST-03 reason, re-measured 2026-08-17 during planning

An earlier draft of this file (and `16-RESEARCH.md`) asserted `xcrun devicectl list devices` →
`No devices found.` **That was true at session start and is no longer true.** Re-measured:

```
dougal | 8E45671C-9E4D-54C9-AC19-2EB65747337E | available (paired) | iPhone16,1
tunnelState: disconnected | pairingState: paired | transport: wired | osVersion: 26.6
```

A **paired iPhone 15 Pro on iOS 26.6, wired, with no live tunnel.** Substantively DIST-03 still
blocks an autonomous run — there is no connected session to drive, and Personal Automations are
user-created on the device regardless — but "No devices found." would be recording something
false, which this project forbids exactly as firmly as a false pass. The blocked reason is
**"paired device present, `tunnelState: disconnected`; no live session to drive"**, not "no
device exists".

Two consequences that matter:

- `iPhone16,1` is **Apple-Intelligence-capable**, so this hardware can exercise the Aware
  (Sentient) fork when a session is arranged — the device split in `## Constraints` is satisfied.
- iOS **26.6** is inside the declared `iOS 26.x` target, so an observation on it is
  same-major-version evidence, not an extrapolation.

Any executor re-measuring this must branch on `tunnelState` from the JSON output, **not** on the
`State` column (which reads `available (paired)` even with the tunnel down), and must record the
output verbatim.

### Hard environmental constraint at plan time — ⚠ SUPERSEDED IN PLACE 2026-08-18

**Read the CORRECTION block immediately above this one; it is the authority. This block's first
sentence is FALSE and is retained only so the correction has something to point at.**

The `No devices found` claim below was true at the start of the 2026-08-17 session and was
already false by the time the correction above was measured. It survived here, *after* its own
correction, which meant an executor reading this file top-to-bottom met the retired claim
**second** and could reasonably have taken it as the later word. Marked superseded rather than
deleted, per this project's standing rule that a record of what was believed is worth more than
the space it costs — but **the corrected reason is "paired device present, `tunnelState:
disconnected`; no live session to drive", not "no device exists".**

Points 1, 2 and 3 at the end of this block are unaffected by the correction and remain in force.

~~`xcrun devicectl list devices` reports **No devices found** (checked 2026-08-17, this run).~~
The same DIST-03 blocker recorded against Phases 4, 9, 10 and 12 is still in force — **for the
corrected reason above.** The
device-proving half of this phase (09-UAT tests 2–12, the five failure-mode trials, the
Emergency Restore tap) **cannot be executed by an autonomous run**. Plans must:

1. Do all non-device work in full — static/structural proof, checker coverage, the UAT
   instrument itself, the decisions the ROADMAP reserves.
2. Record device-gated tests as BLOCKED with a real reason, never as passed or inferred.
   Precedent: Phase 10 DIST-03, Phase 12 `verification_deferred_human`.
3. Escalate no higher on the CLAUDE.md §9 evidence ladder than the open question requires —
   rung 1 (file-level) and rung 2 (simulator) work should be exhausted here so the eventual
   device session is not spent on questions a free rung could have settled.

</decisions>

<code_context>
## Existing Code Insights

### Phase 13 is merged; the P0 was re-verified against the merged tree

This branch merged `main` at 45 commits on 2026-08-17, bringing in Phase 13 (red-operator
conditionals + the `WFItems` List wrapper), which moved `tools/build_state_engine.py` by 293
lines and rewrote both fork XMLs. `16-RESEARCH.md` was authored **before** that merge, so its
action indices were re-measured afterwards. **They are unchanged, and the P0 stands:**

| Measurement | Pre-merge (research) | Post-merge (re-verified) |
|---|---|---|
| Last `State` save on the OPEN arm | index 521 | index 521 |
| `universal_leaving()` start | index 524 | index 524 (comment confirms) |
| Saves after 728 | `Reloaded State` | `Reloaded State` |
| `setbrightness` / `setvolume` sites per fork | 15 / 15 | 15 / 15 |
| Numeric coercion present | 15 / 15 brightness, 4 / 15 volume | 15 / 15 brightness, 4 / 15 volume |

Every `settings_snapshot.*.original_value` write that records a real capture sits at index 1012
or later — i.e. **after** the last `State` save at 521 — and every save from 728 onward targets
`Reloaded State`, a different dictionary. So the capture is written into a dictionary that is
never persisted. CLOSE and Emergency Restore read the file, find the cleared sentinel, fail the
`> 0` gate, and skip. **The screen dims and nothing in the product un-dims it.** Same on the
MANUAL `Test a Circle` path.

Two consequences the plan must respect:

1. **Fix persistence before any device session.** Running `09-UAT.md` tests 2–12 now would
   spend a scarce device session re-proving a defect a script already proves, and would leave
   the user's phone dim. The persistence fix is autonomous work that needs no hardware.
2. **The 11-of-15 uncoerced `setvolume` sites are a separate, real finding.** Brightness is
   15/15 coerced; volume is 4/15. `docs/environmental_restore_check.py` deliberately does not
   assert a coercion count (see its own comment), so nothing catches this. Whether the 11
   uncoerced sites are correct depends on the same open question as D-03 — resolve them
   together, do not "fix" them by pattern-matching brightness.

The ROADMAP's "28 operand sites (14 + 14)" is stale — it is 30 (15 + 15) per fork as shipped.

### Known anchors from prior phases that this phase builds on

- `09-UAT.md` — 12 tests, 1 passed (static coercion-chip gate), 11 outstanding.
- `09-RESEARCH.md` — carries the fresh-donor protocol for an unconfirmed `CoercionItemClass`.
- `docs/environmental_restore_check.py` — Phase 10 structural pin over the 28 operand sites.
- `docs/BUILD-NOTES.md` §17 — the DEV-06 reservation.
- `docs/CAPABILITY-DECISIONS.md` BD-02 (+ Phase 9 addendum) — the brightness-floor correction
  scoped to the experimental fork, pending a main-line decision here.
- `docs/CAPABILITY-DECISIONS.md` BD-06 Decision 4 — settled distinct-Circle allocation.
- `tools/build_state_engine.py`, `tools/build_sentient.py` — the two fork generators; the
  provenance guard (`git merge-base --is-ancestor 7ca8ebb HEAD`) gates both.

</code_context>

<specifics>
## Specific Ideas

No specific requirements — discuss phase skipped. Refer to ROADMAP phase description and
success criteria.

</specifics>

<deferred>
## Deferred Ideas

None — discuss phase skipped.

</deferred>
