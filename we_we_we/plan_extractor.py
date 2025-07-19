from __future__ import annotations

"""plan_extractor – mine actionable lines from a text file and register them as tasks.

Heuristics:
• Lines starting with "- " or "* " followed by an uppercase verb.
• Lines starting with "Step" / "step".
• Lines under a "###" heading whose first word is an imperative verb (optional).

Each extracted line is wrapped into a canonical ``TASK: ...`` form so the
:pyclass:`we_we_we.task_manager.TaskManager` will pick them up.

CLI examples
------------
Extract from a markdown file and immediately remix:

    python -m we_we_we.plan_extractor evil_guide.md --remix
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List

from .memory_palace import MemoryPalace
from .task_manager import TaskManager


_BULLET_RE = re.compile(r"^[\-*]\s+([A-Z][^\n]+)")
_STEP_RE = re.compile(r"^step\s*\d*[:\.]?\s+(.+)", re.IGNORECASE)


# ---------------------------------------------------------------------- logic

def _extract_lines(lines: Iterable[str]) -> List[str]:
    tasks: List[str] = []
    for raw in lines:
        line = raw.strip()
        if not line or len(line) < 4:
            continue
        m = _BULLET_RE.match(line)
        if m:
            tasks.append(m.group(1).strip())
            continue
        m = _STEP_RE.match(line)
        if m:
            tasks.append(m.group(1).strip())
            continue
    return tasks


def extract_to_palace(path: Path, *, remix: bool = False) -> int:
    text = path.read_text("utf-8", errors="ignore")
    tasks = _extract_lines(text.splitlines())
    palace = MemoryPalace()
    for line in tasks:
        palace.add(f"TASK: {line}", "extracted", path.name)
    if remix and tasks:
        manager = TaskManager()
        manager.run_once()
    return len(tasks)


# ----------------------------------------------------------------------- CLI

def _main() -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Extract bullet/step lines as tasks and store in MemoryPalace.")
    parser.add_argument("file", help="input markdown/txt file")
    parser.add_argument("--remix", action="store_true", help="run TaskManager once after extraction")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    count = extract_to_palace(path, remix=args.remix)
    print(f"Extracted {count} tasks into MemoryPalace.")
    if args.remix and count:
        print("Remix complete. Check .we_memory.json for outputs.")


if __name__ == "__main__":
    _main()