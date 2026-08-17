#!/usr/bin/env python3
"""Report every live file that still asserts the RETIRED brightness-floor clause.

TWO INVARIANTS, ONE FILE, because they fail together.  Both failures have one cause: a
RECORD drifting from the BUILD it describes.

**Why this file exists at all.**  User decision D-01 (LOCKED 2026-08-17; the current record
is the 2026-08-18 revision block in
`.planning/phases/16-dimming-and-silence-as-distinct-device-proven-circles/16-CONTEXT.md`)
set `safety.brightness_floor` and `safety.dim_target` to `0` on the main line.  The clause
that had asserted a lower bound is retired.  It is CITED here, never restated -- it lived in
BD-02's original Decision paragraph in `docs/CAPABILITY-DECISIONS.md` and in the canonical
strategy's Sec 21, and `docs/CAPABILITY-DECISIONS.md` BD-02's Supersession note is now the
authority where the two disagree.  The canonical strategy itself is FROZEN: a historical
design input, not a living spec, retained unmodified by user decision 2026-08-18.

**Why a gate and not a sweep.**  The blast radius of D-01 was enumerated FOUR times before
this file existed and every enumeration claimed completeness: six sites, then eight, then
nine, then thirteen-or-more.  Re-measuring during planning found four more that appeared in
no prior list.  A fifth undercount is not a hypothetical; it is the base rate.  The failure
mode is not "someone missed one", it is "the miss was SILENT until the next re-measurement".
This file makes the next one LOUD.  It reports EVERY survivor in one run, with file and line
-- deliberately not the first, because reporting one per run reproduces exactly the
fix-what-is-visible-then-re-measure loop that failed four times.

**What a record asserting the retired clause actually costs.**  Several of the corrected
sites declared themselves BINDING on later phases -- CAP-16's Fallback cell in
`docs/BUILD-NOTES.md` named Phase 5's CIRC-05 by requirement id.  A stale record of that kind
is not a note that has aged; it is a live instruction to build something the build does not
do.  It licenses a change that a true record would have blocked.

+-------------------------------------------------------------------------------------+
| THIS CHECK CANNOT CATCH NON-LEXICAL ENCODINGS.  A GREEN RESULT IS NOT PROOF THAT THE  |
| CLASS IS EMPTY.  See BLIND SPOT below before trusting a pass.                         |
+-------------------------------------------------------------------------------------+

Read-only: reads text files and parses the two built artifacts through the project's
existing Config reader.  No subprocess, no rebuild, no write.
"""
from __future__ import annotations

import json
import plistlib
import re
import sys
from pathlib import Path

# Reuse the existing locate-by-content reader for the built Config literal rather than
# inventing a fourth idiom for the same literal (docs/phase5_self_check.py imports it the
# same way).  Both scripts live in docs/, so this resolves when either is run directly.
from sequence_dispatch_check import config_literal

ROOT = Path(__file__).resolve().parents[1]
FORKS = ("Dumb", "Sentient")
CONFIG_BLOCK = "src/CONFIG-BLOCK.md"

# ---------------------------------------------------------------------------------------
# BLIND SPOT -- STATED HERE, WHERE A READER OF THE GATE WILL FIND IT.
#
# THIS CHECK CANNOT CATCH NON-LEXICAL ENCODINGS OF THE RETIRED RULE, and the class is
# demonstrably not purely lexical.  The proof is a measurement, not an argument:
#
#   docs/phase5_self_check.py carried a live site at line 117 that asserted the brightness
#   parameter was not zero -- the retired rule expressed as a VALUE COMPARISON, carrying
#   NONE of the vocabulary below.  Measured 2026-08-18: a case-insensitive grep of every
#   pattern in this file over that WHOLE file returned ZERO matches while the site was live.
#   It was reachable only by READING the code.  Plan 16-03 fixed it by hand and replaced it
#   with a CAP-08-derived assertion that the WFBrightness operand is PRESENT -- see the long
#   comment above that require() call, which records the same blind-spot status from the
#   other side.
#
# So: a pass here means no LEXICAL survivor remains among the files this gate walks.  It
# says nothing about a rule re-encoded as an inequality, a magic number, a threshold in a
# test fixture, or a comparison in a generator.  Nobody may read a green run as proof the
# class is empty.  The human-reasoned residue list lives in plan 16-05's <measured_site_list>
# section, and that list is MEASURED, NOT PROVEN EXHAUSTIVE -- it says so in its own text.
# ---------------------------------------------------------------------------------------

