---
spike: 003
name: device-model-literal
type: standard
validates: "Given a real iPhone, when Get Device Details queries \"Device Model\", then the exact literal string format (identifier vs marketing name) is known"
verdict: INVALIDATED
related: []
tags: [shortcuts, device-detection]
---

# Spike 003: Device Model Literal

## What This Validates

`Donor 10.shortcut` (decrypted from `.planning/debug/Donor 10.shortcut` via the AEA1
round-trip documented in the project's `CLAUDE.md` §8) proved that
`is.workflow.actions.getdevicedetails` accepts `WFDeviceDetail = "Device Model"` as a
valid literal on a real device — this resolved two previously-UNVERIFIED capability-audit
items in one shot (Current Brightness / Current Volume readback also appear as literals
in the same donor).

What's still unknown: the exact *string this action returns* for Device Model (a raw
identifier like `iPhone16,1` vs a marketing name like `iPhone 16 Pro`).

**Superseded sub-question:** whether "Device Name," "OS Version," and "Build Number" exist
as sibling `WFDeviceDetail` literals was expected to need a device round trip. It did not —
see the correction below. The picker's full case list was found in the bundled catalog.

## Research

### Correction to the original research pass

The original pass concluded that `data/toolkit-v78-first-party-enum-cases.json` had "no
entry for any device-detail enum." **That conclusion was wrong.** It was a lookup error:
the file's enum entries are nested one level down under a top-level `types` key, and the
original sweep iterated only the top level. The entry exists and is complete:

- **Catalog path:** `data/toolkit-v78-first-party-enum-cases.json` → `types` →
  `getdevicedetails_wfdevice_detail`
- **typeId:** `com.apple.shortcuts.is.workflow.actions.getdevicedetails.WFDeviceDetail`
- **platforms:** `["iOS 27 Simulator", "macOS 27"]` — confirmed present on iOS, not
  macOS-only
- **caseCount:** 12

**The complete valid `WFDeviceDetail` case list, in catalog declaration order:**

| # | Literal |
|---|---|
| 1 | `Device Name` |
| 2 | `Device Hostname` |
| 3 | `Device Model` |
| 4 | `Device Is Watch` |
| 5 | `System Version` |
| 6 | `System Build Number` |
| 7 | `Screen Width` |
| 8 | `Screen Height` |
| 9 | `Current Volume` |
| 10 | `Current Brightness` |
| 11 | `Current Appearance` |
| 12 | `Device Is Locked` |

This list **independently corroborates the donor evidence**: all five literals recovered
from `Donor 10.shortcut` (`Device Model`, `Current Brightness`, `Current Volume`,
`Current Appearance`, `Device Is Locked`) appear in it. Two independent sources — device
ground truth and Apple's own ToolKit metadata — agree exactly. Per the project's evidence
hierarchy this is now the highest-confidence action schema in the audit.

### Other sources checked

- `ACTIONS.md`: documents `getdevicedetails` / `WFGetDeviceDetailsAction` only as an
  identifier — no parameter or enum detail. (Unchanged.)
- `golden-shortcuts/xml/*.xml` (19 real shortcuts): none use `getdevicedetails`.
  (Unchanged.)
- `data/toolkit-v78-first-party-parameter-keys.json`: no entry. (Unchanged.)
- Identifier presence: `is.workflow.actions.getdevicedetails` is in **both**
  `toolkit-v63-tool-ids.json` and `toolkit-v78-ios27-tool-ids.json`.

## Guesses Made, and Their Verdicts

Four literals were proposed for the probe before the catalog entry was found. All four
were adjudicated against the catalog **before** the device round trip:

| # | Proposed literal | Rationale for the guess | Verdict | Correct literal |
|---|---|---|---|---|
| 1 | `Device Model` | Confirmed from decrypted donor; used as known-good baseline | **CONFIRMED** | `Device Model` |
| 2 | `Device Name` | Matched the Title Case naming style shared by all donor-confirmed literals | **CONFIRMED** | `Device Name` |
| 3 | `OS Version` | Task's primary guess | **REFUTED** | `System Version` |
| 3-alt | `System Version` | Flagged as the more likely alternate on naming-convention grounds | **CONFIRMED** | `System Version` |
| 4 | `Build Number` | Task's primary guess | **REFUTED** | `System Build Number` |
| 4-alt | `Software Version` | Task's alternate guess | **REFUTED** | `System Build Number` |

Neither proposed candidate for #4 was correct — the real literal is `System Build Number`,
which was not among the guesses. This is the clearest argument for having checked the
catalog rather than shipping guesses: the probe as originally specified would have halted
mid-run and burned a device round trip without answering #4 at all.

## Toolchain Finding (affects every future build)

**`--target-macos 26 --target-platform ios` — the invocation prescribed in the project's
`CLAUDE.md` — is a vacuous combination in Shortcuts Playground v1.2.1 and rejects every
shortcut.**

Mechanism, from `scripts/validate_shortcut.py`:

