import json
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from tubedigest.models import VideoJob


async def delete_all_jobs(db: AsyncSession) -> int:
    result = await db.execute(select(VideoJob))
    jobs = list(result.scalars().all())
    for job in jobs:
        await db.delete(job)
    await db.commit()
    return len(jobs)


def _utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


async def create_job(db: AsyncSession, url: str) -> VideoJob:
    job = VideoJob(url=url)
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def get_job(db: AsyncSession, job_id: str) -> Optional[VideoJob]:
    result = await db.execute(select(VideoJob).where(VideoJob.id == job_id))
    return result.scalar_one_or_none()


async def list_jobs(db: AsyncSession) -> list[VideoJob]:
    result = await db.execute(
        select(VideoJob).order_by(VideoJob.created_at.desc())
    )
    return list(result.scalars().all())


async def update_job(db: AsyncSession, job_id: str, **kwargs) -> Optional[VideoJob]:
    safe_kwargs = {}
    for k, v in kwargs.items():
        if k in ("tags", "chapters") and v is not None:
            safe_kwargs[k] = json.dumps(v)
        else:
            safe_kwargs[k] = v

    safe_kwargs["updated_at"] = _utcnow()

    await db.execute(
        update(VideoJob).where(VideoJob.id == job_id).values(**safe_kwargs)
    )
    await db.commit()
    return await get_job(db, job_id)
