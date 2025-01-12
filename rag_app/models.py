from django.db import models
from dashboard_app.models import DocumentChunk
import uuid
from pgvector.django import VectorField, HnswIndex

# Create your models here.
class VectorEmbedding(models.Model):
    """
    Stores the vector embeddings for document chunks
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chunk = models.OneToOneField(
        DocumentChunk, on_delete=models.CASCADE, related_name="vector"
    )
    embedding = VectorField(dimensions=384)
    content = models.TextField()
    chunk_index = models.IntegerField()
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            HnswIndex(
                name="document_embedding_idx",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],  # Menggunakan cosine similarity
            )
        ]
