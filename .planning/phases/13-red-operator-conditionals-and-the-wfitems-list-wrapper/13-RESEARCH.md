# Phase 13: Red-operator conditionals and the WFItems List wrapper - Research

**Researched:** 2026-08-17
**Domain:** iOS Shortcuts plist serialization — conditional operand envelopes and List row wrappers, via device-donor ground truth
**Confidence:** HIGH (both defect families settled by decrypted device-authored donors; every count re-measured against HEAD)

## Summary

**The phase's premise is half wrong, and the research settled which half.** Both defect
families were investigated by decrypting the three donors named in the ROADMAP and by
re-measuring every claimed count against the artifacts actually at HEAD. The result inverts
one family and massively expands the other.

**Family 1 — the `WFConditionalActionString` "red-operator" sites — is NOT a defect.**
`.planning/debug/Donor 5.shortcut` was decrypted (first analysis ever) and it contains
exactly the construct the ROADMAP suspected: a variable placed into a conditional's TEXT-slot
operand as a `WFTextTokenString` template, alongside a `WFInput` variable slot. That donor was
authored by iOS itself on the target iPhone, so it is device ground truth at the top of this
project's evidence hierarchy — and the generator's `token()` helper emits a **byte-identical**
shape. The 20 variable-bearing sites per fork are correct as they stand. There is no sweep to
perform, and performing one would replace a device-confirmed shape with a guess. The concrete
site the ROADMAP named as the starting point, `if_block("Previous Respected", 4, ...)`, turns
out not to be a member of this family at all — it passes a **raw literal** `"true"`/`"false"`,
never a `token()`.

**Family 2 — the `WFItems` List wrapper — is real, confirmed, and 33× larger than recorded.**
Donors 4 and 4.1 both confirm the wrapper shape verbatim. The ROADMAP records "2 confirmed
instances"; direct plist measurement finds **66 defective List actions carrying 660 unwrapped
variable-bearing rows, in each fork**. Every one of them originates from a single generator
function, `mirror_text()` at `tools/build_state_engine.py:651`, unrolled 66 times across the
Circle dispatch. The fix is one line at one site; a prototype that wraps all 660 rows was
built during this research and still passes validator gate A on both forks.

**Primary recommendation:** Do not touch the conditionals. Record Donor 5's refutation as a
first-class finding, fix `mirror_text()`'s single line, add one recurrence guard for the List
wrapper (plus one *pinning* guard that protects the now-confirmed conditional shape from a
future "fix"), and complete the three documentation updates. The phase's scope shrinks on one
axis and grows on the other.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Conditional operand serialization | Generator (`tools/build_state_engine.py`) | — | The plist is emitted wholesale by Python; there is no runtime tier that could correct it |
| List row wrapper serialization | Generator (`mirror_text()`) | — | Single emitter; Sentient inherits by forking the built XML |
| Recurrence prevention | Build-time guards (`verify_*` in the generator) | `docs/*.py` checkers | Project convention: guards run before the single `SOURCE.write_bytes()`; checkers assert post-hoc over the written artifact |
| Fork propagation | `tools/build_sentient.py` | — | Sentient reads `src/PROSOCHE-Dumb.xml` as its source, so generator fixes propagate on rebuild |
| Structural validity | Shortcuts Playground validator (gate A) | gate B (advisory) | File-level only; cannot see operand-type validity |
| Runtime/visual correctness | Real iPhone (rung 3–4) | — | Red chips and blank rows are invisible to every file-level tool |

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

All implementation choices are at Claude's discretion — discuss phase was skipped per user
setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide
decisions.

### Non-negotiable project constraints that bind this phase

- **Never fabricate a parameter shape.** The Donor 5 decrypt is the evidence source for the
  conditional TEXT-slot operand; the Donor 4 / 4.1 decrypt is the evidence source for the
  `WFItems` row wrapper. If a donor does not settle a shape, record the deviation and use the
  safest fallback rather than guessing (`.claude/CLAUDE.md` § Capability, § Conventions).
- **Two-gate validator rule** (`.claude/CLAUDE.md` §1 `### Exact validator invocation`):
  gate A `--target-macos 26 --target-platform all` is mandatory and must pass clean; gate B
  `--target-macos 27 --target-platform all` is advisory, exits 1 with exactly one permitted
  waived line per fork, and must never be chained into a definition of done.
- **Build provenance guard:** `git merge-base --is-ancestor 7ca8ebbf... HEAD` must hold before
  running `tools/build_state_engine.py` or `tools/build_sentient.py`.
- **Definition of done includes signing.** A valid XML draft without a signed `.shortcut` is
  not a stopping point; signed filenames must equal the exact display names
  (`PROSOCHĒ — Nine Circles — Dumb.shortcut`, `… — Sentient.shortcut`).
- **Fix whole classes, never site-by-site** (`.claude/CLAUDE.md` § Debugging technique).
- **Guards must be sensitivity-demonstrated** against a synthetically reverted artifact — a
  guard that cannot fail proves nothing.

> ⚠️ **One locked constraint is STALE and must not be followed verbatim.** The signed display
> names are no longer `Dumb`/`Sentient`. Phase 11 renamed the *products*: the canonical
> display names are **`PROSOCHĒ — Nine Circles — Core`** and
> **`PROSOCHĒ — Nine Circles — Aware`**, verified against `artifacts/shortcuts/MANIFEST.md`
> rows 40–45 and `tools/build_sentient.py:45-46` (`CORE_NAME` / `AWARE_NAME`). The *source
> filenames* deliberately remain `src/PROSOCHE-Dumb.xml` / `src/PROSOCHE-Sentient.xml`.
> `docs/manifest_check.py` asserts the signed basenames (DIST-04); following the CONTEXT.md
> wording literally would fail that checker. [VERIFIED: MANIFEST.md + build_sentient.py source]

### Deferred Ideas (OUT OF SCOPE)

None — discuss phase skipped.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CIRC-04 | Confession asks for a free-text intention and then a time boundary (2/5/10/15/custom) | **Indirect.** No Confession-owned `is.workflow.actions.list` was found; the boundary picker is a `choosefrommenu`, which is untouched by both defect families. This requirement is protected by regression, not repaired — the rebuild must leave it green (`docs/phase5_self_check.py`, currently passing). Flagged below as a weak mapping. |
| CIRC-07 | The Mirror shows a precise behavioural reflection built only from recorded facts | **Direct and primary.** All 66 defective List actions are the Mirror's fact-gated template selectors emitted by `mirror_text()`. Unwrapped rows render blank on device, so the Mirror can select an empty template — the exact failure CIRC-07 forbids. This is the requirement the phase actually repairs. |
| ROOM-03 | The Note gives exact steps for Automation B (Is Closed / pass input `CLOSE`) | **Indirect.** The Note body is a hand-authored text template, not a List. Protected by `docs/note_identity_check.py` (currently passing). Flagged below as a weak mapping. |
| DIST-01 | Both forks pass the Shortcuts Playground validator at the iOS 26 target | **Direct.** Gate A measured PASS on both forks at HEAD, and measured PASS again on the wrapped-row prototype built during this research — the fix does not regress DIST-01. |
| DIST-02 | Both forks sign successfully into importable `.shortcut` files | **Direct.** Signing via `sign-shortcut --name "<canonical display name>" --mode anyone`; `docs/manifest_check.py` asserts the resulting basenames and digests. |