# FAMILY A -- absolute-prohibition phrasings.  Case-insensitive substrings.
FAMILY_A = (
    "never zero",
    "never set zero",
    "never to zero",
    "never set to zero",
    "never reaches zero",
    "never be lowered to zero",
    "zero brightness",
    "never `0`",
)

# FAMILY B -- the retired percentage band.  Both dash forms, because the em/en dash variant
# is what most of the prose actually used and a hyphen-only pattern would have missed it.
FAMILY_B = ("10-15", "10" + chr(8211) + "15")

# FAMILY C -- the retired strictness description, SCOPED.
#
# `strictly positive` is ordinary technical English and counts ONLY when a dim-target
# mention sits nearby.  Unscoped it produces a KNOWN FALSE POSITIVE:
# tools/build_state_engine.py carries a comment about a "strictly positive EPOCH" -- a UNIX
# timestamp, which genuinely is strictly positive and has nothing to do with brightness.
# (Anchor by content: that comment was at :2084 when the window was swept and had moved to
# :2244 by the time this file was written.  Every anchor in this phase has shifted; locate
# it by the word `epoch`, never by line.)
#
# WHY +/-6 AND NOT TIGHTER.  Swept 2026-08-18 across +/-2, +/-4, +/-6, +/-8 and +/-10 over
# the two files that contained the phrase.  At +/-2 and +/-4 a real site in
# docs/environmental_restore_check.py was MISSED -- its nearest dim-target mention was six
# lines away.  +/-6 is the SMALLEST window that catches every real site, and the epoch false
# positive stays excluded all the way out to +/-10, so the choice is not delicately
# balanced: there is a four-line margin on either side of it.
FAMILY_C_PHRASE = "strictly positive"
FAMILY_C_ANCHORS = ("dim_target", "dim target")
FAMILY_C_WINDOW = 6

# ---------------------------------------------------------------------------------------
# THE ALLOWLIST.  Explicit, commented, and part of the deliverable -- not a walk condition.
#
# These exclusions ARE the freeze, expressed in code, so it survives the memory of the
# person who decided it.  An unexplained exclusion is indistinguishable from a defect, so
# every entry carries its reason on the same line.
#
# TIER 1 -- path prefixes.  The frozen historical record.
# ---------------------------------------------------------------------------------------
ALLOWED_PREFIXES: tuple[tuple[str, str], ...] = (
    (
        "PROSOCHE_Nine_Circles_Canonical_Strategy.md",
        "FROZEN by user decision 2026-08-18: a historical design input, not a living spec. "
        "Its Sec 21 floor clause stays exactly as written; docs/CAPABILITY-DECISIONS.md "
        "BD-02's Supersession note records that D-01 supersedes it on the main line and is "
        "the authority where the two disagree. Editing the canon instead would have "
        "destroyed the original design record to make a checker green.",
    ),
    (
        ".planning/phases/",
        "Dated per-phase planning records: what was intended and believed at a point in "
        "time, not live authority. THIS EXCLUSION IS BROAD AND THE BREADTH IS DELIBERATE -- "
        "it subsumes every closed prior-phase directory AND this phase's own plans, "
        "contexts and summaries, which quote the retired clause PRECISELY in order to "
        "describe its retirement. The tradeoff, stated honestly: a genuinely live authority "
        "document must never be filed here, because this gate will not read it. Live "
        "authority lives in docs/, src/, .planning/{PROJECT,ROADMAP,REQUIREMENTS,STATE}.md "
        "and .claude/CLAUDE.md -- all of which this gate DOES walk.",
    ),
    (
        ".planning/debug/resolved/",
        "Closed debug sessions: a record of what was diagnosed and when. Rewriting a "
        "resolved session destroys the audit trail that makes the diagnosis reviewable.",
    ),
    (
        ".planning/todos/completed/",
        "Closed todos, same reason. NOTE the deliberate asymmetry: "
        ".planning/todos/pending/ is NOT excluded, because a pending todo is live work and "
        "one of them carried a real site (R21).",
    ),
    (
        ".planning/research/",
        "Dated research passes. Their value is that they show what the evidence looked "
        "like at the time, including where it was later corrected.",
    ),
    (
        "artifacts/",
        "Archived and signed builds. Their bytes are pinned by MANIFEST digests, so "
        "rewriting one would additionally invalidate docs/manifest_check.py -- the record "
        "would be corrupted twice over.",
    ),
    (
        ".git/",
        "Version control internals: object storage, not authored text.",
    ),
    (
        "docs/retired_clause_check.py",
        "This gate's own source, which necessarily holds the pattern list it searches for. "
        "Without this entry the gate reports itself and can never be green.",
    ),
)