- `toolkit-v63-tool-ids.json` carries a **macOS** platform label, so `--target-platform ios`
  filters it out entirely.
- The only iOS-labelled snapshot, `toolkit-v78-ios27-tool-ids.json`, is version-gated to
  **27**, so `--target-macos 26` filters it out too.
- Result: the allowlist is empty and every action reports
  `Action identifier requires macOS 27+ (toolkit-v78)`.

Verified by control test: a bundled known-good golden shortcut
(`golden-shortcuts/xml/1be4dde95b794253bf82438e201b33e7.xml`) produces 7 identical
`requires macOS 27` errors under the same flags. This is a tooling artifact, not a defect
in the shortcut under test.

**Use both of these instead**, and require both to pass:

```bash
validate-shortcut "<file>.xml" --target-macos 26                        # iOS-26 baseline (generic v63 allowlist)
validate-shortcut "<file>.xml" --target-macos 27 --target-platform ios  # real iOS snapshot + enum-value gating
```

The second invocation is the valuable one and was **not** part of the documented process:
it is the only mode that loads the v78 first-party enum catalog and therefore the only mode
that can catch an invalid picker literal. It is what caught all three bad guesses above.
The tradeoff noted in `CLAUDE.md` (target 27 also enables OS27-only *parameter* keys such
as `WFAllowWebSearch` / `interpretAsMarkdown`) still stands, so treat target 27 as a
**cross-check for picker values**, not as the primary target.

Recommend updating `CLAUDE.md` §1 "Exact validator invocation" accordingly.

## How to Run

Import `PROSOCHĒ Device Probe.shortcut` onto the target iPhone and tap to run.

## What to Expect

A single result screen with four lines: Device Model, Device Name, System Version, and
System Build Number. All four literals are catalog-verified valid picker options, so the
run should not halt.

The remaining question is purely about **returned value format**, above all whether Device
Model returns a raw identifier (`iPhone16,1`) or a marketing name (`iPhone 16 Pro`).

## Investigation Trail

- Decrypted `Donor 10.shortcut` (2026-08-16) → confirmed `WFDeviceDetail` literals
  `"Device Model"`, `"Current Brightness"`, `"Current Volume"`, `"Current Appearance"`,
  `"Device Is Locked"` all exist and validate on a real device.
- First check of bundled Playground docs + golden corpus found nothing → concluded an
  on-device probe was the only remaining evidence channel.
- Built an 18-action, 6-probe version that showed each result on its own screen, ordered
  most-confident-first, to isolate which guessed literal halted the run.
- Validating that draft at `--target-macos 27 --target-platform ios` surfaced the enum
  catalog, which **rejected three of the six literals by name and printed the full valid
  case list**. This answered the validity question with zero device round trips and
  revealed the lookup error in the original research pass.
- Rebuilt as a 9-action, 4-probe version using only verified literals, with one combined
  result screen. Both validator invocations pass.
- Signed artifact decrypted and re-inspected to confirm what actually shipped: 9 actions,
  the four correct literals, text placeholder offsets `[49, 67, 88, 114]` matching their
  attachment keys.

## Results

**Literal validity: RESOLVED** (by catalog evidence, corroborated by donor evidence — see
the case table above). No device run was required.

**Returned value format: RESOLVED — and it kills the capability-detection premise.**

On-device run (2026-08-16, real iPhone, iOS 26.6):

