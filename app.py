import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load the API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Function to call OpenRouter
def explain_code(code_snippet, mode="Explain"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",  # required for OpenRouter
    }
    prompt_map = {
        "Explain": f"Explain this Python code in plain English:\n{code_snippet}",
        "Refactor": f"Refactor this Python code to make it cleaner and more efficient:\n{code_snippet}",
        "Debug": f"Find and explain bugs or issues in this Python code:\n{code_snippet}"
    }
    data = {
        "model": "mistralai/mistral-small-3.2-24b-instruct-2506:free",
        "messages": [
            {"role": "system", "content": "You are a helpful programming assistant."},
            {"role": "user", "content": prompt_map.get(mode, prompt_map['Explain'])}
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        try:
            return res.json()["choices"][0]["message"]["content"]
        except:
            return "⚠️ Unexpected response format."
    else:
        return f"❌ Error {res.status_code}: {res.text}"

# Streamlit UI
st.set_page_config(page_title="Code Explainer", page_icon="💡")
st.title("💡 Code Explainer")
st.markdown("Paste your Python code below and get a plain-English explanation.")

#user_code = st.text_area("✍️ Your Python Code", height=250)
mode = st.radio("🛠️ What do you want to do?", ["Explain", "Refactor", "Debug"])
user_code = st.text_area("✍️ Your Python Code", height=250)

if st.button("🚀 Run"):
    if user_code.strip() == "":
        st.warning("Please enter some code.")
    else:
        with st.spinner("Thinking..."):
            result = explain_code(user_code, mode)
        st.markdown(f"### 📘 Result: {mode}")
        st.success(result)