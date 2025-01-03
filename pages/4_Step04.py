import streamlit as st
from openai import OpenAI
from rag import QA_MODEL, streaming_question_answering, get_similar_context
from Utils import markdown_creator, chatbot_info


st.title("Simple RAG using Streaming")

# content
markdown_creator(
    *[
        "Use of RAG framework for question answering.",
        "Hands on with Lnagchain and pinecone.",
        "Streaming the answer."
    ]
)

chatbot_info()

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
        pinecone_context = get_similar_context(prompt)
        response = st.write_stream(streaming_question_answering(prompt, pinecone_context))
    st.session_state.messages.append({"role": "assistant", "content": response})