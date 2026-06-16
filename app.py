import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
page_title="AI Chat Application",
page_icon="🤖",
layout="wide"
)

# ---------------- API KEY ----------------

try:
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
st.error(
"GEMINI_API_KEY not found. Add it in Streamlit Secrets."
)
st.stop()

# ---------------- MODEL ----------------

model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- TITLE ----------------

st.title("🤖 AI Chat Application")
st.write("Built with Python + Streamlit + Gemini")

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
st.session_state.messages = []

# ---------------- DISPLAY HISTORY ----------------

for msg in st.session_state.messages:
with st.chat_message(msg["role"]):
st.markdown(msg["content"])

# ---------------- USER INPUT ----------------

prompt = st.chat_input("Type your message here...")

if prompt:

```
st.session_state.messages.append(
    {
        "role": "user",
        "content": prompt
    }
)

with st.chat_message("user"):
    st.markdown(prompt)

with st.chat_message("assistant"):

    with st.spinner("Thinking..."):

        try:
            response = model.generate_content(prompt)

            answer = response.text

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:
            st.error(f"Error: {e}")
```

# ---------------- CLEAR CHAT ----------------

if st.sidebar.button("🗑 Clear Chat"):
st.session_state.messages = []
st.rerun()










