## ☁️ Cloud Deployment

For deploying to a public URL (e.g. Streamlit Community Cloud), use the **`app_cloud.py`** entry point. This version is optimized for single-service cloud hosting and uses **Supabase pgvector** for permanent context storage.

### 1. Unified App Architecture
- Entry point: `app_cloud.py`
- Stores embeddings in Supabase (pgvector), not local files.
- Includes integrated auth and RAG logic.

### 2. Environment Variables (Required in Cloud)
Set these in your deployment dashboard:
- `HUGGINGFACE_API_TOKEN`
- `SUPABASE_URL`
- `SUPABASE_KEY`

### 3. Database Migration (pgvector)
Before deploying, execute the updated **`supabase_schema.sql`** in your Supabase SQL Editor to enable the `vector` extension and the `document_chunks` table.

## 🛠 Setup & Launch

... [previous setup manual steps]

## 🚀 Key Features

- **Intuitive UI**: Clean, ChatGPT-inspired interface with history, new chat, and file uploads.
- **Advanced RAG Pipeline**: 
  - Retrieves top-k relevant chunks from user-uploaded context.
  - Augments responses using Hugging Face dataset knowledge (Financial Phrasebank).
  - Uses `mistralai/Mistral-7B-Instruct-v0.2` via Hugging Face Inference API.
- **Secure File Processing**: Supports PDF, Excel, and DOCX indexing.
- **User Isolation**: Separate FAISS indexes and Supabase storage per user.
- **History & Persistence**: All conversations and documents are stored securely in Supabase.

## 📁 System Architecture

- **Frontend**: Streamlit
- **Backend API**: FastAPI
- **PostgreSQL/Auth/Storage**: Supabase
- **Vector Database**: FAISS (local)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`

## 🛠 Setup & Launch

### 1. Configure Supabase
Ensure you have run the `supabase_schema.sql` within your Supabase SQL Editor. This sets up required tables (`profiles`, `chats`, `messages`, `documents`) and RLS policies.

### 2. Environment Variables
Rename `.env.example` to `.env` and fill in your actual credentials:
- `HUGGINGFACE_API_TOKEN`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_DB_URL`

### 3. Installation
```powershell
pip install -r requirements.txt
```

### 4. Running the Application
Use the provided `run.py` utility to launch both the Backend and Frontend concurrently:
```powershell
python run.py
```

Otherwise, run manually:
```powershell
# Terminal 1: Backend
uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend
streamlit run app/frontend/app.py
```

## 🧪 Example Usage
1. Sign up/Log in.
2. Start a **New Chat**.
3. Upload a tax PDF from India and an Excel sheet from Australia in the sidebar.
4. Ask: "Compare the corporate tax rates and key filing deadlines for India and Australia."
5. The chatbot will provide a structured summary including the comparison and key insights.
