import streamlit as st
import requests
import time


# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(

    page_title="AI Assistant",

    page_icon="🤖",

    layout="wide",

    initial_sidebar_state="expanded"
)


# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #0f172a;
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }

    /* Chat messages */
    .stChatMessage {
        padding: 1rem;
        border-radius: 14px;
        margin-bottom: 1rem;
    }

    /* User bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background-color: #1e293b;
    }

    /* Assistant bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        background-color: #172554;
    }

    /* Title */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: white;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .sub-title {
        color: #94a3b8;
        font-size: 17px;
        margin-bottom: 30px;
    }

    /* Divider */
    hr {
        border: 1px solid #1f2937;
    }

    /* Buttons */
    .stButton button {
        width: 100%;
        border-radius: 10px;
        background-color: #2563eb;
        color: white;
        border: none;
    }

    .stButton button:hover {
        background-color: #1d4ed8;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:

    st.markdown("## ⚙️ Control Panel")

    st.markdown("---")


    # Upload PDF
    st.markdown("### 📄 Upload PDF")


    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )


    if uploaded_file:

        with st.spinner("Processing PDF..."):

            files = {

                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }


            response = requests.post(

                "http://127.0.0.1:8000/upload-pdf",

                files=files
            )


            if response.status_code == 200:

                st.success(
                    "PDF uploaded successfully"
                )

            else:

                st.error(
                    "Upload failed"
                )


    st.markdown("---")


    # Clear Memory
    st.markdown("### 🧹 Conversation")


    if st.button("Clear Conversation"):

        requests.post(
            "http://127.0.0.1:8000/clear-memory"
        )


        st.session_state.messages = []


        st.rerun()


    st.markdown("---")


    # Features
    st.markdown("### 🚀 Features")

    st.markdown("""
    - Smart AI + RAG
    - PDF Chat
    - Conversation Memory
    - Guardrails
    - Hallucination Detection
    - Faithfulness Evaluation
    """)


# --------------------------------
# HEADER
# --------------------------------

st.markdown(
    """
    <div class="main-title">
        🤖 AI Assistant
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="sub-title">
        Chat with PDFs and ask general AI questions naturally.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------
# SESSION STATE
# --------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# --------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------
# CHAT INPUT
# --------------------------------

prompt = st.chat_input(
    "Message Enterprise AI Assistant..."
)


# --------------------------------
# HANDLE USER INPUT
# --------------------------------

if prompt:

    # Add user message
    st.session_state.messages.append({

        "role": "user",

        "content": prompt
    })


    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)


    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = requests.post(

                "http://127.0.0.1:8000/chat",

                json={
                    "question": prompt
                }
            )


            data = response.json()


            # Handle blocked content
            if data.get("blocked"):

                answer = (
                    f"❌ Request Blocked\n\n"
                    f"Reason: {data['reason']}"
                )

                sources = []

            else:

                answer = data.get(
                    "answer",
                    "No response generated."
                )

                sources = data.get(
                    "sources",
                    []
                )


            # --------------------------------
            # STREAMING EFFECT
            # --------------------------------

            message_placeholder = st.empty()

            full_response = ""


            for word in answer.split():

                full_response += word + " "

                time.sleep(0.02)

                message_placeholder.markdown(
                    full_response + "▌"
                )


            message_placeholder.markdown(
                full_response
            )


            # --------------------------------
            # SOURCES
            # --------------------------------

            if sources:

                with st.expander(
                    "📚 View Sources"
                ):

                    for i, source in enumerate(sources):

                        st.markdown(
                            f"### Source {i+1}"
                        )

                        st.write(
                            source["chunk"]
                        )

                        st.markdown("---")


    # Save assistant response
    st.session_state.messages.append({

        "role": "assistant",

        "content": answer
    })