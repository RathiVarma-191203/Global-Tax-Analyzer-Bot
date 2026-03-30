"""
Hugging Face LLM Chain for RAG.
Connects with Hugging Face Inference API and uses a specific prompt template.
"""
import os
import requests
from typing import List, Optional
from langchain_core.documents import Document
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
# Using Mistral 7B Instruct as requested
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# Load a small portion of financial dataset for "Dataset Knowledge"
# In a real app, this might be pre-indexed, but here we'll use a sample
def get_hf_dataset_context() -> str:
    """Load sample knowledge from financial_phrasebank or similar."""
    try:
        # Loading a small subset of financial_phrasebank for "base knowledge"
        dataset = load_dataset("financial_phrasebank", "sentences_allagree", split="train", trust_remote_code=True)
        # Take first 5 sentences as sample context
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
    """Query the LLM using the retrieved context and user query."""
    
    retrieved_chunks = "\n\n".join([doc.page_content for doc in retrieved_docs])
    hf_dataset_context = get_hf_dataset_context()
    
    prompt = PROMPT_TEMPLATE.format(
        retrieved_chunks=retrieved_chunks if retrieved_chunks else "No relevant document context found.",
        hf_dataset_context=hf_dataset_context,
        query=query
    )
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1000,
            "temperature": 0.1,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "Error: No text generated.")
        return str(result)
        
    except Exception as e:
        return f"Error connecting to LLM: {str(e)}"

# For streaming effect in UI
def generate_response_stream(query: str, retrieved_docs: List[Document]):
    """Simulate streaming for the UI (Hugging Face Inference API doesn't support easy streaming in all configurations)."""
    full_text = generate_response(query, retrieved_docs)
    # We yield words to simulate the effect
    import time
    for word in full_text.split(" "):
        yield word + " "
        time.sleep(0.05)
