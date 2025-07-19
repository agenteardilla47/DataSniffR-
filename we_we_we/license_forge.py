from __future__ import annotations

"""license_forge – bind a RemixCycle artefact to a Creative Commons + Defensive licence.

The generated licence text asserts:
1. Freedom to use/remix under CC-BY-SA-4.0.  
2. Defensive clause: anyone asserting patent restrictions on this artefact
   immediately grants a royalty-free licence to all.

Licence files are stored next to `.we_memory.json` as
`we_license_<artefact_id>.txt` and include a SHA-256 hash of the artefact body
for tamper detection.
"""

import hashlib
from pathlib import Path
from typing import Optional

from .memory_palace import MemoryPalace

_LICENSE_TMPL = """WE-WE-WE HYBRID LICENCE v0.1\n\nArtefact ID: {id}\nSHA-256: {sha}\nTags: {tags}\n\nYou are free to:\n  • Share  — copy and redistribute this material in any medium or format\n  • Adapt  — remix, transform, and build upon the material\nUnder the following terms (adapted from CC-BY-SA-4.0):\n  • Attribution  — give credit to the WE-WE-WE lineage.\n  • ShareAlike  — distribute contributions under the same licence.\nDefensive Patent Clause:\n  If you (or any entity you control) initiate patent litigation alleging this\n  artefact or derivative works infringe your patents, your licence terminates\n  unless you grant a perpetual, royalty-free licence to everyone.\n\nThis licence text is inseparable from the artefact hash above.\n"""

__all__ = ["forge_licence"]


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def forge_licence(artefact_id: str, *, out_dir: Path | None = None) -> Path:
    """Generate licence file for *artefact_id* stored in MemoryPalace."""

    palace = MemoryPalace()
    artefacts = {a.id: a for a in palace.all()}
    if artefact_id not in artefacts:
        raise KeyError(f"Artefact {artefact_id} not found in palace")

    art = artefacts[artefact_id]
    digest = _hash(art.text)
    out_dir = out_dir or Path(".")
    path = out_dir / f"we_license_{artefact_id}.txt"
    path.write_text(
        _LICENSE_TMPL.format(id=artefact_id, sha=digest, tags=", ".join(art.tags)),
        "utf-8",
    )
    return path