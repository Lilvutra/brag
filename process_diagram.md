# BRAG Process Diagram

## System Architecture Overview

### **API Service Flow**
```
app.py:query()
├── Generate request_id (UUID)
├── Log query start
├── Call retriever.retrieve()
│   ├── encoder.get_embedding(query)
│   ├── ChromaDB.query()
│   └── Return top-k chunks
├── Call llm.orchestrator.run_llm()
│   ├── Build context from chunks
│   ├── Generate prompt
│   ├── Call LLM (OpenAI)
│   └── Detect actions
├── Handle simulation (if actions)
├── Log completion
└── Return QueryResponse
```

### **Indexer Service Flow**
```
indexer.py:index_pdf() / index_url()
├── Extract text (PDF/URL)
├── Chunk text (word/token-based)
├── For each chunk:
│   ├── encoder.get_embedding(chunk)
│   ├── Generate metadata
│   └── Compute content hash
├── Store in ChromaDB
├── Compute Merkle root
└── Return indexing results
```

### **Retriever Service Flow**
```
retriever.py:retrieve()
├── encoder.get_embedding(query)
├── ChromaDB.query(embeddings, n_results)
├── Format results with metadata
└── Return chunks array
```

### **LLM Orchestrator Flow**
```
orchestrator.py:run_llm()
├── Build context from chunks
├── Create prompt: "Context: {chunks}\nQuestion: {query}"
├── Call LLM for answer
├── Detect actions (heuristic)
└── Return (answer, actions)
```


## Security & Data Flow(expected further update)

```
ENVIRONMENT VARIABLES
├── OPENAI_API_KEY (secure)
├── CHROMA_DB_PATH
└── LOG_LEVEL

DATA FLOW
├── Input: PDF/URL → Text → Chunks → Embeddings → ChromaDB
├── Query: User Query → Embedding → Search → Chunks → LLM → Answer
└── Logging: All operations logged with request_id tracking

SECURITY
├── API keys via environment variables
├── Input validation (Pydantic)
├── Error handling without data leaks
└── Structured logging for audit trails
```
