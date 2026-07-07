#!/usr/bin/env bash
set -euo pipefail

CONFIG="${1:-worktrees.json}"
BASE_BRANCH="${2:-main}"
PARENT_DIR="${3:-$(dirname "$(pwd)")}"

command -v python3 >/dev/null 2>&1 || { echo "python3 required" >&2; exit 1; }
[[ -f "$CONFIG" ]] || { echo "Config not found: $CONFIG" >&2; exit 1; }

git rev-parse --verify "$BASE_BRANCH" >/dev/null 2>&1 || { echo "Base branch not found: $BASE_BRANCH" >&2; exit 1; }

python3 - <<PY | while IFS=$'\t' read -r suffix branch; do
import json
with open('$CONFIG', 'r', encoding='utf-8') as f:
    data = json.load(f)
items = data.get('worktrees', data if isinstance(data, list) else [])
for item in items:
    suffix = item.get('path_suffix') or item.get('key')
    branch = item.get('branch')
    if suffix and branch:
        print(f"{suffix}\t{branch}")
PY
  path="$PARENT_DIR/tubedigest-$suffix"
  if [[ -e "$path" ]]; then
    echo "[skip] $path exists"
    continue
  fi
  if git branch --list "$branch" | grep -q .; then
    git worktree add "$path" "$branch"
  else
    git worktree add -b "$branch" "$path" "$BASE_BRANCH"
  fi
  echo "[ok] $path -> $branch"
done

echo
echo "Open these folders:"
python3 - <<PY
import json, os
with open('$CONFIG', 'r', encoding='utf-8') as f:
    data = json.load(f)
items = data.get('worktrees', data if isinstance(data, list) else [])
for item in items:
    suffix = item.get('path_suffix') or item.get('key')
    if suffix:
        print('  ' + os.path.join('$PARENT_DIR', 'tubedigest-' + suffix))
PY