**Mapping caveat for the planner:** CIRC-04 and ROOM-03 have no defect site in either family.
Treat them as *regression-protection* requirements satisfied by the existing checkers staying
green through the rebuild, and say so explicitly in the plan rather than inventing work to
"address" them. [VERIFIED: grep over generator + checker run]
</phase_requirements>

## Evidence Recovered This Session

All three donors were decrypted with the `.claude/CLAUDE.md` §8 recipe
(`python3` auth-data extraction → `openssl x509` pubkey → `aea decrypt` → `aa extract` →
`plutil -convert xml1`). All three succeeded on the first attempt.

| Donor | Status before | Status now | What it settles |
|---|---|---|---|
| `Donor 5.shortcut` | never analysed | **decrypted, 196-line plist** | The conditional TEXT-slot operand envelope — settles it as ALREADY CORRECT |
| `Donor 4.shortcut` | shape "recovered" but unapplied | **decrypted, 224-line plist** | `WFItems` row wrapper + the `WFItemType` integer + the bare-string row case |
| `Donor 4.1.shortcut` | shape "recovered" but unapplied | **decrypted, 235-line plist** | Same wrapper, plus the numeric-conditional RHS slot (`WFNumberValue`) and the coercion aggrandizement |

### Donor 5 — the conditional operand, literal XML

The single `is.workflow.actions.conditional` mode-0 action in Donor 5, verbatim from the
decrypted plist:

```xml
<key>WFWorkflowActionIdentifier</key>
<string>is.workflow.actions.conditional</string>
<key>WFWorkflowActionParameters</key>
<dict>
    <key>GroupingIdentifier</key>
    <string>5D55FD5B-1180-4720-ADF4-61C7805056EB</string>
    <key>WFCondition</key>
    <integer>4</integer>
    <key>WFConditionalActionString</key>
    <dict>
        <key>Value</key>
        <dict>
            <key>attachmentsByRange</key>
            <dict>
                <key>{0, 1}</key>
                <dict>
                    <key>Type</key>
                    <string>Variable</string>
                    <key>VariableName</key>
                    <string>B</string>
                </dict>
            </dict>
            <key>string</key>
            <string>￼</string>
        </dict>
        <key>WFSerializationType</key>
        <string>WFTextTokenString</string>
    </dict>
    <key>WFControlFlowMode</key>
    <integer>0</integer>
    <key>WFInput</key>
    <dict>
        <key>Type</key>
        <string>Variable</string>
        <key>Variable</key>
        <dict>
            <key>Value</key>
            <dict>
                <key>Type</key>
                <string>Variable</string>
                <key>VariableName</key>
                <string>A</string>
            </dict>
            <key>WFSerializationType</key>
            <string>WFTextTokenAttachment</string>
        </dict>
    </dict>
</dict>
```

Answering each question the phase brief asked, from the literal XML above
[VERIFIED: decrypted device-authored donor]:

| Question | Answer |
|---|---|
| Does the operand live in `WFConditionalActionString`? | **Yes**, for a string-family comparison. |
| With what envelope? | **`WFTextTokenString`** — `string: "￼"` plus `attachmentsByRange` keyed `{0, 1}`. Not a bare `WFTextTokenAttachment`, not a plain string. |
| What is the inner attachment shape? | A **bare** `{Type: "Variable", VariableName: "B"}` dict — **not** re-wrapped in a `Value`/`WFSerializationType` envelope. |
| What `WFCondition` accompanies it? | `<integer>4</integer>` — an **integer**, and the string-family "is" code. |
| Is `WFInput` present alongside? | **Yes, simultaneously.** `WFInput` is the LEFT operand and takes the *opposite* envelope: `{Type: "Variable", Variable: {Value: {...}, WFSerializationType: "WFTextTokenAttachment"}}`. |
| Any coercion aggrandizement? | **None** on either side. Both operands are text, and code 4 is the string comparator — coercion is not required for the text family. |

**Cross-check against the generator.** `tools/build_state_engine.py:145-148` defines:

```python
def token(name: str):
    return {"Value": {"string": "￼", "attachmentsByRange":
            {"{0, 1}": {"Type": "Variable", "VariableName": name}}},
            "WFSerializationType": "WFTextTokenString"}
```

This is structurally identical to Donor 5's `WFConditionalActionString` value, key for key.
The generator has been emitting the device-correct shape all along.

### Donor 4 / 4.1 — the `WFItems` List row, literal XML

Both donors carry the same `is.workflow.actions.list` action. The array mixes two row kinds:

```xml
<key>WFItems</key>
<array>
    <string>Circle</string>
    <dict>
        <key>WFItemType</key>
        <integer>0</integer>
        <key>WFValue</key>
        <dict>
            <key>Value</key>
            <dict>
                <key>attachmentsByRange</key>
                <dict>
                    <key>{0, 1}</key>
                    <dict>
                        <key>OutputName</key>
                        <string>Dictionary Value</string>
                        <key>OutputUUID</key>
                        <string>8ED9505C-5726-4B52-9EFC-92CF36E2CEB0</string>
                        <key>Type</key>
                        <string>ActionOutput</string>
                    </dict>
                </dict>
                <key>string</key>
                <string>￼</string>
            </dict>
            <key>WFSerializationType</key>
            <string>WFTextTokenString</string>
        </dict>
    </dict>
    <string>follows</string>
</array>
```

Findings [VERIFIED: two independent decrypted device-authored donors, byte-identical on this action]:

| Question | Answer |
|---|---|
| Is the `{"WFItemType": 0, "WFValue": <WFTextTokenString>}` claim correct? | **Confirmed exactly**, in both donors independently. |
| What does `WFItemType` 0 correspond to? | A **text** row. Only `0` was observed. Other row kinds (number, dictionary, file) are **not** exercised by either donor — see Open Questions. |
| Do plain literal rows need the wrapper? | **No.** Literal rows are emitted as **bare `<string>` elements** directly in the array (`"Circle"`, `"follows"`). The wrapper appears only when the row carries a variable/attachment. |
| Does the wrapper nest a full `WFTextTokenString`? | Yes — `WFValue` holds the complete `{Value: {string, attachmentsByRange}, WFSerializationType: "WFTextTokenString"}` envelope, unchanged. |

