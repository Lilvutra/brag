blockchain-rag/
├─ services/
│ ├─ api/ # FastAPI 
│ │ ├─ app.py
│ │ ├─ schemas.py
│ │ └─ requirements.txt
│ ├─ retriever/ # retrieval microservice 
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
