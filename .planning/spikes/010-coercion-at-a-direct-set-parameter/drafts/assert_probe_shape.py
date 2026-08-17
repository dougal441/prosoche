#!/usr/bin/env python3
"""Assert both spike-010 probe variants actually carry the shape they claim to test.

A probe that does not hold the shape under test is worse than no probe: it produces an
observation and attributes it to the wrong cause.  This script parses the BUILT XML --
not the build script, not the diff -- and fails loudly if any of the following is untrue.

  1. Exactly three Set Brightness sites exist: leg A coerced, leg B bare control, leg D
     bare restore.  They are identified by OPERAND NAME, not by position, so a reordering
     cannot silently reclassify a leg.
  2. Leg A's coercion is the FIRST entry in its Aggrandizements list.  The order is part
     of what is under test: Donor 7.1 action 7 and golden 332c12a0 both put the coercion
     first because the property is read from the coerced item, and the generator
     reproduces that with `existing.insert(0, ...)`.
  3. Leg A's coercion class is exactly WFNumberContentItem, and NO other CoercionItemClass
     appears anywhere in either variant.  Guessing a second class is prohibited outright
     by 16-CONTEXT.md and by .claude/CLAUDE.md's do-not-fabricate rule; this is the
     mechanical guard on that prohibition.
  4. Leg B carries NO aggrandizement at all.  If a build step ever "corrects" the control
     leg, the coerced leg loses its reference and the probe silently stops discriminating
     -- exactly the failure CONVENTIONS.md warns of for build agents.
  5. Both test operands are text-sourced (a Get Text feeds the Set Variable that feeds
     them).  A Number-sourced operand needs no coercion, so the probe would test nothing.
  6. Each probe is standalone: no reference to the state file, to either production fork
     display name, or to any Personal Automation input.
  7. THE TWO VARIANTS ARE IDENTICAL ON EVERY SET BRIGHTNESS SITE.  This is what licenses
     reading a chip in one variant and a run in the other as observations of the same
     wiring.  Without it that cross-variant claim would be prose; with it, it is checked.

Run: python3 .planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/assert_probe_shape.py
"""

import pathlib
import plistlib
import sys

DRAFTS = pathlib.Path(__file__).resolve().parent
VARIANTS = ("PROSOCHE Coercion Probe.xml",              # silent -- runnable on the simulator
            "PROSOCHE Coercion Probe Breadcrumbs.xml")  # A..D ladder -- for a device session

FORBIDDEN = ("state.json", "PROSOCHE/", "Nine Circles", "PROSOCHĒ",
             "ExtensionInput", "Shortcut Input", "Reloaded State")

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


def brightness_sites(actions):
    """Every Set Brightness action, keyed by the name of the variable feeding it."""
    sites = {}
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.setbrightness":
            continue
        value = item["WFWorkflowActionParameters"].get("WFBrightness", {}).get("Value", {})
        sites[value.get("VariableName")] = value
    return sites


def coercion_classes(node, found):
    if isinstance(node, dict):
        if node.get("Type") == "WFCoercionVariableAggrandizement":
            found.add(node.get("CoercionItemClass"))
        for value in node.values():
            coercion_classes(value, found)
    elif isinstance(node, list):
        for value in node:
            coercion_classes(value, found)
    return found


per_variant_sites = {}

for filename in VARIANTS:
    path = DRAFTS / filename
    check(path.exists(), f"{filename} was not built")
    if not path.exists():
        continue
    raw = path.read_bytes()
    actions = plistlib.loads(raw)["WFWorkflowActions"]
    text = raw.decode("utf-8")
    sites = brightness_sites(actions)
    per_variant_sites[filename] = sites

    check(len(sites) == 3,
          f"{filename}: expected 3 Set Brightness sites (A coerced, B control, D restore), "
          f"found {len(sites)}")

    a = sites.get("Probe Coerced Target")
    check(a is not None, f"{filename}: leg A (coerced) Set Brightness site not found")
    if a is not None:
        ag = a.get("Aggrandizements", [])
        check(bool(ag), f"{filename}: leg A carries no Aggrandizements -- the shape under test is absent")
        if ag:
            check(ag[0].get("Type") == "WFCoercionVariableAggrandizement",
                  f"{filename}: leg A's FIRST aggrandizement is {ag[0].get('Type')!r}, not the "
                  "coercion. Order is part of what is under test.")
            check(ag[0].get("CoercionItemClass") == "WFNumberContentItem",
                  f"{filename}: leg A's coercion class is {ag[0].get('CoercionItemClass')!r}, "
                  "not WFNumberContentItem")

    b = sites.get("Probe Uncoerced Target")
    check(b is not None, f"{filename}: leg B (control) Set Brightness site not found")
    if b is not None:
        check(b.get("Aggrandizements", []) == [],
              f"{filename}: leg B (the CONTROL) carries an aggrandizement -- it must be bare, "
              "or leg A has no reference to be read against and the probe stops discriminating")

    d = sites.get("Probe Original Brightness")
    check(d is not None, f"{filename}: leg D (restore) Set Brightness site not found")
    if d is not None:
        check(d.get("Aggrandizements", []) == [],
              f"{filename}: leg D carries a coercion -- the generator skips already-Number-typed "
              "operands (Get Device Details), so reproducing that skip is part of reproducing it")

    classes = coercion_classes(actions, set())
    check(classes <= {"WFNumberContentItem"},
          f"{filename}: a CoercionItemClass other than WFNumberContentItem appears: "
          f"{sorted(classes)}. Guessing a second class is prohibited; a red result triggers "
          "the fresh-donor protocol instead.")

    text_outputs = {item["WFWorkflowActionParameters"]["UUID"] for item in actions
                    if item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.gettext"}
    for name in ("Probe Coerced Target", "Probe Uncoerced Target"):
        setter = next((item for item in actions
                       if item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.setvariable"
                       and item["WFWorkflowActionParameters"].get("WFVariableName") == name), None)
        check(setter is not None, f"{filename}: no Set Variable assigns {name!r}")
        if setter:
            check(setter["WFWorkflowActionParameters"]["WFInput"]["Value"].get("OutputUUID")
                  in text_outputs,
                  f"{filename}: {name!r} is not fed by a Get Text action -- a Number-sourced "
                  "operand needs no coercion, so the probe would be testing nothing")

    for needle in FORBIDDEN:
        check(needle not in text, f"{filename} is not standalone: it references {needle!r}")

# 7 -- cross-variant equality on the sites that ARE the question.
if len(per_variant_sites) == len(VARIANTS):
    silent, breadcrumbs = (per_variant_sites[v] for v in VARIANTS)
    check(silent == breadcrumbs,
          "the two variants DIFFER on a Set Brightness operand descriptor. A chip observed "
          "in one and a run observed in the other would then not be observations of the same "
          "wiring, and no cross-variant conclusion could be drawn.")

if failures:
    print("PROBE SHAPE ASSERTION FAILED:")
    for failure in failures:
        print(f"  - {failure}")
    sys.exit(1)

print("probe shape asserted from the built XML, both variants:")
print("  leg A  coerced   -- WFCoercionVariableAggrandizement/WFNumberContentItem, FIRST in Aggrandizements")
print("  leg B  control   -- bare descriptor, no Aggrandizements")
print("  leg D  restore   -- bare descriptor (Get Device Details is already Number-typed)")
print("  both test operands are Get Text -> Set Variable sourced")
print("  no reference to the state file, either production fork, or any automation input")
print("  the silent and breadcrumb variants are IDENTICAL on all three Set Brightness sites")
