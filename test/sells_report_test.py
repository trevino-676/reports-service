import json

import pytest
import requests

from app import app


@pytest.fixture
def headers():
    payload = {"username": "user_test@test.com", "password": "test123"}
    headers = {"Content-Type": "application/json"}
    res = requests.post(
        "https://www.sonar32.com.mx/auth", data=json.dumps(payload), headers=headers
    )
    headers["Authorization"] = f"jwt {res.json()['access_token']}"
    return headers


def test_get_sells_by_clients_report(headers):
    test_app = app.test_client()
    headers = headers
    response = test_app.get("/v1/sellsreport/by_client?rfc=PGT190401156", headers=headers)
    assert 200 == response.status_code
    assert response.json["status"] is True
    assert len(response.json["data"]) > 0
