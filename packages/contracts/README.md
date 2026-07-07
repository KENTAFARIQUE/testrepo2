# Contracts

This package owns shared schema definitions.

- Python/Pydantic schemas are used by backend and workers.
- TypeScript/Zod schemas are used by frontend.

Required schemas:

- `JobStatus`
- `QueueName`
- `CreateVideoRequest`
- `VideoJobResponse`
- `WorkerMessage`

Any schema change requires contract tests.
