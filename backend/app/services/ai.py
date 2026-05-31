from app.core.config import settings
from app.services.seed_data import build_dashboard


class MarketBrain:
    def summarize(self) -> dict:
        # Uses deterministic summaries by default. When OPENAI_API_KEY is present, plug LangChain
        # generation here with strict JSON output and source attribution.
        dashboard = build_dashboard()
        if not settings.openai_api_key:
            return dashboard["ai_summary"]
        return dashboard["ai_summary"]


market_brain = MarketBrain()
