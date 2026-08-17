#!/usr/bin/env python3
"""Assert the spike-010 probe actually carries the shape it claims to test.

A probe that does not hold the shape under test is worse than no probe: it produces an
observation and attributes it to the wrong cause.  This script parses the BUILT XML --
not the build script, not the diff -- and fails loudly if any of the following is untrue.

  1. Exactly two Set Brightness sites exist: one coerced (leg A), one bare (leg B).
  2. Leg A's coercion is the FIRST entry in its Aggrandizements list.  The order is part
     of what is under test: Donor 7.1 action 7 and golden 332c12a0 both put the coercion
     first because the property is read from the coerced item, and the generator
     reproduces that with `existing.insert(0, ...)`.
  3. Leg A's coercion class is exactly WFNumberContentItem.  No other value may appear
     anywhere in the probe -- a second, guessed CoercionItemClass is prohibited outright
     by 16-CONTEXT.md and by .claude/CLAUDE.md's do-not-fabricate rule.
  4. Leg B carries NO aggrandizement at all.  If a build step ever "corrects" the
     control leg, the coerced leg loses its reference and the probe silently stops
     discriminating -- exactly the failure CONVENTIONS.md warns of for build agents.
  5. Both operands are text-sourced (a Get Text feeds the Set Variable that feeds them).
     A Number-sourced operand needs no coercion, so the probe would test nothing.
  6. The probe is standalone: no reference to the state file, to either production fork
     display name, or to any Personal Automation input.

Run: python3 .planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/assert_probe_shape.py
"""

import pathlib
import plistlib
import sys

DRAFTS = pathlib.Path(__file__).resolve().parent
XML = DRAFTS / "PROSOCHE Coercion Probe.xml"

root = plistlib.loads(XML.read_bytes())
actions = root["WFWorkflowActions"]
raw = XML.read_bytes().decode("utf-8")

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


# --- 1/2/3/4: the two Set Brightness sites --------------------------------------------
sites = [(i, a) for i, a in enumerate(actions)
         if a.get("WFWorkflowActionIdentifier") == "is.workflow.actions.setbrightness"]

# Leg D restores from the device read; it is a third site and is deliberately uncoerced
# because Get Device Details already yields a Number.  Separate it by variable name
# rather than by position, so a reordering cannot silently reclassify a leg.
def var_name(item):
    value = item["WFWorkflowActionParameters"].get("WFBrightness", {}).get("Value", {})
    return value.get("VariableName")


def aggrandizements(item):
    value = item["WFWorkflowActionParameters"].get("WFBrightness", {}).get("Value", {})
    return value.get("Aggrandizements", [])


by_name = {var_name(a): a for _, a in sites}
check(len(sites) == 3, f"expected 3 Set Brightness sites (A coerced, B control, D restore), found {len(sites)}")
check("Probe Coerced Target" in by_name, "leg A (coerced) Set Brightness site not found")
check("Probe Uncoerced Target" in by_name, "leg B (control) Set Brightness site not found")
check("Probe Original Brightness" in by_name, "leg D (restore) Set Brightness site not found")

if "Probe Coerced Target" in by_name:
    ag = aggrandizements(by_name["Probe Coerced Target"])
    check(bool(ag), "leg A carries no Aggrandizements at all -- the shape under test is absent")
    if ag:
        check(ag[0].get("Type") == "WFCoercionVariableAggrandizement",
              f"leg A's FIRST aggrandizement is {ag[0].get('Type')!r}, not the coercion. "
              "Order is part of what is under test.")
        check(ag[0].get("CoercionItemClass") == "WFNumberContentItem",
              f"leg A's coercion class is {ag[0].get('CoercionItemClass')!r}, not WFNumberContentItem")

if "Probe Uncoerced Target" in by_name:
    check(aggrandizements(by_name["Probe Uncoerced Target"]) == [],
          "leg B (the CONTROL) carries an aggrandizement -- it must be bare, or leg A has "
          "no reference to be read against and the probe stops discriminating")

if "Probe Original Brightness" in by_name:
    check(aggrandizements(by_name["Probe Original Brightness"]) == [],
          "leg D carries a coercion -- the generator skips already-Number-typed operands "
          "(Get Device Details), so reproducing that skip is part of reproducing the generator")

# No second CoercionItemClass may exist anywhere in the probe.
classes = set()
def walk(node):
    if isinstance(node, dict):
        if node.get("Type") == "WFCoercionVariableAggrandizement":
            classes.add(node.get("CoercionItemClass"))
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)
walk(actions)
check(classes <= {"WFNumberContentItem"},
      f"a CoercionItemClass other than WFNumberContentItem appears in the probe: {sorted(classes)}. "
      "Guessing a second class is prohibited; a red result triggers the fresh-donor protocol instead.")

# --- 5: both test operands are TEXT-sourced -------------------------------------------
text_outputs = {a["WFWorkflowActionParameters"]["UUID"]
                for a in actions
                if a.get("WFWorkflowActionIdentifier") == "is.workflow.actions.gettext"}
for name in ("Probe Coerced Target", "Probe Uncoerced Target"):
    setter = next((a for a in actions
                   if a.get("WFWorkflowActionIdentifier") == "is.workflow.actions.setvariable"
                   and a["WFWorkflowActionParameters"].get("WFVariableName") == name), None)
    check(setter is not None, f"no Set Variable assigns {name!r}")
    if setter:
        src = setter["WFWorkflowActionParameters"]["WFInput"]["Value"].get("OutputUUID")
        check(src in text_outputs,
              f"{name!r} is not fed by a Get Text action -- a Number-sourced operand needs "
              "no coercion, so the probe would be testing nothing")

# --- 6: standalone ---------------------------------------------------------------------
FORBIDDEN = ["state.json", "PROSOCHE/", "Nine Circles", "PROSOCHĒ", "ExtensionInput",
             "Shortcut Input", "Reloaded State"]
for needle in FORBIDDEN:
    check(needle not in raw,
          f"probe is not standalone: it references {needle!r}")

if failures:
    print("PROBE SHAPE ASSERTION FAILED:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print(f"probe shape asserted from the built XML ({len(actions)} actions):")
print("  leg A  coerced   -- WFCoercionVariableAggrandizement/WFNumberContentItem, FIRST in Aggrandizements")
print("  leg B  control   -- bare descriptor, no Aggrandizements")
print("  leg D  restore   -- bare descriptor (Get Device Details is already Number-typed)")
print("  both test operands are Get Text -> Set Variable sourced")
print("  no reference to the state file, either production fork, or any automation input")
