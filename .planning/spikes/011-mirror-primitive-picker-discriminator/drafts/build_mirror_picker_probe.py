#!/usr/bin/env python3
"""Build the spike-011 Mirror primitive picker discriminator probe.

ONE QUESTION.  Which of `is.workflow.actions.list`, `is.workflow.actions.getitemfromlist`
or `is.workflow.actions.speaktext` raises "Please choose a value for each parameter in
this action" -- the device-reproduced axis-4 unfilled-picker failure that follows the
Mirror primitive's own action span (`.planning/todos/pending/2026-08-18-mirror-primitive-
unfilled-picker.md`), narrowed to these three identifiers by `15-RESEARCH.md` Pitfall 4
(everything Circles 1, 3 and 9 exercised on device is exonerated).

WHY THIS SCRIPT AND NOT THE shortcut-builder AGENT.  `.planning/spikes/CONVENTIONS.md`
records the direct-authoring exception spike 007 and spike 010 both used: "when a spike's
purpose is to reproduce a byte shape under test, an agent 'corrects' the very value under
test."  Every shape below is TRANSCRIBED from `tools/build_state_engine.py`, not
re-derived -- naming the exact symbol it came from in the comment beside it:

  - `_list_row()` (generator :844) -- the two-kind WFItems row-wrapper discrimination
    (bare string vs. `{"WFItemType": 0, "WFValue": <WFTextTokenString>}`), keyed on
    attachment-bearing-ness, never on Python type.
  - `mirror_text()` (generator :917) -- the List -> Get Item From List "Item At Index"
    shape, WFItemIndex fed by the named variable "Circle Next", WFInput wired to the
    List action's own output by OutputUUID/OutputName (never through an intermediate
    Set Variable).
  - The `speaktext` call inside `voice()` (generator :1006, née `mirror_and_voice()`
    :935-961 before the phase-15-01 split) -- `WFText=variable("Mirror Text")`, which
    `normalise_string_envelopes()` rewrites into the `WFTextTokenString` single-`￼`
    envelope reproduced here directly via `token()`.

MIRROR_SUCCESSES, TRANSCRIBED VERBATIM (generator :80-91), NOT A SYNTHETIC TEN-ROW LIST.
It is the real production array that already contains BOTH row kinds `_list_row()` must
discriminate: 9 of its 10 templates carry exactly one "￼" placeholder (Circle Next
attaches to the FIRST placeholder position under `mirror_templates()`'s facts tuple,
regardless of what the surrounding prose names), and template index 7 -- "Success is
recorded too: the prior boundary was respected." -- carries NONE.  That is not a coincidence
of this probe's authoring; it is `_list_row()`'s own docstring calling out MIRROR_SUCCESSES[7]
/ MIRROR_LAPSES[7] by name as "ROW 8", the exact site where an earlier isinstance-based
discriminator shipped a double-wrapped row for four cycles before Phase 13 caught it.  Using
the real array means a leg-1 failure in THIS probe is evidence about the REAL row shipping at
Circle 8, not about a shape this probe invented.

THE COERCION ON WFItemIndex IS NOT LOCALLY DERIVABLE -- IT MUST BE TRANSCRIBED, NOT
RE-DERIVED.  In this probe, taken in isolation, "Circle Next" is fed only by
`is.workflow.actions.number` (Number-typed already), so a LOCAL run of
`normalise_numeric_operands()` would skip the coercion (`_already_numeric()` would return
True).  But in the SHIPPED artifact "Circle Next" is mixed-typed ARTIFACT-WIDE --
`manual_emergency_restore()`'s Test Circle loop assigns it from both `read_value()` (Text)
and `number()` (Number) -- so the generator's own comment at :5037-5041 records that EVERY
`getitemfromlist.WFItemIndex` site referencing "Circle Next", including this one, carries
`WFCoercionVariableAggrandizement` / `WFNumberContentItem`.  Reproducing what a local
derivation would skip and the real artifact does not skip is exactly what "transcribe, do
not re-derive" means in practice, so it is hardcoded here via `coerced()` rather than left
to a local normalisation pass this standalone probe does not run.

BREADCRUMBS A..D at base depth, `is.workflow.actions.showresult` NEVER `is.workflow.
actions.alert` -- a Show Alert modal wedges a simulator run permanently (spike 010,
`.claude/CLAUDE.md` #9).  Distinct literals per breadcrumb so a partial failure is
attributable from the screen alone (last breadcrumb reached + verbatim error text).

Run:  python3 ".planning/spikes/011-mirror-primitive-picker-discriminator/drafts/build_mirror_picker_probe.py"
"""

import pathlib
import plistlib
import uuid

DRAFTS = pathlib.Path(__file__).resolve().parent
NAME = "PROSOCHE Mirror Picker Discriminator"

# Deterministic UUIDs, same idiom as the generator (uid() :106-109) and spike 010's
# build_coercion_probe.py: a counter through uuid5 so a rebuild is byte-identical.
_COUNTER = 0


def uid():
    global _COUNTER
    _COUNTER += 1
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"prosoche-spike-011/{_COUNTER}")).upper()


