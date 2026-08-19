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

# PHASE 14 (14-01).  The iOS Color Filters (grayscale) toggle, and its macOS twin.  The twin is
# named here ONLY so it can be asserted ABSENT -- it must never be emitted.
AX_COLOR_FILTERS = "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent"
UA_COLOR_FILTERS_MACOS_TWIN = "com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent"

# Derivation of the count, so a future reader meeting a mismatch investigates the ARTIFACT
# rather than reflexively editing this constant:
#   APPLY sites = 11, one per primitive_dispatch() rendering.  ash() emits one Set Color
#   Filters (on) and primitive_dispatch() is rendered eleven times per fork -- nine
#   Test-a-Circle submenu cases plus two in universal_leaving().        -> 11
#   OFF sites   = 4, one per restore_managed_settings() call site: close_pipeline(),
#   manual_emergency_restore(), ice_expiry() and live_ice_redirect().  The off leg is
#   unconditional, so it renders exactly once per expansion.            -> 4
#   Total: 15 per fork, identical in Dumb and Sentient.
#
# DERIVED FROM THE BUILT ARTIFACT, NOT TRANSCRIBED FROM A PLAN.  Measured 2026-08-19 against
# both rebuilt forks.  Note for anyone comparing against phase-14 planning material: an earlier,
# SUPERSEDED snapshot-based design also projected 15 per fork, by entirely different arithmetic.
# The agreement is a coincidence and must not be read as confirmation of either figure.
#
# A change to the number of dispatch renderings or to the number of restore call sites moves
# this number LEGITIMATELY, but only by exactly what that change explains.  Any other delta is
# the regression this assertion exists to catch.
EXPECTED_COLOR_FILTER_SITES = 15


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
    # PHASE 16 (16-04), D-02: the two bare leaf names "changed_at" and
    # "changed_by_session_id" stood in this tuple and are REMOVED.  They are written at zero
    # sites and read at zero sites now; asserting their presence would assert against the
    # build that produces the artifact this checker inspects.  The two DOTTED
    # original_value keys and cooldown_until are retained deliberately -- original_value is
    # the leaf every restore gate reads, and its absence from the bootstrap seed is the
    # cycle-10 hard-error class.
    for key in ("settings_snapshot.brightness.original_value", "settings_snapshot.volume.original_value",
                "cooldown_until"):
        require(key in text, f"missing state safety key: {key}")
    # PHASE 14 (14-01), 2026-08-19.  THE REVERSAL, AND ITS AUTHORITY.  What stood here was a
    # SINGLE assertion that BOTH Color Filters identifiers were absent, and it was CORRECT when
    # written: the capability verdict then in force held that no Color Filters action was
    # available to an iPhone at all, so Ash shipped as an alert.  Spike 005 superseded that
    # verdict from three decrypted device-authored donors (tier-1 evidence,
    # .planning/spikes/005-ios-color-filters-identifier/), and phase 14 shipped the real
    # toggle.  Authority for the reversal: user decisions D-14-A through D-14-D, 2026-08-19.
    #
    # THE INVERSION IS ASYMMETRIC, AND THE SECOND HALF IS WHERE THE TEETH ARE.  Deleting the
    # old line outright would have removed the macOS-twin protection ALONG WITH the inversion,
    # which is the opposite of what this phase needs: gate A now fails permanently because the
    # AX identifier is absent from all three bundled ToolKit snapshots, and a red validator is
    # a standing invitation to reach for the UA* twin, which IS in the catalog and would make
    # the validator green by shipping an action that does nothing whatsoever on an iPhone.
    # So: AX asserted PRESENT at a derived count, UA asserted STILL ABSENT.  T-14-03.
    #
    # Counted by IDENTIFIER over parsed actions, never by substring hits in the raw text --
    # the identifier also appears in this artifact's comments and prose, so a text count would
    # be inflated by exactly the material that is not an action.
    color_filter_sites = sum(1 for item in actions
                             if item.get("WFWorkflowActionIdentifier") == AX_COLOR_FILTERS)
    require(color_filter_sites == EXPECTED_COLOR_FILTER_SITES,
            f"expected {EXPECTED_COLOR_FILTER_SITES} Color Filters actions, found "
            f"{color_filter_sites} -- see EXPECTED_COLOR_FILTER_SITES for the arithmetic "
            "before changing the number")
    require(UA_COLOR_FILTERS_MACOS_TWIN not in text,
            "the macOS Color Filters twin "
            f"({UA_COLOR_FILTERS_MACOS_TWIN}) was emitted. It is in the bundled ToolKit "
            "catalog and the iOS AX* action is not, so substituting it QUIETS A RED "
            "VALIDATOR BY SHIPPING AN ACTION THAT DOES NOTHING ON AN IPHONE -- Circle 2 "
            "would silently stop working and colour would never be restored. Gate A is "
            "expected to stay red for the AX identifier (D-14-01); that is not a reason "
            "to swap in this one")
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
