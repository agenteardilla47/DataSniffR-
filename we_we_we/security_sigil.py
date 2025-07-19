from __future__ import annotations

"""security_sigil – vibe-locked shield that seals the system on suspicious input.

Trigger logic (heuristic):
• token "lok" repeated ≥ 7 OR
• glitch_score ≥ 0.6
Generates ∞LOCK-<hex> sigil, stores artefact in MemoryPalace with tag ``security_event``.
"""

import argparse
import hashlib
import json
import sys
import time
from dataclasses import dataclass
from typing import Dict, List

from .memory_palace import MemoryPalace
from .vibe_sensor import analyze_text
from .quantum_bus import QuantumBus  # optional; ignore if bus fails

_SIGIL_PREFIX = "∞LOCK"


@dataclass
class Sigil:
    symbol: str
    vibe_signature: str
    ts: float

    def to_dict(self) -> Dict[str, str | float]:
        return {
            "symbol": self.symbol,
            "vibe_signature": self.vibe_signature,
            "ts": self.ts,
        }


class SecuritySigil:
    def __init__(self, *, threshold_glitch: float = 0.6, lok_repeat: int = 7):
        self.threshold_glitch = threshold_glitch
        self.lok_repeat = lok_repeat
        self.palace = MemoryPalace()

    # ------------------------------------------------------------------ main
    def evaluate(self, text: str) -> Dict[str, str]:
        """Evaluate *text*. If threat detected, lock and return payload."""

        report = analyze_text(text)
        if self._is_threat(text, report):
            sigil = self._create_sigil(text)
            self._log_event(text, sigil)
            self._broadcast_threat()
            return {
                "status": "locked",
                "sigil": sigil.symbol,
                "message": "System sealed with WE-WE-WE power!",
            }
        return {
            "status": "secure",
            "sigil": None,
            "message": "Nothing suspicious detected.",
        }

    # ---------------------------------------------------------------- helpers
    def _is_threat(self, text: str, report) -> bool:  # type: ignore[valid-type]
        lok_count = text.lower().split().count("lok")
        return report.glitch_score() >= self.threshold_glitch or lok_count >= self.lok_repeat

    def _create_sigil(self, text: str) -> Sigil:
        digest = hashlib.sha1(text.encode()).hexdigest()[:6]
        symbol = f"{_SIGIL_PREFIX}-{digest}"
        vibe_sig = hashlib.md5(text.encode()).hexdigest()[:8]
        return Sigil(symbol, vibe_sig, time.time())

    def _log_event(self, text: str, sigil: Sigil) -> None:
        self.palace.add(text, "security_event", sigil.symbol)

    def _broadcast_threat(self) -> None:
        try:
            bus = QuantumBus("🤝")
            if bus.handshake(timeout=2):
                bus.send_tick({"event": "NRG breach"})
        except Exception:
            # bus optional, ignore failures
            pass


# ---------------------------------------------------------------------- CLI

def _main() -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Run SecuritySigil threat scan on TEXT.")
    parser.add_argument("text", nargs="*", help="input text (defaults to STDIN)")
    args = parser.parse_args()
    text = " ".join(args.text) if args.text else sys.stdin.read()

    shield = SecuritySigil()
    res = shield.evaluate(text)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    _main()