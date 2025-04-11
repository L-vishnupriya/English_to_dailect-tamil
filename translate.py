import streamlit as st
from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7, google_api_key=GOOGLE_API_KEY)

# Prompt template
prompt = PromptTemplate(
    input_variables=["dialect", "text"],
    template="""
You are a Tamil dialect translator. Translate the following English sentence into Tamil in the {dialect} dialect.

Only output the translated sentence. Do not provide any explanation or additional text.

English: {text}
"""
)

# Chain using pipe syntax (LangChain)
chain = prompt | llm

# Streamlit Page Config
st.set_page_config(page_title="Tamil Dialect Translator", page_icon="", layout="centered")

# Custom CSS for dark mode with white text
st.markdown("""
    <style>
        body, .main {
            background-color: #000000;
            color: white;
        }
        label, .stTextInput label, .stSelectbox label, .stMarkdown {
            color: white !important;
            font-weight: bold;
        }
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div {
            font-size: 16px;
            padding: 10px;
            background-color: #1e1e1e;
            color: white;
            border-radius: 6px;
            border: none;
        }
        .stButton>button {
            background-color: #444444;
            color: white;
            padding: 0.5em 2em;
            border-radius: 8px;
            font-size: 18px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #666666;
        }
        .translated-text-box {
            background-color: #1f1f1f;
            padding: 10px;
            border-radius: 10px;
            font-size: 18px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Custom White Title
st.markdown("<h1 style='color:white; text-align:center;'>English ➡️ Tamil Dialect Translator</h1>", unsafe_allow_html=True)

# Input Fields
text = st.text_input("Enter an English sentence:")
dialect = st.selectbox(
    "Select a Tamil dialect:",
    options=["Chennai", "Kanyakumari", "Coimbatore"]
)

# Translate Button
if st.button("Translate"):
    if text and dialect:
        with st.spinner("Translating..."):
            result = chain.invoke({
                "dialect": dialect,
                "text": text
            })
        st.success(f"Translated in {dialect} dialect:")
        st.markdown(f"""<div class='translated-text-box'>
            {result.content}
        </div>""", unsafe_allow_html=True)
    else:
        st.warning("Please fill in both the English sentence and select a dialect.")
