# models.py

from django.db import models
from django.contrib.auth import get_user_model
import uuid
from pgvector.django import VectorField, HnswIndex


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    file_type = models.CharField(max_length=50)
    file_path = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, related_name="chunks")
    chunk_index = models.IntegerField()
    content = models.TextField()  # Tambahkan field content
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["chunk_index"]
        constraints = [
            models.UniqueConstraint(fields=["document", "chunk_index"], name="unique_chunk_per_document")
        ]


