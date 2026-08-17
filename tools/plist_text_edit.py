#!/usr/bin/env python3
"""Guarded plistlib round-trip for editing text inside a Shortcuts plist.

WHY THIS FILE EXISTS.  A `WFTextTokenString` carries ABSOLUTE character offsets in its
`attachmentsByRange` keys, each one pointing at a `￼` (U+FFFC OBJECT REPLACEMENT
CHARACTER) placeholder in its own `string`.  Editing that string with a plain text
substitution on the XML leaves every downstream key reading its OLD offset, so the shipped
plist carries ranges pointing into the middle of unrelated prose.  `.claude/CLAUDE.md` §5
records the consequence: an out-of-bounds range CAN CRASH SHORTCUTS ON IMPORT.  There is no
validator, no ToolKit lookup and no decryption pass that catches it -- the file is
structurally valid the whole way to the device.

Quick task `260817-au7` established the working method and proved it on a 6,210-character
note body with two attachments, but left it as prose in `docs/BUILD-NOTES.md` §20 with no
script behind it.  This module is that method, executable.  The six steps, in order:

  1. Prove a no-op `plistlib.dumps(data, fmt=FMT_XML, sort_keys=False)` is byte-identical to
     the source  ->  `assert_noop_roundtrip()`.  This licenses every later structured edit
     and keeps the resulting diff free of reformatting noise.
  2. Assert the OLD `attachmentsByRange` keys equal the OLD placeholder offsets
     ->  `assert_offsets_match()`, called for you by `replace_in_token()`.
  3. Apply the text replacement                  ->  `replace_in_token()` / `replace_in_plain()`.
  4. Rebuild `attachmentsByRange` from the NEW placeholder offsets in document order
     ->  `replace_in_token()`.
  5. Assert the replacement text introduces no new placeholder  ->  `replace_in_token()`.
  6. `plutil -lint` the file, then re-verify offsets in BOTH forks after the Sentient
     rebuild  ->  the caller's job; `docs/note_identity_check.py` is the standing assertion.

Standard library only -- `plistlib`, `pathlib`, `re`.  No third-party import, by design:
this module is a build-time dependency of a project whose whole output is one XML file.

Failure convention follows `tools/build_state_engine.py`'s `verify_*` family: every guard
raises `SystemExit` with a message naming the CONSEQUENCE, not merely the fact.
"""
from __future__ import annotations

import plistlib
import re
from pathlib import Path

# The single character a `WFTextTokenString` uses to stand in for an embedded variable.
# Exactly one character wide, which is why every `attachmentsByRange` key has length 1.
PLACEHOLDER = "￼"

# `attachmentsByRange` keys are literally `{<offset>, <length>}` strings, e.g. `{5478, 1}`.
RANGE_KEY = re.compile(r"^\{\s*(\d+)\s*,\s*(\d+)\s*\}$")


def _body(token: dict) -> dict:
    """The dict that actually holds `string` / `attachmentsByRange`.

    Accepts either the inner value dict or the full `{WFSerializationType, Value}` envelope,
    because both shapes occur in this artifact and confusing them is a silent no-op rather
    than an error.
    """
    if isinstance(token, dict) and "string" not in token and isinstance(token.get("Value"), dict):
        return token["Value"]
    return token


def _key_offset(key: str) -> int:
    match = RANGE_KEY.match(key)
    if not match:
        raise SystemExit(
            f"attachmentsByRange key {key!r} is not a '{{offset, length}}' range -- an "
            "unparseable key cannot be recomputed after a text edit, and shipping it "
            "unchanged risks an out-of-bounds range that can crash Shortcuts on import")
    return int(match.group(1))


def load(path) -> tuple[object, bytes]:
    """Parse a plist and return `(data, original_bytes)`.

    The original bytes are returned, not re-read later, so `assert_noop_roundtrip()` compares
    against exactly what was parsed.
    """
    raw = Path(path).read_bytes()
    return plistlib.loads(raw), raw


def assert_noop_roundtrip(data, original_bytes: bytes) -> None:
    """Step 1.  Fail unless re-serialising the parsed data reproduces the source byte for byte.

    Until this holds, no structured edit is safe to attribute: any later diff would mix the
    intended change with plistlib's own formatting, and a reviewer could not tell which
    bytes were meant.
    """
    rendered = plistlib.dumps(data, fmt=plistlib.FMT_XML, sort_keys=False)
    if rendered != original_bytes:
        raise SystemExit(
            f"no-op plistlib round trip is NOT byte-identical ({len(original_bytes)} bytes in, "
            f"{len(rendered)} out) -- editing through this module would rewrite unrelated "
            "formatting, so the resulting diff could not be attributed to the intended change "
            "and a real defect could hide inside the noise")


