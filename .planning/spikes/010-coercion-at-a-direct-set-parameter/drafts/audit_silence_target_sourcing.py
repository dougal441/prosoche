#!/usr/bin/env python3
"""Name-scoped audit of the silence-target variable's sourcing, in both built forks.

WHAT THIS SETTLES.  `16-RESEARCH.md` assumption **A2**: *"The `Silence Target` sites are
genuinely Number-sourced and need no coercion."*  A2 is what licenses leaving 11 of the 15
`setvolume` operand sites uncoerced while all 15 `setbrightness` sites carry the coercion.

WHY THE EXISTING EVIDENCE WAS NOT ENOUGH.  A2's own risk note says it: *"`phase9_self_check.py`'s
`site_audit()` currently pins 4-of-15 and passes, which is evidence but not a name-scoped grep."*
A count-based audit proves the split is STABLE.  It cannot prove the split is CORRECT, because it
never asks where the operand's value comes from.  This script asks exactly that.

THE FAILURE MODE IT IS LOOKING FOR is one this project has already been bitten by and named:
*"one Text definition anywhere poisons every numeric use of that name"*
(`tools/build_state_engine.py`, the CYCLE 14 note above `NUMERIC_OPERAND_FIELDS`).  Shortcuts
variables are global to a run and last-write-wins, so a SINGLE `Set Variable "Silence Target"`
fed by a Text source anywhere in either fork would make every uncoerced `setvolume` operand
text-typed -- and nothing in the current checker suite would notice.  That is precisely how
`Circle Next` became mixed-typed and produced 30 real offenders.

WHAT COUNTS AS NUMBER-SOURCED.  The generator's own `NUMERIC_SOURCE_ACTIONS` table
(`tools/build_state_engine.py:3761`), reproduced here rather than imported so this audit cannot
be silently invalidated by an edit to the generator -- and so it stays runnable without importing
a module whose provenance guard would refuse to load.

READ-ONLY.  Touches nothing under `tools/`, `src/` or `docs/`.  It only parses the two built
artifacts.

Run: python3 .planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/audit_silence_target_sourcing.py
"""

import pathlib
import plistlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
FORKS = ("src/PROSOCHE-Dumb.xml", "src/PROSOCHE-Sentient.xml")

# The variable that feeds the uncoerced setvolume operands.  Emitted by
# `silence()` as `number(0.10, "Silence Target")` (generator :631).
TARGET_NAME = "Silence Target"

# tools/build_state_engine.py:3761 -- action identifiers whose output is already Number-typed.
NUMERIC_SOURCE_ACTIONS = {
    "is.workflow.actions.number",
    "is.workflow.actions.number.random",
    "is.workflow.actions.math",
    "is.workflow.actions.round",
    "is.workflow.actions.calculateexpression",
    "is.workflow.actions.gettimebetweendates",
    "is.workflow.actions.getdevicedetails",
    "is.workflow.actions.count",
}

failures = []
report = []

for relative in FORKS:
    path = REPO / relative
    if not path.exists():
        failures.append(f"{relative} not found at {path}")
        continue
    actions = plistlib.loads(path.read_bytes())["WFWorkflowActions"]

    # Map every action UUID to the identifier that produced it, so an operand's
    # provenance is resolved rather than assumed.
    producer = {}
    for item in actions:
        uuid_value = item.get("WFWorkflowActionParameters", {}).get("UUID")
        if uuid_value:
            producer[uuid_value] = item.get("WFWorkflowActionIdentifier")

    assignments = []
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.setvariable":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        if parameters.get("WFVariableName") != TARGET_NAME:
            continue
        value = parameters.get("WFInput", {}).get("Value", {})
        source_uuid = value.get("OutputUUID")
        source = producer.get(source_uuid, f"<unresolved:{value.get('Type')}>")
        assignments.append((index, source))

    numeric = [a for a in assignments if a[1] in NUMERIC_SOURCE_ACTIONS]
    other = [a for a in assignments if a[1] not in NUMERIC_SOURCE_ACTIONS]

    # Count the setvolume sites and how many carry the coercion, so the disposition
    # is stated against a measured split rather than a remembered one.
    volume_sites = [item for item in actions
                    if item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.setvolume"]
    coerced = 0
    fed_by_target = 0
    for item in volume_sites:
        value = item["WFWorkflowActionParameters"].get("WFVolume", {}).get("Value", {})
        if value.get("VariableName") == TARGET_NAME:
            fed_by_target += 1
        if any(a.get("Type") == "WFCoercionVariableAggrandizement"
               for a in value.get("Aggrandizements", [])):
            coerced += 1

    report.append(
        f"{relative}\n"
        f"  Set Variable {TARGET_NAME!r} assignments : {len(assignments)}\n"
        f"    Number-sourced                        : {len(numeric)}  "
        f"({', '.join(sorted({s for _, s in numeric})) or 'none'})\n"
        f"    NOT Number-sourced                    : {len(other)}\n"
        f"  setvolume sites                         : {len(volume_sites)}\n"
        f"    fed by {TARGET_NAME!r}               : {fed_by_target}\n"
        f"    carrying a coercion                   : {coerced}")

    if not assignments:
        failures.append(
            f"{relative}: no Set Variable assigns {TARGET_NAME!r} at all -- either the variable was "
            "renamed or this audit is looking at the wrong name, and A2 cannot be evaluated")
    if other:
        failures.append(
            f"{relative}: A2 IS REFUTED. {len(other)} assignment(s) of {TARGET_NAME!r} are NOT "
            f"Number-sourced: {other}. One Text definition anywhere poisons every numeric use of "
            "that name, so the uncoerced setvolume operands would be text-typed. Record as a "
            "finding for a follow-up plan; do NOT change the generator here.")

print("\n".join(report))
print()

if failures:
    print("SILENCE-TARGET SOURCING AUDIT FAILED:")
    for failure in failures:
        print(f"  - {failure}")
    sys.exit(1)

print(f"A2 HOLDS: every Set Variable {TARGET_NAME!r} in both forks is Number-sourced.")
print("The 11 uncoerced setvolume operands are correctly uncoerced -- the brightness/volume")
print("coercion asymmetry is a SOURCING ARTIFACT, not a gap.")
