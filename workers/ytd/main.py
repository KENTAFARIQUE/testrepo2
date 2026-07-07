import os
import json
import sqlite3
from datetime import datetime, timezone
from typing import Dict, Any

import pika

from tubedigest.contracts import WorkerMessage, QUEUE_VIDEO_DOWNLOAD
from workers.ytd.handler import handle_message, HandlerDeps, Database, Publisher
from workers.ytd.adapters import Downloader, FakeDownloader


class SqliteJobStore:
    def __init__(self, db_path: str):
        self._db_path = db_path

    def _conn(self):
        return sqlite3.connect(self._db_path)

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


def _resolve_downloader() -> Downloader:
    use_fake = os.environ.get("USE_FAKE_DOWNLOAD", "true").lower() == "true"
    if use_fake:
        return FakeDownloader()
    from workers.ytd.adapters import RealYoutubeDownloader
    return RealYoutubeDownloader()


def make_deps(publisher: Publisher) -> HandlerDeps:
    return HandlerDeps(
        db=SqliteJobStore(_resolve_db_path()),
        publisher=publisher,
        downloader=_resolve_downloader(),
        videos_dir=os.environ.get("VIDEOS_DIR", "storage/videos"),
    )


def _process_message(ch, method, body, deps: HandlerDeps) -> None:
    try:
        message = WorkerMessage.model_validate_json(body)
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    try:
        handle_message(message, deps)
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    rabbitmq_url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_VIDEO_DOWNLOAD, durable=True)
    channel.basic_qos(prefetch_count=1)

    publisher = RabbitPublisher(channel)
    deps = make_deps(publisher)

    def on_message(ch, method, properties, body):
        _process_message(ch, method, body, deps)

    channel.basic_consume(
        queue=QUEUE_VIDEO_DOWNLOAD,
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
