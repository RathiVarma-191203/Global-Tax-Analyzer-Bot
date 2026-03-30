"""
API Client for the Streamlit frontend.
Handles communication with the FastAPI backend.
"""
import httpx
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

class TaxAPIClient:
    def __init__(self, auth_token: str = None):
        self.auth_token = auth_token or st.session_state.get("access_token", "")
        self.headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}

    def login(self, email, password):
        """User login."""
        try:
            response = httpx.post(f"{BACKEND_URL}/auth/login", json={"email": email, "password": password})
            return response
        except Exception as e:
            return None

    def signup(self, email, password):
        """User signup."""
        try:
            response = httpx.post(f"{BACKEND_URL}/auth/signup", json={"email": email, "password": password})
            return response
        except Exception as e:
            return None

    def list_chats(self):
        """Fetch user chats."""
        try:
            response = httpx.get(f"{BACKEND_URL}/chat/", headers=self.headers)
            return response.json() if response.status_code == 200 else []
        except:
            return []

    def create_chat(self, title="New Chat"):
        """Create a new chat session."""
        try:
            response = httpx.post(f"{BACKEND_URL}/chat/", headers=self.headers, json={"title": title})
            return response.json() if response.status_code == 200 else None
        except:
            return None

    def get_messages(self, chat_id):
        """Fetch chat history."""
        try:
            response = httpx.get(f"{BACKEND_URL}/chat/{chat_id}/messages", headers=self.headers)
            return response.json() if response.status_code == 200 else []
        except:
            return []

    def submit_query(self, chat_id, content):
        """Submit a query to the chat."""
        try:
            response = httpx.post(
                f"{BACKEND_URL}/chat/query",
                headers=self.headers,
                json={"chat_id": chat_id, "content": content},
                timeout=60.0 # LLM generation can take time
            )
            return response.json() if response.status_code == 200 else {"content": "Error: Could not reach assistant."}
        except Exception as e:
            return {"content": f"Error: {str(e)}"}

    def upload_document(self, file_bytes, filename, country="Global"):
        """Upload a tax document to the backend."""
        try:
            files = {"file": (filename, file_bytes)}
            data = {"country": country}
            response = httpx.post(
                f"{BACKEND_URL}/files/upload",
                headers=self.headers,
                files=files,
                data=data,
                timeout=120.0
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "detail": str(e)}

    def delete_chat(self, chat_id):
        """Delete a chat session."""
        try:
            response = httpx.delete(f"{BACKEND_URL}/chat/{chat_id}", headers=self.headers)
            return response.status_code == 200
        except:
            return False
