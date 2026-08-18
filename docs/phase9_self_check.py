#!/usr/bin/env python3
"""Phase 9 (RESTORE-01) self-check: negative-control + site-audit.

Two independent proofs, neither of which trusts prose:

1. negative_control() -- proves the two new NUMERIC_OPERAND_FIELDS entries
   (is.workflow.actions.setbrightness/.setvolume) are load-bearing, not
   accidentally passing. It calls the REAL production
   bse.verify_numeric_operands() against a synthetic fixture, both with the
   entries removed (must reproduce the pre-fix exemption bug: no SystemExit)
   and with them present (must now raise, then must clear once
   bse.normalise_numeric_operands() has run).
2. site_audit() -- proves the live-generated forks carry the exact expected
   coercion split across all 30 setbrightness/setvolume sites: 15
   setbrightness (all 15 coerced, Restore Brightness x4 + Dim Target x11) and
   15 setvolume (4 coerced -- Restore Volume -- and 11 correctly left
   uncoerced -- Silence Target, already Number-sourced via number()).

See 09-RESEARCH.md ("Site count correction -- 28, not 18", "Which of the 28
sites actually need the coercion") and 09-PATTERNS.md ("Table-driven
numeric-operand coercion") for the full derivation this script verifies.

PHASE 11 (plan 11-05) moved the totals 28 -> 30.  primitive_dispatch() is now
rendered ELEVEN times rather than ten: nine in the Test-a-Circle submenu, plus
TWO in universal_leaving(), where Build Addendum 01 §3 made Panic Escape -- the
`Leaving` case of the Leaving/Continue menu -- removable.  Mechanism A gates the
whole menu on the flat state field `panic_escape_enabled`; the enabled arm still
renders the dispatch inside the Continue case, and the otherwise arm renders it
directly so a user who removed the bypass reaches the intervention with no menu.
Each extra rendering adds one dimming() and one silence(), hence +1 setbrightness
and +1 setvolume.  The COERCED counts move asymmetrically and that is correct:
Dim Target is read_value()-sourced (Text) so every one of the 15 is coerced,
while Silence Target is number()-sourced (already Number-typed) so all 11 stay
deliberately uncoerced and the coerced volume count remains 4, not 5.
Both numbers here were MEASURED against the rebuilt forks, not projected.

PHASE 16 (plan 16-01) added capture_persistence_negative_control(), which proves
bse.verify_capture_persistence() load-bearing.  That guard closes the phase's P0:
dimming()/silence() captured the device's current brightness/volume into the
`State` dictionary and then changed the device, but `State` is never saved again
after the OPEN arm, so the capture never reached state.json -- every restore gate
read the cleared sentinel and skipped, and nothing in the product un-dimmed the
screen.  The fix puts one save_state() inside each APPLYING arm, before the write.

THE NEW CONTROL'S POLARITY IS INVERTED RELATIVE TO negative_control() ABOVE, and
that is deliberate rather than a copy that drifted.  negative_control() removes a
TABLE ENTRY, so its pre-fix phase asserts the guard must NOT raise (the site was
invisible).  capture_persistence_negative_control() removes an ACTION PAIR from
the emitted artifact, so its pre-fix phase asserts the guard MUST raise (the
defect is present and visible).  Read the phase comments, not the shape.

THE SITE COUNTS DID NOT MOVE, and a reader who expected them to needs the reason.
The persistence fix adds only is.workflow.actions.setitemname and
is.workflow.actions.documentpicker.save actions -- 22 of each pair per fork, one
per applying arm across 11 dimming() and 11 silence() renderings, so +44 actions
per fork (Dumb 4346 -> 4390, Sentient 4414 -> 4458).  It adds no setbrightness,
no setvolume and no getdevicedetails action, and it changes no operand's source
or coercion.  So site_audit()'s expected_counts (15/15) and expected_coerced
(15/4) are unchanged, and so is environmental_restore_check.py's EXPECTED_SITES.
That non-movement was MEASURED against the rebuilt forks after the fix, not
assumed: a move in any of those numbers would have been a regression introduced
by this phase, not a table that needed updating.
"""
from __future__ import annotations

import copy
import plistlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_state_engine as bse  # noqa: E402


NEW_ENTRIES = ("is.workflow.actions.setbrightness", "is.workflow.actions.setvolume")


def _synthetic_fixture():
    """A 3-action list reproducing a Text-sourced, uncoerced WFBrightness write.

    Mirrors how read_value() sources Dim Target/Restore Brightness/Restore
    Volume in the real generator: a bare gettext action (carrying a UUID, so
    _numeric_operand_report()'s produced-output trace can resolve it) feeds a
    named Set Variable, which is then wired -- uncoerced -- into
    is.workflow.actions.setbrightness's WFBrightness field.
    """
    text_id = bse.uid()
    return [
        bse.action("is.workflow.actions.gettext", UUID=text_id,
                   WFTextActionText="1"),
        bse.set_var("Test Brightness", bse.output(text_id, "Text")),
        bse.action("is.workflow.actions.setbrightness",
                   WFBrightness=bse.variable("Test Brightness"), ShowWhenRun=False),
    ]


