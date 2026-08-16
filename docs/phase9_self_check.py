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
   coercion split across all 28 setbrightness/setvolume sites: 14
   setbrightness (all 14 coerced, Restore Brightness x4 + Dim Target x10) and
   14 setvolume (4 coerced -- Restore Volume -- and 10 correctly left
   uncoerced -- Silence Target, already Number-sourced via number()).

See 09-RESEARCH.md ("Site count correction -- 28, not 18", "Which of the 28
sites actually need the coercion") and 09-PATTERNS.md ("Table-driven
numeric-operand coercion") for the full derivation this script verifies.
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


def site_audit() -> None:
    expected_counts = {
        "is.workflow.actions.setbrightness": 14,
        "is.workflow.actions.setvolume": 14,
    }
    expected_coerced = {
        "is.workflow.actions.setbrightness": 14,  # Restore Brightness x4 + Dim Target x10
        "is.workflow.actions.setvolume": 4,        # Restore Volume x4; Silence Target x10 left uncoerced
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
    print("site_audit: passed (28/28 sites audited, 18 coerced, 10 correctly not)")


def main() -> None:
    negative_control()
    site_audit()
    print("phase9 self-check: passed")


if __name__ == "__main__":
    main()
