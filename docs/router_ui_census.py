#!/usr/bin/env python3
"""Census every user-facing surface by router arm, and enforce the Circle-0 silent band.

Two jobs in one script:

1. A REPORT.  It prints how many menus, prompts, alerts, notifications, lists, spoken
   lines, Note-showings, Note-searches and Note-creations live in each of the router's
   three arms (OPEN / CLOSE / MANUAL).  That inventory is the thing nobody could state
   from memory during the Phase 10 UX pass, and it is cheap to keep true.

2. A GATE.  It asserts the invariants that 10-01 and 10-02 established:
   the CLOSE arm shows no menu, the OPEN arm emits no notification, the Control Room Note
   opens only on request, and -- the point of this file -- every user-facing action on the
   OPEN path is enclosed by the Circle-0 silent-band conditional.

Read-only.  It parses the built artifact with plistlib and imports the generator only for
its structural enclosure walker.  It never shells out and never rebuilds
src/PROSOCHE-Dumb.xml.
"""
from __future__ import annotations

import plistlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/PROSOCHE-Dumb.xml"
sys.path.insert(0, str(ROOT / "tools"))

# enclosing_groups() is 10-01's single-pass GroupingIdentifier stack walk.  Importing it
# rather than copying it keeps one definition of "what encloses what"; a copy here would be
# free to drift from the build guard that uses the original.
from build_state_engine import enclosing_groups  # noqa: E402


CONDITIONAL = "is.workflow.actions.conditional"
MENU = "is.workflow.actions.choosefrommenu"
NOTIFICATION = "is.workflow.actions.notification"
SHOWNOTE = "is.workflow.actions.shownote"
FIND_NOTES = "is.workflow.actions.filter.notes"
CREATE_NOTE = "com.apple.mobilenotes.SharingExtension"

# Every identifier that can put something in front of the user.  Order is the print order.
# choosefrommenu is counted only at WFControlFlowMode 0: modes 1 and 2 are the case and end
# markers of a menu already counted, not separate surfaces.
COUNTED = (MENU, "is.workflow.actions.ask", "is.workflow.actions.alert", NOTIFICATION,
           "is.workflow.actions.choosefromlist", "is.workflow.actions.speaktext",
           SHOWNOTE, FIND_NOTES, CREATE_NOTE)

ARMS = ("OPEN", "CLOSE", "MANUAL")


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def _parameters(item) -> dict:
    return item.get("WFWorkflowActionParameters", {})


def _tested_variable(item) -> str | None:
    """The variable name a mode-0 conditional tests, or None."""
    if item.get("WFWorkflowActionIdentifier") != CONDITIONAL:
        return None
    parameters = _parameters(item)
    if parameters.get("WFControlFlowMode") != 0:
        return None
    return parameters.get("WFInput", {}).get("Variable", {}).get("Value", {}).get("VariableName")


def _flow_endpoint(actions, group: str, mode: int) -> int:
    """Index of one endpoint of a named control-flow block, by GroupingIdentifier."""
    for index, item in enumerate(actions):
        if _parameters(item).get("GroupingIdentifier") == group \
                and _parameters(item).get("WFControlFlowMode") == mode:
            return index
    raise AssertionError(f"control-flow group {group} has no mode-{mode} endpoint")


def gate_groups(actions, variable_name: str, *, numeric_above_zero: bool = False) -> set:
    """GroupingIdentifiers of every mode-0 conditional testing `variable_name`.

    With numeric_above_zero, restrict to the project's standard "> 0" numeric shape
    (WFCondition 2, WFNumberValue 0) rather than any test on that name.
    """
    found = set()
    for item in actions:
        if _tested_variable(item) != variable_name:
            continue
        parameters = _parameters(item)
        if numeric_above_zero and not (parameters.get("WFCondition") == 2
                                       and parameters.get("WFNumberValue") == 0):
            continue
        found.add(parameters.get("GroupingIdentifier"))
    return found


