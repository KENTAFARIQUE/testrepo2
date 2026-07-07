.PHONY: test test-backend test-workers test-frontend test-contracts lint dev compose-config ci-local gh-checks gh-pr-check

test: test-contracts test-backend test-workers test-frontend

test-backend:
	cd apps/backend && pytest

test-workers:
	pytest workers

test-frontend:
	cd apps/frontend && npm test

test-contracts:
	pytest packages/contracts || true
	cd apps/frontend && npm run test:contracts || true

lint:
	@echo "TODO: add ruff, mypy, eslint, prettier"

dev:
	docker compose up --build

compose-config:
	docker compose config

ci-local: compose-config test

# Requires GitHub CLI auth.
gh-checks:
	gh pr checks --watch

gh-pr-check:
	gh pr view --json title,body,headRefName,baseRefName,labels,reviewDecision,statusCheckRollup
