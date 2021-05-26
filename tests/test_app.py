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


def test_heartbeat_endpoint_get(create_app):

    with create_app as client:

        result = client.get("/collect")
        assert result.status_code == 403
        assert result.get_json()["message"] == "Forbidden Request"


def test_collect_endpoint_post(create_app):

    testing_data = {
        "device": "my device",
        "ip_address": "192.168.0.185",
        "status_code": 200,
        "status_msg": "I am safe"
    }

    with create_app as client:

        result = client.post("/collect", json=testing_data)
        assert result.status_code == 200
        assert result.get_json()["ip_address"] == testing_data["ip_address"]
        assert result.get_json()["status_code"] == testing_data["status_code"]


def test_heartbeat_endpoint_post(create_app):

    testing_data = {
        "device": "my device",
        "ip_address": "192.168.0.185",
        "status_code": 200,
        "status_msg": "I am safe"
    }

    with create_app as client:

        result = client.post("/heartbeat", json=testing_data)
        assert result.status_code == 200
        assert result.get_json()["ip_address"] == testing_data["ip_address"]
        assert result.get_json()["status_code"] == testing_data["status_code"]