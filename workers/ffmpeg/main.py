import os
import json
import sqlite3
from datetime import datetime, timezone
from typing import Dict, Any, Optional

import pika

from tubedigest.contracts import WorkerMessage
from tubedigest.contracts import (
    QUEUE_VIDEO_AUDIO_EXTRACT,
    QUEUE_VIDEO_THUMBNAIL_GENERATE,
)
from workers.ffmpeg.handler import (
    handle_audio_extract,
    handle_thumbnail_generate,
    HandlerDeps,
    Database,
    Publisher,
)
from workers.ffmpeg.adapters import FfmpegAdapter, FakeFfmpegAdapter


class SqliteJobStore:
    def __init__(self, db_path: str):
        self._db_path = db_path

    def _conn(self):
        return sqlite3.connect(self._db_path)

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT id, video_path, audio_path, thumbnail_path "
                "FROM video_jobs WHERE id=?", (job_id,)
            ).fetchone()
            if row is None:
                return None
            return {
                "id": row[0],
                "video_path": row[1],
                "audio_path": row[2],
                "thumbnail_path": row[3],
            }

    def update_job(self, job_id: str, updates: Dict[str, Any]) -> None:
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        columns = ", ".join(f"{k}=?" for k in updates)
        values = list(updates.values()) + [job_id]
        with self._conn() as conn:
            conn.execute(f"UPDATE video_jobs SET {columns} WHERE id=?", values)
            conn.commit()


class RabbitPublisher:
    def __init__(self, channel):
        self._channel = channel

    def publish(self, queue: str, message: dict) -> None:
        self._channel.queue_declare(queue=queue, durable=True)
        self._channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )


def _resolve_db_path() -> str:
    url = os.environ.get("DATABASE_URL", "sqlite:///./data/tubedigest.db")
    if url.startswith("sqlite:///"):
        return url[len("sqlite:///"):]
    return url


def _resolve_ffmpeg() -> FfmpegAdapter:
    use_fake = os.environ.get("USE_FAKE_MEDIA", "true").lower() == "true"
    if use_fake:
        return FakeFfmpegAdapter()
    from workers.ffmpeg.adapters import RealFfmpegAdapter
    return RealFfmpegAdapter()


def make_deps(publisher: Publisher) -> HandlerDeps:
    return HandlerDeps(
        db=SqliteJobStore(_resolve_db_path()),
        publisher=publisher,
        ffmpeg=_resolve_ffmpeg(),
        audio_dir=os.environ.get("AUDIO_DIR", "storage/audio"),
        thumbnails_dir=os.environ.get("THUMBNAILS_DIR", "storage/thumbnails"),
    )


_QUEUE_HANDLERS = {
    QUEUE_VIDEO_AUDIO_EXTRACT: handle_audio_extract,
    QUEUE_VIDEO_THUMBNAIL_GENERATE: handle_thumbnail_generate,
}


def _process_message(ch, method, body, deps: HandlerDeps) -> None:
    try:
        message = WorkerMessage.model_validate_json(body)
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    handler = _QUEUE_HANDLERS.get(method.routing_key)
    if handler is None:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    try:
        handler(message, deps)
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    rabbitmq_url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()

    for queue in _QUEUE_HANDLERS:
        channel.queue_declare(queue=queue, durable=True)

    channel.basic_qos(prefetch_count=1)

    publisher = RabbitPublisher(channel)
    deps = make_deps(publisher)

    def on_message(ch, method, properties, body):
        _process_message(ch, method, body, deps)

    for queue in _QUEUE_HANDLERS:
        channel.basic_consume(
            queue=queue,
            on_message_callback=on_message,
        )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
