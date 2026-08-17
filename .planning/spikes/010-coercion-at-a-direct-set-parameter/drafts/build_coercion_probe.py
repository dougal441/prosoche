#!/usr/bin/env python3
"""Build the spike-010 coercion probe.

ONE QUESTION.  Is `WFCoercionVariableAggrandizement` / `CoercionItemClass:
WFNumberContentItem` correct at a DIRECT Set-action float parameter
(`setbrightness.WFBrightness`), as opposed to the CONDITIONAL-OPERAND position that
Donor 4.1 already confirms?

WHY THIS SCRIPT AND NOT THE shortcut-builder AGENT.  `.planning/spikes/CONVENTIONS.md`
requires delegating plist authoring to `shortcuts-playground:shortcut-builder`, AND
records the exception this probe falls squarely inside: "when a donor already gives the
exact byte shape and the spike's purpose is to *vary* it deliberately, author the plist
directly -- an agent will tend to 'correct' the very values under test (spike 007)."
Leg B is an operand DELIBERATELY missing its coercion.  That is the control, and it is
exactly the kind of value a build agent corrects on sight; correcting it would silently
destroy the only reference the coerced leg can be read against.  The shape is not
guessed either: every byte below is transcribed from `tools/build_state_engine.py`
(`variable()` :140, `set_var()` :244, `device_detail()` :441, `set_brightness()` :448,
`NUMBER_COERCION` :3755, `normalise_numeric_operands()` :3912).  Recorded as a deviation
in the spike README, per the same convention spike 007 used.

BYTE-SHAPE FIDELITY.  Leg A reproduces `restore_managed_settings()`'s
`set_brightness(variable("Restore Brightness"))` -- generator :514 -- which is the
highest-stakes production instance of this exact shape: a gettext-fed named variable
feeding WFBrightness, coerced by `normalise_numeric_operands()`.  The generator's own
docstring at :500 names it: "The operand is gettext-fed, so normalise_numeric_operands()
attaches Donor 4.1's WFCoercionVariableAggrandizement automatically."  gettext-fed is
load-bearing: a `number()`-fed operand is already Number-typed, the generator would skip
the coercion, and the probe would test nothing.

ORDERING IS A SAFETY PROPERTY, NOT A PRESENTATION CHOICE.  The device read (leg C) runs
FIRST, before either write.  Shortcuts has no try/catch, so safety comes from ordering
rather than detection (CONVENTIONS.md, and research Pattern 1: capture -> persist ->
apply).  Reading after the writes would capture 0.42 rather than the true original and
the "restore" leg would restore the probe's own test value -- a restore leg that cannot
restore.  The four legs the plan specifies are all present; they are sequenced so the
probe cannot strand the display.

DISTINCT TEST LITERALS.  Leg A writes 0.42, leg B writes 0.66.  If only one write takes
effect, an observer can tell WHICH from the screen alone.  A shared literal would make
"the uncoerced leg silently no-opped" and "both legs worked" indistinguishable -- which
is the whole discrimination the control leg exists to provide.  Both values are mid-range
and safe; neither darkens the display.

BREADCRUMBS A..D at base depth, per `.claude/CLAUDE.md`'s breadcrumb-bisection convention.
A run that halts reports as a letter, so a failure is attributable to one leg in a single
run rather than to "the probe".  They are `Show Result`, NOT `Show Alert`: a Show Alert
modal in the simulator accepts neither a synthesized tap nor a hardware Return, so the
first alert wedges the run permanently.  See `breadcrumb()` for the measurement.

Run:  python3 .planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/build_coercion_probe.py
"""

import pathlib
import plistlib
import uuid

DRAFTS = pathlib.Path(__file__).resolve().parent
NAME = "PROSOCHE Coercion Probe"

# Deterministic UUIDs, same idiom as the generator (:105-109): a counter through uuid5 so
# a rebuild is byte-identical and a diff shows only real changes.
_COUNTER = 0


