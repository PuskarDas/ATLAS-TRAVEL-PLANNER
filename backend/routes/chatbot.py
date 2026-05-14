"""Chatbot routes."""

from datetime import datetime

from database.store import store
from fastapi import APIRouter, Depends
from models.schemas import ChatMessage
from services.nlp_service import NLPService
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/api/chat", tags=["chatbot"])
service = NLPService()


@router.post("/message")
async def message(payload: ChatMessage, current_user: dict = Depends(get_current_user)):
    result = service.process_message(payload.message)
    entry = {
        **result,
        "user_id": payload.user_id,
        "trip_id": payload.trip_id,
        "timestamp": datetime.utcnow(),
    }
    store.chat_history.setdefault(payload.trip_id, []).append(entry)
    return entry


@router.get("/history/{trip_id}")
async def history(trip_id: int, current_user: dict = Depends(get_current_user)):
    messages = store.chat_history.get(trip_id, [])
    return {"messages": messages, "total_count": len(messages)}