def router_arms(actions) -> dict[str, tuple[int, int]]:
    """The three arm spans, derived from control-flow structure, never from action indices.

    The router is built by restructure_router() as:

        If  Input Key is OPEN      -> OPEN arm
        Otherwise                  -> If Input Key is CLOSE  -> CLOSE arm
                                      Otherwise              -> MANUAL arm

    So the OPEN arm is (first Input Key conditional, its Otherwise), the CLOSE arm is the
    same for the second, and the MANUAL arm is (the second's Otherwise, its End If).
    Every boundary comes from a GroupingIdentifier lookup, so a rebuild that shifts every
    index leaves this correct.
    """
    tests = [(index, _parameters(item).get("WFConditionalActionString"))
             for index, item in enumerate(actions) if _tested_variable(item) == "Input Key"]
    located = {literal: index for index, literal in tests if isinstance(literal, str)}
    for literal in ("OPEN", "CLOSE"):
        require(literal in located,
                f"no conditional tests Input Key against the {literal} literal -- the router "
                "has been restructured and this census can no longer locate its arms; fix "
                "the derivation rather than letting the census silently report nothing")
    open_index, close_index = located["OPEN"], located["CLOSE"]
    open_group = _parameters(actions[open_index])["GroupingIdentifier"]
    close_group = _parameters(actions[close_index])["GroupingIdentifier"]
    return {
        "OPEN": (open_index + 1, _flow_endpoint(actions, open_group, 1)),
        "CLOSE": (close_index + 1, _flow_endpoint(actions, close_group, 1)),
        "MANUAL": (_flow_endpoint(actions, close_group, 1) + 1,
                   _flow_endpoint(actions, close_group, 2)),
    }


def counted_identifier(item) -> str | None:
    """The counted identifier for this action, or None if it is not a user-facing surface."""
    identifier = item.get("WFWorkflowActionIdentifier")
    if identifier not in COUNTED:
        return None
    if identifier == MENU and _parameters(item).get("WFControlFlowMode") != 0:
        return None
    return identifier


def census(actions, arms) -> dict[str, dict[str, int]]:
    table = {arm: dict.fromkeys(COUNTED, 0) for arm in ARMS}
    for arm, (start, end) in arms.items():
        for index in range(start, end):
            identifier = counted_identifier(actions[index])
            if identifier:
                table[arm][identifier] += 1
    return table


def nearest_comment(actions, index: int) -> str:
    """The first line of the nearest preceding comment, for naming an offender in words."""
    for candidate in range(index, -1, -1):
        if actions[candidate].get("WFWorkflowActionIdentifier") == "is.workflow.actions.comment":
            text = _parameters(actions[candidate]).get("WFCommentActionText", "")
            return text.splitlines()[0] if text else ""
    return "<no preceding comment>"


def live_cooldown_arm(actions) -> tuple[int, int] | None:
    """The span of the live-cooldown short-circuit's TRUE arm, or None if it is gone.

    EXEMPTION, deliberate and by construction -- see the silent-band assertion below.
    install_cooldown_branches() puts live_ice_redirect() in the true arm of the conditional
    testing `Cooldown Until`.  That block runs BEFORE any Heat/Pressure/Circle arithmetic:
    an unexpired cooldown routes the run away without ever computing `Circle Next`, so the
    silent band does not exist yet on that path and cannot enclose anything there.  Its one
    surface -- the "Ice is active" menu offering Return Home or Emergency Restore -- is also
    the only way to reach Emergency Restore during a cooldown, so suppressing it would
    strand a user who was left dim or silent.  Located by the tested variable name, the same
    way install_cooldown_branches() locates it, never by index.
    """
    for index, item in enumerate(actions):
        if _tested_variable(item) != "Cooldown Until":
            continue
        group = _parameters(item)["GroupingIdentifier"]
        return index, _flow_endpoint(actions, group, 1)
    return None


def print_census(table) -> None:
    width = max(len(identifier) for identifier in COUNTED)
    print(f"{'identifier'.ljust(width)}  " + "  ".join(arm.rjust(6) for arm in ARMS))
    for identifier in COUNTED:
        row = "  ".join(str(table[arm][identifier]).rjust(6) for arm in ARMS)
        print(f"{identifier.ljust(width)}  {row}")


