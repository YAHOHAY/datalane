import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

import plugins  # noqa: F401
from core.pipeline import run_job


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--telegram", action="store_true")
    parser.add_argument("--no-telegram", action="store_true")
    args = parser.parse_args()

    params = {}
    if args.start:
        params["start"] = args.start
    if args.end:
        params["end"] = args.end

    deliver = args.telegram and not args.no_telegram
    run_job("dongqiudi_schedule", deliver=deliver, **params)


if __name__ == "__main__":
    main()
