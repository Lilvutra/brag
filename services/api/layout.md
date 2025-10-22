blockchain-rag/
├─ services/
│ ├─ api/ # FastAPI service
│ │ ├─ app.py
│ │ ├─ schemas.py
│ │ └─ requirements.txt
│ ├─ retriever/ # retrieval microservice (Chroma or Pinecone)
│ │ ├─ retriever.py
│ │ └─ requirements.txt
│ ├─ indexer/ # ingestion, embedder, anchoring
│ │ ├─ indexer.py
│ │ └─ requirements.txt
│ └─ web3-listener/ # chain event listeners
│ ├─ listener.py
│ └─ requirements.txt
├─ contracts/
│ ├─ MerkleAnchor.sol
│ └─ hardhat.config.js
├─ infra/
│ ├─ docker-compose.yml
│ └─ k8s/...
├─ ci/
│ └─ pipeline.yml
└─ README.md

📥 Ingestion → 📚 Chunk → 🧠 Embed → 📊 Store in Vector DB
                                     ↓
                              🔐 Merkle root → ⛓️ Anchor on-chain

📤 Query → 🔍 Retrieve vectors → 🧠 RAG answer → ✅ Verify with root
