---
spike: 004
name: capability-gate
type: standard
validates: "Given a single merged shortcut with a manual opt-in toggle, when the core deterministic escalation runs before the optional Sentient (Use Model) step, then a Use Model failure on ineligible hardware never prevents the core intervention from firing"
verdict: PARTIAL
related: ["003", "008"]
tags: [shortcuts, device-detection, state-machine]
---

> **⚠ VERDICT DOWNGRADED 2026-08-17: VALIDATED → PARTIAL.** The toggle and the ordering
> discipline still hold. The claim that they were *"confirmed on real ineligible hardware"*
> does not — the run never used the configuration Sentient ships, and the failure it
> observed was never identified. See **Reassessment (2026-08-17)** at the end of this file
> before citing anything here.

# Spike 004: Capability Gate (toggle-only, ordering-based fail-safe)

## What This Validates

Spike 003 proved there is no way to automatically detect Apple-Intelligence-capable
hardware, and no try/catch mechanism to recover from a `Use Model` failure. This spike
tests the only remaining path to "one shortcut instead of two forks": a manual opt-in
toggle, asked once at import (`WFWorkflowImportQuestions`), combined with an **ordering
discipline** rather than detection — the deterministic core logic always runs before the
optional Sentient step, so a `Use Model` halt on ineligible hardware never breaks the
core loop.

**Explicitly not being tested:** automatic fallback to "Dumb wording" mid-run after a
`Use Model` failure. That's impossible per spike 003 (no catch branch exists). What's
being tested is that the failure, if it happens, is contained to the bonus step and never
threatens the core "OPEN → Heat/Gravity/Pressure → Circle → intervention" loop the
project's CLAUDE.md calls non-negotiable.

## Research

No new external research needed — this is applying spike 003's findings, not exploring
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

Both invocations required by spike 003's toolchain correction pass with exit code 0:

```
validate-shortcut "PROSOCHĒ Capability Gate.xml" --target-macos 26                        # Validation passed.
validate-shortcut "PROSOCHĒ Capability Gate.xml" --target-macos 27 --target-platform ios  # Validation passed.
```

Spike 003's finding is re-confirmed as still applying: the combination
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

**Verdict: VALIDATED.**

On-device runs (2026-08-16):

