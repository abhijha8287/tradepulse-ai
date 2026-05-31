from __future__ import annotations

import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from math import sqrt
from typing import Any
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

import httpx

from app.services.cache import cache
from app.services.seed_data import build_admin_health, build_dashboard, build_economic_events, build_watchlist

HEADERS = {
    "accept": "application/json,text/html,application/xml;q=0.9,*/*;q=0.8",
    "accept-language": "en-IN,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
}

NSE_HOME = "https://www.nseindia.com"
NSE_INDICES_URL = f"{NSE_HOME}/api/allIndices"
NSE_OPTION_CHAIN_URL = f"{NSE_HOME}/api/option-chain-indices?symbol=NIFTY"
NSE_FII_DII_URL = f"{NSE_HOME}/api/fiidiiTradeReact"
SEBI_RSS_URL = "https://www.sebi.gov.in/sebirss.xml"
ZERODHA_PULSE_URL = "https://pulse.zerodha.com/"
MONEYCONTROL_FEEDS = [
    "https://www.moneycontrol.com/rss/marketreports.xml",
    "https://www.moneycontrol.com/rss/business.xml",
    "https://www.moneycontrol.com/rss/economy.xml",
    "https://www.moneycontrol.com/rss/MCtopnews.xml",
]

INDEX_MAP = {
    "NIFTY 50": ("NIFTY", "NIFTY 50", "INR"),
    "NIFTY BANK": ("BANKNIFTY", "Bank Nifty", "INR"),
    "INDIA VIX": ("INDIAVIX", "India VIX", "%"),
}

GLOBAL_INDEX_MAP = {
    "NIFTY 50": ("NIFTY", "NIFTY 50", "INR"),
    "NIFTY BANK": ("BANKNIFTY", "Bank Nifty", "INR"),
    "INDIA VIX": ("INDIAVIX", "India VIX", "%"),
}

HIGH_IMPACT_KEYWORDS = {
    "rbi": ("RBI Policy", ["Nifty", "BankNifty", "USDINR"]),
    "sebi": ("Regulation", ["Nifty", "Stocks"]),
    "fed": ("Monetary Policy", ["Nifty", "Gold", "USDINR"]),
    "rate": ("Monetary Policy", ["Nifty", "BankNifty", "USDINR"]),
    "inflation": ("Economy", ["Nifty", "Gold", "USDINR"]),
    "cpi": ("Economy", ["Nifty", "Gold", "USDINR"]),
    "gdp": ("Economy", ["Nifty", "BankNifty"]),
    "crude": ("Commodities", ["Nifty", "Crude", "USDINR"]),
    "oil": ("Commodities", ["Nifty", "Crude", "USDINR"]),
    "budget": ("Budget", ["Nifty", "BankNifty"]),
    "election": ("Politics", ["Nifty", "USDINR"]),
    "war": ("Geopolitical Risk", ["Nifty", "Gold", "Crude", "USDINR"]),
    "tariff": ("Global Events", ["Nifty", "USDINR"]),
    "nifty": ("Markets", ["Nifty", "BankNifty"]),
    "sensex": ("Markets", ["Nifty", "BankNifty"]),
}


async def build_live_dashboard() -> dict:
    cached = cache.get_json("live:dashboard")
    if cached:
        return cached

    fallback = build_dashboard()
    nse = await fetch_nse_snapshot()
    news = await fetch_high_impact_news()

    indian_markets = nse.get("indian_markets") or fallback["indian_markets"]
    vix = build_vix(indian_markets, fallback)
    flows = nse.get("flows") or fallback["flows"]
    oi = nse.get("oi") or fallback["oi"]
    sentiment = build_sentiment(indian_markets, news, flows, vix)
    ai_summary = build_ai_summary(sentiment, news, flows, vix, oi)

    dashboard = {
        **fallback,
        "generated_at": datetime.now(timezone.utc),
        "market_status": nse.get("market_status", "Live sources polling"),
        "indian_markets": indian_markets,
        "news": news or fallback["news"],
        "sentiment": sentiment,
        "ai_summary": ai_summary,
        "vix": vix,
        "oi": oi,
        "flows": flows,
    }
    cache.set_json("live:dashboard", dashboard, 45)
    return dashboard