# ---------------------------------------------------------------------------
# Transcribed verbatim from tools/build_state_engine.py.  Do not "improve" these.
# ---------------------------------------------------------------------------

def action(identifier: str, **parameters):                      # generator :157
    return {"WFWorkflowActionIdentifier": identifier,
            "WFWorkflowActionParameters": parameters}


def output(uuid_value: str, name: str):                         # generator :179
    return {"Value": {"OutputUUID": uuid_value, "OutputName": name,
                      "Type": "ActionOutput"},
            "WFSerializationType": "WFTextTokenAttachment"}


def variable(name: str):                                        # generator :185
    return {"Value": {"Type": "Variable", "VariableName": name},
            "WFSerializationType": "WFTextTokenAttachment"}


def token(name: str):                                           # generator :190
    """The single-`￼`-placeholder WFTextTokenString envelope speaktext.WFText takes."""
    return {"Value": {"string": "￼", "attachmentsByRange":
            {"{0, 1}": {"Type": "Variable", "VariableName": name}}},
            "WFSerializationType": "WFTextTokenString"}


def text_token(parts):                                          # generator :196
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


def comment(text: str):                                         # generator :285
    return action("is.workflow.actions.comment", WFCommentActionText=text)


def set_var(name: str, source):                                 # generator :289
    return action("is.workflow.actions.setvariable", WFInput=source, WFVariableName=name)


def number(value, name: str):                                   # generator :385
    number_id = uid()
    return [action("is.workflow.actions.number", UUID=number_id, WFNumberActionNumber=value),
            set_var(name, output(number_id, "Number"))]


def breadcrumb(label: str, message: str):
    """A run-time breadcrumb the simulator channel can actually dismiss.

    Reused idiom from spike 010's `sim_input.py`-paired probe: `Show Alert` accepts
    neither a synthesized tap on OK nor a hardware Return on this channel and wedges the
    run permanently at the first one; `Show Result` dismisses on Return, first try.
    """
    return action("is.workflow.actions.showresult",
                  Text=text_token([(f"{label} -- {message}", None)]))


# generator :5005 / :5045 -- Donor 4.1's shape, character for character.
NUMBER_COERCION = {"Type": "WFCoercionVariableAggrandizement",
                   "CoercionItemClass": "WFNumberContentItem"}


def coerced(name: str):
    """A named-variable descriptor carrying the coercion FIRST in Aggrandizements.

    `normalise_numeric_operands()` (generator :5162-5180) does exactly this:
    `existing.insert(0, dict(NUMBER_COERCION))` -- coercion goes first because golden
    332c12a0 orders it that way (the property is read from the coerced item).  Reproduced
    here directly rather than by running the pass, because -- see the module docstring --
    a LOCAL run over this probe's own 17 actions would not attach it at all: "Circle Next"
    is Number-sourced everywhere IN THIS PROBE, and only mixed-typed ARTIFACT-WIDE in the
    real shipped fork.  The site under test is the real fork's site, so its real shape is
    transcribed rather than re-derived from this probe's narrower context.
    """
    descriptor = variable(name)
    descriptor["Value"].setdefault("Aggrandizements", []).insert(0, dict(NUMBER_COERCION))
    return descriptor


def _list_row(item):                                            # generator :844-908
    """The two-kind WFItems row-wrapper discrimination, transcribed verbatim.

    A LITERAL row is a bare string.  An ATTACHMENT-BEARING row is
    {"WFItemType": 0, "WFValue": <the WFTextTokenString, unchanged>}.  Discriminated on
    attachment-bearing-ness, never on Python type -- an attachment-free WFTextTokenString
    (no "￼" placeholder, empty attachmentsByRange) collapses to its bare string, exactly
    as MIRROR_SUCCESSES[7] does below.
    """
    if isinstance(item, str):
        return item
    body = item.get("Value")
    if (isinstance(body, dict) and isinstance(body.get("string"), str)
            and not body.get("attachmentsByRange")):
        return body["string"]
    return {"WFItemType": 0, "WFValue": item}


def mirror_templates(templates):                                # generator :929-933
    facts = ("Circle Next", "Pressure Next", "Heat Final")
    return tuple(text_token([(part, facts[index] if index < len(template.split("￼")) - 1 else None)
                             for index, part in enumerate(template.split("￼"))]) for template in templates)


# MIRROR_SUCCESSES, transcribed verbatim from tools/build_state_engine.py :80-91.
# Index 7 ("Success is recorded too: the prior boundary was respected.") carries no
# placeholder -- this is the real ROW 8 _list_row()'s own docstring names.
MIRROR_SUCCESSES = (
    "A recorded boundary was kept before this Circle ￼ open.",
    "The last recorded boundary was respected; this open is Circle ￼.",
    "There is a kept boundary in the record; current Circle: ￼.",
    "The previous contract was kept. Recorded pressure is ￼.",
    "A kept boundary is part of this record; heat is ￼.",
    "The record includes a respected contract before Circle ￼.",
    "One prior boundary was kept; this run's pressure is ￼.",
    "Success is recorded too: the prior boundary was respected.",
    "The last contract was kept; the current heat is ￼.",
    "A recorded success precedes this Circle ￼ interruption.",
)


