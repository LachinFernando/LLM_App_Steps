import streamlit as st


IMAGE_ADDRESS = "https://upload.wikimedia.org/wikipedia/commons/1/1a/Irritable_bowel_syndrome.jpg"


def markdown_creator(*args) -> None:
    st.subheader("Learning Curve")
    for argument in args:
        st.markdown(f"- {argument}")
    st.subheader("ChatBot")


def chatbot_info():
    st.image(IMAGE_ADDRESS)
    st.markdown("- The Chatbot has knowledge about IBS Nutrition plans.")
    st.markdown("- The Chatbot can only answer relevant to IBS nutritions.")
