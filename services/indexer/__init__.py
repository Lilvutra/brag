"""
Indexer Service Package

Document processing and indexing services for the blockchain RAG system.
Handles PDF/URL text extraction, chunking, embedding, and ChromaDB storage.
"""

from .indexer import (
    index_pdf,
    index_url, 
    extract_text_from_pdf,
    extract_text_from_url,
    chunk_words_with_overlap,
    chunk_by_tokens
)

__all__ = [
    "index_pdf",
    "index_url", 
    "extract_text_from_pdf",
    "extract_text_from_url",
    "chunk_words_with_overlap",
    "chunk_by_tokens"
]
