---
schema_version: 1
open_count: 2
waived_count: 0
fixed_count: 0
total_count: 2
last_updated: 2026-08-13T03:24:42.828Z
---

# Broken Windows Ledger

> Cross-phase defect register. `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 02 | stub | src/PROSOCHE-Dumb.xml |  | OPEN branch anchor is Comment+Nothing only; Phase 3 fills the OPEN pipeline | open |  | 2026-08-13T03:24:42.716Z |  |
| 2 | 02 | stub | src/PROSOCHE-Dumb.xml |  | CLOSE branch anchor is Comment+Nothing only; Phase 4 fills the CLOSE pipeline | open |  | 2026-08-13T03:24:42.828Z |  |

````json
[
  {
    "id": 1,
    "kind": "stub",
    "phase": "02",
    "file": "src/PROSOCHE-Dumb.xml",
    "line": null,
    "description": "OPEN branch anchor is Comment+Nothing only; Phase 3 fills the OPEN pipeline",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-08-13T03:24:42.716Z",
    "resolved_at": null
  },
  {
    "id": 2,
    "kind": "stub",
    "phase": "02",
    "file": "src/PROSOCHE-Dumb.xml",
    "line": null,
    "description": "CLOSE branch anchor is Comment+Nothing only; Phase 4 fills the CLOSE pipeline",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-08-13T03:24:42.828Z",
    "resolved_at": null
  }
]
````
