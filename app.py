import os
from flask import Flask, request
from flask import Response
from twilio.twiml.messaging_response import MessagingResponse
from services.db import save_message
from ai_agent.ai_agent import generate_ai_response  # Import your AI responder
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

import sys

# Set up logging to both console and optional file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)                # Console (Render dashboard)
        # logging.FileHandler("logs/messages.log")          # Optional: Local file logging
    ]
)
# # Set up logging
# logging.basicConfig(filename='logs/messages.log', level=logging.INFO)

@app.route('/')
def index():
    return 'Server is running!'

@app.route('/whatsapp-webhook', methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')

    logging.info(f"Message from {sender}: {incoming_msg}")

    # Save to DB
    save_message({
        "sender": sender,
        "message": incoming_msg
    })

    # Get AI-based response
    try:
        response = generate_ai_response(incoming_msg)

         # Trim response to avoid WhatsApp truncation (max ~1600 chars safe)
        MAX_WHATSAPP_LENGTH = 1500
        if len(response) > MAX_WHATSAPP_LENGTH:
            logging.warning(f"Response too long ({len(response)} chars). Trimming.")
            response = response[:MAX_WHATSAPP_LENGTH - 50] + "... [truncated]"

        logging.info(f"AI response: {response}")

    except Exception as e:
        logging.error(f"Error generating AI response: {str(e)}")
        response = "Sorry, there was an error processing your request."

    # Reply to WhatsApp
    resp = MessagingResponse()
    resp.message(response)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')