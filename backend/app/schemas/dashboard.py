from datetime import datetime
from pydantic import BaseModel


class MarketItem(BaseModel):
    symbol: str
    name: str
    value: float
    day_change: float
    week_change: float
    month_trend: list[float]
    currency: str


class NewsItemSchema(BaseModel):
    id: str
    headline: str
    category: str
    impact_score: int
    sentiment: str
    summary: str
    affected_markets: list[str]
    source: str
    published_at: datetime


class SentimentSchema(BaseModel):
    score: int
    label: str
    drivers: list[str]


class AISummarySchema(BaseModel):
    pre_market: str
    intraday: str
    end_of_day: str
    bullish_factors: list[str]
    bearish_factors: list[str]
    risks: list[str]


class VixSchema(BaseModel):
    current: float
    index_price: float
    expected_move: float
    expected_high: float
    expected_low: float


class OISchema(BaseModel):
    highest_call_oi: int
    highest_put_oi: int
    pcr_ratio: float
    max_pain: int
    interpretation: str


class FlowSchema(BaseModel):
    fii: float
    dii: float
    series: list[dict[str, float | str]]


class WatchlistItemSchema(BaseModel):
    symbol: str
    name: str
    price: float
    change: float
    news_count: int
    ai_summary: str


class WatchlistSchema(BaseModel):
    name: str
    items: list[WatchlistItemSchema]


class WatchlistSymbolRequest(BaseModel):
    symbol: str


class AlertRuleSchema(BaseModel):
    id: str
    alert_type: str
    label: str
    threshold: str
    channel: str
    enabled: bool
    last_triggered: datetime | None = None


class AlertUpdateRequest(BaseModel):
    enabled: bool


class EconomicEventSchema(BaseModel):
    id: str
    country: str
    event_name: str
    importance: int
    event_time: datetime
    forecast: str
    previous: str
    affected_markets: list[str]


class AdminHealthSchema(BaseModel):
    api: str
    database: str
    redis: str
    workers: str
    cache_hit_rate: float
    avg_response_ms: int
    active_users: int
    news_sources: list[str]
    recent_logs: list[dict[str, str]]


class DashboardSchema(BaseModel):
    generated_at: datetime
    market_status: str
    global_markets: list[MarketItem]
    indian_markets: list[MarketItem]
    news: list[NewsItemSchema]
    sentiment: SentimentSchema
    ai_summary: AISummarySchema
    vix: VixSchema
    oi: OISchema
    flows: FlowSchema
