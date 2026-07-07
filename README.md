# TubeDigest

TubeDigest is a one-hour MVP for demonstrating issue-driven multi-agent development with opencode.

The product: submit a YouTube URL and process it through an asynchronous RabbitMQ pipeline:

```text
URL → download → audio/thumbnail → transcription → summary → tags/chapters → dashboard
```

## Stack

- Backend: FastAPI
- DB: SQLite + SQLAlchemy
- Queue: RabbitMQ
- Frontend: React + Vite + TypeScript
- UI: Tailwind CSS
- Contracts: Pydantic + Zod
- Download: yt-dlp worker
- Media: ffmpeg worker
- Models: Groq Whisper + Groq LLM workers
- CI/CD: GitHub Actions
- Workflow: GitHub CLI + opencode agents

## Recommended setup

This template intentionally separates bootstrapping, issue import, and worktree creation.

### 1. Create GitHub repo and push template

PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\bootstrap.ps1 -RepoName testrepo1 -Visibility private
```

Or use the cmd wrapper:

```cmd
bootstrap.cmd -RepoName testrepo1 -Visibility private
```

Bash:

```bash
./bootstrap.sh --repo-name testrepo1 --visibility private
```

The bootstrap script only:

- initializes git if needed;
- creates or connects the GitHub repository;
- pushes `main`;
- syncs labels from `.github/labels.yml`.

### 2. Import the 18 issues

PowerShell:

```powershell
.\scripts\import-issues.ps1
```

Or explicitly:

```powershell
.\scripts\import-issues.ps1 -Repo KENTAFARIQUE/testrepo1
```

Bash:

```bash
./scripts/import-issues.sh KENTAFARIQUE/testrepo1
```

The issue files live in `docs/issues/`. Their content is not rewritten by the import script.

### 3. Create worktrees for parallel agents

PowerShell:

```powershell
.\scripts\create-worktrees.ps1
```

Bash:

```bash
./scripts/create-worktrees.sh
```

This reads `worktrees.json` and creates sibling folders next to the main checkout:

```text
tubedigest-contracts
tubedigest-backend
tubedigest-workers
tubedigest-frontend
tubedigest-qa
tubedigest-docs
```

Open each folder in a separate VS Code window.

## Important docs

Start here:

- `AGENTS.md`
- `docs/project.md`
- `docs/architecture.md`
- `docs/pipeline.md`
- `docs/contracts.md`
- `docs/testing.md`
- `docs/issue-guidelines.md`
- `docs/roadmap.md`
- `docs/development/import-issues.md`
- `docs/development/worktrees.md`

## Agents

Configured agents live in `.opencode/agents/`:

- `architect-agent`
- `backend-agent`
- `frontend-agent`
- `contracts-agent`
- `worker-agent`
- `infra-agent`
- `github-agent`
- `test-engineer`
- `reviewer`

## Local commands

```bash
make test
make test-backend
make test-frontend
make test-workers
make test-contracts
make compose-config
```

## Environment

Copy `.env.example` to `.env` and add secrets locally:

```bash
cp .env.example .env
```

Never commit `.env`.
