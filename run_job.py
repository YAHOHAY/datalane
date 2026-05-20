"""
Datalane 统一入口

示例:
  python run_job.py dongqiudi
  python run_job.py dongqiudi --start 2026-03-07 --end 2026-03-14
  python run_job.py dongqiudi --no-deliver
  python run_job.py web_monitor
  python run_job.py --list
"""

import argparse
import sys

import plugins  # noqa: F401 — register plugins
from core.job_loader import list_jobs
from core.pipeline import run_job


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="run_job",
        description="Datalane — 数据采集 · 清洗 · 推送",
    )
    parser.add_argument("job_id", nargs="?", help="jobs/ 目录下的任务 ID，如 dongqiudi")
    parser.add_argument("--list", action="store_true", help="列出所有任务")
    parser.add_argument("--start", help="赛程开始日期 YYYY-MM-DD")
    parser.add_argument("--end", help="赛程结束日期 YYYY-MM-DD")
    parser.add_argument(
        "--no-deliver",
        action="store_true",
        help="只采集/清洗，不推送到 Telegram",
    )
    args = parser.parse_args()

    if args.list:
        print("可用任务:")
        for job_id in list_jobs():
            print(f"  - {job_id}")
        return

    if not args.job_id:
        parser.print_help()
        sys.exit(1)

    params = {}
    if args.start:
        params["start"] = args.start
    if args.end:
        params["end"] = args.end

    ok = run_job(args.job_id, deliver=not args.no_deliver, **params)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
