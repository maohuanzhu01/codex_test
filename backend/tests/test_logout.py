import json
import os
import sys
import django
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "legal_ai.settings")
django.setup()

from django.test import RequestFactory
from rest_framework import status
from rest_framework.permissions import AllowAny
from accounts.views import LogoutView


def test_logout_missing_refresh(monkeypatch):
    monkeypatch.setattr(LogoutView, "permission_classes", [AllowAny])
    request = RequestFactory().post(
        "/auth/logout/", data=json.dumps({}), content_type="application/json"
    )
    response = LogoutView.as_view()(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
