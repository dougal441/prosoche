#!/usr/bin/env python3
"""Small structural guard for Phase 5's non-trivial Shortcuts graph."""
from __future__ import annotations

import hashlib
import plistlib
import subprocess
from pathlib import Path

# Reuse the existing locate-by-content reader rather than inventing a third idiom for the
# same literal.  Both scripts live in docs/, so this resolves when either is run directly.
from sequence_dispatch_check import config_literal


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/PROSOCHE-Dumb.xml"
BUILDER = ROOT / "tools/build_state_engine.py"

# BD-06 Decision 3's shipped roster, minus "Redirect", whose implementation is Phase 17's.
# Nine names for nine slots in each of the three sequences.
SHIPPED_PRIMITIVES = {"Pause", "Black and White", "Silence", "Intention", "Dim", "Eject",
                      "Mirror", "Loud Mirror", "Frozen"}


def digest() -> str:
    return hashlib.sha256(SOURCE.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def marker_index(actions, marker: str) -> int:
    matches = [index for index, item in enumerate(actions)
               if item.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "").startswith(f"--- {marker} ---")]
    require(len(matches) == 1, f"expected one {marker} marker")
    return matches[0]


def conditional_ancestry(actions, until: int) -> list[tuple[str, int]]:
    """Return each enclosing conditional and the arm containing action ``until``."""
    stack: list[list[object]] = []
    for item in actions[:until]:
        if item["WFWorkflowActionIdentifier"] != "is.workflow.actions.conditional":
            continue
        params = item["WFWorkflowActionParameters"]
        mode, group = params.get("WFControlFlowMode"), params.get("GroupingIdentifier")
        if mode == 0:
            stack.append([group, 0])
        elif mode == 1:
            require(stack and stack[-1][0] == group, "otherwise without matching conditional")
            stack[-1][1] = 1
        elif mode == 2:
            require(stack and stack[-1][0] == group, "end conditional without matching start")
            stack.pop()
    return [(group, arm) for group, arm in stack]


