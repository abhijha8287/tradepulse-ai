from datetime import datetime, timezone
from math import sqrt

GLOBAL_MARKETS = [
    {"symbol": "IXIC", "name": "Nasdaq", "value": 18948.2, "day_change": 0.86, "week_change": 1.92, "currency": "USD", "month_trend": [18100, 18320, 18410, 18640, 18590, 18770, 18948]},
    {"symbol": "GSPC", "name": "S&P 500", "value": 6124.4, "day_change": 0.42, "week_change": 1.15, "currency": "USD", "month_trend": [5980, 6010, 6048, 6070, 6065, 6100, 6124]},
    {"symbol": "DJI", "name": "Dow Jones", "value": 43870.6, "day_change": -0.12, "week_change": 0.44, "currency": "USD", "month_trend": [43600, 43820, 43740, 43910, 44120, 44010, 43870]},
    {"symbol": "USDINR", "name": "USD/INR", "value": 83.32, "day_change": -0.08, "week_change": -0.21, "currency": "INR", "month_trend": [83.58, 83.51, 83.48, 83.44, 83.37, 83.34, 83.32]},
    {"symbol": "N225", "name": "Nikkei 225", "value": 39290.5, "day_change": 0.51, "week_change": 1.33, "currency": "JPY", "month_trend": [38300, 38610, 38920, 38770, 39110, 39080, 39290]},
    {"symbol": "HSI", "name": "Hang Seng", "value": 18620.3, "day_change": -0.73, "week_change": -1.04, "currency": "HKD", "month_trend": [19080, 18920, 18840, 18700, 18780, 18690, 18620]},
    {"symbol": "SSEC", "name": "Shanghai Composite", "value": 3128.8, "day_change": 0.19, "week_change": 0.62, "currency": "CNY", "month_trend": [3090, 3108, 3112, 3104, 3120, 3125, 3128]},
    {"symbol": "CL", "name": "Crude Oil", "value": 79.4, "day_change": 1.62, "week_change": 3.18, "currency": "USD", "month_trend": [75, 76.4, 77.2, 76.8, 78.1, 78.7, 79.4]},
    {"symbol": "GC", "name": "Gold", "value": 2368.9, "day_change": -0.24, "week_change": 0.76, "currency": "USD", "month_trend": [2320, 2338, 2350, 2362, 2378, 2372, 2368]},
    {"symbol": "SI", "name": "Silver", "value": 31.2, "day_change": 0.31, "week_change": 1.54, "currency": "USD", "month_trend": [29.8, 30.1, 30.4, 30.6, 30.9, 31.0, 31.2]},
    {"symbol": "US10Y", "name": "US 10Y Treasury", "value": 4.28, "day_change": -0.04, "week_change": -0.12, "currency": "%", "month_trend": [4.42, 4.39, 4.36, 4.34, 4.31, 4.29, 4.28]},
]

INDIAN_MARKETS = [
    {"symbol": "NIFTY", "name": "NIFTY 50", "value": 25035.4, "day_change": 0.64, "week_change": 1.42, "currency": "INR", "month_trend": [24620, 24780, 24830, 24910, 24880, 24960, 25035]},
    {"symbol": "BANKNIFTY", "name": "Bank Nifty", "value": 53120.8, "day_change": 0.38, "week_change": 0.92, "currency": "INR", "month_trend": [52500, 52620, 52840, 52920, 52810, 53010, 53120]},
    {"symbol": "INDIAVIX", "name": "India VIX", "value": 13.8, "day_change": -2.18, "week_change": -4.4, "currency": "%", "month_trend": [15.2, 14.9, 14.5, 14.2, 14.1, 13.9, 13.8]},
]

