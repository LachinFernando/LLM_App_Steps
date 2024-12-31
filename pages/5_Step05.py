from openai import OpenAI
import streamlit as st
from text_graph import graph_streamer, graph_answer_generator
from langchain_core.messages import AIMessage, HumanMessage
from Utils import markdown_creator, chatbot_info


IMAGE_ADDRESS = "https://upload.wikimedia.org/wikipedia/commons/1/1a/Irritable_bowel_syndrome.jpg"


st.title("Simple RAG Based Langgraph Chain")

# content
markdown_creator(
    *[
        "Use of RAG framework along with Langgraph for question answering.",
        "Hands on with Langgraph.",
    ]
)

chatbot_info()

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
        message_list = [HumanMessage(prompt)]
        response = graph_answer_generator(message_list)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})