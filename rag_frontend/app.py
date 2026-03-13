import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="AI Document Chat", layout="wide")

st.title("📄 AI Document Chat")
st.write("Upload a PDF and ask questions about it.")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# PDF Upload
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:

    files = {"file": uploaded_file}

    res = requests.post(f"{API_URL}/upload/", files=files)

    if res.status_code == 200:
        st.success("PDF uploaded and indexed successfully")
    else:
        st.error("Upload failed")


# Chat UI
st.subheader("Ask Questions")

question = st.chat_input("Ask something about the document...")

if question:

    # Save user message
    st.session_state.messages.append({"role": "user", "content": question})

    response = requests.post(
        f"{API_URL}/ask/",
        json={"question": question}
    )

    answer = response.json()["answer"]

    st.session_state.messages.append({"role": "assistant", "content": answer})


# Display chat history
for msg in st.session_state.messages:

    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])

    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])