# ---------------------------------------------------------------------------------------
# TIER 2 -- anchored per-site entries: (path, distinguishing substring, reason).
#
# For a LIVE occurrence deliberately spared. Anchored on CONTENT, never on a line number --
# every anchor in this phase has shifted at least once, several of them twice.
#
# SEEDED EMPTY, and that is a finding rather than an oversight: after plan 16-05's tasks 1
# and 2, no live occurrence needed sparing. Any future entry must carry a written reason
# here, in this constant, where a reader can see what was spared and why.
# ---------------------------------------------------------------------------------------
ALLOWED_SITES: tuple[tuple[str, str, str], ...] = ()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def allowed_by_prefix(relative: str) -> bool:
    return any(relative == prefix or relative.startswith(prefix)
               for prefix, _reason in ALLOWED_PREFIXES)


def allowed_by_site(relative: str, line: str) -> bool:
    return any(relative == path and anchor in line
               for path, anchor, _reason in ALLOWED_SITES)


def family_c_hit(lines: list[str], index: int) -> bool:
    """`strictly positive` counts only with a dim-target mention within +/-6 lines."""
    if FAMILY_C_PHRASE not in lines[index].lower():
        return False
    low = max(0, index - FAMILY_C_WINDOW)
    high = min(len(lines), index + FAMILY_C_WINDOW + 1)
    window = " ".join(lines[low:high]).lower()
    return any(anchor in window for anchor in FAMILY_C_ANCHORS)


def scan_repository() -> list[tuple[str, int, str, str]]:
    """Every surviving occurrence in every live file: (path, line number, pattern, text).

    EVERY one, never the first. This class was under-fixed four times by correcting what
    was visible and re-measuring afterwards; a gate that stopped at the first hit would
    cost one full pass per site and reproduce that loop exactly.
    """
    found: list[tuple[str, int, str, str]] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if allowed_by_prefix(relative):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue  # binary or unreadable: carries no authored prose to assert anything
        for index, line in enumerate(lines):
            low = line.lower()
            pattern = next((p for p in FAMILY_A + FAMILY_B if p in low), None)
            if pattern is None and family_c_hit(lines, index):
                pattern = FAMILY_C_PHRASE
            if pattern is None or allowed_by_site(relative, line):
                continue
            found.append((relative, index + 1, pattern, line.strip()))
    return found


