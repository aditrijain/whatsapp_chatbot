from fastapi import FastAPI
from message import router as message_router
app = FastAPI()

app.include_router(message_router)
@app.get("/")
async def index():
    return {"msg": "running..."}