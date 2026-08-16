---
status: diagnosed
trigger: "i don't have a reliable indicator of experiencing a circle (which indicates OPEN or CLOSE ran. i think we need to move to get that up and running first, which would be Ship-readiness cleanup for PROSOCHĒ Dumb (post OPEN-path closure) from todo. remove trace breadcrumbs, then i see Leaving / Continue menu which is confusing. not sure what's going on?"
created: 2026-08-16T19:00:00.000Z
updated: 2026-08-16T19:40:00.000Z
---

## Current Focus

hypothesis: CONFIRMED (see Resolution)
test: n/a — diagnosis complete, goal is find_root_cause_only
expecting: n/a
next_action: return ROOT CAUSE FOUND to caller

## Symptoms

expected: A user manually testing OPEN/CLOSE behavior on-device should be able to tell,
  without ambiguity, whether OPEN fired, whether CLOSE fired, and roughly what state
  resulted (e.g., which Circle, if any) — without needing hidden debug breadcrumbs.
actual: User reported no reliable indicator of a Circle/OPEN/CLOSE firing once debug
  breadcrumbs are considered for removal, and encountered a confusing "Leaving /
  Continue" menu popup mid-test with no explanation of what it signified.
errors: No error dialog — ambiguous/confusing UI feedback only.
reproduction: Perform OPEN/CLOSE cycles on device and attempt to determine, from the UI
  alone (no breadcrumb inspection), whether OPEN/CLOSE fired and what happened.
started: Discovered during Phase 04 UAT (close-pipeline-session-race), 2026-08-16. Blocks
  3 skipped UAT tests (G-04-4b gap).

## Eliminated

(none — converged directly on root cause via code tracing, no false hypotheses tested)

## Evidence

- timestamp: 2026-08-16T19:05:00.000Z
  checked: .planning/todos/pending/2026-08-15-ship-readiness-cleanup.md
  found: Item 1 / Solution step 1 proposes to strip `BUILD_STAMP`, `ROUTER_TRACE`,
    `OPEN_BISECT`, and "the ten breadcrumb alerts" from tools/build_state_engine.py, with
    no replacement observability mechanism specified anywhere in the todo's Solution
    section (5 steps total — cleanup, .gitignore, MANIFEST refresh, one-tap Control Room
    check, brightness/volume MVP cut — none mention adding a permanent confirmation
    signal).
  implication: if executed exactly as scoped, this todo removes the only currently
    unconditional, primitive-independent on-device confirmation that OPEN progressed to
    the end of its pipeline (breadcrumb J), without replacing it with anything.

- timestamp: 2026-08-16T19:10:00.000Z
  checked: tools/build_state_engine.py lines 21-43, 387-398
  found: `OPEN_BISECT = True` (line 34) gates `breadcrumb()` (line 387), which emits a
    bare `alert(BISECT_TITLE, "{letter}\n\nReport the LAST letter you see.")` — ten of
    these (A-J) fire sequentially through open_pipeline(). Comment at line 33 states
    explicitly: "Set False to strip every breadcrumb; nothing else depends on them."
    Confirms breadcrumbs are self-contained debug scaffolding with zero product logic
    depending on them — consistent with the ship-readiness todo's plan to strip them
    outright.
  implication: breadcrumbs are correctly identified as debug-only and safe to remove in
    isolation — the actual problem is not that removal is wrong, but that nothing
    permanent takes their place as a confirmation signal.

- timestamp: 2026-08-16T19:15:00.000Z
  checked: tools/build_state_engine.py lines 969-1138 (open_pipeline), specifically
    breadcrumb "J" (line 1135) immediately followed by `save_state() + universal_leaving()`
    (line 1137)
  found: breadcrumb J is the LAST breadcrumb, firing right before `universal_leaving()`
    — i.e. right before the "Leaving/Continue" menu and the Circle's primitive dispatch.
    Once breadcrumbs are stripped, the very next thing the user sees after a successful
    OPEN is the bare menu itself, with zero interstitial signal.
  implication: breadcrumb J is currently functioning as the de-facto "OPEN pipeline
    completed successfully" confirmation the user relies on — its removal is precisely
    what triggers the "no reliable indicator" symptom.

