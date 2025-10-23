"""
API Service Package

FastAPI gateway for the blockchain RAG system.
Handles request validation, logging, and response formatting.
"""

from .app import app, QueryRequest, QueryResponse

__all__ = ["app", "QueryRequest", "QueryResponse"]
