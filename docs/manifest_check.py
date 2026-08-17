#!/usr/bin/env python3
"""Prove that `artifacts/shortcuts/MANIFEST.md` describes the artifacts that actually exist.

Why this file exists, stated plainly so nobody has to reconstruct it from git:

`MANIFEST.md` is the only human-readable claim this repository makes about **what shipped**.
Every other check in `docs/` inspects `src/` or the generator -- none of them looks at the
signed `.shortcut` files a person would actually import, and none of them notices when the
manifest's rows drift away from those files.  A stale row is not a cosmetic defect: it is a
false provenance claim, and it makes "which build is on my phone" unanswerable after the
fact.  Phase 10's research measured three of the six rows already wrong before this phase
began, which is exactly the failure mode this script exists to make impossible to repeat.

What it asserts, per row of the manifest's table:

  * the declared path exists;
  * its real size on disk equals the declared byte count;
  * its real SHA-256 equals the declared hash.

And across the table as a whole:

  * each fork has at least one source, one dated archive and one signed row;
  * both signed rows name files whose basenames are exactly the two canonical display
    names plus `.shortcut`, with **no suffix of any kind**.

That last one is `DIST-04` expressed as a check rather than as prose.  It matters more than
it looks: a signed artifact carries **no** display name inside it.  Measured this phase by
decrypting both containers -- the AEA1 auth-data plist holds only `SigningCertificateChain`,
and the recovered `Shortcut.wflow` has had its `WFWorkflowName` key **stripped** by the
signer, even though both `src/*.xml` files carry it.  The display name therefore lives in
the filename and nowhere else, so a `_signed`-suffixed file imports as a second, differently
named library entry that the user's two Personal Automations do not reference -- a silently
dead install.

Sizes and hashes are computed here in Python with `pathlib` and `hashlib` rather than by
shelling out to `stat` / `shasum`, so this script behaves identically on any machine and
spawns no child process at all.  Files are read as UTF-8 and paths are compared as text: the product
name contains `Ē` and an em dash, and normalising either would silently mask a real mismatch.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts/shortcuts/MANIFEST.md"

# The two canonical display names, from which the only two acceptable signed basenames
# follow.  DIST-04: the signed filename must equal the intended library name exactly.
DISPLAY_NAMES = [
    "PROSOCHĒ — Nine Circles — Core",
    "PROSOCHĒ — Nine Circles — Aware",
]
SIGNED_BASENAMES = {f"{name}.shortcut" for name in DISPLAY_NAMES}

# Row labels are `<Fork> <kind>`; the kind vocabulary the table uses.
KINDS = ("source", "archive", "signed")

CELL_FENCE = re.compile(r"^`(.*)`$")


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def unfence(cell: str) -> str:
    """Strip one layer of backtick fencing from a table cell, if present."""
    cell = cell.strip()
    match = CELL_FENCE.match(cell)
    return match.group(1) if match else cell


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            sha.update(chunk)
    return sha.hexdigest()


def rows(text: str) -> list[tuple[str, str, int, str]]:
    """Every data row of the manifest's pipe-delimited table.

    Returns (label, path, declared_bytes, declared_sha256).  Header and alignment rows are
    skipped by shape, not by line number, so the table can move within the document.
    """
    found = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 4:
            continue
        label, path_cell, size_cell, hash_cell = cells
        if set(size_cell) <= set("-: ") or label.lower().startswith("fork"):
            continue  # header or alignment row
        size_text = unfence(size_cell).replace(",", "")
        require(size_text.isdigit(), f"row {label!r}: byte count {size_cell!r} is not a number")
        found.append((label, unfence(path_cell), int(size_text), unfence(hash_cell)))
    return found


def main() -> None:
    require(MANIFEST.is_file(), f"{MANIFEST} does not exist")
    table = rows(MANIFEST.read_text(encoding="utf-8"))
    require(bool(table), "MANIFEST.md contains no parseable artifact rows")

    for label, path_text, declared_size, declared_hash in table:
        path = ROOT / path_text
        require(path.is_file(), f"row {label!r}: {path_text} does not exist")
        actual_size = path.stat().st_size
        require(
            actual_size == declared_size,
            f"row {label!r}: MANIFEST declares {declared_size} bytes, {path_text} is "
            f"{actual_size} bytes",
        )
        actual_hash = digest(path)
        require(
            actual_hash == declared_hash,
            f"row {label!r}: MANIFEST declares SHA-256 {declared_hash}, {path_text} hashes "
            f"to {actual_hash}",
        )

    # Coverage: every fork needs a source, an archive and a signed row.
    labels = [label for label, _, _, _ in table]
    for name in DISPLAY_NAMES:
        fork = name.rsplit("—", 1)[-1].strip()  # "Dumb" / "Sentient"
        for kind in KINDS:
            require(
                any(label.startswith(fork) and kind in label.lower() for label in labels),
                f"MANIFEST has no {kind!r} row for the {fork} fork",
            )

    # DIST-04: signed rows must name the canonical display names, with no added suffix.
    signed = [path_text for label, path_text, _, _ in table if "signed" in label.lower()]
    require(len(signed) == 2, f"expected exactly 2 signed rows, found {len(signed)}: {signed}")
    for path_text in signed:
        basename = Path(path_text).name
        require(
            basename in SIGNED_BASENAMES,
            f"signed artifact {basename!r} is not one of the two canonical display names "
            f"{sorted(SIGNED_BASENAMES)} -- a suffixed name imports as a separate library "
            f"entry the Personal Automations do not reference (DIST-04)",
        )

    print(f"manifest check: passed ({len(table)} rows verified against disk)")


if __name__ == "__main__":
    main()
