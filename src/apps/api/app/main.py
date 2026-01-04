from fastapi import FastAPI
from apps.api.app.deps import init_service
from apps.api.app.routers.chat import router as chat_router

app = FastAPI(title="RAG Chat API")

@app.on_event("startup")
def on_startup():
    # 起動時に1回だけ service を初期化（load_vectorstoreが毎回走らない）
    init_service()

app.include_router(chat_router)
