"""
Unified Streamlit App for Cloud Deployment (e.g. Streamlit Community Cloud).
Combines Business Logic and RAG to avoid a separate FastAPI backend.
Uses Supabase pgvector for cloud persistence.
"""
import streamlit as st
import time
import os
from dotenv import load_dotenv

# Import our custom modules (ensure they are in the path)
from app.db.supabase_client import (
    supabase, create_chat, get_chats, get_messages, 
    save_message, delete_chat, update_chat_title,
    upload_file_to_storage, save_document_metadata
)
from app.utils.document_processor import process_document
from app.rag.vector_store_supabase import add_documents_to_supabase, search_supabase_index
from app.rag.llm_chain import generate_response

load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="Tax Analyzer AI",
    page_icon="⚖️",
    layout="wide",
)

# --- Theming/Styling ---
st.markdown("""
<style>
    .stChatMessage { border-radius: 12px; padding: 15px; margin-bottom: 10px; }
    section[data-testid="stSidebar"] {
        background-color: #1a1c24 !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 { color: #4facfe !important; }
    section[data-testid="stSidebar"] .stMarkdown p { color: #e2e8f0 !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        background: -webkit-linear-gradient(#2E3192, #1BFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    /* Push content above the pinned chat bar */
    .main .block-container { padding-bottom: 5rem !important; }

    /* ── Paperclip: float it INSIDE the chat input bar ── */
    /* Streamlit chat input container sits at fixed bottom */
    .stChatInputContainer {
        position: relative !important;
    }
    /* Position the popover containing the paperclip to float inside chat input */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 1.5rem !important;
        /* Align it exactly at the left edge of the chat input area */
        left: 50%;
        transform: translateX(-340px);
        z-index: 10001;
        display: flex;
        align-items: center;
        width: auto !important;
    }
    /* Make the chat input text area start further right so it doesn't overlap the paperclip */
    .stChatInputContainer textarea {
        padding-left: 3.5rem !important;
    }
    /* The popover trigger button — minimal icon style */
    div[data-testid="stPopover"] > button {
        background: transparent !important;
        border: none !important;
        font-size: 1.3rem !important;
        padding: 0.3rem !important;
        cursor: pointer !important;
        color: #a0aec0 !important;
        border-radius: 6px !important;
        width: 2.5rem !important;
        height: 2.5rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: color 0.15s, background 0.15s !important;
    }
    div[data-testid="stPopover"] > button:hover {
        color: #4facfe !important;
        background: rgba(79,172,254,0.1) !important;
    }
    /* Hide the dropdown arrow from the button */
    div[data-testid="stPopover"] > button span[data-testid="stIconMaterial"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "access_token" not in st.session_state:
    st.session_state["access_token"] = ""
if "user_id" not in st.session_state:
    st.session_state["user_id"] = ""
if "email" not in st.session_state:
    st.session_state["email"] = ""
if "current_chat_id" not in st.session_state:
    st.session_state["current_chat_id"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

def clear_session():
    for key in ["access_token", "user_id", "email", "current_chat_id", "messages"]:
        st.session_state[key] = "" if key != "messages" else []
    st.rerun()

# --- AUTH UI ---
if not st.session_state["access_token"]:
    st.markdown("<h1 class='main-title'>Global Tax Analyzer AI</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state["access_token"] = res.session.access_token
                    st.session_state["user_id"] = str(res.user.id)
                    st.session_state["email"] = res.user.email
                    st.success("Welcome back!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")

    with tab2:
        with st.form("signup_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Create Account"):
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    if res.user:
                        st.success("Check your email for confirmation!")
                        # If email confirmation is off, we can auto-login or redirect
                        if res.session:
                            st.session_state["access_token"] = res.session.access_token
                            st.session_state["user_id"] = str(res.user.id)
                            st.session_state["email"] = res.user.email
                            st.rerun()
                except Exception as e:
                    st.error(f"Signup failed: {str(e)}")

else:
    # --- APP UI ---
    
    def render_context_hub_icon():
        """Renders the Context Hub as a fixed-position 📎 paperclip icon at bottom-right."""
        with st.popover("📎"):
            st.markdown("#### 📁 Context Hub (Cloud Persistent)")
            country = st.selectbox("Country Context", [
                "Global", "Australia", "India", "USA", "UK", "Canada", "Germany", "China"
            ], key="ctx_country")
            uploaded_file = st.file_uploader(
                "Upload PDF / Excel / DOCX",
                type=["pdf", "xlsx", "xls", "docx", "csv"],
                key="ctx_uploader"
            )
            if uploaded_file:
                if st.button("🚀 Index to Cloud", key="ctx_index_btn"):
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        try:
                            file_bytes = uploaded_file.read()
                            storage_path = f"{st.session_state['user_id']}/{uploaded_file.name}"
                            public_url = upload_file_to_storage(file_bytes, storage_path)
                            full_text, chunks = process_document(file_bytes, uploaded_file.name)
                            doc_record = save_document_metadata(
                                st.session_state['user_id'], uploaded_file.name,
                                public_url, uploaded_file.name.split('.')[-1], country, "supabase_pgvector"
                            )
                            metadata = [{"source": uploaded_file.name, "country": country}] * len(chunks)
                            add_documents_to_supabase(
                                st.session_state['user_id'], doc_record["id"], chunks, metadata
                            )
                            st.success("✅ Indexed successfully!")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")


    # Sidebar
    with st.sidebar:
        st.markdown(f"**🛡️ User:** {st.session_state['email']}")
        if st.button("Logout"):
            clear_session()
        st.divider()
        
        # New Chat
        if st.button("➕ New Chat"):
            chat = create_chat(st.session_state["user_id"])
            if chat:
                st.session_state["current_chat_id"] = chat["id"]
                st.session_state["messages"] = []
                st.rerun()

        # Chat History
        st.markdown("### 💬 Your Chats")
        chats = get_chats(st.session_state["user_id"])
        for chat in chats:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                if st.button(f"📄 {chat['title']}", key=f"chat_{chat['id']}", use_container_width=True):
                    st.session_state["current_chat_id"] = chat["id"]
                    st.session_state["messages"] = get_messages(chat["id"])
                    st.rerun()
            with col2:
                if st.button("🗑", key=f"del_{chat['id']}"):
                    delete_chat(chat["id"])
                    if st.session_state["current_chat_id"] == chat["id"]:
                        st.session_state["current_chat_id"] = None
                        st.session_state["messages"] = []
                    st.rerun()
        
        st.divider()
        st.divider()

    # Main Chat Area
    if st.session_state["current_chat_id"]:
        st.markdown(f"### Tax Intellectual Core ⚖️")
        
        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        # st.chat_input at top level = auto sticks to bottom of page
        prompt = st.chat_input("Ask a tax question...")
        
        # Paperclip rendered via fixed CSS anchor — always at bottom right
        render_context_hub_icon()
        
        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state["messages"].append({"role": "user", "content": prompt})
            
            # Save message to DB
            save_message(st.session_state["current_chat_id"], "user", prompt)
            
            # Auto-name the chat on the first user message
            if len(st.session_state["messages"]) == 1:
                auto_title = prompt[:45] + "..." if len(prompt) > 45 else prompt
                try:
                    update_chat_title(st.session_state["current_chat_id"], auto_title)
                except Exception:
                    pass

            with st.chat_message("assistant"):
                placeholder = st.empty()
                with st.spinner("Searching cloud context and datasets..."):
                    # Search pgvector index
                    retrieved_docs = search_supabase_index(st.session_state["user_id"], prompt, top_k=8)
                    # Generate with LLM — pass chat history for follow-up query context
                    full_response = generate_response(
                        prompt, retrieved_docs,
                        chat_history=st.session_state["messages"]
                    )
                    
                    # Typing Animation
                    typed = ""
                    for word in full_response.split(" "):
                        typed += word + " "
                        placeholder.markdown(typed + "▌")
                        time.sleep(0.04)
                    placeholder.markdown(typed)
                    
                    # Save assistant message
                    save_message(st.session_state["current_chat_id"], "assistant", full_response)
                    st.session_state["messages"].append({"role": "assistant", "content": full_response})
    else:
        st.markdown("<h1 class='main-title'>Global Tax AI Hub</h1>", unsafe_allow_html=True)
        st.info("👋 Select or create a chat to begin. Your uploaded documents are permanently indexed in Supabase pgvector.")
        render_context_hub_icon()
        st.markdown("""
        **System Specs:**
        - **LLM**: Mistral-7B-Instruct (Cloud)
        - **Vector DB**: Supabase pgvector (Permanent)
        - **Datasets**: HF Financial Phrasebank
        """)
