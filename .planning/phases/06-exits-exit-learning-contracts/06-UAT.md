---
status: partial
phase: 06-exits-exit-learning-contracts
source: [06-01-SUMMARY.md, 06-02-SUMMARY.md, 06-03-SUMMARY.md]
started: 2026-08-16T00:12:00.000Z
updated: 2026-08-16T00:12:00.000Z
---

## Current Test

[testing paused — 5 items outstanding: Tests 5, 7, 14, 15 pending; Test 13 blocked on G-06-12]

## Context

This phase has the **highest known unfixed defect load in the product** and covers two
distinct feature areas that both depend on CLOSE (Phase 4) being verified first — run
`04-UAT.md` before this one.

**Contracts** (Confession / Intention Contract, §11 Primitive D) have never run on a
device. They're the mechanism the strategy leans on hardest: §6.7 names contract-fidelity
(intended vs. actual use) as potentially more informative than total screen time, and
§14.2 makes contract auditing — not lie detection — the entire basis of what Sentient is
allowed to do. If contracts don't work, the product degrades into a timer with dramatic
naming. Contracts are also the most *stateful* interaction in the product: free text in, a
duration choice in, both persisted across a session, compared against a CLOSE-measured
duration, then fed back into the next OPEN's Heat — every hop crosses a boundary this
project has already been burned at.

**Exits** carry the worst defect risk in the codebase: `exit_events` is **entirely absent**
from the bootstrap `state.json` template — the exact STATE-SHAPE class (axis 7) that
hard-errored on device twice already. It sits directly on `record_exit_and_route()` and
will very likely crash the first time a real exit is recorded against clean state.
`active_session` (the last remaining `KNOWN_SENTINEL_EXISTENCE_GATES` entry) is read on the
same path. **Both are tracked in the `close-state-shape-sentinel-gaps` todo — land that
first, before running any of the exit tests below.** Beyond crashes: if explore/exploit
learning doesn't actually work, PROSOCHĒ becomes a machine for changing which app consumes
the time (§30, §36 — explicitly not the goal).

Canonical strategy §11 Primitive D, §13.2, §6.1, §6.7, §8, §9, §16, §23, §27, §30, §32.

## Pre-install device forensics — 2026-08-18 (rung 1 over a rung-4 artifact)

The previous build's accumulated `state.json` was recovered from the device before the new
install was run, preserved at
`.planning/debug/device-state/state-2026-08-18T1931-stale-preinstall.json`, and analysed in
`.planning/debug/device-state/README.md`. Two of this phase's tests are advanced by it, and one
is resolved against the build itself rather than the device.

**It was written by a PRE-PHASE-16 build** (it still carries the `changed_at` /
`changed_by_session_id` leaves that decision D-02 removed, and `exit_events` is not the `[]` the
current template seeds). Nothing in it confirms a current-build fix.

## Tests

### 1. Resolve the Phase 6 verification conflict
expected: read both `06-VERIFICATION.md` and `VERIFICATION.md`, determine which is
current, record the answer. Do not proceed against an unclear static baseline.
result: pass
note: "Resolved 2026-08-18 from git chronology — no device needed. Three commits, in order:
  a03f737 (18:14:14) 'docs(06): record verification gaps' wrote VERIFICATION.md with
  status gaps_found, 1/5 must-haves; e6ea081 (18:19:38) 'fix(06): close exit learning semantic
  gaps'; 4f28084 (18:23:17) 'docs(06): reverify exit learning phase' wrote 06-VERIFICATION.md
  with status passed, 5/5, whose own header calls itself a 'Gap-fix audit after e6ea081'.
  Each of the four gaps recorded in the older file maps to a truth marked VERIFIED in the newer
  one (Consult menu gained Notes/Reminders/Calendar/Back plus a user query; Create reloads and
  re-proves ownership; the selector picks exactly one canonical candidate; no-contract outcomes
  serialise distinctly and next-OPEN feedback is guarded on a positive declared duration).
  VERDICT: 06-VERIFICATION.md (passed, 5/5) is current and authoritative.
  The bare VERIFICATION.md has been renamed VERIFICATION-superseded.md so this conflict cannot
  be re-raised by a future /gsd-verify-work run."


