import os
import requests
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Read the OpenRouter API key from .env
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_code_explanation(code):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",  # required by OpenRouter
    }
    data = {
        "model": "mistralai/mistral-small-3.2-24b-instruct-2506:free",
        "messages": [
            {"role": "system", "content": "You are a helpful programming assistant. Explain code in simple terms."},
            {"role": "user", "content": f"Explain this Python code:\n\n{code}"}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # Print raw response in case of error
    if response.status_code != 200:
        return f"❌ API Error: {response.status_code}\n{response.text}"

    try:
        return response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        return f"⚠️ Unexpected API response:\n{response.text}"

# ----------- Main Execution Flow ------------

if __name__ == "__main__":
    print("🔎 Enter your Python code (end with Enter + Ctrl+Z on Windows / Ctrl+D on Mac/Linux):")
    user_code = ""
    try:
        while True:
            line = input()
            user_code += line + "\n"
    except EOFError:
        pass

    print("\n📘 GPT Explanation:\n")
    print(get_code_explanation(user_code))
