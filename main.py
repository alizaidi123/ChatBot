import  streamlit as stl
from openai import OpenAI

stl.title("Ali's Chat Bot")

client = OpenAI(api_key=stl.secrets["OPENAI_API_KEY"])

if "openai_model" not in stl.session_state:
    stl.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in stl.session_state:
    stl.session_state.messages = []

for message in stl.session_state.messages:
    with stl.chat_message(message["role"]):
        stl.markdown(message["content"])

if prompt := stl.chat_input("What is up?"):
    stl.session_state.messages.append({"role": "user", "content": prompt})
    with stl.chat_message("user"):
        stl.markdown(prompt)
    with stl.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=stl.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in stl.session_state.messages
            ],
            stream=True,
        )
        response = stl.write_stream(stream)
    stl.session_state.messages.append({"role": "assistant", "content": response})

