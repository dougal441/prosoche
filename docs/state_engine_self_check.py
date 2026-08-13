#!/usr/bin/env python3
"""Reference arithmetic and structural checks for phases 3–4.

The arithmetic checks the specification; the plist checks only wiring shape and
cannot substitute for an on-device Shortcuts run.
"""

THRESHOLDS = {
    "Paradise": [1, 4, 7, 10, 13, 16, 19, 22, 25],
    "Limbo": [1, 3, 5, 7, 9, 11, 14, 17, 20],
    "Inferno": [1, 2, 4, 6, 8, 10, 12, 14, 16],
}


def gravity(opens_today):
    return min(opens_today // 6, 5)


def circle(profile, pressure):
    result = 1
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
    assert [circle("Limbo", n) for n in (0, 3, 20, 99)] == [1, 2, 9, 9]
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
    assert ids.count("is.workflow.actions.gettimebetweendates") >= 3
    assert "is.workflow.actions.round" in ids
    assert "is.workflow.actions.number.random" in ids
    assert "is.workflow.actions.documentpicker.open" in ids
    assert "is.workflow.actions.appendvariable" in ids

    setters = [(index, action) for index, action in enumerate(actions)
               if action["WFWorkflowActionIdentifier"] == "is.workflow.actions.setvalueforkey"]
    keys = [action["WFWorkflowActionParameters"]["WFDictionaryKey"] for _, action in setters]
    for required in ("heat", "gravity", "pressure", "circle", "active_session", "recent_sessions", "last_close_at"):
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