- timestamp: 2026-08-16T19:18:00.000Z
  checked: tools/build_state_engine.py lines 915-920 (`universal_leaving()`)
  found: `menu(group, 0, prompt="PROSOCHĒ", items=["Leaving", "Continue"])` — the outer
    menu's prompt is the bare string "PROSOCHĒ", with no explanatory copy about what
    "Leaving" or "Continue" do, what Circle is active, or that this menu is part of the
    OPEN path specifically. This is a PERMANENT, intentional product feature (the Phase 6
    dismissal/choice-architecture primitive mandated by canonical strategy §6.4 — "the
    single strongest mechanism is giving the user an easy option to dismiss the
    consumption attempt"), NOT a debug artifact, and is untouched by the ship-readiness
    cleanup todo.
  implication: the "Leaving/Continue" menu is real and intentional, but its confusing
    presentation (no context, no state disclosure, no indication it's OPEN-only) is a
    genuine, separate UX defect independent of the breadcrumb-removal issue.

- timestamp: 2026-08-16T19:20:00.000Z
  checked: grep for `universal_leaving(` call sites (whole file)
  found: called exactly once, at line 1137, inside `open_pipeline()` only. It is never
    called from `close_pipeline()`.
  implication: the "Leaving/Continue" menu ONLY ever appears as a result of an OPEN, never
    a CLOSE. The user's confusion ("it kind of looks like it gets open, and gets close
    (because i get a menu popup)") is a direct consequence of nothing in the UI disclosing
    this — the menu looks the same regardless of which app-tracking event preceded it, and
    CLOSE produces no comparable popup at all (see next finding), so the user reasonably
    but incorrectly attributed the popup to CLOSE.

- timestamp: 2026-08-16T19:25:00.000Z
  checked: tools/build_state_engine.py lines 1141-1218 (`close_pipeline()`), full read
  found: close_pipeline() contains exactly one conditional `alert("Contract", "Overrun
    seconds: ...")` (line 1212-1214), and it only fires when `Declared Duration > 0` —
    i.e. only when the user made a Confession-primitive contract declaring a time
    boundary during that session. In the common case (a session with no declared
    contract, e.g. every test the user ran on "pre-Circles test hardware"), close_pipeline
    runs entirely silently: reads state, delays 0.5s, reloads, checks session ownership,
    computes duration, appends the session record, clears active_session, restores
    settings, saves — zero alerts, zero notifications, zero visible signal of any kind.
    No `breadcrumb()` calls exist anywhere in close_pipeline (confirmed via grep across
    the whole file — all ten breadcrumb call sites are inside open_pipeline, lines
    976-1135).
  implication: CLOSE currently has NO on-device confirmation signal at all outside the
    rare declared-contract-overrun path — worse than OPEN, which at least has the
    (debug-only, soon-to-be-removed) breadcrumbs plus a primitive-dependent alert. This is
    the direct cause of UAT Test 3/4's "doesnt look like the session id has changed...
    it's also hard to tell" report.

- timestamp: 2026-08-16T19:30:00.000Z
  checked: tools/build_state_engine.py primitive implementations — knock() (512-518),
    ash() (521-525), confession() (528-551), dimming() (570-589), silence() (592-612),
    exile() (615-619), mirror_and_voice() (639-664), ice_start() (667-676)
  found: on-device confirmation of "a Circle fired" is entirely dependent on which
    primitive the active sequence config selects for that Circle:
    - knock(): alerts "Circle N · pressure P · heat H" — clear, always fires.
    - mirror_and_voice(): alerts templated text embedding Circle/Pressure/Heat facts —
      clear, always fires (plus optional speech).
    - ash(): alerts a generic "Pause. Put the phone down for one breath." — fires, but
      names no Circle/state, indistinguishable from any other Ash firing.
    - dimming() / silence(): fire an alert ONLY on the failure path ("could not be
      captured, so nothing was changed"); on the normal success path they change
      brightness/volume with ZERO visible confirmation.
    - exile() / ice_start(): silently call Return to Home Screen (ice_start additionally
      writes a cooldown) — the user is ejected from the app with no message at all.
    - confession(): shows an Ask-for-Input prompt and a boundary-choice menu — visible,
      but is itself the interaction, not a confirmation that a Circle fired.
  implication: even leaving breadcrumbs untouched, roughly half of the nine primitives
    (Ash generically, Dimming/Silence silently, Exile/Ice silently) give the user no way
    to confirm a Circle intervened, or which one. Knock/Mirror are the only two primitives
    that are self-confirming. This is a structural gap in the product's confirmation
    design, not merely a side effect of debug-scaffolding removal.

- timestamp: 2026-08-16T19:33:00.000Z
  checked: grep for `is.workflow.actions.notification` / `shownotification` / `show.result`
    across tools/build_state_engine.py
  found: zero matches. Every user-visible signal in the entire generator is implemented
    via `alert()` (`is.workflow.actions.alert`, a blocking modal dialog) — no lightweight,
    non-blocking Notification action is used anywhere.
  implication: there is no existing lightweight confirmation primitive to reuse; a fix
    would either add a new (currently absent from the generator, though VERIFIED
    available per this project's own capability audit — Notification is a standard,
    long-standing first-party Shortcuts action) permanent Notification-style action, or
    accept the blocking-alert cost of extending `alert()` usage to every close_pipeline
    exit and every silent-primitive path.

## Resolution

root_cause: "Two related, independently-diagnosable causes: (1) [product/process, category:
  config/design] The 'Ship-readiness cleanup' todo (2026-08-15-ship-readiness-cleanup.md,
  item 1 / Solution step 1) proposes to strip OPEN_BISECT/ROUTER_TRACE/BUILD_STAMP
  breadcrumb scaffolding from tools/build_state_engine.py with no replacement
  observability mechanism specified in its Solution section, and breadcrumb J
  (tools/build_state_engine.py:1135) is currently functioning as the de-facto
  'OPEN pipeline completed' signal the user relies on — executing the todo as scoped
  would leave OPEN with a confirmation signal that only fires for 2 of 9 primitives
  (Knock, Mirror/Voice; see knock()/mirror_and_voice()) and would leave CLOSE
  (tools/build_state_engine.py close_pipeline(), 1141-1218) with ZERO on-device
  confirmation in the common no-declared-contract case, since it has never had
  breadcrumbs or any unconditional alert to begin with. (2) [code/UX, category: code] The
  'Leaving / Continue' menu the user found confusing is a real, permanent, intentional
  Phase-6 dismissal-choice feature (universal_leaving(), tools/build_state_engine.py:
  915-920), not a debug artifact — its bare prompt ('PROSOCHĒ', items ['Leaving',
  'Continue'], no explanatory copy, no Circle/state disclosure, no indication it is
  OPEN-only) makes it genuinely ambiguous, and because it is called only from
  open_pipeline() (never close_pipeline()) while CLOSE produces no comparable popup, the
  user reasonably misread the OPEN-only menu as a signal of CLOSE having fired. AND-gate:
  both causes are independently sufficient to explain part of the reported confusion (the
  todo-scoping gap explains 'no indicator once breadcrumbs go'; the bare menu copy
  explains 'confusing popup, not sure what it indicates') and both must be addressed for
  the full symptom to resolve — fixing only one leaves the other complaint live."
fix: (not applied — find_root_cause_only mode; no code changes made)
verification: (not applicable — diagnosis only)
files_changed: []
