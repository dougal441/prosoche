---
schema_version: 1
open_count: 0
waived_count: 0
fixed_count: 2
total_count: 2
last_updated: 2026-08-13T06:48:07.512Z
---

# Broken Windows Ledger

> Cross-phase defect register. `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 02 | stub | src/PROSOCHE-Dumb.xml |  | OPEN branch anchor is Comment+Nothing only; Phase 3 fills the OPEN pipeline | fixed |  | 2026-08-13T03:24:42.716Z | 2026-08-13T06:48:07.399Z |
| 2 | 02 | stub | src/PROSOCHE-Dumb.xml |  | CLOSE branch anchor is Comment+Nothing only; Phase 4 fills the CLOSE pipeline | fixed |  | 2026-08-13T03:24:42.828Z | 2026-08-13T06:48:07.512Z |

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
  }
]
````
