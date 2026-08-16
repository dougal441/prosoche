---
created: 2026-08-16T23:28:00.000Z
title: Device UAT — nine Circles and sequence switching (RUNNING)
area: general
severity: major
running: true
files:
  - .planning/phases/05-nine-primitives-environmental-safety/05-UAT.md
  - .planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md
  - tools/build_state_engine.py
---

## Problem

**This is a running meta todo. It does not close when a build lands — it closes when all
nine Circles have been seen to fire on a real iPhone, in all three sequences.** Update the
matrix below as evidence arrives; do not delete rows.

**Exactly one Circle has ever executed on real hardware.** Circle 1, once, build
`2026-08-15o`, reported as Pressure 0.1667 / Heat 0. That is the sum total of device
evidence for the intervention layer. Circles 2 through 9 have never run. No sequence other
than the default has ever been selected on a device. The three-sequence design
(Classic / BlackMirror / Ambient) is entirely untested.

Every Phase 5 "passed" verdict is static analysis of the generated action graph. The graph
being well-formed has repeatedly failed to predict device behaviour in this project — the
seven parameter-defect axes in `.claude/CLAUDE.md` were each discovered by a device run
after a clean validation, and each was invisible to the sweep that caught the previous one.

The nine primitives are the most **heterogeneous** code in the product. They share almost
no machinery: an alert, an accessibility intent, two Get-Device-Details capture-and-restore
loops, an Ask + Menu + persisted contract, a Home Screen call, a 30-template selector, a
speech action, and a profile-aware cooldown writer. There is no reason to expect that
Circle 1 working predicts anything about Circle 6.

**What to watch for specifically**, all with precedent in this repo:

- **Blank text.** The `WFTextTokenString` envelope defect (axis 2, 367 sites) presented
  exactly as silently-empty fields — the action fires, the copy is missing. The open
  `WFItems` List-wrapper defect is known from a screenshot to render list rows blank
  (`2026-08-15-fix-red-operator-and-list-wrapper-defects.md`).
- **Red operators.** A numeric condition on a text-typed operand renders red in the UI, is
  structurally valid in the file, and fails at runtime. **No file-level analysis can detect
  this** — inspecting the imported shortcut on device is a first-class evidence channel
  here, not a fallback.
- **Hard errors from missing state shape.** A dotted read raises if any segment is absent.
  `exit_events` is still absent from the bootstrap template
  (`2026-08-15-close-state-shape-sentinel-gaps.md`).
- **Silently doing nothing**, which is how Circle 8 was found — statically, not by testing.

## Circle matrix

Update `Device` as evidence lands. `—` = never run on hardware.

| # | Classic | Built? | Device | Blocking todo |
|---|---|---|---|---|
| 1 | Knock | yes | ✅ build `2026-08-15o`, once | — |
| 2 | Ash | **alert only** — grayscale not built | — | `build-ash-as-real-color-filters-grayscale` |
| 3 | Silence | yes; writes now live, restore untested | — | `dimming-and-silence-as-distinct-circles` |
| 4 | Confession | yes | — | — |
| 5 | Dimming | yes; writes now live, restore untested | — | `dimming-and-silence-as-distinct-circles` |
| 6 | Exile | bare Home Screen only | — | `split-exile-into-two-circles` |
| 7 | Mirror | yes | — | — |
| 8 | Voice | **dispatches nothing** | — | `build-circle-8-voice-primitive` |
| 9 | Ice | yes | — | — |

Sequence coverage: Classic `—`, BlackMirror `—`, Ambient `—`.

## Solution

Run in this order. Each stage is a real gate.

1. **Fix the instrument first.** `Test a Circle` (Control Room → menu) is the harness
   everything below depends on, and it was itself broken on device once (the `sequence`
   Set Dictionary Value error). Confirm it fires clean before trusting any result it
   produces. It copies the recorded Circle into a test variable and never writes Pressure,
   so it is safe to run repeatedly — but only if it works.
2. **Land the state-shape prerequisite.** `2026-08-15-close-state-shape-sentinel-gaps.md`
   (`exit_events`, `active_session`). Anything that records an exit will hit it.
3. **Sweep all nine, in Classic**, via `Test a Circle`. For each: does the intervention
   appear at all; is the copy correct and **non-empty**; is there a reachable dismiss/exit
   path; does control return cleanly. Record per-Circle, not as one verdict.
4. **Switch sequence and re-sweep.** Control Room → Change Sequence → BlackMirror, then
   Ambient. BlackMirror is the interesting one: it is the only sequence using combined
   entries (`Ash+Confession`, `Silence+Mirror`, `Dimming+Mirror`), which work today only
   because the dispatch match is "contains". Confirm both halves of each combined entry
   actually fire.
5. **Prove the environmental primitives as closed loops** — the `09-UAT.md` tests 2–12.
   Highest risk in the whole matrix: these writes went live at the Phase 9 merge and their
   restore path has zero device evidence. Include the ugly cases — force-quit, restart,
   CLOSE never firing, overlapping sessions, screen locked mid-session.
6. **Give Ice its own scrutiny.** It is the only Circle that leaves the user in a
   *persistent* state. Confirm: the cooldown deadline is written; a live cooldown
   short-circuits the next OPEN into the two-item menu; **Emergency Restore works from
   inside Ice**; the cooldown expires naturally and applies Heat relief; profile-aware
   durations (60 / 180 / 300 s) are correct.
7. **Then verify Pressure actually drives Circle** — not just that a Circle fires when
   asked. `Test a Circle` bypasses the arithmetic. The real question is whether repeated
   opens escalate 1 → 2 → 3 as the thresholds say. Note the known unfloored-Gravity defect
   (`open_pipeline()`, no `round_down()` on `Gravity Raw`) — the 0.1667 in the one device
   reading is exactly 1 ÷ 6 unfloored, so escalation timing is currently off-spec.

## Standing notes

- **Read the error text, not just the symptom.** Three times in the OPEN-path debug session
  a correct fix looked refuted because the surface symptom was unchanged while the
  underlying error had changed completely.
- **Fix whole classes, never site-by-site.** Every defect found in that session was
  systematic — 147, 367, 25, 20 and 8 sites respectively. Device round trips are the scarce
  resource; one class-wide fix per trip, not one site.
- **The nine slots are contested.** Three in-flight todos each want Circle positions
  (Ash rebuild, Dimming/Silence distinct, Exile split), and the roster runs to ten
  primitives for nine slots. `split-exile-into-two-circles.md` step 5 owns that decision.
  This matrix must be re-cut once it lands.

## Related

- `.planning/phases/05-nine-primitives-environmental-safety/05-UAT.md` — the per-Circle
  test list this rolls up.
- `.planning/phases/09-.../09-UAT.md` — the 12 Dimming/Silence tests; 1 of 12 passed.
- `.planning/phases/07-control-room-dumb-freeze/07-UAT.md` — owns `Test a Circle` and
  `Emergency Restore`, both of which this UAT depends on.
- `.planning/phases/04-close-pipeline-session-race/04-UAT.md` — CLOSE, where session
  duration and therefore all restore-on-close behaviour comes from. Tests 3–6 pending.
- Canonical strategy §11, §12, §21, §22, §32.
- Run via `/gsd-verify-work 5`; rolled up by `/gsd-audit-uat`.
