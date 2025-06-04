import os
import sys
import django
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "legal_ai.settings")
django.setup()

from django.test import RequestFactory
from legal_ai.health import healthz


def test_healthz_ok(monkeypatch):
    monkeypatch.setattr("legal_ai.health.redis_client.ping", lambda: True)
    request = RequestFactory().get("/healthz/")
    response = healthz(request)
    assert response.status_code == 200
    assert response.data["redis"] == "ok"
