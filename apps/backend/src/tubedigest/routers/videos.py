import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from tubedigest.contracts import (
    QUEUE_VIDEO_DOWNLOAD,
    CreateVideoRequest,
    VideoJobResponse,
    WorkerMessage,
)
from tubedigest.database import get_db
from tubedigest.dependencies import get_publisher
from tubedigest.publisher import MessagePublisher
from tubedigest.repository import create_job, list_jobs, get_job

router = APIRouter(prefix="/videos", tags=["videos"])


def _model_to_response(job) -> VideoJobResponse:
    tags = []
    if job.tags:
        try:
            tags = json.loads(job.tags)
        except (json.JSONDecodeError, TypeError):
            tags = []
    return VideoJobResponse(
        id=job.id,
        url=job.url,
        title=job.title,
        status=job.status,
        current_step=job.current_step,
        video_path=job.video_path,
        audio_path=job.audio_path,
        thumbnail_path=job.thumbnail_path,
        transcript=job.transcript,
        summary=job.summary,
        tags=tags,
        chapters=[],
        error=job.error,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_video(
    body: CreateVideoRequest,
    db: AsyncSession = Depends(get_db),
    publisher: MessagePublisher = Depends(get_publisher),
):
    job = await create_job(db, url=body.url)
    msg = WorkerMessage(
        job_id=job.id,
        video_id=job.id,
        url=job.url,
        attempt=1,
    )
    await publisher.publish(QUEUE_VIDEO_DOWNLOAD, msg)
    return _model_to_response(job)


@router.get("")
async def list_videos(
    db: AsyncSession = Depends(get_db),
):
    jobs = await list_jobs(db)
    return [_model_to_response(j) for j in jobs]


@router.get("/{job_id}")
async def get_video(
    job_id: str,
    db: AsyncSession = Depends(get_db),
):
    job = await get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return _model_to_response(job)
