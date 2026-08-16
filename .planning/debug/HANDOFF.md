# PROSOCHĒ OPEN-path debug — consolidated handoff

**Status: CLOSED, resolved.** All three original symptoms from the 2026-08-13 todo are
now device-verified. The debug session is archived at
`.planning/debug/resolved/open-routing-sequence-error.md`. Nothing is in flight in this
session. Residual follow-up work (never claimed resolved by inference) has been spun off
into four standalone todos in `.planning/todos/pending/` — see §9.

**Final device confirmation (2026-08-15), verbatim from the user, on build `2026-08-15o`:**
> "we did it! we got every single letter, I clicked Always allow save 1 dictionary to a
> file (good). we got a menu of 'Leaving / Continue' and we got Circle 1. pressure
> 0.166666666666667 heat 0. amazing."

Every breadcrumb A through J fired with no error, the one-time Shortcuts file-save
permission prompt behaved as expected, the Leaving/Continue intervention menu displayed,
and Circle 1 fired with a plausible Pressure=0.166666666666667 (1/6) / Heat=0 reading
consistent with a first-ever OPEN. This is the terminal confirmation the 16-cycle session
was chasing. **Not covered by this report:** an explicit "Open Control Room, confirm no
note picker" check — Finding 2 (the `filter.notes` result-bound fix, cycle 16) remains
locally verified only; see §6 and the new ship-readiness todo.

