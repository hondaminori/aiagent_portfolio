from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    query: str = Field(..., description="ユーザーの質問")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="チャットボットの回答")
