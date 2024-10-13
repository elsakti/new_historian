import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")

if not api_key or not model_name:
    st.error("API Key or Model Name missing from environment!")

class Static:
    def config():
        return st.set_page_config(
                page_title="GEMA HISTORIAN GPT",
                layout="centered",
                page_icon="🗺️",
            )
        
    def styling():
        return st.markdown("""
        <style>
            body {
                font-family: 'Arial', sans-serif;
                
            }
            .title {
                color: #FFFFFF;
                text-align: center;
                font-size: 3em;
                font-weight: bold;
                margin-bottom: 20px;
            }
            .subtitle {
                color: #007bff;
                text-align: center;
                margin-bottom: 40px;
            }
            .footer {
                text-align: center;
                font-size: 0.9em;
                color: #666;
                margin-top: 40px;
            }
            .stButton>button {
                background-color: #001f3f;
                color: white;
                font-size: 1.2em;
                padding: 10px 20px;
            }
            @media only screen and (max-width: 768px) {
                .title {
                    font-size: 2.5em;
                }
            }
        </style>
    """, unsafe_allow_html=True)
        
    def logo(image):
        return st.image(image, width=120)
         
    def title(text):
        return st.markdown(f'<h1 class="title">{text}</h1>', unsafe_allow_html=True)
    
    def load_api():
        return ChatOpenAI(
            model=model_name,
            temperature=0.2,
            api_key=api_key
        )        


