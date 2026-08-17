---
phase: 16-dimming-and-silence-as-distinct-device-proven-circles
plan: 06
subsystem: distribution-and-device-instrument
tags: [D-MANIFEST, re-sign, decrypt-verify, device-instrument, DIST-03, CAP-08, blocked, human-needed]
status: complete
requires:
  - "16-01: the capture-persistence fix — the reason a device session now tests something new"
  - "16-02: CAP-08 and the retirement of the coercion-chip gate — both of which shape how the instrument had to be written"
  - "16-03: D-01's code half — the floor and target of 0 this rebuild ships"
  - "16-04: D-02's leaf removal — the state shape the instrument's test 12 asserts"
  - "16-05: docs/retired_clause_check.py — run here so it gates rather than sweeps"
  - "tools/build_sentient.py::CORE_NAME, AWARE_NAME — the display names, read not typed"
provides:
  - "artifacts/shortcuts/: both forks re-signed at commit 04f3612 under their exact existing display names, decrypt-verified"
  - "artifacts/shortcuts/MANIFEST.md: six refreshed rows + a new leading narrative paragraph; docs/manifest_check.py GREEN — constraint D-MANIFEST closed"
  - ".planning/phases/16-*/16-UAT.md: a cold-runnable, build-pinned, 12-test device instrument"
  - ".planning/phases/16-*/COVERAGE.md: the reasoned no-external-API declaration"
  - "the re-measured DIST-03 reason, recorded in three live carriers"
affects:
  - ".planning/phases/09-*/09-UAT.md — superseded by banner; its single recorded pass explicitly does not carry forward"
  - ".planning/STATE.md — standing device backlog and blocker reason corrected (content only, no bookkeeping)"
  - ".planning/phases/16-*/16-RESEARCH.md — the stale 'No devices found.' assertion retired in place"
tech-stack:
  added: []
  patterns:
    - "read the display names from the generator's own constants, never type them"
    - "decrypt-verify what shipped, never trust the source plus a file timestamp"
    - "supersede in place, never delete — struck text keeps the correction anchored"
    - "the pin is only real if the check demands a full 64-character digest"
    - "verify the value applied, never the absence of an error (CAP-08)"
key-files:
  created:
    - .planning/phases/16-dimming-and-silence-as-distinct-device-proven-circles/16-UAT.md
    - .planning/phases/16-dimming-and-silence-as-distinct-device-proven-circles/COVERAGE.md
    - artifacts/shortcuts/2026-08-18/PROSOCHĒ — Nine Circles — Core-094139.xml
    - artifacts/shortcuts/2026-08-18/PROSOCHĒ — Nine Circles — Aware-094152.xml
  modified:
    - artifacts/shortcuts/MANIFEST.md
    - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut
    - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut
    - .planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md
    - .planning/STATE.md
    - .planning/phases/16-dimming-and-silence-as-distinct-device-proven-circles/16-RESEARCH.md
decisions:
  - "The checkpoint resolved BLOCKED on a re-measured tunnelState of 'unavailable' — a THIRD distinct value, recorded as measured rather than as planned"
  - "16-UAT.md Test 1 replaces the chip gate with an applied-value observation, because 16-02 showed the chip carries no information at a direct Set-action parameter"
  - "The locked-screen case is handed to Phase 18 by reference and is deliberately not a test here"
metrics:
  duration: ~55m
  completed: 2026-08-18
  tasks: 3
  commits: 3
  files: 9
requirements: [CIRC-03, CIRC-05, SAFE-01, SAFE-02, SAFE-03, SAFE-05, DIST-03]
---

# Phase 16 Plan 06: Close the phase — re-sign, refresh, instrument, and hand over honestly Summary

Both forks ship rebuilt and re-signed under unchanged display names with their decrypted
payloads proven byte-identical to source, the entire static suite is green for the first time
since wave 1, and a twelve-test device instrument pinned to those exact artifacts exists — with
every device-gated claim recorded as BLOCKED on a reason that was re-measured rather than
copied.

## The headline: the phase ends at `human_needed`, and that is the correct outcome

**Everything this phase shipped is structurally proven and behaviourally unproven.** The
capture-and-restore loop has still never executed on hardware and Emergency Restore has still
never been tapped on a device. Precedent: Phase 10's DIST-03 resolution, Phase 12's and Phase
13's `verification_deferred_human`.

Pitfall 1 — the ordering argument this whole phase rests on — paid off exactly as predicted.
Opening with "run the eleven outstanding tests" would have dimmed a tester's phone, found that
CLOSE does not restore, found that Emergency Restore does not restore either, and ended with a
known result and a dim phone. The persistence defect was fixed first, the artifacts re-signed,
and the instrument pinned to the new build — **so the device session, when it happens, tests
something new.**

