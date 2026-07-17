from __future__ import annotations

import app as app_module
from app import create_app
import lib.people_api_client as people_module


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_people_api_client_get_response_body_loads_json(monkeypatch):
    payload = [{"name": "Ada Lovelace", "role": "mathematician"}]

    def fake_get(url: str, timeout: int):
        assert url == people_module.PeopleApiClient.DEFAULT_ENDPOINT
        assert timeout == 10
        return DummyResponse(payload)

    monkeypatch.setattr(people_module.requests, "get", fake_get)

    client = people_module.PeopleApiClient()
    assert client.get_response_body() == payload


def test_people_endpoint_returns_json_payload(monkeypatch):
    payload = [{"name": "Alan Turing", "role": "scientist"}]
    monkeypatch.setattr(app_module.people_client, "get_response_body", lambda: payload)

    client = create_app().test_client()
    response = client.get("/api/people")

    assert response.status_code == 200
    assert response.get_json() == payload