**This two-kind rule is the load-bearing detail.** A sweep that wraps *every* row would
corrupt the six bare-string rows in `list_items(EXIT_NAMES, ...)`. Wrap only rows that are
currently dicts.

### Bonus finding — Donor 4.1 settles the numeric-conditional RHS

Donor 4.1 differs from Donor 4 in exactly one action: its conditional is numeric. It shows
that the numeric right-hand operand does **not** use `WFConditionalActionString` at all:

```xml
<key>WFCondition</key><integer>2</integer>
<key>WFNumberValue</key><string>10</string>
```

…with the LEFT operand carrying the coercion aggrandizement:

```xml
<key>Aggrandizements</key>
<array>
    <dict>
        <key>CoercionItemClass</key><string>WFNumberContentItem</string>
        <key>Type</key><string>WFCoercionVariableAggrandizement</string>
    </dict>
</array>
```

Two things worth recording: `WFNumberValue` is serialized as a **`<string>`**, not an
`<integer>`; and the string and numeric RHS slots are mutually exclusive. Donor 4 (condition
100, "has any value") carries **neither** RHS slot — confirming that existence-family
conditions take no comparison target. The generator's `if_block()` already implements all
three cases correctly via its optional `number=` / `string=` keywords. [VERIFIED: decrypted donors]

## Measured Site Inventory at HEAD

Every count below was measured by loading `src/PROSOCHE-Dumb.xml` and
`src/PROSOCHE-Sentient.xml` with `plistlib` and walking the action array. **The ROADMAP's
numbers are wrong on both families** — report these instead.

### Family 1 — `WFConditionalActionString` (ROADMAP says 14)

| Measure | Dumb | Sentient |
|---|---:|---:|
| Total actions in artifact | 4346 | 4414 |
| Mode-0 conditionals carrying `WFConditionalActionString` | **192** | **195** |
| …of which are variable-bearing `WFTextTokenString` (the "Donor 5 family") | **20** | **20** |
| …of which are raw literal strings | 172 | 175 |
| Bare abandoned `"￼"` placeholders (the already-guarded defect) | **0** | **0** |

The 20 variable-bearing sites split as 19 at `WFCondition` 4 and 1 at `WFCondition` 99
(contains), in both forks. **All 20 match Donor 5 exactly and require no change.**

The ROADMAP's "14" traces to `.planning/debug/HANDOFF.md:155`, which records axis 6 as
"20 Dumb, 25 Sentient" — a different number again, and itself describing *operand
type/coercion*, a different axis from the text-envelope question. Neither figure survives
measurement. [VERIFIED: plistlib walk over both artifacts at HEAD]

### Family 2 — `WFItems` List wrapper (ROADMAP says 2)

| Measure | Dumb | Sentient |
|---|---:|---:|
| `is.workflow.actions.list` actions | 67 | 67 |
| …correct (bare-string rows only) | 1 | 1 |
| …**defective** (unwrapped dict rows) | **66** | **66** |
| Bare-string rows (correct) | 6 | 6 |
| **Unwrapped variable-bearing rows** | **660** | **660** |
| Already-wrapped rows | 0 | 0 |

Every defective action carries exactly 10 rows. The ROADMAP's "2 confirmed instances"
under-counts actions by 33× and rows by 330×. The "nine consecutive blank rows" described
from the screenshot is consistent with a 10-row action viewed with one row scrolled off.
[VERIFIED: plistlib walk over both artifacts at HEAD]

### Generator anchors

| Site | File:line | Emits | Verdict |
|---|---|---|---|
| `token()` | `tools/build_state_engine.py:145-148` | The conditional text-slot envelope | **Correct — matches Donor 5** |
| `if_block()` | `tools/build_state_engine.py:309-329` | `WFCondition` + `WFInput` + optional `WFNumberValue`/`WFConditionalActionString` | **Correct — matches Donors 4 / 4.1 / 5** |
| `list_items()` | `tools/build_state_engine.py:416-419` | 1 action, 6 bare-string rows | **Correct — matches Donor 4's bare-string rows** |
| **`mirror_text()`** | **`tools/build_state_engine.py:648-656`** | **66 actions × 10 unwrapped dict rows** | **THE defect — single point of failure** |
| `mirror_templates()` | `tools/build_state_engine.py:659-662` | The `text_token(...)` values fed to `mirror_text` | Correct in isolation; its output needs wrapping at the consumer |
| `mirror_and_voice()` | `tools/build_state_engine.py:665-679` | Calls `mirror_text` 3× | Unrolled ~22× by Circle dispatch → 66 |

The defective line is exactly one:

```python
# tools/build_state_engine.py:651
a = [action("is.workflow.actions.list", UUID=list_id, WFItems=list(items)),
```

`items` here is a tuple of `text_token(...)` dicts from `mirror_templates()`. They are placed
raw into the array with no `{WFItemType: 0, WFValue: …}` wrapper.

### The `if_block("Previous Respected", 4, ...)` site — not what the ROADMAP thought

The ROADMAP names this as "a concrete starting site" for the Donor 5 family. Measurement
shows it is **not a member of that family**:

- `tools/build_state_engine.py:675-676` and `:1196` call
  `if_block("Previous Respected", 4, string="true")` / `string="false"` — a **raw Python
  literal**, never `token(...)`. It has no variable in the text slot at all.
- The left operand is genuinely Text-typed: emitted actions 366→367→368 are
  `getvalueforkey("respected")` → `gettext` → `setvariable("Previous Respected")`, which is
  `read_value()`'s chain. A Text left operand with condition 4 (string "is") is the *valid*
  operator/operand pairing per `.claude/CLAUDE.md` § "Operator/operand type validity".
- Variable definedness was checked: `Previous Respected` is set at action index 368 and all
  44 uses occur at index 375 or later. **Zero uses precede the set**, so there is no dangling
  reference that would render a red chip.

**Conclusion:** at HEAD this site is structurally correct on every axis file-level analysis
can see. The red render observed on 2026-08-14 is not reproducible against the current
artifact, and the todo's own hedge — "This is *very likely* one of the 14 already-catalogued
sites" — was a guess that measurement now falsifies. The most probable explanation is that
the screenshot predates cycles 14–16 and Phases 9–12, several of which reworked exactly this
binding (`read_value()` / `get_value()`, cycle 15). [VERIFIED: plistlib walk + generator grep]
[ASSUMED: that the 2026-08-14 build differed at this site — not provable, the build is not retained]

