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

PHASE 11 PLAN 09 GENERALISED THE EXCISION FROM ONE AUDIT SPAN TO N, AND STOPPED PINNING THE
COUNT.  The bounded-and-counted property above is PRESERVED exactly, and preserving it is the
point: every excision below is still a bounded, counted, content-located region, so anything
the known divergences do not explain still fails the equality.  What changed is that the
number of audit spans is now DERIVED from the Core fork rather than written here as a
literal.  A literal count is what turned this file into a defect that pinned itself: the
retired model-count assertion named a single audit, which described the artifact while the
fork had one OPEN-arm rendering -- and when plan 11-05 added a second, that assertion went
on asserting the number the MISSING audit produced, so the checker agreed with the defect
instead of reporting it.  A derived count moves with the source instead.
"""
import copy
import json
import plistlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

# The SAME structural derivation tools/build_sentient.py uses to place the audits and
# tools/build_state_engine.py's verify_circle_zero_silence() uses to bound the OPEN arm.
# Imported rather than reimplemented: a second copy of "where the OPEN arm is" would be free
# to drift from the builder, and this checker's whole job is to disagree when the builder is
# wrong -- which it cannot do if it derives the answer differently.
from build_state_engine import flow_index, input_key_tests  # noqa: E402

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


def comment_text(item):
    return item.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "")


# WHY THESE TWO NUMBERS MUST AGREE, which is the whole content of the assertion below.
#
# Every primitive_dispatch() rendering reaches the Intention primitive; Intention calls
# persist_contract(); persist_contract() emits exactly one "Reload before writing a contract."
# comment.  So inside the OPEN arm, contract markers COUNT RENDERINGS.  build_sentient.py
# inserts exactly one audit block -- and therefore exactly one Use Model action -- at each of
# them.  The two counts are the same quantity measured on either side of the fork.
#
# A MISMATCH IS NEVER COSMETIC.  Fewer models than renderings means some rendering reaches
# Intention with no contract audit at all: that user's Aware fork silently behaves as Core on
# that path, which is what plan 11-05 accidentally shipped when it added the bypass-removed
# rendering.  More models than renderings means an audit landed somewhere no rendering
# reaches -- most likely one of the nine Test-a-Circle markers in the MANUAL arm, which would
# put an on-device model call behind a diagnostic menu item.
#
# Derived from the CORE fork on purpose.  Core is the source the Aware fork is built from, so
# deriving from it makes this an independent statement about the builder's output rather than
# the Aware artifact agreeing with itself.
core_open = next(((i, s) for i, c, s in input_key_tests(da) if c == 4 and s == "OPEN"), None)
assert core_open is not None, (
    "no conditional tests Input Key against the OPEN literal in the Core fork -- the router "
    "has been restructured and the expected audit count can no longer be derived")
core_open_end = flow_index(da, da[core_open[0]]["WFWorkflowActionParameters"]["GroupingIdentifier"], 1)
expected_audits = sum(1 for i in range(core_open[0], core_open_end)
                      if comment_text(da[i]).startswith("Reload before writing a contract."))
assert expected_audits >= 1, "the Core fork's OPEN arm contains no contract marker at all"

models = [a for a in sa if a["WFWorkflowActionIdentifier"] == "is.workflow.actions.askllm"]
assert len(models) == expected_audits, (
    f"the Aware fork carries {len(models)} Use Model action(s) but the Core fork's OPEN arm "
    f"has {expected_audits} dispatch rendering(s). Each rendering reaches Intention and must "
    f"carry exactly one contract audit; fewer means a rendering silently behaves as Core, "
    f"more means an audit landed where no OPEN rendering reaches it.")
# EVERY model, not the first: a second block that lost the pinned on-device source, or gained
# an OS27-gated key, is invisible to a check that stops at index 0.
for n, m in enumerate(models):
    p = m["WFWorkflowActionParameters"]
    assert p["WFLLMModel"] == "Apple Intelligence on Device", (
        f"Use Model #{n} names {p.get('WFLLMModel')!r}; the on-device source is a privacy "
        f"constraint, not a default -- no behavioural data may leave the device")
    assert p["WFGenerativeResultType"] == "Text", f"Use Model #{n} result type is {p.get('WFGenerativeResultType')!r}"
    assert "WFAllowWebSearch" not in p and "FollowUp" not in p, (
        f"Use Model #{n} emits an OS27-gated key; the target is iOS 26")

# Every audit span, paired start-to-end in document order.
starts = [i for i, a in enumerate(sa) if "--- SENTIENT CONTRACT AUDIT ---" in comment_text(a)
          and "--- SENTIENT CONTRACT AUDIT END ---" not in comment_text(a)]
ends = [i for i, a in enumerate(sa) if "--- SENTIENT CONTRACT AUDIT END ---" in comment_text(a)]
assert len(starts) == len(ends) == expected_audits, (
    f"found {len(starts)} audit start marker(s) and {len(ends)} end marker(s), expected "
    f"{expected_audits} of each")
spans = list(zip(starts, ends))
assert all(s < e for s, e in spans) and all(spans[i][1] < spans[i + 1][0] for i in range(len(spans) - 1)), (
    f"audit spans are not disjoint and in order: {spans}")

# The import prologue, resolved BY CONTENT rather than by two hard-coded slice indexes.
# Those indexes were the mirror of the builder's WR-11 defect: they named the same integer
# the builder used to hard-code, so the moment that integer legitimately moved this checker
# would have failed for a reason that had nothing to do with what it exists to prove.  Now
# the builder and this file agree BY CONSTRUCTION -- both resolve the same anchor -- rather
# than by both happening to say 6.
anchor = next((i for i, a in enumerate(sa)
               if a["WFWorkflowActionIdentifier"] == "is.workflow.actions.setvariable"
               and a["WFWorkflowActionParameters"].get("WFVariableName") == "Import Voice"), None)
assert anchor is not None, "no set-variable names 'Import Voice'; the import prologue anchor is gone"
splice = anchor + 1
assert [a["WFWorkflowActionIdentifier"] for a in sa[splice:splice + 2]] == [
    "is.workflow.actions.gettext", "is.workflow.actions.setvariable"], (
    f"the two import-preference actions are not at the derived splice {splice}")
assert sa[splice + 1]["WFWorkflowActionParameters"]["WFVariableName"] == "Import AI"
assert SENTIENT["WFWorkflowImportQuestions"][-1]["ActionIndex"] == splice, (
    "the third import question's ActionIndex does not equal the derived splice position -- it "
    "would prompt for the AI preference and write the answer into another action's parameter")

# Fork-normalised additivity, generalised to N audit spans.  Excising only the FIRST span
# would leave the others in the comparison and fail the equality for the wrong reason --
# reporting "the fork diverged" when what actually happened is that it gained a second audit
# exactly as intended.  The excision stays bounded and counted: N spans located by their own
# paired comment markers, plus the two import-preference actions at the derived splice.
normalised = denormalise_fork_strings(sa)
excised = {splice, splice + 1}
for s, e in spans:
    excised |= set(range(s, e + 1))
core_comparable = [a for i, a in enumerate(normalised) if i not in excised]
assert len(core_comparable) == len(da), (
    f"after excising {len(excised)} Sentient-only action(s) the Aware fork has "
    f"{len(core_comparable)} actions against the Core fork's {len(da)}")
assert core_comparable == da, "the Aware fork diverges from Core outside the fork strings"
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

print(f"sentient core check: fork-normalised Dumb core, {len(models)} bounded model gate(s) "
      f"matching {expected_audits} Core OPEN-arm rendering(s), and the Aware fork names itself")
