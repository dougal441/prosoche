---
status: resolved
trigger: "Ok, I got an error when testing both. I have an iphone 15 pro on 26.6. Can you identify what features could be causing this and tell me. \"can't import shortcut because it contains features not supported on this device\""
created: 2026-08-13T19:30:00+10:00
updated: 2026-08-13T21:38:00+10:00
---

## Current Focus

hypothesis: Confirmed — the synthetic Notes AppIntent serialization is rejected by iOS 26.6; the Apple-exported `com.apple.mobilenotes.SharingExtension` pipeline is supported. Bare-string Open App values and `Down` rounding are independent runtime serialization defects.
test: Replace each generator-created Open App action with an app descriptor and `WFAppIdentifier`, replace the Note action with Text → Rich Text from Markdown → Create Note, then validate and sign both forks.
expecting: Sources contain no legacy Notes AppIntent or bare app strings, every downward-round action uses `Always Round Down`, and signed artifacts are non-empty with archives matching their sources.
next_action: Resolved — target-device import and first-run Note creation confirmed for both rebuilt forks.
bug_class: bohrbug
reasoning_checkpoint:
  hypothesis: "The unsupported synthetic Notes AppIntent causes the importer rejection; replacing it with the target device's native Create Note representation removes that unsupported feature while preserving the Control Room body."
  confirming_evidence:
    - "The isolated synthetic Notes probe reproduced the exact import error on iOS 26.6."
    - "The target iPhone donor uses Text → Rich Text from Markdown → com.apple.mobilenotes.SharingExtension with CreateNoteLinkAction."
  falsification_test: "A rebuilt signed shortcut that still contains no synthetic Notes action but fails the same device import error would disprove this being the first blocker."
  fix_rationale: "The replacement uses the native action identifier, parameter names, and variable wiring emitted by the target device rather than an inferred AppIntent."
  blind_spots: "Only the user can run final import and first-run Notes behavior on the target iPhone."
  candidate_causes:
    - "code: an inferred/unsupported Notes AppIntent action identifier and payload"
    - "environment: iOS 26.6 rejects that inferred action during import"
  and_gate: "no — the isolated Notes probe reproduces the symptom; environment is the compatibility boundary, but a supported donor payload alone avoids it."
tdd_checkpoint: null

## Symptoms

expected: Both signed shortcuts import successfully on an iPhone 15 Pro running iOS 26.6.
actual: Both shortcuts are rejected during import.
errors: "Can't import shortcut because it contains features not supported on this device."
reproduction: Open either signed `.shortcut` file on the iPhone and attempt to import it.
started: First real-device import test after the shortcuts were built and signed.

## Eliminated

- hypothesis: Bare-string `WFSelectedApp` is an iOS 26.6 import blocker.
  evidence: Probe 2 imported successfully. Its blank icon and failure to open until Notes was manually selected prove a runtime serialization defect instead.
  timestamp: 2026-08-13T20:59:13+10:00

- hypothesis: `WFRoundMode="Down"` is an iOS 26.6 import blocker.
  evidence: Probe 4 imported and ran. It returned 5 for 4.7, showing iOS ignored the invalid mode and used normal rounding rather than rejecting the shortcut.
  timestamp: 2026-08-13T20:59:13+10:00

- hypothesis: The Sentient-only On-Device model action is the sole cause.
  evidence: The Dumb fork contains no model action and fails with the same importer message.
  timestamp: 2026-08-13T19:30:00+10:00

## Evidence

- timestamp: 2026-08-13T21:38:00+10:00
  checked: Target-device acceptance check on the iPhone 15 Pro running iOS 26.6.
  found: The user confirmed both rebuilt forks imported successfully and the first Manual/Control Room action created the Note successfully.
  implication: The donor-backed native Notes replacement removes the importer blocker and preserves the required first-run Notes behavior on the affected device.

- timestamp: 2026-08-13T21:35:00+10:00
  checked: Shared source generator and static Dumb Notes action.
  found: The generator now emits full Open App descriptors plus `WFAppIdentifier` and uses `Always Round Down`; both rebuilt forks replace the synthetic Notes AppIntent with `gettext` → `getrichtextfrommarkdown` → `com.apple.mobilenotes.SharingExtension` using `CreateNoteLinkAction` and a Rich Text output attachment.
  implication: The unsupported isolated-probe identifier and the known runtime-serialization defects are absent from the rebuilt sources.

- timestamp: 2026-08-13T21:37:00+10:00
  checked: Rebuilt Dumb and Sentient XML plus new signed artifacts.
  found: Both XML sources pass `plutil`, the Shortcuts Playground macOS-26/all validator, and an agent-authored structural check covering all 18 Open App actions, three downward-round actions, the absence of the legacy Notes action, and the Create Note Rich Text wiring. Both signing runs completed and produced non-empty distribution artifacts with dated archives.
  implication: The static, signing, and source-to-artifact gates pass; target-device import and first-run Notes creation remain the required acceptance check.

- timestamp: 2026-08-13T21:20:31+10:00
  checked: Apple-signed `.planning/debug/Donor - apps.shortcut` exported from the affected iPhone.
  found: The AEA1 archive decrypts cleanly and contains exactly six `is.workflow.actions.openapp` actions for Notes, Voice Memos, Camera, Reminders, Calendar, and Contacts. Every action carries a native `WFSelectedApp` dictionary with `BundleIdentifier`, `Name`, and `TeamIdentifier`, plus the matching `WFAppIdentifier`.
  implication: The repair can replace all 18 bare-string Open App selections with exact native descriptor shapes instead of inferred picker data.

