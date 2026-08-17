#!/usr/bin/env python3
"""Build the Sentient shortcut as an additive, repeatable Dumb fork."""
from __future__ import annotations

import hashlib
import os
import plistlib
import tempfile
import uuid
from pathlib import Path

from plist_text_edit import find_action, replace_in_token
from build_state_engine import (
    normalise_numeric_operands,
    normalise_output_names,
    normalise_string_envelopes,
    verify_active_session_seed,
    verify_capture_persistence,
    verify_compound_value_reads,
    verify_conditional_action_string,
    verify_conditional_inputs,
    verify_dispatch_coverage,
    verify_exit_events_seed,
    verify_list_item_wrappers,
    verify_no_removed_snapshot_leaf_reads,
    verify_numeric_operands,
    verify_output_names,
    verify_panic_escape_seed,
    verify_pending_exit_seed,
    verify_required_pickers,
    verify_restore_gates,
    verify_router_shape,
    verify_sentinel_gates,
    verify_state_seed,
    verify_string_envelopes,
)

SOURCE = Path("src/PROSOCHE-Dumb.xml")
TARGET = Path("src/PROSOCHE-Sentient.xml")
MODEL = "Apple Intelligence on Device"  # direct device-export evidence
MARKER = "--- SENTIENT CONTRACT AUDIT ---"

# The two canonical display names, phase 11 plan 06.  The source FILENAMES deliberately
# still read `Dumb`/`Sentient`: renaming them is pure churn across ten code files and some
# seventy planning documents, it breaks every historical plan's reproducibility, and the
# addendum renames the PRODUCTS, not the sources.  `docs/BUILD-NOTES.md` §25 records that.
CORE_NAME = "PROSOCHĒ — Nine Circles — Core"
AWARE_NAME = "PROSOCHĒ — Nine Circles — Aware"


def uid(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"prosoche/sentient/{name}")).upper()


def action(identifier: str, **parameters):
    return {"WFWorkflowActionIdentifier": identifier, "WFWorkflowActionParameters": parameters}


def output(id_: str, name: str):
    return {"Value": {"OutputUUID": id_, "OutputName": name, "Type": "ActionOutput"},
            "WFSerializationType": "WFTextTokenAttachment"}


def variable(name: str):
    return {"Value": {"Type": "Variable", "VariableName": name},
            "WFSerializationType": "WFTextTokenAttachment"}


def token(name: str):
    return {"Value": {"string": "\ufffc", "attachmentsByRange": {"{0, 1}": {"Type": "Variable", "VariableName": name}}},
            "WFSerializationType": "WFTextTokenString"}


def text(parts: list[tuple[str, str | None]]):
    string, ranges, offset = "", {}, 0
    for literal, name in parts:
        string += literal
        offset += len(literal)
        if name:
            ranges[f"{{{offset}, 1}}"] = {"Type": "Variable", "VariableName": name}
            string += "\ufffc"
            offset += 1
    return {"Value": {"string": string, "attachmentsByRange": ranges}, "WFSerializationType": "WFTextTokenString"}


def comment(value: str):
    return action("is.workflow.actions.comment", WFCommentActionText=value)


def set_var(name: str, value):
    return action("is.workflow.actions.setvariable", WFInput=value, WFVariableName=name)


def if_block(name: str, condition: int, *, number=None, string=None, key="if"):
    group = uid(key)
    params = {"GroupingIdentifier": group, "WFControlFlowMode": 0, "WFCondition": condition,
              "WFInput": {"Type": "Variable", "Variable": variable(name)}}
    if number is not None:
        params["WFNumberValue"] = number
    if string is not None:
        params["WFConditionalActionString"] = string
    return group, action("is.workflow.actions.conditional", **params)


def otherwise(group: str):
    return action("is.workflow.actions.conditional", GroupingIdentifier=group, WFControlFlowMode=1)


def end(group: str):
    return action("is.workflow.actions.conditional", GroupingIdentifier=group, WFControlFlowMode=2)


