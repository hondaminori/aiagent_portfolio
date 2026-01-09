from __future__ import annotations

import logging
import os

from common.bootstrap import init_app
from rag_core.query.service import create_service_from_env
from common.config import SEARCH_KWARGS, SEARCH_TYPE

init_app("ragtest")

logger = logging.getLogger(__name__)

def main() -> None:
    service = create_service_from_env(
        api_key=os.getenv("OPENAI_API_KEY"),
        embedding_model_name=os.getenv("EMBEDDING_MODEL_NAME"),
        chat_model_name=os.getenv("CHAT_MODEL_NAME"),
        collection_name="WorkRules",
        k=SEARCH_KWARGS,
        search_type=SEARCH_TYPE
    )

    q = "時短について教えてください。"
    logger.info(f"query: {q}")
    ans = service.ask(q)
    logger.info("質問に返答しました")
    logger.info(f"回答: {ans}")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("ragtestが失敗しました")
        raise


# setup_logging("rag_app")

# logger.info("アプリを起動しました")

# service = create_service_from_env(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     embedding_model_name=os.getenv("EMBEDDING_MODEL_NAME"),
#     chat_model_name=os.getenv("CHAT_MODEL_NAME"),
#     collection_name="WorkRules",
#     k=SEARCH_KWARGS,
#     search_type=SEARCH_TYPE
# )

# print(service.ask("介護休暇について教えて"))

# logger.info("アプリを終了しました")