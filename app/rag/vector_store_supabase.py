"""
Supabase Vector Store management — cloud-persistent storage using pgvector.
"""
import os
from typing import List, Optional, Dict, Any
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.documents import Document
from app.rag.embeddings import get_embeddings
from app.db.supabase_client import supabase
from dotenv import load_dotenv

load_dotenv()

def _insert_chunks_direct(user_id: str, document_id: str, chunks: List[str], metadatas: List[Dict[Any, Any]], embeddings_model):
    """
    Insert chunks directly via psycopg2, bypassing Supabase RLS.
    Used by bulk_ingest.py to avoid auth issues.
    """
    import psycopg2
    import json
    from psycopg2.extras import execute_batch
    
    conn = psycopg2.connect(
        host="aws-1-ap-northeast-1.pooler.supabase.com",
        port=6543,
        dbname="postgres",
        user="postgres.uthyxhcovkcfkjtsyxoc",
        password="Varma@191203",
        sslmode="require"
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    batch = []
    for i in range(0, len(chunks), 50):
        batch_chunks = chunks[i:i+50]
        batch_meta = metadatas[i:i+50]
        vectors = embeddings_model.embed_documents(batch_chunks)
        for text, meta, vec in zip(batch_chunks, batch_meta, vectors):
            batch.append((
                str(document_id), str(user_id), text,
                json.dumps({**meta, "user_id": user_id, "document_id": str(document_id)}),
                vec
            ))
    
    execute_batch(cur, """
        INSERT INTO public.document_chunks (document_id, user_id, content, metadata, embedding)
        VALUES (%s, %s, %s, %s::jsonb, %s::vector)
    """, batch, page_size=100)
    cur.close()
    conn.close()
    return True


def add_documents_to_supabase(user_id: str, document_id: str, chunks: List[str], metadatas: List[Dict[Any, Any]], sb_client=None, use_direct_db: bool = False):
    """
    Split chunks and add them to the Supabase pgvector store.
    use_direct_db=True bypasses RLS via direct psycopg2 (for bulk ingestion).
    """
    embeddings = get_embeddings()
    client = sb_client if sb_client is not None else supabase
    
    for meta in metadatas:
        meta["user_id"] = user_id
        meta["document_id"] = document_id
    
    if use_direct_db:
        return _insert_chunks_direct(user_id, document_id, chunks, metadatas, embeddings)
    
    vector_store = SupabaseVectorStore(
        client=client,
        embedding=embeddings,
        table_name="document_chunks",
        query_name="match_document_chunks",
    )
    
    vector_store.add_texts(texts=chunks, metadatas=metadatas)
    return True

def search_supabase_index(user_id: str, query: str, top_k: int = 5) -> List[Document]:
    """
    Search the Supabase pgvector store for the given user.
    """
    embeddings = get_embeddings()
    
    vector_store = SupabaseVectorStore(
        client=supabase,
        embedding=embeddings,
        table_name="document_chunks",
        query_name="match_document_chunks",
    )
    
    # We use the search function with a filter for the user_id
    # Note: match_document_chunks function in SQL already filters by p_user_id
    # but LangChain's similarity_search usually expects metadata filters if available.
    
    # Using the RPC call directly via the vector store or the client
    # actually match_document_chunks is the RPC query_name here.
    
    # We'll use the similarity_search with the user_id as a parameter to the query
    # Since match_document_chunks takes p_user_id, we pass it in the search.
    
    # Re-implementing search to ensures we pass p_user_id correctly to the RPC
    # The LangChain SupabaseVectorStore standard similarity_search doesn't always 
    # map extra params to custom query_names easily if they deviate from 'match_documents'
    
    # Alternative: Direct RPC call for maximum control
    query_embedding = embeddings.embed_query(query)
    
    try:
        res = supabase.rpc(
            "match_document_chunks",
            {
                "query_embedding": query_embedding,
                "match_threshold": 0.35,
                "match_count": top_k,
                "p_user_id": user_id
            }
        ).execute()
        
        docs = []
        for row in res.data:
            docs.append(Document(
                page_content=row["content"],
                metadata=row["metadata"]
            ))
        return docs
    except Exception as e:
        print(f"Error searching Supabase index: {e}")
        return []

def delete_user_data_from_supabase(user_id: str):
    """
    Delete all vector data for a user.
    """
    supabase.table("document_chunks").delete().eq("user_id", user_id).execute()
    return True
