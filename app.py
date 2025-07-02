import os
from flask import Flask, request
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

# Set up logging
logging.basicConfig(filename='logs/messages.log', level=logging.INFO)

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
    except Exception as e:
        logging.error(f"Error generating AI response: {str(e)}")
        response = "Sorry, there was an error processing your request."

    # Reply to WhatsApp
    resp = MessagingResponse()
    msg = resp.message(response)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
