import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from core.triggers import start_blocking_scheduler

if __name__ == "__main__":
    start_blocking_scheduler()
