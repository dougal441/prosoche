#!/usr/bin/env python3
"""Gate the build on which Config sequence entries dispatch nothing, and which branches nothing names.

THIS IS A GATE.  It exits non-zero on any orphan, any unreachable branch, any branch of
unknown matching semantics, any entry matched by more than one distinct branch name, and
(PHASE 15, 15-04) any two DISTINCT entry names whose dispatch bodies are action-equal.
It was written as a reporter, and it stayed one for as long as the defect it reports was
owned elsewhere; phase 11 plan 02 closed that defect and this is the promotion its own
docstring anticipated.

PHASE 15's ADDITION IS THE GENERAL FORM OF THE DEFECT THIS FILE HAS ALWAYS EXISTED TO CLOSE.
Every check above asks whether a name has A receiver.  None of them asks whether two names
have DIFFERENT receivers.  'Mirror' and 'Loud Mirror' dispatched the identical function
(`mirror_and_voice()`) for four phases while this script, `verify_dispatch_coverage()`,
`validate_shortcut.py`, the ToolKit catalog and a decrypt of the signed container all stayed
green throughout, because a structurally perfect plist looks identical whether two branches
that share no code happen to test different names, or two branches that ARE the identical
code happen to as well.  `branch_bodies()` / `action_equal_pairs()` compare each dispatch
branch's own action span, normalised so two renderings of the SAME behaviour compare equal
and two DIFFERENT behaviours compare on content alone -- the assertion that would have
caught the original defect.

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


def _branch_end(actions, start_index: int, group_id) -> int | None:
    """The index of the mode-2 endpoint matching `group_id`, walking forward from a branch's
    own mode-0 conditional (never assuming a fixed action count between them).

    primitive_dispatch()'s per-branch shape is
    [mode-0 If, <implementation()>, mode-1 Otherwise, is.workflow.actions.nothing, mode-2 End],
    but this walk makes no assumption about what lies between the If and its own End -- it
    looks only for the End sharing the SAME GroupingIdentifier, which is what makes it
    survive an implementation whose body is longer or shorter than another's.
    """
    for index in range(start_index + 1, len(actions)):
        item = actions[index]
        parameters = item.get("WFWorkflowActionParameters", {})
        if (item.get("WFWorkflowActionIdentifier") == CONDITIONAL
                and parameters.get("WFControlFlowMode") == 2
                and parameters.get("GroupingIdentifier") == group_id):
            return index
    return None


# The three keys whose VALUES are freshly generated on every rebuild and legitimately differ
# between any two renderings of the identical behaviour: an action's own identity (UUID), a
# control-flow block's identity (GroupingIdentifier), and a reference to another action's
# output (OutputUUID).  Normalising all three to one fixed placeholder each is what turns
# "two renderings of the same function" into two byte-identical bodies, and what keeps two
# GENUINELY different bodies genuinely different -- their literal parameters, action
# identifiers and ordering are untouched.
_NORMALISED_KEYS = ("UUID", "GroupingIdentifier", "OutputUUID")


def normalise_body(node):
    """Strip every UUID, GroupingIdentifier and OutputUUID reference from an action span.

    Recurses through the whole parameter tree rather than a named slot -- the same reasoning
    tools/build_state_engine.py's _reference_descriptors() docstring gives for its own
    whole-tree walk: enumerating slots is a rename hazard, and a reference to normalise away
    can sit wherever Shortcuts permits one (a bare attachment, a WFItems row wrapper, a nested
    if_block() input), not only at the top level of WFWorkflowActionParameters.
    """
    if isinstance(node, dict):
        return {key: ("<normalised>" if key in _NORMALISED_KEYS else normalise_body(value))
                for key, value in node.items()}
    if isinstance(node, list):
        return [normalise_body(item) for item in node]
    return node


def branch_bodies(actions, branches) -> dict[str, list[str]]:
    """Every dispatch branch's normalised action span, grouped by its tested NAME.

    Each span runs from a branch's own mode-0 conditional (inclusive) to the matching mode-2
    endpoint (inclusive) sharing its GroupingIdentifier -- located by _branch_end(), which
    walks forward from the START collect_dispatch_branches() already found, rather than
    assuming a fixed action count between them.  Every UUID, GroupingIdentifier and
    OutputUUID reference is normalised away by normalise_body() before comparison, so what
    remains is BEHAVIOUR: which actions, in which order, with which literal parameters --
    never the freshly generated identifiers that legitimately differ between any two
    renderings of the identical thing.  A malformed branch (no matching mode-2 endpoint)
    RAISES rather than being silently skipped: a body that cannot be extracted cannot be
    compared, and skipping it would let this check report a name's placement clean without
    ever having looked at it.
    """
    bodies: dict[str, list[str]] = {}
    for branch in branches:
        if not isinstance(branch["tested"], str):
            continue
        start = branch["index"]
        group_id = actions[start].get("WFWorkflowActionParameters", {}).get("GroupingIdentifier")
        end = _branch_end(actions, start, group_id)
        if end is None:
            raise AssertionError(
                f"branch bodies: the dispatch branch at action {start} testing "
                f"{branch['tested']!r} has no matching mode-2 endpoint sharing its "
                "GroupingIdentifier -- the control-flow block is malformed and no body can be "
                "extracted to compare it against any other branch")
        span = actions[start:end + 1]
        bodies.setdefault(branch["tested"], []).append(json.dumps(normalise_body(span), sort_keys=True))
    return bodies


def action_equal_pairs(bodies: dict[str, list[str]]) -> list[tuple[str, str]]:
    """Every pair of DISTINCT branch names whose normalised bodies intersect.

    This is the general form of the defect this phase exists to close.  'Mirror' and 'Loud
    Mirror' dispatched the identical function for four phases while verify_dispatch_coverage(),
    validate_shortcut.py, the ToolKit catalog and a decrypt of the signed container all stayed
    green, because every one of them asks whether a name has A receiver and none asks whether
    two names have DIFFERENT receivers.  Comparing normalised bodies pairwise, across every
    combination of distinct names, is what asks that second question.

    NEGATIVE CONTROL (measured 2026-08-18, both mutations exercised in-memory against
    branch_bodies()'s real output for the shipped Core artifact rather than by mutating disk):
      (a) simulating the retarget ('Loud Mirror', voice) -> ('Loud Mirror', mirror) at the
          bodies level -- overwriting every "Loud Mirror" body with a real "Mirror" body --
          made this function return [('Loud Mirror', 'Mirror')], and passing that result to
          require() raised.  This mutation cannot be reproduced by editing
          tools/build_state_engine.py's dispatch tuple and rebuilding: that retarget is caught
          BEFORE this script ever runs, by verify_speaktext_placement() (11-01),
          verify_voice_gates() and verify_voice_path_volume_silence() (both 15-04), all of
          which halt the build before SOURCE.write_bytes() -- so the artifact this script
          reads from disk would simply never change.  Simulating the retarget at the bodies
          level is what makes this specific assertion's own teeth measurable in isolation from
          those three earlier gates;
      (b) computing bodies with NO normalisation (raw span JSON, UUIDs and
          GroupingIdentifiers intact) made every pair compare as DISTINCT, including
          'Mirror'/'Loud Mirror' -- confirming that normalisation, not the pairwise
          comparison itself, is what gives this assertion any power to catch a real collision.
    """
    names = sorted(bodies)
    return [(name_a, name_b) for index, name_a in enumerate(names) for name_b in names[index + 1:]
            if set(bodies[name_a]) & set(bodies[name_b])]


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

    # ACTION-EQUAL PAIRS.  Skip a branch of unknown matching semantics -- its span cannot be
    # trusted to be a real dispatch receiver, and the UNKNOWN MATCH SEMANTICS gate above
    # already fails the run on it, so comparing its body here would only be noise on a run
    # that is failing for a different, already-reported reason.
    bodies = branch_bodies(actions, [branch for branch in branches if branch["strategy"] != "unknown"])
    action_equal = action_equal_pairs(bodies)

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

    print("\nACTION-EQUAL PAIRS -- distinct names whose dispatch bodies are behaviourally identical:")
    if not action_equal:
        print("  (none)")
    for name_a, name_b in action_equal:
        print(f"  {name_a!r} and {name_b!r}")

    unexpected = [component for component in orphans if component not in KNOWN_ORPHANS]
    print(f"\nsequence dispatch check: {len(orphans)} orphan(s) "
          f"({len(unexpected)} unexpected), {len(unreachable)} unreachable, "
          f"{len(unknown)} of unknown semantics, {len(duplicates)} duplicate(s), "
          f"{len(action_equal)} action-equal pair(s)")

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
    # PHASE 15 (15-04).  The GENERAL form of the defect this phase exists to close: two
    # distinct sequence-entry names must not resolve to action-equal dispatch branch bodies.
    # 'Mirror' and 'Loud Mirror' dispatched the identical function for four phases while
    # every OTHER check in this file -- and verify_dispatch_coverage(), validate_shortcut.py,
    # the ToolKit catalog and a decrypt of the signed container -- stayed green throughout,
    # because every one of them asks whether a name has A receiver and none asks whether two
    # names have DIFFERENT receivers.  This is the assertion that would have caught it.
    require(
        not action_equal,
        f"{len(action_equal)} distinct sequence-entry name pair(s) resolve to ACTION-EQUAL "
        "dispatch branch bodies: "
        + "; ".join(f"{name_a!r} and {name_b!r}" for name_a, name_b in action_equal)
        + ".  A stronger Circle is replaying a weaker Circle's prompt verbatim (CIRC-14): two "
        "differently-named entries that emit byte-identical behaviour, once every UUID, "
        "GroupingIdentifier and OutputUUID reference is normalised away, are the same "
        "intervention wearing two names.  Give the stronger Circle's entry its own "
        "implementation in primitive_dispatch()'s name tuple, or accept that the two Circles "
        "are, by design, the same intervention and record that decision explicitly -- do not "
        "leave two names silently pointing at one behaviour",
    )
    print("\nsequence dispatch check: passed")


if __name__ == "__main__":
    main()
