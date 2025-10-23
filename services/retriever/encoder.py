# services/retriever/embeddings/encoder.py
from typing import List
import os

# Secure API key handling - NEVER hardcode keys in production
def _get_openai_client():
    """Safely initialize OpenAI client with environment variable."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable not set. "
            "Please set it in your .env file or environment: export OPENAI_API_KEY=your_key_here"
        )
    if api_key.startswith("sk-") and len(api_key) < 20:
        raise RuntimeError(
            "Invalid OpenAI API key format. Please check your OPENAI_API_KEY environment variable."
        )
    return api_key

# If you want OpenAI embeddings (requires `pip install openai`)
try:
    from openai import OpenAI
    _USE_OPENAI = True
    try:
        api_key = _get_openai_client()
        client = OpenAI(api_key=api_key)
    except RuntimeError as e:
        print(f"⚠️ OpenAI client initialization failed: {e}")
        _USE_OPENAI = False
        client = None
except ImportError:
    print("⚠️ OpenAI package not installed. Install with: pip install openai")
    _USE_OPENAI = False
    client = None

# Optional: fallback to local embeddings
try:
    from sentence_transformers import SentenceTransformer
    local_model = SentenceTransformer("all-MiniLM-L6-v2")
except ImportError:
    print("⚠️ sentence-transformers package not installed. Install with: pip install sentence-transformers")
    local_model = None


def get_embedding(text: str) -> List[float]:
    """
    Convert text into an embedding vector.

    Priority:
    1. Use OpenAI if installed and API key present
    2. Else, use local sentence-transformers model if available
    3. Else, raise an error
    """
    text = text.strip()
    if not text:
        raise ValueError("Cannot embed empty text.")

    # Option 1: Use OpenAI
    if _USE_OPENAI:
        resp = client.embeddings.create(
            model="text-embedding-3-small",  # or "text-embedding-3-large"
            input=text
        )
        return resp.data[0].embedding

    # Option 2: Use local model
    if local_model:
        return local_model.encode(text).tolist()

    # Fallback: no embedding backend available
    raise RuntimeError(
        "No embedding backend found. Install `openai` or `sentence-transformers`."
    )
