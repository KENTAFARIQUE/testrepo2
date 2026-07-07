## Add README demo script and sample issue flow

## Owner
github-agent

## Labels
agent:infra, scope:infra, type:docs

## Context
The project needs to be easy to demo. This issue adds a demo script to the README that walks through the full issue-driven development flow, and provides sample issue/PR commands.

## Scope
- Update README.md with:
  - Quick start section (prerequisites, setup steps)
  - Demo walkthrough: From Issue to PR in 5 minutes
  - Sample commands for creating issues, branches, PRs
  - Architecture diagram (ASCII from docs)
  - Link to all documentation files
- Create docs/demo.md with:
  - End-to-end demo script
  - Expected output at each step
  - Troubleshooting tips for demo presenters
- Verify all Makefile targets work as documented

## Out of scope
- Product code changes
- CI workflow changes
- Infrastructure changes

## Acceptance criteria
- README has Quick Start section that works from clean clone
- Demo walkthrough shows issue creation, branch, PR flow
- docs/demo.md is self-contained for presentation
- All Makefile commands in README are accurate

## Tests required
- No code tests - this is a documentation issue
- Manual verification: follow demo script from clean state

## Likely affected files
- README.md (modify)
- docs/demo.md (new)
- Makefile (minor fixes if needed)

## Dependencies
All implementation issues complete.

## Definition of Done
- implementation matches scope
- README quick start works from clean clone
- Demo walkthrough covers issue-to-PR flow
- PR has evidence of manual verification
