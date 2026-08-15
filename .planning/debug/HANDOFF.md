# PROSOCHĒ OPEN-path debug — consolidated handoff

**Status: PAUSED, clean.** Nothing in flight. Working tree committed. Safe to resume cold.

This file is the **single authoritative entry point** for resuming. It consolidates the
per-cycle working documents (`cycle10-orchestrator-findings.md`,
`cycle13-user-findings.md`, `TYPE-AUDIT-first-pass.md`, `DO-NOT-RUN-BUILD-J.md`), which
have been folded in here and deleted; their full text remains in git history.

| artifact | role |
|---|---|
| **this file** | resume here |
| `open-routing-sequence-error.md` | full session checkpoint / audit trail (~300 KB) |
| `.claude/CLAUDE.md` § Conventions | the durable authoring rules — **read before generating any plist** |
| `docs/BUILD-NOTES.md` §13–17 | deviations, capability findings, ship checklist |
| `unsupported-device-import.md` | a **separate, unrelated** debug session — do not merge |

Branch `codex/automation-parameter-diagnosis`. Nothing pushed. Never switch to
`codex/prosochedebug1` or `codex/round1` — both predate every fix here, and rebuilding
from either silently reproduces all three original symptoms.

---

## 1. Where the work stands

Current build **`2026-08-14k`**, committed, signed, both forks.

Three symptoms were reported on 2026-08-13. Two are closed and device-verified.

| # | symptom | status |
|---|---|---|
| 2 | `No value provided … Set Dictionary Value … key "sequence"` | **CLOSED**, device-verified |
| 3 | Control Room note bootstraps empty | **CLOSED**, device-verified |
| 1 | OPEN path never reaches the intervention | **OPEN** — now failing in span D→E |

Symptom 1 has moved a long way. Breadcrumb bisection reports the earliest remaining
defect, and it has advanced `B → C → D` across builds `h`, `i`, `k`.

Latest device result (build `k`): reached **letter D**, then

> Get Time Between Dates failed because Shortcuts couldn't convert from Text to Date.

No screen darkening — the numeric restore gates held.

**Breadcrumb positions (Dumb; Sentient +2), unchanged for four builds:**
`A=92 B=147 C=168 D=286 E=306 F=415 G=424 H=458 I=473 J=527`

---

## 2. The seven defect axes — all found, all guarded

Every defect this session was **systematic**, not a one-off: a generator-wide
misunderstanding of the plist format. Each is now asserted by a build guard in
`tools/build_state_engine.py`, so the class cannot silently return.

| # | axis | sites fixed | how it presented |
|---|---|---|---|
| 1 | wrong parameter key name | 147 | "No value provided …" |
| 2 | value envelope, `str` | 367 | fields silently empty |
| 3 | value envelope, `AttributedString` | 2 | empty note body |
| 4 | required picker enum missing | 2 | "Please choose a value …" |
| 5 | variable slot took wrong envelope | 25 | "Please choose a value …" |
| 6 | operand type / coercion | 20 Dumb, 25 Sentient | red operator, runtime failure |
| 7 | state shape absent before read | 8 keys | "no value was found for dictionary key" |

**The full rules are in `.claude/CLAUDE.md` § Conventions.** Read them before touching the
generator. The two traps that cost the most cycles:

- Rules 2 and 5 are **inverses**. String-typed *parameters* need `WFTextTokenString`;
  variable *slots* need the bare `WFTextTokenAttachment`. Every sweep that checked for the
  presence of one was blind to the other.
- Axis 6 was **scoped too narrowly** — applied only to numeric comparisons. It is general:
  *any* non-text parameter fed by a variable reference needs an explicit coercion
  aggrandizement. This is the live defect (§3).

---

## 3. The immediate blocker — date coercion

**Verified statically.** All five `gettimebetweendates` actions pass bare text templates
into date-typed parameters with **zero coercion aggrandizements**:

| action | parameters |
|---|---|
| 15, 292, 317, 334, 490 | `WFInput`, `WFTimeUntilFromDate` |
| 17 | `adjustdate.WFDate` |
| 19 | `format.date.WFDate`, `WFDateFormatString` |

**Action 292 is in span D→E** — exactly where build `k` stops.

**A second, independent defect on the same action.** `format.date` action 19 carries:

```
WFDateFormatStyle  = 'Custom'
WFDateFormat       = 'Custom'      <- the literal word, not a UTS#35 pattern
WFDateFormatString = TEXT-TEMPLATE '￼'
```

The UI renders `WFDateFormat` as the Format String, showing the word "Custom". Establish
which key iOS actually reads; correct or remove the other.

**Do not guess the Date `CoercionItemClass`.** Donor evidence is required — see §5.

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

**Consequence, load-bearing:** a read-then-`has any value` gate on a dotted path is
**unimplementable**. The read raises unless the final key exists; if it exists, the gate is
true. No sentinel value fixes it. Gate on numeric `> 0`, or restructure to a flat read.
This killed three separate proposed fixes before it was understood.