def main() -> None:
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    first = digest()
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    require(first == digest(), "builder output is not idempotent")

    workflow = plistlib.loads(SOURCE.read_bytes())
    actions = workflow["WFWorkflowActions"]
    text = SOURCE.read_text()
    ids = [item["WFWorkflowActionIdentifier"] for item in actions]
    comments = "\n".join(item.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "") for item in actions)

    require(ids[:5] == ["is.workflow.actions.comment", "is.workflow.actions.comment", "is.workflow.actions.gettext",
                         "is.workflow.actions.setvariable", "is.workflow.actions.gettext"], "pinned imports changed")
    # BD-06 Decision 3's nine shipped primitive names plus the three sequence names.  This
    # tuple and the Config `sequences` arrays must change in the same commit, so the artifact
    # and the checker can never disagree about which names are live.
    for name in ("Pause", "Black and White", "Silence", "Intention", "Dim", "Eject",
                 "Mirror", "Loud Mirror", "Frozen", "Classic", "BlackMirror", "Ambient"):
        require(name in text, f"missing sequence or primitive: {name}")

    # The retired vocabulary is proved gone STRUCTURALLY, over the parsed Config literal's
    # sequences, never by a text grep over the whole artifact.  Several retired words
    # legitimately survive elsewhere in the file as internal variable names and structural
    # markers -- "Ice Profile", "Ice Until", LIVE_ICE_MARKER, "Confession Intention",
    # "Voice Enabled", "Toggle Voice", "Voice Memos" -- so a file-wide grep for them would be
    # both wrong and unsatisfiable.  What BD-06 actually constrains is the sequences arrays.
    sequences = config_literal(actions)["sequences"]
    require(set(sequences) == {"Classic", "BlackMirror", "Ambient"},
            f"sequences are {sorted(sequences)}, expected exactly Classic/BlackMirror/Ambient")
    for name, entries in sequences.items():
        require(len(entries) == 9, f"sequence {name} has {len(entries)} slots, expected 9")
    components = {entry for entries in sequences.values() for entry in entries}
    require(components == SHIPPED_PRIMITIVES,
            f"sequence components are {sorted(components)}, expected exactly the nine BD-06 "
            f"shipped names {sorted(SHIPPED_PRIMITIVES)}")
    for component in sorted(components):
        require("+" not in component,
                f"sequence entry {component!r} is a combined entry; BD-06 Decision 5 abolished "
                "all three, and under condition 4 ('string is') a combined entry dispatches "
                "NOTHING -- a silent runtime no-op with no error anywhere")
    require("Redirect" not in components,
            "the name 'Redirect' appears in a sequence, but no Redirect branch is emitted "
            "until Phase 17 -- naming it now is an entry that dispatches nothing")
    for marker in ("PHASE 5 PRIMITIVE DISPATCH", "PHASE 5 LIVE ICE REDIRECT", "PHASE 5 ICE EXPIRY",
                   "PHASE 5 RESTORE MANAGED SETTINGS", "PHASE 5 MANUAL EMERGENCY RESTORE"):
        require(marker in comments, f"missing semantic marker: {marker}")
    for key in ("settings_snapshot.brightness.original_value", "settings_snapshot.volume.original_value",
                "changed_at", "changed_by_session_id", "cooldown_until"):
        require(key in text, f"missing state safety key: {key}")
    require("AXToggleColorFiltersIntent" not in text and "UAToggleColorFiltersIntent" not in text,
            "unsupported Color Filters action was emitted")
    for item in actions:
        params = item.get("WFWorkflowActionParameters", {})
        if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.setvolume":
            require(params.get("WFVolumeSetting") == "Media", "non-Media volume write")
        if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.setbrightness":
            # PHASE 16 (plan 16-03).  What stood here was a value check forbidding a
            # brightness operand of 0.  It encoded the lower-bound clause that user decision
            # D-01 (LOCKED) retired -- cited, not quoted: it lived in BD-02's original
            # Decision paragraph in docs/CAPABILITY-DECISIONS.md and in the canonical
            # strategy's Sec 21.  Under D-01 the shipped dim target IS 0, so the old test
            # asserted against the build that produced the artifact it inspects.
            #
            # THIS SITE IS THE PHASE'S KNOWN NON-LEXICAL ENCODING.  It carried none of the
            # retired vocabulary -- measured 2026-08-18, a case-insensitive grep for every
            # retired phrase over this whole file returned ZERO hits while this line was
            # live.  No lexical gate can see it; only reading the code reaches it.  Plan
            # 16-05's repo-scoped gate names this line as its known blind spot for exactly
            # that reason, so nobody mistakes a green gate for proof the class is empty.
            #
            # WHAT REPLACES IT is the honest version of what it was reaching for: a
            # brightness write must never be left to an unstated operand.  Per CAP-08
            # (plan 16-02, simulator-measured) WFBrightness is OPTIONAL -- an ABSENT operand
            # does not raise the unfilled-parameter error, it silently applies an
            # unrequested 50% with no capture behind it.  That is a live SAFE-01 / CIRC-05
            # hazard nothing else in docs/ pins.  The complementary direction -- that a
            # variable-fed operand is numerically gated so the cleared sentinel or an empty
            # read never reaches the write -- is already enforced from the generator side by
            # verify_restore_gates(), so the two together cover the write without either
            # one re-imposing a bound on its VALUE.
            require("WFBrightness" in params,
                    "a Set Brightness action ships with no WFBrightness operand; an absent "
                    "operand silently applies a default brightness with no captured "
                    "original to restore (CAP-08)")

    cooldown_index, cooldown = next(
        ((index, item) for index, item in enumerate(actions)
         if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
         and item["WFWorkflowActionParameters"].get("WFControlFlowMode") == 0
         and item["WFWorkflowActionParameters"].get("WFInput", {}).get("Variable", {}).get("Value", {})
         .get("VariableName") == "Cooldown Until"),
        (None, None),
    )
    require(cooldown is not None, "named cooldown conditional missing")
    cooldown_group = cooldown["WFWorkflowActionParameters"]["GroupingIdentifier"]
    # The router's earlier "Input Key has any value" gate (WFCondition 100) was removed by
    # the resolved open-routing-sequence-error fix: ROUTER_OVERVIEW in
    # tools/build_state_engine.py explains routing is now done by POSITIVE identification
    # of Input Key (== "OPEN"/"CLOSE"), never by an absence/presence gate. The live-Ice and
    # expiry markers are therefore nested two levels deep (open_group, cooldown_group), not
    # three -- there is no more input_present_group to include in the ancestry chain.
    open_group = next(
        item["WFWorkflowActionParameters"]["GroupingIdentifier"] for item in actions
        if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
        and item["WFWorkflowActionParameters"].get("WFControlFlowMode") == 0
        and item["WFWorkflowActionParameters"].get("WFCondition") == 4
        and item["WFWorkflowActionParameters"].get("WFConditionalActionString") == "OPEN"
        and item["WFWorkflowActionParameters"].get("WFInput", {}).get("Variable", {}).get("Value", {})
        .get("VariableName") == "Input Key")
    otherwise_index = next(index for index, item in enumerate(actions[cooldown_index + 1:], cooldown_index + 1)
                           if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
                           and item["WFWorkflowActionParameters"].get("GroupingIdentifier") == cooldown_group
                           and item["WFWorkflowActionParameters"].get("WFControlFlowMode") == 1)
    cooldown_end = next(index for index, item in enumerate(actions[otherwise_index + 1:], otherwise_index + 1)
                        if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
                        and item["WFWorkflowActionParameters"].get("GroupingIdentifier") == cooldown_group
                        and item["WFWorkflowActionParameters"].get("WFControlFlowMode") == 2)
    live_index = marker_index(actions, "PHASE 5 LIVE ICE REDIRECT")
    expiry_index = marker_index(actions, "PHASE 5 ICE EXPIRY")
    require(conditional_ancestry(actions, live_index) == [(open_group, 0), (cooldown_group, 0)],
            "live-Ice marker is not exactly in the live-cooldown branch")
    require(conditional_ancestry(actions, expiry_index) == [(open_group, 0), (cooldown_group, 1)],
            "expiry marker is not exactly in the expired-cooldown branch")
    live_actions = actions[cooldown_index + 1:otherwise_index]
    require(any(item["WFWorkflowActionIdentifier"] == "is.workflow.actions.returntohomescreen" for item in live_actions),
            "live-cooldown branch has no redirect")
    live_keys = "\n".join(str(item.get("WFWorkflowActionParameters", {}).get("WFDictionaryKey", "")) for item in live_actions)
    require("heat" not in live_keys and "opens_today" not in live_keys,
            "live-cooldown branch inflates Heat or open count")
    expiry_actions = actions[otherwise_index + 1:cooldown_end]
    expiry_keys = "\n".join(str(item.get("WFWorkflowActionParameters", {}).get("WFDictionaryKey", "")) for item in expiry_actions)
    require("cooldown_until" in expiry_keys and "heat" in expiry_keys,
            "expired-cooldown branch does not clear cooldown and apply relief")

    stack: list[str] = []
    flow_ids = {"is.workflow.actions.conditional", "is.workflow.actions.repeat.count",
                "is.workflow.actions.repeat.each", "is.workflow.actions.choosefrommenu"}
    for item in actions:
        if item["WFWorkflowActionIdentifier"] not in flow_ids:
            continue
        params = item["WFWorkflowActionParameters"]
        mode, group = params.get("WFControlFlowMode"), params.get("GroupingIdentifier")
        if mode == 0:
            stack.append(group)
        elif mode == 2:
            require(stack and stack[-1] == group, "unbalanced control flow")
            stack.pop()
    require(not stack, "unclosed control flow")
    require("superseded CLOSE reaches no restore" in comments, "superseded CLOSE restore guard missing")
    print("phase5 self-check: passed")


if __name__ == "__main__":
    main()
