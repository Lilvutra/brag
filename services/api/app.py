from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid 

# API gateway 
app = FastAPI()

class QueryRequest(BaseModel):
    wallet: str
    query: str
    options: dict = {}

@app.post('/api/v1/query')
async def query(req: QueryRequest):
    # Log to Kafka / queue
    request_id = str(uuid.uuid4())
    # 2) call retriever service (HTTP/RPC)
    # For this starter, call local funciton
    from retriever.retriever import retrieve
    chunks = retrieve(req.query, top_k=5)
   
    from llm.orchestrator import run_llm 
    answer, actions = run_llm(req.query, chunks)
    
    #4) If actions contains on_chain ops, run simulation/audit flow 
    if actions:
        from simulator.sim import simulate_actions
        sim_result = simulate(actions)
        # run static analyzers, gating, multisig, etc.
        return {
            "request_id": request_id,
            "answer": answer,
            "actions": actions,
            "simulation": sim_result
        }
    return ("answer": answer, "sources": chunks, "request_id": request_id)

































