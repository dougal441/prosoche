# Walking Skeleton — Phase 2: Routing, Bootstrap & Control Room Onboarding

**Created:** 2026-08-13 (planning)
**Owning phase:** 02-routing-bootstrap-control-room
**Artifact under construction:** `src/PROSOCHE-Dumb.xml`

This is the Phase-1-of-a-new-artifact special case of the tracer. `src/PROSOCHE-Dumb.xml`
does not exist yet; this phase creates it, and Phases 3–7 grow it in place before Phase 8
forks it to `src/PROSOCHE-Sentient.xml`. Every architectural decision recorded here is
inherited by all of those phases. Later phases extend this skeleton; they do not
re-litigate it.

---

## 1. The thinnest end-to-end path (what plan 02-01 proves)

```
import questions  →  router  →  bootstrap gate  →  state.json  →  Control Room Note  →  show it
```

Concretely, one manual tap of a freshly imported Shortcut, on a device with no prior
PROSOCHĒ state, must:

1. carry the two import-question answers (descent profile, voice permission) into the run;
2. parse the static Config block once;
3. materialise the run clock (integer epoch seconds, behavioural day key);
4. classify Shortcut Input as absent → take the MANUAL branch;
5. attempt to read `state.json`, find nothing, and take the bootstrap branch;
6. write a schema-valid, bounded, versioned `state.json`;
7. create exactly one Note titled `PROSOCHĒ — Control Room` with a **non-empty** body;
8. open that Note in front of the user.

Every layer this phase will ever touch is exercised once, on one path, in that single
slice. Plans 02-02 through 02-04 expand horizontally from it — they add Note content,
the OPEN/CLOSE/fail-safe branches, and the self-healing/idempotence guards — but they do
not change its shape.

---

## 2. Architectural decisions this skeleton records

| # | Decision | Source |
|---|----------|--------|
| S-01 | **One monolithic action graph per fork.** No internal `Run Shortcut` hops. The only `Run Shortcut` call in the product is the mandatory one from each Personal Automation into this Shortcut. | D-14; ARCHITECTURE.md §1 |
| S-02 | **Nested `If`/`Otherwise` only.** `Otherwise If` (mode 1 carrying condition fields) is macOS-27+ and is never emitted. Every nesting level gets its own freshly generated `GroupingIdentifier`. | D-15, D-23; CONTROL_FLOW.md |
| S-03 | **Three invocation modes off Shortcut Input**: absent/empty → MANUAL, `OPEN`, `CLOSE`. Anything else is inert by construction — the fail-safe branch performs zero state mutation. | D-16; ARCHITECTURE.md §1 |
| S-04 | **Shortcut Input is referenced via an `ExtensionInput` token attachment.** `is.workflow.actions.input` is never emitted. | BEST_PRACTICES.md lines 88, 95 |
| S-05 | **All timestamps are integer Unix epoch seconds (UTC)**, built once per run from a fixed `1970-01-01 00:00:00` Date anchor through `Get Time Between Dates` (unit: seconds). `behavioural_day` is the single exception: an ISO `yyyy-MM-dd` string key. | D-17; ARCHITECTURE.md §2 |
| S-06 | **One JSON state file, one Apple Note.** `state.json` is the machine store; the Note is the human store. No CSV, no second machine store. | D-18; ARCHITECTURE.md §10 |
| S-07 | **State is bounded and versioned.** `schema_version: 1`; rolling windows (`recent_sessions` cap 20, `recent_contracts` cap 10, per-exit `samples` cap 20); no unbounded arrays. | D-19; STATE-12 |
| S-08 | **There is no file-existence-check action.** Bootstrap branches off `Get File` with `WFFileErrorIfNotFound` off, piped through `Detect Dictionary`; a non-dictionary/empty result means "state absent." | DEV-02 in `docs/BUILD-NOTES.md` §5 |
| S-09 | **`state.json` is written from a `Text` action holding a JSON template**, not from a Dictionary→JSON action — no such action is evidenced anywhere in the bundle. | CAP-04 Fallback cell |
| S-10 | **The Control Room Note is created with `com.apple.Notes.CreateNoteFromMarkdownLinkAction` and the camelCase key `markdownContents`.** The key `markdown` passes the validator and produces an empty body at runtime. | D-21; CAP-08; PITFALLS A8 |
| S-11 | **Display-facing text uses `WFTextTokenString`** with `￼` placeholders and `attachmentsByRange`, even for a single bare variable. Data-flow parameters use `WFTextTokenAttachment`. | D-22; PITFALLS A2; VARIABLES.md |
| S-12 | **Dictionary values destined for an `If` comparison are routed through a `Text` action first.** JSON booleans read back as numeric `1`/`0`; JSON `null` reads back as empty; a nested read on a null parent breaks. | D-24; PITFALLS A4; CONFIG-BLOCK.md coercion hazards |
| S-13 | **The Config block is transcribed verbatim into one `Text` action** and parsed once per run by `Detect Dictionary` into the `Config` variable. No tunable number is ever inlined where a `Config` read is available. | `src/CONFIG-BLOCK.md` transcription recipe |
| S-14 | **The two import-question `Text` actions are pinned at `WFWorkflowActions` indices 2 and 4**, immediately after the two mandatory header Comments. `WFWorkflowImportQuestions` binds by `ActionIndex`, the validator does not check it, and every later insertion happens below index 5 so those indices never shift. | STACK.md §7 |
| S-15 | **The fixed data path is `PROSOCHE/state.json`** — ASCII folder name, no macron, so no non-ASCII byte ever enters a filesystem path. The Note *title* keeps its diacritics (`PROSOCHĒ — Control Room`); only the folder is ASCII. | Claude's discretion under D-26 |
| S-16 | **The operative validator invocation for this build is `--target-macos 26 --target-platform all`.** See §4 below — this is a correction to the invocation recorded in `docs/BUILD-NOTES.md` §3, and plan 02-01 must record it as a deviation. | Measured against `scripts/validate_shortcut.py` |