### The screenshot does not exist

`.planning/debug/Screenshot 2026-08-14 at 11.55.12 pm.png` is **absent from the repository**.
Verified three ways: no `.png` under `.planning/` in this worktree (only two marketing
diagrams under `assets/`); the path does not exist in the main checkout; and
`git log --all -- '*.png'` returns only the initial refactor commit. The filename in
`HANDOFF.md` also contains a **U+2060 word-joiner** between `11.55.12` and `pm`, so it is not
merely a path-quoting problem.

**Planner impact:** no task may depend on reading this screenshot. Both defects it allegedly
showed have now been established independently and more precisely — family 2 by direct
measurement, family 1 by donor refutation — so nothing is lost, but the plan must not
schedule "read the screenshot" as an evidence step. If the user still holds the image, it is
a rung-4 item worth requesting for the historical record only, not as a gate.
[VERIFIED: filesystem + git history search]

## Standard Stack

This phase adds **no new dependencies**. The toolchain is fixed by the project.

### Core

| Tool | Version | Purpose | Why standard |
|---|---|---|---|
| Python 3 (stdlib `plistlib`) | ≥3.10 | Generator + all guards + all checkers | Already the entire build system; PEP 604 syntax required by the validator |
| Shortcuts Playground | 1.2.1 | `validate-shortcut`, `sign-shortcut` | Only toolchain on this machine that can validate/sign |
| `aea` + `aa` (macOS built-ins) | system | Donor decryption | The §8 recipe; used successfully three times this session |
| `shortcuts` CLI (macOS) | system | Real signer wrapped by `sign-shortcut` | No substitute; macOS-only |

**Installation:** none required. All tools verified present and working during this research.

### Alternatives Considered

| Instead of | Could use | Tradeoff |
|---|---|---|
| Editing `mirror_text()` in the generator | `tools/plist_text_edit.py` post-pass | Rejected — the generator is the single source of truth; a post-pass would not survive regeneration and violates "fix whole classes" |
| A new `docs/*.py` checker | An in-generator `verify_*` guard | Prefer the guard: project convention runs guards *before* `SOURCE.write_bytes()`, so a defect never reaches disk. A checker is post-hoc. Both is best — guard blocks, checker documents. |

## Package Legitimacy Audit

**Not applicable — this phase installs no external packages.** The entire change set is
Python standard library (`plistlib`, `json`, `uuid`) plus already-installed macOS and
Shortcuts Playground tooling. No registry lookup was required and none was performed.

## Architecture Patterns

### System Architecture Diagram

```
                    .planning/debug/Donor {4, 4.1, 5}.shortcut  (AEA1, device-authored)
                                        │
                          aea decrypt → aa extract → plutil
                                        │
                                        ▼
                            GROUND-TRUTH SHAPES
                    ┌───────────────────┴───────────────────┐
                    │                                       │
          conditional operand                        WFItems row
       (WFTextTokenString + WFInput)      ({WFItemType:0, WFValue:…} | bare str)
                    │                                       │
                    ▼                                       ▼
            ┌───────────────┐                    ┌─────────────────────┐
            │  NO CHANGE    │                    │  mirror_text():651  │
            │  20 sites/fork│                    │  wrap dict rows     │
            │  already match│                    │  leave str rows     │
            └───────┬───────┘                    └──────────┬──────────┘
                    │                                       │
                    └───────────────┬───────────────────────┘
                                    ▼
                    tools/build_state_engine.py  main()
                                    │
                    normalise_* ──► verify_* guards (21) ──┐
                                    │                       │ raise SystemExit
                                    ▼                       │ before any write
                    SOURCE.write_bytes(src/PROSOCHE-Dumb.xml)
                                    │
                                    ▼
                    tools/build_sentient.py  (forks the BUILT Dumb XML)
                                    │
                    re-runs 17 inherited guards ──► src/PROSOCHE-Sentient.xml
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
        12 × docs/*.py checkers        gate A (mandatory) / gate B (advisory)
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
                    sign-shortcut --name "PROSOCHĒ — Nine Circles — {Core,Aware}"
                                    │
                                    ▼
                    decrypt-verify the signed artifact  →  MANIFEST.md refresh
                                    │
                                    ▼
                            Phase 19 device UAT
```

### Component Responsibilities

| Component | File | Responsibility in this phase |
|---|---|---|
| `mirror_text()` | `tools/build_state_engine.py:648` | The one line to change |
| `list_items()` | `tools/build_state_engine.py:416` | Must be left alone — bare strings are correct |
| `token()` / `if_block()` | `:145`, `:309` | Must be left alone — Donor-5-confirmed |
| Guard harness | `:4160-4177` | Register the new guard(s) here |
| Sentient import list | `tools/build_sentient.py:13-32` | New guards must be added here too |
| Sentient guard block | `tools/build_sentient.py:~303-357` | And invoked here |
| `docs/manifest_check.py` | — | Asserts signed basenames + digests (DIST-04) |

### Pattern 1: The two-kind `WFItems` row rule

**What:** A List row is either a bare string (literal) or a `{WFItemType, WFValue}` dict
(variable-bearing). Never both, never a raw `WFTextTokenString` sitting directly in the array.

**When to use:** Every `is.workflow.actions.list` emission.

**Example** — the minimal correct transform, prototyped and validated during this research:

```python
# Source: Donor 4 / Donor 4.1 decrypted plists (device ground truth)
def _list_row(item):
    """Bare strings stay bare; attachment-bearing values take the iOS row wrapper."""
    return item if isinstance(item, str) else {"WFItemType": 0, "WFValue": item}

# tools/build_state_engine.py:651
a = [action("is.workflow.actions.list", UUID=list_id,
            WFItems=[_list_row(i) for i in items]), ...]
```

Applying this to all 66 actions wrapped exactly 660 rows and the result **passed validator
gate A** (`Validation passed.`, exit 0). [VERIFIED: prototype run this session]

### Pattern 2: Guards that pin a *confirmed-correct* shape

This phase needs an unusual guard. Family 1 is not a defect, but the ROADMAP, the pending
todo, and `HANDOFF.md` all assert it is — so the standing risk is that a future pass "fixes"
the 20 correct sites and breaks them. The established `verify_conditional_action_string()`
(`:2413-2446`) already guards the *bare-placeholder* variant; extend the same function, or add
a sibling, to assert positively that a variable-bearing `WFConditionalActionString` **is** a
`WFTextTokenString` with a `￼` string and a non-empty `attachmentsByRange`.

