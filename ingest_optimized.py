import os
import glob
from supabase import create_client
from dotenv import load_dotenv
from app.utils.document_processor import process_document
from app.rag.vector_store_supabase import add_documents_to_supabase

load_dotenv()

# ──────────────────────────────────────────────
# CONFIG (Fixed credentials from bulk_ingest.py)
# ──────────────────────────────────────────────
EMAIL    = "varma32005@gmail.com"
PASSWORD = "Varma@191203"
# ──────────────────────────────────────────────

def ingest_new_only():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    sb = create_client(url, key)

    print("🔐 Signing in to Supabase...")
    try:
        res = sb.auth.sign_in_with_password({"email": EMAIL, "password": PASSWORD})
        user_id = str(res.user.id)
        sb.auth.set_session(res.session.access_token, res.session.refresh_token)
        print(f"✅ Signed in as {EMAIL}")
    except Exception as e:
        print(f"❌ Auth failed: {e}")
        return

    def save_doc(user_id, file_name, country):
        response = sb.table("documents").insert({
            "user_id": user_id,
            "file_name": file_name,
            "file_url": "local-updated",
            "file_type": "pdf",
            "country": country,
            "faiss_index_path": "supabase_pgvector",
        }).execute()
        return response.data[0] if response.data else {}

    country_map = {
        "AUSTRALIA": "Australia", "INDIA": "India", "US": "USA",
        "UK": "UK", "CANADA": "Canada", "GERMANY": "Germany", "CHINA": "China"
    }

    print("\n🚀 INGESTING UPDATED COMPREHENSIVE TAX GUIDES ONLY...")
    for folder, display_country in country_map.items():
        # ONLY INGEST THE COMPREHENSIVE FILE WE UPDATED
        file_name = f"{folder}_Tax_Comprehensive.pdf"
        file_path = os.path.join("PDF", folder, file_name)
        
        if os.path.exists(file_path):
            print(f"📄  {file_name}...")
            try:
                with open(file_path, "rb") as f:
                    file_bytes = f.read()

                # Extract + chunk
                full_text, chunks = process_document(file_bytes, file_name)
                print(f"    → {len(chunks)} chunks")

                # Save metadata
                doc_record = save_doc(user_id, file_name, display_country)

                # Embed + store
                metadata = [{"source": file_name, "country": display_country}] * len(chunks)
                add_documents_to_supabase(user_id, doc_record["id"], chunks, metadata, use_direct_db=True)
                print(f"    ✅ Indexed successfully!")

            except Exception as e:
                print(f"    ⚠️  Failed: {e}")
        else:
            print(f"❓ Skipping {file_name} (Not found)")

    print("\n🎉 Targeted ingestion complete! New calculation logic is now in pgvector.")

if __name__ == "__main__":
    ingest_new_only()
