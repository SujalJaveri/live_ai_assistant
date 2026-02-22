import streamlit as st
import requests
import json
from duckduckgo_search import DDGS

MEMORY_FILE = "memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def web_search(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        text = ""
        for r in results:
            text += r["body"] + "\n"
        return text

def ask_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

st.title("🤖 Live AI Assistant")

memory = load_memory()

user_input = st.text_input("Ask something:")

if st.button("Ask") and user_input:
    search_data = web_search(user_input)

    full_prompt = f"""
Use this internet data if useful:

{search_data}

Question: {user_input}
"""

    answer = ask_llm(full_prompt)

    memory.append({"user": user_input, "assistant": answer})
    save_memory(memory)

    st.write("### Answer:")
    st.write(answer)