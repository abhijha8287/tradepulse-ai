from celery import Celery
from app.core.config import settings

celery_app = Celery("tradepulse_ai", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.beat_schedule = {
    "refresh-market-data-every-minute": {
        "task": "app.workers.tasks.refresh_market_data",
        "schedule": 60.0,
    },
    "generate-hourly-intraday-summary": {
        "task": "app.workers.tasks.generate_intraday_summary",
        "schedule": 3600.0,
    },
}
