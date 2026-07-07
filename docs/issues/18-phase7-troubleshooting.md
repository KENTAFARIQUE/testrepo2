## Add troubleshooting and final demo polish

## Owner
infra-agent

## Labels
agent:infra, scope:infra, type:docs

## Context
The project needs troubleshooting documentation and final polish to ensure a smooth demo experience. This issue consolidates common issues, adds debugging tips, and verifies the full setup works.

## Scope
- Create docs/troubleshooting.md with sections for:
  - Common setup issues (RabbitMQ not starting, port conflicts)
  - No jobs appearing - debugging steps
  - Worker not consuming messages
  - Fake mode vs real mode configuration
  - How to check logs for each service
  - How to reset state (delete SQLite DB)
- Update .env.example with comments explaining each variable
- Verify docker compose up --build works end-to-end
- Verify make test passes
- Verify make ci-local passes
- File any remaining small issues as follow-ups

## Out of scope
- Feature implementation
- Changing contracts
- Adding new tests beyond verification

## Acceptance criteria
- docs/troubleshooting.md documents 5+ common issues
- .env.example has comments explaining each variable
- docker compose up --build succeeds
- make test passes (all CI commands)
- make ci-local passes
- Demo can be presented without surprises

## Tests required
- No code tests - this is documentation and verification
- Manual verification: full docker compose up from clean state

## Likely affected files
- docs/troubleshooting.md (new)
- .env.example (modify - add comments)
- README.md (minor polish)

## Dependencies
#17 (README demo script - needs demo flow first)

## Definition of Done
- implementation matches scope
- docker compose up --build verified working
- make test passes
- make ci-local passes
- Troubleshooting docs cover common issues
- PR has evidence of verification
