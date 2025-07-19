import sys
import json
from pathlib import Path

from .vibe_sensor import analyze_text


def main() -> None:
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read()
    report = analyze_text(text)
    print(json.dumps(report.to_dict(), indent=2))


if __name__ == "__main__":
    main()