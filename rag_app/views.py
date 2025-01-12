from django.http import JsonResponse
from .utils import RAGHandler
from dashboard_app.models import DocumentChunk
from .models import VectorEmbedding
import numpy as np
from django.db import transaction
from django.db.models import F
from django.db.models.functions import Cast
from django.db.models import FloatField

rag_handler = RAGHandler()

def process_embeddings(chunk_ids=None):
    try:
        if chunk_ids:
            chunks = DocumentChunk.objects.filter(id__in=chunk_ids)
        else:
            # Hanya proses chunk yang belum memiliki embedding
            chunks = DocumentChunk.objects.filter(vector__isnull=True)

        if not chunks.exists():
            return {
                'status': 'success',
                'message': 'No new chunks to process',
                'processed_count': 0
            }

        batch_size = 32
        processed_count = 0

        for i in range(0, chunks.count(), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            texts = [chunk.content for chunk in batch_chunks]
            
            embeddings = rag_handler.generate_embeddings(texts)

            with transaction.atomic():
                for chunk, embedding in zip(batch_chunks, embeddings):
                    VectorEmbedding.objects.create(
                        chunk=chunk,
                        embedding=embedding.tolist(),
                        content=chunk.content,
                        chunk_index=chunk.chunk_index
                    )
            
            processed_count += len(batch_chunks)

        return {
            'status': 'success',
            'message': f'Successfully processed {processed_count} chunks',
            'processed_count': processed_count
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error processing embeddings: {str(e)}',
            'processed_count': 0
        }

def search_similar_chunks(query_text, top_k=5):
    try:
        query_embedding = rag_handler.generate_single_embedding(query_text)
        
        # Use cosine similarity
        similar_chunks = VectorEmbedding.objects.raw('''
            SELECT id, content, chunk_index, chunk_id,
                   1 - (embedding <=> %s::vector) as similarity
            FROM rag_app_vectorembedding
            ORDER BY similarity DESC
            LIMIT %s
        ''', [query_embedding.tolist(), top_k])

        results = []
        for chunk in similar_chunks:
            results.append({
                'content': chunk.content,
                'chunk_index': chunk.chunk_index,
                'document_id': chunk.chunk_id,
                'similarity_score': float(chunk.similarity)
            })

        return {
            'status': 'success',
            'results': results
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error searching chunks: {str(e)}'
        }