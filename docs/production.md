# TerrainPilot Production Guide

## Targets
- Frontend: Vercel using [`vercel.json`](/Users/zachhersick/Desktop/DevPersonal/offroad-skiing-app/vercel.json)
- API and worker: Railway using the Dockerfiles in [`infra/docker`](/Users/zachhersick/Desktop/DevPersonal/offroad-skiing-app/infra/docker)
- Data services: managed Postgres and Redis on Railway
- Fully free hosted baseline: Render using [`render.yaml`](/Users/zachhersick/Desktop/DevPersonal/offroad-skiing-app/render.yaml)

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
- `INTERNAL_API_BASE_URL`
- `RUN_INLINE_AGENT_JOBS`
- `CORS_ORIGINS`

## Deployment Sequence
1. Provision Postgres and Redis.
2. Deploy the API service with [`infra/docker/Dockerfile.api`](/Users/zachhersick/Desktop/DevPersonal/offroad-skiing-app/infra/docker/Dockerfile.api).
3. Run migrations from the API container: `alembic upgrade head`.
4. Deploy the worker with [`infra/docker/Dockerfile.worker`](/Users/zachhersick/Desktop/DevPersonal/offroad-skiing-app/infra/docker/Dockerfile.worker).
5. Deploy the web app to Vercel with the API URL exposed as `NEXT_PUBLIC_API_BASE_URL`.

## Free Render Path
1. Create a new Blueprint deploy from [`render.yaml`](/Users/zachhersick/Desktop/DevPersonal/offroad-skiing-app/render.yaml).
2. Set `OPENAI_API_KEY` only if you want live model-backed behavior later; the seeded MVP works without it.
3. Set `CORS_ORIGINS` to the Render web service URL after the frontend service is created.
4. Keep `RUN_INLINE_AGENT_JOBS=true` on the API service so the free deployment does not require a separate worker.
5. Use the web service as the public entrypoint; it proxies authenticated requests to the API service.

## Notes
- No billing or deployment actions are performed by this repo automatically.
- Live HTTP tooling remains disabled until `ENABLE_LIVE_HTTP=true` and an allowlist is configured.
- The code is ready for free hosted deployment, but an actual external deploy still requires your Render or Vercel account credentials from this machine.
