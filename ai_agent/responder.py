# ai_agent/responder.py

import requests
import os

HUGGINGFACE_API_TOKEN = os.getenv("HF_API_TOKEN")  # Keep this in your .env file
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

def query_huggingface(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7, "max_new_tokens": 300}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            generated = response.json()
            return generated[0]["generated_text"]
        else:
            return f"Error from Hugging Face API: {response.status_code}, {response.text}"
    except requests.exceptions.Timeout:
        return "⚠️ The AI model took too long to respond. Please try again in a few moments."
