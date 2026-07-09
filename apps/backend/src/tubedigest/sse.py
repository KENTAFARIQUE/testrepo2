import asyncio
import json
import logging
import threading

import pika

from tubedigest.contracts import QUEUE_VIDEO_STATUS
from typing import Optional

logger = logging.getLogger(__name__)


class SSEManager:
    def __init__(self) -> None:
        self._clients: dict[str, list[asyncio.Queue]] = {}
        self._lock = asyncio.Lock()

    async def register(self, job_id: str) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue()
        async with self._lock:
            self._clients.setdefault(job_id, []).append(queue)
        return queue

    async def unregister(self, job_id: str, queue: asyncio.Queue) -> None:
        async with self._lock:
            clients = self._clients.get(job_id, [])
            if queue in clients:
                clients.remove(queue)
            if not clients:
                self._clients.pop(job_id, None)

    async def broadcast(self, job_id: str, data: dict) -> None:
        async with self._lock:
            queues = list(self._clients.get(job_id, []))
        for q in queues:
            await q.put(data)


def _consumer_thread(loop: asyncio.AbstractEventLoop, sse: SSEManager, url: str) -> None:
    try:
        connection = pika.BlockingConnection(pika.URLParameters(url))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_VIDEO_STATUS, durable=True)
        channel.basic_qos(prefetch_count=1)

        def callback(
            ch: pika.channel.Channel,
            method: pika.spec.Basic.Deliver,
            properties: pika.spec.BasicProperties,
            body: bytes,
        ) -> None:
            try:
                data = json.loads(body)
                job_id = data.get("job_id")
                if job_id:
                    asyncio.run_coroutine_threadsafe(
                        sse.broadcast(job_id, data),
                        loop,
                    )
            except Exception:
                logger.exception("Failed to process status message")
            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(
            queue=QUEUE_VIDEO_STATUS,
            on_message_callback=callback,
        )
        channel.start_consuming()
    except Exception:
        logger.exception("RabbitMQ consumer thread failed")


def start_consumer(loop: asyncio.AbstractEventLoop, sse: SSEManager, url: str) -> threading.Thread:
    thread = threading.Thread(
        target=_consumer_thread,
        args=(loop, sse, url),
        daemon=True,
    )
    thread.start()
    return thread


sse_manager = SSEManager()