def audit_block():
    """One optional advisory call. Every non-ALLOW branch continues Dumb."""
    before, model, after, elapsed, matches, count, first, revision, scope, prior = (uid(x) for x in (
        "before", "model", "after", "elapsed", "matches", "count", "first", "revision", "scope", "prior"))
    enabled_g, enabled = if_block("Import AI", 4, string="yes", key="enabled")
    min_g, minimum = if_block("Circle Next", 3, number=2, key="circle-min")
    max_g, maximum = if_block("Circle Next", 0, number=9, key="circle-max")
    fast_g, fast = if_block("Audit Seconds", 1, number=8, key="fast")
    found_g, found = if_block("Audit Match Count", 2, number=0, key="found")
    challenge_g, challenge = if_block("Audit Token", 99, string="CHALLENGE", key="challenge")
    deny_g, deny = if_block("Audit Token", 99, string="DENY", key="deny")
    high_g, high = if_block("Circle Next", 3, number=7, key="deny-high")
    bounded_g, bounded = if_block("Circle Next", 3, number=4, key="scope-bounded")
    consistency_g, consistency = if_block("Circle Next", 3, number=7, key="scope-consistency")
    return [
        comment(MARKER + "\n\n- Audit only a voluntary contract after Confession and before its existing Dumb save.\n- The model receives compact recorded facts, never the Note or app contents.\n- Empty, malformed, or completed-slow output continues the unchanged Dumb path."),
        comment("AI preference gate:\n- A no response keeps this run entirely Dumb.\n- Only an explicit yes reaches the optional audit."), enabled,
        comment("Circle gate:\n- Circle I remains deterministic.\n- Only Circle II and above may reach the audit."), minimum,
        comment("Circle ceiling:\n- Circle IX remains deterministic Ice.\n- Only Circles II through VIII may reach the audit."), maximum,
        action("is.workflow.actions.gettext", UUID=scope, WFTextActionText="specificity"),
        set_var("Audit Scope", output(scope, "Text")),
        action("is.workflow.actions.gettext", UUID=prior, WFTextActionText="not supplied at this Circle"),
        set_var("Audit Prior Fact", output(prior, "Text")),
        comment("Progressive audit scope:\n- Circles II–III assess specificity only.\n- Circles IV–VI add boundedness.\n- Circles VII–VIII additionally receive the recorded prior-contract result."), bounded,
        action("is.workflow.actions.gettext", UUID=uid("scope-bounded-text"), WFTextActionText="specificity and boundedness"),
        set_var("Audit Scope", output(uid("scope-bounded-text"), "Text")),
        end(bounded_g),
        comment("High-circle consistency gate:\n- Only Circles VII–VIII receive the existing Previous Respected fact.\n- Lower circles never receive that history."), consistency,
        action("is.workflow.actions.gettext", UUID=uid("scope-consistency-text"), WFTextActionText="specificity, boundedness, and recorded consistency"),
        set_var("Audit Scope", output(uid("scope-consistency-text"), "Text")),
        set_var("Audit Prior Fact", variable("Previous Respected")),
        end(consistency_g),
        action("is.workflow.actions.date", UUID=before, WFDateActionMode="Current Date"),
        set_var("Audit Before", output(before, "Date")),
        action("is.workflow.actions.askllm", UUID=model,
               WFLLMModel=MODEL, WFGenerativeResultType="Text",
               WFLLMPrompt=text([(
                   "You are a bounded contract auditor. Return exactly one first token: ALLOW, CHALLENGE, or DENY. ", None),
                   ("ALLOW a clearly bounded deliberate leisure choice. Audit only this scope: ", None), ("", "Audit Scope"), (". ", None),
                   ("Never claim lying, diagnosis, addiction, morality, feelings, or knowledge of app contents. Do not prescribe settings, arithmetic, timers, exits, or Ice.\n", None),
                   ("Intention: ", "Confession Intention"), ("\nBoundary minutes: ", "Declared Boundary Minutes"),
                   ("\nCircle: ", "Circle Next"), ("\nHeat: ", "Heat Final"), ("\nOpen count: ", "Opens Today Next"), ("\nPrior respected: ", "Audit Prior Fact"),
               ])),
        action("is.workflow.actions.date", UUID=after, WFDateActionMode="Current Date"),
        set_var("Audit After", output(after, "Date")),
        action("is.workflow.actions.gettimebetweendates", UUID=elapsed, WFInput=text([("", None), ("", "Audit After")]),
               WFTimeUntilFromDate=text([("", None), ("", "Audit Before")]), WFTimeUntilUnit="Seconds"),
        set_var("Audit Seconds", output(elapsed, "Time Between Dates")),
        comment("Completed latency gate:\n- Use the dates immediately around Use Model.\n- A result over eight seconds takes the Dumb path."), fast,
        action("is.workflow.actions.text.match", UUID=matches, text=output(model, "Model Result"),
               WFMatchTextPattern=r"(?i)^\s*(ALLOW|CHALLENGE|DENY)\b"),
        action("is.workflow.actions.count", UUID=count, WFCountType="Items",
               WFInput=output(matches, "Matches"), Input=output(matches, "Matches")),
        set_var("Audit Match Count", output(count, "Count")),
        comment("Parsed-token gate:\n- Only a matched first token is considered.\n- Empty or malformed output takes the Dumb path."), found,
        action("is.workflow.actions.getitemfromlist", UUID=first, WFItemSpecifier="First Item", WFInput=output(matches, "Matches")),
        set_var("Audit Token", output(first, "Item from List")),
        comment("Challenge branch:\n- CHALLENGE may ask once for revision or continuation.\n- The revision does not create another model call."), challenge,
        comment("One optional revision only:\n- The user may revise or continue the contract once.\n- This response is never sent to the model again."),
        action("is.workflow.actions.ask", UUID=revision, WFAskActionPrompt="Revise or continue your boundary? (optional)", WFInputType="Text"),
        set_var("Confession Intention", output(revision, "Provided Input")), otherwise(challenge_g),
        comment("Deny branch:\n- Only a DENY token may redirect.\n- Lower circles continue Dumb without punishment."), deny,
        comment("High-circle gate:\n- DENY redirects only at Circle VII or VIII.\n- It cannot alter deterministic state."), high,
        comment("High-circle DENY redirects without punishment:\n- Use the already offered Leaving route or return home.\n- No settings, arithmetic, timer, Ice, or exit selection changes here."),
        action("is.workflow.actions.returntohomescreen"),
        action("is.workflow.actions.exit"), otherwise(high_g), action("is.workflow.actions.nothing"), end(high_g),
        otherwise(deny_g), action("is.workflow.actions.nothing"), end(deny_g),
        end(challenge_g), end(found_g), otherwise(fast_g), action("is.workflow.actions.nothing"), end(fast_g),
        end(max_g), end(min_g), end(enabled_g),
        comment("--- SENTIENT CONTRACT AUDIT END ---"),
    ]


