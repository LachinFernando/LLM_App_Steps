from openai import OpenAI
import streamlit as st
from PIL import Image
from image_utils import image_description_generator_streamer
from Utils import markdown_creator, chatbot_info


IMAGE_NAME = "uploaded_image.png"


st.title("Image Based LLM Interaction with Streaming")

# content
markdown_creator(
    *[
        "Use of images to get LLM response.",
        "Hands on with Langchain with structured outputs.",
        "Streaming the output."
        
    ]
)

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
        image_info = st.write_stream(image_description_generator_streamer(IMAGE_NAME))
        st.toast('Information Generation Successful!', icon='✅')

    if not image_info:
        st.error("Cannot Interpret the Image", icon = "❌")
        st.stop()