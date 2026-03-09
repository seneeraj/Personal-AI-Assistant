from fastapi import APIRouter
from pydantic import BaseModel

from backend.orchestrator.assistant_orchestrator import run_assistant

# Add API prefix
router = APIRouter(prefix="/api")


class ChatRequest(BaseModel):
    message: str
    document: str | None = None


@router.post("/chat")
async def chat_api(request: ChatRequest):

    response, sources = run_assistant(
        request.message,
        request.document
    )

    return {
        "status": "success",
        "response": response,
        "sources": sources if sources else []
    }