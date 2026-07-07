# Worktree workflow

Use worktrees when several agents work in parallel. Do not run multiple agents in the same checkout.

## Create worktrees

PowerShell:

```powershell
.\scripts\create-worktrees.ps1
```

Bash:

```bash
./scripts/create-worktrees.sh
```

This reads `worktrees.json` and creates sibling directories next to the main checkout:

```text
tubedigest-contracts
tubedigest-backend
tubedigest-workers
tubedigest-frontend
tubedigest-qa
tubedigest-docs
```

## Open in VS Code

Open each worktree folder in a separate VS Code window. Each folder contains the whole repository, including `AGENTS.md` and `docs/`, but sits on its own branch.

## Rule

One worktree = one agent stream = one branch family.

Agents may read any file, but should modify only files required by the assigned issue.
