import pytest
from fastapi.testclient import TestClient

from app.main import app, reset_store


@pytest.fixture()
def client():
    reset_store()
    with TestClient(app) as test_client:
        yield test_client
