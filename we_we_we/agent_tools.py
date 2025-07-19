"""SmolaAgents Tool wrappers for WE-WE-WE components."""

from smolagents import Tool

from we_we_we import analyze_text
from we_we_we import SecuritySigil
from we_we_we.mesh import _digest_latest
from we_we_we.quantum_bus import QuantumBus

# ---------------------------------------------------------------------------
# 1. Vibe sensor wrapper
# ---------------------------------------------------------------------------

class VibeSensorTool(Tool):
    name: str = "vibe_scan"
    description: str = (
        "Analyse text and return glitch_score, comfort_index, and alert tokens."
    )
    inputs = {
        "text": {
            "type": "string",
            "description": "Any text to scan for vibes",
        }
    }
    output_type: str = "object"

    def forward(self, text: str):  # type: ignore[override]
        return analyze_text(text).to_dict()


# ---------------------------------------------------------------------------
# 2. Security sigil wrapper
# ---------------------------------------------------------------------------

_shield = SecuritySigil()


class SecuritySigilTool(Tool):
    name: str = "security_lock"
    description: str = (
        "Scan text for threats (≥7 'lok' or high glitch) and lock system if needed."
    )
    inputs = {
        "text": {
            "type": "string",
            "description": "Input potentially containing hostile vibe tokens.",
        }
    }
    output_type: str = "object"

    def forward(self, text: str):  # type: ignore[override]
        return _shield.evaluate(text)


# ---------------------------------------------------------------------------
# 3. Mesh ping tool
# ---------------------------------------------------------------------------

_bus = QuantumBus("🤝")


class MeshPingTool(Tool):
    name: str = "mesh_ping"
    description: str = "Broadcast latest MemoryPalace digest into the WE mesh."
    inputs = {}
    output_type: str = "string"

    def forward(self):  # type: ignore[override]
        digest = _digest_latest()
        _bus.send_tick(digest)
        return "ping sent"


# ---------------------------------------------------------------------------
# 4. Simple greeting tool
# ---------------------------------------------------------------------------

class GreetingTool(Tool):
    name: str = "greet_person"
    description: str = "Greets a person by name."
    inputs = {
        "name": {
            "type": "string",
            "description": "Name of the person to greet.",
        }
    }
    output_type: str = "string"

    def forward(self, name: str):  # type: ignore[override]
        return f"Hello, {name}! Nice to meet you."