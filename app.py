import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from services.db import save_message
import logging

app = Flask(__name__)

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

    # Reply placeholder
    resp = MessagingResponse()
    msg = resp.message("Thanks for your message! Our team will get back to you soon.")
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')