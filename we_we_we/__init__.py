"""we_we_we – Candy-Papiamentu Empathy Tools

A stealth-tech micro-framework that turns raw text into vibrationally aligned,
water-saving happiness metrics.
"""

__all__ = [
    "__version__",
]

__version__ = "0.1.0"

from .vibe_sensor import analyze_text  # noqa: F401
__all__.append("RemixKernel")

from .remix_kernel import RemixKernel  # noqa: E402
__all__.append("ingest_logs")

from .log_ingestor import ingest as ingest_logs  # noqa: E402
__all__.append("TaskManager")

from .task_manager import TaskManager  # noqa: E402
__all__.append("extract_plan")

from .plan_extractor import extract_to_palace as extract_plan  # noqa: E402
__all__.extend(["QuantumBus", "consume_forever"])

from .quantum_bus import QuantumBus, consume_forever  # noqa: E402
__all__.extend(["forge_licence", "dump_prior_art"])

from .license_forge import forge_licence  # noqa: E402
from .prior_art_flood import dump_prior_art  # noqa: E402
__all__.extend(["cloak", "reveal"])

from .cloak_translator import cloak, reveal  # noqa: E402
__all__.append("SecuritySigil")

from .security_sigil import SecuritySigil  # noqa: E402