from sqlalchemy.orm import Session
from models import Conversation
from models import SessionLocal

db = SessionLocal()
conversations = db.query(Conversation).order_by(Conversation.timestamp.desc()).all()

for convo in conversations:
    print(f"[{convo.timestamp}] {convo.sender}: {convo.message} → {convo.response}")
