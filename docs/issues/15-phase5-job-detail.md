## Add job detail with status timeline and result card

## Owner
frontend-agent

## Labels
agent:frontend, scope:frontend, type:feature

## Context
Users need to see detailed job progress and final results. This issue creates a job detail page with a visual status timeline and a result card showing summary, tags, and chapters.

## Scope
- Create apps/frontend/src/components/StatusTimeline.tsx:
  - Visual step indicator for pipeline stages
  - Shows completed steps as green, current as blue, future as gray
  - Shows failed step with error message
- Create apps/frontend/src/components/ResultCard.tsx:
  - Displays when status=completed
  - Shows: title, summary, tags as chips, chapters as list
- Create apps/frontend/src/pages/JobDetailPage.tsx:
  - Fetches job by ID on mount
  - Renders StatusTimeline
  - Renders ResultCard if completed
  - Polls/refreshes every 5 seconds while job is processing
  - Loading state
  - 404 error state (job not found)
- Tests for all components

## Out of scope
- URL submit form
- Job list view
- Modifying job data

## Acceptance criteria
- StatusTimeline shows all pipeline steps with correct visual state
- StatusTimeline highlights current_step
- StatusTimeline shows error for failed jobs
- ResultCard renders summary, tags, chapters when job is completed
- ResultCard is hidden when job is not completed
- JobDetailPage fetches job by ID from URL param
- JobDetailPage polls while job is processing
- 404 shows Job not found message

## Tests required
- StatusTimeline renders all steps
- StatusTimeline highlights current step
- StatusTimeline shows completed steps as green
- StatusTimeline shows failed step
- ResultCard renders title, summary, tags, chapters
- ResultCard hidden when job not completed
- JobDetailPage fetches job by ID
- JobDetailPage shows loading state
- JobDetailPage shows 404 error for missing job
- JobDetailPage polls non-terminal statuses

## Likely affected files
- apps/frontend/src/components/StatusTimeline.tsx (new)
- apps/frontend/src/components/StatusTimeline.test.tsx (new)
- apps/frontend/src/components/ResultCard.tsx (new)
- apps/frontend/src/components/ResultCard.test.tsx (new)
- apps/frontend/src/pages/JobDetailPage.tsx (modify)
- apps/frontend/src/pages/JobDetailPage.test.tsx (new)

## Dependencies
#12 (frontend bootstrap - needs API client and routing)

## Definition of Done
- implementation matches scope
- npm test passes with all new tests
- StatusTimeline shows correct pipeline state
- ResultCard shows completed data
- Detail page polls while processing
- PR has test evidence
