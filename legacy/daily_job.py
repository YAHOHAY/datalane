import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

import plugins  # noqa: F401
from core.pipeline import run_job

if __name__ == "__main__":
    run_job("dongqiudi_schedule", deliver=True)
