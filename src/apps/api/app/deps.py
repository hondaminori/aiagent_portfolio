import os
from dotenv import load_dotenv
from common.paths import ENV_PATH

from rag_core.query.service import create_service_from_env

_service = None  # module-level singleton

def init_service() -> None:
    """
    アプリ起動時に1回だけ呼ぶ想定。
    .env を読み込み、RAGService を初期化して保持する。
    """
    global _service

    load_dotenv(ENV_PATH)

    api_key = os.getenv("OPENAI_API_KEY")
    embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
    chat_model_name = os.getenv("CHAT_MODEL_NAME")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY が見つかりません (.env を確認してください)")
    if not embedding_model_name:
        raise RuntimeError("EMBEDDING_MODEL_NAME が見つかりません (.env を確認してください)")
    if not chat_model_name:
        raise RuntimeError("CHAT_MODEL_NAME が見つかりません (.env を確認してください)")

    # collection_name や k は必要なら環境変数化してもOK
    _service = create_service_from_env(
        api_key=api_key,
        embedding_model_name=embedding_model_name,
        chat_model_name=chat_model_name,
        collection_name=os.getenv("COLLECTION_NAME", "WorkRules"),
        k=int(os.getenv("TOP_K", "3")),
        search_type=os.getenv("SEARCH_TYPE", "similarity"),
    )

def get_service():
    """
    ルーターから呼ばれる。初期化済み service を返す。
    """
    if _service is None:
        raise RuntimeError("Service is not initialized. init_service() が呼ばれていません。")
    return _service
