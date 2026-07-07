# Issue-driven Development Rules

Each issue must be independently understandable and testable.

## Required issue sections

- Goal
- Scope
- Non-goals
- Affected area
- Contracts changed
- Acceptance criteria
- Required tests
- Demo notes

## Definition of Done

An issue is done only when:

- implementation is complete;
- tests are added or updated;
- focused tests pass;
- relevant contracts are updated;
- docs are updated if behavior or setup changed;
- the agent reports exact commands run.

## Agent handoff format

At the end of a session, the agent must report:

```text
Changed files:
Tests added:
Commands run:
Result:
Known gaps:
Next recommended issue:
```