def negative_control() -> None:
    actions = _synthetic_fixture()

    saved = {}
    for identifier in NEW_ENTRIES:
        if identifier in bse.NUMERIC_OPERAND_FIELDS:
            saved[identifier] = bse.NUMERIC_OPERAND_FIELDS.pop(identifier)
    try:
        # Pre-fix state: the site is invisible to the audit, so the guard must
        # NOT raise even though the operand is genuinely uncoerced and
        # Text-sourced. This reproduces the exemption bug this plan closes.
        try:
            bse.verify_numeric_operands(copy.deepcopy(actions))
        except SystemExit:
            raise AssertionError(
                "verify_numeric_operands() raised with the new table entries "
                "removed -- the negative control does not reproduce the "
                "pre-fix exemption bug, so it cannot prove the fix is "
                "load-bearing")
    finally:
        bse.NUMERIC_OPERAND_FIELDS.update(saved)

    # Post-fix state, still uncoerced: the guard must now raise.
    post_fix = copy.deepcopy(actions)
    raised = False
    try:
        bse.verify_numeric_operands(post_fix)
    except SystemExit:
        raised = True
    assert raised, (
        "verify_numeric_operands() did NOT raise with the table entries "
        "restored -- the guard is not actually load-bearing for this site")

    # Post-fix, post-normalise: the same fixture must now pass cleanly.
    bse.normalise_numeric_operands(post_fix)
    bse.verify_numeric_operands(post_fix)  # must not raise
    print("negative_control: passed")


def _strip_persisting_save(actions):
    """A deep copy of `actions` with the PHASE 16 persisting save pair removed.

    Located BY CONTENT, never by index: the pair is the setitemname whose WFName is the
    state filename immediately followed by the documentpicker.save that consumes it, sitting
    immediately before a setbrightness/setvolume.  Every action index recorded in this
    phase's research is a measurement, and the fix that this control exists to test moved
    all of them -- an index-keyed fixture would silently stop reproducing the defect.

    Returns (pre_fix_actions, removed_pair_count).  A zero count means the fixture did not
    reproduce anything and the caller must treat that as a failure, not as a pass.
    """
    pre_fix = copy.deepcopy(actions)
    removed = 0
    for index in range(len(pre_fix) - 1, -1, -1):
        item = pre_fix[index]
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.documentpicker.save":
            continue
        if index + 1 >= len(pre_fix) or index == 0:
            continue
        applies = pre_fix[index + 1].get("WFWorkflowActionIdentifier") in {
            "is.workflow.actions.setbrightness", "is.workflow.actions.setvolume"}
        namer = pre_fix[index - 1]
        names_state = (namer.get("WFWorkflowActionIdentifier") == "is.workflow.actions.setitemname"
                       and namer.get("WFWorkflowActionParameters", {}).get("WFName") == "state.json")
        if applies and names_state:
            del pre_fix[index - 1:index + 1]
            removed += 1
    return pre_fix, removed


def _nest_persisting_save(actions):
    """A deep copy of `actions` with the persisting save pair sunk one IF arm deeper.

    THE SECOND DEFECT SHAPE, added after 16-REVIEW CR-01.  _strip_persisting_save() above
    removes the pair outright; that is only the crudest way to break the invariant.  The
    subtler one -- and the one that actually got past the guard -- keeps the save in the
    artifact but moves it inside a nested conditional, so it is still emitted, still sources
    `State`, and still precedes the apply in ACTION ORDER, while sitting on a branch that
    need not run.  The old unscoped `pending.clear()` accepted that shape silently.

    Located BY CONTENT exactly as the stripper is, and built from the REAL generator output,
    so it cannot drift from what dimming()/silence() emit.  The wrapper is a real
    bse.if_block()/bse.end_if() pair, not a hand-rolled dict.

    Returns (nested_actions, nested_pair_count).  A zero count means the fixture reproduced
    nothing and the caller must treat that as a failure, not as a pass.
    """
    nested = copy.deepcopy(actions)
    count = 0
    for index in range(len(nested) - 1, -1, -1):
        item = nested[index]
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.documentpicker.save":
            continue
        if index + 1 >= len(nested) or index == 0:
            continue
        applies = nested[index + 1].get("WFWorkflowActionIdentifier") in {
            "is.workflow.actions.setbrightness", "is.workflow.actions.setvolume"}
        namer = nested[index - 1]
        names_state = (namer.get("WFWorkflowActionIdentifier") == "is.workflow.actions.setitemname"
                       and namer.get("WFWorkflowActionParameters", {}).get("WFName") == "state.json")
        if applies and names_state:
            group, opener = bse.if_block("Something Else", 2, number=0)
            nested[index - 1:index + 1] = [opener, namer, item, bse.end_if(group)]
            count += 1
    return nested, count


