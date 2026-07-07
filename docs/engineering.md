# Engineering Workflow

## Work model
All work is issue-driven.

```text
Issue → branch → implementation + tests → PR → CI → review → merge
```

## Branch naming

```text
feature/<issue-number>-short-name
fix/<issue-number>-short-name
ci/<issue-number>-short-name
docs/<issue-number>-short-name
```

Examples:

```text
feature/12-backend-post-videos
feature/18-ytd-worker-handler
ci/22-agent-guard
```

## Commit style
Use conventional commits when practical:

```text
feat(api): add POST /videos
feat(worker): add ytd handler
fix(ci): install frontend dependencies
chore(docs): update pipeline contract
```

## Pull requests
Every PR must include:

- linked issue;
- summary;
- tests added/updated;
- commands run;
- screenshots for UI changes when useful;
- note about contract changes if any.

## GitHub CLI
The GitHub agent may use `gh` for:

- creating issues;
- listing issues;
- creating PRs;
- checking CI status;
- merging PRs only after explicit approval.

## CI principle
CI is the neutral referee for agents.

CI must verify:

- backend tests;
- worker tests;
- frontend tests;
- contract tests;
- agent guard rules.
