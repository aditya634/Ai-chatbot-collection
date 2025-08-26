import streamlit as st
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b-instruct"  # Updated to match your installed model

SYSTEM_PROMPT = (
    "You are a knowledgeable and respectful chatbot .")

st.set_page_config(page_title="Chatbot", page_icon="🕉️")
st.markdown(
    "<h1 style='text-align: center; color: #8B0000;'>🕉️ Chatbot 🕉️</h1>",
    unsafe_allow_html=True,
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

def get_ollama_response(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{SYSTEM_PROMPT}\nUser: {prompt}\nBot:",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"].strip()

def send_message():
    user_input = st.session_state.user_input
    if user_input.strip():
        bot_response = get_ollama_response(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_response))
        # Set flag to clear input on next render
        st.session_state.clear_input = True

def on_input_change():
    # This function is called when Enter is pressed in the input field
    user_input = st.session_state.user_input
    if user_input.strip():
        send_message()

# Chat display area
chat_placeholder = st.container()
with chat_placeholder:
    st.markdown(
        """
        <style>
        .user-bubble {
            background-color: #e6f7ff;
            color: #005580;
            padding: 10px 15px;
            border-radius: 15px;
            margin-bottom: 8px;
            margin-left: 40px;
            text-align: right;
        }
        .bot-bubble {
            background-color: #fff4e6;
            color: #8B0000;
            padding: 10px 15px;
            border-radius: 15px;
            margin-bottom: 8px;
            margin-right: 40px;
            text-align: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"<div class='user-bubble'><b>🧑‍💻 You:</b> {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'><b>🕉️ Bot:</b> {message}</div>", unsafe_allow_html=True)

st.markdown("---")
col1, col2 = st.columns([5, 1])

# Clear input if flag is set
if st.session_state.clear_input:
    st.session_state.user_input = ""
    st.session_state.clear_input = False

with col1:
    user_input = st.text_input(
        "Type your message...",
        key="user_input",
        label_visibility="collapsed",
        on_change=on_input_change
    )
with col2:
    if st.button("Send", use_container_width=True):
        if user_input.strip():
            send_message()
            st.rerun()