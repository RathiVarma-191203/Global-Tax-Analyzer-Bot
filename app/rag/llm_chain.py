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

SYSTEM_PROMPT = """You are a precise and expert Global Tax Intelligence Assistant.
Your job is to answer the user's specific tax question accurately and concisely.
Rules:
- Answer ONLY what the user asked. Do NOT add unrelated country comparisons unless the user explicitly asked to compare countries.
- Use the provided context as your primary source.
- If context has the answer, cite specific rates, rules, sections, or policies from it.
- If context does not contain enough information, say clearly: "This specific data is not available in the current knowledge base."
- Do not pad responses with generic summaries or repetitive key insights.
- Format with markdown: use headings, bullet points, and tables ONLY when they genuinely improve clarity for the specific question.
- Be detailed and technically accurate (mention exact percentages, thresholds, section numbers where relevant).
- Never invent data. Never say "Not found in data" as a bullet point filler — only say it once if truly nothing is relevant."""

PROMPT_TEMPLATE = """Relevant context retrieved from tax documents:
---
{retrieved_chunks}
---

User Question: {query}

Answer the above question directly and precisely using only the context provided above. Structure your response to match the nature of the question:
- For "what is" questions: give a clear, direct definition with relevant specifics.
- For rate/percentage questions: list exact rates, thresholds, and any conditions.
- For "how" or procedure questions: give step-by-step guidance.
- For comparison questions (only if explicitly asked): use a table.
- Do NOT add a "Country-wise Comparison" section unless the question explicitly asks to compare countries.
- Do NOT add a generic "Summary" or "Key Insights" section unless required by the question's complexity.
"""

def generate_response(query: str, retrieved_docs: List[Document]) -> str:
    """Query the LLM using the modern Hugging Face Inference API."""
    
    retrieved_chunks = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    user_message = PROMPT_TEMPLATE.format(
        retrieved_chunks=retrieved_chunks if retrieved_chunks else "No relevant document context found for this query.",
        query=query
    )
    
    # Using the Chat Completion format for the new router
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 1500,
        "temperature": 0.05,
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
