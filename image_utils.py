from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState
from typing import  Annotated
import operator
from pinecone import Pinecone
from openai import OpenAI
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

import base64
import os
import streamlit as st


IMAGE_INSTRUCTIONS = """You are an expert image analyser.

You are an expert generating descriptions based on given image.

When generating descriptions for images, follow these guidelines:

1. Use only the information provided in the image.

2. Provide the information as a paragraph.
"""


# set the openai model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class ImageDescription(BaseModel):
    description: str = Field(None, description = "Description of the image")


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def image_description_generator(image_local_path: str) -> str:
    image_data = encode_image(image_local_path)
    # set up the message
    message = HumanMessage(
        content=[
            {"type": "text", "text": IMAGE_INSTRUCTIONS},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
    # create a structured output
    structured_llm = llm.with_structured_output(ImageDescription)
    # invoke the llm to generatr an query
    invoke_image_query = structured_llm.invoke([message])

    return invoke_image_query.description


def image_description_generator_streamer(image_local_path: str) -> str:
    image_data = encode_image(image_local_path)
    # set up the message
    message = HumanMessage(
        content=[
            {"type": "text", "text": IMAGE_INSTRUCTIONS},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
    # create a structured output
    structured_llm = llm.with_structured_output(ImageDescription)
    # invoke the llm to generatr an query
    for chunk in structured_llm.stream([message]):
        if chunk.description:
            yield chunk.description

    