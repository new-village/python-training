""" app.py
"""
import os
import streamlit as st
from langchain.llms import OpenAI

apikey = os.environ['OPENAI_API_KEY']

st.title("Welcome to GPT with LangChain")
prompt = st.text_input('Plug In your prompt here')
