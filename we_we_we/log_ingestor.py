from __future__ import annotations

"""log_ingestor – scans .log / .txt files and decodes *reversed* lines.

Usage
-----
python -m we_we_we.log_ingestor path/to/file1.log path/to/dir/*.txt

Detected decoded artefacts are stored in the :pyclass:`we_we_we.memory_palace.MemoryPalace`
so other modules (or curious humans) can inspect the hidden payload later.
"""

import argparse
import glob
import re
import sys
from pathlib import Path
from typing import Iterable, List

from .memory_palace import MemoryPalace

_COMMON_WORDS = {"the", "and", "we", "you", "to", "of", "in", "is"}
_LETTER_RE = re.compile(r"[a-zA-Z]")


def _is_likely_reversed(text: str) -> bool:
    """Heuristic: reversed text becomes readable English."""

    if text.strip() == "":
        return False
    # high ratio of letters
    letters = len(_LETTER_RE.findall(text))
    ratio = letters / max(1, len(text))
    if ratio < 0.6:
        return False
    words = set(w.lower() for w in text.split())
    return len(words & _COMMON_WORDS) >= 2  # at least two common words


def _iter_files(patterns: Iterable[str]) -> Iterable[Path]:
    for pattern in patterns:
        for path in glob.glob(pattern, recursive=True):
            p = Path(path)
            if p.is_file():
                yield p


def ingest(patterns: List[str]) -> None:
    palace = MemoryPalace()
    for file in _iter_files(patterns):
        for line in file.read_text("utf-8", errors="ignore").splitlines():
            rev = line[::-1]
            if _is_likely_reversed(rev):
                palace.add(rev, "decoded", file.name)


# -------------------------------------------------------------------------- CLI

def _main() -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Decode reversed lines from log files.")
    parser.add_argument("paths", nargs="+", help="file/dir patterns (glob)")
    args = parser.parse_args()

    ingest(args.paths)
    print("Decoded artefacts stored in MemoryPalace.")


if __name__ == "__main__":
    _main()