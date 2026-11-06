"""Request dependencies.

Shop isolation: later steps inject the authenticated shop_id from the JWT
and ignore any shop_id sent in the request body.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database import get_db


def db_session() -> Generator[Session, None, None]:
    yield from get_db()
