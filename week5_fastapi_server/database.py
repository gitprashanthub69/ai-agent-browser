"""
Week 5 — Database setup
Uses SQLite (file: agent.db) via SQLModel.
"""

from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///agent.db"

engine = create_engine(DATABASE_URL, echo=False)


def create_db():
    """Create all tables defined in models.py."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    """Context manager that yields a DB session and auto-commits/rolls back."""
    with Session(engine) as session:
        yield session
