"""
Hugging Face LLM Chain for RAG.
Uses the modern Hugging Face Inference API (Serverless) with the new router endpoint.
"""
import os
import requests
import json
from typing import List, Optional
from langchain_core.documents import Document
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
# Using Mistral 7B Instruct v0.3
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
# New Hugging Face Inference Endpoint (OpenAI-compatible)
API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
    "Content-Type": "application/json"
}

def get_hf_dataset_context() -> str:
    """Load sample knowledge from financial_phrasebank."""
    try:
        dataset = load_dataset("financial_phrasebank", "sentences_allagree", split="train", trust_remote_code=True)
        samples = dataset.select(range(5))
        context = "\n".join([f"- {item['sentence']}" for item in samples])
        return context
    except Exception as e:
        print(f"Error loading HF dataset: {e}")
        return "No additional financial dataset knowledge available at this time."

PROMPT_TEMPLATE = """
You are a Global Tax Intelligence Assistant.

Context:
{retrieved_chunks}

Dataset Knowledge:
{hf_dataset_context}

User Query:
{query}

Instructions:
- Answer ONLY using context + dataset
- If comparing countries, format clearly
- Extract tax rates, rules, policies
- If missing info -> say "Not found in data"
- Be structured and concise

Output Format:
- Summary
- Country-wise comparison
- Key insights
"""

def generate_response(query: str, retrieved_docs: List[Document]) -> str:
    """Query the LLM using the modern Hugging Face Inference API."""
    
    retrieved_chunks = "\n\n".join([doc.page_content for doc in retrieved_docs])
    hf_dataset_context = get_hf_dataset_context()
    
    prompt = PROMPT_TEMPLATE.format(
        retrieved_chunks=retrieved_chunks if retrieved_chunks else "No relevant document context found.",
        hf_dataset_context=hf_dataset_context,
        query=query
    )
    
    # Using the Chat Completion format for the new router
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a professional tax assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.1,
        "stream": False
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        return f"Error: Unexpected response format: {json.dumps(result)}"
        
    except Exception as e:
        # Fallback to the model-specific URL if the router is not available for this model
        # But generally, 410 Gone means we MUST use the new endpoint.
        return f"Error connecting to LLM: {str(e)}"

def generate_response_stream(query: str, retrieved_docs: List[Document]):
    """Simulate streaming for the UI."""
    full_text = generate_response(query, retrieved_docs)
    import time
    for word in full_text.split(" "):
        yield word + " "
        time.sleep(0.05)
