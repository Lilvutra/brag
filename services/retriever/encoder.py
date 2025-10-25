# services/retriever/embeddings/encoder.py
from typing import List
import os
from openai import OpenAI

# Secure API key handling - NEVER hardcode keys in production
def _get_openai_client():
    """Safely initialize OpenAI client with environment variable."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable not set. "
            "Please set it in your .env file or environment: export OPENAI_API_KEY=your_key_here"
        )
    return api_key

_USE_OPENAI = True
try:
    api_key = _get_openai_client()
    client = OpenAI(api_key=api_key)
except RuntimeError as e:
    print(f"⚠️ OpenAI client initialization failed: {e}")
    _USE_OPENAI = False
    client = None


# Optional: fallback to local embeddings


def get_embedding(text: str) -> List[float]:
    """
    Convert text into an embedding vector using OpenAI if installed and API key present
    might use local sentence-transformers model if available
    """
    text = text.strip()
    if not text:
        raise ValueError("Cannot embed empty text.")

    # Use OpenAI
    if _USE_OPENAI:
        resp = client.embeddings.create(
            model="text-embedding-3-small",  # or "text-embedding-3-large"
            input=text
        )
        return resp.data[0].embedding

    # Option 2: Use local model
    #if local_model:
        #return local_model.encode(text).tolist()

    # Fallback: no embedding backend available
    raise RuntimeError(
        "No embedding backend found. Install `openai` or `sentence-transformers`."
    )
