## Add Zod schemas and contract tests for frontend

## Owner
contracts-agent

## Labels
agent:contracts, scope:contracts, type:feature

## Context
Phase 2 of the roadmap requires Zod schemas that mirror the existing Pydantic contracts. The Python-side Pydantic schemas (JobStatus, CreateVideoRequest, VideoJobResponse, WorkerMessage, Chapter) and their tests are already complete. The frontend needs equivalent Zod schemas to validate API responses and form inputs at runtime.

## Scope
- Create apps/frontend/src/contracts/schemas.ts with Zod schemas for:
  - JobStatus enum (same 10 values as Pydantic)
  - Chapter schema (start: string, title: string)
  - CreateVideoRequest schema (url: string)
  - VideoJobResponse schema (all fields matching Pydantic)
  - WorkerMessage schema (matching Pydantic)
- Create apps/frontend/src/contracts/queues.ts with queue name constants
- Create apps/frontend/src/contracts/index.ts for re-exports
- Create apps/frontend/src/contracts/__tests__/ with Vitest contract tests
- Ensure Zod default values and optionals match Pydantic defaults

## Out of scope
- Any React components or UI code
- Backend or worker implementation
- Changing Pydantic schemas

## Acceptance criteria
- All Zod schemas accept valid payloads that match the Pydantic contract spec
- Invalid payloads (missing required fields, wrong types, bad enums) are rejected
- Queue constants ALL_QUEUES contains all 7 queue name strings
- Default values for status, current_step, attempt, tags, chapters match Pydantic
- npm run test:contracts passes

## Tests required
- Zod: JobStatus accepts all 10 valid values, rejects invalid
- Zod: Chapter validates start and title, rejects empty strings
- Zod: CreateVideoRequest validates url, rejects empty/missing
- Zod: VideoJobResponse validates minimal payload with defaults
- Zod: VideoJobResponse validates full payload with all fields
- Zod: VideoJobResponse rejects missing id, missing url, invalid status
- Zod: WorkerMessage validates with url, without url, with defaults
- Zod: WorkerMessage rejects missing job_id, missing video_id
- Queue constants: all 7 values match expected strings, ALL_QUEUES has no duplicates

## Likely affected files
- apps/frontend/src/contracts/schemas.ts (new)
- apps/frontend/src/contracts/queues.ts (new)
- apps/frontend/src/contracts/index.ts (new)
- apps/frontend/src/contracts/__tests__/schemas.test.ts (new)
- apps/frontend/src/contracts/__tests__/queues.test.ts (new)

## Dependencies
None - Pydantic schemas already exist as source of truth.

## Definition of Done
- implementation matches scope
- npm run test:contracts passes with all tests
- Zod schemas validated against Pydantic contract spec
- PR has test evidence
