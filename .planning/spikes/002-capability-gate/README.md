---
spike: 002
name: capability-gate
type: standard
validates: "Given a single merged shortcut with a manual opt-in toggle, when the core deterministic escalation runs before the optional Sentient (Use Model) step, then a Use Model failure on ineligible hardware never prevents the core intervention from firing"
verdict: PENDING
related: ["001"]
tags: [shortcuts, device-detection, state-machine]
---

# Spike 002: Capability Gate (toggle-only, ordering-based fail-safe)

## What This Validates

Spike 001 proved there is no way to automatically detect Apple-Intelligence-capable
hardware, and no try/catch mechanism to recover from a `Use Model` failure. This spike
tests the only remaining path to "one shortcut instead of two forks": a manual opt-in
toggle, asked once at import (`WFWorkflowImportQuestions`), combined with an **ordering
discipline** rather than detection — the deterministic core logic always runs before the
optional Sentient step, so a `Use Model` halt on ineligible hardware never breaks the
core loop.

**Explicitly not being tested:** automatic fallback to "Dumb wording" mid-run after a
`Use Model` failure. That's impossible per spike 001 (no catch branch exists). What's
being tested is that the failure, if it happens, is contained to the bonus step and never
threatens the core "OPEN → Heat/Gravity/Pressure → Circle → intervention" loop the
project's CLAUDE.md calls non-negotiable.

## Research