---

## Task 1 — the rebuild, the re-sign, and D-MANIFEST

### Build provenance and determinism

The guard ran before either generator: `git merge-base --is-ancestor 7ca8ebb HEAD` → exit 0.

Both generators then ran and **`git status` was empty afterwards** — the tree already held
byte-identical output from wave 4, so this rebuild is reproducible rather than run-specific.
That is worth stating because it means the digests below are a property of the generator at
this commit, not of this particular invocation.

### The six refreshed rows, measured from disk after signing

| Row | Path | Bytes | SHA-256 |
|---|---|---:|---|
| Core source | `src/PROSOCHE-Dumb.xml` | 2854976 | `e2da2742e662263e972fb3621dec33fd965bdcfb21deb67a8e8bd3d1d6d4da29` |
| Core archive | `artifacts/shortcuts/2026-08-18/PROSOCHĒ — Nine Circles — Core-094139.xml` | 2854976 | `e2da2742e662263e972fb3621dec33fd965bdcfb21deb67a8e8bd3d1d6d4da29` |
| **Core signed** | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` | **230232** | `9b0f261488beb396d01f8cf63fc539d4ef1f25063ddf6baad8d5569a055a2e7c` |
| Aware source | `src/PROSOCHE-Sentient.xml` | 2891657 | `b3f8b9cbbf85ca4a819279de65aa18891ac97f87c3acdfcb4052f16ceb548443` |
| Aware archive | `artifacts/shortcuts/2026-08-18/PROSOCHĒ — Nine Circles — Aware-094152.xml` | 2891657 | `b3f8b9cbbf85ca4a819279de65aa18891ac97f87c3acdfcb4052f16ceb548443` |
| **Aware signed** | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` | **234623** | `1db5c1ef0cf50862128ad45686600be8f144b1d5b88661582f43f5a93c1d93b6` |

Each dated archive is byte-identical to its `src/` counterpart, which is what makes it a
pre-sign record rather than a copy of something else.

### Signed-name discipline — asserted against the constants, not typed

The two names were read at run time from `tools/build_sentient.py`'s `CORE_NAME` / `AWARE_NAME`
and passed straight to `sign-shortcut --name`. Asserted after signing, per fork:

```
'PROSOCHĒ — Nine Circles — Core.shortcut':  exists=True bytes=230232 magic=b'AEA1'
    basename_equals_display_name=True suffix_free=True
'PROSOCHĒ — Nine Circles — Aware.shortcut': exists=True bytes=234623 magic=b'AEA1'
    basename_equals_display_name=True suffix_free=True
```

Both signer quirks that `sign-shortcut` auto-retries were **not encountered** — each fork signed
on the first attempt.

### Decrypt-verification — what actually shipped

Both containers were round-tripped through the AEA1 recipe (`aea decrypt` → `aa extract` →
`plistlib`) and compared against the built sources:

| Fork | Recovered actions | Built actions | First five identical | **Full list identical** | `WFWorkflowName` in recovered plist |
|---|---:|---:|---|---|---|
| Core | **4302** | 4302 | yes | **yes** | **absent** — stripped by the signer |
| Aware | **4370** | 4370 | yes | **yes** | **absent** |

The plan asked for the action counts and the first five actions. **The full action lists were
compared instead and are byte-identical**, which is strictly stronger and costs nothing.

Both counts match plan 16-04's post-removal figures exactly (4390 − 88 = 4302; 4458 − 88 =
4370), so the phase's net −44 per fork (+44 from 16-01, −88 from 16-04) is confirmed on the
**decrypted payload** rather than on `src/`.

`WFWorkflowName` being absent from both recovered plists re-confirms, on this build, why the
filename discipline is load-bearing rather than cosmetic: **the signed artifact carries no
display name internally at all**, so a rename would silently break the user's two Personal
Automations with no mechanism anywhere able to re-point them.

### The static suite — green, including the two gates that mattered

Every checker exits 0:

