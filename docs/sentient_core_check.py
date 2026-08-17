#!/usr/bin/env python3
"""Structural proof that Sentient is an additive fork of Dumb.

PHASE 11 PLAN 06 CHANGED THE EQUALITY BELOW, DELIBERATELY -- DO NOT RESTORE THE STRICTER FORM.

Until that plan, `build_sentient.py` made no CONTENT change to the forked source at all, so
"additive fork" could be proven by plain whole-list equality once Sentient's own insertions
were excised.  Plan 06 introduced the first deliberate divergence: `fix_fork_strings()`
rewrites the Aware fork's own name into its Control Room Note (both automation steps), its
settings-block fork label, and its bootstrap `"fork"` seed.  Before that, the Aware fork
instructed its users to select the OTHER fork's shortcut -- a silently dead install, since a
signed `.shortcut` carries no display name inside it and the two Personal Automations
reference the library entry by filename.

Plain equality is therefore false BY DESIGN, and deleting it would throw away the only proof
that nothing ELSE diverged.  It is replaced by a FORK-NORMALISED equality: the inverse
substitution is applied to the Sentient side, with an exact expected count per site, and the
result must equal Dumb action for action.  A bounded, counted normalisation cannot absorb an
unrelated drift -- anything the three known substitutions do not explain still fails.

The normalisation is paired with a POSITIVE divergence assertion, because a normalisation
that silently rewrote a genuine defect would otherwise look like a pass: the Aware Note must
name the Aware display name at least twice and the Core display name zero times, and its
bootstrap seed must read the Aware label.  Together they say: the divergence is real, it is
complete, and it is exactly the fork strings and nothing else.
"""
import copy
import json
import plistlib
import re
from pathlib import Path

CORE = "PROSOCHĒ — Nine Circles — Core"
AWARE = "PROSOCHĒ — Nine Circles — Aware"
PLACEHOLDER = "￼"
RANGE_KEY = re.compile(r"^\{\s*(\d+)\s*,\s*(\d+)\s*\}$")

# The exact inverse of `tools/build_sentient.py`'s `fix_fork_strings()`: (Aware form, Core
# form, occurrences expected across the whole Sentient action list).  The counts are what
# bound the normalisation -- a fourth divergent site would not be undone here and would fail
# the equality below, which is the point.
FORK_STRINGS = (
    (AWARE, CORE, 2),
    ("- Fork: Aware", "- Fork: Core", 1),
    ('"fork": "Aware"', '"fork": "Core"', 1),
)

DUMB = plistlib.loads(Path("src/PROSOCHE-Dumb.xml").read_bytes())
SENTIENT = plistlib.loads(Path("src/PROSOCHE-Sentient.xml").read_bytes())
da, sa = DUMB["WFWorkflowActions"], SENTIENT["WFWorkflowActions"]
assert SENTIENT["WFWorkflowName"].endswith("Aware")


def token_bodies(actions):
    """Every `{string, attachmentsByRange}` body reachable from a `WFTextActionText`."""
    for item in actions:
        value = item.get("WFWorkflowActionParameters", {}).get("WFTextActionText")
        if isinstance(value, dict):
            body = value.get("Value", value)
            if isinstance(body, dict) and isinstance(body.get("string"), str):
                yield body


def denormalise_fork_strings(actions):
    """Undo `fix_fork_strings()` on a COPY, recomputing every attachment offset.

    `Aware` is one character longer than `Core` and sits upstream of every attachment in
    both edited strings, so a plain substitution would leave `attachmentsByRange` keys
    pointing into unrelated prose -- and the resulting inequality would be an artefact of
    this checker rather than a real drift.
    """
    out = copy.deepcopy(actions)
    counts = {old: 0 for old, _, _ in FORK_STRINGS}
    for body in token_bodies(out):
        string = body["string"]
        rewritten = string
        for old, new, _ in FORK_STRINGS:
            counts[old] += rewritten.count(old)
            rewritten = rewritten.replace(old, new)
        if rewritten == string:
            continue
        attachments = body.get("attachmentsByRange")
        body["string"] = rewritten
        if attachments is None:
            continue
        ordered = [attachments[key]
                   for key in sorted(attachments, key=lambda k: int(RANGE_KEY.match(k).group(1)))]
        offsets = [index for index, char in enumerate(rewritten) if char == PLACEHOLDER]
        assert len(offsets) == len(ordered), (
            f"placeholder count changed across the inverse substitution ({len(ordered)} -> "
            f"{len(offsets)}) -- the normalisation would drop or invent an attachment")
        body["attachmentsByRange"] = {f"{{{offset}, 1}}": value
                                      for offset, value in zip(offsets, ordered)}
    for old, _, expected in FORK_STRINGS:
        assert counts[old] == expected, (
            f"expected {expected} occurrence(s) of {old!r} in the Sentient fork, found "
            f"{counts[old]} -- the deliberate fork divergence is partial or has spread, and "
            f"the normalised equality below would then be comparing the wrong thing")
    return out


models = [a for a in sa if a["WFWorkflowActionIdentifier"] == "is.workflow.actions.askllm"]
assert len(models) == 1
p = models[0]["WFWorkflowActionParameters"]
assert p["WFLLMModel"] == "Apple Intelligence on Device" and p["WFGenerativeResultType"] == "Text"
assert "WFAllowWebSearch" not in p and "FollowUp" not in p
marker = next(i for i, a in enumerate(sa) if "--- SENTIENT CONTRACT AUDIT ---" in a.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", ""))
end = next(i for i, a in enumerate(sa[marker + 1:], marker + 1) if "--- SENTIENT CONTRACT AUDIT END ---" in a.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", ""))
assert [a["WFWorkflowActionIdentifier"] for a in sa[6:8]] == ["is.workflow.actions.gettext", "is.workflow.actions.setvariable"]
assert sa[7]["WFWorkflowActionParameters"]["WFVariableName"] == "Import AI"

# Fork-normalised additivity: everything except the fork strings is identical.
normalised = denormalise_fork_strings(sa)
assert normalised[:6] + normalised[8:marker] + normalised[end + 1:] == da
assert all(a["WFWorkflowActionIdentifier"] != "is.workflow.actions.askllm" for a in da)

# Positive divergence: the fork really does name itself, so the normalisation above cannot
# be hiding a defect by quietly rewriting a Note that still names the other fork.
note = [b["string"] for b in token_bodies(sa) if "## READ THIS FIRST" in b["string"]]
assert len(note) == 1, f"expected exactly 1 Control Room Note body, found {len(note)}"
assert note[0].count(AWARE) >= 2, (
    f"the Aware Note names {AWARE!r} {note[0].count(AWARE)} time(s), expected at least 2 -- "
    f"its two automation steps must name the shortcut the user actually has")
assert note[0].count(CORE) == 0, (
    f"the Aware Note still names {CORE!r} {note[0].count(CORE)} time(s) -- a user following "
    f"it would point both Personal Automations at the other fork's shortcut")
seed = [b["string"] for b in token_bodies(sa) if '"schema_version"' in b["string"]]
assert len(seed) == 1, f"expected exactly 1 bootstrap state.json template, found {len(seed)}"
assert json.loads(seed[0].replace(PLACEHOLDER, "0"))["fork"] == "Aware"

print("sentient core check: fork-normalised Dumb core, one bounded model gate, "
      "and the Aware fork names itself")