NEWS = [
    {
        "id": "fed-hold-risk",
        "headline": "Fed signals patience on rate cuts as inflation cools slowly",
        "category": "Monetary Policy",
        "impact_score": 9,
        "sentiment": "Neutral",
        "summary": "Fed held rates unchanged. This is mildly bullish for equities if yields stay soft, but negative for aggressive USD shorts.",
        "affected_markets": ["Nifty", "BankNifty", "Gold", "USDINR"],
        "source": "Federal Reserve adapter",
        "published_at": datetime.now(timezone.utc),
    },
    {
        "id": "crude-supply",
        "headline": "Crude rises on supply disruption headlines",
        "category": "Commodities",
        "impact_score": 8,
        "sentiment": "Bearish",
        "summary": "Higher crude can pressure Indian macros and OMC margins. Watch USDINR and aviation names for second-order impact.",
        "affected_markets": ["Nifty", "Crude", "USDINR"],
        "source": "GDELT adapter",
        "published_at": datetime.now(timezone.utc),
    },
    {
        "id": "fii-flows",
        "headline": "FII cash market buying continues for second session",
        "category": "Institutional Flows",
        "impact_score": 7,
        "sentiment": "Bullish",
        "summary": "Consistent FII buying supports gap-up follow-through, especially if global cues remain constructive.",
        "affected_markets": ["Nifty", "BankNifty"],
        "source": "Exchange flow adapter",
        "published_at": datetime.now(timezone.utc),
    },
    {
        "id": "rbi-liquidity",
        "headline": "RBI liquidity operation keeps overnight rates stable",
        "category": "RBI Policy",
        "impact_score": 6,
        "sentiment": "Bullish",
        "summary": "Stable liquidity is supportive for rate-sensitive sectors and reduces tail risk in banking names.",
        "affected_markets": ["BankNifty", "Nifty"],
        "source": "RBI adapter",
        "published_at": datetime.now(timezone.utc),
    },
]

WATCHLIST = [
    {
        "symbol": "RELIANCE",
        "name": "Reliance Industries",
        "price": 2876.45,
        "change": 0.82,
        "news_count": 3,
        "ai_summary": "Bullish on refining margin expansion, but crude risk needs watching above $80.",
    },
    {
        "symbol": "HDFCBANK",
        "name": "HDFC Bank",
        "price": 1689.10,
        "change": -0.31,
        "news_count": 2,
        "ai_summary": "Neutral until deposit growth and margin commentary confirm a fresh banking impulse.",
    },
    {
        "symbol": "TCS",
        "name": "Tata Consultancy Services",
        "price": 4012.30,
        "change": 1.14,
        "news_count": 4,
        "ai_summary": "Constructive after US tech strength; rupee softness can support IT earnings sentiment.",
    },
]

ALERT_RULES = [
    {
        "id": "vix-spike",
        "alert_type": "Volatility",
        "label": "India VIX spike",
        "threshold": "Notify when India VIX rises above 16 or jumps 8% intraday",
        "channel": "Push + Email",
        "enabled": True,
        "last_triggered": None,
    },
    {
        "id": "fii-flow",
        "alert_type": "Institutional Flow",
        "label": "FII cash flow reversal",
        "threshold": "Notify when FII net cash flow crosses +/- Rs 1,000 Cr",
        "channel": "Email",
        "enabled": True,
        "last_triggered": None,
    },
    {
        "id": "breaking-news",
        "alert_type": "News",
        "label": "High-impact breaking news",
        "threshold": "Notify for impact score 8+ on Fed, RBI, crude, war, CPI, or budget news",
        "channel": "Push",
        "enabled": True,
        "last_triggered": NEWS[0]["published_at"],
    },
    {
        "id": "oi-shift",
        "alert_type": "Options",
        "label": "OI support/resistance shift",
        "threshold": "Notify when max pain shifts by 100+ points or PCR moves below 0.9",
        "channel": "Push",
        "enabled": False,
        "last_triggered": None,
    },
]

ECONOMIC_EVENTS = [
    {
        "id": "us-cpi",
        "country": "US",
        "event_name": "Core CPI MoM",
        "importance": 10,
        "event_time": datetime.now(timezone.utc),
        "forecast": "0.2%",
        "previous": "0.3%",
        "affected_markets": ["Nasdaq", "Gold", "USDINR", "Nifty"],
    },
    {
        "id": "india-iip",
        "country": "India",
        "event_name": "Industrial Production",
        "importance": 7,
        "event_time": datetime.now(timezone.utc),
        "forecast": "4.8%",
        "previous": "5.2%",
        "affected_markets": ["Nifty", "BankNifty"],
    },
    {
        "id": "rbi-policy",
        "country": "India",
        "event_name": "RBI Policy Decision",
        "importance": 10,
        "event_time": datetime.now(timezone.utc),
        "forecast": "Unchanged",
        "previous": "Unchanged",
        "affected_markets": ["BankNifty", "USDINR", "Bonds"],
    },
]


