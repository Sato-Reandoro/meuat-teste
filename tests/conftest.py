from unittest.mock import MagicMock

import pytest
from dotenv import load_dotenv

from app.core.db import get_db
from app.main import app

load_dotenv()


@pytest.fixture
def mock_db():
    """Cria uma sessão de banco mockada."""
    return MagicMock()


@pytest.fixture
def override_get_db(mock_db):
    """Substitui a dependência get_db por um mock."""

    def _get_mock_db():
        yield mock_db

    app.dependency_overrides[get_db] = _get_mock_db
    yield mock_db
    app.dependency_overrides.clear()
