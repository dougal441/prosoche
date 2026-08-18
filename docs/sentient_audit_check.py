#!/usr/bin/env python3
"""Focused evidence for the bounded Sentient audit protocol, in EVERY audit block.

PHASE 11 PLAN 09.  Until this plan the file located ONE span, from the first start marker in
document order, and asserted a dozen properties inside it.  That was correct while the fork
carried one audit; once plan 11-05 added a second OPEN-arm dispatch rendering it became the
same blindness class as the defect it was meant to catch -- with two blocks it inspected one
and stayed green, so a second block that had lost the latency gate, the parsed-token gate,
the bounded prompt or the forbidden-action exclusions was invisible here.  Measured on the
two-block artifact before this rewrite: exit 0, one block inspected.

THE PER-BLOCK COUNTS ARE DELIBERATELY NOT SUMMED INTO ARTIFACT-WIDE TOTALS.  "Exactly one
Use Model per block" and "exactly one revision prompt per block" are the properties that
matter; an artifact-wide total of two would be satisfied just as well by two model calls
inside one block and none in the other, which is precisely the shape this file exists to
reject.  The count of BLOCKS is reconciled against the count of Use Model actions instead.

THIS FILE DELIBERATELY CARRIES NO CORE-DERIVED EXPECTATION, and the reason is recorded here
because a previous version of the reason was measurably wrong.  Everything below reconciles
the Aware fork AGAINST ITSELF -- span count against model count, gate by gate inside each
block -- so one block plus one model is a clean run here by construction.  That is a real
blind spot and it is stated rather than hidden: this file cannot see a MISSING rendering's
audit, and it never could.  PHASE 11 CODE REVIEW (WR-18, then IN-04) measured it twice.

What closed that gap is NOT a third copy of the Core derivation.  It is
tools/build_sentient.py's assertion, which as of IN-04 re-derives the expected count from the
Core fork's own untouched bytes via the shared open_arm_contract_markers() and refuses to
write the artifact on a mismatch -- so the defect is now caught BEFORE disk, and by a
quantity independent of the collection it checks.  docs/sentient_core_check.py keeps the
same expectation post-hoc, on the shipped artifact.  Adding a third instance here would
duplicate what that file already asserts, on the same artifact and at the same moment, and
give the derivation a third place to drift.  The declined-with-reason record: the earlier
justification for declining -- "the builder assertion is strictly stronger than a second
standalone checker because it fires before the artifact reaches disk" -- was HALF WRONG and
is retracted.  It was stronger in TIMING and weaker in INDEPENDENCE, which is the half that
mattered; the fix was to make the builder independent, not to leave the claim standing.
"""
import plistlib
import re
from pathlib import Path

a = plistlib.loads(Path("src/PROSOCHE-Sentient.xml").read_bytes())["WFWorkflowActions"]


def comment_text(x):
    return x.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "")


starts = [i for i, x in enumerate(a) if "--- SENTIENT CONTRACT AUDIT ---" in comment_text(x)
          and "--- SENTIENT CONTRACT AUDIT END ---" not in comment_text(x)]
ends = [i for i, x in enumerate(a) if "--- SENTIENT CONTRACT AUDIT END ---" in comment_text(x)]
assert starts, "no Sentient audit block at all -- this artifact is a Core fork under another name"
assert len(starts) == len(ends), f"{len(starts)} audit start marker(s) but {len(ends)} end marker(s)"
spans = list(zip(starts, ends))
assert all(s < e for s, e in spans), f"an audit end marker precedes its start: {spans}"
assert all(spans[i][1] < spans[i + 1][0] for i in range(len(spans) - 1)), (
    f"audit spans overlap or are out of order: {spans}")

# Block count reconciled against model count.  One audit block carries exactly one model
# call, so these are the same quantity counted two ways; a mismatch means a block lost its
# model, or a model was emitted outside any block where none of the gates below guard it.
models = [i for i, x in enumerate(a) if x["WFWorkflowActionIdentifier"] == "is.workflow.actions.askllm"]
assert len(spans) == len(models), (
    f"{len(spans)} audit block(s) but {len(models)} Use Model action(s) -- every model call "
    f"must sit inside a block, behind its Circle, latency and parsed-token gates")

for n, (start, end) in enumerate(spans):
    block = a[start:end + 1]
    raw = str(block)
    where = f"audit block {n} (actions {start}-{end})"
    assert raw.count("is.workflow.actions.askllm") == 1, f"{where}: expected exactly 1 Use Model"
    for phrase in ("ALLOW", "CHALLENGE", "DENY", "deliberate leisure", "lying", "diagnosis",
                   "feelings", "app contents", "Intention", "Boundary minutes", "Circle", "Heat",
                   "Open count", "specificity", "boundedness", "recorded consistency",
                   "Previous Respected"):
        assert phrase in raw, f"{where}: missing {phrase!r}"
    assert "WFAllowWebSearch" not in raw and "FollowUp" not in raw, f"{where}: OS27-gated key"
    # The completed-latency gate: the two dates sit immediately around Use Model and an
    # eight-second result takes the Dumb path.
    assert "gettimebetweendates" in raw and "Audit Seconds" in raw and "WFNumberValue': 8" in raw, (
        f"{where}: the eight-second completed-latency gate is missing")
    pattern = next(x for x in block if x["WFWorkflowActionIdentifier"] == "is.workflow.actions.text.match"
                   )["WFWorkflowActionParameters"]["WFMatchTextPattern"]
    assert all(re.search(pattern, token) for token in ("ALLOW", "CHALLENGE", "DENY")), (
        f"{where}: the parsed-token pattern does not match all three tokens")
    prompt = next(x for x in block if x["WFWorkflowActionIdentifier"] == "is.workflow.actions.askllm"
                  )["WFWorkflowActionParameters"]["WFLLMPrompt"]["Value"]
    assert {v["VariableName"] for v in prompt["attachmentsByRange"].values()} >= {
        "Audit Scope", "Audit Prior Fact"}, f"{where}: the prompt lost a scope variable"
    assert raw.count("Revise or continue") == 1, f"{where}: expected exactly one revision prompt"
    assert "Circle Next" in raw and "returntohomescreen" in raw and "is.workflow.actions.exit" in raw, (
        f"{where}: the bounded DENY fallback is incomplete")
    # The model may never touch arithmetic, timers, state or any safety decision.
    for forbidden in ("setbrightness", "setvolume", "setvalueforkey", "number.random", "WFDelayTime"):
        assert forbidden not in raw, f"{where}: forbidden action {forbidden!r} inside an audit block"

print(f"sentient audit check: {len(spans)} block(s), each a compact prompt, one challenge, "
      f"bounded fallback")
