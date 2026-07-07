import json
import logging
from abc import ABC, abstractmethod
from typing import Optional

from tubedigest.contracts import WorkerMessage

logger = logging.getLogger(__name__)


class MessagePublisher(ABC):
    @abstractmethod
    async def publish(self, queue: str, message: WorkerMessage) -> None:
        ...


class RabbitMQPublisher(MessagePublisher):
    def __init__(self, url: str):
        self._url = url
        self._connection = None
        self._channel = None

    async def publish(self, queue: str, message: WorkerMessage) -> None:
        try:
            import pika

            body = message.model_dump_json()
            params = pika.URLParameters(self._url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue=queue, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=queue,
                body=body,
                properties=pika.BasicProperties(delivery_mode=2),
            )
            connection.close()
        except Exception:
            logger.exception("Failed to publish message to queue %s", queue)


class FakePublisher(MessagePublisher):
    def __init__(self):
        self.published_messages: list[tuple[str, WorkerMessage]] = []

    def reset(self) -> None:
        self.published_messages.clear()

    async def publish(self, queue: str, message: WorkerMessage) -> None:
        self.published_messages.append((queue, message))
