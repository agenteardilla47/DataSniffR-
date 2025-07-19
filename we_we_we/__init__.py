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