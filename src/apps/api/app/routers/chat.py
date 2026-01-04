from fastapi import APIRouter, Depends
from apps.api.app.schemas import ChatRequest, ChatResponse
from apps.api.app.deps import get_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, service=Depends(get_service)):
    answer = service.ask(req.query)
    return ChatResponse(answer=answer)
