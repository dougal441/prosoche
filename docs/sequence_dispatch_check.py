#!/usr/bin/env python3
"""Gate the build on which Config sequence entries dispatch nothing, and which branches nothing names.

THIS IS A GATE.  It exits non-zero on any orphan, any unreachable branch, any branch of
unknown matching semantics, and any entry matched by more than one distinct branch name.
It was written as a reporter, and it stayed one for as long as the defect it reports was
owned elsewhere; phase 11 plan 02 closed that defect and this is the promotion its own
docstring anticipated.

WHY A GATE AND NOT A REPORT.  A sequence entry that names no emitted dispatch branch is a
SILENT RUNTIME NO-OP: the Circle produces no intervention, no error and no log, the run
completes, and State is written as though the intervention had fired.  It is invisible to
`validate_shortcut.py`, which sees a structurally perfect plist; invisible to the ToolKit
catalog, which knows nothing about the value of a `WFConditionalActionString`; and invisible
to decrypting the signed artifact, which recovers the same perfect plist.  Nothing between
the generator and the user's iPhone can see it.  That is exactly how Circle 8 shipped dead
for four phases: the entry `"Voice"` named no branch and matched nothing.  Plan 11-02
retired that entry, gave Circle 8 the `"Loud Mirror"` name and a real dispatch branch, and
`KNOWN_ORPHANS` is empty as a result.

`docs/CAPABILITY-DECISIONS.md` BD-06 Decision 5 is the governing decision.  It abolishes the
three combined sequence entries (`Ash+Confession`, `Silence+Mirror`, `Dimming+Mirror`),
moves `primitive_dispatch()` from condition code 99 ("contains") to condition code 4
("string is"), and states the invariant in the form this script now enforces: every distinct
primitive name in any `sequences` array has EXACTLY ONE matching dispatch branch, and every
branch is named by at least one entry.

This script survived plan 11-02's condition-code move with no edit to its resolution logic,
and the properties that made that possible are load-bearing rather than stylistic:

  * it never hard-codes a condition code as a filter.  Every mode-0 conditional testing the
    selected-primitive variable is collected, whatever code it carries.
  * it never assumes substring matching.  Each conditional's matching rule is derived from
    ITS OWN code by match_strategy(); a code neither rule recognises is failed as unknown
    semantics rather than silently treated as one of them.
  * it splits entries on the plus character unconditionally.  Splitting a name with no plus
    yields the name itself, so the same code read the retired combined entries and reads
    today's single-name entries with no branch -- and fails on a combined entry under exact
    matching rather than mis-parsing it.

`tools/build_state_engine.py`'s `verify_dispatch_coverage()` enforces the same invariant
inside both builders, before any write.  The two are deliberate duplicates: the build guard
aborts a bad build, and this script proves the shipped artifact independently, from disk,
without importing the generator that produced it.

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

# Orphans that are known, accepted, and owned elsewhere.  Each maps to the artifact that
# owns the fix.  THE ESCAPE HATCH IS DELIBERATELY LEFT VISIBLE AND DELIBERATELY EMPTY: now
# that this script gates, a non-empty mapping is a reviewed exception that suppresses a hard
# failure, never the normal case.  Its single historical entry was the Circle-8 `"Voice"`
# orphan, closed by phase 11 plan 02.  An orphan NOT in this mapping fails the run.
KNOWN_ORPHANS = {}


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


def require(value: bool, message: str) -> None:
    """The docs/*.py failure convention: AssertionError, never SystemExit.

    SystemExit belongs to the generator's own verify_* family.  Keeping the two apart is
    what makes a traceback attributable to the right side of the build.
    """
    if not value:
        raise AssertionError(message)


def resolving_names(component: str, branches) -> set:
    """The distinct branch NAMES that fire for this sequence component.

    Distinct NAMES, never action instances.  Each branch name is legitimately rendered once
    per primitive_dispatch() rendering -- ten times in the current artifact -- so an instance
    count is not the invariant BD-06 states.  "Exactly one dispatch branch" is a statement
    about names.
    """
    return {branch["tested"] for branch in branches
            if isinstance(branch["tested"], str)
            and resolves(branch["tested"], component, branch["strategy"])}


def main() -> None:
    actions = load_actions()
    components = sequence_components(config_literal(actions))
    branches = collect_dispatch_branches(actions)

    orphans, unreachable, unknown, duplicates = [], [], [], []

    for component in sorted(components):
        matched = resolving_names(component, branches)
        if not matched:
            orphans.append(component)
        elif len(matched) > 1:
            # BD-06 says EXACTLY one.  The orphan test above is an at-least-one test, and
            # this is the half it never covered: under condition 99 the entry "Loud Mirror"
            # also matches the "Mirror" branch, so Circle 8 would silently run two
            # interventions back to back.  This is what would have caught the collision had
            # the 99 -> 4 move been forgotten.
            duplicates.append((component, sorted(matched)))

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

    print("\nDUPLICATES -- sequence entries matched by more than one distinct branch name:")
    if not duplicates:
        print("  (none)")
    for component, matched in duplicates:
        print(f"  {component}: matched by {matched}")

    unexpected = [component for component in orphans if component not in KNOWN_ORPHANS]
    print(f"\nsequence dispatch check: {len(orphans)} orphan(s) "
          f"({len(unexpected)} unexpected), {len(unreachable)} unreachable, "
          f"{len(unknown)} of unknown semantics, {len(duplicates)} duplicate(s)")

    # The gate.  Every message states the CONSEQUENCE, not merely the fact.
    require(
        not unexpected,
        f"{len(unexpected)} sequence entr(y/ies) dispatch NOTHING and are not a reviewed "
        f"exception: " + "; ".join(f"{name!r} at {_positions(components[name])}" for name in unexpected)
        + ".  An undispatched entry is a silent runtime no-op -- the Circle produces no "
        "intervention, no error and no log -- and it is invisible to validate_shortcut.py, "
        "to the ToolKit catalog and to the signed-artifact decrypt, which is how Circle 8 "
        "shipped dead for four phases.  Add the branch to primitive_dispatch()'s name tuple "
        "or correct the name in the Config literal; do not add it to KNOWN_ORPHANS to "
        "silence this",
    )
    require(
        not unreachable,
        f"{len(unreachable)} dispatch branch(es) {unreachable} are named by NO sequence "
        "entry.  Dead generated code is not harmless here: it is the signature of a "
        "half-applied rename, in which the generator tuple moved and the Config literal did "
        "not, and the matching orphan on the other side is a Circle that now dispatches "
        "nothing.  Name it in a sequence or stop emitting it",
    )
    require(
        not unknown,
        f"{len(unknown)} dispatch branch(es) carry a condition code neither 99 ('contains') "
        f"nor 4 ('string is'): "
        + "; ".join(f"action {b['index']} tests {b['tested']!r} with {b['code']!r}" for b in unknown)
        + ".  Guessing which rule applies would let this script report a clean dispatch "
        "surface it never actually checked, which is worse than no check at all",
    )
    require(
        not duplicates,
        f"{len(duplicates)} sequence entr(y/ies) match MORE THAN ONE distinct dispatch "
        f"branch: " + "; ".join(f"{name!r} matched by {matched}" for name, matched in duplicates)
        + ".  BD-06 Decision 5 requires exactly one.  Under condition 99 ('contains') a "
        "branch fires whenever its name is a substring of the entry, so the entry silently "
        "runs two interventions back to back and the user sees the wrong Circle.  Move the "
        "dispatch to condition 4 ('string is') or rename the colliding branch",
    )
    print("\nsequence dispatch check: passed")


if __name__ == "__main__":
    main()
