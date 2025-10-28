from sqlmodel import select
from app.db import get_session
from app.models import Conversation, Message
from typing import List, Optional

def get_or_create_conversation(session_id: str) -> Conversation:
    with get_session() as s:
        conv = s.exec(select(Conversation).where(Conversation.session_id == session_id)).first()
        if conv:
            return conv
        conv = Conversation(session_id=session_id)
        s.add(conv)
        s.commit()
        s.refresh(conv)
        return conv

def add_message(conversation_id: int, sender: str, text: str) -> Message:
    with get_session() as s:
        msg = Message(conversation_id=conversation_id, sender=sender, text=text)
        s.add(msg)
        s.commit()
        s.refresh(msg)
        return msg

def get_history(session_id: str, limit: Optional[int] = 100) -> List[Message]:
    with get_session() as s:
        conv = s.exec(select(Conversation).where(Conversation.session_id == session_id)).first()
        if not conv:
            return []
        msgs = s.exec(select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at)).all()
        return msgs
