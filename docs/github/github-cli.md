# GitHub CLI workflow

This repository is designed for issue-driven multi-agent development. The GitHub CLI (`gh`) is the control surface for creating issues, assigning labels, opening PRs, and checking CI.

## Setup

```bash
gh auth login
gh repo create tubedigest --private --source=. --remote=origin --push
```

Sync labels after the repository exists:

```bash
while IFS= read -r line; do echo "$line"; done < .github/labels.yml
# Option A: use a label-sync action/tool later.
# Option B: create labels manually through GitHub UI for the MVP demo.
```

## Issue-first flow

Create one issue per agent-sized task:

```bash
gh issue create \
  --title "Implement backend video API" \
  --label "agent:backend,scope:backend,type:feature,ready-for-agent" \
  --body-file docs/issues/example-issues.md
```

Pick an issue:

```bash
gh issue list --label ready-for-agent
gh issue view 1
```

Create a branch:

```bash
git checkout -b issue-1-backend-video-api
```

Open a PR:

```bash
gh pr create --fill --base main --head issue-1-backend-video-api
```

Watch checks:

```bash
gh pr checks --watch
gh run list
gh run view --log
```

Merge only after CI is green and review is complete:

```bash
gh pr merge --squash --delete-branch
```

## Agent control rules

- Every PR must link an issue using `Closes #123`, `Fixes #123`, or `Resolves #123`.
- Every PR must include test evidence.
- Each issue should target one layer unless the contract requires a coordinated change.
- If an agent changes a contract, it must update both Pydantic and Zod tests.
- CI is the quality gate; do not merge failing checks.
