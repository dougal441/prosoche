---
phase: 08-sentient-fork-dual-distribution
plan: 01
subsystem: shortcuts
tags: [shortcuts, plist, apple-intelligence]
requires: [{phase: 07, provides: frozen Dumb shortcut}]
provides: [reproducible additive Sentient source, deterministic-core structural proof]
affects: [08-02, 08-03]
tech-stack: {added: [], patterns: [semantic plist insertion, atomic serialization]}
key-files: {created: [tools/build_sentient.py, src/PROSOCHE-Sentient.xml, docs/sentient_core_check.py], modified: []}
key-decisions: ["Use the device-evidenced Apple Intelligence on Device literal.", "Keep Circle I and IX model-free."]
requirements-completed: [SENT-01, SENT-02, SENT-03, SENT-12, SENT-15]
status: complete
---

# Phase 8 Plan 01: Additive Sentient Fork Summary

The Sentient XML is a reproducible clone of frozen Dumb with one optional audited-contract wrapper.

## Accomplishments

- Atomic builder preserves the Dumb source checksum and deterministic core.
- One `askllm` call is gated to Circles II–VIII with `Apple Intelligence on Device` and Text output.
- The check rejects OS-27-only web-search/follow-up keys and confirms Dumb has no model call.

## Verification

`python3 tools/build_sentient.py`, `python3 docs/sentient_core_check.py`, `plutil -lint`, target-26/all validator, and Phase 5–7 checks passed.

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check: PASSED

Commit `5485ca9` exists and the three declared artifacts exist.
