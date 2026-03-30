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
- Carefully read any CONVERSATION HISTORY provided to understand the topic and context before answering.
- If the user's current query is short (a keyword or phrase), interpret it as a follow-up to the conversation history and give a detailed, relevant answer about that specific topic.
- Answer ONLY what the user asked. Do NOT add unrelated country comparisons unless the user explicitly asked to compare countries.
- Use the provided DOCUMENT CONTEXT as your primary source. If the document context is relevant, cite exact rates, rules, section numbers, thresholds, and policies.
- If context does not contain enough information, say: "This specific data is not available in the current knowledge base." — say this ONCE, not as a bullet filler.
- Format with markdown using headings, bullet points, and tables ONLY when they genuinely improve clarity.
- Be detailed and technically accurate: mention exact percentages, thresholds, section numbers where relevant.
- Never invent data. Never pad responses with irrelevant country comparisons or generic summaries."""

PROMPT_TEMPLATE = """DOCUMENT CONTEXT (retrieved from tax knowledge base):
---
{retrieved_chunks}
---

{history_section}
Current User Question: {query}

Answer the above question directly and precisely. If the question is a short keyword or follow-up, use the conversation history above to understand what topic is being asked about and answer it thoroughly.
- For deduction/section questions: list exact limits, conditions, eligible items.
- For rate questions: list exact percentages and thresholds.
- For procedure/how questions: give step-by-step guidance.
- Do NOT add "Country-wise Comparison" unless explicitly asked.
- Do NOT add "Summary" or "Key Insights" sections unless needed for complex multi-part answers.
"""

def generate_response(query: str, retrieved_docs: List[Document], chat_history: list = None) -> str:
    """Query the LLM. Accepts optional chat_history list of {role, content} dicts."""
    
    retrieved_chunks = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # Build history section for context on short/follow-up queries
    history_section = ""
    if chat_history:
        recent = chat_history[-6:]  # last 3 exchanges
        lines = []
        for msg in recent:
            role = "User" if msg["role"] == "user" else "Assistant"
            lines.append(f"{role}: {msg['content'][:300]}")  # truncate long msgs
        history_section = "CONVERSATION HISTORY (for context on follow-up queries):\n" + "\n".join(lines) + "\n\n"
    
    user_message = PROMPT_TEMPLATE.format(
        retrieved_chunks=retrieved_chunks if retrieved_chunks else "No relevant document context found for this query.",
        history_section=history_section,
        query=query
    )
    
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 1800,
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
        return f"Error connecting to LLM: {str(e)}"

def generate_response_stream(query: str, retrieved_docs: List[Document], chat_history: list = None):
    """Simulate streaming for the UI."""
    full_text = generate_response(query, retrieved_docs, chat_history)
    import time
    for word in full_text.split(" "):
        yield word + " "
        time.sleep(0.05)
