import logging

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db


router = APIRouter(tags=["santé"])
logger = logging.getLogger("mmotors.health")


@router.get("/health")
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "database": "ok",
        "alerting": "simulated",
        "rpo": "15 min",
        "rto": "1 heure",
    }


@router.post("/health/alert-test")
def alert_test() -> dict[str, bool | str]:
    logger.warning("ALERTE SIMULEE - test de supervision M-Motors")
    return {"alert_sent": True, "channel": "journal applicatif simulé"}