async def fetch_nse_snapshot() -> dict:
    cached = cache.get_json("live:nse")
    if cached:
        return cached

    result: dict[str, Any] = {}
    async with httpx.AsyncClient(headers=HEADERS, timeout=8, follow_redirects=True) as client:
        try:
            await client.get(NSE_HOME)
            indices = await client.get(NSE_INDICES_URL)
            indices.raise_for_status()
            result["indian_markets"] = parse_nse_indices(indices.json())
            result["market_status"] = "NSE live"
        except (httpx.HTTPError, ValueError):
            result["market_status"] = "NSE delayed"

        try:
            option_chain = await client.get(NSE_OPTION_CHAIN_URL)
            option_chain.raise_for_status()
            result["oi"] = parse_option_chain(option_chain.json())
        except (httpx.HTTPError, ValueError, KeyError, TypeError):
            pass

        try:
            flows = await client.get(NSE_FII_DII_URL)
            flows.raise_for_status()
            result["flows"] = parse_fii_dii(flows.json())
        except (httpx.HTTPError, ValueError, KeyError, TypeError):
            pass

    cache.set_json("live:nse", result, 45)
    return result


def parse_nse_indices(payload: dict) -> list[dict]:
    rows = payload.get("data", [])
    markets = []
    for row in rows:
        name = str(row.get("index", "")).upper()
        if name not in INDEX_MAP:
            continue
        symbol, label, currency = INDEX_MAP[name]
        value = as_float(row.get("last") or row.get("lastPrice"))
        day_change = as_float(row.get("percentChange") or row.get("perChange365d"))
        previous = value - as_float(row.get("variation"))
        trend = trend_from(value, previous if previous else value)
        markets.append(
            {
                "symbol": symbol,
                "name": label,
                "value": value,
                "day_change": day_change,
                "week_change": as_float(row.get("perChange30d")) / 4,
                "currency": currency,
                "month_trend": trend,
            }
        )
    return markets


def parse_option_chain(payload: dict) -> dict:
    records = payload.get("records", {})
    rows = records.get("data", [])
    expiry_dates = records.get("expiryDates", [])
    nearest_expiry = expiry_dates[0] if expiry_dates else None
    filtered = [row for row in rows if not nearest_expiry or row.get("expiryDate") == nearest_expiry]
    calls = [(as_int(row.get("strikePrice")), as_int(row.get("CE", {}).get("openInterest"))) for row in filtered if row.get("CE")]
    puts = [(as_int(row.get("strikePrice")), as_int(row.get("PE", {}).get("openInterest"))) for row in filtered if row.get("PE")]
    highest_call = max(calls, key=lambda item: item[1], default=(25200, 0))[0]
    highest_put = max(puts, key=lambda item: item[1], default=(25000, 0))[0]
    total_call = sum(oi for _, oi in calls)
    total_put = sum(oi for _, oi in puts)
    pcr = round(total_put / total_call, 2) if total_call else 1
    max_pain = min(filtered, key=lambda row: abs(as_int(row.get("CE", {}).get("openInterest")) - as_int(row.get("PE", {}).get("openInterest"))), default={"strikePrice": 25100}).get("strikePrice")
    bias = "bullish" if pcr >= 1 else "cautious"
    return {
        "highest_call_oi": highest_call,
        "highest_put_oi": highest_put,
        "pcr_ratio": pcr,
        "max_pain": as_int(max_pain),
        "interpretation": f"Live NSE option chain shows PCR near {pcr}. Bias is {bias}; support is visible near {highest_put}, resistance near {highest_call}.",
    }


def parse_fii_dii(payload: Any) -> dict:
    rows = payload if isinstance(payload, list) else payload.get("data", [])
    fii = 0.0
    dii = 0.0
    for row in rows:
        category = str(row.get("category") or row.get("name") or "").upper()
        net = as_float(row.get("netValue") or row.get("net") or row.get("buyValue", 0)) - as_float(row.get("sellValue", 0))
        if "FII" in category or "FPI" in category:
            fii = net
        if "DII" in category:
            dii = net
    return {"fii": fii, "dii": dii, "series": [{"date": "Live", "fii": fii, "dii": dii}]}


async def fetch_high_impact_news() -> list[dict]:
    cached = cache.get_json("live:news")
    if cached:
        return cached

    items: list[dict] = []
    async with httpx.AsyncClient(headers=HEADERS, timeout=8, follow_redirects=True) as client:
        rss_urls = [SEBI_RSS_URL, *MONEYCONTROL_FEEDS]
        for url in rss_urls:
            try:
                response = await client.get(url)
                response.raise_for_status()
                items.extend(parse_rss(response.text, source_name(url)))
            except httpx.HTTPError:
                continue

        try:
            response = await client.get(ZERODHA_PULSE_URL)
            response.raise_for_status()
            items.extend(parse_zerodha_pulse(response.text))
        except httpx.HTTPError:
            pass

    ranked = sorted(dedupe_news(items), key=lambda item: (item["impact_score"], item["published_at"]), reverse=True)
    high_impact = ranked[:12]
    cache.set_json("live:news", high_impact, 90)
    return high_impact