def uid():
    global _COUNTER
    _COUNTER += 1
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"prosoche-spike-010/{_COUNTER}")).upper()


# ---------------------------------------------------------------------------
# Transcribed verbatim from tools/build_state_engine.py.  Do not "improve" these.
# ---------------------------------------------------------------------------

def action(identifier: str, **parameters):                      # generator :112
    return {"WFWorkflowActionIdentifier": identifier,
            "WFWorkflowActionParameters": parameters}


def output(uuid_value: str, name: str):                         # generator :134
    return {"Value": {"OutputUUID": uuid_value, "OutputName": name,
                      "Type": "ActionOutput"},
            "WFSerializationType": "WFTextTokenAttachment"}


def variable(name: str):                                        # generator :140
    return {"Value": {"Type": "Variable", "VariableName": name},
            "WFSerializationType": "WFTextTokenAttachment"}


def text_token(parts):                                          # generator :151
    string, attachments, cursor = "", {}, 0
    for literal, name in parts:
        string += literal
        cursor += len(literal)
        if name:
            attachments[f"{{{cursor}, 1}}"] = {"Type": "Variable", "VariableName": name}
            string += "￼"
            cursor += 1
    return {"Value": {"string": string, "attachmentsByRange": attachments},
            "WFSerializationType": "WFTextTokenString"}


def comment(text: str):                                         # generator :240
    return action("is.workflow.actions.comment", WFCommentActionText=text)


def set_var(name: str, source):                                 # generator :244
    return action("is.workflow.actions.setvariable", WFInput=source, WFVariableName=name)


def alert(title: str, message):                                 # generator :402
    return action("is.workflow.actions.alert", WFAlertActionTitle=title,
                  WFAlertActionMessage=message)


def breadcrumb(label: str, message: str):
    """A run-time breadcrumb the simulator channel can actually dismiss.

    MEASURED THIS SESSION, and the reason this is not `alert()`.  A `Show Alert`
    (`is.workflow.actions.alert`) modal in the simulator responds to NEITHER a synthesized
    tap on OK nor a hardware Return -- six attempts, three of each, window geometry
    verified against the display bounds.  The run wedges there permanently and the probe
    teaches nothing past its first breadcrumb.  A `Show Result` sheet dismisses on Return
    on the same channel, first try.  Regular in-app UI (the Add Shortcut button, the run
    button, list scrolling) does take synthesized taps; it is specifically the modal
    ALERT that does not.

    The distinction matters beyond this probe: the product's own `alert()` is used
    throughout both forks, so any future attempt to exercise a real fork on the simulator
    hits this wall at the first message-only degrade path.  Recorded in the spike README
    as a channel finding.
    """
    return action("is.workflow.actions.showresult",
                  Text=text_token([(f"{label} -- {message}", None)]))


def device_detail(detail: str, name: str):                      # generator :441
    detail_id = uid()
    return [action("is.workflow.actions.getdevicedetails", UUID=detail_id,
                   WFDeviceDetail=detail),
            set_var(name, output(detail_id, "Device Details"))]


def set_brightness(source):                                     # generator :448
    return action("is.workflow.actions.setbrightness", WFBrightness=source,
                  ShowWhenRun=False)


# generator :3755 -- Donor 4.1's shape, character for character.
NUMBER_COERCION = {"Type": "WFCoercionVariableAggrandizement",
                   "CoercionItemClass": "WFNumberContentItem"}


def coerced(name: str):
    """A named-variable descriptor carrying the coercion FIRST in Aggrandizements.

    `normalise_numeric_operands()` (:3926-3930) does exactly this:
    `existing.insert(0, dict(NUMBER_COERCION))`.  Coercion goes first because the
    property is read from the coerced item -- golden 332c12a0 and Donor 7.1 action 7
    both order it that way.  The insert-at-0 is reproduced literally rather than
    approximated, because the ORDER is part of what is under test.
    """
    descriptor = variable(name)
    descriptor["Value"].setdefault("Aggrandizements", []).insert(0, dict(NUMBER_COERCION))
    return descriptor


