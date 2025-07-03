# ai_agent/responder.py

import requests
import os

HUGGINGFACE_API_TOKEN = os.getenv("HF_API_TOKEN")  # Keep this in your .env file
# API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"

def generate_response(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "HuggingFaceH4/zephyr-7b-alpha",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant who answers election policy questions. Avoid medical or irrelevant content."
                )
            },
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        if response is not None:
            return f"Error: {e}\nDetails: {response.text}"
        print('Exception occured:',e)
        return f"Error talking to AI model: {e}"