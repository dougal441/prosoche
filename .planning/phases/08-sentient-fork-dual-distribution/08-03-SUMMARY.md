---
phase: 08-sentient-fork-dual-distribution
plan: 03
subsystem: distribution
tags: [shortcuts, signing, artifacts]
requires: [{phase: 08-02, provides: validator-clean Sentient source}]
provides: [two signed shortcuts, dated unsigned archives, checksum manifest, honest UAT record]
affects: [release, real-device-uat]
tech-stack: {added: [], patterns: [validate-sign-verify-nonzero]}
key-files: {created: [README.md, artifacts/shortcuts/MANIFEST.md, docs/device-evidence/Phase8-DIST-03-BLOCKED.md], modified: [docs/BUILD-NOTES.md]}
key-decisions: ["DIST-03 remains unchecked without a qualifying iPhone."]
requirements-completed: [DIST-01, DIST-02, DIST-04, DIST-05, DIST-06, DIST-07, DIST-08]
status: blocked
---

# Phase 8 Plan 03: Dual Distribution Summary

Both distinct forks validate, archive, sign, and retain verifiable distribution evidence; device UAT is honestly blocked.

## Accomplishments

- Resolver-confirmed Dumb icon stayed frozen; Sentient received its own teal metadata.
- Both XML files passed plist lint and target-26/all validation, then produced non-empty signed files and dated unsigned archives.
- README, build notes, manifest, and a device-UAT record document privacy, fallbacks, and exact SHA-256 values.

## Checkpoint

`xcrun devicectl list devices` returned no devices. DIST-03 is unchecked; see `docs/device-evidence/Phase8-DIST-03-BLOCKED.md`.

## Verification

Both signed files and archives are non-empty; hashes are distinct in `artifacts/shortcuts/MANIFEST.md`.

## Self-Check: PASSED

Commit `24a290c` and all manifest artifacts exist.
