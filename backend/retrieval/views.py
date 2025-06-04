from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from pgvector.django import CosineDistance
from rest_framework.parsers import MultiPartParser, FormParser
from legalchat.models import Organization
from .models import LegalDocumentChunk, LegalDocument
from .tasks import ingest_document
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q")
        if not query:
            return Response({"detail": "Query parameter q required."}, status=400)
        embedding = model.encode([query])[0].tolist()
        qs = LegalDocumentChunk.objects.annotate(
            rank=SearchRank(SearchVector("text"), SearchQuery(query))
        ).order_by(CosineDistance("embedding", embedding))[:5]
        results = [
            {"document_id": chunk.document_id, "text": chunk.text} for chunk in qs
        ]
        return Response({"results": results})


class DocumentUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        upload = request.FILES.get("file")
        if not upload:
            return Response({"detail": "File required."}, status=400)
        organization = getattr(request.user, "organization", None)
        if organization is None:
            organization = Organization.objects.first()
        doc = LegalDocument.objects.create(organization=organization, file=upload)
        ingest_document.delay(doc.id)
        return Response({"id": doc.id}, status=201)
