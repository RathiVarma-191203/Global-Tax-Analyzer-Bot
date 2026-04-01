import os
import streamlit as st
from app.db.supabase_client import supabase, save_document_metadata
from app.utils.document_processor import process_document
from app.rag.vector_store_supabase import add_documents_to_supabase

USER_ID = "d78fd600-e3ae-4884-8a61-d1d314f6d35f" # From previous logs
PDF_PATH = os.path.join("PDF", "INDIA", "INDIA_Tax_Comprehensive.pdf")

if os.path.exists(PDF_PATH):
    print(f"📄 Processing {PDF_PATH}...")
    with open(PDF_PATH, "rb") as f:
        file_bytes = f.read()
        full_text, chunks = process_document(file_bytes, "INDIA_Tax_Comprehensive.pdf")
        doc_record = save_document_metadata(
            USER_ID, "INDIA_Tax_Comprehensive.pdf",
            "local", "pdf", "India", "supabase_pgvector"
        )
        metadata = [{"source": "INDIA_Tax_Comprehensive.pdf", "country": "India"}] * len(chunks)
        add_documents_to_supabase(USER_ID, doc_record["id"], chunks, metadata)
        print("✅ India Tax Comprehensive Indexed successfully!")
else:
    print(f"❌ File not found: {PDF_PATH}")
