# ai_agent/responder.py

import requests
import os
import logging

HUGGINGFACE_API_TOKEN = os.getenv("HF_API_TOKEN")  # Keep this in your .env file
# API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"

def generate_response(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "HuggingFaceH4/zephyr-7b-beta",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an election campaign assistant helping voters understand a candidate's policies. "
                    "Respond to WhatsApp queries concisely (under 300 characters) using only factual info shared "
                    "in context. Do not make up answers or change the candidate's views."
                )
            },
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        logging.info("Hugging Face response received successfully.")

        if "choices" not in result or not result["choices"]:
            logging.error("Unexpected HF API response format.")
            return "I'm having trouble understanding that right now."

        ai_response = result["choices"][0]["message"]["content"]

          # 🛡️ Optional: Filter out poetic/fantasy content
        if any(keyword in ai_response.lower() for keyword in [
            "poem", "poetry", "once upon", "muse", "verse", "stars", "fantasy", "fiction", "rhymes"
        ]):
            return "Sorry, please ask about employment, healthcare, or government schemes."

        return ai_response.strip()[:1024]
    
    except Exception as e:
        logging.error(f"Hugging Face API error: {e}")
        if 'response' in locals() and response is not None:
            logging.error(f"Details: {response.text}")
        return "AI model error. Please try again later."
    #     return response.json()["choices"][0]["message"]["content"]
    # except Exception as e:
    #     if response is not None:
    #         return f"Error: {e}\nDetails: {response.text}"
    #     print('Exception occured:',e)
    #     return f"Error talking to AI model: {e}"