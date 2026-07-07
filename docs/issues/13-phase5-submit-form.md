## Add URL submit form component

## Owner
frontend-agent

## Labels
agent:frontend, scope:frontend, type:feature

## Context
Users need to submit YouTube URLs for processing. This issue creates a URL input form on the home page that validates input, calls the API, and navigates to the job detail page.

## Scope
- Create apps/frontend/src/components/SubmitForm.tsx:
  - URL input field with label
  - Submit button
  - Client-side validation (non-empty URL using Zod)
  - Calls api.createVideo() on submit
  - Loading state during submission
  - Error display for API failures
  - On success: navigate to /jobs/:id
- Create apps/frontend/src/components/SubmitForm.test.tsx:
  - Renders form with input and button
  - Valid URL submits and redirects
  - Empty URL shows validation error
  - API error shows error message
- Wire SubmitForm into HomePage

## Out of scope
- Job list
- Job detail view
- Status timeline

## Acceptance criteria
- Form renders with URL input and submit button
- Submitting valid URL calls createVideo API and navigates to detail page
- Submitting empty URL shows inline validation error
- API failure shows error message to user
- Loading state disables submit button
- Input field has proper label and accessibility attributes

## Tests required
- Form renders input and button
- Submit with valid URL calls API and navigates
- Submit with empty URL shows validation error
- Submit during loading shows disabled button
- API error displays error message

## Likely affected files
- apps/frontend/src/components/SubmitForm.tsx (new)
- apps/frontend/src/components/SubmitForm.test.tsx (new)
- apps/frontend/src/pages/HomePage.tsx (modify)

## Dependencies
#12 (frontend bootstrap - needs API client and routing)

## Definition of Done
- implementation matches scope
- npm test passes with SubmitForm tests
- Form submits valid URL and navigates
- Invalid URL shows client-side error
- PR has test evidence
