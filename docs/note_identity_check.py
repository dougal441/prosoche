#!/usr/bin/env python3
"""Prove the Control Room Note's three identity sites agree, and that no attachment range has drifted.

TWO INVARIANTS, ONE FILE, because they fail together.

**Note identity.** PROSOCHĒ finds its Note by NAME.  Three separate places in each fork spell
that name, and nothing in the repository makes them agree: the Find Notes predicate that
looks the Note up, the H1 heading a user reads at the top of the body, and the `name`
parameter of the Create Note action that actually sets the title.  If the predicate and the
title drift apart, PROSOCHĒ silently creates a second Note on every state-changing run and
the user's ledger stops accumulating anywhere they can see it -- with no error, on device or
in any check.  Asserting all three against ONE constant is what makes plan 11-03's rename a
one-line edit instead of a three-site hunt.

**Attachment offsets.** A `WFTextTokenString` carries absolute character offsets in its
`attachmentsByRange` keys, each pointing at a `￼` (U+FFFC) placeholder in its own `string`.
Any text edit upstream of a placeholder moves it, and `.claude/CLAUDE.md` §5 records the
consequence of not recomputing: an out-of-bounds range CAN CRASH SHORTCUTS ON IMPORT.  The
Note body is the largest hand-held string in the artifact and the one this phase edits most,
so the invariant is armed HERE, before any Note copy is touched, and it is checked across the
WHOLE document rather than only at the three sites above -- a checker that only looked where
it expected damage would not have caught the class.

Both invariants are STRUCTURAL.  `DIST-03` (device verification) is open: no iPhone has been
connected, so nothing this file asserts is evidence that the Note is found, created or read
correctly at runtime.  It is evidence that the file says what it is supposed to say.

Read-only: parses both built artifacts with plistlib.  No subprocess, no rebuild.
"""
from __future__ import annotations

import plistlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORKS = ("Dumb", "Sentient")

# The Note's USER-FACING title, and the single line plan 11-03 changes to the bare product
# name.  "Control Room" remains the INTERNAL name everywhere in code and docs -- menu items,
# variable names, comment markers, function names, prose -- settled by commit `e84ee77`
# ("the codebase and docs continue to call it the Control Room").  Only the three sites
# asserted below are user-facing, and only they move.
EXPECTED_TITLE = "PROSOCHĒ — Control Room"

# The Find Notes predicate's current comparison on the `Name` property.  99 is "contains".
# Recorded as an assertion rather than ignored because RESEARCH §6.2 proposes moving it to 4
# ("string is") in the same edit that shortens the title: under `contains`, a shortened title
# would also match a leftover Note from an earlier install, and with a limit of 1 plus First
# Item, PROSOCHĒ would bind to the wrong Note and append its ledger there forever.  Pinning
# the value here makes that move a deliberate, visible edit instead of a silent one.
EXPECTED_NAME_OPERATOR = 99

# Identifiers, matching `docs/router_ui_census.py:40-42`.
FIND_NOTES = "is.workflow.actions.filter.notes"
CREATE_NOTE = "com.apple.mobilenotes.SharingExtension"
GETTEXT = "is.workflow.actions.gettext"

# The Note body is located by two of its own headings, never by index.
BODY_HEADING_PREFIX = "# "
BODY_ANCHOR = "## READ THIS FIRST"

PLACEHOLDER = "￼"
RANGE_KEY = re.compile(r"^\{\s*(\d+)\s*,\s*(\d+)\s*\}$")

# Measured at the phase-11 baseline (`ae0226c`) and re-measured on the decrypted payload of
# both signed containers.  A DROP below this floor means token strings were replaced by bare
# `WFTextTokenAttachment` values -- parameter-defect axis 2, which resolves to empty text at
# runtime while validating and importing cleanly.
MINIMUM_TOKEN_STRINGS = 775


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def sole(matches: list, description: str):
    """The single item matching a content-based search.

    Exactly one, never the first of several: a duplicate Note-identity site is precisely the
    defect this file exists to expose, and taking `[0]` would hide it behind a passing run.
    """
    require(
        len(matches) == 1,
        f"expected exactly 1 {description}, found {len(matches)} -- zero means the site moved "
        f"and this check is now asserting nothing; more than one means two places can spell "
        f"the Note's identity differently and PROSOCHĒ would bind to whichever it reached first",
    )
    return matches[0]


def token_body(value):
    """The `{string, attachmentsByRange}` dict inside a `WFTextTokenString`, or None."""
    if isinstance(value, dict) and value.get("WFSerializationType") == "WFTextTokenString":
        inner = value.get("Value")
        if isinstance(inner, dict) and isinstance(inner.get("string"), str):
            return inner
    return None


def parameters(item) -> dict:
    return item.get("WFWorkflowActionParameters", {}) if isinstance(item, dict) else {}


def walk(node):
    """Every nested dict in the document, in document order."""
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def range_offsets(attachments: dict, where: str) -> list[int]:
    found = []
    for key in attachments:
        match = RANGE_KEY.match(key)
        require(
            match is not None,
            f"{where}: attachmentsByRange key {key!r} is not a '{{offset, length}}' range -- an "
            f"unparseable key cannot be recomputed after a text edit, so it would survive one "
            f"unchanged and could point out of bounds",
        )
        found.append(int(match.group(1)))
    return sorted(found)


def placeholder_offsets(string: str) -> list[int]:
    return [index for index, character in enumerate(string) if character == PLACEHOLDER]


