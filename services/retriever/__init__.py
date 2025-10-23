"""
Retriever Service Package

Vector search and embedding services for the blockchain RAG system.
Handles ChromaDB operations and embedding generation.
"""

from .retriever import retrieve
from .encoder import get_embedding

__all__ = ["retrieve", "get_embedding"]
