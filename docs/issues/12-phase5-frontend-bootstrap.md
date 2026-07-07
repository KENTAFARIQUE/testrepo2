## Bootstrap frontend React app with API client and Dockerfile

## Owner
frontend-agent

## Labels
agent:frontend, scope:frontend, type:feature

## Context
The frontend directory has package.json and vite.config.ts but no source code. This issue creates the React application shell with routing, typed API client using Zod, main layout, and Dockerfile.

## Scope
- Create apps/frontend/src/main.tsx - React entry point
- Create apps/frontend/src/App.tsx - Main app component with routing (react-router)
- Create apps/frontend/src/api/client.ts - API client with:
  - createVideo(url) returning typed VideoJobResponse
  - listVideos() returning typed VideoJobResponse array
  - getVideo(id) returning typed VideoJobResponse
  - Base URL configurable via env var
  - Zod validation on all responses
- Create apps/frontend/src/pages/HomePage.tsx placeholder
- Create apps/frontend/src/pages/JobDetailPage.tsx placeholder
- Create apps/frontend/src/index.css with Tailwind directives
- Create apps/frontend/Dockerfile for nginx or vite preview
- Wire react-router for routes: / (home) and /jobs/:id (detail)
- Tests for API client and basic rendering

## Out of scope
- Submit form component
- Job list component
- Status timeline component
- Result card component

## Acceptance criteria
- npm run dev starts and shows home page
- npm test passes
- API client methods return typed responses
- API client validates responses with Zod schemas
- Dockerfile builds without error
- Routing works: / shows HomePage, /jobs/:id shows JobDetailPage

## Tests required
- API client: createVideo sends POST request with correct body
- API client: listVideos returns array of VideoJobResponse
- API client: getVideo returns single VideoJobResponse
- API client: invalid response throws Zod validation error
- App renders without crashing (smoke test)
- Routes render correct placeholder pages

## Likely affected files
- apps/frontend/src/main.tsx (new)
- apps/frontend/src/App.tsx (new)
- apps/frontend/src/api/client.ts (new)
- apps/frontend/src/pages/HomePage.tsx (new)
- apps/frontend/src/pages/JobDetailPage.tsx (new)
- apps/frontend/src/index.css (new)
- apps/frontend/Dockerfile (new)
- apps/frontend/src/__tests__/App.test.tsx (new)
- apps/frontend/src/__tests__/api.test.ts (new)

## Dependencies
#1 (Zod schemas - needed for API client response validation)

## Definition of Done
- implementation matches scope
- npm test passes
- npm run build succeeds
- Dockerfile builds
- PR has test evidence
