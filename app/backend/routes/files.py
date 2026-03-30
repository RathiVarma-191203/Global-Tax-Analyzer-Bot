"""
File upload and indexing routes.
"""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from app.auth.router import get_current_user
from app.utils.document_processor import process_document
from app.db.supabase_client import upload_file_to_storage, save_document_metadata
from app.rag.vector_store import create_or_update_index
import os

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    country: str = Form("Global"),
    user: dict = Depends(get_current_user)
):
    """
    Handle document upload, extract text, chunk, embed into FAISS,
    and update Supabase storage and database.
    """
    try:
        # 1. Read file bytes
        file_bytes = await file.read()
        filename = file.filename
        
        # 2. Upload to Supabase Storage
        # Structure storage with user_id for isolation
        storage_path = f"{user['id']}/{filename}"
        public_url = upload_file_to_storage(file_bytes, storage_path)
        
        # 3. Process Document (Extract + Chunk)
        full_text, chunks = process_document(file_bytes, filename)
        
        # 4. Generate Embeddings and Save to FAISS index
        # We index chunks with the filename and country as metadata
        metadata = [{"source": filename, "country": country}] * len(chunks)
        index_path = create_or_update_index(user["id"], chunks, metadata)
        
        # 5. Save Document Metadata to Database
        file_type = filename.split(".")[-1] if "." in filename else "unknown"
        doc_record = save_document_metadata(
            user_id=user["id"],
            file_name=filename,
            file_url=public_url,
            file_type=file_type,
            country=country,
            faiss_index_path=index_path
        )
        
        return {
            "status": "success",
            "message": f"Successfully indexed {filename}",
            "doc_id": doc_record.get("id")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing file: {str(e)}")

@router.get("/")
async def list_user_documents(user: dict = Depends(get_current_user)):
    """Return all document metadata for the current user."""
    from app.db.supabase_client import get_user_documents
    return get_user_documents(user["id"])
