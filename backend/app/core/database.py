from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import inspect, text

from app.core.settings import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ensure_runtime_schema():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if "applications" not in tables:
        return

    columns = {column["name"] for column in inspector.get_columns("applications")}

    with engine.begin() as connection:
        if "internal_comment" not in columns:
            connection.execute(
                text("ALTER TABLE applications ADD COLUMN internal_comment TEXT DEFAULT '' NOT NULL")
            )