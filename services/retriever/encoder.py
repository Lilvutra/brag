# services/retriever/embeddings/encoder.py
from typing import List
import os

# If you want OpenAI embeddings (requires `pip install openai`)
try:
    from openai import OpenAI
    _USE_OPENAI = True
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    _USE_OPENAI = False

# Optional: fallback to local embeddings
try:
    from sentence_transformers import SentenceTransformer
    local_model = SentenceTransformer("all-MiniLM-L6-v2")
except ImportError:
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

    # ✅ Option 1: Use OpenAI
    if _USE_OPENAI:
        resp = client.embeddings.create(
            model="text-embedding-3-small",  # or "text-embedding-3-large"
            input=text
        )
        return resp.data[0].embedding

    # ✅ Option 2: Use local model
    if local_model:
        return local_model.encode(text).tolist()

    # ❌ Fallback: no embedding backend available
    raise RuntimeError(
        "No embedding backend found. Install `openai` or `sentence-transformers`."
    )
