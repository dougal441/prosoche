---
spike: 002
name: close-automation-vs-screen-lock
type: standard
validates: "Given a tracked app in foreground, when the user locks the screen (vs. switches app), then determine whether the \"App Is Closed\" Personal Automation fires the same CLOSE signal in both cases"
verdict: PENDING
related: [001]
tags: [session-model, close-pipeline, personal-automations]
---

# Spike 002: Close-Automation vs. Screen-Lock

## What This Validates

Given a tracked app in the foreground, when the user (a) switches to a different app,
(b) locks the screen directly, or (c) locks the screen and later unlocks straight back
into the same app, then does iOS's "App Is Closed" Personal Automation trigger fire the
same `CLOSE` signal in all three cases — the exact signal PROSOCHĒ's CLOSE pipeline
depends on to end `active_session`, restore `settings_snapshot`, and finalize
`recent_sessions` (`.planning/research/ARCHITECTURE.md` §4–5).

This is a pure iOS runtime-behavior question. No file-level analysis, catalog lookup, or
donor-shortcut decryption can answer it — it requires a device log across real lock/unlock
events, the same "device ground truth beats inference" discipline this project already
applies everywhere else (`.claude/CLAUDE.md` "Evidence hierarchy").

## Research

Apple's own documentation for Personal Automations describes "App Is Closed" as firing
when the app "is no longer active" — which is ambiguous between "backgrounded because the
user switched apps" and "backgrounded because the screen locked." Community reporting is
mixed and version-dependent, which is exactly why this project's evidence hierarchy puts
external corroboration below on-device confirmation. No Playground-bundled doc
(`AUTOMATION_TRIGGERS.md`) documents Personal Automation trigger semantics — it only covers
`WFWorkflowTriggers` metadata for shortcut-embedded triggers, which explicitly does not
apply here (this project's Personal Automations are user-created outside the shortcut).

## How to Run

**Artifacts in this spike folder:**
- `Lock Signal Probe.shortcut` — signed, ready to AirDrop/import to the test iPhone
- `Lock Signal Probe.xml` — unsigned editable source

**What the probe does:** on every run it appends one line to a Note named
"Lock Signal Probe Log" — no UI, no dialogs, nothing to dismiss. Each line records:
timestamp (`yyyy-MM-dd HH:mm:ss`), which signal triggered the run (`OPEN`, `CLOSE`, or
`MANUAL` for a bare manual run), and the live `Device Is Locked` reading at that moment
(confirmed literal per [Spike 001](../001-device-is-locked-literal/README.md)).

**Setup (one-time, on the test iPhone):**
1. If a shortcut named "Lock Signal Probe" already exists in the library, delete it first
   — duplicate names silently skip on import.
2. Import `Lock Signal Probe.shortcut`.
3. Run it once manually to confirm it logs `signal=MANUAL` with no crash — this also
   triggers the one-time iOS Notes permission prompt (a system prompt, not shortcut UI).
4. Pick one already-tracked app for this test (any app you don't mind automations firing
   against for a few minutes).
5. Create two Personal Automations if you don't already have equivalents:
   - **App Is Opened** → [test app] → Run Shortcut "Lock Signal Probe" with input text `OPEN`
   - **App Is Closed** → [test app] → Run Shortcut "Lock Signal Probe" with input text `CLOSE`
6. In **both** automations, turn **Ask Before Running OFF** and confirm **Notify When Run**
   is off. If either is left on, iOS will show its own confirmation/notification banner on
   every lock/unlock — that's an OS automation setting, not something the shortcut controls.

**Test protocol — run each scenario once, then open the "Lock Signal Probe Log" Note and
copy the new lines into the Investigation Trail below before moving to the next scenario:**

| Scenario | Steps | What you're checking |
|---|---|---|
| A — baseline app switch | Open test app → wait 3s → swipe to home screen (do not lock) → wait 3s | Confirms OPEN and CLOSE both log normally with a plain app-switch. This is the known-working case; it's the control. |
| B — direct screen lock | Open test app → wait 3s → press the side button to lock the screen directly (screen still showing the app when you lock it) → wait 5s | Does a CLOSE line appear? If yes, at what point — before or after the log shows `locked=true`? |
| C — lock then unlock back in | Open test app → wait 3s → lock the screen → wait 10s → unlock and land back in the same test app → wait 3s → leave the app | Does locking produce a CLOSE, and does unlocking back into the same app produce a *second* OPEN — i.e., does the automation treat "still on the lock screen over the same app" as one continuous session or two? |
| D — lock, wait long, then leave from lock screen | Open test app → lock the screen → wait 30s+ → without unlocking, swipe home or open a different app from the app switcher (if reachable) | Edge case: does a CLOSE ever fire if the device is never unlocked again in the same test window? |

## What to Expect

Four (or more) new lines in the "Lock Signal Probe Log" Note, one per automation fire,
each showing `signal=OPEN` or `signal=CLOSE` plus the `locked=` reading at that instant.
The critical comparison is Scenario A's CLOSE line (known good) against Scenario B's —
does a CLOSE line exist at all for B, and if so is its `locked=` field `true` (meaning
Get Device Details itself resolves correctly even while the screen is locked, which would
support using it as a defensive check elsewhere in the pipeline)?

## Investigation Trail

*(To be filled in from the on-device log after each scenario is run — this is the
human-verification checkpoint; the agent cannot execute this on the user's phone.)*

- Scenario A:
- Scenario B:
- Scenario C:
- Scenario D:

## Results

**Verdict: PENDING — requires on-device confirmation.**

The probe is built, validated (`--target-macos 26`; see Deviations below for the
`--target-platform ios` finding), and signed. What is already known without running it:

- The `Device Is Locked` literal itself is donor-confirmed independent of this spike
  (Spike 001) — the probe's own reading of it is not in question, only whether the
  *automation trigger* fires at the moments this test protocol targets.
- This spike cannot reach VALIDATED/INVALIDATED without the human checkpoint below.

╔══════════════════════════════════════════════════════════════╗
║  CHECKPOINT: Verification Required                           ║
╚══════════════════════════════════════════════════════════════╗

**Spike 002: close-automation-vs-screen-lock**
**How to run:** see "How to Run" above — import `Lock Signal Probe.shortcut`, wire the two
Personal Automations, run scenarios A–D in order.
**What to expect:** a CLOSE log line for scenario A (control) and a direct comparison for
whether scenario B (direct lock) also produces one.

──────────────────────────────────────────────────────────────
→ Run the four scenarios and report back what the "Lock Signal Probe Log" Note shows —
paste the new lines it accumulates, in order. That updates this spike's Investigation
Trail and Verdict.
──────────────────────────────────────────────────────────────

## Build Notes — Deviations from Spec (shortcut-builder agent report)

1. **`--target-macos 26 --target-platform ios` is degenerate in the installed Playground
   version (v1.2.1)** — it rejects every action including `is.workflow.actions.comment`,
   because no iOS-26-specific ToolKit snapshot is bundled and `--target-platform ios`
   filters out the generic v63 allowlist entirely, leaving only OS-27-gated rows. This is
   a tooling artifact, not a defect in the probe. Validation instead used
   `--target-macos 26` (passed) and `--target-macos 26 --target-platform all` (passed) as
   the closest honest rendering of the intended iOS-26 posture. Cross-checking at
   `--target-macos 27 --target-platform ios` failed on exactly the three Notes actions
   (`filter.notes`, `appendnote`, `mobilenotes.SharingExtension`) — the same
   bundled-data completeness gap already recorded in this project's own capability audit
   (`.claude/CLAUDE.md` §3 item 5), not a new finding. **Follow-up:** the project's
   "Exact validator invocation" section should be corrected — the prescribed flag pair
   cannot pass for any shortcut in this Playground version.
2. **Create Note carries two content keys** (`contents` and the legacy `WFCreateNoteInput`)
   because the validator's accepted key set didn't include `contents` alone. Both are
   real, documented keys (not invented); whichever the device recognizes wins, and
   Shortcuts silently ignores the other. Check the very first auto-created note's body —
   if it's empty, flag it, but the cost of being wrong is one silently-empty note title
   that self-heals on the next Append.
3. **`AppIntentDescriptor` for Create Note was synthesized** from the documented template
   pattern (`BundleIdentifier com.apple.mobilenotes`, `AppIntentIdentifier SharingExtension`)
   — not independently attested for this specific action, per the project's own
   do-not-fabricate discipline.
4. **`WFWorkflowInputContentItemClasses` is non-empty** on this probe (unlike the
   production PROSOCHĒ shortcut's "leave empty" guidance) because the validator hard-rejects
   referencing Shortcut Input with an empty class list. `WFWorkflowTypes` stays empty so
   this doesn't add the probe to the Share Sheet.
5. **Append newline behavior is undocumented** in this bundle — if log lines run together
   without paragraph breaks in the Note, add a leading newline to the log-line Text action
   and re-sign.

None of these deviations affect this spike's actual question (lock-vs-close automation
behavior) — they're standard Shortcuts wiring notes captured for completeness per this
project's conventions.
