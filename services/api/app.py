from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import json

# import existing functions
from ..llm.orchestrator import protocol_analyze  

app = FastAPI()

# simple home page UI
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <head>
        <title>Protocol Analyzer</title>
        <style>
            body { font-family: sans-serif; margin: 40px; background-color: #f9f9f9; }
            textarea, input { width: 100%; margin: 10px 0; padding: 10px; border-radius: 8px; border: 1px solid #ccc; }
            button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; }
            button:hover { background: #45a049; }
            pre { background: #fff; padding: 20px; border-radius: 10px; border: 1px solid #ddd; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>BRaG</h1>
        <form action="/analyze" method="post">
            <label>Address:</label><br>
            <input name="factory_contract" placeholder="" required><br>
            
            <label>Your Question:</label><br>
            <textarea name="query" placeholder="e.g. Explain the upgrade path for this protocol" rows="4" required></textarea><br>
            
            <button type="submit">Analyze</button>
        </form>
    </body>
    </html>
    """

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(factory_contract: str = Form(...), query: str = Form(...)):
    try:
        response = protocol_analyze(factory_contract, query)
        return f"""
        <html><body style='font-family:sans-serif; margin:40px'>
        <h2>Analysis Result</h2>
        <pre>{response}</pre>
        <a href="/">🔙 Back</a>
        </body></html>
        """
    except Exception as e:
        return f"<h3>Error:</h3><pre>{str(e)}</pre>"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


























