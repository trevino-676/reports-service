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


def test_get_taxables_perceptions_report(headers):
    test_app = app.test_client()
    rfc = "GPR070228780"
    to = "2021-05-10"
    from_date = "2021-05-01"
    response = test_app.get(
        "/v1/payroll/reports/taxables_perceptions?datos.Rfc={}&from_date={}&to_date={}".format(
            rfc, from_date, to
        )
    )
    assert 200 == response.status_code
    assert response.json["status"] is True
    assert len(response.json["data"]) > 0