| Field | Returned value |
|---|---|
| Device Model | `iPhone` |
| Device Name | *(the phone's user-assigned name — omitted here, not load-bearing)* |
| System Version | `26.6` |
| System Build Number | `23G71` |

**Device Model returns the bare literal `"iPhone"` — not a model identifier
(`iPhone16,1`) and not a marketing name (`iPhone 15 Pro`/`iPhone 16`).** It does not
disambiguate hardware generation at all. Every iPhone running Shortcuts, from an
iPhone 8 to the newest Pro Max, would return the identical string. This makes it
structurally impossible to build the hardware-capability lookup table spike 004 was
scoped to build — there is no signal here to gate on.

`System Version` (`26.6`) is real OS-version data, but OS version alone cannot stand in
for hardware capability: iOS 26 runs on both Apple-Intelligence-capable (iPhone 15 Pro+)
and non-capable hardware. Gating on OS version alone would incorrectly mark plenty of
real devices as capable.

**No other `WFDeviceDetail` case offers a usable proxy either.** Of the 12 confirmed
literals (see enum table above), the only device-shape-adjacent ones are `Screen Width` /
`Screen Height` — and screen dimensions repeat across many hardware generations, so they
can't reliably distinguish an Apple-Intelligence-eligible model from an ineligible one.

**Verdict: INVALIDATED.** `Get Device Details` cannot support automatic
Apple-Intelligence-capability detection on iOS 26 Shortcuts. This is a hard platform
ceiling, not a wiring mistake — there is no available action, parameter, or picker case
anywhere in the audited surface that exposes a disambiguating hardware identifier.
Spike 004 (capability-gate) as originally scoped depends entirely on this signal existing
and cannot proceed as planned. See MANIFEST.md for the pivot decision.

### Follow-up research: is there ANY indirect signal? (web search, 2026-08-16)

Requested by the user after the on-device result came back, to check whether
`System Build Number` or some other indirect proxy could substitute. All dead ends:

- **`System Build Number` is a pure OS-build identifier** (e.g. `23G71` = iOS 26.6 RC),
  identical across every device running that build regardless of hardware. No
  hardware signal at all. [BetaWiki](https://betawiki.net/wiki/IOS_26.6_build_23G71),
  [TidBITS build-number explainer](https://tidbits.com/2020/07/08/how-to-decode-apple-version-and-build-numbers/).
- **Apple Intelligence hardware floor:** A17 Pro (iPhone 15 Pro / 15 Pro Max) or
  A18 / A18 Pro (iPhone 16 family), plus an 8 GB RAM minimum. Notably the plain
  **iPhone 15 / 15 Plus do not qualify** (A16 Bionic, 6 GB RAM) despite shipping the same
  generation and same iOS as the 15 Pro — capability doesn't even track cleanly by
  "device generation," only by specific SKU/chip.
  [macobserver](https://www.macobserver.com/iphone/what-iphones-have-apple-intelligence/),
  [techpp](https://techpp.com/2026/04/01/apple-intelligence-supported-devices/).
- **iOS 26 itself supports back to iPhone 11 / SE (2nd gen)**, i.e. any A13+ device —
  a huge population, the large majority of which is *not* Apple-Intelligence-capable.
  So `System Version` returning "26.x" carries almost no capability signal; most
  iOS-26-capable devices are ineligible for Apple Intelligence.
  [SimplyMac iOS 26 compatibility list](https://www.simplymac.com/ios/ios-26-compatible-phones-full-list),
  [TechRadar iOS 26 compatibility](https://www.techradar.com/phones/iphone/ios-26-and-ipados-26-compatibility-explained-which-models-are-supported).
- **The real capability check exists, but isn't reachable from Shortcuts.** Apple's
  actual API for this is `SystemLanguageModel.default.availability` (Foundation
  Models framework) — a Swift API for native app code, not a Shortcuts action. Even if
  it were reachable, PROSOCHĒ's own constraints ("no companion app, no private APIs")
  already rule out that path. [dev.to fallback-gracefully writeup](https://dev.to/arshtechpro/how-to-fall-back-gracefully-when-apple-intelligence-isnt-available-48j).
- **No app-presence check exists in Shortcuts** to probe for an Apple-Intelligence-only
  system app (e.g. Image Playground) as a proxy — consistent with the project's own
  capability audit finding "no native file/app-existence check anywhere in Shortcuts."
- **`Use Model` failing on ineligible hardware wouldn't help even if confirmed** —
  Shortcuts has no try/catch, so any failure surfaces as a visible user-facing error
  dialog rather than something a shortcut can silently branch on. One forum thread
  ([Apple Developer Forums](https://developer.apple.com/forums/thread/813757)) confirms
  `Use Model` error-handling is already a known pain point for context-window overflows;
  nothing suggests ineligible-hardware failures behave differently or more catchably.

**Net: confirmed, not just suspected — there is no detection path, direct or indirect,
available to a pure Shortcuts implementation.** The ceiling is architectural (Apple's own
API surface + PROSOCHĒ's no-companion-app constraint), not a gap in this research pass.

### Second follow-up: could a try/catch pattern work instead? (2026-08-16)

User's proposal: attempt the on-device model, catch failure, save the result as a
boolean. Checked against the toolchain docs (zero error/try/catch parameters documented
on `askllm` or any other action in `ACTIONS.md`/`APPINTENTS.md`/`CONTROL_FLOW.md`) and web
research, both agree:

- **Shortcuts has no catch branch, structurally.** When an action errors, the entire
  shortcut halts immediately — no action after the failure point runs, including a
  "save this to a boolean" step. There is no "if fail" to attach recovery logic to; the
  shortcut just stops and surfaces an error to the user.
  [Apple Community thread](https://discussions.apple.com/thread/254812093),
  [Apple Developer Forums — Use Model error handling](https://developer.apple.com/forums/thread/813757).
- **`Use Model` reportedly shows as greyed out in the Shortcuts editor UI itself** on
  incapable hardware, per Apple's own support docs — meaning the incompatibility can
  surface at the authoring/configuration level, not only at runtime. Even setting aside
  the no-catch-branch problem, there may be no clean "attempt it and observe the result"
  moment to hook into at all.
  [Apple Support — Use Apple Intelligence in Shortcuts](https://support.apple.com/guide/iphone/use-apple-intelligence-in-shortcuts-iph78c41eaf8/ios).

**Verdict: also infeasible, for a different reason than the device-detection path (no
catch mechanism exists at all, vs. no disambiguating data exists).** Both routes to
automatic fork selection are closed. The only remaining mechanism is an explicit,
user-set toggle.
