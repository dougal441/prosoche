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

**What the probe does:** on every run it appends one JSON line to a file at
`Shortcuts/PROSOCHE/lock-signal-probe-log.jsonl` in iCloud Drive — no UI, no dialogs,
nothing to dismiss. Each line records: timestamp (`yyyy-MM-dd HH:mm:ss`), which signal
triggered the run (`OPEN`, `CLOSE`, or `MANUAL` for a bare manual run), and the live
`Device Is Locked` reading at that moment (confirmed literal per
[Spike 001](../001-device-is-locked-literal/README.md)). Readable directly from the Files
app on-device, or from a synced Mac.

**Revision history for this probe (two prior builds both failed on-device):**
1. v1 used Notes (`Create Note` + `Filter Notes`/`Append to Note`). The `Create Note`
   action's hand-synthesized `AppIntentDescriptor` came back "unknown action" on import.
2. v2 removed `Create Note` but kept `Filter Notes`/`Append to Note`; on device this
   popped the full interactive Notes picker instead of silently filtering, and nothing
   was written — a genuine broken-wiring bug, not just the known Create Note gap.
3. **v3 (current) drops Notes entirely** and logs to a fixed-path JSON-lines file instead,
   reusing this project's own already-device-verified `state.json` file-I/O pattern
   verbatim (`is.workflow.actions.documentpicker.open`/`.save`,
   `is.workflow.actions.file.createfolder`, `is.workflow.actions.setitemname`) — see
   Build Notes below for the full action list and a UUID-collision root-cause finding
   from v2.

**Setup (one-time, on the test iPhone):**
1. Delete any shortcut named "Lock Signal Probe" already in the library first — duplicate
   names silently skip on import, and you'd end up testing a stale broken build.
2. Import `Lock Signal Probe.shortcut`.
3. Run it once manually to confirm it logs a line with no crash — no permission prompts
   are expected this time (no Notes access needed).
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

## Build Notes — v3 (current, file-based) Deviations and Findings

1. **`--target-macos 26 --target-platform ios` is degenerate in the installed Playground
   version (v1.2.1)** — it rejects every action including `is.workflow.actions.comment`,
   because no iOS-26-specific ToolKit snapshot is bundled and `--target-platform ios`
   filters out the generic v63 allowlist entirely, leaving only OS-27-gated rows. This is
   a tooling artifact, not a defect in the probe. All three builds of this probe instead
   validated at `--target-macos 26` alone (passed). **Follow-up:** the project's "Exact
   validator invocation" section should be corrected — the prescribed flag pair cannot
   pass for any shortcut in this Playground version.
2. **Root cause found for v2's "missing variables" symptom.** v2's `Create Note` action's
   own `UUID` was identical to the `GroupingIdentifier` of an unrelated If block — a single
   UUID doing double duty as both an action identity and a control-flow group identity,
   exactly the collision class this project's conventions name as the #1 documented
   real-world Shortcuts mistake. Every UUID in v3 was freshly generated and verified to
   not collide with any `GroupingIdentifier`.
3. **`New Content` is built inline in each branch of the has-existing-file check**, not via
   a separate `Existing Log` variable set to an empty string in the else branch, because
   `BEST_PRACTICES.md` hard-rejects a Text action holding an empty string and the validator
   confirmed this on the first pass. Semantically identical result (true branch:
   `File + log line`; false branch: `log line` alone).
4. **Unverified at runtime: how `Device Is Locked` renders as text.** The log line leaves
   `locked:` unquoted (`"locked":￼` not `"locked":"￼"`) so the line parses as strict JSON
   if Shortcuts emits `true`/`false`. No device-verified evidence exists in this bundle for
   whether it instead emits `1`/`0` or `Yes`/`No` — check the first captured line; if it's
   not literally `true`/`false`, the line is still human-readable but not strict JSON, and
   the field would need quoting.
5. **No manual setup needed beyond import** — the `PROSOCHE` iCloud folder is created
   defensively on every run, and a missing log file returns nothing (not an error) via
   `WFFileErrorIfNotFound: false`, so a completely fresh install works with zero
   pre-existing state. This removes the Spike 002 v1/v2 requirement to pre-create a Note.

None of these deviations affect this spike's actual question (lock-vs-close automation
behavior) — they're standard Shortcuts wiring notes captured for completeness per this
project's conventions.
