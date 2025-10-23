from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging
def setup_logging():
    """Setup structured logging for the API."""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
   
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Setup file handler for API logs
    file_handler = logging.FileHandler("logs/api.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Initialize logging
logger = setup_logging()

# API gateway 
app = FastAPI(title="Blockchain RAG API", version="1.0.0")

class QueryRequest(BaseModel):
    wallet: str
    query: str
    options: dict = {}

class QueryResponse(BaseModel):
    request_id: str
    answer: str
    sources: Optional[list] = None
    actions: Optional[list] = None
    simulation: Optional[dict] = None
    timestamp: str

def log_query_start(request_id: str, wallet: str, query: str, options: dict):
    """Log the start of a query request."""
    logger.info(f"QUERY_START - ID: {request_id} | Wallet: {wallet} | Query: '{query[:100]}...' | Options: {options}")

def log_query_success(request_id: str, answer: str, chunks_count: int, actions_count: int = 0):
    """Log successful query completion."""
    logger.info(f"QUERY_SUCCESS - ID: {request_id} | Answer length: {len(answer)} | Chunks: {chunks_count} | Actions: {actions_count}")

def log_query_error(request_id: str, error: str, error_type: str = "UNKNOWN"):
    """Log query errors."""
    logger.error(f"QUERY_ERROR - ID: {request_id} | Type: {error_type} | Error: {error}")

@app.post('/api/v1/query', response_model=QueryResponse)
async def query(req: QueryRequest):
    """Handle blockchain RAG queries with comprehensive logging."""
    request_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    try:
        # Log query start
        log_query_start(request_id, req.wallet, req.query, req.options)
        
        # Call retriever service
        try:
            from services.retriever import retrieve
            chunks = retrieve(req.query, top_k=5) #return 5 most relevant chunks
            logger.info(f"RETRIEVAL_SUCCESS - ID: {request_id} | Retrieved {len(chunks)} chunks")
        except Exception as e:
            log_query_error(request_id, f"Retrieval failed: {str(e)}", "RETRIEVAL_ERROR")
            raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")
       
        # Call LLM orchestrator
        try:
            from services.llm import run_llm 
            answer, actions = run_llm(req.query, chunks)
            logger.info(f"LLM_SUCCESS - ID: {request_id} | Answer generated, actions: {len(actions) if actions else 0}")
        except Exception as e:
            log_query_error(request_id, f"LLM processing failed: {str(e)}", "LLM_ERROR")
            raise HTTPException(status_code=500, detail=f"LLM processing failed: {str(e)}")
        
        # Handle actions if present
        simulation_result = None
        if actions:
            try:
                # Note: simulator module doesn't exist yet, so we'll mock it
                logger.info(f"ACTIONS_DETECTED - ID: {request_id} | Actions: {actions}")
                # from simulator.sim import simulate_actions
                # simulation_result = simulate_actions(actions)
                simulation_result = {"status": "mocked", "actions": actions}
                logger.info(f"SIMULATION_SUCCESS - ID: {request_id} | Simulation completed")
            except Exception as e:
                log_query_error(request_id, f"Simulation failed: {str(e)}", "SIMULATION_ERROR")
                # Don't fail the entire request for simulation errors
                simulation_result = {"status": "error", "error": str(e)}
        
        # Log successful completion
        log_query_success(request_id, answer, len(chunks), len(actions) if actions else 0)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"QUERY_COMPLETE - ID: {request_id} | Processing time: {processing_time:.2f}s")
        
        # Return response
        return QueryResponse(
            request_id=request_id,
            answer=answer,
            sources=chunks,
            actions=actions,
            simulation=simulation_result,
            timestamp=start_time.isoformat()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (already logged)
        raise
    except Exception as e:
        # Log unexpected errors
        log_query_error(request_id, f"Unexpected error: {str(e)}", "UNEXPECTED_ERROR")
        raise HTTPException(status_code=500, detail="Internal server error")

































