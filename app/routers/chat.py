from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app import crud
from app.services import llm

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    session_id: str
    message: str
    topic: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    # create/get conversation
    conv = crud.get_or_create_conversation(req.session_id)
    # persist user message
    crud.add_message(conv.id, "user", req.message)

    # prepare message history for llm (simple)
    messages = []
    history = crud.get_history(req.session_id)
    for m in history:
        messages.append({"role": m.sender, "content": m.text})

    # call LLM service
    reply = await llm.generate_reply(messages=messages, user_message=req.message, topic=req.topic)

    # persist bot reply
    crud.add_message(conv.id, "bot", reply)
    return {"reply": reply}
