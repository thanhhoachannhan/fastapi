from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import settings
from app.log import get_logger


log = get_logger(__name__)

engine = create_engine(str(settings.database_uri))


def get_db() -> Generator[Session, None, None]:
    log.debug('getting database session')
    with Session(engine) as session:
        yield session
    log.debug('closing database session')