**Anti-pattern to avoid:** deleting the ROADMAP claim without leaving a tombstone. The
project's own convention (`HANDOFF.md`, `CAPABILITY-DECISIONS.md`) is to record refutations,
because an un-recorded refutation gets re-litigated next cycle.

### Anti-Patterns to Avoid

- **Sweeping all 192/195 `WFConditionalActionString` sites.** Only 20 are variable-bearing
  and all 20 are correct. A blanket sweep would convert 172 correct raw literals into
  something no donor supports.
- **Wrapping bare-string List rows.** Donor 4 shows literals stay bare. Wrapping the 6 rows
  in `list_items(EXIT_NAMES, …)` would be an unforced regression on EXIT-08.
- **Hand-editing `src/PROSOCHE-Sentient.xml`.** It is generated by forking the built Dumb XML;
  any direct edit is erased on the next `build_sentient.py` run.
- **Chaining gate B into the definition of done.** Its waiver is permanent, so it can never
  exit 0.
- **Treating the missing screenshot as a blocker.** Both defects are settled without it.

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---|---|---|---|
| Reading a signed `.shortcut` | A plist parser over the AEA1 container | The §8 `aea decrypt` + `aa extract` recipe | `plutil`/`xxd` see the encrypted container, not the payload — worked first try on all three donors |
| Finding defect sites | Line-number-based edits | `plistlib` walk over the emitted XML + content-based re-location | Line numbers shift on every regeneration; the todo itself warns of this |
| Fork propagation | Editing Sentient separately | Rebuild via `build_sentient.py` | It forks the built Dumb XML and asserts `frozen Dumb source changed` |
| A new verification harness | Custom test runner | The existing 21 `verify_*` guards + 12 `docs/*.py` checkers | Already wired, already green, already the project's definition of done |
| Guessing `WFItemType` for non-text rows | Inference from `0` | Leave unaudited; only text rows are needed here | Donors cover only `0`; guessing violates the do-not-fabricate rule |

**Key insight:** every shape this phase touches is already settled by a decrypted donor. The
work is *applying* recovered evidence, not discovering it — which is precisely why the phase
was blocked for three cycles: nobody ran the decrypt.

## Runtime State Inventory

This is a generator/serialization phase, not a rename or data migration. Each category was
checked explicitly.

| Category | Items Found | Action Required |
|---|---|---|
| Stored data | **None.** `state.json` schema is untouched; no key names, sentinels, or `SCHEMA_VERSION` change. Verified: the fix alters only `WFItems` row framing inside List actions, which hold Mirror display templates, never persisted state. | None |
| Live service config | **None.** No external service. Personal Automations reference the shortcut by name; display names are unchanged by this phase (`Core`/`Aware` already current since Phase 11). | None |
| OS-registered state | **None.** No Task Scheduler / launchd / pm2 analogue. The user's two Personal Automations point at the shortcut *name*, which does not change. | None |
| Secrets / env vars | **None.** No secrets anywhere in this project; no `.env`, no SOPS. | None |
| Build artifacts | **Yes — the signed artifacts and MANIFEST.** `artifacts/shortcuts/PROSOCHĒ — Nine Circles — {Core,Aware}.shortcut` and all six `artifacts/shortcuts/MANIFEST.md` rows (sizes + SHA-256) become stale the moment the source is regenerated. | Re-archive, re-sign, refresh all six MANIFEST rows, and re-run `docs/manifest_check.py` |

**The one real runtime consideration:** a user who already imported the current signed build
keeps the blank-row Mirror until they re-import. That is inherent to Shortcuts distribution
and needs no migration — but the plan should note it so Phase 19 UAT re-imports rather than
testing a stale install.

## Common Pitfalls

### Pitfall 1: Wrapping every row instead of only dict rows

**What goes wrong:** The six bare-string rows in `list_items(EXIT_NAMES, …)` get wrapped.
**Why it happens:** A naive `[{"WFItemType": 0, "WFValue": i} for i in items]` sweep.
**How to avoid:** Branch on `isinstance(item, str)`, as in Pattern 1.
**Warning signs:** The measured post-fix count is not exactly 660 wrapped + 6 bare per fork.

### Pitfall 2: Guard passes because it can never fail

