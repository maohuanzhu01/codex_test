from django.test import RequestFactory
from legal_ai.health import healthz


def test_healthz_ok(monkeypatch):
    monkeypatch.setattr("legal_ai.health.redis_client.ping", lambda: True)
    request = RequestFactory().get("/healthz/")
    response = healthz(request)
    assert response.status_code == 200
    assert response.data["redis"] == "ok"
