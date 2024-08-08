from datetime import timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.db import get_db
from app.main import app
from app.config import settings as _test_settings


TEST_SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{_test_settings.POSTGRES_USER}:{_test_settings.POSTGRES_PASSWORD}@'
    f'{_test_settings.POSTGRES_SERVER}:{_test_settings.POSTGRES_PORT}/{_test_settings.POSTGRES_DB}'
)


@pytest.fixture
def test_sqlalchemy_database_url():
    return TEST_SQLALCHEMY_DATABASE_URL


@pytest.fixture
def test_settings():
    return _test_settings


engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=False)


@pytest.fixture
def _engine():
    return engine


@pytest.fixture
def _test_session(_engine):
    return sessionmaker(bind=_engine, autocommit=False, autoflush=False)


def override_get_db():
    db = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
