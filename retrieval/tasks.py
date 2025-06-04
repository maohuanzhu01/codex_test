from celery import shared_task
from .models import LegalDocument, LegalDocumentChunk
from sentence_transformers import SentenceTransformer
from django.contrib.postgres.search import SearchVector
import pdfminer.high_level
import docx

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

@shared_task
def ingest_document(document_id: int) -> None:
    doc = LegalDocument.objects.get(id=document_id)
    text = _extract_text(doc.file.path)
    chunks = list(_split_text(text, 1000))
    embeddings = model.encode(chunks)
    for chunk, emb in zip(chunks, embeddings):
        LegalDocumentChunk.objects.create(
            document=doc,
            text=chunk,
            embedding=emb.tolist(),
            search_vector=SearchVector(chunk),
        )

def _extract_text(path: str) -> str:
    if path.lower().endswith('.pdf'):
        return pdfminer.high_level.extract_text(path)
    if path.lower().endswith('.docx'):
        document = docx.Document(path)
        return '\n'.join(p.text for p in document.paragraphs)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def _split_text(text: str, tokens: int):
    words = text.split()
    for i in range(0, len(words), tokens):
        yield ' '.join(words[i:i+tokens])
