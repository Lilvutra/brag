# minimal Chroma retriever example 
from chromadb import Client 
from chromadb.config import Settings
from openai import OpenAI # embedding provider

# pseudo code for retriever service
# adapt the embedding provider 
from services.retriever.encoder import get_embedding

client = Client(Settings())
collection = client.get_or_create_collection(name="my_collection")

def retrieve(query: str, top_k: int = 5):
    # get embedding(use OpenAI)
    q_emb = get_embedding(query)
    results = collection.query(query_embeddings=[q_emb], n_results=top_k)
    
    # results contain documents, metadatas, ids, distances
    chunks = []
    
    # if multiple queries, loop over results['documents'][i] instead of hardcoded [0]
    for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        chunks.append({
            "content": doc, 
            "metadata": meta, 
            "distance": dist})
    return chunks
































































































