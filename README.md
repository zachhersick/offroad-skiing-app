# TerrainPilot

TerrainPilot is a workspace-first trip planning and recommendation app for off-road and ski enthusiasts. The MVP is off-road-first, but the schema, runtime, and UI support both modes from the start.

## Stack
- Next.js + TypeScript + Tailwind
- FastAPI + SQLAlchemy + Pydantic
- Postgres + Redis
- Docker Compose for local development
- OpenAI-first agent runtime with bounded planner, executor, and reviewer roles

## Local Development
1. Copy `.env.example` to `.env` and set secrets.
2. Start the stack:
   ```bash
   docker compose up --build
   ```
3. Open `http://localhost:3000` for the web app and `http://localhost:8000/docs` for the API.
4. Postgres and Redis are network-internal by default to avoid host port conflicts; access them from containers unless you intentionally add host bindings.

## Services
- `apps/web`: Next.js frontend
- `apps/api`: FastAPI backend
- `apps/worker`: background processor for agent runs
- `packages/agent-core`: bounded multi-agent runtime and tool system
- `packages/shared`: shared TypeScript types

## Core Workflow
1. Create an account and profile.
2. Add a vehicle or ski quiver.
3. Submit a planner request.
4. Inspect recommendations, checklist, and review artifacts.
5. Approve any external side effects before execution resumes.

## Data Model
The API stores users, profiles, vehicles, ski quivers, gear items, trips, routes, trail entries, resort entries, conditions, packing lists, recommendations, agent runs, step logs, artifacts, and approvals.

## Testing
- Python tests:
  ```bash
  docker compose run --rm api pytest
  ```
- Web lint:
  ```bash
  docker compose run --rm web pnpm lint
  ```
- Web end-to-end:
  ```bash
  docker compose run --rm web pnpm test:e2e
  ```

## Deployment
See [`docs/production.md`](/Users/zachhersick/Desktop/DevPersonal/offroad-skiing-app/docs/production.md) for Vercel and Railway setup.

## Safety
- No repo code triggers paid API calls by default.
- Live HTTP requests in the planner are approval-gated and only progress when the feature flag is enabled.
- Approval is required before any external network action or shell command execution.
