# WhatsApp Chatbot

A Python-based WhatsApp chatbot application that responds to messages using OpenAI.  
It is deployed using Docker and Render for 24/7 availability and ease of management.
Link to the demo video: [link](https://drive.google.com/file/d/1sWH4xsHP0lvu4OvMvVZ0xXgS408cuP_S/view?usp=sharing)

##  Features

- Responds to text and media messages (images and audio) via WhatsApp.
- Uses OpenAI API for intelligent responses.
- Handles audio transcription using OpenAI Whisper.
- Stores conversations in PostgreSQL.
- Fully dockerized for easy deployment.


##  Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- Docker & Docker Compose
- OpenAI API
- Twilio API

##  Setup

### 1. Clone the Repository

```bash
git clone https://github.com/aditrijain/whatsapp_chatbot.git
cd whatsapp_chatbot
```
### 2. Install requirements

```bash
pip install -r requirements.txt
```
### 3. Configure env variables
Set up a .env file in the project root with the following keys for local development:
```bash
DB_USER
DB_PASSWORD
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_NUMBER=+14155238886
TO_NUMBER
OPENROUTER_API_KEY
```
For deployment (e.g., on Render), use:
```bash
DATABASE_URL=<render_provided_db_url>
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_NUMBER
TO_NUMBER
OPENROUTER_API_KEY
```

### 4. Run Locally:
```bash
docker-compose up --build
```
### 5. Deployment (Already Deployed on Render):

The service is running continuously in the cloud.
Twilio webhooks call the Render URL directly. [Link](https://whatsapp-chatbot-final.onrender.com)

