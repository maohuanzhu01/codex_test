from django.urls import path
from .views import SearchView, DocumentUploadView

urlpatterns = [
    path("v1/search/", SearchView.as_view(), name="search"),
    path("v1/upload/", DocumentUploadView.as_view(), name="upload"),
]
