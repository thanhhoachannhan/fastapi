from typing import Generator
from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from app.tests.conftest import override_get_db


@patch("app.database.db.get_db", return_value=override_get_db())
def test_get_db(mock_get_db):
    # Test case 1: Check if the function returns a generator
    db = mock_get_db()
    print(db)
    assert isinstance(db, Generator)

    # Test case 2: Check if the generator yields a session object
    session: Session = next(db)
    assert isinstance(session, Session)

    with pytest.raises(StopIteration) as e:
        next(db)
    assert e.type == StopIteration
