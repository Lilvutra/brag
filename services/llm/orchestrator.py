# pseudo orchestration: accept query and chunks 

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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




























































