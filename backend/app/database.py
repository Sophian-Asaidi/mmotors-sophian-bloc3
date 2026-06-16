from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config import settings


def _database_url() -> str:
    if settings.database_url.startswith("postgres://"):
        return settings.database_url.replace("postgres://", "postgresql://", 1)
    return settings.database_url


engine_options: dict = {}
if _database_url().startswith("sqlite"):
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(_database_url(), **engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

