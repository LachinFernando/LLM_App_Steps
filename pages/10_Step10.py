from openai import OpenAI
import streamlit as st
from PIL import Image
from image_graph import graph_streamer
from Utils import markdown_creator, chatbot_info


IMAGE_NAME = "uploaded_image.png"


st.title("RAG Based Image Graph with Streaming")

# content
markdown_creator(
    *[
        "Use of images with RAG framework to get LLM response.",
        "Hands on with Langchain with structured outputs.",
        "Hands on with Langgraph with conditional graph.",
        "Streaming the output."
        
    ]
)

chatbot_info()

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # open the image
    image = Image.open(uploaded_file)
    
    # display the image
    st.header("Uploaded Image")
    st.image(image, caption='Uploaded Image.', use_container_width=True)
    
    # save the image as a PNG file
    image.save(IMAGE_NAME)

    # analyse the image
    with st.spinner("Generating Information......"):
        info = st.write_stream(graph_streamer(IMAGE_NAME))
        st.toast('Information Generation Successful!', icon='✅')

    if not info:
        st.error("Cannot Interpret the Image", icon = "❌")
        st.stop()