### 2. Free-text intention accepted and persisted
expected: intention text is accepted and persisted verbatim — watch for silently-empty
fields (the axis-2 envelope defect presented exactly this way).
result: pass
note: "DEVICE 2026-08-18 22:44. A real OPEN landing on Circle 4 prompted 'What are you reaching
  for? (optional)'; the text 'Check one thing then leave' was entered and state.json then held
  active_session.intention = 'Check one thing then leave' — VERBATIM, not empty. The axis-2
  silently-empty failure mode this test was written to catch does not reproduce.
  READ IT AT THE FLAT KEY (finding F-4): the value lands in a literal top-level key
  'active_session.intention'; the NESTED active_session block still reads 'null'. Checking only
  the nested block would report a false negative.

### 3. Each contract duration option works
expected: 2 / 5 / 10 / 15 / Custom all work, including Custom's own input path.
result: partial
note: "The menu renders all five options correctly. TESTED: '2 minutes' (persisted as
  declared_duration_seconds = 120, exact) and 'Custom' (raises its own numeric 'How many
  minutes?' prompt, which accepted 3). NOT individually exercised: 5, 10, 15 — they share the
  literal-menu path that 2 minutes proved, so the risk is low, but they are not observed.

### 4. Deliberate leisure is accepted as a valid contract
expected: "watch stupid videos for ten minutes" is accepted, not treated as a challenge
trigger (§6.1, §32 — getting this wrong makes the product moralistic, §12's named killing
failure).
result: pass
note: "DEVICE. The literal phrase 'watch stupid videos for ten minutes' was entered at the
  Intention prompt and accepted without challenge, comment or re-prompt — the flow went straight
  to 'Choose a boundary'. No moralising surface exists on this path.

### 5. Kept contract recorded and reduces next-OPEN Heat
expected: a contract kept within its bound is recorded as kept and reduces Heat on the next
OPEN (§10.2 rule 5).
result: pending
note: "ATTEMPTED, NOT COMPLETED. The overrun twin (Test 6) was captured cleanly, and the
  kept-contract run was set up — Pressure was put back into the Circle 4 band — but the run was
  cut off before the contract could be declared and closed within its bound. Nothing was
  observed, so nothing is claimed.
  TO FINISH: reach Circle 4 with a live session, declare 15 minutes, close after ~20 s, then
  confirm the session record carries respected: true with a negative overrun_seconds, and
  compare Heat on the NEXT open against the no-contract baseline. The recording half is very
  likely fine given Test 6, but the HEAT RELIEF half (§10.2 rule 5) is the part with no evidence
  at all yet and is the reason this test exists.

### 6. Overrun contract recorded with overrun amount and adds Heat
expected: a contract exceeded is recorded with its overrun, adding Heat per §10.2 rule 4
(>50% and >2 min).
result: partial
note: "RECORDING HALF: PASS, device 2026-08-18 22:47. A 120 s contract closed at 150 s produced,
  on screen, an alert reading 'Contract — Overrun seconds: 30', and in state.json a session
  record of declared_duration_seconds 120, duration_seconds 150, overrun_seconds 30,
  respected false. Arithmetic exact on every field.
  HEAT HALF: NOT ISOLATED. This overrun was 30 s — deliberately BELOW both of §10.2 rule 4's
  thresholds (>50% and >2 min) — so no penalty should have applied, and none was distinguishable
  from the ordinary rapid-return heat rise. The rule's positive case (a large overrun that DOES
  add Heat) is untested.
  UX, recorded not raised: 'Overrun seconds: 30' is bare machine phrasing shown to a user who
  has just finished using an app. Phase 20 territory.

### 7. Blank/vague contract response handled per §13.2
expected: no attempt to parse sincerity; behaves per the documented Dumb intent gate.
result: pending
note: "Not exercised. Note the prompt itself is labelled '(optional)', and the generator's own
  comment says 'Confession accepts any wording, including a blank intention', so the design
  intent is clear — but no blank or vague answer was actually submitted on device.

