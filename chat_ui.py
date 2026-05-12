import streamlit as st
import requests
from datetime import datetime

# ==========================================
# CONFIG
# ==========================================

API_URL = "https://web-production-71a2e.up.railway.app"

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #0b1120;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #0f172a);
    border-right: 1px solid #1e293b;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

.chat-container {
    max-width: 900px;
    margin: auto;
}

.user-msg {
    background: #2563eb;
    color: white;
    padding: 14px;
    border-radius: 15px 15px 0px 15px;
    margin-bottom: 10px;
    margin-left: 20%;
    font-size: 16px;
}

.bot-msg {
    background: #111827;
    color: white;
    padding: 14px;
    border-radius: 15px 15px 15px 0px;
    margin-bottom: 15px;
    margin-right: 20%;
    border: 1px solid #1f2937;
    font-size: 16px;
}

.title {
    font-size: 42px;
    font-weight: bold;
    color: white;
}

.subtitle {
    color: #94a3b8;
    margin-bottom: 30px;
}

.stTextInput > div > div > input {
    background-color: #111827;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## ⚙️ Control Panel")

    st.divider()

    st.markdown("### 📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        with st.spinner("Uploading PDF..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            try:
                response = requests.post(
                    f"{API_URL}/upload-pdf",
                    files=files
                )

                if response.status_code == 200:
                    st.success("PDF uploaded successfully!")

                else:
                    st.error("Failed to upload PDF")

            except Exception as e:
                st.error(f"Upload Error: {e}")

    st.divider()

    st.markdown("### 🧹 Conversation")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("""
    ### 🚀 Features

    - Smart AI + RAG
    - PDF Chat
    - Conversation Memory
    - Groq LLM
    - Railway Backend
    - FastAPI Integration
    """)

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="chat-container">
    <div class="title">🤖 AI Assistant</div>
    <div class="subtitle">
        Chat with PDFs and ask general AI questions naturally.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# DISPLAY CHAT
# ==========================================

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(
            f"""
            <div class="chat-container">
                <div class="user-msg">
                    {msg["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="chat-container">
                <div class="bot-msg">
                    {msg["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================
# USER INPUT
# ==========================================

prompt = st.chat_input("Message Enterprise AI Assistant...")

if prompt:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Show user message
    st.markdown(
        f"""
        <div class="chat-container">
            <div class="user-msg">
                {prompt}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Generate AI response
    with st.spinner("Thinking..."):

        try:

            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "question": prompt
                }
            )

            if response.status_code == 200:

                data = response.json()

                answer = data.get(
                    "answer",
                    "No response generated."
                )

            else:

                answer = f"API Error: {response.status_code}"

        except Exception as e:

            answer = f"Connection Error: {str(e)}"

    # Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # Display assistant response
    st.markdown(
        f"""
        <div class="chat-container">
            <div class="bot-msg">
                {answer}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )