"""
FAISS vector store management — per-user index isolation.
"""
import os
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from app.rag.embeddings import get_embeddings
from dotenv import load_dotenv

load_dotenv()

FAISS_INDEX_DIR = os.getenv("FAISS_INDEX_DIR", "faiss_indexes")


def _get_user_index_path(user_id: str) -> str:
    """Return the filesystem path for a user's FAISS index."""
    os.makedirs(FAISS_INDEX_DIR, exist_ok=True)
    return os.path.join(FAISS_INDEX_DIR, f"user_{user_id}")


def create_or_update_index(user_id: str, chunks: List[str],
                           metadata: Optional[List[dict]] = None) -> str:
    """
    Create a new FAISS index or merge new chunks into an existing one.
    Returns the index path.
    """
    embeddings = get_embeddings()
    index_path = _get_user_index_path(user_id)

    # Build Document objects with optional metadata
    if metadata is None:
        metadata = [{}] * len(chunks)
    docs = [Document(page_content=c, metadata=m) for c, m in zip(chunks, metadata)]

    if os.path.exists(index_path):
        # Load existing and merge
        existing_store = FAISS.load_local(
            index_path, embeddings, allow_dangerous_deserialization=True
        )
        new_store = FAISS.from_documents(docs, embeddings)
        existing_store.merge_from(new_store)
        existing_store.save_local(index_path)
    else:
        store = FAISS.from_documents(docs, embeddings)
        store.save_local(index_path)

    return index_path


def search_index(user_id: str, query: str, top_k: int = 5) -> List[Document]:
    """Search a user's FAISS index and return the top-k relevant chunks."""
    embeddings = get_embeddings()
    index_path = _get_user_index_path(user_id)

    if not os.path.exists(index_path):
        return []

    store = FAISS.load_local(
        index_path, embeddings, allow_dangerous_deserialization=True
    )
    results = store.similarity_search(query, k=top_k)
    return results


def delete_user_index(user_id: str) -> bool:
    """Delete a user's entire FAISS index."""
    import shutil
    index_path = _get_user_index_path(user_id)
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
        return True
    return False