No new external research needed — this is applying spike 001's findings, not exploring
new API surface. Reused: `WFWorkflowImportQuestions` schema (project CLAUDE.md §7, golden
XML evidence), `is.workflow.actions.askllm` parameter schema (CLAUDE.md capability audit
item #15), state.json read/write pattern (CLAUDE.md §3 item 2, Get File/Save File).

## How to Run

Import the signed shortcut. Import-time prompt: "Do you have an iPhone 15 Pro or later
and want to enable Sentient mode (on-device AI mirror)? Type yes or no." Then run the
shortcut manually to observe the branch.

## What to Expect

- Answer "no" (or leave default) → core escalation stub runs, no `Use Model` attempted,
  `sentient_enabled: false` cached in state.json.
- Answer "yes" on eligible hardware → core escalation stub runs, then `Use Model` runs
  and appends mirror text, `sentient_enabled: true` cached.
- Answer "yes" on ineligible hardware (untestable on the developer's own device — see
  Investigation Trail) → core escalation stub should still have completed before the
  `Use Model` halt/error.

## Investigation Trail

### What was built

`PROSOCHĒ Capability Gate.shortcut` — 35 actions, 9 of them Comments. Built, validated,
signed, and the signed artifact decrypted and re-inspected to confirm what actually
shipped (35 actions, import question intact, ordering intact).

Action sequence, with the load-bearing ordering in bold:

| # | Action | Role |
|---|---|---|
| 0–2 | Comment ×3 | Description, required Playground notice, core-escalation section header |
| **3** | **Show Alert** | **CORE ESCALATION — unconditional, first executable action, no condition above it** |
| 4 | Comment | Opt-in section header |
| 5 | Text `"no"` | **Import-question target** (`ActionIndex: 5`) |
| 6 | Set Variable `Sentient Answer` | Consumes the raw answer |
| 7 | Comment | Wiring bullets before the If |
| 8–14 | If / Otherwise / End If | Normalize answer → `sentient_enabled` = text `"true"`/`"false"` |
| 15 | Comment | Read-state section header |
| 16 | Get File | `PROSOCHE-state.json`, `WFFileErrorIfNotFound = false` |
| 17 | Get Dictionary from Input | Parses file text; yields nothing if absent |
| 18 | Comment | Wiring bullets before the If |
| 19–25 | If / Otherwise / End If | `State Status` = `existing` or `bootstrapped` |
| 26 | Comment | Write-state section header |
| 27 | Text (JSON body) | Interpolates `sentient_enabled` + `State Status` |
| 28 | Set Name | `PROSOCHE-state.json` |
| 29 | Save File | `WFAskWhereToSave = false`, `WFSaveFileOverwrite = true` |
| 30 | Comment | Sentient section header + explicit no-recovery note |
| 31 | If `sentient_enabled` is `"true"` | Gate |
| **32** | **Use Model** | **LAST substantive action — nothing but Show Result and End If follow** |
| 33–34 | Show Result, End If | Display mirror text; close block |

Decrypted-artifact check: core Show Alert at index 3, Use Model at index 32, and the only
things after Use Model are its own Show Result and the End If. The fail-safe ordering
holds in the shipped bytes, not just the source.

### Wiring decisions

**Core step placed before the toggle is even read.** The task allowed the core step merely
to precede *Sentient-branch* logic. It was placed ahead of everything — before the toggle
read, before both Ifs, before the state I/O — so no downstream failure of any kind
(including a state-file error, not just a Use Model error) can pre-empt it. This is the
strictest available reading of the ordering fail-safe and makes the spike a stronger test.

**No dictionary key is ever read.** The state-present check gates on whether the
**Get Dictionary from Input** output itself has any value (condition code `100`), not on
reading a key out of it. This deliberately sidesteps the trap recorded in the project's
`CLAUDE.md`: a dotted read hard-errors when any segment is missing, so a
read-then-`has any value` gate on a dotted path is unimplementable. It also respects the
documented operator/operand rule that an uncoerced Dictionary Value supports *only*
`has any value` / `does not have any value` — code `100` is exactly that operator, so no
coercion aggrandizement is needed and no red-in-UI operator mismatch is possible.

**`WFFileErrorIfNotFound = false` is the real answer to the missing file-exists check.**
The project's `CLAUDE.md` §3 item 2 records "no native file-existence check" and proposes
attempting Get File and treating the result as absent. The golden corpus supplies the
missing mechanism: this boolean makes a missing file return nothing instead of halting the
run. Recommend amending `CLAUDE.md` §3 item 2 — the fallback is cleaner than documented.

**Boolean is written unquoted.** The JSON template places the `sentient_enabled`
placeholder *outside* the quotes (`"sentient_enabled": ￼,`) so the file receives a real
JSON boolean `true`/`false`, while `state_status` is quoted as a string. The Shortcuts
variable itself holds the text `"true"`/`"false"`, compared with string condition code `4`.

**Flat path, ASCII filename.** State lives at `PROSOCHE-state.json` in the Shortcuts iCloud
folder root — no subfolder, because `WFFileDestinationPath` folder-creation semantics are
unverified, and ASCII `PROSOCHE` rather than `PROSOCHĒ` to keep the macron out of a
filename round-trip. The shortcut's display name keeps the `Ē`.

**Import question is a text prefill, as documented.** Confirmed against 4 golden shortcuts:
`{ActionIndex, Category: "Parameter", DefaultValue, ParameterKey, Text}`. `ActionIndex` is
**0-based** into `WFWorkflowActions` — verified by checking that the targeted index in
`afa83b6be811483b9c32189c41eb9312.xml` is indeed its Text action. There is no native
yes/no control at import time; the answer arrives as free text and must be normalized in
the shortcut, which is why step 2 exists at all.

### Confirmed vs guessed parameter keys

Confirmed from the golden corpus (real shipped shortcuts) or bundled docs:

- `documentpicker.open` → `WFGetFilePath`, `WFShowFilePicker`, `WFFileErrorIfNotFound`
- `documentpicker.save` → `WFAskWhereToSave`, `WFSaveFileOverwrite`
- `setitemname` → `WFName`
- `detect.dictionary` → `WFInput` as `WFTextTokenAttachment`
- `askllm` → `WFLLMPrompt` (`WFTextTokenString`), `WFGenerativeResultType = "Text"`
- Condition codes `4` (string is) and `100` (has any value) plus the uniform
  `WFInput` `Type = Variable` wrapper
- `WFWorkflowImportQuestions` entry shape and 0-based `ActionIndex`

All of the above come from `golden-shortcuts/xml/332c12a0060043b388b22b806be7ab58.xml`
(a clipboard manager that performs the exact Get File → modify → Set Name → Save File
round trip at the Shortcuts folder root), the four import-question-bearing golden
shortcuts, `EXAMPLES.md`, and `BEST_PRACTICES.md`.

Guessed / deviating — **flag these for the on-device run**:

1. **Explicit `WFInput` on Set Name and Save File.** The golden corpus omits `WFInput`
   entirely on both and relies on implicit input chaining. `BEST_PRACTICES.md` §Files
   instead mandates providing it explicitly. Policy was followed over corpus. Both forms
   validate; only a device run shows whether the explicit form renders a connected input
   chip or an empty one.
2. **`WFAlertActionCancelButtonShown = false`.** Standard key, but not present in the
   corpus samples pulled for this build. Intent is that the user cannot cancel out of the
   core escalation.
3. **`WFLLMModel` omitted entirely**, per the task. The on-device model-source enum
   literal remains unverified (project `CLAUDE.md` capability audit item #15) and is
   deliberately out of scope here. Use Model will run on whatever the default source is —
   which means this shortcut does **not** yet prove on-device pinning, only that the
   action is reached and gated correctly.
4. **`documentpicker.save` writes to the Shortcuts folder root** by relying on Set Name
   plus an omitted `WFFileDestinationPath`. Proven in the corpus for `Clipboard.txt`;
   assumed to generalize.

### Validator results

Both invocations required by spike 001's toolchain correction pass with exit code 0:

```
validate-shortcut "PROSOCHĒ Capability Gate.xml" --target-macos 26                        # Validation passed.
validate-shortcut "PROSOCHĒ Capability Gate.xml" --target-macos 27 --target-platform ios  # Validation passed.
```

Spike 001's finding is re-confirmed as still applying: the combination
`--target-macos 26 --target-platform ios` from the project's `CLAUDE.md` was **not** used,
because it yields an empty allowlist and rejects everything.

One Craig Loop iteration was needed. The only error was an `attachmentsByRange` offset:
the Show Result placeholder was written at `{16, 1}` but `"Sentient mirror: "` puts the
object-replacement character at index 17. Fixed by a one-character edit; the JSON template
offsets at indices 24 and 46 were correct on the first pass.

### Artifacts

- Unsigned XML: `drafts/PROSOCHĒ Capability Gate.xml`
- Timestamped archive: `2026-08-16/PROSOCHĒ Capability Gate-210722.xml`
- Signed: `PROSOCHĒ Capability Gate.shortcut` (26,065 bytes, `AEA1` magic, mode `anyone`)

## Results

_Pending build and verification._

Build is complete and signed; **the on-device run has not happened yet** and no verdict is
claimed here. A human needs to import the signed shortcut on a real iPhone and confirm:

1. The import prompt actually appears and its answer lands in the Text action (answer
   "yes" once and "no" once).
2. Answering "no" → core alert fires, no Use Model attempt, `state.json` contains
   `"sentient_enabled": false`.
3. Answering "yes" on eligible hardware → core alert fires *first*, then the mirror text
   appears, `"sentient_enabled": true`.
4. The ordering fail-safe under real failure — ideally on ineligible hardware, where the
   core alert should still have completed before the Use Model halt. Not testable on the
   developer's own device if it is Apple-Intelligence-capable; a proxy is to force a Use
   Model failure some other way and confirm the alert and the state write both survived.
5. Whether the explicit `WFInput` on Set Name / Save File (deviation 1 above) shows a
   connected input in the editor or an empty field.
