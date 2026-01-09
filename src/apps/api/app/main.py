from __future__ import annotations

import logging
from fastapi import FastAPI
from common.bootstrap import init_app
from apps.api.app.deps import init_service
from apps.api.app.routers.chat import router as chat_router

init_app("api")
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Chat API")

@app.on_event("startup")
def on_startup() -> None:
    init_service()
    logger.info("API が起動しました")

app.include_router(chat_router)

@app.get("/health")
def health():
    logger.info("ヘルスチェック")
    return {"OK": True}
