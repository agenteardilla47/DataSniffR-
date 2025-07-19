from __future__ import annotations

"""task_manager – monitors the *Memory Palace* for task artefacts and remixes them.

A *task* is any artefact whose text starts with ``TASK:"`` (case-insensitive) or
contains the literal substring ``[task]``. When detected, the manager runs
:pyclass:`we_we_we.remix_kernel.RemixKernel` on the body and saves the remix
result as a new artefact tagged ``remixed`` (plus original tags).

Run once:
    python -m we_we_we.task_manager --once

Continuous watch (default 5 s):
    python -m we_we_we.task_manager --watch 10
"""

import argparse
import time
from typing import Dict, Set

from .memory_palace import MemoryPalace
from .remix_kernel import RemixKernel

_TASK_PREFIXES = ("task:", "todo:")


class TaskManager:
    """Scan the palace, remix tasks, and store outputs."""

    def __init__(self, *, poll_interval: float = 5.0):
        self.poll_interval = poll_interval
        self.palace = MemoryPalace()
        self.kernel = RemixKernel()
        self._seen: Set[str] = set()

    # -------------------------------------------------------------------- util
    def _is_task(self, text: str) -> bool:
        t = text.lower()
        if any(t.startswith(prefix) for prefix in _TASK_PREFIXES):
            return True
        return "[task]" in t

    def _process(self, artefact_id: str, text: str, tags):
        body = text.split(":", 1)[-1].strip()
        cycle = self.kernel.remix(body)
        self.palace.add(
            cycle.to_json(indent=None),
            "remixed",
            *tags,
            artefact_id,
        )

    # ------------------------------------------------------------------- loops
    def run_once(self) -> None:
        for artefact in self.palace.all():
            if artefact.id in self._seen:
                continue
            if self._is_task(artefact.text):
                self._process(artefact.id, artefact.text, artefact.tags)
            self._seen.add(artefact.id)

    def run_loop(self):
        try:
            while True:
                self.palace._load()  # reload from disk in case another process wrote
                self.run_once()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            print("TaskManager stopped.")


# -------------------------------------------------------------------------- CLI

def _main() -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Run task manager to remix tasks from Memory Palace.")
    parser.add_argument("--once", action="store_true", help="process tasks once and exit")
    parser.add_argument("--watch", type=float, nargs="?", const=5.0, help="watch mode with optional poll interval (seconds)")
    args = parser.parse_args()

    manager = TaskManager(poll_interval=args.watch if args.watch else 5.0)

    if args.once:
        manager.run_once()
    else:
        manager.run_loop()


if __name__ == "__main__":
    _main()