import structlog
from app.workers.celery_app import celery_app

logger = structlog.get_logger()


@celery_app.task
def refresh_market_data() -> str:
    logger.info("market_data_refresh_started")
    return "market data refresh queued"


@celery_app.task
def generate_intraday_summary() -> str:
    logger.info("intraday_summary_generation_started")
    return "intraday summary generated"
