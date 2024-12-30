import streamlit as st
from openai import OpenAI


def markdown_creator(*args) -> None:
    for argument in args:
        st.markdown(f"- {argument}")
    st.subheader("ChatBot")


st.title("Simple API Call")

# content
markdown_creator(
    *[
        "In here chatbot is simply asking the user question from the LLM with the chat history.",
        "The chatbot waits until the whole answer is generated."
    ]
)


OPENAI_CHAT_MODEL = "gpt-4o-mini"

# set openai key
client = OpenAI(api_key= st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = OPENAI_CHAT_MODEL

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        answer = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=False,
        )
        response = answer.choices[0].message.content
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})