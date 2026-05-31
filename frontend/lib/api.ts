export const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    next: { revalidate: 30 },
    headers: { "Content-Type": "application/json" }
  });

  if (!res.ok) {
    throw new Error(`API ${path} failed: ${res.status}`);
  }

  return res.json();
}

export type MarketItem = {
  symbol: string;
  name: string;
  value: number;
  day_change: number;
  week_change: number;
  month_trend: number[];
  currency: string;
};

export type NewsItem = {
  id: string;
  headline: string;
  category: string;
  impact_score: number;
  sentiment: "Bullish" | "Bearish" | "Neutral";
  summary: string;
  affected_markets: string[];
  source: string;
  published_at: string;
};

export type DashboardPayload = {
  generated_at: string;
  market_status: string;
  global_markets: MarketItem[];
  indian_markets: MarketItem[];
  news: NewsItem[];
  sentiment: {
    score: number;
    label: string;
    drivers: string[];
  };
  ai_summary: {
    pre_market: string;
    intraday: string;
    end_of_day: string;
    bullish_factors: string[];
    bearish_factors: string[];
    risks: string[];
  };
  vix: {
    current: number;
    index_price: number;
    expected_move: number;
    expected_high: number;
    expected_low: number;
  };
  oi: {
    highest_call_oi: number;
    highest_put_oi: number;
    pcr_ratio: number;
    max_pain: number;
    interpretation: string;
  };
  flows: {
    fii: number;
    dii: number;
    series: { date: string; fii: number; dii: number }[];
  };
};

export type WatchlistItem = {
  symbol: string;
  name: string;
  price: number;
  change: number;
  news_count: number;
  ai_summary: string;
};

export type AlertRule = {
  id: string;
  alert_type: string;
  label: string;
  threshold: string;
  channel: string;
  enabled: boolean;
  last_triggered: string | null;
};

export type EconomicEvent = {
  id: string;
  country: string;
  event_name: string;
  importance: number;
  event_time: string;
  forecast: string;
  previous: string;
  affected_markets: string[];
};

export type AdminHealth = {
  api: string;
  database: string;
  redis: string;
  workers: string;
  cache_hit_rate: number;
  avg_response_ms: number;
  active_users: number;
  news_sources: string[];
  recent_logs: { level: string; message: string }[];
};

export const api = {
  dashboard: () => getJson<DashboardPayload>("/api/v1/dashboard"),
  global: () => getJson<{ markets: MarketItem[] }>("/api/v1/markets/global"),
  indian: () => getJson<DashboardPayload>("/api/v1/markets/india"),
  news: () => getJson<{ news: NewsItem[] }>("/api/v1/news/high-impact"),
  insights: () => getJson<DashboardPayload["ai_summary"]>("/api/v1/ai/insights"),
  watchlist: () => getJson<{ name: string; items: WatchlistItem[] }>("/api/v1/watchlist"),
  alerts: () => getJson<{ alerts: AlertRule[] }>("/api/v1/alerts"),
  events: () => getJson<{ events: EconomicEvent[] }>("/api/v1/events"),
  adminHealth: () => getJson<AdminHealth>("/api/v1/admin/health")
};
