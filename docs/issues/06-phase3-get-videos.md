## Add GET /videos and GET /videos/{id} endpoints

## Owner
backend-agent

## Labels
agent:backend, scope:backend, type:feature

## Context
Users need to view submitted jobs and their processing status. This issue creates list and detail endpoints that return VideoJobResponse.

## Scope
- Add to apps/backend/src/tubedigest/routers/videos.py:
  - GET /videos - returns list of VideoJobResponse, ordered by created_at desc
  - GET /videos/{id} - returns single VideoJobResponse by ID
  - 404 response when job ID does not exist
- Tests for list and detail endpoints

## Out of scope
- POST /videos endpoint
- URL submission flow
- Frontend rendering
- Pagination or filtering

## Acceptance criteria
- GET /videos returns JSON array of VideoJobResponse
- GET /videos returns empty array when no jobs exist
- GET /videos/{id} returns matching job when it exists
- GET /videos/{id} returns 404 when job does not exist
- Response includes all VideoJobResponse fields
- Status field uses JobStatus enum values

## Tests required
- GET /videos returns empty list initially
- GET /videos returns jobs ordered by created_at desc
- GET /videos/{id} returns correct job with all fields
- GET /videos/{id} returns 404 for unknown UUID
- GET /videos/{id} returns 422 for invalid UUID format
- Response matches VideoJobResponse schema

## Likely affected files
- apps/backend/src/tubedigest/routers/videos.py (modify)
- apps/backend/tests/test_api.py (modify - add GET tests)

## Dependencies
- #3 (VideoJob model and repository)
- #5 (POST /videos - useful for test setup)

## Definition of Done
- implementation matches scope
- pytest apps/backend/tests/test_api.py passes with GET tests
- GET /videos and GET /videos/{id} return correct responses
- 404 for missing jobs
- PR has test evidence