def build_dashboard() -> dict:
    index_price = 25035.4
    vix = 13.8
    expected_move = (index_price * vix) / (100 * sqrt(365))
    return {
        "generated_at": datetime.now(timezone.utc),
        "market_status": "India open",
        "global_markets": GLOBAL_MARKETS,
        "indian_markets": INDIAN_MARKETS,
        "news": NEWS,
        "sentiment": {
            "score": 68,
            "label": "Bullish",
            "drivers": ["US tech closed positive", "FII cash buying is supportive", "India VIX is falling", "Crude remains the key macro risk"],
        },
        "ai_summary": {
            "pre_market": "US markets closed positive, crude is up around 2%, FII bought Rs 1,200 Cr, and India VIX is falling. Bias: Mild bullish with crude and USDINR as the main risk checks.",
            "intraday": "Breadth remains constructive. Bulls retain control above the opening range; below it, watch for mean reversion into financials.",
            "end_of_day": "Market advanced on supportive global cues and institutional buying. Tomorrow's focus is crude direction, USDINR, and scheduled macro releases.",
            "bullish_factors": ["FII net buying: +1,200 Cr", "PCR above 1.1", "VIX trend is cooling"],
            "bearish_factors": ["Crude oil is elevated", "Hang Seng weakness", "US yields still above 4.25%"],
            "risks": ["Fed commentary surprise", "Geopolitical crude spike", "Opening gap exhaustion"],
        },
        "vix": {
            "current": vix,
            "index_price": index_price,
            "expected_move": expected_move,
            "expected_high": index_price + expected_move,
            "expected_low": index_price - expected_move,
        },
        "oi": {
            "highest_call_oi": 25200,
            "highest_put_oi": 25000,
            "pcr_ratio": 1.18,
            "max_pain": 25100,
            "interpretation": "PCR is bullish. Strong support is visible near 25,000 while 25,200 remains the first call-wall resistance.",
        },
        "flows": {
            "fii": 1200,
            "dii": -420,
            "series": [
                {"date": "Mon", "fii": -820, "dii": 540},
                {"date": "Tue", "fii": 260, "dii": 180},
                {"date": "Wed", "fii": 740, "dii": -120},
                {"date": "Thu", "fii": 980, "dii": -330},
                {"date": "Fri", "fii": 1200, "dii": -420},
            ],
        },
    }


def build_watchlist() -> dict:
    return {"name": "Primary Watchlist", "items": WATCHLIST}


def add_watchlist_symbol(symbol: str) -> dict:
    clean_symbol = symbol.strip().upper()
    if not clean_symbol:
        return build_watchlist()
    if all(item["symbol"] != clean_symbol for item in WATCHLIST):
        WATCHLIST.append(
            {
                "symbol": clean_symbol,
                "name": clean_symbol,
                "price": 0,
                "change": 0,
                "news_count": 0,
                "ai_summary": "New symbol queued for adapter refresh and AI stock summary generation.",
            }
        )
    return build_watchlist()


def remove_watchlist_symbol(symbol: str) -> dict:
    clean_symbol = symbol.strip().upper()
    WATCHLIST[:] = [item for item in WATCHLIST if item["symbol"] != clean_symbol]
    return build_watchlist()


def build_alerts() -> dict:
    return {"alerts": ALERT_RULES}


def update_alert(alert_id: str, enabled: bool) -> dict:
    for alert in ALERT_RULES:
        if alert["id"] == alert_id:
            alert["enabled"] = enabled
            break
    return build_alerts()


def build_economic_events() -> dict:
    return {"events": ECONOMIC_EVENTS}


def build_admin_health() -> dict:
    return {
        "api": "healthy",
        "database": "configured",
        "redis": "configured",
        "workers": "configured",
        "cache_hit_rate": 91.4,
        "avg_response_ms": 142,
        "active_users": 18,
        "news_sources": ["Reuters adapter", "Bloomberg adapter", "Economic Times adapter", "Moneycontrol adapter", "RBI adapter", "Federal Reserve adapter"],
        "recent_logs": [
            {"level": "INFO", "message": "Dashboard payload generated from normalized adapters"},
            {"level": "INFO", "message": "High-impact news filter returned 4 items"},
            {"level": "WARN", "message": "Live provider keys missing; deterministic adapters active"},
        ],
    }
