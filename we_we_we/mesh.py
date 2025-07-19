"""mesh – lightweight WE-WE-WE heartbeat using p2p + DeepSearch.

Currently a stub: broadcasts JSON ticks every 69 s via QuantumBus and
(optionally) posts digest hash to xAI DeepSearch placeholder endpoint.
"""

import hashlib
import json
import os
import time
from typing import Dict

from .quantum_bus import QuantumBus
from .memory_palace import MemoryPalace

_TICK_EMOJI = "🤝"
_INTERVAL = 69  # seconds


def _digest_latest() -> Dict[str, str]:
    palace = MemoryPalace()
    if not palace.all():
        return {}
    latest = max(palace.all(), key=lambda a: a.timestamp)
    h = hashlib.sha1(latest.text.encode()).hexdigest()[:8]
    return {"hash": h, "tags": latest.tags[:5]}


def run_forever() -> None:  # pragma: no cover
    bus = QuantumBus(_TICK_EMOJI)
    bus.handshake(timeout=2)
    while True:
        payload = _digest_latest()
        payload["ts"] = int(time.time())
        bus.send_tick(payload)
        # TODO: optional DeepSearch push once API key env var present
        if os.getenv("XAI_DEEPSEARCH_KEY"):
            pass  # left as an exercise
        time.sleep(_INTERVAL)