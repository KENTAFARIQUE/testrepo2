import asyncio
import json
import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
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
from tubedigest.repository import create_job, list_jobs, get_job, delete_all_jobs
from tubedigest.settings import settings
from tubedigest.sse import sse_manager

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


@router.get("/{job_id}/download")
async def download_video(
    job_id: str,
    db: AsyncSession = Depends(get_db),
):
    job = await get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    path = job.video_path
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No video file available for this job",
        )

    relative = path
    for prefix in ("storage/", "audio/", "thumbnails/", "transcripts/"):
        if relative.startswith(prefix):
            relative = relative[len(prefix):]
            break
    full_path: str = path if os.path.isabs(path) else os.path.join(settings.storage_root, relative)

    if not os.path.exists(full_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video file not found on disk",
        )

    filename: str = os.path.basename(path)
    return FileResponse(full_path, filename=filename)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_videos(
    db: AsyncSession = Depends(get_db),
):
    await delete_all_jobs(db)


@router.get("/{job_id}/events")
async def job_events(job_id: str):
    queue = await sse_manager.register(job_id)

    async def event_stream():
        try:
            yield ": connected\n\n"
            while True:
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=15)
                    yield f"data: {json.dumps(data)}\n\n"
                except asyncio.TimeoutError:
                    yield ": heartbeat\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            await sse_manager.unregister(job_id, queue)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
