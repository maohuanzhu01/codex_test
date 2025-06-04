from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from pgvector.django import CosineDistance
from .models import LegalDocumentChunk
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({'detail': 'Query parameter q required.'}, status=400)
        embedding = model.encode([query])[0].tolist()
        qs = (LegalDocumentChunk.objects
              .annotate(rank=SearchRank(SearchVector('text'), SearchQuery(query)))
              .order_by(CosineDistance('embedding', embedding))[:5])
        results = [{'document_id': chunk.document_id, 'text': chunk.text} for chunk in qs]
        return Response({'results': results})
