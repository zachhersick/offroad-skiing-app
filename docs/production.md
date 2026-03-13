# TerrainPilot Production Guide

## Targets
- Frontend: Vercel using [`vercel.json`](/Users/zachhersick/Desktop/DevPersonal/offroad-skiing-app/vercel.json)
- API and worker: Railway using the Dockerfiles in [`infra/docker`](/Users/zachhersick/Desktop/DevPersonal/offroad-skiing-app/infra/docker)
- Data services: managed Postgres and Redis on Railway

## Required Environment Variables
- `DATABASE_URL`
- `REDIS_URL`
- `JWT_SECRET`
- `JWT_REFRESH_SECRET`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- `ENABLE_LIVE_HTTP`
- `APPROVED_HTTP_HOSTS`
- `NEXT_PUBLIC_API_BASE_URL`

## Deployment Sequence
1. Provision Postgres and Redis.
2. Deploy the API service with [`infra/docker/Dockerfile.api`](/Users/zachhersick/Desktop/DevPersonal/offroad-skiing-app/infra/docker/Dockerfile.api).
3. Run migrations from the API container: `alembic upgrade head`.
4. Deploy the worker with [`infra/docker/Dockerfile.worker`](/Users/zachhersick/Desktop/DevPersonal/offroad-skiing-app/infra/docker/Dockerfile.worker).
5. Deploy the web app to Vercel with the API URL exposed as `NEXT_PUBLIC_API_BASE_URL`.

## Notes
- No billing or deployment actions are performed by this repo automatically.
- Live HTTP tooling remains disabled until `ENABLE_LIVE_HTTP=true` and an allowlist is configured.