def gettext(literal: str):
    """A Text action holding a numeric literal.  Its output is TEXT-typed.

    This is what makes the probe load-bearing: the operand downstream is text-sourced,
    so the coercion is the only thing that can make it a Number.
    """
    text_id = uid()
    return text_id, action("is.workflow.actions.gettext", UUID=text_id,
                           WFTextActionText=literal)


# ---------------------------------------------------------------------------
# The probe
# ---------------------------------------------------------------------------

COERCED_TARGET = "0.42"
UNCOERCED_TARGET = "0.66"

def build(silent: bool):
    global _COUNTER
    _COUNTER = 0          # deterministic UUIDs per variant
    actions = []

        # The validator requires exactly this two-comment preamble (BEST_PRACTICES.md "Shortcut
    # Building Techniques"; validate_shortcut.py :2552-2569) and separately REJECTS internal
    # parameter names anywhere in comment text, requiring Shortcuts UI wording instead.  So
    # every comment below names actions and fields the way the editor shows them; the exact
    # plist keys live in this script's docstrings and in the spike README, which is where a
    # reader who needs them is looking anyway.
    actions.append(comment(
        "SPIKE 010 -- NUMBER COERCION AT A DIRECT SET-ACTION PARAMETER\n"
        "\n"
        "ONE question: is the Number coercion correct on a Set Brightness operand -- a\n"
        "DIRECT action parameter -- as opposed to the If-condition operand position that\n"
        "Donor 4.1 already confirms?\n"
        "\n"
        "Standalone. Reads no state file, references no production shortcut, needs no\n"
        "Personal Automation. Safe to run: it captures the current brightness BEFORE it\n"
        "writes anything, and restores it at the end.\n"
        "\n"
        "PRIMARY observation is the EDITOR, not the run: compare leg A's operand chip\n"
        "against leg B's. Leg B is deliberately uncoerced. That is the control, not a bug."))

    actions.append(comment(
        "Shortcuts generated by Shortcuts Playground. May contain mistakes. Always check "
        "the shortcut's actions first.\n"
        "\n"
        "This shortcut was created via the following user prompt:\n"
        "\n"
        "> Build an aimed probe that isolates exactly one open question: whether the Number\n"
        "> coercion this project attaches to variable operands is correct at a direct Set\n"
        "> Brightness parameter, as opposed to the If-condition operand position a donor\n"
        "> already confirms. Four legs: a coerced Set Brightness, an identical uncoerced\n"
        "> control, a Get Device Details brightness read, and a restore leg so running it\n"
        "> cannot strand the display."))

    # --- LEG C first: capture before any write. Ordering is the safety mechanism. ---
    actions.append(comment(
        "LEG C (runs FIRST) -- READ.\n"
        "Get Device Details -> Current Brightness. The detail name is donor-confirmed\n"
        "(spike 001, Donor 10), not invented. Runs before either write so leg D restores\n"
        "the TRUE original rather than the probe's own test value."))
    actions += device_detail("Current Brightness", "Probe Original Brightness")
    if not silent:
        actions.append(action("is.workflow.actions.showresult",
                              Text=text_token([("Leg C -- Current Brightness reads: ", None),
                                               ("", "Probe Original Brightness")])))

    # --- LEG A: the question under test ---
    actions.append(comment(
        "LEG A -- COERCED. THE QUESTION UNDER TEST.\n"
        "Text '0.42' -> Set Variable -> Set Brightness fed by that named variable, WITH the\n"
        "Number coercion attached first. Byte-identical to the shape the generator emits at\n"
        "the restore step -- the highest-stakes production instance of this wiring. The Text\n"
        "source is load-bearing: a Number-sourced operand would need no coercion at all, and\n"
        "the probe would be testing nothing."))
    if not silent:
        actions.append(breadcrumb("Probe A", "COERCED leg is next. Set Brightness 0.42, operand carries the Number coercion."))
    a_text_id, a_text = gettext(COERCED_TARGET)
    actions.append(a_text)
    actions.append(set_var("Probe Coerced Target", output(a_text_id, "Text")))
    actions.append(set_brightness(coerced("Probe Coerced Target")))

    # --- LEG B: the control ---
    actions.append(comment(
        "LEG B -- UNCOERCED CONTROL.\n"
        "The identical chain with NO aggrandizement. Its purpose is to show what an ABSENT\n"
        "coercion looks like in the same editor, so leg A is read against a reference rather\n"
        "than against expectation. A different literal (0.66) so an observer can tell from\n"
        "the screen alone WHICH write took effect if only one did."))
    if not silent:
        actions.append(breadcrumb("Probe B", "COERCED leg done. UNCOERCED control leg is next. Set Brightness 0.66, operand bare."))
    b_text_id, b_text = gettext(UNCOERCED_TARGET)
    actions.append(b_text)
    actions.append(set_var("Probe Uncoerced Target", output(b_text_id, "Text")))
    actions.append(set_brightness(variable("Probe Uncoerced Target")))

    # --- LEG D: restore ---
    actions.append(comment(
        "LEG D -- RESTORE.\n"
        "Put brightness back to leg C's captured value. NO coercion here, deliberately and\n"
        "correctly: Get Device Details already returns a Number, so the generator skips an\n"
        "already-Number-typed operand and leaves such a site untouched. Reproducing that\n"
        "skip is part of reproducing the generator faithfully."))
    if not silent:
        actions.append(breadcrumb("Probe C", "UNCOERCED leg done. Restore leg is next."))
    actions.append(set_brightness(variable("Probe Original Brightness")))
    if not silent:
        actions.append(breadcrumb("Probe D", "Restore done. Probe complete -- brightness is back at its original value."))

    return actions


