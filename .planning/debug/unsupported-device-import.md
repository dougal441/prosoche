---
status: resolved
trigger: "Ok, I got an error when testing both. I have an iphone 15 pro on 26.6. Can you identify what features could be causing this and tell me. \"can't import shortcut because it contains features not supported on this device\""
created: 2026-08-13T19:30:00+10:00
updated: 2026-08-13T21:20:31+10:00
---

## Current Focus

hypothesis: Confirmed — the serialized `com.apple.Notes.CreateNoteFromMarkdownLinkAction` payload is the first iOS 26.6 importer blocker. Open App and Round mode are separate runtime serialization defects, not import blockers.
test: Completed four-probe iPhone import matrix and inspected two Apple-signed donor shortcuts exported from the affected iPhone.
expecting: Matched. The donors provide native iOS 26.6 payloads for all six Open App targets and for Text → Rich Text from Markdown → Create Note.
next_action: Apply the donor-backed payloads in the source generator, change downward rounding to `Always Round Down`, rebuild and sign both shortcuts, then repeat full-device import and runtime verification.
bug_class: bohrbug
reasoning_checkpoint: null
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
fix: Not applied; diagnosis only. Use an iPhone-native iOS 26.6 Notes export or supported fallback, then also repair the Open App descriptor and use `Always Round Down` where downward rounding is intended.
verification: Four signed isolated probes tested on the target iPhone: baseline pass, Open App import pass/runtime fail, Notes AppIntent import fail with matching error, Round import/runtime pass with default-normal result.
oracle_type: Target-device iPhone import and runtime behavior.
files_changed: [artifacts/device-import-probes/01-baseline.xml, artifacts/device-import-probes/02-open-app.xml, artifacts/device-import-probes/03-notes-app-intent.xml, artifacts/device-import-probes/04-round-mode.xml, artifacts/device-import-probes/PROSOCHĒ Probe 1 — Baseline.shortcut, artifacts/device-import-probes/PROSOCHĒ Probe 2 — Open App.shortcut, artifacts/device-import-probes/PROSOCHĒ Probe 3 — Notes Intent.shortcut, artifacts/device-import-probes/PROSOCHĒ Probe 4 — Round Mode.shortcut, artifacts/device-import-probes/TESTING.md]
