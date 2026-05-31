from abc import ABC, abstractmethod
from app.services.seed_data import GLOBAL_MARKETS, NEWS


class MarketDataAdapter(ABC):
    @abstractmethod
    async def fetch(self) -> list[dict]:
        raise NotImplementedError


class NewsAdapter(ABC):
    @abstractmethod
    async def fetch(self) -> list[dict]:
        raise NotImplementedError


class MockMarketDataAdapter(MarketDataAdapter):
    async def fetch(self) -> list[dict]:
        return GLOBAL_MARKETS


class YahooFinanceAdapter(MarketDataAdapter):
    async def fetch(self) -> list[dict]:
        # Production implementation should call Yahoo-compatible endpoints and normalize here.
        return GLOBAL_MARKETS


class MockNewsAdapter(NewsAdapter):
    async def fetch(self) -> list[dict]:
        return NEWS


class GdeltNewsAdapter(NewsAdapter):
    async def fetch(self) -> list[dict]:
        # Production implementation should filter GDELT by high-impact macro categories.
        return NEWS
