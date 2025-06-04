from django.db import models
from django.contrib.postgres.search import SearchVectorField
from pgvector.django import VectorField

class LegalDocument(models.Model):
    organization = models.ForeignKey('legalchat.Organization', on_delete=models.CASCADE, related_name='legal_documents')
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class LegalDocumentChunk(models.Model):
    document = models.ForeignKey(LegalDocument, on_delete=models.CASCADE, related_name='chunks')
    text = models.TextField()
    embedding = VectorField(dimensions=768)
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['search_vector'], name='ld_chunk_search_vector_idx'),
        ]

