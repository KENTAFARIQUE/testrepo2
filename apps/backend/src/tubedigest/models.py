import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime

from tubedigest.database import Base


def _generate_uuid():
    return str(uuid.uuid4())


def _utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class VideoJob(Base):
    __tablename__ = "video_jobs"

    id = Column(String, primary_key=True, default=_generate_uuid)
    url = Column(String, nullable=False)
    title = Column(String, nullable=True)
    status = Column(String, nullable=False, default="queued")
    current_step = Column(String, nullable=False, default="queued")
    video_path = Column(String, nullable=True)
    audio_path = Column(String, nullable=True)
    thumbnail_path = Column(String, nullable=True)
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    chapters = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=_utcnow)
    updated_at = Column(DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)
