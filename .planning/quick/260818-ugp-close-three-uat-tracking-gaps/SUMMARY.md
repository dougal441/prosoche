---
slug: uat-tracking-gaps
status: complete
completed: 2026-08-18
---

# Summary — three UAT-tracking gaps closed

## Task 1 — `audit-uat` parser (the substantive one)

Patched `~/.claude/gsd-core/bin/lib/uat.cjs`, `parseUatItems()`. Backup at
`uat.cjs.bak-20260818`. Two independent defects, both silent under-reports:

**1a — a wrapped `expected:` dropped the whole test.** The old single contiguous
regex required `expected:` to occupy one line with `result:` on the very next.
Replaced with a per-`###`-block parser: blocks are bounded by the next numbered
heading, `expected:` may span any number of lines (including a `|` block scalar),
and `result:` is matched at line start anywhere in the block. Also accepts
letter-suffixed ids (`### 2b.`), which `(\d+)\.` rejected outright.

**1b — the `outcome:` convention was unknown to the parser.** Two UAT templates
coexist: older files use `result: pending`; newer narrative files (10, 12, 13) have
no `result:` line and end each test with a bare `outcome:` left empty until filled.
Those files reported **zero** outstanding items and looked complete. Phase 10 had no
VERIFICATION file to compensate, so it was invisible in the audit entirely. An empty
`outcome:` (labelled or not) is now surfaced as pending; a filled one is treated as
done.

### Measured before → after

| phase | before | after | truth |
|---|---:|---:|---|
| 04 | 1 | **4** | file has 4 outstanding |
| 05 | **0** | **13** | was wholly invisible |
| 06 | 4 | **15** | |
| 07 | 8 | **7** | 7 is correct *now* — several were closed this session |
| 09 | **0** | **11** | was wholly invisible |
| 10 | **0** | **6** | was wholly invisible; 6 = exactly the untested ones |
| **total** | **26** | **89** | |

Phase 04 was the clean proof of 1a: of its four outstanding tests only test 4 had a
single-line `expected:`, and test 4 was the only one the audit could see.

Also fixed three stale empty `outcome:` lines left in `10-UAT.md` by this session's
own edits, which the new parser correctly flagged as outstanding.

## Task 2 — archived the superseded Phase 06 verification

`06/VERIFICATION.md` → `06/VERIFICATION-superseded.md`, with a header stating what
superseded it and when. Phase 06 carried two verification files disagreeing
(gaps_found 1/5 vs passed 5/5); nothing marked the older one stale, so any future
`/gsd-verify-work 06` would re-raise a settled conflict.

`06-UAT.md` Test 1 — whose entire purpose was resolving that conflict — is now
recorded **pass**, with the git chronology (a03f737 → e6ea081 → 4f28084) as evidence.

## Task 3 — master outstanding list

Added `.planning/OUTSTANDING.md` for work that lives in neither a `*-UAT.md` nor a
`*-VERIFICATION.md` and so cannot be surfaced by `audit-uat`. It records the three
items missed during the device UAT because five built phases (01, 02, 03, 08, 11)
have no UAT file:

- **Phase 08** — `human_score: 0/1`; the Aware fork's real-device behaviour is
  unclaimed and the Aware artifact is not installed on the test device.
- **Phase 11** — a **failed** truth: `dimming()`/`silence()` gate on the
  `settings_snapshot` container at condition 100, the axis-7 existence-gate trap.
  Now linked to a corroborating device observation (Circle 3 ran with no visible
  effect and no error).
- **Phase 11 deferred items** — 3, one of which is now device-confirmed.

## Verification

`gsd-tools query audit-uat --raw` re-run after each change; final total **89** items
across 9 phases, with Phase 10 reporting exactly the six tests deliberately left
blank. Module load checked with `node -e "require(...)"` after each patch.

## Note on durability

The parser fix edits the installed GSD runtime, which is **global to this machine**,
not scoped to this project. A `gsd-update` may overwrite it; `/gsd-reapply-patches`
is the mechanism for re-merging, and the backup is at `uat.cjs.bak-20260818`. Worth
upstreaming — both defects are generic, not project-specific.