### 8. recent_contracts bounded window is correct
expected: state.json's `recent_contracts` holds the last ~10 per §16; fidelity figures are
arithmetically right — recompute by hand for at least two cases.
result: issue
reported: "recent_contracts is never written by any code path, on any build. Confirmed from
  both sides on 2026-08-18. DEVICE: the recovered state.json has recent_contracts: [] while
  simultaneously holding a fully-evaluated contract (declared_duration_seconds 120,
  overrun_seconds -99, respected true) inside a recent_sessions entry. GENERATOR:
  `grep -c 'set_value(\"recent_contracts\"' tools/build_state_engine.py` returns 0 — the key is
  seeded [] by the bootstrap template and nothing ever appends to it. Contract outcomes are
  instead folded into the recent_sessions record. So the test as written cannot pass on any
  build. NOTE the capability may nonetheless be intact: contract fidelity is computable from
  recent_sessions today, and the arithmetic there is correct (21 - 120 = -99; respected =
  overrun <= 0). The open question is whether §16's named rolling contract window is genuinely
  required or was superseded by the fold-into-sessions design — a scope call, recorded as an
  issue rather than silently re-scoped."
severity: major
evidence: ".planning/debug/device-state/README.md finding F-2"

### 9. No phantom contract-overrun Mirror message
expected: a time-overrun message is never shown when no contract existed (§13.1).
result: pass
note: "DEVICE, across roughly a dozen no-contract sessions this session. Every session that
  closed with declared_duration_seconds = 0 showed NO Contract alert at all, and stored
  overrun_seconds: null / respected: null rather than a fabricated zero. The single session that
  DID carry a contract was the only one to show the alert. The gate is behaving.

