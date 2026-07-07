## Add RabbitMQ publisher abstraction for backend

## Owner
backend-agent

## Labels
agent:backend, scope:backend, type:feature

## Context
The backend must publish messages to RabbitMQ queues without depending on a live RabbitMQ broker. This issue creates a publisher abstraction with a real implementation that uses pika and a fake implementation for testing.

## Scope
- Create apps/backend/src/tubedigest/publisher.py with:
  - Abstract MessagePublisher base class
  - RabbitMQPublisher implementation using pika
  - FakePublisher implementation (stores messages in memory)
  - published_messages list for assertions
  - reset() method for test isolation
- Create apps/backend/src/tubedigest/dependencies.py with publisher factory and DI
- Wire USE_FAKE_MODELS env var to select publisher implementation
- Tests covering both publisher implementations

## Out of scope
- API endpoints or job creation
- Worker message consumers
- Queue declaration (handled by workers)

## Acceptance criteria
- RabbitMQPublisher publishes JSON messages with correct routing key
- RabbitMQPublisher handles connection failures gracefully (logs error, does not crash)
- FakePublisher.publish() stores messages for later assertion
- FakePublisher.published_messages returns list of (queue, message) tuples
- FakePublisher.reset() clears all stored messages
- Dependency factory returns FakePublisher when USE_FAKE_MODELS=true

## Tests required
- FakePublisher stores published message
- FakePublisher stores multiple messages in order
- FakePublisher.reset() clears all messages
- FakePublisher.publish with WorkerMessage serialization
- Mock publisher test: verify publish method signature

## Likely affected files
- apps/backend/src/tubedigest/publisher.py (new)
- apps/backend/src/tubedigest/dependencies.py (new)
- apps/backend/tests/test_publisher.py (new)

## Dependencies
#2 (backend bootstrap - needs pyproject.toml with pika dep)

## Definition of Done
- implementation matches scope
- pytest apps/backend/tests/test_publisher.py passes
- FakePublisher used when USE_FAKE_MODELS=true
- PR has test evidence
