# PROSOCHĒ OPEN-path debug — consolidated handoff

**Status: PAUSED, clean.** Nothing in flight. Working tree has cycle-15 generator + Dumb
source/artifact changes, uncommitted. **Not yet device-tested.**

This file is the **single authoritative entry point** for resuming. It consolidates the
per-cycle working documents, which have been folded in here and deleted; their full text
remains in git history. Cycle 14 and 15's own reasoning is in
`open-routing-sequence-error.md`'s Current Focus / Evidence / Resolution
(`cycle_14_*`/`cycle_15_*`) — this file is the summary, that file is the durable record.

| artifact | role |
|---|---|
| **this file** | resume here |
| `open-routing-sequence-error.md` | full session checkpoint / audit trail (~370 KB, 15 cycles) |
| `.claude/CLAUDE.md` § Conventions | the durable authoring rules — **read before generating any plist** |
| `docs/BUILD-NOTES.md` §13–17 | deviations, capability findings, ship checklist |
| `unsupported-device-import.md` | a **separate, unrelated** debug session — do not merge |

Branch `codex/automation-parameter-diagnosis`. Nothing pushed. Never switch to
`codex/prosochedebug1` or `codex/round1` — both predate every fix here, and rebuilding
from either silently reproduces all three original symptoms.

---

## 1. Where the work stands

