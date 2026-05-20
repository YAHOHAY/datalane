"""入口：python daily_job.py → 抓取赛程并推送 Telegram"""
import plugins  # noqa: F401
from core.pipeline import run_job

if __name__ == "__main__":
    run_job("dongqiudi", deliver=True)
