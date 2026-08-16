---
spike: 001
name: device-model-literal
type: standard
validates: "Given a real iPhone, when Get Device Details queries \"Device Model\", then the exact literal string format (identifier vs marketing name) is known"
verdict: PARTIAL
related: []
tags: [shortcuts, device-detection]
---

# Spike 001: Device Model Literal

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

**Returned value format: PENDING** — awaiting the on-device round trip. Record the four
values here when reported.