**Process note (2026-08-15, not a debug cycle):** the cycle-16 signed artifact was briefly
misplaced at a dated subfolder (`artifacts/shortcuts/2026-08-15/...shortcut`, with a doubled
`2026-08-15/2026-08-15/` archive path) instead of the canonical
`artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut`. Root cause: a one-off invocation
mistake, not a bug in `tools/build_state_engine.py` (which owns only `src/PROSOCHE-Dumb.xml`
generation and has no archive/sign logic at all) or in the shortcuts-playground skill's
`bin/sign-shortcut` wrapper (which is correctly designed already — see below). User manually
repaired it; re-verified this turn by decrypting the canonical artifact (build `2026-08-15o`
confirmed, no regression) and by re-running the pipeline with the correct invocation. Full
account in `resolved/open-routing-sequence-error.md`'s "Process note" under `## Resolution`.
No code-level recurrence guard exists for this class (it's a CLI-invocation mistake in
tooling this project doesn't own); the only guard is this canonical-invocation banner —
named honestly as a residual gap in the resolved file's Prevention postmortem.

**The correct, canonical archive/sign invocation** (always use this, exactly):
```
bin/sign-shortcut src/PROSOCHE-Dumb.xml --name "PROSOCHĒ — Nine Circles — Dumb" \
  --mode anyone --output-dir artifacts/shortcuts
```
`--output-dir` must always be the plain `artifacts/shortcuts` — **never** a pre-dated path
(e.g. never `artifacts/shortcuts/$(date +%F)`). The wrapper already does the right thing on
its own: it archives the pre-sign unsigned XML to `artifacts/shortcuts/<today>/<name>-<HHMMSS>.xml`
(one dated level, matching the `2026-08-13`/`2026-08-14` precedent in
`artifacts/shortcuts/MANIFEST.md`) and separately signs directly to the canonical
`artifacts/shortcuts/<name>.shortcut` — no manual "promote to canonical" step is needed or
should be added. Passing an already-dated `--output-dir` is what causes both symptoms at once
(signed file one dated level too deep, archive doubled two levels deep).

This file is the **single authoritative entry point** for this closed session — read it
first, then follow §9 into whichever follow-up todo is being picked up next. It
consolidates the per-cycle working documents, which have been folded in here and
deleted; their full text remains in git history. Cycle 14, 15 and 16's own reasoning,
plus the closing Resolution summary and Prevention postmortem, are in
`resolved/open-routing-sequence-error.md`'s Current Focus / Evidence / Resolution
(`cycle_14_*`/`cycle_15_*`/`cycle_16_*`, plus the FINAL summary block) — this file is the
summary, that file is the durable record.

| artifact | role |
|---|---|
| **this file** | start here |
| `resolved/open-routing-sequence-error.md` | full session checkpoint / audit trail (~450 KB, 16 cycles + closure) |
| `.claude/CLAUDE.md` § Conventions | the durable authoring rules — **read before generating any plist** |
| `docs/BUILD-NOTES.md` §13–17 | deviations, capability findings, ship checklist |
| `unsupported-device-import.md` | a **separate, unrelated** debug session — do not merge |

Branch `codex/automation-parameter-diagnosis`. Nothing pushed. Never switch to
`codex/prosochedebug1` or `codex/round1` — both predate every fix here, and rebuilding
from either silently reproduces all three original symptoms.

---

## 1. Where the work stands — CLOSED

**Device evidence arrived on build `2026-08-15n` (cycle 15's shipped build, committed at
`1cb857c`):** the device progressed from breadcrumb E to breadcrumb I — confirming every
cycle-15 fix (the five compound-value coercion sites, `get_value()`, the
`verify_compound_value_reads()` guard) as far as I — then hit **one blocker on the OPEN
critical path** immediately after I:

> In '', no value was found for dictionary key 'pending_exit'

This is the exact failure this file's own `KNOWN_SENTINEL_EXISTENCE_GATES` note predicted
in advance: `pending_exit` was entirely absent from the bootstrap `state.json` template,
so `complete_pending_exit()`'s unconditional flat read hard-errors on the first OPEN —
the identical error *shape* cycle 11 found for `settings_snapshot` (STATE SHAPE, axis 6),
not the "couldn't convert Text to Dictionary" shape cycle 15 closed (axis 8).

**Separately, on the MANUAL path (independent defect, same device evidence batch):**
choosing "Open Control Room" correctly opens the resolved Control Room Note (cycle 14's
`shownote` fix confirmed still working) but a picker/list of every note *also* appears.
Traced to the one `is.workflow.actions.filter.notes` ("Find Notes") site in this artifact
carrying no declared result bound — Donor 8's own device-authored `filter.notes` action
(re-decrypted this cycle) carries `AppIntentDescriptor` +
`WFContentItemLimitEnabled=true` + `WFContentItemLimitNumber=1`; this artifact's site had
none of the three.

**Both findings were fixed in cycle 16:**

1. **`pending_exit` restructured to a permanent `{type, timestamp}` container** —
   mirroring `settings_snapshot`'s own already-verified container/leaf split exactly
   (`seed_pending_exit()`, `verify_pending_exit_seed()`; `record_exit_and_route()` and
   `complete_pending_exit()` now write/clear/gate only the leaves, condition 5 against
   the cleared sentinel, not condition 100). `pending_exit` is removed from
   `KNOWN_SENTINEL_EXISTENCE_GATES`; only `active_session` remains there, deliberately
   (confirmed safely inert on this device run, not fixed speculatively — see §6, and the
   new `2026-08-15-close-state-shape-sentinel-gaps.md` todo).
2. **`filter.notes` gained `AppIntentDescriptor` + `WFContentItemLimitEnabled` +
   `WFContentItemLimitNumber`**, copied verbatim from Donor 8, via a new
   `fix_notes_filter_limit()` pass. `VERIFIED_PARAMETER_KEYS` extended as the recurrence
   guard, matching `shownote`'s own precedent.

Build **`2026-08-15o`** (Dumb only) shipped this fix, and was **device-confirmed on
2026-08-15** — see the top banner for the verbatim report. **Sentient was NOT rebuilt
this session** — it still reflects build `2026-08-14k`; re-running
`tools/build_sentient.py` to fork all of cycles 14, 15 and 16's fixes into it is now the
first item in the new `2026-08-15-fork-sentient-post-openpath-fix.md` todo.

Three symptoms were reported on 2026-08-13. **All three are now closed and
device-verified.**

| # | symptom | status |
|---|---|---|
| 2 | `No value provided … Set Dictionary Value … key "sequence"` | **CLOSED**, device-verified |
| 3 | Control Room note bootstraps empty | **CLOSED**, device-verified |
| 1 | OPEN path never reaches the intervention | **CLOSED**, device-verified 2026-08-15 — every breadcrumb A–J fired on build `2026-08-15o`, Leaving/Continue menu displayed, Circle 1 fired (Pressure=0.166666666666667, Heat=0) |

**Breadcrumb positions confirmed on build 15o (Dumb), device pass 2026-08-15:**
`A=94 B=149 C=170 D=288 E=308 F=416 G=425 H=459 I=474 J=524` — every letter reported
fired ("we got every single letter"), matching this file's own pre-registered
prediction exactly (confirmed directly against the decrypted signed artifact in cycle
16, then confirmed live on device in the closing report).

**One check this closure does NOT cover:** the device report confirms the OPEN critical
path only. It does not explicitly confirm "Open Control Room" was tapped and opened
with no note-picker/list — Finding 2 (the `filter.notes` fix) remains **locally
verified, not device-confirmed**. This is tracked, not silently assumed resolved — see
§6 and the new `2026-08-15-ship-readiness-cleanup.md` todo, item 4.

---

## 2. The defect axes — all found, all guarded

Every defect this session was **systematic**, not a one-off: a generator-wide
misunderstanding of the plist format. Each is now asserted by a build guard in
`tools/build_state_engine.py`, so the class cannot silently return.

| # | axis | sites fixed | how it presented |
|---|---|---|---|
| 1 | wrong parameter key name | 147 + 1 (`shownote`, cycle 14) | "No value provided …" / interactive fallback |
| 2 | value envelope, `str` | 367 | fields silently empty |
| 3 | value envelope, `AttributedString` | 2 | empty note body |
| 4 | required picker enum missing | 2 | "Please choose a value …" |
| 5 | variable slot took wrong envelope | 25 | "Please choose a value …" |
| 6 | operand type / coercion — conditionals | 20 Dumb, 25 Sentient | red operator, runtime failure |
| 6b | operand type / coercion — **math + getitemfromlist** (cycle 14) | 67 (18 brightness/volume deliberately deferred) | runtime type-conversion failure, invisible red-chip equivalent |
| 7 | state shape absent before read | 8 keys + **`pending_exit`, cycle 16** | "no value was found for dictionary key" |
| 8 | **STRUCTURED VALUE — compound Array read through `read_value()`'s Text coercion, then fed to a List-consuming action (cycle 15)** | 5 (recent_sessions ×2, profile_snapshot.enabled_exits, exit_events, exit_stats.\<type\>.samples) | "Get Dictionary Value failed … couldn't convert Text to Dictionary" |
| — | date-typed action fed non-date data (cycle 14) | 3 sites | "couldn't convert from Text to Date" |
| — | stale validity gate / missing rebind (cycle 14) | 1 gate + 2-action rebind | corrected template never reaches the device |
| **9** | **CANDIDATE, cycle 16 — declared cardinality omitted on an App-Intent-backed content-item query** (`filter.notes`) | **1** | resolves silently in the source/validator, but iOS shows an interactive disambiguation UI on-device (a "list of every note") instead of the single deterministic result |

**The full rules are in `.claude/CLAUDE.md` § Conventions.** Read them before touching the
generator. (Neither the cycle-15 axis nor the cycle-16 candidate axis 9 is yet folded into
CLAUDE.md's own numbered list — see §9 as a candidate follow-up if this cycle is confirmed
on device. Axis 9 is deliberately marked "candidate" rather than numbered permanently: it
has one confirmed site and is not yet proven to be a systematic class the way axes 1–8
were, since a systematic sweep for OTHER App-Intent-backed content-item actions with a
missing cardinality bound has not been run this cycle.)

---

## 3. ~~The date-coercion blocker~~ RESOLVED cycle 14 — superseded by axis 8, then axis 6/7

All five `gettimebetweendates`-adjacent sites were fixed in cycle 14 (see git history for
the full account) and are now **device-confirmed correct as far as breadcrumb I**. The
axis-8 compound-value defect (cycle 15) is also device-confirmed correct as far as I. The
active blocker going into cycle 17 (if the device run refutes cycle 16's fix) is whatever
the next device report actually names — per this session's own inverted lesson: same-ish
letter, different error text, means a new defect, not a recurring one.

---

## 4. Verified iOS runtime semantics

Established by user-built donors on the target iPhone, and — as of cycle 16 — by the
production artifact's own confirmed device behaviour. Not in the Playground bundle, not
derivable from a plist alone.

| construct | behaviour |
|---|---|
| flat read, missing key, key present with SOME value elsewhere in a partially-seeded dictionary | returns nothing, no error → gate **false** (Donor 6.1) |
| flat read, key **entirely absent** from the dictionary (never declared anywhere in the JSON, not even as a sibling) | **hard error**, "In '', no value was found for dictionary key '\<key\>'" (cycle 11, settings_snapshot; **re-confirmed cycle 16, pending_exit, on the actual production artifact**) |
| flat read, present but empty | → gate **true** |
| dotted read, any missing segment | **hard error**, "could not evaluate the key path" |
| `"null"` / `""` → `WFNumberContentItem` | **false**, no error |
| `shownote.target` (nonexistent key) | **iOS falls back to an interactive note picker** — cycle 14, Donor 8 |
| date-typed action fed a Text epoch-seconds string | **"couldn't convert from Text to Date"** — cycle 14, device-confirmed |
| `getvalueforkey` (Get Dictionary Value) fed a Text WFInput | **"couldn't convert Text to Dictionary"** — cycle 15, device-confirmed |
| `filter.notes` ("Find Notes") with no `WFContentItemLimitEnabled`/`Number` declared | resolves fine in the source and validator; **on-device, presents an interactive disambiguation UI (a list of every match) instead of the single deterministic result** — cycle 16, reported device behaviour, corroborated by Donor 8's own device-authored shape always declaring a limit |

**Consequence, load-bearing:** a read-then-`has any value` gate on a dotted path is
**unimplementable**. The read raises unless the final key exists; if it exists, the gate is
true. No sentinel value fixes it. Gate on numeric `> 0`, or on a STRING "is not sentinel"
test (condition 5) against the leaf directly, or restructure to a flat read. This killed
three separate proposed fixes before it was understood, and is the exact reasoning behind
cycle 16's container/leaf split for `pending_exit`.

**Operator/operand type validity is a UI-only signal.** Shortcuts offers comparison
operators based on the left operand's resolved type. A numeric condition on a text-typed
operand renders **red**, is structurally valid in the file, and fails at runtime. No
file-level analysis can detect it — not the validator, not the catalog, not decryption.
The user's on-device eyeball found this class; it is a first-class evidence channel.

**Cycle 16 addendum — a state-shape gap can be LIVE, not just latent.** Cycles 12 and 15
both found real defects that sat past every breadcrumb the device had reached and were
deliberately left as documented, non-blocking follow-ups. Cycle 16's `pending_exit` gap
was the SAME kind of finding (recorded, deferred, in `KNOWN_SENTINEL_EXISTENCE_GATES`
since before cycle 14) but turned out to be reachable on the very first OPEN once the
device progressed far enough — a reminder that "latent" is a statement about what a
*specific* device run has exercised so far, not a permanent property of the defect.

---

## 5. Donor shortcuts — device ground truth

Eight, built by the user in Shortcuts.app on the target iPhone, exported here,
decrypted via the `aea decrypt` + `aa extract` recipe (`docs/BUILD-NOTES.md:619`). **This
channel has been decisive every time it was used.** Cycle 16 re-decrypted Donor 8 (already
on disk from cycle 14) rather than requesting a new donor — the SAME donor settles both
`shownote` (cycle 14) and, now, `filter.notes` (cycle 16), because both actions live in
the same hand-authored find-or-create block Donor 8 was originally built to mirror.

| donor | settled |
|---|---|
| `Donor - apps`, `Donor - notes` | Notes action shapes; proved signed artifacts are decryptable |
| `Donor 3` | numeric constructs; killed three ranked candidates; closed DEV-05 |
| `Donor 4` / `Donor 4.1` | **A/B pair** — isolated the coercion aggrandizement exactly (`WFCoercionVariableAggrandizement`/`WFNumberContentItem`) |
| `Donor 5` | for the 14 `WFConditionalActionString` sites — **still not analysed, past breadcrumb J** |
| `Donor 6` | miswired (trailing space, misrouted input) — superseded |
| `Donor 6.1` | flat vs dotted reads; present-but-empty; `"null"` coercion |
| `Donor 7` / `Donor 7.1` | **CLOSED cycle 14.** CLOCK block Date→Date chain; `format.date`'s real pattern key. |
| `Donor 8` | **CLOSED cycle 14** (`shownote` reads `WFInput`, not `target`) **and cycle 16** (`filter.notes` needs `AppIntentDescriptor` + a declared result limit). |

---

## 6. Open items, ranked — closure classification, 2026-08-15

Symptom 1 is CLOSED (§1). Everything below survived closure review: each item was
classified as either **spun off into a standalone todo** (real, scoped, actionable —
`.planning/todos/pending/`) or **left as historical/reference context** (inert,
superseded, or too speculative to action yet) — never left as an unclassified prose
paragraph in this now-closed session.

### CLOSED this session
- ~~Device pass on build `2026-08-15o`~~ — device-confirmed 2026-08-15, see §1 top
  banner. Both checks the prior version of this item asked for: (a) OPEN reaches Circle
  1 past breadcrumb J — **CONFIRMED**; (b) Open Control Room shows no note picker/list —
  **NOT explicitly covered by the report**, carried forward, see below.
- ~~The breadcrumb I→J blocker~~ — `pending_exit` restructured to a permanent
  `{type, timestamp}` container, mirroring `settings_snapshot`'s own split; device-
  confirmed. See §1–§2.
- ~~The Open Control Room note-picker (code fix)~~ — `filter.notes` gained a declared
  result bound and App Intent identity, Donor-8-matched, locally verified. **Device
  confirmation of this specific check is carried forward** — see
  `2026-08-15-ship-readiness-cleanup.md`, item 4 (SPUN OFF — real, scoped, one-tap
  verification, not left as prose).
- ~~Recurrence guards~~ — `verify_pending_exit_seed()` (state shape) plus the unchanged
  `verify_sentinel_gates()` now protecting `pending_exit.type` automatically (no longer
  exempted); `VERIFIED_PARAMETER_KEYS` gained a `filter.notes` entry.

### SPUN OFF — `2026-08-15-close-state-shape-sentinel-gaps.md`
- **`exit_events`** — still entirely absent from the bootstrap `state.json` template
  (unchanged from cycle 15's own finding). SAME STATE-SHAPE category `pending_exit` was
  before cycle 16 closed it. Not on the OPEN critical path A–J, so it did not block the
  closed measurement — but it is a live crash risk on the exit-recording path, real and
  scoped, so spun off rather than left in prose.
- **`active_session`** (the sole remaining `KNOWN_SENTINEL_EXISTENCE_GATES` entry) —
  same unimplementable-gate construct, confirmed SAFELY INERT on the closing device run
  specifically (past every `active_session` read on the OPEN critical path with no
  error) — but "latent" is a statement about what that ONE run exercised, not a
  permanent property; needs the SAME container/leaf treatment `pending_exit` received.
  Bundled with `exit_events` per this file's own prior suggestion (same code path, same
  fix pattern).
- **DEV-06 — restore-ownership check** (`changed_at`/`changed_by_session_id`, written at
  20 sites, read nowhere) is noted in that same todo as MOOT if the brightness/volume
  cut (below) proceeds — not spun off separately, since its relevance is entirely
  contingent on that other decision.

### SPUN OFF — `2026-08-15-fix-red-operator-and-list-wrapper-defects.md`
- **`WFItems` wrapper** (2 confirmed instances) — iOS wraps variable-bearing list rows
  as `{"WFItemType": 0, "WFValue": <WFTextTokenString>}`; ours omits the wrapper, so rows
  render blank. Shape already recovered from Donors 4/4.1. **New evidence found during
  closure:** `.planning/debug/Screenshot 2026-08-14 at 11.55.12⁠pm.png` — never
  referenced anywhere in the debug session, reviewed for the first time during this
  closure — shows this defect directly on-device (a 9-row List rendering entirely blank
  "Text" placeholders).
- **Donor 5 / 14 `WFConditionalActionString` sites** — still unopened, past breadcrumb
  J, Donor 5 on disk since cycle 14. The SAME reviewed screenshot also shows a concrete,
  previously-unnamed site: an `If` testing `Previous Respected` `is`, rendered fully
  red — corresponding to `if_block("Previous Respected", 4, ...)` in
  `tools/build_state_engine.py:649-650`/`:1069`, giving the todo a concrete starting
  point instead of an abstract count of 14.
- **`If [Audit Token] contains` renders red** (Sentient-only) — likely the SAME family;
  cross-referenced from `2026-08-15-fork-sentient-post-openpath-fix.md` rather than
  duplicated as its own item, so it isn't investigated twice in parallel.

### SPUN OFF — `2026-08-15-fork-sentient-post-openpath-fix.md`
- **Re-fork Sentient** (`tools/build_sentient.py`) now that Dumb's OPEN path is
  device-confirmed — still reflects build `2026-08-14k`, has not picked up cycles
  14/15/16's fixes at all. Now unblocked and actionable (previously gated on Dumb's own
  device confirmation, which just arrived).

### SPUN OFF — `2026-08-15-ship-readiness-cleanup.md`
- **Cut brightness/volume manipulation from the MVP.** User decision, reaffirmed
  2026-08-15. Still not implemented in code — `restore_managed_settings`, `dim()`,
  `silence()`, `settings_snapshot` all still ship, and the 18 uncoerced
  `setbrightness`/`setvolume` sites remain deferred. A real scope decision that needs to
  actually be executed, not just re-affirmed in prose again.
- **Strip debug scaffolding before ship** — `BUILD_STAMP`, `ROUTER_TRACE`,
  `OPEN_BISECT`, and the ten breadcrumbs. Deliberately kept in throughout the closed
  session; now un-blocked.
- **No `.gitignore`** — `.DS_Store`/`__pycache__` keep reappearing in `git status`.
- **`artifacts/shortcuts/MANIFEST.md` staleness** — still dated `2026-08-13` only.
- **Device-confirm the Control Room open flow** (Finding 2 / `filter.notes` fix) — see
  above; the closing device report did not explicitly cover this check.

### LEFT AS HISTORICAL CONTEXT (not spun off — reasons given per item)
- **`cooldown_until` sentinel** — device-verified safe, leave untouched. Genuinely
  inert; no action needed, ever, unless new evidence contradicts this.
- **The archive/sign output-dir process mistake** — already fully resolved
  procedurally (canonical invocation pinned at the top of this file); the tooling it
  concerns (`bin/sign-shortcut`) is owned by the shortcuts-playground plugin, not this
  repo, and its own default behaviour is already correct by design. No project-owned
  code to spin a todo against; named as a residual, honestly-weaker-guarded item in the
  resolved file's Prevention postmortem instead.
- **Whether `filter.notes`' cardinality-omission (candidate axis 9) is a genuinely
  systematic class** — this artifact has no other `filter.*` actions today, so a
  build-time sweep for the class would have nothing else to check; explicitly "moot
  today" per this file's own prior note (§9, pre-closure). Revisit only if/when a
  second App-Intent-backed content-item query is added to the generator — not
  actionable now, so not spun off as a todo that would sit empty.
- **Folding the axis-8/axis-9 rules into `.claude/CLAUDE.md`'s numbered axis list** —
  folded into `2026-08-15-fix-red-operator-and-list-wrapper-defects.md`'s Solution
  (step 5) rather than given its own todo, since it is documentation housekeeping that
  naturally belongs alongside whoever next touches that same defect family.

(The former "Before any ship" items 10-12 — strip debug scaffolding, add `.gitignore`,
re-fork Sentient — are now covered above under the `2026-08-15-ship-readiness-cleanup.md`
and `2026-08-15-fork-sentient-post-openpath-fix.md` SPUN OFF sections; not duplicated
here.)

---

## 7. Technique — what actually worked

Recorded because it was learned expensively and is not obvious.

- **Fix whole classes, never site-by-site.** Reaffirmed a fourth time in cycle 16: the
  `pending_exit` fix required BOTH the state-shape half (seed the container) AND the
  gate-semantics half (leaf-scoped condition 5, not container-scoped condition 100)
  together — seeding alone would have traded one confirmed hard error for a different,
  already-documented one (cycle-10-finding-5's anti-pattern) on the very next OPEN
  following any exit.
- **Read the error text, not just the breadcrumb letter.** Cycle 16's device report
  ("In '', no value was found for dictionary key 'pending_exit'") was matched directly
  against cycle 11's own settings_snapshot precedent (identical shape) rather than
  cycle 15's "couldn't convert Text to Dictionary" shape — confirming which axis was live
  before forming any hypothesis, exactly as this session's own established discipline
  requires.
- **A defect can be "latent" only relative to what a device run has actually exercised.**
  `pending_exit` sat in `KNOWN_SENTINEL_EXISTENCE_GATES` since before cycle 14 as a
  documented-but-deferred, presumed-latent gap; cycle 16's device run simply progressed
  far enough to make it live. The corollary — check whether a sibling deferred item
  (`active_session`) is ALSO now reachable before assuming it's still safe — was applied
  this cycle and confirmed `active_session` is still inert on this specific run, not
  fixed speculatively.
- **Reuse an existing verified pattern rather than inventing a new one, even under time
  pressure.** `pending_exit`'s fix is a structural copy of `settings_snapshot`'s own
  already-device-verified container/leaf split (cycles 10–12), not a new construct.
- **Re-decrypt a donor already on disk for a NEW question it wasn't originally opened
  for.** Donor 8 was decrypted in cycle 14 to answer a `shownote` question; cycle 16
  re-opened the SAME decrypted export to answer a `filter.notes` question, because both
  actions live in the same hand-authored block. No new donor request was needed.
- **Catalog cross-checks corroborate donor evidence; they don't replace it.**
  `WFContentItemLimitEnabled`/`Number` being present in the bundled ToolKit catalog raised
  confidence that Donor 8's shape is the action's genuine general schema, not a one-off
  authoring quirk — but the FIX itself still copies the donor's exact values (types
  included: a plist `<real>1</real>`, not an integer), not just "a value satisfying the
  catalog's type."
- **Direct grep before forming a binding-defect hypothesis.** The directive's own
  candidate list for the Control Room symptom included "a leftover/duplicate Notes
  action" and "two separate actions both touch Notes" — both were REFUTED in under a
  minute by a direct count (exactly one `filter.notes`, one `shownote`, two legitimate
  `appendnote`s) before any code was touched, avoiding a wasted investigation branch.
  Attack the WELL-EVIDENCED candidate first (the directive's own third listed candidate,
  matched exactly by re-checking Donor 8), don't investigate every candidate equally.
- **Idempotency is cheap insurance for a self-modifying generator.** Cycle 16's fix was
  verified idempotent the same way as every prior cycle's.
- **Signed `.shortcut` files are decryptable** — verify what actually shipped rather than
  trusting unsigned source plus an mtime. Confirmed again this cycle: the predicted
  breadcrumb shift (A–I unchanged, J −3) was verified against the DECRYPTED shipped
  artifact, not assumed from action-count arithmetic.
- **State a prediction and its refutation criteria before each device test.** Cycle 16's
  is in §1 and in the debug session's Current Focus `falsification_test`.

---

## 8. Type audit, cycle-14 nested-descent pass (unchanged by cycles 15–16)

Cross-checked twice (once against a bug in the first draft that wrongly flagged
already-fixed conditional sites, caught and corrected before trusting the numbers).

| field | offenders before | offenders after | status |
|---|---:|---:|---|
| `conditional.WFInput` (numeric codes) | 0 | 0 | already complete (cycle 9) |
| `getitemfromlist.WFItemIndex` | 30 | 0 | fixed cycle 14 |
| `math.WFMathOperand` | 26 | 0 | fixed cycle 14 |
| `math.WFInput` | 11 | 0 | fixed cycle 14 |
| `setbrightness.WFBrightness` | 14 | 14 | deliberately deferred, MVP cut |
| `setvolume.WFVolume` | 4 | 4 | deliberately deferred, MVP cut |

**Correction (Phase 9 research, 2026-08-16):** this snapshot is stale. A later cycle added
`silence()` to the Python `for test_circle in range(1, 10):` unroll inside
`manual_emergency_restore()`'s "Test a Circle" menu (`tools/build_state_engine.py`), which added
10 more `setvolume` call sites (and 10 more `setbrightness` sites, already counted in the 14
above via the matching `dimming()` unroll). As of build `848d00e`, direct plist inspection of
`src/PROSOCHE-Dumb.xml`/`src/PROSOCHE-Sentient.xml` shows **`setbrightness.WFBrightness` = 14,
`setvolume.WFVolume` = 14 — 28 total, not 18.** See
`.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-RESEARCH.md`
"Site count correction" for the full trace. Do not cite the "18" figure below as current.

Total (as originally recorded, now stale by the correction above): 227 numeric-field sites
inspected → 85 offenders → 67 fixed, 18 deferred by
explicit decision, 0 unexplained. (This is a NUMERIC-operand audit, axis 6b — a
different axis from cycle 15's STRUCTURED-value audit, axis 8, and from cycle 16's
STATE-SHAPE/GATE-SEMANTICS pair on `pending_exit`, axes 6/7. See §2's table for the
cycle-15 numbers: 55 `read_value()` target names scanned, 5 offenders, 5 fixed, 0
deferred, 1 known-uncoverable-by-guard. Cycle 16 touched exactly 1 STATE-SHAPE key
(`pending_exit`) plus 1 candidate-axis-9 site (`filter.notes`), both confirmed by direct
inspection rather than a systematic sweep — a systematic sweep for OTHER App-Intent-backed
content-item actions with an undeclared cardinality bound has not been run.)

---

## 9. Related todos

**Origin todos (both updated to reflect closure):**
- `.planning/todos/pending/2026-08-13-fix-open-routing-and-test-circle-sequence-error.md`
  — the origin of this session. **Both symptoms now CLOSED**, status section updated
  2026-08-15 to reflect full resolution and index the four new todos below.
- `.planning/todos/pending/2026-08-14-repair-ios-26-automation-onboarding.md`
  — independently corroborated by this session, still unfixed itself (a documentation +
  generator propagation task, not a code defect). Updated 2026-08-15 to note this
  session's closure changes nothing about its own scope/status — still the next
  concrete unblocked task in the queue if nothing else is prioritised first.

**New todos filed during this closure** (see §6 for which HANDOFF item each traces to):
- `.planning/todos/pending/2026-08-15-fork-sentient-post-openpath-fix.md` — re-fork
  Sentient now that Dumb is device-confirmed; check the Sentient-only `Audit Token`
  red-render against the same family as the sibling todo below before treating it as a
  separate investigation.
- `.planning/todos/pending/2026-08-15-close-state-shape-sentinel-gaps.md` — apply the
  now-twice-verified container/leaf pattern to the two remaining sentinel gaps
  (`exit_events`, `active_session`); notes DEV-06 as moot if the brightness/volume cut
  proceeds.
- `.planning/todos/pending/2026-08-15-fix-red-operator-and-list-wrapper-defects.md` —
  Donor 5 / the 14 `WFConditionalActionString` sites (a concrete starting site,
  `Previous Respected`, found via the previously-unexamined screenshot reviewed during
  this closure) + the `WFItems` List wrapper (2 sites, same screenshot shows the blank
  rows directly). Includes folding both axes into `.claude/CLAUDE.md`'s numbered axis
  list once fixed.
- `.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md` — strip debug
  scaffolding, add `.gitignore`, refresh `MANIFEST.md`, device-confirm the Control Room
  open flow (Finding 2, not covered by the closing device report), and execute the
  brightness/volume MVP-cut decision.

**Genuinely not actionable yet (left as historical context, not filed):** whether
`filter.notes`' cardinality-omission is a systematic class worth a build-time sweep —
moot today, this artifact has no other `filter.*` actions to check against; revisit only
if/when one is added.

## 10. Post-closure guidance

This session is closed; there is no "resume" step for it. To pick up where it left off:

1. Read `.claude/CLAUDE.md` § Conventions (the 7+1-axis authoring rules this session
   established) before touching the generator again, regardless of which follow-up todo
   is picked up.
2. Confirm branch is `codex/automation-parameter-diagnosis` and the provenance guard
   (`git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD`) passes.
3. Pick a todo from §9's "New todos filed during this closure" list based on priority —
   none of them can regress the now-closed OPEN path (all sit past breadcrumb J or on
   unrelated code paths), but treat each as new-risk surface requiring its own
   device-round-trip discipline, not a free pass on rigor.
4. If a NEW defect surfaces while working any of these todos, open a fresh debug session
   rather than reopening `resolved/open-routing-sequence-error.md` — that file is now an
   immutable audit trail of a closed investigation, per this project's own debug-file
   protocol.
