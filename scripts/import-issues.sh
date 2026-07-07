#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-}"
if [[ -z "$REPO" ]]; then
  ORIGIN="$(git remote get-url origin 2>/dev/null || true)"
  if [[ "$ORIGIN" =~ github.com[:/]([^/]+)/([^/.]+)(\.git)?$ ]]; then
    REPO="${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
  else
    echo "Pass repo as first arg: ./scripts/import-issues.sh owner/repo" >&2
    exit 1
  fi
fi

for f in docs/issues/[0-9][0-9]-*.md; do
  title="$(grep -m1 -E '^#{1,2} ' "$f" | sed -E 's/^#{1,2} //')"
  [[ -n "$title" ]] || title="$(basename "$f" .md)"
  labels="$(awk 'BEGIN{found=0} /^## Labels/{found=1; next} /^## /{if(found) exit} found{print}' "$f" | tr '\n' ' ' | sed 's/[[:space:]]//g')"

  if gh issue list --repo "$REPO" --state all --limit 300 --json title --jq '.[].title' | grep -Fxq "$title"; then
    echo "[skip] $title"
    continue
  fi

  args=(issue create --repo "$REPO" --title "$title" --body-file "$f")
  if [[ -n "$labels" ]]; then
    IFS=',' read -ra labs <<< "$labels"
    for lab in "${labs[@]}"; do
      [[ -n "$lab" ]] && args+=(--label "$lab")
    done
  fi
  gh "${args[@]}"
done
