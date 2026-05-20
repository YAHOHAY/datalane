from dataclasses import dataclass, field
from typing import Any


@dataclass
class JobContext:
    """Runtime options passed from CLI into a job run."""

    job_id: str
    deliver: bool = True
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineData:
    """Payload flowing through ingest → transform → deliver."""

    payload: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.payload.get(key, default)
