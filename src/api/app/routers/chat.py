from fastapi import APIRouter, Depends
from api.app.schemas import ChatRequest, ChatResponse
from api.app.deps import get_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, service=Depends(get_service)):
    response_dict = service.ask(req.query)
    return ChatResponse(answer=response_dict["answer"])
