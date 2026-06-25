import os

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mmotors.db")

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

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