def token_string(item):
    """The `{string, attachmentsByRange}` body of a `WFTextActionText` token, or None.

    The bootstrap seed and the Note body are both `WFTextTokenString` DICTS, not plain
    `str` -- the opposite envelope from the Config literal, which is a bare string with no
    placeholders at all.  A plain-`str` filter here would silently match neither.
    """
    value = item.get("WFWorkflowActionParameters", {}).get("WFTextActionText")
    if isinstance(value, dict):
        body = value.get("Value", value)
        if isinstance(body, dict) and isinstance(body.get("string"), str):
            return body
    return None


def fix_fork_strings(actions) -> None:
    """The FIRST deliberate content divergence between the two forks (phase 11 plan 06).

    Until this function existed, `build_sentient.py` made exactly three kinds of change to
    the forked source -- icon and import question, `WFWorkflowName`, and the audit-block
    insertion -- and touched neither the Note body nor the `"fork"` seed.  The measured
    consequence: the Aware fork's Control Room Note instructed its users to select the
    OTHER fork's shortcut, in BOTH automation steps, and reported the other fork's label in
    its settings block.  A signed `.shortcut` carries no display name inside it, so the
    filename is the library entry's name and the user's two Personal Automations reference
    it by that name -- an Aware build whose Note names the Core shortcut is a SILENTLY DEAD
    INSTALL for every Aware user.  Fixing it therefore cannot be deferred to copy review.

    Three sites, each with an expected occurrence count, because a partial rename validates,
    signs and imports cleanly and is still wrong:

      * the Note body's two Run Shortcut targets (Automation A step 10, Automation B step 10);
      * the Note's settings-block fork label;
      * the `"fork"` value in the bootstrap `state.json` template.

    The Note TITLE is deliberately NOT touched: both forks create a Note with the same title
    on purpose, which is pre-existing and outside this plan.  It is out of reach by
    construction -- this function only ever edits `WFTextActionText` token strings, and the
    title lives in the Create Note action's `name` parameter.

    Every edit goes through `tools/plist_text_edit.py`'s offset-recomputing replacement
    rather than a second hand-rolled substitution.  `Core` -> `Aware` is one character
    LONGER and sits upstream of every attachment in both edited strings, so all of their
    `attachmentsByRange` offsets move; an out-of-bounds range can crash Shortcuts on import.

    Runs BEFORE the `normalise_*` / `verify_*` chain so the rewritten token strings pass
    through the same envelope, output-name and offset guards as everything else.
    """
    note = find_action(
        actions,
        lambda a: (b := token_string(a)) is not None and "## READ THIS FIRST" in b["string"])
    seed = find_action(
        actions,
        lambda a: (b := token_string(a)) is not None and '"schema_version"' in b["string"])
    edits = (
        (token_string(note), CORE_NAME, AWARE_NAME, 2, "the Note's two Run Shortcut targets"),
        (token_string(note), "- Fork: Core", "- Fork: Aware", 1, "the Note's settings-block fork label"),
        (token_string(seed), '"fork": "Core"', '"fork": "Aware"', 1, "the bootstrap state.json fork seed"),
    )
    for body, old, new, expected, description in edits:
        try:
            replace_in_token(body, old, new, expected_count=expected)
        except SystemExit as failure:
            raise SystemExit(
                f"fix_fork_strings could not rewrite {description}: {failure}\n"
                f"CONSEQUENCE: this Aware build would ship a Control Room Note naming the "
                f"Core shortcut. The signed filename is the only carrier of a shortcut's "
                f"display name, so a user following that Note builds two Personal "
                f"Automations pointing at a shortcut that does not exist under these names "
                f"-- a silently dead install for every Aware user, with no error on device "
                f"and nothing any structural check downstream of here can see.") from failure