def assert_offsets_match(token: dict) -> None:
    """Step 2 / step 6.  Fail unless every range key points at a real placeholder.

    Compares the leading integer of each `attachmentsByRange` key against the character
    offsets of U+FFFC in the token's own `string`, both in document order.
    """
    body = _body(token)
    string = body.get("string")
    if not isinstance(string, str):
        raise SystemExit(
            "assert_offsets_match() was handed a value with no 'string' key -- it is not a "
            "WFTextTokenString, and treating it as one would edit the wrong parameter")
    attachments = body.get("attachmentsByRange", {})
    declared = sorted(_key_offset(key) for key in attachments)
    actual = [index for index, character in enumerate(string) if character == PLACEHOLDER]
    if declared != actual:
        raise SystemExit(
            f"attachmentsByRange offsets {declared} do not match the U+FFFC offsets {actual} "
            "in the same string -- a range that does not land on a placeholder points into "
            "unrelated prose, and an out-of-bounds range can crash Shortcuts on import")


def replace_in_token(token: dict, old: str, new: str, *, expected_count: int) -> None:
    """Steps 2-5.  Replace text inside a `WFTextTokenString` and recompute its ranges.

    `expected_count` is not a convenience: an edit that matched fewer or more sites than
    intended is the exact shape of a silent partial rename, so the count is asserted before
    anything is written.
    """
    body = _body(token)
    assert_offsets_match(body)
    string = body["string"]
    found = string.count(old)
    if found != expected_count:
        raise SystemExit(
            f"expected {expected_count} occurrence(s) of {old!r} in this WFTextTokenString, "
            f"found {found} -- proceeding would leave a partial rename in which some sites "
            "carry the new name and some the old, which validates, signs and imports cleanly "
            "and is still wrong")
    if PLACEHOLDER in new:
        raise SystemExit(
            f"replacement text {new!r} contains a U+FFFC placeholder -- this module rebuilds "
            "attachmentsByRange from placeholder positions and has no attachment to bind a "
            "new one to, so the result would be a range with no owner")

    ordered = [body["attachmentsByRange"][key]
               for key in sorted(body.get("attachmentsByRange", {}), key=_key_offset)]
    body["string"] = string.replace(old, new)
    offsets = [index for index, character in enumerate(body["string"]) if character == PLACEHOLDER]
    if len(offsets) != len(ordered):
        raise SystemExit(
            f"placeholder count changed from {len(ordered)} to {len(offsets)} across the edit "
            "-- an attachment would be dropped or invented, and either leaves a variable slot "
            "that cannot resolve at runtime")
    body["attachmentsByRange"] = {f"{{{offset}, 1}}": value
                                  for offset, value in zip(offsets, ordered)}
    assert_offsets_match(body)


def replace_in_plain(action: dict, key: str, old: str, new: str, *, expected_count: int) -> None:
    """The same guarded replacement for a parameter whose value is a plain `str`.

    The Config JSON literal is one: `is.workflow.actions.gettext` -> `WFTextActionText`, a
    bare string with no token envelope, consumed at runtime by `detect.dictionary`.  It has
    no attachments to recompute, but it has exactly the same partial-rename hazard.
    """
    parameters = action.get("WFWorkflowActionParameters", {})
    value = parameters.get(key)
    if not isinstance(value, str):
        raise SystemExit(
            f"parameter {key!r} is {type(value).__name__}, not a plain str -- if it is a token "
            "envelope use replace_in_token() instead, because editing it as text would leave "
            "its attachmentsByRange offsets stale")
    found = value.count(old)
    if found != expected_count:
        raise SystemExit(
            f"expected {expected_count} occurrence(s) of {old!r} in {key!r}, found {found} -- "
            "proceeding would leave a partial rename that validates, signs and imports "
            "cleanly and is still wrong")
    parameters[key] = value.replace(old, new)


def save(path, data) -> None:
    """Exactly one serialisation and exactly one write, mirroring the generator's own `main()`."""
    Path(path).write_bytes(plistlib.dumps(data, fmt=plistlib.FMT_XML, sort_keys=False))


def find_action(actions, predicate):
    """The one action satisfying `predicate`, located by CONTENT and never by index.

    Action numbers shift on every rebuild, so an index is a stale address the moment the
    generator runs.  Exactly one match is required: a second match means the edit would be
    applied to an arbitrary one of two candidates, and a duplicate could hide behind it.
    """
    matches = [item for item in actions if predicate(item)]
    if len(matches) != 1:
        raise SystemExit(
            f"expected exactly 1 action matching the predicate, found {len(matches)} -- zero "
            "means the edit would silently apply to nothing, and more than one means it would "
            "apply to an arbitrary member of a set the caller did not know existed")
    return matches[0]
