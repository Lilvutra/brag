# To improve search efficiency, we chunk documents into smaller pieces, embed them into vectors, and store them in a vector database (ChromaDB). 
# We then anchor the Merkle root of the stored data on-chain for integrity verification later.
import hashlib
# placeholder import for further development
# from web3 import Web3

# Indexer: chunk documents, embed, insert into vector DB, then anchor merkle root on chain

import os
from typing import List, Dict, Iterable, Optional 

import chromadb
from chromadb.config import Settings
from ..chroma_storage.chroma_config import get_chroma_client

import pdfplumber
import PyPDF2
import trafilatura
import requests
import tiktoken
import hashlib 
from bs4 import BeautifulSoup
import argparse

from ..retriever.encoder import get_embedding


def extract_text_from_url(url: str) -> str:
    """Extract text from a protocol documentation blog/URL.
    
    Optimized for technical documentation with clean content extraction.
    Priority:
    1) trafilatura (best for web content, handles protocol docs well)
    2) BeautifulSoup fallback
    3) Raise helpful error
    """
    
    if not url or not url.startswith(('http://', 'https://')):
        raise ValueError(f"Invalid URL: {url}")
   
    # trafilatura  

    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        text = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
        if text and text.strip():
            return text.strip()
    # BeautifulSoup 


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file using the best available backend.

    Priority:
    1) pdfplumber if installed
    2) PyPDF2 if installed
    3) Raise a helpful error instructing how to install
    """
    if not pdf_path or not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # pdfplumber
    try:
        text_parts: List[str] = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_parts.append(page_text)
        return "\n".join(text_parts).strip()
    except Exception:
        pass

    # PyPDF2
    try:
        text_parts = []
        with open(pdf_path, "rb") as fh:
            reader = PyPDF2.PdfReader(fh)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text_parts.append(page_text)
        return "\n".join(text_parts).strip()
    except Exception as e:
        raise RuntimeError(
            "No PDF backend available. Install one of: `pip install pdfplumber` or `pip install PyPDF2`"
        ) from e


def chunk_text(text, size=500): # 500 words per chunk first
    # word-based chunking: split by words and produce chunks with up to `size` words each
    words = text.split()
    if not words: return []
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]
    

def chunk_words_with_overlap(text: str, size: int = 500, overlap: int = 50) -> List[str]:
    # split text into word-chunks with overlap between consecutive chunks 
    # size: number of words per chunk
    # overlap: number of overlapping words between consecutive chunks
    # note: there are limits
   
    if not text:
        return []
    if size <= 0:
        raise ValueError("size must > 0")
    
    if overlap < 0 or overlap >= size:
        raise ValueError("overlap must be >=0 and < size")
    
    words = text.split()
    chunks = []
    
    step = size - overlap
    if step <= 0:
        step = size # no overlap
    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start+size])
        chunks.append(chunk)
    return chunks 

def chunk_by_tokens(text: str, size_tokens: int = 1024, overlap_tokens: int = 128,
                    encoding_name: str = "cl100k_base") -> List[str]:
    
    # chunk text by tokens using tiktoken
   
    enc = tiktoken.get_encoding(encoding_name)
    # encode -> list[int]
    token_ids = enc.encode(text)
    chunks = []
    for i in range(0, len(token_ids), size_tokens - overlap_tokens):
        chunk = token_ids[i:i + size_tokens]
        chunks.append(chunk)
    return chunks


# Indexing pipeline for a single PDF 
def _ensure_collection(collection_name: str = "my_collection"):
    client = get_chroma_client()
    return client.get_or_create_collection(name=collection_name)


def _hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _compute_merkle_root(hashes: List[str]) -> Optional[str]:
    if not hashes:
        return None
    layer = hashes[:]
    while len(layer) > 1:
        next_layer: List[str] = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else left
            combined = bytes.fromhex(left) + bytes.fromhex(right)
            next_layer.append(_hash_bytes(combined))
        layer = next_layer
    return layer[0]


def _index_text(text: str, source: str, source_type: str,
                collection_name: str = "my_collection",
                chunk_size_words: int = 500,
                overlap_words: int = 50) -> Dict[str, Optional[str]]:
    """Core indexing logic: chunk, embed, and insert text into Chroma.
    placeholder for later on-chain anchoring"""
    
    chunks = chunk_words_with_overlap(text, size=chunk_size_words, overlap=overlap_words)
    if not chunks:
        return {"added": "0", "merkle_root": None}

    collection = _ensure_collection(collection_name)

    ids: List[str] = []
    documents: List[str] = []
    metadatas: List[Dict[str, str]] = []
    embeddings: List[List[float]] = []
    content_hashes: List[str] = []

    for idx, chunk in enumerate(chunks):
        emb = get_embedding(chunk)
        embeddings.append(emb)
        documents.append(chunk)
        cid = f"{source}:{idx}"
        ids.append(cid)
        metadatas.append({
            "source": source, 
            "source_type": source_type,
            "chunk_index": str(idx)
        })
        content_hashes.append(_hash_bytes(chunk.encode("utf-8")))

    #print("embeddings:", embeddings)
    #print("documents:", documents)
    #print("metadatas:", metadatas)
    #print("checky")
    
    collection.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)

    merkle_root = _compute_merkle_root(content_hashes)

    return {
        "added": str(len(ids)),
        "merkle_root": merkle_root,
        "source": source,
        "source_type": source_type
    }


def index_pdf(pdf_path: str,
              collection_name: str = "my_collection",
              chunk_size_words: int = 500,
              overlap_words: int = 50) -> Dict[str, Optional[str]]:
    """Extract text from a PDF, chunk, embed, and upsert into Chroma.

    Returns dict with basic provenance info including optional merkle_root.
    """
    text = extract_text_from_pdf(pdf_path)
    return _index_text(text, pdf_path, "pdf", collection_name, chunk_size_words, overlap_words)


def index_url(url: str,
              collection_name: str = "my_collection", 
              chunk_size_words: int = 500,
              overlap_words: int = 50) -> Dict[str, Optional[str]]:
    """Extract text from a protocol documentation URL, chunk, embed, and upsert into Chroma.

    Optimized for technical documentation and protocol blogs.
    Returns dict with basic provenance info including optional merkle_root.
    """
    text = extract_text_from_url(url)
    return _index_text(text, url, "url", collection_name, chunk_size_words, overlap_words)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Index PDF files or protocol documentation URLs into Chroma")
    parser.add_argument("input", help="Path to a PDF file or URL to protocol documentation")
    parser.add_argument("--collection", default="my_collection", help="Chroma collection name")
    parser.add_argument("--size", type=int, default=500, help="Chunk size in words")
    parser.add_argument("--overlap", type=int, default=50, help="Chunk overlap in words")
    args = parser.parse_args()

    if args.input.startswith(('http://', 'https://')):
        print(f"Indexing URL: {args.input}")
        result = index_url(args.input, collection_name=args.collection, chunk_size_words=args.size, overlap_words=args.overlap)
    else:
        print(f"Indexing PDF: {args.input}")
        result = index_pdf(args.input, collection_name=args.collection, chunk_size_words=args.size, overlap_words=args.overlap)
    
    print(result)




