def main() -> None:
    actions = plistlib.loads(SOURCE.read_bytes())["WFWorkflowActions"]
    arms = router_arms(actions)
    table = census(actions, arms)
    print_census(table)

    # The standing evidence for the reported "a menu appeared on close" symptom: whatever
    # the user saw, it did not come from the CLOSE arm, because the CLOSE arm asks nothing.
    for identifier in (MENU, "is.workflow.actions.ask", "is.workflow.actions.choosefromlist"):
        require(table["CLOSE"][identifier] == 0,
                f"the CLOSE arm contains {table['CLOSE'][identifier]} {identifier} action(s); "
                "a genuine CLOSE must complete the session without asking the user anything")

    # 10-01 deleted the unconditional OPEN notification.  The CLOSE confirmation survives,
    # and it is the only notification in the artifact.
    require(table["OPEN"][NOTIFICATION] == 0,
            f"the OPEN arm emits {table['OPEN'][NOTIFICATION]} notification(s); no OPEN of "
            "any kind may produce a Circle/pressure/heat banner")
    total = sum(1 for item in actions if item.get("WFWorkflowActionIdentifier") == NOTIFICATION)
    require(total == 1, f"expected exactly one notification in the artifact, found {total}")
    require(table["CLOSE"][NOTIFICATION] == 1,
            "the single notification is not in the CLOSE arm; it is the session-closed "
            "confirmation and belongs nowhere else")

    # The Control Room block: found or created on every manual run (BOOT-08 self-heal),
    # shown only on request (10-02).
    for identifier in (SHOWNOTE, FIND_NOTES, CREATE_NOTE):
        require(table["MANUAL"][identifier] == 1,
                f"expected exactly one {identifier} in the MANUAL arm, found "
                f"{table['MANUAL'][identifier]}")

    # THE CIRCLE-0 SILENT BAND.  This assertion exists so that no future phase can
    # reintroduce a surface into the silent band unnoticed.  "Circle 0 shows nothing at all"
    # is a PRODUCT invariant -- an open below the profile's entry threshold is recorded and
    # never remarked on -- not an implementation detail of where a conditional happens to
    # sit.  Its value collapses the moment one dialog escapes the band, and nothing else in
    # the suite would notice: verify_circle_zero_silence() pins the Leaving/Continue menu
    # and the dotted sequences read, which is the crash-safety half, but a stray alert
    # emitted beside them would break the product property while passing every build guard.
    silent = gate_groups(actions, "Circle Next", numeric_above_zero=True)
    require(silent, "no 'Circle Next > 0' conditional exists; the silent band is gone")
    enclosure = enclosing_groups(actions)
    cooldown = live_cooldown_arm(actions)
    offenders = []
    for index in range(*arms["OPEN"]):
        identifier = counted_identifier(actions[index])
        if not identifier:
            continue
        if cooldown and cooldown[0] <= index < cooldown[1]:
            continue  # the live-cooldown short-circuit; see live_cooldown_arm()
        if not set(enclosure[index]) & silent:
            offenders.append(f"{identifier} near {nearest_comment(actions, index)!r}")
    require(not offenders,
            "OPEN-arm surface(s) outside the Circle-0 silent band, so a Circle-0 open would "
            "show something: " + "; ".join(offenders))

    # Restated from docs/phase7_self_check.py so this census is self-contained as the
    # regression guard for the whole UX pass rather than half of one.
    gate = gate_groups(actions, "Manual Show Note Requested")
    require(gate, "no conditional tests 'Manual Show Note Requested'")
    for index in range(*arms["MANUAL"]):
        if actions[index].get("WFWorkflowActionIdentifier") != SHOWNOTE:
            continue
        require(set(enclosure[index]) & gate,
                "the Control Room Show Note is not enclosed by a 'Manual Show Note "
                "Requested' conditional, so every manual menu item would launch Notes")

    # DELIBERATELY NOT ASSERTED: absolute surface counts for the OPEN or MANUAL arms beyond
    # those above.  The MANUAL arm legitimately carries dozens of structurally duplicated
    # alerts because the Test-a-Circle submenu renders the full primitive dispatch nine
    # times; pinning that number would turn every future primitive edit into a check failure
    # for no safety gain.  The counts are printed so a reader can see them, not asserted.
    print("router UI census: passed")


if __name__ == "__main__":
    main()