def name_filter_row(action, fork: str) -> dict:
    """The Find Notes predicate row that filters on the `Name` property."""
    templates = parameters(action).get("WFContentItemFilter", {}).get("Value", {}) \
        .get("WFActionParameterFilterTemplates", [])
    require(
        isinstance(templates, list) and templates,
        f"{fork}: the Find Notes action carries no filter templates -- with no predicate it "
        f"returns every Note on the device and First Item binds to an arbitrary one",
    )
    return sole([row for row in templates if row.get("Property") == "Name"],
                f"{fork}: Find Notes predicate row filtering on Property 'Name'")


def check_identity(actions, fork: str) -> None:
    """The three sites that spell the Note's identity, each located by content."""
    # 1. The lookup predicate -- how PROSOCHĒ finds the Note at all.
    row = name_filter_row(sole([item for item in actions
                                if item.get("WFWorkflowActionIdentifier") == FIND_NOTES],
                               f"{fork}: {FIND_NOTES} action"), fork)
    predicate = token_body(row.get("Values", {}).get("String"))
    require(
        predicate is not None,
        f"{fork}: the Find Notes 'Name' row's value is not a WFTextTokenString -- a bare "
        f"attachment in a string-typed slot resolves to empty at runtime (parameter-defect "
        f"axis 2), so the predicate would match every Note",
    )
    require(
        predicate["string"] == EXPECTED_TITLE,
        f"{fork}: Find Notes looks up {predicate['string']!r}, but the Note is titled "
        f"{EXPECTED_TITLE!r} -- a predicate that does not match the title makes PROSOCHĒ "
        f"create a fresh Note on every state-changing run and the user's ledger accumulates "
        f"nowhere they can see it",
    )
    require(
        row.get("Operator") == EXPECTED_NAME_OPERATOR,
        f"{fork}: the Find Notes 'Name' row uses Operator {row.get('Operator')!r}, not the "
        f"recorded {EXPECTED_NAME_OPERATOR!r} -- changing how the title is matched changes "
        f"which Notes can collide with it, so it must be a deliberate edit to this constant "
        f"and not a side effect of a copy change",
    )

    # 2. The H1 a user reads at the top of the body.
    body = sole([token_body(parameters(item).get("WFTextActionText")) for item in actions
                 if item.get("WFWorkflowActionIdentifier") == GETTEXT
                 and (token_body(parameters(item).get("WFTextActionText")) or {})
                 .get("string", "").startswith(BODY_HEADING_PREFIX)
                 and BODY_ANCHOR in (token_body(parameters(item).get("WFTextActionText")) or {})
                 .get("string", "")],
                f"{fork}: Control Room Note body (a {GETTEXT} whose text opens with "
                f"{BODY_HEADING_PREFIX!r} and contains {BODY_ANCHOR!r})")
    heading = body["string"].splitlines()[0]
    require(
        heading == BODY_HEADING_PREFIX + EXPECTED_TITLE,
        f"{fork}: the Note body's H1 is {heading!r}, not "
        f"{BODY_HEADING_PREFIX + EXPECTED_TITLE!r} -- the heading is the only place a user "
        f"can confirm they are reading the right Note, so a stale one makes a wrong-Note "
        f"binding invisible to them",
    )

    # 3. The parameter that actually sets the title.
    title = parameters(sole([item for item in actions
                             if item.get("WFWorkflowActionIdentifier") == CREATE_NOTE],
                            f"{fork}: {CREATE_NOTE} action")).get("name")
    require(
        isinstance(title, str),
        f"{fork}: Create Note's 'name' is {type(title).__name__}, not a plain str -- the "
        f"catalog types it as a plain string and any other envelope is ignored, leaving the "
        f"Note untitled and unfindable by the predicate above",
    )
    require(
        title == EXPECTED_TITLE,
        f"{fork}: Create Note titles the Note {title!r}, but the predicate looks up "
        f"{EXPECTED_TITLE!r} -- the two must be changed in the same commit or PROSOCHĒ "
        f"creates a Note it can never find again",
    )


def check_offsets(document, fork: str) -> int:
    """Every WFTextTokenString in the whole document, not only the three sites above."""
    counted = 0
    for node in walk(document):
        string = node.get("string")
        attachments = node.get("attachmentsByRange")
        if not isinstance(string, str) or not isinstance(attachments, dict):
            continue
        counted += 1
        declared = range_offsets(attachments, f"{fork}: token string #{counted}")
        actual = placeholder_offsets(string)
        require(
            declared == actual,
            f"{fork}: token string #{counted} declares attachment offsets {declared} but its "
            f"U+FFFC placeholders sit at {actual} -- a range that does not land on a "
            f"placeholder points into unrelated prose, and an out-of-bounds range can crash "
            f"Shortcuts on import",
        )
    require(
        counted >= MINIMUM_TOKEN_STRINGS,
        f"{fork}: only {counted} WFTextTokenString values found, below the measured floor of "
        f"{MINIMUM_TOKEN_STRINGS} -- a drop means string-typed parameters were converted to "
        f"bare WFTextTokenAttachment values, which validate and import cleanly and then "
        f"resolve to empty text at runtime (parameter-defect axis 2)",
    )
    return counted


def main() -> None:
    for fork in FORKS:
        source = ROOT / f"src/PROSOCHE-{fork}.xml"
        require(source.is_file(), f"{source} does not exist")
        document = plistlib.loads(source.read_bytes())
        check_identity(document["WFWorkflowActions"], fork)
        counted = check_offsets(document, fork)
        print(f"note identity check: {fork} -- three identity sites agree on "
              f"{EXPECTED_TITLE!r} (Name operator {EXPECTED_NAME_OPERATOR}), "
              f"{counted} token strings, 0 attachment-offset mismatches [structural only; "
              f"DIST-03 open]")


if __name__ == "__main__":
    main()
