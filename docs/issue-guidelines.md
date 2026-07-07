# Issue Guidelines for Architect Agent

The architect agent creates issues from project documentation. It must not invent scope outside the MVP.

## Required issue format

Each issue must include:

1. Title
2. Owner agent
3. Context
4. Scope
5. Out of scope
6. Acceptance criteria
7. Tests required
8. Files/directories likely affected
9. Dependencies
10. Definition of Done

## Issue sizing
A good issue should be completable in 15–30 minutes.

Bad:

```text
Implement complete backend and workers
```

Good:

```text
Implement POST /videos and publish video.download message
```

## Ownership rules
One issue should have one primary owner.

Allowed owners:

- architect-agent
- backend-agent
- frontend-agent
- contracts-agent
- worker-agent
- infra-agent
- github-agent
- test-engineer
- reviewer

## Dependency rules
If an issue depends on a contract, create or schedule the contract issue first.

If an agent discovers missing scope, it should create a follow-up issue instead of expanding the current one.

## Test requirements
Each issue must state tests explicitly.

Examples:

```text
Tests required:
- API test: POST /videos returns queued job.
- API test: invalid URL returns 422.
- Unit test: publisher receives video.download message.
```

## Architect output style
When asked to create MVP issues, the architect should output a numbered backlog grouped by phase:

1. Bootstrap
2. Contracts
3. Backend
4. Workers
5. Frontend
6. CI/GitHub
7. Demo/docs
