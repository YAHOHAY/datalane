"""入口：python main.py → 网页关键词监控"""
import plugins  # noqa: F401
from core.pipeline import run_job

if __name__ == "__main__":
    run_job("web_monitor")
