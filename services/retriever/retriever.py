# minimal Chroma retriever example 
from chromadb import Client 
from chromadb.config import Settings
from openai import OpenAI 

# pseudo code for retriever service
# adapt the embedding provider 
#from services.retriever.encoder import get_embedding
from ..retriever.encoder import get_embedding
from ..chroma_storage.chroma_config import get_chroma_client

client = get_chroma_client()
collection = client.get_or_create_collection(name="protocol_docs")
print("col count:", collection.count())
all_items = collection.get(limit=3)
print("Sample stored items:", all_items)

# query embedding
def retrieve(query: str, top_k: int = 1):
    # get embedding(OpenAI)
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
    #print(chunks)
    best_chunk = min(chunks, key=lambda x: x["distance"])
    print("best_chunk content:", best_chunk["content"])
    
    return best_chunk

retrieve("How does Ethereum handle liquidity?")






























































































