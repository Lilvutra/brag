sequenceDiagram
participant User
participant API as FastAPI
participant Retriever as "Retriever Service (Vector DB)"
participant LLM as "LLM Orchestrator (LangChain)"
participant Simulator as "Simulation (Hardhat/Tenderly)"
participant Auditor as "Static Analyzer (Slither/MythX)"
participant Multisig as "Gnosis Safe"
participant Chain as "Blockchain (RPC)"


User->>API: POST /api/v1/query {wallet, query, options}
API->>Retriever: embed(query) -> top_k
Retriever-->>API: [chunks + metadata + merkle_proofs]
API->>LLM: prompt(query + chunks + chain_state)
LLM-->>API: answer + actions (optional)
alt action_required
API->>Simulator: simulate(tx/actions)
Simulator-->>API: sim_result
API->>Auditor: run static analysis (if contract/code)
Auditor-->>API: audit_report
API->>Multisig: create proposal (tx payload)
Multisig-->>Chain: signed tx
Chain-->>API: tx_hash + receipt
API-->>User: answer + tx_hash + provenance
else no_action
API-->>User: answer + provenance
end


Note right of Retriever: Vector DB (Pinecone/Chroma)
Note right of LLM: Option for local LLM or OpenAI/Claude