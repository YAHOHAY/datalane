"""
Datalane CLI 入口

示例:
  python scripts/run_job.py dongqiudi_schedule
  python scripts/run_job.py dongqiudi --start 2026-03-07 --end 2026-03-14
  python scripts/run_job.py web_monitor
  python scripts/run_job.py --list
"""

import sys
from pathlib import Path

# 保证从项目根目录可导入
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from core.triggers import run_cli

if __name__ == "__main__":
    raise SystemExit(run_cli())
