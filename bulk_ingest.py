import os
import glob
from supabase import create_client
from dotenv import load_dotenv
from app.utils.document_processor import process_document
from app.rag.vector_store_supabase import add_documents_to_supabase

load_dotenv()

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
EMAIL    = "varma32005@gmail.com"
PASSWORD = "Varma@191203"
# ──────────────────────────────────────────────

def bulk_ingest():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    # Create a fresh authenticated client (bypasses the unauthenticated singleton)
    sb = create_client(url, key)

    # 1. Sign in to get user_id + access token
    print("🔐 Signing in to Supabase...")
    try:
        res = sb.auth.sign_in_with_password({"email": EMAIL, "password": PASSWORD})
        user_id     = str(res.user.id)
        access_token  = res.session.access_token
        refresh_token = res.session.refresh_token
        # Attach the session so RLS accepts writes
        sb.auth.set_session(access_token, refresh_token)
        print(f"✅ Signed in as {EMAIL}  |  user_id: {user_id}")
    except Exception as e:
        print(f"❌ Auth failed: {e}")
        return

    # 2. Helper: save document metadata using the authenticated client
    def save_doc(user_id, file_name, public_url, file_type, country, index_path):
        response = sb.table("documents").insert({
            "user_id":         user_id,
            "file_name":       file_name,
            "file_url":        public_url,
            "file_type":       file_type,
            "country":         country,
            "faiss_index_path": index_path,
        }).execute()
        return response.data[0] if response.data else {}

    # 3. Helper: upload file using the authenticated client
    def upload_file(file_bytes, storage_path):
        try:
            sb.storage.from_("tax-documents").upload(storage_path, file_bytes)
        except Exception:
            pass  # already exists — continue
        return sb.storage.from_("tax-documents").get_public_url(storage_path)

    # 4. Walk through PDF directories
    pdf_root = os.path.join(os.getcwd(), "PDF")
    country_map = {
        "AUSTRALIA": "Australia",
        "INDIA":     "India",
        "US":        "USA",
        "UK":        "UK",
        "CANADA":    "Canada",
        "GERMANY":   "Germany",
        "CHINA":     "China"
    }

    for folder, display_country in country_map.items():
        files = glob.glob(os.path.join(pdf_root, folder, "*.pdf"))
        print(f"\n--- Processing {display_country} ({len(files)} files) ---")

        for file_path in files:
            file_name = os.path.basename(file_path)
            print(f"📄  {file_name}...")
            try:
                with open(file_path, "rb") as f:
                    file_bytes = f.read()

                # A. Upload to storage
                storage_path = f"{user_id}/{file_name}"
                public_url   = upload_file(file_bytes, storage_path)

                # B. Extract + chunk
                full_text, chunks = process_document(file_bytes, file_name)
                print(f"    → {len(chunks)} chunks")

                # C. Save metadata (authenticated)
                doc_record = save_doc(
                    user_id, file_name, public_url, "pdf",
                    display_country, "supabase_pgvector"
                )

                # D. Embed + store in pgvector
                metadata = [{"source": file_name, "country": display_country}] * len(chunks)
                add_documents_to_supabase(user_id, doc_record["id"], chunks, metadata, use_direct_db=True)

                print(f"    ✅ Indexed successfully!")

            except Exception as e:
                print(f"    ⚠️  Failed: {e}")

    print("\n🎉 Bulk ingestion complete! All PDFs are now in pgvector.")


if __name__ == "__main__":
    bulk_ingest()
