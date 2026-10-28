# TradePulse AI

A trader's dashboard that brings global and Indian markets, high-impact news, institutional flows, watchlists, alerts and short AI summaries onto one screen for pre-market and intraday use.

## Why this exists
Before and during the trading day, the information a trader needs is spread across many sites. This is a starter for collecting it in one place, refreshed automatically.

## What it does
- Polls public live sources first: NSE India (index snapshots, FII/DII flows, quotes), SEBI RSS, Moneycontrol RSS and Zerodha Pulse
- Shows global and Indian market cards, VIX, open interest and expected move
- Filters news down to high-impact items
- Produces pre-market, intraday and end-of-day summaries, with a rule-based fallback when no OpenAI key is set
- Supports watchlists and alerts; caches payloads briefly and refreshes every 30 seconds

## Project structure
```
tradepulse-ai/
├── backend/
│   ├── app/api/       FastAPI routes (/api/v1)
│   ├── app/services/  Data source adapters and summaries
│   ├── app/workers/   Celery background jobs
│   ├── app/models/    Database tables
│   ├── app/schemas/   Response models
│   ├── app/db/        Database session
│   ├── app/core/      Settings and auth
│   └── alembic/       Migrations
├── frontend/
│   ├── app/           Pages: global, india, news, insights, watchlist, alerts, admin
│   ├── components/    Dashboard widgets
│   └── lib/           API client
├── infra/             Nginx config
├── .github/workflows/ CI pipeline
├── docker-compose.yml Full local stack
└── .env.example       Required settings
```

## Getting started
Requirements: Docker and Docker Compose (or Python 3.11+ and Node.js 18+).
```bash
git clone https://github.com/abhijha8287/tradepulse-ai.git
cd tradepulse-ai
cp .env.example .env
docker compose up --build
```
| Service | Address |
|:--|:--|
| Frontend | http://localhost:3000 |
| API docs | http://localhost:8000/docs |
| Nginx gateway | http://localhost:8080 |

## Configuration
| Variable | Purpose |
|:--|:--|
| `DATABASE_URL`, `REDIS_URL` | Data stores |
| `CORS_ORIGINS`, `NEXT_PUBLIC_API_URL` | Frontend and API addresses |
| `CLERK_SECRET_KEY`, `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, `CLERK_JWKS_URL` | Optional Clerk auth |
| `OPENAI_API_KEY` | Optional AI summaries |
| `ALPHA_VANTAGE_API_KEY`, `NEWSAPI_KEY`, `FMP_API_KEY` | Optional extra data providers |
| `SENTRY_DSN` | Optional error tracking |
| `APP_ENV` | Environment name |

## Main endpoints
| Path | Returns |
|:--|:--|
| `GET /api/v1/dashboard` | Full dashboard payload |
| `GET /api/v1/markets/global` | Global market cards |
| `GET /api/v1/markets/india` | NIFTY, VIX, flows, OI, expected move |
| `GET /api/v1/news/high-impact` | High-impact news |
| `GET /api/v1/ai/insights` | Pre-market, intraday, EOD summaries |
| `GET /api/v1/admin/health` | Service status |

## Tech stack
Next.js 15, TypeScript, Tailwind CSS, TanStack Query, Recharts, Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL, Redis, Celery, Nginx, Docker, GitHub Actions

## Data Source Architecture

Adapters live in `backend/app/services/adapters.py` and `backend/app/services/live_sources.py`. The app now polls public live sources first, then falls back to deterministic starter data if a website blocks, rate-limits, or times out.

Current live sources:

- NSE India: index snapshots, FII/DII data, and watchlist equity quotes
- SEBI RSS: press releases, circulars, orders, and rulings
- Moneycontrol RSS: market, business, economy, and top-news feeds
- Zerodha Pulse: aggregated Indian market headlines

The backend caches live dashboard and quote payloads for short TTLs, while the frontend revalidates data every 30 seconds and refreshes mounted pages every 60 seconds.

Production adapters should normalize all providers into the same market/news schema:

- Market data: Yahoo Finance, Alpha Vantage, Polygon, Twelve Data
- News: NewsAPI, GDELT, Financial Modeling Prep
- Official feeds: RBI, Federal Reserve, government announcements
- Economic calendar: FRED and Investing-compatible adapters

## Database

Alembic migration `0001_initial_schema` creates tables for:

- users
- watchlists
- news
- market_data
- economic_events
- sentiment_scores
- ai_summaries
- alerts
- logs

Run migrations inside the backend container:

```bash
docker compose exec backend alembic upgrade head
```

## Deployment

Frontend can deploy to Vercel with:

- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`

Backend can deploy to Railway or Render with:

- `DATABASE_URL`
- `REDIS_URL`
- `OPENAI_API_KEY`
- provider API keys
- `CLERK_JWKS_URL`
- `SENTRY_DSN`

Run Celery worker and beat as separate services. Put Nginx or the platform router in front of FastAPI for production traffic.

## Security Notes

The scaffold includes rate-limiting middleware, CORS configuration, typed validation, SQLAlchemy query boundaries, environment-based secrets, and Sentry-ready instrumentation. Add Clerk JWT verification to protected endpoints before exposing user-specific watchlist and alert writes.
