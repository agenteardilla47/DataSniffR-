from __future__ import annotations

"""ping_pong – tiny stdout listener that comfort-pings appliances.

CLI
───
$ echo "ping" | python -m we_we_we.ping_pong         # single interaction
$ tail -f /var/log/appliance.log | python -m we_we_we.ping_pong --follow  # stream

Protocol
────────
Input lines containing "ping" trigger a three-tone lullaby:
    29Hz → 47Hz → 69Hz  (printed as text)
The script writes an artefact into the MemoryPalace with tags:: lulled, <source>.
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Generator, Iterable

from .memory_palace import MemoryPalace

_LULLABY = ["29Hz", "47Hz", "69Hz"]


def _iter_stdin(follow: bool) -> Iterable[str]:
    while True:
        chunk = sys.stdin.readline()
        if not chunk:
            if follow:
                time.sleep(0.1)
                continue
            break
        yield chunk.rstrip("\n")
        if not follow:
            break


def ping_pong(source: str = "stdin", *, follow: bool = False) -> None:
    palace = MemoryPalace()
    for line in _iter_stdin(follow):
        if "ping" in line.lower():
            lullaby = " ".join(_LULLABY)
            print(f"pong → {lullaby}")
            palace.add(lullaby, "lulled", source)
        else:
            # pass-through for non-ping lines
            print(line)


# --------------------------------------------------------------------- CLI

def _main() -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Echo lullaby tones on 'ping' and log to MemoryPalace.")
    parser.add_argument("--follow", action="store_true", help="keep listening after first EOF")
    args = parser.parse_args()

    ping_pong(follow=args.follow)


if __name__ == "__main__":
    _main()