**What goes wrong:** A guard written against the post-fix artifact only, never exercised
against the defect.
**Why it happens:** Writing the guard after the fix and never reverting.
**How to avoid:** The project's established sensitivity demonstration — revert the generator
line (or `git stash` the source), rebuild, confirm the guard raises `SystemExit` with the
expected message *before* `SOURCE.write_bytes()`, then restore and rebuild clean. Phase 12
recorded exactly this pattern (`.planning/phases/12-*`: "seeder commented out + source
reverted → exited 1 with the identical message before `SOURCE.write_bytes()`; both files
restored via `git checkout --`, rebuilt clean, Sentient digest byte-identical").
**Warning signs:** No recorded failure output in the plan's verification evidence.

### Pitfall 3: Adding a guard to Dumb but not Sentient

**What goes wrong:** The Aware fork ships unguarded.
**Why it happens:** `build_sentient.py` has *two* touch points — an import list
(`:13-32`) and a separate invocation block — and both are easy to miss.
**How to avoid:** Phase 12 hit this exact trap and documented it ("build_sentient.py imported
13 symbols and ran 13 guards, and none of these four was among them"). Add to both.
**Warning signs:** `grep -c verify_ tools/build_sentient.py` unchanged after the edit.

### Pitfall 4: Assuming the ROADMAP's counts

**What goes wrong:** A plan sized for "14 + 2 sites" against a reality of "0 + 66 actions /
660 rows".
**Why it happens:** The ROADMAP, CONTEXT.md and the pending todo all repeat unverified figures.
**How to avoid:** Use this document's measured table; re-measure after the fix.
**Warning signs:** Any task text containing "14 sites" or "2 List sites".

### Pitfall 5: Treating gate B's single waived line as a regression

**What goes wrong:** The build is declared broken because gate B exits 1.
**Why it happens:** Gate B's waiver is permanent by design.
**How to avoid:** Expect **exactly one** `Unknown AppIntent parameter key … WFCreateNoteInput`
line per fork — measured this session: 1 for Dumb, 1 for Sentient. Anything else is real.

### Pitfall 6: Byte-idempotency drift

**What goes wrong:** A second build produces a different digest, breaking
`docs/phase6_self_check.py`.
**Why it happens:** Non-deterministic ordering in the new wrapper construction.
**How to avoid:** Build twice; the second run must be byte-identical. `uid()` is a seeded
`uuid5` counter, so determinism holds as long as no new `uid()` call is introduced — the
Pattern 1 fix adds none.

## Code Examples

### Measuring the defect (re-usable as the guard's core)

```python
# Source: this session's measurement script; shapes from Donor 4 / 4.1
import plistlib
d = plistlib.load(open("src/PROSOCHE-Dumb.xml", "rb"))
bad = []
for i, a in enumerate(d["WFWorkflowActions"]):
    if a["WFWorkflowActionIdentifier"] != "is.workflow.actions.list":
        continue
    for j, row in enumerate(a["WFWorkflowActionParameters"].get("WFItems", [])):
        if isinstance(row, dict) and "WFItemType" not in row:
            bad.append((i, j))
print(len(bad))   # HEAD: 660
```

### The guard, in the established project shape

```python
# Follows verify_conditional_action_string() (tools/build_state_engine.py:2413):
# module-level def, iterate emitted actions, collect offenders, raise SystemExit
# with a truncated list and a total count.  SystemExit, never assert.
def verify_list_item_wrappers(actions):
    """Fail the build if a variable-bearing List row omits the iOS row wrapper.

    Donor 4 and Donor 4.1 (device-authored, decrypted Phase 13) both serialize a
    variable-bearing row as {"WFItemType": 0, "WFValue": <WFTextTokenString>} and a
    literal row as a bare string.  A raw WFTextTokenString placed directly in WFItems
    validates, signs and imports, then renders as an EMPTY row on device -- so the
    Mirror can select a blank template, violating CIRC-07.  Invisible to the validator
    and to the ToolKit catalog, which has no entry for WFItems row shape at all.
    """
    offenders = []
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.list":
            continue
        for position, row in enumerate(item.get("WFWorkflowActionParameters", {})
                                           .get("WFItems", [])):
            if isinstance(row, dict) and "WFItemType" not in row:
                offenders.append((index, position))
    if offenders:
        raise SystemExit("List rows carry a raw WFTextTokenString instead of the iOS "
                         "{WFItemType, WFValue} wrapper (renders blank on device): "
                         + ", ".join(f"action {i} row {p}" for i, p in offenders[:5])
                         + f" ({len(offenders)} total)")
```

### Pinning the Donor-5-confirmed conditional shape

```python
# Extends verify_conditional_action_string()'s existing loop.  Positive assertion:
# a variable-bearing comparison target MUST remain a WFTextTokenString.
value = parameters["WFConditionalActionString"]
if isinstance(value, dict):
    if value.get("WFSerializationType") != "WFTextTokenString" \
       or "￼" not in value.get("Value", {}).get("string", "") \
       or not value.get("Value", {}).get("attachmentsByRange"):
        offenders.append(index)   # Donor 5 shape lost
```

## State of the Art

| Old belief | Corrected understanding | When | Impact |
|---|---|---|---|
| "14 `WFConditionalActionString` sites are defective" | 0 are defective; 20/fork are variable-bearing and all match Donor 5 | This research | Removes the phase's larger half |
| "`WFItems` wrapper: 2 confirmed instances" | 66 actions / 660 rows per fork | This research | Expands the remaining half 33× |
| "`if_block("Previous Respected", 4, …)` is one of the 14" | It passes a raw literal; not a member of the family | This research | The named "concrete starting site" was a false lead |
| "The screenshot shows both defects" | The file does not exist in the repo | This research | No task may depend on it |
| Display names `Dumb` / `Sentient` | `Core` / `Aware` since Phase 11 | Phase 11 | CONTEXT.md's signing constraint is stale |
| `is.workflow.actions.conditional` has zero device coverage | Donors 4, 4.1 and 5 now cover conditions 2, 4 and 100 | This research | The catalog gap is closed by donor evidence |

**Deprecated/outdated:** `HANDOFF.md:239` ("`Donor 5` … still not analysed") and
`HANDOFF.md:155` (axis 6 "20 Dumb, 25 Sentient") are both superseded. The pending todo
`.planning/todos/pending/2026-08-15-fix-red-operator-and-list-wrapper-defects.md` should be
closed with the refutation recorded, not silently deleted.

## Validation Architecture

### Test Framework

| Property | Value |
|---|---|
| Framework | None conventional — this project uses **executable structural checkers** (`docs/*.py`) plus **in-generator guards** (`verify_*`) |
| Config file | none — each checker is a standalone script exiting 0/1 |
| Quick run command | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py` (runs 21 + 17 guards inline) |
| Full suite command | build + all 12 `docs/*.py` checkers + gate A on both forks |

### Phase Requirements → Test Map

| Req ID | Behavior | Test type | Automated command | Exists? |
|---|---|---|---|---|
| CIRC-07 | No List row renders blank | structural guard | `python3 tools/build_state_engine.py` (new `verify_list_item_wrappers`) | ❌ Wave 0 |
| CIRC-07 | Mirror dispatch intact | checker | `python3 docs/sequence_dispatch_check.py` | ✅ |
| CIRC-04 | Confession flow unregressed | checker | `python3 docs/phase5_self_check.py` | ✅ |
| ROOM-03 | Note identity/Automation B text unregressed | checker | `python3 docs/note_identity_check.py` | ✅ |
| DIST-01 | Gate A clean, both forks | validator | `validate-shortcut src/PROSOCHE-{Dumb,Sentient}.xml --target-macos 26 --target-platform all` | ✅ |
| DIST-02 | Signed artifacts + canonical basenames | checker | `python3 docs/manifest_check.py` | ✅ |
| — | Byte-idempotent rebuild | checker | `python3 docs/phase6_self_check.py` | ✅ |
| — | Donor-5 conditional shape preserved | structural guard | extend `verify_conditional_action_string` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `python3 tools/build_state_engine.py && python3 tools/build_sentient.py`
- **Per wave merge:** full 12-checker sweep + gate A on both forks
- **Phase gate:** full suite green, gate B showing exactly one waived line per fork, signed
  artifacts re-generated and MANIFEST refreshed, before `/gsd-verify-work`

### Measured Baseline (this session, HEAD, all green)

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebbf… HEAD` | exit 0 — provenance OK |
| 12 × `docs/*.py` | **all PASS** |
| Gate A, Dumb | `Validation passed.` |
| Gate A, Sentient | `Validation passed.` |
| Gate B, Dumb | exactly 1 waived line |
| Gate B, Sentient | exactly 1 waived line |
| Wrapped-row prototype (660 rows), gate A | `Validation passed.` |

Everything is green *before* the phase starts, so any red during execution is caused by the
phase. [VERIFIED: commands run this session]

### Wave 0 Gaps

- [ ] `verify_list_item_wrappers()` in `tools/build_state_engine.py` — covers CIRC-07
- [ ] Register it in the guard harness at `:4160-4177`
- [ ] Add it to `tools/build_sentient.py`'s import list **and** its guard block
- [ ] Extend `verify_conditional_action_string()` with the positive Donor-5 assertion
- [ ] Sensitivity demonstration for both guards against a synthetically reverted artifact

*No new test framework is needed — the project's guard/checker mechanism covers everything.*

## Security Domain

`security_enforcement` is enabled (`security_asvs_level: 1`). This phase changes plist
serialization inside a locally-generated, on-device Shortcut with no network surface.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard control |
|---|---|---|
| V2 Authentication | no | No accounts, no auth surface |
| V3 Session Management | no | "Session" here is a behavioural app-usage session, not a security session |
| V4 Access Control | no | Single-user, on-device, explicitly bypassable by design |
| V5 Input Validation | **yes** | The Mirror templates are generator-authored constants, never user input; `WFItems` rows carry only `text_token()` output built from a fixed template list. No untrusted data enters the wrapper. |
| V6 Cryptography | no (consumed only) | AEA1 decryption uses Apple's `aea`/`aa`; no crypto is implemented here |
| V7 Error Handling / Logging | **yes** | Guards must raise `SystemExit` with an actionable message before any write — the project's existing convention |
| V12 Files & Resources | **yes** | Single atomic `SOURCE.write_bytes()`; `build_sentient.py` writes via `tempfile` + `os.replace` |

### Known Threat Patterns

| Pattern | STRIDE | Standard mitigation |
|---|---|---|
| Signed artifact ships under a wrong filename → silently dead install | Denial of service | `sign-shortcut --name` with the exact canonical display name + `docs/manifest_check.py` DIST-04 assertion (carried from Phase 11 threat T-11-29) |
| Rebuild from a stale/forked ref reintroduces closed defects | Tampering | `git merge-base --is-ancestor 7ca8ebbf… HEAD` precondition |
| A guard that cannot fail creates false assurance | Repudiation | Mandatory sensitivity demonstration against a reverted artifact |
| Blank Mirror row leaks nothing but breaks the intervention | (safety, not security) | `verify_list_item_wrappers()` |

**No new attack surface.** No network, no secrets, no user-supplied data, no new dependency.
DIST-08 (no external network dependency) is unaffected.

## Environment Availability

| Dependency | Required by | Available | Version | Fallback |
|---|---|---|---|---|
| Python 3 | generator, guards, checkers | ✓ | ≥3.10 | — |
| `validate-shortcut` | DIST-01, gates A/B | ✓ | Playground 1.2.1 | — |
| `sign-shortcut` | DIST-02 | ✓ | Playground 1.2.1 | — |
| `aea` / `aa` | donor decryption | ✓ | macOS built-in | **already used — all 3 donors decrypted** |
| `openssl` | donor pubkey extraction | ✓ | system | — |
| `git` | provenance ancestor check | ✓ | ancestor check passes | — |
| Donors 4, 4.1, 5 | evidence | ✓ | on disk + decrypted | — |
| `Screenshot 2026-08-14…png` | (was) evidence | **✗** | absent from repo and git history | **Not needed** — both defects settled independently |
| Real iPhone | device confirmation of the fix | ✗ (not live) | — | Deferred to Phase 19 UAT; file-level + donor evidence is sufficient to ship the fix |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** the screenshot (superseded by direct measurement); the
device (Phase 19 owns UAT, and `DIST-03` is already the project's one open Pending requirement).

## Assumptions Log

| # | Claim | Section | Risk if wrong |
|---|---|---|---|
| A1 | The 2026-08-14 red render at `Previous Respected` was caused by a *then-current* binding since changed by cycles 14–16 / Phases 9–12 | Site inventory | Low — a red operator would still be caught at Phase 19 UAT. The site is provably valid at HEAD on every axis file-level analysis can reach, so no action is available now regardless. |
| A2 | `WFItemType` values other than `0` exist for non-text rows | Donor 4/4.1 findings | None for this phase — only text rows are emitted. Do not encode a guess about other values in the guard or the docs. |
| A3 | Bare-string rows remain valid when mixed with wrapped rows in the same array | Pattern 1 | Low — Donor 4/4.1 show exactly this mix in one device-authored array. This is close to VERIFIED; listed here only because our fix produces arrays that are *all* wrapped, a configuration no donor shows. |
| A4 | Wrapping rows does not change Mirror selection semantics (`getitemfromlist` "Item At Index" over the List output) | Architecture | Medium — if iOS treats a wrapped row differently on extraction, the Mirror text could change shape. Phase 19 UAT must specifically exercise a Mirror. Note `WFItemSpecifier`/`WFItemIndex` are untouched. |

## Open Questions (RESOLVED)

All three are dispositioned below and carried forward as named flagged assumptions (A1–A4) with
owners in `13-01`/`13-04` `must_haves`, `13-UAT.md`, and Phase 19. None is silently dropped.

1. **Does wrapping change what `getitemfromlist` returns?**
   **RESOLVED: proceed now, confirm on device in Phase 19 UAT.**
   - What we know: Donor 4/4.1 show iOS itself producing wrapped rows, so a wrapped List is
     the native shape; `mirror_text()`'s `getitemfromlist` reads `Item At Index` off the List
     output.
   - What's unclear: no donor chains a *wrapped* List into `getitemfromlist`.
   - Recommendation: proceed — the native shape cannot be less correct than the non-native
     one — and add "Mirror renders non-empty text" as an explicit Phase 19 UAT assertion.

2. **What actually caused the 2026-08-14 red operator?**
   **RESOLVED: closed by refutation — no phase budget spent; Phase 19 UAT observes the live artifact.**
   - What we know: not reproducible at HEAD; the site uses a raw literal with a Text left
     operand and condition 4, which is a valid pairing; no dangling variable reference.
   - What's unclear: whether it was a since-fixed binding, a different site, or a stale
     imported build in the editor.
   - Recommendation: do **not** spend phase budget here. Record it as closed-by-refutation
     and let Phase 19 UAT observe the actual current artifact on device. If a red chip
     appears there, it will be a *new* finding with a live artifact to inspect — which is
     precisely the outcome the phase goal ("a blank Circle in testing is a real finding
     rather than a known artifact") is asking for.

3. **Should the 172/175 raw-literal `WFConditionalActionString` values be `WFTextTokenString`?**
   **RESOLVED: left unaudited by decision — device-proven working, out of scope, evidence named.**
   - What we know: Donor 5 covers only the *variable-bearing* case. No donor shows a pure
     literal comparison target.
   - What's unclear: whether iOS writes a literal as a bare string or as a
     `WFTextTokenString` with no attachments.
   - Recommendation: **leave them alone.** They are device-proven working — the OPEN/CLOSE
     router tests `Input Key` against raw `"OPEN"`/`"CLOSE"` literals and `HANDOFF.md:126`
     records every breadcrumb A–J firing on device. Changing a device-proven-working
     construct on speculation is exactly what the do-not-fabricate rule forbids. If it is
     ever worth settling, the evidence is a one-action donor with a literal comparison —
     a rung-4 request, not a rung-1 inference.

## Project Constraints (from CLAUDE.md)

Directives the planner must honour, extracted from `.claude/CLAUDE.md`:

| Directive | Where | Binding on this phase |
|---|---|---|
| Two-gate validator rule; gate A mandatory clean, gate B advisory and never `&&`-chained | §1 | Every verification block |
| Never fabricate an action identifier or parameter shape; use safest fallback + record deviation | § Capability, § What NOT to use | Open Question 3 — leave literals alone |
| Evidence hierarchy: device donor > simulator > golden corpus > `.intentdefinition` > ToolKit catalog > inference | § Conventions | Donor 5 outranks the ROADMAP's assertion |
| Evidence-escalation ladder: never climb higher than the question requires, never skip a rung | §9 | Rung 1 settled both families; do not request a device session for these |
| The seven parameter-defect axes | § Conventions | Fold in the newly confirmed axes; note the List wrapper is a **new axis**, not an instance of axis 2 |
| Fix whole classes, never site-by-site | § Debugging technique | One `mirror_text()` change, not 66 edits |
| Signed filename must equal the display name, no `_signed` suffix | §8 | Use `Core` / `Aware` |
| Definition of done includes signing | §1 | XML alone is not a stopping point |
| Build provenance ancestor check before any rebuild | § Constraints | Precondition on every build task |
| Guards use `SystemExit`, never `assert`, and run before the single write | (observed in all 21 guards) | New guard must match |
| `/ponytail` laziness never licenses skipping the defect axes | §9 | The minimal fix is genuinely one line — but the guard and docs are not optional |

## Documentation Updates Required (the single-pass deliverable)

The phase requires three doc updates in one pass. All three targets are located:

| # | Update | Target | Source material |
|---|---|---|---|
| 1 | **New axis — List row wrapper** | `.claude/CLAUDE.md:353-391`, the numbered list (currently "the seven parameter-defect axes"; becomes eight) | Donor 4/4.1 shape above; note it is a *container* defect, distinct from axis 2's string-envelope defect, and that literal rows stay bare |
| 2 | **`read_value()` / `get_value()` distinction** | Same numbered list or the adjacent runtime-semantics section | Already fully written as a docstring at `tools/build_state_engine.py:248-296` — the rule is: `get_value()` for COMPOUND values consumed as a List (`recent_sessions`, `exit_events`, `exit_stats.<n>.samples`, `profile_snapshot.enabled_exits`); `read_value()` for SCALARS in text/numeric comparisons. Guarded by `verify_compound_value_reads()` |
| 3 | **`pending_exit` container/leaf pattern** | Same list / § Conventions axis 7 | `seed_pending_exit()` at `:2686`, `clear_snapshot()`'s docstring at `:458`, and the CYCLE-12 block at `:196-228`. Rule: seed the container as a permanent invariant; write and clear only LEAVES; gate on a string "is not sentinel" (code 5) or numeric `> 0`, never a condition-100 existence test over the container |
| 4 | **The Donor 5 refutation** (recommended addition) | `docs/CAPABILITY-DECISIONS.md` + close the pending todo | This document's Donor 5 section — prevents re-litigation |

Also update `docs/BUILD-NOTES.md` with the decrypt results, per the §9 "recording duty"
("A probe's result is recorded, not consumed").

## Sources

### Primary (HIGH confidence — device ground truth, rung 1 analysis of rung 3/4 artifacts)

- `.planning/debug/Donor 5.shortcut` — decrypted this session; settles the conditional
  TEXT-slot operand envelope
- `.planning/debug/Donor 4.shortcut`, `.planning/debug/Donor 4.1.shortcut` — decrypted this
  session; settle the `WFItems` row wrapper, the bare-string row case, and the numeric-RHS slot
- `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` at HEAD — `plistlib` walks producing
  every count in this document
- `tools/build_state_engine.py` (4193 lines), `tools/build_sentient.py` (370 lines) — read
  directly for helper shapes, guard harness, and fork mechanics
- Command runs this session: provenance check, 12 checkers, gates A and B, wrapped-row
  prototype validation

### Secondary (MEDIUM confidence — project records, some superseded)

- `.claude/CLAUDE.md` — two-gate rule, evidence hierarchy, ladder, seven axes, §8 recipe
- `artifacts/shortcuts/MANIFEST.md` — canonical display names `Core` / `Aware`
- `.planning/phases/12-*/` plan and verification blocks — the guard sensitivity pattern and
  the canonical automated verification command
- `docs/BUILD-NOTES.md`, `docs/CAPABILITY-DECISIONS.md` — update targets

### Superseded by this research

- `.planning/todos/pending/2026-08-15-fix-red-operator-and-list-wrapper-defects.md` — "14
  sites", "2 instances", and the `Previous Respected` attribution are all refuted
- `.planning/debug/HANDOFF.md:155, :239` — axis-6 counts and "Donor 5 not analysed"
- `.planning/debug/Screenshot 2026-08-14 at 11.55.12 pm.png` — file does not exist

### Not used

No external/web sources were consulted. All search providers are disabled in
`.planning/config.json` (`brave_search`, `exa_search`, `firecrawl`, `tavily_search`,
`ref_search`, `perplexity`, `jina` all `false`), and every question this phase raises is
answerable from local donor and artifact evidence — which this project's evidence hierarchy
ranks above any external source anyway.

## Metadata

**Confidence breakdown:**

- Conditional operand shape (family 1): **HIGH** — device-authored donor, decrypted, quoted
  verbatim, cross-checked against the generator helper key-for-key
- List wrapper shape (family 2): **HIGH** — two independent device-authored donors agreeing
  byte-for-byte on the same action
- Site counts: **HIGH** — direct `plistlib` measurement of both shipped artifacts at HEAD, not
  inference from source
- Fix feasibility: **HIGH** — prototype built and passed gate A on the real artifact
- Guard pattern: **HIGH** — 21 existing guards read; Phase 12's sensitivity demonstration
  quoted
- Cause of the 2026-08-14 red render: **LOW** — not reproducible; screenshot absent; recorded
  as an open question, not a finding
- `WFItemType` values beyond `0`: **LOW** — deliberately unaudited, flagged, not guessed

**Research date:** 2026-08-17
**Valid until:** stable — donor evidence does not expire; re-measure the site counts after any
generator change, since they are the only figures here that drift
