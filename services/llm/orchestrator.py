# pseudo orchestration: accept query and chunks 
from ..retriever.retriever import retrieve
from ..log_tracing.trace import get_logs, fetch_abi_from_logs
import json
from ..retriever.encoder import _get_openai_client
from openai import OpenAI

api_key = _get_openai_client()
client = OpenAI(api_key=api_key)

def llm_generate(prompt):
    response = client.chat.completions.create(
        model="gpt-5",  # or "gpt-4o-mini"
        messages=[
            {"role": "system", "content": "You are an expert blockchain protocol auditor."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def run_llm(query, chunks):
    # build prompt 
    context = "\n".join([c['text'] for c in chunks])
    prompt = f"Context: \n{context}\n\nQuestion: {query}\nAnswer:"
    
    # call LLM (pseudo code) or local llm
    # for prototype, we just return a dummy answer
    answer = f"(prototype) Answer based on {len(chunks)} chunks"
    actions = None 
    
    # Heuristic: if prompt contains "sth", we trigger on-chain action
    if "transfer" in query.lower() or "send" in query.lower():
        actions = [{"type": "transfer", "to": "0xABC...", "amount": "10 ETH"}]
        
    return answer, actions
    
    
def protocol_analyze(factory_contract, query):
    # Retrieve relevant documentation context
    chunks = retrieve(query)
    
    # Fetch recent on-chain logs for the factory and its deployed contracts
    logs = get_logs(factory_contract, 21000000)
    
    # For each address in logs, fetch its ABI
    abis = fetch_abi_from_logs(logs)
    
    #docs_context = "\n".join(c.get("text", "") for c in chunks)
    abi_logs = json.dumps(abis, indent=2)

    # Build unified context
    context = f"""
    Protocol Docs Context:
    {chunks}
    
    ABI from logs data:
    {abi_logs}
    
    """
    
    # Pass context + query to the LLM
    prompt = f"""
    You are analyzing the protocol upgrade behavior.
    Using the context below, answer the question:

    {query}

    {context}
    """

    response = llm_generate(prompt)
    return response

print("protocol analysis:", protocol_analyze("0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9", "Analyze Aave protocol?" ))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




























































