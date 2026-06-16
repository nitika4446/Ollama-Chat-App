# app.py
# ChatGPT-like Application using Ollama + Python + Streamlit

import streamlit as st
import requests
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ollama Chat App",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}
.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🤖 AI Chat Application using Ollama")
st.write("Built with Python + Streamlit + Ollama")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙ Settings")

model_name = st.sidebar.selectbox(
    "Choose Ollama Model",
    ["llama3", "mistral", "gemma", "phi3"]
)

temperature = st.sidebar.slider(
    "Temperature",
    0.0,
    1.0,
    0.7
)

max_tokens = st.sidebar.slider(
    "Max Tokens",
    50,
    1000,
    300
)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- USER INPUT ----------------
prompt = st.chat_input("Type your message here...")

# ---------------- OLLAMA FUNCTION ----------------
def get_ollama_response(prompt, model):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["response"]
    else:
        return f"Error: {response.status_code}"

# ---------------- CHAT FLOW ----------------
if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = get_ollama_response(prompt, model_name)

            st.markdown(response)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# ---------------- CLEAR CHAT ----------------
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()






