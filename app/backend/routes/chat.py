"""
Chat routes for conversation management.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.auth.router import get_current_user
from app.db.supabase_client import (
    create_chat, get_chats, get_messages, 
    save_message, delete_chat, update_chat_title
)
from app.rag.vector_store import search_index
from app.rag.llm_chain import generate_response

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatCreate(BaseModel):
    title: str = "New Chat"

class MessageCreate(BaseModel):
    chat_id: str
    content: str

class ChatResponse(BaseModel):
    id: str
    title: str
    created_at: str

@router.post("/", response_model=ChatResponse)
async def start_chat(chat_data: ChatCreate, user: dict = Depends(get_current_user)):
    """Start a new chat session."""
    try:
        chat = create_chat(user["id"], chat_data.title)
        return chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat: {str(e)}")

@router.get("/", response_model=List[ChatResponse])
async def list_chats(user: dict = Depends(get_current_user)):
    """List all chats for the current user."""
    return get_chats(user["id"])

@router.get("/{chat_id}/messages")
async def list_messages(chat_id: str, user: dict = Depends(get_current_user)):
    """Fetch all messages for a specific chat."""
    # Note: RLS handles verification that user owns chat
    return get_messages(chat_id)

@router.post("/query")
async def submit_query(msg: MessageCreate, user: dict = Depends(get_current_user)):
    """Submit a query to the chat and get a RAG response."""
    # 1. Save user msg
    save_message(msg.chat_id, "user", msg.content)

    # 2. RAG retrieve
    retrieved_docs = search_index(user["id"], msg.content, top_k=5)

    # 3. Generate response
    ai_content = generate_response(msg.content, retrieved_docs)

    # 4. Save AI Response
    save_message(msg.chat_id, "assistant", ai_content)
    
    # 5. Optionally Update Chat Title if it's default
    # (Bonus: Auto-generate title could go here)

    return {"role": "assistant", "content": ai_content}

@router.delete("/{chat_id}")
async def remove_chat(chat_id: str, user: dict = Depends(get_current_user)):
    """Delete a chat session."""
    delete_chat(chat_id)
    return {"status": "success"}