**Device evidence arrived on build `2026-08-15m` (cycle 14's build):** the device
progressed from breadcrumb D to breadcrumb E — confirming every cycle-14 fix (elapsed_since(),
the numeric-operand coercion generalisation, the shownote key, the format.date key, the
state rebind, and the checkpoint's Control Room split) as far as E — then failed with a
**NEW, different** error immediately after E:

> Get Dictionary Value failed because Shortcuts couldn't convert Text to Dictionary.

Cycle 15 traced this to a systematic class (not a one-off): `read_value()`, the helper
behind every scalar state read in this artifact, unconditionally applies **Get Text**
(gettext) to whatever it reads — correct for a scalar meant for text/numeric comparison,
and a categorical mismatch for a **compound value** (an Array) meant to be consumed
structurally by a downstream Get Item From List / Repeat With Each. A systematic scan
found **five** sites sharing this exact defect, one of which — `recent_sessions` in
`open_pipeline()` — is the confirmed E→F blocker, and a second —
`exit_stats.<type>.samples` in `complete_pending_exit()` — sits **on the OPEN critical path
itself** (between breadcrumbs I and J), reachable on the first OPEN following any exit.
All five are fixed; a new build guard (`verify_compound_value_reads()`, the **eighth**
defect axis) prevents the class from silently returning for any statically-known key.

Current build **`2026-08-15n`** (Dumb only), regenerated, validated, signed, and
decrypt-verified locally. **Sentient was NOT rebuilt this cycle** — it still reflects
build `2026-08-14k`; re-running `tools/build_sentient.py` once Dumb is device-confirmed
will fork all of cycles 14 and 15's fixes into it automatically.

Three symptoms were reported on 2026-08-13. Two are closed and device-verified.

| # | symptom | status |
|---|---|---|
| 2 | `No value provided … Set Dictionary Value … key "sequence"` | **CLOSED**, device-verified |
| 3 | Control Room note bootstraps empty | **CLOSED**, device-verified |
| 1 | OPEN path never reaches the intervention | **OPEN** — device confirmed D→E on build 15m; cycle 15 fixed the new E-blocker (and 4 sibling sites of the same class); **build 15n not yet device-tested** |

**Predicted breadcrumb positions for build 15n (Dumb):**
`A=94 B=149 C=170 D=288 E=308 F=416 G=425 H=459 I=474 J=527`
(A–E unchanged from build 15m; F/G/H/I each shift −1 because the `recent_sessions` fix
removes one action between E and F; J shifts a further −1, to −2 total, because the
`exit_stats.<type>.samples` fix also removes one action between I and J.) Confirmed
directly against the decrypted signed 2026-08-15n artifact, not assumed from arithmetic.

**Predicted next letter: E, then continuing PAST F with no error at all, through
G/H/I/J and into the Circle 1 intervention actually displaying** — see §7/§10 and the
debug session's cycle 15 `falsification_test` for the full prediction and refutation
criteria. **Whether/when to run this on-device is the user's own call**; this cycle
deliberately stopped at local build/validate/sign/decrypt-verify.

---

## 2. The eight defect axes — all found, all guarded

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
| 7 | state shape absent before read | 8 keys | "no value was found for dictionary key" |
| — | date-typed action fed non-date data (cycle 14) | 3 sites | "couldn't convert from Text to Date" |
| — | stale validity gate / missing rebind (cycle 14) | 1 gate + 2-action rebind | corrected template never reaches the device |
| **8** | **STRUCTURED VALUE — compound Array read through `read_value()`'s Text coercion, then fed to a List-consuming action (cycle 15)** | **5** (recent_sessions ×2, profile_snapshot.enabled_exits, exit_events, exit_stats.\<type\>.samples) | **"Get Dictionary Value failed … couldn't convert Text to Dictionary"** |

**The full rules are in `.claude/CLAUDE.md` § Conventions.** Read them before touching the
generator. (The cycle-15 axis is not yet folded into CLAUDE.md's own numbered list — see
§9 as a candidate follow-up if this is confirmed on device.)

---

## 3. ~~The date-coercion blocker~~ RESOLVED cycle 14 — superseded as the active blocker by axis 8

All five `gettimebetweendates`-adjacent sites were fixed in cycle 14 (see the prior
version of this file, preserved in git history, for the full account) and are now
**device-confirmed correct as far as breadcrumb E**. The active blocker going into cycle
16 (if the device run refutes cycle 15's fix) is axis 8 above, not this class returning —
per this session's own inverted lesson: same-ish letter, different error text, means a
new defect, not this one recurring.

---

## 4. Verified iOS runtime semantics

Established by user-built donors on the target iPhone. Not in the Playground bundle, not
derivable from a plist. Full table in `.claude/CLAUDE.md`.

| construct | behaviour |
|---|---|
| flat read, missing key | returns nothing, no error → gate **false** |
| flat read, present but empty | → gate **true** |
| dotted read, any missing segment | **hard error** |
| `"null"` / `""` → `WFNumberContentItem` | **false**, no error |
| `shownote.target` (nonexistent key) | **iOS falls back to an interactive note picker** — cycle 14, Donor 8 |
| date-typed action fed a Text epoch-seconds string | **"couldn't convert from Text to Date"** — cycle 14, device-confirmed |
| `getvalueforkey` (Get Dictionary Value) fed a Text WFInput | **"couldn't convert Text to Dictionary"** — cycle 15, device-confirmed (traced from the exact reported error string against a statically-read source defect, not from a fresh donor; see §5's note) |

**Consequence, load-bearing:** a read-then-`has any value` gate on a dotted path is
**unimplementable**. The read raises unless the final key exists; if it exists, the gate is
true. No sentinel value fixes it. Gate on numeric `> 0`, or restructure to a flat read.
This killed three separate proposed fixes before it was understood.

**Operator/operand type validity is a UI-only signal.** Shortcuts offers comparison
operators based on the left operand's resolved type. A numeric condition on a text-typed
operand renders **red**, is structurally valid in the file, and fails at runtime. No
file-level analysis can detect it — not the validator, not the catalog, not decryption.
The user's on-device eyeball found this class; it is a first-class evidence channel.

**Cycle 15 addendum — NOT a new donor-verified fact, a traced one:** the specific claim
that "Get Item From List accepts a bare Text WFInput without itself erroring" (needed to
explain how the failure surfaced one action *later*, at the Get Dictionary Value call,
rather than at the Get Item From List call itself) is **inferred from the device error's
own location**, not confirmed by a dedicated donor. It was not treated as license to guess
a fix, though: the fix itself (`get_value()`) does not depend on this claim being exactly
right — it simply stops stringifying the array in the first place, which is correct
regardless of exactly how Get Item From List would have handled the corrupted Text input.

---

## 5. Donor shortcuts — device ground truth

Eight-plus, built by the user in Shortcuts.app on the target iPhone, exported here,
decrypted via the `aea decrypt` + `aa extract` recipe (`docs/BUILD-NOTES.md:619`). **This
channel has been decisive every time it was used.** Cycle 15 did **not** request or use a
new donor: the fix follows directly from (a) the device's own reported error string, (b)
a direct read of the generator's source showing the one call chain that string can refer
to, and (c) this artifact's own already-established write-side behaviour for the same
field (recent_sessions is already written back as a genuine List elsewhere in the same
file) — no unverified plist construct was introduced; the fix *removes* a coercion step
rather than adding one.

| donor | settled |
|---|---|
| `Donor - apps`, `Donor - notes` | Notes action shapes; proved signed artifacts are decryptable |
| `Donor 3` | numeric constructs; killed three ranked candidates; closed DEV-05 |
| `Donor 4` / `Donor 4.1` | **A/B pair** — isolated the coercion aggrandizement exactly (`WFCoercionVariableAggrandizement`/`WFNumberContentItem`) |
| `Donor 5` | for the 14 `WFConditionalActionString` sites — **still not analysed, past breadcrumb J** |
| `Donor 6` | miswired (trailing space, misrouted input) — superseded |
| `Donor 6.1` | flat vs dotted reads; present-but-empty; `"null"` coercion |
| `Donor 7` / `Donor 7.1` | **CLOSED cycle 14.** CLOCK block Date→Date chain; `format.date`'s real pattern key. |
| `Donor 8` | **CLOSED cycle 14.** `shownote` reads `WFInput`, not `target`. |

---

## 6. Open items, ranked

### Blocking symptom 1 — still open pending device confirmation
1. **Device pass on build `2026-08-15n`.** Everything below this line was fixed and
   locally verified in cycle 15; nothing in this project can confirm it beyond that
   without a device run. **This is the user's call, not a directive.**

### Resolved this cycle (cycle 15)
- ~~The breadcrumb E→F blocker~~ — `recent_sessions` read via `read_value()` then fed
  to `getitemfromlist`; see §1–§2.
- ~~Four sibling sites of the same class~~ — `recent_sessions` (CLOSE),
  `profile_snapshot.enabled_exits`, `exit_events`, `exit_stats.<type>.samples`. The last
  sits on the OPEN critical path (I→J).
- ~~Recurrence guard~~ — `verify_compound_value_reads()`, axis 8. Known limitation: it
  matches literal string keys only; `exit_stats.<type>.samples` (a dynamic, text_token-built
  key) is NOT mechanically covered and was found by manual systematic scan.

### New, found but NOT fixed this cycle (recorded, not dropped)
- **`exit_events` is entirely absent from the bootstrap `state.json` template.** Same
  STATE-SHAPE category as `KNOWN_SENTINEL_EXISTENCE_GATES` (item 9 below). The cycle-15
  coercion fix stops double-corrupting the type once a value exists, but does not
  establish the key exists on a device that has never recorded an exit. Needs the same
  bootstrap-seed-plus-rebind treatment cycle 14 did for `settings_snapshot`/`State`.
  Candidate for the next cycle that touches this area.

### Agreed scope changes, still not applied (unchanged from before cycle 14)
2. **Cut brightness/volume manipulation from the MVP.** User decision, reaffirmed
   2026-08-15. Still not implemented — `restore_managed_settings`, `dim()`, `silence()`,
   `settings_snapshot` all still ship. The 18 uncoerced `setbrightness`/`setvolume`
   operand sites found by the cycle-14 type audit are the SAME class as the fixed
   math/getitemfromlist sites and would need identical coercion treatment if/when this
   is un-deferred.

### MVP-critical, independent of OPEN — resolved cycle 14, pending device confirmation
3. **Control Room open flow.** The `shownote` key fix should eliminate the reported
   picker + editable-box symptom; Open Control Room is read-only, Status has its own
   read path. Build `2026-08-15m`/`n`, locally validated/signed/decrypt-verified.
   **Not yet device-confirmed** — see §10.

### Known, non-blocking
4. **`WFItems` wrapper** — iOS wraps variable-bearing list rows as
   `{"WFItemType": 0, "WFValue": <WFTextTokenString>}`; ours omits the wrapper, so rows
   render blank. **Two instances confirmed** (index shifted again by cycle 15's
   regeneration, re-locate by content not number). Shape already recovered from Donors
   4/4.1.
5. **Donor 5 / 14 `WFConditionalActionString` sites** — still unopened. Past breadcrumb J.
6. **`If [Audit Token] contains` renders red** (Sentient-only) — out of scope while
   Sentient stays parked.

### Deferred by explicit decision
7. **DEV-06 — restore-ownership check.** `changed_at` and `changed_by_session_id` are
   written at 20 sites and **read nowhere**. Moot if item 2 (brightness/volume cut)
   proceeds.
8. **`cooldown_until` sentinel** — device-verified safe, leave untouched.
9. **`KNOWN_SENTINEL_EXISTENCE_GATES`** (`pending_exit`, `active_session`) — same
   unimplementable-gate construct as the settings_snapshot defect cycle 11/12 fixed, but
   deliberately not touched. `exit_events`'s new bootstrap-seed gap (above) is the same
   family; consider bundling all three into one future cycle.

### Before any ship
10. Strip `BUILD_STAMP`, `ROUTER_TRACE`, `OPEN_BISECT` and the ten breadcrumbs. All are
    single-constant toggles; removal documented at `tools/build_state_engine.py` (search
    for `OPEN_BISECT =`).
11. Repo has **no `.gitignore`**, which is why `.DS_Store` and `__pycache__` keep
    appearing.
12. Re-fork Sentient (`tools/build_sentient.py`) once Dumb is device-confirmed, so it
    picks up all cycle-14 AND cycle-15 fixes.

---

## 7. Technique — what actually worked

Recorded because it was learned expensively and is not obvious.

- **Fix whole classes, never site-by-site.** Reaffirmed a third time in cycle 15: fixing
  only the ONE site the device error named (`recent_sessions` in `open_pipeline()`) would
  have left the OPEN path blocked a second time, later, at `complete_pending_exit()`'s
  `exit_stats.<type>.samples` — on the very same I→J span breadcrumbs already bracket.
- **Read the error text, not just the breadcrumb letter — INVERTED THIS CYCLE.** Every
  prior cycle used this to recognise a correct fix behind an unchanged letter. Cycle 15
  used the inverse: an *advanced* letter (D→E) with a *different* error text means a NEW
  defect, not the old one returning. Both directions of the same discipline.
  A subtlety worth keeping: the device report language ("reached breadcrumb E") means E's
  own alert *fired*; the failure is strictly *after* E, not at it. Don't conflate "last
  letter seen" with "letter that failed."
  **Note on this cycle's own wording:** the falsification_test in cycle 14 predicted this
  outcome twice — once as "D, then continuing PAST E" (E confirmed working) and once
  implicitly assuming the run might stop exactly at D. The device report landing on "E,
  then a new failure" is consistent with (not a refutation of) that prediction; it simply
  means the run got one breadcrumb further than the minimum the prediction required.
- **Keep breadcrumbs in between cycles.** Confirmed working exactly as designed a second
  time: E localises the cycle-15 defect to a span of ~80 actions instead of the whole file.
- **A systematic (grep/scan), not manual-only, sweep for a whole class.** Cycle 15's scan
  (every `read_value()` site × every List-consumer WFInput reference) found a site
  (`exit_stats.<type>.samples`) that manual reading alone found only because the scan
  pointed at it first — matching cycle 14's own lesson about the nested-descent audit.
- **A build guard's own blind spot should be written down next to the guard**, not just
  fixed manually and forgotten. `verify_compound_value_reads()` cannot see a
  text_token-built dynamic key; that limitation is now a comment beside
  `COMPOUND_STATE_KEYS` in the source, not just in this file.
- **A guard's first draft can be too broad — test it against a KNOWN-good case before
  trusting it.** The first version of `verify_compound_value_reads()` flagged EVERY
  `read_value()` read of a compound key, including the legitimate text-display-only read
  (`manual_note_refresh()`'s "Snapshot Exits") — a false positive caught by running the
  guard immediately, before regenerating, and narrowed to only flag reads that are ALSO
  consumed by a List-typed action.
- **Ask the user to build donors — but recognise when a fix doesn't need one.** Cycle 15
  found and fixed its defect entirely from source-tracing plus the device's own error
  string, with zero new donor request — the fix *removes* an unverified-in-effect
  coercion step rather than adding a new construct, so the project's "never fabricate"
  rule was never at risk of being violated.
- **Idempotency is cheap insurance for a self-modifying generator.** Cycle 15's fix was
  verified idempotent the same way as every prior cycle's.
- **Signed `.shortcut` files are decryptable** — verify what actually shipped rather than
  trusting unsigned source plus an mtime. Confirmed again this cycle: the predicted
  breadcrumb shift (A–E unchanged, F–I −1, J −2) was verified against the DECRYPTED
  shipped artifact, not assumed from action-count arithmetic.
- **State a prediction and its refutation criteria before each device test.** Cycle 15's
  is in §1 and in the debug session's Current Focus `falsification_test`.

---

## 8. Type audit, cycle-14 nested-descent pass (unchanged by cycle 15)

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

Total: 227 numeric-field sites inspected → 85 offenders → 67 fixed, 18 deferred by
explicit decision, 0 unexplained. (This is a NUMERIC-operand audit, axis 6b — a
different axis from cycle 15's STRUCTURED-value audit, axis 8. See §2's table for the
cycle-15 numbers: 55 `read_value()` target names scanned, 5 offenders, 5 fixed, 0
deferred, 1 known-uncoverable-by-guard.)

---

## 9. Related todos

- `.planning/todos/pending/2026-08-13-fix-open-routing-and-test-circle-sequence-error.md`
  — the origin of this session. Its symptom 2 is **closed**; its symptom 1 is item 1 in §6.
- `.planning/todos/pending/2026-08-14-repair-ios-26-automation-onboarding.md`
  — **independently corroborated by this session.** Still unfixed in the generator and
  both Note bodies.
- **Candidate new todo (not filed yet):** fold cycle 15's axis-8 rules
  (`read_value()` vs `get_value()`, when each applies) into `.claude/CLAUDE.md` §
  Conventions' seven-axis list, once this cycle is device-confirmed — it is currently
  only documented in the generator's own comments and in this file.

## 10. Resume checklist

1. Read `.claude/CLAUDE.md` § Conventions.
2. Confirm branch is `codex/automation-parameter-diagnosis`.
3. **If a device pass on build `2026-08-15n` has happened:** read the reported letter and
   error text (if any) against §1's prediction and the debug session's CYCLE 15
   `falsification_test`, and update accordingly.
4. **If not:** nothing further is required from this session before that device pass —
   §6 item 1 is the only blocking item, and it is the user's call when to run it.
5. Once Dumb is device-confirmed: re-fork Sentient (`tools/build_sentient.py`), then
   revisit §6 items 4/5/6/7/9 and the new `exit_events` bootstrap gap as the next
   cycle's candidates — none of them can affect the OPEN-path measurement.
