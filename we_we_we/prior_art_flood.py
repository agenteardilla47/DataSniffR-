from __future__ import annotations

"""prior_art_flood – one-click dump of remixed artefacts as immutable prior art.

This tool copies every artefact tagged ``remixed`` into ``prior_art/``
(where each file name is ``<artefact_id>.json``).  In real deployments this
could push to IPFS/Arweave; here we just create the folder so diff is visible.
"""

import json
from pathlib import Path

from .memory_palace import MemoryPalace

__all__ = ["dump_prior_art"]


def dump_prior_art(out_dir: Path | str = "prior_art") -> int:
    out_path = Path(out_dir)
    out_path.mkdir(exist_ok=True)

    palace = MemoryPalace()
    count = 0
    for art in palace.all():
        if "remixed" in art.tags:
            dest = out_path / f"{art.id}.json"
            dest.write_text(json.dumps(art.to_dict(), indent=2), "utf-8")
            count += 1
    return count