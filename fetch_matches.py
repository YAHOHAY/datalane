"""入口：python fetch_matches.py [--start] [--end] [--telegram]"""
import argparse

import plugins  # noqa: F401
from core.pipeline import run_job


def main() -> None:
    parser = argparse.ArgumentParser(description="抓取懂球帝赛程")
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--telegram", action="store_true", help="推送到 Telegram")
    parser.add_argument("--no-telegram", action="store_true")
    args = parser.parse_args()

    params = {}
    if args.start:
        params["start"] = args.start
    if args.end:
        params["end"] = args.end

    deliver = True
    if args.no_telegram:
        deliver = False
    elif not args.telegram:
        deliver = False

    run_job("dongqiudi", deliver=deliver, **params)


if __name__ == "__main__":
    main()
