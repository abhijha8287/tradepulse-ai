# TradePulse AI

Production-ready starter for a professional trader dashboard that compresses global markets, Indian markets, macro news, volatility, institutional flows, options context, sentiment, watchlists, alerts, and AI summaries into a fast pre-market and intraday command center.

## Stack

- Frontend: Next.js 15 App Router, TypeScript, Tailwind CSS, TanStack Query, Recharts, Framer Motion-ready UI
- Backend: FastAPI, SQLAlchemy, Alembic, PostgreSQL, Redis, Celery
- AI: OpenAI/LangChain integration boundary with deterministic fallback summaries
- Auth: Clerk-ready environment and JWT verification boundary
- Ops: Docker Compose, Nginx, Sentry-ready logging, GitHub Actions

## Run Locally

1. Copy `.env.example` to `.env`.
2. Start everything:

```bash
docker compose up --build
```

3. Open:

- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs
- Nginx gateway: http://localhost:8080

For local non-Docker development:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

```bash
cd frontend
npm install
npm run dev
```

## API Modules

- `GET /api/v1/dashboard` complete dashboard payload
- `GET /api/v1/markets/global` global market cards
- `GET /api/v1/markets/india` NIFTY, VIX, flows, OI, expected move
- `GET /api/v1/news/high-impact` filtered high-impact news
- `GET /api/v1/ai/insights` pre-market, intraday, EOD summaries
- `GET /api/v1/admin/health` operational status

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
