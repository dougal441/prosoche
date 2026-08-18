<!-- Task 1 partial content. Expanded into the full plan summary once Tasks 2-3 complete. -->

## Schema bump — sequencing constraint

**Recorded 2026-08-18, Task 1 of this plan. This is a sequencing constraint, not a decision** —
the blocking `checkpoint:decision` that previously occupied this slot was downgraded by the
developer on 2026-08-18 because it was framed as destroying user data, and there are no users.
`docs/CAPABILITY-DECISIONS.md` BD-06-A1 Amendment 3 (the developer's own 2026-08-17 statement)
already answered the question it asked: PROSOCHĒ is a new, as-yet-undeployed product, the only
installs are the developer's own testing, and old `state.json` files are explicitly not a
consideration. That amendment discharged the identical gate on the 2 → 3 `schema_version` bump
in Phase 11, and it discharges this one the same way.

**The ordering rule.** Build and install Phase 15 BEFORE the Pressure-accumulation UAT session, never after. The `schema_version` 4 → 5 bump this plan carries (Task 2) wipes
`heat`, `gravity`, `pressure`, every rolling window, the session record, `exit_events` and every
`exit_stats[*].samples` on the developer's own iPhone at the first run of the new build. Measured
at planning time that fixture is close to empty — `07-UAT.md` observed `pressure: 0`,
`10-UAT.md` expects `pressure: 1` at the first interruption, and `.planning/STATE.md` still names
accumulating Pressure to >=2 as a step yet to be taken — so the wipe costs approximately nothing
**today**. The cost is entirely one of ordering and inverts once the accumulation session
happens: running the Pressure-accumulation UAT first and only then installing a Phase-15-bumped
build throws that session away and forces it to be repeated, and that session is the prerequisite
for roughly thirty queued tests across phases 06, 12 and 13.

**Correction to a stale premise.** Re-installing a `.shortcut` does **not** wipe `state.json` —
the two are separate files, and the shortcut re-install alone leaves accumulated state intact.
The `schema_version` bump is specifically and solely what forces the rebuild. An earlier draft of
this plan claimed the device "has to re-install for Phase 15 anyway" as though that made the wipe
incidental; it does not — the shortcut re-install and the state wipe are two independent events,
and only the schema bump causes the second one.

Plan 15-05 carries the same constraint into the device UAT instrument so whoever runs it sees the
ordering rule before touching the phone.

Execution reached Task 2 without pausing for a decision — this plan carries no decision
checkpoint and no blocking gate.