- timestamp: 2026-08-13T21:20:31+10:00
  checked: Apple-signed `.planning/debug/Donor - notes.shortcut` exported from the affected iPhone.
  found: The AEA1 archive decrypts cleanly and contains `is.workflow.actions.gettext` → `is.workflow.actions.getrichtextfrommarkdown` → `com.apple.mobilenotes.SharingExtension`. The native Create Note action uses `AppIntentIdentifier: CreateNoteLinkAction`, a `WFCreateNoteInput` token attachment referencing the Rich Text output, and the default iCloud Notes folder.
  implication: The unsupported `com.apple.Notes.CreateNoteFromMarkdownLinkAction` can be replaced with the exact iOS 26.6-native action and variable wiring; no opaque AppIntent fields need to be guessed.

- timestamp: 2026-08-13T20:59:13+10:00
  checked: On-device import and minimal runtime behavior on iPhone 15 Pro running iOS 26.6.
  found: Probe 1 imported. Probe 2 imported, but Open App displayed a blank app icon and could not run until Notes was manually selected. Probe 3 failed import with the same unsupported-feature error as both full shortcuts. Probe 4 imported, ran, and rounded 4.7 to 5.
  implication: The Notes Create Note from Markdown AppIntent payload is the confirmed first import blocker. Bare-string Open App and Round mode `Down` still require repair because they import with broken/default runtime behavior.

- timestamp: 2026-08-13T20:53:58+10:00
  checked: Minimal signed device-probe matrix.
  found: Built four isolated probes under `artifacts/device-import-probes/`. All XML plists pass `plutil`, default validation, and the original macOS-26/all validator path; the stricter v78 catalog rejects only probe 4 because `WFRoundMode="Down"` is not a current enum value. All four were signed for anyone, are non-empty (22 KB each), and their archived unsigned inputs match the source XML byte-for-byte.
  implication: The iPhone import results can distinguish shared signing/root-metadata failure from each of the three ranked suspect payloads without running any shortcut.

- timestamp: 2026-08-13T19:30:00+10:00
  checked: User device and failure scope.
  found: Both forks fail identically on an iPhone 15 Pro running iOS 26.6.
  implication: Start with shared graph actions and workflow metadata, then consider additional Sentient-only blockers separately.

- timestamp: 2026-08-13T19:30:00+10:00
  checked: Shared-action serialization, signed-artifact parity, and validator/catalog coverage.
  found: 18 `is.workflow.actions.openapp` actions serialize `WFSelectedApp` as bare strings (Notes ×4, Reminders ×4, Calendar ×4, Camera ×2, Contacts ×2, Voice Memos ×2) although the parameter is an app-descriptor state; one shared `com.apple.Notes.CreateNoteFromMarkdownLinkAction` contains unverified `TeamIdentifier: "0000000000"`, `BundleIdentifier: "com.apple.mobilenotes"`, and speculative `name`; and three shared `is.workflow.actions.round` actions emit invalid `WFRoundMode: "Down"` literals rejected by the current enum validator, which permits `Normal`, `Always Round Up`, and `Always Round Down`.
  implication: These shared serialization defects are the ranked import-blocker cluster. A minimal device export comparison is required to prove which one is rejected first.

- timestamp: 2026-08-13T19:30:00+10:00
  checked: Validation coverage and alternative shared candidates.
  found: The release check used `--target-macos 26 --target-platform all`, which suppresses the current catalog's v78 parameter/enum checks; iOS-target validation is not reliable because its v63 snapshot lacks basic actions. Apple documents Get Device Details current volume and brightness as available since iOS/iPadOS 16.4. Signed artifacts decrypt and have action graphs identical to their archived unsigned inputs; signing changed only root metadata.
  implication: The static pass does not clear the serializer candidates. Current Volume/Current Brightness and artifact corruption/source drift are eliminated.

## Resolution

root_cause: The serialized `com.apple.Notes.CreateNoteFromMarkdownLinkAction` payload is rejected by the iOS 26.6 importer and reproduces the original error in isolation. The probe does not distinguish whether the unsupported component is the action identifier, AppIntentDescriptor, or one of its parameters. Bare-string `WFSelectedApp` and `WFRoundMode="Down"` are additional runtime defects but do not block import.
fix: Replaced the unsupported Notes AppIntent with native `getrichtextfrommarkdown` → `com.apple.mobilenotes.SharingExtension` / `CreateNoteLinkAction` wiring; normalized every Open App descriptor and changed all downward rounding to `Always Round Down`.
verification: Both XML files pass `plutil` and `validate_shortcut.py --target-macos 26 --target-platform all`; structural assertions, signing, and archive/source parity pass. On the target iPhone 15 Pro/iOS 26.6, both rebuilt forks imported and the first Manual/Control Room action created the Note successfully.
oracle_type: Target-device iPhone import and runtime behavior.
files_changed: [tools/build_state_engine.py, src/PROSOCHE-Dumb.xml, src/PROSOCHE-Sentient.xml, artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut, artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut]
prevention: why not caught: no iPhone import gate existed for inferred AppIntent payloads; guard: retain a signed target-device donor-export compatibility probe plus target-iPhone import/first-run smoke check for new native actions.
