from typing import Optional

from tubedigest.publisher import FakePublisher, MessagePublisher, RabbitMQPublisher
from tubedigest.settings import settings


_publisher: Optional[MessagePublisher] = None


def get_publisher() -> MessagePublisher:
    global _publisher
    if _publisher is None:
        if settings.use_fake_publisher:
            _publisher = FakePublisher()
        else:
            _publisher = RabbitMQPublisher(url=settings.rabbitmq_url)
    return _publisher
