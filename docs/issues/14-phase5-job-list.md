## Add job list view with status badges

## Owner
frontend-agent

## Labels
agent:frontend, scope:frontend, type:feature

## Context
Users need to see all submitted jobs and their current status. This issue creates a job list component that fetches jobs from the API and displays them with status badges.

## Scope
- Create apps/frontend/src/components/JobList.tsx:
  - Fetches job list from API on mount
  - Displays table/cards with: title/url, status badge, created_at
  - Loading state
  - Empty state (No jobs yet message)
  - Error state with retry option
  - Each row links to /jobs/:id
- Create apps/frontend/src/components/StatusBadge.tsx:
  - Renders colored badge for each JobStatus value
  - Distinct colors for each status group
- Create apps/frontend/src/components/JobList.test.tsx
- Create apps/frontend/src/components/StatusBadge.test.tsx
- Wire JobList into HomePage below the submit form

## Out of scope
- URL submit form
- Job detail view
- Status timeline

## Acceptance criteria
- JobList fetches and displays jobs on mount
- Each job shows status badge with correct color
- Empty state shows No jobs yet message
- Loading state shows spinner or skeleton
- Error state shows retry option
- Each job row links to /jobs/:id
- StatusBadge renders all 10 statuses with distinct colors

## Tests required
- JobList renders job rows from mocked API
- JobList shows empty state when list is empty
- JobList shows loading state during fetch
- JobList shows error state on API failure
- JobList links to job detail page
- StatusBadge renders correct color for each status
- StatusBadge handles unknown status gracefully

## Likely affected files
- apps/frontend/src/components/JobList.tsx (new)
- apps/frontend/src/components/JobList.test.tsx (new)
- apps/frontend/src/components/StatusBadge.tsx (new)
- apps/frontend/src/components/StatusBadge.test.tsx (new)
- apps/frontend/src/pages/HomePage.tsx (modify)

## Dependencies
#12 (frontend bootstrap - needs API client and routing)

## Definition of Done
- implementation matches scope
- npm test passes with JobList and StatusBadge tests
- Job list renders from API data
- Status colors match convention
- PR has test evidence
