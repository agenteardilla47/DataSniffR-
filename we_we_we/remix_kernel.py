from __future__ import annotations

"""RemixKernel – minimal proof-of-concept for the AI-OS Remix Architecture.

The kernel cycles arbitrary *text* through four transformational phases:

* death_phase   – identify obsolete patterns (high glitch score)
* alive_phase   – retain core essence
* inlive_phase  – integrate external wisdom (placeholder)
* newbirth      – emit an evolved artefact

At the moment everything is heuristics on top of :pyfunc:`we_we_we.vibe_sensor.analyze_text`.
Future versions can plug in real ML models, vector DBs, or network calls.
"""

import json
import random
from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from .vibe_sensor import VibeReport, analyze_text
from .memory_palace import MemoryPalace

__all__ = [
    "RemixCycle",
    "RemixKernel",
]


@dataclass
class CycleSnapshot:
    """A labelled bundle captured at a single remix phase."""

    label: str
    analysis: Dict[str, Any]
    notes: str = ""


@dataclass
class RemixCycle:
    """Holds every stage of the remix traversal so it can be exported as JSON."""

    original: CycleSnapshot
    death: CycleSnapshot
    alive: CycleSnapshot
    inlive: CycleSnapshot
    newbirth: CycleSnapshot

    # Convenience helpers -------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, *, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


class RemixKernel:
    """Extremely lightweight orchestrator for *one* remix pass.

    Parameters
    ----------
    glitch_threshold : float, default 0.5
        If the initial text scores above this value we tag it as *unstable* and
        perform stronger *death* pruning.
    """

    def __init__(self, *, glitch_threshold: float = 0.5):
        self.glitch_threshold = glitch_threshold

    # ------------------------------------------------------------------ API
    def remix(self, text: str, *, context: Dict[str, Any] | None = None) -> RemixCycle:
        """Run a full remix cycle on *text* and return the structured result."""

        context = context or {}

        # 1. perceive ------------------------------------------------------
        original_report: VibeReport = analyze_text(text)

        # containment fiction logging
        if getattr(original_report, "alert_tokens", []):
            MemoryPalace().add(text, "containment_fiction", *original_report.alert_tokens)

        original = CycleSnapshot(
            label="original",
            analysis=original_report.to_dict(),
            notes="raw perception of incoming artefact",
        )

        # 2. death phase ---------------------------------------------------
        death_notes: List[str] = []
        if original_report.glitch_score() > self.glitch_threshold:
            death_notes.append("high glitch score – pruning unstable patterns")
        else:
            death_notes.append("stable enough – minimal pruning")
        death_snapshot = CycleSnapshot(
            label="death",
            analysis={
                "pruned": original_report.glitch_score() > self.glitch_threshold,
            },
            notes="; ".join(death_notes),
        )

        # 3. alive phase ---------------------------------------------------
        alive_snapshot = CycleSnapshot(
            label="alive",
            analysis={
                "core_tokens": sum(
                    1 for w in text.split() if len(w) > 3  # coarse heuristic
                ),
            },
            notes="preserved long-form tokens as essence",
        )

        # 4. inlive phase --------------------------------------------------
        inlive_snapshot = CycleSnapshot(
            label="inlive",
            analysis={
                "network_signal": random.uniform(0.0, 1.0),  # placeholder
            },
            notes="stub – would fetch collective intelligence here",
        )

        # 5. newbirth phase -----------------------------------------------
        new_text = self._manifest(text, original_report)
        newbirth_report = analyze_text(new_text)
        newbirth_snapshot = CycleSnapshot(
            label="newbirth",
            analysis=newbirth_report.to_dict(),
            notes="evolved artefact generated via _manifest()",
        )

        return RemixCycle(
            original=original,
            death=death_snapshot,
            alive=alive_snapshot,
            inlive=inlive_snapshot,
            newbirth=newbirth_snapshot,
        )

    # ----------------------------------------------------------------- internals
    def _manifest(self, text: str, report: VibeReport) -> str:
        """Very naive manifestation: if the input is glitchy, we tone it down; otherwise we add a gentle sugar overlay."""

        if report.glitch_score() > self.glitch_threshold:
            # Tone down by removing excessive punctuation and repetitions
            toned = text.replace("!", ".").replace("?", ".")
            return toned[:280]  # trim long rants
        else:
            # Sweeten with a touch of candy vibes
            return f"{text} 🫧💾🌫️ mmm we we we"


# ------------------------------------------------------------- CLI helper

def _main() -> None:  # pragma: no cover – convenience only
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Run a remix cycle on TEXT.")
    parser.add_argument("text", nargs="*", help="input text (defaults to STDIN)")
    parser.add_argument("-q", "--quiet", action="store_true", help="only output JSON")
    args = parser.parse_args()

    text = " ".join(args.text) if args.text else sys.stdin.read()
    kernel = RemixKernel()
    cycle = kernel.remix(text)

    if not args.quiet:
        print("# Remix cycle complete\n")
    print(cycle.to_json())


if __name__ == "__main__":
    _main()