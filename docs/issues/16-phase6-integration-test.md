## Add fake full pipeline integration test

## Owner
test-engineer

## Labels
agent:test, scope:backend, type:test

## Context
The testing strategy requires one integration test that exercises the full pipeline from job creation through all worker handlers using fake adapters, without Docker or RabbitMQ.

## Scope
- Create tests/integration/test_full_pipeline.py:
  - Set up temporary SQLite database
  - Create fake publisher that records messages
  - Walk through the full pipeline:
    1. Create a VideoJob via repository
    2. Run ytd handler with fake downloader
    3. Run ffmpeg handler with fake processor (audio extract)
    4. Run ffmpeg handler with fake processor (thumbnail generate)
    5. Run transcribe handler with fake transcriber
    6. Run summary handler with fake summarizer
    7. Run tags handler with fake tagger
  - Assert job ends in completed status
  - Assert all fields populated (video_path, audio_path, thumbnail_path, transcript, summary, tags, chapters)
  - Assert correct queue messages published at each step
- Ensure test can run without Docker, RabbitMQ, YouTube, ffmpeg, or Groq

## Out of scope
- Any real external service calls
- Docker Compose based tests
- Performance or load tests

## Acceptance criteria
- Pipeline test passes in CI without external services
- All 7 handler steps execute in order
- Job ends in completed status
- All result fields have expected values
- Correct queue messages published at each transition
- Test runs as part of make test

## Tests required
- Integration: full pipeline from create to completed
- Assert status transitions through all pipeline steps
- Assert all result fields populated
- Assert each queue message published in correct order

## Likely affected files
- tests/integration/test_full_pipeline.py (new)
- tests/integration/__init__.py (new)
- pytest conftest.py for shared fixtures (if needed)

## Dependencies
- All Phase 3 issues (backend: model, publisher, API)
- All Phase 4 issues (all 5 workers: handler + adapters)
- contracts package (Pydantic schemas, queue constants)

## Definition of Done
- implementation matches scope
- pytest tests/integration/ passes without Docker or external services
- Pipeline job completes with all fields populated
- PR has test evidence
