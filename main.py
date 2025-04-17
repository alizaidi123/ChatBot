import streamlit as st
from openai import OpenAI

# Page config: adds favicon, title bar name, and layout
st.set_page_config(page_title="Ali's Chat Bot 🤖", page_icon="💬", layout="centered")

# Custom CSS styling
st.markdown("""
    <style>
        .stApp {
            background-color: #f0f2f6;
        }
        .chat-message.user {
            background-color: #d1e7dd;
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }
        .chat-message.assistant {
            background-color: #f8d7da;
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }
        .stChatMessage {
            padding-bottom: 1rem;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Title with emoji
st.title("💬 Ali's Chat Bot")

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session state setup
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"**{message['role'].capitalize()}**: {message['content']}")

# Chat input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"**You**: {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