| Checker | Result |
|---|---|
| `state_engine_self_check` | exit 0 |
| `phase5_self_check` | `phase5 self-check: passed` |
| `phase6_self_check` | `phase6 self-check: passed` |
| `phase7_self_check` | `phase7 self-check: passed` |
| `phase9_self_check` | exit 0 — `site_audit: passed (30/30 sites audited, 19 coerced, 11 correctly not)`; `capture_persistence_negative_control: passed` |
| `environmental_restore_check` | `environmental restore check: passed` |
| `sequence_dispatch_check` | passed — 0 orphans, 0 unreachable, 0 unknown semantics, 0 duplicates |
| `note_identity_check` | passed both forks — three identity sites agree on `PROSOCHĒ`, 0 attachment-offset mismatches |
| `sentient_core_check` | passed |
| `sentient_audit_check` | passed |
| **`retired_clause_check`** | passed — 0 live lexical occurrences; CONFIG-BLOCK agrees with both forks on `brightness_floor=0`, `dim_target=0` |
| **`manifest_check`** | **`manifest check: passed (6 rows verified against disk)`** |

**`docs/retired_clause_check.py` ran here on purpose.** Plan 16-05 created it; a gate that only
ever runs in the plan that created it is a sweep, not a gate. It is now in a phase-close verify
chain.

**Constraint D-MANIFEST is CLOSED.** `docs/manifest_check.py` had been deliberately red since
plan 16-01's first rebuild. It went green by **re-signing and then refreshing the rows from
disk** — never by editing a row to match a stale artifact. Its last red output before the fix,
for the record: `row 'Core source': MANIFEST declares 2901248 bytes, src/PROSOCHE-Dumb.xml is
2854976 bytes`.

### Gate A — mandatory, clean

| Fork | Command | Result |
|---|---|---|
| Core | `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` | `Validation passed.` **exit 0** |
| Aware | `validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all` | `Validation passed.` **exit 0** |

### Gate B — advisory, recorded verbatim, chained into nothing

Run standalone per fork. **Exactly one waived line each and nothing else.**

**Core** (`--target-macos 27 --target-platform all`), exit 1:

```
Validation failed:

First failing action: index 0 (is.workflow.actions.comment)
Snippet: {'WFCommentActionText': 'PROSOCHE - Nine Circles (Dumb fork). This shortcut is the whole product: it reads two setup answers from import, checks for a saved setup file, creates one on first run along with a setup note, and opens that not...

- Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index 4148: WFCreateNoteInput. ToolKit v78 expects: OpenWhenRun, contents, folder, interpretAsMarkdown, name.
```

**Aware**, exit 1:

```
Validation failed:

First failing action: index 0 (is.workflow.actions.comment)
Snippet: {'WFCommentActionText': 'PROSOCHE - Nine Circles (Dumb fork). This shortcut is the whole product: it reads two setup answers from import, checks for a saved setup file, creates one on first run along with a setup note, and opens that not...

- Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index 4216: WFCreateNoteInput. ToolKit v78 expects: OpenWhenRun, contents, folder, interpretAsMarkdown, name.
```

Both are the single permanent `WFCreateNoteInput` waiver, at the indices plan 16-04 measured
(**4148** / **4216**) — unmoved, which independently corroborates that this rebuild changed no
action count. **No line outside the waiver was reported on either fork**, so there is no finding
to investigate. Gate B was never `&&`-chained into a success condition; it is permanently exit 1
and structurally incapable of being a definition of done.

### The manifest's new narrative paragraph

Appended in the file's established form as the **new leading paragraph**, with no earlier
paragraph deleted. It names this rebuild's three changes (16-01's capture persistence, D-01's
floor and target reaching zero with the 11-per-fork false safety comment removed, D-02's
snapshot-leaf removal), gives the net −44 action delta with its derivation, records gate A clean
and gate B's waiver indices, and retains **the superseded phase-13 CR-01 rows** so a reader can
identify a build already on a device.

Two further corrections were made in the same file, and both are Rule 2 rather than
housekeeping — see Deviations.

---

## Task 2 — the instrument

### `16-UAT.md`, and the four things that make it more than a checklist

**1. It is pinned, and the pin is real.** The build-identity header carries the commit
(`04f3612`), both display names, both byte counts and **two distinct full 64-character SHA-256
digests**, each matched verbatim into a refreshed `MANIFEST.md` row. The plan's revised verify
demands full-length, distinct, and matched-in-full precisely because a looser hex pattern also
matches the pinned commit SHA the same instrument carries by design — a length-tolerant check
could have passed with **neither** fork digest present. A one-line `shasum -a 256` re-verification
recipe is included, and the file states plainly that a digest mismatch invalidates every outcome
below it.

**2. It is written around CAP-08, which changes what a brightness test may assert.**
`setbrightness.WFBrightness` is OPTIONAL and defaults to 50%, so an unresolved operand fails
**silently** rather than erroring. Every brightness test in the file therefore verifies **the
value actually applied**, and the instrument says in its own text that *"no error appeared" is
fully consistent with a silently defaulted 50%*, that such a test is a false-pass generator, and
that any outcome recorded in those terms must be treated as unrecorded.

