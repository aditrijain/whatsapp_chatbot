from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from decouple import config
from datetime import datetime
import os


# Get Database URL from environment or construct from components
DATABASE_URL = os.getenv("DATABASE_URL", None)
if DATABASE_URL is None:
    # Local development fallback
    url = URL.create(
        drivername="postgresql",
        username=config("DB_USER"),
        password=config("DB_PASSWORD"),
        host="db",  # This should be 'db' in Docker and 'localhost' for local dev
        database="mydb",
        port=5432
    )
else:
    # Production (Render) environment
    url = DATABASE_URL

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)
    message = Column(String)
    image_url = Column(String, nullable=True)
    response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)