def parse_rss(xml_text: str, source: str) -> list[dict]:
    parsed: list[dict] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return parsed

    for item in root.findall(".//item")[:20]:
        title = text_of(item, "title")
        link = text_of(item, "link")
        description = clean_html(text_of(item, "description"))
        published = parse_date(text_of(item, "pubDate"))
        parsed.append(build_news_item(title, description, source, published, link))
    return [item for item in parsed if item["impact_score"] >= 5]


def parse_zerodha_pulse(html: str) -> list[dict]:
    parsed = []
    pattern = re.compile(r"<h2>\s*<a[^>]+href=\"([^\"]+)\"[^>]*>(.*?)</a>.*?</h2>\s*<p>(.*?)</p>\s*<span[^>]*>(.*?)</span>", re.S | re.I)
    for link, title, summary, meta in pattern.findall(html)[:30]:
        source = clean_html(meta).split("—")[-1].strip() or "Zerodha Pulse"
        parsed.append(build_news_item(clean_html(title), clean_html(summary), f"Pulse: {source}", datetime.now(timezone.utc), urljoin(ZERODHA_PULSE_URL, link)))
    return [item for item in parsed if item["impact_score"] >= 5]


def build_news_item(title: str, summary: str, source: str, published_at: datetime, link: str) -> dict:
    category, affected = classify_news(f"{title} {summary}")
    score = impact_score(f"{title} {summary}", source)
    sentiment = sentiment_for(f"{title} {summary}")
    return {
        "id": slugify(f"{source}-{title}")[:80],
        "headline": title[:240],
        "category": category,
        "impact_score": score,
        "sentiment": sentiment,
        "summary": summary[:420] or f"Live item from {source}. Open the linked source for full details.",
        "affected_markets": affected,
        "source": source,
        "published_at": published_at,
        "url": link,
    }


def classify_news(text: str) -> tuple[str, list[str]]:
    lower = text.lower()
    for keyword, result in HIGH_IMPACT_KEYWORDS.items():
        if keyword in lower:
            return result
    return "Markets", ["Nifty"]


def impact_score(text: str, source: str) -> int:
    lower = text.lower()
    score = 5
    for keyword in HIGH_IMPACT_KEYWORDS:
        if keyword in lower:
            score += 1
    if "SEBI" in source or "Pulse" in source:
        score += 1
    if any(word in lower for word in ["breaking", "surge", "crash", "falls", "rises", "policy", "decision"]):
        score += 1
    return min(score, 10)


def sentiment_for(text: str) -> str:
    lower = text.lower()
    bearish = ["fall", "falls", "crash", "weak", "selloff", "risk", "war", "sanction", "inflation", "probe"]
    bullish = ["rise", "rises", "gain", "gains", "boost", "buy", "growth", "approval", "relief"]
    if any(word in lower for word in bearish):
        return "Bearish"
    if any(word in lower for word in bullish):
        return "Bullish"
    return "Neutral"


def build_vix(markets: list[dict], fallback: dict) -> dict:
    nifty = next((item for item in markets if item["symbol"] == "NIFTY"), None)
    vix_item = next((item for item in markets if item["symbol"] == "INDIAVIX"), None)
    index_price = as_float(nifty.get("value")) if nifty else fallback["vix"]["index_price"]
    vix = as_float(vix_item.get("value")) if vix_item else fallback["vix"]["current"]
    expected_move = (index_price * vix) / (100 * sqrt(365))
    return {
        "current": vix,
        "index_price": index_price,
        "expected_move": expected_move,
        "expected_high": index_price + expected_move,
        "expected_low": index_price - expected_move,
    }


def build_sentiment(markets: list[dict], news: list[dict], flows: dict, vix: dict) -> dict:
    nifty = next((item for item in markets if item["symbol"] == "NIFTY"), {"day_change": 0})
    score = 50
    score += min(max(as_float(nifty["day_change"]) * 8, -12), 12)
    score += 8 if as_float(flows.get("fii")) > 0 else -6
    score += 6 if vix["current"] < 15 else -8
    score += sum(2 if item["sentiment"] == "Bullish" else -2 if item["sentiment"] == "Bearish" else 0 for item in news[:6])
    score = int(max(0, min(100, score)))
    label = "Extremely Bullish" if score >= 80 else "Bullish" if score >= 60 else "Neutral" if score >= 40 else "Bearish" if score >= 20 else "Extremely Bearish"
    return {
        "score": score,
        "label": label,
        "drivers": [
            f"NIFTY day change: {as_float(nifty['day_change']):+.2f}%",
            f"FII flow: {as_float(flows.get('fii')):+,.0f} Cr",
            f"India VIX: {vix['current']:.2f}",
            f"High-impact live news items: {len(news)}",
        ],
    }