---

## 3. Named shortcut variables introduced by Phase 2

Later phases **must not** reuse these names for anything else. Phase 3 onward adds its own
names; this table is the collision register.

| Variable | Type | Set by | Meaning |
|----------|------|--------|---------|
| `Import Descent` | text | 02-01 | Raw descent-profile answer from import question 1 (`Paradise`/`Limbo`/`Inferno`, default `Limbo`) |
| `Import Voice` | text | 02-01 | Raw voice-permission answer from import question 2 (`yes`/`no`, default `yes`) |
| `Config` | dictionary | 02-01 | Parsed static Config block from `src/CONFIG-BLOCK.md` |
| `Epoch Anchor` | date | 02-01 | Fixed `1970-01-01 00:00:00` Date value |
| `Now Date` | date | 02-01 | Materialised current instant (never the `CurrentDate` magic token) |
| `Now Epoch` | number | 02-01 | Integer Unix epoch seconds for this run |
| `Behavioural Day` | text | 02-01 | `yyyy-MM-dd` day key = `Now Date` − 4h |
| `Input Key` | text | 02-01 (declared), 02-03 (normalised) | Classified Shortcut Input: empty, `OPEN`, `CLOSE`, or unrecognised |
| `State File` | file | 02-01 | Raw `Get File` result for `PROSOCHE/state.json` |
| `State` | dictionary | 02-01 | Parsed state document |
| `State Schema Text` | text | 02-01 | `schema_version` routed through `Text` for the validity gate |
| `State Present` | text | 02-04 | `yes`/`no` outcome of the load-validity gate |
| `Default State JSON` | text | 02-01 | The bootstrap `state.json` body |
| `Control Room Body` | text | 02-01 (minimal), 02-02 (full) | The assembled Control Room Note markdown |
| `Control Room Note` | note | 02-01 | Result of `Find Notes` / `Create Note` |
| `Note Present` | text | 02-04 | `yes`/`no` outcome of the Note-existence guard |

