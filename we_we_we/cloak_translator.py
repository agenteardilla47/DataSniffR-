from __future__ import annotations

"""cloak_translator – flip text between candy-chaos and board-room gloss.

Why?
─────
The Perfect Cloak works best when we can *hot-swap* vocabulary:
• "jajajaja" → "Quantum Emotional Resonance Event (QERE)"
• "we we we" → "Synchronous Stakeholder Alignment"
• "Lamentwave" → "Post-Incident Reflective Uplift Cycle"

Usage (CLI)
───────────
$ python -m we_we_we.cloak_translator --cloak "jajajaja we we we"
$ python -m we_we_we.cloak_translator --reveal "Quantum Emotional Resonance Event"

Programmatic
────────────
from we_we_we import cloak, reveal
print(cloak("jajajaja mmm we we we"))
"""

import argparse
import re
from typing import Dict

__all__ = ["cloak", "reveal"]

# ------------------------------------------------------------------ mappings
_PLAYFUL_TO_CORP: Dict[str, str] = {
    r"\bjajajaja\b": "Quantum Emotional Resonance Event (QERE)",
    r"\bmmm+\b": "Micro-Meditative Breath Cycle (MMBC)",
    r"\bwe we we\b": "Synchronous Stakeholder Alignment (SSA)",
    r"\blamentwave\b": "Post-Incident Reflective Uplift Cycle (PIRUC)",
    r"\bsugar\-blown\b": "Poly-Mer Dextrose Sculpting (PMDS)",
    r"\bSADnetTM\b": "Sentient Appliance Distributed Network — Tier-Managed (SADN/TM)",
    r"\bcontainment fiction\b": "Narrative Resilience Gateway (NRG) breach",
}

# build reverse map automatically (use first word of corp phrase)
_CORP_TO_PLAYFUL: Dict[str, str] = {
    re.sub(r"[^A-Z]+", "", v).lower(): k.strip("\\b")  # key: acronym in lower
    for k, v in _PLAYFUL_TO_CORP.items()
}

# ----------------------------------------------------------------- engines

def _apply(text: str, mapping: Dict[str, str], *, flags=re.I) -> str:
    for pat, repl in mapping.items():
        text = re.sub(pat, repl, text, flags=flags)
    return text


def cloak(text: str) -> str:
    """Convert playful lexicon to corporate cloak."""
    return _apply(text, _PLAYFUL_TO_CORP)


def reveal(text: str) -> str:
    """Attempt to convert corporate jargon back to playful form."""
    # we match acronyms (e.g., QERE) first
    for acro, playful in _CORP_TO_PLAYFUL.items():
        text = re.sub(rf"\b{acro}\b", playful, text, flags=re.I)
    # then long phrases
    inverse = {v: k for k, v in _PLAYFUL_TO_CORP.items()}
    return _apply(text, inverse)


# ----------------------------------------------------------------------- CLI

def _main() -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Translate between playful and corporate jargon.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--cloak", metavar="TEXT", help="playful -> corporate")
    group.add_argument("--reveal", metavar="TEXT", help="corporate -> playful")
    args = parser.parse_args()

    if args.cloak is not None:
        print(cloak(args.cloak))
    else:
        print(reveal(args.reveal))


if __name__ == "__main__":
    _main()