def build_ai_summary(sentiment: dict, news: list[dict], flows: dict, vix: dict, oi: dict) -> dict:
    top_news = news[0]["headline"] if news else "No high-impact live headline available"
    return {
        "pre_market": f"Live sources show sentiment at {sentiment['score']}/100 ({sentiment['label']}). FII flow is {as_float(flows.get('fii')):+,.0f} Cr, India VIX is {vix['current']:.2f}, and top news is: {top_news}.",
        "intraday": f"Watch NIFTY against the expected range {vix['expected_low']:.0f}-{vix['expected_high']:.0f}. Options data points to support near {oi['highest_put_oi']} and resistance near {oi['highest_call_oi']}.",
        "end_of_day": "End-of-day summary will refresh from closing price action, institutional flow, options positioning, and late regulatory/news updates.",
        "bullish_factors": [driver for driver in sentiment["drivers"] if "+" in driver or "VIX" in driver][:3],
        "bearish_factors": [item["headline"] for item in news if item["sentiment"] == "Bearish"][:3] or ["No dominant bearish live headline in the current feed"],
        "risks": ["NSE/Moneycontrol/Pulse source blocking or delayed feed", "Crude and USDINR shocks", "Regulatory headlines from SEBI/RBI"],
    }


def text_of(item: ET.Element, tag: str) -> str:
    value = item.findtext(tag)
    return clean_html(value or "")


def clean_html(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = unescape(value).replace("#39;", "'").replace("&amp;", "&")
    return re.sub(r"\s+", " ", value).strip()


def parse_date(value: str) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    try:
        parsed = parsedate_to_datetime(value)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return datetime.now(timezone.utc)


def source_name(url: str) -> str:
    if "sebi" in url:
        return "SEBI RSS"
    if "moneycontrol" in url:
        return "Moneycontrol RSS"
    return url


def dedupe_news(items: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for item in items:
        key = item["headline"].lower()
        if key in seen or not item["headline"]:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def as_float(value: Any) -> float:
    if value is None:
        return 0.0
    return float(str(value).replace(",", "").replace("%", "").strip() or 0)


def as_int(value: Any) -> int:
    return int(as_float(value))


def trend_from(value: float, previous: float) -> list[float]:
    if not previous:
        previous = value
    step = (value - previous) / 6
    return [round(previous + step * index, 2) for index in range(7)]


async def get_live_watchlist() -> dict:
    cached = cache.get_json("live:watchlist")
    if cached:
        return cached

    watchlist = build_watchlist()
    async with httpx.AsyncClient(headers=HEADERS, timeout=8, follow_redirects=True) as client:
        try:
            await client.get(NSE_HOME)
        except httpx.HTTPError:
            pass

        items = []
        for item in watchlist["items"]:
            items.append(await enrich_watchlist_item(client, item))

    live_watchlist = {"name": watchlist["name"], "items": items}
    cache.set_json("live:watchlist", live_watchlist, 45)
    return live_watchlist


async def enrich_watchlist_item(client: httpx.AsyncClient, item: dict) -> dict:
    try:
        response = await client.get(f"{NSE_HOME}/api/quote-equity?symbol={item['symbol']}")
        response.raise_for_status()
        payload = response.json()
        price = payload.get("priceInfo", {})
        security = payload.get("info", {})
        return {
            **item,
            "name": security.get("companyName") or item["name"],
            "price": as_float(price.get("lastPrice")) or item["price"],
            "change": as_float(price.get("pChange")) or item["change"],
            "ai_summary": build_stock_summary(item["symbol"], as_float(price.get("pChange")), item["news_count"]),
        }
    except (httpx.HTTPError, ValueError, KeyError, TypeError):
        return item


def build_stock_summary(symbol: str, change: float, news_count: int) -> str:
    if change > 1:
        tone = "positive momentum"
    elif change < -1:
        tone = "negative momentum"
    else:
        tone = "range-bound trade"
    return f"NSE live quote shows {tone} in {symbol}; linked news count is {news_count}, so confirm sector headlines before acting."


async def get_live_events() -> dict:
    return build_economic_events()


async def get_live_admin_health() -> dict:
    health = build_admin_health()
    health["recent_logs"] = [
        {"level": "INFO", "message": "Live adapters active for NSE, SEBI RSS, Moneycontrol RSS, and Zerodha Pulse"},
        {"level": "INFO", "message": "Dashboard/news payloads refresh through backend cache TTLs"},
        {"level": "WARN", "message": "Public websites may rate-limit automated requests; stale fallback stays enabled"},
    ]
    return health
