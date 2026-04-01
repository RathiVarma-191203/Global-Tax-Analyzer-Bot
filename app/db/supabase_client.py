"""
Supabase client initialization and helper functions.
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client() -> Client:
    """Return authenticated Supabase client."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# Singleton client
supabase: Client = get_supabase_client()


# ---- Chat helpers ------------------------------------------------

def create_chat(user_id: str, title: str = "New Chat") -> dict:
    response = supabase.table("chats").insert({
        "user_id": user_id,
        "title": title
    }).execute()
    return response.data[0] if response.data else {}


def get_chats(user_id: str) -> list:
    """Fetches chats with a retry mechanism for transient SSL/Connection errors."""
    import time
    for attempt in range(3):
        try:
            response = (
                supabase.table("chats")
                .select("*")
                .eq("user_id", user_id)
                .order("updated_at", desc=True)
                .execute()
            )
            return response.data or []
        except Exception as e:
            if attempt == 2:
                # If it still fails, raise it
                raise e
            time.sleep(1) # Wait briefly before retrying
    return []


def delete_chat(chat_id: str) -> bool:
    supabase.table("chats").delete().eq("id", chat_id).execute()
    return True


def update_chat_title(chat_id: str, title: str) -> dict:
    response = (
        supabase.table("chats")
        .update({"title": title, "updated_at": "now()"})
        .eq("id", chat_id)
        .execute()
    )
    return response.data[0] if response.data else {}


# ---- Message helpers ------------------------------------------------

def save_message(chat_id: str, role: str, content: str) -> dict:
    response = supabase.table("messages").insert({
        "chat_id": chat_id,
        "role": role,
        "content": content
    }).execute()
    return response.data[0] if response.data else {}


def get_messages(chat_id: str) -> list:
    response = (
        supabase.table("messages")
        .select("*")
        .eq("chat_id", chat_id)
        .order("timestamp", desc=False)
        .execute()
    )
    return response.data or []


# ---- Document helpers -----------------------------------------------

def save_document_metadata(user_id: str, file_name: str, file_url: str,
                            file_type: str, country: str, faiss_index_path: str) -> dict:
    response = supabase.table("documents").insert({
        "user_id": user_id,
        "file_name": file_name,
        "file_url": file_url,
        "file_type": file_type,
        "country": country,
        "faiss_index_path": faiss_index_path
    }).execute()
    return response.data[0] if response.data else {}


def get_user_documents(user_id: str) -> list:
    response = (
        supabase.table("documents")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data or []


def upload_file_to_storage(file_bytes: bytes, bucket_path: str) -> str:
    """Upload a file to Supabase Storage and return its URL."""
    response = supabase.storage.from_("tax-documents").upload(bucket_path, file_bytes)
    public_url = supabase.storage.from_("tax-documents").get_public_url(bucket_path)
    return public_url
