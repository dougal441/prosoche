---
schema_version: 1
open_count: 2
waived_count: 0
fixed_count: 2
total_count: 4
last_updated: 2026-08-17T00:47:22.461Z
---

# Broken Windows Ledger

> Cross-phase defect register. `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 02 | stub | src/PROSOCHE-Dumb.xml |  | OPEN branch anchor is Comment+Nothing only; Phase 3 fills the OPEN pipeline | fixed |  | 2026-08-13T03:24:42.716Z | 2026-08-13T06:48:07.399Z |
| 2 | 02 | stub | src/PROSOCHE-Dumb.xml |  | CLOSE branch anchor is Comment+Nothing only; Phase 4 fills the CLOSE pipeline | fixed |  | 2026-08-13T03:24:42.828Z | 2026-08-13T06:48:07.512Z |
| 3 | 11 | deviation | tools/build_state_engine.py |  | Rule 2: knock() emitted comment body renamed to Pause as well as the dispatch tuple, so the retired name left the shipped artifact (plan 11-01) | open |  | 2026-08-17T00:47:19.199Z |  |
| 4 | 11 | deviation | src/CONFIG-BLOCK.md |  | Rule 1: two now-false 'unchanged from plan 01-01' provenance claims corrected after the sequences edit (plan 11-01) | open |  | 2026-08-17T00:47:22.461Z |  |

````json
[
  {
    "id": 1,
    "kind": "stub",
    "phase": "02",
    "file": "src/PROSOCHE-Dumb.xml",
    "line": null,
    "description": "OPEN branch anchor is Comment+Nothing only; Phase 3 fills the OPEN pipeline",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-08-13T03:24:42.716Z",
    "resolved_at": "2026-08-13T06:48:07.399Z"
  },
  {
    "id": 2,
    "kind": "stub",
    "phase": "02",
    "file": "src/PROSOCHE-Dumb.xml",
    "line": null,
    "description": "CLOSE branch anchor is Comment+Nothing only; Phase 4 fills the CLOSE pipeline",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-08-13T03:24:42.828Z",
    "resolved_at": "2026-08-13T06:48:07.512Z"
  },
  {
    "id": 3,
    "kind": "deviation",
    "phase": "11",
    "file": "tools/build_state_engine.py",
    "line": null,
    "description": "Rule 2: knock() emitted comment body renamed to Pause as well as the dispatch tuple, so the retired name left the shipped artifact (plan 11-01)",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-08-17T00:47:19.199Z",
    "resolved_at": null
  },
  {
    "id": 4,
    "kind": "deviation",
    "phase": "11",
    "file": "src/CONFIG-BLOCK.md",
    "line": null,
    "description": "Rule 1: two now-false 'unchanged from plan 01-01' provenance claims corrected after the sequences edit (plan 11-01)",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-08-17T00:47:22.461Z",
    "resolved_at": null
  }
]
````