def check_no_survivors() -> int:
    """INVARIANT 1 -- no live file still asserts the retired clause."""
    survivors = scan_repository()
    if survivors:
        report = "\n".join(
            f"  {path}:{number}  [{pattern}]  {text[:150]}"
            for path, number, pattern, text in survivors
        )
        raise AssertionError(
            f"{len(survivors)} live occurrence(s) of the retired brightness-floor clause "
            f"survive, in {len({p for p, _, _, _ in survivors})} file(s):\n{report}\n"
            f"  Correct each one by CITING where the clause lived -- BD-02's original "
            f"Decision paragraph, or canonical strategy Sec 21 -- and never by restating "
            f"it. An amendment that quotes what it supersedes is itself a surviving "
            f"occurrence and this gate reports it as one. If an occurrence is deliberate, "
            f"add it to ALLOWED_SITES with a written reason."
        )
    return len(ALLOWED_PREFIXES)


def fenced_config(text: str) -> dict:
    """The fenced Config JSON in src/CONFIG-BLOCK.md, parsed as JSON rather than matched."""
    block = re.search(r"```json(.+?)```", text, re.S)
    require(
        block is not None,
        f"{CONFIG_BLOCK} no longer contains a fenced json block -- that block is the file's "
        f"own declared transcription source, so losing it silently removes the only thing "
        f"invariant 2 can compare the build against",
    )
    return json.loads(block.group(1))


def check_record_matches_build() -> dict:
    """INVARIANT 2 -- the transcription source agrees with what actually shipped.

    src/CONFIG-BLOCK.md's header calls its fenced block "the transcription source, not a
    description of one". So a drift between it and the built forks is not a stale note; it
    is the record telling a reader something false about the build. That drift is exactly
    what four enumeration passes failed to catch by reading, and it is mechanical -- so it
    is asserted here instead.

    PINS THE AGREEMENT, NOT THE VALUES. `brightness_floor` and `dim_target` are tuning
    values and may legitimately move again; what may never happen is the record and the
    build disagreeing about them. A check that hard-coded 0 would have to be edited (and
    would probably be deleted) the next time they change.
    """
    keys = ("brightness_floor", "dim_target")
    source = ROOT / CONFIG_BLOCK
    require(source.is_file(), f"{CONFIG_BLOCK} does not exist")
    record = fenced_config(source.read_text(encoding="utf-8")).get("safety", {})
    for key in keys:
        require(key in record, f"{CONFIG_BLOCK}'s fenced Config JSON has no safety.{key}")

    for fork in FORKS:
        artifact = ROOT / f"src/PROSOCHE-{fork}.xml"
        require(artifact.is_file(), f"{artifact} does not exist")
        built = config_literal(
            plistlib.loads(artifact.read_bytes())["WFWorkflowActions"]
        ).get("safety", {})
        for key in keys:
            require(key in built, f"{fork}: the built Config literal has no safety.{key}")
            require(
                built[key] == record[key],
                f"{fork}: the built Config literal has safety.{key} = {built[key]!r} but "
                f"{CONFIG_BLOCK}'s fenced JSON -- which that file calls the transcription "
                f"source, not a description of one -- says {record[key]!r}. The record and "
                f"the build disagree about a safety value; fix the record, or rebuild, but "
                f"do not leave them apart",
            )
    return {key: record[key] for key in keys}


def main() -> None:
    tiers = check_no_survivors()
    agreed = check_record_matches_build()
    values = ", ".join(f"{key}={value!r}" for key, value in agreed.items())
    print(
        f"retired clause check: passed -- 0 live lexical occurrences "
        f"({tiers} allowlisted path prefixes, {len(ALLOWED_SITES)} anchored sites); "
        f"{CONFIG_BLOCK} agrees with both built forks on {values} "
        f"[LEXICAL ONLY: this is not proof the class is empty -- see BLIND SPOT in this "
        f"file's source]"
    )


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"retired clause check: FAILED -- {error}", file=sys.stderr)
        raise SystemExit(1)