# ---------------------------------------------------------------------------
# The probe
# ---------------------------------------------------------------------------

def build():
    global _COUNTER
    _COUNTER = 0          # deterministic UUIDs
    actions = []

    # The validator requires exactly this two-comment preamble (BEST_PRACTICES.md
    # "Shortcut Building Techniques"; validate_shortcut.py :2552-2569) and separately
    # REJECTS internal parameter names anywhere in comment text, requiring Shortcuts UI
    # wording instead.  So every comment below names actions the way the editor shows
    # them; the exact plist keys live in this script's docstrings and the spike README.
    actions.append(comment(
        "SPIKE 011 -- MIRROR PRIMITIVE PICKER DISCRIMINATOR\n"
        "\n"
        "ONE question: which of List, Get Item From List, or Speak Text raises \"Please "
        "choose a value for each parameter in this action\" -- the device-reproduced "
        "failure that follows the Mirror primitive rather than any Circle index.\n"
        "\n"
        "Standalone. Reads no state file, references no production shortcut, needs no "
        "Personal Automation. No blocking alert anywhere -- every breadcrumb is a "
        "Show Result, and a partial failure is attributable from the last one reached."))

    actions.append(comment(
        "Shortcuts generated by Shortcuts Playground. May contain mistakes. Always check "
        "the shortcut's actions first.\n"
        "\n"
        "This shortcut was created via the following user prompt:\n"
        "\n"
        "> Build an alert-free probe that isolates which of three action identifiers "
        "> unique to the Mirror primitive's span -- List, Get Item From List, Speak Text "
        "> -- raises an unfilled required picker error on a real device. Reuse the "
        "> production List row-wrapper shape and the real MIRROR_SUCCESSES templates so a "
        "> failure observed here is evidence about the real Circle 8 span."))

    # --- Breadcrumb A ---
    actions.append(breadcrumb("Breadcrumb A", "probe started -- nothing has run yet."))

    # --- Set-up: Circle 8's own index, not a synthetic one ---
    actions.append(comment(
        "SET-UP.\n"
        "Number 8 -> Set Variable \"Circle Next\", so the probe exercises Circle 8's own "
        "index rather than a synthetic one. This is the same variable name mirror_text() "
        "feeds Get Item From List with in the production generator."))
    actions += number(8, "Circle Next")

    # --- Leg 1: is.workflow.actions.list ---
    actions.append(comment(
        "LEG 1 -- LIST. A List action whose Items hold MIRROR_SUCCESSES, transcribed "
        "verbatim from the generator's own array. Nine rows carry an attachment on "
        "\"Circle Next\"; row 8 (\"Success is recorded too...\") carries none and stays a "
        "bare string -- both row kinds present, exactly as the production Mirror emits "
        "them."))
    list_id = uid()
    actions.append(action("is.workflow.actions.list", UUID=list_id,
                          WFItems=[_list_row(item) for item in mirror_templates(MIRROR_SUCCESSES)]))

    # --- Breadcrumb B ---
    actions.append(breadcrumb("Breadcrumb B", "List leg done. Get Item From List is next."))

    # --- Leg 2: is.workflow.actions.getitemfromlist ---
    actions.append(comment(
        "LEG 2 -- GET ITEM FROM LIST. Item At Index, index fed by \"Circle Next\" WITH the "
        "Number coercion attached first (the real artifact-wide shape -- see this script's "
        "module docstring for why this probe's own local context would not derive it), "
        "input wired directly to the List action's own output."))
    item_id = uid()
    actions.append(action("is.workflow.actions.getitemfromlist", UUID=item_id,
                          WFItemSpecifier="Item At Index", WFItemIndex=coerced("Circle Next"),
                          WFInput=output(list_id, "List")))
    actions.append(set_var("Mirror Text", output(item_id, "Item from List")))

    # --- Breadcrumb C ---
    actions.append(breadcrumb("Breadcrumb C", "Get Item From List leg done. Speak Text is next."))

    # --- Leg 3: is.workflow.actions.speaktext ---
    actions.append(comment(
        "LEG 3 -- SPEAK TEXT. The Text field carries \"Mirror Text\" in the single-"
        "placeholder text-token envelope, the same shape the generator's string-envelope "
        "normalisation produces for a bare variable at this catalog-str parameter. No "
        "other Speak Text parameter is set -- Wait Until Finished/Rate/Pitch/Language/"
        "Voice are catalog-real but no donor shows their serialization, so they are "
        "omitted (C-1)."))
    actions.append(action("is.workflow.actions.speaktext", WFText=token("Mirror Text")))

    # --- Breadcrumb D ---
    actions.append(breadcrumb("Breadcrumb D", "Speak Text leg done. Probe complete -- no error was raised."))

    # --- Terminator: ends the run without a modal ---
    actions.append(action("is.workflow.actions.returntohomescreen"))

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


write(build(), NAME)
