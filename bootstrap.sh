#!/usr/bin/env bash
set -euo pipefail

REPO_NAME=""
ORG_NAME=""
VISIBILITY="private"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-name|-r) REPO_NAME="$2"; shift 2 ;;
    --org-name|-o) ORG_NAME="$2"; shift 2 ;;
    --visibility|-v) VISIBILITY="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

[[ -n "$REPO_NAME" ]] || { echo "Usage: ./bootstrap.sh --repo-name testrepo --visibility private" >&2; exit 1; }
command -v git >/dev/null || { echo "git required" >&2; exit 1; }
command -v gh >/dev/null || { echo "gh required" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Run gh auth login first" >&2; exit 1; }

if [[ -n "$ORG_NAME" ]]; then
  REPO="$ORG_NAME/$REPO_NAME"
else
  USER="$(gh api user --jq .login)"
  REPO="$USER/$REPO_NAME"
fi

if [[ ! -d .git ]]; then
  git init -b main
fi
BRANCH="$(git branch --show-current || true)"
if [[ "$BRANCH" != "main" ]]; then
  git switch main 2>/dev/null || git checkout -b main
fi

git add .
if [[ -n "$(git status --porcelain)" ]]; then
  git commit -m "chore: bootstrap tubedigest template"
fi

if ! gh repo view "$REPO" >/dev/null 2>&1; then
  gh repo create "$REPO" "--$VISIBILITY"
fi
TARGET="https://github.com/$REPO.git"
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$TARGET"
else
  git remote add origin "$TARGET"
fi

git push -u origin main

echo "Bootstrap complete. Next:"
echo "  ./scripts/import-issues.sh $REPO"
echo "  ./scripts/create-worktrees.sh"
