from fastapi import APIRouter
from app.schemas.dashboard import (
    AdminHealthSchema,
    AISummarySchema,
    AlertRuleSchema,
    AlertUpdateRequest,
    DashboardSchema,
    EconomicEventSchema,
    MarketItem,
    NewsItemSchema,
    WatchlistSchema,
    WatchlistSymbolRequest,
)
from app.services.ai import market_brain
from app.services.cache import cache
from app.services.live_sources import build_live_dashboard, fetch_high_impact_news, get_live_admin_health, get_live_events, get_live_watchlist
from app.services.seed_data import (
    add_watchlist_symbol,
    build_alerts,
    remove_watchlist_symbol,
    update_alert,
)

router = APIRouter()


@router.get("/dashboard", response_model=DashboardSchema)
async def dashboard() -> dict:
    return await build_live_dashboard()


@router.get("/markets/global")
async def global_markets() -> dict[str, list[MarketItem]]:
    dashboard_payload = await build_live_dashboard()
    return {"markets": dashboard_payload["global_markets"]}


@router.get("/markets/india", response_model=DashboardSchema)
async def india_markets() -> dict:
    return await build_live_dashboard()


@router.get("/news/high-impact")
async def high_impact_news() -> dict[str, list[NewsItemSchema]]:
    news = await fetch_high_impact_news()
    if news:
        return {"news": news}
    dashboard_payload = await build_live_dashboard()
    return {"news": dashboard_payload["news"]}


@router.get("/ai/insights", response_model=AISummarySchema)
def ai_insights() -> dict:
    return market_brain.summarize()


@router.get("/watchlist", response_model=WatchlistSchema)
async def watchlist() -> dict:
    return await get_live_watchlist()


@router.post("/watchlist", response_model=WatchlistSchema)
async def add_symbol(payload: WatchlistSymbolRequest) -> dict:
    cache.delete("live:watchlist")
    add_watchlist_symbol(payload.symbol)
    return await get_live_watchlist()


@router.delete("/watchlist/{symbol}", response_model=WatchlistSchema)
async def remove_symbol(symbol: str) -> dict:
    cache.delete("live:watchlist")
    remove_watchlist_symbol(symbol)
    return await get_live_watchlist()


@router.get("/alerts", response_model=dict[str, list[AlertRuleSchema]])
def alerts() -> dict:
    return build_alerts()


@router.patch("/alerts/{alert_id}", response_model=dict[str, list[AlertRuleSchema]])
def set_alert(alert_id: str, payload: AlertUpdateRequest) -> dict:
    return update_alert(alert_id, payload.enabled)


@router.get("/events", response_model=dict[str, list[EconomicEventSchema]])
async def economic_events() -> dict:
    return await get_live_events()


@router.get("/admin/health", response_model=AdminHealthSchema)
async def admin_health() -> dict:
    return await get_live_admin_health()