**3. It removes work from the device session rather than only adding it.** A dedicated section
lists what was **already settled at rung 1 or 2 and must NOT be re-run on hardware**: the
coercion-chip gate (void — the coerced and uncoerced legs render identically, because
`Set Brightness` has no operator picker for a type mismatch to break, so `09-UAT.md`'s one
recorded pass *was never evidence about `WFBrightness` at all*); the 11 uncoerced `setvolume`
sites (correctly uncoerced, on name-scoped provenance, 11 + 4 = 15 exactly); the simulator import
channel; and the persist-before-apply ordering. It then states which questions are genuinely
device-gated and why nothing cheaper settles them, citing §9's rung-2 ceiling.

**4. Twelve numbered tests, contiguous, each with a blank `outcome:`.** Verified mechanically:
12 headings, numbered 1..12, with 12+ outcome fields counted separately so a shortfall in either
fails.

| # | Test | Why it is here |
|---|---|---|
| 1 | Coerced operand's applied **value**, via the spike-010 Breadcrumbs probe | The sharpened form of the retired chip question — observe 0.42 vs 0.66, not a chip |
| 2 | **A real capture VISIBLE in `state.json`** | The direct test for the persistence defect and **the one that would have caught it** |
| 3 | The has-any-value guard correctly **SKIPS** the change | A non-event is the pass; written for both reachable paths |
| 4 | Full capture → apply → restore against the **hand-recorded** originals | The phase's central claim; also `12-UAT.md` Test 3 |
| 5 | What `WFBrightness = 0` looks like on a real screen | Device input to D-01, a decision already taken on one unrepeated report |
| 6 | App force-quit mid-session | SAFE-03 |
| 7 | Device restart mid-session | The harshest persistence test — only what reached disk survives |
| 8 | CLOSE never fires | The most likely *silent* failure in ordinary use |
| 9 | Two overlapping sessions | Where the no-ownership-check reasoning meets hardware; carries the DEV-06 cross-check |
| 10 | **The compound trial — overlap plus force-quit of the winner** | Its own number, both modes named in the heading |
| 11 | Emergency Restore after **every** failure mode | It has never been tapped on a device; one outcome row per mode |
| 12 | Removed snapshot leaves absent from a fresh bootstrap | D-02's device half, plus the upgrade case and the Aware fork |

**Test 10 holds its own number and names both modes in its heading**, per Pitfall 4. The
instrument says why in its own text: Test 9 leaves a valid owner, Test 6 leaves a single unowned
session, and only the compound produces a snapshot that *no* CLOSE can ever reach — which is
precisely the state Emergency Restore exists for. A compound mode demoted to a footnote is a
compound mode never tested.

**The safety preamble is the first thing on the page**, before the header. It states that
brightness and volume will actually change, names iOS Settings as the only recovery, warns not
to begin if the phone is needed for ~90 minutes, and then states the live hazard plainly: **any
device already running a post-coercion-fix build is dim and quiet right now with no capture on
disk, and Emergency Restore cannot help it** — because it reads the same file as CLOSE and finds
the same cleared sentinel. That device must be restored by hand, and the instrument observes
that finding a phone in that state *is* the clearest possible statement of the defect this phase
fixed.

**The re-import precondition** explains why a stale install produces a false negative on nine of
the twelve tests, and — because a signed `.shortcut` carries no readable version — gives a
replace-don't-inspect procedure, plus the reminder that deleting a shortcut leaves both Personal
Automations pointing at nothing.

