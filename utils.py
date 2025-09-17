# Standard library import
import logging

# Third-party imports
from twilio.rest import Client
from decouple import config
import base64
from models import SessionLocal

account_sid = config("TWILIO_ACCOUNT_SID")
auth_token = config("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = config('TWILIO_NUMBER')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sending message logic through Twilio Messaging API
def send_message(to_number, body_text):
    try:
        # Split message if it's longer than Twilio's limit
        MAX_LENGTH = 1500  # Leave some room for safety
        messages = [body_text[i:i+MAX_LENGTH] for i in range(0, len(body_text), MAX_LENGTH)]
        
        for i, msg_part in enumerate(messages, 1):
            # Add part number if message is split
            if len(messages) > 1:
                msg_part = f"({i}/{len(messages)}) {msg_part}"
            
            message = client.messages.create(
                from_=f"whatsapp:{twilio_number}",
                body=msg_part,
                to=f"whatsapp:{to_number}"
            )
            logger.info(f"Message part {i}/{len(messages)} sent to {to_number}")
            
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")
# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
    
