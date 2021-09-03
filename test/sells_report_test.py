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
    response = test_app.get(
        "/v1/sellsreport/by_client?datos.Rfc=PGT190401156", headers=headers
    )
    assert 200 == response.status_code
    assert response.json["status"] is True
    assert len(response.json["data"]) > 0


def test_get_sells_by_items_report(headers):
    test_app = app.test_client()
    headers = headers
    response = test_app.get(
        "/v1/sellsreport/by_items?datos.Rfc=PGT190401156", headers=headers
    )
    assert 200 == response.status_code
    assert response.json["status"] is True
    assert len(response.json["data"]) > 0


def test_get_sells_by_service_report(headers):
    test_app = app.test_client()
    headers = headers
    response = test_app.get(
        "/v1/sellsreport/by_services?datos.Rfc=SED160404EK6", headers=headers
    )
    assert 200 == response.status_code
    assert response.json["status"] is True
    assert len(response.json["data"]) > 0


def test_detail_sells_report(headers):
    test_app = app.test_client()
    f_date = "2021-05-01T00:00:00"
    t_date = "2021-05-31T23:59:59"
    rfc = "PGT190401156"
    response = test_app.get(
        f"/v1/sellsreport/detailed?datos.Rfc={rfc}&from_date={f_date}&to_date={t_date}",
        headers=headers,
    )

    assert 200 == response.status_code
    assert response.json["status"] is True


def test_total_sells(headers):
    test_app = app.test_client()
    f_date = "2021-05-01T00:00:00"
    t_date = "2021-05-31T23:59:59"
    rfc = "PGT190401156"

    response = test_app.get(
        f"/v1/sellsreport/total?datos.Rfc={rfc}&from_date={f_date}&to_date={t_date}",
        headers=headers,
    )

    assert 200 == response.status_code
    assert response.json["status"] is True


def test_get_top_by_clients(headers):
    test_app = app.test_client()
    f_date = "2021-05-01T00:00:00"
    t_date = "2021-05-31T23:59:59"
    rfc = "PGT190401156"
    route = (
        f"/v1/sellsreport/top/clients?datos.Rfc={rfc}&from_date={f_date}&to_date={t_date}"
    )

    response = test_app.get(route, headers=headers)

    assert 200 == response.status_code
    assert response.json["status"] is True


def test_get_top_by_items(headers):
    test_app = app.test_client()
    f_date = "2021-05-01T00:00:00"
    t_date = "2021-05-31T23:59:59"
    rfc = "PGT190401156"
    route = (
        f"/v1/sellsreport/top/items?datos.Rfc={rfc}&from_date={f_date}&to_date={t_date}"
    )

    response = test_app.get(route, headers=headers)

    assert 200 == response.status_code
    assert response.json["status"] is True


def test_get_top_by_services(headers):
    test_app = app.test_client()
    f_date = "2021-06-01T00:00:00"
    t_date = "2021-06-30T23:59:59"
    rfc = "PGT190401156"
    route = (
        f"/v1/sellsreport/top/service?datos.Rfc={rfc}&from_date={f_date}&to_date={t_date}"
    )

    response = test_app.get(route, headers=headers)

    assert 200 == response.status_code
    assert response.json["status"] is True
