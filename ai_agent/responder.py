import os
import requests
import logging

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Embed the manifesto directly in the system prompt
PARTY_MANIFESTO = """
Bharat Jan Shakti Party - 2024 Manifesto:
1. Employment: Create 2 crore jobs via manufacturing, start-ups, rural MNREGA boost.
2. Women: 33% reservation in Parliament/Assemblies. Expand self-help & financial support.
3. Education: Free quality education till Class 12, digital classrooms, teacher training.
4. Healthcare: Ayushman Bharat to cover OPD. Super-specialty hospital in every district.
5. Infrastructure: ₹5 lakh crore for rural roads, smart cities, clean water.
6. Environment: 40% renewable energy by 2030, river cleaning, tree plantation drives.
7. Governance: Tech-driven anti-corruption, citizens' charter for transparency.
"""

def generate_response(user_message: str) -> str:
    logging.info(f"Generating AI response for: {user_message}")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "ElectionSupportBot",
        "HTTP-Referer": "https://your-domain.com"
    }

    system_prompt = (
        "You are an election campaign assistant bot for the Bharat Jan Shakti Party. "
        "Only respond based on the party manifesto provided. Never invent facts. "
        "Keep replies under 300 characters.\n\n"
        f"{PARTY_MANIFESTO}"
    )

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": system_prompt},
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