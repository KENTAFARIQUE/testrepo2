# GitHub Actions CI/CD

The MVP uses GitHub Actions as a quality gate rather than a production deployment system.

## Workflows

### CI

`.github/workflows/ci.yml` runs:

- contract tests;
- backend tests;
- worker tests;
- frontend tests and build;
- Docker Compose config validation.

### Agent Guard

`.github/workflows/agent-guard.yml` checks that agent PRs follow the issue-driven rules:

- PR body links an issue;
- PR body includes test evidence;
- generated media files from `storage/` are not committed;
- broad cross-layer changes are flagged.

## Recommended branch protection

Enable these rules on `main`:

- require pull request before merge;
- require status checks to pass;
- require branches to be up to date;
- require conversation resolution;
- block force pushes;
- optionally require one approval.

Required checks:

```text
Contracts
Backend
Workers
Frontend
Docker Compose Smoke
Issue-driven guardrails
```

## Secrets

For real model integration, configure:

```text
GROQ_API_KEY
```

Tests must not require this secret. Unit tests should use fake model clients.
