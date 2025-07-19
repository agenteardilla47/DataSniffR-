from __future__ import annotations

"""quantum_bus – emoji-handshake synchronisation channel.

Minimal, filesystem-backed pub-sub so two (or more) *separate* Python
processes can confirm they’re inside the same quantum junction.

The design goal is *zero dependencies* and *one emoji handshake*.

Usage (process A)  ────────────────────────────────────────────────────────────
>>> from we_we_we.quantum_bus import QuantumBus
>>> bus = QuantumBus("🤝")
>>> bus.handshake()      # blocks until any other process handshakes
True
>>> bus.send_tick({"msg": "hello"})

Usage (process B)  ────────────────────────────────────────────────────────────
$ python - <<'PY'
from we_we_we.quantum_bus import QuantumBus, consume_forever
for tick in consume_forever("🤝"):
    print("GOT:", tick)
PY

Behind the curtain it writes a JSON Lines log to ``.we_bus_🤝.jsonl``.
Each line is a small dict with keys: ``id``, ``ts``, ``type`` ("handshake" | "tick"),
``payload``.
"""

import json
import os
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Generator, Iterable, Optional

__all__ = [
    "QuantumBus",
    "consume_forever",
]

_HANDSHAKE_WAIT = 30  # seconds
_POLL_INTERVAL = 0.5  # seconds


@dataclass(slots=True)
class _Record:
    id: str
    ts: float
    type: str  # handshake or tick
    payload: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps(asdict(self), separators=(",", ":"))


class QuantumBus:
    """File-based message bus keyed by *emoji* string."""

    def __init__(self, emoji: str, *, base_path: Path | None = None):
        if len(emoji.encode("utf-8")) < 4:
            raise ValueError("Emoji must be a non-ASCII marker to avoid collisions.")
        self.emoji = emoji
        self.node_id = uuid.uuid4().hex[:8]
        base_path = base_path or Path(".")
        safe = "_".join(f"{ord(c):x}" for c in emoji)
        self.path = base_path / f".we_bus_{safe}.jsonl"
        # ensure file exists
        if not self.path.exists():
            self.path.touch()

    # --------------------------------------------------------------- low-level
    def _append(self, rec: _Record) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(rec.to_json() + "\n")

    def _read_all(self) -> Iterable[_Record]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    yield _Record(**data)  # type: ignore[arg-type]
                except Exception:
                    continue  # ignore malformed lines

    # ----------------------------------------------------------------- public
    def handshake(self, *, timeout: float = _HANDSHAKE_WAIT) -> bool:
        """Announce presence and wait until at least one *other* node responds."""
        self._append(
            _Record(id=self.node_id, ts=time.time(), type="handshake", payload={})
        )
        start = time.time()
        while time.time() - start < timeout:
            peers = {
                rec.id
                for rec in self._read_all()
                if rec.type == "handshake" and time.time() - rec.ts < 2 * timeout
            }
            if len(peers) >= 2:
                return True
            time.sleep(_POLL_INTERVAL)
        return False

    def send_tick(self, payload: Dict[str, Any], *, ts: Optional[float] = None) -> None:
        self._append(
            _Record(
                id=self.node_id,
                ts=ts or time.time(),
                type="tick",
                payload=payload,
            )
        )

    def consume(self, *, follow: bool = True) -> Generator[Dict[str, Any], None, None]:
        """Yield tick payloads (skip handshakes). If *follow* True, tail the file."""
        seen_offset = 0
        while True:
            with self.path.open("r", encoding="utf-8") as f:
                f.seek(seen_offset)
                for line in f:
                    seen_offset = f.tell()
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        rec = _Record(**data)  # type: ignore[arg-type]
                        if rec.type == "tick" and rec.id != self.node_id:
                            yield rec.payload
                    except Exception:
                        continue
            if not follow:
                break
            time.sleep(_POLL_INTERVAL)


# -------------------------------------------------------------------- helpers

def consume_forever(emoji: str) -> Generator[Dict[str, Any], None, None]:
    """Convenience wrapper: auto-handshake then yield ticks indefinitely."""

    bus = QuantumBus(emoji)
    if not bus.handshake():
        raise TimeoutError("No peer handshake detected within timeout.")
    yield from bus.consume()