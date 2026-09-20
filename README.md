# Pulse

Create a poll, share the link, watch results update live.

**Live:** [pulse-sigma-eosin.vercel.app](https://pulse-sigma-eosin.vercel.app) · API: [pulse-p86x.onrender.com](https://pulse-p86x.onrender.com/docs)

## Why this project

My other repos are mostly single-concept exercises: one GoF pattern per repo,
one testing technique per repo, one framework per repo. Useful for learning
in isolation, but none of them show how the pieces fit together in a real
system. Pulse is a small, complete vertical slice (create poll → vote → see
results) that puts several architectural decisions in one place, wired
end-to-end, so they can be reviewed together instead of one at a time.

## What's new here versus my earlier repos

- **Hexagonal architecture in the backend is now enforced by module
  boundaries**, not just described in a README. `domain/` has zero imports
  from `infrastructure/` or `interface/`; the only thing crossing that line
  is the `PollRepository` `Protocol` in `domain/ports.py`. Earlier repos
  (`spring-clean-architecture-testing-example`) demonstrated the pattern
  once; here it's the only way the app is built.
- **Contract-first FE/BE integration.** `packages/contracts` is the single
  source of truth for the wire format (Zod on the frontend), and a
  consumer-driven Pact test (`apps/web`) is verified against the live
  FastAPI app (`apps/api`) in CI — the two codebases never need to run each
  other's test suite to know they still agree. This generalizes what
  `cdct-testing` explored in isolation.
- **The full testing pyramid runs against the real thing, not mocks**: unit
  tests use a fake in-memory repository (proving the port abstraction is
  real), integration tests spin up an actual Postgres via Testcontainers,
  and Playwright drives the actual built Next.js app against the actual
  API. This is the practice from `spring-boot-testcontainers-crud` and
  `fullstack-e2e-playwright-example`, combined into one pipeline.
- **A monorepo that has an actual reason to be one**: the frontend and
  backend share a typed contract package, so a schema change in the API
  shows up as a type error in the web app before it ships. `my-turborepo`
  and `monorepo-storybook-alternatives` were monorepo mechanics practice;
  this is the first time the shared package carries real weight.

## Architecture

```
apps/
  web/            Next.js 15 (App Router), feature-sliced (features/polls/*)
  api/            FastAPI, hexagonal: domain -> application -> infrastructure/interface
packages/
  contracts/      Zod schemas + TS types shared by web (and mirrored by the API's
                   Pydantic schemas, which serialize to the same camelCase shape)
```

### Backend — hexagonal / ports & adapters

```
domain/           Poll, PollOption entities + business rules (pure Python, no I/O)
                  PollRepository Protocol (the port)
application/      PollService: use cases, orchestrates domain + port
infrastructure/   SQLAlchemy models + SqlAlchemyPollRepository (the adapter)
interface/        FastAPI routers, Pydantic schemas, composition root (main.py)
```

The dependency rule is one-directional: `interface` and `infrastructure` both
depend on `domain`; `domain` depends on nothing. Swapping Postgres for
something else means writing a new adapter for `PollRepository` — the domain
and application layers don't change, and neither do their tests.

### Frontend — feature-sliced, server components by default

Pages under `app/` are thin; the actual feature logic (data fetching hooks,
components, API client) lives in `features/polls/`. TanStack Query owns
server state (polling refresh instead of websockets — a deliberate
trade-off for a serverless deploy target, see below); there's no global
client state store because the app doesn't need one yet.

### Deploy shape

The frontend and the API deploy to different hosts, on purpose — see
[Deploying](#deploying) below for why and where.

## Testing strategy

| Layer | Tool | What it proves | Location |
|---|---|---|---|
| Domain unit | pytest | Business rules in isolation, no I/O | `apps/api/tests/unit` |
| Application unit | pytest + fake repo | Use cases work against the `PollRepository` port | `apps/api/tests/unit` |
| Repository integration | pytest + Testcontainers | The SQLAlchemy adapter works against real Postgres | `apps/api/tests/integration` |
| Contract | Pact (consumer in web, provider verification in api) | FE and BE agree on the wire format without a shared test run | `apps/web/src/features/polls/__tests__`, `apps/api/tests/contract` |
| Component unit | Vitest + Testing Library | UI renders correctly for given data | `apps/web/src/features/polls/components/__tests__` |
| E2E | Playwright | The full stack (web + api + db) supports the create → vote → see-results flow | `apps/web/e2e` |

All of it runs in `.github/workflows/ci.yml` as separate jobs so a failure
tells you which layer broke, not just "something broke."

## Deploying

Frontend and backend deploy independently, on different hosts, because they
have different runtime shapes — that split is itself an architecture
decision, not an accident:

- **`apps/web` → [Vercel](https://vercel.com).** Connected to this repo's
  `main` branch, builds via `pnpm turbo run build --filter=@pulse/web` from
  the repo root (see `vercel.json`), redeploys automatically on every push.
- **`apps/api` → [Render](https://render.com)**, from `apps/api/Dockerfile`.
  It needs a long-lived process (persistent async DB connections, Alembic
  migrations on boot), which is a different shape than Vercel's serverless
  functions are built for — Fly.io or Railway would fit the same profile.
- **Database → [Neon](https://neon.tech)**, serverless Postgres, connected
  to the API via its direct (non-pooled) endpoint so SQLAlchemy's own
  connection pool isn't fighting PgBouncer's transaction-mode prepared
  statement handling.

The API's container command runs `alembic upgrade head` before starting
`uvicorn`, so schema migrations ship as part of every deploy instead of a
separate manual step.

Note: on Render's free tier the API sleeps after ~15 minutes idle, so the
first request after a quiet period takes 30-50s to wake it up.

## Running locally

```bash
pnpm install

# backend
cd apps/api
pip install -e ".[dev]"
docker compose -f ../../docker-compose.yml up -d postgres
alembic upgrade head
uvicorn pulse_api.interface.main:app --reload

# frontend (separate shell)
cd apps/web
pnpm dev
```

## What's deliberately left out (next iterations)

- Auth — polls are public/anonymous by design for this slice; adding
  poll-owner accounts is the natural next vertical slice and would exercise
  the hexagonal boundaries again (a new `User` aggregate, a new port).
- Real-time results via SSE/websockets instead of polling — the API's host
  (a long-lived container) could support it now, but the frontend still
  needs to special-case it for the fact that Vercel's serverless functions
  can't hold a persistent connection open; polling was the smaller change
  for this slice.
- OpenTelemetry tracing — the API already emits structured JSON request
  logs with a correlation id (`infrastructure/logging.py`), which covers
  "what happened and how long did it take." Distributed tracing across
  web → api → db is the natural next step once there's a second service to
  trace across; wiring an OTel exporter is a small addition on top of the
  existing composition root in `main.py`.
