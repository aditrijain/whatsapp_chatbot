# Third-party imports
import os
from fastapi import APIRouter, Form, Depends, UploadFile, File
from decouple import config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from openai import OpenAI
from datetime import datetime
import requests
import subprocess
import whisper
# Internal imports
from models import Conversation
from utils import send_message, logger, get_db


router = APIRouter()
# Set up the OpenAI API client
openrouter_api_key = config("OPENROUTER_API_KEY")
whatsapp_number = config("TO_NUMBER")
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=openrouter_api_key,
)



UPLOAD_DIR = "./uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/message")
async def reply(
    Body: str = Form(default=""), 
    From: str = Form(...),
    MediaUrl0: str = Form(default=None),
    MediaContentType0: str = Form(default=None),
    NumMedia: str = Form(default="0"),  # Twilio sends this to indicate if media is present
    db: Session = Depends(get_db)
):
    # Log all incoming parameters
    logger.info(f"Received webhook with:")
    logger.info(f"Body: {Body}")
    logger.info(f"MediaUrl0: {MediaUrl0}")
    logger.info(f"MediaContentType0: {MediaContentType0}")
    logger.info(f"NumMedia: {NumMedia}")
    
    # Call the OpenAI API to generate text with GPT-3.5
    
    if MediaUrl0 and MediaContentType0.startswith("audio/"):
        audio_data = requests.get(MediaUrl0).content
        original_audio_path = os.path.join(UPLOAD_DIR, f"{datetime.now().timestamp()}.ogg")
        with open(original_audio_path, "wb") as f:
            f.write(audio_data)
        converted_audio_path = original_audio_path.replace(".ogg", ".mp3")
        subprocess.run([
            "ffmpeg", "-y", "-i", original_audio_path, converted_audio_path
        ], check=True)
        
        model = whisper.load_model("tiny.en")
        result = model.transcribe(converted_audio_path)
        print(result["text"])
        transcription_text= result["text"]
        Body+=" "+transcription_text
        logger.info(f"Transcription result: {transcription_text}")
        os.remove(original_audio_path)
        os.remove(converted_audio_path)

    last_conversations= (db.query(Conversation).order_by(Conversation.timestamp.desc()).limit(3).all()) #fetches last 3 conversations from db
    convo_history=""
    for convo in reversed(last_conversations):
        convo_history+=f"User:{convo.message}\nBot:{convo.response}\n"
    full_prompt=convo_history+f"User: {Body}\n"
    response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {
                "role": "developer",
                "content": "Talk like a friend." #Bot responds in a fun persona - change according to liking
                },
                {
                "role": "user",
                "content": [
                        {
                            "type": "text",
                            "text": full_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": MediaUrl0 if MediaContentType0 and MediaContentType0.startswith("image/") else None
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000  # Limit the response length
        )   
    chat_response= response.choices[0].message.content
    print(chat_response)
    # Store the conversation in the database
    try:
        conversation = Conversation(
            sender=From,
            message=Body,
            image_url=MediaUrl0,
            response=chat_response
            )
        db.add(conversation)
        db.commit()
        logger.info(f"Conversation #{conversation.id} stored in database")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error storing conversation in database: {e}")
    send_message(From, chat_response)
    return ""