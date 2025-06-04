from django.test import RequestFactory
from rest_framework import status
from rest_framework.permissions import AllowAny
from unittest import mock
import importlib
import sys


class DummyModel:
    def encode(self, _: list[str]) -> list[list[int]]:
        return [[0] * 768]


def get_search_view():
    with mock.patch(
        "sentence_transformers.SentenceTransformer", lambda *a, **k: DummyModel()
    ):
        if "retrieval.views" in sys.modules:
            del sys.modules["retrieval.views"]
        module = importlib.import_module("retrieval.views")
        module.SearchView.permission_classes = [AllowAny]
    return module.SearchView


def test_search_missing_q():
    SearchView = get_search_view()
    request = RequestFactory().get("/v1/search/")
    response = SearchView.as_view()(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