**Operator/operand type validity is a UI-only signal.** Shortcuts offers comparison
operators based on the left operand's resolved type. A numeric condition on a text-typed
operand renders **red**, is structurally valid in the file, and fails at runtime. No
file-level analysis can detect it — not the validator, not the catalog, not decryption.
The user's on-device eyeball found this class; it is a first-class evidence channel.

---

## 5. Donor shortcuts — device ground truth

Eight built by the user in Shortcuts.app on the target iPhone, exported here, decrypted via
the `aea decrypt` + `aa extract` recipe (`docs/BUILD-NOTES.md:619`). **This channel has been
decisive every time it was used**, and outranks the ToolKit catalog, which carries no
required/optional bit and omits the control-flow identifiers entirely.

| donor | settled |
|---|---|
| `Donor - apps`, `Donor - notes` | Notes action shapes; proved signed artifacts are decryptable |
| `Donor 3` | numeric constructs; killed three ranked candidates; closed DEV-05 |
| `Donor 4` / `Donor 4.1` | **A/B pair** — isolated the coercion aggrandizement exactly |
| `Donor 5` | for the 14 `WFConditionalActionString` sites — **not yet analysed** |
| `Donor 6` | miswired (trailing space, misrouted input) — superseded |
| `Donor 6.1` | flat vs dotted reads; present-but-empty; `"null"` coercion |
| **`Donor 7`** | **dates — PROVIDED 2026-08-15, NOT YET ANALYSED** |
| **`Donor 8`** | **entity/file refs — PROVIDED 2026-08-15, NOT YET ANALYSED** |

**Donors 7 and 8 were supplied at the user's initiative and deliberately left untouched.**
They are the first work of the next cycle:

- **Donor 7** should settle the Date `CoercionItemClass` **and** the
  `WFDateFormat` / `WFDateFormatStyle` / `WFDateFormatString` question — i.e. all of §3.
- **Donor 8** should settle entity/file references, and `shownote.target` is a live suspect
  for the Control Room note-picker fault (§6).

---

## 6. Open items, ranked

### Blocking symptom 1
1. **Date coercion** (§3) — analyse Donor 7, fix all 13 date-parameter sites as one class,
   plus the `format.date` key confusion. Highest priority.
2. **Type audit, second pass.** The first pass is folded into §8 below. Its classifier only
   inspected **top-level** parameter shapes and did not descend into the nested
   `{"Type":"Variable","Variable":{…}}` wrapper, so its "zero coerced" counts
   **under-report** — build `i` demonstrably added 20 conditional coercions that it missed.
   Redo with nested handling before scoping any fix from those numbers.

### Agreed scope changes, not yet applied
3. **Cut brightness/volume manipulation from the MVP.** User decision, 2026-08-14. Justified
   by the project's own capability audit, which records Get-current-brightness/volume as
   UNVERIFIED and prescribes exactly this fallback. Removes `restore_managed_settings`,
   `dim()`, `silence()` and the `settings_snapshot` machinery — the source of the impossible
   gate, the `Session ID` scope defect, the write-only ownership fields and a black-screen
   risk. Record as a deviation citing the audit's fallback clause.
4. **Stale-state rebind.** Actions 37–41 accept a stored `state.json` on three checks the
   device's file passes; the bootstrap branch at 52–81 saves a new file but **never rebinds
   `State`**, which stays bound to the parse of the old one. Repair is ~2 actions (schema
   bump + rebind) but shifts every breadcrumb — do it together with item 3, which shifts
   them anyway, and recompute the spans once.
5. **`ROUTER_TRACE = False`.** The router restructure is device-verified; the
   `Input Key: [] / Empty ref: []` alert is now noise on every manual run. One line.

### MVP-critical, independent of OPEN
6. **Control Room open flow.** Choosing *Open Control Room* shows a picker listing **all**
   the user's notes; selecting the Control Room note opens an **editable text box** whose
   contents are **appended to the note**. Two faults: the note should be resolved directly,
   and opening must be read-only. The append path is a data-integrity risk — a stray tap
   writes into the ledger. Suspect `shownote.target`; Donor 8 may settle it.

### Known, non-blocking
7. **`WFItems` wrapper** — iOS wraps variable-bearing list rows as
   `{"WFItemType": 0, "WFValue": <WFTextTokenString>}`; ours omits the wrapper, so rows
   render blank. **Two instances confirmed** (actions ~1164 and the Mirror templates
   section), so treat as a class fix. Shape already recovered from Donors 4/4.1.
8. **Donor 5 / 14 `WFConditionalActionString` sites** — these are *right-hand* operands, and
   the operator picker is driven by the **left** input only, so establish whether they are
   genuinely defective or merely residual before fixing. All past breadcrumb J.
9. **`If [Audit Token] contains` renders red** — axis-5 operator/operand-type validity, on a
   string operator this time. Needs the operand's type established.
10. **`Screenshot 2026-08-14 at 11.55.12 pm.png`** — never examined.