---

## 4. Validator invocation — a measured correction

`docs/BUILD-NOTES.md` §3 records the invocation as:

```
validate-shortcut <file.xml> --target-macos 26 --target-platform ios
```

That invocation **cannot pass any shortcut built from long-standing actions.** Measured
against `skills/shortcuts-playground/scripts/validate_shortcut.py`:

- `load_packaged_toolkit_ids` filters snapshots by two independent gates —
  `_toolkit_snapshot_min_macos_major` (v78 and v78-ios27 both require target ≥ 27) and
  `_snapshot_matches_target_platform` (a snapshot whose platform label is `macOS` is
  admitted only when `--target-platform macos`).
- `toolkit-v63-tool-ids.json` carries the `macOS` platform label, so `--target-platform ios`
  excludes it. `toolkit-v78-ios27-tool-ids.json` carries the `iOS` label but is excluded by
  `--target-macos 26`.
- The two flags together therefore admit **no snapshot at all**, leaving only the hardcoded
  control-flow and HealthKit exception sets.

Empirical confirmation, same file, same validator, only the platform flag differing:

| Invocation | `requires macOS 27+` errors |
|---|---|
| `--target-macos 26 --target-platform ios` | 118 |
| `--target-macos 26 --target-platform all` | 0 |
| `--target-macos 26 --target-platform macos` | 0 |

**Operative invocation for every Phase 2 gate:**

```
validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all
```

`--target-macos 26` is still correct and still load-bearing: it is what keeps the OS27
parameter catalog (and its `interpretAsMarkdown`-class OS27-gated keys) out of the
allowlist, which is the actual reason `docs/BUILD-NOTES.md` §3 pinned target 26 in the
first place. Only the platform flag changes. Plan 02-01 records this as `DEV-04` in
`docs/BUILD-NOTES.md` §5 with the evidence above; that document is append-only, so the
original §3 text stays and the deviation entry supersedes it.

---

## 5. Validator rules this skeleton must satisfy from its first commit

These are enforced by `validate_shortcut.py` and are cheap to satisfy at authoring time
and expensive to retrofit:

1. `WFWorkflowActions[0]` is a non-empty `is.workflow.actions.comment`.
2. `WFWorkflowActions[1]` is a `is.workflow.actions.comment` whose `WFCommentActionText`
   contains the literal string `Shortcuts generated by Shortcuts Playground.`
3. A descriptive `Comment` immediately precedes every control-flow start.
4. Comment density scales with action count: ≥ 8 actions → 3 comments, ≥ 16 → 4, ≥ 24 → 5.
5. `WFControlFlowMode` is `<integer>`, never `<string>`.
6. `WFWorkflowIcon` carries a `WFWorkflowIconGlyphNumber` from the official 507-glyph
   mapping and a `WFWorkflowIconStartColor` from the known palette — obtain both from
   `bin/resolve-icon --prompt "..."`, never by hand.
7. Every action output that is referenced later carries a `UUID`; no action output is left
   unused.
8. No parameter is left empty (an empty `WFFileDestinationPath` is a reported error).

---

## 6. What this skeleton deliberately does not decide

- Heat / Gravity / Pressure arithmetic and Circle mapping (Phase 3)
- CLOSE session measurement and the race protocol (Phase 4)
- The nine primitives (Phase 5)
- Exits, exit learning, contracts (Phase 6)
- The manual Control Room menu, the dynamic state snapshot, the Attention Ledger writer,
  and the Mirror templates (Phase 7)
- Signing and on-device import testing (Phase 7 for Dumb, Phase 8 for both forks)
- Anything Sentient or `Use Model` (Phase 8, gated by UA-02)

The OPEN and CLOSE branches this phase creates are real routing destinations with real
`Comment` anchors and no state mutation. Phases 3 and 4 fill them. That is a roadmap
phase boundary, not a reduction of Phase 2's scope.
