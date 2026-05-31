from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    clerk_user_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(32), default="trader")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Watchlist(Base):
    __tablename__ = "watchlists"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(120))
    symbols: Mapped[list[str]] = mapped_column(JSON, default=list)
    user = relationship("User")


class NewsItem(Base):
    __tablename__ = "news"
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(120), index=True)
    headline: Mapped[str] = mapped_column(String(500))
    summary: Mapped[str] = mapped_column(Text)
    sentiment: Mapped[str] = mapped_column(String(32))
    impact_score: Mapped[int] = mapped_column(Integer)
    affected_markets: Mapped[list[str]] = mapped_column(JSON, default=list)
    published_at: Mapped[datetime] = mapped_column(DateTime, index=True)


class MarketData(Base):
    __tablename__ = "market_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    name: Mapped[str] = mapped_column(String(120))
    value: Mapped[float] = mapped_column(Float)
    day_change: Mapped[float] = mapped_column(Float)
    week_change: Mapped[float] = mapped_column(Float)
    month_trend: Mapped[list[float]] = mapped_column(JSON, default=list)
    currency: Mapped[str] = mapped_column(String(12))
    region: Mapped[str] = mapped_column(String(32), index=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class EconomicEvent(Base):
    __tablename__ = "economic_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(64))
    event_name: Mapped[str] = mapped_column(String(200))
    importance: Mapped[int] = mapped_column(Integer)
    event_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    actual: Mapped[str | None] = mapped_column(String(64), nullable=True)
    forecast: Mapped[str | None] = mapped_column(String(64), nullable=True)


class SentimentScore(Base):
    __tablename__ = "sentiment_scores"
    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int] = mapped_column(Integer)
    label: Mapped[str] = mapped_column(String(64))
    drivers: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AISummary(Base):
    __tablename__ = "ai_summaries"
    id: Mapped[int] = mapped_column(primary_key=True)
    summary_type: Mapped[str] = mapped_column(String(64), index=True)
    content: Mapped[str] = mapped_column(Text)
    factors: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    alert_type: Mapped[str] = mapped_column(String(80))
    threshold: Mapped[dict] = mapped_column(JSON, default=dict)
    channel: Mapped[str] = mapped_column(String(32))
    enabled: Mapped[bool] = mapped_column(default=True)


class AppLog(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[str] = mapped_column(String(24))
    message: Mapped[str] = mapped_column(Text)
    context: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