**The screen-locked case is handed to Phase 18 by reference and is NOT duplicated.** The
instrument names Phase 18 as the owner, cites its ROADMAP text ("the two should be investigated
together rather than twice"), names the two adjacent spikes, and makes one concrete handoff
request: that Phase 18's own instrument include a brightness or volume change in the locked
session.

**The batching note is in the header, as a table**, naming `12-UAT.md` Test 3, Phase 18, Phase
19, `13-UAT.md`, `10-UAT.md` and the already-built spike-010 Breadcrumbs probe, each with the
reason it batches here.

**The known-artifact list** records the three interim states that still ship — Circle 6
dispatching `Eject` where `Redirect` is designed (Phase 17), Circle 8's `Loud Mirror` being the
same implementation as Circle 7's `Mirror` (Phase 15), and `Black and White` shipping as an alert
rather than a real grayscale toggle (Phase 14) — so a blank or odd alert during the trials is
attributed correctly rather than blamed on Dimming.

**The Verdict placeholder** states its required shape: exactly one of **DEMONSTRATED SAFE** or
**RETIRED**, each citing test numbers per claim, with the note that a verdict citing no test
numbers is not a verdict.

#### One finding surfaced while writing the instrument

**With `dim_target = 0`, the already-dim short-circuit is unreachable for brightness.** The arm
fires when the captured reading is **≤** the dim target, and it sits inside an arm that already
requires the captured reading to be **> 0**; the two are now mutually exclusive. So every
dimming run on this build drives brightness to `0`.

This is **not a defect** — it is decision D-01 working exactly as specified (16-03 recorded the
same boundary from the other side: the floor now "binds exactly rather than never"), and the
shipped comment's surviving claim *"do not brighten an already dim screen"* stays true because a
target of 0 can never raise brightness. It is recorded in the instrument because it changes what
a tester should expect: Test 5's zero-brightness observation now happens on **every** dimming
run rather than occasionally.

### `COVERAGE.md`

The reasoned declaration, not a fabricated matrix: **no external API integration**, with the
reason given per component — local Python generators (stdlib only across all six plans), local
static checkers, local build tooling consulting **bundled** ToolKit snapshots, `xcrun devicectl`
enumerating devices attached to this Mac, and iOS action identifiers that are **on-device system
actions resolved by iOS at run time**, not network endpoints. It names why the detector fired
(trigger vocabulary — "capture", "restore", "returns a value"), inherits the product's own
no-network-surface constraint including On-Device-only AI, cross-references threat register entry
**T-16-32**, records that **zero external packages** were installed by any plan in this phase,
and closes by stating what it does **not** claim: nothing about device verification.

### `09-UAT.md` — superseded, not edited

A banner was added; **no test, no `result:` field and no line of the DEV-06 write-up was
touched.** It names `16-UAT.md` as its replacement and gives the three reasons: no
build-identity header, pre-rename fork names, and a test list predating the persistence finding
(no test in it looks at `state.json` for a capture, so it would have found the P0 only as a
cascade of unexplained restore failures).

**Its single recorded pass explicitly does NOT carry forward**, and the banner says why in
detail: Test 1 treated a non-red coercion chip as a hard gate cleared, and plan 16-02 — using a
deliberately-uncoerced control leg — measured that the coerced and uncoerced legs render
identically. Without that control leg, "the chip was not red" would have been recorded as a
pass and the pass would have been vacuous. **That is exactly what happened.** The banner also
notes that the DEV-06 write-up survives as *reasoning* (carried forward as the prediction
`16-UAT.md` Test 9 tests) but that D-02 has since closed the ownership question by removal
rather than by deferral.

---

## Task 3 — the checkpoint, resolved on the MEASURED state

### The measurement, verbatim, at execution time

```
$ xcrun devicectl list devices
Name     Hostname                  Identifier                             State         Model
------   -----------------------   ------------------------------------   -----------   --------------------------
dougal   dougal.coredevice.local   8E45671C-9E4D-54C9-AC19-2EB65747337E   unavailable   iPhone 15 Pro (iPhone16,1)

$ xcrun devicectl list devices --json-output <path>
tunnelState     = 'unavailable'
pairingState    = 'paired'
transportType   = None
osVersionNumber = '26.6'
productType     = 'iPhone16,1'
udid            = '00008130-00094480229A001C'
identifier      = '8E45671C-9E4D-54C9-AC19-2EB65747337E'
```

Measured twice — once at plan start and once again at the checkpoint — with identical results.

### The branch taken, and why

`tunnelState` is **`unavailable`**, not `connected`. **BLOCKED branch.**

**The reason has now moved twice, and this is the third distinct value.** `16-CONTEXT.md`'s
original block and `16-RESEARCH.md` both said `No devices found.`; the 2026-08-17 correction
measured `tunnelState: disconnected` with `transport: wired`; **today it is `tunnelState:
unavailable` with `transportType: none`** — the device is no longer even wired. The plan
anticipated `disconnected` and instructed that whatever was actually measured be recorded, which
is what was done.

**The true blocked reason is: "paired device present, `tunnelState: unavailable`,
`transportType: none`; no live session to drive"** — not "no device exists". Recording the older
wording would be recording something false, which this project forbids exactly as firmly as it
forbids a false pass.

**The `State` column is not the tunnel**, and this phase has already been bitten by it: on
2026-08-17 the column read `available (paired)` while `tunnelState` was `disconnected`. Every
carrier written by this plan says to branch on `tunnelState` from `--json-output`.

Two facts carried forward: **`iPhone16,1` is Apple-Intelligence-capable**, so this hardware can
exercise the **Aware** fork when a session is arranged, satisfying the device split in
`## Constraints`; and **iOS 26.6 is inside the declared `iOS 26.x` target**, so an observation on
it will be same-major-version evidence rather than an extrapolation.

Substantively DIST-03 would gate this work **even with a live tunnel**: Personal Automations are
user-created on the device and cannot be exercised anywhere else, at any effort.

### The blocked-branch record work

| Carrier | What was done |
|---|---|
| `16-UAT.md` | `status: blocked`, `blocked_on: DIST-03`; **all twelve tests' `outcome:` fields left blank**; the measured output recorded verbatim in a Reachability probe section; the iPhone16,1 / iOS 26.6 facts noted with their consequences |
| `.planning/STATE.md` | Standing device backlog re-headed by `16-UAT.md` with the full batching set; a new **authoritative** DIST-03 blocker entry carrying the measured reason; the three stale entries **struck in place, not deleted**, each pointing at the new one |
| `16-RESEARCH.md` | The `No devices found.` assertion **retired in place** with a boxed re-measurement note; the original struck rather than deleted so the correction has something to point at; the note states that points 1–3 of that block are unaffected and that the file's three other occurrences of the retired wording are retired by the same note |
| `16-CONTEXT.md` | **Re-verified, NOT re-applied** — see below |

### The `16-CONTEXT.md` re-verification, recorded as the plan required

The plan directed re-verifying the 2026-08-18 supersession marking rather than re-applying it.
**Measured, not assumed:**

```
:211  ### CORRECTION — the DIST-03 reason, re-measured 2026-08-17 during planning
:239  ### Hard environmental constraint at plan time — ⚠ SUPERSEDED IN PLACE 2026-08-18
:254  ~~`xcrun devicectl list devices` reports **No devices found** (checked 2026-08-17, this run).~~
```

**The marking is intact**: the correction block sits above the stale block, the stale block's
heading carries the supersession marker, and the retired assertion is struck through. **No edit
was made to `16-CONTEXT.md`.**

One nuance recorded rather than silently absorbed: that file's CORRECTION block states the
reason as `tunnelState: disconnected` / `transport: wired`, which today's measurement has moved
past. It is **not false** — it is a dated 2026-08-17 measurement and is labelled as one — and
`16-CONTEXT.md` is not among this plan's declared files, so it was left alone. **The current
record lives in `16-UAT.md`, `.planning/STATE.md` and `16-RESEARCH.md`**, all three written this
plan.

---

## Requirements — what this plan can and cannot claim

| Requirement | Status after this plan |
|---|---|
| **DIST-03** | **BLOCKED**, on the re-measured reason above. Both forks are signed, decrypt-verified and importable, but no import onto a real iPhone and no first manual run has occurred. |
| **CIRC-03, CIRC-05** | Structurally proven (16-01, 16-03, 16-04); the closed loop on hardware is **BLOCKED** — `16-UAT.md` Tests 2, 3, 4. |
| **SAFE-01** | D-01 is settled as a **decision** (16-03 code, 16-05 record). The claim that `0` renders dim rather than black is **BLOCKED** on one unrepeated user report — `16-UAT.md` Test 5. |
| **SAFE-02** | Media-only scoping and never-increase are unchanged and still asserted by `environmental_restore_check`; `silence()`'s comment was not edited by any plan in this phase. Device-unobserved. |
| **SAFE-03** | The five failure modes are **BLOCKED** — Tests 6, 7, 8, 9, 10. |
| **SAFE-05** | Emergency Restore is now structurally *capable* of restoring (16-01). It has **never been tapped on a device** — Test 11. **BLOCKED.** |

**No device-gated test was recorded as passed, inferred, or satisfied by a simulator, a static
check, or a decrypted artifact.**

---

## Deviations from Plan

### Auto-fixed issues

**1. [Rule 2 — missing critical functionality] The manifest's closing DIST-03 bullet asserted
something false, and was corrected**

- **Found during:** Task 1, while appending the new narrative paragraph.
- **Issue:** `MANIFEST.md` closed with *"`xcrun devicectl list devices` reports no devices, so no
  criterion in either UAT file has been exercised."* Unlike the paragraphs above it — each of
  which is a dated record of its own rebuild — that bullet is a **standing claim** in the
  distribution manifest, and it is now false. This plan's first prohibition is against recording
  a false device reason; leaving one live in the manifest while writing the corrected reason into
  three other files would have left the project's most-read provenance document contradicting
  them.
- **Fix:** the retired wording is **struck rather than deleted**, and the measured replacement is
  recorded beneath it with the full `tunnelState` / `pairingState` / `transportType` reading and
  the "read the JSON, not the State column" rule. No paragraph was deleted.
- **Files modified:** `artifacts/shortcuts/MANIFEST.md`
- **Commit:** `04f3612`

**2. [Rule 2 — missing critical functionality] A Phase 16 hazard bullet was added to the
manifest's `⚠` block**

- **Found during:** Task 1, same edit.
- **Issue:** every prior phase that shipped device-unproven behaviour added a `⚠` bullet naming
  it, so a reader deciding whether to import knows what is unproven in the build they are about
  to install. Phase 16 ships the most consequential such change yet — brightness and volume now
  actually change and the code that puts them back has never run — and would have had **no
  bullet at all**, breaking a convention every prior phase observed and omitting exactly the
  hazard a person most needs before importing.
- **Fix:** a bullet naming the three changes, stating the live already-dim-device hazard that
  Emergency Restore cannot help, stating that `dim_target` is now `0` and that the "dim, not
  black" report is unrepeated and untested, and pointing at `16-UAT.md`.
- **Files modified:** `artifacts/shortcuts/MANIFEST.md`
- **Commit:** `04f3612`

### Scope note

Both deviations are inside a file this plan already declares and modifies, and neither touches a
gate, a checker assertion, a count or a manifest **row**. The six rows were refreshed only by
re-measuring disk after re-signing.

### Two acceptance criteria satisfied more strongly than written

- The plan asked for the decrypt-verified **action count and first five actions** to match.
  **The full action lists were compared and are byte-identical** on both forks.
- The checkpoint anticipated `tunnelState: disconnected`. The measured value is
  **`unavailable`**, with `transportType: none`. The measured value is what was recorded, in
  every carrier.

---

## Authentication Gates

None.

## Known Stubs

None. No stub, placeholder, TODO, skipped test or unrun `<verify>` was introduced. Both task
verify blocks were run in full and passed, and gate B was run standalone on both forks and its
output recorded verbatim above.

The twelve blank `outcome:` fields in `16-UAT.md` are **not** stubs: an unrun device test
recorded as blank with its real blocked reason is this project's standing, deliberate policy —
`10-UAT.md`, `12-UAT.md` and `13-UAT.md` set the same precedent. A fabricated pass would be the
defect; a blank is the correct record.

## Threat mitigations applied

- **T-16-27** (critical, spoofing — a device-gated test recorded as passed on non-device
  evidence): mitigated. The checkpoint's decision rule was applied mechanically against
  `tunnelState` read from JSON; every device test is blank; the rung-2 results carried into the
  instrument keep their channel label and are explicitly marked *not to be promoted to device
  results*; `09-UAT.md`'s one recorded pass is explicitly retired rather than inherited.
- **T-16-28** (high, repudiation — a blocked reason copied from a stale document): mitigated. The
  reason was re-measured at execution time, found to differ from **both** the original claim and
  the planning-time correction, and recorded verbatim in three live carriers with the stale
  assertions struck in place rather than deleted.
- **T-16-29** (high, tampering — a fork re-signed under a changed display name): mitigated. The
  names were read from `build_sentient.py`'s constants and asserted against the signed basenames;
  both are exact and suffix-free, and `manifest_check`'s DIST-04 assertion re-proves it.
- **T-16-30** (high, tampering — a manifest row edited to match disk without re-signing):
  mitigated. Both forks were re-signed first and all six rows recomputed from disk in one pass;
  `manifest_check` proves every row; decrypt-verification proves the signed artifact matches the
  built source.
- **T-16-31** (high, DoS — a tester's phone left dim or quiet): mitigated in the instrument. The
  safety preamble is the first thing on the page, names iOS Settings as the recovery, warns about
  the already-dim-device hazard before any trial, and the restore trials are ordered so Emergency
  Restore is exercised **after each** failure mode rather than only at the end.
- **T-16-32** (low, information disclosure): accepted and re-recorded in `COVERAGE.md` — no
  network surface, no secrets, nothing leaves the device.
- **T-16-SC** (low, accepted): **no external package was installed.** Python usage is stdlib only
  (`hashlib`, `plistlib`, `struct`, `pathlib`, `subprocess`, `tempfile`, `json`, `re`, `sys`).
  The only subprocesses invoked are the pre-existing `sign-shortcut`, `validate-shortcut`,
  `openssl`, `aea`, `aa` and `xcrun`.

## Prohibitions honoured

- **No device-gated test recorded as passed, inferred, or satisfied by a simulator, a static
  check, or a decrypted artifact.** All twelve are blank.
- **Neither fork re-signed under any name other than the two exact existing ones** — asserted
  against the generator's constants, not typed.
- **`09-UAT.md`'s single recorded pass was NOT carried forward**, and the banner states why.
- **No manifest row was edited to match disk without re-signing** — the artifacts were re-signed
  first, then every row recomputed.
- **No API coverage matrix was fabricated**; `COVERAGE.md` declares the absence with its reason.
- **`09-UAT.md` was superseded, not edited** — banner only; no test, `result:` field or write-up
  line touched.
- **No progress, status or plan-count bookkeeping** was written to `STATE.md` or `ROADMAP.md` —
  the orchestrator owns those writes. `STATE.md`'s edits are content corrections the checkpoint
  explicitly directs.
- **No frozen path touched:** `PROSOCHE_Nine_Circles_Canonical_Strategy.md`, the closed
  prior-phase directories, `.planning/debug/resolved/`, `.planning/todos/completed/` and
  `.planning/research/` are all untouched. The one exception is `09-UAT.md`, which this plan
  declares in `files_modified` and which received a banner and nothing else.

## Device-gated work NOT done here (recorded, not inferred)

**The entire behavioural half of this phase.** Stated precisely so the next session does not
re-derive it:

1. **The capture-and-restore loop has never executed on hardware.** Structurally proven on both
   forks; behaviourally unknown.
2. **Emergency Restore has never been tapped on a device**, and until this build it was
   structurally incapable of restoring.
3. **`Get Device Details → Current Brightness` returning a usable, correctly-typed value on real
   hardware** is UNVERIFIED and inside §9's rung-2 ceiling.
4. **Whether `Set Brightness` consumes a Number-coerced operand at run time** is UNVERIFIED, and
   plan 16-02 established that **no further simulator effort will help** — the run-time channel
   cannot distinguish a resolved operand from an absent one.
5. **What `WFBrightness = 0` looks like on a real screen** rests on one unrepeated user report.
6. **The five failure modes and the compound trial** all require interrupting a live run.
7. **Both forks importing onto a real iPhone and completing a first manual run** — DIST-03's
   irreducible core.

All seven are **BLOCKED**: paired device present, `tunnelState: unavailable`, `transportType:
none`, no live session to drive. `16-UAT.md` is the instrument that settles them.

## Follow-up

- **The phase ends at `human_needed`.** That is the expected and correct outcome, not a failure.
- **One device session should discharge several debts** — `16-UAT.md`'s header carries the
  batching table: `12-UAT.md` Test 3, Phase 18's locked-screen investigation, Phase 19's
  nine-Circle sweep, `13-UAT.md`, `10-UAT.md` and the spike-010 Breadcrumbs probe.
- **Phase 18 owns the screen-locked case** and should include a brightness or volume change in
  its locked session, so the environmental restore is observed on that path in the same session.
- **If `16-UAT.md` is still blocked when Phase 19 runs, fold it in rather than dropping it.**
  Tests 2, 4 and 11 are what convert this phase from structurally-proven to actually-working, and
  Test 10 must not be demoted back into a footnote.
- **If Test 5 finds the screen effectively black and unusable**, that is a real finding against a
  LOCKED decision. Surface it to the user; D-01 is theirs to revisit.
- **If Test 1's coerced leg does not apply 0.42**, follow `09-RESEARCH.md`'s fresh-donor
  protocol. **Do not guess a second `CoercionItemClass`** — `assert_probe_shape.py` fails the
  build if one appears.

## Self-Check: PASSED

Files claimed created, verified present on disk: `16-UAT.md`, `COVERAGE.md`, and both
`2026-08-18/` dated archives.

Files claimed modified, verified present on disk: `artifacts/shortcuts/MANIFEST.md`, both signed
`.shortcut` artifacts, `09-UAT.md`, `.planning/STATE.md`, `16-RESEARCH.md`.

Commits claimed, verified in `git log`: `04f3612` (task 1), `32aaedf` (task 2), `8d98afb`
(task 3). **No commit deleted a tracked file** — `git diff --diff-filter=D` empty for all three.
Working tree clean after each commit.

Both signed artifacts verified non-zero, `AEA1`-magic, exactly named, and decrypt-verified
byte-identical to their built sources. `python3 docs/manifest_check.py` re-run after every
subsequent edit and still `passed (6 rows verified against disk)`;
`python3 docs/retired_clause_check.py` likewise still green after the `STATE.md` edit.
