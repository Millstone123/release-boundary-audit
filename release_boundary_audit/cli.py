from __future__ import annotations

import argparse
from pathlib import Path

from .checker import inspect_repository
from .report import render_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit semantic release boundaries.")
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    args = parser.parse_args()
    result = inspect_repository(args.root)
    print(render_text(result), end="")
    return 1 if result.issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
