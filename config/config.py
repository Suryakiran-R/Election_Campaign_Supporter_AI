import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")