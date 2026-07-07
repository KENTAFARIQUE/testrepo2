from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class JobStatus(str, Enum):
    queued = "queued"
    downloading = "downloading"
    downloaded = "downloaded"
    extracting_audio = "extracting_audio"
    generating_thumbnail = "generating_thumbnail"
    transcribing = "transcribing"
    summarizing = "summarizing"
    generating_tags = "generating_tags"
    completed = "completed"
    failed = "failed"


class Chapter(BaseModel):
    start: str = Field(min_length=1)
    title: str = Field(min_length=1)


class CreateVideoRequest(BaseModel):
    url: str = Field(min_length=1)


class VideoJobResponse(BaseModel):
    id: str
    url: str
    title: Optional[str] = None
    status: JobStatus = JobStatus.queued
    current_step: str = "queued"
    video_path: Optional[str] = None
    audio_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    transcript: Optional[str] = None
    summary: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    chapters: list[Chapter] = Field(default_factory=list)
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class WorkerMessage(BaseModel):
    job_id: str
    video_id: str
    attempt: int = 1
    url: Optional[str] = None
