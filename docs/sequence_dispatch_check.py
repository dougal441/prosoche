#!/usr/bin/env python3
"""Report which Config sequence entries dispatch nothing, and which branches nothing names.

THIS IS A REPORTING SCRIPT, NOT A GATE.  It exits 0 in every case, including when it finds
an orphan it has never seen before.  That is deliberate and is required by the ROADMAP:
Circle 8 already ships dead -- the `"Voice"` sequence entry names no emitted dispatch branch
and silently matches nothing, with no error anywhere -- and fixing it is a later phase's
work (`.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md`).  A checker
that failed on it would block this phase on a defect this phase was told not to fix.  So the
orphan is RECORDED, by name and by the Circle positions it occupies, and the run stays green.
A future phase may promote this script to a build guard once the primitive roster and the
matching strategy have settled under BD-06.

BD-06 FORWARD COMPATIBILITY, which is why this file looks more indirect than it needs to be
today.  `docs/CAPABILITY-DECISIONS.md` BD-06 Decision 5 abolishes the three combined
sequence entries (`Ash+Confession`, `Silence+Mirror`, `Dimming+Mirror`) and moves
`primitive_dispatch()` from condition code 99 ("contains") to condition code 4 ("string
is") -- exact matching, under which an unmatched entry becomes a build-time failure instead
of a silent runtime no-op.  This script must survive that change WITHOUT EDITS, so:

  * it never hard-codes a condition code as a filter.  Every mode-0 conditional testing the
    selected-primitive variable is collected, whatever code it carries.
  * it never assumes substring matching.  Each conditional's matching rule is derived from
    ITS OWN code by match_strategy(); a code neither rule recognises is reported as unknown
    semantics rather than silently treated as one of them.
  * it splits entries on the plus character unconditionally.  Splitting a name with no plus
    yields the name itself, so the same code reads today's combined entries and tomorrow's
    single-name entries with no branch.

Read-only: parses the built artifact with plistlib.  No subprocess, no rebuild.
"""
from __future__ import annotations

import json
import plistlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/PROSOCHE-Dumb.xml"

CONDITIONAL = "is.workflow.actions.conditional"

# The variable primitive_dispatch() writes the looked-up sequence entry into, and the one
# every dispatch arm tests.  A name, not a code -- see the module docstring.
SELECTED_PRIMITIVE = "Selected Primitive"

# Orphans that are known, accepted, and owned elsewhere.  Each maps to the todo that owns
# the fix.  An orphan NOT in this mapping is still reported and still exits 0, but it is
# marked as unexpected so it cannot hide among the accepted ones.
KNOWN_ORPHANS = {
    "Voice": ".planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md",
}


def match_strategy(code):
    """Resolve one conditional's own WFCondition into the matching rule IT uses.

    This is the code -> strategy resolver, and it is the only place in this file that looks
    at a condition code at all.  Both arms below dispatch on a code READ FROM A CONDITIONAL
    in the artifact; neither presumes which code the artifact will carry.  That is what lets
    this script keep working across BD-06 Decision 5's move from "contains" to "string is":
    when the generator changes, the conditionals change, and this function simply returns
    the other answer for them.

    Anything else is "unknown" -- reported, never guessed at.
    """
    if code == 99:  # "contains": the tested string need only appear inside the entry
        return "contains"
    if code == 4:   # "string is": the tested string must equal the entry exactly
        return "exact"
    return "unknown"


def resolves(tested: str, component: str, strategy: str) -> bool:
    """Does a branch testing `tested` fire for the sequence component `component`?

    Resolution is evaluated per COMPONENT rather than per whole entry.  Under exact matching
    that is the only correct reading.  Under contains matching it is the stricter of the two
    -- a component is by construction a substring of its own entry, so anything that
    resolves per component also resolves per entry -- and it is the reading BD-06 makes
    universal once combined entries are gone.
    """
    if strategy == "contains":
        return tested in component
    if strategy == "exact":
        return tested == component
    return False


def load_actions() -> list:
    return plistlib.loads(SOURCE.read_bytes())["WFWorkflowActions"]


