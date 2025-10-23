# Blockchain RAG System - Complete Process Diagram

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           BLOCKCHAIN RAG SYSTEM                                 │
│                                                                                 │
│  📥 INPUT LAYER          🔄 PROCESSING LAYER        📤 OUTPUT LAYER             │
│  ┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐      │
│  │ PDF Files       │    │ Indexer Service     │    │ API Response       │      │
│  │ Protocol URLs   │    │ Retriever Service  │    │ Answer + Sources   │      │
│  │ User Queries    │    │ LLM Orchestrator   │    │ Actions + Simulation│      │
│  └─────────────────┘    └─────────────────────┘    └─────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📊 Complete Process Flow

### 1. **INDEXING PHASE** (Offline/Batch Processing)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                INDEXING PHASE                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

📄 PDF INPUT                    🌐 URL INPUT
    │                              │
    ▼                              ▼
┌─────────────┐              ┌─────────────┐
│ PDF Parser  │              │ Web Scraper │
│ (pdfplumber │              │ (trafilatura│
│  PyPDF2)    │              │  BeautifulSoup)│
└─────────────┘              └─────────────┘
    │                              │
    ▼                              ▼
┌─────────────────────────────────────────────────┐
│              TEXT EXTRACTION                    │
│  • Extract raw text from documents              │
│  • Clean and normalize content                  │
│  • Handle different formats (PDF, HTML, etc.)  │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              CHUNKING STRATEGY                  │
│  • Word-based chunking (500 words, 50 overlap) │
│  • Token-based chunking (1024 tokens)          │
│  • Preserve context between chunks              │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              EMBEDDING GENERATION               │
│  • OpenAI API (text-embedding-3-small)         │
│  • Sentence Transformers (fallback)             │
│  • Convert text chunks to vectors             │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              CHROMA DB STORAGE                  │
│  • Store embeddings + metadata                 │
│  • Index for fast similarity search             │
│  • Track source provenance                      │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              MERKLE ROOT COMPUTATION             │
│  • Hash all chunk contents                      │
│  • Build Merkle tree for integrity              │
│  • (Future: Anchor on blockchain)               │
└─────────────────────────────────────────────────┘
```

### 2. **QUERY PHASE** (Real-time Processing)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                QUERY PHASE                                     │
└─────────────────────────────────────────────────────────────────────────────────┘

👤 USER QUERY
    │
    ▼
┌─────────────────────────────────────────────────┐
│              API GATEWAY                        │
│  • FastAPI endpoint: /api/v1/query             │
│  • Request validation (Pydantic)               │
│  • Generate unique request_id                  │
│  • Log query start                             │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              QUERY EMBEDDING                    │
│  • Convert user query to vector                │
│  • Use same embedding model as indexing        │
│  • Handle API key validation                  │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              VECTOR SEARCH                       │
│  • Search ChromaDB for similar chunks           │
│  • Return top-k most relevant results          │
│  • Include metadata and similarity scores       │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              LLM ORCHESTRATION                  │
│  • Build context from retrieved chunks          │
│  • Generate prompt with context + query        │
│  • Call LLM for answer generation               │
│  • Detect potential on-chain actions            │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              ACTION DETECTION                   │
│  • Analyze query for transaction intent        │
│  • Extract action parameters (amount, address)  │
│  • Return structured action objects            │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              SIMULATION (Future)                │
│  • Simulate on-chain actions                   │
│  • Run static analysis (Slither, MythX)       │
│  • Generate multisig proposals                 │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              RESPONSE ASSEMBLY                  │
│  • Combine answer + sources + actions          │
│  • Add simulation results (if applicable)      │
│  • Include request metadata                    │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              LOGGING & MONITORING               │
│  • Log query completion                         │
│  • Track performance metrics                    │
│  • Record processing time                       │
└─────────────────────────────────────────────────┘
    │
    ▼
👤 USER RESPONSE
```

## 🔄 Detailed Component Interactions

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

## 📁 File Structure & Responsibilities

```
services/
├── api/
│   └── app.py                    # FastAPI gateway, request handling, logging
├── retriever/
│   ├── retriever.py             # ChromaDB vector search
│   └── encoder.py               # Embedding generation (OpenAI/SentenceTransformers)
├── llm/
│   └── orchestrator.py          # LLM orchestration, action detection
└── indexer/
    └── indexer.py               # Document processing, chunking, indexing
```

## 🔐 Security & Data Flow

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

## 🚀 Execution Paths

### **Indexing Path**
```
python services/indexer/indexer.py document.pdf
→ extract_text_from_pdf()
→ chunk_words_with_overlap()
→ get_embedding() for each chunk
→ store in ChromaDB
→ compute Merkle root
→ return results
```

### **Query Path**
```
POST /api/v1/query
→ validate request
→ retrieve(query, top_k=5)
→ run_llm(query, chunks)
→ detect actions
→ simulate (if actions)
→ return response
```

This diagram shows the complete end-to-end flow of the blockchain RAG system, from document ingestion to query processing and response generation.
