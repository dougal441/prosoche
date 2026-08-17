# Phase 16 — API Coverage Declaration

**Status:** declared, 2026-08-18, plan 16-06
**Verdict:** **No external API integration in this phase.**

## The declaration, with its reason

**No external API integration.** This phase integrates nothing external, so there is no API
surface to enumerate and no coverage matrix to fill in. A matrix authored anyway would be a
fabrication — rows invented to satisfy a detector rather than to describe anything that exists.

The reason, stated rather than asserted:

| What this phase actually builds against | Why it is not an external API |
|---|---|
| `tools/build_state_engine.py` and `tools/build_sentient.py` | Local Python generators that emit a Shortcuts plist. They call no service and open no socket. Python usage across all six plans of this phase is **stdlib only** — `plistlib`, `pathlib`, `json`, `copy`, `inspect`, `re`, `uuid`, `hashlib`, `sys`. |
| The thirteen `docs/*.py` static checkers | Local file-level assertions over `src/*.xml`, the generators and the repository's own records. They read files and exit 0 or 1. |
| The Shortcuts Playground validator and the macOS `shortcuts` CLI | Local build tooling, invoked as subprocesses on this machine. The validator consults **bundled** ToolKit snapshots shipped with the plugin; nothing is fetched. |
| `xcrun devicectl` | A local Apple developer tool that enumerates devices attached to *this* Mac. |
| The iOS action identifiers the product emits (`is.workflow.actions.setbrightness`, `…setvolume`, `…getdevicedetails`, `com.apple.mobilenotes.*`, and the rest) | These are **on-device system actions**, resolved by iOS at run time inside the Shortcuts runtime. They are not network endpoints, they carry no authentication, and they are not reachable from this repository at all. |

## Why the detector fired anyway

The API-coverage detector keys on trigger vocabulary, and this phase's artifacts are dense with
it: "capture", "restore", "request", "response", "gate", "endpoint"-adjacent phrasing in the
threat register, and repeated discussion of `Get Device Details` "returning a value". Every one
of those is a **local** operation inside the Shortcuts runtime on the user's own phone.

## The product's own position, which this declaration inherits

PROSOCHĒ has **no network surface at all**, by design and as a hard constraint:

- No behavioural data leaves the device.
- No accounts, no authentication, no tenancy, no telemetry, no referral, no tracking.
- The Sentient/Aware fork's AI path is Apple **On-Device** Intelligence via the iOS 26
  `Use Model` action — **never** cloud, never Private Cloud Compute, never ChatGPT. That is a
  constraint in `.claude/CLAUDE.md`, not a preference.
- State is one `state.json` in the Shortcuts iCloud folder and one Apple Note. Both are local
  files; iCloud's own sync is Apple's, not an integration this project makes.

Threat register entry **T-16-32** records the same fact from the security side and dispositions
it `accept` for exactly this reason: *the product has no network surface and no secrets; nothing
leaves the device.* It is recorded for completeness rather than as an open risk.

## Package legitimacy

**Zero external packages were installed by any plan in this phase.** `16-RESEARCH.md`'s Package
Legitimacy Audit records the phase as installing nothing, verified by direct inspection, and all
six plan summaries independently record `T-16-SC` as accepted on the same ground. The signing
toolchain is the already-vetted Shortcuts Playground plugin plus the macOS `shortcuts` CLI —
both pre-existing on the build machine, neither fetched by this phase.

## What this declaration does NOT claim

It says nothing about **device** verification. The absence of an external API is a fact about
integration surface; it is not evidence about behaviour. Every device-gated claim in this phase
remains **BLOCKED on DIST-03** and is recorded as such in
`16-UAT.md`, with the reason re-measured at execution time.