def capture_persistence_negative_control() -> None:
    """Prove bse.verify_capture_persistence() raises when the persisting save is removed.

    Built from the REAL generator helpers -- bse.dimming() and bse.silence() are called
    directly and their output IS the post-fix fixture, so this control can never drift from
    what the generator actually emits.  It calls the REAL production guard; a
    re-implementation here would prove only that this file agrees with itself.

    POLARITY: inverted relative to negative_control() above.  See the module docstring --
    that control removes a table entry and asserts the guard stays silent; this one removes
    the emitted save pair, which is the defect itself, and asserts the guard fires.
    """
    for name, primitive in (("dimming", bse.dimming), ("silence", bse.silence)):
        post_fix = primitive()
        pre_fix, removed = _strip_persisting_save(post_fix)
        assert removed == 1, (
            f"{name}(): expected to strip exactly one state.json save immediately preceding "
            f"a brightness/volume apply, stripped {removed} -- the fixture no longer "
            f"reproduces the pre-fix defect, so it cannot prove the guard is load-bearing")

        # Pre-fix state: the capture is written and the device is changed with nothing
        # persisted in between. The guard MUST raise.
        raised = False
        try:
            bse.verify_capture_persistence(pre_fix)
        except SystemExit:
            raised = True
        assert raised, (
            f"verify_capture_persistence() did NOT raise against {name}() with the "
            f"persisting save removed -- the negative control does not reproduce the P0 "
            f"(a capture written only into the State variable, then an apply), so it "
            f"cannot prove the guard is load-bearing")

        # Second defect shape (16-REVIEW CR-01): the save is still emitted, still sources
        # `State`, and still precedes the apply in action order -- but one IF arm deeper,
        # so it need not run on the path that reaches the apply. The guard MUST raise.
        # This is the case the unscoped pending.clear() accepted silently.
        nested, count = _nest_persisting_save(post_fix)
        assert count == 1, (
            f"{name}(): expected to sink exactly one state.json save into a nested arm, "
            f"sank {count} -- the fixture no longer reproduces the nested-save bypass")
        raised = False
        try:
            bse.verify_capture_persistence(nested)
        except SystemExit:
            raised = True
        assert raised, (
            f"verify_capture_persistence() did NOT raise against {name}() with the "
            f"persisting save sunk one arm deeper -- the arm-scoped clear is not "
            f"load-bearing, and a save on an untaken branch can again vouch for a "
            f"capture it never persisted")

        # Post-fix state: the real generator output. The same guard must stay silent.
        try:
            bse.verify_capture_persistence(copy.deepcopy(post_fix))
        except SystemExit as failure:
            raise AssertionError(
                f"verify_capture_persistence() raised against the REAL {name}() output -- "
                f"the fix and the guard disagree about where the save belongs: {failure}")
    print("capture_persistence_negative_control: passed")


def site_audit() -> None:
    # Derivation, measured after PHASE 11's eleventh primitive_dispatch() rendering
    # (see this module's docstring for why there are eleven):
    #   setbrightness = 4 restore_managed_settings() call sites + 11 dimming() renderings
    #   setvolume     = 4 restore_managed_settings() call sites + 11 silence() renderings
    # A delta larger than the rendering count explains is a regression, not a table update.
    expected_counts = {
        "is.workflow.actions.setbrightness": 15,
        "is.workflow.actions.setvolume": 15,
    }
    expected_coerced = {
        "is.workflow.actions.setbrightness": 15,  # Restore Brightness x4 + Dim Target x11
        "is.workflow.actions.setvolume": 4,        # Restore Volume x4; Silence Target x11 left uncoerced
    }
    for fork in ("Dumb", "Sentient"):
        source = ROOT / f"src/PROSOCHE-{fork}.xml"
        data = plistlib.loads(source.read_bytes())
        counts: dict[str, int] = {}
        coerced: dict[str, int] = {}
        for item in data["WFWorkflowActions"]:
            identifier = item.get("WFWorkflowActionIdentifier")
            if identifier not in expected_counts:
                continue
            counts[identifier] = counts.get(identifier, 0) + 1
            field = "WFBrightness" if "brightness" in identifier else "WFVolume"
            value = item["WFWorkflowActionParameters"].get(field)
            descriptor = value.get("Value") if isinstance(value, dict) else None
            has_coercion = isinstance(descriptor, dict) and any(
                aggrandizement.get("Type") == "WFCoercionVariableAggrandizement"
                and aggrandizement.get("CoercionItemClass") == "WFNumberContentItem"
                for aggrandizement in descriptor.get("Aggrandizements", []))
            coerced[identifier] = coerced.get(identifier, 0) + (1 if has_coercion else 0)
        for identifier, expected in expected_counts.items():
            assert counts.get(identifier) == expected, (
                f"{fork}: expected {expected} {identifier} sites, found "
                f"{counts.get(identifier)}")
        for identifier, expected in expected_coerced.items():
            assert coerced.get(identifier) == expected, (
                f"{fork}: expected {expected} coerced {identifier} sites, "
                f"found {coerced.get(identifier)}")
    print("site_audit: passed (30/30 sites audited, 19 coerced, 11 correctly not)")


def main() -> None:
    negative_control()
    capture_persistence_negative_control()
    site_audit()
    print("phase9 self-check: passed")


if __name__ == "__main__":
    main()
