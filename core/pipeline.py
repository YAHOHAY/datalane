import asyncio

from core.job_loader import JobConfig, load_job
from core.models import JobContext, PipelineData
from core.registry import ASYNC_INGEST, DELIVER, INGEST, TRANSFORM


def _run_transforms(data: PipelineData, job: JobConfig, ctx: JobContext) -> PipelineData:
    for step in job.transform:
        fn = TRANSFORM.get(step.plugin)
        if fn is None:
            raise KeyError(f"Unknown transform plugin: {step.plugin}")
        data = fn(data, step.params, ctx)
    return data


def _run_deliver(data: PipelineData, job: JobConfig, ctx: JobContext) -> bool:
    if not ctx.deliver or job.deliver is None:
        print(f"[pipeline] Job '{ctx.job_id}' finished (deliver skipped).")
        return True

    fn = DELIVER.get(job.deliver.plugin)
    if fn is None:
        raise KeyError(f"Unknown deliver plugin: {job.deliver.plugin}")
    return fn(data, job.deliver.params, ctx)


def run_job(job_id: str, *, deliver: bool = True, **params) -> bool:
    """Run a synchronous job pipeline."""
    job = load_job(job_id)
    if job.async_ingest:
        return asyncio.run(run_job_async(job_id, deliver=deliver, **params))

    ctx = JobContext(job_id=job_id, deliver=deliver, params=params)
    ingest_fn = INGEST.get(job.ingest.plugin)
    if ingest_fn is None:
        raise KeyError(f"Unknown ingest plugin: {job.ingest}")

    print(f"[pipeline] Job: {job.name or job.id}")
    data = ingest_fn(job.ingest.params, ctx)
    data = _run_transforms(data, job, ctx)
    return _run_deliver(data, job, ctx)


async def run_job_async(job_id: str, *, deliver: bool = True, **params) -> bool:
    """Run a job whose ingest step is async (e.g. Playwright)."""
    job = load_job(job_id)
    ctx = JobContext(job_id=job_id, deliver=deliver, params=params)

    ingest_fn = ASYNC_INGEST.get(job.ingest.plugin)
    if ingest_fn is None:
        raise KeyError(f"Unknown async ingest plugin: {job.ingest.plugin}")

    print(f"[pipeline] Job: {job.name or job.id}")
    data = await ingest_fn(job.ingest.params, ctx)
    data = _run_transforms(data, job, ctx)
    return _run_deliver(data, job, ctx)
