# ai_agent/responder.py

import os
import requests
import logging

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_response(user_message: str) -> str:
    logging.info(f"Generating AI response for: {user_message}")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "ElectionSupportBot",
        "HTTP-Referer": "https://your-domain.com"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an election campaign assistant bot. "
                    "Answer the user's question clearly and briefly (max 300 characters). "
                    "Do NOT make up information. Focus only on candidate policies."
                )
            },
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        safe = reply.strip()[:1000] or "I’m here! How can I help with campaign questions?"
        logging.info(f"AI response: {safe}")
        return safe
    except Exception as e:
        logging.error(f"OpenRouter error: {e}")
        return "Sorry, I'm facing technical issues. Please try again later."
