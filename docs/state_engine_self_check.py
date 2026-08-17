#!/usr/bin/env python3
"""Reference arithmetic and structural checks for phases 3–4.

The arithmetic checks the specification; the plist checks only wiring shape and
cannot substitute for an on-device Shortcuts run.
"""

# PHASE 10-01: raised entry curves. Every entry rose by that profile's own first band
# width, so band widths are preserved exactly and only entry into Circle 1 is delayed.
# This table is a duplicate of the Config literal at src/PROSOCHE-Dumb.xml action 7 and
# must be changed in the same commit as it.
# BD-06-A1 (phase 11-03): the middle profile is `Purgatory`, renamed from `Limbo` so that
# `Limbo` names exactly one thing -- Circle 1's positional depth. The three profiles are the
# three canticles. The ARRAY is unchanged; only the key moved.
THRESHOLDS = {
    "Paradise": [4, 7, 10, 13, 16, 19, 22, 25, 28],
    "Purgatory": [3, 5, 7, 9, 11, 13, 16, 19, 22],
    "Inferno": [2, 3, 5, 7, 9, 11, 13, 15, 17],
}


def gravity(opens_today):
    return min(opens_today // 6, 5)


def circle(profile, pressure):
    # PHASE 10-01: the seed is 0, not 1 -- Pressure below the profile's first threshold
    # resolves to Circle 0, the silent band, in which state accumulates and nothing is
    # shown. Mirrors number(0, "Circle Next") in open_pipeline().
    result = 0
    for index, threshold in enumerate(THRESHOLDS[profile], 1):
        if pressure >= threshold:
            result = index
    return min(result, 9)


def heat(value, away_seconds=0, opened=True):
    value += -(away_seconds // 600)
    if opened:
        value += 1
    return min(max(value, 0), 30)


def main():
    assert [circle("Purgatory", n) for n in (0, 3, 20, 99)] == [0, 1, 8, 9]
    # Circle 0, the silent band: Pressure below the profile's first threshold shows nothing.
    assert circle("Purgatory", 2) == 0 and circle("Paradise", 3) == 0 and circle("Inferno", 1) == 0
    # Config-literal invariants (src/CONFIG-BLOCK.md): nine entries, strictly ascending,
    # and a last entry below heat.cap + gravity.cap = 35 so Circle 9 stays reachable.
    for profile, table in THRESHOLDS.items():
        assert len(table) == 9, profile
        assert all(a < b for a, b in zip(table, table[1:])), profile
        assert table[-1] < 35, profile
    assert len({circle(profile, 8) for profile in THRESHOLDS}) == 3
    assert [gravity(n) for n in (0, 6, 30, 60)] == [0, 1, 5, 5]
    assert heat(10, away_seconds=1500) == 9  # -2 decay, then +1 OPEN
    assert heat(40) == 30 and heat(0, away_seconds=600) == 0
    structural_check()


def structural_check():
    from pathlib import Path
    import plistlib

    actions = plistlib.loads(Path("src/PROSOCHE-Dumb.xml").read_bytes())["WFWorkflowActions"]
    ids = [action["WFWorkflowActionIdentifier"] for action in actions]
    comments = [action.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "") for action in actions]

    assert len(actions) >= 374
    assert ids[:5] == ["is.workflow.actions.comment", "is.workflow.actions.comment", "is.workflow.actions.gettext", "is.workflow.actions.setvariable", "is.workflow.actions.gettext"]
    assert not any(text.startswith("OPEN branch anchor.") or text.startswith("CLOSE branch anchor.") for text in comments)
    assert any(text.startswith("--- OPEN STATE ENGINE") for text in comments)
    assert any(text.startswith("--- CLOSE SESSION PIPELINE") for text in comments)
    assert any(text.startswith("Resolve Circle by an ordered nine-step threshold scan") for text in comments)
    assert any(action.get("WFWorkflowActionParameters", {}).get("WFRepeatCount") == 9 for action in actions)
    assert "is.workflow.actions.delay" in ids
    # CYCLE 14 replaced every downstream elapsed-time computation with plain numeric
    # subtraction (elapsed_since()); only the CLOCK block's own "Now Epoch" derivation
    # still uses Get Time Between Dates (see elapsed_since()'s docstring). That block's
    # construct is Donor-7-confirmed and needs zero coercion. This count was stale from
    # before the replacement; the exact value is deliberate, so a new call site has to be
    # a conscious decision rather than silently passing a floor check.
    assert ids.count("is.workflow.actions.gettimebetweendates") == 1
    assert "is.workflow.actions.round" in ids
    assert "is.workflow.actions.number.random" in ids
    assert "is.workflow.actions.documentpicker.open" in ids
    assert "is.workflow.actions.appendvariable" in ids

    setters = [(index, action) for index, action in enumerate(actions)
               if action["WFWorkflowActionIdentifier"] == "is.workflow.actions.setvalueforkey"]
    keys = [action["WFWorkflowActionParameters"]["WFDictionaryKey"] for _, action in setters]
    # PHASE 12 (12-03): the required literal moved to the dotted leaf "active_session.id"
    # -- the container/leaf split converted every setter to write only that leaf, so the
    # unqualified container key no longer appears among setter keys by construction.
    for required in ("heat", "gravity", "pressure", "circle", "active_session.id", "recent_sessions", "last_close_at"):
        assert required in keys
    # Every write immediately rebinds the full dictionary it just returned.
    for index, action in setters:
        parameters = action["WFWorkflowActionParameters"]
        target = parameters["WFDictionary"]["Value"]["VariableName"]
        next_parameters = actions[index + 1]["WFWorkflowActionParameters"]
        assert actions[index + 1]["WFWorkflowActionIdentifier"] == "is.workflow.actions.setvariable"
        assert next_parameters["WFVariableName"] == target
        assert next_parameters["WFInput"]["Value"]["OutputUUID"] == parameters["UUID"]

    close = next(index for index, text in enumerate(comments) if text.startswith("--- CLOSE SESSION PIPELINE"))
    owner = next(index for index, text in enumerate(comments) if text.startswith("Compare the reloaded active session"))
    owner_group = actions[owner + 1]["WFWorkflowActionParameters"]["GroupingIdentifier"]
    otherwise_index = next(index for index in range(owner + 2, len(actions))
                           if actions[index]["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
                           and actions[index]["WFWorkflowActionParameters"].get("GroupingIdentifier") == owner_group
                           and actions[index]["WFWorkflowActionParameters"].get("WFControlFlowMode") == 1)
    owner_end = next(index for index in range(otherwise_index + 1, len(actions))
                     if actions[index]["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
                     and actions[index]["WFWorkflowActionParameters"].get("GroupingIdentifier") == owner_group
                     and actions[index]["WFWorkflowActionParameters"].get("WFControlFlowMode") == 2)
    assert all(action["WFWorkflowActionIdentifier"] != "is.workflow.actions.documentpicker.save"
               for action in actions[otherwise_index:owner_end])
    assert close < owner < otherwise_index < owner_end


if __name__ == "__main__":
    main()
