import pytest
from app import app


@pytest.fixture
def create_app():

    return app.test_client()


def test_index(create_app):

    with create_app as client:

        result = client.get("/")
        assert result.status_code == 200
        assert result.get_json()["message"] == "Hello World!"


def test_collect_endpoint_get(create_app):

    with create_app as client:

        result = client.get("/collect")
        assert result.status_code == 403
        assert result.get_json()["message"] == "Forbidden Request"