def main() -> None:
    original = SOURCE.read_bytes()
    root = plistlib.loads(original)
    actions = root["WFWorkflowActions"]
    if any(MARKER in a.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "") for a in actions):
        raise SystemExit("source is already a Sentient fork")
    # Add the third import preference after the two frozen import literals.
    import_id = uid("import-ai")
    actions[6:6] = [action("is.workflow.actions.gettext", UUID=import_id, WFTextActionText="yes"),
                    set_var("Import AI", output(import_id, "Text"))]
    root["WFWorkflowImportQuestions"].append({"ActionIndex": 6, "Category": "Parameter", "DefaultValue": "yes",
                                               "ParameterKey": "WFTextActionText",
                                               "Text": "Use Apple's on-device intelligence contract audit when available? Answer yes or no."})
    root["WFWorkflowName"] = AWARE_NAME
    root["WFWorkflowIcon"] = {"WFWorkflowIconGlyphNumber": 59856, "WFWorkflowIconStartColor": 431817727}
    for index, item in enumerate(actions):
        value = item.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "")
        if value.startswith("Reload before writing a contract."):
            actions[index:index] = audit_block()
            break
    else:
        raise SystemExit("semantic Confession contract marker not found")
    # Phase 11 plan 06.  The fork's own name, in its own Note and its own state seed.  This
    # runs BEFORE the normalise/verify chain so the rewritten token strings are guarded like
    # every other string in the file, and it mutates the forked COPY only -- the frozen-source
    # assertion at the end of main() proves src/PROSOCHE-Dumb.xml was not touched.
    fix_fork_strings(actions)
    # Sentient-only actions are inserted after the Dumb generator has already run, so
    # they never passed its string-envelope pass.  Reuse the same rule and the same
    # build guard rather than duplicating the allowlist: a string-typed parameter
    # holding a bare WFTextTokenAttachment resolves to empty at run time.
    normalise_string_envelopes(actions)
    normalise_output_names(actions)
    # Sentient adds its own numeric conditionals (the Circle-bound and scope gates), so the
    # cycle-9 operand-type normalisation and its invariant have to run on THIS fork too --
    # running them only in build_state_engine.py would leave every Sentient-only comparison
    # with a Text-typed operand and a red operator.
    normalise_numeric_operands(actions)
    verify_string_envelopes(actions)
    verify_output_names(actions)
    verify_required_pickers(actions)
    verify_conditional_inputs(actions)
    verify_numeric_operands(actions)
    # Sentient INHERITS the seeded bootstrap template from the built Dumb source rather
    # than re-seeding it, so the assertion is the whole point here: it proves the subtree
    # survived the fork, and it fails loudly if a future Sentient-only insertion ever adds
    # a settings_snapshot read that the shared bootstrap does not establish.
    verify_state_seed(actions)
    # PHASE 12 (12-01).  Sentient INHERITS the seeded bootstrap template from the built Dumb
    # source rather than re-seeding it, so the assertion is the whole point here: it proves
    # exit_events and exit_selection_counter survived the fork.  Asserted per fork, never
    # inferred from Dumb -- a fork that dropped the rolling window would leave STATE-12's
    # "bounded, versioned document" claim false on the Aware artifact with no error anywhere.
    verify_exit_events_seed(actions)
    # PHASE 12 (12-02).  Sentient INHERITS the seeded bootstrap template from the built Dumb
    # source rather than re-seeding it, so the assertion is the whole point here: it proves
    # the permanent four-leaf active_session container survived the fork.  Asserted per
    # fork, never inferred from Dumb -- restore_managed_settings("Reloaded State") sits
    # inside three nested active_session-derived arms in close_pipeline(), so a fork that
    # dropped a leaf would strand the Aware-fork user dimmed or silenced with no error
    # anywhere else in the pipeline (SESS-07 / SAFE-01).
    verify_active_session_seed(actions)
    # PHASE 12 (12-01, PD-3) -- four guards this fork inherited but never asserted.  Measured
    # before this phase: build_sentient.py imported 13 symbols and ran 13 guards, and none of
    # these four was among them -- so pending_exit, the very seed pattern 12-01 mirrors, was
    # not checked on the Aware fork at all.  The phase rule is "fix whole classes, never
    # site-by-site", and a verifier set that asserts the NEW seed but not the pattern it
    # copies is exactly the site-by-site posture that rule forbids.  Each is a pure assertion
    # over the already-emitted artifact, so arming them cannot change what ships -- it can
    # only reveal a pre-existing defect.  Sentient inherits each of these from the built Dumb
    # source, so these assert the fork did not lose them:
    #   verify_pending_exit_seed        -- the {type, timestamp} container whose absence
    #                                      reproduced the confirmed cycle-16 hard error.
    #   verify_panic_escape_seed        -- the flat numeric panic_escape_enabled seed and the
    #                                      numeric (never condition-100/101) gate over it.
    #   verify_compound_value_reads     -- that no COMPOUND_STATE_KEYS member (recent_sessions,
    #                                      recent_contracts, exit_events,
    #                                      profile_snapshot.enabled_exits) is read through
    #                                      read_value()'s gettext chain; the guard most
    #                                      directly at risk from this phase's exit_events work.
    #   verify_conditional_action_string -- the ownership-compare WFConditionalActionString
    #                                      shape that plan 12-03 must preserve at four sites.
    #
    # PHASE 13 (13-02).  verify_conditional_action_string now carries a SECOND, POSITIVE
    # assertion, so this already-armed call asserts more than it did in Phase 12 -- and this
    # plan adds NO new touch point here, which is a genuine exception to the two-touch-point
    # rule and is recorded rather than left to inference: the guard was ALREADY in the
    # `from build_state_engine import (...)` list above AND already invoked below, armed by
    # Phase 12 (12-01, PD-3).  What it now also asserts on this fork: the Aware artifact's 20
    # inherited variable-bearing comparison targets still carry the Donor-5 envelope after
    # the fork -- a WFTextTokenString whose Value.string holds a "￼" and whose
    # Value.attachmentsByRange is non-empty.  Asserted per fork, never inferred from the Dumb
    # run: Sentient forks the BUILT Dumb XML and re-serializes it, so a fork that flattened
    # or re-enveloped one of those operands would ship an Aware conditional that can never
    # match a real value -- the Mirror's fact gates would silently select the wrong template
    # family (CIRC-07) with no error anywhere, and neither validator gate can see it.
    # The 172/175 raw-literal targets stay unasserted on BOTH forks, for the reason the
    # guard's own docstring records: no donor covers the pure-literal case.
    #
    # PHASE 13 CODE REVIEW (WR-02).  The "flattened" half of the sentence above was, until
    # now, a claim the guard could not back: the shape pin only runs `if isinstance(value,
    # dict)`, and a flattened target is a plain str it skips -- probed, and it PASSED.  The
    # guard now also pins the CENSUS (EXPECTED_VARIABLE_TARGETS = 20, measured on both
    # forks), which is what makes a flattened Aware target detectable at all.  Still no new
    # touch point here: the guard was already imported and already invoked.
    verify_pending_exit_seed(actions)
    verify_panic_escape_seed(actions)
    verify_compound_value_reads(actions)
    verify_conditional_action_string(actions)
    # PHASE 13 (13-01).  Sentient forks the BUILT Dumb XML, so it inherits all 67
    # is.workflow.actions.list actions and every one of their 666 rows -- the 616 Mirror rows
    # this phase wrapped in the donor-confirmed {WFItemType, WFValue} envelope and the 50 that
    # are bare <string> literals by the same donor rule.  Asserted per fork, never inferred
    # from the Dumb run: a fork that dropped, re-serialized or unwrapped a row would ship a
    # BLANK Mirror on the Aware artifact with no error anywhere in the pipeline -- the
    # validator sees a structurally perfect plist and the ToolKit catalog has no entry for
    # WFItems row shape at all.  Phase 12 already recorded what site-by-site arming costs here
    # (four inherited guards imported by Dumb and never run on Aware); the phase rule is "fix
    # whole classes, never site-by-site".
    #
    # PHASE 13 CODE REVIEW (WR-01).  The sentence above used to claim more than the guard
    # delivered: it tested only for a dict row missing WFItemType, so a DROPPED row, a
    # FLATTENED row, a missing WFItems key, a malformed payload and a DOUBLE-WRAPPED row all
    # passed it silently -- every drop/flatten direction this comment advertises.  The guard
    # now asserts the whole two-kind contract per row AND pins the census (67 / 616 / 50,
    # measured identically on both forks), which is what makes "a fork that dropped a row"
    # a claim rather than a hope.  No new touch point: already imported, already invoked.
    verify_list_item_wrappers(actions)
    # Cycle 12, axis 7 -- GATE SEMANTICS.  Sentient inherits the restore block and every
    # sentinel write from Dumb, so these assert the fork did not lose them; and because
    # Sentient adds its own conditionals, they also cover any Sentient-only gate that a
    # future insertion puts over a sentinel-written key.  A brightness/volume write reached
    # with an empty value is a black screen, so this is asserted per fork, never inferred.
    verify_restore_gates(actions)
    # PHASE 16 (16-01), same per-fork reasoning one axis over: Sentient inherits
    # dimming()/silence() and the whole capture-persist-apply ordering from the built Dumb
    # source, but a Sentient-only insertion between a capture and its apply would strand the
    # user dim or silent with no recorded way back, and neither validator gate can see
    # ordering.  Asserted per fork, never inferred from the Dumb run.
    verify_capture_persistence(actions)
    # PHASE 16 (16-04), D-02, same per-fork reasoning again.  Sentient inherits the reduced
    # settings_snapshot shape from the built Dumb source rather than re-seeding it, so this
    # asserts the fork added no read of a leaf D-02 retired.  A Sentient-ONLY read is exactly
    # the case Dumb's own run cannot see: the Mirror's context window is assembled on this
    # fork alone, and a dotted read of a removed leaf there is a hard runtime error that
    # aborts before restore_managed_settings() and strands the Aware-fork user dim or silent.
    # Asserted per fork, never inferred from the Dumb run.
    verify_no_removed_snapshot_leaf_reads(actions)
    verify_sentinel_gates(actions)
    # Sentient inherits the router verbatim from the built Dumb source, but assert it here
    # too: an inserted Sentient block must never land between the OPEN/CLOSE tests and the
    # MANUAL arm, and the absence gate must not reappear through a stale fork.
    verify_router_shape(actions)
    # BD-06 Decision 5's TENTH class (renumbered by the phase 13 code review, WR-06; it read
    # "eighth" when .claude/CLAUDE.md carried seven axes), enforced PER FORK rather than
    # inferred for Sentient
    # from Dumb.  Sentient inherits both halves of the dispatch surface -- the Config literal
    # and the branches -- from the built Dumb source, so a fork that dropped or rewrote
    # either would produce a Circle that dispatches nothing, with no error anywhere.
    verify_dispatch_coverage(actions)
    payload = plistlib.dumps(root, fmt=plistlib.FMT_XML, sort_keys=False)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=TARGET.parent, delete=False) as tmp:
        tmp.write(payload)
        temporary = Path(tmp.name)
    os.replace(temporary, TARGET)
    if SOURCE.read_bytes() != original:
        raise SystemExit("frozen Dumb source changed")
    print(f"built {TARGET} ({hashlib.sha256(payload).hexdigest()})")


if __name__ == "__main__":
    main()
