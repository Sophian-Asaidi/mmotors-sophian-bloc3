from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.settings import settings
from app.services.monitoring import metrics

router = APIRouter(tags=["monitoring"])


@router.get("/health")
def health(db: Session = Depends(get_db)):
    database_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        database_status = "error"
    return {
        "status": "ok" if database_status == "ok" else "degraded",
        "database": database_status,
        "alerting": "simulated",
        "rpo": settings.rpo,
        "rto": settings.rto,
    }


@router.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics():
    return metrics.prometheus_text()


@router.post("/health/alert-test")
def alert_test(reason: str = "manual-test"):
    return metrics.trigger_alert(reason)
