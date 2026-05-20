"""
Datalane 定时调度：每天 00:00 执行 dongqiudi 任务。

用法:
  python scripts/scheduler.py
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import plugins  # noqa: F401
from core.pipeline import run_job


def _daily_dongqiudi() -> None:
    run_job("dongqiudi", deliver=True)


def main() -> None:
    scheduler = BlockingScheduler()
    scheduler.add_job(
        _daily_dongqiudi,
        CronTrigger(hour=0, minute=0),
        id="datalane_dongqiudi",
        name="Datalane 每日赛程",
    )

    print("Datalane 定时任务已启动：每天 00:00 → run_job dongqiudi")
    print("按 Ctrl+C 停止\n")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n定时任务已停止")


if __name__ == "__main__":
    main()
