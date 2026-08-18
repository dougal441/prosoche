---
slug: uat-tracking-gaps
created: 2026-08-18
mode: quick
---

# Close three UAT-tracking gaps found during device UAT

## Why

The 2026-08-17/18 device UAT surfaced that the outstanding-work picture was
incomplete in three independent ways. All three are tracking defects, not
product defects — but each one hides real work.

## Task 1 — `audit-uat` silently drops tests (the important one)

`~/.claude/gsd-core/bin/lib/uat.cjs`, `parseUatItems()` matches with:

```
/###\s*(\d+)\.\s*([^\n]+)\nexpected:\s*([^\n]+)\nresult:\s*\[?(\w+)\]?/g
```

`expected:\s*([^\n]+)\nresult:` requires the `expected:` value to occupy
EXACTLY one line and `result:` to be the very next line. Any test whose
`expected:` wraps — which the UAT template's own prose style produces
constantly — fails the match and is dropped with no warning.

Measured undercount on this project:

| file | file really has | audit-uat reported |
|---|---:|---:|
| `04-UAT.md` | 4 pending | **1** |
| `06-UAT.md` | 15 pending | **4** |
| `07-UAT.md` | 16 pending | **8** |

Phase 04 is the clean proof: of tests 3–6, only test 4 has a single-line
`expected:`, and test 4 is the only one reported.

A second, smaller miss: `### 2b.` style headings fail `(\d+)\.` entirely.

**Fix:** parse per-`###`-block instead of by one rigid contiguous regex —
split the file on `###` headings, then within each block find `result:` at
line start. Keep the existing category/reason/blocked_by handling and the
`parseGapsItems` call unchanged.

**Verification:** re-run `gsd-tools query audit-uat --raw` and assert the three
counts above become 4 / 15 / 16.

## Task 2 — archive the superseded `06/VERIFICATION.md`

Phase 06 carries two verification files. `06-VERIFICATION.md` (passed, 5/5,
written 18:23:17 as a re-verify after fix `e6ea081`) supersedes the bare
`VERIFICATION.md` (gaps_found, 1/5, written 18:14:14). Nothing marks the older
one stale, so any future `/gsd-verify-work 06` re-raises a conflict that was
already settled — which is exactly what `06-UAT.md` Test 1 existed to resolve.

**Fix:** move it to `VERIFICATION-superseded.md` with a header stating what
superseded it and when, so the history is kept but the conflict cannot recur.

## Task 3 — fold Phase 08 and Phase 11 into the outstanding list

Five built phases (01, 02, 03, 08, 11) have no `*-UAT.md`, so a UAT-file-shaped
view of outstanding work cannot see them. Three items are genuinely open:

- **Phase 08** — `08-VERIFICATION.md` is `human_needed`, `automated_score:
  22/22`, `human_score: 0/1`: "real-device behavior is not claimed". The whole
  Sentient/Aware distribution surface.
- **Phase 11** — `11-VERIFICATION.md` is `gaps_found` with a FAILED truth:
  `dimming()` and `silence()` gate on the `settings_snapshot` CONTAINER at
  condition 100 — the axis-7 existence-gate trap.
- **Phase 11 `deferred-items.md`** — 3 doc/copy items.

**Fix:** record them in a single master outstanding-items file so they are
visible alongside the UAT tests.

## Done when

- `audit-uat` reports 4 / 15 / 16 for phases 04 / 06 / 07
- the superseded Phase 06 verification file can no longer be mistaken for current
- Phase 08 and Phase 11 items appear in the master outstanding list