### Deferred by explicit decision
11. **DEV-06 — restore-ownership check.** `changed_at` and `changed_by_session_id` are
    written at 20 sites and **read nowhere**, so the ownership check the restore path is
    meant to perform does not exist. `Session ID` is also mis-scoped (assigned under
    `[OPEN → not-in-cooldown → genuine-open]`; only 2 of 20 writes share that ancestry), but
    fixing the scope would not help while nothing consults the owner. Implementing it is a
    **design change, not a bug fix**. Moot if item 3 proceeds.
12. **`cooldown_until` sentinel** — device-verified safe, leave untouched at generator lines
    1249, 1258, 1300. `"null"` coerces to numeric false without error, and its only consumer
    is the numeric comparison at action 170.
13. **`KNOWN_SENTINEL_EXISTENCE_GATES`** — `pending_exit` and `active_session` carry the same
    unimplementable gate construct but were deliberately not changed: `pending_exit` is
    absent from the bootstrap template and `active_session` is a bare JSON null, so a flat
    read returns nothing, *passes* `is not "null"`, and would run the nested dotted read
    against a missing parent — trading a latent hard error for an immediate one.

### Before any ship
14. Strip `BUILD_STAMP`, `ROUTER_TRACE`, `OPEN_BISECT` and the ten breadcrumbs. All are
    single-constant toggles; removal documented at `tools/build_state_engine.py:1080`.
15. Repo has **no `.gitignore`**, which is why `.DS_Store` and `__pycache__` keep appearing.

---

## 7. Technique — what actually worked

Recorded because it was learned expensively and is not obvious.

- **Fix whole classes, never site-by-site.** Bisection only ever reveals the *earliest*
  remaining defect, so incremental fixing costs one device round trip per site. Every defect
  here was systematic: 147, 367, 25, 20, 8 sites.
- **Read the error text, not just the breadcrumb letter.** *Three times* a correct fix looked
  refuted because the letter was unchanged while the error text had changed completely.
- **Keep breadcrumbs in between cycles.** A second defect then reports as a *later letter* —
  progress plus location — instead of an ambiguous repeat.
- **Ask the user to build donors.** Faster and more authoritative than any amount of static
  analysis for anything the catalog does not express.
- **Inspect the imported shortcut on device.** The red-operator class is invisible to every
  file-level tool by construction. The user found it by scrolling.
- **Signed `.shortcut` files are decryptable** — verify what actually shipped rather than
  trusting unsigned source plus an mtime. This corrected a claim in `CLAUDE.md` §8.
- **State a prediction and its refutation criteria before each device test.** This is what
  made "letter unchanged, error changed" legible instead of demoralising.

---

## 8. Type audit, first pass — ranked (superseded numbers, see §6 item 2)

⚠ Counts under-report; classifier did not descend into nested variable wrappers.

1. **Date parameters** — 5 actions, 13 sites. Device-confirmed failing.
2. **Numeric on non-conditional actions** — `math.WFInput` (42), `math.WFMathOperand` (28),
   `getitemfromlist.WFItemIndex` (31), `conditional.WFNumberValue` (30), `round` (3),
   `calculateexpression` (2), `count` (1). Build `i` coerced conditional *left operands
   only*; `math` at 275/319/323/325 is on the OPEN Heat path.
3. **`setbrightness.WFBrightness` (14) / `setvolume.WFVolume` (14)** — moot if the cut
   proceeds; resolve by deletion, not coercion.
4. **Entity / file / dictionary refs** — `appendnote.entity`, `shownote.target`,
   `documentpicker.save`, `setitemname`, `detect.dictionary`,
   `setvalueforkey.WFDictionary` (147), `repeat.each`. Entirely unchecked.
5. **Text-typed, expected bare** — `setvariable` (692), `gettext` (231). Control group.

---

## 9. Related todos

- `.planning/todos/pending/2026-08-13-fix-open-routing-and-test-circle-sequence-error.md`
  — the origin of this session. Its symptom 2 is **closed**; its symptom 1 is item 1 above.
- `.planning/todos/pending/2026-08-14-repair-ios-26-automation-onboarding.md`
  — **independently corroborated by this session.** The embedded onboarding instructions
  cannot produce a working automation as written, and the wrapper flow it prescribes
  (Text `OPEN` → Run Shortcut with Input = that Text) is exactly the configuration proven
  correct here by the INPUT PROBE: the probe received `RAW [OPEN] / NORMALISED [OPEN]`
  through a wrapper built that way. Still unfixed in the generator and both Note bodies.

## 10. Resume checklist

1. Read `.claude/CLAUDE.md` § Conventions.
2. Confirm branch is `codex/automation-parameter-diagnosis`.
3. Decrypt and analyse **Donor 7** → fix the date class (§3).
4. Decrypt and analyse **Donor 8** → entity refs and the Control Room flow (§6 item 6).
5. Apply items 3–5 of §6 together, recompute breadcrumb spans once.
6. Rebuild, validate `--target-macos 26 --target-platform ios`, sign, verify by decryption.
7. State the predicted letter and refutation criteria before handing the build over.
