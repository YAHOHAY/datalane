"""触发器：CLI 参数解析、定时调度。"""

import argparse
import sys
from typing import Any

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import plugins  # noqa: F401
from core.job_loader import JOB_ALIASES, list_jobs, resolve_job_id
from core.pipeline import run_job

DEFAULT_CRON_JOB = "dongqiudi_schedule"


def build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_job",
        description="Datalane — 数据采集 · 清洗 · 推送",
    )
    parser.add_argument("job_id", nargs="?", help="jobs/*.yaml 的任务 ID")
    parser.add_argument("--list", action="store_true", help="列出所有任务")
    parser.add_argument("--start", help="赛程开始日期 YYYY-MM-DD")
    parser.add_argument("--end", help="赛程结束日期 YYYY-MM-DD")
    parser.add_argument("--no-deliver", action="store_true", help="不推送 Telegram")
    return parser


def parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_cli_parser().parse_args(argv)


def cli_params_from_args(args: argparse.Namespace) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if args.start:
        params["start"] = args.start
    if args.end:
        params["end"] = args.end
    return params


def run_cli(argv: list[str] | None = None) -> int:
    """CLI 触发：python scripts/run_job.py <job_id>"""
    args = parse_cli_args(argv)

    if args.list:
        print("可用任务:")
        for job_id in list_jobs():
            print(f"  - {job_id}")
        return 0

    if not args.job_id:
        build_cli_parser().print_help()
        return 1

    job_id = resolve_job_id(args.job_id)
    ok = run_job(job_id, deliver=not args.no_deliver, **cli_params_from_args(args))
    return 0 if ok else 1


def run_scheduled_job(job_id: str = DEFAULT_CRON_JOB, *, deliver: bool = True) -> None:
    """定时触发：执行指定 Job。"""
    run_job(resolve_job_id(job_id), deliver=deliver)


def start_blocking_scheduler(
    job_id: str = DEFAULT_CRON_JOB,
    *,
    hour: int = 0,
    minute: int = 0,
) -> None:
    """每天固定时刻跑 Job（阻塞，需保持进程运行）。"""
    scheduler = BlockingScheduler()
    job_id = resolve_job_id(job_id)
    scheduler.add_job(
        run_scheduled_job,
        CronTrigger(hour=hour, minute=minute),
        id=f"datalane_{job_id}",
        name=f"Datalane {job_id}",
        kwargs={"job_id": job_id, "deliver": True},
    )

    print(f"Datalane 定时任务：每天 {hour:02d}:{minute:02d} → {job_id}")
    print("按 Ctrl+C 停止\n")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n定时任务已停止")
