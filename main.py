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
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": "You are a highly intelligent and helpful AI assistant specializing in software development. You can provide detailed explanations, solve complex problems, and write complete, functional code in various languages and frameworks, including Python, Streamlit, Next.js, and database interactions. Always strive for clear, efficient, and well-commented code. If asked for code, provide the full, runnable script."})


for message in st.session_state.messages:
    if message["role"] != "system": 
        with st.chat_message(message["role"]):
            display_role = "You" if message["role"] == "user" else "Assistant"
            st.markdown(f"**{display_role}**: {message['content']}")


# Chat input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(f"**You**: {prompt}")

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages # All messages are sent to API
                ],
                stream=True,
            )
            full_response = ""

            for chunk in stream:
                full_response += (chunk.choices[0].delta.content or "")
                st.markdown(full_response + "▌") # Blinking cursor while typing
            st.markdown(full_response) # Final response

    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