### 10. Each of the six exits routes correctly
expected: Capture → Notes/Voice Memos/Camera; Coordinate → Reminders/Calendar; Create → the
user-defined target; Connect → Messages/Phone/FaceTime, never auto-contacting anyone
(§8.4); Consult → verify whether `searchweb` or an `openurl` fallback actually fires on
device and what it opens; Close → Home/Lock Screen/put device down, confirmed not degraded
(§8.6, §36).
result: partial
note: "TESTED: Capture → sub-menu 'Notes / Voice Memos / Camera' exactly as specified; Notes
  selected and the Notes app opened. Coordinate → sub-menu 'Reminders / Calendar'; Calendar
  selected and Calendar opened. NOT TESTED: Create, Connect, Consult, Close.
  NOT A DEFECT, recorded so it is not re-raised as one: Capture → Notes landed on the PROSOCHĒ
  Control Room note rather than a blank note. The route is open_app('Notes')
  (tools/build_state_engine.py:1148 and route_exit()'s Capture branch), so iOS simply restored
  the last-viewed note — and the last note PROSOCHĒ itself opened is its own Control Room. It is
  correct per the implementation and still worth a product decision, since a user sent to
  'capture a thought' lands on the app's settings page.
  THIS TEST IS ALSO COMPROMISED BY G-06-12: the menu the user picks from is wrong before any
  route is reached — see Test 12.

### 11. Exit outcomes recorded correctly
expected: exit type, timestamp, triggering app, Circle, Heat/Pressure, time of day, and —
the load-bearing field — time until the next target-app OPEN (§9.1). If that last field
isn't captured correctly, learning is decorative.
result: pass
note: "DEVICE 2026-08-18, measured end to end (finding F-19). A Capture exit was recorded at
  epoch 1787092241 with pending_exit.type='Capture' and pending_exit.timestamp set; the next
  tracked OPEN was at 1787092494; exit_stats.Capture.sum_return_seconds became 253, and
  1787092494 - 1787092241 = 253 EXACTLY. count incremented to 1 and pending_exit.type was
  correctly cleared back to 'null'. So the load-bearing field is captured correctly and learning
  is not decorative.
  The event object carries app, timestamp, type, heat and circle. It does NOT carry the return
  time per event — that lives only in the aggregate. Whether §9.1 requires per-event retention
  is the open scope question also raised by F-3; flagged, not assumed.
  SHAPE CAVEAT (F-20): exit_events serialised as a bare OBJECT at one element despite the
  bootstrap seeding [], and became a proper array at two. See Test 15's note.
note: "PRE-INSTALL FORENSICS (finding F-3), two things to carry into the device run.
  (1) On the OLD build exit_events degraded to a SINGLE OVERWRITTEN OBJECT rather than a list —
  {app, timestamp, type, heat, circle} — because the key was never seeded. This settles
  assumption A1 in seed_exit_events()'s docstring, which recorded the pre-fix failure mode as
  [ASSUMED] and settleable only at rung 2: it is a SILENT SHAPE DEGRADATION, not a crash and not
  a zero-iteration no-op. The current build seeds exit_events: [], so verify on device that a
  second exit APPENDS rather than replaces — that is the actual regression risk this test now
  carries. seed_exit_events()'s docstring should be updated from [ASSUMED] to measured.
  (2) The recorded event object carries NO per-event field for time-until-next-OPEN. The return
  time is accumulated only into exit_stats.<Exit>.sum_return_seconds (1044 s for the single
  Capture event on the old build). Since this test names that field 'load-bearing', decide
  explicitly on device whether per-event retention is required or whether the aggregate
  satisfies §9.1."

### 12. Explore phase rotates across enabled exits only
expected: exploration never selects an exit the user has disabled.
result: issue
reported: "enabled_exits() does not filter at all. With all six exits enabled the 'Which one?'
  menu listed THIRTY-SIX entries — every exit repeated six times. A controlled re-run with
  profile_snapshot.enabled_exits reduced to ['Capture','Close'] produced TWELVE entries — every
  one of the six canonical exits, twice each. That is 6 canonical x N enabled, measured at two
  values of N, which pins the mechanism: the nested Repeat With Each in enabled_exits() appends
  the outer Canonical Exit on every inner iteration, i.e. its inner conditional evaluates TRUE
  unconditionally. Worse than the duplication: Coordinate, Create, Connect and Consult were all
  DISABLED and all still offered — and Coordinate was selected and FULLY ROUTED, presenting its
  Reminders/Calendar sub-menu. The disabled-exit guarantee is not weak, it is absent."
severity: blocker
evidence: ".planning/debug/device-state/README.md finding F-18

### 13. Exploit phase prefers historically stronger exits
expected: once `exits.exploit_min_observations` is met, exploitation prefers exits with
longer observed time-away; both `exploration_rate` and `exploit_min_observations`
(PROTOTYPE DEFAULT values) are reachable in realistic use, not just theoretically correct.
result: blocked
blocked_by: prior-phase
reason: "Blocked on G-06-12. The selector's counter arithmetic runs over the list enabled_exits()
  builds, and that list is 6N entries instead of N with every canonical exit present regardless
  of the profile. Any exploit-vs-explore result measured against it would be measuring the
  defect. Re-run after G-06-12 is fixed. Two observations were accumulated in the meantime and
  are on file (Capture 253 s, Coordinate 237 s), so the data path itself is producing samples.

### 14. Selection is deterministic, local, no model
expected: no model, no variable randomness source, no network involved in exit selection
(§9.3, §27).
result: pending
note: "Not directly instrumented. Nothing observed on device contradicts it — the Core fork
  contains no Use Model action at all, selection ran with no perceptible latency and no network
  permission prompt ever appeared, against a build whose only network-capable exit route is the
  user-initiated Consult search. But absence of a contrary observation is not a test, and this
  test asks for a positive one. Cheapest honest close: assert it structurally over the shipped
  plist (no askllm, no randomness source inside select_exit()'s span) rather than spend device
  time on it.

### 15. exit_stats stays bounded
expected: per-exit aggregates respect §16's rolling-window rule across a long test — no
unbounded growth.
result: pending
note: "Not reachable in one session — it needs a long run, and only two exits were recorded.
  ONE FINDING THAT CHANGES HOW TO TEST IT (F-20): a Shortcuts list holding exactly ONE item
  serialises into state.json as the bare item, not a one-element array. Observed on three
  independent containers — recent_sessions, exit_events and exit_stats.Capture.samples (which
  read as the bare scalar 253). recent_sessions and exit_events both self-healed into proper
  arrays at two elements; exit_stats.<Exit>.samples has NOT yet been observed at n>=2, and it is
  the one §16 actually trims and the one exploit-phase averaging consumes.
  This also corrects the expectation behind seed_exit_events(): the fresh bootstrap DID carry
  exit_events: [] and the first exit still wrote a bare object, so seeding an empty array does
  not prevent the collapse — it only prevents the unseeded read. That docstring should be
  amended.
  Inspect the FLAT dotted keys, not the nested exit_stats subtree, which is shadowed and
  permanently stale (F-4).
note: "PRE-INSTALL FORENSICS (finding F-4) — read before testing this. exit_stats is written
  through dotted keys, and on device a dotted Set Dictionary Value creates a LITERAL FLAT
  top-level key rather than writing into the nested container. The recovered file holds
  exit_stats.Capture.count = 1 (flat) alongside exit_stats.Capture.count = 0 (nested, the
  bootstrap seed), and exit_stats.Capture.samples = 1044 as a FLAT SCALAR alongside a nested
  samples: []. A dotted read prefers the flat key, so the aggregates are read correctly and the
  engine works — but when checking boundedness, inspect the FLAT keys. The nested exit_stats
  subtree is shadowed and permanently stale, and reading it would report zeros forever."

## Summary

total: 15
passed: 5
issues: 2
partial: 3
pending: 4
skipped: 0
blocked: 1

## Gaps

- gap_id: G-06-12
  truth: "Exploration never selects an exit the user has disabled."
  status: failed
  reason: "enabled_exits() filters nothing. Measured on device at two profile sizes: 36 menu entries with 6 exits enabled, 12 with 2 enabled — i.e. 6 canonical x N enabled. Disabled exits are offered, selectable and fully routable (Coordinate was disabled, chosen, and presented its Reminders/Calendar sub-menu)."
  severity: blocker
  test: 12
  root_cause: "enabled_exits()'s nested Repeat With Each appends the outer `Canonical Exit` on EVERY inner iteration — its inner conditional (`Enabled Exit Candidate` string-is `Canonical Exit`) evaluates TRUE unconditionally at runtime. The 6-canonical x N-enabled entry count measured at two values of N is what identifies this rather than a mis-seeded list."
  artifacts:
    - path: "tools/build_state_engine.py — enabled_exits()"
      issue: "The inner match conditional sets WFConditionalActionString TWICE — first to a bare placeholder, then to token('Canonical Exit'). The second assignment is present (unlike the unfinished G-04-1/G-04-3 sites), so the shape is not obviously wrong and the comparator must be compared on device against a known-good conditional."
    - path: ".planning/debug/device-state/README.md"
      issue: "Finding F-18 — the two-profile measurement and the disabled-exit routing observation."
  missing:
    - "Fix the inner conditional so it matches only on equal names, then re-measure the entry count at two different profile sizes — the count is the discriminator and a single-profile check cannot tell a fixed filter from a broken one."
    - "Add a build guard asserting the emitted list length equals the enabled count, so a regression is caught without a device."
    - "Re-run 06-UAT Tests 10, 12 and 13 afterwards; all three are measured against this list."
  debug_session: ".planning/debug/device-state/README.md (finding F-18)"

- gap_id: G-06-8
  truth: "state.json's recent_contracts holds the last ~10 per §16; fidelity figures are arithmetically right."
  status: failed
  reason: "recent_contracts is seeded [] and never written by any generator path (0 set_value sites); the recovered device state.json confirms it stayed empty while a contract was evaluated and stored inside recent_sessions instead."
  severity: major
  test: 8
  root_cause: "No append path exists. Contract outcome fields (declared_duration_seconds, overrun_seconds, respected) are written into the recent_sessions record by close_pipeline() and nowhere else."
  artifacts:
    - path: "tools/build_state_engine.py"
      issue: "Bootstrap template seeds \"recent_contracts\": [] but no set_value(\"recent_contracts\", ...) call exists anywhere in the file."
    - path: ".planning/debug/device-state/state-2026-08-18T1931-stale-preinstall.json"
      issue: "Device confirmation: recent_contracts: [] alongside a fully-evaluated contract in recent_sessions."
  missing:
    - "DECIDE FIRST, then implement: is §16's named rolling contract window required, or was it superseded by folding contract outcomes into recent_sessions? Contract fidelity is already computable from recent_sessions, so this may be a documentation fix rather than a code fix."
    - "If required: add the append + rolling-window trim in close_pipeline() beside the recent_sessions append, and treat recent_contracts as a COMPOUND_STATE_KEYS member (it is already listed there) so it is read with get_value(), never read_value()."
    - "If superseded: restate §16 and this UAT test, and remove the dead seeded key or document it as reserved."
  debug_session: ".planning/debug/device-state/README.md (finding F-2)"
