# ⚖️ Global Tax Analyzer AI

A production-ready, RAG-powered tax assistant designed to provide accurate, multi-country tax insights. Built with a unified Streamlit architecture, it leverages Supabase pgvector for persistent cloud storage and Hugging Face inference for high-quality LLM responses.

## 🚀 Key Features

- **Unified Cloud Architecture**: Designed to be easily deployed on Streamlit Community Cloud without needing a separate FastAPI backend.
- **Intelligent RAG Pipeline**:
  - Contextualizes responses using user-uploaded documents (PDF, Excel, DOCX).
  - Uses `mistralai/Mistral-7B-Instruct-v0.2` via the Hugging Face Serverless Inference API.
  - Leverages the Hugging Face Financial Phrasebank dataset for augmented context.
- **Robust Cloud Storage**: 
  - User Authentication, Chats, Messages, and Document storage handled cleanly by **Supabase**.
  - Document embeddings are securely stored in **Supabase pgvector**, ensuring permanent, cross-session contextual memory.
- **Responsive & Modern UI**: ChatGPT-inspired interface featuring robust chat history, dynamic file uploads, and a clean floating UI design.

## 🛠 Tech Stack

- **Frontend & App Logic**: Streamlit (via `app_cloud.py`)
- **Remote LLM Inference**: Hugging Face Hub (Mistral 7B)
- **Vector Database & Auth**: Supabase (pgvector & Storage)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`

## ☁️ Deployment to Streamlit Community Cloud

The local "Deploy" button in Streamlit can sometimes fail if it doesn't recognize your local Git tracking or Streamlit account authorization. To deploy this app seamlessly to the cloud:

1. Ensure your code is pushed to your GitHub Repository.
2. Visit [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. Click **"New app"** and select your GitHub repository.
4. Set the **Main file path** to: `app_cloud.py`
5. **CRITICAL**: Go to **Advanced Settings** -> **Secrets** and add your environment variables:
   ```toml
   HUGGINGFACE_API_TOKEN = "your_token_here"
   SUPABASE_URL = "your_supabase_url_here"
   SUPABASE_KEY = "your_supabase_key_here"
   ```
6. Click **Deploy!**

## 💻 Local Setup & Launch

### 1. Database Setup
Ensure you execute `supabase_schema.sql` in your Supabase SQL Editor. This initializes the `vector` extension and creates all required tables (`profiles`, `chats`, `messages`, `document_chunks`) alongside their security rules policies.

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
HUGGINGFACE_API_TOKEN=your_token
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
```

### 3. Installation & Local Run
Install the dependencies, and then start the Streamlit application:
```powershell
pip install -r requirements.txt
python -m streamlit run app_cloud.py
```

## 🧪 Usage Example
1. Create an account via the Sign Up screen.
2. Click **➕ New Chat** to create an isolated conversation thread.
3. Click the **📎** floating action button pinned above the chat box to upload heavy tax manuals (PDF) or financial data sheets (Excel).
4. Ask a question such as: *"Based on the uploaded Indian Tax code, what are the exact GST rate cuts for electronic goods?"*
5. The AI scans your cloud pgvector chunks and generates a precise answer!
