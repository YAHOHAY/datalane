from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from config.settings import JOBS_DIR

# 旧命令别名 → jobs/*.yaml 文件名（不含扩展名）
JOB_ALIASES: dict[str, str] = {
    "dongqiudi": "dongqiudi_schedule",
}


def resolve_job_id(job_id: str) -> str:
    return JOB_ALIASES.get(job_id, job_id)


class StepConfig(BaseModel):
    plugin: str
    params: dict[str, Any] = Field(default_factory=dict)


class JobConfig(BaseModel):
    id: str
    name: str = ""
    description: str = ""
    ingest: StepConfig
    transform: list[StepConfig] = Field(default_factory=list)
    deliver: StepConfig | None = None
    async_ingest: bool = False


def load_job(job_id: str) -> JobConfig:
    job_id = resolve_job_id(job_id)
    path = JOBS_DIR / f"{job_id}.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"Job not found: {job_id} (expected {path})")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return JobConfig.model_validate(raw)


def list_jobs() -> list[str]:
    return sorted(p.stem for p in JOBS_DIR.glob("*.yaml"))
