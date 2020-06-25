import pytest
from fastapi import testclient

from surfacescan import main


@pytest.fixture(scope="function")
def app():
    with testclient.TestClient(main.create_app()) as client:
        yield client
