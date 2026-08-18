#!/usr/bin/env python3
"""Assert the built spike-011 probe XML actually carries the shape under test.

A probe that does not hold the shape it claims to test is worse than no probe: it
produces an observation and attributes it to the wrong cause. This script parses the
BUILT XML -- not the build script, not the diff -- and fails loudly if any of the
following is untrue.

  1. Exactly one is.workflow.actions.list, exactly one is.workflow.actions.getitemfromlist,
     exactly one is.workflow.actions.speaktext -- the three suspect identifiers,
     each present exactly once.
  2. At least four is.workflow.actions.showresult breadcrumbs exist, and ZERO
     is.workflow.actions.alert actions exist anywhere -- a Show Alert modal wedges a
     simulator run permanently (spike 010), so its total absence is asserted mechanically
     rather than promised in prose.
     <!-- planner-discipline-allow: is.workflow.actions.alert -->
  3. The getitemfromlist action carries WFItemSpecifier == "Item At Index", and its
     WFItemIndex operand carries an Aggrandizements entry of type
     WFCoercionVariableAggrandizement with CoercionItemClass WFNumberContentItem.
  4. The speaktext action carries WFText with WFSerializationType WFTextTokenString and a
     non-empty attachmentsByRange, and carries NO other WFSpeakText* parameter key.
  5. The WFItems array on the list action contains at least one bare-string row and at
     least one row that is a dict with a WFItemType key and a WFValue whose
     attachmentsByRange is non-empty -- both row kinds _list_row() must discriminate.

Run: python3 ".planning/spikes/011-mirror-primitive-picker-discriminator/drafts/assert_probe_shape.py"
"""

import pathlib
import plistlib
import sys

DRAFTS = pathlib.Path(__file__).resolve().parent
PROBE_XML = DRAFTS / "PROSOCHE Mirror Picker Discriminator.xml"

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


if not PROBE_XML.exists():
    print(f"PROBE SHAPE ASSERTION FAILED: {PROBE_XML} was not built")
    sys.exit(1)

actions = plistlib.loads(PROBE_XML.read_bytes())["WFWorkflowActions"]


def by_identifier(identifier):
    return [item for item in actions if item.get("WFWorkflowActionIdentifier") == identifier]


# --- 1. exactly one each of the three suspect identifiers -----------------------------
lists = by_identifier("is.workflow.actions.list")
get_items = by_identifier("is.workflow.actions.getitemfromlist")
speaks = by_identifier("is.workflow.actions.speaktext")

check(len(lists) == 1, f"expected exactly 1 is.workflow.actions.list, found {len(lists)}")
check(len(get_items) == 1, f"expected exactly 1 is.workflow.actions.getitemfromlist, found {len(get_items)}")
check(len(speaks) == 1, f"expected exactly 1 is.workflow.actions.speaktext, found {len(speaks)}")

# --- 2. >=4 breadcrumbs, ZERO blocking modals ------------------------------------------
show_results = by_identifier("is.workflow.actions.showresult")
alerts = by_identifier("is.workflow.actions.alert")  # <!-- planner-discipline-allow: is.workflow.actions.alert -->

check(len(show_results) >= 4,
      f"expected at least 4 is.workflow.actions.showresult breadcrumbs, found {len(show_results)}")
check(len(alerts) == 0,
      f"found {len(alerts)} is.workflow.actions.alert action(s) -- a Show Alert modal wedges a "
      "simulator run permanently and this probe must contain zero")

# --- 3. getitemfromlist shape -----------------------------------------------------------
if get_items:
    params = get_items[0]["WFWorkflowActionParameters"]
    check(params.get("WFItemSpecifier") == "Item At Index",
          f"getitemfromlist.WFItemSpecifier is {params.get('WFItemSpecifier')!r}, not 'Item At Index'")
    index_descriptor = params.get("WFItemIndex", {}).get("Value", {})
    aggrandizements = index_descriptor.get("Aggrandizements", [])
    coercion = next((a for a in aggrandizements
                     if a.get("Type") == "WFCoercionVariableAggrandizement"), None)
    check(coercion is not None,
          "getitemfromlist.WFItemIndex carries no WFCoercionVariableAggrandizement -- the "
          "shape under test is absent")
    if coercion is not None:
        check(coercion.get("CoercionItemClass") == "WFNumberContentItem",
              f"getitemfromlist.WFItemIndex coercion class is "
              f"{coercion.get('CoercionItemClass')!r}, not WFNumberContentItem")

# --- 4. speaktext shape ------------------------------------------------------------------
if speaks:
    params = speaks[0]["WFWorkflowActionParameters"]
    text_value = params.get("WFText", {})
    check(text_value.get("WFSerializationType") == "WFTextTokenString",
          f"speaktext.WFText WFSerializationType is "
          f"{text_value.get('WFSerializationType')!r}, not WFTextTokenString")
    attachments = text_value.get("Value", {}).get("attachmentsByRange", {})
    check(bool(attachments),
          "speaktext.WFText carries an empty attachmentsByRange -- the variable reference "
          "would resolve to nothing at runtime")
    other_speak_params = {key for key in params if key != "WFText" and key.startswith("WFSpeakText")}
    check(not other_speak_params,
          f"speaktext carries unexpected WFSpeakText* parameter(s): {sorted(other_speak_params)} "
          "-- only WFText should be present (C-1: no donor shows how the other five serialize)")

# --- 5. WFItems row-wrapper discrimination ------------------------------------------------
if lists:
    items = lists[0]["WFWorkflowActionParameters"].get("WFItems", [])
    bare_rows = [row for row in items if isinstance(row, str)]
    wrapped_rows = [row for row in items
                    if isinstance(row, dict) and "WFItemType" in row
                    and row.get("WFValue", {}).get("Value", {}).get("attachmentsByRange")]
    check(len(bare_rows) >= 1,
          f"expected at least 1 bare-string WFItems row, found {len(bare_rows)}")
    check(len(wrapped_rows) >= 1,
          f"expected at least 1 wrapped (WFItemType/WFValue) WFItems row with a non-empty "
          f"attachmentsByRange, found {len(wrapped_rows)}")

if failures:
    print("PROBE SHAPE ASSERTION FAILED:")
    for failure in failures:
        print(f"  - {failure}")
    sys.exit(1)

print("probe shape asserted from the built XML:")
print(f"  {len(lists)} list, {len(get_items)} getitemfromlist, {len(speaks)} speaktext -- each exactly 1")
print(f"  {len(show_results)} showresult breadcrumbs, {len(alerts)} alert (must be 0)")
print("  getitemfromlist: WFItemSpecifier 'Item At Index', WFItemIndex carries "
      "WFCoercionVariableAggrandizement/WFNumberContentItem")
print("  speaktext: WFText is WFTextTokenString with non-empty attachmentsByRange, no other "
      "WFSpeakText* parameter")
print(f"  WFItems: {len(bare_rows) if lists else 0} bare-string row(s), "
      f"{len(wrapped_rows) if lists else 0} wrapped row(s) with non-empty attachmentsByRange")
