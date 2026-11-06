from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


def _is_sqlite_url(url: str) -> bool:
    return url.startswith("sqlite")


def _sqlite_connect_args(url: str) -> dict:
    if _is_sqlite_url(url):
        return {"check_same_thread": False}
    return {}


def create_db_engine(url: str | None = None) -> Engine:
    database_url = url or settings.database_url
    engine = create_engine(
        database_url,
        connect_args=_sqlite_connect_args(database_url),
        future=True,
    )
    if _is_sqlite_url(database_url):
        _register_sqlite_pragmas(engine)
    return engine


def _register_sqlite_pragmas(engine: Engine) -> None:
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragmas(dbapi_connection, _connection_record) -> None:  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA busy_timeout=5000")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()


engine = create_db_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session, future=True)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
