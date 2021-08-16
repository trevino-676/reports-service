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


def test_get_provider_detailed_report(headers):
    test_app = app.test_client()
    rfc = "PGT190401156"
    from_date = "2021-05-01T00:00:00"
    to_date = "2021-05-31T23:59:59"
    url = "/v1/report/detialed/provider?rfc={}&from_date={}&to_date={}".format(
        rfc, from_date, to_date
    )
    response = test_app.get(url, headers=headers)

    assert 200 == response.status_code
    assert response.json["status"] is True
    assert len(response.json["data"]) > 0
