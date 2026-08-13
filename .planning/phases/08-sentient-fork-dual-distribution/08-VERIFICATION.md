---
phase: 08-sentient-fork-dual-distribution
status: human_needed
verified: 2026-08-13
automated_score: 22/22
human_score: 0/1
---

# Phase 8 Verification

All automated Phase 8 requirements pass. DIST-03 remains unverified because no qualifying iPhone is connected.

## Automated evidence

- `docs/sentient_core_check.py` reconstructs the frozen Dumb action list after removing exactly the Sentient import pair and audit block; it passes.
- `docs/sentient_audit_check.py` proves one On-Device call, progressive Circle II–VIII scope, recorded prior-consistency input only at VII–VIII, strict tokens, one challenge, completed-slow fallback, and high-Circle DENY exiting before persistence; it passes.
- Phase 5, 6, and 7 regression self-checks pass.
- Both XML sources pass `plutil` and Shortcuts Playground validation at macOS 26 / platform all.
- Both signed shortcuts and dated unsigned archives are non-empty and match `artifacts/shortcuts/MANIFEST.md`.
- Frozen Dumb SHA-256 remains `36d062e5dea739d6dd93eb007c4c3d0b18275782b49de7b29234cc1e49a8d899`.

## Human gate

`xcrun devicectl list devices` returned `No devices found.` DIST-03 requires an Apple-Intelligence-capable iPhone, both imports and first Manual runs, one Circle II–VIII audit/fallback case, and model-free Circle I/IX evidence. See `docs/device-evidence/Phase8-DIST-03-BLOCKED.md`.

## Verdict

`human_needed`: both requested artifacts are built, validated, archived, signed, and delivered; real-device behavior is not claimed.
