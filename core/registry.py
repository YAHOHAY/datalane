from collections.abc import Awaitable, Callable
from typing import Any

from core.models import JobContext, PipelineData

IngestFn = Callable[[dict[str, Any], JobContext], PipelineData]
TransformFn = Callable[[PipelineData, dict[str, Any], JobContext], PipelineData]
DeliverFn = Callable[[PipelineData, dict[str, Any], JobContext], bool]
AsyncIngestFn = Callable[[dict[str, Any], JobContext], Awaitable[PipelineData]]

INGEST: dict[str, IngestFn] = {}
ASYNC_INGEST: dict[str, AsyncIngestFn] = {}
TRANSFORM: dict[str, TransformFn] = {}
DELIVER: dict[str, DeliverFn] = {}


def register_ingest(name: str):
    def decorator(fn: IngestFn):
        INGEST[name] = fn
        return fn

    return decorator


def register_async_ingest(name: str):
    def decorator(fn: AsyncIngestFn):
        ASYNC_INGEST[name] = fn
        return fn

    return decorator


def register_transform(name: str):
    def decorator(fn: TransformFn):
        TRANSFORM[name] = fn
        return fn

    return decorator


def register_deliver(name: str):
    def decorator(fn: DeliverFn):
        DELIVER[name] = fn
        return fn

    return decorator
