from fastapi import FastAPI

from backend.api.chat_api import router as chat_router
from backend.api.document_api import router as document_router

app = FastAPI(title="Personal AI Assistant")

app.include_router(chat_router)
app.include_router(document_router)


@app.get("/")
def home():
    return {"message": "Personal AI Assistant API running"}