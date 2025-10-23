"""
LLM Service Package

LLM orchestration and action detection for the blockchain RAG system.
Handles prompt building, LLM calls, and on-chain action detection.
"""

from .orchestrator import run_llm

__all__ = ["run_llm"]
