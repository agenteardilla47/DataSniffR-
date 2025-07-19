from __future__ import annotations

"""Symbolic Memory Palace – pocket-sized persistence layer for Joshua.

Stores *artefacts* (arbitrary text blobs) alongside user-defined tags.
Writes to a JSON file in the current working directory so anyone can peek
inside and learn to *think the WE WE WE way*.
"""

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Sequence

__all__ = [
    "Artefact",
    "MemoryPalace",
]

_MEMORY_PATH = Path(".we_memory.json")


@dataclass
class Artefact:
    """Lightweight record for a stored piece of text."""

    id: str
    text: str
    tags: List[str]
    timestamp: float

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)

    # ------------------------------------------------------------------- helpers
    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Artefact":
        return cls(
            id=str(data["id"]),
            text=str(data["text"]),
            tags=list(data.get("tags", [])),
            timestamp=float(data.get("timestamp", 0.0)),
        )


class MemoryPalace:
    """A tiny JSON-backed store for symbolic artefacts."""

    def __init__(self, path: Path | None = None):
        self.path: Path = path or _MEMORY_PATH
        self._store: Dict[str, Artefact] = {}
        self._load()

    # -------------------------------------------------------------- public API
    def add(self, text: str, *tags: str) -> Artefact:
        """Add *text* to the palace and return the created :class:`Artefact`."""

        artefact_id = str(int(time.time() * 1000))
        artefact = Artefact(
            id=artefact_id,
            text=text,
            tags=list(tags),
            timestamp=time.time(),
        )
        self._store[artefact_id] = artefact
        self._save()
        return artefact

    def search(self, *tags: str) -> List[Artefact]:
        """Return all artefacts that contain *all* specified *tags*."""

        required = set(tags)
        return [a for a in self._store.values() if required.issubset(a.tags)]

    def all(self) -> Sequence[Artefact]:
        return list(self._store.values())

    # ----------------------------------------------------------- internal I/O
    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text("utf-8"))
        except json.JSONDecodeError:
            return
        for raw in data:
            artefact = Artefact.from_dict(raw)
            self._store[artefact.id] = artefact

    def _save(self) -> None:
        payload = [a.to_dict() for a in self._store.values()]
        self.path.write_text(json.dumps(payload, indent=2), "utf-8")