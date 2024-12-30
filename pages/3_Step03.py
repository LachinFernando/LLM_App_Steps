import streamlit as st
from openai import OpenAI
from rag import QA_MODEL, generate_answer, get_similar_context


def markdown_creator(*args) -> None:
    for argument in args:
        st.markdown(f"- {argument}")
    st.subheader("ChatBot")


st.title("Simple RAG")

# content
markdown_creator(
    *[
        "In here chatbot uses RAG framework to answer the user question.",
        "The chatbot waits until the whole answer is generated.",
        "No Chat History.",
    ]
)

# set openai key
client = OpenAI(api_key= st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = QA_MODEL

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
        response = generate_answer(prompt)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})