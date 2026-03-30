"""
Streamlit Frontend for Global Tax Analyzer Chatbot.
"""
import streamlit as st
import time
from app.frontend.api_client import TaxAPIClient

# Page Config
st.set_page_config(
    page_title="Global Tax Analyzer AI",
    page_icon="⚖️",
    layout="wide",
)

# Custom Styling (Rich Aesthetics)
st.markdown("""
<style>
    /* Styling for the chat container */
    .stChatMessage {
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }
    
    /* Elegant Dark-themed Sidebar */
    .stSidebar {
        background-color: #f7f9fc;
    }
    
    /* New Chat Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Main title styling */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        background: -webkit-linear-gradient(#2E3192, #1BFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
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

# API Client
api = TaxAPIClient(st.session_state["access_token"])

def clear_session():
    st.session_state["access_token"] = ""
    st.session_state["user_id"] = ""
    st.session_state["email"] = ""
    st.session_state["current_chat_id"] = None
    st.session_state["messages"] = []
    st.rerun()

# --- AUTHENTICATION UI ---
if not st.session_state["access_token"]:
    st.markdown("<h1 class='main-title'>Global Tax Analyzer AI</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="tax.expert@example.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In")
            if submitted:
                with st.spinner("Authenticating..."):
                    res = api.login(email, password)
                    if res and res.status_code == 200:
                        data = res.json()
                        st.session_state["access_token"] = data["access_token"]
                        st.session_state["user_id"] = data["user_id"]
                        st.session_state["email"] = data["email"]
                        st.success("Welcome back!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")

    with tab2:
        with st.form("signup_form"):
            email = st.text_input("Email", placeholder="tax.expert@example.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Create Account")
            if submitted:
                with st.spinner("Joining the platform..."):
                    res = api.signup(email, password)
                    if res and res.status_code == 200:
                        data = res.json()
                        st.session_state["access_token"] = data["access_token"]
                        st.session_state["user_id"] = data["user_id"]
                        st.session_state["email"] = data["email"]
                        st.success("Account created successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Registration failed. Please try again.")

else:
    # --- AUTHENTICATED CHAT UI ---
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"**Logged in as:** {st.session_state['email']}")
        if st.button("Logout", key="logout_btn"):
            clear_session()
            
        st.divider()
        
        # New Chat Button
        if st.button("➕ New Chat", use_container_width=True):
            new_chat = api.create_chat()
            if new_chat:
                st.session_state["current_chat_id"] = new_chat["id"]
                st.session_state["messages"] = []
                st.rerun()

        st.markdown("### 💬 Chat History")
        chats = api.list_chats()
        for chat in chats:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                if st.button(f"📄 {chat['title']}", key=f"chat_{chat['id']}", use_container_width=True):
                    st.session_state["current_chat_id"] = chat["id"]
                    st.session_state["messages"] = api.get_messages(chat["id"])
                    st.rerun()
            with col2:
                if st.button("🗑", key=f"del_{chat['id']}"):
                    api.delete_chat(chat["id"])
                    if st.session_state["current_chat_id"] == chat["id"]:
                        st.session_state["current_chat_id"] = None
                        st.session_state["messages"] = []
                    st.rerun()
        
        st.divider()
        
        # File Upload
        st.markdown("### 📁 Context Upload")
        with st.expander("Upload Tax Documents", expanded=True):
            country = st.selectbox("Select Country", ["Global", "India", "USA", "Australia", "UK", "Canada"])
            uploaded_file = st.file_uploader(
                "Drop PDF, Excel or DOCX",
                type=["pdf", "xlsx", "xls", "docx", "csv"]
            )
            if uploaded_file:
                if st.button("🚀 Index Document"):
                    with st.spinner(f"Analyzing {uploaded_file.name}..."):
                        file_bytes = uploaded_file.read()
                        res = api.upload_document(file_bytes, uploaded_file.name, country)
                        if res.get("status") == "success":
                            st.success(f"Indexed {uploaded_file.name}!")
                        else:
                            st.error(f"Failed to index: {res.get('detail', 'Unknown error')}")

    # Main Chat Area
    if st.session_state["current_chat_id"]:
        st.markdown(f"### Current Hub: Tax Analyzer ⚖️")
        
        # Display Messages
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat Input
        if prompt := st.chat_input("Ask about tax rates, policies or regulations..."):
            # 1. Show user message
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state["messages"].append({"role": "user", "content": prompt})
            
            # 2. Query Backend and Stream AI's Response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                with st.spinner("Consulting intelligence..."):
                    res = api.submit_query(st.session_state["current_chat_id"], prompt)
                    full_response = res.get("content", "Error: No response generated.")
                    
                    # Simulation of typing if needed, or direct display
                    # Since backend generation can take time, we already waited for it.
                    # We can use a small typing animation here
                    time_per_word = 0.05
                    words = full_response.split(" ")
                    typed_text = ""
                    for word in words:
                        typed_text += word + " "
                        message_placeholder.markdown(typed_text + "▌")
                        time.sleep(time_per_word)
                    message_placeholder.markdown(typed_text)
                    
            st.session_state["messages"].append({"role": "assistant", "content": full_response})
    else:
        # Welcome Screen
        st.markdown("<h1 class='main-title'>Global Tax Intelligence Center</h1>", unsafe_allow_html=True)
        st.info("👋 Select a chat from the history or start a 'New Chat' to begin.")
        
        st.markdown("""
        ### Features:
        - **Multi-Country Support**: Compare rates across jurisdictions.
        - **Document Intelligence**: Upload PDFs or Excels for specific context.
        - **Live RAG Pipeline**: Combines your data with core tax knowledge.
        - **Secure**: Personal isolation for all your uploaded tax data.
        """)
        
        # Display sample datasets/models being used
        st.caption("Powered by Hugging Face (Mistral-7B-Instruct) & Supabase.")