**iPhone 15 Pro (Apple-Intelligence-capable):**
- Answered "no" → core escalation alert fired, no Use Model attempt.
- Reinstalled, answered "yes" → core escalation alert fired **first**, then a system
  permission prompt appeared ("Allow to save 1 dictionary to a file" — a one-time Save
  File authorization, not previously documented in the project's file-I/O findings),
  then the Use Model result: *"Sentient mirror: Hello! How can I assist you today?"*
  Toggle → state write → Sentient branch all behaved as designed.

**iPhone SE (not Apple-Intelligence-capable):**
- Answered "yes" → core escalation alert fired (action index 3, first executable step —
  unconditional per the build), then Use Model failed with a native, non-crashing system
  error: *"Could not run 'Use Model' to use this action. Support for selected model is
  downloading."* This is exactly the ordering fail-safe under test: the core intervention
  had already completed before the failure, and the failure itself was a graceful OS-level
  message rather than a corrupt state write or a silent hang.

**What this confirms:** the ordering-based fail-safe works as designed on real ineligible
hardware, not just in theory. The toggle correctly gates the Sentient branch in both
directions, and a Use Model failure — whatever its cause — cannot pre-empt the core
deterministic escalation because nothing about the core step depends on the Sentient
branch succeeding, or even being attempted.

**New finding, not previously in the project's capability audit:** Save File triggers a
one-time OS permission prompt ("Allow to save 1 dictionary to a file") on first write per
installation. Worth noting in the real build's onboarding UX — it's a single tap
("Always Allow"), not a blocker, but it is a user-visible interruption during first run
that the design should anticipate.

**Not fully verified:** whether the iPhone SE error is deterministic/permanent for
ineligible hardware, or a transient "model support downloading" state that could
eventually resolve on that device (the message's wording suggests Apple attempts to
provision model support even on some borderline/ineligible hardware, which the project's
capability audit did not anticipate) — not chased further, since the ordering fail-safe
already answers what this spike set out to prove regardless of which case it is.

---

## Reassessment (2026-08-17) — verdict downgraded to PARTIAL

Prompted by new device evidence from the project owner: **an iPhone 16e, with the Apple
Intelligence models downloaded, ran this same Capability Gate shortcut and returned the
Sentient result successfully.** That datapoint does not contradict anything above — the
16e is Apple-Intelligence-capable (A18, 8 GB) so success is the expected outcome — but it
forces the paragraph above to be taken seriously rather than waved off, and reviewing the
spike in that light surfaced a second, larger problem the original write-up missed.

### Problem 1 — the run never used the configuration Sentient ships

Verified directly from the artifacts:

```
spike 004 draft XML : askllm has WFGenerativeResultType, WFLLMPrompt, UUID — no WFLLMModel
src/PROSOCHE-Sentient.xml : askllm has WFLLMModel = "Apple Intelligence on Device"
```

The spike deliberately omitted `WFLLMModel` (recorded above under "Guessed / deviating"
item 3) because spike 008 had not yet recovered the literal. So **both device runs
exercised whatever the default model source is, not the pinned On-Device path.** The
default is undocumented — MacStories' Use Model write-up explicitly has no information on
which source is selected when none is chosen, and Apple's own Shortcuts documentation does
not say either. If the default resolves to Private Cloud Compute, or auto-selects, then the
SE's failure and the 15 Pro's success are both observations about a code path PROSOCHĒ does
not ship.

The spike's own words — *"this shortcut does not yet prove on-device pinning, only that the
action is reached and gated correctly"* — were correct and should have capped the verdict.

### Problem 2 — the observed failure was never identified, and now probably isn't the one claimed

The SE returned *"Support for selected model is downloading."* That is a **provisioning-state**
message, not an eligibility rejection. The 16e evidence shows the message tracks download
state: models present → success. So the SE observation is equally consistent with

- **(a)** genuinely ineligible hardware, Shortcuts emitting a generic message, or
- **(b)** a device that simply had not finished (or begun) provisioning models.

Nothing in the run distinguishes them, and **which one it was decides whether the finding
generalises at all.** The spike's own record does not even note which iPhone SE generation
was used — that must be recorded before any re-run.

### Problem 3 — the failure class is wider than "ineligible hardware", which changes the merge risk

This is the consequential part. If the message is about provisioning rather than
eligibility, then **capable devices fail too**, in an ordinary and common state:

- Apple Intelligence has been on by default on compatible devices since iOS 18.3, but the
  models are a **~7 GB download** requiring Wi-Fi and power, and are not present on a fresh
  or freshly-reset device.
- The user can also simply turn Apple Intelligence off in Settings → Apple Intelligence & Siri.

Under **two forks**, that failure window can only be entered by someone who deliberately
downloaded Aware. Under **one merged product**, it is entered by a new user on perfectly
capable hardware, during first-run — which is precisely PROSOCHĒ's most fragile moment and
the one Phase 20 exists to protect. The merge risk was scoped as "users who answer the
toggle wrongly on old hardware"; it is actually "any user whose models haven't landed yet."

### What still stands

Unaffected by all of the above, and still device-confirmed:

- The `WFWorkflowImportQuestions` toggle gates the branch correctly in **both** directions.
- **The ordering discipline held under a real failure**: on the SE the core escalation at
  action index 3 had already completed before the halt. That is a structural property — core
  runs first, so *any* downstream halt is contained — and it is now backed by one real
  observation.
- `WFFileErrorIfNotFound = false` as the file-existence answer.
- Save File's one-time OS permission prompt on first write.
- **No try/catch exists**, now confirmed by an Apple DTS engineer directly:
  *"there is currently no way to detect an error from an action."* Spike 003's conclusion is
  reinforced, not weakened.

### What is now unproven, and what would close it

| Open question | Evidence needed |
|---|---|
| Does the **On-Device-pinned** `askllm` behave like the unpinned one? | Re-run the gate with `WFLLMModel = "Apple Intelligence on Device"` — the shipped config |
| Is a genuinely-ineligible-hardware failure a graceful **halt**, or a hang / partial write? | A run on a *known* ineligible device, with the generation recorded, AI state recorded |
| What happens on **capable hardware with models not yet downloaded**? | A capable device with Apple Intelligence freshly toggled on, run before provisioning completes |
| What happens with **Apple Intelligence switched off** on capable hardware? | Same device, AI toggled off in Settings |

The last two are the ones that actually matter for the merge, and neither has ever been
tested. A re-run should also record, for every device: model, iOS version, whether
Apple Intelligence is enabled, and whether model download had completed.

### Sources consulted for this reassessment

- [Apple Developer Forums — "Use Model" error handling](https://developer.apple.com/forums/thread/813757)
  (Apple DTS: no way to detect an action error)
- [MacStories — Apple's updated Foundation Models and the Use Model action](https://www.macstories.net/notes/i-have-many-questions-about-apples-updated-foundation-models-and-the-great-use-model-action-in-shortcuts/)
  (three model sources; no documented default)
- [Apple Support — How to get Apple Intelligence](https://support.apple.com/en-us/121115)
- [The Register — Apple Intelligence on by default from iOS 18.3](https://www.theregister.com/2025/01/22/apple_intelligence_enabled/)
- [MacRumors — iPhone 16e, A18, Apple Intelligence](https://www.macrumors.com/2025/02/19/apple-announces-iphone-16e/) and
  [GSMArena — iPhone 16e 8 GB RAM](https://m.gsmarena.com/iphone_16e_appears_on_geekbench_with_8gb_ram_-news-66653.php)
