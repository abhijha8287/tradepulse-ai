"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-30
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("clerk_user_id", sa.String(128), nullable=False), sa.Column("email", sa.String(255), nullable=False), sa.Column("role", sa.String(32), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_index("ix_users_clerk_user_id", "users", ["clerk_user_id"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("market_data", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("symbol", sa.String(32), nullable=False), sa.Column("name", sa.String(120), nullable=False), sa.Column("value", sa.Float(), nullable=False), sa.Column("day_change", sa.Float(), nullable=False), sa.Column("week_change", sa.Float(), nullable=False), sa.Column("month_trend", sa.JSON(), nullable=False), sa.Column("currency", sa.String(12), nullable=False), sa.Column("region", sa.String(32), nullable=False), sa.Column("captured_at", sa.DateTime(), nullable=False))
    op.create_index("ix_market_data_symbol", "market_data", ["symbol"])
    op.create_index("ix_market_data_region", "market_data", ["region"])
    op.create_table("news", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("source", sa.String(120), nullable=False), sa.Column("category", sa.String(120), nullable=False), sa.Column("headline", sa.String(500), nullable=False), sa.Column("summary", sa.Text(), nullable=False), sa.Column("sentiment", sa.String(32), nullable=False), sa.Column("impact_score", sa.Integer(), nullable=False), sa.Column("affected_markets", sa.JSON(), nullable=False), sa.Column("published_at", sa.DateTime(), nullable=False))
    op.create_index("ix_news_category", "news", ["category"])
    op.create_index("ix_news_published_at", "news", ["published_at"])
    op.create_table("economic_events", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("country", sa.String(64), nullable=False), sa.Column("event_name", sa.String(200), nullable=False), sa.Column("importance", sa.Integer(), nullable=False), sa.Column("event_time", sa.DateTime(), nullable=False), sa.Column("actual", sa.String(64), nullable=True), sa.Column("forecast", sa.String(64), nullable=True))
    op.create_index("ix_economic_events_event_time", "economic_events", ["event_time"])
    op.create_table("sentiment_scores", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("score", sa.Integer(), nullable=False), sa.Column("label", sa.String(64), nullable=False), sa.Column("drivers", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("ai_summaries", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("summary_type", sa.String(64), nullable=False), sa.Column("content", sa.Text(), nullable=False), sa.Column("factors", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_index("ix_ai_summaries_summary_type", "ai_summaries", ["summary_type"])
    op.create_table("watchlists", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("name", sa.String(120), nullable=False), sa.Column("symbols", sa.JSON(), nullable=False))
    op.create_table("alerts", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("alert_type", sa.String(80), nullable=False), sa.Column("threshold", sa.JSON(), nullable=False), sa.Column("channel", sa.String(32), nullable=False), sa.Column("enabled", sa.Boolean(), nullable=False))
    op.create_table("logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("level", sa.String(24), nullable=False), sa.Column("message", sa.Text(), nullable=False), sa.Column("context", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))


def downgrade() -> None:
    for table in ["logs", "alerts", "watchlists", "ai_summaries", "sentiment_scores", "economic_events", "news", "market_data", "users"]:
        op.drop_table(table)