def config_literal(actions) -> dict:
    """The Config JSON literal, located by content rather than by action index."""
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.gettext":
            continue
        value = item.get("WFWorkflowActionParameters", {}).get("WFTextActionText")
        if isinstance(value, str) and '"config_version"' in value:
            return json.loads(value)
    raise AssertionError("the Config JSON literal was not found in the artifact")


def sequence_components(config) -> dict[str, list[tuple[str, int]]]:
    """Every distinct primitive name named by any sequence, with where it is named.

    Returns component -> [(sequence name, Circle position), ...].  Circle positions are
    1-based, matching how the sequence arrays are indexed by the resolved Circle.
    """
    found: dict[str, list[tuple[str, int]]] = {}
    for sequence, entries in config.get("sequences", {}).items():
        for position, entry in enumerate(entries, start=1):
            for component in str(entry).split("+"):
                component = component.strip()
                if component:
                    found.setdefault(component, []).append((sequence, position))
    return found


def collect_dispatch_branches(actions) -> list[dict]:
    """Every mode-0 conditional that tests the selected-primitive variable.

    NO FILTERING BY CONDITION CODE.  Each record carries the code it found so the caller can
    resolve semantics per branch; excluding a branch here because its code is unfamiliar
    would make an unrecognised dispatch scheme look like an empty dispatch surface, which is
    exactly the silent failure this script exists to expose.
    """
    branches = []
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != CONDITIONAL:
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        if parameters.get("WFControlFlowMode") != 0:
            continue
        name = parameters.get("WFInput", {}).get("Variable", {}).get("Value", {}).get("VariableName")
        if name != SELECTED_PRIMITIVE:
            continue
        code = parameters.get("WFCondition")
        branches.append({"index": index, "tested": parameters.get("WFConditionalActionString"),
                         "code": code, "strategy": match_strategy(code)})
    return branches


def _positions(sites) -> str:
    return ", ".join(f"{sequence} (Circle {position})" for sequence, position in sites)


def main() -> None:
    actions = load_actions()
    components = sequence_components(config_literal(actions))
    branches = collect_dispatch_branches(actions)

    orphans, unreachable, unknown = [], [], []

    for component in sorted(components):
        if not any(resolves(branch["tested"], component, branch["strategy"])
                   for branch in branches if isinstance(branch["tested"], str)):
            orphans.append(component)

    for tested in sorted({branch["tested"] for branch in branches
                          if isinstance(branch["tested"], str)}):
        strategies = {branch["strategy"] for branch in branches if branch["tested"] == tested}
        if not any(resolves(tested, component, strategy)
                   for component in components for strategy in strategies):
            unreachable.append(tested)

    for branch in branches:
        if branch["strategy"] == "unknown":
            unknown.append(branch)

    print(f"dispatch surface: {len(branches)} branch(es) testing {SELECTED_PRIMITIVE!r}, "
          f"{len(set(b['tested'] for b in branches))} distinct name(s); "
          f"{len(components)} distinct sequence component(s)")

    print("\nORPHANS -- sequence entries that dispatch nothing:")
    if not orphans:
        print("  (none)")
    for component in orphans:
        marker = ("KNOWN OPEN DEFECT, owned by " + KNOWN_ORPHANS[component]
                  if component in KNOWN_ORPHANS else "UNEXPECTED -- not in KNOWN_ORPHANS")
        print(f"  {component}: {_positions(components[component])} -- {marker}")

    print("\nUNREACHABLE -- dispatch branches no sequence entry names:")
    if not unreachable:
        print("  (none)")
    for tested in unreachable:
        print(f"  {tested}")

    print("\nUNKNOWN MATCH SEMANTICS -- branches whose condition code neither rule knows:")
    if not unknown:
        print("  (none)")
    for branch in unknown:
        print(f"  action {branch['index']} tests {branch['tested']!r} "
              f"with condition {branch['code']!r}")

    unexpected = [component for component in orphans if component not in KNOWN_ORPHANS]
    print(f"\nsequence dispatch check: {len(orphans)} orphan(s) "
          f"({len(unexpected)} unexpected), {len(unreachable)} unreachable, "
          f"{len(unknown)} of unknown semantics -- reported, not gated")


if __name__ == "__main__":
    main()