def write(actions, name):
    root = {
        "WFWorkflowActions": actions,
        "WFWorkflowClientVersion": "2700.0.4",
        "WFWorkflowHasOutputFallback": False,
        "WFWorkflowIcon": {"WFWorkflowIconGlyphNumber": 61521,
                           "WFWorkflowIconStartColor": 4271458815},
        "WFWorkflowInputContentItemClasses": [],
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowName": name,
        "WFWorkflowOutputContentItemClasses": [],
        "WFWorkflowTypes": [],
    }
    out = DRAFTS / f"{name}.xml"
    out.write_bytes(plistlib.dumps(root, fmt=plistlib.FMT_XML, sort_keys=False))
    print(f"wrote {out} ({len(actions)} actions)")
    return out


# TWO VARIANTS, ONE SOURCE OF TRUTH.  The Set Brightness actions -- the entire question
# under test -- are emitted by the SAME code path in both, so a chip observed in one and
# a run observed in the other are observations of the same wiring.  `assert_probe_shape.py`
# checks both files, so that claim is asserted rather than asserted-in-prose.
#
#   SILENT   -- no Show Result, no Show Alert, nothing that blocks.  This is the variant
#               the simulator can actually run end to end, because modal run-time UI on
#               that channel accepts neither a synthesized tap nor a hardware Return (see
#               `breadcrumb()`).  With no blocking UI the RUN ITSELF is the signal: a
#               clean completion means every Set Brightness accepted its operand; a
#               rejection surfaces as an error naming the offending action.
#   BREADCRUMB -- the A..D ladder, for a future DEVICE session where a human taps. There
#               the breadcrumbs are worth their cost, because a halt reports as a letter.
#
# Keeping both is the point: the instrument a simulator needs and the instrument a device
# needs are genuinely different, and discovering that was itself a channel finding.
write(build(silent=True), NAME)
write(build(silent=False), f"{NAME} Breadcrumbs")
