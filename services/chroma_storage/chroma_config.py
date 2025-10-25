import chromadb
from chromadb.config import Settings
import os 

# Persistent directory shared by all services
CHROMA_DB_DIR = "./chroma_storage"

# Persist directory (relative to project root)
#CHROMA_DB_DIR = os.path.join(os.path.dirname(__file__), "../../chroma_storage")

print("CHROMA_DB_DIR =", os.path.abspath(CHROMA_DB_DIR))

def get_chroma_client():
    """Return a ChromaDB client that persists data."""
    return chromadb.PersistentClient(path=CHROMA_DB_DIR)
